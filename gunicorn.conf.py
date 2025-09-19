# Gunicorn configuration file for TakeOpinion

# Bind to the port that Render provides
bind = "0.0.0.0:" + str(os.environ.get("PORT", 8000))

# Worker processes
workers = os.environ.get("WEB_CONCURRENCY", 3)

# Worker class
worker_class = "sync"

# Worker connections (for async workers)
worker_connections = 1000

# Timeout
timeout = 30

# Keep alive
keepalive = 2

# Max requests
max_requests = 1000
max_requests_jitter = 100

# Preload app
preload_app = True

# User and group
user = os.environ.get("USER", "ubuntu")
group = os.environ.get("GROUP", "ubuntu")

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"