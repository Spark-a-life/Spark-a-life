import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";
function stable(v){if(Array.isArray(v))return v.map(stable);if(v&&typeof v==="object")return Object.fromEntries(Object.keys(v).sort().map(k=>[k,stable(v[k])]));return v;}
function canonical(v){return JSON.stringify(stable(v));}
export class WitnessChain{
 constructor(filePath){this.filePath=filePath;fs.mkdirSync(path.dirname(filePath),{recursive:true});}
 read(){if(!fs.existsSync(this.filePath))return[];const t=fs.readFileSync(this.filePath,"utf8").trim();return t?t.split("\n").map(JSON.parse):[];}
 append({eventType,requestId,payload}){const records=this.read(),prev=records.at(-1);const unsigned={sequence:records.length+1,timestamp:new Date().toISOString(),event_type:eventType,request_id:requestId,payload,previous_hash:prev?.hash||"GENESIS"};const hash=crypto.createHash("sha256").update(canonical(unsigned)).digest("hex");const record={...unsigned,hash};fs.appendFileSync(this.filePath,`${JSON.stringify(record)}\n`,"utf8");return record;}
 verify(){const records=this.read();for(let i=0;i<records.length;i++){const r=records[i],expectedPrev=i===0?"GENESIS":records[i-1].hash;if(r.previous_hash!==expectedPrev)return{valid:false,index:i,reason:"previous_hash mismatch"};const{hash,...unsigned}=r;const expected=crypto.createHash("sha256").update(canonical(unsigned)).digest("hex");if(hash!==expected)return{valid:false,index:i,reason:"record hash mismatch"};}return{valid:true,records:records.length};}
 reset(){if(fs.existsSync(this.filePath))fs.unlinkSync(this.filePath);}
}
