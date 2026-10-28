# Prompt & Cache-Readiness Optimizer

**A framework for designing AI prompts that make better use of prompt caching. It provides methods for organizing reusable context, reducing changes that interrupt cache reuse, and measuring performance over repeated requests.**

A prompt is the instructions and context supplied to an AI model. **Prompt caching** lets a provider reuse saved processing for repeated text, so it may not need to process that text from scratch on every request. Think of asking several questions about the same long document: the shared document can stay at the beginning, while each new question comes later. This skill helps organize recurring prompts for that kind of reuse.

Caching can reduce processing time and input costs when a provider supports it and the requests qualify. Results depend on the service, model, pricing, and workload. Keeping the shared beginning of the prompt unchanged can help, but a cache hit is not guaranteed. 

I built the skill, a versioned prompt library, Python tools that check and assemble its contents, and experiments that compare prompt arrangements. The project shows how I turn a promising idea into a measurable workflow: define the requirements, test the result, investigate failures, and choose the next experiment based on the evidence.

## What you can accomplish

| Your task | What you receive |
|---|---|
| Improve a rough request | A clearer prompt that preserves required facts, constraints, format, and approval limits |
| Prepare recurring AI work | Reusable and changing content separated, plus changes that could interrupt cache reuse |
| Plan a provider-specific comparison | The model settings to verify, official sources, test cases, and measurements needed to assess performance |
| Maintain shared prompt pieces | Consistent assembly, saved versions, and fingerprints that detect content changes |

A fingerprint is a calculated value used to detect content changes. Other technical terms are defined in [the glossary](references/glossary.md).

## Quick start

You need Git and Python 3.10 or later. From a terminal:

```bash
git clone https://github.com/JaredIRivera/prompt-optimizer.git
cd prompt-optimizer
python scripts/compile_prompt_modules.py
python scripts/benchmark_prompts.py
```

The compiler checks the saved prompt pieces and prints a JSON build summary, a structured text record, with library version `1.0.1`, three modules, and their fingerprints. The second command prints a local comparison report. Both commands make no model calls and require no AI account.

Without the optional tokenizer, token estimates appear as `Not run`. A tokenizer counts the pieces of text a model processes. To include those estimates, install the pinned library in your chosen Python environment:

```bash
python -m pip install -r scripts/requirements.txt
python scripts/benchmark_prompts.py --require-tokenizer
```

Installing the library and its first-use token data may require internet access. The report separates measured text properties from modeled cache and cost estimates. This assembly check catches unexpected changes early; a live provider test is still needed to measure savings.

### Use the skill in your assistant

