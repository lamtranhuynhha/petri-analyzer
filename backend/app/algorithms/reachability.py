from typing import Dict, List, Set, Tuple, Any, Optional
from collections import deque

from app.core.schemas import PetriNetRequest, ReachabilityResult
from app.models.petri_net import PetriNet

def build_reachability_graph(net: PetriNet, max_nodes: int = 10000, max_depth: Optional[int] = None) -> Dict[str, Any]:
    """
    Xây reachability graph từ PetriNet từ models/petri_net.py.
    
    Args:
        net: PetriNet object từ models/petri_net.py
        max_nodes: chặn số lượng marking để tránh nổ trạng thái
        max_depth: chặn độ sâu BFS (None = không chặn)
    
    Returns:
        Dict chứa:
        - places: list tên place theo thứ tự
        - initial: marking khởi tạo (tuple)
        - nodes: set các marking (tuple)
        - edges: dict {marking: [(t_name, next_marking), ...]}
        - deadlocks: set các marking không có transition enabled
        - truncated: bool cho biết có bị cắt do max_nodes hay max_depth
        - parent: dict để truy vết đường đi
    """
    # Lấy danh sách place names theo thứ tự
    place_names = sorted(net.places.keys())
    
    # Hàm chuyển marking dict -> tuple để hash
    def marking_to_tuple(marking: Dict[str, int]) -> Tuple[int, ...]:
        return tuple(marking.get(p, 0) for p in place_names)
    
    # Hàm chuyển tuple -> marking dict
    def tuple_to_marking(marking_tuple: Tuple[int, ...]) -> Dict[str, int]:
        return {place_names[i]: marking_tuple[i] for i in range(len(place_names))}
    
    # Initial marking
    initial_marking = net.get_initial_marking()
    initial_tuple = marking_to_tuple(initial_marking)
    
    nodes: Set[Tuple[int, ...]] = {initial_tuple}
    edges: Dict[Tuple[int, ...], List[Tuple[str, Tuple[int, ...]]]] = {}
    deadlocks: Set[Tuple[int, ...]] = set()
    parent: Dict[Tuple[int, ...], Tuple[Optional[Tuple[int, ...]], Optional[str]]] = {initial_tuple: (None, None)}
    
    q = deque([(initial_tuple, 0)])
    truncated = False
    
    while q:
        current_tuple, depth = q.popleft()
        current_marking = tuple_to_marking(current_tuple)
        
        # Lấy các transition có thể kích hoạt
        enabled = net.get_enabled_transitions(current_marking)
        
        if not enabled:
            deadlocks.add(current_tuple)
        
        for transition_name in enabled:
            # Fire transition để có marking mới
            try:
                new_marking = net.fire_transition(transition_name, current_marking.copy())
                new_tuple = marking_to_tuple(new_marking)
                
                # Kiểm tra giới hạn trước khi thêm node
                if new_tuple not in nodes:
                    if max_depth is not None and depth + 1 > max_depth:
                        truncated = True
                        continue
                    if len(nodes) >= max_nodes:
                        truncated = True
                        continue
                    nodes.add(new_tuple)
                    parent[new_tuple] = (current_tuple, transition_name)
                    q.append((new_tuple, depth + 1))
                
                # Thêm cạnh
                if new_tuple in nodes:
                    edges.setdefault(current_tuple, []).append((transition_name, new_tuple))
            
            except ValueError:
                # Transition không thể fire (không nên xảy ra vì đã check enabled)
                continue
    
    return {
        "places": place_names,
        "initial": initial_tuple,
        "nodes": nodes,
        "edges": edges,
        "deadlocks": deadlocks,
        "truncated": truncated,
        "parent": parent,
    }

def format_marking(marking, place_names):
    return "{" + ", ".join(f"{place_names[i]}={marking[i]}" for i in range(len(marking))) + "}"

