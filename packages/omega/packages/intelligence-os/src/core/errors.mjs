export class GovernanceError extends Error { constructor(message, details={}) { super(message); this.name="GovernanceError"; this.details=details; } }
