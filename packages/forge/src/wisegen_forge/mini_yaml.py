"""Zero-dependency YAML subset loader.

Portability contract: WiseGen Forge must run on a bare Python 3.10+ interpreter
with no wheels available (air-gapped estates, locked-down customer VPCs).
If PyYAML is present we defer to it; otherwise this parser handles the subset
used by every policy, registry and workflow file shipped in this repository:

  * nested block mappings (indentation based)
  * block sequences of scalars and of mappings
  * scalars: str, int, float, bool, null
  * single and double quoted strings
  * full-line and trailing comments
  * inline flow lists  [a, b, c]

Anything outside that subset is rejected loudly rather than silently mis-parsed.
"""
from __future__ import annotations

from typing import Any

try:  # pragma: no cover - environment dependent
    import yaml as _pyyaml
except Exception:  # pragma: no cover
    _pyyaml = None


class YamlSubsetError(ValueError):
    """Raised when a document uses constructs outside the supported subset."""


def _scalar(raw: str) -> Any:
    text = raw.strip()
    if text == "" or text in ("null", "~", "None"):
        return None
    if len(text) >= 2 and text[0] == text[-1] and text[0] in ("'", '"'):
        return text[1:-1]
    low = text.lower()
    if low in ("true", "yes", "on"):
        return True
    if low in ("false", "no", "off"):
        return False
    if text.startswith("[") and text.endswith("]"):
        inner = text[1:-1].strip()
        if not inner:
            return []
        return [_scalar(part) for part in inner.split(",")]
    try:
        return int(text)
    except ValueError:
        pass
    try:
        return float(text)
    except ValueError:
        pass
    return text


def _strip_comment(line: str) -> str:
    out: list[str] = []
    quote: str | None = None
    for index, char in enumerate(line):
        if quote:
            out.append(char)
            if char == quote:
                quote = None
            continue
        if char in ("'", '"'):
            quote = char
            out.append(char)
            continue
        if char == "#" and (index == 0 or line[index - 1] in (" ", "\t")):
            break
        out.append(char)
    return "".join(out).rstrip()


def _lines(text: str) -> list[tuple[int, str]]:
    rows: list[tuple[int, str]] = []
    for raw in text.splitlines():
        if "\t" in raw.split("#")[0]:
            raise YamlSubsetError("tab indentation is not supported")
        stripped = _strip_comment(raw)
        if not stripped.strip():
            continue
        if stripped.strip() in ("---", "..."):
            continue
        indent = len(stripped) - len(stripped.lstrip(" "))
        rows.append((indent, stripped.strip()))
    return rows


def _split_key(item: str) -> tuple[str, str] | None:
    quote: str | None = None
    for index, char in enumerate(item):
        if quote:
            if char == quote:
                quote = None
            continue
        if char in ("'", '"'):
            quote = char
            continue
        if char == ":" and (index + 1 == len(item) or item[index + 1] == " "):
            return item[:index].strip().strip("'\""), item[index + 1 :].strip()
    return None


def _parse_block(rows: list[tuple[int, str]], start: int, indent: int) -> tuple[Any, int]:
    if start >= len(rows):
        return None, start
    if rows[start][1].startswith("- "):
        return _parse_sequence(rows, start, indent)
    return _parse_mapping(rows, start, indent)


def _parse_sequence(rows: list[tuple[int, str]], start: int, indent: int) -> tuple[list, int]:
    items: list[Any] = []
    cursor = start
    while cursor < len(rows):
        row_indent, content = rows[cursor]
        if row_indent < indent or not content.startswith("- "):
            break
        body = content[2:].strip()
        cursor += 1
        pair = _split_key(body)
        if pair is None:
            items.append(_scalar(body))
            continue
        key, value = pair
        entry: dict[str, Any] = {}
        if value:
            entry[key] = _scalar(value)
        else:
            child, cursor = _parse_block(rows, cursor, row_indent + 2)
            entry[key] = child
        while cursor < len(rows) and rows[cursor][0] > row_indent:
            nested_indent, nested = rows[cursor]
            if nested.startswith("- "):
                break
            nested_pair = _split_key(nested)
            if nested_pair is None:
                raise YamlSubsetError(f"unsupported sequence member: {nested!r}")
            nested_key, nested_value = nested_pair
            cursor += 1
            if nested_value:
                entry[nested_key] = _scalar(nested_value)
            else:
                child, cursor = _parse_block(rows, cursor, nested_indent + 1)
                entry[nested_key] = child
        items.append(entry)
    return items, cursor


def _parse_mapping(rows: list[tuple[int, str]], start: int, indent: int) -> tuple[dict, int]:
    mapping: dict[str, Any] = {}
    cursor = start
    while cursor < len(rows):
        row_indent, content = rows[cursor]
        if row_indent < indent:
            break
        if content.startswith("- "):
            break
        pair = _split_key(content)
        if pair is None:
            raise YamlSubsetError(f"unsupported line: {content!r}")
        key, value = pair
        cursor += 1
        if value:
            mapping[key] = _scalar(value)
            continue
        if cursor < len(rows) and rows[cursor][0] > row_indent:
            child, cursor = _parse_block(rows, cursor, rows[cursor][0])
            mapping[key] = child
        elif cursor < len(rows) and rows[cursor][0] == row_indent and rows[cursor][1].startswith("- "):
            child, cursor = _parse_sequence(rows, cursor, row_indent)
            mapping[key] = child
        else:
            mapping[key] = None
    return mapping, cursor


def loads(text: str) -> Any:
    """Parse a YAML document, preferring PyYAML when it is installed."""
    if _pyyaml is not None:  # pragma: no cover - environment dependent
        return _pyyaml.safe_load(text)
    rows = _lines(text)
    if not rows:
        return {}
    value, _ = _parse_block(rows, 0, rows[0][0])
    return value


def load_file(path) -> Any:
    from pathlib import Path

    return loads(Path(path).read_text(encoding="utf-8"))


def dumps(data: Any, indent: int = 0) -> str:
    """Emit the same subset. Deterministic key order, stable for diffing."""
    pad = " " * indent
    if isinstance(data, dict):
        if not data:
            return pad + "{}\n"
        out = []
        for key, value in data.items():
            if isinstance(value, (dict, list)) and value:
                out.append(f"{pad}{key}:\n{dumps(value, indent + 2)}")
            elif isinstance(value, (dict, list)):
                out.append(f"{pad}{key}: {'{}' if isinstance(value, dict) else '[]'}\n")
            else:
                out.append(f"{pad}{key}: {_emit_scalar(value)}\n")
        return "".join(out)
    if isinstance(data, list):
        out = []
        for item in data:
            if isinstance(item, dict):
                body = dumps(item, indent + 2)
                first, _, rest = body.partition("\n")
                out.append(f"{pad}- {first.strip()}\n")
                if rest.strip():
                    out.append(rest if rest.endswith("\n") else rest + "\n")
            else:
                out.append(f"{pad}- {_emit_scalar(item)}\n")
        return "".join(out)
    return f"{pad}{_emit_scalar(data)}\n"


def _emit_scalar(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    text = str(value)
    if text == "" or any(ch in text for ch in ":#") or text.strip() != text:
        return '"' + text.replace('"', '\\"') + '"'
    return text
