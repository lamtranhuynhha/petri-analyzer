"""
Boundedness Analysis using Coverability Tree
Algorithm 4 từ tài liệu
"""

from typing import List, Dict, Tuple, Any
from collections import deque


OMEGA = float('inf')  # Symbol for unbounded


def is_greater_equal(m1: Dict[str, Any], m2: Dict[str, Any], places: List[str]) -> bool:
    """
    Kiểm tra m1 >= m2 (component-wise)
    """
    for p in places:
        v1 = m1.get(p, 0)
        v2 = m2.get(p, 0)
        
        # Handle omega
        if v1 == OMEGA:
            continue
        if v2 == OMEGA:
            return False
        
        if v1 < v2:
            return False
    
    return True


def introduce_omega(m1: Dict[str, Any], m2: Dict[str, Any], places: List[str]) -> Dict[str, Any]:
    """
    Introduce omega for places that increased from m2 to m1
    m1 là marking mới, m2 là marking ancestor
    """
    result = m1.copy()
    
    for p in places:
        v1 = m1.get(p, 0)
        v2 = m2.get(p, 0)
        
        if v2 != OMEGA and v1 != OMEGA and v1 > v2:
            result[p] = OMEGA
    
    return result


def fire_with_omega(
    marking: Dict[str, Any],
    transition: str,
    arcs: List[Tuple[str, str]],
    weights: Dict[str, int]
) -> Dict[str, Any]:
    """
    Fire transition với xử lý omega
    """
    new_marking = {}
    
    # Initialize with current marking
    for p, v in marking.items():
        new_marking[p] = v
    
    # Consume tokens
    for (source, target) in arcs:
        if target == transition:
            weight_key = f'["{source}","{target}"]'
            weight = weights.get(weight_key, 1)
            
            current = new_marking.get(source, 0)
            if current == OMEGA:
                new_marking[source] = OMEGA
            else:
                new_marking[source] = current - weight
    
    # Produce tokens
    for (source, target) in arcs:
        if source == transition:
            weight_key = f'["{source}","{target}"]'
            weight = weights.get(weight_key, 1)
            
            current = new_marking.get(target, 0)
            if current == OMEGA:
                new_marking[target] = OMEGA
            else:
                new_marking[target] = current + weight
    
    return new_marking


def enabled_with_omega(
    marking: Dict[str, Any],
    transition: str,
    arcs: List[Tuple[str, str]],
    weights: Dict[str, int]
) -> bool:
    """
    Check if transition enabled with omega
    """
    for (source, target) in arcs:
        if target == transition:
            weight_key = f'["{source}","{target}"]'
            weight = weights.get(weight_key, 1)
            
            tokens = marking.get(source, 0)
            if tokens == OMEGA:
                continue  # Omega >= any weight
            if tokens < weight:
                return False
    
    return True


def boundedness_analysis(
    places: List[str],
    transitions: List[str],
    arcs: List[Tuple[str, str]],
    weights: Dict[str, int],
    initial_marking: Dict[str, int],
    max_nodes: int = 10000
) -> Dict[str, Any]:
    """
    Phân tích boundedness bằng Coverability Tree
    """
    # Build coverability tree
    root = initial_marking.copy()
    nodes = [root]
    edges = []
    
    # Track path from root to current node
    paths = {0: []}  # node_idx -> list of ancestor indices
    
    queue = deque([(0, root)])  # (node_idx, marking)
    truncated = False
    
    while queue:
        if len(nodes) >= max_nodes:
            truncated = True
            break
        
        current_idx, current_marking = queue.popleft()
        current_path = paths[current_idx]
        
        # Try firing each transition
        for trans in transitions:
            if enabled_with_omega(current_marking, trans, arcs, weights):
                new_marking = fire_with_omega(current_marking, trans, arcs, weights)
                
                # Check ancestors for omega introduction
                for ancestor_idx in current_path:
                    ancestor_marking = nodes[ancestor_idx]
                    if is_greater_equal(new_marking, ancestor_marking, places):
                        new_marking = introduce_omega(new_marking, ancestor_marking, places)
                
                # Add new node
                new_idx = len(nodes)
                nodes.append(new_marking)
                paths[new_idx] = current_path + [current_idx]
                
                edges.append({
                    'from': current_idx,
                    'to': new_idx,
                    'transition': trans
                })
                
                queue.append((new_idx, new_marking))
    
    # Analyze results
    has_omega = any(
        any(v == OMEGA for v in marking.values())
        for marking in nodes
    )
    
    is_bounded = not has_omega
    
    # Calculate k-bounded for each place
    place_bounds = {}
    unbounded_places = []
    
    for p in places:
        max_tokens = 0
        is_unbounded = False
        
        for marking in nodes:
            v = marking.get(p, 0)
            if v == OMEGA:
                is_unbounded = True
                break
            if v > max_tokens:
                max_tokens = v
        
        if is_unbounded:
            place_bounds[p] = OMEGA
            unbounded_places.append(p)
        else:
            place_bounds[p] = max_tokens
    
    k_value = max(
        (v for v in place_bounds.values() if v != OMEGA),
        default=0
    )
    
    return {
        'is_bounded': is_bounded,
        'k_value': k_value if is_bounded else None,
        'place_bounds': place_bounds,
        'unbounded_places': unbounded_places,
        'tree_nodes': len(nodes),
        'truncated': truncated,
    }


