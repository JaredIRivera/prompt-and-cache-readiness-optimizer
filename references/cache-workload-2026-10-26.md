# Repeated-workload cache experiment: October 26, 2026

> Historical record for **Prompt & Cache-Readiness Optimizer**, produced with earlier project instructions or settings. Recorded prompts, responses, scores, and settings are preserved. See the [current README](../README.md) and [glossary](glossary.md) for the maintained message and term definitions.

I compared two ways to arrange the same instructions, records, and changing task across a repeated workload. The goal was to observe whether the reported cache use differed when the reusable material came before the changing request.

## Results

| Measure across 12 requests | Changing request first | Reusable records first |
|---|---:|---:|
| Correct JSON answers | 12/12 | 12/12 |
| Total input tokens reported | 295,973 | 295,944 |
| Input tokens reported as cached | 188,160 | 195,584 |
| Cached share of reported input | 63.6% | 66.1% |
| Reported cache-write input tokens | 0 | 0 |

Every request reported a nonzero number of cached input tokens. The stable-first arrangement reported 7,424 more cached tokens across the 12 requests, about 2.5 percentage points more of the total input. Cache counts varied between requests in both groups.

These are observed Codex usage figures, not a measured dollar saving. The usage totals include Codex's own instructions and other request context; the telemetry does not identify which specific text was cached. The result therefore does not establish that the reusable records caused the difference.

## How the test worked

A synthetic set of 100 records was used for 12 matching retrieval tasks. Each task asked for one record's ID and amount in JSON. Both arrangements had the same records, instructions, and tasks. One placed the changing task before the records; the other placed it after them, following the skill's stable-first principle.

I ran 24 separate, serial Codex sessions using `gpt-6.1-sol`, in three blocks of four requests per arrangement. The order of the blocks alternated. Each response was checked against the expected JSON. The cache was not cleared between requests; the first request in each block cannot be assumed to be a cold cache write.

The [script](../evals/cache-workload.py) and [recorded answers and usage](../evals/cache-workload-results.json) include the data and results. Running the script requires a signed-in Codex CLI and uses its account allowance.

## Limits

This is a small synthetic pilot of repeated requests, not a single long-running conversation or a production workload. The instructions were arranged manually using the skill's principles; the skill was not invoked to generate them. There was one trial per task and arrangement, no held-out data, and no controlled cache key, guaranteed cold start, or item-level cache tracing.

Codex's reported cache use includes its own request prefix. Cache reads for the shared system context may account for some or all of the difference. Timing, actual billing, production accuracy, and the cost of generating an optimized prompt were not established. The zero cache-write values are what Codex reported and should not be treated as proof of the provider's full write economics.

A stronger cost test would use an API where the complete request, cache key, cold writes, warm reads, model settings, and billing rates can be controlled and measured. Compare equivalent requests with and without repeatable prefix reuse across realistic long-running tasks, repeat the trials, and include the cost of creating the optimized prompt.

## Run another comparison

From a separate checkout with a signed-in Codex CLI:

```bash
python evals/cache-workload.py
```

This uses account allowance for 24 requests and overwrites `evals/cache-workload-results.json`. Inspect individual answers and reported usage. The script does not establish a cold cache or enforce an overall passing process status. Keep the original published data when recording a new run.
