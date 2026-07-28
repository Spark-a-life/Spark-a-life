export class OrchestrationEngine {
 constructor({gate,witness,runtimeFactory,runtimeDefinitions}){this.gate=gate;this.witness=witness;this.runtimeFactory=runtimeFactory;this.runtimeDefinitions=runtimeDefinitions;}
 async run(request,task){
  const gate=this.gate.evaluate(request);
  this.witness.append({eventType:"captains-gate.decision",requestId:request.request_id,payload:{request,gate}});
  if(gate.decision!=="allow") return {gate,executed:false};
  const definition=this.runtimeDefinitions.runtimes.find(r=>r.id===request.runtime_id);
  const runtime=this.runtimeFactory(definition);
  this.witness.append({eventType:"runtime.execution.started",requestId:request.request_id,payload:{runtime_id:runtime.id,capability_id:request.capability_id}});
  try{
   const result=await runtime.execute({request,task});
   this.witness.append({eventType:"runtime.execution.completed",requestId:request.request_id,payload:{runtime_id:runtime.id,capability_id:request.capability_id,result}});
   return {gate,executed:true,result};
  }catch(error){
   this.witness.append({eventType:"runtime.execution.failed",requestId:request.request_id,payload:{runtime_id:runtime.id,capability_id:request.capability_id,error:error.message}});
   throw error;
  }
 }
}
