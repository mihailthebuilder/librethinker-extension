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
class JobResult:
    latestExtensionVersion: str
    status: str
    response: str


@dataclass
class Response:
    latestExtensionVersion: str
    success: bool
    response: str = ""
    message: str = ""


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
            if result.status == "successful":
                return Response(
                    response=result.response,
                    latestExtensionVersion=result.latestExtensionVersion,
                    success=True,
                )

            if result.status == "failed":
                return Response(
                    latestExtensionVersion=result.latestExtensionVersion,
                    success=False,
                    message="Failed to get response from LLM.",
                )

        return Response(
            latestExtensionVersion=result.latestExtensionVersion,
            success=False,
            message="LLM took too long to answer.",
        )

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

    def getJobResult(self, jobId: str) -> JobResult:
        data = json.dumps({"jobId": jobId, "clientSecret": self.clientSecret}).encode(
            "utf-8"
        )

        jobResultReq = urllib.request.Request(
            self.baseUrl + "fetch",
            method="POST",
            data=data,
            headers=self.getBaseHeaders(),
        )

        with urllib.request.urlopen(jobResultReq, timeout=30) as res:
            data = json.loads(res.read().decode("utf-8"))

            response = JobResult(
                latestExtensionVersion=res.headers["Client-Version-Latest"],
                status=data["status"],
                response=data["response"],
            )

        return response
