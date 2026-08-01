from wisegen_mamt_fundraising.prompting.master_prompt import generate_master_prompt


def test_prompt_generator_contains_routes_and_chunking():
    prompt = generate_master_prompt("demo-project", "no-zip", 5)
    assert "Route B" in prompt
    assert "Stop after every 5 files" in prompt
    assert "Mandatory Expert Review Checkpoint" in prompt


def test_zip_prompt_prefers_python_scaffold():
    prompt = generate_master_prompt("demo-project", "zip")
    assert "Python scaffolding" in prompt
    assert "create a local zip archive" in prompt
