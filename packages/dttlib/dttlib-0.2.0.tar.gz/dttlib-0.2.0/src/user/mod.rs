use core::borrow;
use borrow::Borrow;
use std::fmt::{Debug, Display, Formatter};
use std::boxed::Box;
use std::time::Duration;

use gps_pip::{PipDuration, PipInstant};
#[cfg(feature = "python")]
use pyo3::{
    pyclass,
    pymethods, Bound, BoundObject,
    IntoPyObject, IntoPyObjectExt, PyAny,
    PyErr,
    Python,
};

use tokio::runtime::Handle;
use tokio::task::JoinError;
use tokio::sync::mpsc::unbounded_channel;
use tokio::sync::watch;
use tokio::sync::mpsc::error::SendError;
#[cfg(test)]
use tokio::time::Instant;

use user_messages::{MessageHash, MessageJob, Sender};
use crate::analysis::result::{
    record::ResultsRecord,
    AnalysisResult,
};
use crate::data_source::{ChannelQuery, DataSourceRef};
use crate::errors::DTTError;
use crate::run::{RunHandle, RunStatusMsg, RunStatusSender};
use crate::scope_view::{ScopeViewHandle, ViewSet};
use crate::run_context::RunContext;
use crate::params::test_params::TestParams;
use crate::timeline::{init::calculate_timeline, CalcTimelineResult, Timeline};


///# User interface data objects
#[derive(Debug)]
pub (crate) enum UserMessage {
    NoOp,
    NewTestParams(TestParams),
    RunTest,
    AbortTest,
    NewDataSource(DataSourceRef),
    NewFixedScopeView{
        return_channel: tokio::sync::oneshot::Sender<ScopeViewHandle>,
        set: ViewSet,
        start_pip: PipInstant,
        end_pip: PipInstant,
    },
    NewOnlineScopeView{
        return_channel: tokio::sync::oneshot::Sender<ScopeViewHandle>,
        set: ViewSet,
        span_pip: PipDuration,
    },
    QueryChannels(ChannelQuery),
}

#[derive(Clone, Debug)]
#[cfg_attr(feature = "python", pyclass(frozen, str))]
pub enum ResponseToUser {
    AllMessages(MessageHash),
    UpdateMessages{message_job: MessageJob},
    NewTimeline(Timeline),
    NewResult(AnalysisResult),
    FinalResults(ResultsRecord),
    ScopeViewResult{id: usize, result: AnalysisResult},
    ChannelQueryResult{channels: Vec<Channel>},
}

impl Display for ResponseToUser {
    fn fmt(&self, f: &mut Formatter<'_>) -> std::fmt::Result {
        match self {
            Self::AllMessages(_) => write!(f, "AllMessages(...)"),
            Self::UpdateMessages{message_job} => write!(f, "MessageJob({})", message_job),
            Self::NewTimeline(_) => write!(f, "NewTimeline(...)"),
            Self::NewResult(_) => write!(f, "NewResult(...)"),
            Self::FinalResults(_) => write!(f, "FinalResult(...)"),
            Self::ScopeViewResult{id, result: r} => write!(f, "ScopeViewResult({}, {})", id, r),
            Self::ChannelQueryResult{channels: _c} => write!(f, "ChannelQueryResult(...)"),
        }
    }
}

// #[cfg(feature = "python")]
// impl<'py> IntoPyObject<'py> for ResponseToUser {
//     type Target = PyAny;
//     type Output = Bound<'py, Self::Target>;
//     type Error = PyErr;
//
//     fn into_pyobject(self, py: Python<'py>) -> Result<Self::Output, Self::Error> {
//         match(self) {
//             AllMessages(m) => m.into_pyobject(py).map(|v|{v.into_any()}),
//             ResponseToUser::UpdateMessages(m) => m.into_pyobject(py).map(|v|{v.into_any()}),
//             ResponseToUser::NewTimeline(t) => t.into_pyobject(py).map(|v|{v.into_any()}),
//             ResponseToUser::NewResult(r) => r.into_pyobject(py).map(|v|{v.into_any()}),
//             ResponseToUser::FinalResults(r) => r.into_pyobject(py).map(|v|{v.into_any()}),
//             ResponseToUser::ScopeViewResult(id, r) =>
//         }
//     }
// }


