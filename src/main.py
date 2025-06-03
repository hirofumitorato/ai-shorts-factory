"""
main.py
YouTube Shorts を自動生成・自動投稿するスクリプト
GitHub Actions でも動作し、環境変数から認証情報を取得
"""

import os
import json
import random
import datetime
import tempfile
from pathlib import Path

import openai
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from PIL import Image, ImageDraw, ImageFont
import moviepy.editor as mp
import elevenlabs
from dotenv import load_dotenv

load_dotenv()

# 環境変数から API キー取得
OPENAI_API_KEY   = os.getenv("OPENAI_API_KEY")
ELEVEN_API_KEY   = os.getenv("ELEVENLABS_API_KEY")
YT_OAUTH_B64JSON = os.getenv("YT_OAUTH_JSON")

assert OPENAI_API_KEY and ELEVEN_API_KEY and YT_OAUTH_B64JSON, "環境変数が不足しています"

openai.api_key = OPENAI_API_KEY
elevenlabs.set_api_key(ELEVEN_API_KEY)

# YouTube 認証
def get_yt_service():
    creds_json = json.loads(
        os.popen(f"echo '{YT_OAUTH_B64JSON}' | base64 -d").read()
    )
    creds = Credentials.from_authorized_user_info(creds_json, ["https://www.googleapis.com/auth/youtube.upload"])
    return build("youtube", "v3", credentials=creds, cache_discovery=False)

# 台本生成
def create_script():
    res = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "60 words of motivational advice on focus."}],
        max_tokens=100,
        temperature=0.9
    )
    return res.choices[0].message.content.strip()

# 背景画像生成
def create_background(text, output_path):
    W, H = (1080, 1920)
    img = Image.new("RGB", (W, H), random.choice(["#004488", "#112244", "#334455"]))
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("DejaVuSans.ttf", 64)
    except:
        font = ImageFont.load_default()
    y = 300
    for line in text.split('\n'):
        draw.text((50, y), line, fill="white", font=font)
        y += 80
    img.save(output_path)

# 音声生成
def create_voice(text, output_path):
    audio = elevenlabs.generate(text=text, voice="Bella", model="eleven_multilingual_v2")
    with open(output_path, "wb") as f:
        f.write(audio)

# 動画合成
def compose_video(bg_path, voice_path, output_path):
    clip = mp.ImageClip(str(bg_path)).set_duration(15).set_fps(30)
    clip = clip.set_audio(mp.AudioFileClip(str(voice_path)))
    clip.write_videofile(str(output_path), codec="libx264", audio_codec="aac", fps=30)

# 投稿処理
def upload_to_youtube(video_path, title):
    yt = get_yt_service()
    request = yt.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": title,
                "description": "AIによる自動投稿動画 #AIShorts",
                "tags": ["AI", "Shorts", "Motivation"]
            },
            "status": {
                "privacyStatus": "public"
            }
        },
        media_body=str(video_path)
    )
    request.execute()

# メイン実行
def main():
    script = create_script()
    today = datetime.date.today().isoformat()
    title = f"集中力ブースト {today}"

    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)
        bg = tmpdir / "bg.png"
        wav = tmpdir / "voice.mp3"
        mp4 = tmpdir / "shorts.mp4"

        create_background(script, bg)
        create_voice(script, wav)
        compose_video(bg, wav, mp4)
        upload_to_youtube(mp4, title)

if __name__ == "__main__":
    main()
