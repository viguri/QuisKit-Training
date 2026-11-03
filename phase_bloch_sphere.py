from qiskit import QuantumCircuit
from qiskit.visualization import plot_bloch_multivector
from qiskit.visualization import plot_histogram
from qiskit_aer import Aer
from qiskit.quantum_info import Statevector
import matplotlib.pyplot as plt
import os
import math

# Create directories for images
os.makedirs('pictures/bloch_visualization', exist_ok=True)

def visualize_state(circuit, filename, title):
    """
    Visualizes a quantum state on the Bloch sphere and saves the image.
    """
    state = Statevector.from_instruction(circuit)
    plot_bloch_multivector(state)
    plt.title(title)
    plt.savefig(filename)
    plt.close()

def create_basis_states():
    """
    Creates and visualizes the computational basis states |0⟩ and |1⟩.
    """
    # |0⟩ state
    zero_circuit = QuantumCircuit(1)
    visualize_state(zero_circuit, 
                   'pictures/bloch_visualization/01_zero_state.png',
                   'Basis State |0⟩')

    # |1⟩ state
    one_circuit = QuantumCircuit(1)
    one_circuit.x(0)
    visualize_state(one_circuit, 
                   'pictures/bloch_visualization/02_one_state.png',
                   'Basis State |1⟩')

def create_superposition_states():
    """
    Creates and visualizes superposition states using Hadamard gate.
    """
    # |+⟩ state
    plus_circuit = QuantumCircuit(1)
    plus_circuit.h(0)
    visualize_state(plus_circuit, 
                   'pictures/bloch_visualization/03_plus_state.png',
                   'Superposition State |+⟩')

    # |-⟩ state
    minus_circuit = QuantumCircuit(1)
    minus_circuit.x(0)
    minus_circuit.h(0)
    visualize_state(minus_circuit, 
                   'pictures/bloch_visualization/04_minus_state.png',
                   'Superposition State |-⟩')

def create_phase_states():
    """
    Creates and visualizes states with different phases.
    """
    # Create circuit for phase rotation
    phase_circuit = QuantumCircuit(1)
    phase_circuit.h(0)

    # Visualize different phase rotations
    phases = [math.pi/4, math.pi/2, math.pi]
    for i, phase in enumerate(phases):
        phase_circuit_copy = phase_circuit.copy()
        phase_circuit_copy.p(phase, 0)
        visualize_state(phase_circuit_copy, 
                       f'pictures/bloch_visualization/05_phase_rotation_{i+1}.png',
                       f'Phase Rotation (φ = {phase/math.pi}π)')

def create_arbitrary_states():
    """
    Creates and visualizes arbitrary states using rotation gates.
    """
    # Create circuit for arbitrary state
    arb_circuit = QuantumCircuit(1)

    # Different combinations of rotations
    rotations = [
        (math.pi/4, 0, 0),      # Rx rotation
        (0, math.pi/4, 0),      # Ry rotation
        (math.pi/4, math.pi/4, 0)  # Combined rotation
    ]

    for i, (rx, ry, rz) in enumerate(rotations):
        arb_circuit_copy = arb_circuit.copy()
        if rx: arb_circuit_copy.rx(rx, 0)
        if ry: arb_circuit_copy.ry(ry, 0)
        if rz: arb_circuit_copy.rz(rz, 0)
        
        visualize_state(arb_circuit_copy, 
                       f'pictures/bloch_visualization/06_arbitrary_state_{i+1}.png',
                       f'Arbitrary State (Rx={rx/math.pi}π, Ry={ry/math.pi}π, Rz={rz/math.pi}π)')

def measure_states():
    """
    Demonstrates measurement of different states and creates histograms.
    """
    # States to measure
    states = {
        '|0⟩': QuantumCircuit(1),
        '|1⟩': QuantumCircuit(1),
        '|+⟩': QuantumCircuit(1),
        '|-⟩': QuantumCircuit(1)
    }
    
    # Add gates to create states
    states['|1⟩'].x(0)
    
    states['|+⟩'].h(0)
    
    # For |-⟩ state: first apply X, then H
    states['|-⟩'].x(0)
    states['|-⟩'].h(0)
    
    # Create new circuits with measurement capability
    for name, circuit in states.items():
        # Create a new circuit with measurement capability
        meas = QuantumCircuit(1, 1)
        # Copy operations from the original circuit
        meas = meas.compose(circuit)
        meas.barrier()
        meas.measure(0, 0)

        # Run measurements for each state
        
        # Run simulation
        simulator = Aer.get_backend('qasm_simulator')
        job = simulator.run(meas, shots=1000)
        job.wait_for_final_state()  # Ensure job completes
        counts = job.result().get_counts()

        print(f"Measurement results for {name}: {counts}")
        # Create histogram
        fig = plt.figure(figsize=(8, 6))
        plot_histogram(counts)
        plt.title(f'Measurement Results for State {name}')
        plt.savefig(f'pictures/bloch_visualization/07_measurement_{name.replace("|", "").replace("⟩", "")}.png')
        plt.close()

def main():
    """
    Creates a comprehensive visualization of quantum states on the Bloch sphere.
    """
    print("Creating Bloch sphere visualizations...")
    
    # Create and visualize different types of states
    create_basis_states()
    print("✓ Basis states visualized")
    
    create_superposition_states()
    print("✓ Superposition states visualized")
    
    create_phase_states()
    print("✓ Phase states visualized")
    
    create_arbitrary_states()
    print("✓ Arbitrary states visualized")
    
    measure_states()
    print("✓ Measurement results visualized")
    
    print("\nAll visualizations have been saved in 'pictures/bloch_visualization/'")
    print("\nVisualization categories:")
    print("1. Basis states (|0⟩, |1⟩)")
    print("2. Superposition states (|+⟩, |-⟩)")
    print("3. Phase rotations (π/4, π/2, π)")
    print("4. Arbitrary states (different rotation combinations)")
    print("5. Measurement results for various states")

if __name__ == "__main__":
    main()