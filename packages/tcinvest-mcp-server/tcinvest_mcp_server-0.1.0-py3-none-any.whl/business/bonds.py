from src.api.client import ApiClient


def get_iconnect_bond_products(client: ApiClient, filter: str = "channel:cus,markettype:iconnect", level: str="basic", order_by: str = "code(asc)", excludePP: int = 0) -> dict:
    """
    Get bond products from iConnect.
    """
    # Assuming `client` is an instance of ApiClient
    response = client.get("bond-trading/v1/products", params={
        "filter": filter,
        "level": level,
        "order_by": order_by,
        "excludePP": excludePP
    })
    return response