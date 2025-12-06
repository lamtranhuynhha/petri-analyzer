"""
PNML Parser - Parse và generate PNML (Petri Net Markup Language) files
"""

import xml.etree.ElementTree as ET
from typing import Dict, List, Any


import xml.etree.ElementTree as ET
from typing import Dict, Any, List

def parse_pnml(pnml_string: str) -> Dict[str, Any]:
    """
    Parse PNML XML string thành JSON format chuẩn.
    
    Trả về dict với keys:
        - places: [{'id', 'label', 'position': {'x','y'}}]
        - transitions: [{'id', 'label', 'position': {'x','y'}}]
        - arcs: [[source_id, target_id]]
        - weights: {"[source,target]": int}
        - initial_marking: {place_id: int}
    """
    try:
        # Parse XML
        root = ET.fromstring(pnml_string)
        ns = {'pnml': 'http://www.pnml.org/version-2009/grammar/pnml'}

        # Net
        net = root.find('pnml:net', ns)
        if net is None:
            raise ValueError("No <net> element found in PNML")

        # Page (optional)
        page = net.find('pnml:page', ns)
        if page is None:
            page = net  # fallback

        places = []
        transitions = []
        arcs = []
        weights = {}
        initial_marking = {}

        # ----------- Places -----------
        for place in page.findall('pnml:place', ns):
            pid = place.get('id')
            if not pid:
                continue

            # Label
            name_elem = place.find('pnml:name/pnml:text', ns)
            label = name_elem.text if name_elem is not None else pid

            # Position
            pos_elem = place.find('pnml:graphics/pnml:position', ns)
            x = int(pos_elem.get('x', 0)) if pos_elem is not None else 0
            y = int(pos_elem.get('y', 0)) if pos_elem is not None else 0

            places.append({'id': pid, 'label': label, 'position': {'x': x, 'y': y}})

            # Initial marking
            marking_elem = place.find('pnml:initialMarking/pnml:text', ns)
            initial_marking[pid] = int(marking_elem.text) if marking_elem is not None and marking_elem.text else 0

        # ----------- Transitions -----------
        for t in page.findall('pnml:transition', ns):
            tid = t.get('id')
            if not tid:
                continue

            # Label
            name_elem = t.find('pnml:name/pnml:text', ns)
            label = name_elem.text if name_elem is not None else tid

            # Position
            pos_elem = t.find('pnml:graphics/pnml:position', ns)
            x = int(pos_elem.get('x', 0)) if pos_elem is not None else 0
            y = int(pos_elem.get('y', 0)) if pos_elem is not None else 0

            transitions.append({'id': tid, 'label': label, 'position': {'x': x, 'y': y}})

        # ----------- Arcs -----------
        for arc in page.findall('pnml:arc', ns):
            source = arc.get('source')
            target = arc.get('target')
            if not source or not target:
                continue

            arcs.append({
                'source': source,
                'target': target
            })

            # Weight
            weight_elem = arc.find('pnml:inscription/pnml:text', ns)
            weight = int(weight_elem.text) if weight_elem is not None and weight_elem.text else 1
            key = f'["{source}","{target}"]'
            weights[key] = weight

        return {
            'places': places,
            'transitions': transitions,
            'arcs': arcs,
            'weights': weights,
            'initial_marking': initial_marking
        }

    except ET.ParseError as e:
        raise ValueError(f"Invalid PNML XML: {str(e)}")
    except Exception as e:
        raise ValueError(f"Error parsing PNML: {str(e)}")



def generate_pnml(data: Dict[str, Any]) -> str:
    ns = ""
    ET.register_namespace("", ns)

    pnml = ET.Element('pnml', xmlns="http://www.pnml.org/version-2009/grammar/pnml")
    net = ET.SubElement(pnml, 'net', id="net", type="http://www.pnml.org/version-2009/grammar/ptnet")
    page = ET.SubElement(net, 'page', id="page")

    # Places
    for p in data.get("places", []):
        place = ET.SubElement(page, "place", id=p.get("id"))
        graphics = ET.SubElement(place, "graphics")
        pos = ET.SubElement(graphics, "position", {
            "x": str(p.get("position", {}).get("x", 0)),
            "y": str(p.get("position", {}).get("y", 0))
        })

        name = ET.SubElement(place,"name")
        ntext = ET.SubElement(name,"text")
        ntext.text = p.get("label", p.get("id"))

        marking = ET.SubElement(place, "initialMarking")
        mtext = ET.SubElement(marking, "text")
        mtext.text = str(data.get("initial_marking", {}).get(p.get("id"), 0))

    # Transitions
    for t in data.get("transitions", []):
        trans = ET.SubElement(page, "transition", id=t.get("id"))
        graphics = ET.SubElement(trans, "graphics")
        pos = ET.SubElement(graphics, "position", {
            "x": str(t.get("position", {}).get("x", 0)),
            "y": str(t.get("position", {}).get("y", 0))
        })
        name = ET.SubElement(trans,"name")
        ntext = ET.SubElement(name,"text")
        ntext.text = t.get("label", t.get("id"))

    # Arcs
    weights = data.get("weights", {})
    print(weights)

    for arc_info in data.get("arcs", []):
        arc = ET.SubElement(page, "arc", {
            "id": arc_info.get("id","0"),
            "source": arc_info["source"],
            "target": arc_info["target"]
        })

        ins = ET.SubElement(arc, "inscription")
        itext = ET.SubElement(ins, "text")

        import json
        key = json.dumps([arc_info["source"], arc_info["target"]],separators=(',', ':'))


        weight = weights.get(key, 1)
        print(key, ":", weight)

        itext.text = str(weight)


    ET.indent(pnml, space="  ")
    return ET.tostring(pnml, encoding='unicode', xml_declaration=True)


