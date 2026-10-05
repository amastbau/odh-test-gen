# Native test-plan producer

The consumer supplies one `FULLSEND_TASK` and a separate target workspace. The
agent writes `agent-result.json` with the feature directory relative to that
workspace. Fullsend validates the result, then the post hook copies designated
plan, review, source snapshot, output directory marker, optional gaps, and case
files into the caller's `TARGET_REPO_DIR`. Normal create requires `TestPlan.md`
and `README.md`; cases also requires `test_cases/INDEX.md`. If create reaches
the skill's no-acceptance-criteria stop, the result sets
`no_acceptance_criteria: true` and a score-zero review is sufficient without a
plan or README. The marker's `output_dir` is rebased to the caller's output
parent. The consumer must likewise rebase the marker when staging a fresh cases
target.

The Fullsend runner's Python environment needs `jsonschema>=4.18` for the
native validation hook. Provision it with the runner; the hook does not install
packages. No producer pre hook is configured: both existing skills run the
plugin bootstrap and dependency setup in their own preflight steps, and a host
pre hook must not execute scripts from the target workspace.
