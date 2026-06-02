from circuit.neqr_circuit import create_circuit

from extract_message import extract_secret_message

from qiskit_aer import AerSimulator
from qiskit import transpile
from qiskit.visualization import plot_histogram

import matplotlib.pyplot as plt


# create circuit
qc = create_circuit()

# measure all qubits
qc.measure(range(4), range(4))

# simulator
simulator = AerSimulator()

# transpile
compiled_circuit = transpile(qc, simulator)

# run simulation
job = simulator.run(compiled_circuit, shots=1024)

# results
result = job.result()

counts = result.get_counts()

# print raw counts
print("\nMeasurement Results:\n")
print(counts)

# extract hidden message
message = extract_secret_message(counts)

print("\nRecovered Secret Message:\n")
print(message)

# draw circuit
print("\nCircuit:\n")
print(qc.draw())

# histogram
# -----------------------------------
# SAVE CIRCUIT DIAGRAM


figure = qc.draw(output='mpl')

figure.savefig("output/quantum_circuit.png")


# -----------------------------------
# SAVE HISTOGRAM
# -----------------------------------

histogram = plot_histogram(counts)

histogram.savefig("output/histogram.png")


# show plots
plt.show()