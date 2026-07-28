# MCP connector

Model Context Protocol client and server support is defined and deferred. The design position, so it is not reinvented later:

- An MCP server is an external system. It goes through the tool gateway like any other, with its own connector contract and classification ceiling.
- MCP tool descriptions are untrusted input. A description that instructs the model is a prompt injection vector, and is treated as data.
- Tool poisoning is assumed. Tool identity is pinned by digest, and a changed tool definition requires re-approval rather than silent adoption.
- Every MCP invocation is witnessed with the server identity, the tool name and a request digest.

Activation criterion: a named engagement requires an MCP-exposed system the customer already operates.
