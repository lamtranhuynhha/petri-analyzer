from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import analyze, net_upload, visualize

# Create FastAPI app
app = FastAPI(
    title="Petri Net Analyzer API",
    description="Backend API for Petri Net analysis, visualization, and simulation",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3001",
        "petrinet-analyzer.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(analyze.router)
app.include_router(net_upload.router)
app.include_router(visualize.router)

@app.get("/")
def read_root():
    return {
        "message": "Petri Net Analyzer backend is running!",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/api/health")
def health_check():
    return {
        "status": "ok",
        "message": "Backend is healthy"
    }
