import { GovernanceError } from "../core/errors.mjs";
const riskOrder={low:1,medium:2,high:3,critical:4};
export class CapabilityRegistry {
  constructor(registry){this.registry=registry;}
  list(){return [...this.registry.capabilities];}
  get(id){const c=this.registry.capabilities.find(x=>x.id===id); if(!c) throw new GovernanceError(`Unknown capability: ${id}`,{capability_id:id}); return c;}
  assertUsable({capabilityId,runtimeId,riskTier,dataClassification}){
    const c=this.get(capabilityId);
    if(c.status!=="certified") throw new GovernanceError("Capability is not certified",{capability:c});
    if(!c.permitted_runtimes.includes(runtimeId)) throw new GovernanceError("Runtime is not permitted for this capability",{capability_id:capabilityId,runtime_id:runtimeId});
    if(riskOrder[riskTier]>riskOrder[c.risk_ceiling]) throw new GovernanceError("Requested risk exceeds capability ceiling",{requested:riskTier,ceiling:c.risk_ceiling});
    if(!c.permitted_data_classifications.includes(dataClassification)) throw new GovernanceError("Data classification is not permitted",{requested:dataClassification,permitted:c.permitted_data_classifications});
    return c;
  }
}
