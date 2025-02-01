import requests
import os
import re
import json

with open('settings.json', 'r') as f:
    data = json.load(f)

ROBLOX_COOKIE = data["cookie"]
PLACE_ID = data["placeId"]
AUDIOS = list(set(data["audioIds"]))
CHUNK_SIZE = 25

def sanitize_filename(filename):
    filename = os.path.basename(filename)
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)
    filename = filename[:200]
    
    return filename

def getAssetName(assetId: int) -> str:
    assetName = ""
    try:
       assetName = requests.get(f"https://economy.roblox.com/v2/developer-products/{assetId}/info").json()["Name"]
    except:
        print(f"Error getting asset name for ID {assetId}")
        raise Exception("Error getting asset name")
    return assetName

def getAudioLocation(audioList: list, placeId: str, cookie: str) -> list:
    audioData = []
    returnData = []
    for id in audioList:
        audioData.append({
            "assetId": id,
			"assetType": "Audio",
			"requestId": "0"
        })
    response = requests.post("https://assetdelivery.roblox.com/v2/assets/batch", headers={
			"User-Agent": "Roblox/WinInet",
			"Content-Type": "application/json",
			"Cookie": f".ROBLOSECURITY={cookie}",
			"Roblox-Place-Id": str(placeId),
			"Accept": "*/*",
			"Roblox-Browser-Asset-Request": "false"
		}, json=audioData)

    if response.status_code == 200:
        locations = response.json()
        for i,v in enumerate(locations):
            returnData.append({
                "assetId": audioData[i]["assetId"], 
                "url": v["locations"][0]["location"],
                "audioName": getAssetName(audioData[i]["assetId"])
            })
    else:
        print("Something went wrong while fetching audio location(s)")
        return
    return returnData

audio_chunks = [AUDIOS[i:i + CHUNK_SIZE] for i in range(0, len(AUDIOS), CHUNK_SIZE)]
def downloadAudioFiles():
    for chunk in audio_chunks:
        for data in getAudioLocation(chunk, PLACE_ID, ROBLOX_COOKIE):
            response = requests.get(data["url"], stream=True)
            response.raise_for_status()
            
            with open(f"Audios/{sanitize_filename(data['audioName'])}.ogg", 'wb') as file:
                for content_chunk in response.iter_content(chunk_size=8192):
                    if content_chunk:
                        file.write(content_chunk)
            print(f"Successfully downloaded {sanitize_filename(data['audioName'])}")
    
downloadAudioFiles()
