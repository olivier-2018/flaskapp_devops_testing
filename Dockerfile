FROM python:3.11-alpine

# Install minimal build deps
RUN apk add --no-cache gcc musl-dev

# Create working directory
WORKDIR /app

# Copy application files
COPY requirements.txt /app/
COPY app.py /app/
COPY static /app/static
COPY templates /app/templates

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Default port
ENV PORT=5000
EXPOSE 5000

# Run the app
CMD ["python", "app.py"]
