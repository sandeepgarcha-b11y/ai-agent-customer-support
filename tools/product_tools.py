"""Mock tools for product and stock queries."""

from langchain_core.tools import tool


@tool
def check_stock(product_id: str, size: str) -> dict:
    """Check the stock level for a product in a given size."""
    inventory = {
        ("PROD-MERINO-JUMPER", "XS"): "low",
        ("PROD-MERINO-JUMPER", "S"): "available",
        ("PROD-MERINO-JUMPER", "M"): "available",
        ("PROD-MERINO-JUMPER", "L"): "low",
        ("PROD-MERINO-JUMPER", "XL"): "out_of_stock",
        ("PROD-LINEN-SHIRT", "XS"): "out_of_stock",
        ("PROD-LINEN-SHIRT", "S"): "out_of_stock",
        ("PROD-LINEN-SHIRT", "M"): "low",
        ("PROD-LINEN-SHIRT", "L"): "available",
        ("PROD-CANVAS-SHORTS", "S"): "available",
        ("PROD-CANVAS-SHORTS", "M"): "available",
        ("PROD-CANVAS-SHORTS", "L"): "available",
        ("PROD-FLEECE-JACKET", "XS"): "available",
        ("PROD-FLEECE-JACKET", "S"): "available",
        ("PROD-FLEECE-JACKET", "M"): "available",
        ("PROD-FLEECE-JACKET", "L"): "low",
        ("PROD-FLEECE-JACKET", "XL"): "out_of_stock",
    }
    status = inventory.get((product_id, size), "unknown")
    if status == "unknown":
        return {
            "product_id": product_id,
            "size": size,
            "status": "unknown",
            "message": "Product or size not recognised.",
        }
    return {"product_id": product_id, "size": size, "status": status}
