"""
Tests for the pypccl package.
"""

import unittest
from pypccl.core import ExampleClass, example_function


class TestExampleClass(unittest.TestCase):
    """Test cases for the ExampleClass."""
    
    def test_init(self):
        """Test initialization."""
        obj = ExampleClass()
        self.assertIsNone(obj.value)
        
        obj = ExampleClass("test")
        self.assertEqual(obj.value, "test")
    
    def test_get_value(self):
        """Test get_value method."""
        obj = ExampleClass("test")
        self.assertEqual(obj.get_value(), "test")
    
    def test_set_value(self):
        """Test set_value method."""
        obj = ExampleClass()
        obj.set_value("new value")
        self.assertEqual(obj.value, "new value")


class TestExampleFunction(unittest.TestCase):
    """Test cases for the example_function."""
    
    def test_with_one_param(self):
        """Test with only one parameter."""
        result = example_function("test")
        self.assertEqual(result, "test")
    
    def test_with_two_params(self):
        """Test with two parameters."""
        result = example_function("test1", "test2")
        self.assertEqual(result, ("test1", "test2"))


if __name__ == "__main__":
    unittest.main()
