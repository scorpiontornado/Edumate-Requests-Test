import requests
from bs4 import BeautifulSoup

with requests.Session() as s:
  ### request 1
  
  url1 = "https://edumate.sacs.nsw.edu.au/sacs/web/app.php/sso-login/?return_path=dashboard%2Fmy-edumate%2F"
  
  r = requests.get(url1) # requests automatically redirects you to the login form. The response of the get request contains the "AuthState" parameter.

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

  r2 = requests.post(url2, data=payload) # response appears to just be the same as the get request to the login page rather than the long SAMLResponse I was hoping for

  print(r2, r2.text, sep="\n")