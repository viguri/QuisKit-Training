from qiskit import QuantumCircuit
from qiskit_aer import Aer
from qiskit.visualization import plot_histogram
from qiskit_ibm_provider import IBMProvider
from qiskit_ibm_runtime import QiskitRuntimeService, Sampler
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import os

# Load environment variables from .env file
load_dotenv()

# Get the IBMQ key from environment variables
IBMQ_KEY = os.getenv('IBMQ_KEY')
if IBMQ_KEY is None:
    raise ValueError("IBMQ_KEY not found in environment variables")

# Initialize the Runtime Service
service = QiskitRuntimeService(channel="ibm_quantum", token=IBMQ_KEY)

# Get the available backends
backends = service.backends()

# Print the available backends
print("Available backends:")
for backend in backends:
    try:
        qbits_count = len(backend.properties().qubits)
    except:
        qbits_count = "N/A"
    print(f"- {backend.name}: {qbits_count} qubits")
    status = backend.status()
    print(f"  Status: {status}")
    print(f"  Properties: {backend.properties}")
    print(f"  Configuration: {backend.configuration}")
    
# Create a quantum circuit with 2 qubits and 2 classical bits
circuit = QuantumCircuit(2, 2)

# Apply a Hadamard gate to the first qubit
circuit.h(0)

# Draw the circuit using matplotlib
circuit.draw(output='mpl', filename='pictures/hadamard_gate.png')

# Apply a CNOT gate using the first qubit as control and the second as target
circuit.cx(0, 1)  # 0: control qubit, 1: target qubit

# Draw the CNOT gate
circuit.draw(output='mpl', filename='pictures/CNOT_gate.png')

# Measure both qubits
circuit.measure([0,1], [0,1])

# Draw the measurements
circuit.draw(output='mpl', filename='pictures/measurements.png')

# Draw the circuit
print("\nQuantum Circuit:")
print(circuit)

# Set up the Sampler primitive and run
print("\nExecuting circuit using Qiskit Runtime Sampler...")
sampler = Sampler(service=service, backend="ibmq_qasm_simulator")
job = sampler.run(circuits=[circuit], shots=1000)
result = job.result()
quasi_dists = result.quasi_dists[0]

# Convert quasi-distribution to counts format
counts = {format(k, '0' + str(2) + 'b'): int(v * 1000) for k, v in quasi_dists.items()}
print("\nMeasurement results:", counts)

# Visualize the results
plt.figure(figsize=(8, 6))
plot_histogram(counts)
plt.title("Results Histogram")
plt.savefig('pictures/results_histogram.png')
print("\nHistogram saved as 'results_histogram.png'")

# Print an explanation of the results
print("\nExplanation:")
print("- The results show the different measurements obtained and their frequency")
print("- We mainly observe '00' and '11' states with similar probabilities")
print("- This demonstrates quantum entanglement: the qubits are perfectly correlated")
print("- This is an example of a Bell state, one of the most important quantum states")