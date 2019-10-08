# Grover's Quantum Search Algorithm Tool
# Requirements: Python 3 (https://www.python.org), Qiskit (https://qiskit.org)
# Github: https://github.com/ikhvorost/quantum-computing
# Copyright Iurii Khvorost <iurii.khvorost@gmail.com> 2019

import sys, getopt, math, time
from collections import namedtuple
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, execute, Aer, IBMQ
from qiskit.providers.jobstatus import JobStatus, JOB_FINAL_STATES

# Version
__version__ = "1.1"

def params():
    # Default params
    N = 4
    oracle = 3
    provider_name = "Aer"
    backend_name = "qasm_simulator"
    token = None
    shots = 10
    draw = True
    file = None

    # Input params
    if len(sys.argv):
        help =  "usage:\tpython3 grover.py -n 128 -p IBMQ -b ibmq_qasm_simulator -s 100" \
                "\n-h, --help:\tPrint this help message and exit" \
                "\n-n, --number:\tNumber of items" \
                "\n-o, --oracle:\tOracle number" \
                "\n-p, --provider:\tProvider (Aer|IBMQ)" \
                    "\n\tAer - Provides access to several simulators that are included with Qiskit and run on your local machine" \
                    "\n\tIBMQ - implements access to cloud-based backends — simulators and real quantum devices — hosted on IBMQ" \
                "\n-b, --backend:\tBackend name" \
                    "\n\tAer - qasm_simulator, qasm_simulator_py, statevector_simulator, statevector_simulator_py, unitary_simulator, clifford_simulator" \
                    "\n\tIBMQ - ibmq_qasm_simulator, ibmq_16_melbourne, ibmq_ourense, ibmqx2, ibmq_vigo" \
                "\n-t, --token:\tIBMQ API token" \
                "\n-s, --shots:\tNumber of repetitions of a quantum circuit" \
                "\n-d, --draw:\tDraw a generated quantum circuit to the console or a file"

        try:
            opts, args = getopt.getopt(sys.argv[1:], "hn:o:p:b:t:s:d:", ["help", "number=", "oracle=", "provider=", "backend=", "token=", "shots=", "draw="])
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
                elif opt in ("-t", "--token"):
                    token = arg
                elif opt in ("-s", "--shots"):
                    shots = int(arg)
                elif opt in ("-d", "--draw"):
                    draw = True
                    file = arg

            # Errors
            if oracle >= N:
                print("Error: Oracle is equal or greater than N!")
                exit()

    Params = namedtuple('Params', 'N oracle provider_name backend_name token shots draw file')
    return Params(N, oracle, provider_name, backend_name, token, shots, draw, file)

def search(N, oracle, provider_name, backend_name, token, shots, draw, file):
    print("Grover's Search Algorithm Tool v.{}".format(__version__))
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
        if bool(file):
            f = open(file, "w+")
            print(circuit, file=f)
            f.close()
        else:
            print(circuit)

    # Backend

    # Aer
    if provider_name == "Aer":
        backend = Aer.get_backend(backend_name)
    # IBMQ
    elif provider_name == "IBMQ":
        account = IBMQ.stored_account()
        if bool(account):
            provider = IBMQ.load_account()
        else:
            if bool(token):
                provider = IBMQ.enable_account(token)
            else:
                print("Token is not provided!")
                exit()
        backend = provider.get_backend(backend_name)

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

    num = int(state, 2)
    print("Answer: {}, State: '{}', {} times".format(num, state, max))
    return num

if __name__ == "__main__":
    params = params()
    search(params.N, params.oracle, params.provider_name, params.backend_name, params.token, params.shots, params.draw, params.file)
