import matplotlib.pyplot as plt
import numpy as np
from qiskit import QuantumCircuit, Aer, transpile
from qiskit.utils.classtools import *  # Assuming we want to import everything from classtools
from qiskit_aer import AerSimulator
from qiskit import Shor
from qiskit.visualization import plot_histogram
from math import gcd
from numpy.random import randint
from fractions import Fraction
from dotenv import load_dotenv
import os
import logging
print("Imports Successful")


# Set up the quantum instance
quantum_instance = QuantumInstance(AerSimulator())

# Create the Shor instance
shor = Shor()

# Run the Shor algorithm
result = shor.factor(N=15, a=7, quantum_instance=quantum_instance)

# Print the factors
print(result.factors)