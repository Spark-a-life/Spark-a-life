from wisegen_creative_engineering.io import load_yaml
from wisegen_creative_engineering.contracts import validate_contract, parse_brief


def test_example_contract_valid():
    data = load_yaml('examples/briefs/linkedin_social_creative.yaml')
    assert validate_contract(data) == []
    brief = parse_brief(data)
    assert brief.output.adapter == 'muse_manual'
