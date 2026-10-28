# Prompt & Cache-Readiness Optimizer: glossary

Use everyday words when they are sufficient. Explain a necessary technical term at first use and link here for detail. In skill responses, include only terms used in the explanation or plan. Keep definitions outside the runtime prompt unless the task requires them.

| Term | Meaning |
|---|---|
| Prompt | Instructions and context supplied to an AI model. |
| Runtime prompt | The actual text and instructions sent to a model to perform the task. |
| Provider | The company or service running the model. |
| Model | The AI system selected to process the request. |
| Model snapshot | A specific saved model version, rather than a name that may point to changing versions. |
| Cache / prompt caching | Saved processing that a provider may reuse when later requests meet its rules. |
| Cache readiness | How well a request is prepared for possible cache reuse. It does not itself establish a cache hit. |
| Reusable prefix / stable prefix | The unchanged beginning shared by multiple requests. |
| Dynamic suffix | The changing content placed after the reusable beginning. |
| Cache-breaking change | A change that can prevent reuse of previously processed content. |
| Cache hit / cache read | Reuse of eligible processing already saved in the cache. |
| Cache write / cold write | Initial preparation and storage of reusable processing. |
| Warm request | A later request that may reuse previously saved processing. |
| Cache key | A request label whose role depends on the provider and model, such as grouping accounting or helping route related requests. |
| Breakpoint | A marked boundary up to which a provider can save or reuse processing. |
| TTL / cache lifetime | A provider's stated reuse period. Check whether it is a minimum lifetime, an expiry rule, or a retention limit. |
| Token | A piece of text counted by the model. |
| LCP | Longest common prefix: the identical beginning shared by a group of requests. |
| Code fence | Markdown markers that display a block of code; extra fences can make an otherwise valid JSON response fail a JSON parser. |
| CPU / GPU / quantization | Types of processors, and a way of storing model numbers with reduced precision to use less memory. These affect local-model performance. |
| Tokenizer | Software that divides text into tokens and counts them. |
| Proxy | An estimate or stand-in measurement that does not directly measure the final outcome. |
| Benchmark | A planned comparison using defined tasks and measurements. |
| Preflight | A local check performed before a live experiment. |
| Arm | One version or condition in a comparison, such as the original or revised prompt. |
| Paired comparison | Testing both versions on the same task cases. |
| Held-out cases | Examples not used while developing the prompt. |
| Fixture | Fixed sample data used to make a check repeatable. |
| Rubric | Written rules for scoring a result. |
| Non-inferiority rule | A rule chosen before testing that defines how much worse a result may be while still passing. This project permits no loss of required behavior or safety. |
| Regression | Previously working behavior that stops working after a change. |
| Validated | A label reserved here for representative held-out tests meeting the project's quality, safety, and measured-efficiency criteria. |
| Schema | A definition of the required structure of an output or tool input. |
| JSON | A structured text format using objects, keys, values, and lists. |
| API | A defined interface through which software sends requests to a service. |
| CLI | A program used by entering commands in a terminal. |
| CI | Checks that run automatically when source code changes. |
| Module | A saved, reusable piece of prompt text or structured content. |
| Manifest / build manifest | A structured record of modules, versions, ordering, or an assembled output. |
| Artifact | A saved output or versioned bundle of files. |
| Canonicalization | Converting equivalent content into a consistent representation before checking or assembling it. |
| Fingerprint / SHA-256 hash | A calculated value used to detect content changes. It does not prove source authenticity or answer quality. |
| Provenance | The recorded source and version history of an artifact or result. |
| UTF-8 / LF | A text encoding and line-ending convention used for repeatable saved content. |
| Telemetry | Usage and timing information reported by a system. |
| Latency | Time taken to produce a response. |
| TTFT | Time to the first useful output token. |
| Reasoning effort | A provider-specific control affecting how much internal processing a model uses. |
| Verbosity | A setting or instruction affecting answer detail. |
| Service tier | A provider's processing or pricing option. |
| Lifecycle cost / amortized cost | Full workflow cost, including initial preparation and any optimization step, spread over the requests that benefit. |
| Telegraphic wording / ablation | Extremely shortened wording, or a comparison that removes a feature to test its effect. |
| Retention / residency / ZDR | How long data may be kept, where it may be processed, and provider-specific zero-data-retention rules. Check the actual service policy. |
| Instruction hierarchy / developer role | Rules determining which instructions have authority; the developer role carries authorized application instructions. |
| Untrusted data / prompt injection | Supplied content with no authority to change application rules, and attempts inside such content to redirect the model. |
| Deterministic | Producing the same result from the same inputs under the stated conditions. |
| Duplicate-action prevention / idempotency | Ensuring a retried request does not unintentionally perform the same external action twice. |
