# Promptly 🌅

**Send fun, warm "Custom Prompted" messages with beautiful images to your loved ones via WhatsApp—automatically, every day.**

## ✨ Features

- 📸 **Fetch Beautiful Images**: Random high-quality images from Unsplash
- 💬 **Automated Messaging**: Send scheduled messages via WhatsApp
- 📝 **Comprehensive Logging**: Track events and errors
- ⚙️ **Full Customization**: Personalize messages, timing, and images

## 🛠️ Tech Stack

- **Python**: Core application logic
- **Unsplash API**: For fetching beautiful images
- **PyWhatKit**: WhatsApp automation
- **Schedule**: Task scheduling

## 🚀 Getting Started

### Prerequisites
- Python 3.6+
- WhatsApp Web access
- Unsplash API key

### Installation

1. Clone the repository:
```bash
git clone https://github.com/itsmeved24/Promptly.git
cd Promptly
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file:
```
PHONE_NUMBER=+911234567890
UNSPLASH_API_KEY=your_unsplash_api_key_here
```

4. Run the application:
```bash
python main.py
```

## ⚙️ Customization

- **Message Text**: Edit message templates in `main.py`
- **Image Categories**: Modify keywords in `image_fetcher.py`
- **Scheduling**: Adjust timing with `schedule.every().day.at("HH:MM")` in `main.py`
- **Custom Images**: Add personal images to `images/` directory

## 📋 Project Structure

```
.
├── images/               # Directory for storing images
├── .env                  # Environment variables
├── image_fetcher.py      # Image fetching module
├── main.py               # Core application file
├── image_fetcher.log     # Logs for debugging
├── requirements.txt      # Dependencies
└── README.md             # This file
```

## 📊 Logging

The application creates detailed logs (`image_fetcher.log`) that include:
- Timestamps for each operation
- Success/failure status
- Image URLs and query terms
- Detailed error information
- Debug information

## Made with ❤️ by Vedank

## 📜 License

This project is licensed under the MIT License.

