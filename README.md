# Spark on Kubernetes (Demo)

This repo contains a small PySpark demo packaged for execution on Kubernetes using the Spark Operator.

Included files:
- `Dockerfile` (builds the Spark image that runs `app.py`)
- `app.py` (PySpark job; designed to keep the pod alive for observation)
- `spark-app.yaml` (`SparkApplication` custom resource)
- `spark-role.yaml` + `spark-role-binding.yaml` (RBAC for the service account)

## What to apply (high level)
1. RBAC (`spark-role.yaml` and `spark-role-binding.yaml`)
2. Spark job CR (`spark-app.yaml`)

## Prerequisites
- Kubernetes cluster with the Spark Operator installed (so `SparkApplication` CRDs exist).
- `kubectl` configured to point to the target cluster.
- A container registry accessible by your Kubernetes nodes (or your cluster can pull from wherever you push the image).
- Docker (or any compatible tool) to build the image.

## 1) Build and push the image
The `spark-app.yaml` refers to an image named `spark-py-demo:latest`.

### Build
```bash
docker build -t spark-py-demo:latest .
```

### Push
Tag and push to your registry (example only):
```bash
docker tag spark-py-demo:latest <YOUR_REGISTRY>/spark-py-demo:latest
docker push <YOUR_REGISTRY>/spark-py-demo:latest
```

### Update YAML (recommended)
Edit `spark-app.yaml` and replace:
```yaml
image: spark-py-demo:latest
```
with your fully-qualified pushed image, for example:
```yaml
image: <YOUR_REGISTRY>/spark-py-demo:latest
```

## 2) Apply the Kubernetes resources
All YAMLs are in this folder, and the `spark-app.yaml` targets the `default` namespace.

```bash
kubectl apply -f spark-role.yaml -f spark-role-binding.yaml
kubectl apply -f spark-app.yaml
```

## 3) Verify
### Check the SparkApplication CR status
```bash
kubectl get sparkapplication -n default
```

### Watch pods created for the job
```bash
kubectl get pods -n default -w
```

### View Spark job logs
```bash
kubectl logs -n default -l sparkoperator.k8s.io/app-name=spark-demo --all-containers=true
```

## Cleaning up
```bash
kubectl delete -f spark-app.yaml
kubectl delete -f spark-role-binding.yaml -f spark-role.yaml
```

## Customization knobs
In `spark-app.yaml` you can adjust:
- `metadata.name` and `metadata.namespace`
- `spec.executor.instances`, `spec.executor.cores`, `spec.executor.memory`
- `spec.driver.cores`, `spec.driver.memory`
- `spec.sparkVersion`

