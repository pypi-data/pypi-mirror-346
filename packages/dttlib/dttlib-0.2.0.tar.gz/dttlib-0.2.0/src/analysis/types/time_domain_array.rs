use std::fmt::{Display, Formatter};
use pipelines::{PipeData, PipeDataPrimitive};
use std::ops::{Add, Mul, Sub};
use std::sync::Arc;
use num_traits::FromPrimitive;
#[cfg(any(feature = "python-pipe", feature = "python"))]
use pyo3::{
    Bound, FromPyObject, PyAny, pyclass, PyResult, Python,
    types::{
        PyAnyMethods,
    },
    IntoPyObject, PyErr, Py,
    pymethods,
};
#[cfg(any(feature = "python-pipe", feature = "python"))]
use numpy::{
    array::PyArray,
};
use user_messages::{UserMsgProvider};
use crate::analysis::types::{Accumulation, AccumulationStats, MutableAccumulation, Scalar};
use crate::errors::DTTError;
use gps_pip::{PipDuration, PipInstant};
use nds_cache_rs::buffer::{Buffer, TimeSeries};
use pipelines::complex::{c128, c64};
use crate::analysis::types::math_traits::Sqrt;

/// use ts_tree_rs::time_series::TimeSeries;

/// # Fixed pitch data blocks

/// ## Time Domain array
#[derive(Clone, Debug)]
pub struct TimeDomainArray<T> {
    pub start_gps_pip: PipInstant,
    pub rate_hz: f64,
    pub data: Vec<T>,
    pub accumulation_stats: AccumulationStats
}

impl<T> Default for TimeDomainArray<T> {
    fn default() -> Self {
        Self {
            start_gps_pip: PipInstant::gpst_epoch(),
            rate_hz: 1.0,
            data: Vec::new(),
            accumulation_stats: AccumulationStats::default(),
        }
    }
}

/// Equality in time, not in value
impl<T> PartialEq<Self> for TimeDomainArray<T> {
    fn eq(&self, other: &Self) -> bool {
        self.start_gps_pip == other.start_gps_pip && self.rate_hz == other.rate_hz
    }
}

impl<T> Add<Arc<TimeDomainArray<T>>> for TimeDomainArray<T>
where
    T: Copy + Add<T, Output=T>
{
    type Output = Result<TimeDomainArray<T>, DTTError>;

    fn add(mut self, rhs: Arc<TimeDomainArray<T>>) -> Self::Output {
        if self.rate_hz != rhs.rate_hz {
            let msg = format!("Can't add time domain arrays.  Sample rates differ: ({}, {})",
                              self.rate_hz, rhs.rate_hz);
            return Err(DTTError::CalcError(msg))
        };
        if self.data.len() != rhs.data.len() {
            let msg = format!("Can't add time domain arrays.  Lengths differ: ({}, {})",
                              self.data.len(), rhs.data.len());
            return Err(DTTError::CalcError(msg))
        }
        for i in 0..self.data.len() {
            self.data[i] = self.data[i] + rhs.data[i]
        }
        Ok( self )
    }
}

impl<T> Add<Arc<TimeDomainArray<T>>> for &TimeDomainArray<T>
where
    T: Copy + Add<T, Output=T>
{
    type Output = Result<TimeDomainArray<T>, DTTError>;

    fn add(self: Self, rhs: Arc<TimeDomainArray<T>>) -> Self::Output {
        let sum: TimeDomainArray<T> = self.clone();
        sum + rhs
    }
}


impl<T> Mul<f64> for TimeDomainArray<T>
where
    T: Copy + Mul<f64, Output=T>
{
    type Output = TimeDomainArray<T>;

    fn mul(mut self, rhs: f64) -> Self::Output {
        for i in 0..self.data.len() {
            self.data[i] = self.data[i] * rhs
        }
        self
    }
}

impl<T> Eq for TimeDomainArray<T> {

}

impl <T: PipeDataPrimitive> PipeData for TimeDomainArray<T> {

}

