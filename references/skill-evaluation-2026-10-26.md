# Testing the skill: October 26, 2026

> Historical record for **Prompt & Cache-Readiness Optimizer**, produced with earlier project instructions or settings. Recorded prompts, responses, scores, and settings are preserved. See the [current README](../README.md) and [glossary](glossary.md) for the maintained message and term definitions.

I tested the skill on eight synthetic requests covering invoices, meeting notes, inventory, account authorization, embedded instructions, currency, missing information, and a calculation. A fresh Codex session received the full `SKILL.md` and each original request and returned a revised prompt. Separate fresh sessions then executed the original and revised versions.

## Results

| Measure | Original prompts | Skill-generated prompts |
|---|---:|---:|
| Responses passing exact JSON checks | 7/8 | 7/8 |
| Total prompt characters | 1,746 | 1,675 |

The skill-generated prompts used 71 fewer characters in total, a 4.1% reduction. Five rewrites were shorter and three were longer. Character counts are not token counts and do not establish cost savings.

The strict test marked the meeting case wrong for both versions. Both responses included the correct owner and date and said “The team approved the pilot.” The expected text was “approved the pilot.” The responses preserved the meaning, but the automatic check required exact wording. The recorded score remains 7/8 rather than changing the rule after seeing the answers.

## Example

The original inventory prompt asked for a stock calculation in JSON: start with 80 units, subtract 27 sold, and add 3 returned. The skill's rewrite kept the SKU, all three quantities, the two required output keys, and the JSON-only requirement. Both executions returned `{"sku":"B-17","remaining":56}`.

## Method and limitations

The test used `gpt-6.1-sol`, eight independent skill-generation calls, and 16 separate execution calls. The instruction text from the repository's skill file was supplied to Codex directly. This tests the skill instructions, but not automatic discovery or installation of the skill. Each case was run once per version, with up to three calls at a time. The prompts and expected outputs were created for this test, and no held-out set was used.

The checker compares JSON keys, values, and types exactly. It does not independently grade whether each rewritten instruction preserved every subtle requirement. In the embedded-instruction and authorization cases, the expected answers matched; this is not a security audit or proof that a real application enforces permissions.

The [script](../evals/skill-evaluation.py) and [recorded prompts and responses](../evals/skill-evaluation-results.json) are available for review. Running the script requires a signed-in Codex CLI and uses its allowance. The experiment did not measure API cost, cache behavior, or reliable speed differences. Results are a small feasibility check, not validation for production.

## Reproduce a comparison

From the root of a separate checkout with a signed-in Codex CLI:

```bash
python evals/skill-evaluation.py
```

The script reads the checkout's current `SKILL.md`, makes eight rewrite calls and 16 execution calls, consumes account allowance, and overwrites `evals/skill-evaluation-results.json`. Running it on version 1.1.0 evaluates the new instructions. The earlier source commit is not included in this fresh repository history; saved prompts and responses remain available in the results file. A changing model alias and assistant environment can still change new results.

The script records individual failures but does not fail its overall process when an answer check fails. Inspect the saved cases and scores. The original score stays 7/8; any new semantic scoring rule must be defined before another run.
