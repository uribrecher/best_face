import asyncio
from entities import FaceDetectionAPI, ImageAPI, Image, best_face, Face
from typing import List


async def gather_images(list_of_image_urls: List[str],
                        image_api: ImageAPI) -> List[Image]:
    tasks = []
    for url in list_of_image_urls:
        tasks.append(image_api.load_from_url(url))
    return await asyncio.gather(*tasks)


async def gather_faces(list_of_image_urls: List[str],
                       face_detection_api: FaceDetectionAPI) -> List[Face]:
    tasks = []
    for url in list_of_image_urls:
        tasks.append(face_detection_api.detect(url))
    detect_results = await asyncio.gather(*tasks)
    flat_list = [item for sublist in detect_results for item in sublist]
    return flat_list


async def handle_best_face(list_of_image_urls: List[str],
                           face_detection_api: FaceDetectionAPI,
                           image_api: ImageAPI) -> str:
    # TODO: handle timeouts and best effort logic
    images, faces = await asyncio.gather(
        gather_images(list_of_image_urls, image_api),
        gather_faces(list_of_image_urls, face_detection_api))
    face_ids = [face.id for face in faces]
    groups = await face_detection_api.group(face_ids)

    face_by_id = {face.id: face for face in faces}
    image_by_url = {image.url: image for image in images}
    image_by_id = {face.id: image_by_url[face.url] for face in faces}

    best_face_id = best_face(face_by_id, image_by_id, groups)
    return face_by_id[best_face_id].url
