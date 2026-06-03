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
        ("PROD-LINEN-TROUSERS", "8"): "available",
        ("PROD-LINEN-TROUSERS", "10"): "available",
        ("PROD-LINEN-TROUSERS", "12"): "out_of_stock",
        ("PROD-LINEN-TROUSERS", "14"): "low",
        ("PROD-LINEN-TROUSERS", "16"): "available",
        ("PROD-CANVAS-SHORTS", "S"): "available",
        ("PROD-CANVAS-SHORTS", "M"): "available",
        ("PROD-CANVAS-SHORTS", "L"): "available",
        ("PROD-FLEECE-JACKET", "XS"): "available",
        ("PROD-FLEECE-JACKET", "S"): "available",
        ("PROD-FLEECE-JACKET", "M"): "available",
        ("PROD-FLEECE-JACKET", "L"): "low",
        ("PROD-FLEECE-JACKET", "XL"): "out_of_stock",
        ("PROD-CANVAS-OVERSHIRT", "XS"): "available",
        ("PROD-CANVAS-OVERSHIRT", "S"): "available",
        ("PROD-CANVAS-OVERSHIRT", "M"): "available",
        ("PROD-CANVAS-OVERSHIRT", "L"): "low",
        ("PROD-CANVAS-OVERSHIRT", "XL"): "out_of_stock",
        ("PROD-ORGANIC-TEE", "XS"): "available",
        ("PROD-ORGANIC-TEE", "S"): "available",
        ("PROD-ORGANIC-TEE", "M"): "available",
        ("PROD-ORGANIC-TEE", "L"): "available",
        ("PROD-ORGANIC-TEE", "XL"): "low",
        ("PROD-MERINO-BEANIE", "ONE SIZE"): "available",
        ("PROD-WAXED-JACKET", "XS"): "available",
        ("PROD-WAXED-JACKET", "S"): "available",
        ("PROD-WAXED-JACKET", "M"): "available",
        ("PROD-WAXED-JACKET", "L"): "available",
        ("PROD-WAXED-JACKET", "XL"): "out_of_stock",
        ("PROD-CORDUROY-SHIRT", "XS"): "low",
        ("PROD-CORDUROY-SHIRT", "S"): "available",
        ("PROD-CORDUROY-SHIRT", "M"): "available",
        ("PROD-CORDUROY-SHIRT", "L"): "available",
        ("PROD-CORDUROY-SHIRT", "XL"): "low",
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
