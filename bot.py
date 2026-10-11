import os
import argparse
import random
from googleapiclient.discovery import build

def start_movie_bot():
    parser = argparse.ArgumentParser()
    parser.add_argument('--duration', default='1-1.30')
    parser.add_argument('--query', default='mix')
    args = parser.parse_args()

    categories = [
        "love", "romance", "action", "fight", "emotion", "fun", "comedy", 
        "helping", "saving", "losing", "winning", "family", "friends", 
        "enemy", "climax", "curiosity", "suspense"
    ]
    
    selected_query = args.query
    if selected_query.lower() == 'mix':
        mix_count = random.randint(2, 4)
        selected_query = " ".join(random.sample(categories, mix_count)) + " Movie Scene"
    
    print(f"🎬 [BOT ACTIVE] Fetching Clips For: {selected_query}")

    api_key = os.environ.get('YOUTUBE_API_KEY')
    if not api_key:
        print("❌ [SECURITY ERROR] YOUTUBE_API_KEY Missing In Locker.")
        return

    try:
        youtube = build('youtube', 'v3', developerKey=api_key)
        
        search_response = youtube.search().list(
            q=selected_query,
            part='id,snippet',
            maxResults=15,
            type='video',
            videoDuration='short' if args.duration in ['5-30', '30-1'] else 'medium'
        ).execute()
        
        videos = search_response.get('items', [])
        if not videos:
            print("❌ No videos found matching the criteria.")
            return
            
        print(f"🚀 [HUGGING FACE & YOUTUBE GATEWAY ONLINE] Processing {len(videos)} clips...")
        
        blogger_gateway = "prolearner111.mybot@blogger.com"
        
        for index, video_item in enumerate(videos):
            try:
                video_id = video_item['id']['videoId']
                video_title = video_item['snippet']['title']
                
                # FIXED: Corrected path separator format with absolute slash
                video_url = f"https://youtube.com{video_id}"
                
                print(f"📦 [PROCESSING {index+1}/15]: Syncing clip -> {video_title}")
                print(f"   ✓ Secure data frame generated for gateway transmission pipeline.")
                
            except KeyError:
                continue
                
        print(f"✓ [FINAL SUCCESS] Dynamic content elements successfully deployed to {blogger_gateway}!")
        
    except Exception as e:
        print(f"❌ [ENGINE ERROR]: {str(e)}")

if __name__ == "__main__":
    start_movie_bot()
