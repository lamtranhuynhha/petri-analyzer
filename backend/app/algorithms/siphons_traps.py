from typing import List, Tuple, Set
from itertools import combinations

from app.core.schemas import PetriNetRequest, SiphonTrapResult
from app.models.petri_net import PetriNet


def find_minimal_siphons_and_traps(P: List[str], T: List[str], F: List[Tuple[str, str]]) -> Tuple[List[List[str]], List[List[str]]]:
    """
    Tìm minimal siphons và traps từ các danh sách Places, Transitions, và Flow (arcs).

    Tham số:
    P: List[str] - Danh sách các place (ví dụ: ['p1', 'p2'])
    T: List[str] - Danh sách các transition (ví dụ: ['t1', 't2'])
    F: List[Tuple[str, str]] - Danh sách các cung (flow) 
                                (ví dụ: [('p1', 't1'), ('t1', 'p2')])
    
    Returns:
        Tuple[List[List[str]], List[List[str]]]: (minimal_siphons, minimal_traps)
    """
    places_set = set(P)
    transitions_set = set(T)
    pre_p = {}  
    post_p = {} 

    for source, target in F:
        if source in places_set and target in transitions_set:
            pre_p.setdefault(source, set()).add(target)
        elif source in transitions_set and target in places_set:
            post_p.setdefault(target, set()).add(source)

    def solve(constraint_func, places_list):
        all_sets = []
        minimal_sets_for_pruning = set()
        n = len(places_list)
        
        for size in range(1, n + 1):
            for comb in combinations(places_list, size):
                candidate = set(comb)

                if any(s.issubset(candidate) for s in minimal_sets_for_pruning):
                    continue
                    
                if constraint_func(candidate):
                    all_sets.append(frozenset(candidate))
                    minimal_sets_for_pruning.add(frozenset(candidate))

        return all_sets

    def siphon_constraint(s: Set[str]) -> bool:
        if not s:
            return False
        
        pre_s = set()
        for p in s:
            pre_s.update(post_p.get(p, set()))

        post_s = set()
        for p in s:
            post_s.update(pre_p.get(p, set()))
            
        return pre_s.issubset(post_s)

    def trap_constraint(t_set: Set[str]) -> bool:
        if not t_set:
            return False
            
        post_t = set()
        for p in t_set:
            post_t.update(pre_p.get(p, set()))
            
        pre_t = set()
        for p in t_set:
            pre_t.update(post_p.get(p, set()))
        
        return post_t.issubset(pre_t)
    
    minimal_siphons = solve(siphon_constraint, P)
    minimal_traps = solve(trap_constraint, P)

    return [sorted(list(s)) for s in minimal_siphons], [sorted(list(t)) for t in minimal_traps]


def analyze_siphons_traps(request: PetriNetRequest) -> SiphonTrapResult:
    """
    Phân tích Siphons và Traps trong mạng Petri.

    Thuật toán tìm tất cả các minimal siphons và minimal traps.

    Args:
        request: Dữ liệu đầu vào của mạng Petri.

    Returns:
        SiphonTrapResult chứa danh sách các siphons và traps.
    """
    # Lấy dữ liệu từ request
    P = request.places
    T = request.transitions
    F = [tuple(arc) for arc in request.arcs]
    
    # Gọi thuật toán chính
    minimal_siphons, minimal_traps = find_minimal_siphons_and_traps(P, T, F)
    
    # Trả về kết quả theo schema
    # Note: Thuật toán này chỉ tìm minimal, nên siphons = minimal_siphons
    return SiphonTrapResult(
        siphons=minimal_siphons,
        minimal_siphons=minimal_siphons,
        traps=minimal_traps,
        minimal_traps=minimal_traps
    )