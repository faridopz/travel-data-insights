# travel_data_analysis.py

import os
import pandas as pd

# === 1. Load CSV files ===
base_path = os.path.expanduser('~/Desktop/dataprojectfarid')
data_path = os.path.join(base_path, 'data')

users_df = pd.read_csv(os.path.join(data_path, 'users_complex.csv'))
partners_df = pd.read_csv(os.path.join(data_path, 'partners_complex.csv'))
bookings_df = pd.read_csv(os.path.join(data_path, 'bookings_complex.csv'))
reviews_df = pd.read_csv(os.path.join(data_path, 'reviews.csv'))

# === 2. Check for missing values ===
print("Missing values in bookings:")
print(bookings_df.isnull().sum())

# === 3. Drop bookings with missing 'amount_usd' ===
bookings_df.dropna(subset=['amount_usd'], inplace=True)

# === 4. Convert columns to datetime ===
bookings_df['booking_date'] = pd.to_datetime(bookings_df['booking_date'], errors='coerce')
bookings_df['travel_date'] = pd.to_datetime(bookings_df['travel_date'], errors='coerce')
users_df['signup_date'] = pd.to_datetime(users_df['signup_date'], errors='coerce')
reviews_df['review_date'] = pd.to_datetime(reviews_df['review_date'], errors='coerce')

# Remove rows with bad date formats
bookings_df.dropna(subset=['booking_date', 'travel_date'], inplace=True)

# === 5. Add days_to_travel feature ===
bookings_df['days_to_travel'] = (bookings_df['travel_date'] - bookings_df['booking_date']).dt.days

# === 6. Merge datasets ===
merged_df = bookings_df.merge(users_df, on='user_id', how='left') \
                       .merge(partners_df, on='partner_id', how='left') \
                       .merge(reviews_df[['booking_id', 'rating']], on='booking_id', how='left')

# === 7. Summary statistics ===
print("\nSummary statistics:")
print(merged_df.describe())

# === 8. Grouped insights ===
# Revenue by partner
revenue_by_partner = merged_df.groupby(['partner_name', 'partner_type'])['amount_usd'].sum().reset_index()
revenue_by_partner.sort_values(by='amount_usd', ascending=False, inplace=True)

# Average rating by partner
avg_rating = merged_df.groupby('partner_name')['rating'].mean().reset_index().sort_values(by='rating', ascending=False)

# Travel type summary
travel_type_summary = merged_df.groupby('preferred_travel_type').agg({
    'booking_id': 'count',
    'amount_usd': 'sum'
}).rename(columns={'booking_id': 'total_bookings'}).reset_index()

# === 9. Export results ===
output_path = os.path.join(base_path, 'output')
os.makedirs(output_path, exist_ok=True)

merged_df.to_csv(os.path.join(output_path, 'cleaned_merged_travel_data.csv'), index=False)
revenue_by_partner.to_csv(os.path.join(output_path, 'revenue_by_partner.csv'), index=False)
avg_rating.to_csv(os.path.join(output_path, 'avg_rating_by_partner.csv'), index=False)
travel_type_summary.to_csv(os.path.join(output_path, 'travel_type_summary.csv'), index=False)

print("\n✅ Travel data analysis complete. Output saved in '/output' folder.")

median_amt = bookings_df['amount_usd'].median()
bookings_df['amount_usd'].fillna(median_amt, inplace=True)


# Load the cleaned data
import pandas as pd
import os

data_path = os.path.join(os.path.expanduser("~"), "Desktop", "dataprojectfarid", "output", "cleaned_merged_travel_data.csv")
df = pd.read_csv(data_path)

# Convert dates
df['booking_date'] = pd.to_datetime(df['booking_date'])
df['travel_date'] = pd.to_datetime(df['travel_date'])

# KPIs
total_bookings = len(df)
total_revenue = df['amount_usd'].sum()
avg_revenue = df['amount_usd'].mean()
top_countries = df['destination_country'].value_counts().head(5)

print("📌 Total Bookings:", total_bookings)
print("💵 Total Revenue: $", round(total_revenue, 2))
print("💳 Average Revenue per Booking: $", round(avg_revenue, 2))
print("✈️ Top 5 Destination Countries:")
print(top_countries)

print(df.columns.tolist())

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Assuming you've already loaded your DataFrame as df
# For example:
# df = pd.read_csv('your_data.csv')

# Group by 'partner_name' and calculate the average conversion rate
campaign_performance = df.groupby('partner_name')['conversion_rate'].mean().sort_values(ascending=False)

# Plot the campaign performance
plt.figure(figsize=(10, 6))
sns.barplot(x=campaign_performance.values, y=campaign_performance.index)
plt.title('Average Conversion Rate by Partner')
plt.xlabel('Conversion Rate')
plt.ylabel('Partner Name')
plt.tight_layout()
plt.savefig('visuals/campaign_performance.png')
plt.show()




