# create a gunicorn config file
import multiprocessing
bind = "0.0.0.0:5001"
workers = (multiprocessing.cpu_count() * 2) + 1
threads = workers
worker_class = "gevent"
timeout = 0