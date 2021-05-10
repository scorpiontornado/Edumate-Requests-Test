# 31/03/2021
# Moved to main.py
import requests
from bs4 import BeautifulSoup
import json

# the session automatically handles the cookies for me.
# I was doing requests.get, not s.get
#https://stackoverflow.com/questions/21736970/using-requests-module-how-to-handle-set-cookie-in-request-response
with requests.Session() as s:
  ### request 1
  
  url1 = "https://edumate.sacs.nsw.edu.au/sacs/web/app.php/sso-login/?return_path=dashboard%2Fmy-edumate%2F"
  
  r = s.get(url1) # requests automatically redirects you to the login form. The response of the get request contains the "AuthState" parameter.

  #print(r, r.text, sep="\n")

  # Finding the authstate input in form, e.g.
  # <input type="hidden" name="AuthState" value="_1ce27c3da257ac39314e4f3ed9f3d8ef71b8076cc4:https://sacs-login.cloudworkengine.net/saml2/idp/SSOService.php?spentityid=https%3A%2F%2Fedumate.sacs.nsw.edu.au%2Fsacs%2Fweb%2Fapp.php&amp;cookieTime=1616913127&amp;RelayState=%257B%2522return_path%2522%253A%2522dashboard%255C%252Fmy-edumate%255C%252F%2522%257D" />

  soup = BeautifulSoup(r.text, "html.parser")

  for input_tag in soup.find_all("input"):
    # print(input_tag)
    input_type = input_tag.attrs.get("type", "text")
    if input_type == "hidden":
      #print("hi", input_tag)
      input_name = input_tag.attrs.get("name")
      input_value = input_tag.attrs.get("value")
      #print(input_name, input_value)

      payload = {'username':input("Username: "), 'password':input("Password: "), input_name:input_value}
      
      break
  
  ### request 2

  url2 = "https://sacs-login.cloudworkengine.net/module.php/core/loginuserpass.php?"

  r2 = s.post(url2, data=payload)
  # When not using the session, the response appears to just be the same as the get request to the login page rather than the long SAMLResponse I was hoping for
  # When using the session, it automatically passes the cookie set in the get request of the login form (SimpleSAMLSessionID) to the post request.

  # print(r2, r2.text, sep="\n")

  soup2 = BeautifulSoup(r2.text, "html.parser")
  payload2 = {}

  for input_tag in soup2.find_all("input"):
    #print(input_tag)
    input_type = input_tag.attrs.get("type", "text")
    if input_type == "hidden":
      # the input we are after is: <input name="SAMLResponse" type="hidden" value="PHNhbW...
      # as well as <input name="RelayState" type="hidden" value="%7B%22return_path%22%3A%22dashboard%5C%2Fmy-edumate%5C%2F%22%7D"/>
      # Without the relaystate it doesn't send you to the right place with the PHPSESSID
      # Luckily, both of their types are "hidden" and the other input, the first one, is type "submit".
      #print("hi", input_tag)
      input_name = input_tag.attrs.get("name")
      input_value = input_tag.attrs.get("value")
      # print(input_name, input_value)

      payload2[input_name] = input_value

  #print(payload2)

  ### request 3
  url3 = "https://edumate.sacs.nsw.edu.au/sacs/web/app.php/saml/acs"

  r3 = s.post(url3, data=payload2) # get PHPSESSID cookie

  #print(r3, r3.text, sep="\n")

  r4 = s.get('https://edumate.sacs.nsw.edu.au/sacs/web/app.php/admin/get-day-calendar/20210323') # the requests session automatically sends the PHPSESSID cookie

  # print(r4, r4.text)

  timetable_json = json.dumps(r4.json(), indent=2)
  print(timetable_json)