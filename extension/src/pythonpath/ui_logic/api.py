import urllib.request
import json
import platform


def get_answer(inputPrompt: str, docText: str, api_key: str | None) -> str:
    url = "https://api.librethinker.com/api/v1/responses/"

    body = json.dumps(
        {
            "prompt": inputPrompt,
            "text": docText,
            "platform": platform.platform(),
            "extensionVersion": "0.1.2",
        }
    ).encode("utf-8")
    headers = {
        "Content-Type": "application/json",
    }

    append_url = "free"
    if api_key is not None:
        headers["X-Third-Party-Key"] = api_key
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
