#!/usr/bin/env python3
import importlib.util, sys
required=['yaml','jsonschema','jinja2','pytest']
missing=[m for m in required if importlib.util.find_spec(m) is None]
if missing:
    print('Missing Python modules: '+', '.join(missing), file=sys.stderr)
    print('Install project dependencies from packages/omega/pyproject.toml and pytest.', file=sys.stderr)
    raise SystemExit(1)
print('Python dependencies available: '+', '.join(required))
