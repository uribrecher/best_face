import unittest
from entities import best_face, Face, Image


class BestFaceTests(unittest.TestCase):
    def test_empty(self):
        faces = {}
        images = {}
        groups = {}
        with self.assertRaises(ValueError):
            best_face(faces, images, groups)

    def test_single(self):
        faces = {
            'face1': Face(id='face1', width=10, height=10, url='url1'),
        }
        images = {
            'face1': Image(url='url1', width=100, height=100),
        }
        groups = [['face1']]
        self.assertEqual('face1', best_face(faces, images, groups))

    def test_simple(self):
        faces = {
            'face1': Face(id='face1', width=10, height=10, url='url1'),
            'face2': Face(id='face2', width=30, height=20, url='url2'),
            'face3': Face(id='face3', width=100, height=100, url='url3'),
        }
        images = {
            'face1': Image(url='url1', width=100, height=100),
            'face2': Image(url='url2', width=40, height=50),
            'face3': Image(url='url3', width=2048, height=1024)
        }
        groups = [['face1', 'face2'], ['face3']]
        self.assertEqual('face2', best_face(faces, images, groups))


    # TODO: add more test cases
