from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from auth.router import router as auth_router
from detection.router import router as image_router
from task.router import router as task_router

app = FastAPI(
    title="Object Detection",
)

origins = [
    "http://54.89.224.132",
    "https://detect.uno",  
    "http://detect.uno",  
    "http://localhost",    
    "http://localhost:8008"
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(image_router)
app.include_router(task_router)

@app.get("/", include_in_schema=False)
async def redirect():
    return RedirectResponse("/docs")
