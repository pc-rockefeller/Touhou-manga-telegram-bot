import requests

headers = {

    'Host': 'mangalib.me',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:122.0) Gecko/20100101 Firefox/122.0',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate, br',
    'Content-Type': 'application/json;charset=utf-8',
    'Content-Length': '136',
    'Referer': 'https://mangalib.me/manga-list?sort=rate&dir=desc&page=1&name=touhou&site_id=1&type=manga&caution_list[]=%D0%9E%D1%82%D1%81%D1%83%D1%82%D1%81%D1%82%D0%B2%D1%83%D0%B5%D1%82&caution_list[]=16+&caution_list[]=18+',
    #'X-CSRF-TOKEN': 'k3Q0MuGqTSH6GPZEiqySqxcP0XOCEUa17ipQkD6D',
    'X-Requested-With': 'XMLHttpRequest',
    #'X-XSRF-TOKEN': 'eyJpdiI6InZTbTM4WjNaQzFoakU2OU9hYURmeGc9PSIsInZhbHVlIjoiWVp5UzNwbXIxL2VxWms0M0syOTVRSTZ2YUtTc005R0J4czFheVpaSzhNWUVPV0ZVWmlrZURsVzVGdWdzc0pUODFyeno1b2drNVpTOHlUcndYS3ZJRnZrWllJZVVTODB5aVZweFp6blEyQ0lDVTkvd2hKZkxsVHR2SFRYc3dDdEkiLCJtYWMiOiI0NDhmMWY2MGMzZDhmNWE4NTFhYTFkY2Q1Y2NhM2ZhNTJmMzdmMGIwNDEwMTFlZDEyYjcyMDkxN2IzYjhhMjhmIiwidGFnIjoiIn0=',
    'Origin': 'https://mangalib.me',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'Connection': 'keep-alive',
    #'Cookie': '_ga_SF8S8RTHBE=GS1.1.1708353780.4.0.1708353780.60.0.0; _ga=GA1.2.675048095.1708009756; _ym_uid=1708009758778382939; _ym_d=1708009758; XSRF-TOKEN=eyJpdiI6InZTbTM4WjNaQzFoakU2OU9hYURmeGc9PSIsInZhbHVlIjoiWVp5UzNwbXIxL2VxWms0M0syOTVRSTZ2YUtTc005R0J4czFheVpaSzhNWUVPV0ZVWmlrZURsVzVGdWdzc0pUODFyeno1b2drNVpTOHlUcndYS3ZJRnZrWllJZVVTODB5aVZweFp6blEyQ0lDVTkvd2hKZkxsVHR2SFRYc3dDdEkiLCJtYWMiOiI0NDhmMWY2MGMzZDhmNWE4NTFhYTFkY2Q1Y2NhM2ZhNTJmMzdmMGIwNDEwMTFlZDEyYjcyMDkxN2IzYjhhMjhmIiwidGFnIjoiIn0%3D; mangalib_session=eyJpdiI6ImtVaGJHV3Y4WmRIajNlUmROMGJOdEE9PSIsInZhbHVlIjoieStCYjJoSERkQmZDUXBiUWxPSTFzUTZHN0duSWJUQUpNWnN6NmR1cS84ZXY4R2N1ZTIrREozenFIQmprdmdLa0dLRVBFRlQxa0tHdkNRay9qcUJvbURuT01aN1dSd3hvREFyYlNkZjUvQTlteVB4Y2xEc0thTzdQU3I5RlNsZ3giLCJtYWMiOiJmMTUyNGU4OTU3YTY2MDJjOWJmZjhkMjAxMWMxMThkNmYwMTNlMzBiZWU5ZDAxZWVjYmJmNDM3NzI2NzVkM2VlIiwidGFnIjoiIn0%3D; _gid=GA1.2.1096974947.1708350722; _ym_isad=2',

}

data = {

    'caution_list': ['Отсутствует', '16+', '18+'],
    'dir': 'desc',
    'name': 'touhou',
    'page': 20,
    'site_id': '1',
    'sort': 'rate',
    'type': 'manga',

}

#response = requests.post('https://mangalib.me/manga-list?sort=rate&dir=desc&page=1&name=touhou&site_id=1&type=manga&caution_list', headers=headers)
##response = requests.get('https://mangalib.me/manga-list', cookies=cookies, headers=headers)

#response.encoding = response.apparent_encoding

response = requests.post('https://mangalib.me/api/list', headers=headers, json=data)


print(response.status_code)
print(response.json())
#print(response.content.decode('utf-8', 'replace'))
