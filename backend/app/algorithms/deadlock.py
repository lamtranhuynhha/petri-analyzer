"""
Phát hiện deadlock dựa trên đồ thị reachability.
Deadlock = marking mà không có transition nào enabled.
"""

from typing import List, Dict, Tuple, Any
from .reachability import reachability_analysis, enabled


def deadlock_detection(
    places: List[str],
    transitions: List[str],
    arcs: List[Tuple[str, str]],
    weights: Dict[str, int],
    initial_marking: Dict[str, int]
) -> Dict[str, Any]:
    """
    Xác định tất cả các marking gây deadlock trong mạng Petri.
    """
    # Build reachability graph
    rg_data = reachability_analysis(places, transitions, arcs, weights, initial_marking)
    
    states = rg_data['states']
    deadlocks = []
    
    # Find states with no enabled transitions
    for marking in states:
        has_enabled = any(enabled(marking, t, arcs, weights) for t in transitions)
        if not has_enabled:
            deadlocks.append(marking)
    
    return {
        'total_states': len(states),
        'total_deadlocks': len(deadlocks),
        'deadlock_markings': deadlocks,
    }
