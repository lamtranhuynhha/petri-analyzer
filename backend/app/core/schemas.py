"""
schemas.py
Khai báo các cấu trúc dữ liệu cho API (Pydantic models)
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class PetriNetRequest(BaseModel):
    """
    Cấu trúc dữ liệu đầu vào của mạng Petri
    """
    places: List[str] = Field(..., description="Danh sách tên các place trong mạng")
    transitions: List[str] = Field(..., description="Danh sách tên các transition trong mạng")
    arcs: List[List[str]] = Field(..., description="Danh sách các cung dạng [nguồn, đích]")
    weights: Dict[str, int] = Field(..., description="Trọng số các cung, key dạng JSON string [\"source\",\"target\"]")
    initial_marking: Dict[str, int] = Field(..., description="Marking khởi tạo của mạng")


class ReachabilityResult(BaseModel):
    """
    Kết quả phân tích đồ thị đạt được
    """
    states: List[Dict[str, int]] = Field(..., description="Danh sách các marking (trạng thái)")
    edges: List[Dict[str, Any]] = Field(..., description="Danh sách các cạnh đồ thị")
    graph_image: Optional[str] = Field(None, description="Ảnh đồ thị dạng base64")


class ReachabilityResult(BaseModel):
    """
    Kết quả phân tích Reachability Graph
    """
    type: str = "reachability"
    success: bool = True
    result: Dict[str, Any]


class DeadlockResult(BaseModel):
    """
    Kết quả phát hiện deadlock
    """
    total_states: int = Field(..., description="Tổng số marking có thể đạt được")
    total_deadlocks: int = Field(..., description="Số lượng marking bị deadlock")
    deadlock_markings: List[Dict[str, int]] = Field(..., description="Danh sách các marking deadlock")


class BoundednessLivenessResult(BaseModel):
    """
    Kết quả kiểm tra boundedness và liveness
    """
    is_bounded: bool = Field(..., description="Petri Net có bị unbounded hay không")
    bound: Optional[int] = Field(None, description="Giá trị k-bounded (None nếu unbounded)")
    unbounded_places: List[str] = Field(..., description="Danh sách place có token tăng vô hạn")
    is_live: bool = Field(..., description="Petri Net có đảm bảo liveness không")
    unreachable_transitions: List[str] = Field(..., description="Danh sách transition không bao giờ firing được")


class SiphonTrapResult(BaseModel):
    """
    Kết quả phân tích siphons và traps
    """
    siphons: List[List[str]] = Field(..., description="Danh sách các siphon tìm được")
    minimal_siphons: List[List[str]] = Field(..., description="Các siphon tối thiểu")
    traps: List[List[str]] = Field(..., description="Danh sách các trap tìm được")
    minimal_traps: List[List[str]] = Field(..., description="Các trap tối thiểu")


class AnalysisResponse(BaseModel):
    """
    Phản hồi kết quả phân tích
    """
    status: str = Field(..., description="Trạng thái phản hồi (ok hoặc error)")
    message: Optional[str] = Field(None, description="Thông báo bổ sung")
    data: Optional[Dict[str, Any]] = Field(None, description="Dữ liệu kết quả")


# Alias cho tương thích ngược
BoundednessResult = BoundednessLivenessResult
LivenessResult = BoundednessLivenessResult
