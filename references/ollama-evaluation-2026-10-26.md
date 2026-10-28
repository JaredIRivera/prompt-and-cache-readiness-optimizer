# Local Ollama comparison: October 26, 2026

> Historical record for **Prompt & Cache-Readiness Optimizer**, produced with earlier project instructions or settings. Recorded prompts, responses, scores, and settings are preserved. See the [current README](../README.md) and [glossary](glossary.md) for the maintained message and term definitions.

I tested the original and skill-generated prompts on a locally installed Gemma 4 12B model using Ollama. The eight synthetic tasks and the skill-generated rewrites come from the [direct skill evaluation](skill-evaluation-2026-10-26.md). This is a follow-up using a different model, not a separate test of the skill generating rewrites.

## Results

| Measure | Original prompts | Skill-generated prompts |
|---|---:|---:|
| Input tokens across eight requests | 500 | 527 |
| Output tokens without JSON mode | 254 | 254 |
| Exact JSON checks without JSON mode | 0/8 | 0/8 |
| Output tokens with JSON mode | 214 | 214 |
| Exact JSON checks with JSON mode | 7/8 | 7/8 |

The revised prompts used 27 more input tokens, or 5.4% more, on this model. They were shorter in characters in the earlier test, which shows why character count is not a reliable substitute for the model's token count. This sample did **not** show token savings.

Without JSON mode, the model put every response inside Markdown code fences, so none was valid as a standalone JSON document. Enabling Ollama's JSON mode produced valid JSON in all 16 responses. The remaining exact-check failure in each group was the meeting case: “The team approved the pilot.” expressed the expected decision but did not match the checker's exact phrase. The score stays 7/8 under the original strict rule.

## What I changed after the first result

The model's formatting failure showed that asking for JSON in a prompt was insufficient for this setup. I repeated the same cases using Ollama's built-in JSON output mode. That addressed the code-fence issue in this sample. It does not prove that a real application validates values, enforces authorization, or handles failures safely.

## Method and limits

I ran one response per prompt version in each mode, with a warmup before each set and alternating order. The model was `gemma4:12b` (11.9B parameters, Q4_K_M), on Ollama 0.30.10, with temperature 0, seed 42, context size 4096, and output limit 256 tokens. The model ran locally using a mixture of CPU and GPU. Ollama reported the token counts. The local run incurred no API charges; electricity and hardware costs were not measured.

These are eight synthetic tasks and one trial per prompt per mode. There was no unseen evaluation set, repeated sampling, production traffic, measured energy use, or live provider cache comparison. The skill-rewrite calls used Codex and their overhead is not included in the Ollama token totals. The model's initial load took about 69 seconds on this machine; the timing and results cannot be generalized to other machines or workloads.

This evidence does not establish cost savings or production readiness. Before deployment, test representative tasks and unseen cases, validate output against an application schema, enforce approvals in application code, measure error handling and operational limits, and measure the full workflow including any optimization step.

The [test script](../evals/ollama-evaluation.py), [default-mode results](../evals/ollama-evaluation-results.json), and [JSON-mode results](../evals/ollama-json-evaluation-results.json) contain the prompts, responses, token counts, and timings.

## Run another comparison

Start a local Ollama service with `gemma4:12b` available, then run from a separate checkout:

```bash
python evals/ollama-evaluation.py
python evals/ollama-evaluation.py --json-mode
```

Both commands read `evals/skill-evaluation-results.json`. They use its saved rewrites rather than generating new ones. The commands overwrite `evals/ollama-evaluation-results.json` and `evals/ollama-json-evaluation-results.json`, respectively. Model installation may require downloading model files; these commands do not install it. Inspect the saved results, including failures.
