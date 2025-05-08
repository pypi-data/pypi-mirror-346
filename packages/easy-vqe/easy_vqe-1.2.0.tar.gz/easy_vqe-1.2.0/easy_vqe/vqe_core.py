# =============================================================================
#           easy_vqe: Core VQE Implementation Logic
# =============================================================================
# This module contains the core functions for parsing Hamiltonians,
# building ansatz circuits, calculating expectation values, and running
# the VQE optimization loop using Qiskit and SciPy.
# =============================================================================

import numpy as np
import matplotlib.pyplot as plt
import warnings
import re
from scipy.optimize import minimize
from typing import List, Tuple, Union, Dict, Optional, Any, Sequence

from easy_vqe.hamiltonian import parse_hamiltonian_expression
from easy_vqe.circuit import create_custom_ansatz
from easy_vqe.measurement import get_hamiltonian_expectation_value

class OptimizationLogger:
    """Helper class to store optimization history during scipy.minimize."""
    def __init__(self):
        self.eval_count = 0
        self.params_history: List[np.ndarray] = []
        self.value_history: List[float] = []
        self._last_print_eval = 0

    def callback(self, current_params: np.ndarray, current_value: float, display_progress: bool = False, print_interval: int = 10):
        """Stores current parameters and value, optionally prints progress."""
        self.eval_count += 1
        self.params_history.append(np.copy(current_params))
        self.value_history.append(current_value)

        if display_progress and (self.eval_count - self._last_print_eval >= print_interval):
             # Only print if the value is finite
             if np.isfinite(current_value):
                 print(f"  Eval: {self.eval_count:4d} | Energy: {current_value: .8f}")
             else:
                 print(f"  Eval: {self.eval_count:4d} | Energy: {current_value}") # Print inf/nan directly
             self._last_print_eval = self.eval_count

    def get_history(self) -> Tuple[List[float], List[np.ndarray]]:
        """Returns the recorded history."""
        return self.value_history, self.params_history


