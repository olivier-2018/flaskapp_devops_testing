FROM python:3.11-alpine 

# Install minimal dependencies 
RUN apk add --no-cache gcc musl-dev 

# Create working directory 
WORKDIR /app 

# Install Flask 
COPY app.py /app/ 
COPY static /app/static 
RUN pip install --no-cache-dir flask 

# Expose port 
EXPOSE 5000 

# Run the app 
CMD ["python", "app.py"] 
