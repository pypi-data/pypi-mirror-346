"""
Hamiltonian parsing and manipulation functions for Easy VQE.

This module provides tools for parsing Hamiltonian expressions in string format
and calculating theoretical ground state energies.
"""

import re
import numpy as np
from typing import List, Tuple


def parse_hamiltonian_expression(hamiltonian_string: str) -> List[Tuple[float, str]]:
    """
    Parses a Hamiltonian string expression into a list of (coefficient, pauli_string) tuples.

    Handles explicit coefficients (e.g., "-1.5 * XY"), implicit coefficients (e.g., "+ ZZ", "- YI"),
    various spacing, combinations like "+ -0.5 * ZIZ", and validates the format.

    Args:
        hamiltonian_string: The Hamiltonian expression (e.g., "1.0*XX - 0.5*ZI + YZ").

    Returns:
        List[Tuple[float, str]]: List of (coefficient, pauli_string) tuples.

    Raises:
        ValueError: If the string format is invalid, contains inconsistent Pauli lengths,
                    invalid characters, or invalid numeric coefficients.
        TypeError: If input is not a string.
    """
    if not isinstance(hamiltonian_string, str):
        raise TypeError("Hamiltonian expression must be a string.")

    hamiltonian_string = hamiltonian_string.strip()
    if not hamiltonian_string:
         raise ValueError("Hamiltonian expression cannot be empty.")

    combined_pattern = re.compile(
        r"([+\-]?\s*(?:[+\-]\s*)?(?:(?:\d+\.?\d*|\.?\d+)(?:[eE][+\-]?\d+)?)\s*\*\s*([IXYZ]+))"
        r"|(\s*(?:(?:\d+\.?\d*|\.?\d+)(?:[eE][+\-]?\d+)?)\s*\*\s*([IXYZ]+))"
        r"|(([+\-])\s*([IXYZ]+))"
        r"|^([IXYZ]+)"
    )

    parsed_terms = []
    current_pos = 0
    ham_len = len(hamiltonian_string)

    while current_pos < ham_len:
        match_start_search = re.search(r'\S', hamiltonian_string[current_pos:])
        if not match_start_search:
            break
        search_pos = current_pos + match_start_search.start()

        match = combined_pattern.match(hamiltonian_string, search_pos)

        if not match:
            remaining_str = hamiltonian_string[search_pos:]
            if remaining_str.startswith('*'):
                 raise ValueError(f"Syntax error near position {search_pos}: Unexpected '*' without preceding coefficient.")
            raise ValueError(f"Could not parse term starting near position {search_pos}: '{hamiltonian_string[search_pos:min(search_pos+20, ham_len)]}...'. Check syntax (e.g., signs, '*', Pauli chars [IXYZ]).")

        coefficient: float = 1.0
        pauli_str: str = None
        term_str = match.group(0).strip()

        if match.group(1): # Option 1 (+/- optional sign) coeff * Pauli
             term_part = match.group(1).split('*')[0].strip()
             try:
                 coefficient = float(term_part.replace(" ", ""))
             except ValueError: raise ValueError(f"Invalid numeric coefficient '{term_part}' in term '{term_str}'.")
             pauli_str = match.group(2)
        elif match.group(3): # Option 1b (coeff * Pauli, positive implicit sign)
            term_part = match.group(3).split('*')[0].strip()
            try: coefficient = float(term_part.replace(" ", ""))
            except ValueError: raise ValueError(f"Invalid numeric coefficient '{term_part}' in term '{term_str}'.")
            pauli_str = match.group(4)
        elif match.group(5): # Option 2 (+/- Pauli)
            sign = match.group(6)
            coefficient = -1.0 if sign == '-' else 1.0
            pauli_str = match.group(7)
        elif match.group(8): # Option 2b (Pauli at start, positive implicit sign)
             # Check context: is it really the start or just after another Pauli?
             if search_pos != 0:
                 # Look backwards for the last non-whitespace character
                 look_back_pos = search_pos - 1
                 while look_back_pos >= 0 and hamiltonian_string[look_back_pos].isspace():
                     look_back_pos -= 1
                 if look_back_pos >= 0 and hamiltonian_string[look_back_pos] not in '+-':
                      raise ValueError(f"Ambiguous term '{match.group(8)}' at pos {search_pos}. Terms after the first need explicit '+', '-', or 'coeff *'.")
             coefficient = 1.0
             pauli_str = match.group(8)
        else:
             raise RuntimeError(f"Internal parsing error: Regex match failed unexpectedly near '{hamiltonian_string[search_pos:search_pos+10]}...'")

        if pauli_str is None: raise ValueError(f"Failed to extract Pauli string from parsed term '{term_str}'.")
        if not pauli_str: raise ValueError(f"Empty Pauli string found in term '{term_str}'.")
        if not all(c in 'IXYZ' for c in pauli_str): raise ValueError(f"Invalid character '{next((c for c in pauli_str if c not in 'IXYZ'), '')}' found in Pauli string '{pauli_str}' within term '{term_str}'. Only 'I', 'X', 'Y', 'Z' allowed.")
        if np.isnan(coefficient) or np.isinf(coefficient): raise ValueError(f"Invalid coefficient value ({coefficient}) found for term '{pauli_str}'.")


        parsed_terms.append((coefficient, pauli_str))
        current_pos = match.end()

    if not parsed_terms:
        raise ValueError(f"Could not parse any valid Hamiltonian terms from the input string: '{hamiltonian_string}'.")

    if parsed_terms:
        num_qubits = len(parsed_terms[0][1])
        if num_qubits == 0: raise ValueError("Parsed Pauli string has zero length (Internal Error).")
        for i, (coeff, p_str) in enumerate(parsed_terms):
            if len(p_str) != num_qubits:
                raise ValueError(f"Inconsistent Pauli string lengths found: Term 0 '{parsed_terms[0][1]}' (len {num_qubits}) vs Term {i} '{p_str}' (len {len(p_str)}). All terms must act on the same number of qubits.")

    return parsed_terms


