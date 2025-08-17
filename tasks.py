from celery_app import app
import time  # For simulating long-running tasks

@app.task(bind=True, autoretry_for=(Exception,), retry_kwargs={'max_retries': 3})
def process_data(self, data):
    """Simulates a long-running data processing task."""
    try:
        # Simulate processing (e.g., heavy computation)
        time.sleep(5)  # Replace with actual logic, e.g., data analysis
        result = f"Processed data: {data.upper()}"
        return result
    except Exception as exc:
        # Automatic retry on failure (e.g., network timeout)
        raise self.retry(exc=exc)

@app.task(bind=True, autoretry_for=(Exception,), retry_kwargs={'max_retries': 3})
def process_image(self, image_url):
    """Simulates image processing from a URL."""
    try:
        # Simulate image download and manipulation (requires additional libraries like Pillow if needed)
        time.sleep(10)  # Replace with actual image processing
        result = f"Processed image from URL: {image_url}"
        return result
    except Exception as exc:
        raise self.retry(exc=exc)