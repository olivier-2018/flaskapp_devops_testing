FROM python:3.11-alpine

# Create working directory
WORKDIR /app

# Copy application files
COPY requirements.txt /app/
COPY app.py /app/
COPY static /app/static
COPY templates /app/templates

# Set environment variable for Flask
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=3000
ENV CUSTOM_HEADER="My Default Containerized Webapp"

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the app
CMD ["flask", "run"]
