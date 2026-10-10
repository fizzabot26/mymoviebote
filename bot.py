import os
import requests
from googleapiclient.discovery import build

# --- CONFIGURATION LOADER ---
settings = {}
if os.path.exists("settings.txt"):
    with open("settings.txt", "r") as f:
        for line in f:
            if "=" in line and not line.startswith("#"):
                key, val = line.split("=", 1)
                settings[key.strip()] = val.split("#")[0].strip().strip('"').strip("'")

YOUTUBE_API_KEY = settings.get("YOUTUBE_API_KEY", "")
BLOG_ID = settings.get("BLOG_ID", "")
HUGGINGFACE_TOKEN = settings.get("HUGGINGFACE_TOKEN", "")
SHORT_DURATION = int(settings.get("SHORT_DURATION_SECONDS", 60))
MAX_SHORTS = int(settings.get("MAX_SHORTS_TO_EXTRACT", 15))

# --- YOUTUBE LONG TO SHORTS PARSER ---
def process_long_video_to_shorts(query):
    youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
    request = youtube.search().list(q=query, part="snippet", maxResults=1, type="video")
    response = request.execute()
    
    videos = []
    for item in response.get("items", []):
        v_id = item['id']['videoId']
        for i in range(1, MAX_SHORTS + 1):
            start_sec = i * SHORT_DURATION
            videos.append({
                "title": f"{item['snippet']['title']} - Part {i}",
                "description": item['snippet']['description'],
                "url": f"https://youtube.com{v_id}&t={start_sec}s",
                "embed_id": v_id,
                "start": start_sec
            })
    return videos

def classify_clip(text):
    API_URL = "https://huggingface.co"
    headers = {"Authorization": f"Bearer {HUGGINGFACE_TOKEN}"}
    payload = {"inputs": text, "parameters": {"candidate_labels": ["Funny", "Fight scene", "Romantic", "Emotional Climax", "Motivation"]}}
    try:
        res = requests.post(API_URL, headers=headers, json=payload).json()
        return res["labels"][0]
    except:
        return "General"

print("🚀 Bot starting on local system...")
print("📂 Loading configurations from settings.txt...")
