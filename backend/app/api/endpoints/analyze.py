"""
analyze.py
------------
Các API phân tích Petri Net (reachability, deadlock, boundedness, liveness, siphons-traps)
"""

from fastapi import APIRouter, HTTPException
from app.core.schemas import (
    PetriNetRequest,
    DeadlockResult,
    ReachabilityResult,
    BoundednessResult,
    LivenessResult,
    SiphonTrapResult
)
from app.algorithms.reachability import reachability_analysis
from app.algorithms.deadlock import deadlock_detection
from app.algorithms.boundedness import boundedness_analysis
from app.algorithms.liveness import liveness_analysis
from app.algorithms.siphons_traps import siphons_traps_analysis
# from utils.json_converter import convert_to_backend_format

router = APIRouter(prefix="/api/analyze", tags=["Analysis"])


def convert_arcs(request: PetriNetRequest):
    """Helper to convert request arcs to tuple format"""
    return [tuple(edge) for edge in request.arcs]


@router.post("/reachability", response_model=ReachabilityResult)
def analyze_reachability(request: PetriNetRequest):
    """
    Xây dựng Reachability Graph
    """
    try:
        P = request.places
        T = request.transitions
        F = convert_arcs(request)
        W = request.weights
        M0 = request.initial_marking
        
        result = reachability_analysis(P, T, F, W, M0)
        
        return ReachabilityResult(result=result)
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error analyzing reachability: {str(e)}")


@router.post("/deadlock", response_model=DeadlockResult)
def analyze_deadlock(request: PetriNetRequest):
    """
    Phát hiện deadlock trong Petri Net.
    """
    try:
        P = request.places
        T = request.transitions
        F = convert_arcs(request)
        W = request.weights
        M0 = request.initial_marking
        
        result = deadlock_detection(P, T, F, W, M0)
        return DeadlockResult(**result)
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error analyzing deadlock: {str(e)}")


@router.post("/boundedness", response_model=BoundednessResult)
def analyze_boundedness(request: PetriNetRequest):
    """
    Kiểm tra boundedness bằng Coverability Tree
    """
    try:
        P = request.places
        T = request.transitions
        F = convert_arcs(request)
        W = request.weights
        M0 = request.initial_marking
        
        result = boundedness_analysis(P, T, F, W, M0)
        
        return BoundednessResult(result=result)
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error analyzing boundedness: {str(e)}")


@router.post("/liveness", response_model=LivenessResult)
def analyze_liveness(request: PetriNetRequest):
    """
    Kiểm tra liveness của các transitions
    """
    try:
        P = request.places
        T = request.transitions
        F = convert_arcs(request)
        W = request.weights
        M0 = request.initial_marking
        
        # Build RG first if not provided
        rg_data = reachability_analysis(P, T, F, W, M0)
        
        result = liveness_analysis(P, T, F, W, M0, reachability_data=rg_data)
        
        return LivenessResult(result=result)
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error analyzing liveness: {str(e)}")


@router.post("/siphons-traps", response_model=SiphonTrapResult)
def analyze_siphons_traps(request: PetriNetRequest):
    """
    Tìm siphons và traps
    """
    try:
        P = request.places
        T = request.transitions
        F = convert_arcs(request)
        W = request.weights
        
        result = siphons_traps_analysis(P, T, F, W)
        
        return SiphonTrapResult(result=result)
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error computing siphons/traps: {str(e)}")
