# Deployment Guide

This guide provides instructions for deploying the Super-Intelligence Autonomous Agentic AI System in various environments.

## Local Development with Docker Compose

For local development and testing, Docker Compose is the recommended approach. It sets up the FastAPI application and the Qdrant vector database.

### Prerequisites
- Docker Desktop installed (includes Docker Engine and Docker Compose)

### Steps
1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/super-intelligence-agent.git
   cd super-intelligence-agent
   ```
2. **Set up environment variables:**
   Copy the example environment file and fill in your API keys:
   ```bash
   cp .env.example .env
   # Open .env and add your LLM API keys and other configurations
   ```
3. **Build and run the services:**
   ```bash
   docker-compose up --build -d
   ```
   This command will:
   - Build the `agent-api` Docker image based on the `Dockerfile` in the `deploy/` directory.
   - Start the `agent-api` service, exposing it on port `8000`.
   - Start the `qdrant` vector database service, exposing it on ports `6333` (gRPC) and `6334` (HTTP).

4. **Verify deployment:**
   Access the API at `http://localhost:8000` in your browser or using `curl`:
   ```bash
   curl http://localhost:8000
   ```
   You should see a response indicating the API is online.

5. **Stop the services:**
   ```bash
   docker-compose down
   ```

## Production Deployment with Kubernetes (Conceptual)

For production environments, Kubernetes is recommended for its scalability, resilience, and management capabilities. This section outlines a conceptual deployment, and actual implementation will require Kubernetes manifests (e.g., `deployment.yaml`, `service.yaml`, `ingress.yaml`).

### Prerequisites
- A running Kubernetes cluster (e.g., GKE, EKS, AKS, or a self-managed cluster).
- `kubectl` configured to connect to your cluster.
- Docker images of your application pushed to a container registry (e.g., Docker Hub, Google Container Registry).

### Key Considerations

#### 1. Containerization
Ensure your application is containerized and optimized for Kubernetes. The provided `Dockerfile` serves as a starting point.

#### 2. Kubernetes Manifests
You will need to create Kubernetes manifests for:
- **Deployment**: To manage the `agent-api` pods.
- **Service**: To expose the `agent-api` within the cluster.
- **Ingress (Optional)**: For external access and load balancing.
- **Persistent Volume Claims (PVCs)**: For Qdrant data persistence.
- **Secrets**: To securely manage API keys and sensitive configurations.

#### 3. Scaling
- **Horizontal Pod Autoscaler (HPA)**: Configure HPA to automatically scale the `agent-api` pods based on CPU utilization or custom metrics.
- **Qdrant Cluster**: For high-availability and scalability of the vector database, consider deploying Qdrant in a distributed cluster mode.

#### 4. Observability
- Integrate with Kubernetes-native monitoring solutions like Prometheus and Grafana for metrics collection and visualization.
- Implement distributed tracing (e.g., Jaeger, OpenTelemetry) to track requests across microservices.
- Centralized logging (e.g., ELK stack, Loki) for effective troubleshooting.

#### 5. CI/CD Pipeline
Automate the deployment process using CI/CD tools (e.g., GitHub Actions, GitLab CI, Jenkins) to:
- Build Docker images.
- Push images to a container registry.
- Update Kubernetes deployments.

### Example Kubernetes Deployment (Conceptual `deployment.yaml`)

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: agent-api-deployment
  labels:
    app: agent-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: agent-api
  template:
    metadata:
      labels:
        app: agent-api
    spec:
      containers:
      - name: agent-api
        image: your-docker-registry/super-intelligence-agent:latest
        ports:
        - containerPort: 8000
        envFrom:
        - secretRef:
            name: agent-api-secrets
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "1000m"
      # Add init containers for Qdrant health check if needed
```

**Note**: This is a simplified example. A full production deployment would involve more detailed configurations for networking, security, and resource management.
