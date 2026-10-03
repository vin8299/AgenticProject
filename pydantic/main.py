from fastapi import FastAPI
app = FastAPI(
    title="Course Management API",
    description="A simple API created using FastAPI",
    version="1.0.0"
)
@app.get("/")
async def home():
    return {
        "application": "Course Management API",
        "framework": "FastAPI",
        "status": "running"
    }

