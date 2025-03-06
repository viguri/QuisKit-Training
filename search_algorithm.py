import qiskit 
from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
from qiskit_ibm_runtime import QiskitRuntimeService, Sampler
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt
from dotenv import load_dotenv

# classical search algorithm
myList = [5,4,6,9,1,2,3,7,8,0]

def oracle(number):
    winningNumber = 8
    if number == winningNumber:
        return True
    else:
        return False

for index, number in enumerate(myList):
    if oracle(number):
        print(f"Winner found at index {index}")
        print(f"execution count: {index + 1}")
        break

# quantum search algorithm, Grover's Algortihm
oracleCircuit = QuantumCircuit(2, name = "oracleCircuit")
oracleCircuit.cz(0, 1)
oracleGate = oracleCircuit.to_gate(label="Oracle")
oracleCircuit.draw(output='mpl', filename="pictures/grovers/oracleCircuit.png")

mainCircuit = QuantumCircuit(2, 2)
mainCircuit.h([0, 1])
mainCircuit.append(oracleGate, [0, 1])
mainCircuit.barrier()
mainCircuit.draw(output='mpl', filename="pictures/grovers/mainCircuit.png")

reflectionircuit = QuantumCircuit(2, name="reflectionCircuit")
reflectionircuit.h([0, 1])
reflectionircuit.z([0, 1])
reflectionircuit.cz(0, 1)
reflectionircuit.h([0, 1])
reflectionGate = reflectionircuit.to_gate(label="Reflection")
reflectionircuit.draw(output='mpl', filename="pictures/grovers/reflectionCircuit.png")  

mainCircuit.append(reflectionGate, [0, 1])
mainCircuit.measure([0, 1], [0, 1])
mainCircuit.draw(output='mpl', filename="pictures/grovers/groversCircuit.png")

simulator = Aer.get_backend('qasm_simulator')
result = simulator.run(transpile(mainCircuit, simulator), shots=1).result()
counts = result.get_counts(mainCircuit)

plot_histogram(counts)
plt.savefig('pictures/grovers/grovers_histogram.png')
plt.close()