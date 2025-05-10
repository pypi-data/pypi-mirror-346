use prost::Message;
//use pyo3::ffi::c_str;
use pyo3::prelude::*;
use pyo3::types::{IntoPyDict, PyAny, PyDict, PyString, PyTuple};

mod otlp {
    pub mod common {
        pub mod v1 {
            include!(concat!(
                env!("OUT_DIR"),
                "/opentelemetry.proto.common.v1.rs"
            ));
        }
    }
    pub mod resource {
        pub mod v1 {
            include!(concat!(
                env!("OUT_DIR"),
                "/opentelemetry.proto.resource.v1.rs"
            ));
        }
    }
    pub mod trace {
        pub mod v1 {
            include!(concat!(env!("OUT_DIR"), "/opentelemetry.proto.trace.v1.rs"));
        }
    }
    pub mod collector {
        pub mod trace {
            pub mod v1 {
                include!(concat!(
                    env!("OUT_DIR"),
                    "/opentelemetry.proto.collector.trace.v1.rs"
                ));
            }
        }
    }
}

use crate::otlp::{
    collector::trace::v1::ExportTraceServiceRequest,
    common::v1::{AnyValue, InstrumentationScope, KeyValue, any_value::Value},
    resource::v1::Resource,
    trace::v1::{ResourceSpans, ScopeSpans, Span, Status, span::SpanKind},
};

/// Convert something that satisfies Python dict[str, str] protocol.
/// Must be done with a hack, because OTEL attributes are a mapping, not a dict.
fn dict_like_to_kv(py_mapping: &Bound<'_, PyAny>) -> PyResult<Vec<KeyValue>> {
    let items = py_mapping.call_method0("items")?.try_iter()?;
    Ok(items
        .filter_map(|item| {
            let pair = item.ok()?;
            let key = pair.get_item(0).ok()?.extract::<String>().ok()?;
            let v = pair.get_item(1).ok()?;

            // https://opentelemetry.io/docs/specs/otel/common/attribute-type-mapping/
            let value = if let Ok(b) = v.extract::<bool>() {
                Value::BoolValue(b)
            } else if let Ok(n) = v.extract::<i64>() {
                Value::IntValue(n)
            } else if let Ok(f) = v.extract::<f64>() {
                Value::DoubleValue(f)
            } else if let Ok(s) = v.extract::<String>() {
                Value::StringValue(s)
            // FIXME: Yes, bytes are now allowed!
            // https://github.com/open-telemetry/opentelemetry-specification/blob/main/specification/common/README.md
            } else if let Ok(b) = v.extract::<Vec<u8>>() {
                Value::BytesValue(b)
            // FIXME: not sure about this, would this not break out for a bad value?
            } else if let Ok(s) = v.str().ok()?.extract::<String>() {
                Value::StringValue(s)
            } else {
                // FIXME: the attribute type mapping appears to suggest that empty values
                // are OK, yielding an AnyValue with every field unset
                // However, I think that OTLP spec is clear that attributes should only be
                // bool|int|float|str or a homogeneous array thereof.
                return None;
            };
            // FIXME: arrays of things... to ArrayValue
            // FIXME: mappings of things... to KeyValueList

            Some(KeyValue {
                key,
                value: Some(AnyValue { value: Some(value) }),
            })
        })
        .collect())
}

