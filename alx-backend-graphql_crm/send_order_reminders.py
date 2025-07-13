#!/usr/bin/env python3

import requests
import json
from datetime import datetime, timedelta

def main():
    url = "http://localhost:8000/graphql"

    query = """
    query GetRecentOrders {
      orders(orderDate_Gte: "%s") {
        id
        customer {
          email
        }
      }
    }
    """ % (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")

    response = requests.post(
        url,
        json={'query': query}
    )
    data = response.json()

    log_path = "/tmp/order_reminders_log.txt"
    with open(log_path, "a") as f:
        for order in data["data"]["orders"]:
            f.write("%s - Order ID: %s, Customer Email: %s\n" % (
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                order["id"],
                order["customer"]["email"]
            ))

    print("Order reminders processed!")

if __name__ == "__main__":
    main()
