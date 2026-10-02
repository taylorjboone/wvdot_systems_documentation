# Raw distress study (2026-09-29) — scripts and outputs

The write-ups live one level up and in the app under **Documents → Pavement Studies**:

| Page | What it covers |
|---|---|
| `../Pavement_Raw_Distress_Study.md` | how the study was done, step by step, and how to rerun it (start here) |
| `../Pavement_Raw_Distress_Deterioration.md` | how the raw values deteriorate |
| `../Pavement_Treatment_Resets.md` | what treatments do to the raw values |
| `../Pavement_Treatment_Strategies.md` | strategies and treatment order |

`scripts/` holds every script, in the order they run:

| Order | Scripts |
|---|---|
| Data | `load_raw` → `pull_hub_mms` → `build_pairs` |
| Deterioration | `forms`, `covs`, `multipliers`, `nls`, `nls_cv`, `families`, `gfp_validate`, `engine_rates` |
| Resets | `resets`, `resets_analyze`, `engine_resets` |
| Strategies | `history`, `strategies`, `budget`, `engine_trigger_check` |

`results/` holds the outputs of the 2026-09-29 run. Everything is read-only against the database, TheHub and OM. Working files go to `$STUDY_DIR`.
