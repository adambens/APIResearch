import json
import pandas as pd #for Reddit Visualization
import plotly #for Reddit Visualization
import plotly.plotly as py
import plotly.graph_objs as go 
from mpl_toolkits.basemap import Basemap #Visualization, importing map (using Miller Project world map)
import numpy as np #Visualization
import matplotlib.pyplot as plt #Visualization
from wordcloud import WordCloud #World Cloud Visualization
import urllib.request, urllib.parse, urllib.error
import facebook
import praw #Reddit python wrapper
import requests
import hiddeninfo
import sys
import datetime
import time #for NYT rate-limit
import re 
import sqlite3
#Adam Benson
#Final Project
#Purpose: Using 3 API's, Reddit, Facebook, and New York Times to collect interactions on various platforms.
#Goals: Visualize the data to gain insights 
#####################################################################################
#CREATING BASE MAP FOR FB VISUALIZATION#

wmap = Basemap(projection='mill',llcrnrlat=-90,urcrnrlat=90,\
            llcrnrlon=-180,urcrnrlon=180,resolution='c')
# resolution set to crude
# lat/lon values *llcrnrlat = lower left corner lat, set up values for lower left and upper right corners
wmap.drawcoastlines() #draws coastlines
#wmap.drawcountries() #draws countries
wmap.drawcountries(color='beige')
wmap.fillcontinents(lake_color='cyan')
wmap.drawmapboundary(fill_color='cyan')

plotly.tools.set_credentials_file(username='adambens', api_key = 'HlNmUvXljCgx9vTiKigd')


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
#This portion requires that a USER has a Reddit account
#User must generate client information via Reddit account
#Enter user information when prompted to
#This function will retrieve up to 100 of the top, non-stickied, submissions of the specified subreddit
#I was interested in 'bigdata', but wrote this function to match any existing subreddit

print("Welcome to the Reddit Analysis Portion of the project")
name = input('Enter Reddit Username: ')

##Set Up Reddit Instance with user information
if name == 'BobCruddles':  #Using personal information for my account
    reddit = praw.Reddit(client_id = hiddeninfo.reddit_id,
                         client_secret = hiddeninfo.reddit_secret,
                         user_agent = 'APIResearch by /u/BobCruddles',
                         username = hiddeninfo.reddit_username,
                         password = hiddeninfo.reddit_password)
else:
    outside_id = input('Enter Reddit client_id: ')
    outside_secret = input('Enter Reddit client_secret: ')
    outside_agent = input('Enter Reddit user_agent: ')
    outside_name = name
    outside_password = input('Enter Reddit password: ')
    reddit = praw.Reddit(client_id = outside_id,
                         client_secret = outside_secret,
                         user_agent = outside_agent,
                         username = outside_name,
                         password = outside_password)


print('Accessing User: ', reddit.user.me()) #make sure you are accessing correct account

def get_subreddit_submissions(subred): #retrieve submissions for subreddit
    if subred in REDDIT_CACHE_DICTION:
        print("Data Was Cached")
        return REDDIT_CACHE_DICTION[subred]
        
    else:
        print("Making New Request")
        response = reddit.subreddit(subred)
        x = response.top(limit=100) 
        REDDIT_CACHE_DICTION[subred] = x
        reddit_cache_file = open(REDDIT_CACHE, 'w')
        reddit_cache_file.write(str(REDDIT_CACHE_DICTION))
        reddit_cache_file.close()
        return REDDIT_CACHE_DICTION[subred]

redditinput = input("Enter subreddit 'ex)bigdata' : ")
subreddit = get_subreddit_submissions(redditinput) #big data subreddit
#print("subreddit title: ", subreddit.title)
#print(type(subreddit)) #type = praw_object
count = 0

###################################################################################
#CREATING REDDIT DB

