from parsers import *

from random import randrange

import grpc

from concurrent.futures import ThreadPoolExecutor

from parsers_pb2 import MangaResponse
from parsers_pb2_grpc import ParsersServicer, add_ParsersServicer_to_server

class ParsersServer(ParsersServicer):
    def __init__(self) -> None:
        self.parsers = []
        globalObjs = list(globals().items())
        for name, obj in globalObjs:
            if obj is not BaseParser and isinstance(obj, type) and issubclass(obj, BaseParser):
                self.parsers.append(obj())

    def Parse(self, request, context):
        mangaName = request.mangaName
        mangaCounts = []
        mangaCountSum = 0
        for parser in self.parsers:
            mangaCounts.append(parser.parseElementsCount(mangaName))
        mangaCountSum = sum(mangaCounts)
        randomMangaIndex = randrange(mangaCountSum)

        parserIndex = 0
        for mangaCount in mangaCounts:
            if randomMangaIndex < mangaCount:
                mangaLink = self.parsers[parserIndex].parseElement(mangaName, randomMangaIndex)
                response = MangaResponse(mangaLink=mangaLink)
                return response
            parserIndex += 1
            randomMangaIndex -= mangaCount

if __name__ == '__main__':
    server = grpc.server(ThreadPoolExecutor())
    add_ParsersServicer_to_server(ParsersServer(), server)
    port = 9999
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    server.wait_for_termination()