# Prompt & Cache-Readiness Optimizer: release notes

Technical terms are defined in [the glossary](references/glossary.md).

## 1.1.0: clearer prompts and cache-readiness planning

Turn rough requests into clear, efficient prompts. For recurring AI workflows, identify reusable context, reduce cache-breaking changes, and get a provider-specific plan for measuring cache performance.

- Introduces the new display name and two explicit usage paths: single-prompt improvement and recurring-workflow preparation.
- Keeps `$prompt-optimizer`, the repository URL, folder name, and internal identifiers compatible.
- Adds a shared glossary and a provider-plan checklist.
- Reorganizes setup, examples, design choices, experiment reproduction, and evidence in the README.
- Refreshes provider guidance while keeping model-specific examples clearly identified.
- Preserves historical prompts, responses, scores, experiment settings, and saved prompt modules.

The repository includes small Codex and Ollama model evaluations. They establish feasibility on their recorded cases; production validation and attributed cost savings remain open measurements. The 1.1.0 instructions have not been rerun through those model experiments.

## Historical 1.0.0 evidence

On October 26, 2026, the compiler and local comparison stopped because the `core-system` module did not match its recorded fingerprint. The earlier matching file could not be recovered. The preserved content was registered as module version 1.0.1 with a new fingerprint and module-library version. The original provenance remains unresolved; the historical benchmark describes a different saved module version.

Eight skill-generated rewrites were compared with their originals. Both versions passed 7/8 exact-output checks. The remaining case used a semantically equivalent phrase in both versions. See [the direct evaluation](references/skill-evaluation-2026-10-26.md), [the Ollama formatting lesson](references/ollama-evaluation-2026-10-26.md), and [the cache pilot](references/cache-workload-2026-10-26.md).

## Before a production release

- [ ] Define the real workflow, permissions, data handling, and acceptance criteria.
- [ ] Test installation and skill discovery in the intended assistant.
- [ ] Run representative and held-out paired model comparisons, including safety cases, using an authorized budget.
- [ ] Record exact source versions, date, model, settings, cases, trials, failures, timing, and actual cost.
- [ ] Include optimization overhead and initial cache preparation in the comparison.
- [ ] Test the consuming application's spending limits, retries, duplicate-action prevention, and approvals.
- [ ] Confirm the examples match the tested implementation and establish support expectations.

Add a regression check when a real failure is confirmed. Preserve historical scores rather than changing the scoring rule after seeing the answers.
