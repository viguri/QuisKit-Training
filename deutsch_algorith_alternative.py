import qiskit
from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
from qiskit_ibm_runtime import QiskitRuntimeService, Sampler
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import os
import logging
import random

# Execution type: 'simulator' or 'hardware'
RUN_TYPE = 'hardware'  # Change to 'hardware' to run on quantum hardware

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Ensure pictures directory exists
os.makedirs('pictures/deutsch', exist_ok=True)

def constant_oracle():
    """Creates a quantum oracle for a constant function (f(x) = 0)"""
    oracle = QuantumCircuit(2)
    return oracle.to_gate(label="Constante")

def balanced_oracle():
    """Creates a quantum oracle for a balanced function (f(x) = x)"""
    oracle = QuantumCircuit(2)
    oracle.cx(0, 1)  # CNOT gate makes f(x) = x
    return oracle.to_gate(label="Balanceada")

def deutsch_algorithm(oracle):
    """
    Implements the Deutsch algorithm with the given oracle.
    
    Args:
        oracle: Quantum gate implementing either constant or balanced function
        
    Returns:
        QuantumCircuit: The complete Deutsch algorithm circuit
    """
    qc = QuantumCircuit(2, 1)  # Two qubits and one classical bit
    
    # Initialization
    qc.x(1)  # Apply X to auxiliary qubit
    qc.h([0, 1])  # Apply Hadamard to both qubits
    
    # Apply the oracle
    qc.append(oracle, [0, 1])
    
    # Final transformation
    qc.h(0)
    
    # Measure first qubit
    qc.measure(0, 0)
    
    return qc

def format_histogram_data(raw_counts):
    """Convert raw counts to the format expected by plot_histogram"""
    formatted_counts = {}
    for k, v in raw_counts.items():
        # Ensure k is treated as a string and get its length
        k_str = str(k)
        # For single bit results, pad with leading zero if needed
        if len(k_str) == 1:
            k_str = '0' + k_str
        formatted_counts[k_str] = v
    return formatted_counts

def run_simulation(circuit, oracle_type):
    """Run the circuit on the local simulator"""
    simulator = Aer.get_backend('qasm_simulator')
    transpiled_circuit = transpile(circuit, backend=simulator)
    job = simulator.run(transpiled_circuit, shots=1000)
    result = job.result()
    counts = result.get_counts()

    logger.info(f"Simulation results for {oracle_type} oracle: {counts}")
    plot_histogram(counts)
    plt.title(f"Simulation Results ({oracle_type} oracle)")
    plt.savefig('pictures/deutsch/deutsch_algorithm_simulation.png')
    plt.close()
    
    return counts

def run_hardware(circuit, oracle_type):
    """Run the circuit on quantum hardware"""
    # Load environment variables
    load_dotenv()
    
    # Get the IBMQ key
    IBMQ_KEY = os.getenv('IBMQ_KEY')
    if IBMQ_KEY is None:
        raise ValueError("IBMQ_KEY not found in environment variables")

    # Initialize Runtime Service
    service = QiskitRuntimeService(channel="ibm_quantum", token=IBMQ_KEY)
    
    # Get available backends
    backends = service.backends()
    logger.info("Available backends:")
    for backend in backends:
        try:
            qbits_count = len(backend.properties().qubits)
        except:
            qbits_count = "simulated"
        logger.info(f"- {backend.name}: {backend.status().pending_jobs} pending jobs & {qbits_count} qubits")
    
    # Get ibm_kyiv backend
    backend = None
    for b in backends:
        if b.name == "ibm_kyiv":
            backend = b
            break
            
    if backend is None:
        raise ValueError("ibm_kyiv backend not found")

    # Transpile circuit for hardware
    logger.info("Transpiling circuit for hardware...")
    hw_transpiled = transpile(circuit, backend=backend)
    logger.info("Circuit transpiled successfully")
    
    # Save transpiled circuit visualization
    hw_transpiled.draw(output='mpl').savefig('pictures/deutsch/deutsch_algorithm_transpiled.png')
    plt.close()

    # Initialize sampler and run
    sampler = Sampler(mode=backend)
    logger.info("Submitting job to quantum hardware...")
    job = sampler.run([hw_transpiled], shots=1000)

    logger.info(f"Job ID: {job.job_id}")
    logger.info("Waiting for job completion...")
    result = job.result()
    pub_result = result[0].data.c.get_counts()
    
    # Format the results for histogram plotting
    formatted_results = format_histogram_data(pub_result)
    
    logger.info(f"Quantum hardware results for {oracle_type} oracle: {formatted_results}")
    plot_histogram([formatted_results])
    plt.title(f"Quantum Hardware Results ({oracle_type} oracle)")
    plt.savefig('pictures/deutsch/deutsch_algorithm_hardware.png')
    plt.close()
    
    return pub_result

def main():
    """Main execution function"""
    # Choose oracle type randomly
    oracle_type = random.choice(["constant", "balanced"])
    logger.info(f"Using {oracle_type} oracle")

    # Create oracle
    oracle = constant_oracle() if oracle_type == "constant" else balanced_oracle()

    # Create the Deutsch circuit
    circuit = deutsch_algorithm(oracle)

    # Save initial circuit visualization
    circuit.draw(output='mpl').savefig('pictures/deutsch/deutsch_algorithm_initial.png')
    plt.close()

    try:
        if RUN_TYPE == 'simulator':
            results = run_simulation(circuit, oracle_type)
        else:
            results = run_hardware(circuit, oracle_type)
        logger.info(f"Algorithm completed successfully on {RUN_TYPE}")
    except Exception as e:
        logger.error(f"Error running on {RUN_TYPE}: {str(e)}")

if __name__ == "__main__":
    main()
