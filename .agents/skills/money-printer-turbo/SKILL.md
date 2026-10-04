---
name: money-printer-turbo
description: Guides on how to use and install MoneyPrinterTurbo, an AI-powered short-form video generator. Use when the user asks to generate videos from text, set up MoneyPrinterTurbo, or configure its AI pipelines.
---

# MoneyPrinterTurbo Skill

This skill guides the AI assistant on how to install, configure, and run **MoneyPrinterTurbo**, an open-source tool designed to generate short-form videos (like YouTube Shorts or TikTok) automatically from a topic or keyword.

## Key Pipelines

1. **Script Generation**: Generates video scripts based on user-provided topics using LLMs (OpenAI, Gemini, DeepSeek, etc.).
2. **Footage Gathering**: Fetches stock video clips from Pexels/Pixabay that match script keywords.
3. **Voice Narration**: Converts script text to speech using Edge-TTS or Azure Speech.
4. **Media Assembly**: Merges video clips, voiceover, and generated subtitles using FFmpeg and MoviePy.

## Installation & Setup

### Option 1: Via Docker (Recommended)
```bash
docker compose up -d
```

### Option 2: Local Installation (via uv / pip)
1. **Clone the repository**:
   ```bash
   git clone https://github.com/harry0703/MoneyPrinterTurbo.git
   cd MoneyPrinterTurbo
   ```
2. **Install dependencies using uv**:
   ```bash
   uv venv
   # Activate environment, then:
   uv pip install -r requirements.txt
   ```
3. **Start the Web UI (Streamlit)**:
   ```bash
   uv run streamlit run webui.py
   ```

## Configuration (env / config.yaml)

To use the tool, configure the following keys in your environment or `.env` file:
- `PEXELS_API_KEY`: For fetching stock videos.
- `OPENAI_API_KEY` (or DeepSeek, Gemini): For video script generation.
- `SUBTITLE_PROVIDER`: Provider for subtitle generation (e.g. whisper).
