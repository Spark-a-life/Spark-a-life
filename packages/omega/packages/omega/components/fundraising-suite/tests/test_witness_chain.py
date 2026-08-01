from wisegen_mamt_fundraising.audit.witness_chain import WitnessChain


def test_witness_chain_verifies(tmp_path):
    path = tmp_path / "chain.jsonl"
    chain = WitnessChain(path)
    chain.append("a", {"value": 1})
    chain.append("b", {"value": 2})
    assert WitnessChain(path).verify() is True
