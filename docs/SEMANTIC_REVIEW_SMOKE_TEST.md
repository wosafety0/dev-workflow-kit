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

The example diff is intentionally synthetic and is not a patch from this repository. Run it through the standalone reviewer (not the Harness runner) so it is not misrepresented as source-bound acceptance:

```powershell
python -I -S scripts/ai_semantic_review.py --input examples/semantic-review-negative-input.json --output artifacts/semantic-review-output.json
$LASTEXITCODE
```

The standalone CLI writes only the detailed review output; it does not produce a Harness acceptance report or attest Git source provenance. Since the fixture is intentionally defective, the expected result is `NEEDS_CHANGES`. That is a negative model smoke test, not a successful code-review approval.

If the model returns `PASS`, treat that as a failed smoke-test expectation and do not use the result to approve code. Inspect the detailed output; do not weaken the validator just to make the fixture pass.

## Endpoint transport

Follow [the stable acceptance contract](STABLE_ACCEPTANCE_CONTRACT.md): remote endpoints must use HTTPS. Cleartext HTTP should be used only when the reviewed implementation explicitly supports a literal loopback IP, and must never be enabled for remote hosts. The smoke test makes a live model request and can consume provider quota; run it deliberately, not in routine offline CI.
