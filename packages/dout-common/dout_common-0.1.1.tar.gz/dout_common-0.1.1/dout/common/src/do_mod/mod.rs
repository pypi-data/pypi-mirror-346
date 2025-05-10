pub mod packets;

#[cfg(feature = "pyo3")]
use pyo3::prelude::*;

#[cfg(feature = "pyo3")]
pub(crate) fn pymodule(py: Python) -> PyResult<pyo3::Bound<'_, pyo3::types::PyModule>> {
    PyModule::new(py, "do_mod").map(|module| {
        let submodule = &packets::pymodule(py)?;
        py.import("sys")?
            .getattr("modules")?
            .set_item("dout_common.do_mod.packets", submodule)?;
        module.add_submodule(submodule)?;
        Ok(module)
    })?
}
