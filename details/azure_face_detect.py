from entities import FaceDetectionAPI, Face
from typing import List
import aiohttp
import logging

FACE_RECT = 'faceRectangle'
WIDTH = 'width'
HEIGHT = 'height'
FACE_ID = 'faceId'
FACE_IDS = 'faceIds'
URL = 'url'
GROUPS = 'groups'


class AzureFaceDetect(FaceDetectionAPI):
    def __init__(self, host, key):
        self.headers = {'Ocp-Apim-Subscription-Key': key}
        self.endpoint = f'https://{host}/face/v1.0'
        self.detect_params = {
            'returnFaceId': 'true',
            'detectionModel': 'detection_02',
        }

    async def detect(self, image_url: str) -> List[Face]:
        logging.info('START detect')
        async with aiohttp.ClientSession() as session:
            async with session.post(self.endpoint + '/detect',
                                    params=self.detect_params,
                                    json={URL: image_url},
                                    headers=self.headers) as response:
                results = await response.json()
                face_list = [Face(id=r[FACE_ID],
                                  width=r[FACE_RECT][WIDTH],
                                  height=r[FACE_RECT][HEIGHT],
                                  url=image_url) for r in results]
                logging.info('STOP detect')
                return face_list

    async def group(self, face_ids: List[str]) -> List[List[str]]:
        logging.info('START group')
        async with aiohttp.ClientSession() as session:
            async with session.post(self.endpoint + '/group',
                                    json={FACE_IDS: face_ids},
                                    headers=self.headers) as response:
                result = await response.json()
                logging.info('STOP group')
                return result[GROUPS]
