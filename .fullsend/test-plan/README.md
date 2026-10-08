# Run the test-plan producer

The normal `test-plan` agent keeps Jira label stamping. For a comparison run,
choose `test-plan-dry-run`: it sets `FULLSEND_DRY_RUN=true` inside the sandbox,
skips label stamping, and overrides the Jira profile with enforced read-only
access. There is no `--dry-run` flag on `fullsend run`; select the agent name.

## Prerequisites

- Run from an `odh-test-gen` checkout with the Fullsend CLI and OpenShell configured.
- Install `jsonschema>=4.18` in the host Python environment.
- Export `JIRA_URL`, `JIRA_USER`, and `JIRA_TOKEN`.
- Export `ANTHROPIC_VERTEX_PROJECT_ID`, `GOOGLE_CLOUD_PROJECT`, `CLOUD_ML_REGION`, and `GOOGLE_APPLICATION_CREDENTIALS`.

## Create a plan

From the producer checkout, set the strategy key and run Fullsend with the checkout as its target:

```bash
RUN_OUTPUT=$(mktemp -d /tmp/fullsend-test-plan.XXXXXX)
export FULLSEND_TASK='/test-plan-create RHAISTRAT-XXX --output-dir plans'
fullsend run test-plan-dry-run --fullsend-dir .fullsend --target-repo . --output-dir "$RUN_OUTPUT"
```

Replace `RHAISTRAT-XXX` with the strategy issue. If credentials are stored in an env file, add
`--env-file .env`; add `--keep-sandbox` when you need to inspect a failed run.
Use `fullsend run test-plan` for the normal flow that stamps Jira labels.

## Generate cases for an eligible plan

Before continuing, inspect `plans/<feature>/TestPlanReview.md` and proceed only when the verdict is
`Ready` and the score is at least 8.

```bash
export FULLSEND_TASK='/test-plan-create-cases plans/example_feature'
fullsend run test-plan-dry-run --fullsend-dir .fullsend --target-repo . --output-dir "$RUN_OUTPUT"
```

Plans and reviews are written under `plans/<feature>/`; generated cases are written to that feature's
`test_cases/` directory. Fullsend logs and transcripts are under `$RUN_OUTPUT`.