impl <T> TimeDomainArray<T>
where
    T: Scalar,
{
    pub fn mean(&self) -> T {
        if self.data.len() == 0 {
            return T::default();
        }

        let mut mean = T::default();
        for element in &self.data {
            mean += *element;
        }

        let n = f64::from_usize(self.data.len()).unwrap_or(1.0);
        mean /= n.into();
        mean
    }
}

impl <T> TimeDomainArray<T> {
    pub fn len(&self) -> usize {
        self.data.len()
    }


 }

/// Convert a TimeSeries of type f32 to a TimeDomainArray of type f64
pub fn from_time_series_f32_to_f64<C>(value: TimeSeries<C,f32>) -> TimeDomainArray<f64> {
    let start_gps_pip = value.start();
    let rate_hz = value.period().period_to_freq_hz();
    let data_vec: Vec<_> = value.into();
    TimeDomainArray {
        start_gps_pip,
        rate_hz,
        data: data_vec.into_iter().map(|x| x as f64).collect(),
        accumulation_stats: AccumulationStats::default(),
    }
}

impl<C: Clone, T: Clone> From<TimeSeries<C, T>> for TimeDomainArray<T> {
    fn from(value: TimeSeries<C, T>) -> Self {
        Self {
            start_gps_pip: value.start(),
            rate_hz: value.period().period_to_freq_hz(),
            data: value.into(),
            accumulation_stats: AccumulationStats::default(),
        }
    }
}

impl TryFrom<Buffer> for TimeDomainArray<i8> {
    type Error = DTTError;

    fn try_from(value: Buffer) -> Result<Self, Self::Error> {
        match value {
            _ => {
                let msg = "Expected data buffer of type i8";
                Err(DTTError::MismatchedTypesError(msg.into()))
            }
        }
    }
}

impl TryFrom<Buffer> for TimeDomainArray<i16> {
    type Error = DTTError;

    fn try_from(value: Buffer) -> Result<Self, Self::Error> {
        match value {
            Buffer::Int16(t) => Ok(TimeDomainArray::<i16>::from(t)),
            _ => {
                let msg = "Expected data buffer of type i16";
                Err(DTTError::MismatchedTypesError(msg.into()))
            }
        }
    }
}

impl TryFrom<Buffer> for TimeDomainArray<i32> {
    type Error = DTTError;

    fn try_from(value: Buffer) -> Result<Self, Self::Error> {
        match value {
            Buffer::Int32(t) => Ok(TimeDomainArray::<i32>::from(t)),
            _ => {
                let msg = "Expected data buffer of type i32";
                Err(DTTError::MismatchedTypesError(msg.into()))
            }
        }
    }
}

impl TryFrom<Buffer> for TimeDomainArray<i64> {
    type Error = DTTError;

    fn try_from(value: Buffer) -> Result<Self, Self::Error> {
        match value {
            Buffer::Int64(t) => Ok(TimeDomainArray::<i64>::from(t)),
            _ => {
                let msg = "Expected data buffer of type i64";
                Err(DTTError::MismatchedTypesError(msg.into()))
            }
        }
    }
}

impl TryFrom<Buffer> for TimeDomainArray<f32> {
    type Error = DTTError;

    fn try_from(value: Buffer) -> Result<Self, Self::Error> {
        match value {
            Buffer::Float32(t) => Ok(TimeDomainArray::<f32>::from(t)),
            t => {
                let msg = format!("Expected data buffer of type f32, got {:?}", t);
                Err(DTTError::MismatchedTypesError(msg.into()))
            }
        }
    }
}

impl TryFrom<Buffer> for TimeDomainArray<f64> {
    type Error = DTTError;

    fn try_from(value: Buffer) -> Result<Self, Self::Error> {
        match value {
            Buffer::Float64(t) => Ok(TimeDomainArray::<f64>::from(t)),
            Buffer::Float32(t) => Ok(
                    from_time_series_f32_to_f64(t)
            ),
            _ => {
                let msg = "Expected data buffer of type f64";
                Err(DTTError::MismatchedTypesError(msg.into()))
            }
        }
    }
}

impl TryFrom<Buffer> for TimeDomainArray<c64> {
    type Error = DTTError;

