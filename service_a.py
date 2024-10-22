# service_a.py
from fastapi import FastAPI
import requests
from opentelemetry import trace
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.jaeger.thrift import JaegerExporter

app = FastAPI()

# Initialize Tracer Provider
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)

# Configure Jaeger Exporter
jaeger_exporter = JaegerExporter(agent_host_name="jaeger", agent_port=6831)
span_processor = BatchSpanProcessor(jaeger_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

# Instrument requests library
RequestsInstrumentor().instrument()

@app.get("/")
def root():
    with tracer.start_as_current_span("Service A Root Request"):
        response = requests.get("http://service-b:8000/")
        return {"message": "Hello from Service A", "Service B response": response.json()}
