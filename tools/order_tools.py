"""Mock tools for order-related support flows."""

from langchain_core.tools import tool


@tool
def lookup_order(order_id: str) -> dict:
    """Look up the status, carrier, and estimated delivery for an order."""
    mock_orders = {
        "PAS-10042": {
            "order_id": "PAS-10042",
            "status": "in_transit",
            "carrier": "DPD",
            "tracking_number": "1Z999AA10123456784",
            "estimated_delivery": "2026-06-05",
            "items": ["Merino Crew Neck Jumper (Forest Green, M)"],
            "placed_at": "2026-05-30",
        },
        "PAS-10038": {
            "order_id": "PAS-10038",
            "status": "delivered",
            "carrier": "Royal Mail",
            "tracking_number": "RM123456789GB",
            "estimated_delivery": "2026-05-28",
            "delivered_at": "2026-05-28",
            "items": ["Linen Shirt (Ecru, S)", "Canvas Shorts (Olive, S)"],
            "placed_at": "2026-05-25",
        },
        "PAS-10055": {
            "order_id": "PAS-10055",
            "status": "processing",
            "carrier": None,
            "tracking_number": None,
            "estimated_delivery": "2026-06-07",
            "items": ["Recycled Fleece Jacket (Slate, L)"],
            "placed_at": "2026-06-02",
        },
    }
    order = mock_orders.get(order_id)
    if not order:
        return {"error": "Order not found", "order_id": order_id}
    return order


@tool
def check_return_eligibility(order_id: str) -> dict:
    """Check whether an order is eligible for return and the reason if not."""
    mock_eligibility = {
        "PAS-10042": {
            "order_id": "PAS-10042",
            "eligible": True,
            "reason": None,
            "return_window_days": 30,
            "days_remaining": 27,
        },
        "PAS-10038": {
            "order_id": "PAS-10038",
            "eligible": True,
            "reason": None,
            "return_window_days": 30,
            "days_remaining": 22,
        },
        "PAS-10055": {
            "order_id": "PAS-10055",
            "eligible": False,
            "reason": "Order has not yet been delivered.",
            "return_window_days": 30,
            "days_remaining": None,
        },
        "PAS-10001": {
            "order_id": "PAS-10001",
            "eligible": False,
            "reason": "Return window of 30 days has expired.",
            "return_window_days": 30,
            "days_remaining": 0,
        },
    }
    result = mock_eligibility.get(order_id)
    if not result:
        return {"error": "Order not found", "order_id": order_id}
    return result


@tool
def initiate_return(order_id: str) -> dict:
    """Initiate a return for an eligible order and get a return reference number."""
    eligible_orders = {"PAS-10042", "PAS-10038"}
    if order_id not in eligible_orders:
        return {
            "success": False,
            "order_id": order_id,
            "error": "Order is not eligible for return.",
        }
    return {
        "success": True,
        "order_id": order_id,
        "return_reference": f"RET-{order_id}-7821",
        "instructions": (
            "A prepaid returns label has been emailed to you. "
            "Please pack items securely and drop off at any DPD Parcelshop within 7 days. "
            "Refunds are processed within 5–7 business days of receipt."
        ),
    }


@tool
def initiate_exchange(order_id: str, new_product_id: str, size: str) -> dict:
    """Initiate an exchange for an order, specifying the replacement product and size."""
    in_stock = {("PROD-FLEECE-JACKET", "M"), ("PROD-LINEN-SHIRT", "L")}
    if (new_product_id, size) in in_stock:
        return {
            "success": True,
            "order_id": order_id,
            "exchange_reference": f"EXC-{order_id}-3310",
            "new_product_id": new_product_id,
            "size": size,
            "instructions": (
                "A prepaid returns label has been emailed to you. "
                "Once we receive your item, your exchange will be dispatched within 2 business days."
            ),
        }
    return {
        "success": False,
        "order_id": order_id,
        "new_product_id": new_product_id,
        "size": size,
        "error": "Requested size is currently out of stock. Would you like to choose a different size or request a refund instead?",
    }
