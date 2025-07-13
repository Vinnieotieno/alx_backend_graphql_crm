from celery import shared_task
from datetime import datetime
import requests

@shared_task
def generate_crm_report():
    query = """
    query {
        customers {
            id
        }
        orders {
            id
            totalAmount
        }
    }
    """

    resp = requests.post(
        "http://localhost:8000/graphql",
        json={"query": query}
    )
    data = resp.json()["data"]

    total_customers = len(data["customers"])
    total_orders = len(data["orders"])
    total_revenue = sum(float(o["totalAmount"]) for o in data["orders"])

    log_path = "/tmp/crm_report_log.txt"
    with open(log_path, "a") as f:
        f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Report: {total_customers} customers, {total_orders} orders, {total_revenue} revenue\n")
