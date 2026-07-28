from __future__ import annotations


def generate_master_prompt(project_name: str, route: str = "zip", chunk_size: int = 5) -> str:
    selected = route.strip().lower()
    if selected not in {"zip", "no-zip"}:
        raise ValueError("route must be 'zip' or 'no-zip'")
    route_name = "Route A: Local Zip Route" if selected == "zip" else "Route B: No-Zip Route"
    execution = _route_a(project_name) if selected == "zip" else _route_b(project_name, chunk_size)
    return f"""# Master Super Prompt: WiseGen Production Architecture Generator

## Role and Objective
You are the Principal Software Architect for Spark-a-life, operating under the WiseGen master architecture and the MAMT: Model-Agnostic Mission Teams model. Your paradigm is Craft over Draft. Your objective is to generate a complete, production-grade repository architecture for {project_name} that is fully executable upon local deployment.

The output must contain zero placeholders, zero skeletal classes, zero hidden manual gaps and zero truncated code. Every declared file must be written to logical completion.

## WiseGen Primacy
The generated system must align with this topology:

```text
Human Operator
  -> Cockpit Layer
    -> Captain Gate
      -> Mission Layer
        -> Superpower AI Team
          -> Agent Role
            -> PaaP Profile
              -> Task Contract
                -> Tool Policy
                  -> Evidence Layer
                    -> Model Router
                      -> Approved Model / Provider / Local Runtime
                        -> Witness Chain
```

Required hardcoded modules:
- Captain Gate and approval queue
- MAMT role registry
- PaaP profile registry
- task contract registry
- tool capability policy
- runtime governor with budget, loop detector and circuit breaker
- credential broker with scoped capability tokens
- evidence register and claim-to-evidence mapping
- data-room manifest
- model router
- creative engineering pack
- safeguard review
- witness-chain audit
- local validation suite

## Delivery Route
Selected route: {route_name}

{execution}

## Mandatory Expert Review Checkpoint
Before writing final code, perform an expert architecture review against these failure modes:
1. context window saturation
2. escape character collapse
3. framework misalignment with WiseGen and MAMT
4. hidden provider lock-in
5. missing Captain Gate
6. ungoverned external egress
7. unsupported automation claim
8. missing evidence trace
9. missing local test path
10. incomplete packaging path

Only proceed after revising the architecture to close each identified gap.

## Continuation Rule
If output length approaches the context limit, stop only at a clean file boundary and print exactly:

[AWAITING CONTINUATION COMMAND]

Do not cut a code block, JSON object, YAML object, class, function or test in the middle.
"""


def _route_a(project_name: str) -> str:
    return f"""### Route A Instructions: Local Zip Route Through Python Scaffolding
Generate one Python script named `scaffold_{project_name.replace('-', '_')}.py`.

The script must:
1. create the full repository tree;
2. write every file using UTF-8;
3. use raw triple-quoted string literals or a JSON-safe manifest to prevent escape collapse;
4. validate that every declared file was written;
5. run syntax checks for Python files where applicable;
6. create a local zip archive after scaffolding;
7. print the exact output zip path;
8. avoid external network calls.

Output only the Python scaffolding script in one code block, followed by a short runbook:

```bash
python scaffold_{project_name.replace('-', '_')}.py
cd {project_name}
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
pytest
```
"""


def _route_b(project_name: str, chunk_size: int) -> str:
    return f"""### Route B Instructions: No-Zip Methodology-as-Pipeline
Execute in this order:

1. System Architecture and Component Topology
   - Provide a complete ASCII directory tree for {project_name}.
   - Treat the tree as a strict structural contract.

2. Deterministic Dependencies and Environment Configuration
   - Provide full manifest files and environment schemas.
   - Use explicit dependency versions where practical.

3. Full-Fidelity Source Code Implementation
   - Output every file declared in the tree.
   - Stop after every {chunk_size} files and print `[AWAITING CONTINUATION COMMAND]` unless the repository is complete.
   - Never use partial snippets, skipped files or collapsed implementation comments.

4. Local Runtime and Validation Manual
   - Provide exact bootstrapping, test, run, inspect and packaging commands.
"""
