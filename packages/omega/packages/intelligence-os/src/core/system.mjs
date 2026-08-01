import path from "node:path";
import { loadSystem, ROOT } from "./config.mjs";
import { CapabilityRegistry } from "../governance/registry.mjs";
import { CaptainsGate } from "../governance/captains-gate.mjs";
import { WitnessChain } from "../witness/chain.mjs";
import { createRuntime } from "../runtime/factory.mjs";
import { OrchestrationEngine } from "../orchestration/engine.mjs";
export class WiseGenOS{
 constructor({witnessFile}={}){this.config=loadSystem();this.registry=new CapabilityRegistry(this.config.registry);this.gate=new CaptainsGate({policy:this.config.gatePolicy,registry:this.registry,runtimeRegistry:this.config.runtimes,estates:this.config.estates});this.witness=new WitnessChain(witnessFile||path.join(ROOT,"var/witness/witness-chain.jsonl"));this.engine=new OrchestrationEngine({gate:this.gate,witness:this.witness,runtimeFactory:createRuntime,runtimeDefinitions:this.config.runtimes});}
 evaluate(request){return this.gate.evaluate(request);}
 execute(request,task){return this.engine.run(request,task);}
 verify(){const issues=[],estateIds=new Set(this.config.estates.map(e=>e.id));for(const c of this.registry.list()){if(!estateIds.has(c.owner_estate))issues.push(`Capability ${c.id} has unknown owner estate`);for(const rid of c.permitted_runtimes)if(!this.config.runtimes.runtimes.some(r=>r.id===rid))issues.push(`Capability ${c.id} references unknown runtime ${rid}`);}const witness=this.witness.verify();return{valid:issues.length===0&&witness.valid,configuration_issues:issues,witness_chain:witness};}
}
