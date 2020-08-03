from dataclasses import dataclass


@dataclass
class Image:
    width: int
    height: int
    url: str


class ImageAPI:
    """
    The sole purpose of this API is to get the width and height of an image
    """
    async def load_from_url(self, url) -> Image:
        pass