#[pyfunction]
#[pyo3(signature = (resource_cache, scope_cache, span))]
fn _linearise(
    py: Python<'_>,
    resource_cache: Bound<'_, PyDict>,
    scope_cache: Bound<'_, PyDict>,
    span: Bound<'_, PyAny>,
) -> PyResult<PyObject> {
    let builtins = PyModule::import(py, "builtins")?;
    let r = span.getattr("resource")?;
    if !resource_cache.contains(r.as_ref())? {
        resource_cache.set_item(
            r.as_ref(),
            PyTuple::new(
                py,
                &[
                    &r.getattr("schema_url")?,
                    &builtins.call_method1(
                        "tuple",
                        (r.getattr("attributes")?.call_method0("items")?,),
                    )?,
                ],
            )?,
        )?;
    }
    let s = span.getattr("instrumentation_scope")?;
    if !scope_cache.contains(s.as_ref())? {
        scope_cache.set_item(
            s.as_ref(),
            PyTuple::new(
                py,
                &[
                    &s.getattr("schema_url")?,
                    &s.getattr("name")?,
                    &s.getattr("version")?,
                    &builtins.call_method1(
                        "tuple",
                        (r.getattr("attributes")?.call_method0("items")?,),
                    )?,
                ],
            )?,
        )?;
    }

    let rv = PyTuple::new(
        py,
        &[
            &resource_cache.get_item(r.as_ref())?,
            &scope_cache.get_item(s.as_ref())?,
        ],
    )?;
    Ok(rv.into_any().unbind())
}

