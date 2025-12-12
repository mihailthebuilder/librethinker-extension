import urllib.request
import json
import os


def get_answer(inputPrompt: str, docText: str, api_key: str | None) -> str:
    LLM_API_URL = "https://api.librethinker.com/api/v1/responses"

    body = json.dumps({"prompt": inputPrompt, "text": docText}).encode("utf-8")
    headers = {
        "Content-Type": "application/json",
    }
    if api_key is not None:
        headers["X-Third-Party-Key"] = api_key

    req = urllib.request.Request(
        LLM_API_URL,
        data=body,
        method="POST",
        headers=headers,
    )

    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode("utf-8"))
        return data["response"]
