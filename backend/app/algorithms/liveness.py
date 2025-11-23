"""
Liveness Analysis using Tarjan SCC Algorithm
Algorithms 5 & 6 từ tài liệu
"""

from typing import List, Dict, Tuple, Any, Set
from collections import defaultdict, deque


def tarjan_scc(graph: Dict[int, List[int]]) -> List[Set[int]]:
    """
    Tarjan's algorithm for finding Strongly Connected Components
    
    Args:
        graph: Adjacency list {node: [neighbors]}
    
    Returns:
        List of SCCs (each SCC is a set of node indices)
    """
    index_counter = [0]
    stack = []
    lowlinks = {}
    index = {}
    on_stack = defaultdict(bool)
    sccs = []
    
    def strongconnect(node):
        index[node] = index_counter[0]
        lowlinks[node] = index_counter[0]
        index_counter[0] += 1
        on_stack[node] = True
        stack.append(node)
        
        # Consider successors
        for successor in graph.get(node, []):
            if successor not in index:
                strongconnect(successor)
                lowlinks[node] = min(lowlinks[node], lowlinks[successor])
            elif on_stack[successor]:
                lowlinks[node] = min(lowlinks[node], index[successor])
        
        # If node is a root node, pop the stack
        if lowlinks[node] == index[node]:
            component = set()
            while True:
                w = stack.pop()
                on_stack[w] = False
                component.add(w)
                if w == node:
                    break
            sccs.append(component)
    
    for node in graph:
        if node not in index:
            strongconnect(node)
    
    return sccs


def classify_liveness(
    transition: str,
    sccs: List[Set[int]],
    state_to_idx: Dict[tuple, int],
    edges: List[Dict[str, Any]],
    states: List[Dict[str, int]]
) -> str:
    """
    Classify liveness level of a transition
    
    Returns:
        'Dead', 'L1', 'L2', 'L3', 'Live' (L4)
    """
    # Build transition occurrence info
    trans_in_edges = [e for e in edges if e['transition'] == transition]
    
    if not trans_in_edges:
        return 'Dead'
    
    # Check if transition appears in any SCC (terminal or non-terminal)
    trans_states = set(e['from'] for e in trans_in_edges)
    
    # Find which SCCs contain this transition
    sccs_with_trans = []
    for scc in sccs:
        if any(state_idx in scc for state_idx in trans_states):
            sccs_with_trans.append(scc)
    
    if not sccs_with_trans:
        return 'L1'  # Potentially fireable but not in any cycle
    
    # Check if transition is in a terminal SCC (no outgoing edges to other SCCs)
    terminal_sccs = []
    for scc in sccs:
        is_terminal = True
        for node in scc:
            for e in edges:
                if e['from'] == node and e['to'] not in scc:
                    is_terminal = False
                    break
            if not is_terminal:
                break
        if is_terminal and len(scc) > 1:  # Non-trivial SCC
            terminal_sccs.append(scc)
    
    # L4 (Live): Transition can fire infinitely in all reachable sequences
    # Simplified: transition appears in all terminal SCCs
    if any(any(state_idx in scc for state_idx in trans_states) for scc in terminal_sccs):
        # Check if it's truly live (can fire from any reachable marking)
        return 'Live'
    
    # L3: Can fire infinitely often in some firing sequence
    if sccs_with_trans:
        return 'L3'
    
    # L2: Can fire at least k times for any k
    # L1: Can fire at least once
    return 'L1'


def liveness_analysis(
    places: List[str],
    transitions: List[str],
    arcs: List[Tuple[str, str]],
    weights: Dict[str, int],
    initial_marking: Dict[str, int],
    reachability_data: Dict[str, Any] = None
) -> Dict[str, Any]:
    """
    Phân tích liveness cho tất cả transitions
    Requires reachability graph data
    """
    if not reachability_data:
        # Need to build RG first
        from .reachability import reachability_analysis
        reachability_data = reachability_analysis(places, transitions, arcs, weights, initial_marking)
    
    states = reachability_data['states']
    edges = reachability_data['edges']
    
    if not states:
        return {
            'is_live': False,
            'details': {t: 'Dead' for t in transitions}
        }
    
    # Build adjacency list for SCC algorithm
    graph = defaultdict(list)
    for edge in edges:
        graph[edge['from']].append(edge['to'])
    
    # Find SCCs
    sccs = tarjan_scc(dict(graph))
    
    # Build state to index mapping
    def marking_to_tuple(m):
        return tuple(m.get(p, 0) for p in places)
    
    state_to_idx = {marking_to_tuple(states[i]): i for i in range(len(states))}
    
    # Classify each transition
    liveness_levels = {}
    for trans in transitions:
        level = classify_liveness(trans, sccs, state_to_idx, edges, states)
        liveness_levels[trans] = level
    
    # Overall liveness: network is live if all transitions are L4
    is_live = all(level == 'Live' for level in liveness_levels.values())
    
    # Find dead and live transitions
    dead_transitions = [t for t, level in liveness_levels.items() if level == 'Dead']
    live_transitions = [t for t, level in liveness_levels.items() if level == 'Live']
    
    return {
        'is_live': is_live,
        'details': liveness_levels,
        'dead_transitions': dead_transitions,
        'live_transitions': live_transitions,
    }


