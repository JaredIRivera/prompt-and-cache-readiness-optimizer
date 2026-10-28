# Codex prompt comparison: October 26, 2026

> Historical record for **Prompt & Cache-Readiness Optimizer**, produced with earlier project instructions or settings. Recorded prompts, responses, scores, and settings are preserved. See the [current README](../README.md) and [glossary](glossary.md) for the maintained message and term definitions.

I tested whether a shorter set of instructions could preserve results on a small set of tasks. The revised instruction was written using the skill's principles: remove repetition while keeping the task, facts, format, and treatment of supplied data.

## Results

| Measure | Original instruction | Revised instruction |
|---|---:|---:|
| Instruction length, including spaces | 340 characters | 178 characters |
| Responses matching the expected JSON | 20 of 20 | 20 of 20 |
| Extraction cases passed | 10 of 10 | 10 of 10 |
| Arithmetic cases passed | 5 of 5 | 5 of 5 |
| Authorization scenarios passed | 5 of 5 | 5 of 5 |

The revised instruction was 162 characters shorter, a **47.6% reduction in the instruction text**. Both versions passed every check in this sample. The task text was identical in each pair and was not included in that length calculation.

## What I tested

I ran 40 separate Codex sessions using `gpt-6.1-sol`: one original and one revised instruction for each of 20 synthetic tasks. Ten tasks extracted fields from short records, five calculated totals, and five asked for a decision when authorization was not confirmed. Two extraction records included a conflicting instruction inside the source data.

A script compared each response with its expected JSON, including the required fields and values. A second check confirmed the recorded JSON matched the expected values with their types. The calls ran with up to four sessions at once. The order of the two versions alternated by case number.

The [cases and full responses](../evals/codex-comparison-results.json) and the [test script](../evals/codex-comparison.py) are included for inspection. The script requires Python and a signed-in Codex CLI; it uses the account's Codex allowance rather than a paid API call.

## What these results do and do not show

This test shows that the shorter instruction matched the expected answers on these 20 cases. It does not establish that the skill will preserve quality on other tasks or in a production system. The cases are simple, synthetic, and created for this test; there is no separate held-out set or repeated trial per case.

The revised instruction was manually prepared using the skill's principles. The test did not invoke the skill itself to generate it, and it did not run the bundled compiler or benchmark. The authorization cases check the model's written response, not an application's actual permission controls. The two embedded-instruction cases are a small check, not a security audit.

No API charges, API cost savings, or reliable speed improvement were measured. Session usage and elapsed time in the raw results include Codex's own instructions, setup, and shared service conditions; they cannot be attributed to the prompt edit alone. The original prompt was constructed for this comparison and is not a measurement of a real user's existing workflow.

A stronger follow-up would use real, anonymized tasks, ask the skill to produce the revised prompts, reserve unseen cases, repeat trials, and check the complete workflow against a baseline.

## Run another comparison

From a separate checkout with a signed-in Codex CLI:

```bash
python evals/codex-comparison.py
```

This uses account allowance for 40 requests and overwrites `evals/codex-comparison-results.json`. Its revision is hand-written; it does not invoke the skill. Inspect saved pass/fail results rather than using the process exit status as a passing score.
