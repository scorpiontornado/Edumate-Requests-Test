# Most current version of the code as of 19/05/2021 (before working on it)

# Order of requests:
  # Request 1: Get request to url1 - response contains Authstate parameter (generated each time)
  # Request 2: Post request to url2 - data: login details (username, password, Authstate), returns SAMLResponse
  # Request 3: Post request to url3 - data: SAMLRespone, sets PHPSESSID cookie
  # Request 4: Get request to url4 - response contains the timetable json, requires PHPSESSID cookie

import os

import requests
from bs4 import BeautifulSoup
import json
import html

import time # to test runtime

def get_timetable(session, url_stem, my_date):
  response = session.get(url_stem + my_date)

  timetable = []
    
  if response.status_code == 200:
    # Will also return 200 if login fails 
    # Check if login is successful
    #print (response.headers.get('content-type')) # always: text/plain; charset=UTF-8
    #print(response.content) # looks like json to me..
    try:
      timetable_json = response.json()


      timetable_data = json.dumps(timetable_json, indent=2) # makes it look pretty for printing, converts into a string

      #print(timetable_data)

      # Get class in each period:
      for i, event in enumerate(timetable_json["events"]):
        event_type = event["eventType"]
        activity_name = html.unescape(event["activityName"])
        if event_type == "class":
          period = html.unescape(event["period"])
          timetable.append(f"Period\t{period}: {activity_name}")
        else:
          # event_type == "activity", "event" etc
          display_time = html.unescape(event["displayTime"]) # probably not necessary
          timetable.append(f"\t{display_time}:\n\t\t{activity_name}")
    except ValueError:
      print("Login failed")
      timetable = -1
  else:
    timetable = ["Invalid date"]
  
  return timetable

def main():
  # the session automatically handles the cookies for me.
  with requests.Session() as s:
    print("Connecting to Edumate...")
    ### request 1
    # Get AuthState parameter (needed in order log in)
    
    url1 = "https://edumate.sacs.nsw.edu.au/sacs/web/app.php/sso-login/?return_path=dashboard%2Fmy-edumate%2F"
    
    r = s.get(url1) # requests automatically follows redirects to the login form. Response contains the "AuthState" parameter (needed for logging in - request 2)

    soup = BeautifulSoup(r.text, "html.parser")

    for input_tag in soup.find_all("input"):
      input_type = input_tag.attrs.get("type", "text")
      if input_type == "hidden":
        input_name = input_tag.attrs.get("name")
        input_value = input_tag.attrs.get("value")

        # Set necessary values for the login in request 2 - username, password, authstate
        # Will only prompt user for username and password if the environment variables are not set (replit secrets)
        # They will not be set for anyone who doesn't have edit privledges (e.g. anonymous user, someone forking)
        username = os.environ['username'] if 'username' in os.environ else input("Username: ")
        password = os.environ['password'] if 'password' in os.environ else input("Password: ")

        payload = {'username':username, 'password':password, input_name:input_value}
        
        break
    
    ### request 2
    # Log in

    url2 = "https://sacs-login.cloudworkengine.net/module.php/core/loginuserpass.php?"

    r2 = s.post(url2, data=payload)

    # Will return 200 if successful or not... maybe bc it redirects back to the login page.

    print("Login attempted...")

    soup2 = BeautifulSoup(r2.text, "html.parser")
    payload2 = {}

    for input_tag in soup2.find_all("input"):
      input_type = input_tag.attrs.get("type", "text")
      if input_type == "hidden":
        input_name = input_tag.attrs.get("name")
        input_value = input_tag.attrs.get("value")

        payload2[input_name] = input_value

    ### request 3
    # Get PHPSESSID cookie (needed to access timetable)
    url3 = "https://edumate.sacs.nsw.edu.au/sacs/web/app.php/saml/acs"

    r3 = s.post(url3, data=payload2)

    ### request 4
    # Get timetable json
    
    # example url: https://edumate.sacs.nsw.edu.au/sacs/web/app.php/admin/get-day-calendar/20210323

    url4_stem = "https://edumate.sacs.nsw.edu.au/sacs/web/app.php/admin/get-day-calendar/"

    timetable = get_timetable(s, url4_stem, "today")
    print("\nToday's timetable:", "\n".join(timetable), sep="\n")

    # return # for time testing

    my_date = input("\nDate (YYYYMMDD or today/tomorrow etc.): ")
    while my_date:
      timetable = get_timetable(s, url4_stem, my_date)

      if timetable == -1:
        break
      print("\n".join(timetable))

      my_date = input("\nDate (YYYYMMDD or today/tomorrow etc.): ")

#start_time = time.time()

main()

# print("--- %.2f seconds ---" % (time.time() - start_time)) # Fastest time to auto login, type today, quit program by pressing enter was: 11.26 seconds

# With auto today's timetable followed by return: 10.94 seconds

# Fastest time with Edumate with autofill password: 21.90 seconds. ~ 2 seconds slower without autofill on desktop.

# Therefore, my program is roughly 2x faster than using Edumate in a browser on a laptop