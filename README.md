# Quantum Computing

## Grover Search Tool 
[![Build Status](https://travis-ci.org/ikhvorost/quantum-computing.svg?branch=master)](https://travis-ci.org/ikhvorost/quantum-computing)

It's a command line tool that implements [Grover's algorithm](https://en.wikipedia.org/wiki/Grover%27s_algorithm) of quantum search. The script is written on [python](https://www.python.org/) and uses [Qiskit](https://qiskit.org/). Many params allow to test the algorithm with various values and to run on different backends such as a local simulators or cloud [IBMQ](https://quantum-computing.ibm.com) quantum processors.

**Usage Help:**
```console
$ python3 grover.py --help
usage:	python3 grover.py -n 128 -p IBMQ -b ibmq_qasm_simulator -s 100
-h, --help:	Print this help message and exit
-n, --number:	Number of items
-o, --oracle:	Oracle number
-p, --provider:	Provider (Aer|IBMQ)
	Aer - Provides access to several simulators that are included with Qiskit and run on your local machine
	IBMQ - implements access to cloud-based backends — simulators and real quantum devices — hosted on IBMQ
-b, --backend:	Backend name
	Aer - qasm_simulator, qasm_simulator_py, statevector_simulator, statevector_simulator_py, unitary_simulator, clifford_simulator
	IBMQ - ibmq_qasm_simulator, ibmq_16_melbourne, ibmq_ourense, ibmqx2, ibmq_vigo
-t, --token:	IBMQ API token
-s, --shots:	Number of repetitions of a quantum circuit
-d, --draw:	Draw a generated quantum circuit to the console or a file
```

**Run with default params:**
```console
$ python3 grover.py
Grover's Search Algorithm Tool v.1.1
Params: N = 4, Oracle = 3, Backend = Aer/qasm_simulator, Shots = 10
Quantum circuit: 4 qubits, 1 iteration(s)
Building...
           ┌───┐          ┌───┐┌───┐     ┌───┐┌───┐┌─┐   
c_qb_0: |0>┤ H ├───────■──┤ H ├┤ X ├──■──┤ X ├┤ H ├┤M├───
           ├───┤       │  ├───┤├───┤  │  ├───┤├───┤└╥┘┌─┐
c_qb_1: |0>┤ H ├───────■──┤ H ├┤ X ├──■──┤ X ├┤ H ├─╫─┤M├
           └───┘       │  └───┘└───┘  │  └───┘└───┘ ║ └╥┘
a_qb_0: |0>────────────┼──────────────┼─────────────╫──╫─
           ┌───┐┌───┐┌─┴─┐          ┌─┴─┐           ║  ║
t_qb_0: |0>┤ X ├┤ H ├┤ X ├──────────┤ X ├───────────╫──╫─
           └───┘└───┘└───┘          └───┘           ║  ║
  c_b_0: 0 ═════════════════════════════════════════╩══╬═
                                                       ║
  c_b_1: 0 ════════════════════════════════════════════╩═

Executing...
(0) JobStatus.DONE
Answer: 3, State: '11', 10 times
```

**Run on a IBMQ cloud backend:**
```console
$ python3 grover.py -n 4 -o 3 -p IBMQ -b ibmq_vigo -t <YOUR_API_TOKEN> -s 100
Grover's Search Algorithm Tool v.1.1
Params: N = 4, Oracle = 3, Backend = IBMQ/ibmq_vigo, Shots = 100
Quantum circuit: 4 qubits, 1 iteration(s)
Building...
Executing...
(0) JobStatus.INITIALIZING
(2) JobStatus.VALIDATING
(3) JobStatus.QUEUED
(50) JobStatus.RUNNING
(57) JobStatus.DONE
Answer: 3, State: '11', 52 times
```
