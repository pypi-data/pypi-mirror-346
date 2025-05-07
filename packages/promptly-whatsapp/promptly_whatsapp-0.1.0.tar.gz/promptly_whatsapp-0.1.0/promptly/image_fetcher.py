import os
import requests
import logging
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API Key from environment variable
API_KEY = os.getenv("UNSPLASH_API_KEY")

# Setup logging
logging.basicConfig(
    filename="image_fetcher.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

def log_and_print(message, level="info"):
    print(message)
    getattr(logging, level)(message)

# Fetch Image
def fetch_good_morning_image():
    if not API_KEY:
        log_and_print("Error: Unsplash API key is missing. Check your .env file.", "error")
        return None

    URL = "https://api.unsplash.com/photos/random"
    HEADERS = {"Authorization": f"Client-ID {API_KEY}"}
    PARAMS = {"query": "F1 Cars", "orientation": "landscape"}

    try:
        response = requests.get(URL, headers=HEADERS, params=PARAMS, timeout=10)
        response.raise_for_status()  # Handle HTTP errors

        data = response.json()
        if "urls" in data and "regular" in data["urls"]:
            image_url = data["urls"]["regular"]
            log_and_print(f"Fetched Image URL: {image_url}")
            return image_url
        else:
            log_and_print("Invalid API response format.", "error")
            return None

    except requests.exceptions.Timeout:
        log_and_print("Error: Request timed out.", "error")
    except requests.exceptions.ConnectionError:
        log_and_print("Error: Network connection issue.", "error")
    except requests.exceptions.HTTPError as e:
        log_and_print(f"HTTP Error: {e}", "error")
    except requests.exceptions.RequestException as e:
        log_and_print(f"Request Error: {e}", "error")
    except Exception as e:
        log_and_print(f"Unexpected error: {e}", "error")

    return None
