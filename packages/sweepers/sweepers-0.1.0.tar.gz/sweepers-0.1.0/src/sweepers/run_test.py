#!/usr/bin/env python3
"""Tests for the run.py module."""

import subprocess
from unittest import mock

from absl.testing import absltest
from absl.testing import parameterized

from sweepers import run


class RunCommandTest(parameterized.TestCase):
    """Tests for the run_command function."""

    def test_dry_run_mode(self):
        """Test that dry run mode doesn't execute the command."""
        cmd = ["echo", "test"]
        params = {"param1": "value1", "param2": 123}

        with mock.patch("subprocess.run") as mock_run:
            result = run.run_command(cmd, params, dry_run=True)

            # Check that the command was not executed
            mock_run.assert_not_called()

            # Check that dry_run returns True
            self.assertTrue(result)

    def test_successful_command(self):
        """Test that a successful command returns True."""
        # Use a simple echo command that should always succeed
        cmd = ["echo", "test"]
        params = {"param1": "value1"}

        result = run.run_command(cmd, params, dry_run=False)
        self.assertTrue(result)

    def test_failed_command(self):
        """Test that a failed command returns False."""
        # Use a command that should always fail
        cmd = ["false"]  # 'false' exits with status 1
        params = {}

        result = run.run_command(cmd, params, dry_run=False)
        self.assertFalse(result)

    @parameterized.parameters(
        (["echo", "test"], {"a": 1, "b": 2}, ["echo", "test", "--a", "1", "--b", "2"]),
        (["echo"], {"param": "value"}, ["echo", "--param", "value"]),
        (["cmd"], {"flag": True}, ["cmd", "--flag", "True"]),
    )
    def test_parameter_formatting(self, cmd, params, expected_cmd_parts):
        """Test that parameters are formatted correctly."""
        with mock.patch("subprocess.run") as mock_run:
            run.run_command(cmd, params, dry_run=False)

            # Check that subprocess.run was called with the right command
            mock_run.assert_called_once()
            actual_cmd_parts = mock_run.call_args[0][0]
            self.assertEqual(actual_cmd_parts, expected_cmd_parts)

    def test_list_parameter_formatting(self):
        """Test that list parameters are formatted correctly."""
        cmd = ["echo"]
        params = {"layers": [1, 2, 3]}
        expected_cmd_parts = ["echo", "--layers", "1 2 3"]

        with mock.patch("subprocess.run") as mock_run:
            run.run_command(cmd, params, dry_run=False)

            # Check that subprocess.run was called with the right command
            mock_run.assert_called_once()
            actual_cmd_parts = mock_run.call_args[0][0]
            self.assertEqual(actual_cmd_parts, expected_cmd_parts)

    def test_subprocess_error_handling(self):
        """Test that CalledProcessError is caught and handled."""
        cmd = ["echo", "test"]
        params = {}

        with mock.patch("subprocess.run") as mock_run:
            # Make subprocess.run raise CalledProcessError
            mock_run.side_effect = subprocess.CalledProcessError(1, cmd)

            # Check that the error is caught and False is returned
            result = run.run_command(cmd, params, dry_run=False)
            self.assertFalse(result)


if __name__ == "__main__":
    absltest.main()
