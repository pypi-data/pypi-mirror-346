// Copyright 2025 EvoBandits
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

use pyo3::exceptions::PyRuntimeError;
use pyo3::prelude::*;
use pyo3::types::PyList;
use std::panic;

use evobandits_rust::arm::OptimizationFn;
use evobandits_rust::evobandits::EvoBandits as RustEvoBandits;
use evobandits_rust::genetic::{
    GeneticAlgorithm, CROSSOVER_RATE_DEFAULT, MUTATION_RATE_DEFAULT, MUTATION_SPAN_DEFAULT,
    POPULATION_SIZE_DEFAULT,
};

struct PythonOptimizationFn {
    py_func: PyObject,
}

impl PythonOptimizationFn {
    fn new(py_func: PyObject) -> Self {
        Self { py_func }
    }
}

impl OptimizationFn for PythonOptimizationFn {
    fn evaluate(&self, action_vector: &[i32]) -> f64 {
        Python::with_gil(|py| {
            let py_list = PyList::new(py, action_vector);
            let result = self
                .py_func
                .call1(py, (py_list.unwrap(),))
                .expect("Failed to call Python function");
            result.extract::<f64>(py).expect("Failed to extract f64")
        })
    }
}

#[pyclass(eq)]
#[derive(Debug, PartialEq)]
struct EvoBandits {
    evobandits: RustEvoBandits,
}

#[pymethods]
impl EvoBandits {
    #[new]
    #[pyo3(signature = (
        population_size=POPULATION_SIZE_DEFAULT,
        mutation_rate=MUTATION_RATE_DEFAULT,
        crossover_rate=CROSSOVER_RATE_DEFAULT,
        mutation_span=MUTATION_SPAN_DEFAULT,
    ))]
    fn new(
        population_size: Option<usize>,
        mutation_rate: Option<f64>,
        crossover_rate: Option<f64>,
        mutation_span: Option<f64>,
    ) -> PyResult<Self> {
        let genetic_algorithm = GeneticAlgorithm {
            population_size: population_size.unwrap(),
            mutation_rate: mutation_rate.unwrap(),
            crossover_rate: crossover_rate.unwrap(),
            mutation_span: mutation_span.unwrap(),
            ..Default::default()
        };
        let evobandits = RustEvoBandits::new(genetic_algorithm);
        Ok(EvoBandits { evobandits })
    }

    #[pyo3(signature = (
        py_func,
        bounds,
        simulation_budget,
        seed=None,
    ))]
    fn optimize(
        &mut self,
        py_func: PyObject,
        bounds: Vec<(i32, i32)>,
        simulation_budget: usize,
        seed: Option<u64>,
    ) -> PyResult<Vec<i32>> {
        let py_opti_function = PythonOptimizationFn::new(py_func);

        let result = panic::catch_unwind(std::panic::AssertUnwindSafe(|| {
            self.evobandits
                .optimize(py_opti_function, bounds, simulation_budget, seed)
        }));

        match result {
            Ok(v) => Ok(v),
            Err(err) => {
                if let Some(s) = err.downcast_ref::<&str>() {
                    Err(PyRuntimeError::new_err(format!("{}", s)))
                } else if let Some(s) = err.downcast_ref::<String>() {
                    Err(PyRuntimeError::new_err(format!("{}", s)))
                } else {
                    Err(PyRuntimeError::new_err(
                        "EvoBandits Core raised an Error with unknown cause.",
                    ))
                }
            }
        }
    }
}

#[pymodule]
fn evobandits(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<EvoBandits>()?;

    m.add("POPULATION_SIZE_DEFAULT", POPULATION_SIZE_DEFAULT)?;
    m.add("MUTATION_RATE_DEFAULT", MUTATION_RATE_DEFAULT)?;
    m.add("CROSSOVER_RATE_DEFAULT", CROSSOVER_RATE_DEFAULT)?;
    m.add("MUTATION_SPAN_DEFAULT", MUTATION_SPAN_DEFAULT)?;

    Ok(())
}
