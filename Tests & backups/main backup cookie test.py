# This was copied from main on 06/04/2021, however it was likely written after the other two main backups, i.e. after 23/03/2021

import json

###

import requests

# cookies = {
#     'device_view': 'full',
#     '7d1be18e3ca53f3ee143a68d87f2a2ee': 'elpfhjq73t9i7gkj0ree911hec',
#     'e29cdba1dd8910420c6ce0b6544428a1': '6dqv6u8mi6nmcsjui06839usda',
#     'OldWikiSession': 'ec57995c03e6a60bef8aa61eeb7058fc',
#     'PHPSESSID': 'fmlmadt8d6uumh25vmjugd8pbi',
#     'ec57995c03e6a60bef8aa61eeb7058fc': 'vupfg63aerk995u1ete0fl8bn7',
#     'e713fd4a2803019219a03850291a2e5c': 'b2hw9p40Q8Jdvq^%^2FlCuOPOCRwN9CWlEIjgVFWbRRcHC3RY8GT65X01SetH4QLOupUjefnSQXJknBRsS1WpsQyHe0wqgy^%^2Bt7WyrKr0HaIZeRcc81vcEaBU^%^2Bh16Xc6LUwdiaPZTewVjQxhov3^%^2Fs4^%^2Fk7DzCoyTJX2ZjysBc^%^3D',
# }

cookies = {
  'PHPSESSID': 'fmlmadt8d6uumh25vmjugd8pbi',
}

# headers don't affect it
# all cookies except PHPSESSID don't affect it
# PHPSESSID is the only factor that influences it. If PHPSESSID is gone, it breaks. PHPSESSID appears to expire after a small amount of time

response = requests.get('https://edumate.sacs.nsw.edu.au/sacs/web/app.php/admin/get-day-calendar/20210323', cookies=cookies)

###
# print(response)
response_json = json.dumps(response.json(), indent=2)
print(response_json)
