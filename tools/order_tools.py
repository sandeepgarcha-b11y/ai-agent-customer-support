"""Mock tools for order-related support flows."""

from langchain_core.tools import tool


@tool
def lookup_order(order_id: str) -> dict:
    """Look up the status, carrier, tracking, and estimated delivery for an order."""
    mock_orders = {
        # Untracked — placed 2 days ago, within the 3-day SLA
        "PAS-10061": {
            "order_id": "PAS-10061",
            "status": "processing",
            "tracking_available": False,
            "carrier": "Royal Mail",
            "tracking_number": None,
            "placed_at": "2026-06-01",
            "estimated_dispatch": "2026-06-04",
            "estimated_delivery": "2026-06-06",
            "items": [{"name": "Merino Crew Neck Jumper (Forest Green, M)", "product_id": "PROD-MERINO-JUMPER", "size": "M"}],
            "sla_breached": False,
        },
        # Untracked — placed 5 days ago, outside the 3-day SLA
        "PAS-10057": {
            "order_id": "PAS-10057",
            "status": "processing",
            "tracking_available": False,
            "carrier": "Royal Mail",
            "tracking_number": None,
            "placed_at": "2026-05-29",
            "estimated_dispatch": "2026-06-01",
            "estimated_delivery": "2026-06-03",
            "items": [{"name": "Linen Wide-Leg Trousers (Sand, 12)", "product_id": "PROD-LINEN-TROUSERS", "size": "12"}],
            "sla_breached": True,
        },
        # Tracked — within the 1-2 day delivery window, on its way
        "PAS-10062": {
            "order_id": "PAS-10062",
            "status": "in_transit",
            "tracking_available": True,
            "carrier": "DPD",
            "tracking_number": "15086429741",
            "placed_at": "2026-05-31",
            "estimated_delivery": "2026-06-04",
            "last_update": "Out for delivery — DPD depot, Bristol",
            "last_update_at": "2026-06-03T07:14:00",
            "items": [{"name": "Recycled Fleece Jacket (Slate, L)", "product_id": "PROD-FLEECE-JACKET", "size": "L"}],
            "sla_breached": False,
        },
        # Tracked — outside window, not yet delivered, last known coordinates
        "PAS-10048": {
            "order_id": "PAS-10048",
            "status": "in_transit",
            "tracking_available": True,
            "carrier": "DPD",
            "tracking_number": "15086100293",
            "placed_at": "2026-05-26",
            "estimated_delivery": "2026-05-30",
            "last_update": "Parcel held at DPD Swindon depot — collection card left",
            "last_update_at": "2026-05-30T09:41:00",
            "last_known_location": "DPD Parcelshop, 14 Commercial Road, Swindon, SN1 5NF",
            "items": [{"name": "Canvas Overshirt (Rust, S)", "product_id": "PROD-CANVAS-OVERSHIRT", "size": "S"}],
            "sla_breached": True,
        },
        # Tracked — marked delivered, with delivery coordinates (left safe)
        "PAS-10042": {
            "order_id": "PAS-10042",
            "status": "delivered",
            "tracking_available": True,
            "carrier": "DPD",
            "tracking_number": "15085774410",
            "placed_at": "2026-05-25",
            "estimated_delivery": "2026-05-28",
            "delivered_at": "2026-05-28T13:22:00",
            "delivery_note": "Left in rear alleyway, beside the blue gate",
            "last_known_location": "Rear of 42 Ashford Street, Bristol, BS3 1QH",
            "items": [
                {"name": "Organic Cotton Tee (White, M)", "product_id": "PROD-ORGANIC-TEE", "size": "M"},
                {"name": "Merino Beanie (Charcoal)", "product_id": "PROD-MERINO-BEANIE", "size": "ONE SIZE"},
            ],
            "sla_breached": False,
        },
        # Tracked — genuinely lost, no movement in 9 days
        "PAS-10039": {
            "order_id": "PAS-10039",
            "status": "lost",
            "tracking_available": True,
            "carrier": "Evri",
            "tracking_number": "H8823001294GB",
            "placed_at": "2026-05-20",
            "estimated_delivery": "2026-05-24",
            "last_update": "Parcel received at Evri national hub",
            "last_update_at": "2026-05-24T18:05:00",
            "last_known_location": None,
            "items": [{"name": "Waxed Cotton Jacket (Navy, XL)", "product_id": "PROD-WAXED-JACKET", "size": "XL"}],
            "sla_breached": True,
        },
        # Multi-order customer — most recent order (for order selection testing)
        "PAS-10063": {
            "order_id": "PAS-10063",
            "status": "in_transit",
            "tracking_available": True,
            "carrier": "DPD",
            "tracking_number": "15086510044",
            "placed_at": "2026-06-02",
            "estimated_delivery": "2026-06-05",
            "last_update": "In transit to local DPD depot",
            "last_update_at": "2026-06-03T06:30:00",
            "items": [{"name": "Corduroy Shirt (Teal, L)", "product_id": "PROD-CORDUROY-SHIRT", "size": "L"}],
            "sla_breached": False,
        },
        # Multi-order customer — second recent order
        "PAS-10051": {
            "order_id": "PAS-10051",
            "status": "delivered",
            "tracking_available": True,
            "carrier": "Royal Mail",
            "tracking_number": "RM998871234GB",
            "placed_at": "2026-05-22",
            "estimated_delivery": "2026-05-25",
            "delivered_at": "2026-05-25T11:04:00",
            "delivery_note": "Delivered to front door",
            "items": [
                {"name": "Ripstop Shorts (Khaki, M)", "product_id": "PROD-CANVAS-SHORTS", "size": "M"},
                {"name": "Organic Cotton Tee (Rust, M)", "product_id": "PROD-ORGANIC-TEE", "size": "M"},
            ],
            "sla_breached": False,
        },
        # Multi-order customer — third recent order
        "PAS-10044": {
            "order_id": "PAS-10044",
            "status": "delivered",
            "tracking_available": True,
            "carrier": "DPD",
            "tracking_number": "15084900871",
            "placed_at": "2026-05-10",
            "estimated_delivery": "2026-05-13",
            "delivered_at": "2026-05-13T09:55:00",
            "delivery_note": "Signed for by occupant",
            "items": [{"name": "Merino Crew Neck Jumper (Slate, S)", "product_id": "PROD-MERINO-JUMPER", "size": "S"}],
            "sla_breached": False,
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
