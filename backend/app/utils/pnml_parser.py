"""
PNML Parser - Parse và generate PNML (Petri Net Markup Language) files
"""

import xml.etree.ElementTree as ET
from typing import Dict, List, Any


def parse_pnml(pnml_string: str) -> Dict[str, Any]:
    """
    Parse PNML XML string thành JSON format chuẩn
    
    Returns:
        {
            'places': [str],
            'transitions': [str],
            'arcs': [[str, str]],
            'weights': {str: int},
            'initial_marking': {str: int}
        }
    """
    try:
        root = ET.fromstring(pnml_string)
        
        # Find net element
        net = root.find('.//{http://www.pnml.org/version-2009/grammar/pnml}net')
        if net is None:
            # Try without namespace
            net = root.find('.//net')
        if net is None:
            raise ValueError("No <net> element found in PNML")
        
        # Find page element (optional)
        page = net.find('.//{http://www.pnml.org/version-2009/grammar/pnml}page')
        if page is None:
            page = net.find('.//page')
        if page is None:
            page = net  # Use net directly if no page
        
        places = []
        transitions = []
        arcs = []
        weights = {}
        initial_marking = {}
        
        # Parse places
        for place in page.findall('.//{http://www.pnml.org/version-2009/grammar/pnml}place'):
            place_id = place.get('id')
            if not place_id:
                continue
            
            places.append(place_id)
            
            # Parse initial marking
            marking_elem = place.find('.//{http://www.pnml.org/version-2009/grammar/pnml}initialMarking')
            if marking_elem is None:
                marking_elem = place.find('.//initialMarking')
            
            if marking_elem is not None:
                text_elem = marking_elem.find('.//{http://www.pnml.org/version-2009/grammar/pnml}text')
                if text_elem is None:
                    text_elem = marking_elem.find('.//text')
                
                if text_elem is not None and text_elem.text:
                    try:
                        initial_marking[place_id] = int(text_elem.text)
                    except ValueError:
                        initial_marking[place_id] = 0
            else:
                initial_marking[place_id] = 0
        
        # Parse places without namespace (fallback)
        if not places:
            for place in page.findall('.//place'):
                place_id = place.get('id')
                if place_id:
                    places.append(place_id)
                    initial_marking[place_id] = 0
                    
                    marking_elem = place.find('.//initialMarking')
                    if marking_elem is not None:
                        text_elem = marking_elem.find('.//text')
                        if text_elem is not None and text_elem.text:
                            try:
                                initial_marking[place_id] = int(text_elem.text)
                            except ValueError:
                                pass
        
        # Parse transitions
        for trans in page.findall('.//{http://www.pnml.org/version-2009/grammar/pnml}transition'):
            trans_id = trans.get('id')
            if trans_id:
                transitions.append(trans_id)
        
        if not transitions:
            for trans in page.findall('.//transition'):
                trans_id = trans.get('id')
                if trans_id:
                    transitions.append(trans_id)
        
        # Parse arcs
        for arc in page.findall('.//{http://www.pnml.org/version-2009/grammar/pnml}arc'):
            source = arc.get('source')
            target = arc.get('target')
            
            if source and target:
                arcs.append([source, target])
                
                # Parse weight (inscription)
                weight_elem = arc.find('.//{http://www.pnml.org/version-2009/grammar/pnml}inscription')
                if weight_elem is None:
                    weight_elem = arc.find('.//inscription')
                
                weight = 1
                if weight_elem is not None:
                    text_elem = weight_elem.find('.//{http://www.pnml.org/version-2009/grammar/pnml}text')
                    if text_elem is None:
                        text_elem = weight_elem.find('.//text')
                    
                    if text_elem is not None and text_elem.text:
                        try:
                            weight = int(text_elem.text)
                        except ValueError:
                            weight = 1
                
                weight_key = f'["{source}","{target}"]'
                weights[weight_key] = weight
        
        if not arcs:
            for arc in page.findall('.//arc'):
                source = arc.get('source')
                target = arc.get('target')
                
                if source and target:
                    arcs.append([source, target])
                    weight_key = f'["{source}","{target}"]'
                    weights[weight_key] = 1
        
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


def generate_pnml(net_data: Dict[str, Any]) -> str:
    """
    Generate PNML XML string từ JSON format
    """
    pnml = ET.Element('pnml', xmlns="http://www.pnml.org/version-2009/grammar/pnml")
    net = ET.SubElement(pnml, 'net', id="net1", type="http://www.pnml.org/version-2009/grammar/ptnet")
    page = ET.SubElement(net, 'page', id="page1")
    
    # Add places
    for place_id in net_data.get('places', []):
        place_elem = ET.SubElement(page, 'place', id=place_id)
        
        # Add initial marking
        tokens = net_data.get('initial_marking', {}).get(place_id, 0)
        if tokens > 0:
            marking = ET.SubElement(place_elem, 'initialMarking')
            text = ET.SubElement(marking, 'text')
            text.text = str(tokens)
    
    # Add transitions
    for trans_id in net_data.get('transitions', []):
        ET.SubElement(page, 'transition', id=trans_id)
    
    # Add arcs
    arc_id = 1
    for arc in net_data.get('arcs', []):
        source, target = arc
        arc_elem = ET.SubElement(page, 'arc', id=f"arc{arc_id}", source=source, target=target)
        
        # Add weight
        weight_key = f'["{source}","{target}"]'
        weight = net_data.get('weights', {}).get(weight_key, 1)
        
        if weight > 1:
            inscription = ET.SubElement(arc_elem, 'inscription')
            text = ET.SubElement(inscription, 'text')
            text.text = str(weight)
        
        arc_id += 1
    
    # Convert to string with pretty formatting
    ET.indent(pnml, space="  ")
    return ET.tostring(pnml, encoding='unicode', xml_declaration=True)
