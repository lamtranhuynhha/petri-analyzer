class Place: 
    def __init__(self, tokens = 0, name = None):
        if tokens < 0: 
            raise ValueError("tokens must be >= 0")
        self.tokens = tokens
        self.name = name
    
    def __repr__(self):
        return f"Place(name = {self.name}, tokens = {self.tokens})"
    

class Arc:
    def __init__(self, place, weight = 1, direction = "in"):
        #direction:"in" = place -> transittion (input arc)
        # direction:"out" = transition -> place (output arc)
        if weight < 0:
            raise ValueError("weight must be >= 0")
        self.place = place
        self.weight = weight
        if direction not in ["in", "out"]:
            raise ValueError("direction must be 'in' or 'out'")
        self.direction = direction 
    
    def can_consume(self):
        #only use for input arcs
        if self.direction != "in":
            return True
        return self.place.tokens >= self.weight
    
    def consume(self):
        # Dùng cho input arc khi fire
        if self.direction != "in":
            return
        self.place.tokens -= self.weight
    
    def product(self):
        # Dùng cho output arc khi fire
        if self.direction != "out":
            return
        self.place.tokens += self.weight
        

class Transition:
    def __init__(self, name, in_arcs = None, out_arcs = None):
        self.name = name
        self.in_arcs = list(in_arcs or [])
        self.out_arcs = list(out_arcs or [])

    def __repr__(self):
        return f"Transition(name = {self.name}, in_arcs = {self.in_arcs}, out_arcs = {self.out_arcs})"
    
    def enable(self):
        return all(arc.can_consume() for arc in self.in_arcs)
    
    def fire(self):
        if not self.enable():
            return False
        for arc in self.in_arcs:
            arc.consume()
        for arc in self.out_arcs:
            arc.product()
        return True
    
class PetriNet:
    def __init__(self,places = None, transitions = None):
        self.places = list(places or [])
        self.transitions = {t.name: t for t in (transitions or [])}

    def marking(self):
        return [p.tokens for p in self.places]
    
    def fire_sequence(self, sequence):
        history = []
        for name in sequence:
            t = self.transitions[name]
            fired = t.fire()
            history.append((name, fired, self.marking()))
        return history

    def enabled_transitions(self):
        return [t for t in self.transitions.values() if t.enable()]


from collections import deque

def build_reachability_graph(net, max_nodes=10000, max_depth=None):
    """
    Xây reachability graph từ PetriNet 'net'.
    - max_nodes: chặn số lượng marking để tránh nổ trạng thái
    - max_depth: chặn độ sâu BFS (None = không chặn)
    Trả về dict gồm:
      places: list tên place theo thứ tự
      initial: marking khởi tạo (tuple)
      nodes: set các marking (tuple)
      edges: dict {marking: [(t_name, next_marking), ...]}
      deadlocks: set các marking không có transition enabled
      truncated: bool cho biết có bị cắt do max_nodes hay max_depth
    """
    places = list(net.places)
    print(places)
    place_idx = {p: i for i, p in enumerate(places)}

    def is_enabled(t, m):
        for arc in t.in_arcs:
            if m[place_idx[arc.place]] < arc.weight:
                return False
        return True

    def fire_on_marking(t, m):
        res = list(m)
        for arc in t.in_arcs:
            res[place_idx[arc.place]] -= arc.weight
        for arc in t.out_arcs:
            res[place_idx[arc.place]] += arc.weight
        return tuple(res)

    initial = tuple(p.tokens for p in places)
    nodes = {initial}
    edges = {}
    deadlocks = set()
    parent = {initial: (None, None)}  # marking -> (parent_marking, transition_name)

    q = deque([(initial, 0)])
    truncated = False

    while q:
        m, depth = q.popleft()
        enabled = [t for t in net.transitions.values() if is_enabled(t, m)]

        if not enabled:
            deadlocks.add(m)

        for t in enabled:
            m2 = fire_on_marking(t, m)

            # Kiểm tra giới hạn trước khi thêm node/cạnh
            if m2 not in nodes:
                if max_depth is not None and depth + 1 > max_depth:
                    truncated = True
                    continue
                if len(nodes) >= max_nodes:
                    truncated = True
                    continue
                nodes.add(m2)
                parent[m2] = (m, t.name)
                q.append((m2, depth + 1))

            # Chỉ thêm cạnh khi đích nằm trong nodes (nhất quán)
            if m2 in nodes:
                edges.setdefault(m, []).append((t.name, m2))

    return {
        "places": [p.name if p.name is not None else f"p{i}" for i, p in enumerate(places)],
        "initial": initial,
        "nodes": nodes,
        "edges": edges,
        "deadlocks": deadlocks,
        "truncated": truncated,
        "parent": parent,  # để truy vết đường đi ngắn nhất
    }

def format_marking(marking, place_names):
    return "{" + ", ".join(f"{place_names[i]}={marking[i]}" for i in range(len(marking))) + "}"

def reachability_to_dot(rg):
    """
    Xuất đồ thị ra chuỗi DOT (Graphviz) để vẽ, bố cục dọc (Top-Down) rõ ràng.
    """
    place_names = rg["places"]

    def mark_label(m):
        return "(" + " ".join(str(m[i]) for i in range(len(m))) + ")"

    # Tạo ID gọn cho node
    nodes = list(rg["nodes"])
    id_map = {m: f"M{i}" for i, m in enumerate(nodes)}

    lines = []
    lines.append("digraph RG {")
    lines.append("  // Bố cục dọc, tránh chồng chéo")
    lines.append("  rankdir=TB;")          # Top → Bottom
    lines.append("  layout=dot;")
    lines.append("  splines=true;")
    lines.append("  overlap=false;")
    lines.append("  nodesep=0.5;")         # khoảng cách giữa các node ngang
    lines.append("  ranksep=0.7;")         # khoảng cách giữa các tầng dọc
    lines.append("  node [shape=oval, fontname=Helvetica];")
    lines.append("  { rank=min; start; }")

    # Node
    for m in nodes:
        nid = id_map[m]
        lbl = mark_label(m)
        shape = "doublecircle" if m in rg.get("deadlocks", []) else "oval"
        lines.append(f'  {nid} [label="{lbl}", shape={shape}];')

    # Start arrow
    lines.append("  start [shape=point];")
    lines.append(f'  start -> {id_map[rg["initial"]]};')

    # Edges
    for m, outs in rg["edges"].items():
        for t, m2 in outs:
            lines.append(f'  {id_map[m]} -> {id_map[m2]} [label="{t}"];')

    lines.append("}")
    return "\n".join(lines)


def reconstruct_path(rg, target):
    # target là tuple marking có trong rg["nodes"]
    if target not in rg["parent"]:
        return None
    path = []
    cur = target
    while True:
        par, tname = rg["parent"][cur]
        if par is None:
            break
        path.append((tname, cur))
        cur = par
    path.reverse()
    return [t for t, _ in path]

def find_marking(rg, predicate):
    for m in rg["nodes"]:
        if predicate(m):
            return m
    return None

