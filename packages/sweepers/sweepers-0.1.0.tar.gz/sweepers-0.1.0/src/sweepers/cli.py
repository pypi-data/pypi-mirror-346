#!/usr/bin/env python3
"""Command-line interface for sweepers.

This module provides the main command-line interface for the sweepers package.
It defines the available command-line flags, parses arguments, and coordinates
the parameter generation and command execution workflow.

The main functionality is accessible through the 'sweepers' command when
installed, which allows users to:
- Define parameter spaces in Python files
- Run commands with all combinations of those parameters
- Control the number of parameter combinations
- Preview commands without execution (dry run)
"""

import sys
import shlex
from typing import Any
from absl import app, flags, logging

from beartype import beartype
from beartype.door import die_if_unbearable, is_bearable
from sweepers import generate, run

# Define flags at module level
FLAGS = flags.FLAGS

# Define flags with short names
flags.DEFINE_string(
    "params_file",
    None,
    "Python file defining a generate_parameters function",
    short_name="p",
)
flags.DEFINE_string(
    "cmd",
    None,
    "Command to run with generated parameters (use quotes for multiple words)",
    short_name="c",
)
flags.DEFINE_boolean(
    "dry_run", False, "Show commands without executing them", short_name="n"
)
flags.DEFINE_integer(
    "limit",
    256,
    "Maximum number of parameter combinations to generate (use negative value for no limit)",
    short_name="l",
)


@beartype
def parse_command(cmd_string: str) -> list[str]:
    """Parse a command string into a list of command parts.

    Args:
        cmd_string: The command string to parse

    Returns:
        List of command parts
    """
    return shlex.split(cmd_string)


def run_parameter_sweep(
    params_file: str, cmd_parts: list[str], dry_run: bool = False, limit: int = 256
) -> None:
    """Run a parameter sweep with the given parameters.

    This is the main orchestration function that:
    1. Loads the parameter space definition from the specified file
    2. Validates the parameter structure
    3. Generates combinations of parameters (with optional limit)
    4. Executes the command with each parameter combination

    When the limit parameter is smaller than the total possible combinations,
    only the first 'limit' combinations will be used. Set limit to a negative
    value to remove the limit and generate all combinations.

    Args:
        params_file: Path to the parameters file containing the parameters_space function
        cmd_parts: List of command parts (program and arguments)
        dry_run: Whether to run in dry-run mode (only display commands)
        limit: Maximum number of parameter combinations to generate (negative for no limit)

    Raises:
        Various exceptions from the generate and run modules, such as ImportError,
        AttributeError, TypeError, and subprocess.CalledProcessError
    """
    # Load parameters and generate combinations
    params_module = generate.load_parameters_module(params_file)
    params_dict = params_module.parameters_space()

    # Validate parameters using beartype's die_if_unbearable
    die_if_unbearable(params_dict, generate.ParameterIterable)

    # Calculate total possible combinations
    total_possible = 0

    # Check if we have a list of parameter dictionaries or a single dictionary
    if is_bearable(params_dict, list[dict[str, list[Any]]]):
        # Calculate total combinations across all parameter groups
        for param_group in params_dict:
            group_combinations = 1
            for values in param_group.values():
                group_combinations *= len(values)
            total_possible += group_combinations
    else:
        # Calculate total combinations for a single parameter dictionary
        total_possible = 1
        for values in params_dict.values():
            total_possible *= len(values)

    # Check if limit is smaller than total possible combinations
    if limit > 0 and limit < total_possible:
        logging.warning(
            "Limit (%d) is smaller than the total possible combinations (%d). "
            "Some parameter combinations will be skipped.",
            limit,
            total_possible,
        )

    # Generate parameter combinations with limit
    combinations = list(generate.generate_parameter_combinations(params_dict, limit))

    total_combinations = len(combinations)
    logging.info(
        "Generated %d parameter combinations out of %d possible",
        total_combinations,
        total_possible,
    )

    # Run commands with each parameter combination
    for i, params in enumerate(combinations):
        logging.debug("Processing combination %d: %s", i + 1, params)
        run.run_command(cmd_parts, params, dry_run)


@beartype
def main(argv):
    """Main function for the sweepers command-line interface.

    This is the entry point for the command-line application. It:
    1. Ensures required flags are set
    2. Parses the command string
    3. Initiates the parameter sweep
    4. Handles errors gracefully

    Args:
        argv: Command-line arguments passed by absl.app

    Returns:
        None. The function exits with status code 1 on error
    """
    # Mark required flags inside the main function
    # This allows help to display without requiring these flags
    flags.mark_flag_as_required("params_file")
    flags.mark_flag_as_required("cmd")

    # Parse the command string into a list
    cmd_parts = parse_command(FLAGS.cmd)

    logging.debug(
        "Starting parameter sweep with params_file=%s, cmd=%s, dry_run=%s, limit=%s",
        FLAGS.params_file,
        cmd_parts,
        FLAGS.dry_run,
        FLAGS.limit,
    )

    try:
        run_parameter_sweep(FLAGS.params_file, cmd_parts, FLAGS.dry_run, FLAGS.limit)
    except Exception as e:
        logging.exception("Error: %s", e)
        sys.exit(1)


@beartype
def entrypoint():
    """Entry point for the package when installed."""
    # Use absl's app.run to properly handle flags and help
    app.run(main)


if __name__ == "__main__":
    entrypoint()
