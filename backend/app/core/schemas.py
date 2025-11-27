"""
schemas.py
Khai báo các cấu trúc dữ liệu cho API (Pydantic models)
"""

from typing import List, Dict, Any, Optional, Union
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
    liveness_level: int = Field(..., description="Mức độ liveness (0-4): 0=dead, 1=L1-live, 2=L2-live, 3=L3-live, 4=L4-live")
    unreachable_transitions: List[str] = Field(..., description="Danh sách transition không bao giờ firing được")


class SiphonTrapResult(BaseModel):
    """
    Kết quả phân tích siphons và traps
    """
    siphons: List[List[str]] = Field(..., description="Danh sách các siphon tìm được")
    minimal_siphons: List[List[str]] = Field(..., description="Các siphon tối thiểu")
    traps: List[List[str]] = Field(..., description="Danh sách các trap tìm được")
    minimal_traps: List[List[str]] = Field(..., description="Các trap tối thiểu")

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


BoundednessResult = BoundednessLivenessResult
LivenessResult = BoundednessLivenessResult
