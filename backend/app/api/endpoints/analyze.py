"""
analyze.py
------------
Các API phân tích Petri Net (deadlock, reachability, v.v.)
"""

from fastapi import APIRouter, HTTPException
from app.core.schemas import PetriNetRequest, DeadlockResult
from app.algorithms.deadlock import deadlock_detection

router = APIRouter(prefix="/analyze", tags=["Analysis"])


@router.post("/deadlock", response_model=DeadlockResult)
def analyze_deadlock(request: PetriNetRequest):
    """
    Phát hiện deadlock trong Petri Net.
    Nhận dữ liệu PN từ frontend (JSON), trả về danh sách marking deadlock.
    """
    try:
        P = request.places
        T = request.transitions
        F = [tuple(edge) for edge in request.arcs]  # chuyển list -> tuple
        
        # Convert weights to the expected format
        W = {tuple(weight_item["arc"]): weight_item["weight"] for weight_item in request.weights}
            
        M0 = request.initial_marking

        result = deadlock_detection(P, T, F, W, M0)
        return result

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error analyzing deadlock: {str(e)}")
