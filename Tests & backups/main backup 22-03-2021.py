# http://www.gregreda.com/2015/02/15/web-scraping-finding-the-api/
# https://stackoverflow.com/questions/42115727/how-to-programmatically-replicate-a-request-found-in-chrome-developer-tools
# https://curl.trillworks.com/

import json

###

import requests

cookies = {
    'device_view': 'full',
    '32384176ddb381a7301e65646794b407': 'u21mtbvsnsarfbvrufn68uf2lj',
    'bf792387386e8338b37ab8570901f323': '95ddvpodk1thsqsqffftnhmefq',
    'd28a4bc8e90fc1343245c6021c971030': 'l94epn1ep3sri5d8nc15r7vilb',
    '7c5578f2c8f37e3415299b9ed5416109': 'b73t0aqqdbrsubmivoatbeeppt',
    '85a22f38fdfda23a1ede4016c552f3de': '9uuhbd11d8ip6ih12n2g5hoi1a',
    'd21b3f95be4741c85b688d8593aab895': 'e8feo9dnber6i2kb1sqb4em80a',
    '8b77966037aafee0e6ba8244c92b1768': 'fr8drlvkkdalvpua9chfjgfv3i',
    'e713fd4a2803019219a03850291a2e5c': 'LRRLjnUmfiKkpjxDzahUGCRwN9CWlEIjgVFWbRRcHC3RY8GT65X01SetH4QLOupUjefnSQXJknBRsS1WpsQyHe0wqgy^%^2Bt7WyrKr0HaIZeRcc81vcEaBU^%^2Bh16X8^%^2BLWwdiaPZTewVjQxhov3^%^2Fs4^%^2Fk7DzCozzJS1JTysBc^%^3D',
    'OldWikiSession': 'f68d5e218385eb2346803caab4a7c54c',
    'PHPSESSID': 'orvqde0kd2ln04mh6h63k844ql',
}

headers = {
    'Connection': 'keep-alive',
    'sec-ch-ua': '^\\^Google',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua-mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
    'Accept': '*/*',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://edumate.sacs.nsw.edu.au/sacs/web/app.php/dashboard/my-edumate/?eduId=3481862',
    'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
}

params = (
    ('_dc', '1616401337397'),
    ('page', '1'),
    ('start', '0'),
    ('limit', '25'),
)

response = requests.get('https://edumate.sacs.nsw.edu.au/sacs/web/app.php/admin/get-day-calendar/today/current', headers=headers, params=params, cookies=cookies)

#NB. Original query string below. It seems impossible to parse and
#reproduce query strings 100% accurately so the one below is given
#in case the reproduced version is not "correct".
# response = requests.get('https://edumate.sacs.nsw.edu.au/sacs/web/app.php/admin/get-day-calendar/today/current?_dc=1616401337397&page=1&start=0&limit=25', headers=headers, cookies=cookies)

###
print(response)
# response_json = json.dumps(response.json(), indent=2)
# print(response_json)
