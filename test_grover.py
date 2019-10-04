import grover

def test_aer_simulator():
    oracle = 3
    result = grover.search(4, oracle, "Aer", "qasm_simulator", None, 100, False)
    assert result == oracle

def test_ibmq_simulator():
    oracle = 3
    result = grover.search(4, oracle, "IBMQ", "ibmq_qasm_simulator", None, 100, False)
    assert result == oracle