conn = sqlite3.connect('Reddit_APIandDB.sqlite')
cur = conn.cursor()
cur.execute('DROP TABLE IF EXISTS Submissions')
cur.execute('CREATE TABLE Submissions (subid TEXT PRIMARY KEY, title TEXT, score INTEGER, comments INTEGER, creation_date DATETIME, author TEXT, author_karma INTEGER)')

###################################################################################

for sub in subreddit: #for submission in top 100 submissions in specified subreddit
    if not sub.stickied: #for submissions that are not "stickied"
        count += 1
        subid = sub.id #type str
        subtitle = sub.title #type str
        submission_score = sub.score #type int
        total_comments = sub.num_comments #type int
        sdate = sub.created_utc
        submission_date = datetime.datetime.utcfromtimestamp(sdate) #type datetime
        submission_author = str(sub.author) #from praw.models.reddit
        uprint('submission_title: ', subtitle)
        print('sub_id :', subid)
        print('total comments: ', total_comments)
        print('submission created at: ', submission_date)
        print('submission score: ', submission_score) #score = likes - dislikes
        print('submission author: ', submission_author) #author = username
        aredditor = reddit.redditor(submission_author)
        try:
            authorkarma = aredditor.link_karma
            uprint('link karma: ', authorkarma)
            print('\n')
        except:
            authorkarma = 0
            print("No Karma\n")
        sub_info = [subid, subtitle, sub.score, sub.num_comments, submission_date, submission_author, authorkarma]
        cur.execute('INSERT or IGNORE INTO Submissions VALUES (?,?,?,?,?,?,?)', sub_info)
print(count)
conn.commit()


###################################################################################
## REDDIT VISUALIZATION COMPONENT USING PANDAS AND PLOTLY #########################
###################################################################################
cur.execute('SELECT score, creation_date from Submissions')
p = cur.fetchall()
df = pd.DataFrame([[x for x in y] for y in p])
df.rename(columns={0: 'Score', 1: 'CreationDate'}, inplace = True)


trace1 = go.Scatter(
    x=df['CreationDate'],
    y = df['Score'],
    mode = 'markers')

layout = go.Layout(
    title = 'Reddit Submissions Score vs Date',
    xaxis = go.XAxis(title = 'Creation Date'),
    yaxis = go.YAxis(title = 'Submission Score'))

data = [trace1]
fig = dict(data= data, layout=layout)
py.iplot(fig, filename='Reddit Submissions')
cur.close()
conn.close()

print('Reddit Visualization Success')
###################################################################################
###################################################################################
###################################################################################
#API #2: Facebook
# This portion requires that the USER generates an access token from facebook
# Enter token when prompted
# When prompted, type in search query for Events that you are interested in.
# Again, I was interested in ' Big Data', however, I wrote the function so that it matches events to any search queries
# This function will return data, including lat and longitude, of up to  facebook 100 events
# Note that not all search queries will yield 100 events

print("Welcome to the Facebook Analysis Portion of the project")

access_token = None
if access_token is None: #get token from fb user in order to run this script
    access_token = input("\nCopy and paste token from https://developers.facebook.com/tools/explorer\n>  ")
graph = facebook.GraphAPI(access_token)

def get_fb_events(topic):
    if topic in FB_CACHE_DICTION:
        print("Data Was Cached")
        events = FB_CACHE_DICTION[topic]
        return events
    else:
        print("making new request")
        params = { 'q': topic, 'type': 'Event', 'limit': '100', 'time_format': 'U'}
        events = graph.request("/search?", params) #matching fb events with user input words.  'Big Data' was the original goal in this project
        FB_CACHE_DICTION[topic] = events
        x = json.dumps(FB_CACHE_DICTION)
        fb_cache_file = open(FB_CACHE, 'w')
        fb_cache_file.write(x)
        fb_cache_file.close()
        return FB_CACHE_DICTION[topic]

