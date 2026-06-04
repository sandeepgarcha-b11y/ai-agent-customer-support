"""Builds and compiles the WISMO LangGraph StateGraph."""

from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

from graph.state import WISMOState
from graph.nodes import (
    identify_customer,
    confirm_order,
    assess_status,
    communicate_situation,
    resolve,
    escalate,
)
from graph.nodes import _last_human_message


# ---------------------------------------------------------------------------
# Per-node routing functions
# Each one answers: "given the state after THIS node ran, where do we go next?"
# They only run within the same invocation — they do NOT wait for human input.
# Nodes that need human input return END, so the graph pauses until next invoke.
# ---------------------------------------------------------------------------

def _after_identify(state: WISMOState) -> str:
    if state.get("escalated"):
        return "escalate"
    # If we now have email + account, proceed — otherwise END and wait for email
    if state.get("email") and state.get("account"):
        return "confirm_order"
    return END


def _after_confirm(state: WISMOState) -> str:
    if state.get("escalated"):
        return "escalate"
    # If order confirmed, run assess immediately (no human input needed between)
    if state.get("confirmed_order_id"):
        return "assess_status"
    return END  # waiting for customer to confirm/select order


def _after_communicate(state: WISMOState) -> str:
    if state.get("escalated"):
        return "escalate"
    resolution_step = state.get("resolution_step")
    # Terminal branches (untracked_within_sla, in_transit_ok) set resolution_step=complete
    if resolution_step == "complete":
        return END
    # All other branches — END after communicating situation, wait for customer reply
    # The entry router handles routing to resolve on the next invocation
    return END


def _after_resolve(state: WISMOState) -> str:
    if state.get("escalated"):
        return "escalate"
    if state.get("resolution_step") == "complete":
        return END
    # More resolution steps pending — wait for customer response
    return END


def _entry_router(state: WISMOState) -> str:
    """Entry point: route to the right node based on current state."""
    if state.get("escalated"):
        return "escalate"
    if not state.get("email") or not state.get("account"):
        return "identify_customer"
    if not state.get("confirmed_order_id"):
        return "confirm_order"
    if not state.get("flow_branch"):
        # Should not reach here via entry after first run — assess fires inline
        return "assess_status"
    if not state.get("situation_communicated"):
        return "communicate_situation"

    resolution_step = state.get("resolution_step")
    if resolution_step in ("resend", "credit", "refund"):
        return "resolve"
    if resolution_step == "complete":
        return END

    # Situation communicated, waiting for customer signal to start resolutions
    branch = state.get("flow_branch")
    if branch in ("delivered", "in_transit_overdue", "untracked_breached"):
        last = _last_human_message(state)
        resolution_signals = [
            "checked", "not there", "still not", "looked", "can't find",
            "cannot find", "wasn't there", "wasn't delivered", "never arrived",
            "not arrived", "still missing", "already checked", "not found",
        ]
        if any(s in last for s in resolution_signals):
            return "resolve"
        return "communicate_situation"

    return END


def build_graph():
    builder = StateGraph(WISMOState)

    builder.add_node("identify_customer", identify_customer)
    builder.add_node("confirm_order", confirm_order)
    builder.add_node("assess_status", assess_status)
    builder.add_node("communicate_situation", communicate_situation)
    builder.add_node("resolve", resolve)
    builder.add_node("escalate", escalate)

    # Entry point
    builder.set_conditional_entry_point(_entry_router, {
        "identify_customer": "identify_customer",
        "confirm_order": "confirm_order",
        "assess_status": "assess_status",
        "communicate_situation": "communicate_situation",
        "resolve": "resolve",
        "escalate": "escalate",
        END: END,
    })

    # identify_customer: if email+account now known, go to confirm_order; else END (wait)
    builder.add_conditional_edges("identify_customer", _after_identify, {
        "confirm_order": "confirm_order",
        "escalate": "escalate",
        END: END,
    })

    # confirm_order: if order confirmed, run assess immediately; else END (wait)
    builder.add_conditional_edges("confirm_order", _after_confirm, {
        "assess_status": "assess_status",
        "escalate": "escalate",
        END: END,
    })

    # assess_status: always goes straight to communicate_situation
    builder.add_edge("assess_status", "communicate_situation")

    # communicate_situation: lost → resolve immediately; terminal → END; others → END (wait)
    builder.add_conditional_edges("communicate_situation", _after_communicate, {
        "resolve": "resolve",
        "escalate": "escalate",
        END: END,
    })

    # resolve: always END after responding (wait for customer reply)
    builder.add_conditional_edges("resolve", _after_resolve, {
        "escalate": "escalate",
        END: END,
    })

    builder.add_edge("escalate", END)

    memory = MemorySaver()
    return builder.compile(checkpointer=memory)
