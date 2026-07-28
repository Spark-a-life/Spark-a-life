# Evaluations

Eight gates, five blocking. The list is short deliberately: gates run on every candidate in every run, so an expensive gate set produces pressure to skip it, and a skipped gate is worse than an absent one.

```bash
make demo    # runs the gates
cat .forge/demo/evidence/evaluation.json
```

Adding a gate requires stating what it asks and what a failure means. A gate whose failure nobody can interpret produces a red light nobody acts on.
