from celery import Celery

# Configure Celery with Redis broker and backend
app = Celery('distributed_job_scheduler',
             broker='redis://localhost:6379/0',
             backend='redis://localhost:6379/0',
             include=['tasks'])

# Configure task retries for fault tolerance
app.conf.task_default_retry_delay = 10  # Retry after 10 seconds
app.conf.task_max_retries = 3  # Maximum 3 retries per task
app.conf.task_acks_late = True  # Acknowledge tasks after execution