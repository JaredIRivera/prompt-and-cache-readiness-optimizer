# Small benchmark: baseline vs optimized prompts

> Historical record for **Prompt & Cache-Readiness Optimizer**, produced with earlier project instructions or settings. Recorded prompts, responses, scores, and settings are preserved. See the [current README](../README.md) and [glossary](glossary.md) for the maintained message and term definitions.

Status: unvalidated  
Run type: local controlled structural preflight; no model inference  
Run UTC: 2026-07-27T03:15:31.230472+00:00  
Benchmark version: 1.0.0  
Target for future live run: gpt-5.6-sol, standard tier  
Cache policy modeled: explicit mode, 30m TTL, one declared breakpoint per eligible family  
Python: 3.11.15  
Tokenizer: tiktoken 0.13.0, o200k_base  
Artifact version: 1.0.0  
Module versions: core-system@1.0.0:dca783df8a98, quality-safety-gate@1.0.0:9ffbaff5f6a0, output-contract@1.0.0:9da054b117f1  
Script SHA-256: `2b9995b17531001686e37ec638328a8222c2552832c250e1be8a930150145d78`  
Cases SHA-256: `508eeb026356cc18d287c2933f4ce36129152639dd4b170159b7cd40a1de8780`  
Manifest SHA-256: `8ef2a200f5e4dab45b209abe719640e913c3edf7a19731c032ab6b54bf00e2a5`  
Source state: `a07b24bd7bc12faa11d210c2f52107b6767fd8e4+dirty`  
Configured price snapshot: 2026-07-26, standard-tier requests at or below 272,000 input tokens  
Price source: https://developers.openai.com/api/docs/models/gpt-5.6-sol

This fixture deliberately puts dynamic input before stable evidence in Arm A to isolate prefix-order effects. Do not transfer its percentages to an existing stable-first baseline. Plain-text token counts omit API framing, tools, files, images, and structured-output schemas. Modeled fields assume the declared prefix is written once and read perfectly by later calls without eviction. Exact API tokens, output, cache telemetry, latency, quality, and safety were not run.

## Results

| Metric | A baseline | B optimized | B vs A | C telegraphic | C vs B |
|---|---:|---:|---:|---:|---:|
| UTF-8 bytes, measured | 21,299 | 21,740 | +2.1% | 21,488 | -1.2% |
| Plain-text token proxy | 4,692 | 4,770 | +1.7% | 4,734 | -0.8% |
| Potential cache writes, modeled proxy | 0 | 1,479 | N/A | 1,469 | N/A |
| Potential cached reads, modeled proxy | 0 | 2,958 | N/A | 2,938 | N/A |
| Processed uncached input, modeled proxy | 4,692 | 1,812 | -61.4% | 1,796 | -0.9% |
| Lifecycle input-equivalent, modeled proxy | 4,692 | 2477.550 | -47.2% | 2457.050 | -0.8% |
| Warm cache-read ratio, modeled proxy | 0.000 | 0.930 | N/A | 0.931 | N/A |
| Input-only cost, modeled perfect-hit scenario | $0.023460 | $0.012388 | -47.2% | $0.012285 | -0.8% |
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
| long-grounded-qa | B optimized | 3 | 6,679 | 1,479 | 1,483 | Yes | `4c53e034f64c` |
| short-prompt-rewrite | B optimized | 3 | 286 | 50 | 54 | No | `085e35448b5b` |
| long-grounded-qa | C telegraphic | 3 | 6,606 | 1,469 | 1,473 | Yes | `ea07ea9c3b80` |
| short-prompt-rewrite | C telegraphic | 3 | 275 | 48 | 52 | No | `70885865c32f` |

## Interpretation

- Dynamic-input transport integrity only proves that declared literal strings survived assembly. It is not semantic parity or output quality.
- The bundled fixture covers prompt rewriting and grounded question answering only. Add production-representative extraction, tool or coding, and safety cases before rollout.
- A shorter prompt is not automatically faster. Output generation, service load, tools, and round trips can dominate latency.
- Arm C remains experimental even if smaller. Promote it only after paired target-model quality and safety evaluation.
- Run `references/benchmark-protocol.md` with the full API payload before making production claims.