pub (crate) type UserInputReceiver = tokio::sync::mpsc::UnboundedReceiver<UserMessage>;
pub (crate) type UserInputSender = tokio::sync::mpsc::UnboundedSender<UserMessage>;
pub type UserOutputReceiver = tokio::sync::mpsc::UnboundedReceiver<ResponseToUser>;
pub (crate) type UserOutputSender = tokio::sync::mpsc::UnboundedSender<ResponseToUser>;

pub (crate) fn new_user_output_channel() -> (UserOutputSender, UserOutputReceiver) {
    unbounded_channel::<ResponseToUser>()
}

pub (crate) fn new_user_input_channel() -> (UserInputSender, UserInputReceiver) {
    unbounded_channel::<UserMessage>()
}

/// Wrap a UserOutputSender so we can implement the user_messages::Sender trait
pub (crate) struct UserOutputSenderWrapper {
    sender: UserOutputSender
}

impl Sender for UserOutputSenderWrapper {
    fn update_all(&mut self, messages: MessageHash) -> Result<(), String> {
        self.sender.send(ResponseToUser::AllMessages(messages)).map_err(|e|{e.to_string()})
    }

    fn set_message(&mut self, tag: String, msg: user_messages::UserMessage) -> Result<(), String> {
        self.sender.send(ResponseToUser::UpdateMessages {
            message_job: MessageJob::SetMessage{tag,
            msg}
        }).map_err(|e|{e.to_string()})
    }

    fn clear_message(&mut self, tag: &str) -> Result<(), String> {
        self.sender.send(ResponseToUser::UpdateMessages {
            message_job: MessageJob::ClearMessage{tag: tag.to_string()}
        }).map_err(|e|{e.to_string()})
    }
}

impl UserOutputSenderWrapper {
   pub (crate) fn new(sender: UserOutputSender) -> Self {
       UserOutputSenderWrapper{
           sender
       }
   }
}

///## immutable "global" values
/// A DTT struct stores channels used to communicate with the user.
/// The user owns the struct and merely drops it when done.
/// The entire core will shut down at that point.
/// Most public API is called on this structure.
///
/// Applications should use the init_...() functions to create this structure.
#[cfg_attr(feature = "python", pyclass)]
#[derive(Clone)]
pub struct DTT {

    /// send a message from the user to DTT core
    send: UserInputSender,

    /// async runtime associated with the context.
    pub (crate) runtime: Handle,
}

impl DTT {
    pub(crate) fn create(runtime: Handle) -> (Self, UserInputReceiver, UserOutputSender, UserOutputReceiver) {
        let in_chan = new_user_input_channel();
        let out_chan = new_user_output_channel();
        let uc = DTT {
            send: in_chan.0,
            runtime,
        };
        (uc, in_chan.1, out_chan.0, out_chan.1)
    }

    fn send(&self, msg: UserMessage) -> Result<(), SendError<UserMessage>> {
        self.send.send(msg)
    }


    // # Non-python public interface methods

    /// Get the handle the Tokio runtime that
    /// libdtt is using
    /// depending on how libdtt is initialized,
    /// this could be a runtime passed to libdtt or
    /// one created internally
    pub fn runtime_handle(&self) -> Handle {
        self.runtime.clone()
    }


    /// Create a new online scope view and return a handle to it.
    /// Drop all clones of the handle to close the view.
    pub async fn async_new_online_scope_view(&mut self, set: ViewSet, span_pip: PipDuration) -> Result<ScopeViewHandle, DTTError> {
        let (handle_tx, handle_rx) = tokio::sync::oneshot::channel();
        self.send(UserMessage::NewOnlineScopeView{return_channel: handle_tx, set, span_pip})?;
        match handle_rx.await {
            Ok(h) => Ok(h),
            Err(e) => Err(DTTError::ViewConfig(e.to_string())),
        }
    }

