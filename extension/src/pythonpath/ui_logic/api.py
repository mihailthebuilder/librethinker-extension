import urllib.request
import json
import platform
from dataclasses import dataclass


@dataclass
class Request:
    inputPrompt: str
    docText: str
    apiKey: str | None


def get_answer(request: Request) -> str:
    url = "https://api.librethinker.com/api/v1/responses/"

    body = json.dumps(
        {
            "prompt": request.inputPrompt,
            "text": request.docText,
            "platform": platform.platform(),
            "extensionVersion": "0.1.2",
        }
    ).encode("utf-8")
    headers = {
        "Content-Type": "application/json",
    }

    append_url = "free"
    if request.apiKey is not None:
        headers["X-Third-Party-Key"] = request.apiKey
        append_url = "byok"

    url += append_url

    req = urllib.request.Request(
        url,
        data=body,
        method="POST",
        headers=headers,
    )

    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode("utf-8"))
        return data["response"]
