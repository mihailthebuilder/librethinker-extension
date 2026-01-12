import urllib.request
import json
import platform
from dataclasses import dataclass
from typing import Optional
import random
import time
import uuid
import base64
import os


@dataclass
class Response:
    latestExtensionVersion: str
    success: bool
    message: str
    response: str


class LtClient:
    def __init__(
        self,
        extensionVersion: str,
    ):
        self.requestId = str(uuid.uuid4())
        self.base_headers = {
            "Content-Type": "application/json",
            "X-Client-Request-ID": self.requestId,
            "X-Client-Platform": platform.platform(),
            "X-Extension-Version": extensionVersion,
        }
        self.baseUrl = "https://api.librethinker.com/api/v1/jobs/"
        self.clientSecret = (
            base64.urlsafe_b64encode(os.urandom(16)).decode("utf-8").rstrip("=")
        )

    def getBaseHeaders(self):
        return self.base_headers.copy()

    def getAnswer(
        self, inputPrompt: str, docText: str, apiKey: Optional[str]
    ) -> Response:
        jobId = self.initJob(inputPrompt, docText, apiKey)

        timeout_seconds = 180
        start_time = time.monotonic()

        delay = 2
        max_delay = 30

        while time.monotonic() - start_time < timeout_seconds:
            # Randomized jitter aroudn sleep time
            sleep_time = delay + random.uniform(0, delay)

            # Don't sleep past the total timeout
            remaining = timeout_seconds - (time.monotonic() - start_time)
            if remaining <= 0:
                break

            time.sleep(min(sleep_time, remaining))
            delay = min(delay + 2, max_delay)

            result = self.getJobResult(jobId)
            if len(result.response) > 0:
                return result

        result.success = False
        result.message = "Request timed out."
        return result

    def initJob(self, inputPrompt: str, docText: str, apiKey: Optional[str]) -> str:
        body = json.dumps(
            {"prompt": inputPrompt, "text": docText, "clientSecret": self.clientSecret}
        ).encode("utf-8")

        headers = self.getBaseHeaders()
        if apiKey is not None:
            headers["X-Third-Party-Key"] = apiKey
            appendUrl = "byok"
        else:
            appendUrl = "free"

        initJobReq = urllib.request.Request(
            self.baseUrl + appendUrl,
            data=body,
            method="POST",
            headers=headers,
        )

        with urllib.request.urlopen(initJobReq, timeout=30) as response:
            data = json.loads(response.read().decode("utf-8"))
            jobId = data["jobId"]

        return jobId

    def getJobResult(self, jobId: str) -> Response:
        body = json.dumps({"jobId": jobId, "clientSecret": self.clientSecret}).encode(
            "utf-8"
        )

        jobResultReq = urllib.request.Request(
            self.baseUrl + "fetch",
            method="POST",
            data=body,
            headers=self.getBaseHeaders(),
        )

        with urllib.request.urlopen(jobResultReq, timeout=30) as res:
            response = Response(
                latestExtensionVersion=res.headers["Client-Version-Latest"],
                success=True,
                response=json.loads(res.read().decode("utf-8"))["response"],
                message="",
            )

        return response
