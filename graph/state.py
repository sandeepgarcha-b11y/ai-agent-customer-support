from typing import Annotated, Literal, Optional
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages

FlowBranch = Literal[
    "untracked_within_sla",
    "untracked_breached",
    "in_transit_ok",
    "in_transit_overdue",
    "delivered",
    "lost",
]

ResolutionStep = Literal["resend", "credit", "refund", "complete"]


class WISMOState(TypedDict):
    messages: Annotated[list, add_messages]
    email: Optional[str]
    account: Optional[dict]
    confirmed_order_id: Optional[str]
    order_data: Optional[dict]
    flow_branch: Optional[FlowBranch]
    resolution_step: Optional[ResolutionStep]
    situation_communicated: bool   # True once communicate_situation has fired
    escalated: bool
