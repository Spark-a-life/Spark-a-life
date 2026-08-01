from difflib import SequenceMatcher

class LoopDetector:
    def __init__(self, max_similar: int = 3, similarity_threshold: float = 0.92):
        self.max_similar = max_similar
        self.similarity_threshold = similarity_threshold
        self._history: list[str] = []

    def observe(self, action_signature: str) -> bool:
        self._history.append(action_signature)
        if len(self._history) < self.max_similar:
            return False
        recent = self._history[-self.max_similar:]
        first = recent[0]
        return all(SequenceMatcher(None, first, item).ratio() >= self.similarity_threshold for item in recent[1:])
