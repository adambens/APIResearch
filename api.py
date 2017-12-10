import json
import urllib3
import facebook
import requests
import hiddeninfo.py as secrets 



#Adam Benson
#Final Project
#Purpose: Using API's to collect posts on "Big Data"


#API #1: Reddit


#API #2: Facebook
print("Welcome")
access_token = None
if access_token is None:
    access_token = input("\nCopy and paste token from https://developers.facebook.com/tools/explorer\n>  ")

graph = facebook.GraphAPI(access_token)
events = graph.request(‘/search?q=Big%20Data&type=event&limit=21’)
eventid = eventList[1][‘id’]

attenders = requests.get(“https://graph.facebook.com/v2.7/"+eventid+"/attending?access_token="+token+”&limit=”+str(attenderscount)) 
attenders_json = attenders.json()

#API #3: New York Times


