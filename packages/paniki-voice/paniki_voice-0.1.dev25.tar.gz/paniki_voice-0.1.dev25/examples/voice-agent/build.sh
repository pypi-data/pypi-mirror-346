#!/bin/bash

# Build Docker image
docker build -t voice-agent .

# Run container
docker run -d \
  --name voice-agent \
  -p 8080:8080 \
  --env-file .env \
  voice-agent