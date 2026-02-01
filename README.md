
# Flask-app
A minimal Flask application packaged for Docker and deployable with Helm.

Quick steps
- **Build image**:

```bash
docker build -t yourrepo/flaskapp:dev .
```

- **Run locally** (fallback uses env `MESSAGE`):

```bash
docker run -p 5000:5000 -e MESSAGE="Local header" yourrepo/flaskapp:dev
# then open http://localhost:5000
```

Helm chart
- Chart is under `charts/flaskapp` and uses a ConfigMap key `CUSTOM_HEADER` to configure the header shown by the app.

- **Install with defaults** (override image repo/tag as needed):

```bash
helm install my-dev ./charts/flaskapp \
	--set image.repository=yourrepo/flaskapp --set image.tag=dev
```

- **Override the header** (set the ConfigMap value):

```bash
helm upgrade --install my-dev ./charts/flaskapp \
	--set configmap.data.CUSTOM_HEADER="This is a simplistic Flask app for CICD testing." \
	--set image.repository=yourrepo/flaskapp --set image.tag=dev
```

- **Port-forward to access**:

```bash
kubectl port-forward svc/my-dev-flaskapp-svc 8080:80
# then open http://localhost:8080
```

Notes
- The app reads `/etc/config/CUSTOM_HEADER` (mounted from the Helm-created ConfigMap). For local Docker runs, set `MESSAGE` env var instead.
- Templates and deployment use sensible Helm `default` values so `values.yaml` only needs to provide environment-specific `configmap.data` entries.

