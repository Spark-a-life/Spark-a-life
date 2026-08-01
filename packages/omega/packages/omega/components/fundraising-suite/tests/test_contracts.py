from wisegen_mamt_fundraising.contracts import load_brief


def test_example_contract_loads():
    brief = load_brief("examples/missions/fundraising_500k_programme.yaml")
    assert brief.mission.id == "fundraise-programme-expansion-500k"
    assert brief.risk.maximum_external_calls == 0