def get_theoretical_ground_state_energy(hamiltonian_expression: str) -> float:
    """
    Calculates the theoretical ground state energy of a Hamiltonian.

    Args:
        hamiltonian_expression: Hamiltonian string (e.g., "-1.0*ZZ + 0.5*X").

    Returns:
        float: The theoretical ground state energy.

    Raises:
        ValueError: If the Hamiltonian expression is invalid
    """
    pauli_i = np.array([[1, 0], [0, 1]], dtype=complex)
    pauli_x = np.array([[0, 1], [1, 0]], dtype=complex)
    pauli_y = np.array([[0, -1j], [1j, 0]], dtype=complex)
    pauli_z = np.array([[1, 0], [0, -1]], dtype=complex)
    pauli_map = {'I': pauli_i, 'X': pauli_x, 'Y': pauli_y, 'Z': pauli_z}

    parsed_ham = parse_hamiltonian_expression(hamiltonian_expression)

    num_qubits = len(parsed_ham[0][1])
    dim = 2**num_qubits
    ham_matrix = np.zeros((dim, dim), dtype=complex)

    for coeff, pauli_str in parsed_ham:
        term_matrix = np.array([[1]], dtype=complex) # Start with 1x1 identity for kron
        for pauli_char in pauli_str:
            term_matrix = np.kron(term_matrix, pauli_map[pauli_char])
        ham_matrix += coeff * term_matrix

    # Use eigvalsh for Hermitian matrices (faster and returns real eigenvalues)
    eigenvalues = np.linalg.eigvalsh(ham_matrix)
    ground_state_energy_exact = np.min(eigenvalues)

    # Eigenvalues should be real for Hermitian, but return .real for safety
    return ground_state_energy_exact.real