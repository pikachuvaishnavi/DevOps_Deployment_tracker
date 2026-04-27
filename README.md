🚀 DevOps Deployment Tracker

A production-style DevOps project that demonstrates end-to-end application deployment, monitoring, and automation using modern cloud-native tools.

This project showcases how to containerize, deploy, monitor, and maintain a Python Flask application using a complete DevOps pipeline.

📌 Project Overview

This application is a Dockerized Flask-based deployment tracker deployed on Amazon Web Services EC2, behind an Nginx reverse proxy, with automated CI/CD pipelines and real-time monitoring.

It simulates real-world DevOps workflows including:

*Continuous Integration & Deployment
*Containerized application delivery
*Observability & monitoring
*Secure HTTPS configuration
*High availability through automated recovery

DevOps pipelines combine automation, tools, and processes to deliver software quickly and reliably .

🏗️ Architecture
User → Nginx → Flask App (Docker Container)
                     ↓
               Prometheus Monitoring
                     ↓
               GitHub Actions CI/CD
                     ↓
                AWS EC2 Instance
⚙️ Tech Stack
*Backend: Python (Flask)
*Containerization: Docker
*CI/CD: GitHub Actions
*Cloud: Amazon Web Services EC2
*Reverse Proxy: Nginx
*Monitoring: Prometheus
*Security: Let's Encrypt (HTTPS)

✨ Features

🐳 Containerized Flask application using Docker
🔁 Automated CI/CD pipeline for build, test, and deployment
🌐 Nginx reverse proxy for routing and scalability
📊 Real-time monitoring (requests, latency, uptime, deployments)
🔐 Automatic HTTPS with SSL certificates
❤️ Health checks with auto-redeployment on failure
⚡ Zero-touch deployments via GitHub Actions

🚀 Getting Started

1️⃣ Clone the repository
git clone https://github.com/pikachuvaishnavi/DevOps_Deployment_tracker.git
cd DevOps_Deployment_tracker
2️⃣ Run locally using Docker
docker build -t deployment-tracker .
docker run -p 5000:5000 deployment-tracker
3️⃣ Access the app
http://localhost:5000

🔄 CI/CD Pipeline
*Triggered on push to main branch
*Builds Docker image
*Runs tests
*Pushes image
*Deploys automatically to EC2

📊 Monitoring & Observability
*Metrics collected using Prometheus
*Tracks:
**HTTP request count
**Response latency
**Application uptime
**Deployment frequency

🔐 Security
*HTTPS enabled using Let's Encrypt
*Secure reverse proxy configuration with Nginx

🧠 What I Learned
Building end-to-end DevOps pipelines
Automating deployments with GitHub Actions
Managing production-like environments on AWS
Implementing monitoring and observability
Improving system reliability with health checks


👤 Author

Vaishnavi
DevOps Enthusiast 🚀
