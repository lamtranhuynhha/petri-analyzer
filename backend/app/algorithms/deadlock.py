from typing import Dict, List, Set, Tuple, Deque
from collections import deque

from app.core.schemas import PetriNetRequest, DeadlockResult
from app.models.petri_net import PetriNet


def analyze_deadlock(request: PetriNetRequest) -> DeadlockResult:
    """
    Phân tích deadlock trong mạng Petri bằng cách xây dựng đồ thị đạt được.

    Thuật toán sử dụng BFS để duyệt qua tất cả các trạng thái có thể đạt được từ
    marking ban đầu và kiểm tra các trạng thái deadlock.

    Args:
        request: Dữ liệu đầu vào của mạng Petri.

    Returns:
        Một đối tượng DeadlockResult chứa thông tin về deadlock.
    """
    net = PetriNet(request)
    
    # Đánh dấu các trạng thái đã duyệt
    visited: Set[Tuple[Tuple[str, int], ...]] = set()
    # Hàng đợi cho BFS
    queue: Deque[Dict[str, int]] = deque()
    # Danh sách các trạng thái deadlock
    deadlock_markings: List[Dict[str, int]] = []
    
    # Lấy marking ban đầu
    initial_marking = net.get_initial_marking()
    queue.append(initial_marking)
    
    # Chuyển marking thành dạng tuple để có thể hash và lưu vào set
    initial_marking_tuple = tuple(sorted(initial_marking.items()))
    visited.add(initial_marking_tuple)
    
    while queue:
        current_marking = queue.popleft()
        
        # Lấy các transition có thể kích hoạt
        enabled_transitions = net.get_enabled_transitions(current_marking)
        
        # Nếu không có transition nào có thể kích hoạt, đây là deadlock
        if not enabled_transitions:
            deadlock_markings.append(current_marking)
            continue
        
        # Duyệt qua tất cả các transition có thể kích hoạt
        for transition in enabled_transitions:
            # Tạo bản sao của marking hiện tại để thao tác
            new_marking = net.fire_transition(transition, current_marking.copy())
            new_marking_tuple = tuple(sorted(new_marking.items()))
            
            # Nếu marking mới chưa được duyệt, thêm vào hàng đợi
            if new_marking_tuple not in visited:
                visited.add(new_marking_tuple)
                queue.append(new_marking)
    
    return DeadlockResult(
        total_states=len(visited),
        total_deadlocks=len(deadlock_markings),
        deadlock_markings=deadlock_markings
    )
