# AI Customer Support Agent

A LangGraph-based customer support agent built for Passenger, a mid-market sustainable fashion brand. Explores how AI can automate common support workflows while maintaining a good customer experience.

## Why I Built This

Customer support is one of the areas where AI has the greatest potential to create value.

Having worked on customer support automation in production, I wanted to better understand how modern AI agents handle workflows, tool use, orchestration and customer interactions.

## What It Does

The agent handles five support flows for Passenger customers:

| Flow | Status |
|------|--------|
| **WISMO** (order tracking) | Complete |
| **Returns** | Placeholder |
| **Exchanges** | Placeholder |
| **Damaged orders** | Placeholder |
| **Account access** | Placeholder |

## Architecture

Built with LangGraph (multi-node StateGraph), OpenAI `gpt-4o`, and LangSmith tracing. Each support flow is implemented as a discrete graph with purpose-built nodes — no single monolithic prompt.

```
cs-ai-agent/
├── agent.py              # CLI entrypoint
├── graph/
│   ├── state.py          # WISMOState TypedDict
│   ├── nodes.py          # Node functions per flow stage
│   └── graph.py          # StateGraph wiring and compilation
├── tools/
│   ├── order_tools.py    # lookup_order, check_return_eligibility, initiate_return, initiate_exchange
│   ├── product_tools.py  # check_stock
│   └── account_tools.py  # lookup_account
├── prompts/
│   ├── node_prompts.py   # Focused prompts for each LLM-calling node
│   └── system_prompt.py  # Brand voice reference
├── traces/               # LangSmith trace exports (gitignored)
├── case_study/           # Iteration logs and docs (gitignored)
├── CLAUDE.md             # Guidance for Claude Code
├── requirements.txt
└── .env.example
```

## Setup

```bash
# 1. Clone and create a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment variables
cp .env.example .env
# Edit .env and fill in your API keys

# 4. Run the agent
set -a && source .env && set +a && python agent.py
```

## Environment variables

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENAI_API_KEY` | Yes | OpenAI API key |
| `LANGCHAIN_TRACING_V2` | No | Set to `true` to enable LangSmith tracing |
| `LANGCHAIN_API_KEY` | No | LangSmith API key |
| `LANGCHAIN_ENDPOINT` | No | LangSmith endpoint (EU: `https://eu.api.smith.langchain.com`) |
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

## Areas Explored

- Agent orchestration with multi-node StateGraph
- Tool calling and structured mock data
- Prompt design at the node level
- State management across conversation turns
- Human handoff patterns
- Customer support automation

## What I Learned

Building this project gave me a much deeper understanding of the challenges involved in deploying customer-facing AI systems, including reliability, trust, escalation and workflow design.
