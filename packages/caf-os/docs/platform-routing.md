# Platform Routing Guide

| Profile | Prefer when | Avoid when |
|---|---|---|
| Kling-style | one strong starting frame, short controlled motion, natural physics, close-up or insert | major head rotation, long multi-shot identity, heavy occlusion |
| Seedance-style | multi-shot sequence, camera cuts, dialogue, persistent multi-angle references | single-shot physics is the only priority or reference binding is weak |
| LoRA/local | recurring proprietary character or style, repeated production value | one-off production, inadequate training data, low technical capacity |
| Avatar | presenter, localisation, corporate instruction, clear speech | dramatic action, environmental interaction, cinematic staging |
| Assembly engine | rapid explainer, stock-led content, social adaptation | narrative acting and strong cross-shot character continuity |

The router in `src/core/router.ts` implements an auditable baseline. It is deliberately deterministic, so organisations can inspect and amend policy weights.
