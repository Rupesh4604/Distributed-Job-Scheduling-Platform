# Distributed Job Scheduling Platform

## Overview

This repository contains the implementation of a scalable and fault-tolerant distributed job scheduling platform. The system enables users to submit resource-intensive or long-running tasks via a web API, with processing handled asynchronously by a pool of worker nodes. This architecture ensures high responsiveness, efficient workload distribution, and robust error handling, making it suitable for applications requiring high-volume task management.

Key objectives include achieving scalability to handle over 500,000 daily jobs, 99.99% uptime, and a 60% reduction in average task latency through asynchronous processing and optimized resource allocation.

## Features

- **Asynchronous Job Submission**: Users submit tasks via API endpoints, receiving immediate task IDs without waiting for completion.
- **Task Status Querying**: Retrieve real-time status and results for submitted jobs.
- **Fault Tolerance**: Automatic retries for transient failures, with configurable retry limits and delays.
- **Scalability**: Dynamic scaling of worker nodes based on workload, supporting high-volume operations.
- **Monitoring and Dashboards**: Integration with Prometheus and Grafana for performance metrics and visualizations.
- **Containerized Deployment**: Dockerized components for consistent environments, orchestrated on Kubernetes for high availability.
- **CI/CD Automation**: Streamlined pipelines for building, testing, and deploying updates.

## Technologies

- **API Framework**: FastAPI (for high-performance asynchronous endpoints).
- **Task Queue**: Celery (for distributed task scheduling and execution).
- **Message Broker/Backend**: Redis (for queuing tasks and storing results).
- **Containerization**: Docker.
- **Orchestration**: Kubernetes on Google Cloud Platform (GCP).
- **Monitoring**: Prometheus and Grafana.
- **Programming Language**: Python 3.10+.

## Prerequisites

- Python 3.10 or later.
- Redis server (install via package manager, e.g., `brew install redis` on macOS or `apt install redis-server` on Ubuntu).
- Docker (for containerization).
- Kubernetes cluster (e.g., on GCP via Google Kubernetes Engine).
- Optional: Prometheus and Grafana for monitoring.

## Installation

1. Clone the repository:

   ```
   git clone https://github.com/Rupesh4604/Distributed-Job-Scheduling-Platform.git
   cd distributed-job-scheduler
   ```

2. Create and activate a virtual environment:

   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:

   ```
   pip install -r requirements.txt
   ```

4. Start Redis (if not already running):
   ```
   redis-server
   ```

## Usage

### Running Locally

1. Start the FastAPI server:

   ```
   uvicorn app:app --host 0.0.0.0 --port 8000 --reload
   ```

2. Start Celery workers (in a separate terminal):
   ```
   celery -A celery_app worker --loglevel=info -c 4  # -c 4 for 4 concurrent workers
   ```

### API Endpoints

- **Submit Job** (`POST /submit_job`):

  - Body: `{"job_type": "data", "payload": {"data": "sample input"}}` or `{"job_type": "image", "payload": {"image_url": "https://example.com/image.jpg"}}`.
  - Response: `{"task_id": "unique-task-id"}`.

- **Get Job Status** (`GET /get_job_status/{task_id}`):
  - Response: `{"task_id": "unique-task-id", "status": "SUCCESS", "result": "Processed output"}`.

Access the API documentation at `http://localhost:8000/docs`.

### Example Tasks

- Data processing: Simulates heavy computation (e.g., string transformation).
- Image processing: Handles URL-based image manipulation (extendable with libraries like Pillow).

## Deployment

### Docker

1. Build the Docker image:

   ```
   docker build -t job-scheduler .
   ```

2. Run the API container:

   ```
   docker run -d -p 8000:8000 --name api job-scheduler uvicorn app:app --host 0.0.0.0 --port 8000
   ```

3. Run worker containers (link to Redis):

   ```
   docker run -d --name worker job-scheduler celery -A celery_app worker --loglevel=info
   ```

   Ensure Redis is running in a separate container:

   ```
   docker run -d -p 6379:6379 --name redis redis
   ```

### Kubernetes on GCP

1. Create a GKE cluster:

   ```
   gcloud container clusters create my-cluster --num-nodes=3
   ```

2. Build and push Docker image to Google Container Registry:

   ```
   docker tag job-scheduler gcr.io/your-project/job-scheduler
   docker push gcr.io/your-project/job-scheduler
   ```

3. Apply Kubernetes manifests:
   ```
   kubectl apply -f k8s/deployment.yaml
   kubectl apply -f k8s/service.yaml
   kubectl apply -f k8s/hpa.yaml
   ```

This deploys the API, workers, and Redis, with autoscaling enabled.

## Monitoring

- Install Prometheus and Grafana via Helm:
  ```
  helm install prometheus prometheus-community/prometheus
  helm install grafana grafana/grafana
  ```
- Configure dashboards to monitor queue lengths, task latencies, and CPU usage.

## CI/CD

The repository includes a GitHub Actions workflow (`.github/workflows/ci-cd.yml`) that automates building, pushing images, and deploying to Kubernetes on pushes to the main branch.

## Contributing

Contributions are welcome. Please follow these steps:

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/new-feature`).
3. Commit changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature/new-feature`).
5. Open a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
