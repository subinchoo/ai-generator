import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests
import time

# ─── STEP A: Read Google Sheet ──────────────────────────────────────────────
# 1. authenticate
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
gc = gspread.authorize(creds)

SPREADSHEET_ID = "1nFY1YRJfRKL1PaoT0X-6ix9-iGg-TOsQYoIGOY2kAAE"
sheet = gc.open_by_key(SPREADSHEET_ID).sheet1
row = sheet.get_all_records()[0]

# 3. generate your script text from the row
script_text = f"""
Hi there! Welcome to your {row['program_name']} session.

This program runs for {row['duration']} with {row['days_per_week']} days on-site per week,
and you need at least {row['min_hours_per_week']} hours each week.

Our coordinators:
• NSW: {row['NSW coordinator']}
• VIC: {row['VIC coordinator']}
• QLD: {row['QLD coordinator']}

Self-employment requirements:
1. {row['OE_requirement1']}
2. {row['OE_requirement2']}
3. {row['OE_requirement3'].strip()}
4. {row['OE_requirement4'].strip()}
5. {row['OE_requirement5'].strip()}
6. {row['OE_requirement6'].strip()}

Thanks for watching—good luck on your PY journey!
""".strip()

# ─── STEP B: Your existing HeyGen logic ──────────────────────────────────────
API_KEY   = "MmE2ZGRhYWRhZTllNDI0YTlhODM4Mzk2ZDNjNDIzMDctMTc0NzAxMDM2Ng=="
AVATAR_ID = "Abigail_standing_office_front"
VOICE_ID  = "c8e176c17f814004885fd590e03ff99f"

headers = {
    "X-Api-Key": API_KEY,
    "Content-Type": "application/json"
}

data = {
    "video_inputs": [
        {
            "character": {
                "type": "avatar",
                "avatar_id": AVATAR_ID,
                "avatar_style": "normal"
            },
            "voice": {
                "type": "text",
                "input_text": script_text,     # ← use dynamic text here
                "voice_id": VOICE_ID
            },
            "background": {
                "type": "color",
                "value": "#FFFFFF"
            }
        }
    ],
    "dimension": {
        "width": 1280,
        "height": 720
    }
}

print("🎬 Sending video generation request…")
response = requests.post("https://api.heygen.com/v2/video/generate", headers=headers, json=data)

if response.status_code == 200:
    video_id = response.json().get("data", {}).get("video_id")
    print("✅ Video ID:", video_id)
else:
    print("❌ Failed to generate video:", response.text)
    exit()

def poll_status(video_id):
    while True:
        print("🔄 Checking video status…")
        status_url = f"https://api.heygen.com/v1/video_status.get?video_id={video_id}"
        status_response = requests.get(status_url, headers=headers)

        if status_response.status_code == 200:
            d = status_response.json().get("data", {})
            if d.get("status") == "completed":
                print("🎉 Video is ready!")
                print("🔗 URL:", d.get("video_url"))
                break
            elif d.get("status") == "failed":
                print("❌ Video failed to generate.")
                break
            else:
                print(f"⏳ Status: {d.get('status')}. Waiting 30s…")
        else:
            print("❌ Error checking status:", status_response.text)
            break
        time.sleep(30)

poll_status(video_id)
