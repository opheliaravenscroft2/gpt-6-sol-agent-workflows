# OpenCode workflows for GPT-6 Sol

This repository is a small, reviewable OpenCode configuration for coding tasks that benefit from GPT-6 Sol reasoning. It is independent of OpenCode and OpenAI. **[ArgoLink](https://argolink.io/gh-gpt-6-sol-agent-workflows) is the OpenAI-compatible endpoint in the example.** Checked 2026-10-07.

## Current OpenCode provider schema

OpenCode's current provider documentation distinguishes the AI SDK package by wire contract: use `@ai-sdk/openai-compatible` for `/v1/chat/completions`; use `@ai-sdk/openai` when the provider/model uses `/v1/responses`. GPT-6 Sol is configured with the latter. The provider block in [`.opencode/opencode.json`](.opencode/opencode.json) therefore uses:

- `npm: "@ai-sdk/openai"`;
- `options.baseURL: "https://argolink.io/v1"` and `apiKey: "{env:OPENAI_API_KEY}"`;
- model `gpt-6-sol` with `reasoning: true`;
- `reasoning_options` values `low`, `medium`, `high`, `xhigh`, `max`;
- `limit.context: 1050000` and `limit.output: 128000` from the live catalog;
- effective catalog cost input $0.60/M, output $3.00/M, cached read $0.06/M, cache write $0.75/M;
- `variants` that make each reasoning effort selectable in the model picker.

The model selector is `argolink/gpt-6-sol`. OpenCode's current provider docs show the `provider/models/options` shape and explain that `limit` helps the UI understand context remaining. They also document `/models` for checking that a custom provider loaded.

## Setup

1. Install the current OpenCode release according to its official instructions.
2. Export the key in the host environment; do not put it in JSON:

   ```bash
   export OPENAI_API_KEY='replace-with-a-development-key'
   ```

3. Put this repository's `.opencode/opencode.json` in the project or user configuration location supported by your OpenCode version.
4. Start OpenCode and run `/models`; select `argolink/gpt-6-sol`.
5. Read `GET https://argolink.io/v1/models` and the model page on the same date before accepting the cost and limits.

The config is a routing description, not a claim that every OpenCode feature works through every provider. Verify Responses streaming, tools, structured output, image input, usage, timeout, and error parsing with a local mock or a small approved canary.

## Workflows

[`examples/workflows.yaml`](examples/workflows.yaml) is a reviewable plan, not YAML that OpenCode executes automatically. It gives three repeatable shapes:

- **refactor:** inspect, plan, patch, test, review;
- **review:** read the diff, identify risks, and write comments;
- **test-authoring:** inspect behavior, propose cases, write tests, run them, and review.

Use `high` for a refactor or test-authoring plan, `medium` for a first review, and limit iterations to three. Start write workflows from a clean branch, inspect proposed tool calls, and stop on an authentication or unknown-model error. Keep generated diffs reviewable and do not let a timeout replay a state-changing tool.

## Cost and long context

A cold 200k-input/20k-output run is about $0.18 at the checked effective rate. GPT-6 Sol's catalog rule applies input ×2 and output ×1.5 above 272k input tokens; tool rounds and retries add more. Keep a request-level usage record and a retry reserve rather than treating the displayed model cost as an invoice.

## Troubleshooting

- **Provider missing in `/models`:** confirm the provider ID is `argolink`, the model selector is `argolink/gpt-6-sol`, and the JSON is loaded from the right scope.
- **Wrong endpoint:** `@ai-sdk/openai-compatible` targets chat completions; this configuration intentionally uses `@ai-sdk/openai` for Responses.
- **401:** `OPENAI_API_KEY` is unset, belongs to another endpoint, or was written into a config the process cannot read.
- **400:** check model ID, reasoning effort spelling, tool schema, and unsupported sampling fields.
- **Timeout:** preserve any response/request ID and reconcile before retrying a billable call.

## Validation and sources

```bash
python3 -m unittest discover -s tests -v
```

The tests parse the configuration offline and check the provider package, endpoint base, reasoning values, limits, costs, and workflow plan. No OpenCode session or billable request is run here.

Primary sources: [OpenCode providers](https://docs.opencode.ai/docs/providers/) · [OpenCode config](https://opencode.ai/docs/config/) · [ArgoLink model list](https://argolink.io/v1/models) · [ArgoLink model pages](https://argolink.io/en/models).
