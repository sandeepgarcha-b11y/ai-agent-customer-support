from tools.order_tools import lookup_order, check_return_eligibility, initiate_return, initiate_exchange
from tools.product_tools import check_stock
from tools.account_tools import lookup_account

ALL_TOOLS = [
    lookup_order,
    check_return_eligibility,
    initiate_return,
    initiate_exchange,
    check_stock,
    lookup_account,
]
