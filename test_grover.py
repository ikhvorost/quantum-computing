import grover

def test_grover_aer_simulator():
    oracle = 3
    result = grover.search(4, oracle, "Aer", "qasm_simulator", 100, False)
    assert result == oracle

#def test_grover_ibmq_simulator():
#    oracle = 3
#    result = grover.search(4, oracle, "IBMQ", "ibmq_qasm_simulator", 100, False)
#    assert result == oracle