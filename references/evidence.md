# Prompt & Cache-Readiness Optimizer: evidence and operating assumptions

Provider guidance and the linked research abstracts were checked on October 27, 2026. This maintained reference is also input to the local sample comparison; changing it changes that fixture. Historical reports retain their original measurements. Definitions are in [the glossary](glossary.md).

## Working decision

Use clear grammatical prompts. Remove repetition while keeping required facts, constraints, output format, privacy rules, and approval limits. For recurring tasks, identify reusable content and prepare a provider-specific comparison. Treat shorter wording, cache readiness, observed cache use, and actual savings as different claims.

## Current provider guidance

The [OpenAI prompt-caching guide](https://developers.openai.com/api/docs/guides/prompt-caching) says reuse depends on a matching eligible beginning. Keep shared instructions and reference material consistent, preserve earlier conversation messages where supported, and put changing material later. On GPT-5.6 and later, `prompt_cache_key` is optional for separate cache accounting; earlier models use stable keys to help routing. Recheck the selected model's boundaries, minimum length, lifetime, and charges before deployment.

The [OpenAI data-controls guide](https://developers.openai.com/api/docs/guides/your-data) defines data handling by feature and account controls. Review the actual retention, residency, and approval requirements before proposing cached sensitive content. A minimum cache lifetime does not promise deletion at that time.

The [OpenAI token-counting guide](https://developers.openai.com/api/docs/guides/token-counting) is the reference for full-request input counts. Local plain-text counts omit request framing and may omit tools, schemas, files, or images. A token is a piece of text counted by the model.

Use the selected provider's current billing rates. The sample comparison retains its July 2026 OpenAI price assumptions to keep historical settings intact; those numbers are modeled inputs, not a current quote. Follow [the provider-plan checklist](cache-readiness-plan.md) for other services.

## Research and applicability

These sources inform what to test. Their reported outcomes are not measurements of this skill.

| Source | Finding relevant to this project | Application limit |
|---|---|---|
| [CAVEWOMAN](https://arxiv.org/abs/2606.24083), June 2026 preprint | Input compression and output compression can have different effects; aggressive input deletion increased cost and reduced accuracy in the reported tasks | The tested models and tasks do not establish a general result for this skill |
| [Prompt Compression in the Wild](https://arxiv.org/abs/2604.02985), ECIR 2026 | Compression overhead can cancel faster response generation; benefits depend on prompt length and hardware | Its serving setups do not establish hosted-provider savings here |
| [Information Preservation in Prompt Compression](https://aclanthology.org/2025.findings-emnlp.949/), EMNLP 2025 | Some compression methods lose important details and grounding in the supplied material | Specialized compression methods differ from careful prompt editing |
| [POSIX](https://aclanthology.org/2024.findings-emnlp.852/), EMNLP 2024 | Small wording and template changes can change model behavior | Sensitivity is not the same measurement as task accuracy |
| [Prompt Cache](https://proceedings.mlsys.org/paper_files/paper/2024/hash/a66caa1703fe34705a4368c3014c1966-Abstract-Conference.html), MLSys 2024 | A custom server reused modular processing and improved first-output time in its experiments | This repository does not implement that serving system |
| [LongLLMLingua](https://aclanthology.org/2024.acl-long.91/), ACL 2024 | A specialized long-context compressor improved selected task results and efficiency | It does not establish benefits for ordinary short-prompt rewriting |

An earlier project note cited an [Instagram post](https://www.instagram.com/p/DbGUvqFkkjX/) about shorter answers. Treat that as an anecdotal lead, not controlled evidence. The useful question is whether concise output instructions improve the actual task after quality and full cost are checked.

## Practical conclusions

- Preserve required behavior before optimizing length.
- Measure input and output separately; include the cost of any optimization step.
- Prepare reuse only where the workflow naturally repeats.
- Compare the existing request with the revised request under the same model and task conditions.
- Keep observed usage separate from estimated cache behavior.
- Use a small pilot to find problems, then use representative held-out cases before promotion.
- Keep sensitive data and approval enforcement within the intended application's controls.