def reachability_to_dot(rg):
    """
    Xuất đồ thị ra chuỗi DOT (Graphviz) để vẽ, bố cục dọc (Top-Down) rõ ràng.
    """
    place_names = rg["places"]

    def mark_label(m):
        return "(" + " ".join(str(m[i]) for i in range(len(m))) + ")"

    # Tạo ID gọn cho node
    nodes = list(rg["nodes"])
    id_map = {m: f"M{i}" for i, m in enumerate(nodes)}

    lines = []
    lines.append("digraph RG {")
    lines.append("  // Bố cục dọc, tránh chồng chéo")
    lines.append("  rankdir=TB;")          # Top → Bottom
    lines.append("  layout=dot;")
    lines.append("  splines=true;")
    lines.append("  overlap=false;")
    lines.append("  nodesep=0.5;")         # khoảng cách giữa các node ngang
    lines.append("  ranksep=0.7;")         # khoảng cách giữa các tầng dọc
    lines.append("  node [shape=oval, fontname=Helvetica];")
    lines.append("  { rank=min; start; }")

    # Node
    for m in nodes:
        nid = id_map[m]
        lbl = mark_label(m)
        shape = "doublecircle" if m in rg.get("deadlocks", []) else "oval"
        lines.append(f'  {nid} [label="{lbl}", shape={shape}];')

    # Start arrow
    lines.append("  start [shape=point];")
    lines.append(f'  start -> {id_map[rg["initial"]]};')

    # Edges
    for m, outs in rg["edges"].items():
        for t, m2 in outs:
            lines.append(f'  {id_map[m]} -> {id_map[m2]} [label="{t}"];')

    lines.append("}")
    return "\n".join(lines)


def reconstruct_path(rg, target):
    # target là tuple marking có trong rg["nodes"]
    if target not in rg["parent"]:
        return None
    path = []
    cur = target
    while True:
        par, tname = rg["parent"][cur]
        if par is None:
            break
        path.append((tname, cur))
        cur = par
    path.reverse()
    return [t for t, _ in path]

def find_marking(rg: Dict[str, Any], predicate) -> Optional[Tuple[int, ...]]:
    """Tìm marking thỏa mãn predicate."""
    for m in rg["nodes"]:
        if predicate(m):
            return m
    return None


def analyze_reachability(
    request: PetriNetRequest,
    max_states: int = 10000
) -> ReachabilityResult:
    """
    Phân tích đồ thị đạt được (Reachability Graph) của một mạng Petri.
    
    Function chính để gọi từ API endpoint.

    Args:
        request: Dữ liệu đầu vào của mạng Petri.
        max_states: Số lượng trạng thái tối đa để tránh vòng lặp vô hạn.

    Returns:
        ReachabilityResult chứa danh sách các states, edges và ảnh đồ thị.
    """
    # Khởi tạo mạng Petri
    net = PetriNet(request)
    
    # Xây dựng reachability graph
    rg = build_reachability_graph(net, max_nodes=max_states)
    
    # Chuyển đổi format để trả về API
    place_names = rg["places"]
    markings: List[Dict[str, int]] = []
    edges: List[Dict[str, Any]] = []
    initial_tuple = rg["initial"]
    
    # Tạo mapping từ marking tuple -> index
    node_to_index: Dict[Tuple[int, ...], int] = {}

    node_to_index[initial_tuple] = 0
    markings.append({place_names[i]: initial_tuple[i] for i in range(len(place_names))})

    other_nodes = rg["nodes"] - {initial_tuple}

    for idx, marking_tuple in enumerate(other_nodes, start=1):
        node_to_index[marking_tuple] = idx
        # Chuyển tuple thành dict
        marking_dict = {place_names[i]: marking_tuple[i] for i in range(len(place_names))}
        markings.append(marking_dict)
    
    # Chuyển edges sang format API
    for source_tuple, transitions in rg["edges"].items():
        source_idx = node_to_index[source_tuple]
        for transition_name, target_tuple in transitions:
            target_idx = node_to_index[target_tuple]
            edges.append({
                'from': source_idx,
                'to': target_idx,
                'transition': transition_name
            })
    
    # Tạo ảnh đồ thị (nếu cần)
    # graph_image = reachability_to_dot(rg)  # Có thể thêm sau
    initial_marking = {
        place_names[i]: initial_tuple[i]
        for i in range(len(place_names))
    }
    deadlocks = [list(m) for m in rg["deadlocks"]]

    return ReachabilityResult(
        states=markings,
        initial_marking=initial_marking,
        deadlocks=deadlocks,
        edges=edges,
        graph_image=None  # Sẽ thêm logic tạo ảnh sau
    )