from .adapters.muse_manual import MuseManualAdapter
from .adapters.local_deterministic import LocalDeterministicAdapter
from .adapters.base import Adapter

ADAPTERS: dict[str, type[Adapter]] = {
    'muse_manual': MuseManualAdapter,
    'local_deterministic': LocalDeterministicAdapter,
}

def get_adapter(name: str) -> Adapter:
    try:
        return ADAPTERS[name]()
    except KeyError as exc:
        raise ValueError(f"Unknown adapter '{name}'. Available: {', '.join(sorted(ADAPTERS))}") from exc
