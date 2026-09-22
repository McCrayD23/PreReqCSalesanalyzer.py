import csv

sales_data = []

with open("sales_data.csv", "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        # Convert quantity to int()
        row["quantity"] = int(row["quantity"])
        row["price"] = float(row["price"])
        sales_data.append(row)

print(f"Loaded {len(sales_data)} sales records.")

"""Step 2. Analyze and Group Data"""

total_revenue = 0.0
product_stats = {}
daily_revenue = {}

for row in sales_data:
    product = row["product"]
    qty = row["quantity"]
    price = row["price"]
    date = row["date"]

    # Calculate row revenue
    item_revenue = qty * price
    total_revenue += item_revenue

    # Group by Product
    if product not in product_stats:
        product_stats[product] = {"quantity": 0, "revenue": 0.0}
    product_stats[product]["quantity"] += qty
    product_stats[product]["revenue"] += item_revenue

    # Group by Date (to find highest revenue day)
    if date not in daily_revenue:
        daily_revenue[date] = 0.0
    daily_revenue[date] += item_revenue

# Find the best revenue day
best_day = max(daily_revenue, key=daily_revenue.get)
best_day_revenue = daily_revenue[best_day]


with open("sales_report.txt", "w") as file:
    file.write("Sales Report Analysis Summary\n")
    file.write("=" * 35 + "\n\n")
    file.write(f"Total Overall Revenue: ${total_revenue:.2f}\n")
    file.write(f"Highest Revenue Day: {best_day} (${best_day_revenue:.2f})\n\n")

    file.write("Revenue and Quantity by product:\n")
    file.write("-" * 35 + "\n")
    for product, stats in product_stats.items():
        file.write(f"{product}: {stats['quantity']} units sold | Total: ${stats['revenue']:.2f}\n")

print("Sales report written to: sales_report.txt")

summary_rows = []
for product, stats in product_stats.items():
    summary_rows.append({
        "product": product,
        "total_quantity": stats["quantity"],
        "total_revenue": round(stats["revenue"], 2)
    })

fieldnames= ["product", "total_quantity", "total_revenue"]

with open("product_summary.csv", "w") as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(summary_rows)

print("Product summary written to: product_summary.csv")
