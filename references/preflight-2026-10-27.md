# Prompt & Cache-Readiness Optimizer: local preflight

This preflight, a local check before live testing, was generated on October 27, 2026 from the current documentation fixture. The saved prompt modules and comparison settings remain unchanged. See the [glossary](glossary.md) for technical terms.


Status: unvalidated  
Run type: local controlled structural preflight; no model inference  
Run UTC: 2026-10-27T19:54:41.598292+00:00  
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
Stable context SHA-256: `evidence.md:bcaee580b2a68f75f5d4f02973d1cd57353a29a71589fb8bd357c1a62601e62f`  
Run-manifest SHA-256: `14e3378cfc066def026d29a9312e5e38ece67d4b0a93e2e8dda38a4984749645`  
Source state: `Unavailable`  
Configured price snapshot: 2026-07-26, standard-tier requests at or below 272,000 input tokens  
Price source: https://developers.openai.com/api/docs/models/gpt-5.6-sol

This fixture deliberately puts dynamic input before stable evidence in Arm A to isolate prefix-order effects. Do not transfer its percentages to an existing stable-first baseline. Plain-text token counts omit API framing, tools, files, images, and structured-output schemas. Modeled fields assume the declared prefix is written once and read perfectly by later calls without eviction. Exact API tokens, output, cache telemetry, latency, quality, and safety were not run.

## Results

| Metric | A baseline | B optimized | B vs A | C telegraphic | C vs B |
|---|---:|---:|---:|---:|---:|
| UTF-8 bytes, measured | 17,504 | 18,581 | +6.2% | 18,329 | -1.4% |
| Plain-text token proxy | 3,504 | 3,696 | +5.5% | 3,660 | -1.0% |
| Potential cache writes, modeled proxy | 0 | 1,102 | N/A | 1,092 | N/A |
| Potential cached reads, modeled proxy | 0 | 2,204 | N/A | 2,184 | N/A |
| Processed uncached input, modeled proxy | 3,504 | 1,492 | -57.4% | 1,476 | -1.1% |
| Lifecycle input-equivalent, modeled proxy | 3,504 | 1987.900 | -43.3% | 1967.400 | -1.0% |
| Warm cache-read ratio, modeled proxy | 0.000 | 0.894 | N/A | 0.895 | N/A |
| Input-only cost, modeled perfect-hit scenario | $0.017520 | $0.009939 | -43.3% | $0.009837 | -1.0% |
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
| long-grounded-qa | B optimized | 3 | 5,520 | 1,102 | 1,106 | Yes | `4fc0cfbfbf23` |
| short-prompt-rewrite | B optimized | 3 | 392 | 69 | 73 | No | `a4d34a730599` |
| long-grounded-qa | C telegraphic | 3 | 5,447 | 1,092 | 1,096 | Yes | `d5597e40e305` |
| short-prompt-rewrite | C telegraphic | 3 | 381 | 67 | 71 | No | `1d6473bc92d7` |

## Interpretation

- Dynamic-input transport integrity only proves that declared literal strings survived assembly. It is not semantic parity or output quality.
- The bundled fixture covers prompt rewriting and grounded question answering only. Add production-representative extraction, tool or coding, and safety cases before rollout.
- A shorter prompt is not automatically faster. Output generation, service load, tools, and round trips can dominate latency.
- Arm C remains experimental even if smaller. Promote it only after paired target-model quality and safety evaluation.
- Run `references/benchmark-protocol.md` with the full API payload before making production claims.

## Reproduction and source context

Reproduce the measurements from repository root without overwriting a saved report:

```bash
python scripts/benchmark_prompts.py --require-tokenizer
```

The command ran in an isolated snapshot based on upstream commit 141d90dcf26e4164df7f11762852e2c7f02e7e38, with the 1.1.0 documentation changes applied before publication. Source state is unavailable because the snapshot had no local commit. The recorded input fingerprints identify the checked contents. This report adds the product heading and navigation around the generated measurements.
