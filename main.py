# Most current version of the code as of 4/05/2021

# Order of requests:
  # Request 1: Get request to url1 - response contains Authstate parameter (generated each time)
  # Request 2: Post request to url2 - data: login details (username, password, Authstate), returns SAMLResponse
  # Request 3: Post request to url3 - data: SAMLRespone, sets PHPSESSID cookie
  # Request 4: Get request to url4 - response contains the timetable json, requires PHPSESSID cookie

import requests
from bs4 import BeautifulSoup
import json

# the session automatically handles the cookies for me.
with requests.Session() as s:
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
      payload = {'username':input("Username: "), 'password':input("Password: "), input_name:input_value}
      
      break
  
  ### request 2
  # Log in

  url2 = "https://sacs-login.cloudworkengine.net/module.php/core/loginuserpass.php?"

  r2 = s.post(url2, data=payload)

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

  my_date = input("\nDate (YYYYMMDD or today/tomorrow etc.): ") 
  while my_date:
    url4 = "https://edumate.sacs.nsw.edu.au/sacs/web/app.php/admin/get-day-calendar/" + my_date

    r4 = s.get(url4)
    
    if r4.status_code == 200:
      timetable_json = r4.json()


      timetable_data = json.dumps(timetable_json, indent=2) # makes it look pretty for printing, converts into a string

      # Get class in each period:
      for i, event in enumerate(timetable_json["events"]):
        event_type = event["eventType"]
        activity_name = event["activityName"]
        if event_type == "class":
          period = event["period"]
          print(f"Period\t{period}: {activity_name}")
        elif event_type == "event":
          # could also do event["displayTime"] (this is in both events and classes)
          print(f"\t{activity_name}")
        

    else:
      print("Invalid date")
    
    my_date = input("\nDate (YYYYMMDD or today/tomorrow etc.): ")


# Example response:

