import pandas as pd
import mysql.connector

# ==========================================
# Connect to MySQL
# ==========================================
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="24112004",
    database="FinancialFraudDB"
)

# ==========================================
# Read Data
# ==========================================
query = "SELECT * FROM transactions"
df = pd.read_sql(query, conn)
conn.close()

print("Database Connected Successfully!")

# ==========================================
# Convert Amount
# ==========================================
df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")

# ==========================================
# Convert Time
# ==========================================
df["Transaction_Time"] = pd.to_datetime(
    df["Transaction_Time"],
    format="%H:%M:%S",
    errors="coerce"
)

df["Hour"] = df["Transaction_Time"].dt.hour

# ==========================================
# Create Fraud Flag
# ==========================================
df["Fraud_Flag"] = "Normal"

# Rule 1
rule1 = (
    (df["Amount"] >= 20000) &
    (df["Hour"].between(0,5))
)

# Rule 2
rule2 = (
    (df["Previous_Fraud_History"] == "Yes") &
    (df["Amount"] >= 7000)
)

# Rule 3
rule3 = (
    (df["Transaction_Type"] == "Online") &
    (df["Merchant_Category"] == "Electronics") &
    (df["Amount"] >= 8000)
)

# Rule 4
rule4 = (
    (df["City"] != df["Home_City"]) &
    (df["Amount"] >= 10000)
)

# Rule 5
rule5 = (
    (df["Device_Type"] == "Mobile") &
    (df["Transaction_Type"].isin(["Online","UPI"])) &
    (df["Amount"] >= 8000)
)

# Apply Rules
df.loc[
    rule1 | rule2 | rule3 | rule4 | rule5,
    "Fraud_Flag"
] = "Fraud"

# Remove Hour column
df.drop(columns=["Hour"], inplace=True)

# ==========================================
# Summary BEFORE Saving
# ==========================================
print("\nBefore Saving CSV")
print(df["Fraud_Flag"].value_counts())

fraud_rate = (df["Fraud_Flag"] == "Fraud").mean() * 100
print(f"Fraud Rate : {fraud_rate:.2f}%")

# ==========================================
# Save CSV
# ==========================================
output_file = "fraud_report.csv"

df.to_csv(output_file, index=False)

print("\nCSV Saved Successfully!")

# ==========================================
# Verify Saved CSV
# ==========================================
check = pd.read_csv(output_file)

print("\nAfter Reading Saved CSV")
print(check["Fraud_Flag"].value_counts())

print("\nFile Name :", output_file)

import os
print(os.path.abspath("fraud_report.csv"))