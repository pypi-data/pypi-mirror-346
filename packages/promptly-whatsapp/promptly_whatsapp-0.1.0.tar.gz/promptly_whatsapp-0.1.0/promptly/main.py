import schedule
import time
from image_fetcher import fetch_good_morning_image
import pywhatkit
import requests
import os
import logging
from datetime import datetime
from dotenv import load_dotenv

load_dotenv() 

# Configure logging
logging.basicConfig(
    filename="script.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

def log_and_print(message, level="info"):
    print(message)
    getattr(logging, level)(message)

# Checks If the images folder exists, if not create it
def ensure_images_folder():
    folder_path = "images"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        log_and_print(f"Created folder: {folder_path}")
    return folder_path

# Downloads the images locally on the device
def download_image(url):
    try:
        folder_path = ensure_images_folder()
        filename = f"good_morning_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
        save_path = os.path.join(folder_path, filename)

        response = requests.get(url, stream=True, timeout=10)
        response.raise_for_status()  # Error handling for bad responses

        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)

        log_and_print(f"Image successfully downloaded to {save_path}")
        return save_path

    except requests.exceptions.Timeout:
        log_and_print("Error: Request timed out.", "error")
    except requests.exceptions.ConnectionError:
        log_and_print("Error: Network connection issue.", "error")
    except requests.exceptions.RequestException as e:
        log_and_print(f"Request Error: {e}", "error")
    except Exception as e:
        log_and_print(f"Unexpected error: {e}", "error")

    return None

# Custom Prompt while fetching the image
def send_good_morning():
    log_and_print("Fetching good morning image...")

    image_url = fetch_good_morning_image()
    if image_url:
        local_image_path = download_image(image_url)
        if local_image_path:
            group_id = os.getenv('WHATSAPP_GROUP_ID')
            try:
                time.sleep(5)
                pywhatkit.sendwhats_image(
                    group_id, 
                    local_image_path, 
                    "Good Morning Bhai Log!", 
                    15,
                    True
                )
                time.sleep(5)
                log_and_print("Good morning image sent successfully!")
            except Exception as e:
                log_and_print(f"Error sending WhatsApp message: {e}", "error")
                try:
                    time.sleep(10)
                    pywhatkit.sendwhats_image(
                        group_id, 
                        local_image_path, 
                        "Good Morning Bhai Log!", 
                        20,
                        True
                    )
                    log_and_print("Good morning image sent successfully on retry!")
                    # Use a more robust method to find VS Code executable       
                    vscode_paths = [
                        os.environ.get('VSCODE_PATH'),  # Check environment variable first
                        r"C:\Program Files\Microsoft VS Code\Code.exe",  # Windows default
                        r"C:\Users\%USERNAME%\AppData\Local\Programs\Microsoft VS Code\Code.exe",  # User install
                        "/usr/bin/code",  # Linux
                        "/Applications/Visual Studio Code.app/Contents/Resources/app/bin/code"  # macOS
                    ]
                    
                    vscode_exe = None
                    for path in vscode_paths:
                        if path and os.path.exists(os.path.expandvars(path)):
                            vscode_exe = os.path.expandvars(path)
                            break
                    
                    if vscode_exe:
                        script_path = os.path.abspath(__file__)
                        os.system(f'"{vscode_exe}" "{script_path}"')
                except Exception as retry_e:
                    log_and_print(f"Retry also failed: {retry_e}", "error")
        else:
            log_and_print("Failed to download the image.", "error")
    else:
        log_and_print("Failed to fetch the image URL. Check API/network.", "error")

# Schedule the message according to the daily routines
schedule.every().day.at("03:33").do(send_good_morning)  # Modfiy the timings (24-hour format)

log_and_print("Scheduler started...")

while True:
    schedule.run_pending()
    time.sleep(1)