    /// Create a new fixed scope view and return a handle to it.
    /// Drop all clones of the handle to close the view
    pub async fn async_new_fixed_scope_view(&mut self, set: ViewSet, start_pip: PipInstant, end_pip: PipInstant) -> Result<ScopeViewHandle, DTTError> {
        let (handle_tx, handle_rx) = tokio::sync::oneshot::channel();
        self.send(UserMessage::NewFixedScopeView{return_channel: handle_tx, set, start_pip, end_pip})?;
        match handle_rx.await {
            Ok(h) => Ok(h),
            Err(e) => Err(DTTError::ViewConfig(e.to_string())),
        }
    }
}

#[cfg_attr(feature = "python", pymethods)]
impl DTT {

    /// set the desired data source
    pub fn set_data_source(&mut self, data_source: DataSourceRef) -> Result<(), DTTError> {
        Ok( self.send(UserMessage::NewDataSource(data_source))? )
    }

    // # python public interface methods

    /// Set up a test.  Eventually, the library will send an updated Timeline object
    /// on the associated output receiver
    /// start the test with run_test()
    /// an error means the DTT management process has died.
    pub fn set_test_params(&mut self, params: TestParams) -> Result<(), DTTError> {
        Ok(self.send(UserMessage::NewTestParams(params))?)
    }


    /// start a test
    /// the test must already be configured with set_test_params
    /// as the test is run, status messages and results will appear on
    /// the associated output receiver.
    /// An error means the DTT management process has died.
    pub fn run_test(& mut self) -> Result<(), DTTError > {
        Ok( self.send(UserMessage::RunTest)? )
    }

    /// Send a no-op message.  Good test if the
    /// If this succeeds than  the DTT object is working in some sense.
    pub fn no_op(&mut self) -> Result<(), DTTError> {
        self.send(NoOp).map_err(|e|{e.into()})
    }

    /// Create a new online scope view and return a handle to it.
    /// Drop all clones of the handle to close the view.
    pub fn new_online_scope_view(&mut self, set: ViewSet, span_pip: PipDuration) -> Result<ScopeViewHandle, DTTError> {
        let (handle_tx, handle_rx) = tokio::sync::oneshot::channel();
        self.send(UserMessage::NewOnlineScopeView{return_channel: handle_tx, set, span_pip})?;
        match handle_rx.blocking_recv() {
            Ok(h) => Ok(h),
            Err(e) => Err(DTTError::ViewConfig(e.to_string())),
        }
    }

    /// Create a new fixed scope view and return a handle to it.
    /// Drop all clones of the handle to close the view
    pub fn new_fixed_scope_view(&mut self, set: ViewSet, start_pip: PipInstant, end_pip: PipInstant) -> Result<ScopeViewHandle, DTTError> {
        let (handle_tx, handle_rx) = tokio::sync::oneshot::channel();
        self.send(UserMessage::NewFixedScopeView{return_channel: handle_tx, set, start_pip, end_pip})?;
        match handle_rx.blocking_recv() {
            Ok(h) => Ok(h),
            Err(e) => Err(DTTError::ViewConfig(e.to_string())),
        }
    }

    pub fn find_channels(&mut self, query: ChannelQuery) -> Result<(), DTTError> {
        Ok(self.send(QueryChannels(query))?)
    }
}

#[cfg(test)]
use user_messages::Severity;
use crate::params::channel_params::Channel;
use crate::user::UserMessage::{NoOp, QueryChannels};

