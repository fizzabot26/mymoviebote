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

# --- YOUTUBE CLIPS PARSER ---
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
                "url": f"https://www.youtube.com/watch?v={v_id}&t={start_sec}s",
                "embed_id": v_id,
                "start": start_sec
            })
    return videos

# --- AI SE CATEGORY CHECK KARNA ---
def classify_clip(text):
    API_URL = "https://huggingface.co"
    headers = {"Authorization": f"Bearer {HUGGINGFACE_TOKEN}"}
    payload = {"inputs": text, "parameters": {"candidate_labels": ["Funny", "Fight scene", "Romantic", "Emotional Climax", "Motivation"]}}
    try:
        res = requests.post(API_URL, headers=headers, json=payload).json()
        return res["labels"][0]
    except:
        return "General"

# --- 🚀 BLOGGER PAR ASLI POSTING KA FUNCTION ---
def post_to_blogger_live(video, category):
    embed_code = f'''
    <p>{video['description']}</p>
    <div style="position:relative; padding-bottom:56.25%; height:0; overflow:hidden;">
        <iframe src="https://youtube.com{video['embed_id']}?start={video['start']}" 
                style="position:absolute; top:0; left:0; width:100%; height:100%;" 
                frameborder="0" allowfullscreen></iframe>
    </div>
    <br><p>Category: <b>{category}</b></p>
    '''
    
    url = f"https://googleapis.com{BLOG_ID}/posts/"
    post_url = f"{url}?key={YOUTUBE_API_KEY}"
    
    payload = {
        "kind": "blogger#post",
        "title": f"[{category}] {video['title']}",
        "content": embed_code,
        "labels": [category]
    }
    
    res = requests.post(post_url, json=payload)
    if res.status_code == 200:
        print(f"✅ Successfully posted: {video['title']}")
    else:
        print(f"❌ Post failed on Blogger API. Testing local embed link instead: {video['url']}")

# --- MAIN RUNNER ---
print("🚀 Bot starting live cloud generation...")
search_queries = ["avengers infinity war clips"]
for query in search_queries:
    clips = process_long_video_to_shorts(query)
    for clip in clips[:3]: # Initial live batch check
        cat = classify_clip(clip["title"] + " " + clip["description"])
        post_to_blogger_live(clip, cat)
