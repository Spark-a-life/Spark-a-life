import test from "node:test";import assert from "node:assert/strict";import { WiseGenOS } from "../src/core/system.mjs";
test("registry contains only known owner estates",()=>{const os=new WiseGenOS({witnessFile:"/tmp/wisegen-registry.jsonl"});const estates=new Set(os.config.estates.map(e=>e.id));for(const c of os.registry.list())assert.ok(estates.has(c.owner_estate));});
