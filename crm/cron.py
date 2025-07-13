import requests
from datetime import datetime

def log_crm_heartbeat():
    timestamp = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    message = f"{timestamp} CRM is alive"

    try:
        resp = requests.post(
            "http://localhost:8000/graphql",
            json={"query": "{ hello }"}
        )
        if resp.status_code == 200:
            message += " - GraphQL OK"
        else:
            message += " - GraphQL error"
    except Exception as e:
        message += f" - GraphQL unreachable: {str(e)}"

    with open("/tmp/crm_heartbeat_log.txt", "a") as f:
        f.write(message + "\n")
def update_low_stock():
    from datetime import datetime
    import requests

    query = """
    mutation {
        updateLowStockProducts {
            success
            products {
                name
                stock
            }
        }
    }
    """

    resp = requests.post(
        "http://localhost:8000/graphql",
        json={'query': query}
    )
    data = resp.json()

    log_path = "/tmp/low_stock_updates_log.txt"
    with open(log_path, "a") as f:
        f.write(
            f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {data['data']['updateLowStockProducts']['success']}\n"
        )
        for p in data['data']['updateLowStockProducts']['products']:
            f.write(f"Product: {p['name']}, New Stock: {p['stock']}\n")
