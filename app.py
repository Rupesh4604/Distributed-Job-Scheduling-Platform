from fastapi import FastAPI, HTTPException
from celery.result import AsyncResult
from tasks import process_data, process_image  # Import tasks
import uuid  # For generating unique task IDs if needed

app = FastAPI(title="Distributed Job Scheduling Platform")

@app.post("/submit_job")
async def submit_job(job_type: str, payload: dict):
    """
    Submits a job asynchronously and returns a task ID.
    - job_type: 'data' or 'image'
    - payload: {'data': str} for data, {'image_url': str} for image
    """
    if job_type == "data":
        if "data" not in payload:
            raise HTTPException(status_code=400, detail="Missing 'data' in payload")
        task = process_data.delay(payload["data"])
    elif job_type == "image":
        if "image_url" not in payload:
            raise HTTPException(status_code=400, detail="Missing 'image_url' in payload")
        task = process_image.delay(payload["image_url"])
    else:
        raise HTTPException(status_code=400, detail="Invalid job_type. Use 'data' or 'image'.")
    
    return {"task_id": task.id}

@app.get("/get_job_status/{task_id}")
async def get_job_status(task_id: str):
    """
    Retrieves the status and result of a job by task ID.
    """
    task_result = AsyncResult(task_id)
    if not task_result:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return {
        "task_id": task_id,
        "status": task_result.status,
        "result": task_result.result if task_result.ready() else None
    }