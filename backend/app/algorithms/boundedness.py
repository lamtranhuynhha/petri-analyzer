from collections import deque
from typing import List, Tuple, Dict, Optional, Union, Set, Any

from app.core.schemas import PetriNetRequest, BoundednessLivenessResult
from app.models.petri_net import PetriNet


class CoverabilityTree:
    """Coverability Tree để phân tích boundedness của Petri Net."""
    
    def __init__(self, petri_net: PetriNet, initial_marking: Optional[Dict[str, int]] = None):
        self.net = petri_net
        
        # Nếu không truyền initial_marking, lấy từ net
        if initial_marking is None:
            initial_marking = self.net.get_initial_marking()
        
        # Lấy danh sách place names theo thứ tự
        self.place_names = sorted(self.net.places.keys())
        
        # Chuyển marking dict -> tuple
        self.initial_marking = self._marking_to_tuple(initial_marking)
        
        self.place_idx = {name: i for i, name in enumerate(self.place_names)}
        self.nodes = []
        self.edges = {}  # {marking: [(transition_name, new_marking), ...]}
        self.build_tree()
    
    def _marking_to_tuple(self, marking: Dict[str, int]) -> Tuple[Union[int, str], ...]:
        """Chuyển marking dict -> tuple."""
        return tuple(marking.get(p, 0) for p in self.place_names)
    
    def _tuple_to_marking(self, marking_tuple: Tuple[Union[int, str], ...]) -> Dict[str, Union[int, str]]:
        """Chuyển tuple -> marking dict."""
        return {self.place_names[i]: marking_tuple[i] for i in range(len(self.place_names))}
    
    def is_enabled(self, marking: Tuple[Union[int, str], ...], transition_name: str) -> bool:
        """Check if a transition is enabled in given marking."""
        input_arcs = self.net.get_input_arcs(transition_name)
        
        for arc in input_arcs:
            place_idx = self.place_idx[arc.source]
            # Nếu marking có 'ω', coi như có đủ token
            if marking[place_idx] == 'ω':
                continue
            if marking[place_idx] < arc.weight:
                return False
        return True
    
    def fire_transition(self, marking: Tuple[Union[int, str], ...], transition_name: str) -> Tuple[Union[int, str], ...]:
        """Fire a transition and return new marking."""
        new_marking = list(marking)
        
        # Lấy input và output arcs
        input_arcs = self.net.get_input_arcs(transition_name)
        output_arcs = self.net.get_output_arcs(transition_name)
        
        # Loại tokens trong input places
        for arc in input_arcs:
            place_idx = self.place_idx[arc.source]
            if new_marking[place_idx] != 'ω':
                new_marking[place_idx] -= arc.weight
        
        # Thêm tokens vào output places
        for arc in output_arcs:
            place_idx = self.place_idx[arc.target]
            if new_marking[place_idx] == 'ω':
                new_marking[place_idx] = 'ω'
            else:
                new_marking[place_idx] += arc.weight
        
        return tuple(new_marking)
    
    def replace_with_omega(self, marking1, marking2):
        """Replace positions where marking2 > marking1 with ω (infinity)"""
        result = []
        for i in range(len(marking1)):
            m1_val = marking1[i]
            m2_val = marking2[i]
            
            # Nếu marking1 đã có ω, giữ nguyên
            if m1_val == 'ω':
                result.append('ω')
            # Nếu marking2 > marking1, thay bằng ω
            elif m2_val != 'ω' and m2_val > m1_val:
                result.append('ω')
            else:
                result.append(m2_val)
        return tuple(result)
    
    def is_covered_by(self, marking1, marking2):
        """
        Check if marking1 is covered by marking2
        marking1 ≤ marking2 (component-wise)
        """
        for i in range(len(marking1)):
            m1_val = marking1[i]
            m2_val = marking2[i]
            
            # ω covers everything
            if m2_val == 'ω':
                continue
            # Nothing covers ω
            if m1_val == 'ω':
                return False
            # Compare numeric values
            if m1_val > m2_val:
                return False
        return True
    
    def marking_equal(self, m1, m2):
        """Check if two markings are equal"""
        return m1 == m2
    
    def build_tree(self):
        """Build the coverability tree using BFS"""
        # Queue: (marking, parent_path)
        # parent_path: list of ancestor markings from root to parent
        queue = deque([(self.initial_marking, [])])
        visited = {}  # marking -> True if fully explored
        self.nodes = [self.initial_marking]
        self.edges = {}
        
        while queue:
            current_marking, parent_path = queue.popleft()
            
            # Mark as visited
            if current_marking in visited:
                continue
            visited[current_marking] = True
            
            # Try firing each transition
            for t_name in self.net.transitions:
                if not self.is_enabled(current_marking, t_name):
                    continue
                
                new_marking = self.fire_transition(current_marking, t_name)
                
                # Check for ω acceleration
                # If new_marking is covered by an ancestor, apply ω-rule
                omega_applied = False
                for ancestor in parent_path + [current_marking]:
                    if self.is_covered_by(ancestor, new_marking) and not self.marking_equal(ancestor, new_marking):
                        # Replace components where new_marking > ancestor with ω
                        new_marking = self.replace_with_omega(ancestor, new_marking)
                        omega_applied = True
                        break
                
                # Add edge
                if current_marking not in self.edges:
                    self.edges[current_marking] = []
                self.edges[current_marking].append((t_name, new_marking))
                
                # Add to nodes if not visited
                if new_marking not in visited:
                    self.nodes.append(new_marking)
                    queue.append((new_marking, parent_path + [current_marking]))
    
    def is_bounded(self, bound=None):
        """
        Check if Petri Net is bounded
        If bound=None, check if k-bounded for any k (no ω)
        If bound=k, check if all markings ≤ k
        """
        for marking in self.nodes:
            for value in marking:
                if value == 'ω':
                    return False
                if bound is not None and value > bound:
                    return False
        return True
    
    def get_bound(self):
        """Get the bound k if net is k-bounded"""
        if not self.is_bounded():
            return None
        
        max_tokens = 0
        for marking in self.nodes:
            for value in marking:
                if value != 'ω' and value > max_tokens:
                    max_tokens = value
        return max_tokens
    
    def get_unbounded_places(self) -> List[str]:
        """Lấy danh sách các place unbounded (có ω)."""
        unbounded = set()
        for marking in self.nodes:
            for i, value in enumerate(marking):
                if value == 'ω':
                    unbounded.add(self.place_names[i])
        return sorted(list(unbounded))
    
    def print_tree(self):
        """Print the coverability tree."""
        place_names = self.place_names
        
        print("=" * 60)
        print("COVERABILITY TREE")
        print("=" * 60)
        print(f"Places: {place_names}")
        print(f"Initial Marking: {self.initial_marking}\n")
        
        print("Nodes:")
        for i, marking in enumerate(self.nodes):
            print(f"  M{i}: {marking}")
        
        print("\nEdges:")
        node_to_id = {marking: i for i, marking in enumerate(self.nodes)}
        for marking, transitions in self.edges.items():
            src_id = node_to_id[marking]
            for t_name, next_marking in transitions:
                dst_id = node_to_id.get(next_marking, "?")
                print(f"  M{src_id} --{t_name}--> M{dst_id} : {next_marking}")
        
        print("\n" + "=" * 60)
        print(f"Is Bounded: {self.is_bounded()}")
        if self.is_bounded():
            print(f"Bound (k): {self.get_bound()}")
        else:
            print("Net is UNBOUNDED (contains ω)")
        print("=" * 60)
    
    def to_dot(self):
        """Export coverability tree to DOT format for Graphviz"""
        place_names = [p.name if p.name else f"p{i}" for i, p in enumerate(self.places)]
        node_to_id = {marking: i for i, marking in enumerate(self.nodes)}
        
        lines = []
        lines.append("digraph CoverabilityTree {")
        lines.append("  rankdir=TB;")
        lines.append("  node [shape=oval, fontname=Helvetica];")
        lines.append("  { rank=min; start; }")
        
        # Nodes
        for marking, node_id in node_to_id.items():
            label = "(" + " ".join(str(v) for v in marking) + ")"
            lines.append(f'  M{node_id} [label="{label}"];')
        
        # Start arrow
        lines.append("  start [shape=point];")
        lines.append(f'  start -> M{node_to_id[self.initial_marking]};')
        
        # Edges
        for marking, transitions in self.edges.items():
            src_id = node_to_id[marking]
            for t_name, next_marking in transitions:
                dst_id = node_to_id[next_marking]
                lines.append(f'  M{src_id} -> M{dst_id} [label="{t_name}"];')
        
        lines.append("}")
        return "\n".join(lines)


def analyze_boundedness(request: PetriNetRequest) -> BoundednessLivenessResult:
    """
    Phân tích tính bị chặn (Boundedness) của mạng Petri sử dụng Coverability Tree.
    
    Thuật toán xây dựng coverability tree với ω (omega) để phát hiện unbounded places.

    Args:
        request: Dữ liệu đầu vào của mạng Petri.

    Returns:
        BoundednessLivenessResult chứa kết quả phân tích.
    """
    # Khởi tạo mạng Petri
    net = PetriNet(request)
    
    # Xây dựng coverability tree
    tree = CoverabilityTree(net)
    
    # Kiểm tra boundedness
    is_bounded = tree.is_bounded()
    bound = tree.get_bound() if is_bounded else None
    unbounded_places = tree.get_unbounded_places()
    
    return BoundednessLivenessResult(
        is_bounded=is_bounded,
        bound=bound,
        unbounded_places=unbounded_places,
        is_live=False,  # Default to False since we don't know
        liveness_level=0,  # Default to dead (0) since we don't know
        unreachable_transitions=[],  # We don't analyze reachability in boundedness check
        transition_liveness_levels={}
    )