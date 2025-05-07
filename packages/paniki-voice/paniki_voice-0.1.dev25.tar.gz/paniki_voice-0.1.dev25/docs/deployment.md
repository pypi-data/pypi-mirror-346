# Deployment Guide

## Docker Deployment

### Using the Official Docker Image

```bash
docker pull anak10thn/paniki:latest
```

### Custom Dockerfile

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    portaudio19-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy application files
COPY requirements.txt .
COPY pyproject.toml .
COPY libs/ libs/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables
ENV PANIKI_HOST=0.0.0.0
ENV PANIKI_PORT=8080

# Expose port
EXPOSE 8080

# Run the application
CMD ["python", "server.py"]
```

### Docker Compose

```yaml
version: '3.8'

services:
  paniki:
    build: .
    ports:
      - "8080:8080"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - GOOGLE_API_KEY=${GOOGLE_API_KEY}
      - PANIKI_HOST=0.0.0.0
      - PANIKI_PORT=8080
    volumes:
      - ./models:/app/models
    restart: unless-stopped

  redis:
    image: redis:alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    restart: unless-stopped

volumes:
  redis_data:
```

## Kubernetes Deployment

### Deployment Configuration

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: paniki
  namespace: default
spec:
  replicas: 3
  selector:
    matchLabels:
      app: paniki
  template:
    metadata:
      labels:
        app: paniki
    spec:
      containers:
      - name: paniki
        image: anak10thn/paniki:latest
        ports:
        - containerPort: 8080
        env:
        - name: OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: paniki-secrets
              key: openai-api-key
        - name: PANIKI_HOST
          value: "0.0.0.0"
        - name: PANIKI_PORT
          value: "8080"
        resources:
          requests:
            memory: "256Mi"
            cpu: "100m"
          limits:
            memory: "512Mi"
            cpu: "200m"
```

### Service Configuration

```yaml
apiVersion: v1
kind: Service
metadata:
  name: paniki-service
spec:
  selector:
    app: paniki
  ports:
  - port: 80
    targetPort: 8080
  type: LoadBalancer
```

### Secrets Management

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: paniki-secrets
type: Opaque
data:
  openai-api-key: <base64-encoded-key>
  google-api-key: <base64-encoded-key>
```

## Cloud Deployment

### AWS Elastic Beanstalk

1. Create `Procfile`:
```
web: python server.py
```

2. Create `.ebextensions/01_packages.config`:
```yaml
packages:
  yum:
    portaudio-devel: []
    python3-devel: []
    gcc: []
```

### Google Cloud Run

1. Create `cloudbuild.yaml`:
```yaml
steps:
- name: 'gcr.io/cloud-builders/docker'
  args: ['build', '-t', 'gcr.io/$PROJECT_ID/paniki', '.']
- name: 'gcr.io/cloud-builders/docker'
  args: ['push', 'gcr.io/$PROJECT_ID/paniki']
```

### Azure Container Apps

1. Create deployment script:
```bash
az containerapp create \
  --name paniki \
  --resource-group myResourceGroup \
  --image anak10thn/paniki:latest \
  --target-port 8080 \
  --ingress external \
  --env-vars PANIKI_HOST=0.0.0.0 PANIKI_PORT=8080
```

## Scaling Considerations

### Horizontal Scaling

1. Configure auto-scaling:
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: paniki-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: paniki
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

### Load Balancing

1. Configure Nginx:
```nginx
upstream paniki {
    server paniki1:8080;
    server paniki2:8080;
    server paniki3:8080;
}

server {
    listen 80;
    server_name example.com;

    location / {
        proxy_pass http://paniki;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## Monitoring and Logging

### Prometheus Integration

1. Add metrics endpoint:
```python
from prometheus_client import Counter, Histogram
from fastapi import FastAPI

app = FastAPI()
request_count = Counter('request_count', 'Total requests')
response_time = Histogram('response_time', 'Response time')
```

### ELK Stack Integration

1. Configure Filebeat:
```yaml
filebeat.inputs:
- type: log
  enabled: true
  paths:
    - /app/logs/paniki.log

output.elasticsearch:
  hosts: ["elasticsearch:9200"]
```

## Security Considerations

### SSL/TLS Configuration

1. Generate certificates:
```bash
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout private.key -out certificate.crt
```

2. Configure in application:
```python
import ssl

ssl_context = ssl.create_default_context(
    purpose=ssl.Purpose.CLIENT_AUTH
)
ssl_context.load_cert_chain(
    certfile="certificate.crt",
    keyfile="private.key"
)
```

### Network Security

1. Configure network policies:
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: paniki-network-policy
spec:
  podSelector:
    matchLabels:
      app: paniki
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: frontend
    ports:
    - protocol: TCP
      port: 8080
```