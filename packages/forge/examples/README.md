# Examples

## employee-onboarding

The reference demonstrator's inputs. They are deliberately imperfect: the spreadsheet carries blank cells, inconsistent status values and a mix of classifications, because a clean synthetic dataset would prove nothing about the organisations this platform is built for.

| File | Role in the run |
|---|---|
| `requirement.md` | The plain requirement statement, stage 1 intake |
| `onboarding.csv` | The operational sheet the process actually runs on |
| `hr-policy.md` | Organisational policy the application must respect |
| `org-chart.csv` | Reporting lines, used to derive roles and approval paths |

```bash
make demo                                        # full nine-stage run
forge compile-sheet examples/employee-onboarding/onboarding.csv   # just the data inspection
```

The sheet contains fields classified `restricted`. That is intentional: it exercises classification propagation from intake through the specification, the generated schema, the server-side masking rules and the retention rule on the evidence.
