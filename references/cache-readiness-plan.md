# Prompt & Cache-Readiness Optimizer: recurring-workflow plan

Use this checklist to turn recurring work into a clear prompt structure and a provider-specific measurement plan. A provider runs the model; a cache is saved processing it may reuse. Other terms are in [the glossary](glossary.md).

## Capture the workflow

Record the task, required output, non-negotiable facts and rules, provider, exact model, interface, frequency, expected reuse, and data restrictions. Ask one focused question when a missing detail would change the result. Otherwise state a material assumption.

## Map reuse

| Content | Preparation |
|---|---|
| Authorized shared instructions | Keep wording and order consistent while the version stays current |
| Reference material | Keep stable where useful; label it as data with no instruction authority |
| Tools and output structure | Keep the required selection and ordering consistent |
| Conversation history | Preserve earlier messages and tool results where supported; append new material |
| Current question, retrieved data, timestamps, and identifiers | Place later; include only what the task needs |

Identify concrete changes that could interrupt reuse: changing the beginning, moving modules, reordering tools, updating a schema, or replacing earlier conversation messages. Explain which changes are necessary and how to version them deliberately.

## Verify the provider plan

Use current official documentation for the selected provider and exact model. Record the source links and date checked.

Determine:

- What content must match and whether the provider supports explicit reuse boundaries.
- Minimum reusable length, supported request fields, and the role of any cache key.
- Cache lifetime, data-retention and location rules, and required approvals.
- What usage information is reported and whether it isolates the application's content.
- Current input, cache-read, cache-write, and output charges where applicable.
- Relevant differences between the selected model and the example in this repository.

If a field or policy cannot be verified, mark it pending. Do not copy OpenAI settings to another provider. The [OpenAI example](responses-api-template.md) is one documented starting point.

## Plan the comparison

Compare the current and revised prompts on the same task cases. Hold model, settings, tools, output structure, and scoring rules constant. Include representative successes, missing information, conflicting instructions, embedded instructions in data, and relevant approval cases.

Record correct answers and required-format checks; observed input, cached, cache-write, output, and reasoning tokens when available; first-output and completion time; and full cost. A token is a piece of text counted by the model. Include the initial preparation and the cost of improving the prompt.

Separate observed measurements from modeled assumptions. The local script can check assembly and estimates; a live provider experiment must establish actual reuse. Use [the benchmark protocol](benchmark-protocol.md) for scoring and promotion criteria.

## Deliver the plan

1. Improved prompt with reusable and changing content clearly separated.
2. Reuse map and specific changes that could interrupt caching.
3. Provider, model, verified settings, official sources, and data-handling requirements.
4. Test cases, measurements, acceptance criteria, and any missing evidence.
5. A short glossary containing only necessary technical terms used.

State the useful preparation completed. Place limits beside affected measurements and identify what would resolve them.
