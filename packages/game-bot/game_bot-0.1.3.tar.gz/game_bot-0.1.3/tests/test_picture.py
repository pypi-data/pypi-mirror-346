import unittest
import numpy as np
from picture import find_pattern, find_image

class TestPatternMatching(unittest.TestCase):
    def setUp(self):
        # Create a simple test image with known patterns
        self.test_image = np.zeros((100, 100, 3), dtype=np.uint8)
        
        # Add some colored squares as test patterns
        self.test_image[10:20, 10:20] = [255, 0, 0]  # Red square
        self.test_image[30:40, 30:40] = [0, 255, 0]  # Green square
        self.test_image[50:60, 50:60] = [0, 0, 255]  # Blue square
        
        # Define test patterns
        self.red_pattern = [
            (0, 0, (255, 0, 0)),  # Top-left corner
            (9, 9, (255, 0, 0))   # Bottom-right corner
        ]
        
        self.green_pattern = [
            (0, 0, (0, 255, 0)),
            (9, 9, (0, 255, 0))
        ]
        
        self.partial_pattern = [
            (0, 0, (255, 0, 0)),
            (0, 0, (0, 255, 0))  # This shouldn't match
        ]
    
    def test_find_pattern_exact_match(self):
        # Test exact pattern matching
        matches = find_pattern(self.test_image, self.red_pattern, threshold=0.9)
        self.assertEqual(len(matches), 1)
        x, y, score = matches[0]
        self.assertEqual(x, 10)
        self.assertEqual(y, 10)
        self.assertGreater(score, 0.9)
        
    def test_find_pattern_multiple_matches(self):
        # Test finding multiple patterns
        matches = find_pattern(self.test_image, self.green_pattern)
        self.assertEqual(len(matches), 1)
        x, y, score = matches[0]
        self.assertEqual(x, 30)
        self.assertEqual(y, 30)
        
    def test_find_pattern_partial_match(self):
        # Test partial pattern matching with lower threshold
        matches = find_pattern(self.test_image, self.partial_pattern, threshold=0.5)
        self.assertEqual(len(matches), 1)
        
    def test_find_pattern_no_match(self):
        # Test no matches with high threshold
        matches = find_pattern(self.test_image, self.red_pattern, threshold=1.0)
        self.assertEqual(len(matches), 0)

class TestImageMatching(unittest.TestCase):
    def setUp(self):
        # Create test images
        self.source = np.zeros((100, 100, 3), dtype=np.uint8)
        self.template = np.zeros((20, 20, 3), dtype=np.uint8)
        
        # Add template at known position
        self.source[30:50, 40:60] = [255, 255, 255]
        self.template[:, :] = [255, 255, 255]
    
    def test_find_image_exact_match(self):
        # Test exact template matching
        matches = find_image(self.source, self.template, threshold=0.9)
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0], (40, 30))
        
    def test_find_image_no_match(self):
        # Test no matches with high threshold
        matches = find_image(self.source, self.template, threshold=1.0)
        self.assertEqual(len(matches), 0)
        
    def test_find_image_multiple_matches(self):
        # Test finding multiple templates
        # Add another template
        self.source[70:90, 10:30] = [255, 255, 255]
        matches = find_image(self.source, self.template, threshold=0.9)
        self.assertEqual(len(matches), 2)
        self.assertIn((40, 30), matches)
        self.assertIn((10, 70), matches)

if __name__ == '__main__':
    unittest.main()