t = input("Enter Topic 'ex: Big Data' : ")
eventsl = get_fb_events(t) #dictionary of facebook events results for query
#print(type(eventsl)) #type dict
eventslist = eventsl['data']
#eventlist = json.dumps(eventslist, indent= 4)
#uprint(eventlist)

###################################################################################
conn = sqlite3.connect('FB_APIandDB.sqlite')
cur = conn.cursor()
cur.execute('DROP TABLE IF EXISTS Events')
cur.execute('CREATE TABLE Events (event_date DATETIME, description TEXT, attending INTEGER, city TEXT, country TEXT, declined INTEGER, interested INTEGER, eventid INTEGER PRIMARY KEY, latitude REAL, longitude REAL)')
###################################################################################

for x in eventslist: #For all the events that match the search query
    eventid = x['id'] #event id = unique identifier to access more information on the event
    #uprint(eventid)
    eventname = x['name']
    uprint(eventname)
    #try:
    starttime = (x['start_time']) # example 2017-12-19T14:30:00+0100 
    uprint('start time: ', starttime) #time of event in formation YYYY-MM-DD + Time
    #print(type(starttime))
    #except:
    #    starttime = 'None'
    #    print("No Time Specified")
    try:                    
        place = x['place']
        uprint('location: ', place['location']) #printing event location information if avaliable
        city = place['location']['city']
        country = place['location']['country']
        lat = place['location']['latitude']
        longitude = place['location']['longitude']
    except:
        place = 'None'
        print("no location avaliable")
    try:
        description = x['description']
    except:
        description = 'No Description Avaliable'
    detailz = graph.get_object(id=eventid, fields = 'attending_count, declined_count, interested_count')
    #print(type(detailz['attending_count']))  type = 'int'
    num_attending = detailz['attending_count']
    num_interested = detailz['interested_count']
    num_declined = detailz['declined_count']
    #print('attending: ', num_attending)
    #print('interested: ', num_interested)
    #print('declined: ', num_declined, '\n')
    events_info = (starttime, description, num_attending, city, country, num_declined, num_interested, eventid, lat, longitude)
    cur.execute('INSERT or IGNORE INTO Events VALUES (?,?,?,?,?,?,?,?,?,?)', events_info)
    print('\n')
conn.commit() 

###Fb Visualization component
## Creating a Map of events listed for search query
cur.execute('SELECT latitude from EVENTS')
k= cur.fetchall()
lats = [int(x[0]) for x in k]
cur.execute('SELECT longitude from EVENTS')
w = cur.fetchall()
longs = [int(x[0]) for x in w]

l=0

while l < len(lats):
    xpt,ypt = wmap(longs[l], lats[l])
    wmap.plot(xpt, ypt, "d", markersize=15)
    l += 1
plt.title('Facebook Events')
plt.show()
cur.close()
conn.close()
print('Facebook Visualization Success')
###################################################################################
###################################################################################
#API #3: New York Times
# Matches articles based on a user entered query
# NYT requires USER generates an access key via NYTS
# Enter article search query when prompted
# Process returns useful meta-data about articles

print("Welcome to the New York Times Analysis Portion of the project")


nytbase_url = "https://api.nytimes.com/svc/search/v2/articlesearch.json"
params = {}
nyt_key = None
if nyt_key is None: #get token from nyt user in order to run this script
    nyt_key = input("\nCopy and paste API Key from https://developer.nytimes.com/\n>  ")