/// Encode `sdk_spans` into an OTLP 1.5 Protobuf, serialise and return `bytes`.
///
/// Args:
///     sdk_spans: Sequence[opentelemetry.sdk.trace.ReadableSpan],
///
/// Returns:
///     bytes(opentelemetry/proto/collector/trace/v1/trace_service.proto:ExportTraceServiceRequest)
#[pyfunction]
#[pyo3(signature = (sdk_spans), pass_module)]
fn encode_spans(m: &Bound<'_, PyModule>, sdk_spans: &Bound<'_, PyAny>) -> PyResult<Vec<u8>> {
    //fn encode_spans(sdk_spans: &Bound<'_, PyAny>) -> PyResult<Vec<u8>> {
    // Incoming data shape:
    // spans[]:
    //   span{}:
    //     resource{}:
    //       attributes{}
    //     instrumentation_scope{}:
    //       ...
    //     trace_id: int
    //     ...
    //
    // Outgoing data shape:
    // ExportTracesServiceRequest{}:
    //   resource_spans[]:
    //     ResourceSpans{}:
    //       Resource{}
    //         attributes: ...
    //         ...
    //       schema_url: str
    //       scope_spans[]:
    //         ScopeSpans{}:
    //           scope: InstrumentationScope{}:
    //             ...
    //           schema_url: str
    //           spans[]:
    //             Span{}:
    //               trace_id: bytes
    //               ...
    //
    // We don't have to preserve the original order of spans, so we're sorting them
    // by resource and instrumentation scope.
    // That groups spans by their ancestry, and emission is done in a simple loop.

    Python::with_gil(|py| {
        let builtins = PyModule::import(py, "builtins")?;
        let resource_cache = PyDict::new(py);
        let scope_cache = PyDict::new(py);
        let key = m.getattr("functools")?.call_method1(
            "partial",
            (m.getattr("_linearise")?, resource_cache, scope_cache),
        )?;
        let kwargs = [("key", key)].into_py_dict(py)?;
        let spans = builtins.call_method("sorted", (sdk_spans.as_ref(),), Some(&kwargs))?;

        let mut last_resource = py.None().into_pyobject(py)?;
        let mut last_scope = py.None().into_pyobject(py)?;
        let mut request = ExportTraceServiceRequest {
            resource_spans: Vec::new(),
            ..Default::default()
        };

        for item in spans.try_iter()? {
            let span = item?;
            // .resource cannot be None
            if !span.getattr("resource")?.is(&last_resource) {
                last_resource = span.getattr("resource")?;
                last_scope = py.None().into_pyobject(py)?;

                request.resource_spans.push(ResourceSpans {
                    resource: Some(Resource {
                        attributes: dict_like_to_kv(&last_resource.getattr("attributes")?)?,
                        // dropped_attribute_count: ...
                        ..Default::default()
                    }),
                    scope_spans: Vec::new(),
                    // schema_url: ...
                    ..Default::default()
                });
            }
            // .instrumentation_scope cannot be None
            if !span.getattr("instrumentation_scope")?.is(&last_scope) {
                last_scope = span.getattr("instrumentation_scope")?;

                request
                    .resource_spans
                    .last_mut()
                    .expect(".resource_spans can't be empty")
                    .scope_spans
                    .push(ScopeSpans {
                        scope: Some(InstrumentationScope {
                            // TODO can name be missing?
                            name: last_scope.getattr("name")?.extract::<String>()?,
                            // TODO what if the version is missing?
                            version: last_scope.getattr("version")?.extract::<String>()?,
                            // schema_url: ...
                            ..Default::default()
                        }),
                        spans: Vec::new(),
                        // schema_url: ...
                        ..Default::default()
                    });
            }

            let context = span.getattr("context")?;
            let status = span.getattr("status")?;

            request
                .resource_spans
                .last_mut()
                .expect(".resource_spans can't be empty")
                .scope_spans
                .last_mut()
                .expect(".scope_spans can't be empty")
                .spans
                .push(Span {
                    trace_id: context
                        .getattr("trace_id")?
                        .extract::<u128>()?
                        .to_be_bytes()
                        .to_vec(),
                    span_id: context
                        .getattr("span_id")?
                        .extract::<u64>()?
                        .to_be_bytes()
                        .to_vec(),
                    // FIXME: parent_span_id = span.parent?.span_id or unset
                    // TODO: context.trace_state??
                    name: span.getattr("name")?.extract::<String>()?,
                    kind: span
                        .getattr("kind")
                        .and_then(|k| k.extract::<i32>())
                        // TODO: special logic for remote spans?
                        .unwrap_or(SpanKind::Internal as i32),
                    start_time_unix_nano: span
                        .getattr("start_time")
                        .and_then(|t| t.extract::<u64>())
                        .unwrap_or_default(),
                    end_time_unix_nano: span
                        .getattr("end_time")
                        .and_then(|t| t.extract::<u64>())
                        .unwrap_or_default(),
                    flags: span
                        .getattr("flags") // FIXME: span.parent?.WTF
                        .and_then(|f| f.extract::<u32>())
                        .unwrap_or(256),
                    // TODO:
                    // - dropped_attributes_count
                    // - events
                    // - dropped_events_count
                    // - links
                    // - dropped_links_count
                    // TODO: Python drops this struct if the field is None
                    status: Some(Status {
                        // status is always set, and status_code too
                        code: status
                            .getattr("status_code")?
                            .getattr("value")?
                            .extract::<i32>()?,
                        // logically optional. empty str or none?
                        message: status
                            .getattr("description")
                            .ok()
                            .and_then(|d| d.extract::<String>().ok())
                            .unwrap_or_default(),
                        ..Default::default()
                    }),
                    ..Default::default()
                });
        }

        Ok(request.encode_to_vec())
    })
    // FIXME TODO
    // Events
    // Baggage
    // Links
}

#[pyfunction]
fn test_tuple(py: Python<'_>, arg: Bound<'_, PyAny>) -> PyResult<PyObject> {
    let builtins = PyModule::import(py, "builtins")?;
    let rv = builtins.call_method1("tuple", (arg.as_ref(),))?;
    Ok(rv.unbind())
}

/// 🐍Lightweight OTEL span to binary converter, written in Rust🦀
#[pymodule(gil_used = false)]
fn otlp_proto(m: &Bound<'_, PyModule>) -> PyResult<()> {
    Python::with_gil(|py| -> PyResult<()> {
        m.add("CONTENT_TYPE", PyString::new(py, "application/x-protobuf"))?;
        m.add("functools", py.import("functools")?)?;
        Ok(())
    })?;
    m.add_function(wrap_pyfunction!(encode_spans, m)?)?;
    m.add_function(wrap_pyfunction!(test_tuple, m)?)?;
    m.add_function(wrap_pyfunction!(_linearise, m)?)?;
    Ok(())
}
