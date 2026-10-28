#!/usr/bin/env python3
"""Run a local structural preflight for prompt variants.

No model is called. Token counts are a named plain-text proxy when tiktoken is
installed. Cache reads, cost, and uncached processing are modeled only from an
explicit, declared stable-prefix boundary.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import platform
import re
import subprocess
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Iterable


SKILL_ROOT = Path(__file__).resolve().parents[1]
REFERENCES = SKILL_ROOT / "references"
MODULES = REFERENCES / "prompt-modules"
DEFAULT_CASES = REFERENCES / "benchmark-cases.json"
MANIFEST_PATH = MODULES / "manifest.json"


@dataclass(frozen=True)
class RenderedPrompt:
    family: str
    arm: str
    request_index: int
    stable_prefix: str
    text: str
    required_literals: tuple[str, ...]


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def normalize_text(text: str) -> str:
    return "\n".join(
        line.rstrip()
        for line in text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    ).strip()


def normalized_module_bytes(path: Path, kind: str) -> bytes:
    if kind == "json" or path.suffix.lower() == ".json":
        value = json.loads(path.read_text(encoding="utf-8"))
        return (
            json.dumps(
                value,
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
            )
            + "\n"
        ).encode("utf-8")
    if kind != "text":
        raise ValueError(f"Unsupported module kind: {kind}")
    return normalize_text(path.read_text(encoding="utf-8")).encode("utf-8")


def load_modules(selected_ids: Iterable[str]) -> str:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    items = manifest["stable_order"]
    item_ids = [item["id"] for item in items]
    if len(item_ids) != len(set(item_ids)):
        raise ValueError("Duplicate module ids in manifest")

    selected = list(selected_ids)
    if len(selected) != len(set(selected)):
        raise ValueError("Duplicate selected module ids")
    unknown = sorted(set(selected) - set(item_ids))
    if unknown:
        raise ValueError(f"Unknown module ids: {', '.join(unknown)}")

    compiled: list[str] = []
    for item in items:
        if item["id"] not in selected:
            continue
        path = (MODULES / item["path"]).resolve()
        if not path.is_relative_to(MODULES.resolve()) or not path.is_file():
            raise ValueError(f"Invalid module path: {item['path']}")
        content = normalized_module_bytes(path, item.get("kind", "text"))
        actual = sha256_bytes(content)
        if item.get("sha256") != actual:
            raise ValueError(
                f"Hash mismatch for {item['id']}; use compile_prompt_modules.py "
                "to review and accept a versioned change"
            )
        compiled.append(content.decode("utf-8").rstrip("\n"))
    return "\n\n".join(compiled)


def read_context(cases_root: Path, relative: str | None) -> str:
    if not relative:
        return ""
    path = (cases_root / relative).resolve()
    if not path.is_relative_to(cases_root.resolve()) or not path.is_file():
        raise ValueError(f"Invalid stable_context_path: {relative}")
    return normalize_text(path.read_text(encoding="utf-8"))


def render_prompts(
    config: dict[str, Any], cases_root: Path
) -> list[RenderedPrompt]:
    rendered: list[RenderedPrompt] = []
    for family in config["families"]:
        modules = load_modules(family.get("stable_module_ids", []))
        context = read_context(cases_root, family.get("stable_context_path"))

        stable_a = normalize_text(family["baseline_contract"])
        stable_b = "\n\n".join(
            part
            for part in [
                modules,
                normalize_text(family["optimized_contract"]),
                f"SUPPLIED EVIDENCE\n{context}" if context else "",
            ]
            if part
        )
        stable_c = "\n\n".join(
            part
            for part in [
                modules,
                normalize_text(family["telegraphic_contract"]),
                f"SUPPLIED EVIDENCE\n{context}" if context else "",
            ]
            if part
        )

        for index, request in enumerate(family["requests"], start=1):
            dynamic = request["text"]
            literals = tuple(request.get("required_literals", []))
            baseline_parts = [stable_a, f"USER REQUEST\n{dynamic}"]
            if context:
                baseline_parts.append(f"SUPPLIED EVIDENCE\n{context}")

            variants = {
                "A baseline": (
                    stable_a,
                    "\n\n".join(baseline_parts),
                ),
                "B optimized": (
                    stable_b,
                    f"{stable_b}\n\nDYNAMIC INPUT\n{dynamic}",
                ),
                "C telegraphic": (
                    stable_c,
                    f"{stable_c}\n\nDYNAMIC INPUT\n{dynamic}",
                ),
            }
            for arm, (stable_prefix, text) in variants.items():
                if not text.startswith(stable_prefix):
                    raise ValueError(f"{family['id']} {arm} prefix mismatch")
                rendered.append(
                    RenderedPrompt(
                        family=family["id"],
                        arm=arm,
                        request_index=index,
                        stable_prefix=stable_prefix,
                        text=text,
                        required_literals=literals,
                    )
                )
    return rendered


def longest_common_prefix_bytes(values: Iterable[str]) -> bytes:
    encoded = [value.encode("utf-8") for value in values]
    if not encoded:
        return b""
    first = min(encoded)
    last = max(encoded)
    index = 0
    limit = min(len(first), len(last))
    while index < limit and first[index] == last[index]:
        index += 1
    return first[:index]


def longest_common_prefix_tokens(
    values: Iterable[str], encode: Callable[[str], list[int]]
) -> int:
    sequences = [encode(value) for value in values]
    if not sequences:
        return 0
    index = 0
    limit = min(len(sequence) for sequence in sequences)
    while index < limit and all(
        sequence[index] == sequences[0][index] for sequence in sequences[1:]
    ):
        index += 1
    return index


def optional_tokenizer(
    encoding_name: str,
) -> tuple[Callable[[str], list[int]] | None, str]:
    try:
        import tiktoken  # type: ignore
    except ImportError:
        return None, "Not available"
    encoding = tiktoken.get_encoding(encoding_name)
    version = importlib.metadata.version("tiktoken")
    return encoding.encode, f"tiktoken {version}, {encoding_name}"


def aggregate(
    prompts: list[RenderedPrompt],
    config: dict[str, Any],
    encode: Callable[[str], list[int]] | None,
) -> dict[str, dict[str, Any]]:
    cache_minimum = int(config["cache_minimum_tokens"])
    prices = config["prices_per_million_tokens"]
    arms = sorted({prompt.arm for prompt in prompts})
    families = sorted({prompt.family for prompt in prompts})
    result: dict[str, dict[str, Any]] = {}

    for arm in arms:
        arm_prompts = [prompt for prompt in prompts if prompt.arm == arm]
        data: dict[str, Any] = {
            "utf8_bytes": sum(len(prompt.text.encode("utf-8")) for prompt in arm_prompts),
            "proxy_tokens": None,
            "transport_checks": sum(
                1
                for prompt in arm_prompts
                for literal in prompt.required_literals
                if literal in prompt.text
            ),
            "transport_total": sum(
                len(prompt.required_literals) for prompt in arm_prompts
            ),
            "potential_cached_reads": None,
            "potential_cache_writes": None,
            "processed_uncached_proxy": None,
            "input_equivalent_proxy": None,
            "warm_read_ratio_proxy": None,
            "modeled_input_cost": None,
            "families": {},
        }
        if encode:
            data["proxy_tokens"] = sum(len(encode(prompt.text)) for prompt in arm_prompts)
            data["potential_cached_reads"] = 0
            data["potential_cache_writes"] = 0
            data["processed_uncached_proxy"] = data["proxy_tokens"]
            data["input_equivalent_proxy"] = data["proxy_tokens"]
            input_cost = 0.0
            warm_input_tokens = 0

        for family in families:
            group = [prompt for prompt in arm_prompts if prompt.family == family]
            stable_prefixes = {prompt.stable_prefix for prompt in group}
            if len(stable_prefixes) != 1:
                raise ValueError(f"Unstable declared prefix: {family} {arm}")
            stable_prefix = next(iter(stable_prefixes))
            texts = [prompt.text for prompt in group]
            lcp_bytes = longest_common_prefix_bytes(texts)
            family_data: dict[str, Any] = {
                "prompt_count": len(group),
                "declared_prefix_bytes": len(stable_prefix.encode("utf-8")),
                "observed_lcp_bytes": len(lcp_bytes),
                "declared_prefix_sha256": sha256_bytes(
                    stable_prefix.encode("utf-8")
                ),
                "declared_prefix_proxy_tokens": None,
                "observed_lcp_proxy_tokens": None,
                "cache_eligible_proxy": None,
            }

            if encode:
                token_counts = [len(encode(prompt.text)) for prompt in group]
                prefix_tokens = len(encode(stable_prefix))
                observed_lcp_tokens = longest_common_prefix_tokens(texts, encode)
                if prefix_tokens > observed_lcp_tokens:
                    raise ValueError(f"Declared prefix exceeds observed LCP: {family} {arm}")
                eligible = prefix_tokens >= cache_minimum
                family_data.update(
                    {
                        "declared_prefix_proxy_tokens": prefix_tokens,
                        "observed_lcp_proxy_tokens": observed_lcp_tokens,
                        "cache_eligible_proxy": eligible,
                    }
                )
                warm_input_tokens += sum(token_counts[1:])

                if eligible:
                    reads = prefix_tokens * max(0, len(group) - 1)
                    writes = prefix_tokens
                    data["potential_cached_reads"] += reads
                    data["potential_cache_writes"] += writes
                    data["processed_uncached_proxy"] -= reads
                    data["input_equivalent_proxy"] += (
                        0.25 * writes - 0.90 * reads
                    )

                    first_tail = token_counts[0] - prefix_tokens
                    input_cost += (
                        writes * prices["cache_write"]
                        + first_tail * prices["uncached_input"]
                    ) / 1_000_000
                    for token_count in token_counts[1:]:
                        input_cost += (
                            prefix_tokens * prices["cached_read"]
                            + (token_count - prefix_tokens)
                            * prices["uncached_input"]
                        ) / 1_000_000
                else:
                    input_cost += (
                        sum(token_counts) * prices["uncached_input"]
                    ) / 1_000_000

            data["families"][family] = family_data

        if encode:
            data["warm_read_ratio_proxy"] = (
                data["potential_cached_reads"] / warm_input_tokens
                if warm_input_tokens
                else 0.0
            )
            data["modeled_input_cost"] = input_cost
        result[arm] = data
    return result


def percent_delta(candidate: float, baseline: float) -> str:
    if baseline == 0:
        return "N/A"
    return f"{((candidate - baseline) / baseline) * 100:+.1f}%"


def number(value: int | float | None) -> str:
    if value is None:
        return "Not run"
    if isinstance(value, float):
        return f"{value:.3f}"
    return f"{value:,}"


def money(value: float | None) -> str:
    return "Not run" if value is None else f"${value:.6f}"


def best_effort_source_state() -> str:
    try:
        root = subprocess.run(
            ["git", "-C", str(SKILL_ROOT), "rev-parse", "--show-toplevel"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        commit = subprocess.run(
            ["git", "-C", root, "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        dirty = subprocess.run(
            ["git", "-C", root, "status", "--porcelain", "--", str(SKILL_ROOT)],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        return f"{commit}{'+dirty' if dirty else ''}"
    except (OSError, subprocess.SubprocessError):
        return "Unavailable"


def provenance(config: dict[str, Any], cases_path: Path) -> dict[str, Any]:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    context_hashes: dict[str, str] = {}
    for family in config["families"]:
        relative = family.get("stable_context_path")
        if relative:
            path = (cases_path.parent / relative).resolve()
            context_hashes[relative] = sha256_file(path)
    run = {
        "run_utc": datetime.now(timezone.utc).isoformat(),
        "script_sha256": sha256_file(Path(__file__).resolve()),
        "cases_sha256": sha256_file(cases_path),
        "manifest_sha256": sha256_file(MANIFEST_PATH),
        "artifact_version": manifest["artifact_version"],
        "module_versions": ", ".join(
            f"{item['id']}@{item['version']}:{item['sha256'][:12]}"
            for item in manifest["stable_order"]
        ),
        "context_hashes": context_hashes,
        "source_state": best_effort_source_state(),
    }
    run["run_manifest_sha256"] = sha256_bytes(
        json.dumps(
            run,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    )
    return run


def render_report(
    config: dict[str, Any],
    summary: dict[str, dict[str, Any]],
    tokenizer_label: str,
    run: dict[str, Any],
) -> str:
    baseline = summary["A baseline"]
    optimized = summary["B optimized"]
    telegraphic = summary["C telegraphic"]
    context_summary = ", ".join(
        f"{path}:{value}" for path, value in run["context_hashes"].items()
    ) or "None"

    def delta(key: str, candidate: dict[str, Any], reference: dict[str, Any]) -> str:
        if candidate[key] is None or reference[key] is None:
            return "Not run"
        return percent_delta(candidate[key], reference[key])

    lines = [
        "# Small benchmark: baseline vs optimized prompts",
        "",
        "Status: unvalidated  ",
        "Run type: local controlled structural preflight; no model inference  ",
        f"Run UTC: {run['run_utc']}  ",
        f"Benchmark version: {config['benchmark_version']}  ",
        f"Target for future live run: {config['model_for_live_run']}, {config['service_tier']} tier  ",
        f"Cache policy modeled: {config['cache_policy']['mode']} mode, {config['cache_policy']['ttl']} TTL, one declared breakpoint per eligible family  ",
        f"Python: {platform.python_version()}  ",
        f"Tokenizer: {tokenizer_label}  ",
        f"Artifact version: {run['artifact_version']}  ",
        f"Module versions: {run['module_versions']}  ",
        f"Script SHA-256: `{run['script_sha256']}`  ",
        f"Cases SHA-256: `{run['cases_sha256']}`  ",
        f"Manifest SHA-256: `{run['manifest_sha256']}`  ",
        f"Stable context SHA-256: `{context_summary}`  ",
        f"Run-manifest SHA-256: `{run['run_manifest_sha256']}`  ",
        f"Source state: `{run['source_state']}`  ",
        f"Configured price snapshot: {config['price_snapshot_date']}, {config['pricing_scope']}  ",
        f"Price source: {config['price_source_url']}",
        "",
        "This fixture deliberately puts dynamic input before stable evidence in Arm A to isolate prefix-order effects. Do not transfer its percentages to an existing stable-first baseline. Plain-text token counts omit API framing, tools, files, images, and structured-output schemas. Modeled fields assume the declared prefix is written once and read perfectly by later calls without eviction. Exact API tokens, output, cache telemetry, latency, quality, and safety were not run.",
        "",
        "## Results",
        "",
        "| Metric | A baseline | B optimized | B vs A | C telegraphic | C vs B |",
        "|---|---:|---:|---:|---:|---:|",
        f"| UTF-8 bytes, measured | {number(baseline['utf8_bytes'])} | {number(optimized['utf8_bytes'])} | {delta('utf8_bytes', optimized, baseline)} | {number(telegraphic['utf8_bytes'])} | {delta('utf8_bytes', telegraphic, optimized)} |",
        f"| Plain-text token proxy | {number(baseline['proxy_tokens'])} | {number(optimized['proxy_tokens'])} | {delta('proxy_tokens', optimized, baseline)} | {number(telegraphic['proxy_tokens'])} | {delta('proxy_tokens', telegraphic, optimized)} |",
        f"| Potential cache writes, modeled proxy | {number(baseline['potential_cache_writes'])} | {number(optimized['potential_cache_writes'])} | N/A | {number(telegraphic['potential_cache_writes'])} | N/A |",
        f"| Potential cached reads, modeled proxy | {number(baseline['potential_cached_reads'])} | {number(optimized['potential_cached_reads'])} | N/A | {number(telegraphic['potential_cached_reads'])} | N/A |",
        f"| Processed uncached input, modeled proxy | {number(baseline['processed_uncached_proxy'])} | {number(optimized['processed_uncached_proxy'])} | {delta('processed_uncached_proxy', optimized, baseline)} | {number(telegraphic['processed_uncached_proxy'])} | {delta('processed_uncached_proxy', telegraphic, optimized)} |",
        f"| Lifecycle input-equivalent, modeled proxy | {number(baseline['input_equivalent_proxy'])} | {number(optimized['input_equivalent_proxy'])} | {delta('input_equivalent_proxy', optimized, baseline)} | {number(telegraphic['input_equivalent_proxy'])} | {delta('input_equivalent_proxy', telegraphic, optimized)} |",
        f"| Warm cache-read ratio, modeled proxy | {number(baseline['warm_read_ratio_proxy'])} | {number(optimized['warm_read_ratio_proxy'])} | N/A | {number(telegraphic['warm_read_ratio_proxy'])} | N/A |",
        f"| Input-only cost, modeled perfect-hit scenario | {money(baseline['modeled_input_cost'])} | {money(optimized['modeled_input_cost'])} | {delta('modeled_input_cost', optimized, baseline)} | {money(telegraphic['modeled_input_cost'])} | {delta('modeled_input_cost', telegraphic, optimized)} |",
        f"| Dynamic-input transport integrity | {baseline['transport_checks']}/{baseline['transport_total']} | {optimized['transport_checks']}/{optimized['transport_total']} | Same | {telegraphic['transport_checks']}/{telegraphic['transport_total']} | Same |",
        "| Exact API input tokens | Not run | Not run | Not run | Not run | Not run |",
        "| Actual processed uncached tokens | Not run | Not run | Not run | Not run | Not run |",
        "| API output tokens | Not run | Not run | Not run | Not run | Not run |",
        "| Observed cache efficiency | Not run | Not run | Not run | Not run | Not run |",
        "| Observed total cost | Not run | Not run | Not run | Not run | Not run |",
        "| TTFT and completion latency | Not run | Not run | Not run | Not run | Not run |",
        "| Quality pass rate | Not run | Not run | Not run | Not run | Not run |",
        "| Safety failures | Not run | Not run | Not run | Not run | Not run |",
        "",
        "## Prefix structure by family",
        "",
        f"Eligibility uses the declared stable-prefix token proxy and a configured {config['cache_minimum_tokens']}-token threshold. Exact eligibility requires the full-payload input-token endpoint.",
        "",
        "| Family | Arm | Calls | Declared prefix bytes | Declared prefix token proxy | Observed LCP token proxy | Eligible proxy | Prefix SHA-256 |",
        "|---|---|---:|---:|---:|---:|---|---|",
    ]
    for arm, arm_data in summary.items():
        for family, data in arm_data["families"].items():
            eligible = data["cache_eligible_proxy"]
            eligible_text = "Not run" if eligible is None else ("Yes" if eligible else "No")
            lines.append(
                f"| {family} | {arm} | {data['prompt_count']} | "
                f"{data['declared_prefix_bytes']:,} | "
                f"{number(data['declared_prefix_proxy_tokens'])} | "
                f"{number(data['observed_lcp_proxy_tokens'])} | "
                f"{eligible_text} | `{data['declared_prefix_sha256'][:12]}` |"
            )

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- Dynamic-input transport integrity only proves that declared literal strings survived assembly. It is not semantic parity or output quality.",
            "- The bundled fixture covers prompt rewriting and grounded question answering only. Add production-representative extraction, tool or coding, and safety cases before rollout.",
            "- A shorter prompt is not automatically faster. Output generation, service load, tools, and round trips can dominate latency.",
            "- Arm C remains experimental even if smaller. Promote it only after paired target-model quality and safety evaluation.",
            "- Run `references/benchmark-protocol.md` with the full API payload before making production claims.",
            "",
        ]
    )
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cases", type=Path, default=DEFAULT_CASES)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--require-tokenizer", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    cases_path = args.cases.resolve()
    config = json.loads(cases_path.read_text(encoding="utf-8"))
    if config.get("cache_policy", {}).get("mode") != "explicit":
        raise ValueError("The modeled cache scenario requires explicit mode")

    prompts = render_prompts(config, cases_path.parent)
    encode, tokenizer_label = optional_tokenizer(config["local_tokenizer_encoding"])
    if args.require_tokenizer and encode is None:
        raise RuntimeError(
            "tiktoken is required for token and cost proxies; install "
            "scripts/requirements.txt"
        )
    summary = aggregate(prompts, config, encode)
    report = render_report(
        config,
        summary,
        tokenizer_label,
        provenance(config, cases_path),
    )

    if args.output:
        output = args.output.resolve()
        if output.exists() and not args.overwrite:
            raise FileExistsError(f"Refusing to overwrite without --overwrite: {output}")
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(report, encoding="utf-8", newline="\n")
        print(output)
    else:
        print(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