    fn try_from(value: Buffer) -> Result<Self, Self::Error> {
        match value {
            Buffer::Complex32(t) => Ok(TimeDomainArray::<c64>::from(t)),
            _ => {
                let msg = "Expected data buffer of type c64";
                Err(DTTError::MismatchedTypesError(msg.into()))
            }
        }
    }
}

impl TryFrom<Buffer> for TimeDomainArray<u8> {
    type Error = DTTError;

    fn try_from(value: Buffer) -> Result<Self, Self::Error> {
        match value {
            _ => {
                let msg = "Expected data buffer of type u8";
                Err(DTTError::MismatchedTypesError(msg.into()))
            }
        }
    }
}

impl TryFrom<Buffer> for TimeDomainArray<u16> {
    type Error = DTTError;

    fn try_from(value: Buffer) -> Result<Self, Self::Error> {
        match value {
            _ => {
                let msg = "Expected data buffer of type u16";
                Err(DTTError::MismatchedTypesError(msg.into()))
            }
        }
    }
}

impl TryFrom<Buffer> for TimeDomainArray<u32> {
    type Error = DTTError;

    fn try_from(value: Buffer) -> Result<Self, Self::Error> {
        match value {
            Buffer::UInt32(t) => Ok(TimeDomainArray::<u32>::from(t)),
            _ => {
                let msg = "Expected data buffer of type u32";
                Err(DTTError::MismatchedTypesError(msg.into()))
            }
        }
    }
}

impl TryFrom<Buffer> for TimeDomainArray<u64> {
    type Error = DTTError;

    fn try_from(value: Buffer) -> Result<Self, Self::Error> {
        match value {
            _ => {
                let msg = "Expected data buffer of type u64";
                Err(DTTError::MismatchedTypesError(msg.into()))
            }
        }
    }
}

impl TryFrom<Buffer> for TimeDomainArray<c128> {
    type Error = DTTError;

    fn try_from(value: Buffer) -> Result<Self, Self::Error> {
        match value {
            _ => {
                let msg = "Data buffers of type c128 are not supported";
                Err(DTTError::MismatchedTypesError(msg.into()))
            }
        }
    }
}

impl TryFrom<Buffer> for TimeDomainArray<String> {
    type Error = DTTError;

    fn try_from(value: Buffer) -> Result<Self, Self::Error> {
        match value {
            _ => {
                let msg = "Data buffers of type String are not supported";
                Err(DTTError::MismatchedTypesError(msg.into()))
            }
        }
    }
}

impl <T: PipeData> TimeDomainArray<T>
{
    /// return the time of the first timestamp after the end of the time series
    /// equal to the start time of the following series if it is contiguous.
    pub fn end_gps_pip(&self) -> PipInstant {
        // assume rate is a power of two
        self.index_to_gps_pip(self.data.len())
    }

    /// return a copy of a subsection of the time series
    pub fn copy_from(&self, start: PipInstant, end: PipInstant) -> Self {
        let s = self.gps_pip_to_index(start);
        let e = self.gps_pip_to_index(end);

        let new_data = Vec::from_iter(self.data[s..e].iter().cloned());

        Self {
            start_gps_pip: start,
            rate_hz: self.rate_hz,
            data: new_data,
            accumulation_stats: self.accumulation_stats.clone(),
        }
    }

    /// snap a pip value to the nearest integer value of the step size of the array
    pub fn snap_to_step_pip(&self, raw_pip: PipDuration) -> PipDuration {
        let pip_per_cyc = PipDuration::freq_hz_to_period(self.rate_hz);
        raw_pip.snap_to_step(&pip_per_cyc)
    }

    /// snap a pip value to the nearest integer value of the step size of the array
    pub fn snap_to_step_pip_instant(&self, raw_pip: PipInstant) -> PipInstant {
        let pip_per_cyc = PipDuration::freq_hz_to_period(self.rate_hz);
        raw_pip.snap_to_step(&pip_per_cyc)
    }

