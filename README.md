# Passenger Support Agent

A customer support AI agent for [Passenger](https://www.passenger-clothing.com/), built with LangGraph (ReAct architecture), OpenAI `gpt-4o`, and LangSmith tracing.

## Supported flows

| Flow | Status |
|------|--------|
| **WISMO** (order tracking) | Complete |
| **Returns** | Placeholder |
| **Exchanges** | Placeholder |
| **Damaged orders** | Placeholder |
| **Account access** | Placeholder |

## Project structure

```
cs-ai-agent/
├── agent.py              # LangGraph ReAct agent + CLI entrypoint
├── tools/
│   ├── order_tools.py    # lookup_order, check_return_eligibility, initiate_return, initiate_exchange
│   ├── product_tools.py  # check_stock
│   └── account_tools.py  # lookup_account
├── prompts/
│   └── system_prompt.py  # WISMO system prompt (other flows TBD)
├── traces/               # LangSmith trace exports (gitignored)
├── case_study/           # Iteration logs and docs (gitignored)
├── CLAUDE.md             # Guidance for Claude Code
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

## Test personas (WISMO)

All tools use hardcoded mock data. Use these email addresses to drive each scenario:

| Email | Scenario |
|-------|----------|
| `clara.jones@example.com` | Untracked, within SLA |
| `tom.wright@example.com` | Untracked, outside SLA |
| `priya.mehta@example.com` | Tracked, within delivery window |
| `ben.hayes@example.com` | Tracked, overdue, at depot |
| `sarah.okafor@example.com` | Delivered, customer says not received |
| `james.liu@example.com` | Genuinely lost |
| `nina.patel@example.com` | Multiple recent orders |

**Products (for exchange/stock checks):** `PROD-MERINO-JUMPER`, `PROD-LINEN-SHIRT`, `PROD-CANVAS-SHORTS`, `PROD-FLEECE-JACKET`

## LangSmith tracing

With `LANGCHAIN_TRACING_V2=true` set, every agent run is automatically traced to LangSmith. Export traces to the `traces/` directory for offline analysis.
