import { RuntimeAdapter } from "./adapter.mjs";
export class LocalDeterministicRuntime extends RuntimeAdapter {
 async execute({task}){
  const claim=String(task.claim||"").trim();
  if(!claim) throw new Error("Task claim is required");
  const evidence=Array.isArray(task.evidence)?task.evidence:[];
  const supporting=evidence.filter(x=>x.supports===true), contradicting=evidence.filter(x=>x.supports===false);
  let verdict="insufficient-evidence";
  if(supporting.length&& !contradicting.length) verdict="supported";
  if(contradicting.length&& !supporting.length) verdict="not-supported";
  if(contradicting.length&&supporting.length) verdict="contested";
  return {runtime:this.id,task_type:"source-verification",claim,verdict,evidence_summary:{supplied:evidence.length,supporting:supporting.length,contradicting:contradicting.length},limitations:["This deterministic runtime evaluates declared evidence only.","It does not retrieve or authenticate external sources."]};
 }
}
