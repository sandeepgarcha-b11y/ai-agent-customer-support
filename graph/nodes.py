"""LangGraph node functions for the WISMO flow."""

import re
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage

from graph.state import WISMOState
from prompts.node_prompts import (
    IDENTIFY_CUSTOMER,
    CONFIRM_ORDER,
    COMMUNICATE_SITUATION,
    RESOLVE,
    ESCALATE,
)
from tools.account_tools import lookup_account
from tools.order_tools import lookup_order
from tools.product_tools import check_stock

llm = ChatOpenAI(model="gpt-4o", temperature=0)

ESCALATION_SIGNALS = [
    "speak to a human", "speak to someone", "talk to a person", "real person",
    "human agent", "manager", "supervisor", "this is ridiculous", "not good enough",
    "completely useless", "speak to a real", "get a human",
]


def _last_human_message(state: WISMOState) -> str:
    for m in reversed(state["messages"]):
        if isinstance(m, HumanMessage):
            return m.content.lower()
    return ""


def _customer_wants_escalation(state: WISMOState) -> bool:
    text = _last_human_message(state)
    return any(signal in text for signal in ESCALATION_SIGNALS)


def _llm_reply(system_prompt: str, state: WISMOState, extra_context: str = "") -> str:
    """Call the LLM with a focused system prompt and the conversation history."""
    system = system_prompt
    if extra_context:
        system += f"\n\nContext for this turn:\n{extra_context}"
    messages = [SystemMessage(content=system)] + state["messages"]
    response = llm.invoke(messages)
    return response.content


# ---------------------------------------------------------------------------
# Node: identify_customer
# ---------------------------------------------------------------------------

