from data_analysis import *


# Sample dataset
records = [
    {"Price Per Unit": 38.0, "Quantity": 4.0, "Total Spent": 152.0},
    {"Price Per Unit": 6.5, "Quantity": 9.0, "Total Spent": 58.5},
    {"Price Per Unit": 14.0, "Quantity": 10.0, "Total Spent": 140.0},
    {"Price Per Unit": 14.0, "Quantity": 6.0, "Total Spent": 84.0},
    {"Price Per Unit": 17.0, "Quantity": 3.0, "Total Spent": 51.0},
]

fields = ["Price Per Unit", "Quantity", "Total Spent"]

# Mean
prices = [r["Price Per Unit"] for r in records]
print("Mean Price:", mean(prices))


# Median
print("Median Quantity:", median([r["Quantity"] for r in records]))


# Variance
print("Variance Total Spent:", variance([r["Total Spent"] for r in records]))

# Summaries
print("\nSummaries for all fields:")
summary_result = summaries(records, fields)
for field, stats in summary_result.items():
    print(f"{field}: {stats}")

# Correlation
quantity = [r["Quantity"] for r in records]
total_spent = [r["Total Spent"] for r in records]
print("\nCorrelation between Quantity and Total Spent:", correlation(quantity, total_spent))


# Compute Trend
sales_over_time = [r["Total Spent"] for r in records]
print("Trend (percent change) of Total Spent:", compute_trend(sales_over_time))

