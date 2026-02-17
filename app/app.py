import os
import time
from datetime import datetime
from flask import Flask, jsonify, request  # type: ignore
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST # type: ignore

app = Flask(__name__)

# ----------------------------
# Environment Variables
# ----------------------------
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
START_TIME = time.time()

# ----------------------------
# Prometheus Metrics
# ----------------------------
REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP Requests",
    ["method", "endpoint"]
)

DEPLOYMENT_COUNT = Counter(
    "deployment_count",
    "Number of deployments triggered"
)

REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency"
)

# ----------------------------
# Middleware for Metrics
# ----------------------------
@app.before_request
def before_request():
    request.start_time = time.time()

@app.after_request
def after_request(response):
    latency = time.time() - request.start_time
    REQUEST_LATENCY.observe(latency)

    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.path
    ).inc()

    return response

# ----------------------------
# Routes
# ----------------------------

@app.route("/")
def home():
    return jsonify({
        "message": "Welcome to DevOps Deployment Tracker API 🚀",
        "version": APP_VERSION
    })

@app.route("/health")
def health():
    return jsonify({
        "status": "healthy"
    })

@app.route("/version")
def version():
    return jsonify({
        "version": APP_VERSION
    })

@app.route("/deploy", methods=["POST"])
def deploy():
    DEPLOYMENT_COUNT.inc()
    return jsonify({
        "message": "Deployment recorded successfully",
        "timestamp": datetime.utcnow().isoformat()
    })

@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}

@app.route("/uptime")
def uptime():
    current_uptime = time.time() - START_TIME
    return jsonify({
        "uptime_seconds": round(current_uptime, 2)
    })

# ----------------------------
# Run App
# ----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)