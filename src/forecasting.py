import pandas as pd
import matplotlib.pyplot as plt
from prophet import Prophet

# ✅ Load the dataset from the correct 'output' folder
df = pd.read_csv("/Users/faridabdurrahman/Desktop/DATAPROJECTFARID/output/cleaned_merged_travel_data.csv")

# ✅ Convert booking_date to datetime
df['booking_date'] = pd.to_datetime(df['booking_date'])

# ✅ Group by month and count bookings
monthly_bookings = df.resample('M', on='booking_date').size().reset_index(name='bookings')

# ✅ Format for Prophet
prophet_df = monthly_bookings.rename(columns={'booking_date': 'ds', 'bookings': 'y'})

# ✅ Train Prophet model
model = Prophet()
model.fit(prophet_df)

# ✅ Create future dataframe and forecast
future = model.make_future_dataframe(periods=6, freq='M')
forecast = model.predict(future)

# ✅ Plot forecast
fig = model.plot(forecast)
plt.title("Forecast of Monthly Bookings with Prophet")
plt.xlabel("Date")
plt.ylabel("Bookings")
plt.tight_layout()
plt.show()

# ✅ Save forecast output (optional)
forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].to_csv("/Users/faridabdurrahman/Desktop/DATAPROJECTFARID/output/monthly_booking_forecast.csv", index=False)
