import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")

np.random.seed(42)

n = 1200
categories = ["Electronics", "Clothing", "Home & Garden", "Sports", "Books"]
cat_weights = [0.30, 0.25, 0.20, 0.15, 0.10]
countries = ["USA", "UK", "Canada", "Australia", "Germany"]
pay_methods = ["Credit Card", "PayPal", "Debit Card", "Bank Transfer"]
statuses = ["Completed", "Completed", "Completed", "Returned", "Cancelled"]

dates = pd.date_range("2023-01-01", "2023-12-31", periods=n)
category = np.random.choice(categories, n, p=cat_weights)
price_map = {"Electronics": (50, 900), "Clothing": (15, 180),
             "Home & Garden": (20, 350), "Sports": (25, 400), "Books": (8, 60)}
prices = np.array([round(np.random.uniform(*price_map[c]), 2) for c in category])
quantities = np.random.choice([1, 2, 3, 4, 5], n, p=[0.50, 0.25, 0.13, 0.07, 0.05])

df = pd.DataFrame({
    "order_id": range(1001, 1001 + n),
    "date": dates,
    "customer_id": np.random.randint(1, 401, n),
    "category": category,
    "unit_price": prices,
    "quantity": quantities,
    "country": np.random.choice(countries, n),
    "payment": np.random.choice(pay_methods, n),
    "status": np.random.choice(statuses, n),
})

for col in ["unit_price", "quantity"]:
    df.loc[df.sample(frac=0.03).index, col] = np.nan

df["unit_price"].fillna(df.groupby("category")["unit_price"].transform("median"), inplace=True)
df["quantity"].fillna(1, inplace=True)
df.drop_duplicates(inplace=True)
df["quantity"] = df["quantity"].fillna(1).astype(int)
df["revenue"] = (df["unit_price"] * df["quantity"]).round(2)
df["month"] = df["date"].dt.month

completed = df[df["status"] == "Completed"].copy()

print("Total Revenue:", completed["revenue"].sum().round(2))
print("Completed Orders:", len(completed))
print("Avg Order Value:", completed["revenue"].mean().round(2))
print("Unique Customers:", completed["customer_id"].nunique())
print("Return Rate:", round((df["status"] == "Returned").mean() * 100, 1), "%")
