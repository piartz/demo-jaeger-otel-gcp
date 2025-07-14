#!/bin/bash

echo "[INFO] Deleting previous job and pod..."
kubectl delete job send-mock-trace --ignore-not-found

# Wait for pods to actually terminate
echo "[INFO] Waiting for old pods to terminate..."
while kubectl get pods -l job-name=send-mock-trace | grep -q 'send-mock-trace'; do
  echo -n "."
  sleep 1
done
echo -e "\n[INFO] Old pods deleted."

echo "[INFO] Rebuilding Docker image without cache..."
docker build --no-cache -t send-trace:local .

echo "[INFO] Loading image into Minikube..."
minikube image load send-trace:local

echo "[INFO] Applying job YAML..."
kubectl apply -f trace-job.yaml
sleep 2

echo "[INFO] Pods for send-mock-trace:"
kubectl get pods -l job-name=send-mock-trace
