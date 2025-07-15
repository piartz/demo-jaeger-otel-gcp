# Demo: Jaeger & OpenTelemetry Collector on Kubernetes

This demo shows how to deploy Jaeger and the OpenTelemetry Collector to a local Kubernetes cluster (using minikube).
You can generate and visualize distributed traces using telemetrygen.

---

## Prerequisites

- Docker
- kubectl
- minikube
- python3, pip (optional, for generating traces from an instrumented app)

---

## Setup (Minikube)

1. Start minikube:

   `minikube start`

2. (Optional) Use minikube's Docker daemon:

   `eval $(minikube docker-env)`

---

## Deploy Jaeger & OTEL Collector

1. Apply the YAML file:

   `kubectl apply -f jaeger-otel.yaml`

2. Wait for all pods to be running:

   `kubectl get pods`

   Example output:
   ```
     NAME                              READY   STATUS    RESTARTS   AGE
     jaeger-xxxxxxxxx-xxxxx            1/1     Running   0          1m
     otel-collector-xxxxxxxxx-xxxxx    1/1     Running   0          1m
    ```
---

## Generate Test Traces

### gRPC
You can use telemetrygen to generate gRPC traces and send them to the OTEL collector.

Port-forward OTEL collector and use localhost:

  `kubectl port-forward svc/otel-collector 4317:4317`

  In a separate terminal:
```bash
  docker run --rm -it ghcr.io/open-telemetry/opentelemetry-collector-contrib/telemetrygen:latest \
    traces \
    --otlp-endpoint host.docker.internal:4317 \
    --otlp-insecure \
    --duration 10s
```

### HTTP

If we want to generate traffic on 14268 (HTTP, Jaeger Thrift over TCP) we can instrument an app with the `opentelemetry` SDK. `jaeger_client` has been deprecated since 2022, and Jaeger urges its users to replace exporters in favor of native OTEL. 

We have a python example in `jaeger-client-trace.py`. We will still be using a Jaeger Exporter, within the OTEL SDK, as a way to emulate Jaeger-formatted traffic within the OTEL collector.

Setting up a venv is the easiest way to bootstrap this app:
```bash
python3 -m venv ~/venvs/jaeger-demo && source ~/venvs/jaeger-demo/bin/activate
pip install opentelemetry-exporter-jaeger-thrift deprecated
```
Port forward in Kubernetes:
`kubectl port-forward svc/otel-collector 14268:14268`

After the setup, just run it as usual
`python jaeger-client-trace.py`

### UDP

Since this demo is based on `minikube`, exposing UDP ports via `kubectl port-forward` is not possible. Nonetheless, you can experiment within your cluster with a Jaeger agent and UDP traffic.

---

## View Traces in Jaeger UI

The current configuration exports all traces in Zipkin format to a Jaeger collector (port 9411), and then visualized via Jaeger UI.

1. Port-forward the Jaeger UI:

   `kubectl port-forward svc/jaeger 16686:16686`

2. Open your browser to:

   `http://localhost:16686`

3. Search for traces:
   In the Jaeger UI, select a service (e.g. "telemetrygen-server" or "otel-demo") and click "Find Traces".

---

## Troubleshooting

- No traces in Jaeger UI?
  - Ensure both Jaeger and OTEL collector pods are running.
  - Check OTEL collector logs:
      `kubectl logs deployment/otel-collector`
  - Check Jaeger logs:
      `kubectl logs deployment/jaeger`
  - Double-check the endpoint and port you’re sending traces to.
  - If using Docker on Mac/Windows, use host.docker.internal in telemetrygen.

- Port-forwarding fails or is disconnected?
  - Restart the port-forward command.
  - Pods must be running (not restarting or pending).

