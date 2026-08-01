#!/usr/bin/env node
import fs from "node:fs";
import { spawnSync } from "node:child_process";
import { WiseGenOS } from "./core/system.mjs";
const os=new WiseGenOS(),command=process.argv[2]||"help";
const print=v=>process.stdout.write(`${JSON.stringify(v,null,2)}
`);
async function main(){
 if(command==="demo"){
  const request={request_id:`demo-${Date.now()}`,estate:"TAIE",actor:"human-owner",purpose:"Assess whether Hermes Agent is the governing OS or a bounded runtime",action:"internal_assessment",risk_tier:"medium",capability_id:"research.source-verification",data_classification:"public",external_side_effect:false,human_approved:true,approval_reference:"demo-owner-approval",runtime_id:"local-deterministic"};
  const task={claim:"Hermes Agent is the WiseGen APE Intelligence operating system.",evidence:[{source:"WiseGen constitutional architecture",supports:false,rationale:"WiseGen retains system-wide governance authority."},{source:"Runtime registry",supports:false,rationale:"Hermes Agent is classified as an optional external execution substrate."}]};
  print(await os.execute(request,task));return;
 }
 if(command==="verify"){const result=os.verify();print(result);process.exitCode=result.valid?0:1;return;}
 if(command==="test"){const r=spawnSync(process.execPath,["--test"],{stdio:"inherit"});process.exitCode=r.status??1;return;}
 if(command==="gate"){const file=process.argv[3];if(!file)throw new Error("Usage: wisegen gate <action-request.json>");print(os.evaluate(JSON.parse(fs.readFileSync(file,"utf8"))));return;}
 if(command==="run"){const requestFile=process.argv[3],taskFile=process.argv[4];if(!requestFile||!taskFile)throw new Error("Usage: wisegen run <action-request.json> <task.json>");print(await os.execute(JSON.parse(fs.readFileSync(requestFile,"utf8")),JSON.parse(fs.readFileSync(taskFile,"utf8"))));return;}
 if(command==="registry"){print(os.registry.list());return;}
 if(command==="estates"){print(os.config.estates);return;}
 if(command==="lanes"){print(os.config.lanes);return;}
 if(command==="witness"){print(os.witness.verify());return;}
 if(command==="reset"){os.witness.reset();print({reset:true});return;}
 process.stdout.write(`WiseGen APE Intelligence OS

Usage:
  wisegen help
  wisegen demo
  wisegen verify
  wisegen test
  wisegen gate <action-request.json>
  wisegen run <action-request.json> <task.json>
  wisegen registry
  wisegen estates
  wisegen lanes
  wisegen witness
  wisegen reset
`);
}
main().catch(error=>{process.stderr.write(`${error.stack||error.message}
`);process.exitCode=1;});
