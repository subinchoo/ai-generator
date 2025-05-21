# AI Video Generator (Google Sheets → HeyGen)

A Python-based automation that reads structured PY Internship data from a Google Sheet, generates an AI-avatar video via the HeyGen API, downloads the clip, and overlays a slide image as picture-in-picture—producing a ready-to-share MP4.

---

## 🚀 Features

- **Dynamic script**: Reads “program_name”, coordinators, duration, requirements, etc. from a Google Sheet.
- **AI avatar**: Uses HeyGen API to generate a talking-head clip reading your script.
- **Auto-poll & download**: Waits for the video to finish rendering, then downloads it.
- **Picture-in-picture**: Overlays a slide (PNG/JPG) in the corner of your avatar video.
- **Single-click run**: Trainers just update the sheet, drop in `slide.png`, and run the script to get a polished MP4.

---

## 📝 Prerequisites

1. **Python 3.8+**  
2. A **Google Cloud** project with:
   - **Google Sheets API** & **Drive API** enabled  
   - A **service account** JSON key (`credentials.json`)  
3. A **HeyGen** account on a paid plan (API access)  
   - Your **HeyGen API key**  
   - A chosen **avatar_id** & **voice_id**  
4. A **Google Sheet** shared with your service account (Editor role).  

---

## 📦 Installation

1. Clone this repo:  
   ```bash
   git clone https://github.com/yourusername/ai-video-generator.git
   cd ai-video-generator

2. Install dependencies:
   ```bash
   pip install \
   gspread oauth2client \
   requests \
   moviepy pillow imageio[ffmpeg]

3. place your files in the project root:
   credentials.json
   slide.png(or jpg) your overlay image

4. update configuration in the script (or in env)
   ```bash
   SPREADSHEET_ID = "your_google_sheet_id"
  API_KEY        = "your_heygen_api_key"
  AVATAR_ID      = "your_avatar_id"
  VOICE_ID       = "your_voice_id"
  SLIDE_IMAGE    = "slide.png"

## run the main script
   ```bash
   python heygen_ai_generator.py
```

It will : 

Read the first row of your Sheet and build a spoken script.

Call HeyGen to generate the AI video.

Poll the HeyGen API until the clip is ready.

Download it as dynamic.mp4.

Overlay your slide.png in the top-right corner.

Export the final video as dynamic_with_slide.mp4.
