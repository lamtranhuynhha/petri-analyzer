""
Unit tests for the PNML parser module.
"""
import unittest
import os
import tempfile
from pathlib import Path
from xml.etree import ElementTree as ET

# Import the module to test
from app.utils.pnml_parser import PNMLParser

class TestPNMLParser(unittest.TestCase):
    """Test cases for the PNML parser."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.parser = PNMLParser()
        self.test_data_dir = Path(__file__).parent / 'test_data'
        self.test_data_dir.mkdir(exist_ok=True)
        
        # Create a simple PNML file for testing
        self.sample_pnml = """<?xml version="1.0" encoding="UTF-8"?>
        <pnml>
          <net id="net1" type="P/T net">
            <place id="p1">
              <name><text>Place 1</text></name>
              <initialMarking><text>1</text></initialMarking>
              <graphics>
                <position x="100" y="200"/>
              </graphics>
            </place>
            <place id="p2">
              <name><text>Place 2</text></name>
              <graphics>
                <position x="300" y="200"/>
              </graphics>
            </place>
            <transition id="t1">
              <name><text>Transition 1</text></name>
              <graphics>
                <position x="200" y="200"/>
              </graphics>
            </transition>
            <arc id="a1" source="p1" target="t1">
              <inscription><text>1</text></inscription>
            </arc>
            <arc id="a2" source="t1" target="p2">
              <inscription><text>1</text></inscription>
            </arc>
          </net>
        </pnml>
        """
        
        # Save to a temporary file
        self.pnml_file = self.test_data_dir / 'test_net.pnml'
        with open(self.pnml_file, 'w', encoding='utf-8') as f:
            f.write(self.sample_pnml)
    
    def tearDown(self):
        """Clean up after tests."""
        # Remove test files
        if self.pnml_file.exists():
            self.pnml_file.unlink()
        
        # Remove test data directory if empty
        try:
            self.test_data_dir.rmdir()
        except OSError:
            pass
    
    def test_parse_valid_pnml(self):
        """Test parsing a valid PNML string."""
        result = self.parser.parse(self.sample_pnml)
        
        # Check places
        self.assertEqual(len(result['places']), 2)
        self.assertEqual(result['places'][0]['id'], 'p1')
        self.assertEqual(result['places'][0]['label'], 'Place 1')
        self.assertEqual(result['places'][0]['tokens'], 1)
        self.assertEqual(result['places'][1]['id'], 'p2')
        self.assertEqual(result['places'][1]['tokens'], 0)
        
        # Check transitions
        self.assertEqual(len(result['transitions']), 1)
        self.assertEqual(result['transitions'][0]['id'], 't1')
        self.assertEqual(result['transitions'][0]['label'], 'Transition 1')
        
        # Check arcs
        self.assertEqual(len(result['arcs']), 2)
        self.assertEqual(result['arcs'][0]['source'], 'p1')
        self.assertEqual(result['arcs'][0]['target'], 't1')
        self.assertEqual(result['arcs'][0]['weight'], 1)
        self.assertEqual(result['arcs'][1]['source'], 't1')
        self.assertEqual(result['arcs'][1]['target'], 'p2')
        self.assertEqual(result['arcs'][1]['weight'], 1)
    
    def test_parse_invalid_pnml(self):
        """Test parsing an invalid PNML string."""
        with self.assertRaises(ValueError):
            self.parser.parse("<invalid><xml></xml>")
    
    def test_parse_pnml_without_initial_marking(self):
        """Test parsing PNML with a place without initial marking."""
        pnml = """<?xml version="1.0" encoding="UTF-8"?>
        <pnml>
          <net id="net1" type="P/T net">
            <place id="p1">
              <name><text>Place 1</text></name>
            </place>
          </net>
        </pnml>"""
        
        result = self.parser.parse(pnml)
        self.assertEqual(result['places'][0]['tokens'], 0)
    
    def test_parse_pnml_with_arc_weight(self):
        """Test parsing PNML with arc weights."""
        pnml = """<?xml version="1.0" encoding="UTF-8"?>
        <pnml>
          <net id="net1" type="P/T net">
            <place id="p1">
              <name><text>Place 1</text></name>
              <initialMarking><text>2</text></initialMarking>
            </place>
            <transition id="t1">
              <name><text>Transition 1</text></name>
            </transition>
            <arc id="a1" source="p1" target="t1">
              <inscription><text>2</text></inscription>
            </arc>
          </net>
        </pnml>"""
        
        result = self.parser.parse(pnml)
        self.assertEqual(result['arcs'][0]['weight'], 2)
    
    def test_to_pnml_roundtrip(self):
        """Test converting to PNML and back."""
        # Parse the original PNML
        original = self.parser.parse(self.sample_pnml)
        
        # Convert back to PNML
        pnml_str = self.parser.to_pnml(original)
        
        # Parse the generated PNML
        roundtrip = self.parser.parse(pnml_str)
        
        # Check that the result is the same
        self.assertEqual(len(original['places']), len(roundtrip['places']))
        self.assertEqual(len(original['transitions']), len(roundtrip['transitions']))
        self.assertEqual(len(original['arcs']), len(roundtrip['arcs']))
        
        # Check that the first place is the same
        self.assertEqual(original['places'][0]['id'], roundtrip['places'][0]['id'])
        self.assertEqual(original['places'][0]['label'], roundtrip['places'][0]['label'])
        self.assertEqual(original['places'][0]['tokens'], roundtrip['places'][0]['tokens'])

if __name__ == '__main__':
    unittest.main()