    /// Trim the time series to start at the new value.
    pub fn trim_to(&mut self, rc: Box<dyn UserMsgProvider>, raw_new_start: PipInstant) -> Result<(), DTTError> {
        let new_start = self.snap_to_step_pip_instant(raw_new_start);
        if new_start < self.start_gps_pip {
            let msg = "Requested start time was earlier than saved data when trimming a time domain array";
            rc.user_message_handle().error(msg);
            return Err(DTTError::CalcError(msg.to_string()));
        }
        let s = self.gps_pip_to_index(new_start);
        if s >= self.data.len() {
            self.start_gps_pip = self.end_gps_pip();
            self.data.clear();
        } else {
            self.data.drain(0..s);
            self.start_gps_pip = new_start;
        }
        Ok(())
    }


    /// convert a gps time into an array index
    /// not guaranteed to be in bounds
    pub (crate) fn gps_pip_to_index(&self, t: PipInstant) -> usize {
        let span: PipDuration = t - self.start_gps_pip;
        let pip_per_cyc = PipDuration::freq_hz_to_period(self.rate_hz);
        (span / pip_per_cyc) as usize
    }

    pub (crate) fn index_to_gps_pip(&self, index: usize) -> PipInstant {
        let pip_per_cyc = PipDuration::freq_hz_to_period(self.rate_hz);
        self.start_gps_pip + (pip_per_cyc * u64::from_usize(index).unwrap_or(0))
    }

    pub fn time_step(&self) -> f64 {
        1.0 / self.rate_hz
    }

    /// align the start point to a multiple of the sample period
    pub fn align_start(mut self) -> Self {
        let step_pip = PipDuration::freq_hz_to_period(self.rate_hz);
        self.start_gps_pip = self.start_gps_pip.snap_to_step(&step_pip);
        self
    }

    /// Add self into data, filling in gaps and combining contiguous segemnts
    /// data is assumed to be in time order with no overlaps and will remain so
    /// return true if something has changed.
    /// will returned false if self is entirely contained within data already
    ///
    /// Does *not* check if the values in self match the values in data.  Only
    /// splices based on range of time.
    pub(crate) fn splice_into(self, data: &mut Vec<Self>) -> bool {
        let self_end_pip = self.end_gps_pip();

        if data.is_empty() || self.start_gps_pip > data.last().unwrap().end_gps_pip() {
            data.push(self);
            return true;
        }

        if self_end_pip < data[0].start_gps_pip {
            data.insert(0, self);
            return true;
        }

        let mut start_index = 0;
        let mut lo = 0;
        let mut hi = data.len();
        while lo + 1 < hi {
            let mid = (lo + hi) / 2;
            let mid_end = data[mid].end_gps_pip();
            if self.start_gps_pip <= mid_end {
                hi = mid;
            } else {
                lo = mid;
            }
        };

        if hi == data.len() || data[lo].end_gps_pip() >= self.start_gps_pip {
            start_index = lo;
        } else {
            start_index = hi;
        }

        // println!("start = {} end = {} start_index = {} start_si = {} end_si = {}",
        //     self.start_gps_pip.to_gpst_seconds(),
        //     self_end_pip.to_gpst_seconds(), 
        //          start_index,
        //     data[start_index].start_gps_pip.to_gpst_seconds(),
        //     data[start_index].end_gps_pip().to_gpst_seconds(),
        // );

        let mut look = self;
        let mut spliced = true;
        while start_index < data.len() {
            if look.end_gps_pip() < data[start_index].start_gps_pip {
                data.insert(start_index, look);
                return spliced;
            }
            let s = data.remove(start_index);
            (look, spliced) = look.union(s).unwrap();
        }
        data.push(look);
        spliced
    }


    /// return the time history that's the union of
    /// the two time histories.
    /// Time histories must overlap or be contiguous.  It's an error otherwise.
    /// Returns the union and a bool that is true iff
    /// union != other
    /// this bool is used to determine whether a splice_into() call results in any change
    fn union(mut self, mut other: Self) -> Result<(Self, bool), DTTError> {
        if self.end_gps_pip() < other.start_gps_pip && self.start_gps_pip < other.end_gps_pip() {
            let msg = "Cannot take union of time domain arrays that don't overlap or arent contiguous.".to_string();
            return Err(DTTError::CalcError(msg));
        }

        if self.start_gps_pip >= other.start_gps_pip && self.end_gps_pip() <= other.end_gps_pip() {
            return Ok((other, false));
        }

        if self.start_gps_pip <= other.start_gps_pip && self.end_gps_pip() >= other.end_gps_pip() {
            return Ok((self, true));
        }

        if self.start_gps_pip < other.start_gps_pip {
            let new_end = self.gps_pip_to_index(other.start_gps_pip);
            self.data.drain(new_end..);
            self.data.append(&mut other.data);
            return Ok((self, true));
        }

        let new_end = other.gps_pip_to_index(self.start_gps_pip);
        other.data.drain(new_end..);
        other.data.append(&mut self.data);
        Ok((other, true))
    }

