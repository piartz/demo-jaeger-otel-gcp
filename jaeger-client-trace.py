from opentelemetry import trace
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.exporter.jaeger.thrift import JaegerExporter

# Set up tracer provider with service name
trace.set_tracer_provider(
    TracerProvider(
        resource=Resource.create({SERVICE_NAME: "otel-demo"})
    )
)

# Use JaegerExporter in collector (HTTP) mode!
jaeger_exporter = JaegerExporter(
    collector_endpoint="http://localhost:14268/api/traces"
)

trace.get_tracer_provider().add_span_processor(
    SimpleSpanProcessor(jaeger_exporter)
)

tracer = trace.get_tracer(__name__)

with tracer.start_as_current_span("my-first-span"):
    print("This is an event within the trace")
