from entities import Image, ImageAPI
from PIL import Image as PILImage
from io import BytesIO
import aiohttp
import logging

logger = logging.getLogger(__name__)


class PillowImageLoader(ImageAPI):
    async def load_from_url(self, url) -> Image:
        logger.info('START load')
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response.raise_for_status()
                image_bytes = await response.content.read()
                pillow_image = PILImage.open(BytesIO(image_bytes))
                width, height = pillow_image.size
                logger.info('STOP load')
                return Image(url=url, width=width, height=height)
