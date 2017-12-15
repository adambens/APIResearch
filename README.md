# APIResearch
Final Project for 206


APIS USED: REDDIT, FACEBOOK, NEW YORK TIMES

Reddit: requires account on Reddit, generate user access token information
        Retrieves top 100 submissions for specified subreddit. 'r/bigdata is stored in Reddit DB, Submissions table
        Retrieves information about each submission including creation date and submission score

Facebook: requires account on facebook, generate user access token information
        Retrieves up to 100 events for specified Topic. 'Big Data' is stored in Facebook DB, Events table
        Retrieves meta-data for each event, including event time and location.
        
New York Times: requires NYTs API Key
        Retrieves up to 100 articles for specified topic. 'Big Data' is stored in NYT DB, articles, sections, and keywords tables.
        Retrieves meta-data for each article, including publication date.
        

When the program runs, the visualizations for Facebook and NYT will pop up in a new window. You can save these visualizations as PNG's. Close the pop up window to continue with the program.

        
It is possible to comment out portions of the code so that the program only produces visualizations for the existing databases on 'Big Data'.
To do this, 
place """ on line 88
      """ on line 137
      # at beginning of lines 140 and 141
      """ on line 144
      """ on line 174

     
PNG file 'Reddit Submissions' is an example of visualization for bigdata subreddit.
PNG file 'FB EVENTS1' is an example of a visualization for facebook event locations.



