from io import BytesIO
from PIL import Image

from beholder_client.ops import capture, capture_async


class BeholderClient:
    """
    Beholder API client.
    """

    def __init__(self, base_url: str, x_api_key: str, timeout_seconds: float = 10.0):
        """
        Args:
            base_url: Base URL of the Beholder server.
            x_api_key: Beholder API key.
            timeout_seconds: Timeout for requests in seconds.
        """
        self._base_url = base_url.rstrip("/")
        self._x_api_key = x_api_key
        self.timeout_seconds = timeout_seconds

    def capture_raw(self, video_url: str, elapsed_time_millis: int) -> bytes:
        """
        Capture a frame from a video and return the raw bytes.

        Args:
            video_url: URL of the video to capture a frame from.
            elapsed_time_millis: Time in milliseconds since the start of the video.

        Returns:
            Raw bytes of the image.
        """
        return capture(
            self._base_url,
            video_url,
            elapsed_time_millis,
            self._x_api_key,
            timeout_seconds=self.timeout_seconds,
        )

    def capture(self, video_url: str, elapsed_time_millis: int) -> Image.Image:
        """
        Capture a frame from a video and parse it into a PIL Image.

        Args:
            video_url: URL of the video to capture a frame from.
            elapsed_time_millis: Time in milliseconds since the start of the video.

        Returns:
            Parsed image.
        """
        image_bytes = self.capture_raw(video_url, elapsed_time_millis)
        return Image.open(BytesIO(image_bytes))

    async def capture_raw_async(
        self, video_url: str, elapsed_time_millis: int
    ) -> bytes:
        """
        Capture a frame from a video asynchronously and return the raw bytes.

        Args:
            video_url: URL of the video to capture a frame from.
            elapsed_time_millis: Time in milliseconds since the start of the video.

        Returns:
            Raw bytes of the image.
        """
        return await capture_async(
            self._base_url,
            video_url,
            elapsed_time_millis,
            self._x_api_key,
            timeout_seconds=self.timeout_seconds,
        )

    async def capture_async(
        self, video_url: str, elapsed_time_millis: int
    ) -> Image.Image:
        """
        Capture a frame from a video asynchronously and parse it into a PIL Image.

        Args:
            video_url: URL of the video to capture a frame from.
            elapsed_time_millis: Time in milliseconds since the start of the video.

        Returns:
            Parsed image.
        """
        image_bytes = await self.capture_raw_async(video_url, elapsed_time_millis)
        return Image.open(BytesIO(image_bytes))
