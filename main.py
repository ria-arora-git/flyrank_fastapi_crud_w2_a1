from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

tasks = [
    {
        "id": 1,
        "title": "Read the doc",
        "done": False
    },
    {
        "id": 2,
        "title": "Understand the steps",
        "done": False
    },
    {
        "id": 3,
        "title": "Build it",
        "done": False
    }
]

@app.get("/")
def root():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/tasks")
def get_tasks():
    return tasks

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task

    return JSONResponse(
        status_code=404,
        content={"error": f"Task {task_id} not found"}
    )

@app.post("/tasks", status_code=201)
async def create_task(request: Request):
    data = await request.json()

    if "title" not in data or not data["title"]:
        return JSONResponse(
            status_code=400,
            content={"error": "Title is required"}
        )

    new_id = max(task["id"] for task in tasks) + 1

    new_task = {
        "id": new_id,
        "title": data["title"],
        "done": False
    }

    tasks.append(new_task)

    return new_task