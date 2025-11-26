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
    Generate DOT string cho Reachability Graph
    """
    if deadlocks is None:
        deadlocks = []
    
    # Convert deadlocks to set of tuples for easy lookup
    deadlock_set = set()
    for marking in deadlocks:
        marking_tuple = tuple(sorted(marking.items()))
        deadlock_set.add(marking_tuple)
    
    lines = []
    lines.append("digraph RG {")
    lines.append("  rankdir=TB;")
    lines.append("  node [shape=circle, style=filled];")
    lines.append("  ")
    
    # Nodes
    for idx, marking in enumerate(states):
        marking_tuple = tuple(sorted(marking.items()))
        label = "M" + str(idx) + "\\n" + str(tuple(marking.values()))
        
        # Check if deadlock
        if marking_tuple in deadlock_set:
            color = "red"
            style = "filled"
        elif idx == 0:
            color = "lightgreen"
            style = "filled"
        else:
            color = "lightblue"
            style = "filled"
        
        lines.append(f'  M{idx} [label="{label}", fillcolor="{color}", style="{style}"];')
    
    lines.append("  ")
    
    # Edges
    for edge in edges:
        from_idx = edge['from']
        to_idx = edge['to']
        trans = edge['transition']
        lines.append(f'  M{from_idx} -> M{to_idx} [label="{trans}"];')
    
    lines.append("}")
    
    return "\n".join(lines)


def generate_coverability_tree_dot(
    nodes: List[Dict[str, Any]],
    edges: List[Dict[str, Any]]
) -> str:
    """
    Generate DOT string cho Coverability Tree
    """
    lines = []
    lines.append("digraph CoverabilityTree {")
    lines.append("  rankdir=TB;")
    lines.append("  node [shape=circle];")
    lines.append("  ")
    
    # Nodes
    for idx, marking in enumerate(nodes):
        # Format marking with omega
        values = []
        for k, v in marking.items():
            if v == float('inf'):
                values.append('ω')
            else:
                values.append(str(v))
        
        label = "N" + str(idx) + "\\n(" + ",".join(values) + ")"
        lines.append(f'  N{idx} [label="{label}"];')
    
    lines.append("  ")
    
    # Edges
    for edge in edges:
        from_idx = edge['from']
        to_idx = edge['to']
        trans = edge['transition']
        lines.append(f'  N{from_idx} -> N{to_idx} [label="{trans}"];')
    
    lines.append("}")
    
    return "\n".join(lines)


def generate_petri_net_dot(
    places: List[str],
    transitions: List[str],
    arcs: List[List[str]],
    initial_marking: Dict[str, int]
) -> str:
    """
    Generate DOT string cho Petri Net structure
    """
    lines = []
    lines.append("digraph PetriNet {")
    lines.append("  rankdir=LR;")
    lines.append("  ")
    
    # Places
    for place in places:
        tokens = initial_marking.get(place, 0)
        label = f"{place}\\n({tokens})"
        lines.append(f'  {place} [shape=circle, label="{label}", style=filled, fillcolor=lightblue];')
    
    lines.append("  ")
    
    # Transitions
    for trans in transitions:
        lines.append(f'  {trans} [shape=box, label="{trans}", style=filled, fillcolor=lightgray];')
    
    lines.append("  ")
    
    # Arcs
    for arc in arcs:
        source, target = arc
        lines.append(f'  {source} -> {target};')
    
    lines.append("}")
    
    return "\n".join(lines)


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
    places: List[str],
    transitions: List[str],
    arcs: List[List[str]],
    initial_marking: Dict[str, int],
    format_type: str = "svg"
) -> bytes:
    """
    Render Petri Net structure to image
    """
    dot_string = generate_petri_net_dot(places, transitions, arcs, initial_marking)
    return render_dot_to_image(dot_string, format_type)
