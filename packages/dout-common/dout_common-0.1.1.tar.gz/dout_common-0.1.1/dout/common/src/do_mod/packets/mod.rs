use binrw::binrw;
use get_do::{GetDoutsRequest, GetDoutsResponse};
use hal_common::packets::{BaseId, Cmd, Header};
use set_do::{SetDoutsRequest, SetDoutsResponse};

pub mod get_do;
pub mod set_do;

const BASE_ID: u8 = 0x20;

#[binrw]
#[brw(big)]
#[br(import(header: &Header, _len: usize))]
#[derive(Debug, Clone)]
#[cfg_attr(feature = "pyo3", pyo3::pyclass(get_all, set_all))]
pub enum Request {
    #[br(pre_assert(header.cmd == 0x00))]
    GetDouts(GetDoutsRequest),

    #[br(pre_assert(header.cmd == 0x01))]
    SetDouts(SetDoutsRequest),
}

impl BaseId for Request {
    fn base_id() -> u8 {
        BASE_ID
    }
}

impl Cmd for Request {
    fn cmd(&self) -> u8 {
        match self {
            Request::GetDouts(_) => 0x00,
            Request::SetDouts(_) => 0x01,
        }
    }
}

#[cfg(feature = "pyo3")]
#[pymethods]
impl Request {
    #[staticmethod]
    pub fn base_id() -> u8 {
        <Request as BaseId>::base_id()
    }

    pub fn cmd(&self) -> u8 {
        <Request as Cmd>::cmd(&self)
    }
}

#[binrw]
#[br(big, import(header: &Header, _len: usize))]
#[derive(Debug, Clone)]
#[cfg_attr(feature = "pyo3", pyo3::pyclass(get_all, set_all))]
pub enum Response {
    #[br(pre_assert(header.cmd == 0x00))]
    GetDouts(GetDoutsResponse),

    #[br(pre_assert(header.cmd == 0x01))]
    SetDouts(SetDoutsResponse),
}

impl BaseId for Response {
    fn base_id() -> u8 {
        BASE_ID
    }
}

impl Cmd for Response {
    fn cmd(&self) -> u8 {
        match self {
            Response::GetDouts(_) => 0x00,
            Response::SetDouts(_) => 0x01,
        }
    }
}

#[cfg(feature = "pyo3")]
#[pymethods]
impl Response {
    #[staticmethod]
    pub fn base_id() -> u8 {
        <Response as BaseId>::base_id()
    }

    pub fn cmd(&self) -> u8 {
        <Response as Cmd>::cmd(&self)
    }
}

#[cfg(feature = "pyo3")]
use pyo3::prelude::*;

#[cfg(feature = "pyo3")]
pub(crate) fn pymodule(py: Python) -> PyResult<pyo3::Bound<'_, pyo3::types::PyModule>> {
    PyModule::new(py, "packets").map(|module| {
        let submodule = &get_do::pymodule(py)?;
        py.import("sys")?
            .getattr("modules")?
            .set_item("dout_common.do_mod.packets.get_do", submodule)?;
        module.add_submodule(submodule)?;
        let submodule = &set_do::pymodule(py)?;
        py.import("sys")?
            .getattr("modules")?
            .set_item("dout_common.do_mod.packets.set_do", submodule)?;
        module.add_submodule(submodule)?;
        module.add_class::<Request>()?;
        module.add_class::<Response>()?;
        Ok(module)
    })?
}
