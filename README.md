# Roblox Audio Downloader

A simple, fast, and efficient **Python** tool to bulk download Roblox audio assets (`.ogg` files) using Roblox's official Asset Delivery API.

## Features

- Bulk download any number of Roblox audios by their Asset IDs
- Automatically fetches the original audio names from Roblox
- Sanitizes filenames (removes invalid characters)
- Processes audio IDs in batches of 25 to respect rate limits
- Saves all files as `.ogg` in the `audios/` folder
- Easy configuration via `settings.json`
- Uses your personal `.ROBLOSECURITY` cookie for authentication

## Requirements

- Python 3.6 or higher
- `requests` library

## Installation

```bash
git clone https://github.com/NathanDaigle/audiodownloader.git
cd audiodownloader
```

# Install dependencies
```bash
pip install requests
```


## Setup

Open (or create) the `settings.json` file and fill it with your information:

```json
{  
  "cookie": ".ROBLOSECURITY=your_full_roblox_cookie_here",  
  "placeId": 4111023553,  
  "audioIds": [    
    7680356645
  ]
}
