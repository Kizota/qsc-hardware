from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

# Step 1: Create a quantum circuit with 2 qubits and 2 classical bits
qc = QuantumCircuit(2, 2)

# Apply Hadamard gate to qubit 0
# This puts qubit 0 into a superposition
qc.h(0)

# Apply CNOT gate
# Control: qubit 0, Target: qubit 1
# creat3 entanglement between the two qubits
qc.cx(0, 1)

# Step 4: Measure both qubits
qc.measure([0, 1], [0, 1])

# Display the circuit
print(qc)

# Step 5: Run the circuit on the Aer simulator
sim = Aer.get_backend('aer_simulator')
compiled = transpile(qc, sim)
result = sim.run(compiled, shots=1024).result()

#draw the circuit 
qc.draw('mpl')
plt.show()

# Step 6: Get and plot results
counts = result.get_counts()
plot_histogram(counts)

