""
Unit tests for the JSON converter module.
"""
import unittest
import json
import os
from pathlib import Path

# Import the module to test
from app.utils.json_converter import JSONConverter

class TestJSONConverter(unittest.TestCase):
    """Test cases for the JSON converter."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.converter = JSONConverter()
        
        # Sample Petri Net data
        self.sample_net = {
            'name': 'Test Net',
            'description': 'A test Petri net',
            'places': [
                {
                    'id': 'p1',
                    'label': 'Place 1',
                    'tokens': 2,
                    'x': 100,
                    'y': 100,
                    'metadata': {'color': 'red'}
                },
                {
                    'id': 'p2',
                    'label': 'Place 2',
                    'tokens': 0,
                    'x': 300,
                    'y': 100
                }
            ],
            'transitions': [
                {
                    'id': 't1',
                    'label': 'Transition 1',
                    'x': 200,
                    'y': 100,
                    'metadata': {'rate': 1.0}
                }
            ],
            'arcs': [
                {
                    'source': 'p1',
                    'target': 't1',
                    'weight': 2,
                    'metadata': {'type': 'inhibitor'}
                },
                {
                    'source': 't1',
                    'target': 'p2',
                    'weight': 1
                }
            ]
        }
        
        # Expected JSON structure
        self.expected_json = """
        {
          "metadata": {
            "name": "Test Net",
            "description": "A test Petri net",
            "version": "1.0"
          },
          "elements": {
            "places": [
              {
                "id": "p1",
                "label": "Place 1",
                "tokens": 2,
                "position": {
                  "x": 100,
                  "y": 100
                },
                "metadata": {
                  "color": "red"
                }
              },
              {
                "id": "p2",
                "label": "Place 2",
                "tokens": 0,
                "position": {
                  "x": 300,
                  "y": 100
                },
                "metadata": {}
              }
            ],
            "transitions": [
              {
                "id": "t1",
                "label": "Transition 1",
                "position": {
                  "x": 200,
                  "y": 100
                },
                "metadata": {
                  "rate": 1.0
                }
              }
            ],
            "arcs": [
              {
                "source": "p1",
                "target": "t1",
                "weight": 2,
                "metadata": {
                  "type": "inhibitor"
                }
              },
              {
                "source": "t1",
                "target": "p2",
                "weight": 1,
                "metadata": {}
              }
            ]
          }
        }
        """
    
    def test_to_json(self):
        """Test converting a Petri Net to JSON."""
        # Convert to JSON
        json_str = self.converter.to_json(self.sample_net)
        
        # Parse the JSON strings to compare as dictionaries
        result = json.loads(json_str)
        expected = json.loads(self.expected_json)
        
        # Check the structure and values
        self.assertEqual(result['metadata']['name'], expected['metadata']['name'])
        self.assertEqual(result['metadata']['description'], expected['metadata']['description'])
        
        # Check places
        self.assertEqual(len(result['elements']['places']), 2)
        self.assertEqual(result['elements']['places'][0]['id'], 'p1')
        self.assertEqual(result['elements']['places'][0]['tokens'], 2)
        self.assertEqual(result['elements']['places'][0]['position']['x'], 100)
        self.assertEqual(result['elements']['places'][0]['metadata']['color'], 'red')
        
        # Check transitions
        self.assertEqual(len(result['elements']['transitions']), 1)
        self.assertEqual(result['elements']['transitions'][0]['id'], 't1')
        self.assertEqual(result['elements']['transitions'][0]['metadata']['rate'], 1.0)
        
        # Check arcs
        self.assertEqual(len(result['elements']['arcs']), 2)
        self.assertEqual(result['elements']['arcs'][0]['source'], 'p1')
        self.assertEqual(result['elements']['arcs'][0]['target'], 't1')
        self.assertEqual(result['elements']['arcs'][0]['weight'], 2)
    
    def test_from_json(self):
        """Test converting JSON to a Petri Net."""
        # Convert to JSON and back
        json_str = self.converter.to_json(self.sample_net)
        petri_net = self.converter.from_json(json_str)
        
        # Check the structure and values
        self.assertEqual(petri_net['name'], 'Test Net')
        self.assertEqual(petri_net['description'], 'A test Petri net')
        
        # Check places
        self.assertEqual(len(petri_net['places']), 2)
        self.assertEqual(petri_net['places'][0]['id'], 'p1')
        self.assertEqual(petri_net['places'][0]['tokens'], 2)
        self.assertEqual(petri_net['places'][0]['x'], 100)
        self.assertEqual(petri_net['places'][0]['metadata']['color'], 'red')
        
        # Check transitions
        self.assertEqual(len(petri_net['transitions']), 1)
        self.assertEqual(petri_net['transitions'][0]['id'], 't1')
        self.assertEqual(petri_net['transitions'][0]['metadata']['rate'], 1.0)
        
        # Check arcs
        self.assertEqual(len(petri_net['arcs']), 2)
        self.assertEqual(petri_net['arcs'][0]['source'], 'p1')
        self.assertEqual(petri_net['arcs'][0]['target'], 't1')
        self.assertEqual(petri_net['arcs'][0]['weight'], 2)
    
    def test_roundtrip(self):
        """Test converting back and forth between formats."""
        # Convert to JSON and back
        json_str = self.converter.to_json(self.sample_net)
        petri_net = self.converter.from_json(json_str)
        
        # Convert back to JSON
        roundtrip_json = self.converter.to_json(petri_net)
        
        # Parse both JSON strings to compare
        original = json.loads(json_str)
        roundtrip = json.loads(roundtrip_json)
        
        # They should be identical
        self.assertEqual(original, roundtrip)
    
    def test_invalid_json(self):
        """Test handling of invalid JSON input."""
        with self.assertRaises(ValueError):
            self.converter.from_json('{invalid json}')
    
    def test_missing_required_fields(self):
        """Test handling of missing required fields."""
        # Missing 'id' in place
        invalid_net = {
            'places': [{'label': 'No ID'}],
            'transitions': [],
            'arcs': []
        }
        
        with self.assertRaises(ValueError):
            self.converter.to_json(invalid_net)
        
        # Missing 'source' in arc
        invalid_net = {
            'places': [{'id': 'p1'}],
            'transitions': [{'id': 't1'}],
            'arcs': [{'target': 'p1'}]  # Missing source
        }
        
        with self.assertRaises(ValueError):
            self.converter.to_json(invalid_net)

if __name__ == '__main__':
    unittest.main()
