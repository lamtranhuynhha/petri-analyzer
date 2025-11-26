from typing import Dict, List, Set, Tuple, Any
from collections import deque

from app.core.schemas import PetriNetRequest, BoundednessLivenessResult
from app.models.petri_net import PetriNet


class SCCFinder:
    def __init__(self, root,nodes,edges):
        self.root:tuple[int] = root    # tuple: initial marking
        self.nodes: set[tuple] = nodes  # set: marking tuple -> PetriNet
        self.graph: dict[tuple, list[tuple[str, tuple]]] = edges  # dict: node -> list of (transition_name, target_node)
        self.idx:int  = 0
        self.stack = []
        self.visited = []
        self.lowest = {}
        self.num = {}
        self.on_stack = set()
        self.scc = []       # list of list of nodes (marking tuples)

    def run(self):
        for node in self.nodes:
            if node not in self.visited:
                self.strongconnect(node)
        return self.scc
    
    def strongconnect(self, node):
        self.visited.append(node)
        self.num[node] = self.idx
        self.lowest[node] = self.idx
        self.on_stack.add(node)
        self.idx += 1
        self.stack.append(node)

        for transition, neighbor in self.graph.get(node, []):
            if neighbor not in self.visited:
                self.strongconnect(neighbor)
                self.lowest[node] = min(self.lowest[node], self.lowest[neighbor])
            elif neighbor in self.on_stack:
                self.lowest[node] = min(self.lowest[node], self.num[neighbor])

        if self.lowest[node] == self.num[node]:
            component = []
            component_edges = []
            while True:
                w = self.stack.pop()
                self.on_stack.remove(w)
                component.append(w)
                if w == node:
                    break
            for w in component:
                for transition, neighbor in self.graph.get(w, []):
                        if neighbor in component and transition not in component_edges:
                            component_edges.append(transition)
            self.scc.append((component, component_edges))

def _build_reachability_graph_internal(net: PetriNet, max_states: int = 10000) -> Dict[str, Any]:
    """
    Xây dựng reachability graph nội bộ cho thuật toán liveness.
    Format tương tự petri_netV2.py để tương thích với code SCC.
    """
    visited: Set[Tuple[Tuple[str, int], ...]] = set()
    edges: Dict[Tuple, List[Tuple[str, Tuple]]] = {}
    queue: deque = deque()
    
    initial_marking = net.get_initial_marking()
    initial_tuple = tuple(sorted(initial_marking.items()))
    
    queue.append(initial_marking)
    visited.add(initial_tuple)
    nodes = {initial_tuple}
    
    while queue and len(nodes) < max_states:
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
    reachability_graph = _build_reachability_graph_internal(petri_net)
    # Tìm SCC Strong reachability graph
    graph = SCCFinder(reachability_graph['initial'], reachability_graph['nodes'], reachability_graph['edges'])
    sccs = graph.run()

    # Khởi tạo bảng liveness
    liveness_table = {}
    """
    Kiểm tra dead
    Một transition là dead nếu nó không xuất hiện trong đồ thị reachability.
    """
    def is_dead (transition):
        for marking in reachability_graph['nodes']:
            for t,next_marking in reachability_graph['edges'].get(marking, []):
                if t == transition:
                    return False
        return True
    
    """
    Kiểm tra L4-live
    Một transition là L4-live nếu nó xuất hiện trong tất cả các SCC của đồ thị reachability. 
    Đồng nghĩa với việc từ bất kỳ trạng thái nào trong đồ thị reachability, transition có thể được kích hoạt.
    """
            
    def is_live (transition):
        for scc_nodes, scc_edges in sccs:
            if transition not in scc_edges:
                return False
        return True
    
    """
    Kiểm tra L3-live
    Một transition là L3-live nếu nó xuất hiện trong một số SCC của đồ thị reachability. 
    Đồng nghĩa với việc từ một số trạng thái trong đồ thị reachability, transition có thể được kích hoạt vô hạn lần.
    """

    def is_L3_live (transition):
        for scc_nodes, scc_edges in sccs:
            if transition in scc_edges:
                return True
        return False
    
    """
    Kiểm tra L2-live
    Một transition là L2-live nếu nó có thể được kích hoạt k (k>1) lần trong một số chuỗi.
    """
    
    def is_L2_live (transition):
        marking_fire_transition= [(m, n) for m in reachability_graph['nodes']
                                    for t, n in reachability_graph['edges'].get(m, [])
                                    if t == transition]
        
        if len (marking_fire_transition) < 2:
            return False

        for u1, v1 in marking_fire_transition:
            visited = set()
            stack = [v1]
            while stack:
                cur = stack.pop()
                if cur in visited:
                    continue
                visited.add(cur)
                # Nếu cur là đầu của cạnh khác cũng là t
                if any(cur == u2 for (u2, _) in marking_fire_transition if u2 != u1):
                    return True
                for _, nxt in reachability_graph['edges'].get(cur, []):
                    if nxt not in visited:
                        stack.append(nxt)
        return False
    
    """
    L4 => L3 => L2 => L1 => Not Dead
    Điền bảng liveness
    """
    transition_list = list(petri_net.transitions)  # transitions là Set[str], không phải dict
    for t in transition_list:
        if is_dead(t):
            liveness_table[t] = (True, False,False,False,False)
        elif is_live(t):
            liveness_table[t] = (False,True,True,True,True)
        elif is_L3_live(t):
            liveness_table[t] = (False,True,True,True,False)
        elif is_L2_live(t):
            liveness_table[t] = (False,True,True,False,False)
        else: liveness_table[t] = (False,True,False,False,False)
    
    
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
    
    # Xác định các transition dead và unreachable
    dead_transitions = []
    unreachable_transitions = []
    live_transitions = []
    
    for transition, (is_dead, is_L1, is_L2, is_L3, is_L4) in liveness_table.items():
        if is_dead:
            dead_transitions.append(transition)
            unreachable_transitions.append(transition)
        elif is_L4:  # L4-live = fully live
            live_transitions.append(transition)
    
    # Petri net được coi là live nếu tất cả transitions đều L4-live
    is_live = len(live_transitions) == len(net.transitions) and len(dead_transitions) == 0
    
    return BoundednessLivenessResult(
        is_bounded=True,
        bound=None,
        unbounded_places=[],
        is_live=is_live,
        unreachable_transitions=unreachable_transitions
    )


