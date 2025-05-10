use binrw::binrw;

#[cfg(feature = "pyo3")]
use pyo3::prelude::*;

#[binrw]
#[derive(Debug, Clone)]
#[cfg_attr(feature = "pyo3", pyo3::pyclass(get_all, set_all))]
pub struct SetDoutsRequest {
    pub bin_layout: u16,
}

#[cfg(feature = "pyo3")]
#[pymethods]
impl SetDoutsRequest {
    #[new]
    pub fn new(bin_layout: u16) -> Self {
        Self { bin_layout }
    }
}

#[binrw]
#[brw(big)]
#[derive(Debug, Clone)]
#[cfg_attr(feature = "pyo3", pyo3::pyclass(get_all, set_all))]
pub struct SetDoutsResponse {
    pub success: u8,
}

#[cfg(feature = "pyo3")]
#[pymethods]
impl SetDoutsResponse {
    #[new]
    pub fn new(success: u8) -> Self {
        Self { success }
    }
}

#[cfg(feature = "pyo3")]
#[pyfunction]
#[pyo3(name = "set_do_request")]
pub fn set_do_py(bin_state: u16, id: u32) -> Vec<u8> {
    hal_common::packets::Request::with_id(
        crate::do_mod::packets::Request::SetDouts(
            SetDoutsRequest{bin_layout: bin_state}
        ),
        id,
    )
    .into(0 as u8)
    .as_bytes()
}

#[cfg(feature = "pyo3")]
pub(crate) fn pymodule(py: Python) -> PyResult<pyo3::Bound<'_, pyo3::types::PyModule>> {
    PyModule::new(py, "set_do").map(|module| {
        module.add_class::<SetDoutsRequest>()?;
        module.add_class::<SetDoutsResponse>()?;
        Ok(module)
    })?
}
