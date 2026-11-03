from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import Aer
from qiskit.visualization import plot_histogram, plot_bloch_multivector
from qiskit.quantum_info import Statevector
import matplotlib.pyplot as plt
import os

# Create directories for images
os.makedirs('pictures/superdense_coding', exist_ok=True)

def create_bell_pair():
    """
    Creates a Bell pair state |Φ⁺⟩ = (|00⟩ + |11⟩)/√2.
    This is used as the quantum channel between Alice and Bob.
    """
    qr = QuantumRegister(2, name='q')
    circuit = QuantumCircuit(qr)
    
    # Create Bell state |Φ⁺⟩ = (|00⟩ + |11⟩)/√2
    circuit.h(0)  # Apply Hadamard to first qubit
    circuit.cx(0, 1)  # CNOT with first qubit as control
    
    # Save the circuit diagram
    circuit.draw(output='mpl', 
                filename='pictures/superdense_coding/01_bell_pair_creation.png')
    
    # Save the state visualization
    state = Statevector.from_instruction(circuit)
    plot_bloch_multivector(state)
    plt.savefig('pictures/superdense_coding/02_bell_pair_state.png')
    
    return circuit

def alice_encode(circuit, message):
    """
    Alice encodes two classical bits using her qubit from the Bell pair.
    
    Encoding scheme:
    00 -> Do nothing (|Φ⁺⟩ = (|00⟩ + |11⟩)/√2)
    01 -> Apply X   (|Ψ⁺⟩ = (|01⟩ + |10⟩)/√2)
    10 -> Apply Z   (|Φ⁻⟩ = (|00⟩ - |11⟩)/√2)
    11 -> Apply ZX  (|Ψ⁻⟩ = (|01⟩ - |10⟩)/√2)
    """
    # Save initial state
    plot_bloch_multivector(Statevector.from_instruction(circuit))
    plt.savefig(f'pictures/superdense_coding/03_before_encoding_{message}.png')
    
    # Alice's operations
    if message == '01':
        circuit.x(0)  # Bit flip
    elif message == '10':
        circuit.z(0)  # Phase flip
    elif message == '11':
        circuit.z(0)  # Phase flip
        circuit.x(0)  # Bit flip
    
    # Save circuit after encoding
    circuit.draw(output='mpl', 
                filename=f'pictures/superdense_coding/04_alice_encoding_{message}.png')
    
    # Save state after encoding
    plot_bloch_multivector(Statevector.from_instruction(circuit))
    plt.savefig(f'pictures/superdense_coding/05_after_encoding_{message}.png')
    
    return circuit

def bob_decode(circuit):
    """
    Bob decodes the two classical bits using both qubits.
    He performs the reverse of Bell state creation to disentangle the qubits.
    """
    # Add classical bits for measurement
    cr = ClassicalRegister(2, 'c')
    circuit.add_register(cr)
    
    # Bob's decoding operations
    circuit.cx(0, 1)  # CNOT
    circuit.h(0)      # Hadamard
    
    # Save circuit after Bob's operations
    circuit.draw(output='mpl', 
                filename='pictures/superdense_coding/06_bob_decoding.png')
    
    # Measure both qubits
    circuit.measure([0, 1], [0, 1])
    
    # Save final circuit
    circuit.draw(output='mpl', 
                filename='pictures/superdense_coding/07_complete_circuit.png')
    
    return circuit

def simulate_superdense_coding(message):
    """
    Simulates the complete superdense coding protocol.
    
    Protocol steps:
    1. Create Bell pair
    2. Alice encodes 2 classical bits
    3. Bob decodes using both qubits
    4. Measure to retrieve the bits
    """
    # Initialize quantum simulator
    simulator = Aer.get_backend('qasm_simulator')
    
    # Create Bell pair
    circuit = create_bell_pair()
    
    # Alice encodes the message
    circuit = alice_encode(circuit, message)
    
    # Bob decodes and measures
    circuit = bob_decode(circuit)
    
    # Run the simulation
    job = simulator.run(circuit, shots=1000)
    result = job.result()
    counts = result.get_counts(circuit)
    
    # Create and save histogram
    plt.figure(figsize=(8, 6))
    plot_histogram(counts)
    plt.title(f'Measurement Results for Message: {message}')
    plt.savefig(f'pictures/superdense_coding/08_histogram_{message}.png')
    
    return counts

def visualize_eve_interference():
    """
    Creates visualizations demonstrating why Eve cannot intercept the message.
    """
    plt.figure(figsize=(10, 6))
    plt.subplot(121)
    plt.title("What Eve Sees\n(Mixed State)")
    plt.xticks([0, 1], ['|0⟩', '|1⟩'])
    plt.yticks([0, 0.5, 1], ['0', '0.5', '1'])
    plt.bar([0, 1], [0.5, 0.5])
    plt.ylim(0, 1)
    
    plt.subplot(122)
    plt.title("Actual Quantum State\n(Entangled State)")
    plt.xticks([0, 1], ['|00⟩ + |11⟩', '|01⟩ + |10⟩'])
    plt.yticks([0, 0.5, 1], ['0', '0.5', '1'])
    plt.bar([0], [1])
    plt.ylim(0, 1)
    
    plt.tight_layout()
    plt.savefig('pictures/superdense_coding/09_eve_interference.png')

def main():
    """
    Demonstrates superdense coding protocol with all possible 2-bit messages.
    """
    messages = ['00', '01', '10', '11']
    
    print("Superdense Coding Protocol Demonstration")
    print("---------------------------------------")
    print("\nProtocol Steps:")
    print("1. Alice and Bob share a Bell pair (quantum entanglement)")
    print("2. Alice performs quantum operations on her qubit to encode 2 classical bits")
    print("3. Alice sends her qubit to Bob")
    print("4. Bob performs quantum operations on both qubits to decode the message")
    print("\nSecurity Features:")
    print("- Eve cannot intercept the message without detection (no-cloning theorem)")
    print("- The message is encoded in quantum operations, not classical bits")
    print("- Prior entanglement provides quantum security\n")
    
    for msg in messages:
        print(f"\nTesting message: {msg}")
        counts = simulate_superdense_coding(msg)
        print(f"Measurement results: {counts}")
    
    # Create visualization of Eve's limitations
    visualize_eve_interference()
    print("\nVisualization of Eve's limitations saved as 'pictures/superdense_coding/09_eve_interference.png'")

if __name__ == "__main__":
    main()