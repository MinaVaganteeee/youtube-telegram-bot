import time
import feedparser
import requests

channels = {
    "Artie 5ive":       "UC-xCxVgJcaeTk__KaFpPwwQ",
    "Future":           "UCSDvKdIQOwTfcyOimSi9oYA",
    "Metro Boomin":     "UCKC11MOR51CLg4JpYj8jb4g",
    "Lil Baby":         "UCVS88tG_NYgxF6Udnx2815Q",
    "NBA YoungBoy":     "UClW4jraMKz6Qj69lJf-tODA",
    "Don Toliver":      "UCgT01FILdWB9BsXBXKjpQ7A",
    "Travis Scott":     "UCtxdfwb9wfkoGocVUAJ-Bmg",
    "Rondo Da Sosa":    "UCGW91-ExDG5HolRaK59L6ng",
    "Drake":            "UCByOQJjav0CUDwxCk-jVNRQ",
    "LilCr":            "UCBOs_tA4noBqgzif_kmYokQ",
    "Nabi":             "UCraW73SNGkgTfSqS3gVlEUQ",
    "Lil Tecca":        "UCjWRB340EE-E8gSDmXhB0wA"
}

TELEGRAM_TOKEN = "8404241523:AAF3szBqR9dgwaHdIFvaJpsRbM06CVlZmOw"
CHAT_ID = "5389149332"

latest_video_ids = {}

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, data=data)

def check_new_videos():
    for artist, channel_id in channels.items():
        feed_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
        feed = feedparser.parse(feed_url)
        if not feed.entries:
            continue

        latest_video = feed.entries[0]
        video_id = latest_video.yt_videoid
        video_title = latest_video.title
        video_url = latest_video.link

        if channel_id not in latest_video_ids or latest_video_ids[channel_id] != video_id:
            latest_video_ids[channel_id] = video_id
            send_telegram_message(f"📢 Nuovo video da {artist}:
🎬 {video_title}
🔗 {video_url}")

if __name__ == "__main__":
    send_telegram_message("🤖 Bot avviato! Inizio monitoraggio canali YouTube...")
    while True:
        try:
            check_new_videos()
        except Exception as e:
            send_telegram_message(f"❌ Errore nel bot: {str(e)}")
        time.sleep(600)