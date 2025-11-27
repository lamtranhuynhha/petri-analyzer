"""
JSON Converter - Validate và normalize JSON Petri Net data
"""

from typing import Dict, Any, List


def validate_petri_net_json(data: Dict[str, Any]) -> bool:
    """
    Validate Petri Net JSON structure
    
    Required fields:
    - places: List[Dict] (each with 'id', optional 'label', 'position')
    - transitions: List[Dict] (each with 'id', optional 'label','position')
    - arcs: List[List[str]]
    - weights: Dict[str, int]
    - initial_marking: Dict[str, int]
    """
    required_fields = ['places', 'transitions', 'arcs', 'initial_marking']
    
    for field in required_fields:
        if field not in data:
            raise ValueError(f"Missing required field: {field}")
    
    # Validate types
    if not isinstance(data['places'], list):
        raise ValueError("'places' must be a list")
    
    if not isinstance(data['transitions'], list):
        raise ValueError("'transitions' must be a list")
    
    if not isinstance(data['arcs'], list):
        raise ValueError("'arcs' must be a list")
    
    if not isinstance(data['initial_marking'], dict):
        raise ValueError("'initial_marking' must be a dict")
    
    place_ids = set()
    transition_ids = set()
    
    # Validate each place
    for place in data['places']:
        if not isinstance(place, dict):
            raise ValueError(f"Each place must be a dict, got {type(place)}")
        # id 
        if 'id' not in place:
            raise ValueError("Each place must have an 'id'")
        if not isinstance(place['id'], str):
            raise ValueError(f"Id must be string, got {type(place['id'])}")
        pid = place['id']
        if pid in place_ids:
            raise ValueError(f"Duplicated place id '{pid}'")
        place_ids.add(pid)

        # label
        if 'label' not in place:
            place['label'] = place['id']
        elif not isinstance(place['label'], str):
            raise ValueError(f"Label must be string, got {type(place['label'])}")
        
        # position
        if 'position' not in place or not isinstance(place['position'], dict):
            raise ValueError(f"Place '{pid}' must have position")
        pos = place['position']
        if not isinstance(pos.get('x'), (int, float)):
            raise ValueError(f"Place '{pid}' position.x must be number")
        if not isinstance(pos.get('y'), (int, float)):
            raise ValueError(f"Place '{pid}' position.y must be number")
        
        #tokens
        if 'tokens' in place and not isinstance(place['tokens'], int):
            raise ValueError("place.tokens must be integer")
        if 'tokens' not in place:
            place['tokens'] = data['initial_marking'].get(pid, 0)

    # Validate each transition
    for transition in data['transitions']:
        if not isinstance(transition, dict):
            raise ValueError(f"Each transition must be a dict, got {type(transition)}")
        # id
        if 'id' not in transition:
            raise ValueError("Each transition must have an 'id'")
        if not isinstance(transition['id'], str):
            raise ValueError(f"Id must be string, got {type(transition['id'])}")
        tid = transition['id']
        if tid in transition_ids:
            raise ValueError(f"Duplicated transition id '{tid}'")
        transition_ids.add(tid)
        # label
        if 'label' in transition and not isinstance(transition['label'], str):
            raise ValueError("Transition.label must be string")
        if 'label' not in transition:
            transition['label'] = tid
        # position
        if 'position' not in transition or not isinstance(transition['position'], dict):
            raise ValueError(f"Transition '{tid}' must have position")
        pos = transition['position']
        if not isinstance(pos.get('x'), (int, float)):
            raise ValueError(f"Transition '{tid}' position.x must be number")
        if not isinstance(pos.get('y'), (int, float)):
            raise ValueError(f"Transition '{tid}' position.y must be number")

    # Validate arcs format
    for arc in data['arcs']:
        if not isinstance(arc, dict):
            raise ValueError("arc must be dict")
        if 'source' not in arc or 'target' not in arc:
            raise ValueError("arc must contain source and target")

        if not isinstance(arc['source'], str):
            raise ValueError("arc.source must be string")
        if not isinstance(arc['target'], str):
            raise ValueError("arc.target must be string")

        s = arc['source']
        t = arc['target']

        if s not in place_ids and s not in transition_ids:
            raise ValueError(f"Arc source '{s}' does not exist")
        if t not in place_ids and t not in transition_ids:
            raise ValueError(f"Arc target '{t}' does not exist")

        # type rule P→T or T→P
        if (s in place_ids and t in place_ids) or (s in transition_ids and t in transition_ids):
            raise ValueError(f"Invalid arc: {s}->{t}")

    
    # Validate initial marking
    for key, val in data['initial_marking'].items():
        if not isinstance(key, str):
            raise ValueError("initial_marking key must be string")
        if not isinstance(val, int):
            raise ValueError("initial_marking value must be integer")

    for pid in place_ids:
        if pid not in data['initial_marking']:
            data['initial_marking'][pid] = 0
    
    # Ensure weights field exists
    if 'weights' in data:
        if not isinstance(data['weights'], dict):
            raise ValueError("'weights' must be a dict")
        for k, v in data['weights'].items():
            if not isinstance(k, str):
                raise ValueError("weights key must be string")
            if not isinstance(v, int):
                raise ValueError("weights value must be integer")
    else:
        data['weights'] = {}
    
    return True


def normalize_petri_net_json(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalize Petri Net JSON to standard format
    """
    validate_petri_net_json(data)
    
    # Ensure all places have initial marking
    normalized = {
    'places': [p['id'] for p in data['places']],
    'transitions': [t['id'] for t in data['transitions']],
    'arcs': [[a['source'], a['target']] for a in data['arcs']],
    'weights': data.get('weights', {}),
    'initial_marking': {}
    }

    

    for place in normalized['places']:
        normalized['initial_marking'][place] = data.get('initial_marking', {}).get(place, 0)
    
    # Ensure all arcs have weights
    for arc in normalized['arcs']:
        source, target = arc
        weight_key = f'["{source}","{target}"]'
        if weight_key not in normalized['weights']:
            normalized['weights'][weight_key] = 1
    print(normalized)
    return normalized


def convert_to_backend_format(frontend_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convert frontend format to backend format if needed
    Handles different naming conventions (camelCase vs snake_case)
    """
    # Map frontend keys to backend keys
    key_mapping = {
        'initialMarking': 'initial_marking',
        'initial_marking': 'initial_marking',
    }
    
    converted = {}
    for key, value in frontend_data.items():
        new_key = key_mapping.get(key, key)
        converted[new_key] = value
    
    return normalize_petri_net_json(converted)
