import test from "node:test";import assert from "node:assert/strict";import { LocalDeterministicRuntime } from "../src/runtime/local-deterministic.mjs";
const runtime=new LocalDeterministicRuntime({id:"local-deterministic"});
test("returns not-supported for contradicting evidence",async()=>{const r=await runtime.execute({task:{claim:"x",evidence:[{supports:false}]}});assert.equal(r.verdict,"not-supported");});
test("returns contested for mixed evidence",async()=>{const r=await runtime.execute({task:{claim:"x",evidence:[{supports:false},{supports:true}]}});assert.equal(r.verdict,"contested");});
