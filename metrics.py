def get_customer_metrics(*, data, from_, to, min_total_spend=None):
    raise NotImplementedError("Not implemented")
from collections import defaultdict


def get_customer_metrics(data, from_, to, min_total_spend=None):
    customers = defaultdict(lambda: {"orderCount": 0, "totalSpend": 0})

    for order in data:
        order_date = order["orderDate"]

        if not (from_ <= order_date <= to):
            continue

        order_total = sum(
            item["quantity"] * item["unitPrice"]
            for item in order.get("lineItems", [])
        )

        customer_id = order["customerId"]

        customers[customer_id]["orderCount"] += 1
        customers[customer_id]["totalSpend"] += order_total

    results = []

    for customer_id, metrics in customers.items():
        total_spend = metrics["totalSpend"]
        order_count = metrics["orderCount"]

        if (
            min_total_spend is not None
            and total_spend < min_total_spend
        ):
            continue

        results.append(
            {
                "customerId": customer_id,
                "orderCount": order_count,
                "totalSpend": total_spend,
                "avgOrderValue": total_spend / order_count,
            }
        )

    return sorted(results, key=lambda x: x["customerId"])
