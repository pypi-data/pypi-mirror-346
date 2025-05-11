# File: autobyteus/tools/image_downloader.py

import os
import aiohttp
import logging
from datetime import datetime
from autobyteus.tools.base_tool import BaseTool
from PIL import Image
from io import BytesIO
from autobyteus.utils.file_utils import get_default_download_folder
from autobyteus.events.event_types import EventType
from autobyteus.events.decorators import event_listener

logger = logging.getLogger(__name__)

class ImageDownloader(BaseTool):
    # Define supported_formats as a class variable so it can be accessed in class methods
    supported_formats = ['.jpeg', '.jpg', '.gif', '.png', '.webp']
    
    def __init__(self, custom_download_folder=None):
        super().__init__()
        self.default_download_folder = get_default_download_folder()
        self.download_folder = custom_download_folder or self.default_download_folder
        self.supported_formats = self.__class__.supported_formats  # Set instance attribute from class variable for backward compatibility
        self.last_downloaded_image = None

    @classmethod
    def tool_usage_xml(cls):
        """
        Return an XML string describing the usage of the ImageDownloader tool.

        Returns:
            str: An XML description of how to use the ImageDownloader tool.
        """
        return f'''ImageDownloader: Downloads an image from a given URL.

Usage:
<command name="ImageDownloader">
    <arg name="url">image_url</arg>
</command>

Parameters:
- "image_url": A string containing a direct URL to an image file (must end with {', '.join(cls.supported_formats)})

Supported image formats: {', '.join(format.upper()[1:] for format in cls.supported_formats)}

Positive examples:
<command name="ImageDownloader">
    <arg name="url">https://example.com/photo.jpg</arg>
</command>

<command name="ImageDownloader">
    <arg name="url">https://example.com/image.png</arg>
</command>

Negative examples (These will not work):
<command name="ImageDownloader">
    <arg name="url">https://example.com/page_containing_image.html</arg>
</command>

<command name="ImageDownloader">
    <arg name="url">https://example.com/image_without_extension</arg>
</command>

Note: The URL must be a direct link to the image file, not a webpage containing the image.'''
    async def _execute(self, **kwargs):
        url = kwargs.get('url')
        if not url:
            raise ValueError("The 'url' keyword argument must be specified.")

        custom_folder = kwargs.get('folder')
        download_folder = custom_folder or self.download_folder

        if not any(url.lower().endswith(fmt) for fmt in self.supported_formats):
            raise ValueError(
                f"Unsupported image format. The URL must end with one of the following extensions: "
                f"{', '.join(self.supported_formats)}. Provided URL: {url}"
            )

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    response.raise_for_status()
                    image_bytes = await response.read()

            with Image.open(BytesIO(image_bytes)) as img:
                img.verify()
                fmt = img.format

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            extension = os.path.splitext(url)[1].lower()
            filename = f"downloaded_image_{timestamp}{extension}"
            filepath = os.path.join(download_folder, filename)

            os.makedirs(download_folder, exist_ok=True)
            with open(filepath, 'wb') as f:
                f.write(image_bytes)

            self.last_downloaded_image = filepath
            logger.info(f"The image is downloaded and stored at: {filepath}")
            return f"The image is downloaded and stored at: {filepath}"
        except aiohttp.ClientError as e:
            logger.error(f"Failed to download image from {url}. Error: {str(e)}")
            raise ValueError(f"Failed to download image from {url}. Error: {str(e)}")
        except Exception as e:
            logger.error(f"Error processing image from {url}. Error: {str(e)}")
            raise ValueError(f"Error processing image from {url}. Error: {str(e)}")

    @event_listener(EventType.WEIBO_POST_COMPLETED)
    def on_weibo_post_completed(self, *args, **kwargs):
        if self.last_downloaded_image and os.path.exists(self.last_downloaded_image):
            try:
                os.remove(self.last_downloaded_image)
                logger.info(f"Removed downloaded image: {self.last_downloaded_image}")
            except Exception as e:
                logger.error(f"Failed to remove downloaded image: {self.last_downloaded_image}. Error: {str(e)}")
        else:
            logger.warning("No image to remove or image file not found.")
        self.last_downloaded_image = None
