import json
import sqlite3
import urllib.request, urllib.parse, urllib.error
import facebook
import praw
import requests
import hiddeninfo
import sys


#Adam Benson
#Final Project
#Purpose: Using API's to collect interactions on "Big Data" across various platforms.
#Goals: visualize the data to gain insights 

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
CACHE_FNAME = "APIResearch_cache.json"

try:
    cache_file = open(CACHE_FNAME, 'r') # Try to read the data from the file
    cache_contents = cache_file.read()  # If it's there, get it into a string
    CACHE_DICTION = json.loads(cache_contents) # And then load it into a dictionary
    cache_file.close() # Close the file, we're good, we got the data in a dictionary.
except:
    CACHE_DICTION = {}

"""
###################################################################################
#API #1: Reddit
print("Welcome to the Reddit Analysis Portion of the project")
reddit = praw.Reddit(client_id = hiddeninfo.reddit_id,
                     client_secret = hiddeninfo.reddit_secret,
                     user_agent = 'APIResearch by /u/BobCruddles',
                     username = hiddeninfo.reddit_username,
                     password = hiddeninfo.reddit_password)
print(reddit.user.me()) #make sure you are accessing your account
subreddit = reddit.subreddit('bigdata')
print(subreddit.title)
for sub in subreddit.top(limit=10):
    if not sub.stickied:
        #print(sub.score)
        #print(sub.id)
        #print(sub.author)
        #aredditor = reddit.get_redditor(sub.author)
        #print(aredditor)
        #akarma = aredditor.link_karma
        #print(akarma)
        #ascore == sub.score
        #asubmission = sub.id
        #comments = sub.comments.replace_more(limit=0)


###################################################################################
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
    uprint(x['end_time']) #time of event in formation YYYY-MM-DD + Time
    try:                    # example 2017-12-19T14:30:00+0100 
        y = x['place']
        uprint(y['location']) #printing event location information if avaliable
    except:
        print("no location avaliable")
    detailz = graph.get_object(id=eventid, fields = 'attending_count, declined_count, interested_count')
    #print(type(detailz['attending_count']))  type = 'int'
    num_attending = detailz['attending_count']
    num_interested = detailz['interested_count']


###NEXT STEP = access event id to get specific event information
# Store in Database #attending and #interested



event1 = graph.get_object(id=eventid, fields='attending_count,can_guests_invite,category,cover,declined_count,description,end_time,guest_list_enabled,interested_count,is_canceled,is_page_owned,is_viewer_admin,maybe_count,noreply_count,owner,parent_group,place,ticket_uri,timezone,type,updated_time')
attenderscount = event1['attending_count']
declinerscount = event1['declined_count']
interestedcount = event1['interested_count']
maybecount = event1['maybe_count']
noreplycount = event1['noreply_count']
attenderscount = event1['attending_count']
attenders = requests.get("https://graph.facebook.com/v2.7/"+eventid+"/attending?access_token="+access_token+"&limit="+str(attenderscount)) 
attenders_json = attenders.json()
"""

#API #3: New York Times
print("Welcome to the New York Times Analysis Portion of the project")
params = {}

nyt_key = None
if nyt_key is None: #get token from fb user in order to run this script
    nyt_key = input("\nCopy and paste API Key from https://developer.nytimes.com/\n>  ")

for x in range(10):
    nytbase_url = "https://api.nytimes.com/svc/search/v2/articlesearch.json"
    params = {'api-key': nyt_key, 'q': 'big data',
               'fq' : "headline(\"Big Data\")",
               'fl': 'headline, keywords, pub_date, news_desk',
               'page': str(x)}

    nyt_api =  requests.get(nytbase_url, params = params)
    data = json.loads(nyt_api.text) #type = dictionary
                                    #items in data   #status, copyright, response

    print(data['response'])


#new = json.dumps(goodstuff, indent = 4)




#print(new)

