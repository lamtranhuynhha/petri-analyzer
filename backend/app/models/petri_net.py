from dataclasses import dataclass, field
from typing import Dict, List, Set, Tuple, Optional, Any
from enum import Enum, auto

from pydantic import BaseModel, validator

from app.core.schemas import PetriNetRequest

class ArcDirection(Enum):
    """Hướng của cung trong mạng Petri."""
    IN = 'in'  # Place -> Transition
    OUT = 'out'  # Transition -> Place

@dataclass
class Place:
    name: str
    tokens: int = 0
    
    def __post_init__(self):
        if self.tokens < 0:
            raise ValueError("Số token phải >= 0")
    
    def __hash__(self):
        return hash(self.name)
    
    def __eq__(self, other):
        return isinstance(other, Place) and self.name == other.name

@dataclass
class Arc:
    source: str  # Tên của node nguồn (place hoặc transition)
    target: str  # Tên của node đích (place hoặc transition)
    weight: int = 1
    direction: ArcDirection = ArcDirection.IN
    
    def __post_init__(self):
        if self.weight <= 0:
            raise ValueError("Trọng số phải > 0")
    
    def can_consume(self, place_tokens: Dict[str, int]) -> bool:
        """Kiểm tra có thể tiêu thụ token từ place không."""
        if self.direction != ArcDirection.IN:
            return True
        return place_tokens.get(self.source, 0) >= self.weight
    
    def consume(self, place_tokens: Dict[str, int]) -> None:
        """Tiêu thụ token từ place."""
        if self.direction != ArcDirection.IN:
            return
        place_tokens[self.source] = place_tokens.get(self.source, 0) - self.weight
    
    def produce(self, place_tokens: Dict[str, int]) -> None:
        """Tạo token vào place."""
        if self.direction != ArcDirection.OUT:
            return
        place_tokens[self.target] = place_tokens.get(self.target, 0) + self.weight


class PetriNet:
    """
    Lớp đại diện cho một mạng Petri với kiến trúc được cải tiến.
    Kế thừa các ưu điểm từ petri_netV2.py nhưng tối ưu hóa cho mục đích phân tích.
    """
    
    def __init__(self, request: PetriNetRequest):
        """
        Khởi tạo mạng Petri từ đối tượng PetriNetRequest.
        
        Args:
            request: Dữ liệu đầu vào của mạng Petri đã được Pydantic validate.
        """
        # Lưu initial marking để có thể truy xuất sau
        self.initial_marking: Dict[str, int] = request.initial_marking.copy()
        
        # Khởi tạo các place với số token ban đầu
        self.places: Dict[str, Place] = {}
        self.transitions: Set[str] = set(request.transitions)
        self.arcs: List[Arc] = []
        
        # Tạo các place
        for place_name in request.places:
            tokens = request.initial_marking.get(place_name, 0)
            self.places[place_name] = Place(name=place_name, tokens=tokens)
        
        # Tạo các cung
        arc_weights = {tuple(arc): weight for arc, weight in request.weights.items()}
        
        for source, target in request.arcs:
            weight = arc_weights.get((source, target), 1)
            
            # Xác định hướng của cung
            if source in self.places and target in self.transitions:
                direction = ArcDirection.IN
            elif source in self.transitions and target in self.places:
                direction = ArcDirection.OUT
            else:
                raise ValueError(f"Cung không hợp lệ: {source} -> {target}")
            
            self.arcs.append(Arc(
                source=source,
                target=target,
                weight=weight,
                direction=direction
            ))
    
    def get_arcs_for_transition(self, transition: str) -> List[Arc]:
        """Lấy tất cả các cung liên quan đến một transition."""
        return [arc for arc in self.arcs if arc.source == transition or arc.target == transition]
    
    def get_input_arcs(self, transition: str) -> List[Arc]:
        """Lấy các cung đầu vào của một transition."""
        return [arc for arc in self.arcs 
                if arc.target == transition and arc.direction == ArcDirection.IN]
    
    def get_output_arcs(self, transition: str) -> List[Arc]:
        """Lấy các cung đầu ra của một transition."""
        return [arc for arc in self.arcs 
                if arc.source == transition and arc.direction == ArcDirection.OUT]
    
    def is_enabled(self, transition: str, marking: Optional[Dict[str, int]] = None) -> bool:
        """
        Kiểm tra xem một transition có thể kích hoạt được không.
        
        Args:
            transition: Tên của transition cần kiểm tra
            marking: Marking hiện tại, nếu None sử dụng marking hiện tại của các place
            
        Returns:
            True nếu transition có thể kích hoạt, False nếu không
        """
        if marking is None:
            marking = {name: place.tokens for name, place in self.places.items()}
            
        input_arcs = self.get_input_arcs(transition)
        return all(arc.can_consume(marking) for arc in input_arcs)
    
    def fire_transition(self, transition: str, marking: Dict[str, int]) -> Dict[str, int]:
        """
        Kích hoạt một transition và trả về marking mới.
        
        Args:
            transition: Tên của transition cần kích hoạt
            marking: Marking hiện tại
            
        Returns:
            Marking mới sau khi kích hoạt transition
            
        Raises:
            ValueError: Nếu transition không thể kích hoạt
        """
        if not self.is_enabled(transition, marking):
            raise ValueError(f"Không thể kích hoạt transition {transition} với marking hiện tại")
        
        # Tạo bản sao của marking hiện tại
        new_marking = marking.copy()
        
        # Xử lý các cung đầu vào (tiêu thụ token)
        for arc in self.get_input_arcs(transition):
            arc.consume(new_marking)
        
        # Xử lý các cung đầu ra (tạo token)
        for arc in self.get_output_arcs(transition):
            arc.produce(new_marking)
        
        return new_marking
    
    def get_enabled_transitions(self, marking: Optional[Dict[str, int]] = None) -> List[str]:
        """
        Lấy danh sách các transition có thể kích hoạt.
        
        Args:
            marking: Marking hiện tại, nếu None sử dụng marking hiện tại của các place
            
        Returns:
            Danh sách tên các transition có thể kích hoạt
        """
        if marking is None:
            marking = {name: place.tokens for name, place in self.places.items()}
            
        return [t for t in self.transitions if self.is_enabled(t, marking)]
    
    def get_marking(self) -> Dict[str, int]:
        """Lấy marking hiện tại của mạng."""
        return {name: place.tokens for name, place in self.places.items()}
    
    def get_initial_marking(self) -> Dict[str, int]:
        """Lấy marking ban đầu của mạng (từ request)."""
        return self.initial_marking.copy()
    
    def set_marking(self, marking: Dict[str, int]) -> None:
        """Thiết lập marking cho mạng."""
        for name, tokens in marking.items():
            if name in self.places:
                self.places[name].tokens = tokens
    
    def __repr__(self) -> str:
        """Biểu diễn chuỗi của đối tượng PetriNet."""
        places = ", ".join(f"{p.name}({p.tokens})" for p in self.places.values())
        return f"PetriNet(places=[{places}], transitions={list(self.transitions)})"
