"""
Graphviz Helper - Generate DOT files và render với Graphviz
"""

from typing import List, Dict, Any
import subprocess
import tempfile
import os

def generate_rg_dot(
    states: List[Dict[str, int]],
    edges: List[Dict[str, Any]],
    deadlocks: List[Dict[str, int]] = None
) -> str:
    """
    Generate DOT string phong cách "Rounded Box"
    """
    if deadlocks is None:
        deadlocks = []
    
    deadlock_set = set()
    for marking in deadlocks:
        marking_tuple = tuple(sorted(marking.items()))
        deadlock_set.add(marking_tuple)
    
    lines = []
    lines.append("digraph RG {")
    
    # --- GLOBAL SETTINGS ---
    # rankdir=LR: Vẽ từ Trái sang Phải
    lines.append("  rankdir=LR;") 
    lines.append("  nodesep=0.5; ranksep=1.0;")
    lines.append("  splines=true;") 
    
    lines.append('  node [shape=box, style="rounded,filled", fontname="Helvetica", fontsize=12, height=0.5, penwidth=1.5];')
    lines.append('  edge [fontname="Helvetica", fontsize=10, arrowsize=0.8];')
    lines.append("  ")

    # --- MÀU SẮC ---
    COLOR_START_FILL = "#E8F5E9" 
    COLOR_START_BORDER = "#2E7D32"
    
    COLOR_DEAD_FILL = "#FFEBEE"  
    COLOR_DEAD_BORDER = "#C62828"
    
    COLOR_NORM_FILL = "#FFFFFF"  
    COLOR_NORM_BORDER = "#424242"

    # --- NODES ---
    for idx, marking in enumerate(states):
        marking_tuple = tuple(sorted(marking.items()))
        
        # Format label: (1, 0)
        sorted_values = [str(v) for k, v in sorted(marking.items())]
        marking_str = "(" + ",".join(sorted_values) + ")"
        label_text = f"<M{idx}<BR/><B>{marking_str}</B>>"

        if marking_tuple in deadlock_set:
            fill = COLOR_DEAD_FILL
            border = COLOR_DEAD_BORDER
            style = "rounded,filled" 
        elif idx == 0:
            fill = COLOR_START_FILL
            border = COLOR_START_BORDER
            style = "rounded,filled,bold"
        else:
            fill = COLOR_NORM_FILL
            border = COLOR_NORM_BORDER
            style = "rounded,filled"

        lines.append(
            f'  M{idx} ['
            f'label={label_text}, '
            f'fillcolor="{fill}", '
            f'color="{border}", '
            f'style="{style}"'
            f'];'
        )
    
    lines.append("  ")
    
    # --- EDGES ---
    for edge in edges:
        from_idx = edge['from']
        to_idx = edge['to']
        trans = edge['transition']
        edge_label = f'''<
                <TABLE BORDER="0" CELLBORDER="0" CELLSPACING="0" CELLPADDING="4">
                    <TR><TD>{trans}</TD></TR>
                </TABLE>
                >'''
        
        lines.append(f'  M{from_idx} -> M{to_idx} [label={edge_label}, color="#555555"];')
    
    lines.append("}")
    return "\n".join(lines)


