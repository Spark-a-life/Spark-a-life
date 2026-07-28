import test from "node:test";import assert from "node:assert/strict";import { WiseGenOS } from "../src/core/system.mjs";
const base={request_id:"t1",estate:"TAIE",actor:"owner",purpose:"test",action:"internal_assessment",risk_tier:"medium",capability_id:"research.source-verification",data_classification:"public",external_side_effect:false,runtime_id:"local-deterministic"};
test("holds medium-risk work without approval",()=>{const os=new WiseGenOS({witnessFile:"/tmp/wisegen-gate-1.jsonl"});assert.equal(os.evaluate(base).decision,"hold");});
test("allows approved bounded work",()=>{const os=new WiseGenOS({witnessFile:"/tmp/wisegen-gate-2.jsonl"});assert.equal(os.evaluate({...base,human_approved:true}).decision,"allow");});
test("denies external side effects",()=>{const os=new WiseGenOS({witnessFile:"/tmp/wisegen-gate-3.jsonl"});assert.equal(os.evaluate({...base,human_approved:true,external_side_effect:true}).decision,"deny");});
test("denies disabled Hermes runtime",()=>{const os=new WiseGenOS({witnessFile:"/tmp/wisegen-gate-4.jsonl"});assert.equal(os.evaluate({...base,human_approved:true,runtime_id:"hermes-agent"}).decision,"deny");});
