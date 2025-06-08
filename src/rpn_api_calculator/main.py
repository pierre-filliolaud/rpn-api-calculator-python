from fastapi import FastAPI
from .api import health

app = FastAPI(title="RPN API Calculator")

# Include routers
app.include_router(health.router)

@app.get("/")
async def read_root():
    return {"message": "Welcome to the RPN API Calculator!"}