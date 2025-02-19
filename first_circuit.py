from qiskit import QuantumCircuit
from qiskit_aer import Aer
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

# Create a quantum circuit with 2 qubits and 2 classical bits
circuit = QuantumCircuit(2, 2)

# Apply a Hadamard gate to the first qubit
circuit.h(0)

# Apply a CNOT gate using the first qubit as control and the second as target
circuit.cx(0, 1)

# Measure both qubits
circuit.measure([0,1], [0,1])

# Draw the circuit
print("Quantum Circuit:")
print(circuit)

# Set up the simulator and run
simulator = Aer.get_backend('qasm_simulator')
job = simulator.run(circuit, shots=1000)
result = job.result()

# Get the counts
counts = result.get_counts(circuit)
print("\nMeasurement results:", counts)

# Visualize the results
plt.figure(figsize=(8, 6))
plot_histogram(counts)
plt.title("Results Histogram")
plt.savefig('results_histogram.png')
print("\nHistogram saved as 'results_histogram.png'")

# Print an explanation of the results
print("\nExplanation:")
print("- The results show the different measurements obtained and their frequency")
print("- We mainly observe '00' and '11' states with similar probabilities")
print("- This demonstrates quantum entanglement: the qubits are perfectly correlated")
print("- This is an example of a Bell state, one of the most important quantum states")