

# Flask-app

A minimal Flask application packaged for Docker and deployable with Helm.

## Overview
- The app serves a basic HTML page whose header is read from a Kubernetes ConfigMap key named `CUSTOM_HEADER` inside the container.
- In case the app is deployed locally using Docker, the value for CUSTOM_HEADER will default to "Default header" unless passed as env var in docker run.
- The Helm chart lives at `charts/flaskapp` and uses these `values.yaml` keys (defaults present in the repo):
  - `appName` — logical name used for resources (default: `flaskapp`).
  - `image.name` and `image.tag` — image repo and tag used by the Deployment.
  - `configmap.name` and `configmap.data.CUSTOM_HEADER` — ConfigMap name and data.

## Build and run with local docker

```bash
docker build -t flaskapp:latest .
docker run -e CUSTOM_HEADER="My Custom Value" -p 3000:3000 flaskapp:latest

# open http://localhost:3000
```

## Build and run on K8s cluster

### Build locally

```bash
# Option A: Switch Docker CLI to Minikube's daemon and build directly in Minikube
eval $(minikube docker-env)
docker build -t flaskapp:latest .  

# Option B: Build image on local docker and copy it to Minikube (also case if image already built locally)
docker build -t flaskapp:latest .  
minikube image load flaskapp:latest  # 
```

### Build on Dockerhub
```bash
docker login --username  <DockerHub-Username> 
docker build --no-cache -t <DockerHub-Username>/flaskapp:latest .
docker push <DockerHub-Username>/flaskapp:latest
```

### Run app using Helm:

```bash
# Helm install
helm install flaskapp-helm ./charts/flaskapp --set configmap.data.CUSTOM_HEADER="My Custom Value"
# or
helm install flaskapp-helm ./charts/flaskapp

# Uninstall
helm list
helm uninstall flaskapp-helm
```

### Access the app:

```bash
# Option A:  Automatically finds your Minikube IP and opens the app in browser automatically
minikube service flaskapp -n helm-tutorial

# Option B: Get Minikube IP
minikube ip
# Returns something like: 192.168.49.2

# Then open: http://192.168.49.2:30080
```
**Notes:** 
- The chart's Service currently exposes a NodePort:
  - service `port`: 3000
  - `targetPort`: 3000 (container)
  - `nodePort`: 30080

- Access options:
  - NodePort: open `http://<node-ip>:30080` (or use your cloud provider's Node IP).
  - Port-forward the service to localhost:
```
kubectl port-forward service/flaskapp 3000:80 
```

### Update the app:
- To set or change the app header via Helm chart (this updates the ConfigMap created by the chart):

```bash
helm upgrade --install flaskapp-helm ./charts/flaskapp --set configmap.data.CUSTOM_HEADER="This was changed using helm upgrade" 
```
**Important notes:** 
  - configmap are *immuntable* so you will need to restart the pod to see the change.
  - alternatively, you can rename the configmap which will restart the pod automatically.
  
 Ex: helm upgrade --install flaskapp-helm ./charts/flaskapp \
  --set configmap.data.CUSTOM_HEADER="This header comes from helm upgrade" \
  --set configmap.name="newcfgmap" 



## Tips & troubleshooting
- Replace image name to include a dockerhub repository and build directly to it:
```bash
docker build -t <DockerHub-Username>/flaskapp:latest .  
```
- If pods fail with image pull errors, confirm the image name/tag is published and reachable. Example to test locally:
```bash
docker pull <DockerHub-Username>/flaskapp:latest
```
- Private registry: create a Docker registry secret and add it to the chart via `imagePullSecrets` (or pass it into the rendered manifest).
- Preview rendered manifests without installing:
```bash
helm template my-flaskapp ./charts/flaskapp \
  --set image.name=<DOCKERHUB-REPO>/flaskapp --set image.tag=latest
```

Files of interest
- `app.py` — Flask app renders `templates/index.html`.
- `Dockerfile` — builds the image; exposes port 3000.
- `charts/flaskapp/values.yaml` — default chart values (edit or override with `--set`).
- `charts/flaskapp/templates/*` — Deployment, Service, ConfigMap templates used by Helm.



