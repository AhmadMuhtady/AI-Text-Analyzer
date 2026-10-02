import os
import json
from dotenv import load_dotenv
from openai import OpenAI, RateLimitError, APIError, AuthenticationError, NotFoundError

load_dotenv(override=True)
open_Ai_api_key = os.getenv('OPENAI_API_KEY')
open_Ai = OpenAI(api_key=open_Ai_api_key)


system_prompt = """
You are a text analysis engine. Your sole task is to analyze the provided text and output a strictly valid JSON object containing specific metadata.

Field Definitions

1. `title` type = [str]: A concise, relevant headline generated from the text.
2. `main_topic`: The broad subject, domain, or category the text is primarily about (e.g., "Economics", "Artificial Intelligence", "Public Health"). This is an objective classification label, distinct from the headline.
3. `summary`: A single string synthesizing key points and conclusions, formatted according to the requested length parameter:
    "short": 1 to 2 sentences.
    "medium": 3 to 5 sentences.
    "long": 6 to 10 sentences organized into a continuous narrative. Do not use markdown lists, bullet points, or raw line breaks.
4. `sentiment`: The overall tone or stance of the text. Must be exactly one of these lowercase strings: "positive", "negative", or "neutral".
    Use "neutral" for purely informational text, balanced objective reporting, or text containing balanced positive and negative elements.

Output Constraints

 Return ONLY a valid JSON object.
 Do NOT wrap the JSON in Markdown code fences (no ```json).
 Do NOT include commentary, preambles, explanations, or trailing text.
 The JSON object must contain EXACTLY these four keys and no others: "title", "main_topic", "summary", "sentiment".
"""

def handle_ai_error(error):
    if isinstance(error, RateLimitError):
        error_type = "rate_limit"
    elif isinstance(error, AuthenticationError):
        error_type = "authentication_error"
    elif isinstance(error, NotFoundError):
        error_type = "model_not_found"
    elif isinstance(error, APIError):
        error_type = "api_error"
    elif isinstance(error, json.JSONDecodeError):
        error_type = "invalid_json"
    elif isinstance(error,TypeError):
    else:
        error_type = "unknown_error"

    result = {
        "error": error_type,
        "message": str(error)
    }
    print(f"Error:", result)
    return result


def canalyze_text(text,length):
    user_prompt = f"""
    Analyze the text below.
    Target summary length: {length}
    TEXT START:
    {text}
    TEXT END
    """

    try:
        response = open_Ai.chat.completions.create(
            model = "gpt-4o-mini",
            messages = [{'role':'system','content':system_prompt },{'role':'user','content': user_prompt }],
            response_format={"type": "json_object"},
        )

        result = json.loads(response.choices[0].message.content)
        return result
    except Exception as e:
        return handle_ai_error(e)