# Most current version of the code as of 19/05/2021

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

def get_events_date(session, url_stem, my_date):
  response = session.get(url_stem + my_date)
    
  if response.status_code == 200:
    # Will also return 200 if login fails 
    # Check if login is successful
    #print (response.headers.get('content-type')) # always: text/plain; charset=UTF-8
    #print(response.content) # looks like json to me..
    try:
      timetable_json = response.json()
      events = timetable_json["events"]
      if len(events) > 0:
        events = {
          "data": events,
          "status": 0
        }
      else:
        events = {
          "data": "No events for that day",
          "status": 2
        }

      #timetable_data = json.dumps(timetable_json, indent=2) # makes it look pretty for printing, converts into a string

      #print(timetable_data) # debugging
    except ValueError:
      events = {
        "data": "Login failed",
        "status": -1
        }
  else:
    events = {
      "data": "Invalid date",
      "status": 1
    }
  
  # timetable_json["status"]:
  # 0: ok
  # positive: problem, continue
  # negative: problem, terminate

  return events

def format_classes_date(events):
  timetable = {
    "data": [],
  }

  timetable["status"] = events["status"]

  if events["status"] == 0:
    for i, event in enumerate(events["data"]):
      event_type = event["eventType"]
      activity_name = html.unescape(event["activityName"])
      if event_type == "class":
        period = html.unescape(event["period"])
        timetable["data"].append(f"Period\t{period}: {activity_name}")
      else:
        # event_type == "activity", "event" etc
        display_time = html.unescape(event["displayTime"]) # probably not necessary
        timetable["data"].append(f"\t{display_time}:\n\t\t{activity_name}")
  else:
    timetable["data"] = events["data"] # Get the error message

  return timetable

def get_room_period(events):
  pass

def get_start_time(events):
  start_time = {
    "data": [],
  }

  start_time["status"] = events["status"]

  if events["status"] == 0:
    first_period = events["data"][0]
    start_date_time = html.unescape(first_period["startDateTime"]["date"]) # will output something like '2021-05-20 08:30:00.000000' (unescaping probably unecessary)
    start_time["data"] = start_date_time.split()[1][:8] # will get first 8 characters of start time
  else:
    start_time["data"] = events["data"] # Get the error message

  return start_time

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

    today_events = get_events_date(s, url4_stem, "today") # Get raw events for today

    start_time = get_start_time(today_events)
    timetable = format_classes_date(today_events)
    
    print("\nToday's start time:", start_time["data"], sep="\n")
    print("\nToday's timetable:", "\n".join(timetable["data"]), sep="\n")

    # return # for time testing

    my_date = input("\nDate (YYYYMMDD or today/tomorrow etc.): ")
    while my_date:
      date_events = get_events_date(s, url4_stem, my_date)
      timetable = format_classes_date(date_events)
      start_time = get_start_time(date_events)

      if timetable["status"] == 0:
        print(f"\nStart time for {my_date}:", start_time["data"], sep="\n")
        print(f"\nTimetable for {my_date}:", "\n".join(timetable["data"]), sep="\n")
      elif timetable["status"] < 0:
        print(timetable["data"])
        break
      else:
        print("\n" + timetable["data"])

      my_date = input("\nDate (YYYYMMDD or today/tomorrow etc.): ")

#start_time = time.time()

main()

# print("--- %.2f seconds ---" % (time.time() - start_time)) # Fastest time to auto login, type today, quit program by pressing enter was: 11.26 seconds

# With auto today's timetable followed by return: 10.94 seconds

# Fastest time with Edumate with autofill password: 21.90 seconds. ~ 2 seconds slower without autofill on desktop.

# Therefore, my program is roughly 2x faster than using Edumate in a browser on a laptop