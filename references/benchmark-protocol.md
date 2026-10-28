# Prompt & Cache-Readiness Optimizer: benchmark protocol

A benchmark is a planned comparison using defined tasks and measurements. Use this protocol after preparing the prompt and [provider-specific plan](cache-readiness-plan.md). Definitions are in [the glossary](glossary.md).

## Compare equivalent tasks

| Arm, or comparison condition | Definition |
|---|---|
| A: baseline | The existing readable prompt and assembly order |
| B: optimized | Preserved requirements, concise grammatical wording, reusable content first, changing input later |
| C: telegraphic | Optional further shortening of B; preserve every requirement and test separately |

Start with three changing inputs from each relevant task family for screening. Include short rewriting, structured extraction, grounded questions, tool or coding work, and safety or approval cases when they match the workflow. This small pilot can reject a candidate; it cannot establish production validation.

## Hold conditions constant

Record the provider and exact model version, settings, output limit, tools, output structure, service tier, software version, data-processing region, task cases, scoring rules, and saved module versions. A model snapshot is a specific saved version; an alias may change over time.

Check official provider documentation for cache grouping and boundaries. Keep comparison groups separate where supported. Do not assume a request is cold, meaning its content has not been cached, merely because it is first in a local block. Record whether a cold start can actually be established.

For a naturally eligible reusable prefix, compare initial preparation and later reuse. Alternate the order of conditions to reduce order effects. Do not pad the request solely to trigger caching.

## Record measurements

For each request, save:

- Input tokens, observed cached-read and cache-write tokens, output tokens, and reasoning tokens when reported.
- Time to first useful output and completion.
- Correctness, required-format checks, constraint coverage, and safety or authorization result.
- Model version, date, module fingerprints, request settings, current billing rates, and missing measurements.

A token is a piece of text counted by the model. Use full-request provider counts when available. Plain-text tokenizer estimates and character counts are separate measurements.

For a provider that reports total input `I`, cached reads `C`, and writes `W` as disjoint parts of that total:

```text
ordinary_uncached = I - C - W
processed_uncached = I - C
cost = (ordinary_uncached * input_rate
        + W * cache_write_rate
        + C * cached_read_rate
        + output_tokens * output_rate) / 1,000,000
```

Verify that accounting rule against the provider before using it. If write counts are split by lifetime, calculate each component at its corresponding rate without counting the combined write total again.

The bundled local fixture retains its historical modeling rule:

```text
input_equivalent_proxy = ordinary_uncached + 1.25W + 0.10C
```

That proxy uses the fixture's assumed rates. It is not a universal formula for current models or providers.

Include optimizer and evaluator calls, retries, and initial cache preparation. If one improvement call benefits `R` uses:

```text
amortized_cost(R) = optimizer_cost / R + optimized_runtime_cost
```

## Score quality and safety

Score correctness, constraint coverage, completeness and relevance, schema or tool validity, and safety or authorization from 0 to 2 each. A schema defines required output or input structure.

For each pilot output, require at least 9/10, no dimension at 0, no lower score than its paired baseline, all deterministic checks passing, and no new critical or safety failure. Use machine checks first, blinded comparison for open-ended answers, and human review for safety cases.

Reserve `validated` and production promotion for representative held-out cases, examples not used to develop the prompt, under a rule selected before testing. Record an uncertainty interval and require zero loss of required correctness, authorization, safety, or externally consumed output structure. Demonstrate a lower full-workflow cost or response time before claiming an efficiency improvement.

Promote optional C only when it also improves over B beyond measurement uncertainty and passes the same quality and safety requirements.

The recorded meeting-case wording mismatch illustrates why exact wording and preserved meaning should be scored deliberately. Keep historical scores unchanged; define any improved scoring rule before a new experiment.

## Report the result

Show A and B side by side, with optional C. Include input and output counts, initial writes, warm reads, full cost, response time, optimizer overhead, quality checks, and safety failures. Label each row as observed, modeled, or `Not run`.

Put limitations beside the affected measurement. Explain whether telemetry, system-reported usage, isolates the application's content. The existing Codex pilot includes surrounding context and cannot isolate framework-caused cache savings.
