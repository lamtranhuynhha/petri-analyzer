"""
Phát hiện deadlock dựa trên đồ thị reachability.
Deadlock = marking mà không có transition nào enabled.
"""

from typing import List, Dict, Tuple, Any
from app.algorithms.reachability import reachability_graph, enabled


def deadlock_detection(
    P: List[str],
    T: List[str],
    F: List[Tuple[str, str]],
    W: Dict[Tuple[str, str], int],
    M0: Dict[str, int]
) -> Dict[str, Any]:
    """
    Xác định tất cả các marking gây deadlock trong mạng Petri.
    """
    V, E = reachability_graph(P, T, F, W, M0)
    deadlocks = [M for M in V if not enabled(M, T, F, W)]

    return {
        "total_states": len(V),
        "total_deadlocks": len(deadlocks),
        "deadlock_markings": deadlocks
    }
