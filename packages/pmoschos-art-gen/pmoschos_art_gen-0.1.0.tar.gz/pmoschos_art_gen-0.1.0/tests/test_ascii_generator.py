"""
Tests for the ASCII generator functionality
"""

import unittest
from pmoschos_art_gen.ascii_generator import render_ascii_lines, center_ascii_output, generate_rainbow_ascii

class TestAsciiGenerator(unittest.TestCase):
    
    def test_render_ascii_lines(self):
        """Test that rendering produces output"""
        lines = ["A"]
        result = render_ascii_lines(lines)
        self.assertTrue(len(result) > 0)
        
    def test_empty_input(self):
        """Test handling of empty input"""
        lines = [""]
        result = render_ascii_lines(lines)
        self.assertEqual(len(result), 1)  # Just the blank line
        
    def test_multiple_lines(self):
        """Test handling of multiple lines"""
        lines = ["A", "B"]
        result = render_ascii_lines(lines)
        self.assertTrue(len(result) > 2)  # Should have multiple lines
        
    def test_center_ascii_output(self):
        """Test centering functionality"""
        lines = ["test", "line"]
        result = center_ascii_output(lines, vertical=False)
        self.assertEqual(len(lines), len(result))
        
    def test_vertical_center_ascii_output(self):
        """Test vertical centering functionality"""
        lines = ["test", "line"]
        result = center_ascii_output(lines, vertical=True)
        # Vertical centering may add lines, so we can't check exact length
        self.assertTrue(len(result) >= len(lines))
        
    def test_generate_rainbow_ascii(self):
        """Test the main generator function"""
        text = "AB"
        result = generate_rainbow_ascii(text, center=False, vertical_center=False)
        self.assertTrue(isinstance(result, str))
        self.assertTrue(len(result) > 0)
        
    def test_generate_rainbow_ascii_with_newline(self):
        """Test generation with newlines"""
        text = "A  B"  # Double space = newline
        result = generate_rainbow_ascii(text, center=False, vertical_center=False)
        self.assertTrue(isinstance(result, str))
        self.assertTrue("\n\n" in result)  # Should have blank line between blocks

if __name__ == '__main__':
    unittest.main()