    /// clone the meta data of an array, but put in a new data array
    fn clone_metadata<U: PipeData>(&self, data: Vec<U>) -> TimeDomainArray<U> {
        TimeDomainArray {
            start_gps_pip: self.start_gps_pip,
            rate_hz: self.rate_hz,
            data,
            accumulation_stats: self.accumulation_stats.clone(),
        }
    }

}

impl <T: PipeData + Copy> TimeDomainArray<T> {

    /// from a set of ordered, non overlaping arrays, return a single array
    /// with any gaps filled in by a specific value
    pub (crate) fn fill_gaps(data: &Vec<Self>, gap_value: T) -> Option<Self> {
        if data.is_empty() {
            return None;
        }
        if data.len() == 1 {
            return Some(data[0].clone());
        }
        let mut new_data = data[0].clone();


        let step_pip = PipDuration::freq_hz_to_period(new_data.rate_hz);

        for i in 1..data.len() {

            let diff_pip = data[i].start_gps_pip - new_data.end_gps_pip();
            let diff_steps = diff_pip / step_pip;
            let gap = vec![gap_value; diff_steps as usize];
            new_data.data.extend(gap);
            new_data.data.append(&mut data[i].data.clone());
        }
        Some(new_data)
    }
}


impl <T: Clone> Accumulation for TimeDomainArray<T> {
    fn set_accumulation_stats(& self, stats: AccumulationStats) -> Self{
        let mut n = self.clone();
        n.accumulation_stats = stats;
        n
    }

    fn get_accumulation_stats(&self) -> &AccumulationStats {
        &self.accumulation_stats
    }
}

impl <T: Clone> MutableAccumulation for TimeDomainArray<T> {
    fn set_mut_accumulation_stats(&mut self, stats: AccumulationStats) {
        self.accumulation_stats = stats;
    }
}

#[cfg(any(feature = "python-pipe", feature = "python"))]
impl<'py, T: PipeDataPrimitive> IntoPyObject<'py> for TimeDomainArray<T> {
    type Target = PyTimeDomainArray;
    type Output = Bound<'py , PyTimeDomainArray>;
    type Error = PyErr;

    fn into_pyobject(self, py: Python<'py>) -> Result<Self::Output, Self::Error> {
        let data = PyArray::from_vec(py, self.data);
        let ptda = PyTimeDomainArray {
            start_gps_pip: self.start_gps_pip,
            rate_hz: self.rate_hz,
            n: self.accumulation_stats.n,
            sequence_index: self.accumulation_stats.sequence_index,
            sequence_size: self.accumulation_stats.sequence_size,
            data: data.into_any().unbind(),
        };
        //Python::with_gil(|py| {
        let obj = ptda.into_pyobject(py)?;
        
        Ok(obj)
    }
}

#[cfg_attr(any(feature = "python-pipe", feature = "python"),pyclass(frozen, name="TimeDomainArray", str))]
#[cfg(any(feature = "python-pipe", feature = "python"))]
pub struct PyTimeDomainArray {
    #[pyo3(get)]
    start_gps_pip: PipInstant,
    #[pyo3(get)]
    rate_hz: f64,
    #[pyo3(get)]
    n: f64,
    #[pyo3(get)]
    sequence_index: usize,
    #[pyo3(get)]
    sequence_size: usize,
    #[pyo3(get)]
    data: Py<PyAny>,
}

#[cfg(any(feature = "python-pipe", feature = "python"))]
impl Display for PyTimeDomainArray {
    fn fmt(&self, f: &mut Formatter<'_>) -> std::fmt::Result {
        write!(f, "TimeDomainArray(start_gps_pip={}, rate_hz={}, n={})", self.start_gps_pip, self.rate_hz, self.n)
    }
}

