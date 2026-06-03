"""Mock tools for customer account queries."""

from langchain_core.tools import tool


@tool
def lookup_account(email: str) -> dict:
    """Look up a customer account by email address."""
    mock_accounts = {
        "jane.doe@example.com": {
            "email": "jane.doe@example.com",
            "name": "Jane Doe",
            "account_status": "active",
            "last_login": "2026-05-29",
            "flags": [],
            "orders_count": 7,
            "loyalty_tier": "Explorer",
        },
        "locked.user@example.com": {
            "email": "locked.user@example.com",
            "name": "Alex Morgan",
            "account_status": "locked",
            "last_login": "2026-04-10",
            "flags": ["too_many_failed_logins"],
            "orders_count": 2,
            "loyalty_tier": "Trailblazer",
        },
        "flagged.user@example.com": {
            "email": "flagged.user@example.com",
            "name": "Sam Clarke",
            "account_status": "active",
            "last_login": "2026-05-15",
            "flags": ["suspected_fraud"],
            "orders_count": 12,
            "loyalty_tier": "Pioneer",
        },
    }
    account = mock_accounts.get(email.lower())
    if not account:
        return {
            "email": email,
            "account_status": "not_found",
            "error": "No account found with this email address.",
        }
    return account
