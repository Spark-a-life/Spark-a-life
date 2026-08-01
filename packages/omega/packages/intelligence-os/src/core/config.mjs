import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
const here = path.dirname(fileURLToPath(import.meta.url));
export const ROOT = path.resolve(here, "../..");
export function readJson(relativePath) { return JSON.parse(fs.readFileSync(path.join(ROOT, relativePath), "utf8")); }
export function loadSystem() {
  return {
    constitution: readJson("config/constitution.json"),
    lanes: readJson("config/lanes.json"),
    gatePolicy: readJson("config/policies/captains-gate.json"),
    registry: readJson("config/capabilities.json"),
    runtimes: readJson("config/runtimes.json"),
    estates: ["maie","taie","paie","gaie","saie"].map(id => readJson(`config/estates/${id}.json`))
  };
}
