"""
schemas.py
------------
Khai báo các cấu trúc dữ liệu cho API (Pydantic models)
"""

from pydantic import BaseModel
from typing import List, Dict, Tuple, Any, Union, Optional


class PetriNetRequest(BaseModel):
    """
    Cấu trúc dữ liệu đầu vào của Petri Net.
    """
    places: List[str]
    transitions: List[str]
    arcs: List[List[str]]  # danh sách cung [source, target]
    weights: Dict[str, int]  # key là string "[\"source\",\"target\"]"
    initial_marking: Dict[str, int]


class ReachabilityResult(BaseModel):
    """
    Kết quả phân tích Reachability Graph
    """
    type: str = "reachability"
    success: bool = True
    result: Dict[str, Any]


class DeadlockResult(BaseModel):
    """
    Kết quả đầu ra của deadlock detection.
    """
    total_states: int
    total_deadlocks: int
    deadlock_markings: List[Dict[str, int]]


class BoundednessResult(BaseModel):
    """
    Kết quả phân tích boundedness
    """
    type: str = "boundedness"
    success: bool = True
    result: Dict[str, Any]


class LivenessResult(BaseModel):
    """
    Kết quả phân tích liveness
    """
    type: str = "liveness"
    success: bool = True
    result: Dict[str, Any]


class SiphonTrapResult(BaseModel):
    """
    Kết quả siphon & trap
    """
    type: str = "siphons-traps"
    success: bool = True
    result: Dict[str, Any]


class UploadFileResponse(BaseModel):
    """
    Response khi upload file
    """
    status: str = "success"
    message: str
    data: Dict[str, Any]


class ExportRequest(BaseModel):
    """
    Request để export Petri Net
    """
    net_data: Dict[str, Any]
    format: str  # 'pnml', 'json', 'png', 'svg'


class ConvertRequest(BaseModel):
    """
    Request để convert format
    """
    input_format: str
    output_format: str
    data: Union[str, Dict[str, Any]]


class VisualizationRequest(BaseModel):
    """
    Request để generate visualization
    """
    data: Dict[str, Any]  # RG data, tree data, or net data
    format: str = "svg"  # 'png' or 'svg'


class ErrorResponse(BaseModel):
    """
    Standard error response
    """
    status: str = "error"
    message: str
    details: Optional[Any] = None
