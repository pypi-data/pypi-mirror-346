# Easy VQE

[![PyPI version](https://badge.fury.io/py/easy-vqe.svg)](https://badge.fury.io/py/easy-vqe) 
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0) 

A user-friendly Python package for setting up and running Variational Quantum Eigensolver (VQE) calculations using Qiskit. Define Hamiltonians as simple strings and ansatz circuits using nested lists/tuples.

## Features

*   **Simple Hamiltonian Definition:** Define Hamiltonians using intuitive strings (e.g., `"1.0 * XX - 0.5 * ZI + YZ"`). Handles various formats, signs, and spacing.
*   **Flexible Ansatz Creation:** Build parameterized circuits using a list-based structure with standard Qiskit gate names. Auto-generates parameters.
*   **Automated VQE Workflow:** Handles parameter management, basis rotations, measurement simulation, expectation value calculation, and optimization loop.
*   **Built-in Optimization:** Uses `scipy.optimize.minimize` with configurable methods (COBYLA, Nelder-Mead, etc.) and options.
*   **Simulation Backend:** Leverages `qiskit-aer` for efficient classical simulation.
*   **Convergence Plotting:** Optionally save plots of the energy convergence during optimization.
*   **Flexible Initial Parameters:** Supports random initialization, zero initialization, or providing specific lists/NumPy arrays for starting parameters.
*   **Result Summarization:** Includes helper functions to print a clean summary of the VQE results.
*   **Theoretical Energy Calculation:** Provides a utility to compute the exact ground state energy via matrix diagonalization for comparison.
*   **Circuit Visualization:** Includes a helper function to draw the final ansatz circuit with the optimized parameters bound.

## Installation

You can install `easy_vqe` using pip:

```bash
pip install easy-vqe
```

Or, for development, clone this repository and install in editable mode:

```bash
git clone https://github.com/7Abdoman7/easy_vqe.git 
cd easy_vqe
pip install -e .[dev] 
```

## Quick Start

Here's a basic example to find the ground state energy of a 3-qubit Hamiltonian:

```python
import numpy as np
from easy_vqe import find_ground_state

# 1. Define the Hamiltonian string
hamiltonian_str = "-1.0 * ZZI + 0.9 * ZIZ - 0.5 * IZZ + 0.2 * XXX"

# 2. Define the Ansatz Structure
ansatz_block = [
    ('ry', [0, 1, 2]), # Ry on qubits 0, 1, 2 (each gets a parameter)
    ('cx', [0, 1]),    # CNOT 0 -> 1
    ('cx', [1, 2]),    # CNOT 1 -> 2
    ('rz', [0, 1, 2]), # Rz on qubits 0, 1, 2 (each gets a parameter)
]
# Build the full ansatz: Hadamard layer, block, CNOT, block
ansatz_structure = [
    ('h', [0, 1, 2]),
    ansatz_block,
    ('cx', [0, 2]),
    ('barrier', []), # Optional barrier for visual separation
    ansatz_block,
]

# 3. Run the VQE algorithm
results = find_ground_state(
    ansatz_structure=ansatz_structure,
    hamiltonian_expression=hamiltonian_str,
    optimizer_method='COBYLA',
    optimizer_options={'maxiter': 200, 'tol': 1e-5}, # Optimizer settings
    n_shots=4096, # Number of shots for expectation value
    plot_filename="vqe_convergence.png" # Save the plot
)

# 4. Print Results
if 'error' not in results:
    print(f"Optimization Successful: {results['success']}")
    print(f"Optimizer Message: {results['message']}")
    print(f"Minimum Energy Found: {results['optimal_value']:.6f}")
    print(f"Optimal Parameters: {np.round(results['optimal_params'], 4)}")
else:
    print(f"VQE Failed: {results['error']}")

```

See the `examples/` directory for more usage scenarios.

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests. (Add more details here if you like - code style, testing requirements etc.)

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.
