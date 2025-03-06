# Qiskit Training Project

## Project Purpose
This project serves as a comprehensive quantum computing training resource using IBM's Qiskit framework. It implements various fundamental quantum algorithms and protocols, providing practical examples and visualizations to help understand quantum computing concepts.

## Overview
The project includes implementations of several key quantum algorithms and protocols:
- Deutsch's Algorithm
- Bernstein-Vazirani Algorithm
- Bell State Generation
- Quantum Teleportation
- Superdense Coding
- Shor's Algorithm
- Phase Visualization on Bloch Sphere
- Quantum Search Algorithms

Each implementation includes detailed visualizations and step-by-step explanations to aid in understanding the quantum mechanics principles involved.

## Features
- **Multiple Quantum Algorithms**: Complete implementations of fundamental quantum algorithms
- **Enhanced Visualization**: 
  - Circuit diagrams
  - State evolution visualization
  - Measurement histograms
  - Bloch sphere representations
- **Hardware Integration**: Support for running circuits on IBM Quantum hardware
- **Detailed Documentation**: Each algorithm includes comprehensive documentation and explanations
- **Educational Tools**: Step-by-step visualization of quantum state evolution

## Requirements
- Python 3.7 or higher
- Qiskit
- Qiskit Aer (for simulation)
- Qiskit IBM Provider (for hardware access)
- Matplotlib (for visualization)
- python-dotenv (for environment configuration)

You can install the required packages using pip:

```bash
pip install qiskit qiskit-aer qiskit-ibm-provider matplotlib python-dotenv
```

## Installation Instructions
1. Ensure you have Python 3.7 or higher installed on your system.
2. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/Qiskit-Training.git
   ```
3. Navigate to the project directory:
   ```bash
   cd Qiskit-Training
   ```
4. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
5. Create a .env file in the root directory and add your IBM Quantum API key:
   ```
   IBMQ_KEY=your_api_key_here
   ```

## Available Implementations

### 1. Deutsch's Algorithm (`deutsch_algorithm.py`)
- Implementation of the Deutsch-Jozsa algorithm
- Includes circuit visualization and histogram results
- Supports both simulator and real quantum hardware execution

### 2. Bernstein-Vazirani Algorithm (`bernstein_vazirani.py`)
- Discovers a hidden binary string in a single query
- Demonstrates quantum parallelism
- Includes detailed visualization of circuit evolution

### 3. Bell State Generation (`first_circuit.py`)
- Creates and measures Bell states
- Demonstrates quantum entanglement
- Includes histograms of measurement results

### 4. Quantum Teleportation (`teleportation.py`)
- Implements quantum teleportation protocol
- Visualizes state transfer process
- Includes verification of successful teleportation

### 5. Superdense Coding (`superdense_coding.py`)
- Demonstrates quantum data transmission
- Includes visualization of encoding and decoding steps
- Shows practical application of quantum entanglement

## Running the Examples
Each implementation can be run independently. For example:

```bash
python deutsch_algorithm.py
python bernstein_vazirani.py
python teleportation.py
```

The scripts will:
1. Create and display the quantum circuits
2. Run simulations and/or hardware executions
3. Generate visualizations in the `pictures/` directory
4. Display measurement results and explanations

## Understanding the Results
Each implementation generates various visualization files in the `pictures/` directory:
- Circuit diagrams showing gate arrangements
- State evolution visualizations
- Measurement histograms
- Bloch sphere representations (where applicable)

These visualizations help in understanding:
- Quantum circuit construction
- State evolution through the algorithm
- Final measurement results and their interpretation

## Usage Guidelines
To use this project effectively:
- Start with simple examples (Bell states, teleportation)
- Progress to more complex algorithms (Deutsch, Bernstein-Vazirani)
- Examine the generated visualizations to understand each step
- Experiment with different input states and parameters
- Compare simulator results with hardware execution results

## Contribution Guidelines
We welcome contributions to this project! To contribute:
1. Fork the repository
2. Create a new branch for your feature
3. Add your implementation or improvement
4. Ensure proper documentation and visualization
5. Submit a pull request with a clear description of changes

## Further Reading
- [IBM Qiskit Documentation](https://qiskit.org/documentation/)
- [Quantum Computing Concepts](https://qiskit.org/textbook/what-is-quantum.html)
- [IBM Quantum Experience](https://quantum-computing.ibm.com/)