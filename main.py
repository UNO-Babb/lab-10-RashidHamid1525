#MapPlot.py
#Name:
#Date:
#Assignment:

import pandas as pd
import matplotlib.pyplot as plt

print("Loading dataset...")
df = pd.read_csv("billionaires.csv")

print("Initial shape:", df.shape)
print("Columns:", df.columns.tolist())
print(df.head())

df.columns = [
    c.strip().replace(" ", "_").replace(".", "_").replace("/", "_")
    for c in df.columns
]

wealth_col = None
for c in df.columns:
    if "worth" in c.lower():
        wealth_col = c
        break

if wealth_col is None:
    raise ValueError("Could not find wealth column. Check column names.")

print(f"Using wealth column: {wealth_col}")

df[wealth_col] = pd.to_numeric(df[wealth_col], errors="coerce")
df = df.dropna(subset=["year", wealth_col])
df["year"] = df["year"].astype(int)

print("After cleaning:", df.shape)

upper_limit = df[wealth_col].quantile(0.995)
df_trim = df[df[wealth_col] <= upper_limit].copy()

year = 2014
df_year = df[df["year"] == year].nlargest(15, wealth_col)

plt.figure(figsize=(10, 6))
plt.barh(df_year["name"][::-1], df_year[wealth_col][::-1])
plt.xlabel("Net Worth (Billions USD)")
plt.title(f"Top 15 Billionaires in {year}")
plt.tight_layout()
plt.savefig("plot_top15.png")
plt.close()

print("Saved: plot_top15.png")

grouped = df.groupby("year")[wealth_col].agg(["count", "sum"]).reset_index()

plt.figure(figsize=(10, 5))
plt.plot(grouped["year"], grouped["count"], marker="o")
plt.xlabel("Year")
plt.ylabel("Number of Billionaires in Dataset")
plt.title("Count of Billionaires by Year")
plt.grid(True)
plt.tight_layout()
plt.savefig("plot_count_by_year.png")
plt.close()

print("Saved: plot_count_by_year.png")

plt.figure(figsize=(8, 5))
plt.hist(df_trim[wealth_col].dropna(), bins=40)
plt.xlabel("Net Worth (Billions USD)")
plt.ylabel("Count")
plt.title("Distribution of Billionaire Net Worth (trimmed)")
plt.tight_layout()
plt.savefig("plot_distribution.png")
plt.close()

print("Saved: plot_distribution.png")

gdp_col = None
for c in df.columns:
    if "gdp" in c.lower():
        gdp_col = c
        break

if gdp_col:
    plt.figure(figsize=(8, 6))
    plt.scatter(df_trim[gdp_col], df_trim[wealth_col], alpha=0.6)
    plt.xs