/// Test functions
#[cfg(test)]
impl DTT {
    /// run a test and return some results
    pub (crate) async fn exec_test(mut self, mut or: UserOutputReceiver, test_params: TestParams, data_source: DataSourceRef,
                      timeout: Duration) -> (Duration,) {
        self.send(UserMessage::NewTestParams(test_params)).unwrap();
        self.send(UserMessage::NewDataSource(data_source)).unwrap();
        self.send(UserMessage::RunTest).unwrap();

        let start_test = Instant::now();

        'main: loop {

            tokio::select! {
                _ = tokio::time::sleep(timeout) => {
                    panic!("Ran out of time while waiting for test to finish")
                },
                r = or.recv() => {
                    match r {
                        None => {
                            panic!("User output channel closed before test was finished");
                        }
                        Some(m) => {
                            match m {
                                ResponseToUser::FinalResults(_) => {
                                    break 'main;
                                },
                                ResponseToUser::AllMessages(a) => {
                                    for (key, value) in a {
                                        if value.severity >= Severity::Error {
                                            panic!("Error encountered while running test: {}", value.message);
                                        }
                                    }
                                },
                                _ => (),
                            }
                        }
                    }
                },
            }


        }

        let stop_test = Instant::now();

        let test_time = stop_test - start_test;

        (test_time, )
    }
}


#[derive(Clone)]
pub (crate) enum TimelineStatus {
    NotSet,
    Calculating,
    Latest(Timeline),
    Aborted(DTTError),
}

pub (crate) type TimelineStatusSender = watch::Sender<TimelineStatus>;
pub (crate) type TimelineStatusReceiver = watch::Receiver<TimelineStatus>;


/// this is the main control loop of the DTT kernel
pub (crate) async fn start_user_process(mut input_receive: UserInputReceiver, out_send: UserOutputSender) {
    let rc = Box::new(RunContext::create(out_send).await);
    let (timeline_status_sender, timeline_status_receiver) = watch::channel(TimelineStatus::NotSet);

    let (run_status_sender, run_status_receiver) = watch::channel(RunStatusMsg::NeverStarted);
    //let run_test_join = Fuse::terminated(),
    let mut _run_handle = None;

    let mut data_source = None;

    Handle::current().spawn(
        async move {
            while let Some(m) = input_receive.recv().await {
                println!();
                match m {
                    NoOp => (),

                    UserMessage::NewTestParams(p) => {
                        timeline_status_sender.send_replace(TimelineStatus::Calculating);
                        let rct = run_calc_timeline(rc.clone(),
                                                    timeline_status_sender.clone(), p);
                        tokio::spawn(rct);
                    }

                    UserMessage::RunTest => {
                        let m = run_status_receiver.borrow().clone();
                        match m {
                            RunStatusMsg::Aborted(_)
                            | RunStatusMsg::NeverStarted
                            | RunStatusMsg::Finished => {
                                _run_handle = start_test(rc.clone(), timeline_status_receiver.clone(),
                                                         run_status_sender.clone(), &data_source).await;
                            },
                            _ => {
                                rc.user_messages.error("Cannot start a test because another is still running");
                            }
                        }
                    },

                    UserMessage::AbortTest => {},

                    UserMessage::NewDataSource(d) => {
                        rc.user_messages.clear_message("NoDataSource");
                        data_source = Some(d);
                    },
                    UserMessage::NewFixedScopeView{return_channel, set, start_pip, end_pip} => {
                      match &data_source {
                          Some(d) => {
                              let svh = ScopeViewHandle::new_fixed(rc.clone(), d.clone(), set, start_pip, end_pip);
                              if return_channel.send(svh).is_err() {
                                  // do nothing, program must be dying
                              }
                          },
                          None => {
                              rc.user_messages.error("Cannot provision a new scope view without a data source");
                          }
                      }
                    },
                    UserMessage::NewOnlineScopeView{return_channel, set, span_pip} => {
                        match &data_source {
                            Some(d) => {
                                let svh = ScopeViewHandle::new_online(rc.clone(), d.clone(), set, span_pip);
                                if return_channel.send(svh).is_err() {
                                    // do nothing, program must be dying
                                }
                            },
                            None => {
                                rc.user_messages.error("Cannot provision a new scope view without a data source");
                            }
                        }
                    },
                    UserMessage::QueryChannels(q) => {
                        match &data_source {
                            Some(d) => {
                                let rc2 = rc.clone();
                                if let Err(e) = d.find_channels(rc2, &q) {
                                    rc.user_messages.error(e.to_string());
                                }
                            },
                            None => rc.user_messages.error("Cannot query channels without a data source"),
                        }
                    }
                }
                println!("handled user input");
            }
        });
}


