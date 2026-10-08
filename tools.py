"""Milestone 4: the order lookup tool, as a plain Python function (easy to test)."""
import csv
from pathlib import Path

ORDERS_FILE = Path(__file__).parent / "orders.csv"


def get_order_status(order_id: str) -> str:
    """Look up a KartEase order by its order ID (for example KE1002) and return its
    product, status, date and payment method."""
    wanted = order_id.strip().upper()
    with open(ORDERS_FILE, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["order_id"].upper() == wanted:
                if row["status"] in ("Delivered", "Return picked up"):
                    date_text = f"Delivered on: {row['expected_or_delivered_date']}"
                elif row["expected_or_delivered_date"]:
                    date_text = f"Expected delivery: {row['expected_or_delivered_date']}"
                else:
                    date_text = "Delivery date: not applicable"
                return (
                    f"Order {row['order_id']}: {row['product']} ({row['category']}). "
                    f"Status: {row['status']}. Order date: {row['order_date']}. "
                    f"{date_text}. Amount: Rs {row['amount_inr']}. "
                    f"Payment method: {row['payment_method']}."
                )
    return f"No order found with ID {order_id}. Please check the order ID and try again."