def find_ground_state(
    ansatz_structure: List[Union[Tuple[str, List[int]], List]],
    hamiltonian_expression: str,
    n_shots: int = 2048,
    optimizer_method: str = 'COBYLA',
    optimizer_options: Optional[Dict[str, Any]] = None,
    initial_params_strategy: Union[str, np.ndarray, Sequence[float]] = 'random',
    max_evaluations: Optional[int] = 150,
    display_progress: bool = True,
    plot_filename: Optional[str] = None
) -> Dict[str, Any]:
    """
    Performs the Variational Quantum Eigensolver (VQE) algorithm to find the
    approximate ground state energy of a given Hamiltonian using simulation.

    Args:
        ansatz_structure: Definition for `create_custom_ansatz`.
        hamiltonian_expression: Hamiltonian string (e.g., "-1.0*ZZ + 0.5*X").
        n_shots: Number of shots per expectation value estimation. Higher values
                 reduce noise but increase simulation time.
        optimizer_method: Name of the SciPy optimizer to use (e.g., 'COBYLA',
                          'Nelder-Mead', 'L-BFGS-B', 'Powell', 'SLSQP').
        optimizer_options: Dictionary of options passed directly to the SciPy
                           optimizer (e.g., {'maxiter': 200, 'tol': 1e-6}).
                           Overrides `max_evaluations` if relevant keys exist.
        initial_params_strategy: Method for generating initial parameters:
            - 'random': Uniformly random values in [0, 2*pi).
            - 'zeros': All parameters initialized to 0.0.
            - np.ndarray or Sequence: A specific array/list of initial values.
        max_evaluations: Approximate maximum number of objective function calls
                         (used to set 'maxiter' or 'maxfun'/'maxfev' in options
                         if not already specified).
        display_progress: If True, prints energy updates during optimization.
        plot_filename: If a filename string is provided (e.g., "convergence.png"),
                       saves the energy convergence plot to that file. If None,
                       no plot is saved.

    Returns:
        Dict[str, Any]: A dictionary containing VQE results:
            - 'optimal_params' (np.ndarray): Best parameters found.
            - 'optimal_value' (float): Minimum expectation value (energy) found.
            - 'num_qubits' (int): Number of qubits determined from Hamiltonian.
            - 'ansatz' (QuantumCircuit): The constructed ansatz circuit.
            - 'parameters' (List[Parameter]): Parameter objects in the ansatz.
            - 'optimization_result' (OptimizeResult): Full result from `scipy.optimize.minimize`.
            - 'cost_history' (List[float]): Energy values at each evaluation.
            - 'parameter_history' (List[np.ndarray]): Parameter vectors at each evaluation.
            - 'success' (bool): Optimizer success flag.
            - 'message' (str): Optimizer termination message.
            - 'n_shots' (int): Shots used per evaluation.
            - 'optimizer_method' (str): Optimizer used.
            - 'hamiltonian_expression' (str): Original Hamiltonian string.
            - 'plot_filename' (Optional[str]): Filename if plot was saved.
        Returns {'error': ..., 'details': ...} dictionary on critical failure during setup.
    """
    print("-" * 50)
    print("           Easy VQE - Ground State Search")
    print("-" * 50)
    print(f"Hamiltonian: {hamiltonian_expression}")
    print(f"Optimizer: {optimizer_method} | Shots per Eval: {n_shots}")

    result_dict: Dict[str, Any] = {
        'hamiltonian_expression': hamiltonian_expression,
        'optimizer_method': optimizer_method,
        'n_shots': n_shots,
        'plot_filename': plot_filename, # Store requested filename
        'optimal_params': None,
        'optimal_value': None,
        'num_qubits': None,
        'ansatz': None,
        'parameters': [],
        'optimization_result': None,
        'cost_history': [],
        'parameter_history': [],
        'success': False,
        'message': 'Initialization',
        'initial_params': None,
        'initial_params_strategy_used': None,
    }

    try:
        parsed_hamiltonian = parse_hamiltonian_expression(hamiltonian_expression)
        if not parsed_hamiltonian:
             print("[Error] Hamiltonian expression parsed successfully but resulted in zero terms.")
             result_dict.update({'error': 'Hamiltonian parsing resulted in zero terms'})
             return result_dict
        num_qubits = len(parsed_hamiltonian[0][1])
        result_dict['num_qubits'] = num_qubits
        print(f"Parsed Hamiltonian: {len(parsed_hamiltonian)} terms | Qubits: {num_qubits}")
    except Exception as e:
        print(f"\n[Error] Failed during Hamiltonian parsing or validation: {e}")
        result_dict.update({'error': 'Hamiltonian processing failed', 'details': str(e)})
        return result_dict # Exit early

    try:
        ansatz, parameters = create_custom_ansatz(num_qubits, ansatz_structure)
        num_params = len(parameters)
        result_dict.update({'ansatz': ansatz, 'parameters': parameters})
        print(f"Created Ansatz: {num_params} parameters")

        if num_params == 0:
            warnings.warn("Ansatz has no parameters. Calculating fixed expectation value.", UserWarning)
            try:
                # Use None for param_values when no parameters exist
                fixed_value = get_hamiltonian_expectation_value(ansatz, parsed_hamiltonian, None, n_shots)
                print(f"Fixed Expectation Value: {fixed_value:.8f}")
                result_dict.update({
                    'optimal_params': np.array([]), 'optimal_value': fixed_value,
                    'optimization_result': None, 'cost_history': [fixed_value],
                    'parameter_history': [np.array([])], 'success': True,
                    'message': 'Static evaluation (no parameters)'
                 })
                return result_dict
            except Exception as e:
                print(f"\n[Error] Failed to calculate fixed expectation value: {e}")
                result_dict.update({'error': 'Failed static evaluation', 'details': str(e)})
                return result_dict

    except Exception as e:
        print(f"\n[Error] Failed during Ansatz creation: {e}")
        result_dict.update({'error': 'Ansatz creation failed', 'details': str(e)})
        return result_dict # Exit early

    logger = OptimizationLogger()

    def objective_function(current_params: np.ndarray) -> float:
        """Closure for the optimizer, calculates Hamiltonian expectation value."""
        value = np.inf # Default to infinity
        try:
            exp_val = get_hamiltonian_expectation_value(
                ansatz=ansatz,
                parsed_hamiltonian=parsed_hamiltonian,
                param_values=current_params,
                n_shots=n_shots
            )
            value = exp_val
        except (ValueError, RuntimeError, TypeError) as e:
             print(f"\n[Warning] Error during expectation value calculation (params={np.round(current_params[:4], 3)}...): {e}")
             # value remains inf
        except Exception as e:
             print(f"\n[Critical Warning] Unexpected error in objective function: {e}")
             # value remains inf
        finally:
             # Log the attempt regardless of success, potentially with inf value
             logger.callback(current_params, value, display_progress=display_progress)
             return value # Return the calculated value or inf

    initial_params: np.ndarray
    strategy_name_used: str # Variable to store the name

    print("\nProcessing Initial Parameters Strategy...")
    current_strategy = initial_params_strategy

    if isinstance(current_strategy, np.ndarray):
        if current_strategy.shape == (num_params,):
            try:
                initial_params = current_strategy.astype(float)
                strategy_name_used = 'provided_array'
                print(f"Strategy: Using provided numpy array (shape {initial_params.shape}) for initial parameters.")
            except ValueError as ve:
                print(f"[Warning] Could not convert provided numpy array elements to float: {ve}. Defaulting to 'random'.")
                initial_params = np.random.uniform(0, 2 * np.pi, num_params)
                strategy_name_used = 'random'
                print(f"Strategy: Using 'random' (generated {num_params} parameters).")
        else:
            print(f"[Warning] Provided initial_params numpy array shape {current_strategy.shape} != expected ({num_params},). Defaulting to 'random'.")
            initial_params = np.random.uniform(0, 2 * np.pi, num_params)
            strategy_name_used = 'random'
            print(f"Strategy: Using 'random' (generated {num_params} parameters).")

    elif isinstance(current_strategy, (list, tuple)):
         if len(current_strategy) == num_params:
             try:
                 initial_params = np.array(current_strategy, dtype=float)
                 strategy_name_used = 'provided_list_tuple'
                 print(f"Strategy: Using provided list/tuple (length {len(current_strategy)}) for initial parameters.")
             except ValueError as ve:
                 print(f"[Warning] Could not convert provided list/tuple to numeric array: {ve}. Defaulting to 'random'.")
                 initial_params = np.random.uniform(0, 2 * np.pi, num_params)
                 strategy_name_used = 'random'
                 print(f"Strategy: Using 'random' (generated {num_params} parameters).")
         else:
            print(f"[Warning] Provided initial_params list/tuple length {len(current_strategy)} != expected {num_params}. Defaulting to 'random'.")
            initial_params = np.random.uniform(0, 2 * np.pi, num_params)
            strategy_name_used = 'random'
            print(f"Strategy: Using 'random' (generated {num_params} parameters).")

    elif isinstance(current_strategy, str) and current_strategy == 'zeros':
         initial_params = np.zeros(num_params)
         strategy_name_used = 'zeros'
         print(f"Strategy: Using 'zeros' (generated {num_params} parameters).")
    elif isinstance(current_strategy, str) and current_strategy == 'random':
         initial_params = np.random.uniform(0, 2 * np.pi, num_params)
         strategy_name_used = 'random'
         print(f"Strategy: Using 'random' (generated {num_params} parameters).")
    else:
         print(f"[Warning] Unknown or invalid initial_params_strategy '{current_strategy}'. Defaulting to 'random'.")
         initial_params = np.random.uniform(0, 2 * np.pi, num_params)
         strategy_name_used = 'random'
         print(f"Strategy: Using 'random' (generated {num_params} parameters).")

    result_dict['initial_params'] = np.copy(initial_params)
    result_dict['initial_params_strategy_used'] = strategy_name_used

    opt_options = optimizer_options if optimizer_options is not None else {}
    if max_evaluations is not None:
         max_eval_int = int(max_evaluations)
         # Set default based on common SciPy usage if not explicitly provided
         if optimizer_method.upper() in ['COBYLA', 'NELDER-MEAD', 'POWELL', 'SLSQP'] and 'maxiter' not in opt_options:
             opt_options['maxiter'] = max_eval_int
             print(f"Setting optimizer 'maxiter' to {opt_options['maxiter']} based on max_evaluations.")
         elif optimizer_method.upper() in ['L-BFGS-B', 'TNC'] and 'maxfun' not in opt_options:
              opt_options['maxfun'] = max_eval_int
              print(f"Setting optimizer 'maxfun' to {opt_options['maxfun']} based on max_evaluations.")
         elif 'maxiter' not in opt_options and 'maxfev' not in opt_options and 'maxfun' not in opt_options:
             # Generic fallback if optimizer type isn't specifically known
             opt_options['maxiter'] = max_eval_int # Default to maxiter
             print(f"Setting optimizer 'maxiter' to {opt_options['maxiter']} as a default based on max_evaluations.")


    print(f"\nStarting Optimization with {optimizer_method}...")
    print(f"Initial Parameters (first 5): {np.round(initial_params[:5], 5)}")

    initial_energy = objective_function(initial_params) # This also logs the first point
    if not np.isfinite(initial_energy): # Check for inf or nan
        print("[Error] Objective function returned non-finite value for initial parameters. Cannot start optimization.")
        result_dict.update({
            'error': 'Initial parameters yield invalid energy (inf/nan).',
            'details': 'Check ansatz or Hamiltonian.',
            'optimal_value': initial_energy, # Store the non-finite value
            'cost_history': logger.value_history, # Store history up to this point
            'parameter_history': logger.params_history
        })
        return result_dict # Exit early

    print(f"Initial Energy: {initial_energy:.8f}")

    try:
        result = minimize(objective_function,
                          initial_params,
                          method=optimizer_method,
                          options=opt_options)

    except Exception as e:
        print(f"\n[Error] Optimization process failed unexpectedly: {e}")
        cost_history, param_history = logger.get_history()
        result_dict.update({
            'error': 'Optimization process failed', 'details': str(e),
            'cost_history': cost_history, # Log history up to failure
            'parameter_history': param_history,
            'optimization_result': None, # No result object from minimize
            'success': False, # Mark as unsuccessful
            'message': f'Optimization terminated due to error: {e}'
        })
        return result_dict # Exit here


    print("\n" + "-"*20 + " Optimization Finished " + "-"*20)
    cost_history, param_history = logger.get_history()
    result_dict.update({
        'optimal_params': result.x,
        'optimal_value': result.fun,
        'optimization_result': result,
        'cost_history': cost_history,
        'parameter_history': param_history,
        'success': result.success,
        'message': result.message,
    })

    if result.success:
        print("Optimizer terminated successfully.")
    else:
        print(f"[Warning] Optimizer terminated unsuccessfully: {result.message}")

    # Use logger count as fallback if nfev not present
    eval_count_display = getattr(result, 'nfev', logger.eval_count)
    print(f"Function Evaluations: {eval_count_display}")
    if hasattr(result, 'nit'): print(f"Iterations: {result.nit}")

    # Only print optimal energy if it's finite
    if np.isfinite(result_dict['optimal_value']):
        print(f"Optimal Energy Found: {result_dict['optimal_value']:.10f}")
    else:
        print(f"Final Value Found: {result_dict['optimal_value']}") # Print inf/nan directly

    opt_params = result_dict['optimal_params']
    if opt_params is not None:
        if len(opt_params) < 15:
             print(f"Optimal Parameters:\n{np.round(opt_params, 5)}")
        else:
             print(f"Optimal Parameters: (Array length {len(opt_params)})")
             print(f"  First 5: {np.round(opt_params[:5], 5)}")
             print(f"  Last 5:  {np.round(opt_params[-5:], 5)}")
    else:
        print("Optimal Parameters: Not available.")
    print("-" * 50)

    if plot_filename and result_dict['cost_history']:
        try:
            fig, ax = plt.subplots(figsize=(10, 6))
            valid_history = [(i,e) for i, e in enumerate(result_dict['cost_history']) if np.isfinite(e)]
            if valid_history:
                 steps, energies = zip(*valid_history)
                 ax.plot(steps, energies, marker='.', linestyle='-', markersize=4)
                 ax.set_ylabel("Hamiltonian Expectation Value (Energy)")
            else:
                 ax.text(0.5, 0.5, 'No finite energy values recorded', ha='center', va='center')
                 ax.set_ylabel("Value") # Generic label if no energy

            ax.set_xlabel("Optimization Evaluation Step")
            ax.set_title(f"VQE Convergence ({optimizer_method}, {n_shots} shots)")
            ax.grid(True, linestyle='--', alpha=0.6)
            fig.tight_layout()
            fig.savefig(plot_filename)
            plt.close(fig)
            print(f"Convergence plot saved to '{plot_filename}'")
            result_dict['plot_filename'] = plot_filename # Confirm saved filename
        except Exception as e:
            print(f"[Warning] Could not save convergence plot to '{plot_filename}': {e}")
            result_dict['plot_filename'] = None # Indicate failure
    elif plot_filename and not result_dict['cost_history']:
         print(f"[Info] Plotting skipped: No cost history recorded.")
         result_dict['plot_filename'] = None


    return result_dict