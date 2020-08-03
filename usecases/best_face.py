import asyncio
from entities import FaceDetectionAPI, ImageAPI, Image, best_face, Face
from typing import List, Mapping, Tuple
import logging


logger = logging.getLogger(__name__)
TIMEOUT = 2  # TODO: put this in configuration file


async def gather_images(list_of_image_urls: List[str],
                        image_api: ImageAPI) -> Mapping[str, Image]:
    tasks = [asyncio.create_task(image_api.load_from_url(url)) for url in list_of_image_urls]
    image_by_url = {}
    try:
        for coro in asyncio.as_completed(tasks, timeout=TIMEOUT):
            image = await coro
            image_by_url[image.url] = image
    except asyncio.TimeoutError:
        logger.warning(f'gather_images timed out')
    return image_by_url


async def gather_faces(list_of_image_urls: List[str],
                       face_detection_api: FaceDetectionAPI) -> Tuple[List[Face], int]:
    tasks = [asyncio.create_task(face_detection_api.detect(url)) for url in list_of_image_urls]
    face_list = []
    url_count = 0
    try:
        for coro in asyncio.as_completed(tasks, timeout=TIMEOUT):
            detect_result = await coro
            face_list = face_list + detect_result  # flatten the list
            url_count = url_count + 1
    except asyncio.TimeoutError:
        logger.warning(f'gather_faces timed out')

    return face_list, url_count


async def group_faces(list_of_image_urls: List[str],
                      face_detection_api: FaceDetectionAPI) -> (List[Face], List[List[str]]):
    faces, url_count = await gather_faces(list_of_image_urls, face_detection_api)
    # only after all faces are detect can we start sending the group request
    face_ids = [face.id for face in faces]
    groups = await face_detection_api.group(face_ids)
    return faces, groups, url_count


async def handle_best_face(list_of_image_urls: List[str],
                           face_detection_api: FaceDetectionAPI,
                           image_api: ImageAPI):
    """
    :return: he image url that contain the best face

    using both face detection api and image loading api this use-case
    will gather all required data and then process it using best_face function
    """
    image_by_url, (faces, groups, url_count) = await asyncio.gather(
        gather_images(list_of_image_urls, image_api),
        group_faces(list_of_image_urls, face_detection_api))

    # NOTE: if we got timed out fetching images we also remove the
    # face detections of that url (see filters in the comprehensions)
    face_by_id = {face.id: face for face in faces if face.url in image_by_url.keys()}
    image_by_id = {face.id: image_by_url[face.url] for face in face_by_id.values()}
    best_face_id = best_face(face_by_id, image_by_id, groups)
    return {
        'bestFace': face_by_id[best_face_id].url,
        'confidence': min(url_count, len(image_by_url)) / len(list_of_image_urls)
    }
