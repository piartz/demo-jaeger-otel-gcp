# demo-jaeger-otel-gcp
Environment to demo how an OTEL collector can collect data from a Jaeger collector and visualize it on GCP

# Minikube Jaeger → OTEL → GCP Cloud Trace

## 🔧 Prerequisites
- [ ] GCP Project with Cloud Trace API enabled
- [ ] Create Service Account with `Cloud Trace Agent` role
- [ ] Download JSON credentials
- [ ] Install: `kubectl`, `minikube`, `gcloud`

## 🚀 Setup

```bash
minikube start --cpus=2 --memory=4g
kubectl apply -f jaeger/jaeger.yaml
kubectl create secret generic gcp-creds \
  --from-file=creds.json=gcp/YOUR_SERVICE_ACCOUNT.json
kubectl apply -f otel-collector/
```

## 🔍 Test Trace
Send sample traces to Jaeger:
```bash
curl -X POST http://$(minikube service jaeger --url | grep 14268)/api/traces \
  -H 'Content-Type: application/json' \
  -d '{ "traceId": "...", "spans": [...] }'
```

## 📊 View in GCP
Visit [Cloud Trace Console](https://console.cloud.google.com/traces/list) to see the traces.
