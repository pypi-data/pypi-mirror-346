"""
Beholder operations.
"""

from httpx import post, Timeout, AsyncClient


def capture(
    base_url: str,
    video_url: str,
    elapsed_time_millis: int,
    x_api_key: str,
    timeout_seconds: float = 10.0,
) -> bytes:
    """
    Capture a frame from a video.

    Args:
        base_url: Base URL of the Beholder server.
        video_url: URL of the video to capture a frame from.
        elapsed_time_millis: Time in milliseconds since the start of the video.
        x_api_key: Beholder API key.
        timeout_seconds: Timeout for the request in seconds.
    """
    data = {"videoUrl": video_url, "elapsedTimeMillis": elapsed_time_millis}

    headers = {"X-Api-Key": x_api_key}

    url = base_url.rstrip("/") + "/capture"

    response = post(url, json=data, headers=headers, timeout=Timeout(timeout_seconds))
    response.raise_for_status()

    return response.content


async def capture_async(
    base_url: str,
    video_url: str,
    elapsed_time_millis: int,
    x_api_key: str,
    timeout_seconds: float = 10.0,
) -> bytes:
    """
    Capture a frame from a video asynchronously.

    Args:
        base_url: Base URL of the Beholder server.
        video_url: URL of the video to capture a frame from.
        elapsed_time_millis: Time in milliseconds since the start of the video.
        x_api_key: Beholder API key.
        timeout_seconds: Timeout for the request in seconds.
    """
    data = {"videoUrl": video_url, "elapsedTimeMillis": elapsed_time_millis}

    headers = {"X-Api-Key": x_api_key}

    url = base_url.rstrip("/") + "/capture"

    async with AsyncClient() as client:
        response = await client.post(
            url, json=data, headers=headers, timeout=Timeout(timeout_seconds)
        )
        response.raise_for_status()

        return response.content
