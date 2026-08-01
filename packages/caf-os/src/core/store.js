import { promises as fs } from "node:fs";
import path from "node:path";
import crypto from "node:crypto";

export class ProjectStore {
  constructor(root = process.env.CAF_PROJECT_ROOT ?? path.resolve("runtime/projects")) { this.root = root; }
  safe(id) {
    if (!/^[a-z0-9][a-z0-9-]{2,63}$/.test(id)) throw new Error("Invalid project id");
    return path.join(this.root, id);
  }
  async init(project) {
    const dir = this.safe(project.id);
    for (const p of ["assets/references", "assets/audio", "assets/renders", "registry", "witness", "approvals"]) await fs.mkdir(path.join(dir, p), { recursive: true });
    await this.writeJson(path.join(dir, "project.json"), project);
    await this.appendWitness(project.id, "project.initialised", { project });
    return dir;
  }
  async exists(id) { try { await fs.access(this.safe(id)); return true; } catch { return false; } }
  async writeShot(id, shot) {
    const p = path.join(this.safe(id), "registry", "shots.json");
    const rows = await this.readJson(p, []); rows.push(shot); await this.writeJson(p, rows);
  }
  async writeJob(id, job) {
    const p = path.join(this.safe(id), "registry", "jobs.json");
    const rows = await this.readJson(p, []); const i = rows.findIndex(x => x.id === job.id);
    i >= 0 ? rows.splice(i, 1, job) : rows.push(job); await this.writeJson(p, rows);
  }
  async appendWitness(id, event, payload) {
    const dir = path.join(this.safe(id), "witness"); await fs.mkdir(dir, { recursive: true });
    const log = path.join(dir, "witness-chain.jsonl"); let prevHash = "GENESIS";
    try {
      const lines = (await fs.readFile(log, "utf8")).trim().split("\n").filter(Boolean);
      if (lines.length) prevHash = JSON.parse(lines.at(-1)).hash;
    } catch {}
    const base = { id: crypto.randomUUID(), timestamp: new Date().toISOString(), event, payload, prevHash };
    const hash = crypto.createHash("sha256").update(JSON.stringify(base)).digest("hex");
    await fs.appendFile(log, JSON.stringify({ ...base, hash }) + "\n");
    return hash;
  }
  async approve(id, gate, approver, evidence) {
    const rec = { id: crypto.randomUUID(), gate, approver, evidence, approvedAt: new Date().toISOString() };
    const p = path.join(this.safe(id), "approvals", "approvals.json");
    const rows = await this.readJson(p, []); rows.push(rec); await this.writeJson(p, rows);
    await this.appendWitness(id, "gate.approved", rec); return rec;
  }
  projectPath(id, ...parts) { return path.join(this.safe(id), ...parts); }
  async readWitness(id) {
    try { return (await fs.readFile(this.projectPath(id, "witness", "witness-chain.jsonl"), "utf8")).trim().split("\n").filter(Boolean).map(JSON.parse); }
    catch { return []; }
  }
  async writeJson(p, v) { await fs.mkdir(path.dirname(p), { recursive: true }); await fs.writeFile(p, JSON.stringify(v, null, 2) + "\n"); }
  async readJson(p, fallback) { try { return JSON.parse(await fs.readFile(p, "utf8")); } catch { return fallback; } }
}
