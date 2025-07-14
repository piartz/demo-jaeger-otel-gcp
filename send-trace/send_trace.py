from jaeger_client import Config
import time

def init_tracer(service):
    config = Config(
        config={
            'sampler': {'type': 'const', 'param': 1},
            'logging': True,
            'reporter_batch_size': 1,
            'collector_endpoint': 'http://jaeger-proxy:14268/api/traces',  # ✔️ top-level key
        },
        service_name=service,
        validate=True,
    )
    return config.initialize_tracer()

if __name__ == "__main__":
    print("[DEBUG] Starting trace sending process...")
    tracer = init_tracer('mock-service')
    with tracer.start_span('mock-operation') as span:
        span.set_tag('demo.key', 'demo.value')
        print("[DEBUG] Span created.")
        time.sleep(1)
    tracer.close()
    print("[DEBUG] Tracer closed, waiting for flush...")
    time.sleep(5)
    print("[DEBUG] Done.")
