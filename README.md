# BAPCS Stock/Price checker bot  
Listens to reddit.com/r/buildapcsales (by default, can be changed to any sub) for posts, and replies with price, part number, and inventory counts  
Can be expanded with additional sites under /src/stores, provided they return the correct info to main  
Also, logs prices to db for possible price history analysis, but can be reconfigured to use text or csv for simplicity.  If reconfigured, should log reddit post IDs replied to at minimum to avoid duplicate comments

# Domains  

+ Microcenter (Database Logging, Reddit Submission Replies)
+ Newegg (Database Logging)
+ Ebay (Database Logging, No Reddit Submission yet, but in prog)
+ Amazon (Database Logging)
+ BestBuy (Database Logging)
+ Frys (Database Logging)
+ Rakuten (Database Logging)

# Language  
Python  
+ requires 3.6+ (f-strings)

# Libraries  
PRAW  
Requests  
LXML  
SQLAlchemly  
PyMySQL  
+ addl dependencies, all included in requirements.txt  

# Requirements  

+ Everything installed
+ MySQL (or other, but will change library reqs) server running
+ The following files:  

#### File Requirements  
(examples found in /examples)  

+ praw.ini placed in /src/reddit/  

    to configure:
    + go [here](https://www.reddit.com/prefs/apps/)
    + scroll down
    + click 'are you a developer...'
    + give your bot a name (note: this is not the display name, it will still post/comment under your account name)
    + choose 'script'
    + give it a description
    + put something in the about url 
    + put something in the redirect uri - http://localhost:8080 - will work
    + click 'create app'
    + client_id is the key under 'personal use script'
    + client_secret is the key next to secret  
    
+ logfile.log placed in /src/  
    + just a blank file for logs  
    
+ db.ini placed in /src/database/  
    + each section can hold a config for different servers, just name them accordingly
    + under DEFAULT, set UseDatabase to the section name of the db you'd like to use
    
# Want to Add a Store/Site Parser?   

+ Markdown for reply not needed (just return None instead, will still log to database)  
+ Check out /examples/store_parser.py and existing store modules  
+ Prefer LXML over regexes, but site/page layout can make that exceedingly difficult in a lot of cases
+ Must accept a praw.Reddit.submission
+ Must return 2 things:  
    + A dictionary containing mpn and price, or None values for either/both
    + Valid markdown for reddit comment submission, or None
+ None values will be handled by the bot
    + Not all links work the same and network issues happen sometimes
    + Handles errors while allowing the bot to continue running
    + This is not a scientific application, though analyzing price data when enough has been collected will be interesting
    + mpn: string, manufacturer part number, model number, or whatever nomenclature the site uses to refer to a unique product identifier, ideally similar across multiple stores if possible
    + price: Integer, rounded, product price

    


