# Grover's Quantum Search Algorithm Tool
# Requirements: Python 3 (https://www.python.org), Qiskit (https://qiskit.org)
# Github: https://github.com/ikhvorost/quantum-computing
# Copyright Iurii Khvorost <iurii.khvorost@gmail.com> 2019

import sys, getopt, math, time
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, execute, Aer, IBMQ
from qiskit.providers.jobstatus import JobStatus, JOB_FINAL_STATES

# Version
VERSION=1.0
print("Grover's Search Algorithm Tool v.{}".format(VERSION))

# Default params
N = 4
oracle = 3
provider_name = "Aer"
backend_name = "qasm_simulator"
shots = 10
draw = True

# Input params
if len(sys.argv):
    help =  "usage:\tpython3 grover-search-tool.py -n 128 -p IBMQ -b ibmq_qasm_simulator -s 100" \
            "\n-h, --help:\tPrint this help message and exit" \
            "\n-n, --number:\tNumber of items" \
            "\n-o, --oracle:\tOracle number" \
            "\n-p, --provider:\tProvider (Aer|IBMQ)" \
                "\n\tAer - Provides access to several simulators that are included with Qiskit and run on your local machine" \
                "\n\tIBMQ - implements access to cloud-based backends — simulators and real quantum devices — hosted on IBM Q" \
            "\n-b, --backend:\tBackend name" \
                "\n\tAer - qasm_simulator, qasm_simulator_py, statevector_simulator, statevector_simulator_py, unitary_simulator, clifford_simulator" \
                "\n\tIBMQ - ibmq_qasm_simulator, ibmq_16_melbourne, ibmq_ourense, ibmqx2, ibmq_vigo" \
            "\n-s, --shots:\tNumber of repetitions of a quantum circuit" \
            "\n-d, --draw:\tDraw a generated quantum circuit" \

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hn:o:p:b:s:d", ["help", "number=", "oracle=", "provider=", "backend=", "shots=", "draw"])
    except getopt.GetoptError:
        print(help)
        exit()

    if len(opts):
        draw = False

        for opt, arg in opts:
            if opt in ("-h", "--help"):
                print(help)
                exit()
            elif opt in ("-n", "--number"):
                N = int(arg)
            elif opt in ("-o", "--oracle"):
                oracle = int(arg)
            elif opt in ("-p", "--provider"):
                provider_name = arg
            elif opt in ("-b", "--backend"):
                backend_name = arg
            elif opt in ("-s", "--shots"):
                shots = int(arg)
            elif opt in ("-d", "--draw"):
                draw = True

        # Errors
        if oracle >= N:
            print("Error: Oracle is equal or greater than N!")
            exit()

print("Params: N = {}, Oracle = {}, Backend = {}/{}, Shots = {}".format(N, oracle, provider_name, backend_name, shots))

controlsCount = math.ceil(math.log2(N))
controls = QuantumRegister(controlsCount, "c_qb")

ancilla = QuantumRegister(1, "a_qb")
target = QuantumRegister(1, "t_qb")

classical = ClassicalRegister(controlsCount, "c_b")

iterations = int(math.pi / 4 * math.log2(N))

print("Quantum circuit: {} qubits, {} iteration(s)".format(controlsCount + 2, iterations))

print("Building...")

# Create a Quantum Circuit acting on the q register
circuit = QuantumCircuit(controls, ancilla, target, classical)

# State preparation

# Add a H gates to contol qubits
circuit.h(controls)

# |-> to target qubit
circuit.x(target)
circuit.h(target)

# Grover iterator
def grover(circuit, controls, target):
    # Oracle
    binary = format(oracle, "0{}b".format(controlsCount))

    for c, qubit in zip(binary, reversed(controls)):
        if c == '0':
            circuit.x(qubit)

    circuit.mct(controls, target[0], ancilla, mode='advanced')

    for c, qubit in zip(binary, reversed(controls)):
        if c == '0':
            circuit.x(qubit)

    # Diffuser
    circuit.h(controls)
    circuit.x(controls)
    circuit.mct(controls, target[0], ancilla, mode='advanced')
    circuit.x(controls)
    circuit.h(controls)

# Iterations
for i in range(iterations):
    grover(circuit, controls, target)

# Measurement
circuit.measure(controls, classical)

# Draw quantum circuit
if draw:
    print(circuit)

# Backend

# Aer
if provider_name == "Aer":
    backend = Aer.get_backend(backend_name)
# IBMQ
elif provider_name == "IBMQ":
    #IBMQ.save_account('MY_API_TOKEN')
    IBMQ.load_account()
    backend = IBMQ.get_provider().get_backend(backend_name)

# Execute the quantum circuit on the qasm simulator
print("Executing...")
job = execute(circuit, backend, shots=shots)

# Wait results
i = 0
while True:
    time.sleep(1)
    status = job.status()
    print("({}) {}".format(i, status))
    i = i + 1

    if status in JOB_FINAL_STATES:
        if status == JobStatus.ERROR:
            print("Error:", job.error_message())
            exit()
        else:
            break

# Get results from the job
result = job.result()
#print("\nResults:", result)

# Find max counts
max = 0
state = ""
for k, v in result.get_counts(circuit).items():
    if v > max:
        max = v
        state = k

print("Answer: {}, State: '{}', {} times".format(int(state, 2), state, max))
