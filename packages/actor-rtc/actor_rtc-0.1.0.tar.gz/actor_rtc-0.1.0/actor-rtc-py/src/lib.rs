mod config;
mod with_context;
mod wrapper;

use crate::config::*;
use crate::wrapper::*;
use pyo3::prelude::*;
use pyo3_stub_gen::define_stub_info_gatherer;

#[pymodule]
fn actor_rtc(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<Config>()?;
    m.add_class::<RTCIceServer>()?;
    m.add_class::<Actor>()?;
    m.add_class::<ActorDesc>()?;
    m.add_class::<Message>()?;
    m.add_class::<Network>()?;
    Ok(())
}

// Define a function to gather stub information.
define_stub_info_gatherer!(stub_info);
