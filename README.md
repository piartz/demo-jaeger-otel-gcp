# demo-jaeger-otel-gcp
Environment to demo how an OTEL collector can collect data from a Jaeger collector and visualize it on GCP

# Minikube Jaeger → OTEL → GCP Cloud Trace

## Prerequisites
- [ ] GCP Project with Cloud Trace API enabled
- [ ] Create Service Account with `Cloud Trace Agent` role
- [ ] Download JSON credentials
- [ ] Install: `kubectl`, `minikube`, `gcloud`

## Setup
```bash
minikube start --driver=docker
kubectl config use-context minikube
kubectl apply -f jaeger/jaeger.yaml
kubectl create secret generic gcp-creds \
  --from-file=creds.json=gcp/YOUR_SERVICE_ACCOUNT.json
kubectl apply -f otel-collector/
```

## Test Trace
Send sample traces to Jaeger:
```bash
kubectl port-forward svc/jaeger 16686:16686 # Forward Jaeger UI port
```
Open `http://127.0.0.1:16686`
From the Jaeger UI, upload `trace-demo.json` to Jaeger.

To prove OTEL is collecting this data

## View in GCP
Visit [Cloud Trace Console](https://console.cloud.google.com/traces/list) to see the traces.
