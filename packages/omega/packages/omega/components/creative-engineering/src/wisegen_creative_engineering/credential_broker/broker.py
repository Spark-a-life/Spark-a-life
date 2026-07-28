from .capability_token import CapabilityToken, issue_token

class CredentialBroker:
    def __init__(self, tool_policy: dict[str, list[str]] | None = None):
        self.tool_policy = tool_policy or {}
        self.issued: list[CapabilityToken] = []

    def request(self, subject: str, tool: str, scope: list[str]) -> CapabilityToken:
        allowed = self.tool_policy.get(tool, scope)
        if not set(scope).issubset(set(allowed)):
            raise PermissionError(f"Requested scope {scope} exceeds allowed scope for {tool}: {allowed}")
        token = issue_token(subject, tool, scope)
        self.issued.append(token)
        return token

    def revoke_all(self) -> int:
        count = len(self.issued)
        self.issued.clear()
        return count
