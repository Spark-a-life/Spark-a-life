import { RuntimeAdapter } from "./adapter.mjs";
export class HermesAgentAdapter extends RuntimeAdapter { async execute(){throw new Error("Hermes Agent is disabled. Enable only after adapter evaluation, policy approval and runtime-specific assurance.");} }
