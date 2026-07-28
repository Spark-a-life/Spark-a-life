import test from "node:test";import assert from "node:assert/strict";import {readFile} from "node:fs/promises";import {routeShot} from "../src/core/router.js";
const load=async p=>JSON.parse(await readFile(new URL(p,import.meta.url),"utf8"));
test("controlled close-up is routed contextually",async()=>{const r=routeShot(await load("../examples/shots/dialogue-closeup.json"));assert.ok(["kling","seedance"].includes(r.primary.provider));assert.ok(r.primary.score>0)});
test("multi-shot dialogue does not default to Kling",async()=>{const r=routeShot(await load("../examples/shots/multishot-dialogue.json"));assert.ok(["seedance","lora"].includes(r.primary.provider));assert.notEqual(r.primary.provider,"kling")});
