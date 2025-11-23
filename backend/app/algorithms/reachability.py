"""
Reachability Graph Algorithm
Xây dựng đồ thị khả đạt cho Petri Net
"""

from typing import List, Dict, Tuple, Set, Any
from collections import deque


def enabled(marking: Dict[str, int], transition: str, arcs: List[Tuple[str, str]], weights: Dict[str, int]) -> bool:
    """
    Kiểm tra transition có enabled tại marking không
    """
    for (source, target) in arcs:
        if target == transition:  # Input arc to transition
            weight_key = f'["{source}","{target}"]'
            weight = weights.get(weight_key, 1)
            if marking.get(source, 0) < weight:
                return False
    return True


def fire_transition(
    marking: Dict[str, int],
    transition: str,
    arcs: List[Tuple[str, str]],
    weights: Dict[str, int]
) -> Dict[str, int]:
    """
    Fire transition và trả về marking mới
    """
    new_marking = marking.copy()
    
    # Consume tokens from input places
    for (source, target) in arcs:
        if target == transition:
            weight_key = f'["{source}","{target}"]'
            weight = weights.get(weight_key, 1)
            new_marking[source] = new_marking.get(source, 0) - weight
    
    # Produce tokens to output places
    for (source, target) in arcs:
        if source == transition:
            weight_key = f'["{source}","{target}"]'
            weight = weights.get(weight_key, 1)
            new_marking[target] = new_marking.get(target, 0) + weight
    
    return new_marking


def reachability_graph(
    places: List[str],
    transitions: List[str],
    arcs: List[Tuple[str, str]],
    weights: Dict[str, int],
    initial_marking: Dict[str, int],
    max_states: int = 10000
) -> Tuple[List[Dict[str, int]], List[Dict[str, Any]]]:
    """
    Xây dựng Reachability Graph
    
    Returns:
        V: List of markings (states)
        E: List of edges {from_idx, to_idx, transition}
    """
    V = [initial_marking]  # List of markings
    E = []  # List of edges
    
    # Map marking (as tuple) to index
    def marking_to_tuple(m):
        return tuple(m.get(p, 0) for p in places)
    
    marking_indices = {marking_to_tuple(initial_marking): 0}
    queue = deque([initial_marking])
    truncated = False
    
    while queue:
        if len(V) >= max_states:
            truncated = True
            break
        
        current_marking = queue.popleft()
        current_idx = marking_indices[marking_to_tuple(current_marking)]
        
        # Try firing each transition
        for trans in transitions:
            if enabled(current_marking, trans, arcs, weights):
                new_marking = fire_transition(current_marking, trans, arcs, weights)
                new_tuple = marking_to_tuple(new_marking)
                
                if new_tuple not in marking_indices:
                    # New state discovered
                    if len(V) >= max_states:
                        truncated = True
                        break
                    
                    marking_indices[new_tuple] = len(V)
                    V.append(new_marking)
                    queue.append(new_marking)
                
                # Add edge
                new_idx = marking_indices[new_tuple]
                E.append({
                    'from': current_idx,
                    'to': new_idx,
                    'transition': trans
                })
        
        if truncated:
            break
    
    return V, E, truncated


def reachability_analysis(
    places: List[str],
    transitions: List[str],
    arcs: List[Tuple[str, str]],
    weights: Dict[str, int],
    initial_marking: Dict[str, int]
) -> Dict[str, Any]:
    """
    Phân tích đầy đủ Reachability Graph
    """
    V, E, truncated = reachability_graph(places, transitions, arcs, weights, initial_marking)
    
    # Find deadlock states (no enabled transitions)
    deadlocks = []
    for marking in V:
        has_enabled = any(enabled(marking, t, arcs, weights) for t in transitions)
        if not has_enabled:
            deadlocks.append(marking)
    
    return {
        'states': V,
        'edges': E,
        'total_states': len(V),
        'truncated': truncated,
        'deadlocks': deadlocks,
    }
