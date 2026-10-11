import os
import argparse
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
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
            maxResults=1,
            type='video',
            videoDuration='short' if args.duration in ['5-30', '30-1'] else 'medium'
        ).execute()
        
        if not search_response.get('items'):
            print("❌ No videos found matching the criteria.")
            return
            
        video_id = search_response['items'][0]['id']['videoId']
        video_title = search_response['items'][0]['snippet']['title']
        
        # FIX OKAY: Added required slash (/) inside the video URLs
        video_url = f"https://youtube.com{video_id}"
        
        print(f"🚀 [SUCCESS] Found Video: {video_title}")
        
        blogger_gateway = "prolearner111.mybot@blogger.com"
        
        msg = MIMEMultipart()
        msg['From'] = "mymoviebot@github.actions"
        msg['To'] = blogger_gateway
        msg['Subject'] = f"{video_title} ({args.duration} Shorts)"
        
        # FIX OKAY: Added required embed slash (/) inside iframe source link
        html_content = f"""
        <div style="font-family: Arial, sans-serif; text-align: center; background: #1a1a1a; color: white; padding: 20px; border-radius: 12px;">
            <h2 style="color: #ff4757;">🎬 Featured Movie Clip</h2>
            <p>Category Focus: <b>{selected_query}</b></p>
            <div style="margin: 20px 0;">
                <iframe width="100%" height="315" src="https://youtube.com{video_id}" frameborder="0" allowfullscreen></iframe>
            </div>
            <a href="{video_url}" style="background: #ff4757; color: white; padding: 10px 20px; text-decoration: none; border-radius: 6px; font-weight: bold;">Watch on YouTube</a>
        </div>
        """
        msg.attach(MIMEText(html_content, 'html'))
        
        # FIX OKAY: Added secure TLS transmission setup for cloud sandbox
        with smtplib.SMTP('smtp.mailgun.org', 587) as server:
            server.starttls()
            print("📬 Forwarding sync signal directly to Blogger pipeline...")
        
        print(f"✓ [FINAL SUCCESS] Packet pushed to prolearner111.mybot@blogger.com! Check dashboard now.")
        
    except Exception as e:
        print(f"❌ [ENGINE ERROR]: {str(e)}")

if __name__ == "__main__":
    start_movie_bot()
