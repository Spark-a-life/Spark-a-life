from pathlib import Path
import json
import yaml


def load_data(path: str | Path):
    p = Path(path)
    text = p.read_text(encoding="utf-8")
    return json.loads(text) if p.suffix.lower() == ".json" else yaml.safe_load(text)


def write_json(path: str | Path, data):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(
        json.dumps(data, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )
