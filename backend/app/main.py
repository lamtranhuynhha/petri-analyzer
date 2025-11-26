from fastapi import FastAPI
from app.api.endpoints import analyze

app = FastAPI()
app.include_router(analyze.router)

@app.get("/")
def read_root():
    return {"message": "Petri Net Analyzer backend is running!"}
