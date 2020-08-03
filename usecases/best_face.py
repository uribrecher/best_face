import asyncio
from entities import FaceDetectionAPI, ImageAPI, Image, best_face, Face
from typing import List, Mapping


async def gather_images(list_of_image_urls: List[str],
                        image_api: ImageAPI) -> Mapping[str, Image]:
    tasks = []
    for url in list_of_image_urls:
        tasks.append(image_api.load_from_url(url))
    images = await asyncio.gather(*tasks)
    return {image.url: image for image in images}


async def gather_faces(list_of_image_urls: List[str],
                       face_detection_api: FaceDetectionAPI) -> List[Face]:
    tasks = []
    for url in list_of_image_urls:
        tasks.append(face_detection_api.detect(url))
    detect_results = await asyncio.gather(*tasks)
    flat_list = [item for sublist in detect_results for item in sublist]
    return flat_list


async def group_faces(list_of_image_urls: List[str],
                      face_detection_api: FaceDetectionAPI) -> (List[Face], List[List[str]]):
    faces = await gather_faces(list_of_image_urls, face_detection_api)
    # only after all faces are detect can we start sending the group request
    face_ids = [face.id for face in faces]
    groups = await face_detection_api.group(face_ids)
    return faces, groups


async def handle_best_face(list_of_image_urls: List[str],
                           face_detection_api: FaceDetectionAPI,
                           image_api: ImageAPI) -> str:
    """
    :param list_of_image_urls:
    :param face_detection_api:
    :param image_api:
    :return: he image url that contain the best face

    using both face detection api and image loading api this use-case
    will gather all required data and then process it using best_face function
    """
    image_by_url, (faces, groups) = await asyncio.gather(
        gather_images(list_of_image_urls, image_api),
        group_faces(list_of_image_urls, face_detection_api))

    # at this point we gathered all images and faces and we can proceed
    # with creating the following mappings
    face_by_id = {face.id: face for face in faces}
    image_by_id = {face.id: image_by_url[face.url] for face in faces}
    best_face_id = best_face(face_by_id, image_by_id, groups)
    return face_by_id[best_face_id].url
