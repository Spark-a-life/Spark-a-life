# Interoperability

Canonical input is YAML or JSON conforming to `schemas/project.schema.json`.

Every adapter implements:

```python
generate(stage: str, context: dict) -> dict
```

Canonical outputs are Markdown and JSON. Provider-specific formats must remain behind adapters.
