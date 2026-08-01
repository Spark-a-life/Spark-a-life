from dataclasses import dataclass

@dataclass(frozen=True)
class RunResult:
    build_dir: str
    release_status: str
    quality_score: float
    witness_id: str
