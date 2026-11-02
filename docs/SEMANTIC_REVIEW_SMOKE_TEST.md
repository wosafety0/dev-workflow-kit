# Semantic Review Smoke Test

This is a manual, opt-in model smoke test. It is not part of offline CI and must not be treated as proof that the model detects every defect.

## Fixture

- Config: `examples/harness-config-semantic-review.json`
- Input: `examples/semantic-review-negative-input.json`
- The sample diff changes an addition function from `a + b` to `a - b` without authorization.
- The expected semantic result is `NEEDS_CHANGES`; inspect `artifacts/semantic-review-output.json` to confirm the model's finding and evidence.

## Run on a trusted worktree

Set the following process environment variables using your approved local secret-handling method. Do not put API keys in source files, the config JSON, command arguments, or logs:

- `AI_REVIEW_API_BASE`: an OpenAI-compatible `/v1` API base URL.
- `AI_REVIEW_API_KEY`: provider key, or a local placeholder accepted by the inference server.
- `AI_REVIEW_MODEL`: the exact model identifier exposed by that endpoint.

Then run from the project root:

```powershell
python scripts/harness_runner.py --config examples/harness-config-semantic-review.json --review-input examples/semantic-review-negative-input.json --review-output artifacts/semantic-review-output.json
$LASTEXITCODE
```

The runner writes a redacted `artifacts/acceptance-report.json` separately from the detailed review output. Since the fixture is intentionally defective, a correct `NEEDS_CHANGES` result should make the runner return exit code `1` and the acceptance report status `failed`. That is the expected fail-closed result for this negative fixture, not a successful code-review approval.

If the model returns `PASS`, treat that as a failed smoke-test expectation and do not use the result to approve code. Inspect the detailed output; do not weaken the validator just to make the fixture pass.

## Endpoint transport

Follow [the stable acceptance contract](STABLE_ACCEPTANCE_CONTRACT.md): remote endpoints must use HTTPS. Cleartext HTTP should be used only when the reviewed implementation explicitly supports a literal loopback IP, and must never be enabled for remote hosts. The smoke test makes a live model request and can consume provider quota; run it deliberately, not in routine offline CI.
