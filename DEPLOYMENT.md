# Deployment Guide

This guide covers various deployment options for the AI Backend Service.

## Table of Contents
- [Local Development](#local-development)
- [Docker Deployment](#docker-deployment)
- [Production Deployment](#production-deployment)
- [Cloud Deployments](#cloud-deployments)
- [Monitoring and Maintenance](#monitoring-and-maintenance)

## Local Development

### Prerequisites
- Python 3.11+
- Redis server
- Google AI API key

### Quick Setup
```bash
# Clone and setup
git clone <repository-url>
cd ai-backend-service
chmod +x scripts/*.sh
./scripts/setup.sh

# Configure environment
cp .env.example .env
# Edit .env and add your Google API key

# Start Redis (in separate terminal)
redis-server

# Start the API server (in separate terminal)
./scripts/start.sh

# Start Celery worker (in separate terminal)
./scripts/start-worker.sh
```

### Manual Setup
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env
# Edit .env file with your configurations

# Start services
uvicorn app.main:app --reload
celery -A app.workers.celery_worker worker --loglevel=info
```

## Docker Deployment

### Development with Docker
```bash
# Build and start all services
docker-compose -f docker/docker-compose.yml up --build

# Run in background
docker-compose -f docker/docker-compose.yml up -d

# View logs
docker-compose -f docker/docker-compose.yml logs -f

# Stop services
docker-compose -f docker/docker-compose.yml down
```

### Production Docker Setup
```bash
# Create production environment file
cp production.env .env
# Edit .env with production values

# Build production image
docker build -f docker/Dockerfile -t ai-backend-service:latest .

# Run with production settings
docker run -d \
  --name ai-backend-api \
  --env-file .env \
  -p 8000:8000 \
  ai-backend-service:latest
```

## Production Deployment

### Server Requirements
- **CPU**: 2+ cores
- **RAM**: 4GB+ (8GB recommended)
- **Storage**: 20GB+ SSD
- **OS**: Ubuntu 20.04+ or similar Linux distribution

### Production Setup Steps

1. **Server Preparation**
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install required packages
sudo apt install -y python3.11 python3.11-venv python3-pip redis-server nginx

# Create application user
sudo useradd -m -s /bin/bash aiservice
sudo usermod -aG sudo aiservice
```

2. **Application Deployment**
```bash
# Switch to application user
sudo su - aiservice

# Clone repository
git clone <repository-url> /home/aiservice/ai-backend-service
cd /home/aiservice/ai-backend-service

# Setup application
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure environment
cp production.env .env
# Edit .env with production values
```

3. **System Services Setup**

Create systemd service for the API:
```bash
sudo tee /etc/systemd/system/ai-backend-api.service > /dev/null <<EOF
[Unit]
Description=AI Backend API Service
After=network.target redis.service

[Service]
Type=exec
User=aiservice
Group=aiservice
WorkingDirectory=/home/aiservice/ai-backend-service
Environment=PATH=/home/aiservice/ai-backend-service/venv/bin
ExecStart=/home/aiservice/ai-backend-service/venv/bin/gunicorn -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000 app.main:app
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF
```

Create systemd service for Celery worker:
```bash
sudo tee /etc/systemd/system/ai-backend-worker.service > /dev/null <<EOF
[Unit]
Description=AI Backend Celery Worker
After=network.target redis.service

[Service]
Type=exec
User=aiservice
Group=aiservice
WorkingDirectory=/home/aiservice/ai-backend-service
Environment=PATH=/home/aiservice/ai-backend-service/venv/bin
ExecStart=/home/aiservice/ai-backend-service/venv/bin/celery -A app.workers.celery_worker worker --loglevel=info --concurrency=2
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF
```

4. **Nginx Configuration**
```bash
sudo tee /etc/nginx/sites-available/ai-backend > /dev/null <<EOF
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }

    location /health/ {
        proxy_pass http://127.0.0.1:8000/health/;
        access_log off;
    }
}
EOF

# Enable site
sudo ln -s /etc/nginx/sites-available/ai-backend /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

5. **Start Services**
```bash
# Enable and start services
sudo systemctl enable redis-server
sudo systemctl enable ai-backend-api
sudo systemctl enable ai-backend-worker
sudo systemctl enable nginx

sudo systemctl start redis-server
sudo systemctl start ai-backend-api
sudo systemctl start ai-backend-worker
sudo systemctl start nginx
```

## Cloud Deployments

### Render.com Deployment

1. **Connect Repository**
   - Go to [Render.com](https://render.com)
   - Connect your GitHub repository
   - Use the `deployment/render.yaml` configuration

2. **Environment Variables**
   Set these in Render dashboard:
   - `GOOGLE_API_KEY`: Your Google AI API key
   - `DEBUG`: false
   - Other variables as needed

3. **Deploy**
   - Render will automatically deploy using the YAML configuration
   - Services will include: Web service, Redis, and Worker

### Fly.io Deployment

1. **Install Fly CLI**
```bash
curl -L https://fly.io/install.sh | sh
```

2. **Login and Deploy**
```bash
fly auth login
fly launch  # This will use fly.toml configuration
fly deploy
```

3. **Set Environment Variables**
```bash
fly secrets set GOOGLE_API_KEY=your_api_key_here
fly secrets set DEBUG=false
```

### AWS Deployment (ECS/Fargate)

1. **Build and Push Docker Image**
```bash
# Build image
docker build -f docker/Dockerfile -t ai-backend-service .

# Tag for ECR
docker tag ai-backend-service:latest your-account.dkr.ecr.region.amazonaws.com/ai-backend-service:latest

# Push to ECR
docker push your-account.dkr.ecr.region.amazonaws.com/ai-backend-service:latest
```

2. **Create ECS Task Definition**
```json
{
  "family": "ai-backend-service",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "512",
  "memory": "1024",
  "executionRoleArn": "arn:aws:iam::account:role/ecsTaskExecutionRole",
  "containerDefinitions": [
    {
      "name": "ai-backend-api",
      "image": "your-account.dkr.ecr.region.amazonaws.com/ai-backend-service:latest",
      "portMappings": [
        {
          "containerPort": 8000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {"name": "DEBUG", "value": "false"},
        {"name": "REDIS_URL", "value": "redis://your-redis-cluster:6379/0"}
      ],
      "secrets": [
        {
          "name": "GOOGLE_API_KEY",
          "valueFrom": "arn:aws:secretsmanager:region:account:secret:ai-backend/google-api-key"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/ai-backend-service",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```

## Monitoring and Maintenance

### Health Checks
```bash
# Check service health
curl http://your-domain.com/api/v1/health/

# Check system metrics
curl http://your-domain.com/api/v1/health/metrics

# Check service status
sudo systemctl status ai-backend-api
sudo systemctl status ai-backend-worker
```

### Log Management
```bash
# View API logs
sudo journalctl -u ai-backend-api -f

# View worker logs
sudo journalctl -u ai-backend-worker -f

# View application logs
tail -f /home/aiservice/ai-backend-service/logs/app.log
```

### Performance Monitoring
- Use the `/health/metrics` endpoint for system metrics
- Monitor Redis performance: `redis-cli info`
- Monitor Celery: Access Flower at `http://your-domain:5555`

### Backup and Recovery
```bash
# Backup Redis data
redis-cli BGSAVE

# Backup application logs
tar -czf logs-backup-$(date +%Y%m%d).tar.gz logs/

# Backup configuration
cp .env .env.backup
```

### Updates and Maintenance
```bash
# Update application
cd /home/aiservice/ai-backend-service
git pull origin main
source venv/bin/activate
pip install -r requirements.txt

# Restart services
sudo systemctl restart ai-backend-api
sudo systemctl restart ai-backend-worker
```

### Scaling Considerations

1. **Horizontal Scaling**
   - Deploy multiple API instances behind a load balancer
   - Scale Celery workers based on queue length
   - Use Redis Cluster for high availability

2. **Vertical Scaling**
   - Increase server resources (CPU, RAM)
   - Adjust Gunicorn worker count
   - Tune Celery concurrency settings

3. **Database Scaling** (if added)
   - Use read replicas for read-heavy workloads
   - Implement connection pooling
   - Consider database sharding for large datasets

### Security Best Practices

1. **API Security**
   - Implement proper API key authentication
   - Use HTTPS in production
   - Set up rate limiting
   - Validate all inputs

2. **Server Security**
   - Keep system updated
   - Use firewall (ufw/iptables)
   - Implement fail2ban
   - Regular security audits

3. **Application Security**
   - Rotate API keys regularly
   - Use environment variables for secrets
   - Implement proper logging
   - Monitor for suspicious activity