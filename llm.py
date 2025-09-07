import json
from pathlib import Path

from openai import OpenAI

from settings import settings

PROMPT = """
Given an email text/html, help the user extract details that they want in the format that they want.

{metadata}

{content}

What job did I apply to?
Just give me company name, role, location and date if you can find. Exclude links.

return a JSON
{{
    "company_name": ...,
    "role":...,
    "location":...,
    "date":....,
    "status":... #if i have applied or if it is a rejection or acceptance,
    "comment":... # short crisp summary
}}
status field MUST BE on of Literal["APPLIED", "REJECTED", "ACCEPTED"]
"""


def generate(metadata, content):
    client = OpenAI(api_key=settings.OPENAI_API_KEY)

    response = client.responses.create(
        model="gpt-5-nano",
        input=[
            {
                "role": "developer",
                "content": [
                    {
                        "type": "input_text",
                        "text": PROMPT.format(metadata=metadata, content=content),
                    }
                ],
            }
        ],
        text={"format": {"type": "json_object"}, "verbosity": "medium"},
        reasoning={"effort": "minimal"},
        store=False,
    )

    return response.output_text


if __name__ == "__main__":
    emails_dir = Path("emails")

    html_file = next(iter(emails_dir.glob("*.html")))

    text_file = html_file.with_suffix(".txt")
    print(f"Processing: {html_file.name}")

    html_content = html_file.read_text(encoding="utf-8")
    metadata = text_file.read_text(encoding="utf-8")
    response = generate(metadata, html_content)

    cleaned_response = response.replace("```json", "").replace("```", "").strip()

    try:
        data = json.loads(cleaned_response)
        print(f"Extracted data: {json.dumps(data, indent=2)}")
    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON: {e}")
        print(f"Raw response: {response}")

    print("-" * 50)
