import readline from "node:readline";
import { CafService } from "../core/service.js";
import { validateShot } from "../core/validate.js";

const service = new CafService();
const tools = [
  { name: "route_shot", description: "Score a shot and recommend an execution profile", inputSchema: { type: "object", required: ["shot"], properties: { shot: { type: "object" } } } },
  { name: "create_project", description: "Create a governed CAF-OS project", inputSchema: { type: "object", required: ["id", "title", "purpose", "audience"], properties: { id: { type: "string" }, title: { type: "string" }, purpose: { type: "string" }, audience: { type: "string" } } } },
  { name: "approve_gate", description: "Record a human Captain's Gate approval", inputSchema: { type: "object", required: ["projectId", "gate", "approver", "evidence"], properties: { projectId: { type: "string" }, gate: { type: "string" }, approver: { type: "string" }, evidence: { type: "string" } } } },
  { name: "read_witness_chain", description: "Read project provenance records", inputSchema: { type: "object", required: ["projectId"], properties: { projectId: { type: "string" } } } }
];
const result = text => ({ content: [{ type: "text", text: JSON.stringify(text, null, 2) }] });
async function call(name, a) {
  if (name === "route_shot") return result(service.routing(validateShot(a.shot)));
  if (name === "create_project") {
    const p = { id: a.id, title: a.title, purpose: a.purpose, audience: a.audience, createdAt: new Date().toISOString() };
    return result({ project: p, path: await service.store.init(p) });
  }
  if (name === "approve_gate") return result(await service.store.approve(a.projectId, a.gate, a.approver, a.evidence));
  if (name === "read_witness_chain") return result(await service.store.readWitness(a.projectId));
  throw new Error("Unknown tool");
}
const rl = readline.createInterface({ input: process.stdin });
rl.on("line", async line => {
  let req;
  try {
    req = JSON.parse(line);
    let out;
    if (req.method === "initialize") out = { protocolVersion: "2025-03-26", capabilities: { tools: {} }, serverInfo: { name: "wisegen-caf-os", version: "1.0.0" } };
    else if (req.method === "tools/list") out = { tools };
    else if (req.method === "tools/call") out = await call(req.params.name, req.params.arguments ?? {});
    else if (req.method?.startsWith("notifications/")) return;
    else throw new Error("Unsupported method");
    process.stdout.write(JSON.stringify({ jsonrpc: "2.0", id: req.id, result: out }) + "\n");
  } catch (e) {
    process.stdout.write(JSON.stringify({ jsonrpc: "2.0", id: req?.id ?? null, error: { code: -32000, message: e instanceof Error ? e.message : "Unknown error" } }) + "\n");
  }
});
