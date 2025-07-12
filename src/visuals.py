import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set style
sns.set(style="whitegrid")

# Use absolute path relative to this script's location
base_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(base_dir, "..", "output", "cleaned_merged_travel_data.csv")
merged_df = pd.read_csv(data_path)

# Convert dates
merged_df['booking_date'] = pd.to_datetime(merged_df['booking_date'])
merged_df['travel_date'] = pd.to_datetime(merged_df['travel_date'])

# Create output directory for visuals
os.makedirs("visuals", exist_ok=True)

# === 1. Top 10 Destination Countries ===
top_destinations = merged_df['destination_country'].value_counts().head(10)
plt.figure(figsize=(10, 6))
sns.barplot(x=top_destinations.values, y=top_destinations.index, palette="crest")
plt.title("Top 10 Destination Countries")
plt.xlabel("Number of Bookings")
plt.ylabel("Country")
plt.tight_layout()
plt.savefig("visuals/top_destinations.png")
plt.close()

# === 2. Booking Trend Over Time ===
daily_bookings = merged_df['booking_date'].dt.to_period('M').value_counts().sort_index()
plt.figure(figsize=(12, 6))
daily_bookings.plot(kind='line', marker='o')
plt.title("Monthly Booking Trend")
plt.xlabel("Month")
plt.ylabel("Number of Bookings")
plt.tight_layout()
plt.savefig("visuals/booking_trend.png")
plt.close()

# === 3. Revenue Distribution ===
plt.figure(figsize=(10, 6))
sns.histplot(merged_df['amount_usd'], bins=50, kde=True, color='teal')
plt.title("Revenue Distribution per Booking")
plt.xlabel("Booking Revenue (USD)")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig("visuals/revenue_distribution.png")
plt.close()

# === 4. Age Distribution ===
plt.figure(figsize=(10, 6))
sns.histplot(merged_df['age'], bins=20, kde=True, color='orchid')
plt.title("User Age Distribution")
plt.xlabel("Age")
plt.ylabel("Number of Users")
plt.tight_layout()
plt.savefig("visuals/age_distribution.png")
plt.close()

# === 5. Loyalty Status Breakdown ===
plt.figure(figsize=(8, 6))
sns.countplot(data=merged_df, x='loyalty_status', order=merged_df['loyalty_status'].value_counts().index, palette="pastel")
plt.title("Loyalty Status Breakdown")
plt.xlabel("Loyalty Status")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig("visuals/loyalty_status.png")
plt.close()

print("✅ All visualizations generated and saved in the 'visuals' directory.")
