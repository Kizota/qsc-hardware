import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

# create Bell-test circuit (entanglement + measurement)
def bell_test_circuit(alice_basis, bob_basis):
    qc = QuantumCircuit(2, 2)

    # Create entanglement
    qc.h(0)      # Hadamard on Alice's qubit
    qc.cx(0, 1)  # CNOT to entangle qubits

    # Alice measurement basis
    if alice_basis.upper() == 'X':
        qc.h(0)

    # Bob measurement basis
    if bob_basis == 'Z+X':
        qc.ry(-np.pi/4, 1)
    elif bob_basis == 'Z-X':
        qc.ry(np.pi/4, 1)

    # Measurement
    qc.measure(0, 0)
    qc.measure(1, 1)

    return qc

# Correlation calculation
def correlation(counts, shots):
    return (
        counts.get("00", 0) + counts.get("11", 0)
        - counts.get("01", 0) - counts.get("10", 0)
    ) / shots

# Run Bell (CHSH) test
sim = Aer.get_backend('aer_simulator')
shots = 5000

settings = [
    ('Z', 'Z+X'),   # A0, B0
    ('Z', 'Z-X'),   # A0, B1
    ('X', 'Z+X'),   # A1, B0
    ('X', 'Z-X')    # A1, B1
]

E = []

for a, b in settings:
    qc = bell_test_circuit(a, b)
   
    compiled = transpile(qc, sim)
    result = sim.run(compiled, shots=shots).result()
    counts = result.get_counts()
    E.append(correlation(counts, shots))

    #draw the circuit
    print("draw the circuit")
    qc.draw('mpl')
    plt.show()
   
# Compute CHSH Bell parameter
S = E[0] + E[1] + E[2] - E[3]

print("Correlation values E:", E)
print("CHSH Bell parameter S =", S)
