import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set Seaborn style
sns.set(style="whitegrid")

# Define the path to your data directory
data_dir = 'data'

# Load datasets
try:
    bookings = pd.read_csv(os.path.join(data_dir, 'bookings.csv'))
    users = pd.read_csv(os.path.join(data_dir, 'users.csv'))
    partners = pd.read_csv(os.path.join(data_dir, 'partners.csv'))
    campaigns = pd.read_csv(os.path.join(data_dir, 'campaigns.csv'))
except FileNotFoundError as e:
    print(f"Error: {e}")
    exit(1)

# Merge datasets
df = bookings.merge(users, on='user_id', how='left') \
             .merge(partners, on='partner_id', how='left') \
             .merge(campaigns, on='campaign_id', how='left')

# Clean column names
df.columns = df.columns.str.strip()

# Calculate conversion rate if not present
if 'conversion_rate' not in df.columns:
    if 'conversions' in df.columns and 'total_interactions' in df.columns:
        df['conversion_rate'] = df['conversions'] / df['total_interactions']
    else:
        print("Required columns for calculating conversion_rate are missing.")
        exit(1)

# Drop rows with missing values in key columns
df.dropna(subset=['partner_name', 'conversion_rate'], inplace=True)

# Group by partner_name to calculate average conversion rate
campaign_performance = df.groupby('partner_name')['conversion_rate'].mean().sort_values(ascending=False)

# Create visuals directory if it doesn't exist
visuals_dir = 'visuals'
os.makedirs(visuals_dir, exist_ok=True)

# Plot campaign performance
plt.figure(figsize=(12, 8))
sns.barplot(x=campaign_performance.values, y=campaign_performance.index, palette='viridis')
plt.title('Average Conversion Rate by Partner')
plt.xlabel('Conversion Rate')
plt.ylabel('Partner Name')
plt.tight_layout()
plt.savefig(os.path.join(visuals_dir, 'campaign_performance.png'))
plt.show()

# Additional Insights
# Example: Customer segmentation based on age groups
if 'age' in df.columns:
    age_bins = [18, 25, 35, 45, 55, 65, 100]
    age_labels = ['18-24', '25-34', '35-44', '45-54', '55-64', '65+']
    df['age_group'] = pd.cut(df['age'], bins=age_bins, labels=age_labels, right=False)

    age_group_performance = df.groupby('age_group')['conversion_rate'].mean().sort_values(ascending=False)

    # Plot age group performance
    plt.figure(figsize=(10, 6))
    sns.barplot(x=age_group_performance.index, y=age_group_performance.values, palette='coolwarm')
    plt.title('Average Conversion Rate by Age Group')
    plt.xlabel('Age Group')
    plt.ylabel('Conversion Rate')
    plt.tight_layout()
    plt.savefig(os.path.join(visuals_dir, 'age_group_performance.png'))
    plt.show()
else:
    print("Age column not found in the dataset.")

# Save insights to a CSV file
insights = campaign_performance.reset_index()
insights.columns = ['Partner Name', 'Average Conversion Rate']
insights.to_csv(os.path.join(visuals_dir, 'campaign_insights.csv'), index=False)

print("Analysis complete. Visuals and insights have been saved to the 'visuals' directory.")


print(df.columns.tolist())

