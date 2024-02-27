#from base_parser import *
#from parser_exceptions import *
from parsers import base_parser
from parsers import parser_exceptions
import requests
from bs4 import BeautifulSoup

HEADERS_DICT = {

    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:122.0) Gecko/20100101 Firefox/122.0',

}

DATA_DICT = {

    'caution_list': ['Отсутствует', '16+', '18+'],
    'dir': 'desc',
    'name': 'touhou',
    # 'page': 10,
    'site_id': '1',
    'sort': 'rate',
    'type': 'manga',

}

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

        self.xsrf = response.cookies['XSRF-TOKEN']
        self.csrf = soup.find('meta', {'name': '_token'})['content']
        self.cookies = response.cookies

    def getName() -> str:
        return "MangaLib"
    def binarySearchPage(self, leftPage : int, rightPage : int) -> int:
        headers = HEADERS_DICT.copy()
        headers['X-XSRF-TOKEN'] = self.xsrf
        headers['X-CSRF-TOKEN'] = self.csrf

        data = DATA_DICT.copy()
        
        cookies = self.cookies

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
        

    def findRightValueForBinarySearch(self) -> int:
        """ Returns page number that is a valid right value """
        headers = HEADERS_DICT.copy()
        headers['X-XSRF-TOKEN'] = self.xsrf
        headers['X-CSRF-TOKEN'] = self.csrf

        data = DATA_DICT.copy()
        page = 10

        cookies = self.cookies

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

    def parseElementsCount(self) -> int:
        headers = HEADERS_DICT.copy()
        headers['X-XSRF-TOKEN'] = self.xsrf
        headers['X-CSRF-TOKEN'] = self.csrf

        data = DATA_DICT.copy()
        page = 1
        data['page'] = page

        cookies = self.cookies

        response = requests.post('https://mangalib.me/api/list', headers=headers, cookies=cookies, json=data)
        if not response.ok:
            self.reestablishConnection()
            headers['X-XSRF-TOKEN'] = self.xsrf # TODO: maybe remove
            headers['X-CSRF-TOKEN'] = self.csrf
        
        pastLastPage = self.findRightValueForBinarySearch()
        mangaCount = self.binarySearchPage(0, pastLastPage)
        return mangaCount


    def parseElement(self, elementNumber : int) -> str:
        # TODO: write
        pass