# OpenCode workflows for GPT-6 Sol

This repository is a small, reviewable OpenCode configuration for coding tasks that benefit from GPT-6 Sol reasoning. It is independent of OpenCode and OpenAI. **[ArgoLink](https://argolink.io/gh-gpt-6-sol-agent-workflows) is the OpenAI-compatible endpoint in the example.** Last checked: 2026-10-07.

## Configuration

The .opencode/opencode.json entry uses the OpenCode provider shape with @ai-sdk/openai-compatible, a base URL ending at /v1, an environment-backed key, and one model entry. Verify the current OpenCode schema before copying it: configuration keys and provider adapters can change. Do not paste a secret into this file.

The selected model is gpt-6-sol and reasoning is enabled. The checked catalog lists low, medium, high, xhigh, and max efforts with medium as the default. Model page limits and price fields remain authoritative. Chat-only tools and Responses tools may differ; test the operation your workflow needs.

## Workflows

examples/workflows.yaml describes three reviewable phases for a refactor and a smaller review flow. These are planning records, not an assertion that OpenCode will execute YAML directly. In the UI, turn each step into an explicit prompt and keep the diff between plan and result. A refactor should inspect, plan, patch, test, and review; a code review should read the diff before proposing changes.

## Cost

The checked ArgoLink effective GPT-6 Sol rate is $0.60 per million input tokens and $3.00 per million output tokens, with a lower cached-input rate in the catalog. A 200k input plus 20k output cold estimate is $0.18. This excludes long-context multipliers, tool rounds, and retries. Keep a request-level usage record and recalculate after the catalog changes.

## Safe operation

Use OPENAI_API_KEY only in the host environment. Start with a read-only review workflow. Before a write workflow, ensure the repository is clean or the patch is in a branch. Review tool calls, limit iterations, and stop on authentication or unknown model errors. Never let a timeout replay a tool that writes state.

## Validation and FAQ

python3 -m unittest discover -s tests checks the provider configuration offline. A real OpenCode session is not performed here. **Why the compatibility package?** It translates the standard OpenAI-shaped client to the configured base. **Why might tools fail?** Model and endpoint capabilities are separate. **Can another model be used?** Only after adding and verifying its own catalog row.
