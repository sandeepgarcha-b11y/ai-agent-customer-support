# Passenger Support Agent

A customer support AI agent for [Passenger](https://www.passenger-clothing.com/), built with LangGraph (ReAct architecture), OpenAI `gpt-4o`, and LangSmith tracing.

## Supported flows

| Flow | Description |
|------|-------------|
| **WISMO** | Order tracking — status, carrier, estimated delivery |
| **Returns** | Eligibility check and return initiation |
| **Exchanges** | Swap for a different size or product |
| **Damaged orders** | Triage and escalation |
| **Account access** | Account lookup and flag identification |

## Project structure

```
cs-ai-agent/
├── agent.py              # LangGraph ReAct agent + CLI entrypoint
├── tools/
│   ├── order_tools.py    # lookup_order, check_return_eligibility, initiate_return, initiate_exchange
│   ├── product_tools.py  # check_stock
│   └── account_tools.py  # lookup_account
├── prompts/
│   └── system_prompt.py  # Placeholder — system prompt written separately
├── traces/               # LangSmith trace exports (gitignored)
├── case_study/           # Iteration logs and docs (gitignored)
├── requirements.txt
└── .env.example
```

## Setup

```bash
# 1. Clone and install dependencies
pip install -r requirements.txt

# 2. Configure environment variables
cp .env.example .env
# Edit .env and fill in your API keys

# 3. Run the agent
python agent.py
```

## Environment variables

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENAI_API_KEY` | Yes | OpenAI API key |
| `LANGCHAIN_TRACING_V2` | No | Set to `true` to enable LangSmith tracing |
| `LANGCHAIN_API_KEY` | No | LangSmith API key |
| `LANGCHAIN_PROJECT` | No | LangSmith project name (default: `passenger-support-agent`) |

## Mock data

All tools return hardcoded but realistic fake data. Sample identifiers for testing:

**Orders:** `PAS-10042` (in transit), `PAS-10038` (delivered), `PAS-10055` (processing)

**Products:** `PROD-MERINO-JUMPER`, `PROD-LINEN-SHIRT`, `PROD-CANVAS-SHORTS`, `PROD-FLEECE-JACKET`

**Accounts:** `jane.doe@example.com` (active), `locked.user@example.com` (locked), `flagged.user@example.com` (fraud flag)

## Escalation

The agent is designed to recognise when a query is beyond its scope and escalate gracefully to a human agent. Escalation logic is handled via the system prompt (to be added separately).

## LangSmith tracing

With `LANGCHAIN_TRACING_V2=true` set, every agent run is automatically traced to LangSmith. Export traces to the `traces/` directory for offline analysis.
