# Flask-app 
A simple Flask app to test CICD pipeline and DevOps solutions like argoCD, helm, etc


### Build Docker image
docker build -t my-flask-app:v1 . 

### Run Docker
docker run -p 5000:5000 my-flask-app:v1

### See locally
http://localhost:5000

### Push to Dockerhub
docker tag my-flask-app:v1 YOUR_DOCKERHUB_USERNAME/my-flask-app:latest
docker push YOUR_DOCKERHUB_USERNAME/my-flask-app:latest