def generate_coverability_tree_dot(
    nodes: List[Dict[str, Any]],
    edges: List[Dict[str, Any]]
) -> str:
    """
    Generate DOT string Coverability Tree theo style "RG Pro V9":
    - Layout: LR (Trái sang phải).
    - Node: Rounded Box.
    - Marking: In đậm (<B>...</B>).
    - Unbounded Node (chứa ω): Style nét đứt màu đỏ (giống Deadlock).
    - Edge Label: Nền trắng thoáng.
    """
    
    lines = []
    lines.append("digraph CoverabilityTree {")
    
    # --- GLOBAL SETTINGS (Copy từ RG V9) ---
    lines.append("  rankdir=LR;") 
    lines.append("  nodesep=0.6; ranksep=1.2;")
    lines.append("  splines=true;") 
    lines.append('  node [shape=box, style="rounded,filled", fontname="Helvetica", fontsize=12, height=0.5, penwidth=1.5];')
    lines.append('  edge [fontname="Helvetica", fontsize=11, arrowsize=0.8];')
    lines.append("  ")
    
    # --- COLORS ---
    # Dùng màu cảnh báo cho node chứa Omega (Unbounded)
    COLOR_OMEGA_FILL = "#FFEBEE"
    COLOR_OMEGA_BORDER = "#C62828"
    
    COLOR_NORM_FILL = "#FFFFFF"
    COLOR_NORM_BORDER = "#424242"

    # --- NODES ---
    for idx, marking in enumerate(nodes):
        # 1. Xử lý Marking và tìm Omega
        sorted_values = []
        has_omega = False
        
        for k, v in sorted(marking.items()):
            if v == float('inf'):
                sorted_values.append('ω') # Thay inf bằng ω
                has_omega = True
            else:
                sorted_values.append(str(v))
        
        marking_str = "(" + ",".join(sorted_values) + ")"
        
        # 2. Tạo HTML Label (In đậm marking)
        # Ví dụ: N0 xuống dòng (1, ω)
        label_text = f"<N{idx}<BR/><B>{marking_str}</B>>"

        # 3. Xác định Style
        if has_omega:
            # Node vô cùng -> Style nét đứt màu đỏ
            fill = COLOR_OMEGA_FILL
            border = COLOR_OMEGA_BORDER
            style = "rounded,filled"
        else:
            # Node thường -> Trắng
            fill = COLOR_NORM_FILL
            border = COLOR_NORM_BORDER
            style = "rounded,filled"

        lines.append(
            f'  N{idx} ['
            f'label={label_text}, ' # Nhớ: Không dùng dấu " bao quanh HTML
            f'fillcolor="{fill}", '
            f'color="{border}", '
            f'style="{style}"'
            f'];'
        )
    
    lines.append("  ")
    
    # --- EDGES (Style nền trắng padding) ---
    for edge in edges:
        from_idx = edge['from']
        to_idx = edge['to']
        trans = edge['transition']
        
        edge_label = f'''<
        <TABLE BORDER="0" CELLBORDER="0" CELLSPACING="0" CELLPADDING="4">
            <TR><TD>{trans}</TD></TR>
        </TABLE>
        >'''
        
        lines.append(f'  N{from_idx} -> N{to_idx} [label={edge_label}, color="#555555"];')
    
    lines.append("}")
    return "\n".join(lines)


def generate_petri_net_dot(net_data: Dict[str, Any]) -> str:
    """
    Generate DOT string for a petri net
    """
    try:
        lines = []
        lines.append("digraph PetriNet {")
        lines.append("  rankdir=LR;")
        lines.append("  nodesep=0.5;")
        lines.append("  ranksep=1.5;")
        lines.append("  newrank=true;") 
        
        place_color = "#2c4da6"
        trans_color = "#008a8a"
        arc_color = "#a0a0a0"

        # Make sure ID valid
        def safe_id(val):
            return f'"{val}"'

        # --- 1. PLACES ---
        for p in net_data.get("places", []):
            pid = p["id"]
            pname = p.get("label", pid)
            token_count = net_data.get("initial_marking", {}).get(pid, 0)
            
            # Calculate and perform tokens
            label_content = ""
            fontsize = 14
            if token_count > 0:
                if token_count < 10:
                    raw_dots = "●" * token_count
                    chunks = [raw_dots[i:i+3] for i in range(0, len(raw_dots), 3)]
                    label_content = "\\n".join(chunks) 
                    fontsize = 20 if token_count <= 3 else 16
                else:
                    label_content = str(token_count)
            
         
            lines.append(f'  subgraph "cluster_{pid}" {{') 
            lines.append(f'    peripheries=0;')     
            lines.append(f'    label="{pname}";')    
            lines.append(f'    labelloc="b";')      
            lines.append(f'    fontname="Helvetica"; fontsize=12;')
            
            # NODE DEFINITION
            lines.append(
                f'    {safe_id(pid)} ['
                f'shape=circle, '
                f'label="{label_content}", '
                f'style=solid, '
                f'color="{place_color}", '
                f'penwidth=2.5, '
                f'fontsize={fontsize}, '
                f'width=0.8, fixedsize=true' 
                f'];'
            )
            lines.append('  }') 
        
        # --- 2. TRANSITIONS ---
        for t in net_data.get("transitions", []):
            tid = t["id"]
            tname = t.get("label", tid)
            
            lines.append(f'  subgraph "cluster_{tid}" {{')
            lines.append(f'    peripheries=0;')
            lines.append(f'    label="{tname}";')
            lines.append(f'    labelloc="b";')
            lines.append(f'    fontname="Helvetica"; fontsize=12;')

            lines.append(
                f'    {safe_id(tid)} ['
                f'shape=box, label="", '
                f'style="rounded,solid", color="{trans_color}", penwidth=2.5, '
                f'width=0.5, height=1.2];'
            )
            lines.append('  }')
        
        # --- 3. ARCS ---
        weights = net_data.get("weights", {})
        for arc in net_data.get("arcs", []):
            src = arc["source"]
            tgt = arc["target"]
     
            lookup_key = f'["{src}","{tgt}"]'
            weight = weights.get(lookup_key, 1)
            
            label_attr = ""
            if weight != 1:
                label_attr = f'label="{weight}", fontcolor="black"'

            lines.append(
                f'  {safe_id(src)} -> {safe_id(tgt)} ['
                f'color="{arc_color}", penwidth=1.5, arrowsize=0.8, {label_attr}];'
            )
        
        lines.append("}")
        return "\n".join(lines)
        
    except Exception as e:
        raise RuntimeError(f"Error generating DOT: {str(e)}")


