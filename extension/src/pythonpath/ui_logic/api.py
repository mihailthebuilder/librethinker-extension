import urllib.request
import json
import os


def get_answer(prompt: str) -> str:
    LLM_API_URL = "https://api.librethinker.com/api/v0/responses"
    LLM_API_KEY = os.environ["LT_LLM_API_KEY"]

    body = json.dumps({"input": prompt}).encode("utf-8")

    req = urllib.request.Request(
        LLM_API_URL,
        data=body,
        method="POST",
        headers={
            "Content-Type": "application/json",
            "X-Third-Party-Key": LLM_API_KEY,
        },
    )

    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode("utf-8"))
        return data["response"]
