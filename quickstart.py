# quickstart.py
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import json, base64

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

flow = InstalledAppFlow.from_client_secrets_file(
    "client_secret.json", SCOPES)
creds = flow.run_local_server(port=0)

# 認可後、credentials.json を保存
with open("credentials.json", "w") as f:
    f.write(creds.to_json())

# GitHub Secret 用に base64 へ変換
b64 = base64.b64encode(creds.to_json().encode()).decode()
print("\n=== GitHub 用 base64 ===\n")
print(b64)
