import os
import time
from datetime import datetime
from flask import Flask, jsonify, request  # type: ignore
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST # type: ignore
import socket

app = Flask(__name__)

# ----------------------------
# Environment Variables
# ----------------------------
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
START_TIME = time.time()

@app.route("/")
def home():
    hostname = socket.gethostname()
    version = os.getenv("APP_VERSION", "1.0.0")

    return f"""<!DOCTYPE html>
<html>
<head>
    <title>DevOps Tracker</title>
    <style>
        body {{
            margin: 0;
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            font-family: Arial, sans-serif;
            overflow: hidden;
            background: linear-gradient(-45deg, #000000, #008080, #001f3f); /* black, teal, deep blue */
            background-size: 400% 400%;
            animation: gradientBG 12s ease infinite;
            color: white;
        }}

        @keyframes gradientBG {{
            0% {{ background-position: 0% 50%; }}
            50% {{ background-position: 100% 50%; }}
            100% {{ background-position: 0% 50%; }}
        }}

        .container {{
            position: relative;
            background: rgba(255, 255, 255, 0.1);
            padding: 50px;
            border-radius: 20px;
            backdrop-filter: blur(15px);
            box-shadow: 0 10px 40px rgba(0,0,0,0.4);
            text-align: center;
            z-index: 2;
            animation: fadeIn 1.5s ease-in-out;
        }}

        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        h1 {{
            font-size: 42px;
            margin-bottom: 20px;
        }}

        p {{
            font-size: 18px;
            margin: 8px 0;
        }}

        .badge {{
            margin-top: 20px;
            padding: 10px 18px;
            background: #00c9a7;
            color: black;
            border-radius: 25px;
            font-weight: bold;
            display: inline-block;
        }}

        /* Floating Circles */
        .circle {{
            position: absolute;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.08);
            animation: float 20s infinite linear;
        }}

        .circle:nth-child(1) {{
            width: 200px;
            height: 200px;
            top: 10%;
            left: 5%;
        }}

        .circle:nth-child(2) {{
            width: 150px;
            height: 150px;
            bottom: 15%;
            right: 10%;
            animation-duration: 25s;
        }}

        .circle:nth-child(3) {{
            width: 100px;
            height: 100px;
            bottom: 5%;
            left: 30%;
            animation-duration: 18s;
        }}

        .circle:nth-child(4) {{
            width: 120px;
            height: 120px;
            top: 60%;
            left: 15%;
            animation-duration: 22s;
        }}

        .circle:nth-child(5) {{
            width: 70px;
            height: 70px;
            top: 25%;
            right: 25%;
            animation-duration: 28s;
        }}

        /* New top-right circles */
        .circle:nth-child(6) {{
            width: 60px;
            height: 60px;
            top: 10%;
            right: 15%;
            animation-duration: 24s;
        }}

        .circle:nth-child(7) {{
            width: 80px;
            height: 80px;
            top: 20%;
            right: 5%;
            animation-duration: 26s;
        }}

        .circle:nth-child(8) {{
            width: 120px;
            height: 120px;
            top: 5%;
            right: 20%;
            animation-duration: 30s;
        }}

        @keyframes float {{
            0% {{ transform: translateY(0px); }}
            50% {{ transform: translateY(-30px); }}
            100% {{ transform: translateY(0px); }}
        }}
    </style>
</head>
<body>
    <div class="circle"></div>
    <div class="circle"></div>
    <div class="circle"></div>
    <div class="circle"></div>
    <div class="circle"></div>
    <div class="circle"></div> <!-- new small -->
    <div class="circle"></div> <!-- new small -->
    <div class="circle"></div> <!-- new medium -->

    <div class="container">
        <h1>🚀 DevOps CI/CD Project</h1>
        <p>Successfully Deployed with Docker & AWS</p>
        <p>Hostname: {hostname}</p>
        <div class="badge">Version: {version}</div>
    </div>
</body>
</html>"""
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
# ###
# @app.route("/")
# def home():
#     return jsonify({
#         "message": "Welcome to DevOps Deployment Tracker API 🚀",
#         "version": APP_VERSION
#     })
#     ###

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