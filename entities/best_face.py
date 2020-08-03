from .image_api import Image
from typing import List, Mapping
from dataclasses import dataclass
from functools import partial


@dataclass
class Face:
    id: str
    width: int
    height: int
    url: str


def face_area_percent(image: Image, face: Face) -> float:
    return (face.width * face.height) / (image.width * image.height)


def face_area_by_id(faces: Mapping[str, Face], images: Mapping[str, Image], face_id: str) -> float:
    image = images[face_id]
    face = faces[face_id]
    return face_area_percent(image, face)


def best_face(faces: Mapping[str, Face], images: Mapping[str, Image], groups: List[List[str]]) -> str:
    """
    :param faces: face_id->face mapping
    :param images: face_id->image mapping
    :param groups: groups of faces that are detected to be similar
    :return: pick the best face which is the one that is most common and takes up the largest
             portion within an image
    """
    if len(faces) == 0:
        raise ValueError("no faces provided")
    if len(images) == 0:
        raise ValueError("no images provided")
    if len(groups) == 0:
        raise ValueError("no groups provided")

    # first we pick the largest group of face-ids (the most common person)
    largest_group = sorted(groups, key=len, reverse=True)[0]
    if len(largest_group) == 0:
        raise ValueError("all face groups are empty")

    # then we sort that group based on face area within the image
    sorted_by_area = sorted(largest_group, key=partial(face_area_by_id, faces, images), reverse=True)

    # the first item is the one with the largest area, note that we return the face id
    return sorted_by_area[0]
