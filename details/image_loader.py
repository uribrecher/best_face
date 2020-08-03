from entities import Image, ImageAPI
from PIL import Image as PILImage
from io import BytesIO
import aiohttp
import logging


class PillowImageLoader(ImageAPI):
    async def load_from_url(self, url) -> Image:
        logging.info('START load')
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                image_bytes = await response.content.read()
                pillow_image = PILImage.open(BytesIO(image_bytes))
                width, height = pillow_image.size
                logging.info('STOP load')
                return Image(url=url, width=width, height=height)

