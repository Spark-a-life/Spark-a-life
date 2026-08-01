# WiseGen APE Intelligence OS

**Release:** v0.1.0  
**Status:** Canonical executable baseline  
**Owner:** Spark-a-life  
**Design rule:** One OS, multiple estates, many runtimes, replaceable models, governed capabilities, one accountable evidence chain.

WiseGen APE Intelligence OS is a governance-native operating architecture for coordinating human judgement, artificial intelligence, organisational knowledge, agent execution and accountable decision-making.

Hermes Agent, OpenClaw, Claude Code, Codex, Gemini and future frameworks are treated as bounded execution substrates. They do not own system-wide authority, governance policy, canonical knowledge, certification or accountability.

## Included

- Constitutional principles and non-delegable decisions
- Five intelligence estates: MAIE, TAIE, PAIE, GAIE and SAIE
- Nine Full Intentionality by Design lanes
- Captain's Gate policy decision point
- Governed capability registry and lifecycle controls
- Runtime adapter contract with a deterministic local runtime
- Disabled Hermes Agent adapter boundary
- Append-only hash-linked Witness Chain
- Knowledge promotion controls
- Deterministic orchestration engine
- JSON Schemas
- Threat model, security controls and operating runbook
- Automated tests, CI workflow, Dockerfile and Compose file
- Release manifest and checksums

## Requirements

- Node.js 20 or newer
- No npm dependencies
- Docker is optional

## Run

### Linux, WSL2 or macOS

```bash
chmod +x bin/wisegen
./bin/wisegen verify
./bin/wisegen demo
./bin/wisegen test
```

### Windows PowerShell

```powershell
.in\wisegen.ps1 verify
.in\wisegen.ps1 demo
.in\wisegen.ps1 test
```

### Directly

```bash
node src/cli.mjs verify
node src/cli.mjs demo
node --test
```

## Commands

```text
help                       Show usage
demo                       Run a governed TAIE demonstration workflow
verify                     Verify configuration and Witness Chain integrity
test                       Run the complete test suite
gate <request.json>        Evaluate an action through Captain's Gate
run <request.json> <task.json>
                           Execute a governed task
registry                   List capabilities
estates                    List intelligence estates
lanes                      List Full Intentionality by Design lanes
witness                    Show Witness Chain verification summary
reset                      Remove local demonstration evidence
```

## Trust boundary

The baseline is deliberately local and deterministic. It does not make network calls, invoke external models or permit external side effects. Any external runtime must be separately implemented, evaluated, certified and enabled through policy.

## Licence

Apache-2.0.
