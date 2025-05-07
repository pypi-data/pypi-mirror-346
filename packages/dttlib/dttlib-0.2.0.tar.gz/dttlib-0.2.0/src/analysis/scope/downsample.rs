//! Downsample a time-domain trace to
//! a fixed number of points, the easier to draw with
//! Get the min and max for each point.


use std::collections::VecDeque;
use std::mem;
use std::sync::Arc;
use futures::future::FutureExt;
use gps_pip::{PipDuration, PipInstant};
use tokio::task::JoinHandle;
use pipeline_macros::box_async;
use pipelines::{PipeDataPrimitive, PipeResult, PipelineSubscriber};
use pipelines::pipe::Pipe1;
use user_messages::UserMsgProvider;
use crate::AccumulationStats;
use crate::analysis::types::time_domain_array::TimeDomainArray;

#[derive(Default)]
enum DownsampleMode<T>
where
    T: PipeDataPrimitive + Copy + PartialOrd
{
    Rough{factor: usize, join: JoinHandle<DownsampleCache<T>>},
    #[default]
    Full,
}

struct DownsampleAssessment {
    factor: usize,
    non_overlap_points: usize,
}

#[derive(Default)]
pub (crate) struct DownsampleCache<T>
where
    T: PipeDataPrimitive + Copy + PartialOrd
{
    min: VecDeque<T>,
    max: VecDeque<T>,
    n: VecDeque<usize>,
    factor: usize,
    /// the decimator is given some flexibility.
    /// the cache is allowed to range to two times target_size
    /// and won't enlarge unless less than half target_size
    target_size: usize,
    start_pip: PipInstant,
    accumulation_stats: AccumulationStats,
    rate_hz: f64,
    mode: DownsampleMode<T>,
}

