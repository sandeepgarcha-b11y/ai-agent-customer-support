"""Mock tools for customer account queries."""

from langchain_core.tools import tool


@tool
def lookup_account(email: str) -> dict:
    """Look up a customer account by email address."""
    mock_accounts = {
        # Single recent order — untracked within SLA
        "clara.jones@example.com": {
            "email": "clara.jones@example.com",
            "name": "Clara Jones",
            "account_status": "active",
            "last_login": "2026-06-02",
            "flags": [],
            "recent_order_ids": ["PAS-10061"],
            "loyalty_tier": "Trailblazer",
        },
        # Single recent order — untracked outside SLA
        "tom.wright@example.com": {
            "email": "tom.wright@example.com",
            "name": "Tom Wright",
            "account_status": "active",
            "last_login": "2026-06-01",
            "flags": [],
            "recent_order_ids": ["PAS-10057"],
            "loyalty_tier": "Explorer",
        },
        # Single recent order — tracked, within window
        "priya.mehta@example.com": {
            "email": "priya.mehta@example.com",
            "name": "Priya Mehta",
            "account_status": "active",
            "last_login": "2026-06-03",
            "flags": [],
            "recent_order_ids": ["PAS-10062"],
            "loyalty_tier": "Explorer",
        },
        # Single recent order — tracked, outside window, at depot
        "ben.hayes@example.com": {
            "email": "ben.hayes@example.com",
            "name": "Ben Hayes",
            "account_status": "active",
            "last_login": "2026-05-30",
            "flags": [],
            "recent_order_ids": ["PAS-10048"],
            "loyalty_tier": "Trailblazer",
        },
        # Single recent order — delivered, customer says not received
        "sarah.okafor@example.com": {
            "email": "sarah.okafor@example.com",
            "name": "Sarah Okafor",
            "account_status": "active",
            "last_login": "2026-05-29",
            "flags": [],
            "recent_order_ids": ["PAS-10042"],
            "loyalty_tier": "Pioneer",
        },
        # Single recent order — genuinely lost
        "james.liu@example.com": {
            "email": "james.liu@example.com",
            "name": "James Liu",
            "account_status": "active",
            "last_login": "2026-05-25",
            "flags": [],
            "recent_order_ids": ["PAS-10039"],
            "loyalty_tier": "Explorer",
        },
        # Multiple recent orders — for order selection testing
        "nina.patel@example.com": {
            "email": "nina.patel@example.com",
            "name": "Nina Patel",
            "account_status": "active",
            "last_login": "2026-06-03",
            "flags": [],
            "recent_order_ids": ["PAS-10063", "PAS-10051", "PAS-10044"],
            "loyalty_tier": "Pioneer",
        },
        # Placeholder accounts for other flows (not used in WISMO)
        "locked.user@example.com": {
            "email": "locked.user@example.com",
            "name": "Alex Morgan",
            "account_status": "locked",
            "last_login": "2026-04-10",
            "flags": ["too_many_failed_logins"],
            "recent_order_ids": [],
            "loyalty_tier": "Trailblazer",
        },
        "flagged.user@example.com": {
            "email": "flagged.user@example.com",
            "name": "Sam Clarke",
            "account_status": "active",
            "last_login": "2026-05-15",
            "flags": ["suspected_fraud"],
            "recent_order_ids": [],
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
