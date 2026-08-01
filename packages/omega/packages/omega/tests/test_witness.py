from wisegen_omega.witness import WitnessChain, verify

def test_chain(tmp_path):
    p=tmp_path/"audit.jsonl"; w=WitnessChain(p); w.append("m","A","x",{}); w.append("m","B","x",{})
    assert verify(p)==(True,2)
