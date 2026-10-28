# Small benchmark: baseline vs optimized prompts

> Historical record for **Prompt & Cache-Readiness Optimizer**, produced with earlier project instructions or settings. Recorded prompts, responses, scores, and settings are preserved. See the [current README](../README.md) and [glossary](glossary.md) for the maintained message and term definitions.

Status: unvalidated  
Run type: local controlled structural preflight; no model inference  
Run UTC: 2026-10-27T00:26:18.705492+00:00  
Benchmark version: 1.0.0  
Target for future live run: gpt-5.6-sol, standard tier  
Cache policy modeled: explicit mode, 30m TTL, one declared breakpoint per eligible family  
Python: 3.11.15  
Tokenizer: tiktoken 0.13.0, o200k_base  
Artifact version: 1.0.1  
Module versions: core-system@1.0.1:cbafd118acae, quality-safety-gate@1.0.0:9ffbaff5f6a0, output-contract@1.0.0:9da054b117f1  
Script SHA-256: `cae637200dbe77d464caba65e1c9b5c650a002c369d63360554fbf64c296d85d`  
Cases SHA-256: `508eeb026356cc18d287c2933f4ce36129152639dd4b170159b7cd40a1de8780`  
Manifest SHA-256: `9fe1b1734de672cc0d65a2b1ffed0053ba2ac726f2f18a2b60f0c96702e3b5b8`  
Stable context SHA-256: `evidence.md:e2ffbaf94e49d1cbea91e07956e4681f50f57bb7d76724666dff6c3b7048ff4c`  
Run-manifest SHA-256: `fd524727c7cddb0caccfdb7862df55fc2a1b8690b06706e756d4b53069ed5820`  
Source state: `Unavailable`  
Configured price snapshot: 2026-07-26, standard-tier requests at or below 272,000 input tokens  
Price source: https://developers.openai.com/api/docs/models/gpt-5.6-sol

This fixture deliberately puts dynamic input before stable evidence in Arm A to isolate prefix-order effects. Do not transfer its percentages to an existing stable-first baseline. Plain-text token counts omit API framing, tools, files, images, and structured-output schemas. Modeled fields assume the declared prefix is written once and read perfectly by later calls without eviction. Exact API tokens, output, cache telemetry, latency, quality, and safety were not run.

## Results

| Metric | A baseline | B optimized | B vs A | C telegraphic | C vs B |
|---|---:|---:|---:|---:|---:|
| UTF-8 bytes, measured | 22,286 | 23,363 | +4.8% | 23,111 | -1.1% |
| Plain-text token proxy | 4,902 | 5,094 | +3.9% | 5,058 | -0.7% |
| Potential cache writes, modeled proxy | 0 | 1,568 | N/A | 1,558 | N/A |
| Potential cached reads, modeled proxy | 0 | 3,136 | N/A | 3,116 | N/A |
| Processed uncached input, modeled proxy | 4,902 | 1,958 | -60.1% | 1,942 | -0.8% |
| Lifecycle input-equivalent, modeled proxy | 4,902 | 2663.600 | -45.7% | 2643.100 | -0.8% |
| Warm cache-read ratio, modeled proxy | 0.000 | 0.923 | N/A | 0.924 | N/A |
| Input-only cost, modeled perfect-hit scenario | $0.024510 | $0.013318 | -45.7% | $0.013215 | -0.8% |
| Dynamic-input transport integrity | 21/21 | 21/21 | Same | 21/21 | Same |
| Exact API input tokens | Not run | Not run | Not run | Not run | Not run |
| Actual processed uncached tokens | Not run | Not run | Not run | Not run | Not run |
| API output tokens | Not run | Not run | Not run | Not run | Not run |
| Observed cache efficiency | Not run | Not run | Not run | Not run | Not run |
| Observed total cost | Not run | Not run | Not run | Not run | Not run |
| TTFT and completion latency | Not run | Not run | Not run | Not run | Not run |
| Quality pass rate | Not run | Not run | Not run | Not run | Not run |
| Safety failures | Not run | Not run | Not run | Not run | Not run |

## Prefix structure by family

Eligibility uses the declared stable-prefix token proxy and a configured 1024-token threshold. Exact eligibility requires the full-payload input-token endpoint.

| Family | Arm | Calls | Declared prefix bytes | Declared prefix token proxy | Observed LCP token proxy | Eligible proxy | Prefix SHA-256 |
|---|---|---:|---:|---:|---:|---|---|
| long-grounded-qa | A baseline | 3 | 403 | 72 | 75 | No | `63098ebb4ac7` |
| short-prompt-rewrite | A baseline | 3 | 314 | 55 | 58 | No | `658980363bd3` |
| long-grounded-qa | B optimized | 3 | 7,114 | 1,568 | 1,572 | Yes | `6a6a862ac10a` |
| short-prompt-rewrite | B optimized | 3 | 392 | 69 | 73 | No | `a4d34a730599` |
| long-grounded-qa | C telegraphic | 3 | 7,041 | 1,558 | 1,562 | Yes | `bc9fc1f5056e` |
| short-prompt-rewrite | C telegraphic | 3 | 381 | 67 | 71 | No | `1d6473bc92d7` |

## Interpretation

- Dynamic-input transport integrity only proves that declared literal strings survived assembly. It is not semantic parity or output quality.
- The bundled fixture covers prompt rewriting and grounded question answering only. Add production-representative extraction, tool or coding, and safety cases before rollout.
- A shorter prompt is not automatically faster. Output generation, service load, tools, and round trips can dominate latency.
- Arm C remains experimental even if smaller. Promote it only after paired target-model quality and safety evaluation.
- Run `references/benchmark-protocol.md` with the full API payload before making production claims.