#[cfg(any(feature = "python-pipe", feature = "python"))]
#[pymethods]
impl PyTimeDomainArray {
    /// return the time of the first timestamp after the end of the time series
    /// equal to the start time of the following series if it is contiguous.
    pub fn end_gps_pip(&self) -> Result<PipInstant, PyErr> {

        let len = Python::with_gil(|py| {
           let bound = self.data.bind(py);
            bound.len()
        })?;

        // assume rate is a power of two
        Ok(self.index_to_gps_pip(len))
    }


    pub fn index_to_gps_pip(&self, index: usize) -> PipInstant {
        let pip_per_cyc = PipDuration::freq_hz_to_period(self.rate_hz);
        self.start_gps_pip + (pip_per_cyc * u64::from_usize(index).unwrap_or(0))
    }
}

#[cfg(any(feature = "python-pipe", feature = "python"))]
impl<'py, T: PipeData> FromPyObject<'py> for TimeDomainArray<T> {
    fn extract_bound(ob: &Bound<'py, PyAny>) -> PyResult<Self> {
        Python::with_gil(|_py| {
            let start_gps_pip: PipInstant = ob.getattr("start_gps_pip")?.extract()?;
            let rate_hz: f64 =  ob.getattr("rate_hz")?.extract()?;
            let data = ob.getattr("data")?.extract()?;
            let n = ob.getattr("n")?.extract()?;
            let sequence_index: usize = ob.getattr("sequence_index")?.extract()?;
            let sequence_size: usize = ob.getattr("sequence_size")?.extract()?;
            PyResult::Ok(TimeDomainArray{
                start_gps_pip,
                rate_hz,
                data,
                accumulation_stats: AccumulationStats{
                    n,
                    sequence_index,
                    sequence_size,
                }
            })
        })
    }
}


impl <T> Sub<T> for TimeDomainArray<T>
where
    T: Scalar
{
    type Output = TimeDomainArray<T>;

    fn sub(mut self, rhs: T) -> Self::Output {
        for x in self.data.iter_mut() {
            *x -= rhs;
        }
        self
    }
}

pub type TimeDomainArrayReal = TimeDomainArray<f64>;
pub type TimeDomainArrayComplex = TimeDomainArray<c128>;

#[cfg(test)]
mod tests {
    use crate::run_context::tests::start_runtime;
    use super::*;

    fn setup_td() -> TimeDomainArray<f64> {

        let data = (0..2048).map(|x|{x as f64}).collect();

        TimeDomainArray {
            // a bit less than one microsecond
            start_gps_pip: 1024000000000i128.into(),
            rate_hz: 2048.0,
            data,
            ..TimeDomainArray::default()
        }

    }

    const BLOCK_SIZE: usize = 2048;
    const STEP_SIZE: i128 = 1024000000000i128;

    const BIG_BLOCK: usize = BLOCK_SIZE*2;
    const SMALL_BLOCK: usize = BLOCK_SIZE/2;

    const FIRST_START: usize = BLOCK_SIZE + 2;
    const SECOND_START: usize = FIRST_START + 2 + BLOCK_SIZE*2;
    const THIRD_START: usize = SECOND_START + BIG_BLOCK + BLOCK_SIZE;


    fn setup_td_start(start_step: usize) -> TimeDomainArray<f64> {

    let data = (0..BLOCK_SIZE).map(|x|{x as f64}).collect();
        let step = PipDuration::from_pips(STEP_SIZE);
        TimeDomainArray {
            // a bit less than one microsecond
            start_gps_pip: PipInstant::gpst_epoch() + step * start_step,
            rate_hz: 2048.0,
            data,
            ..TimeDomainArray::default()
        }

    }

