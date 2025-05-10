#!/usr/bin/env python3
"""Parameter generation utilities for sweepers.

This module provides functions for loading parameter modules,
validating parameter dictionaries, and generating parameter combinations.
It serves as the core of the parameter sweep generation capabilities.
"""

import importlib.util
import itertools
import sys
from collections.abc import Iterator
from typing import (
    Annotated,
    Any,
    Protocol,
    TypeVar,
    Union,
    runtime_checkable,
)

from absl import logging
from beartype import beartype
from beartype.door import is_bearable
from beartype.vale import Is

# Type variable for generic functions
T = TypeVar("T")

# Define validators for parameter validation
IsValidIdentifier = Is[lambda name: isinstance(name, str) and name.isidentifier()]
IsNonEmptyList = Is[lambda obj: isinstance(obj, list) and len(obj) > 0]
IsNonEmptyDict = Is[lambda obj: isinstance(obj, dict) and bool(obj)]

# Define validated types
ValidParamName = Annotated[str, IsValidIdentifier]
ValidParamValue = Annotated[list[Any], IsNonEmptyList]

# Define the parameter dictionary type
ParameterDict = Annotated[dict[ValidParamName, ValidParamValue], IsNonEmptyDict]
ParameterIterable = Union[ParameterDict, list[ParameterDict]]

# Define a protocol for parameter modules


@runtime_checkable
class ParameterModule(Protocol):
    """Protocol defining the expected interface for parameter modules."""

    def parameters_space(self) -> ParameterIterable:
        """Return a dictionary of parameter names and lists of values,
        or a list of such dictionaries for mutually exclusive parameters."""
        ...


@beartype
def load_parameters_module(file_path: str) -> ParameterModule:
    """Load a Python module from a file path.

    Args:
        file_path: Path to the Python file

    Returns:
        Loaded module containing parameters_space function

    Raises:
        ImportError: If the module cannot be loaded
        AttributeError: If the module doesn't define parameters_space
        TypeError: If parameters_space is not a callable function
    """
    # Validate file_path exists
    try:
        with open(file_path):
            pass  # Just checking if we can open the file
    except FileNotFoundError:
        raise ImportError(f"Parameter file not found: {file_path}")
    except PermissionError:
        raise ImportError(f"Permission denied when reading: {file_path}")

    module_name = "parameters_module"
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load module from {file_path}")

    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module

    try:
        spec.loader.exec_module(module)
    except Exception as e:
        raise ImportError(f"Error executing module {file_path}: {str(e)}")

    if not hasattr(module, "parameters_space"):
        raise AttributeError(
            f"The module {file_path} must define a parameters_space function"
        )

    if not callable(getattr(module, "parameters_space")):
        raise TypeError(f"parameters_space in {file_path} must be a callable function")

    logging.debug("Successfully loaded parameters module from %s", file_path)
    return module


@beartype
def generate_parameter_combinations(
    params: ParameterIterable, limit: int = 256
) -> Iterator[dict[str, Any]]:
    """Generate combinations of parameters, optionally limited to a maximum count.

    This function handles two types of input:
    1. A dictionary mapping parameter names to lists of values - generates
       the Cartesian product of all parameter values.
    2. A list of parameter dictionaries - processes each dictionary separately
       and yields combinations from each.

    This allows for mutually exclusive parameters by placing them in different
    dictionaries in the list.

    The function uses lazy evaluation through Python's iterator protocol to avoid
    generating all combinations at once, which is important for large parameter spaces.

    Args:
        params: Either a dictionary of parameter names and lists of values,
                or a list of such dictionaries for mutually exclusive parameters
        limit: Maximum number of combinations to generate (negative value means no limit)

    Yields:
        Dictionary of parameter names and single values for each combination

    Examples:
        >>> params = {"a": [1, 2], "b": ["x", "y"]}
        >>> list(generate_parameter_combinations(params))
        [{"a": 1, "b": "x"}, {"a": 1, "b": "y"}, {"a": 2, "b": "x"}, {"a": 2, "b": "y"}]

        >>> list(generate_parameter_combinations(params, limit=2))
        [{"a": 1, "b": "x"}, {"a": 1, "b": "y"}]

        >>> params_list = [
        ...     {"optimizer": "adam", "beta1": [0.9, 0.95]},
        ...     {"optimizer": "sgd", "momentum": [0.0, 0.9]}
        ... ]
        >>> list(generate_parameter_combinations(params_list))
        [{"optimizer": "adam", "beta1": 0.9}, {"optimizer": "adam", "beta1": 0.95},
         {"optimizer": "sgd", "momentum": 0.0}, {"optimizer": "sgd", "momentum": 0.9}]
    """
    # Check if input is a list of parameter dictionaries or a single dictionary
    if is_bearable(params, list[dict[str, list[Any]]]):
        logging.debug("Processing a list of %d parameter dictionaries", len(params))

        # Process each dictionary separately, respecting the overall limit
        count = 0
        for param_dict in params:
            # Get parameter names and values for this dictionary
            param_names = list(param_dict.keys())
            param_values = list(param_dict.values())

            logging.debug("Processing parameter group with parameters: %s", param_names)

            # Calculate combinations for this dictionary
            dict_combinations = 1
            for values in param_values:
                dict_combinations *= len(values)
            logging.debug(
                "This parameter group has %d possible combinations", dict_combinations
            )

            # Determine how many combinations to generate from this dictionary
            if limit < 0:
                # No limit, generate all combinations from this dictionary
                dict_limit = -1
            else:
                # Limit remaining combinations
                dict_limit = max(0, limit - count)
                if dict_limit == 0:
                    logging.debug(
                        "Reached overall limit, skipping remaining parameter groups"
                    )
                    break

            # Generate combinations from this dictionary
            sub_count = 0
            for values in itertools.product(*param_values):
                if dict_limit >= 0 and sub_count >= dict_limit:
                    break

                combination = dict(zip(param_names, values))
                logging.debug(
                    "Generated combination from group %d: %s",
                    params.index(param_dict) + 1,
                    combination,
                )
                yield combination

                count += 1
                sub_count += 1

                if limit >= 0 and count >= limit:
                    logging.debug("Reached overall limit of %d combinations", limit)
                    return
    else:
        # Single parameter dictionary
        param_names = list(params.keys())
        param_values = list(params.values())

        logging.debug("Generating combinations for parameters: %s", param_names)

        # Calculate total possible combinations
        total_possible = 1
        for values in param_values:
            total_possible *= len(values)
        logging.debug("Total possible combinations: %d", total_possible)

        if limit >= 0:
            logging.debug("Limiting to %d combinations", limit)
            actual_limit = min(limit, total_possible)
        else:
            logging.debug(
                "No limit specified, will generate all %d combinations", total_possible
            )
            actual_limit = total_possible

        # Generate combinations
        count = 0
        for values in itertools.product(*param_values):
            if limit >= 0 and count >= limit:
                logging.debug("Reached limit of %d combinations, stopping", limit)
                break

            combination = dict(zip(param_names, values))
            if limit >= 0:
                logging.debug(
                    "Generated combination %d/%d: %s",
                    count + 1,
                    actual_limit,
                    combination,
                )
            else:
                logging.debug("Generated combination %d: %s", count + 1, combination)

            yield combination
            count += 1
