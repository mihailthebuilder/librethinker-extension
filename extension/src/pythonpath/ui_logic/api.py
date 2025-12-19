import urllib.request
import json
import platform
from dataclasses import dataclass, fields


class Request:
    def __init__(
        self,
        inputPrompt: str,
        docText: str,
        apiKey: str | None,
        id: str,
        extensionVersion: str,
    ):
        self.inputPrompt = inputPrompt
        self.docText = docText
        self.apiKey = apiKey
        self.id = id
        self.extensionVersion = extensionVersion

        self.platform = platform.platform()


@dataclass
class Response:
    response: str | None = None
    latestExtensionVersion: str
    success: bool
    message: str


def get_answer(request: Request) -> Response:
    url = "https://api.librethinker.com/api/v1/responses/"

    body = json.dumps(
        {
            "prompt": request.inputPrompt,
            "text": request.docText,
        }
    ).encode("utf-8")
    headers = {
        "Content-Type": "application/json",
        "X-Client-Request-ID": request.id,
        "X-Client-Platform": request.platform,
        "X-Extension-Version": request.extensionVersion,
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

    with urllib.request.urlopen(req, timeout=10) as response:
        data = json.loads(response.read().decode("utf-8"))

        allowed_keys = {f.name for f in fields(Response)}
        filtered_data = {k: v for k, v in data.items() if k in allowed_keys}

        return Response(**filtered_data)
