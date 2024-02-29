#from base_parser import *
#from parser_exceptions import *
from socketserver import ThreadingMixIn
from parsers import base_parser
from parsers import parser_exceptions
import multiprocessing
import threading
import requests
from bs4 import BeautifulSoup

HEADERS_DICT = {

    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:122.0) Gecko/20100101 Firefox/122.0',

}

DATA_DICT = {

    'caution_list': ['Отсутствует', '16+', '18+'],
    'dir': 'desc',
    # 'name': 'touhou',
    # 'page': 10,
    'site_id': '1',
    'sort': 'rate',
    'type': 'manga',

}

ELEMENTS_PER_PAGE = 60

class MangalibParser(base_parser.BaseParser):
    def __init__(self):
        self.xsrf = None
        self.csrf = None
        self.cookies = None
        self.reestablishConnection()
    def reestablishConnection(self) -> None:
        headers = HEADERS_DICT.copy()

        response = requests.get('https://mangalib.me/manga-list', headers=headers)

        if not response.ok:
            raise parser_exceptions.ConnectionErrorException("Error establishing connection")
        
        soup = BeautifulSoup(response.text, 'lxml')

        # multiprocessing.Lock
        # threading.Thread()
        # ThreadingMixIn.lock

        # TODO maybe add Lock on these values
        self.xsrf = response.cookies['XSRF-TOKEN']
        self.csrf = soup.find('meta', {'name': '_token'})['content']
        self.cookies = response.cookies

    def getName() -> str:
        return "MangaLib"
    def binarySearchPage(self, elementName : str, leftPage : int, rightPage : int) -> int:
        headers = HEADERS_DICT.copy()
        headers['X-XSRF-TOKEN'] = self.xsrf
        headers['X-CSRF-TOKEN'] = self.csrf

        cookies = self.cookies

        data = DATA_DICT.copy()
        data['name'] = elementName

        while True:
            middlePage = (leftPage + rightPage) // 2
            data['page'] = middlePage
            response = requests.post('https://mangalib.me/api/list', headers=headers, cookies=cookies, json=data)
            if not response.ok:
                raise parser_exceptions.ConnectionErrorException("Error in POST request")
            responseJson = response.json()
            if responseJson.get('items') is None or 'to' not in responseJson['items'].keys():
                raise parser_exceptions.ConnectionErrorException("Error with recieving json in POST request")
            
            if leftPage == rightPage or leftPage + 1 == rightPage:
                return responseJson['items']['to']
            
            if responseJson['items']['to'] is not None:
                leftPage = middlePage
            else:
                rightPage = middlePage
        

    def findRightValueForBinarySearch(self, elementName : str,) -> int:
        """ Returns page number that is a valid right value """
        headers = HEADERS_DICT.copy()
        headers['X-XSRF-TOKEN'] = self.xsrf
        headers['X-CSRF-TOKEN'] = self.csrf

        cookies = self.cookies

        data = DATA_DICT.copy()
        data['name'] = elementName
        page = 10

        while True:
            data['page'] = page
            response = requests.post('https://mangalib.me/api/list', headers=headers, cookies=cookies, json=data)
            if not response.ok:
                raise parser_exceptions.ConnectionErrorException("Error in POST request")
            responseJson = response.json()
            if responseJson.get('items') is None or 'to' not in responseJson['items'].keys():
                raise parser_exceptions.ConnectionErrorException("Error with recieving json in POST request")
            if responseJson['items']['to'] is None:
                break
            page += 10
        return page

    def parseElementsCount(self, elementName : str) -> int:
        headers = HEADERS_DICT.copy()
        headers['X-XSRF-TOKEN'] = self.xsrf
        headers['X-CSRF-TOKEN'] = self.csrf

        cookies = self.cookies

        data = DATA_DICT.copy()
        data['name'] = elementName
        page = 1
        data['page'] = page

        response = requests.post('https://mangalib.me/api/list', headers=headers, cookies=cookies, json=data)
        if not response.ok:
            self.reestablishConnection()
            headers['X-XSRF-TOKEN'] = self.xsrf # TODO: maybe remove
            headers['X-CSRF-TOKEN'] = self.csrf
            cookies = self.cookies
        
        pastLastPage = self.findRightValueForBinarySearch(elementName)
        mangaCount = self.binarySearchPage(elementName, 0, pastLastPage)
        return mangaCount


    def parseElement(self, elementName : str, elementNumber : int) -> str:
        headers = HEADERS_DICT.copy()
        headers['X-XSRF-TOKEN'] = self.xsrf
        headers['X-CSRF-TOKEN'] = self.csrf

        cookies = self.cookies

        data = DATA_DICT.copy()
        data['name'] = elementName

        page = elementNumber // ELEMENTS_PER_PAGE
        elementIndex = elementNumber % ELEMENTS_PER_PAGE

        data['page'] = page
        response = requests.post('https://mangalib.me/api/list', headers=headers, cookies=cookies, json=data)
        if not response.ok:
            self.reestablishConnection()
            # TODO: this looks like trash
            headers['X-XSRF-TOKEN'] = self.xsrf # TODO: maybe remove
            headers['X-CSRF-TOKEN'] = self.csrf
            cookies = self.cookies
            response = requests.post('https://mangalib.me/api/list', headers=headers, cookies=cookies, json=data)
            if not response.ok:
                raise parser_exceptions.ConnectionErrorException("Error in POST request")
            
        responseJson = response.json()
        if responseJson.get('items') is None or 'data' not in responseJson['items'].keys():
            raise parser_exceptions.ConnectionErrorException("Error with recieving json in POST request")
        if elementIndex >= responseJson['items']['to']:
            raise parser_exceptions.BadRequestException("elementIndex is out of range")
        return responseJson['items']['data'][elementIndex]['href']
