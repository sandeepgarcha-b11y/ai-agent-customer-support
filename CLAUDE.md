# Claude guidance — Passenger Support Agent

## Workflow

After each meaningful change, commit and push to `origin main`. A meaningful change is anything that moves the project forward: new flow logic, updated mock data, prompt changes, new tools, structural refactors. Minor wording tweaks can be bundled into the next natural commit.

Also update `README.md` to reflect the change — keep it accurate but concise. Don't add sections that will become stale; remove or update anything that no longer reflects reality. The README is for orientation, not exhaustive documentation.

## Project context

This is a case study build — one support flow at a time. The current focus is always the most recently briefed flow. Everything else stays as scaffolding placeholders until briefed.

The agent is built with LangGraph (ReAct), OpenAI gpt-4o, and LangSmith tracing. Mock tools return hardcoded but realistic fake data — do not add real API calls.

## Flows

| Flow | Status |
|------|--------|
| WISMO (order tracking) | Complete |
| Returns | Placeholder |
| Exchanges | Placeholder |
| Damaged orders | Placeholder |
| Account access | Placeholder |

Update this table when a flow is briefed and built.

## Conventions

- Tools live in `tools/` — one file per domain, registered in `tools/__init__.py`
- System prompt lives in `prompts/system_prompt.py` — one prompt, updated per flow
- `traces/` and `case_study/` are gitignored — do not commit their contents
- Do not add error handling or abstractions beyond what the current flow needs
- Do not write comments unless the reason for something would genuinely surprise a future reader