    fn setup_td_array() -> Vec<TimeDomainArray<f64>> {
        let data = (0..BLOCK_SIZE).map(|x|{x as f64}).collect();
        let step = PipDuration::from_pips(STEP_SIZE);
        let first = TimeDomainArray {
            start_gps_pip: PipInstant::gpst_epoch() + step * (FIRST_START),
            rate_hz: 2048.0,
            data,
            ..TimeDomainArray::default()
        };

        let data = (0..BIG_BLOCK).map(|x|{x as f64}).collect();
        let second = TimeDomainArray {
            start_gps_pip: PipInstant::gpst_epoch() + step * (SECOND_START),
            rate_hz: 2048.0,
            data,
            ..TimeDomainArray::default()
        };

        let data = (0..SMALL_BLOCK).map(|x|{x as f64}).collect();
        let third = TimeDomainArray {
            start_gps_pip: PipInstant::gpst_epoch() +  step * (THIRD_START),
            rate_hz: 2048.0,
            data,
            ..TimeDomainArray::default()
        };

        vec![first, second, third]
    }

    #[test]
    fn test_trim() {

        let (mut _uc, mut _or, rc) = start_runtime();

        let mut td = setup_td();
        let end1 = td.end_gps_pip();
        let period = PipDuration::freq_hz_to_period(td.rate_hz);
        // trim off first 116 values
        let new_start_pip = td.start_gps_pip + period * 116;
        td.trim_to(rc, new_start_pip).unwrap();
        let end2 = td.end_gps_pip();
        assert_eq!(end2, end1);
        assert_eq!(td.data.len(), 2048 - 116);
    }

    #[test]
    fn test_over_trim() {

        let (mut _uc, mut _or, rc) = start_runtime();

        let mut td = setup_td();
        let end1 = td.end_gps_pip();
        // trim off first 116 values
        let new_start_pip = td.start_gps_pip + PipDuration::from_sec(1) * 2164/2048.0;
        td.trim_to(rc, new_start_pip);
        let end2 = td.end_gps_pip();
        assert_eq!(end2, end1);
        assert_eq!(td.data.len(), 0);
    }

    #[test]
    fn test_splice_empty() {
        let mut array = vec![];
        let td = setup_td();
        td.clone().splice_into(&mut array);
        assert_eq!(array.len(), 1);
        assert_eq!(array[0].start_gps_pip, td.start_gps_pip);
        assert_eq!(array[0].data.len(), td.data.len());
        assert_eq!(array[0].rate_hz, td.rate_hz);
    }

    #[test]
    fn test_splice_before() {
        let (mut _uc, mut _or, rc) = start_runtime();

        let mut array = setup_td_array();
        let td = setup_td();

        let changed = td.clone().splice_into(&mut array);
        assert!(changed);
        assert_eq!(array.len(), 4);
        assert_eq!(array[0].start_gps_pip, td.start_gps_pip);
        assert_eq!(array[0].data.len(), td.data.len());
        assert_eq!(array[0].rate_hz, td.rate_hz);
    }

    #[test]
    fn test_splice_before_join() {
        let (mut _uc, mut _or, rc) = start_runtime();

        let mut array = setup_td_array();
        let td = setup_td_start(FIRST_START - BLOCK_SIZE);

        let start_len = array[0].data.len();
        assert_eq!(td.end_gps_pip(), array[0].start_gps_pip);
        let changed = td.clone().splice_into(&mut array);
        assert!(changed);
        assert_eq!(array.len(), 3);
        assert_eq!(array[0].start_gps_pip, td.start_gps_pip);
        assert_eq!(array[0].data.len(), td.data.len() + start_len);
        assert_eq!(array[0].rate_hz, td.rate_hz);
    }

    #[test]
    fn test_splice_before_overlap() {
        let (mut _uc, mut _or, rc) = start_runtime();

        let mut array = setup_td_array();
        let td = setup_td_start(FIRST_START - BLOCK_SIZE + 1);

        let start_len = array[0].data.len();
        let changed = td.clone().splice_into(&mut array);
        assert!(changed);
        assert_eq!(array.len(), 3);
        assert_eq!(array[0].start_gps_pip, td.start_gps_pip);
        assert_eq!(array[0].data.len(), td.data.len() + start_len - 1);
        assert_eq!(array[0].rate_hz, td.rate_hz);
    }

