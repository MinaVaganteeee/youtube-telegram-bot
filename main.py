import feedparser
import time
import requests

# === CONFIGURAZIONE ===
TELEGRAM_BOT_TOKEN = "8404241523:AAF3szBqR9dgwaHdIFvaJpsRbM06CVlZmOw"
TELEGRAM_CHAT_ID = "5389149332"

YOUTUBE_CHANNELS = {
    "Rondo Da Sosa": "UCGW91-ExDG5HolRaK59L6ng",
    "Drake": "UCByOQJjav0CUDwxCk-jVNRQ",
    "LilCr": "UCBOs_tA4noBqgzif_kmYokQ",
    "Nabi": "UCraW73SNGkgTfSqS3gVlEUQ",
    "Lil Tecca": "UCjWRB340EE-E8gSDmXhB0wA"
}

CHECK_INTERVAL = 60 * 5  # ogni 5 minuti

# === FUNZIONI ===
def get_latest_video(channel_id):
    feed_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
    feed = feedparser.parse(feed_url)
    if feed.entries:
        return {
            "title": feed.entries[0].title,
            "link": feed.entries[0].link,
            "published": feed.entries[0].published
        }
    return None

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    requests.post(url, data=data)

# === LOOP PRINCIPALE ===
last_videos = {}

while True:
    for artist, channel_id in YOUTUBE_CHANNELS.items():
        latest_video = get_latest_video(channel_id)
        if latest_video:
            video_id = latest_video["link"].split("=")[-1]
            if artist not in last_videos or last_videos[artist] != video_id:
                last_videos[artist] = video_id
                message = f"📢 Nuovo video da <b>{artist}</b>:\n🎬 {latest_video['title']}\n🔗 {latest_video['link']}"
                send_telegram_message(message)
    time.sleep(CHECK_INTERVAL)
