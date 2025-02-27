# YT Bias & Fact Checker V2

The **YT Bias & Fact Checker V2** is an AI-powered tool designed to assess YouTube videos for factual correctness, bias, and logical consistency. It extracts transcripts, generates search queries, retrieves relevant sources using web scraping, and performs detailed evaluations. The tool consists of a Flask-based backend and a Chrome extension that provides a user-friendly and persistent interface.

## Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Installation](#installation)
  - [Backend Setup](#backend-setup)
  - [Chrome Extension Setup](#chrome-extension-setup)
- [Usage](#usage)
- [File Structure](#file-structure)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)
- [Limitations](#limitations)
- [Future Improvements](#future-improvements)
- [Contributing](#contributing)
- [License](#license)

## Features

- **YouTube Transcript Extraction**  
  Uses `youtube_transcript_api` to extract video transcripts (fallback to other languages if English is unavailable).

- **Search Query Generation**  
  Utilizes the Gemini generative AI to create concise, fact-based search queries from transcripts.

- **Web Scraping for Source Retrieval**  
  Fetches reliable sources by scraping top search results from Google, filtering out low-quality or irrelevant pages.

- **Evaluation Analysis**  
  Combines transcript data and scraped search results to generate a detailed evaluation: factual points, source verification, bias detection, and logical consistency.

- **Sentiment Analysis**  
  Detects video sentiment (positive, neutral, or negative).

## Architecture

The project consists of:

1. **Backend (Flask API)**

   - `app.py`: Handles API requests, extracts transcripts, generates queries, integrates web scraping, and compiles evaluations.
   - Environment variables stored in `.env`.

2. **Chrome Extension**

   - `manifest.json`: Defines metadata and permissions.
   - `background.js`: Opens persistent extension window.
   - `popup.html`, `style.css`, `popup.js`: UI for triggering evaluations and displaying reports.

## Installation

### Backend Setup

1. **Clone Repository**
   ```bash
   git clone https://github.com/Dev07-Harsh/YT-Bias-Fact-Checker-v2.git
   cd yt-bias-fact-checker-v2
   ```
2. **Create & Activate Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```
3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```
4. **Configure Environment Variables**
   ```ini
   GEMINI_API_KEY=your_gemini_api_key
   ```
5. **Run Backend Server**
   ```bash
   python app.py
   ```
   Runs on `http://127.0.0.1:3000`.

### Chrome Extension Setup

1. Ensure extension files (`manifest.json`, `background.js`, `popup.html`, etc.) are in a dedicated folder.
2. Open Chrome → `chrome://extensions`.
3. Enable **Developer Mode**.
4. Click **Load unpacked** and select the folder.

## Usage

1. Navigate to a YouTube video.
2. Click the extension icon.
3. The extension extracts the transcript, generates queries, fetches sources, and evaluates.
4. View the final report in the extension UI.

## File Structure

```
yt-bias-fact-checker-v2/
├── app.py                 # Backend API
├── .env                   # Secrets
├── requirements.txt       # Dependencies
└── extension/             # Chrome Extension
    ├── manifest.json
    ├── background.js
    ├── popup.html
    ├── popup.css
    └── popup.js
```

## Limitations

- **Search Query Issues:** Sometimes, search queries fail to find relevant sources, affecting evaluation accuracy.
- **Web Scraping Limitations:** Web scraping may sometimes fail due to site restrictions and does not currently support JavaScript-rendered pages.
- **Latest News Verification Issues:** Struggles with real-time fact-checking; performs better on historical and general knowledge topics.
- **Dependency on Web Scraping:** If Google search result pages block access, evaluations may be less precise.
- **Model Bias Influence:** The evaluation may sometimes reflect biases inherent in the AI model used for analysis.

## Future Improvements

- **LLM Web Search Integration:** If LLM APIs provide native web search, evaluations will become more precise.
- **Query Optimization:** Refining search queries for better accuracy.
- **Improved Web Scraping:** Enhancing scraping techniques to support JavaScript-rendered pages.
- **User Feedback Mechanism:** Allow users to rate evaluations for accuracy.

## Contributing

Contributions are welcome! Fork the repository, create a feature branch, and submit a pull request. For major changes, open an issue first to discuss improvements.

## License

Licensed under **MIT**. See `LICENSE` file.

---