def identify_customer(state: WISMOState) -> dict:
    if _customer_wants_escalation(state):
        return {"escalated": True}

    last_msg = _last_human_message(state)

    # Try to parse email from the latest human message
    email_match = re.search(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", last_msg)

    if not email_match:
        reply = _llm_reply(IDENTIFY_CUSTOMER, state)
        return {"messages": [AIMessage(content=reply)]}

    email = email_match.group(0)
    result = lookup_account.invoke({"email": email})

    if result.get("account_status") == "not_found":
        reply = _llm_reply(
            IDENTIFY_CUSTOMER, state,
            extra_context=f"The email {email} was not found in the system. Ask them to check the email they registered with."
        )
        return {"messages": [AIMessage(content=reply)]}

    reply = _llm_reply(
        IDENTIFY_CUSTOMER, state,
        extra_context=f"Account found for {result.get('name')}. Acknowledge briefly."
    )
    return {
        "email": email,
        "account": result,
        "messages": [AIMessage(content=reply)],
    }


# ---------------------------------------------------------------------------
# Node: confirm_order
# ---------------------------------------------------------------------------

def confirm_order(state: WISMOState) -> dict:
    if _customer_wants_escalation(state):
        return {"escalated": True}

    account = state["account"]
    order_ids = account.get("recent_order_ids", [])

    if not order_ids:
        reply = _llm_reply(
            CONFIRM_ORDER, state,
            extra_context="This customer has no recent orders on record. Let them know gently."
        )
        return {"messages": [AIMessage(content=reply)]}

    # Fetch all recent orders
    orders = [lookup_order.invoke({"order_id": oid}) for oid in order_ids]

    # Check if the customer has already confirmed or selected an order
    last_msg = _last_human_message(state)

    # If there's only one order and we haven't asked yet, ask for confirmation
    # If there's only one order and the customer said yes, confirm it
    if len(orders) == 1:
        order = orders[0]
        item_names = [i["name"] if isinstance(i, dict) else i for i in order.get("items", [])]
        items_str = ", ".join(item_names)
        placed = order.get("placed_at", "")

        if any(word in last_msg for word in ["yes", "yeah", "yep", "correct", "that's right", "that's the one", "yup"]):
            return {
                "confirmed_order_id": order["order_id"],
                "order_data": order,
            }

        reply = _llm_reply(
            CONFIRM_ORDER, state,
            extra_context=f"One recent order: {items_str}, placed {placed}, order ID {order['order_id']}. Ask if this is the one."
        )
        return {"messages": [AIMessage(content=reply)]}

    # Multiple orders — check if customer is selecting one
    for order in orders:
        if order["order_id"].lower() in last_msg:
            return {"confirmed_order_id": order["order_id"], "order_data": order}

    # Check for numbered selection (1, 2, 3)
    for i, order in enumerate(orders, 1):
        if str(i) in last_msg.split() or last_msg.strip() == str(i):
            return {"confirmed_order_id": order["order_id"], "order_data": order}

    # Check for "yes" confirming most recent
    if any(word in last_msg for word in ["yes", "yeah", "yep", "correct", "that's right", "that's the one", "yup"]):
        order = orders[0]
        return {"confirmed_order_id": order["order_id"], "order_data": order}

    # Build order list for the prompt
    order_lines = []
    for o in orders:
        item_names = [i["name"] if isinstance(i, dict) else i for i in o.get("items", [])]
        order_lines.append(f"{', '.join(item_names)} — placed {o.get('placed_at')}")

    context = "Recent orders:\n" + "\n".join(f"{i+1}. {line}" for i, line in enumerate(order_lines))
    context += "\nAsk which order they're enquiring about."

    reply = _llm_reply(CONFIRM_ORDER, state, extra_context=context)
    return {"messages": [AIMessage(content=reply)]}


# ---------------------------------------------------------------------------
# Node: assess_status  (pure Python — no LLM)
# ---------------------------------------------------------------------------

def assess_status(state: WISMOState) -> dict:
    d = state["order_data"]
    status = d["status"]
    sla_breached = d.get("sla_breached", False)
    tracking = d.get("tracking_available", False)

    if status == "lost":
        branch = "lost"
    elif status == "delivered":
        branch = "delivered"
    elif not tracking and not sla_breached:
        branch = "untracked_within_sla"
    elif not tracking and sla_breached:
        branch = "untracked_breached"
    elif tracking and not sla_breached:
        branch = "in_transit_ok"
    else:
        branch = "in_transit_overdue"

    return {"flow_branch": branch}


# ---------------------------------------------------------------------------
# Node: communicate_situation
# ---------------------------------------------------------------------------

def communicate_situation(state: WISMOState) -> dict:
    if _customer_wants_escalation(state):
        return {"escalated": True}

    branch = state["flow_branch"]
    order = state["order_data"]
    prompt = COMMUNICATE_SITUATION[branch]

    # Build rich context from order data
    item_names = [i["name"] if isinstance(i, dict) else i for i in order.get("items", [])]
    context_parts = [
        f"Items: {', '.join(item_names)}",
        f"Order placed: {order.get('placed_at')}",
        f"Estimated delivery: {order.get('estimated_delivery')}",
    ]
    if order.get("last_update"):
        context_parts.append(f"Latest tracking update: {order['last_update']}")
    if order.get("last_update_at"):
        context_parts.append(f"Last update time: {order['last_update_at']}")
    if order.get("last_known_location"):
        context_parts.append(f"Last known location: {order['last_known_location']}")
    if order.get("delivered_at"):
        context_parts.append(f"Delivered at: {order['delivered_at']}")
    if order.get("delivery_note"):
        context_parts.append(f"Delivery note: {order['delivery_note']}")

    context = "\n".join(context_parts)
    reply = _llm_reply(prompt, state, extra_context=context)

    # Terminal branches — no resolution needed
    if branch in ("untracked_within_sla", "in_transit_ok"):
        return {
            "messages": [AIMessage(content=reply)],
            "situation_communicated": True,
            "resolution_step": "complete",
        }

    # Lost — move straight to resolve on the next turn; mark situation communicated
    if branch == "lost":
        return {
            "messages": [AIMessage(content=reply)],
            "situation_communicated": True,
            "resolution_step": "resend",
        }

    # For delivered, overdue, breached — wait for customer to reply before resolving
    return {
        "messages": [AIMessage(content=reply)],
        "situation_communicated": True,
    }


# ---------------------------------------------------------------------------
# Node: resolve
# ---------------------------------------------------------------------------

def _item_list(order: dict) -> list[dict]:
    items = order.get("items", [])
    result = []
    for item in items:
        if isinstance(item, dict):
            result.append(item)
        else:
            result.append({"name": item, "product_id": None, "size": None})
    return result


def resolve(state: WISMOState) -> dict:
    if _customer_wants_escalation(state):
        return {"escalated": True}

    # If resolution_step not yet set (entry from delivered/overdue/breached branches), start at resend
    step = state.get("resolution_step") or "resend"
    order = state["order_data"]
    last_msg = _last_human_message(state)

    declined = any(
        word in last_msg.split()
        for word in ["no", "nope"]
    ) or any(
        phrase in last_msg
        for phrase in ["don't want", "not interested", "prefer a", "rather have", "instead"]
    )

    if step == "resend":
        items = _item_list(order)
        available_items = []
        for item in items:
            pid = item.get("product_id")
            size = item.get("size")
            if pid and size:
                stock = check_stock.invoke({"product_id": pid, "size": size})
                if stock.get("status") in ("available", "low"):
                    available_items.append(item["name"])

        if available_items and not declined:
            items_str = ", ".join(available_items)
            reply = _llm_reply(
                RESOLVE["resend"], state,
                extra_context=f"Available to resend: {items_str}"
            )
            return {
                "messages": [AIMessage(content=reply)],
                "resolution_step": "resend",
            }
        else:
            # Out of stock or declined — move to credit
            reply = _llm_reply(
                RESOLVE["credit"], state,
                extra_context="Resend is not available. Offer store credit."
            )
            return {
                "messages": [AIMessage(content=reply)],
                "resolution_step": "credit",
            }

    if step == "credit":
        if declined:
            reply = _llm_reply(RESOLVE["refund"], state)
            return {
                "messages": [AIMessage(content=reply)],
                "resolution_step": "refund",
            }
        reply = _llm_reply(
            RESOLVE["credit"], state,
            extra_context="Customer accepted credit. Confirm it's been arranged and close warmly."
        )
        return {
            "messages": [AIMessage(content=reply)],
            "resolution_step": "complete",
        }

    if step == "refund":
        if declined:
            return {"escalated": True}
        reply = _llm_reply(
            RESOLVE["refund"], state,
            extra_context="Customer accepted refund. Confirm it will appear in 5-7 business days and close warmly."
        )
        return {
            "messages": [AIMessage(content=reply)],
            "resolution_step": "complete",
        }

    return {}


# ---------------------------------------------------------------------------
# Node: escalate
# ---------------------------------------------------------------------------

def escalate(state: WISMOState) -> dict:
    reply = _llm_reply(ESCALATE, state)
    return {"messages": [AIMessage(content=reply)]}
