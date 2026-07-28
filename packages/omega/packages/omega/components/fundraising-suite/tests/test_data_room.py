from wisegen_mamt_fundraising.contracts import load_brief
from wisegen_mamt_fundraising.fundraising.data_room import data_room_checklist


def test_data_room_sections_are_present():
    brief = load_brief("examples/missions/fundraising_500k_programme.yaml")
    checklist = data_room_checklist(brief)
    sections = {item["section"] for item in checklist["sections"]}
    assert "Impact Evidence" in sections
    assert "Financials and Budget" in sections
