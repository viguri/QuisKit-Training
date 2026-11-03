"""
Bernstein-Vazirani Algorithm Implementation

This algorithm finds a hidden binary string in a single query. In our case,
we have the secret number '1000101' which we want to discover.

Key concepts:
1. The circuit qubits are ordered from right to left (0 to 6)
2. CNOT gates need to be placed at positions corresponding to '1' bits
3. The measurement result needs to be reversed to match human-readable format

Example:
Secret:   1000101 (reading left to right)
Circuit:  1010001 (reading left to right in circuit)
CNOTs at: 0,2,6   (qubit positions, counting from right)
"""

from qiskit import *
from qiskit_aer import Aer
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

# The secret number we want to discover
secretNumber = '1000101'

# We need to reverse the secret number because:
# 1. In binary numbers, we read from right to left (LSB to MSB)
# 2. But circuit qubits are numbered from right to left
# 3. So we reverse the string to match qubit positions with bit positions
circuit_secret = secretNumber[::-1]

print("\nBernstein-Vazirani Algorithm")
print("-" * 30)
print("Circuit qubit ordering: 6 5 4 3 2 1 0 (right to left)")
print("Secret number positions: 0 1 2 3 4 5 6 (left to right)")
print(f"Secret number: {secretNumber}")
print("Trying to discover this number using Bernstein-Vazirani algorithm\n")

# Create circuit with n+1 qubits (n for secret number, 1 auxiliary)
circuit = QuantumCircuit(len(secretNumber)+1, len(secretNumber))

# Initialize with Hadamard gates
circuit.h(range(len(secretNumber)))  # H gates on all qubits except auxiliary
circuit.x(len(secretNumber))         # X gate on auxiliary qubit
circuit.h(len(secretNumber))         # H gate on auxiliary qubit

circuit.barrier()
circuit.draw(output='mpl', filename='pictures/bernstein_vazirani/01_initial_state.png')

# Add CNOT gates at positions corresponding to 1s in the secret number
# Note: The last qubit (index 7) is the auxiliary qubit used for phase kickback
for i in range(len(secretNumber)):
    if circuit_secret[i] == '1':
        print(f"Adding CNOT gate at qubit {i} because bit {len(secretNumber)-1-i} is 1")
        # CNOT between qubit i and auxiliary qubit
        # This encodes the secret bit pattern into quantum phases
        circuit.cx(i, len(secretNumber))

circuit.barrier()
circuit.draw(output='mpl', filename='pictures/bernstein_vazirani/02_after_cx.png')

print("\nApplying final Hadamard gates and measurement...")

# Final Hadamard gates transform phase differences back into bit values
circuit.h(range(len(secretNumber)))

# Measure all qubits except the auxiliary
# The measurement will collapse the superposition and reveal
# the secret number (after reversing the bit order)
print("Expected measurement result:", secretNumber)
circuit.measure(range(len(secretNumber)), range(len(secretNumber)))
circuit.barrier()
circuit.draw(output='mpl', filename='pictures/bernstein_vazirani/03_after_hadamard.png')

# Run simulation
simulator = Aer.get_backend('qasm_simulator')
result = simulator.run(circuit, shots=1).result()
counts = result.get_counts(circuit)
measured = list(counts.keys())[0]

print("\nMeasurement Analysis:")
print("-" * 30)
print(f"Raw measurement:     {measured}")
print(f"Secret number:       {secretNumber}")

# Verify if we got the correct secret number
if measured == secretNumber:
    print("\nSuccess! We found the secret number!")
    print("The quantum circuit directly measured the secret pattern")
else:
    print("\nNote: The measurement appears reversed because:")
    print("1. Quantum circuit qubits are numbered from right to left")
    print("2. Classical bits are numbered from left to right")
    print(f"Expected: {secretNumber}")
    print(f"Got:      {measured}")

print("\nNote: The algorithm works because:")
print("1. CNOT gates encode the secret pattern into quantum phases")
print("2. Hadamard gates convert these phases back into the correct bit values")
print("3. The auxiliary qubit helps perform phase kickback without changing the state")
