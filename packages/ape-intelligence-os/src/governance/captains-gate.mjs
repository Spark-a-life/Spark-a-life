import { GovernanceError } from "../core/errors.mjs";
export class CaptainsGate {
 constructor({policy,registry,runtimeRegistry,estates}){this.policy=policy;this.registry=registry;this.runtimeRegistry=runtimeRegistry;this.estates=estates;}
 evaluate(request){
  const missing=this.policy.required_fields.filter(f=>!(f in request));
  if(missing.length) return this.#deny("Missing required governance fields",{missing});
  if(!this.estates.some(e=>e.id===request.estate)) return this.#deny("Unknown intelligence estate",{estate:request.estate});
  if(this.policy.automatic_denials.includes(request.action)) return this.#deny("Action is automatically denied by constitutional policy",{action:request.action});
  if(request.external_side_effect===true) return this.#deny("External side effects are disabled in this baseline",{action:request.action});
  const tier=this.policy.risk_tiers[request.risk_tier];
  if(!tier) return this.#deny("Unknown risk tier",{risk_tier:request.risk_tier});
  if(tier.decision==="deny") return this.#deny(tier.reason,{risk_tier:request.risk_tier});
  const runtime=this.runtimeRegistry.runtimes.find(r=>r.id===request.runtime_id);
  if(!runtime||runtime.enabled!==true) return this.#deny("Runtime is unavailable or disabled",{runtime_id:request.runtime_id});
  try{
   const capability=this.registry.assertUsable({capabilityId:request.capability_id,runtimeId:request.runtime_id,riskTier:request.risk_tier,dataClassification:request.data_classification});
   const requires=tier.human_approval===true||capability.human_approval_for.includes("all")||capability.human_approval_for.includes(request.action);
   if(requires&&request.human_approved!==true) return {decision:"hold",reason:"Human approval is required before execution",obligations:["record_approval","append_witness_record"],capability};
   return {decision:"allow",reason:"Request satisfies Captain's Gate controls",obligations:["append_witness_record","preserve_reversibility"],capability};
  }catch(error){if(error instanceof GovernanceError) return this.#deny(error.message,error.details); throw error;}
 }
 #deny(reason,details){return {decision:"deny",reason,obligations:["append_witness_record"],details};}
}
