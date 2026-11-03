from typing import Tuple, Dict, Any
from qiskit import QuantumCircuit
from qiskit_aer import Aer
from qiskit.visualization import circuit_drawer
import logging
import os
from .exceptions import QuantumCircuitError, InvalidInputError

logger = logging.getLogger(__name__)

def create_bernstein_vazirani_circuit(secret_string: str) -> QuantumCircuit:
    """
    Create a Bernstein-Vazirani quantum circuit for the given secret string.
    
    Args:
        secret_string (str): The secret binary string (reading left to right)
        
    Returns:
        QuantumCircuit: The configured quantum circuit
        
    Raises:
        InvalidInputError: If the input string is invalid
    """
    if not secret_string or not all(bit in '01' for bit in secret_string):
        raise InvalidInputError("Secret string must be non-empty and contain only '0' and '1'")
        
    n = len(secret_string)
    circuit = QuantumCircuit(n + 1, n)
    
    # Initialize qubits
    circuit.h(range(n))      # Hadamard on first n qubits
    circuit.x(n)            # X gate on auxiliary qubit
    circuit.h(n)            # Hadamard on auxiliary qubit
    
    # Apply CNOT gates based on secret string
    for i in range(n):
        if secret_string[i] == '1':
            logger.info(f"Adding CNOT from control qubit {n-1-i} (secret bit position {i})")
            circuit.cx(n-1-i, n)
    
    # Apply final Hadamard gates and measure
    circuit.h(range(n))
    circuit.measure(range(n), range(n))
    
    return circuit

def save_circuit_diagram(circuit: QuantumCircuit, secret: str) -> str:
    """
    Save a visualization of the quantum circuit.
    
    Args:
        circuit (QuantumCircuit): The quantum circuit to visualize
        secret (str): The secret string used to generate the circuit
        
    Returns:
        str: Path to the saved circuit diagram
        
    Raises:
        QuantumCircuitError: If there's an error saving the circuit diagram
    """
    try:
        path = f"pictures/bernstein_vazirani/circuit_{secret}.png"
        fig = circuit_drawer(circuit, output='mpl')
        fig.savefig(path)
        return path
    except Exception as e:
        raise QuantumCircuitError(f"Failed to save circuit diagram: {str(e)}")

def run_bernstein_vazirani(secret: str) -> Dict[str, Any]:
    """
    Run the Bernstein-Vazirani algorithm with the given secret string.
    
    Args:
        secret (str): The secret binary string (reading left to right)
        
    Returns:
        Dict[str, Any]: Dictionary containing the result and circuit visualization path
        
    Raises:
        InvalidInputError: If the input is invalid
        QuantumCircuitError: If there's an error in circuit execution
    """
    try:
        # Create and visualize circuit
        circuit = create_bernstein_vazirani_circuit(secret)
        circuit_image = save_circuit_diagram(circuit, secret)
        
        # Run simulation
        simulator = Aer.get_backend('qasm_simulator')
        result = simulator.run(circuit, shots=1).result()
        counts = result.get_counts(circuit)
        measured = list(counts.keys())[0]
        
        # Reverse bits to match input format
        final_result = measured[::-1]
        logger.info(f"Raw measurement (circuit order): {measured}")
        logger.info(f"Final result (human readable): {final_result}")
        
        return {
            'result': final_result,
            'circuit_image': circuit_image,
            'secret': secret
        }
        
    except Exception as e:
        raise QuantumCircuitError(f"Error running Bernstein-Vazirani algorithm: {str(e)}")