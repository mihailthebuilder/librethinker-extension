import urllib.request
import json
import platform
from dataclasses import dataclass, fields
from typing import Optional


class Request:
    def __init__(
        self,
        inputPrompt: str,
        docText: str,
        apiKey: Optional[str],
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
    latestExtensionVersion: str
    success: bool
    message: str
    response: Optional[str] = None


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

    req = urllib.request.Request(
        url + append_url,
        data=body,
        method="POST",
        headers=headers,
    )

    with urllib.request.urlopen(req, timeout=180) as response:
        data = json.loads(response.read().decode("utf-8"))

        allowed_keys = {f.name for f in fields(Response)}
        filtered_data = {k: v for k, v in data.items() if k in allowed_keys}

        return Response(**filtered_data)


def get_direct_answer(
    endpoint: str, model: str, api_key: Optional[str], prompt: str, doc_text: str
) -> str:
    """
    Call OpenAI-compatible /v1/chat/completions endpoint.
    Works with Ollama, LM Studio, and other compatible servers.

    Args:
        endpoint: Base URL (e.g., "http://localhost:11434/v1")
        model: Model name (e.g., "llama3", "mistral")
        api_key: Optional API key (may be required by some servers)
        prompt: User's prompt/instruction
        doc_text: Document or selected text

    Returns:
        str: The generated response text

    Raises:
        Exception: If the request fails or response format is invalid
    """
    # Ensure endpoint ends with proper path
    if not endpoint.endswith("/v1"):
        endpoint = endpoint.rstrip("/") + "/v1"

    url = endpoint.rstrip("/") + "/chat/completions"

    # Combine prompt and document text into a single user message
    combined_content = f"Prompt: {prompt}\n\nDocument:\n{doc_text}"

    body = json.dumps(
        {
            "model": model,
            "messages": [{"role": "system", "content": "This content is from a libre office document. You are a helpful assistant that helps the user edit the document as requested."}, {"role": "user", "content": combined_content}],
            "stream": False,
        }
    ).encode("utf-8")

    headers = {
        "Content-Type": "application/json",
    }

    # Add authorization header if API key is provided
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    req = urllib.request.Request(url, data=body, method="POST", headers=headers)

    try:
        with urllib.request.urlopen(req, timeout=180) as response:
            data = json.loads(response.read().decode("utf-8"))

            # Parse OpenAI-compatible response format
            if "choices" not in data or len(data["choices"]) == 0:
                raise Exception("Invalid response format: missing 'choices'")

            message = data["choices"][0].get("message", {})
            content = message.get("content", "")

            if not content:
                raise Exception("Empty response from model")

            return content

    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8", errors="replace")
        raise Exception(
            f"HTTP {e.code} error from {url}: {error_body[:200]}"
        )
    except urllib.error.URLError as e:
        raise Exception(
            f"Connection error: {str(e)}. Make sure the server is running at {endpoint}"
        )
