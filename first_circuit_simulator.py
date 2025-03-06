from qiskit import QuantumCircuit
from qiskit_aer import Aer
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt
import os

# Create circuit directory if it doesn't exist
os.makedirs('pictures/bell_state_simulator', exist_ok=True)

# Create a quantum circuit with 2 qubits and 2 classical bits
circuit = QuantumCircuit(2, 2)

# Step 1: Apply a Hadamard gate to the first qubit
circuit.h(0)

# Save visualization of circuit after Hadamard
circuit.draw(output='mpl', 
            filename='pictures/bell_state_simulator/01_hadamard_gate.png')

# Step 2: Apply CNOT gate with first qubit as control and second as target
circuit.cx(0, 1)  # 0: control qubit; 1: target qubit

# Save visualization of circuit after CNOT
circuit.draw(output='mpl', 
            filename='pictures/bell_state_simulator/02_hadamard_cnot_gates.png')

# Step 3: Add measurements
circuit.measure([0,1], [0,1])

# Save final circuit visualization
circuit.draw(output='mpl', 
            filename='pictures/bell_state_simulator/03_complete_circuit.png')

# Print the circuit representation
print("Quantum Circuit:")
print(circuit)

# Set up the simulator and run
simulator = Aer.get_backend('qasm_simulator')
job = simulator.run(circuit, shots=1000)
result = job.result()

# Get the counts of measurement outcomes
counts = result.get_counts(circuit)
print("\nMeasurement results:", counts)

# Create histogram visualization
plt.figure(figsize=(8, 6))
plot_histogram(counts)
plt.title("Bell State Measurement Results")
plt.savefig('pictures/bell_state_simulator/04_measurement_histogram.png')
print("\nHistogram saved as 'pictures/bell_state_simulator/04_measurement_histogram.png'")

# Create a state diagram of the Bell state evolution
plt.figure(figsize=(12, 4))

# Initial state |00⟩
plt.subplot(131)
plt.title("Initial State |00⟩")
plt.xticks([0, 1], ['|0⟩', '|1⟩'])
plt.yticks([])
plt.bar([0], [1])
plt.ylim(0, 1)

# After Hadamard
plt.subplot(132)
plt.title("After Hadamard\n(1/√2)(|0⟩ + |1⟩) ⊗ |0⟩")
plt.xticks([0, 1], ['|00⟩', '|10⟩'])
plt.yticks([])
plt.bar([0, 1], [0.5, 0.5])
plt.ylim(0, 1)

# Final Bell state
plt.subplot(133)
plt.title("Bell State\n(1/√2)(|00⟩ + |11⟩)")
plt.xticks([0, 1], ['|00⟩', '|11⟩'])
plt.yticks([])
plt.bar([0, 1], [0.5, 0.5])
plt.ylim(0, 1)

plt.tight_layout()
plt.savefig('pictures/bell_state_simulator/05_state_evolution.png')
print("State evolution diagram saved as 'pictures/bell_state_simulator/05_state_evolution.png'")

# Print explanation of results
print("\nExplanation:")
print("- The histogram shows measurement outcomes and their frequencies")
print("- Equal probability of measuring |00⟩ and |11⟩ states (~50% each)")
print("- Zero probability of measuring |01⟩ or |10⟩ states")
print("- This confirms the creation of the Bell state (|00⟩ + |11⟩)/√2")
print("- The correlations demonstrate quantum entanglement")