def render_dot_to_image(dot_string: str, format_type: str = "svg") -> bytes:
    """
    Render DOT string sang image format bằng Graphviz
    
    Args:
        dot_string: DOT format string
        format_type: 'svg' or 'png'
    
    Returns:
        Image bytes
    """
    try:
        # Write DOT to temp file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.dot', delete=False) as f:
            f.write(dot_string)
            dot_file = f.name
        
        # Output file
        output_file = dot_file.replace('.dot', f'.{format_type}')
        
        # Run Graphviz
        cmd = ['dot', f'-T{format_type}', dot_file, '-o', output_file]
        
        try:
            subprocess.run(cmd, check=True, capture_output=True, text=True)
        except FileNotFoundError:
            # Graphviz not installed, return placeholder
            raise RuntimeError(
                "Graphviz not installed. Please install graphviz: "
                "apt-get install graphviz (Linux) or brew install graphviz (Mac)"
            )
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Graphviz error: {e.stderr}")
        
        # Read output
        with open(output_file, 'rb') as f:
            image_data = f.read()
        
        # Cleanup
        os.unlink(dot_file)
        os.unlink(output_file)
        
        return image_data
    
    except Exception as e:
        # Fallback: return DOT string as text
        raise RuntimeError(f"Error rendering with Graphviz: {str(e)}")


def render_reachability_graph(
    states: List[Dict[str, int]],
    edges: List[Dict[str, Any]],
    deadlocks: List[Dict[str, int]],
    format_type: str = "svg"
) -> bytes:
    """
    Render Reachability Graph to image
    """
    dot_string = generate_rg_dot(states, edges, deadlocks)
    return render_dot_to_image(dot_string, format_type)


def render_coverability_tree(
    nodes: List[Dict[str, Any]],
    edges: List[Dict[str, Any]],
    format_type: str = "svg"
) -> bytes:
    """
    Render Coverability Tree to image
    """
    dot_string = generate_coverability_tree_dot(nodes, edges)
    return render_dot_to_image(dot_string, format_type)


def render_petri_net(
    net_data:Dict[str,Any],
    format_type: str = "svg"
) -> bytes:
    """
    Render Petri Net structure to image
    """
    dot_string = generate_petri_net_dot(net_data)
    return render_dot_to_image(dot_string, format_type)

# --- TEST RG RENDER ---
if __name__ == "__main__":
    test_states = [
        {"p1": 1, "p2": 0}, 
        {"p1": 0, "p2": 1}, 
        {"p1": 1, "p2": 1}, 
        {"p1": 0, "p2": 0}, # Deadlock
    ]

    test_edges = [
        {"from": 0, "to": 1, "transition": "t1"},
        {"from": 1, "to": 2, "transition": "t2"},
        {"from": 2, "to": 0, "transition": "t3"},
        {"from": 1, "to": 3, "transition": "t4"},
    ]

    test_deadlocks = [
        {"p1": 0, "p2": 0}
    ]

    print("Generating Reachability Graph (Rounded Style)...")
    
    try:
        image_bytes = render_reachability_graph(test_states, test_edges, test_deadlocks, format_type="png")
        
        if image_bytes:
            filename = "rg_rounded_style.png"
            with open(filename, "wb") as f:
                f.write(image_bytes)
            print(f"DONE! File created: {filename}")
    except Exception as e:
        print(f"ERROR: {e}")