async fn run_calc_timeline(rc: Box<RunContext>, tss: TimelineStatusSender, params: TestParams) {
    let sleep_fut = tokio::time::sleep(Duration::from_secs(10));
    let rc2 = rc.clone();
    let calc_fut = Handle::current().spawn_blocking(move || {
        calculate_timeline(rc, params)
    });
    tokio::select! {
        res = calc_fut => {
            match res {
                Ok(ctr) => {
                    match ctr {
                        Ok(tl) => {
                            match rc2.output_handle.sender.send(ResponseToUser::NewTimeline(tl.clone())) {
                                Ok(_) => (),
                                Err(_) => (),
                            }
                            tss.send_replace(TimelineStatus::Latest(tl));
                        }
                        Err(e) => {
                            tss.send_replace(TimelineStatus::Aborted(e));
                        },
                    }
                }
                Err(e) => {
                    tss.send_replace(TimelineStatus::Aborted(DTTError::BlockingTaskJoinFailed(e.to_string())));
                }
            }
        },
        _ = sleep_fut => {
            tss.send_replace(TimelineStatus::Aborted(DTTError::TimedOut("Calculating Timeline".to_string())));
        }
    }

}


async fn start_test(rc: Box<RunContext>, mut tsr: TimelineStatusReceiver,
                    run_status_sender: RunStatusSender, data_source: &Option<DataSourceRef>) -> Option<RunHandle> {
    let mut tl_state = tsr.borrow_and_update().clone();
    loop {
        match tl_state.borrow() {
            TimelineStatus::NotSet | TimelineStatus::Aborted(_) => {
                rc.user_messages.error(
                    "A test started when no parameters have been sent".to_string());
                return None;
            },
            TimelineStatus::Calculating => {
                // no need to timeout since run_calc_timeline() will eventually set the state to Abort
                let change = tsr.changed().await;
                match change {
                    Ok(_) => {
                        tl_state = tsr.borrow_and_update().clone();
                    }
                    Err(_) => {
                        // user process is probably dead.  Just close out.
                        return None;
                    }
                }
            },
            TimelineStatus::Latest(timeline) => {
                match data_source {
                    Some(d) => {
                        if let Err(missing_caps) = d.check_timeline_against_capabilities(timeline) {
                            let mut msg = "The data source was missing these capabilities needed to run the test:".to_string();
                            for cap in missing_caps {
                                msg = msg + format!(" [{}]", cap).as_str();
                            }
                            rc.user_messages.error(msg);
                        }
                        else {
                            return Some(RunHandle::run_test(rc, &timeline, run_status_sender, d.clone()).await);
                        }
                    },
                    None => {
                        rc.user_messages.set_error("NoDataSource",
                                                   "A test cannot be started without a data source");
                        return None;
                    }
                }
            }
        }
    };
}

fn _handle_timeline_result(rc: Box<RunContext>, res: Result<CalcTimelineResult, JoinError>) -> Option<Timeline> {
    match res {
        Ok(cres) => {
            match cres {
                Ok(t) => {
                    let _ = rc.output_handle.send(rc.clone(),
                                          ResponseToUser::NewTimeline(t.clone()));
                    Some(t)
                }
                Err(e) => {
                    rc.user_messages.error(e.to_string());
                    None
                }
            }
        }
        Err(e) => {
            let mut err_str: String = "Failed to join timeline calculation: ".to_string();
            err_str.push_str(e.to_string().as_str());
            rc.user_messages.error(err_str);
            None
        }
    }
}



/// Handle the generation of all output to the user
#[derive(Clone)]
pub struct UserOutputHandle {
    sender: UserOutputSender
}

impl UserOutputHandle {
    pub (crate) fn new(sender: UserOutputSender) -> UserOutputHandle {
        UserOutputHandle {
            sender,
        }
    }

