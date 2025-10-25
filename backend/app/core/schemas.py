"""
schemas.py
------------
Khai báo các cấu trúc dữ liệu cho API (Pydantic models)
"""

from pydantic import BaseModel
from typing import List, Dict, Tuple, Any, Union


class PetriNetRequest(BaseModel):
    """
    Cấu trúc dữ liệu đầu vào của Petri Net.
    """
    places: List[str]
    transitions: List[str]
    arcs: List[List[str]]        # danh sách cung [source, target]
    weights: List[Dict[str, Any]]  # list of dicts with 'arc' and 'weight'
    initial_marking: Dict[str, int]


class DeadlockResult(BaseModel):
    """
    Kết quả đầu ra của deadlock detection.
    """
    total_states: int
    total_deadlocks: int
    deadlock_markings: List[Dict[str, int]]
