from qiskit import *
from qiskit_aer import Aer
from qiskit_ibm_provider import IBMProvider
from qiskit_ibm_runtime import QiskitRuntimeService, Sampler, Session
from qiskit.compiler import transpile
from dotenv import load_dotenv
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt
import logging
import sys

logging.basicConfig(level=logging.INFO)
import os

# Ensure pictures directory exists
os.makedirs('pictures/deutsch', exist_ok=True)

circuit = QuantumCircuit(2,1)
circuit.h(0)
circuit.x(1)
circuit.h(1)

circuit.barrier()

circuit.draw(output='mpl').savefig('pictures/deutsch/deutsch_algorithm.png')

circuit.cx(0,1)

circuit.barrier()
circuit.h(0)

circuit.barrier()
circuit.draw(output='mpl').savefig('pictures/deutsch/deutsch_algorithm_circuit.png')

circuit.measure(0,0)
circuit.draw(output='mpl').savefig('pictures/deutsch/deutsch_algorithm_measure.png')

# Run simulation
simulator = Aer.get_backend('qasm_simulator')
result = simulator.run(circuit, shots=1).result()
counts = result.get_counts(circuit)
measured = list(counts.keys())[0]

logging.info(f"Local simulation measurement result: {measured}")
plot_histogram([counts])
plt.savefig('pictures/deutsch/deutsch_algorithm_histogram.png')
plt.close()  # Close the figure to free memory

# Load environment variables from .env file
load_dotenv()

# Get the IBMQ key from environment variables
IBMQ_KEY = os.getenv('IBMQ_KEY')
if IBMQ_KEY is None:
    raise ValueError("IBMQ_KEY not found in environment variables")

try:
    # Initialize the Runtime Service
    service = QiskitRuntimeService(channel="ibm_quantum", token=IBMQ_KEY)
    
    # Get the available backends
    backends = service.backends()
    logging.info("Available backends:")
    for backend in backends:
        try:
            qbits_count = len(backend.properties().qubits)
        except:
            qbits_count = "simulated"
        logging.info(f"- {backend.name}: {backend.status().pending_jobs} pending jobs & {qbits_count} qubits")
    
    # Get the ibm_kyiv backend
    backend = None
    for b in backends:
        if b.name == "ibm_kyiv":
            backend = b
            break
            
    if backend is None:
        raise ValueError("ibm_kyiv backend not found")

    # Transpile the circuit for the target hardware
    logging.info("Transpiling circuit for hardware...")
    transpiled_circuit = transpile(circuit, backend=backend, optimization_level=1)
    logging.info("Circuit transpiled successfully")
    
    # Draw and save the transpiled circuit
    transpiled_circuit.draw(output='mpl').savefig('pictures/deutsch/deutsch_algorithm_transpiled.png')
    plt.close()

    # Initialize the sampler with the backend
    sampler = Sampler(mode=backend)

    # Submit job using the sampler
    logging.info("Submitting job using Sampler primitive")
    job = sampler.run([transpiled_circuit], shots=1)

    logging.info(f"Job ID: {job.job_id}")
    logging.info("Waiting for job completion...")
    result = job.result()
    
    plot_histogram(result)
    plt.title("Quantum Hardware Results")
    plt.savefig('pictures/deutsch/deutsch_algorithm_quantum_histogram.png')
    plt.close()
except Exception as e:
    logging.error(f"Error running on quantum hardware: {str(e)}")
logging.info("Program completed.")
