#Language  
Python  

#Libraries  
PRAW  
Requests  
SQLAlchemly  
PyMySQL  

\+ addl dependencies, all included in requirements.txt  

#Requirements  

+ Everything installed
+ MySQL (or other, but will change library reqs) server running
+ The following files:  

####File Requirements  
(examples found in /examples)  

+ praw.ini placed in /src/  
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

    


