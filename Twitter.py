import tweepy
import os

# Replace with your own Bearer Token from Twitter Developer Portal
BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAOasygEAAAAAcUG3%2FU4uLYdi8AsvunWPfrvrbQ0%3DSl2KODNzqr3Lp1BpKYDZQ5gkkjsrjVgjeMstYaqFMDF9GAnoCt"

# Set up Tweepy client
client = tweepy.Client(bearer_token=BEARER_TOKEN)

# Function to fetch tweets based on a specific search term and save them to a specified location
def fetch_tweets_from_search(search_query, max_results=10, save_path="output/tweets.txt"):
    query = f"{search_query} lang:en -is:retweet"  # Search for the term, filter out retweets, and only English tweets
    tweets = client.search_recent_tweets(query=query, max_results=max_results)

    # Ensure the directory exists before saving the file
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    # Open a text file to save the tweets
    with open(save_path, "w", encoding="utf-8") as file:
        if tweets.data:
            for tweet in tweets.data:
                file.write(f"Tweet: {tweet.text}\n\n")
            print(f"Saved {len(tweets.data)} tweets to {save_path}")
        else:
            print(f"No tweets found for the search query '{search_query}' in English.")

# Specify the path where you want the file saved (absolute or relative path)
save_path = "/Users/bhavyareddy/Documents/fashion/webscraper/fashion_tweets.txt"  # Modify this path
search_query = ""  # Replace with your search term

# Call the function with the specific path
fetch_tweets_from_search(search_query, max_results=10, save_path=save_path)