''' timetable_data:

{
  "label": "Tue, 20<sup>th</sup> Apr 2021",
  "SQLDate": "2021-04-20",
  "events": [
    {
      "eventType": "class",
      "startDateTime": {
        "date": "2021-04-20 07:30:00.000000",
        "timezone_type": 3,
        "timezone": "Australia/SYDNEY"
      },
      "endDateTime": {
        "date": "2021-04-20 08:29:00.000000",
        "timezone_type": 3,
        "timezone": "Australia/SYDNEY"
      },
      "activityName": "CM Wind Symphony (Chapter House)",
      "displayTime": "Period 0 (07:30 am)",
      "period": "0",
      "strCount": 16,
      "room": " (Chapter House)",
      "time": "07:30",
      "subMenuDataURL": "show",
      "links": [
        {
          "text": "<div style=\"font-size: 13px; font-weight: bold;\">Email Teacher</div>",
          "href": "mailto:?subject=RE:CM Wind Symphony&bcc=cwatson@sacs.nsw.edu.au",
          "xtype": "edutoolbarcalendarbuttonmenuitem"
        }
      ]
    },
    {
      "eventType": "class",
      "startDateTime": {
        "date": "2021-04-20 08:30:00.000000",
        "timezone_type": 3,
        "timezone": "Australia/SYDNEY"
      },
      "endDateTime": {
        "date": "2021-04-20 09:29:00.000000",
        "timezone_type": 3,
        "timezone": "Australia/SYDNEY"
      },
      "activityName": "11IB Language and Literature HL 1 (Room B304)",
      "displayTime": "Period 1 (08:30 am)",
      "period": "1",
      "strCount": 33,
      "room": " (Room B304)",
      "time": "08:30",
      "subMenuDataURL": "show",
      "links": [
        {
          "text": "<div style=\"font-size: 13px; font-weight: bold;\">Email Teacher</div>",
          "href": "mailto:?subject=RE:11IB Language and Literature HL 1&bcc=ngoodman@sacs.nsw.edu.au",
          "xtype": "edutoolbarcalendarbuttonmenuitem"
        }
      ]
    },
    {
      "eventType": "class",
      "startDateTime": {
        "date": "2021-04-20 09:35:00.000000",
        "timezone_type": 3,
        "timezone": "Australia/SYDNEY"
      },
      "endDateTime": {
        "date": "2021-04-20 10:34:00.000000",
        "timezone_type": 3,
        "timezone": "Australia/SYDNEY"
      },
      "activityName": "11IB Business Management SL 1 (Room B205)",
      "displayTime": "Period 2 (09:35 am)",
      "period": "2",
      "strCount": 29,
      "room": " (Room B205)",
      "time": "09:35",
      "subMenuDataURL": "show",
      "links": [
        {
          "text": "<div style=\"font-size: 13px; font-weight: bold;\">Email Teacher</div>",
          "href": "mailto:?subject=RE:11IB Business Management SL 1&bcc=alarkin@sacs.nsw.edu.au",
          "xtype": "edutoolbarcalendarbuttonmenuitem"
        }
      ]
    },
    {
      "eventType": "class",
      "startDateTime": {
        "date": "2021-04-20 10:55:00.000000",
        "timezone_type": 3,
        "timezone": "Australia/SYDNEY"
      },
      "endDateTime": {
        "date": "2021-04-20 11:54:00.000000",
        "timezone_type": 3,
        "timezone": "Australia/SYDNEY"
      },
      "activityName": "11IB Physics HL 1 (Room B401)",
      "displayTime": "Period 3 (10:55 am)",
      "period": "3",
      "strCount": 17,
      "room": " (Room B401)",
      "time": "10:55",
      "subMenuDataURL": "show",
      "links": [
        {
          "text": "<div style=\"font-size: 13px; font-weight: bold;\">Email Teacher</div>",
          "href": "mailto:?subject=RE:11IB Physics HL 1&bcc=sfoster@sacs.nsw.edu.au",
          "xtype": "edutoolbarcalendarbuttonmenuitem"
        }
      ]
    },
    {
      "eventType": "class",
      "startDateTime": {
        "date": "2021-04-20 12:00:00.000000",
        "timezone_type": 3,
        "timezone": "Australia/SYDNEY"
      },
      "endDateTime": {
        "date": "2021-04-20 12:29:00.000000",
        "timezone_type": 3,
        "timezone": "Australia/SYDNEY"
      },
      "activityName": "11 Tutorial WE (Room B302)",
      "displayTime": "Period T (12:00 pm)",
      "period": "T",
      "strCount": 14,
      "room": " (Room B302)",
      "time": "12:00",
      "subMenuDataURL": "show",
      "links": [
        {
          "text": "<div style=\"font-size: 13px; font-weight: bold;\">Email Teacher</div>",
          "href": "mailto:?subject=RE:11 Tutorial WE&bcc=asharman@sacs.nsw.edu.au",
          "xtype": "edutoolbarcalendarbuttonmenuitem"
        }
      ]
    },
    {
      "eventType": "class",
      "startDateTime": {
        "date": "2021-04-20 13:10:00.000000",
        "timezone_type": 3,
        "timezone": "Australia/SYDNEY"
      },
      "endDateTime": {
        "date": "2021-04-20 14:09:00.000000",
        "timezone_type": 3,
        "timezone": "Australia/SYDNEY"
      },
      "activityName": "11IB Theory of Knowledge 1 (Room B208)",
      "displayTime": "Period 4 (01:10 pm)",
      "period": "4",
      "strCount": 26,
      "room": " (Room B208)",
      "time": "13:10",
      "subMenuDataURL": "show",
      "links": [
        {
          "text": "<div style=\"font-size: 13px; font-weight: bold;\">Email Teacher</div>",
          "href": "mailto:?subject=RE:11IB Theory of Knowledge 1&bcc=jhall@sacs.nsw.edu.au",
          "xtype": "edutoolbarcalendarbuttonmenuitem"
        }
      ]
    },
    {
      "eventType": "class",
      "startDateTime": {
        "date": "2021-04-20 14:15:00.000000",
        "timezone_type": 3,
        "timezone": "Australia/SYDNEY"
      },
      "endDateTime": {
        "date": "2021-04-20 15:14:00.000000",
        "timezone_type": 3,
        "timezone": "Australia/SYDNEY"
      },
      "activityName": "11IB Computer Science HL 1 (B125 Computer Room)",
      "displayTime": "Period 5 (02:15 pm)",
      "period": "5",
      "strCount": 26,
      "room": " (B125 Computer Room)",
      "time": "14:15",
      "subMenuDataURL": "show",
      "links": [
        {
          "text": "<div style=\"font-size: 13px; font-weight: bold;\">Email Teacher</div>",
          "href": "mailto:?subject=RE:11IB Computer Science HL 1&bcc=mthill@sacs.nsw.edu.au",
          "xtype": "edutoolbarcalendarbuttonmenuitem"
        }
      ]
    }
  ]
}

'''

'''
{'eventType': 'class', 'startDateTime': {'date': '2021-04-21 12:00:00.000000', 'timezone_type': 3, 'timezone': 'Australia/SYDNEY'}, 'endDateTime': {'date': '2021-04-21 12:29:00.000000', 'timezone_type': 3, 'timezone': 'Australia/SYDNEY'}, 'activityName': '11 Tutorial WE (Room B302)', 'displayTime': 'Period T (12:00 pm)', 'period': 'T', 'strCount': 14, 'room': ' (Room B302)', 'time': '12:00', 'subMenuDataURL': 'show', 'links': [{'text': '<div style="font-size: 13px; font-weight: bold;">Email Teacher</div>', 'href': 'mailto:?subject=RE:11 Tutorial WE&bcc=asharman@sacs.nsw.edu.au', 'xtype': 'edutoolbarcalendarbuttonmenuitem'}]}
Period T: 11 Tutorial WE (Room B302)
{'eventType': 'event', 'startDateTime': {'date': '2021-04-21 12:00:00.000000', 'timezone_type': 3, 'timezone': 'Australia/SYDNEY'}, 'endDateTime': {'date': '2021-04-21 12:29:00.000000', 'timezone_type': 3, 'timezone': 'Australia/SYDNEY'}, 'activityName': 'Event: Yr 7 Westminster Peer Support Program (S436)', 'displayTime': '12:00 pm - 12:29 pm', 'strCount': 44, 'room': ' (S436)', 'time': '12:00', 'subMenuDataURL': 'show', 'links': [{'text': '<div style="font-size: 13px; font-weight: bold;">Details</div>', 'xtype': 'edutoolbarnewbuttonmenuitemeventdetail', 'eventId': 50498}]}
'''