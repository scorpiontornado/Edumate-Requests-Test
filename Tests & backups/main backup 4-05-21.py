# Backup of main before random comments were removed. 4/05/2021

# Most current version of the code as of 31/03/2021 - 06/04/2021 // 16/04/2021
# Improved version of phpsessid\ final\ final.py

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

  ### request 4
  
  #r4 = s.get('https://edumate.sacs.nsw.edu.au/sacs/web/app.php/admin/get-day-calendar/20210323') # the requests session automatically sends the PHPSESSID cookie

  my_date = input("\nDate (YYYYMMDD or today/tomorrow etc.): ") 
  while my_date:
    url4 = "https://edumate.sacs.nsw.edu.au/sacs/web/app.php/admin/get-day-calendar/" + my_date

    r4 = s.get(url4)
    #print(r4, r4.text)
    
    if r4.status_code == 200:
      timetable_json = r4.json()
      # print(type(timetable_json)) # <class 'dict'>


      timetable_data = json.dumps(timetable_json, indent=2) # makes it look pretty for printing, converts into a string
      #print(timetable_data)

      # Get class in each period:
      for i, event in enumerate(timetable_json["events"]):
        #print(event)
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