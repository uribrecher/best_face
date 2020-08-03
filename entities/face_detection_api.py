from .best_face import Face
from typing import List


class FaceDetectionAPI:
    """
    A general API for face detection and face grouping
    """
    async def detect(self, image_url: str) -> List[Face]:
        pass

    async def group(self, face_ids: List[str]) -> List[List[str]]:
        pass
