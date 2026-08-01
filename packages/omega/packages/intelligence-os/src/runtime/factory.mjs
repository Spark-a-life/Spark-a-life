import { LocalDeterministicRuntime } from "./local-deterministic.mjs";
import { HermesAgentAdapter } from "./hermes-agent.mjs";
export function createRuntime(definition){if(definition.id==="local-deterministic") return new LocalDeterministicRuntime(definition); if(definition.id==="hermes-agent") return new HermesAgentAdapter(definition); throw new Error(`Unsupported runtime adapter: ${definition.id}`);}
