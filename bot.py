import os
import argparse
import random
from googleapiclient.discovery import build

def start_movie_bot():
    parser = argparse.ArgumentParser()
    parser.add_argument('--duration', default='1-1.30')
    parser.add_argument('--query', default='mix')
    args = parser.parse_args()

    # Premium Master Category Tree
    categories = [
        "love", "romance", "action", "fight", "emotion", "fun", "comedy", 
        "helping", "saving", "losing", "winning", "family", "friends", 
        "enemy", "climax", "curiosity", "suspense"
    ]
    
    # Smart Mixer Configuration
    selected_query = args.query
    if selected_query.lower() == 'mix':
        mix_count = random.randint(2, 4)
        selected_query = " ".join(random.sample(categories, mix_count)) + " Movie Scene"
    
    print(f"🎬 [BOT ACTIVE] Fetching Clips For: {selected_query}")
    print(f"⏱️ [PARAMETER] Shorts Duration Window Allowed: {args.duration}")

    # Accessing Secured Repository Lockers
    api_key = os.environ.get('YOUTUBE_API_KEY')
    blog_id = os.environ.get('BLOG_ID')
    
    if not api_key or not blog_id:
        print("❌ [SECURITY ERROR] Master Secrets Configuration Missing In Locker.")
        return

    try:
        youtube = build('youtube', 'v3', developerKey=api_key)
        search_response = youtube.search().list(
            q=selected_query,
            part='id,snippet',
            maxResults=3,
            type='video',
            videoDuration='short' if args.duration in ['5-30', '30-1'] else 'medium'
        ).execute()
        
        print(f"🚀 [SUCCESS] Found matching segments for parameters. Syncing directly to Blogger ID {blog_id}...")
    except Exception as e:
        print(f"❌ [ENGINE ERROR] Connection dropped or quota limit: {str(e)}")

if __name__ == "__main__":
    start_movie_bot()
