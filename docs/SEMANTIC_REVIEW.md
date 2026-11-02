# AI Semantic Reviewer

## Purpose

This provider-agnostic client asks an OpenAI-compatible chat-completions endpoint to review a supplied change and validates the response before writing a result artifact. It is optional and does not replace deterministic checks, global-rule integrity checks, project-specific tests, or human review.

## Input contract

Provide a UTF-8 JSON object with `task`, `diff`, `changed_files`, `global_rules`, and `project_instructions`. The caller is responsible for sourcing the exact diff and authoritative instructions. Do not silently substitute instructions from an unrelated branch.

## Configuration

Set these environment variables in the execution environment:

- `AI_REVIEW_API_BASE`: API base URL, without credentials.
- `AI_REVIEW_API_KEY`: secret API key.
- `AI_REVIEW_MODEL`: exact model identifier supported by the endpoint.

No provider is selected by default. Never commit these values or print them in logs. Before sending private code to an external model, approve the provider and data-handling policy and minimize/redact context.

## Result and failure policy

Statuses are `PASS`, `NEEDS_CHANGES`, and `INCONCLUSIVE`. The validator checks exact output keys, status and severity values, changed-file membership, positive integer line ranges, and exact substrings for diff evidence and quoted rules. `PASS` with findings and `NEEDS_CHANGES` without findings are rejected. Missing configuration, request errors, malformed JSON, or invalid evidence block the review rather than becoming a pass.

These checks establish only that the response is structurally valid and quotes supplied material. They do not prove reasoning correctness, that line numbers match the quoted text, or that every defect was found. A `PASS` is not proof of total compliance.

## Run offline tests

```sh
python -m unittest discover -s tests -p 'test_ai_semantic_review.py' -v
```

The tests do not call a model API. A live end-to-end test against a non-sensitive fixture remains a separate acceptance requirement.
