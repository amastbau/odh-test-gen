# Native test-plan producer

The consumer supplies one `FULLSEND_TASK` per invocation and shares a single
`TARGET_REPO_DIR` between create and cases. The agent writes
`agent-result.json` with the feature directory relative to that workspace.
Fullsend validates the result, then the post hook copies designated plan,
review, source snapshot, output directory marker, optional gaps, the optional
`.analysis-endpoints.md`, `.analysis-risks.md`, and `.analysis-infra.md` files,
and case files into the caller's target. Normal create requires `TestPlan.md`
and `README.md`; cases also requires `test_cases/INDEX.md`. If create reaches
the skill's no-acceptance-criteria stop, the result sets
`no_acceptance_criteria: true` and a score-zero review is sufficient without a
plan or README. The marker's `output_dir` is rebased to the caller's output
parent. Both invocations use the same target, so the consumer does not rebase
the marker for a separate cases target.

The descriptor sets the native timeout to 90 minutes per invocation for both
create and cases. This is a maximum duration, not a required wait or a guarantee
of completion or a `Ready` review. Verify the behavior manually with the
published descriptor pin.

The Fullsend runner's Python environment needs `jsonschema>=4.18` for the
native validation hook. Provision it with the runner; the hook does not install
packages. No producer pre hook is configured: both existing skills run the
plugin bootstrap and dependency setup in their own preflight steps, and a host
pre hook must not execute scripts from the target workspace.

The descriptor pins a Fullsend sandbox image candidate expected to provide
Tirith for Fullsend's default security hook. Compatibility with the current
Fullsend runtime still needs manual verification.
