import logging
import os
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from pydantic import Field
from src.api.client import ApiClient
from src import constant
from src.business.bonds import get_iconnect_bond_products

def configure_logging():
    # Remove all handlers associated with the root logger object.
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - [%(filename)s:%(lineno)d - %(levelname)s - %(message)s]',
        handlers=[
            logging.FileHandler("app.log", mode="a", encoding="utf-8"),
            logging.StreamHandler()
        ]
    )
    logging.info("Logging configured. Writing to app.log.")

def load_configuration(env_path=None):
    # Allow custom .env path for CLI usage
    if env_path is None:
        env_path = os.environ.get("DOTENV_PATH", ".env")
    load_dotenv(env_path, override=True)
    config = {
        "API_KEY": os.getenv("TCBS_API_KEY"),
        "BASE_URL": os.getenv("BASE_URL", "https://apiextaws.tcbs.com.vn"),
    }
    return config

def create_server(env_path=None):
    configure_logging()
    config = load_configuration(env_path)
    logger = logging.getLogger(__name__)
    logger.info("Starting server with configuration: %s", config)

    mcp = FastMCP("TCinvest MCP Server")
    client_aws = ApiClient(config['API_KEY'], constant.API_EXT_AWS)
    client = ApiClient(config['API_KEY'], constant.API_EXT)
    
    @mcp.tool()
    def get_iconnect_bond_products_tool(filter: str = "channel:cus,markettype:iconnect", level: str="basic", order_by: str = "code(asc)", excludePP: int = 0) -> dict:
        """
        Get bond products from iConnect.
        """
        logger.info("Fetching bond products with filter: %s", filter)
        return get_iconnect_bond_products(client, filter, level, order_by, excludePP)

    return mcp

if __name__ == "__main__":
    server = create_server()
    server.run(transport="sse")