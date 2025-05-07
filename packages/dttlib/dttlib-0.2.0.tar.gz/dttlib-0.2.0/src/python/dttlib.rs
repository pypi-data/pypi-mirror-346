#![cfg(feature = "python")]
//! The python interface to the DTT library

use pyo3::{pyfunction, pymodule, wrap_pyfunction, Bound, PyObject, PyResult, Python};
use pyo3::types::PyTuple;
use pyo3::exceptions::PyRuntimeError;
use pyo3::prelude::{PyModule, PyModuleMethods};
use gps_pip::{PipDuration, PipInstant};
use crate::data_source::{
    ChannelQuery,
    nds_cache::{DataFlow, NDS2Cache}
};

use user_messages::{MessageJob, UserMessage};

use crate::{init_internal_runtime};
use crate::params::channel_params::{Channel, NDSDataType, ChannelType};
use crate::scope_view::{ScopeViewHandle, ViewSet};
use crate::user::{ResponseToUser, UserOutputReceiver, DTT};
use crate::python::dtt_types::dtt_types;
use crate::default_fft_params;
use crate::analysis::result::AnalysisResult;
use crate::analysis::scope::inline_fft::InlineFFTParams;
use crate::params::test_params::FFTWindow;

#[pyfunction]
fn init(callback: PyObject) -> PyResult<DTT> {

    let (uc, or) = init_internal_runtime().map_err(|e| PyRuntimeError::new_err(e.to_string()))?;

    // take a callback function to call with results objects
    uc.runtime.spawn(run_py_callback(uc.clone(), or, callback));


    Ok(uc)
}

/// take an output receiver and PyO3 python function
/// loop on receive of output, and call the python function
/// with each output.
async fn run_py_callback(_uc: DTT, mut or: UserOutputReceiver, py_func: PyObject) {
    while let Some(value) = or.recv().await {
        Python::with_gil( |py| {
            let tup = vec![value];
            match PyTuple::new(py, tup) {
                Ok(pytup) => {
                    if let Err(e) = py_func.call1(py, pytup) {
                        let err_tup = vec![e.to_string()];
                        let pyerrtup = PyTuple::new(py, err_tup).unwrap();
                        if let Err(e2) =  py_func.call1(py, pyerrtup) {
                            println!("Error calling python callback: {}", e);
                            println!("Led to second error when trying to callback with error: {}", e2);
                        }
                    }
                },
                Err(e) => {
                    println!("Error creating python tuple: {}", e);
                }
            }
        });
    };
}

/// when adding to this module, make sure to update dttlib.pyi in the root directory 
#[pymodule]
fn dttlib(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(init, m)?)?;
    m.add_function(wrap_pyfunction!(default_fft_params, m)?)?;
    m.add_class::<PipDuration>()?;
    m.add_class::<PipInstant>()?;
    m.add_class::<ViewSet>()?;
    m.add_class::<Channel>()?;
    m.add_class::<NDS2Cache>()?;
    m.add_class::<DataFlow>()?;
    m.add_class::<NDSDataType>()?;
    m.add_class::<ResponseToUser>()?;
    m.add_class::<ChannelQuery>()?;
    m.add_class::<ChannelType>()?;
    m.add_class::<AnalysisResult>()?;
    m.add_class::<InlineFFTParams>()?;
    m.add_class::<FFTWindow>()?;
    m.add_class::<MessageJob>()?;
    m.add_class::<UserMessage>()?;
    m.add_class::<ScopeViewHandle>()?;
    let types = PyModule::new(m.py(), "types".into())?;
    dtt_types(&types)?;
    m.add_submodule(&types)?;
    Ok(())
}