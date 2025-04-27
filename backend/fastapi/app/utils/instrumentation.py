from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor

from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

from opentelemetry import trace


def setup_otel(app):
    # Set up automatic instrumentation
    FastAPIInstrumentor.instrument_app(app)
    RequestsInstrumentor().instrument()
    LoggingInstrumentor().instrument(set_logging_format=True)

    # Define a resource for the service
    resource = Resource.create(attributes={"service.name": "fastapi-app"})

    # Set up the tracer provider
    tracer_provider = TracerProvider(resource=resource)
    trace.set_tracer_provider(tracer_provider)

    # Configure OTLP exporter to send traces to otel-lgtm
    otlp_exporter = OTLPSpanExporter(endpoint="http://otel-lgtm:4317", insecure=True)
    span_processor = BatchSpanProcessor(otlp_exporter)
    tracer_provider.add_span_processor(span_processor)
