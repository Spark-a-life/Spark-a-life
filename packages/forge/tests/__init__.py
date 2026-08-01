"""Test package bootstrap.

Puts ``src`` on the import path so the suite runs identically from an IDE,
from ``make test`` and from CI, with or without an editable install.
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SRC = REPO_ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

EXAMPLES = REPO_ROOT / "examples" / "employee-onboarding"
POLICIES = REPO_ROOT / "policies"
AGENTS = REPO_ROOT / "agents" / "registry.yaml"
