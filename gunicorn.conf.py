"""
Gunicorn configuration for Render deployment
"""

import multiprocessing
import os

# Server socket
bind = "0.0.0.0:" + os.environ.get("PORT", "8000")
backlog = 2048

# Worker processes
# Use the RENDER_NUM_WEB_WORKERS environment variable if available, otherwise calculate
workers = int(os.environ.get("RENDER_NUM_WEB_WORKERS", multiprocessing.cpu_count() * 2 + 1))
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2

# Restart workers after this many requests, to help prevent memory leaks
max_requests = 1000
max_requests_jitter = 100

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Process naming
proc_name = "takeopinion"

# Server mechanics
preload_app = True
daemon = False
pidfile = "/tmp/gunicorn.pid"
user = None
group = None
tmp_upload_dir = None

# Security
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190

# Enable access log to stdout
capture_output = True
enable_stdio_inheritance = True