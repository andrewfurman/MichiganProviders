
"""
Utility: convert an uploaded image (Werkzeug FileStorage) to
GitHub-flavoured Markdown using an OpenAI Vision model.

Environment:
  * OPENAI_API_KEY – already set in your container / host
"""

import base64
from typing import Union, IO
from openai import OpenAI

client = OpenAI()

def _encode_image(file_obj: Union[IO[bytes], "FileStorage"]) -> str:
    """
    Return a data-URL string (data:image/…;base64,...) that the
    Chat Completions endpoint accepts.
    """
    mime = getattr(file_obj, "mimetype", None) or "image/png"
    b64 = base64.b64encode(file_obj.read()).decode("utf-8")
    return f"data:{mime};base64,{b64}"

def image_to_markdown(file_storage, detail: str = "high") -> str:
    """
    Send the image to the model and return the Markdown transcription.
    """
    data_url = _encode_image(file_storage)

    tools = [{
        "type": "function",
        "function": {
            "name": "transcribe_image",
            "description": "Transcribe text from an image into GitHub-flavoured Markdown format",
            "parameters": {
                "type": "object",
                "properties": {
                    "markdown_text": {
                        "type": "string",
                        "description": "The markdown formatted text transcribed from the image"
                    }
                },
                "required": ["markdown_text"],
                "additionalProperties": False
            },
            "strict": True
        }
    }]

    response = client.chat.completions.create(
        model="gpt-4.1-mini",  # any vision-capable model is fine
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": (
                            "Transcribe every piece of text in this image, "
                            "re-create the layout in GitHub-flavoured Markdown. "
                            "Preserve tables, headings, and any obvious structure."
                        ),
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": data_url, "detail": detail},
                    },
                ],
            }
        ],
        tools=tools,
        tool_choice={"type": "function", "function": {"name": "transcribe_image"}}
    )

    # Extract markdown text from function call
    tool_call = response.choices[0].message.tool_calls[0]
    return tool_call.function.arguments.strip('{}"\n').replace('"markdown_text":', '')