    #[test]
    fn test_splice_first_exact() {
        let (mut _uc, mut _or, rc) = start_runtime();

        let mut array = setup_td_array();
        let td = setup_td_start(FIRST_START);

        let start_len = array[0].data.len();
        let changed = td.clone().splice_into(&mut array);
        assert!(!changed);
        assert_eq!(array.len(), 3);
        assert_eq!(array[0].start_gps_pip, td.start_gps_pip);
        assert_eq!(array[0].data.len(),  start_len);
        assert_eq!(array[0].rate_hz, td.rate_hz);
    }

    #[test]
    fn test_splice_between() {
        let (mut _uc, mut _or, rc) = start_runtime();

        let mut array = setup_td_array();
        let td = setup_td_start(SECOND_START - BLOCK_SIZE - 1);

        let start_len = array[0].data.len();
        let changed = td.clone().splice_into(&mut array);
        assert!(changed);
        assert_eq!(array.len(), 4);
        assert_eq!(array[1].start_gps_pip, td.start_gps_pip);
        assert_eq!(array[1].data.len(),  start_len);
        assert_eq!(array[1].rate_hz, td.rate_hz);
    }

    #[test]
    fn test_splice_subsumed() {
        let (mut _uc, mut _or, rc) = start_runtime();

        let mut array = setup_td_array();
        let td = setup_td_start(SECOND_START + 1);

        let start_len = array[1].data.len();
        let changed = td.clone().splice_into(&mut array);
        assert!(!changed);
        assert_eq!(array.len(), 3);
        assert_eq!(array[1].data.len(),  start_len);
        assert_eq!(array[1].rate_hz, td.rate_hz);
    }

    #[test]
    fn test_splice_exact_join() {
        let (mut _uc, mut _or, rc) = start_runtime();

        let mut array = setup_td_array();
        let td = setup_td_start(THIRD_START - BLOCK_SIZE);

        let start_len = array[1].data.len();
        let start_len2 = array[2].data.len();
        let changed = td.clone().splice_into(&mut array);
        assert!(changed);
        assert_eq!(array.len(), 2);
        assert_eq!(array[1].data.len(),  start_len + start_len2 + td.data.len());
        assert_eq!(array[1].rate_hz, td.rate_hz);
    }

    #[test]
    fn test_splice_cover() {
        let (mut _uc, mut _or, rc) = start_runtime();

        let mut array = setup_td_array();
        let td = setup_td_start(THIRD_START - 1);

        let changed = td.clone().splice_into(&mut array);
        assert!(changed);
        assert_eq!(array.len(), 3);
        assert_eq!(array[2].start_gps_pip, td.start_gps_pip);
        assert_eq!(array[2].data.len(),  td.data.len());
        assert_eq!(array[2].rate_hz, td.rate_hz);
    }

    #[test]
    fn test_splice_after() {
        let (mut _uc, mut _or, rc) = start_runtime();

        let mut array = setup_td_array();
        let td = setup_td_start(THIRD_START + SMALL_BLOCK + 1);

        let start_len = array[0].data.len();
        let changed = td.clone().splice_into(&mut array);
        assert!(changed);
        assert_eq!(array.len(), 4);
        assert_eq!(array[3].start_gps_pip, td.start_gps_pip);
        assert_eq!(array[3].data.len(),  start_len);
        assert_eq!(array[3].rate_hz, td.rate_hz);
    }

    #[test]
    fn test_splice_big() {
        let (mut _uc, mut _or, rc) = start_runtime();

        let mut array = setup_td_array();
        let mut td = setup_td_start(1);
        td.data = (0..20480).map(|x|{x as f64}).collect();

        let changed = td.clone().splice_into(&mut array);
        assert!(changed);
        assert_eq!(array.len(), 1);
        assert_eq!(array[0].start_gps_pip, td.start_gps_pip);
        assert_eq!(array[0].data.len(),  td.data.len());
        assert_eq!(array[0].rate_hz, td.rate_hz);
    }
}


// some more trait implementations

impl<T, U> Sqrt for TimeDomainArray<T>
where
    T: Sqrt<Output=U> + PipeDataPrimitive,
    U: PipeDataPrimitive
{
    type Output = TimeDomainArray<U>;

    fn square_root(&self) -> Self::Output {
        let data = self.data.iter().map(|x|{x.square_root()}).collect();
        self.clone_metadata(data)
    }
}