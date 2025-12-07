from typing import Dict, List, Set, Tuple, Any
from collections import deque

from app.core.schemas import PetriNetRequest, BoundednessLivenessResult
from app.models.petri_net import PetriNet


class SCCFinder:
    def __init__(self, root,nodes,edges):
        self.root:tuple[int] = root   
        self.nodes: set[tuple] = nodes  
        self.graph: dict[tuple, list[tuple[str, tuple]]] = edges  
        self.idx:int  = 0
        self.stack = []
        self.visited = set() 
        self.lowest = {}
        self.num = {}
        self.on_stack = set()
        self.scc = []      

    def run(self):
        # Đảm bảo reset lại trạng thái nếu run lại
        self.visited.clear()
        self.stack.clear()
        self.on_stack.clear()
        self.scc.clear()
        self.lowest.clear()
        self.num.clear()
        self.idx = 0

        for node in self.nodes:
            if node not in self.visited:
                self.strongconnect(node)
        return self.scc

    def strongconnect(self, node):
        self.visited.add(node)
        self.num[node] = self.idx
        self.lowest[node] = self.idx
        self.on_stack.add(node)
        self.idx += 1
        self.stack.append(node)

        neighbors = self.graph.get(node, [])
        for transition, neighbor in neighbors:
            if neighbor not in self.visited:
                self.strongconnect(neighbor)
                self.lowest[node] = min(self.lowest[node], self.lowest[neighbor])
            elif neighbor in self.on_stack:
                self.lowest[node] = min(self.lowest[node], self.num[neighbor])

        if self.lowest[node] == self.num[node]:
            component_nodes = []
            while True:
                w = self.stack.pop()
                self.on_stack.remove(w)
                component_nodes.append(w)
                if w == node:
                    break
            
            # Tìm các cạnh nội bộ (internal edges) của SCC này
            component_edges = set()
            node_set = set(component_nodes)
            
            for w in component_nodes:
                for transition, neighbor in self.graph.get(w, []):
                    if neighbor in node_set:
                        component_edges.add(transition)
            
            self.scc.append((component_nodes, list(component_edges)))


def _build_reachability_graph_internal(net: PetriNet, max_states: int = 10000) -> Dict[str, Any]:
    """
    Xây dựng reachability graph nội bộ cho thuật toán liveness.
    Throw lỗi nếu số lượng trạng thái vượt quá max_states.
    """
    visited: Set[Tuple[Tuple[str, int], ...]] = set()
    edges: Dict[Tuple, List[Tuple[str, Tuple]]] = {}
    queue: deque = deque()

    initial_marking = net.get_initial_marking()
    initial_tuple = tuple(sorted(initial_marking.items()))

    queue.append(initial_marking)
    visited.add(initial_tuple)
    nodes = {initial_tuple}

    while queue:
        if len(nodes) >= max_states:
            raise Exception(
                f"Reachability graph vượt quá max_states={max_states}. "
                f"Đồ thị có thể là vô hạn hoặc quá lớn."
            )

        current_marking = queue.popleft()
        current_tuple = tuple(sorted(current_marking.items()))

        enabled_transitions = net.get_enabled_transitions(current_marking)

        for transition in enabled_transitions:
            new_marking = net.fire_transition(transition, current_marking.copy())
            new_tuple = tuple(sorted(new_marking.items()))

            if new_tuple not in visited:
                visited.add(new_tuple)
                nodes.add(new_tuple)
                queue.append(new_marking)

            # Thêm edge
            if current_tuple not in edges:
                edges[current_tuple] = []
            edges[current_tuple].append((transition, new_tuple))

    return {
        'initial': initial_tuple,
        'nodes': nodes,
        'edges': edges
    }


