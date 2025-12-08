import operator
import csv
from itertools import groupby
from functools import reduce


# 1. filter functions and helper function create condition
def create_condition(field_name, op_func, target_value):
    def condition(record):
        return op_func(record.get(field_name), target_value)

    return condition


def filter_records(records, condition):
    # returns a new list
    return list(filter(condition, records))


# ------------------------------- 2. add column funtion------------------------------------------------------

def add_column(records, column_name, compute_fn):
    # returns a new list with new columns
    return list(map(lambda r: {**r, column_name: compute_fn(r)}, records))


# the new columns calculations
# 1. calculate expected total
def calculate_expected_total(records):
    price = records.get("Price Per Unit", 0)
    quantity = records.get("Quantity", 0)
    return round(price * quantity)


# 2. calculate_taxe
def calculate_tax(records):
    total_spent = records.get("Total Spent", 0)
    return round(total_spent * 0.25)


# -----------------------------------------------------3. group by function------------------------------------
def group_by(records, key):
    sorted_data = sorted(records, key=key)

    # pipeline

    # 1. groupby will group data based on the given key (key ,group)
    # 2. map will return list  (key,list(group))
    # 3. dicionary will make it into a dictionary  again like that {key: v}
    return dict(map(
        lambda item: (item[0], list(item[1])),  # item[0] is key and item[1] is iterator
        groupby(sorted_data, key=key)
    ))


# --------------------------------------------------4. aggregate function------------------------------------------
def aggregate(groups, agg_fn):
    # aggregate based on teh grouped items
    return dict(map(
        lambda item: (item[0], agg_fn(item[1])),
        groups.items()
    ))


def sum_revenue(records):
    # [{'Total': 10}, {'Total': 20}] into [10, 20]
    amounts = map(lambda r: r['Total Spent'], records)
    # [10, 20] into 30 using addition
    return reduce(operator.add, amounts, 0)


# -----------------------------------------------------5. drop column------------------------------------------------
def drop_column(records, name):
    return list(map(
        lambda r: dict(filter(
            lambda item: item[0] != name,
            r.items()
        )), records
    ))


# ---------------------------------------------------6. map function ---------------------------------------------------
def map_records(records, transform_fn):
    return list(map(transform_fn, records))


def fix_types(records):
    new_record = records.copy()

    # Internal helper to safely convert
    def safe_float(value):
        if value is None or value == '':
            return 0.0
        try:
            return float(value)
        except ValueError:
            return 0.0

    new_record['Total Spent'] = safe_float(records.get('Total Spent'))
    new_record['Quantity'] = safe_float(records.get('Quantity'))
    new_record['Price Per Unit'] = safe_float(records.get('Price Per Unit'))
    return new_record


# ==========================================
# 2. THE TEST SCRIPT (Execution)
# ==========================================

print("--- STARTING MEMBER 2 PIPELINE TEST ---\n")

# 1. LOAD CSV
# ---------------------------------------------------------
data = []
try:
    with open('retail_store_sales.csv', 'r') as f:
        reader = csv.DictReader(f)
        data = list(reader)
    print(f"1. LOAD: Loaded {len(data)} records from CSV.")
except FileNotFoundError:
    print("Error: 'retail_store_sales.csv' not found.")
    exit()

# 2. TEST MAP (Fix Types)
# ---------------------------------------------------------
# We MUST fix types first because CSV loads numbers as strings like "18.5"
data_typed = map_records(data, fix_types)
print(f"2. MAP: Fixed types. Sample 'Total Spent': {data_typed[0]['Total Spent']} (Type: {type(data_typed[0]['Total Spent'])})")

# 3. TEST FILTER (Total Spent > 0)
# ---------------------------------------------------------
positive_condition = create_condition('Total Spent', operator.gt, 0)
data_filtered = filter_records(data_typed, positive_condition)
print(f"3. FILTER: Kept {len(data_filtered)} positive records (Dropped {len(data_typed) - len(data_filtered)}).")

# 4. TEST ADD COLUMN (Expected Total & Tax)
# ---------------------------------------------------------
data_w_expected = add_column(data_filtered, 'Expected Total', calculate_expected_total)
data_w_tax = add_column(data_w_expected, 'Tax', calculate_tax)
print(f"4. ADD COLUMN: Added 'Expected Total' & 'Tax'. Sample Record 1: Expected={data_w_tax[0]['Expected Total']}, Tax={data_w_tax[0]['Tax']}")

# 5. TEST DROP COLUMN (Remove 'Item')
# ---------------------------------------------------------
data_dropped = drop_column(data_w_tax, 'Item')
print(f"5. DROP COLUMN: Removed 'Item'. Remaining Keys: {list(data_dropped[0].keys())}")

# 6. TEST GROUP BY (Category)
# ---------------------------------------------------------
# We group by Category. Lambda extracts the key.
grouped_data = group_by(data_dropped, lambda r: r['Category'])
print(f"6. GROUP BY: Found {len(grouped_data)} categories: {list(grouped_data.keys())}")

# 7. TEST AGGREGATE (Sum Revenue)
# ---------------------------------------------------------
final_report = aggregate(grouped_data, sum_revenue)
print("\n--- 7. FINAL AGGREGATE REPORT (Revenue per Category) ---")
import pprint
pprint.pprint(final_report)