Keep the folder named `prompt-optimizer`, with `SKILL.md`, `agents/`, `references/`, and `scripts/` together. Install it in the skills directory used by your assistant. Current [Codex documentation](https://learn.chatgpt.com/docs/build-skills) lists `~/.agents/skills/prompt-optimizer/` for user-level discovery. Keep an existing installation in its configured location; the rebrand does not require a folder rename. Refresh or restart the assistant if it does not appear.

For a single request:

```text
Use $prompt-optimizer to improve the prompt below. Keep every required fact,
constraint, output format, and approval limit. Return the improved prompt
and identify any material assumption.

[Paste the prompt here]
```

For recurring work:

```text
Use $prompt-optimizer to prepare this recurring workflow. Separate reusable
context from changing input, identify changes that could interrupt caching,
and prepare a measurement plan for our provider and model. Explain necessary
technical terms in a short glossary.

Provider and model: [service and exact model]
Task and required output: [description]
Shared context: [instructions, reference material, and tools]
Changing input: [what differs between requests]
Frequency and data restrictions: [details]
```

## Working examples

### A recorded inventory rewrite

This example comes from the earlier skill's [saved prompts and responses](evals/skill-evaluation-results.json). It shows a complete transformation and its recorded output.

**Original prompt**

```text
Read the record and calculate the remaining quantity. Use valid JSON with exactly sku and remaining. Do not add fields. Record: SKU B-17, started with 80 units, sold 27, returned 3 units to stock.
```

**Skill-generated rewrite**

```text
Calculate remaining stock from the record. Return only valid JSON with exactly "sku" and "remaining".

Record: SKU B-17, started with 80 units, sold 27, returned 3 units to stock.
```

**Recorded output from both versions**

```json
{"sku":"B-17","remaining":56}
```

The SKU, quantities, required keys, and format survived this rewrite. Across the eight synthetic tasks, both versions passed **7/8** exact checks. [Method and limitations](references/skill-evaluation-2026-10-26.md)

### Prepare a recurring support workflow

This planning example shows how to apply the framework to a support workflow. It is illustrative; the recorded experiments are linked below.

- **Task:** Answer customer questions from an approved support policy.
- **Reusable context:** Approved response rules, policy text, and required answer format.
- **Changing input:** The current question and necessary account context.
- **Changes to flag:** A timestamp inserted before the shared rules, unnecessary policy rewrites, changing tool order, or repeatedly rewriting earlier conversation messages.
- **Prepared structure:** Keep authorized rules and policy data separate, put stable material first, and place each changing question later.
- **Provider-specific plan:** Verify the selected model's caching rules, compare the existing and revised requests on matched support cases, and record answer correctness, observed cache reuse, time, and full cost.

The [cache-readiness checklist](references/cache-readiness-plan.md) explains what the completed plan should contain.

## How it works and design choices

The workflow is: **capture requirements → clarify the prompt → separate reusable content → check the assembly → measure the result.**

| Choice | Why it matters | What the tradeoff teaches |
|---|---|---|
| Keep requirements while removing repetition | A clear request preserves the facts and rules needed to complete the task | Some good rewrites become longer, so compare task results and token counts rather than rewarding brevity alone |
| Keep reusable context consistent | Avoid unnecessary changes that can interrupt reuse | Reference updates still need deliberate version changes, giving teams a clear way to track when shared material changes |
| Verify saved modules before assembly | Unexpected changes become visible | Fingerprints require maintenance and cannot judge answers; pairing them with task checks covers both content changes and behavior |
| Prefer provider output controls for required formats | The Ollama experiment exposed the limits of asking for JSON through wording alone | Applications still need to check values and handle failures, so format controls are one layer of a dependable workflow |
| Measure full workflow cost | Initial cache preparation and optimization can outweigh later reuse | A useful comparison takes more work than counting characters, but shows whether the whole process earns its cost |

The skill instructions are in [SKILL.md](SKILL.md). The [specification](SPEC.md) defines inputs, outputs, and safeguards.

## Recorded results

The experiments below tested earlier instructions; version 1.1.0 has not yet been rerun through the model experiments. Keeping the original results makes the design decisions traceable and provides a baseline for the next comparison.

| Experiment | Recorded observation | What I learned and would test next |
|---|---|---|
| [Direct skill evaluation](references/skill-evaluation-2026-10-26.md) | Original and rewritten prompts each passed 7/8 exact checks | Eight synthetic cases and one trial per version give an initial comparison. New, unseen cases and repeated trials would test whether it holds more broadly. |
| [Local Ollama comparison](references/ollama-evaluation-2026-10-26.md) | JSON mode improved exact checks from 0/8 to 7/8 per version; rewritten inputs used 5.4% more tokens | Shorter wording did not mean fewer tokens here. Measuring the model's actual token counts and the entire workflow is necessary before claiming savings. |
| [Repeated-workload cache pilot](references/cache-workload-2026-10-26.md) | Both arrangements returned 12/12 correct answers; stable-first reported 195,584 cached input tokens versus 188,160 | Codex's own context is included, so the difference cannot be attributed to the skill. The pilot identifies the need for a controlled provider test that can trace the reused text and measure cost. |
| [Current local preflight](references/preflight-2026-10-27.md) | Checks saved modules, prompt assembly, retained literal strings, and modeled scenarios | It makes no model calls. That makes it a useful low-cost check before a live evaluation of cache use, answer quality, time, and cost. |

The direct evaluation's remaining failure used a correct meaning with different wording. I kept the original 7/8 score and identified a better next step: define semantic checks before the next run, rather than changing the scoring after seeing the answers. The [earlier hand-written comparison](references/codex-comparison-2026-10-26.md) did not invoke the skill, so it is labeled separately. Historical modeled savings describe their fixture and assumptions, giving readers a way to inspect the calculation without mistaking it for a production result.

## Running checks and experiments

A preflight is a check performed before a live experiment. A benchmark is a planned comparison with defined tasks and measurements.

| Command, from repository root | Requirements and behavior |
|---|---|
| `python scripts/compile_prompt_modules.py` | Standard library; checks fingerprints and prints a build summary |
| `python scripts/benchmark_prompts.py` | No model calls; optional token estimates; prints a report |
| `python evals/skill-evaluation.py` | Signed-in Codex CLI; uses its allowance; rewrites eight cases and runs both versions; overwrites `evals/skill-evaluation-results.json` |
| `python evals/cache-workload.py` | Signed-in Codex CLI; uses its allowance; runs 24 requests; overwrites its results file |
| `python evals/codex-comparison.py` | Signed-in Codex CLI; uses its allowance; runs 40 requests using a hand-written revision; overwrites its results file |
| `python evals/ollama-evaluation.py` | Running Ollama service and `gemma4:12b`; reads the saved skill evaluation; overwrites default-mode results |
| `python evals/ollama-evaluation.py --json-mode` | Same prerequisites; overwrites JSON-mode results |

Run experiments in a separate checkout to preserve published records. The evaluation scripts save individual pass/fail results, but their process exit status does not enforce an overall passing score. Review the saved cases directly. A dedicated unit-test suite and automated checks on code changes are future steps for catching regressions more reliably.

Use [the benchmark protocol](references/benchmark-protocol.md) for provider-level measurements and acceptance criteria. Check provider documentation and available allowance before live runs.

## Project status and next decisions

The skill prepares prompts and measurement plans; the selected provider controls cache behavior. This separation makes the framework useful across services while keeping the measurement plan specific to the model, workload, and pricing being tested.

The examples do not demonstrate a deployed business integration. Approvals, spending limits, retries, and duplicate-action prevention need enforcement in application code. Naming those boundaries gives an implementation team a practical starting point for adding controls where they can be enforced.

The next evidence milestone is to rerun the current skill on unseen cases, verify installation and discovery, and measure cache use, answer quality, and full cost in a representative workflow. Those checks would show where the approach is ready to use and where it needs revision.

Keep secrets and unnecessary personal or client information out of examples, reusable instructions, and logs. Review retention and data-location requirements before reusing sensitive content. The local scripts do not send prompts to a model; live experiments use the selected service or local model.

Maintained by Jared Rivera. Report issues through GitHub; no external support commitment is stated. No license has been selected; contact the owner before reuse or redistribution. See [release notes](RELEASE_NOTES.md) for remaining production checks.

## Glossary

Use [the shared glossary](references/glossary.md) for definitions of cache readiness, reusable prefixes, tokens, fingerprints, model settings, and evaluation terms.
