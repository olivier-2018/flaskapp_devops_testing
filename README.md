

# Flask-app

A minimal Flask application packaged for Docker and deployable with Helm.

## Overview
- The app serves a basic HTML page whose header is read from a Kubernetes ConfigMap key named `CUSTOM_HEADER` inside the container.
- In case the app is deployed locally using Docker, the value for CUSTOM_HEADER will default to "Default header".
- The Helm chart lives at `charts/flaskapp` and uses these `values.yaml` keys (defaults present in the repo):
  - `appName` — logical name used for resources (default: `flaskapp`).
  - `image.name` and `image.tag` — image repo and tag used by the Deployment.
  - `configmap.name` and `configmap.data.CUSTOM_HEADER` — ConfigMap name and data.

## Build and run locally
- Build the image (replace `yourrepo`) and run with docker:

```bash
docker build -t yourrepo/flaskapp:latest .
docker run -p 5000:5000 -v "$PWD/dev-CUSTOM_HEADER.txt":/etc/config/CUSTOM_HEADER:ro yourrepo/flaskapp:dev
# open http://localhost:5000
```

## Deploy with Helm
- Basic install (replace `yourrepo`) :

```bash
docker build -t yourrepo/flaskapp:latest .
docker push yourrepo/flaskapp:latest 
helm install my-flaskapp ./charts/flaskapp \
  --set image.name=yourrepo/flaskapp --set image.tag=latest 

# See Notes:
# - Accessing the app requires a port-forward and open browser on localhost:5000
```

- Set or change the header via the chart (this updates the ConfigMap created by the chart):

```bash
helm upgrade --install my-flaskapp ./charts/flaskapp \
  --set configmap.data.CUSTOM_HEADER="This header comes from helm upgrade" 

# Notes: 
#  - configmap are immuntable so you will need to restart the pod to see the change.
#  - alternatively, you can rename the configmap which will restart the pod automatically.
# Ex: helm upgrade --install my-flaskapp ./charts/flaskapp \
#  --set configmap.data.CUSTOM_HEADER="This header comes from helm upgrade" \
#  --set configmap.name="newcfgmap" 
```

## Accessing the app

- The chart's Service currently exposes a NodePort:
  - service `port`: 3000
  - `targetPort`: 5000 (container)
  - `nodePort`: 30080

- Access options:
  - NodePort: open `http://<node-ip>:30080` (or use your cloud provider's Node IP).
  - Port-forward the service to localhost:

```bash
kubectl port-forward service/flaskapp 5000:80  
# then open http://localhost:5000
```

## Tips & troubleshooting
- If pods fail with image pull errors, confirm the image name/tag is published and reachable. Example to test locally:

```bash
docker pull yourrepo/flaskapp:latest
```

- Private registry: create a Docker registry secret and add it to the chart via `imagePullSecrets` (or pass it into the rendered manifest).
- Preview rendered manifests without installing:

```bash
helm template my-flaskapp ./charts/flaskapp \
  --set image.name=yourrepo/flaskapp --set image.tag=latest
```

Files of interest
- `app.py` — Flask app renders `templates/index.html`.
- `Dockerfile` — builds the image; exposes port 5000.
- `charts/flaskapp/values.yaml` — default chart values (edit or override with `--set`).
- `charts/flaskapp/templates/*` — Deployment, Service, ConfigMap templates used by Helm.