def check_liveness(petri_net: PetriNet) -> Dict[str, Tuple[bool, bool, bool, bool, bool]]:
    """
    Kiểm tra trạng thái sống của transition trong Petri net.
    Trả về Bảng liveness với các mức độ:
    - Dead: Transition không thể bao giờ được kích hoạt.
    - L1-live: Transition có thể được kích hoạt ít nhất một lần.
    - L2-live: Transition có thể được kích hoạt k lần trong một số chuỗi.
    - L3-live: Transition có thể được kích hoạt vô hạn lần trong một số chuỗi.
    - Live: Transition có thể được kích hoạt từ bất kỳ trạng thái nào trong đồ thị reachability.
    """
    # Xây dựng reachability graph
    try:
        rg = _build_reachability_graph_internal(petri_net)
    except Exception as e:
        print(f"Liveness Check Error: {e}")
        return {}

    nodes = rg['nodes']
    edges = rg['edges']

    # 1. Tìm SCCs
    scc_finder = SCCFinder(rg['initial'], nodes, edges)
    sccs = scc_finder.run()

    #Tìm Sink SCCs
    node_to_scc_idx = {}
    for idx, (scc_nodes, _) in enumerate(sccs):
        for node in scc_nodes:
            node_to_scc_idx[node] = idx
    num_sccs = len(sccs)
    scc_has_outgoing = [False] * num_sccs

    for u, neighbors in edges.items():
        u_idx = node_to_scc_idx[u]
        for _, v in neighbors:
            v_idx = node_to_scc_idx.get(v)
            # Nếu có cạnh nối từ u (thuộc SCC này) sang v (thuộc SCC KHÁC)
            if v_idx is not None and u_idx != v_idx:
                scc_has_outgoing[u_idx] = True

    sink_sccs_indices = [i for i, has_out in enumerate(scc_has_outgoing) if not has_out]

    # --- Helper Functions ---
    def get_all_transitions_in_rg():
        found = set()
        for neighbors in edges.values():
            for t, _ in neighbors:
                found.add(t)
        return found

    all_transitions_in_rg = get_all_transitions_in_rg()

    def check_l2_by_dfs(transition):
        """Kiểm tra xem transition có bắn được ít nhất 2 lần trên một đường đi không"""
        starts = []
        for u, neighbors in edges.items():
            for t_name, v in neighbors:
                if t_name == transition:
                    starts.append((u, v))
        
        if len(starts) < 2:
            return False

        for _, v1 in starts:
            queue = deque([v1])
            visited_local = {v1}
            while queue:
                curr = queue.popleft()
                if curr in edges:
                    for t_next, v_next in edges[curr]:
                        if t_next == transition:
                            return True
                        if v_next not in visited_local:
                            visited_local.add(v_next)
                            queue.append(v_next)
        return False

    # ---------------------------------------------------------
    # Logic Xếp hạng Liveness
    # ---------------------------------------------------------
    liveness_table = {}
    all_transitions_defined = list(petri_net.transitions)

    for t in all_transitions_defined:
        # Check Dead (L0)
        if t not in all_transitions_in_rg:
            liveness_table[t] = (True, False, False, False, False)
            continue

        # Check Live (L4)
        # Transition phải xuất hiện trong cạnh nội bộ của TẤT CẢ các Sink SCCs
        is_l4 = True
        if not sink_sccs_indices:
            is_l4 = False
        else:
            for idx in sink_sccs_indices:
                scc_edges = sccs[idx][1]
                if t not in scc_edges:
                    is_l4 = False
                    break
        
        if is_l4:
            liveness_table[t] = (False, True, True, True, True)
            continue

        # Check L3
        # Chỉ cần xuất hiện trong BẤT KỲ một SCC nào (có vòng lặp)
        is_l3 = False
        for _, scc_edges in sccs:
            if t in scc_edges:
                is_l3 = True
                break
        
        if is_l3:
            liveness_table[t] = (False, True, True, True, False)
            continue

        # Level 2: Fireable k times (k >= 2)
        # Nếu không phải L3 (không loop), check xem có bắn được 2 lần trên đường thẳng không
        if check_l2_by_dfs(t):
            liveness_table[t] = (False, True, True, False, False)
            continue

        # Check L1 (Nếu đã không Dead thì mặc định L1)
        liveness_table[t] = (False, True, False, False, False)

    return liveness_table


def analyze_liveness(request: PetriNetRequest) -> BoundednessLivenessResult:
    """
    Phân tích tính liveness của mạng Petri.
    
    Args:
        request: Dữ liệu đầu vào của mạng Petri.
    
    Returns:
        BoundednessLivenessResult chứa thông tin về liveness.
    """
    net = PetriNet(request)
    liveness_table = check_liveness(net)

    dead_transitions = []
    unreachable_transitions = []
    live_transitions = []
    transition_liveness_levels = {}
    
    # Khởi tạo min_level là mức cao nhất, sẽ giảm dần nếu gặp mức thấp hơn
    min_level = 4 

    for transition, (is_dead, is_L1, is_L2, is_L3, is_L4) in liveness_table.items():
        level = 0
        if is_dead:
            level = 0
            dead_transitions.append(transition)
            unreachable_transitions.append(transition)
        elif is_L4:
            level = 4
            live_transitions.append(transition)
        elif is_L3:
            level = 3
        elif is_L2:
            level = 2
        elif is_L1:
            level = 1
            
        transition_liveness_levels[transition] = level
        
        # Cập nhật mức độ sống của toàn mạng (là mức thấp nhất của các transition)
        if level < min_level:
            min_level = level

    # Mạng Petri được gọi là Live (L4-system) nếu tất cả transition đều là L4
    is_system_live = (len(live_transitions) == len(net.transitions)) and (len(dead_transitions) == 0)

    if not net.transitions:
        min_level = 0

    return BoundednessLivenessResult(
        is_bounded=True,
        bound=None,
        unbounded_places=[],
        is_live=is_system_live,
        liveness_level=min_level,
        unreachable_transitions=unreachable_transitions,
        transition_liveness_levels=transition_liveness_levels
    )