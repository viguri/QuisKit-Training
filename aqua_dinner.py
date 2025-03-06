from matplotlib import pyplot as plt
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
from dotenv import load_dotenv
import os
import logging

def create_oracle():
    # Create a circuit for 4 qubits (James, Lars, Kirk, Rob) plus 1 auxiliary qubit
    oracle = QuantumCircuit(5)
    
    # James AND Lars (x1 AND x2)
    oracle.ccx(0, 1, 4)  # Store in auxiliary qubit
    
    # Kirk AND Rob (x3 AND x4)
    oracle.ccx(2, 3, 4)  # XOR with auxiliary qubit (effectively OR)
    
    # NOT(Lars AND Rob) - we negate this combination
    oracle.ccx(1, 3, 4)  # If Lars(1) and Rob(3) are together, flip the result
    
    return oracle

def create_diffusion():
    n = 4  # number of qubits
    qc = QuantumCircuit(n + 1)  # +1 for auxiliary qubit
    
    # Apply H-gates
    for qubit in range(n):
        qc.h(qubit)
    
    # Apply X-gates
    for qubit in range(n):
        qc.x(qubit)
    
    # Multi-controlled Z-gate
    qc.h(n-1)
    qc.mcx(list(range(n-1)), n-1)  # Multi-controlled-X (Toffoli)
    qc.h(n-1)
    
    # Apply X-gates
    for qubit in range(n):
        qc.x(qubit)
    
    # Apply H-gates
    for qubit in range(n):
        qc.h(qubit)
    
    return qc

# Set up quantum circuit for Grover's algorithm
n = 4  # number of qubits for input variables
qr = QuantumRegister(n + 1, 'q')  # +1 for auxiliary qubit
cr = ClassicalRegister(n, 'c')
circuit = QuantumCircuit(qr, cr)

# Initialize superposition
for qubit in range(n):
    circuit.h(qubit)

# Number of Grover iterations (pi/4 * sqrt(N))
iterations = 2

# Apply Grover iteration
for _ in range(iterations):
    # Oracle
    circuit.compose(create_oracle(), inplace=True)
    # Diffusion
    circuit.compose(create_diffusion(), inplace=True)

# Measure the first 4 qubits (not the auxiliary)
for i in range(n):
    circuit.measure(i, i)

# Run the circuit
simulator = AerSimulator()
job = simulator.run(circuit, shots=1024)
result = job.result()
counts = result.get_counts(circuit)

# Plot results
plot_histogram(counts, title='Valid Dinner Combinations')
plt.savefig('pictures/dinner/grover_algorithm.png')
plt.close()