from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Petri Net Analyzer backend is running!"}
