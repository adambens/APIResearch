import json
import sqlite3
import urllib.request, urllib.parse, urllib.error
import facebook
import praw
import requests
import hiddeninfo
import sys
import datetime

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
FB_CACHE = "fbAPIResearch_cache.json"
REDDIT_CACHE = "redditAPIResearch_cache.json"
NYT_CACHE = "nytAPIResearch_cache.json"
###################################################################################
try:
    reddit_cache_file = open(REDDIT_CACHE, 'r') # Try to read the data from the file
    reddit_cache_contents = reddit_cache_file.read()  # If it's there, get it into a string
    reddit_cache_file.close() # Close the file, we're good, we got the data in a string.
    REDDIT_CACHE_DICTION = json.loads(reddit_cache_contents) # And then load it into a dictionary
except:
    REDDIT_CACHE_DICTION = {}

try:
    fb_cache_file = open(FB_CACHE, 'r') # Try to read the data from the file
    fb_cache_contents = fb_cache_file.read()  # If it's there, get it into a string
    fb_cache_file.close() # Close the file, we're good, we got the data in a string.
    FB_CACHE_DICTION = json.loads(fb_cache_contents) # And then load it into a dictionary
except:
    FB_CACHE_DICTION = {}

try:
    nyt_cache_file = open(NYT_CACHE, 'r') # Try to read the data from the file
    nyt_cache_contents = nyt_cache_file.read()  # If it's there, get it into a string
    nyt_cache_file.close() # Close the file, we're good, we got the data in a string.
    NYT_CACHE_DICTION = json.loads(nyt_cache_contents) # And then load it into a dictionary
except:
    NYT_CACHE_DICTION = {}
###################################################################################
###################################################################################
#API #1: Reddit
print("Welcome to the Reddit Analysis Portion of the project")

reddit = praw.Reddit(client_id = hiddeninfo.reddit_id,
                     client_secret = hiddeninfo.reddit_secret,
                     user_agent = 'APIResearch by /u/BobCruddles',
                     username = hiddeninfo.reddit_username,
                     password = hiddeninfo.reddit_password)

print(reddit.user.me()) #make sure you are accessing correct account

def get_subreddit_submissions(subred):
    if subred in REDDIT_CACHE_DICTION:
        print("cached")
        response = REDDIT_CACHE_DICTION[subred]
    else:
        print("making new request")
        response = reddit.subreddit(subred)
        REDDIT_CACHE_DICTION[subred] = response
        x = str(REDDIT_CACHE_DICTION)
        reddit_cache_file = open(REDDIT_CACHE, 'w')
        reddit_cache_file.write(x)
        reddit_cache_file.close()
    return response


subreddit = get_subreddit_submissions('bigdata') #big data subreddit
print("subreddit title: ", subreddit.title)
print(type(subreddit))
count = 0
for sub in subreddit.top(limit=100): #for submission in top 100 submissions in subreddit
    if not sub.stickied:
        count += 1
        print('submission score: ', sub.score) #score = likes - dislikes
        #print(sub.id)
        print('submission author: ', sub.author) #author = username
        #print(type(sub.author))
        y = str(sub.author)
        #print(y)
        aredditor = reddit.redditor(y)
        try:
            uprint(aredditor.link_karma)
        except:
            print("No Karma")
        #akarma = aredditor.link_karma
        #print(akarma)
        #ascore == sub.score
        #asubmission = sub.id
        #comments = sub.comments.replace_more(limit=0)
#print(count)

###################################################################################
#API #2: Facebook
print("Welcome to the Facebook Analysis Portion of the project")

access_token = None
if access_token is None: #get token from fb user in order to run this script
    access_token = input("\nCopy and paste token from https://developers.facebook.com/tools/explorer\n>  ")
graph = facebook.GraphAPI(access_token)

def get_fb_events(topic):
    if topic in FB_CACHE_DICTION:
        print("cached")
        events = FB_CACHE_DICTION[topic]
    else:
        print("making new request")
        params = { 'q': topic, 'type': 'Event', 'limit': '100'}
        events = graph.request("/search?", params) #matching fb events with the words 'Big Data' in this project
        FB_CACHE_DICTION[topic] = events
        x = json.dumps(FB_CACHE_DICTION)
        fb_cache_file = open(FB_CACHE, 'w')
        fb_cache_file.write(x)
        fb_cache_file.close()
    return events

t = input('enter topic: ')
eventsl = get_fb_events(t)
#eventsl = get_fb_events("Big Data")
eventslist = eventsl['data']
#uprint(eventslist)

for x in eventslist:
    eventid = x['id'] #event id = unique identifier to access more information on the event
    uprint(eventid)
    try:
        uprint('end time: ', x['end_time']) #time of event in formation YYYY-MM-DD + Time
    except:
        print("No Time Specified")
    try:                    # example 2017-12-19T14:30:00+0100 
        y = x['place']
        uprint('location: ', y['location']) #printing event location information if avaliable
    except:
        print("no location avaliable")
    detailz = graph.get_object(id=eventid, fields = 'attending_count, declined_count, interested_count')
    #print(type(detailz['attending_count']))  type = 'int'
    num_attending = detailz['attending_count']
    num_interested = detailz['interested_count']
    print('attending: ', num_attending)
    print('interested: ', num_interested, '\n')

"""
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


#API #3: New York Times

print("Welcome to the New York Times Analysis Portion of the project")

nytbase_url = "https://api.nytimes.com/svc/search/v2/articlesearch.json"
params = {}
nyt_key = None
if nyt_key is None: #get token from nyt user in order to run this script
    nyt_key = input("\nCopy and paste API Key from https://developer.nytimes.com/\n>  ")



def get_nyt_articles(subject):

    if subject in NYT_CACHE_DICTION:
        print("Cached")
        nyt_api = NYT_CACHE_DICTION[subject]
    else:
        print("Making new request")
        params = {'api-key': nyt_key, 'q': subject,
               'fq' : "headline(\"Big Data\")",
               'fl': 'headline, keywords, pub_date, news_desk'}
               #'page': str(x)}
        nyt_api =  requests.get(nytbase_url, params = params)
        NYT_CACHE_DICTION[subject] = nyt_api
        x = NYT_CACHE_DICTION
        nyt_cache_file = open(NYT_CACHE, 'w')
        nyt_cache_file.write(str(x))
        nyt_cache_file.close()
    return nyt_api


articles = get_nyt_articles('big data')
data_articles = json.loads(articles.text)
#s = json.dumps(data_articles, indent = 4)
#print(s)
#print(len(data_articles['response']))
#print(len(data_articles['response']['docs']))
subject_articles = data_articles['response']['docs']

keywords_dict = {}
for item in subject_articles:
    headline = item["headline"]["main"]
    print(headline)
    publication_date = item.get("pub_date", "Date Unavaliable")
    print(publication_date)
    news_section = item.get("new_desk", "Section Unavaliable")
    print(news_section)
    keywords_list = item["keywords"]
    if len(keywords_list) != 0:
        for piece in keywords_list:
            words = piece['value']
            keywords_dict[words] = keywords_dict.get(words, 0) + 1

print(keywords_dict)


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
###########################################################
    graph = facebook.GraphAPI(access_token)
    params = {'q': 'Big Data', 'type': 'Event', 'limit': '100'} 
    events = graph.request("/search?", params) #matching fb events with the words 'Big Data'
    eventslist = events['data']
    uprint(eventslist)
"""