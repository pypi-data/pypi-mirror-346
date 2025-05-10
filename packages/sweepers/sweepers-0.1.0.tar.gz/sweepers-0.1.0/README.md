# Sweepers

A Python CLI tool for generating parameter sweeps and running commands with the generated parameters.

## Overview

Sweepers makes it easy to run your scripts and programs with many different parameter combinations. By defining parameter sets in a simple Python file, you can quickly:

- Generate comprehensive parameter sweeps
- Run your command with each parameter combination
- Limit the number of combinations to explore
- Preview commands without executing them (dry run)

Ideal for machine learning experimentation, hyperparameter tuning, or any scenario where you need to explore different parameter combinations systematically.

## Installation

### Using uv (recommended)

```bash
uv pip install sweepers
```

### Adding as a dependency to your project

```bash
uv add sweepers
```

### Development installation

```bash
# Clone the repository
git clone https://github.com/yourusername/sweepers.git
cd sweepers

# Install in development mode
uv pip install -e .
```

## Basic Usage

1. Create a parameter file (e.g., `params.py`) with a `parameters_space` function:

```python
def parameters_space():
    """Define the parameter space to explore."""
    return {
        "learning_rate": [0.01, 0.05, 0.1],
        "batch_size": [32, 64, 128],
        "epochs": [10, 50, 100]
    }
```

2. Run your command with the parameter combinations:

```bash
sweepers -p params.py -c "python train.py"
```

This will execute your command with each parameter combination, generated as CLI flags:

```
python train.py --learning_rate 0.01 --batch_size 32 --epochs 10
python train.py --learning_rate 0.01 --batch_size 32 --epochs 50
...
```

## The `parameters_space` Function

The key to using Sweepers is the `parameters_space` function in your parameter file. This function:

1. **Defines the search space**: Creates a dictionary where each key is a parameter name and each value is a list of possible values for that parameter
2. **Controls combinatorial explosion**: By carefully selecting parameter values to test
3. **Can include dynamic generation**: You can use code to programmatically generate parameter values based on complex logic
4. **Supports mutually exclusive parameters**: By returning a list of dictionaries instead of a single dictionary

The function can return either:

1. A dictionary where:
   - Each key becomes a command-line flag (e.g., `--learning_rate`)
   - Each value must be a list of options to explore

   Sweepers then generates the Cartesian product of all parameter values and runs your command with each combination.

2. A list of dictionaries, where:
   - Each dictionary represents a group of compatible parameters
   - Parameters in different dictionaries are treated as mutually exclusive
   - Combinations are generated separately for each dictionary

   This is useful for parameters that should not appear together, like optimizer-specific parameters.

## Command-line Options

- `-p`, `--params_file`: Python file containing the `parameters_space` function (required)
- `-c`, `--cmd`: Command to run with generated parameters (required)
- `-n`, `--dry_run`: Show commands without executing them
- `-l`, `--limit`: Maximum number of parameter combinations to generate (default: 256, use negative value for no limit)
- `--helpfull`: Show detailed help information

## Examples

### Basic Parameter Sweep

```bash
sweepers -p examples/example_params.py -c "python examples/train.py"
```

This will run the training script with every combination of learning rates, batch sizes, and epochs defined in the parameter file.

### Dry Run

Preview the commands without executing them:

```bash
sweepers -p examples/example_params.py -c "python examples/train.py" -n
```

### Limiting Combinations

Limit the maximum number of parameter combinations to try:

```bash
sweepers -p examples/example_params.py -c "python examples/train.py" -l 10
```

## Parameter File Format

The parameter file must define a `parameters_space` function that returns a dictionary with:
- Keys: Parameter names (will be used as command-line flags)
- Values: Lists of parameter values to try

Each parameter will be added as a CLI flag (e.g., `--parameter_name value`).

### Simple Example

```python
def parameters_space():
    return {
        "learning_rate": [0.01, 0.05, 0.1],
        "batch_size": [32, 64, 128]
    }
```

### Advanced Example

You can generate complex combinations:

```python
def parameters_space():
    # Generate network architectures (combinations of layers)
    architectures = []
    for hidden_layers in range(1, 4):
        for width in [32, 64, 128]:
            architectures.append(f"{','.join([str(width)] * hidden_layers)}")

    return {
        "learning_rate": [0.001, 0.01, 0.1],
        "architecture": architectures,
        "activation": ["relu", "tanh", "gelu"]
    }
```

### Mutually Exclusive Parameters Example

You can define parameter groups with mutually exclusive parameters:

```python
def parameters_space():
    # Define base parameters common to all configurations
    learning_rates = [0.001, 0.01, 0.1]
    batch_sizes = [32, 64, 128]

    # Return a list of parameter dictionaries (each dictionary is a separate group)
    return [
        # SGD parameters
        {
            "optimizer": ["sgd"],
            "learning_rate": learning_rates,
            "batch_size": batch_sizes,
            "momentum": [0.0, 0.9, 0.99]
        },

        # Adam parameters
        {
            "optimizer": ["adam"],
            "learning_rate": learning_rates,
            "batch_size": batch_sizes,
            "beta1": [0.9, 0.95],
            "beta2": [0.999]
        }
    ]
```

This will generate commands like:
```
python train.py --optimizer sgd --learning_rate 0.001 --batch_size 32 --momentum 0.0
python train.py --optimizer adam --learning_rate 0.001 --batch_size 32 --beta1 0.9 --beta2 0.999
```

Note that momentum only appears with sgd, and beta parameters only appear with adam.

## Limitations and Tips

- The number of combinations grows exponentially with parameters, use `--limit` to control this
- Use `--dry_run` first to preview commands before running them
- Lists in parameter values will be passed as a single space-separated string
- Parameters are converted to command-line flags following the `--param_name value` format

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
