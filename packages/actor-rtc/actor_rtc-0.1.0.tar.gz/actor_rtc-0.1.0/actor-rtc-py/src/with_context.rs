use pyo3::exceptions::PyRuntimeError;
use pyo3::prelude::*;

/// Trait to add context to Result types
pub trait WithContext<T, E> {
    fn context(self, context: &str) -> PyResult<T>;
}

impl<T, E> WithContext<T, E> for Result<T, E>
where
    E: std::fmt::Debug,
{
    fn context(self, context: &str) -> PyResult<T> {
        self.map_err(|e| PyRuntimeError::new_err(format!("{}: {:?}", context, e)))
    }
}
