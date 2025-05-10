#!/usr/bin/env python3
"""Tests for the cli.py module."""

import os
import tempfile
from unittest import mock

from absl.testing import absltest
from absl.testing import parameterized
from absl.testing import flagsaver

from sweepers import cli


class ParseCommandTest(absltest.TestCase):
    """Tests for the parse_command function."""

    def test_parse_simple_command(self):
        """Test parsing a simple command."""
        cmd_string = "echo test"
        result = cli.parse_command(cmd_string)
        self.assertEqual(result, ["echo", "test"])

    def test_parse_command_with_quotes(self):
        """Test parsing a command with quotes."""
        cmd_string = 'echo "hello world"'
        result = cli.parse_command(cmd_string)
        self.assertEqual(result, ["echo", "hello world"])

    def test_parse_complex_command(self):
        """Test parsing a more complex command."""
        cmd_string = 'python -c "import sys; print(sys.version)"'
        result = cli.parse_command(cmd_string)
        self.assertEqual(result, ["python", "-c", "import sys; print(sys.version)"])


class RunParameterSweepTest(parameterized.TestCase):
    """Tests for the run_parameter_sweep function."""

    def setUp(self):
        """Set up a temporary parameter file for testing."""
        self.param_file = tempfile.NamedTemporaryFile(
            suffix=".py", mode="w", delete=False
        )
        self.param_file.write("""
def parameters_space():
    return {
        "a": [1, 2],
        "b": ["x", "y"]
    }
""")
        self.param_file.flush()
        self.param_file.close()

    def tearDown(self):
        """Clean up temporary files."""
        os.unlink(self.param_file.name)

    def test_run_parameter_sweep(self):
        """Test the run_parameter_sweep function."""
        cmd_parts = ["echo", "test"]

        # Mock the run_command function to avoid actual execution
        with mock.patch("sweepers.run.run_command") as mock_run:
            mock_run.return_value = True

            # Run the parameter sweep
            cli.run_parameter_sweep(self.param_file.name, cmd_parts, dry_run=True)

            # Check that run_command was called for each combination
            self.assertEqual(mock_run.call_count, 4)

            # Check that each call had the right arguments
            calls = mock_run.call_args_list
            params_list = [call[0][1] for call in calls]

            # Expected combinations
            expected_params = [
                {"a": 1, "b": "x"},
                {"a": 1, "b": "y"},
                {"a": 2, "b": "x"},
                {"a": 2, "b": "y"},
            ]

            # Sort both lists to ensure deterministic comparison
            sorted_expected = sorted(expected_params, key=lambda x: (x["a"], x["b"]))
            sorted_actual = sorted(params_list, key=lambda x: (x["a"], x["b"]))

            self.assertEqual(sorted_actual, sorted_expected)

    def test_run_parameter_sweep_with_limit(self):
        """Test the run_parameter_sweep function with a limit."""
        cmd_parts = ["echo", "test"]

        # Mock the run_command function to avoid actual execution
        with mock.patch("sweepers.run.run_command") as mock_run:
            mock_run.return_value = True

            # Run the parameter sweep with a limit of 2
            cli.run_parameter_sweep(
                self.param_file.name, cmd_parts, dry_run=True, limit=2
            )

            # Check that run_command was called only twice
            self.assertEqual(mock_run.call_count, 2)


class MainTest(absltest.TestCase):
    """Tests for the main function."""

    def setUp(self):
        """Set up a temporary parameter file for testing."""
        self.param_file = tempfile.NamedTemporaryFile(
            suffix=".py", mode="w", delete=False
        )
        self.param_file.write("""
def parameters_space():
    return {
        "a": [1, 2],
        "b": ["x", "y"]
    }
""")
        self.param_file.flush()
        self.param_file.close()

    def tearDown(self):
        """Clean up temporary files."""
        os.unlink(self.param_file.name)

    @flagsaver.flagsaver
    def test_main_function(self):
        """Test the main function with flags."""
        # Set up flags
        cli.FLAGS.params_file = self.param_file.name
        cli.FLAGS.cmd = "echo test"
        cli.FLAGS.dry_run = True
        cli.FLAGS.limit = 2

        # Mock run_parameter_sweep to avoid actual execution
        with mock.patch("sweepers.cli.run_parameter_sweep") as mock_sweep:
            # Run main
            cli.main(argv=[])

            # Check that run_parameter_sweep was called with the right arguments
            mock_sweep.assert_called_once()
            args = mock_sweep.call_args[0]
            self.assertEqual(args[0], self.param_file.name)  # params_file
            self.assertEqual(args[1], ["echo", "test"])  # cmd_parts
            self.assertEqual(args[2], True)  # dry_run
            self.assertEqual(args[3], 2)  # limit

    @flagsaver.flagsaver
    def test_main_error_handling(self):
        """Test that main handles errors properly."""
        # Set up flags
        cli.FLAGS.params_file = self.param_file.name
        cli.FLAGS.cmd = "echo test"

        # Mock run_parameter_sweep to raise an exception
        with mock.patch("sweepers.cli.run_parameter_sweep") as mock_sweep:
            mock_sweep.side_effect = ValueError("Test error")

            # Mock sys.exit to avoid actually exiting
            with mock.patch("sys.exit") as mock_exit:
                # Run main
                cli.main(argv=[])

                # Check that sys.exit was called with code 1
                mock_exit.assert_called_once_with(1)


if __name__ == "__main__":
    absltest.main()
