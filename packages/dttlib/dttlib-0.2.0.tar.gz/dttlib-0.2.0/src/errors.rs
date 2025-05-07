use nds2_client_rs::NDSError;
#[cfg(feature = "python")]
use pyo3::exceptions::PyRuntimeError;
use thiserror::Error;
use tokio::sync::mpsc::error::SendError;

#[derive(Error, Debug, Clone)]
pub enum DTTError {
    #[error("Timeline Calculation Failed: {0}")]
    TimelineCalcFailed(String),
    #[error("Failed to create async runtime: {0}")]
    RuntimeCreationFailed(String),
    #[error("A bad test parameter '{0}' caused a failure")]
    BadTestParameter(String),
    #[error("A constraint could not be satisfied")]
    UnsatisfiedConstraint,
    #[error("Blocking task join error: {0}")]
    BlockingTaskJoinFailed(String),
    #[error("Timed out while {0}")]
    TimedOut(String),
    #[error("Channel closed")]
    ChannelClosed,
    #[error("Bad Argument in {0}: {1} {2}")]
    BadArgument(&'static str, &'static str, &'static str),
    #[error("Error in calculation: {0}")]
    CalcError(String),
    #[error("Unrecognized Error: {0}")]
    UnrecognizedError(String),
    #[error("out of memory: {0}")]
    OutOfMemory(&'static str),
    #[error("{0}")]
    NDSClientError(#[from] NDSError),
    #[error("A calculation that needs a bound start time was made on an unbound start time")]
    UnboundStartTime,
    #[error("MPSC send error {0}")]
    TokioMPSCSend(String),
    #[error("Send failure on tokio watch channel: {0}")]
    TokioWatchSend(String),
    #[error("Failure on tokio join: {0}")]
    TokioJoinError(String),
    #[error("Unimplemented Option: {0}, {1}")]
    UnimplementedOption(String, String),
    #[error("Error in constructed analysis pipelines: {0}")]
    AnalysisPipelineError(String),
    #[error("Warning in constructed analysis pipelines: {0}")]
    AnalysisPipelineWarning(String),
    #[error("Mismatched types: {0}")]
    MismatchedTypesError(String),
    #[error("Unsupported type {0} when {1}")]
    UnsupportedTypeError(&'static str, &'static str),
    #[error("Missing data stream: {0}")]
    MissingDataStreamError(String),
    #[error["{0} does not have the capability to {1}"]]
    NoCapabaility(String, String),
    #[error("View closed")]
    ViewClosed,
    #[error("Error while configuring view: {0}")]
    ViewConfig(String),
}

impl <T> From<tokio::sync::mpsc::error::SendError<T>> for DTTError {
    fn from(value: SendError<T>) -> Self {
        DTTError::TokioMPSCSend(value.to_string())
    }
}

impl From<tokio::task::JoinError> for DTTError {
    fn from(value: tokio::task::JoinError) -> Self {
        DTTError::TokioJoinError(value.to_string())
    }   
}

impl <T> From<tokio::sync::watch::error::SendError<T>> for DTTError {
    fn from(value: tokio::sync::watch::error::SendError<T>) -> Self {
        DTTError::TokioWatchSend(value.to_string())
    }
}

#[cfg(feature = "python")]
impl From<DTTError> for pyo3::PyErr {
    fn from(value: DTTError) -> Self {
        PyRuntimeError::new_err(value.to_string())
    }   
}
