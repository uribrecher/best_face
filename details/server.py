from details import AzureFaceDetect, PillowImageLoader
from usecases import handle_best_face
from aiohttp import web
import logging
import argparse


class Handler:
    def __init__(self, args):
        self.face_detect = AzureFaceDetect(args.api_endpoint, args.api_key)
        self.image_loader = PillowImageLoader()

    async def handle_best_face(self, request):
        logging.info("start handling best face request-------------------------")

        if not request.can_read_body:
            logging.error('missing request body')
            raise web.HTTPBadRequest

        body = await request.json()
        # TODO: validate json structure, make sure we get a list of string
        # and that the string are well formatted urls
        list_of_urls = body

        result = await handle_best_face(list_of_urls, self.face_detect, self.image_loader)
        logging.info(result)
        return web.json_response(result)


def main():
    parser = argparse.ArgumentParser(description='best face service')
    parser.add_argument('--api_key', help='microsoft face recognition api key')
    parser.add_argument('--api_endpoint', help='microsoft face recognition endpoint')
    args = parser.parse_args()
    handler = Handler(args)
    logging.basicConfig(level=logging.INFO)
    app = web.Application()
    app.add_routes([web.get('/best_face', handler.handle_best_face)])
    web.run_app(app, port=80)


if __name__ == '__main__':
    main()
