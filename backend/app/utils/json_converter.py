"""
JSON Converter - Validate và normalize JSON Petri Net data
"""

from typing import Dict, Any, List


def validate_petri_net_json(data: Dict[str, Any]) -> bool:
    """
    Validate Petri Net JSON structure
    
    Required fields:
    - places: List[str]
    - transitions: List[str]
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
    
    # Validate arcs format
    for arc in data['arcs']:
        if not isinstance(arc, list) or len(arc) != 2:
            raise ValueError("Each arc must be [source, target]")
    
    # Validate initial marking
    for place in data['places']:
        if place not in data['initial_marking']:
            # Auto-fill with 0
            data['initial_marking'][place] = 0
    
    # Ensure weights field exists
    if 'weights' not in data:
        data['weights'] = {}
    
    return True


def normalize_petri_net_json(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalize Petri Net JSON to standard format
    """
    validate_petri_net_json(data)
    
    # Ensure all places have initial marking
    normalized = {
        'places': data['places'],
        'transitions': data['transitions'],
        'arcs': data['arcs'],
        'weights': data.get('weights', {}),
        'initial_marking': {}
    }
    
    for place in data['places']:
        normalized['initial_marking'][place] = data.get('initial_marking', {}).get(place, 0)
    
    # Ensure all arcs have weights
    for arc in data['arcs']:
        source, target = arc
        weight_key = f'["{source}","{target}"]'
        if weight_key not in normalized['weights']:
            normalized['weights'][weight_key] = 1
    
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
