import os
import grover

token = os.environ.get('IBMQ_API_TOKEN')

def test_aer_simulator():
    oracle = 3
    result = grover.search(4, oracle, "Aer", "qasm_simulator", None, 100, False)
    assert result == oracle

def test_ibmq_simulator():
    oracle = 3
    result = grover.search(4, oracle, "IBMQ", "ibmq_qasm_simulator", token, 100, False)
    assert result == oracle
