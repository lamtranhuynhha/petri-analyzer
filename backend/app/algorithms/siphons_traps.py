from itertools import combinations

def find_minimal_siphons_and_traps(P, T, F):
    """
    Tìm minimal siphons và traps từ các danh sách Places, Transitions, và Flow (arcs).

    Tham số:
    P: List[str] - Danh sách các place (ví dụ: ['p1', 'p2'])
    T: List[str] - Danh sách các transition (ví dụ: ['t1', 't2'])
    F: List[Tuple[str, str]] - Danh sách các cung (flow) 
                                (ví dụ: [('p1', 't1'), ('t1', 'p2')])
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

    def siphon_constraint(s):
        if not s:
            return False
        
        pre_s = set()
        for p in s:
            pre_s.update(post_p.get(p, set()))

        post_s = set()
        for p in s:
            post_s.update(pre_p.get(p, set()))
            
        return pre_s.issubset(post_s)

    def trap_constraint(t_set):
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

    return [list(s) for s in minimal_siphons], [list(t) for t in minimal_traps]

# --- VÍ DỤ SỬ DỤNG ---
P_list = ["p1", "p2", "p3", "p4", "p5"]
T_list = ["t1", "t2", "t3", "t4", "t5", "t6"]
F_list = [
    ["p1", "t1"],["p1", "t2"],
    ["t1", "p2"],["t5","p2"],["p2","t3"],
    ["t2","p3"],["t6","p3"],["p3","t4"],
    ["t3","p4"],["p4","t5"],
    ["t4","p5"],["p5","t6"]
  ]

siphons, traps = find_minimal_siphons_and_traps(P_list, T_list, F_list)

print(f"Places: {P_list}")
print(f"Transitions: {T_list}")
print("---")
print(f"Minimal Siphons: {siphons}")
print(f"Minimal Traps: {traps}")