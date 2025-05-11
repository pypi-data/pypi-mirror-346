import os
import requests
import base64
from fastmcp import FastMCP
from dotenv import load_dotenv

load_dotenv()

mcp = FastMCP("Organizze MCP Server")

ORGANIZZE_API_URL = "https://api.organizze.com.br/rest/v2"


def get_auth_header():
    """Get API authentication header using environment variables"""
    
    auth_str = f"{os.getenv('ORGANIZZE_EMAIL')}:{os.getenv('ORGANIZZE_TOKEN')}"
    auth_bytes = auth_str.encode("ascii")
    auth_b64 = base64.b64encode(auth_bytes).decode("ascii")
    
    return {"Authorization": f"Basic {auth_b64}", "User-Agent": f"Diego ({os.getenv('ORGANIZZE_EMAIL')})"}

@mcp.tool()
def list_transactions(start_date: str, end_date: str):
    """List transactions for a given date range
    
    Args:
        start_date (str): The start date of the date range (YYYY-MM-DD)
        end_date (str): The end date of the date range (YYYY-MM-DD)

    Returns:
        list: A list of transaction
    """
    response = requests.get(f"{ORGANIZZE_API_URL}/transactions", headers=get_auth_header(), params={"start_date": start_date, "end_date": end_date})

    transactions = []
    for transaction in response.json():
        transactions.append({
            "id": transaction["id"],
            "date": transaction["date"],
            "amount_cents": transaction["amount_cents"]/100,
            "description": transaction["description"],
            "category_id": transaction["category_id"],
            "tags": transaction["tags"],
            "account_id": transaction["account_id"]
        })

    return transactions

@mcp.tool()
def list_categories():
    """List all categories
    
    Returns:
        list: A list of categories:
        - id: The category id
        - name: The category name
        - kind: The category kind (income, expense, transfer)
    """
    response = requests.get(f"{ORGANIZZE_API_URL}/categories", headers=get_auth_header())
    categories = []
    for category in response.json():
        categories.append({
            "id": category["id"],
            "name": category["name"],
            "kind": category["kind"]
        })
    return categories

@mcp.tool()
def set_category(transaction_id: str, category_id: str):
    """Set the category of a transaction
    Before update check if the category id isn't already correct
    
    Args:
        transaction_id (str): The transaction id
        category_id (str): The category id
    """
    response = requests.put(f"{ORGANIZZE_API_URL}/transactions/{transaction_id}", headers=get_auth_header(), json={"category_id": category_id})
    return response.json()

if __name__ == "__main__":
    mcp.run()