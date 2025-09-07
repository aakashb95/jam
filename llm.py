import json
from pathlib import Path

from google import genai
from google.genai import types

from settings import settings

PROMPT = """
Given an email text/html, help the user extract details that they want in the format that they want.

{email}

What job did I apply to?
Just give me company name, role, location and date if you can find. Exclude links.

return a JSON
{{
    "company_name": ...,
    "role":...,
    "location":...,
    "date":....,
    "comment":... #if i have applied or if it is a rejection or acceptance
}}
comment field MUST BE on of Literal["APPLIED", "REJECTED", "ACCEPTED"]
"""


def generate(text):
    client = genai.Client(
        api_key=settings.GEMINI_API_KEY,
    )

    model = "gemma-3-27b-it"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=PROMPT.format(email=text)),
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig()

    response = client.models.generate_content(
        model=model, contents=contents, config=generate_content_config
    )

    return response.text


if __name__ == "__main__":
    emails_dir = Path("emails")

    html_file = next(iter(emails_dir.glob("*.html")))
    print(f"Processing: {html_file.name}")

    html_content = html_file.read_text(encoding="utf-8")
    response = generate(html_content)

    cleaned_response = response.replace("```json", "").replace("```", "").strip()

    try:
        data = json.loads(cleaned_response)
        print(f"Extracted data: {json.dumps(data, indent=2)}")
    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON: {e}")
        print(f"Raw response: {response}")

    print("-" * 50)
