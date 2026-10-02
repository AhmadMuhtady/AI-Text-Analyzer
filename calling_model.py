import os
import json
from dotenv import load_dotenv
from openai import OpenAI, RateLimitError, APIError, AuthenticationError, NotFoundError
from json_validation import json_validation

load_dotenv(override=True)
open_ai_api_key = os.getenv('OPENAI_API_KEY')

if open_ai_api_key is None:
    raise ValueError('OPENAI_API_KEY is missing')

open_ai = OpenAI(api_key=open_ai_api_key)

LENGTH_RULES = {
    "short": "exactly 1 to 2 sentences",
    "medium": "exactly 3 to 5 sentences",
    "long": "exactly 6 to 10 sentences",
}

SYSTEM_PROMPT_TEMPLATE = """You are a text analysis engine. Your sole task is to analyze the provided text and output a strictly valid JSON object containing specific metadata.

Field Definitions:
1. `title` (string): A concise, relevant headline generated from the text.
2. `main_topic` (string): The broad subject, domain, or category the text is primarily about (e.g., "Economics", "Artificial Intelligence", "Public Health").
3. `summary` (array of strings): A list of sentences synthesizing key points and conclusions. Each item in the array MUST be exactly one standalone sentence. You must produce {length_rule}.
4. `sentiment` (string): The overall tone or stance. Must be exactly one of: "positive", "negative", or "neutral".

Output Constraints:
Return ONLY the JSON object conforming to the schema. Do not include markdown formatting or commentary."""

text_analysis_format = {
    "type": "json_schema",
    "name": "text_analysis",
    "strict": True,
    "schema": {
        "type": "object",
        "properties": {
            "title": {"type": "string"},
            "main_topic": {"type": "string"},
            "summary": {
                "type": "array",
                "items": {"type": "string"},
                "description": "A list of individual sentences making up the summary.",
            },
            "sentiment": {
                "type": "string",
                "enum": ["positive", "neutral", "negative"],
            },
        },
        "required": ["title", "main_topic", "summary", "sentiment"],
        "additionalProperties": False,
    },
}

def handle_ai_error(error: Exception) -> dict:
    if isinstance(error, RateLimitError):
        error_type = "rate_limit"
        ui_message = "We're receiving a high volume of requests right now. Please wait a few seconds and try again."
    elif isinstance(error, AuthenticationError):
        error_type = "authentication_error"
        ui_message = "Authentication issue encountered. Please verify your API key or account settings."
    elif isinstance(error, NotFoundError):
        error_type = "model_not_found"
        ui_message = "The requested AI model is currently unavailable. Please check your configuration."
    elif isinstance(error, json.JSONDecodeError):
        error_type = "invalid_json"
        ui_message = "The model generated a malformed response. Please retry with your text."
    elif isinstance(error, APIError):
        error_type = "api_error"
        ui_message = "The AI service is experiencing a brief hiccup. Please try submitting again in a moment."
    else:
        error_type = "unknown_error"
        ui_message = "Something unexpected occurred. Please try again shortly."

    result = {"error": error_type, "message": ui_message, "detail": str(error)}
    print(f"Error: {result}")
    return result

def handle_validation_errors(error: Exception) -> dict:
    if isinstance(error, (TypeError, KeyError, ValueError)):
        error_type = "validation_error"
        ui_message = "The analysis output did not match the expected format. Please try running it again."
    else:
        error_type = "unknown_error"
        ui_message = "An unexpected error occurred during validation. Please try again."

    result = {"error": error_type, "message": ui_message, "detail": str(error)}
    print(f"Error: {result}")
    return result

def analyze_text(record: dict) -> dict:
    text = record.get('text')
    length_key = record.get('length')
    rule = LENGTH_RULES.get(length_key, "exactly 3 to 5 sentences")

    system_prompt = SYSTEM_PROMPT_TEMPLATE.format(length_rule=rule)
    user_prompt = f"""Target summary length: {rule}. Provide each sentence as an item in the `summary` array.

TEXT START:
{text}
TEXT END"""

    try:
        response = open_ai.responses.create(
            model="gpt-4o-mini",
            instructions=system_prompt,
            input=user_prompt,
            text={'format': text_analysis_format},
        )

        raw_result = json.loads(response.output_text)
        validated = json_validation(raw_result)
        

        validated["summary"] = " ".join(validated["summary"])
        return validated
    except json.JSONDecodeError as e:
        return handle_ai_error(e)
    except (TypeError, KeyError, ValueError) as e:
        return handle_validation_errors(e)
    except Exception as e:
        return handle_ai_error(e)