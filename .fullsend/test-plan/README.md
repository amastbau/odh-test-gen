# Run the test-plan producer

This comparison branch runs with `FULLSEND_DRY_RUN=true` inside the sandbox.
It skips Jira label stamping and enforces read-only Jira access, while still
fetching the strategy and producing local plan artifacts. Do not pass a
`--dry-run` flag to `fullsend run`; the harness applies this mode automatically.

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
fullsend run test-plan --fullsend-dir .fullsend --target-repo . --output-dir "$RUN_OUTPUT"
```

Replace `RHAISTRAT-XXX` with the strategy issue. If credentials are stored in an env file, add
`--env-file .env`; add `--keep-sandbox` when you need to inspect a failed run.

## Generate cases for an eligible plan

Before continuing, inspect `plans/<feature>/TestPlanReview.md` and proceed only when the verdict is
`Ready` and the score is at least 8.

```bash
export FULLSEND_TASK='/test-plan-create-cases plans/example_feature'
fullsend run test-plan --fullsend-dir .fullsend --target-repo . --output-dir "$RUN_OUTPUT"
```

Plans and reviews are written under `plans/<feature>/`; generated cases are written to that feature's
`test_cases/` directory. Fullsend logs and transcripts are under `$RUN_OUTPUT`.
