#!/usr/bin/env node
/** Score a portfolio file against the demand rubric and print the result. */
import * as fs from 'node:fs';
import * as path from 'node:path';
import { fileURLToPath } from 'node:url';
import { scorePortfolio } from './scorer.mjs';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const rubric = JSON.parse(fs.readFileSync(path.join(ROOT, 'config', 'demand-rubric.json'), 'utf8'));
const file = process.argv[2] || path.join(ROOT, 'examples', 'sample-portfolio.json');
const portfolio = JSON.parse(fs.readFileSync(file, 'utf8'));

const result = scorePortfolio(portfolio.units, rubric);

console.log(`Rubric ${rubric.rubric_version} (${rubric.status}) | scored ${result.units_scored}, excluded ${result.units_excluded}\n`);
for (const s of [...result.scored].sort((a, b) => b.demand_index - a.demand_index)) {
  console.log(`${s.unit_name.padEnd(20)} hc=${String(s.headcount).padStart(4)}  index=${String(s.demand_index).padStart(5)}  ${s.coverage_recommendation.padEnd(16)} alt=${(s.alternative||'-').padEnd(16)} risk=${s.risk.padEnd(6)} conf=${s.confidence}`);
  for (const c of s.cautions) console.log(`  caution: ${c}`);
}
for (const e of result.excluded) console.log(`\nEXCLUDED ${e.unit_name}: ${e.reason} (headcount ${e.details.headcount}, minimum ${e.details.minimum_cell_size})`);
if (result.portfolio_caution) console.log(`\n${result.portfolio_caution}`);
