import test from "node:test";import assert from "node:assert/strict";import { evaluateKnowledgePromotion } from "../src/knowledge/promotion.mjs";
test("rejects incomplete candidates",()=>assert.equal(evaluateKnowledgePromotion({statement:"x"}).decision,"reject"));
test("holds unapproved candidates",()=>assert.equal(evaluateKnowledgePromotion({statement:"x",source_provenance:"s",validation_method:"m",owner:"o",review_status:"pending"}).decision,"hold"));
test("promotes approved candidates",()=>assert.equal(evaluateKnowledgePromotion({statement:"x",source_provenance:"s",validation_method:"m",owner:"o",review_status:"approved"}).decision,"promote"));
