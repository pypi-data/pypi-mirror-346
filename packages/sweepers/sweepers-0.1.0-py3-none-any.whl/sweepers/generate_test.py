#!/usr/bin/env python3
"""Tests for the generate.py module."""

import os
import tempfile
from typing import Any

from absl.testing import absltest
from absl.testing import parameterized

from sweepers import generate


class ParameterCombinationsTest(parameterized.TestCase):
    """Tests for the generate_parameter_combinations function."""

    @parameterized.parameters(
        ({"a": [1, 2]}, -1, 2),
        ({"a": [1, 2], "b": [3, 4]}, -1, 4),
        ({"a": [1, 2, 3], "b": [4, 5, 6]}, -1, 9),
        ({"a": [1, 2], "b": [3, 4], "c": [5, 6]}, -1, 8),
    )
    def test_generate_all_combinations(
        self, params: dict[str, list[Any]], limit: int, expected_count: int
    ):
        """Test that all combinations are generated when no limit is set."""
        combinations = list(generate.generate_parameter_combinations(params, limit))
        self.assertLen(combinations, expected_count)

    @parameterized.parameters(
        ({"a": [1, 2], "b": [3, 4]}, 1, 1),
        ({"a": [1, 2], "b": [3, 4]}, 2, 2),
        ({"a": [1, 2], "b": [3, 4]}, 3, 3),
        ({"a": [1, 2], "b": [3, 4]}, 4, 4),
        ({"a": [1, 2], "b": [3, 4]}, 5, 4),  # Only 4 possible combinations
    )
    def test_generate_limited_combinations(
        self, params: dict[str, list[Any]], limit: int, expected_count: int
    ):
        """Test that limit parameter is respected."""
        combinations = list(generate.generate_parameter_combinations(params, limit))
        self.assertLen(combinations, expected_count)

    def test_combination_structure(self):
        """Test that generated combinations have the correct structure."""
        params = {"a": [1, 2], "b": ["x", "y"]}
        combinations = list(generate.generate_parameter_combinations(params))

        # Check that each combination is a dictionary
        for combo in combinations:
            self.assertIsInstance(combo, dict)

            # Check that each combination has the right keys
            self.assertCountEqual(combo.keys(), params.keys())

            # Check that values are from the original lists
            self.assertIn(combo["a"], params["a"])
            self.assertIn(combo["b"], params["b"])

        # Check that all combinations are generated
        expected_combinations = [
            {"a": 1, "b": "x"},
            {"a": 1, "b": "y"},
            {"a": 2, "b": "x"},
            {"a": 2, "b": "y"},
        ]

        # Sort both lists to ensure deterministic comparison
        sorted_expected = sorted(expected_combinations, key=lambda x: (x["a"], x["b"]))
        sorted_actual = sorted(combinations, key=lambda x: (x["a"], x["b"]))

        self.assertEqual(sorted_actual, sorted_expected)


class LoadParametersModuleTest(absltest.TestCase):
    """Tests for the load_parameters_module function."""

    def test_load_valid_module(self):
        """Test loading a valid module with parameters_space function."""
        with tempfile.NamedTemporaryFile(suffix=".py", mode="w", delete=False) as f:
            f.write("""
def parameters_space():
    return {
        "a": [1, 2, 3],
        "b": ["x", "y", "z"]
    }
""")
            f.flush()
            module_path = f.name

        try:
            module = generate.load_parameters_module(module_path)
            params = module.parameters_space()

            self.assertIsInstance(params, dict)
            self.assertEqual(params["a"], [1, 2, 3])
            self.assertEqual(params["b"], ["x", "y", "z"])
        finally:
            # Clean up temporary file
            os.unlink(module_path)

    def test_load_nonexistent_module(self):
        """Test that loading a nonexistent module raises ImportError."""
        with self.assertRaises(ImportError):
            generate.load_parameters_module("/nonexistent/path/module.py")

    def test_load_module_without_parameters_space(self):
        """Test that loading a module without parameters_space raises AttributeError."""
        with tempfile.NamedTemporaryFile(suffix=".py", mode="w", delete=False) as f:
            f.write("""
def some_other_function():
    return "Hello"
""")
            f.flush()
            module_path = f.name

        try:
            with self.assertRaises(AttributeError):
                generate.load_parameters_module(module_path)
        finally:
            # Clean up temporary file
            os.unlink(module_path)


if __name__ == "__main__":
    absltest.main()
