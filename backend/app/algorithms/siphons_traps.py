"""
Siphons and Traps Detection
Algorithm 3 - CSP-based approach
"""

from typing import List, Dict, Tuple, Set, Any
from itertools import combinations


def get_preset(element: str, arcs: List[Tuple[str, str]]) -> Set[str]:
    """
    Get preset of an element (places/transitions that have arcs TO it)
    •element = {x | (x, element) in arcs}
    """
    return {source for source, target in arcs if target == element}


def get_postset(element: str, arcs: List[Tuple[str, str]]) -> Set[str]:
    """
    Get postset of an element (places/transitions that have arcs FROM it)
    element• = {x | (element, x) in arcs}
    """
    return {target for source, target in arcs if source == element}


def is_siphon(place_set: Set[str], arcs: List[Tuple[str, str]]) -> bool:
    """
    Check if a set of places is a siphon
    S is a siphon if •S ⊆ S•
    (all input transitions also have output to S)
    """
    # Get all transitions that are inputs to S
    input_transitions = set()
    for place in place_set:
        input_transitions.update(get_preset(place, arcs))
    
    # Get all transitions that are outputs from S
    output_transitions = set()
    for place in place_set:
        output_transitions.update(get_postset(place, arcs))
    
    # Siphon condition: •S ⊆ S•
    return input_transitions.issubset(output_transitions)


def is_trap(place_set: Set[str], arcs: List[Tuple[str, str]]) -> bool:
    """
    Check if a set of places is a trap
    Q is a trap if Q• ⊆ •Q
    (all output transitions also have input from Q)
    """
    # Get all transitions that are outputs from Q
    output_transitions = set()
    for place in place_set:
        output_transitions.update(get_postset(place, arcs))
    
    # Get all transitions that are inputs to Q
    input_transitions = set()
    for place in place_set:
        input_transitions.update(get_preset(place, arcs))
    
    # Trap condition: Q• ⊆ •Q
    return output_transitions.issubset(input_transitions)


def is_minimal(
    candidate: Set[str],
    collection: List[Set[str]]
) -> bool:
    """
    Check if candidate is minimal (no proper subset in collection)
    """
    for other in collection:
        if other < candidate:  # other is proper subset of candidate
            return False
    return True


def find_all_siphons_traps(
    places: List[str],
    arcs: List[Tuple[str, str]],
    max_size: int = None
) -> Tuple[List[Set[str]], List[Set[str]]]:
    """
    Find all siphons and traps using exhaustive search
    
    Returns:
        (all_siphons, all_traps)
    """
    if max_size is None:
        max_size = len(places)
    
    all_siphons = []
    all_traps = []
    
    # Try all possible subsets of places
    for size in range(1, min(max_size + 1, len(places) + 1)):
        for subset in combinations(places, size):
            place_set = set(subset)
            
            if is_siphon(place_set, arcs):
                all_siphons.append(place_set)
            
            if is_trap(place_set, arcs):
                all_traps.append(place_set)
    
    return all_siphons, all_traps


def filter_minimal(structures: List[Set[str]]) -> List[Set[str]]:
    """
    Filter to keep only minimal structures
    """
    minimal = []
    
    # Sort by size to check smaller sets first
    sorted_structures = sorted(structures, key=len)
    
    for candidate in sorted_structures:
        is_min = True
        for existing in minimal:
            if existing < candidate:  # existing is proper subset
                is_min = False
                break
        
        if is_min:
            # Also remove any existing that are supersets of candidate
            minimal = [s for s in minimal if not candidate < s]
            minimal.append(candidate)
    
    return minimal


def siphons_traps_analysis(
    places: List[str],
    transitions: List[str],
    arcs: List[Tuple[str, str]],
    weights: Dict[str, int]
) -> Dict[str, Any]:
    """
    Tìm tất cả siphons và traps, sau đó filter minimal
    """
    # Limit search to avoid explosion
    max_search_size = min(len(places), 10)  # Limit subset size
    
    all_siphons, all_traps = find_all_siphons_traps(places, arcs, max_search_size)
    
    # Filter to minimal
    minimal_siphons = filter_minimal(all_siphons)
    minimal_traps = filter_minimal(all_traps)
    
    # Convert to lists of lists for JSON serialization
    siphons_list = [sorted(list(s)) for s in all_siphons]
    traps_list = [sorted(list(t)) for t in all_traps]
    minimal_siphons_list = [sorted(list(s)) for s in minimal_siphons]
    minimal_traps_list = [sorted(list(t)) for t in minimal_traps]
    
    return {
        'siphons': siphons_list,
        'traps': traps_list,
        'minimal_siphons': minimal_siphons_list,
        'minimal_traps': minimal_traps_list,
        'total_siphons': len(all_siphons),
        'total_traps': len(all_traps),
    }