    /// Sends the message to a user. If the send fails, sets
    /// an error message (that probably won't get to a user!).
    pub (crate) fn send(&self, rc: Box<RunContext>, resp: ResponseToUser) -> Result<(), SendError<ResponseToUser>> {
        const TAG: &str = "UserSendError";
        let r = self.sender.send(resp);
        match &r {
            Ok(_) => {
                rc.user_messages.clear_message(TAG)
            },
            Err(e) => {
                rc.user_messages.set_warning(TAG, format!("Could not send a response to the user: {}", e.to_string()))
            }
        }
        r
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::tokio_setup::tokio_init;
    use crate::params::test_params::{TestParams, TestType};
    use std::time::Duration;
    use num_traits::abs;
    use tokio::time::sleep;
    use user_messages::Severity;
    use crate::data_source::DataSource;
    use crate::data_source::dummy::Dummy;
    use crate::params::channel_params::{nds_data_type::NDSDataType, ChannelSettings, ChannelSettingsParams, ChannelType};
    use crate::params::channel_params::channel::Channel;
    use crate::params::channel_params::decimation_parameters::{DecimationDelays, DecimationParameters};

    fn create_ffttools_tp() -> TestParams {
        let mut tp = TestParams::default_fft_params();
        if let TestType::FFTTools =  tp.test_type{
            tp.measurement_channels = Vec::from(
                [
                    ChannelSettingsParams {
                        active: true,
                        channel: ChannelSettings {
                            raw_decimation_params: DecimationParameters::default(),
                            heterodyned_decimation_params: DecimationParameters::default(),
                            do_heterodyne: false,
                            decimation_delays: DecimationDelays::default(),
                            channel: Channel {
                                name: "X1:NOT-A_CHANNEL".to_string(),
                                channel_type: ChannelType::Unknown,
                                data_type: NDSDataType::Float64,
                                rate_hz: 16384.0,
                                dcu_id: None,
                                channel_number: None,
                                calibration: None,
                                heterodyne_freq_hz: None,
                                gain: None,

                                use_active_time: false,
                                offset: None,
                                slope: None,
                                units: None,
                            },
                        }
                    }
                ]
            );
            // tp.average_size = 1;
            // tp.measurement_time_pip = sec_to_pip(1.0);
        }
        else
        {
            panic!("Wrong test type '{}' when getting FFTToolsParams", tp.test_type);
        }
        tp
    }

    #[test]
    fn no_active_channels_test() {
        let rt = tokio::runtime::Runtime::new().unwrap();
        let (mut uc, mut or) = tokio_init(rt.handle()).unwrap();
        let mut tp = create_ffttools_tp();
        tp.measurement_channels[0].active = false;

        uc.send.send(UserMessage::NewTestParams(tp.clone())).unwrap();
        uc.runtime.block_on(
            async {
                loop {
                    tokio::select! {
                        _ = sleep(Duration::from_secs(2)) => {
                            panic!("Constraint failure message not received")
                        },
                        Some(m) = or.recv() => {
                             match m {
                                ResponseToUser::NewTimeline(_tl) => {
                                   panic!("Timeline received, but it should have failed a constraint")
                                },
                                ResponseToUser::AllMessages(m) => {
                                    if m.contains_key("MissingMeasurementChannel") {
                                        break;
                                    }
                                }
                                _ => (),
                            };
                        },

                    }

                }
            }
        );
    }

    #[test]
    fn sleep_test() {
        let rt = tokio::runtime::Runtime::new().unwrap();
        let (mut uc, mut or) = tokio_init(rt.handle()).unwrap();
        let _tp = create_ffttools_tp();

        uc.runtime.block_on(
            async {
                loop {
                    tokio::select! {
                        _ = sleep(Duration::from_secs(1)) => {
                            break;
                        },
                        Some(m) = or.recv() => {
                             match m {
                                ResponseToUser::NewTimeline(_tl) => {
                                   panic!("No timeline should have been calculated")
                                },
                                ResponseToUser::AllMessages(m) => {
                                }
                                _ => (),
                            };
                        },

                    }

                }
            }
        );
    }

    #[test]
    fn run_test() {
        let rt = tokio::runtime::Runtime::new().unwrap();
        let (mut uc, mut or) = tokio_init(rt.handle()).unwrap();
        let mut tp = create_ffttools_tp();
        let ds = Dummy::default().as_ref();

        tp.stop_hz = 700.0;
        uc.send.send(UserMessage::NewTestParams(tp.clone())).unwrap();
        uc.send.send(UserMessage::NewDataSource(ds)).unwrap();
        uc.send.send(UserMessage::RunTest).unwrap();
        uc.runtime.block_on(
            async {
                loop {
                    tokio::select! {
                        _ = sleep(Duration::from_secs(2)) => {
                            panic!("Test never finished");
                        },
                        r = or.recv() => {
                            match r {
                              Some(m) =>
                                 match m {
                                    ResponseToUser::AllMessages(m2) => {
                                        dbg!(&m2);
                                        for (key, val) in m2.iter() {
                                            if val.severity >= Severity::Error {
                                                panic!("Error message received");
                                            }
                                        }
                                    },
                                    ResponseToUser::FinalResults(_) => {
                                        break;
                                    },
                                    ResponseToUser::NewResult(a) => {
                                    },
                                    _ => {
                                    },
                                },
                                None => panic!("User context closed before test was finished"),
                            }
                        },
                    }
                }
            }
        );
    }

    #[test]
    fn timeline_test() {
        let rt = tokio::runtime::Runtime::new().unwrap();
        let (mut uc, mut or) = tokio_init(rt.handle()).unwrap();
        let mut tp = create_ffttools_tp();
        tp.overlap = 0.8;

        tp.overlap = 0.20;

        uc.send.send(UserMessage::NewTestParams(tp.clone())).unwrap();
        uc.runtime.block_on(
            async  {
                loop {
                    tokio::select! {
                        _ = sleep(Duration::from_secs(2)) => {
                            panic!("Timeline not received")
                        },
                        Some(m) = or.recv() => {
                            match m {
                                ResponseToUser::NewTimeline(tl) => {
                                        let d = abs(tl.segment_pitch_pip.to_seconds() - 0.8);
                                        // value is rounded to decimated sample rate
                                        assert!(d < 1.0/2048.0);
                                        break;
                                    },
                                _ => (),
                            };
                        },
                    }
                }
            }
        );

        // should cause a constraint failure
        tp.overlap = 1.10;
        uc.send.send(UserMessage::NewTestParams(tp.clone())).unwrap();
        uc.runtime.block_on(
            async {
                loop {
                    tokio::select! {
                        _ = sleep(Duration::from_secs(2)) => {
                            panic!("Constraint failure message not received")
                        },
                        Some(m) = or.recv() => {
                             match m {
                                ResponseToUser::NewTimeline(_tl) => {
                                   panic!("Timeline received, but it should have failed a constraint")
                                },
                                ResponseToUser::AllMessages(m) => {
                                    if m.contains_key("OverlapOutOfRange") {
                                        break;
                                    }
                                }
                                _ => (),
                            };
                        },

                    }

                }
            }
        );

        tp.overlap = 0.80;
        uc.send.send(UserMessage::NewTestParams(tp.clone())).unwrap();
        uc.runtime.block_on(
            async {
                loop {
                    tokio::select! {
                        _ = sleep(Duration::from_secs(2)) => {
                            panic!("Timeline not received")
                        },
                        Some(m) = or.recv() => {
                             match m {
                                ResponseToUser::NewTimeline(tl) => {
                                    let d = abs(tl.segment_pitch_pip.to_seconds() - 0.2);
                                    // value is rounded to decimated sample rate
                                    assert!(d < 1.0/2048.0);
                                    break;
                                },
                                _ => (),
                            };
                        },

                    }

                }
            }
        );
    }
}
