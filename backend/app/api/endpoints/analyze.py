"""
analyze.py
------------
Các API phân tích Petri Net (reachability, deadlock, boundedness, liveness, siphons-traps)
"""

from fastapi import APIRouter, HTTPException
from app.core.schemas import (
    PetriNetRequest,
    DeadlockResult,
    BoundednessLivenessResult,
    SiphonTrapResult,
    ReachabilityResult
)
from app.algorithms.deadlock import analyze_deadlock
from app.algorithms.liveness import analyze_liveness
from app.algorithms.siphons_traps import analyze_siphons_traps
from app.algorithms.reachability import analyze_reachability
from app.algorithms.boundedness import analyze_boundedness

router = APIRouter(prefix="/analyze", tags=["Analysis"])


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
def api_analyze_deadlock(request: PetriNetRequest):
    try:
        result = analyze_deadlock(request)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error analyzing deadlock: {str(e)}")


@router.post("/liveness", response_model=BoundednessLivenessResult)
def api_analyze_liveness(request: PetriNetRequest):
    try:
        result = analyze_liveness(request)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error analyzing liveness: {str(e)}")


@router.post("/boundedness", response_model=BoundednessLivenessResult)
def api_analyze_boundedness(request: PetriNetRequest):
    try:
        result = analyze_boundedness(request)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error analyzing boundedness: {str(e)}")


@router.post("/siphons-traps", response_model=SiphonTrapResult)
def api_analyze_siphons_traps(request: PetriNetRequest):
    try:
        result = analyze_siphons_traps(request)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error analyzing siphons/traps: {str(e)}")


@router.post("/reachability", response_model=ReachabilityResult)
def api_analyze_reachability(request: PetriNetRequest, max_states: int = 1000):
    try:
        result = analyze_reachability(request, max_states=max_states)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error analyzing reachability: {str(e)}")
