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
    