impl <T>  DownsampleCache<T>
where
    T: PipeDataPrimitive + Copy + Default + PartialOrd
{
    fn new(target_size: usize) -> Self {
        Self {
            min: VecDeque::with_capacity(3*target_size),
            max: VecDeque::with_capacity(3*target_size),
            n: VecDeque::with_capacity(3*target_size),
            factor: 0,
            target_size,
            start_pip: PipInstant::gpst_epoch(),
            rate_hz: 0.0,
            accumulation_stats: AccumulationStats::default(),
            mode: DownsampleMode::Full,
        }
    }

    fn len(&self) -> usize {
        self.min.len()
    }

    fn assess_update(&self, input: &TimeDomainArray<T>) -> DownsampleAssessment {
        let suggested_factor = if input.len() < self.target_size {
            return DownsampleAssessment { factor: 1, non_overlap_points: 0 };
        } else if input.len() % self.target_size == 0 {
            input.len() / self.target_size
        } else {
            input.len() / self.target_size + 1
        };

        let input_period = PipDuration::freq_hz_to_period(input.rate_hz);
        let orig_dec_period = self.factor * input_period;

        // if the factor is changed by at least 2x, or if the new data doesn't intersect the cache
        // clear the cache
        if (self.factor == 0)
            || (! (self.factor / 2 + 1 .. self.factor * 2).contains(&suggested_factor) )
            || (self.start_pip > input.end_gps_pip())
            || (self.start_pip + self.len()*orig_dec_period < input.start_gps_pip)
        {
            return DownsampleAssessment { factor: suggested_factor, non_overlap_points: input.len() };
        }

        let mut non_overlap_points = 0;

        let dec_end = self.start_pip + self.len() * orig_dec_period;

        if input.end_gps_pip() > dec_end {
            non_overlap_points += ((input.end_gps_pip() - dec_end)/input_period) as usize;
        }

        if input.start_gps_pip < self.start_pip {
            non_overlap_points += ((self.start_pip - input.start_gps_pip)/input_period) as usize;
        }

        DownsampleAssessment{factor: self.factor, non_overlap_points}
    }

    fn update(&mut self, input: &TimeDomainArray<T>) -> (TimeDomainArray<T>, TimeDomainArray<T>) {
        self.accumulation_stats = input.accumulation_stats;

        let input_period = PipDuration::freq_hz_to_period(input.rate_hz);


        let dec_period = self.factor * input_period;

        self.rate_hz = input.rate_hz / self.factor as f64;


        {
            // Find out of there is any leading component of the input
            // that's not in the cache, and how much
            let (lead_end, mut block_start_pip) = if self.len() == 0 {
                // if the cache is empty, we have to do the whole thing
                (Some(input.len() - 1), None)
            } else if input.start_gps_pip.snap_down_to_step(&dec_period) < self.start_pip {
                let max_time = self.start_pip + (self.factor - 1) * input_period;
                let block_start_pip = max_time.snap_down_to_step(&dec_period);
                (Some(input.gps_pip_to_index(max_time).min(input.len() - 1)), Some(block_start_pip))
            } else {
                (None, None)
            };

            // if there is any leading component, then decimate it.
            if let Some(e) = lead_end {
                let (mut new_min, mut new_max, mut new_n) = if let Some(start_pip) = block_start_pip {
                    let block_start_index = (start_pip - self.start_pip) / dec_period;
                    if block_start_index >= 0 {
                        (Some(self.min[block_start_index as usize]), Some(self.max[block_start_index as usize]), self.n[block_start_index as usize])
                    } else {
                        (None, None, 0)
                    }
                } else {
                    (None, None, 0)
                };

                for inp_index in (0..=e).rev() {
                    let inp_pip = input.index_to_gps_pip(inp_index);
                    let new_block_start_pip = inp_pip.snap_down_to_step(&dec_period);

                    if let Some(t) = &block_start_pip {
                        if &new_block_start_pip != t {
                            let block_start_index = ((t - self.start_pip) / dec_period) as usize;
                            if let Some(min) = new_min {
                                self.min[block_start_index] = min;
                            }
                            if let Some(max) = new_max {
                                self.max[block_start_index] = max;
                            }
                            self.n[block_start_index] = new_n;

                            // fill in any zero-size blocks that might have been pushed earlier
                            for i in block_start_index..self.min.len() {
                                if self.n[i] == 0 {
                                    self.min[i] = self.min[block_start_index];
                                    self.max[i] = self.max[block_start_index];
                                } else {
                                    break;
                                }
                            }

                            let new_block_start_index = (new_block_start_pip - self.start_pip) / dec_period;
                            if new_block_start_index >= 0 {
                                let nbsi = new_block_start_index as usize;
                                new_min = Some(self.min[nbsi]);
                                new_max = Some(self.max[nbsi]);
                                new_n = self.n[nbsi];
                            } else {
                                new_min = None;
                                new_max = None;
                                new_n = 0;
                            }
                        }
                    } else {
                        self.min.push_front(T::default());
                        self.max.push_front(T::default());
                        self.n.push_front(0);
                        self.start_pip = new_block_start_pip;
                    }

                    while new_block_start_pip < self.start_pip {
                        self.min.push_front(T::default());
                        self.max.push_front(T::default());
                        self.n.push_front(0);
                        self.start_pip -= dec_period;
                    }

                    block_start_pip = Some(new_block_start_pip);

                    new_min = match new_min {
                        None => Some(input.data[inp_index]),
                        Some(x) => if input.data[inp_index] < x { Some(input.data[inp_index]) } else { Some(x) }
                    };

                    new_max = match new_max {
                        None => Some(input.data[inp_index]),
                        Some(x) => if input.data[inp_index] > x { Some(input.data[inp_index]) } else { Some(x) }
                    };

                    new_n += 1;
                }

                // fill in the last block
                if new_n > 0 {
                    let block_start_index = ((block_start_pip.unwrap() - self.start_pip) / dec_period) as usize;
                    self.min[block_start_index] = new_min.unwrap();
                    self.max[block_start_index] = new_max.unwrap();
                    self.n[block_start_index] = new_n;
                }
            }
        }

        {
            // handle any extension of the input past the cache end
            let inp_last = input.len() - 1;
            let inp_last_pip = input.index_to_gps_pip(inp_last);

            let mut block_start_pip = self.start_pip + (self.len() - 1) * dec_period;
            let _last_block_start_index = self.len() - 1;


            if inp_last_pip.snap_down_to_step(&dec_period) > block_start_pip {
                let mut new_min = if self.len() > 0 {
                    Some(self.min[self.len() - 1])
                } else {
                    None
                };
                let mut new_max = if self.len() > 0 {
                    Some(self.max[self.len() - 1])
                } else {
                    None
                };
                let mut new_n = if self.len() > 0 {
                    self.n[self.len() - 1]
                } else {
                    0
                };

                let inp_start_pip = input.gps_pip_to_index(block_start_pip).max(0);
                //println!("[DOWNSAMPLE] begin block_start_n = {}", self.n[last_block_start_index]);

                for inp_index in inp_start_pip..=inp_last {
                    let inp_pip = input.index_to_gps_pip(inp_index);
                    let new_block_start_pip = inp_pip.snap_down_to_step(&dec_period);


                    if new_block_start_pip != block_start_pip {
                        let block_start_index = ((block_start_pip - self.start_pip) / dec_period) as usize;
                        self.min[block_start_index] = if let Some(min) = new_min {
                            min
                        } else if block_start_index > 0 {
                            self.min[block_start_index - 1]
                        } else {
                            T::default()
                        };

                        self.max[block_start_index] = if let Some(max) = new_max {
                            max
                        } else if block_start_index > 0 {
                            self.max[block_start_index - 1]
                        } else {
                            T::default()
                        };

                        self.n[block_start_index] = new_n;

                        let nbsi = ((new_block_start_pip - self.start_pip) / dec_period) as usize;
                        if nbsi < self.len() {
                            new_min = Some(self.min[nbsi]);
                            new_max = Some(self.max[nbsi]);
                            new_n = self.n[nbsi];
                        } else {
                            new_min = None;
                            new_max = None;
                            new_n = 0;
                        }
                    }


                    while new_block_start_pip >= self.start_pip + self.len() * dec_period {
                        self.min.push_back(T::default());
                        self.max.push_back(T::default());
                        self.n.push_back(0);
                    }

                    block_start_pip = new_block_start_pip;

                    new_min = match new_min {
                        None => Some(input.data[inp_index]),
                        Some(x) => if input.data[inp_index] < x { Some(input.data[inp_index]) } else { Some(x) }
                    };

                    new_max = match new_max {
                        None => Some(input.data[inp_index]),
                        Some(x) => if input.data[inp_index] > x { Some(input.data[inp_index]) } else { Some(x) }
                    };

                    new_n += 1;
                }


                if new_n > 0 {
                    let block_start_index = ((block_start_pip - self.start_pip) / dec_period) as usize;
                    //println!("[DOWNSAMPLE] fill in last block {}", block_start_index);
                    self.min[block_start_index] = new_min.unwrap();
                    self.max[block_start_index] = new_max.unwrap();
                    self.n[block_start_index] = new_n;
                }

                //println!("[DOWNSAMPLE] end block_start_n = {}, new_n = {}", self.n[last_block_start_index], new_n);
                //print!("[DOWNSAMPLE] min == max blocks out of {} ", self.len());

                // for i in 0..self.len() {
                //     if self.max[i] == self.min[i] {
                //         print!("[{}]={} ", i, self.n[i]);
                //     }
                // }
                // println!();
            }
        }

        // trim the cache to minimize its size

        let end_time = (input.end_gps_pip() - input_period).snap_down_to_step(&dec_period);
        let start_time = input.start_gps_pip.snap_down_to_step(&dec_period);

        let start_index = ((start_time - self.start_pip) / dec_period) as usize;
        let end_index = ((end_time - self.start_pip) / dec_period) as usize;

        if start_index > 0
        {
            self.min.drain(..start_index);
            self.max.drain(..start_index);
            self.n.drain(..start_index);
            self.start_pip += (start_index) * dec_period;
        }

        if end_index < self.min.len() - 1 {
            self.min.truncate(end_index+1);
            self.max.truncate(end_index+1);
            self.n.truncate(end_index+1);
        }

        //println!("downsampled from {} to {} points", input.len(), self.len());

        self.get_min_max()
    }


    fn update_rough(&mut self, input: &TimeDomainArray<T>) -> TimeDomainArray<T> {

        let factor= self.factor;

        let rate_hz = input.rate_hz / factor as f64;

        let new_size = input.len() / factor;
        let mut data = Vec::with_capacity(new_size);

        for out_index in 0..new_size {
            let in_index = out_index * factor;
            data.push(input.data[in_index]);
        }

        TimeDomainArray{
            start_gps_pip: input.start_gps_pip,
            rate_hz,
            data,
            accumulation_stats: input.accumulation_stats,
        }
    }

    fn get_min_max(&self) -> (TimeDomainArray<T>, TimeDomainArray<T>) {

        (
            TimeDomainArray {
                start_gps_pip: self.start_pip,
                rate_hz: self.rate_hz,
                data: self.min.clone().make_contiguous().to_vec(),
                accumulation_stats: self.accumulation_stats,
            }
            ,
            TimeDomainArray {
                start_gps_pip: self.start_pip,
                rate_hz: self.rate_hz,
                data: self.max.clone().make_contiguous().to_vec(),
                accumulation_stats: self.accumulation_stats,
            }
        )

    }

    fn almost_clone(&self) -> Self {
        Self {
            min: self.min.clone(),
            max: self.max.clone(),
            n: self.n.clone(),
            factor: self.factor,
            start_pip: self.start_pip,
            rate_hz: self.rate_hz,
            accumulation_stats: self.accumulation_stats,
            mode: DownsampleMode::Full,
            target_size: self.target_size,
        }
    }

    fn copy_from(&mut self, other: Self) {
        self.min = other.min;
        self.max = other.max;
        self.n = other.n;
        self.factor = other.factor;
        self.start_pip = other.start_pip;
        self.rate_hz = other.rate_hz;
        self.accumulation_stats = other.accumulation_stats;
        self.target_size = other.target_size;
        self.mode = DownsampleMode::Full;
    }


    fn clear(&mut self) {
        self.min.clear();
        self.max.clear();
        self.n.clear();
    }


    #[box_async]
    pub (crate) fn generate(rc: Box<dyn UserMsgProvider>, state: &mut Self,
                                  input: Arc<TimeDomainArray<T>>)
        -> PipeResult<(TimeDomainArray<T>, TimeDomainArray<T>)>
    {

        //println!("[DOWNSAMPLE] Start downsample" );
        let dm = mem::take(&mut state.mode);
        // check join if in rough
        if let DownsampleMode::Rough{factor, join} = dm {
            if join.is_finished() {
                match join.await {
                    Ok(dc) => {
                        //println!("[DOWNSAMPLE] joined background downsample");
                        rc.user_message_handle().clear_message("BadBackgroundDownsample");
                        state.copy_from(dc)
                    }
                    Err(e) => {
                        let msg = format!("Error while calculating downsample in the background: {}", e);
                        rc.user_message_handle().set_error("BadBackgroundDownsample", msg);
                        state.factor = 0;
                        state.mode = DownsampleMode::Full;
                    }
                };
            } else {
                state.mode = DownsampleMode::Rough {factor, join};
            }
        }

        let assessment = state.assess_update(input.as_ref());

        // check direct

        if assessment.factor == 1 {
            //println!("[DOWNSAMPLE] direct");
            state.factor = 1;
            state.mode = DownsampleMode::Full;
            return (input.as_ref().clone(), input.as_ref().clone()).into();
        }

        if assessment.factor != state.factor {
            //println!("[DOWNSAMPLE] new factor: {}", assessment.factor);
            state.factor = assessment.factor;
            state.clear();
        }

        // if let DownsampleMode::Full = state.mode {
        //     if assessment.non_overlap_points > 100000 {
        //         //println!("[DOWNSAMPLE] large non overlap.  Running in background.");
        //         // do it in the background
        //         let mut dc = state.almost_clone();
        //         let inpclone = input.clone();
        //         let join = tokio::task::spawn_blocking(move || {
        //             dc.update(inpclone.as_ref());
        //             dc
        //         });
        //         state.mode = DownsampleMode::Rough{factor: state.factor, join};
        //     }
        // }

        match  &state.mode {
            DownsampleMode::Rough{factor, join:_} => {
                if *factor != state.factor {
                    //println!("[DOWNSAMPLE] background update stale.  Creating a new one.");
                    // if factor has changed, start a new background udpate
                    let mut dc = state.almost_clone();
                    let inpclone = input.clone();
                    let join = tokio::task::spawn_blocking(move || {
                        dc.update(inpclone.as_ref());
                        dc
                    });
                    state.mode = DownsampleMode::Rough { factor: state.factor, join };
                }
                //println!("[DOWNSAMPLE] rough update");
                let result = state.update_rough(input.as_ref());
                (result.clone(), result).into()
            },
            DownsampleMode::Full => {

                // let result = state.update_rough(input.as_ref());
                // println!("[DOWNSAMPLE] rough update: {}", result.len());
                // (result.clone(), result).into()
                //println!("[DOWNSAMPLE] full update");
                tokio::task::block_in_place(|| { state.update(input.as_ref())}).into()
            }
        }


    }


    pub (crate) async fn create(rc: Box<dyn UserMsgProvider>, name: impl Into<String>,
                                   input: &PipelineSubscriber<TimeDomainArray<T>>)
                                   -> PipelineSubscriber<(TimeDomainArray<T>, TimeDomainArray<T>)>
    {
        let state = Self::new(4096);

        Pipe1::create(rc, name.into(), Self::generate, state, None, None, input).await
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::analysis::types::time_domain_array::TimeDomainArray;

    #[test]
    fn test_add_lead() {
        let mut dc = DownsampleCache::<f64>::new(4);
        let rate_hz = 100.0;
        let step_pip = PipDuration::freq_hz_to_period(rate_hz);
        let offset = 10;

        let t1 = TimeDomainArray{
            start_gps_pip: PipInstant::gpst_epoch() + step_pip * (offset + 5),
            rate_hz,
            data: vec![1.0; 20],
            accumulation_stats: AccumulationStats::default()
        };

        let t2 = TimeDomainArray{
            start_gps_pip: PipInstant::gpst_epoch() + step_pip * (offset),
            rate_hz,
            data: vec![2.0; 27],
            accumulation_stats: AccumulationStats::default()
        };

        let assess = dc.assess_update(&t1);
        dc.factor = assess.factor;

        dc.update(&t1);

        assert_eq!(dc.factor, 5);
        assert_eq!(dc.min.len(), 4);

        let assess2 = dc.assess_update(&t2);
        dc.factor = assess2.factor;
        dc.update(&t2);

        assert_eq!(dc.factor, 5);
        assert_eq!(dc.min.len(), 6);
        assert_eq!(dc.n[0], 5);
        assert_eq!(dc.min[0], 2.0);
        assert_eq!(dc.max[1], 2.0);
        assert_eq!(dc.min[1], 1.0);
    }
}



