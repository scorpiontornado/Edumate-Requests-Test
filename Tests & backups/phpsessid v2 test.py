# 26/03/21
# Used Burp Suite to find important requests + responses


# https://stackoverflow.com/questions/41350762/python-requests-logging-into-website-using-post-and-cookies

import requests


payload = {'username':input("Username: "), 'password':input("Password: "), 'AuthState':'_a08a1c3b2ca8afdf480ba5134d26bbde9a53dd973a%3Ahttps%3A%2F%2Fsacs-login.cloudworkengine.net%2Fsaml2%2Fidp%2FSSOService.php%3Fspentityid%3Dhttps%253A%252F%252Fedumate.sacs.nsw.edu.au%252Fsacs%252Fweb%252Fapp.php%26cookieTime%3D1616736959%26RelayState%3D%25257B%252522return_path%252522%25253A%252522dashboard%25255C%25252Fmy-edumate%25255C%25252F%252522%25257D'}

# Gives a 400 bad request response when just sending the username and password
# When navigating to the url, it says "Missing AuthState parameter"
# Leaving it blank ('Authstate':'') gives a 500 internal server error
# Giving it an expired one gives a 500 internal server error, html says “State information lost”… looks like I’ll need to request it myself.

url_login = 'https://sacs-login.cloudworkengine.net/module.php/core/loginuserpass.php?'

url_cookie = 'https://edumate.sacs.nsw.edu.au/sacs/web/app.php/saml/acs'
url_timetable = 'https://edumate.sacs.nsw.edu.au/sacs/web/app.php/admin/get-day-calendar/20210323'

with requests.Session() as s:
    r = s.post(url_login, data=payload)
    #cookie = {'PHPSESSID': requests.utils.dict_from_cookiejar(s.cookies)['PHPSESSID']}

    #print(cookie['PHPSESSID'])

    # for cookie in requests.utils.dict_from_cookiejar(s.cookies):
    #   print(cookie)

    print(r, r.text)