import json

###

import requests

cookies = {
    'device_view': 'full',
    '7d1be18e3ca53f3ee143a68d87f2a2ee': 'elpfhjq73t9i7gkj0ree911hec',
    'e29cdba1dd8910420c6ce0b6544428a1': '6dqv6u8mi6nmcsjui06839usda',
    'OldWikiSession': 'ec57995c03e6a60bef8aa61eeb7058fc',
    'PHPSESSID': 'fmlmadt8d6uumh25vmjugd8pbi',
    'ec57995c03e6a60bef8aa61eeb7058fc': 'vupfg63aerk995u1ete0fl8bn7',
    'e713fd4a2803019219a03850291a2e5c': 'b2hw9p40Q8Jdvq^%^2FlCuOPOCRwN9CWlEIjgVFWbRRcHC3RY8GT65X01SetH4QLOupUjefnSQXJknBRsS1WpsQyHe0wqgy^%^2Bt7WyrKr0HaIZeRcc81vcEaBU^%^2Bh16Xc6LUwdiaPZTewVjQxhov3^%^2Fs4^%^2Fk7DzCoyTJX2ZjysBc^%^3D',
}

headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'sec-ch-ua': '^\\^Google',
    'sec-ch-ua-mobile': '?0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'document',
    'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
}

response = requests.get('https://edumate.sacs.nsw.edu.au/sacs/web/app.php/admin/get-day-calendar/20210323', headers=headers, cookies=cookies)

###
# print(response)
response_json = json.dumps(response.json(), indent=2)
print(response_json)
