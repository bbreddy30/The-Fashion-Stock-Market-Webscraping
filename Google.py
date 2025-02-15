from pytrends.request import TrendReq
import matplotlib.pyplot as plt

# Initialize Pytrends
pytrends = TrendReq(hl='en-US', tz=360)

# Define fashion brands/celebrities/item to track
fashion = ["Balenciaga","Gucci"]

# Build payload correctly
pytrends.build_payload(fashion, timeframe='today 12-m', geo='US')

# Fetch interest over time
trend_data = pytrends.interest_over_time()
print(trend_data)

# Plot trend data
trend_data.plot(figsize=(10, 5))
plt.title("Fashion Search Trends Over Time")
plt.xlabel("Date")
plt.ylabel("Search Interest")
plt.legend(trend_data.columns)
plt.show()