#Question = where to implement range(10) in order to get 100 results
def get_nyt_articles(subject): #creating an API request for NYT articles on a certain subject
    y=0
    if subject in NYT_CACHE_DICTION:
       print("Data in Cache")
       return NYT_CACHE_DICTION[subject]
    else:
        print("Making new request")
        data = list()
        t = 0
        for x in range(0,10): #10 results per page. 10 pages = 100 results
            params = {'page':  str(x), 'api-key': nyt_key, 'q': subject,
                   'fq' : "headline(\"" + str(subject) + "\")",
                   'fl': 'headline, keywords, pub_date, news_desk'}
                   #'offset': x}
        #while x <= 3:
           
            nyt_api =  requests.get(nytbase_url, params = params)
            print(type(json.loads(nyt_api.text)))
            #uprint(json.loads(nyt_api.text))
            #try:
            data.append(json.loads(nyt_api.text))
            #except: 
                #print('didnt work')
                #continue

            #x = x + 1
            time.sleep(1) #avoid making too many requests during pagnation

            NYT_CACHE_DICTION[subject] = data
            dumped_json_cache = json.dumps(NYT_CACHE_DICTION)
            nyt_cache_file = open(NYT_CACHE, 'w')
            nyt_cache_file.write(dumped_json_cache)
            nyt_cache_file.close()
            t +=1
            print(t)

        return NYT_CACHE_DICTION[subject]
        
subj = input("Enter Search Query: ")
articles = (get_nyt_articles(subj))
#uprint(articles)  #type(articles) = LIST
#uprint(articles)
#print(len(articles[2]['docs']))
#s = json.dumps(articles, indent = 4)
#print(s)

###################################################################################
conn = sqlite3.connect('NYT_APIandDB.sqlite')
cur = conn.cursor()
cur.execute('DROP TABLE IF EXISTS Articles')
cur.execute('DROP TABLE IF EXISTS Keywords')
cur.execute('DROP TABLE IF EXISTS Sections')
cur.execute('CREATE TABLE Articles (date_published DATETIME, headline TEXT, query TEXT, section TEXT)')
cur.execute('CREATE TABLE Keywords (keyword TEXT, value INTEGER)')
cur.execute('CREATE TABLE Sections (section TEXT, value INTEGER)')
###################################################################################

keywords_dict = {}
sections_dict = {}

for t in articles:
    if t['status'] == 'OK':
        stories = t["response"]["docs"]
        for item in stories:
            headline = item["headline"]["main"]
            #print(headline)
            publication_date = item.get("pub_date", "Date Unavaliable")
            #print(publication_date)
            news_section = item.get("new_desk", "Section Unavaliable")
            #print(news_section)
            if news_section != 'Section Unavaliable':
                sections_dict[news_section] = sections_dict.get(news_section, 0) + 1
            keywords_list = item["keywords"]
            if len(keywords_list) != 0:
                for piece in keywords_list:
                    words = piece['value']
                    keywords_dict[words] = keywords_dict.get(words, 0) + 1
            stories_info = (publication_date, headline, subj, news_section, )
            cur.execute('INSERT or IGNORE INTO Articles VALUES (?,?,?,?)', stories_info)
    else:
        continue
#stories = articles[0]["response"]['docs']
#print(type(stories), type(articles))
#print(len(stories))
#s = str(stories)
#ss = re.findall('headline', s)
#print(len(ss))


sorted_keywords = [(a, keywords_dict[a]) for a in sorted(keywords_dict,
                    key = keywords_dict.get, reverse = True)]

for k, v in sorted_keywords:
    #print(k, v)
    g = (k,v)
    cur.execute('INSERT or IGNORE INTO Keywords VALUES (?,?)', g)

sorted_sections = [(a, sections_dict[a]) for a in sorted(sections_dict,
                    key = sections_dict.get, reverse = True)]
print('\n')

print('Sorted News Sections: ')
for c, d in sorted_sections:
    print(c, d)
    b = (c,d)
    cur.execute('INSERT or IGNORE INTO Sections VALUES (?,?)', b)
#printing sections based on value
conn.commit()

keyword_wordcloud = WordCloud(background_color="black", max_font_size=60, min_font_size = 12, max_words = 100, width = 800, height =800).generate_from_frequencies(keywords_dict)
#plt.figure.Figure()
plt.imshow(keyword_wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()
cur.close()
conn.close()

print('NYTimes Visualization Success')
print('End of Final Project')
###############################################################
###############################################################

