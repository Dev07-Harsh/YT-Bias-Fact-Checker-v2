from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests
from bs4 import BeautifulSoup
from googlesearch import search
from youtube_transcript_api import YouTubeTranscriptApi
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

app = Flask(__name__)
CORS(app)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


genai.configure(api_key=GEMINI_API_KEY)

generation_config_eval = {
    "temperature": 0.7,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 1000,  
}

generation_config_query = {
    "temperature": 0.3,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 100, 
}

def get_transcript_any_language(video_id):
    """
    Attempts to fetch an English transcript first.
    If not available, iterates over the list of available transcripts
    and returns the first transcript that can be fetched.
    """
    try:
        return YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
    except Exception as e:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        for transcript in transcript_list:
            try:
                return transcript.fetch()
            except Exception as e:
                pass
        raise Exception("Could not retrieve any transcript for video: " + video_id)

def generate_text(prompt, generation_config):
    """
    Uses the google.generativeai library to generate text using the Gemini model.
    """
    model = genai.GenerativeModel(
        model_name="gemini-2.0-flash-exp",
        generation_config=generation_config,
    )
    chat_session = model.start_chat(history=[])
    response = chat_session.send_message(prompt)
    return response.text.strip()

def perform_web_scraping(query, limit_results=5, word_limit=300):
    """
    Scrapes content from top search results based on a query.
    Filters out generic Google search pages and limits output to a specified number of results.
    Each result is truncated to a fixed word limit and formatted with a clickable URL and an excerpt.
    """
    urls = []
   
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"}
    
   
    for url in search(query, num_results=10):
        if not url.startswith("http"):
            url = "https://www.google.com" + url
       
        if "google." in url:
            continue
        urls.append(url)
    
    scraped_content = []
    for url in urls[:limit_results]:
        try:
            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.text, "html.parser")
            content = soup.get_text(separator=' ', strip=True)
            words = content.split()
            if len(words) > word_limit:
                excerpt = " ".join(words[:word_limit]) + "..."
            else:
                excerpt = content
            formatted = f"- **Source:** [{url}]({url})\n  **Excerpt:** {excerpt}\n"
            scraped_content.append(formatted)
        except Exception as e:
            print(f"Error scraping {url}: {e}")
    
    return scraped_content

@app.route("/evaluate", methods=["POST"])
def evaluate():
    data = request.get_json()
    video_id = data.get("videoId")
    if not video_id:
        return jsonify({"error": "videoId is required"}), 400

    try:
        transcript_entries = get_transcript_any_language(video_id)
        transcript = " ".join([entry["text"] for entry in transcript_entries])
       
       
        prompt_for_query = f"""
You are a search query expert specializing in crafting concise and effective search queries from lengthy transcripts. Analyze the transcript provided below and extract a brief, fact-based search query that captures all relevant factual points from the video. Please ensure that the query:
- Clearly identifies the primary subject and key themes discussed in the transcript.
- Includes essential factual details, such as names, dates, events, and significant terms.
- Excludes any promotional content, advertisements, or irrelevant information.
- Is structured to maximize retrieval of high-quality and reliable factual information from reputable sources.
- Uses specific keywords or phrases that reflect the core message of the video.
- Is limited to no more than 20-30 words for optimal search performance.
- Focus on named entities, dates, statistics

- Prioritize verifiable factual claims
   
- Maximum 25 words

Transcript:
{transcript}
"""
        search_query = generate_text(prompt_for_query, generation_config_query)
        print("Generated Search Query:", search_query)

        
        reliable_sources = perform_web_scraping(search_query)
        
        
        reliable_sources_str = "\n".join(reliable_sources)

       
        prompt_evaluation = f"""
You are an expert fact-checker and media analyst with extensive experience in evaluating online video content for accuracy, bias, and logical consistency. Given the following transcript from a YouTube video and a list of reliable sources with factual data, please perform a comprehensive analysis using the steps below. Note: Ignore any promotions, advertisements, or monetization content as these are not relevant to factual accuracy or bias.

1. **Key Factual Points:**  
   - Identify and list the main factual assertions and claims made in the transcript.
   
2. **Source Verification:**  
   - For each factual point, compare it with the information provided by the reliable sources.
   - Highlight any discrepancies, confirmations, or additional context provided by the sources.
   
3. **Bias and Representation Analysis:**  
   - Examine the transcript for any signs of bias, including selective presentation of facts, omission of alternative viewpoints, or use of emotionally charged language.
   - Note if certain perspectives are overemphasized or ignored.
   
4. **Logical Consistency and Reasoning:**  
   - Assess the logical flow of the arguments in the transcript.
   - Identify any logical fallacies, inconsistencies, or gaps in the reasoning.
   
5. **Additional Observations:**  
   - Note any misleading statements or rhetorical strategies that could influence the audience's perception.
   
6. **Overall Assessment:**  
   - Provide a concise summary judgment on the overall credibility, balance, and reliability of the video's content.

Please produce your evaluation in a clear, structured bullet-point format, and ensure that in any case the final output does not exceed 500 words.

Transcript:
{transcript}

Reliable Sources:
{reliable_sources_str}
"""
        evaluation = generate_text(prompt_evaluation, generation_config_eval)
        return jsonify({"evaluation": evaluation})
    
    except Exception as e:
        print(f"Evaluation error: {e}")
        return jsonify({"error": "Failed to evaluate content"}), 500

if __name__ == "__main__":
    app.run(port=3000, debug=True)
