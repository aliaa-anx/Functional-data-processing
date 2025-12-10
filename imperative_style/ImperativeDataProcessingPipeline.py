import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Read the dataset
df = pd.read_csv("retail_store_sales.csv")
print("Read file retail_store_sales.csv")

# Check if there is any missing data in general
print("Check if there is any missing data ")
print(df.isnull().any())

# Show how many missing values are in each column
# print(df.isnull().sum())

# Remove rows where Item is missing
rows_to_keep = []
for i in range(len(df)):
    if pd.notnull(df.loc[i, 'Item']):
        rows_to_keep.append(i)
df = df.loc[rows_to_keep].reset_index(drop=True)

# Handle Discount Applied (fill missing with false)
for i in range(len(df)):
    if pd.isnull(df.loc[i, 'Discount Applied']):
        df.loc[i, 'Discount Applied'] = False

# Fill missing numerical columns with mean
numerical_cols = ['Price Per Unit', 'Quantity', 'Total Spent']
for col in numerical_cols:
    total = 0
    count = 0
    for i in range(len(df)):
        if pd.notnull(df.loc[i, col]):
            total += df.loc[i, col]
            count += 1
    mean_value = total / count if count > 0 else 0

    for i in range(len(df)):
        if pd.isnull(df.loc[i, col]):
            df.loc[i, col] = mean_value
print("All Missing data Have been processed.")
print(df.isnull().any())

# Standardize formats (e.g., dates, numerical precision).
print("Standardize Date Format")
date_col_name = 'Transaction Date'
default_date = '2025-01-01'
for i in range(len(df)):
    dt = pd.to_datetime(df.loc[i, date_col_name], errors='coerce')
    if pd.notnull(dt):
        df.loc[i, date_col_name] = dt.strftime('%Y-%m-%d')
    else:
        # Replace missing/invalid dates with default
        df.loc[i, date_col_name] = default_date

# Standardize 'Price Per Unit' and 'Total Spent' to two decimal places
print("Standardize Price Per Unit and Total Spent ")
precision_cols = ['Price Per Unit', 'Total Spent']
for col in precision_cols:
    for i in range(len(df)):
        df.loc[i, col] = float(round(df.loc[i, col], 2))

# Standardize 'Quantity' to ensure it's an integer
print("Standardize Quantity")
for i in range(len(df)):
    if pd.notnull(df.loc[i, 'Quantity']):
        df.loc[i, 'Quantity'] = int(df.loc[i, 'Quantity'])

# save the new csv file
clean_file = "retail_store_sales_clean.csv"
df.to_csv("retail_store_sales_clean.csv", index=False, float_format="%.2f")
print("Cleaned data saved to 'retail_store_sales_clean.csv'")

# Read data from the new file
dfn = pd.read_csv("retail_store_sales_clean.csv")

# Higher-order
def filter_rows(df, condition_func):
    return df[condition_func(df)]

# Higher-order
def add_column(df, new_col, transform_func):
    df[new_col] = transform_func(df)
    return df

# Higher-order
def aggregate(df, group_col, agg_col, agg_func):
    result = df.groupby(group_col)[agg_col].agg(agg_func).reset_index()
    return result

# Higher-order
def compute_stat(df, col, stat_func):
    return stat_func(df[col])


# Filter sales: Sales > 200
condition_func = lambda df: df["Total Spent"] > 200
filtered_dfn = filter_rows(dfn, condition_func)

filtered_dfn.to_csv("Filtered_Total_Spent_Over_200.csv", index=False)
print("Filtered data saved in Filtered_Total_Spent_Over_200.csv")

# Compute new column: Day of the week
dfn["Transaction Date"] = pd.to_datetime(dfn["Transaction Date"], errors="coerce")

weekday_transform = lambda df: df["Transaction Date"].dt.day_name()
dfn = add_column(dfn, "Weekday", weekday_transform)

dfn.to_csv("sales_data_with_weekday.csv", index=False)
print("Updated CSV with Weekday column saved as: retail_sales_data_with_weekday.csv")

# Aggregate data by key: Total sales per year
dfn["Transaction Date"] = pd.to_datetime(dfn["Transaction Date"], errors="coerce")
dfn["Year"] = dfn["Transaction Date"].dt.year

sum_strategy = lambda col: col.sum().round(2)
total_sales_per_year = aggregate(dfn, "Year", "Total Spent", sum_strategy)

print("---- Total Sales Per Year ----")
print(total_sales_per_year)


# Statistical summaries
columns = ["Price Per Unit", "Quantity", "Total Spent"]

# Strategy functions
mean_func = lambda col: round(col.mean(), 2)
median_func = lambda col: round(col.median(), 2)
variance_func = lambda col: round(col.var(), 2)

for col in columns:
    mean_value = compute_stat(df, col, mean_func)
    median_value = compute_stat(df, col, median_func)
    variance_value = compute_stat(df, col, variance_func)

    print(f"---- Statistics for {col} ----")
    print(f"Mean: {mean_value}")
    print(f"Median: {median_value}")
    print(f"Variance: {variance_value}\n")


# Compute correlation matrix
correlation_matrix = round(df[columns].corr(), 2)
print("---- Correlation Matrix ----")
print(correlation_matrix)

# Bar chart: total sales per year

plt.figure(figsize=(10,6))
sns.barplot(x="Year", y="Total Spent", data=total_sales_per_year, palette="Purples_d")

# Writing the numbers above each column

for index, row in total_sales_per_year.iterrows():
    plt.text(index, row["Total Spent"] + 10, str(row["Total Spent"]),
             ha='center', va='bottom', fontsize=10)

plt.title("Total Sales Per Year")
plt.xlabel("Year")
plt.ylabel("Total Spent")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("total_sales_per_year.png")
plt.show()


"""
# Test the new file for missing data
df_test = pd.read_csv(clean_file)
missing_counts = {}
for col in df_test.columns:
    count = 0
    for i in range(len(df_test)):
        if pd.isnull(df_test.loc[i, col]):
            count += 1
    missing_counts[col] = count

print("Remaining missing values in the cleaned file:")
print(missing_counts)
"""









