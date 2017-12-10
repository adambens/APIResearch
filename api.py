import json
import sqlite3
import urllib.request, urllib.parse, urllib.error
import facebook
import requests
import hiddeninfo
import sys


#Adam Benson
#Final Project
#Purpose: Using API's to collect interactions on "Big Data"
#across various platforms. 

######## PRINTING FUNCTION FOR CODEC ISSUES #########################################
def uprint(*objects, sep=' ', end='\n', file=sys.stdout):
    enc = file.encoding
    if enc == 'UTF-8':
        print(*objects, sep=sep, end=end, file=file)
    else:
        f = lambda obj: str(obj).encode(enc, errors='backslashreplace').decode(enc)
        print(*map(f, objects), sep=sep, end=end, file=file)
#####################################################################################

######## SET UP CACHING ################
########################################


#API #1: Reddit
print("Welcome to the Reddit Analysis Portion of the project")


#API #2: Facebook
print("Welcome to the Facebook Analysis Portion of the project")

access_token = None
if access_token is None: #get token from fb user in order to run this script
    access_token = input("\nCopy and paste token from https://developers.facebook.com/tools/explorer\n>  ")

graph = facebook.GraphAPI(access_token)
events = graph.request("/search?q=Big%20Data&type=event&limit=100") #matching fb events with the words 'Big Data'
eventslist = events['data']
uprint(eventslist)

for x in eventslist:
    eventid = x['id']  #event id = unique identifier to access more information on the event
    uprint(eventid)
    uprint(x['end_time'])
    try:
        y = x['place']
        uprint(y['location']) #printing event location information if avaliable
    except:
        print("no location avaliable")

###NEXT STEP = access event id to get specific event information
# Store in Database #attending and #interested


"""
event1 = graph.get_object(id=eventid, fields='attending_count,can_guests_invite,category,cover,declined_count,description,end_time,guest_list_enabled,interested_count,is_canceled,is_page_owned,is_viewer_admin,maybe_count,noreply_count,owner,parent_group,place,ticket_uri,timezone,type,updated_time')
attenderscount = event1['attending_count']
declinerscount = event1['declined_count']
interestedcount = event1['interested_count']
maybecount = event1['maybe_count']
noreplycount = event1['noreply_count']
attenderscount = event1['attending_count']
attenders = requests.get("https://graph.facebook.com/v2.7/"+eventid+"/attending?access_token="+access_token+"&limit="+str(attenderscount)) 
attenders_json = attenders.json()

#API #3: New York Times
print("Welcome to the New York Times Analysis Portion of the project")

"""