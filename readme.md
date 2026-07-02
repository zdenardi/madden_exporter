# Madden 26 Exporter 
This repo uses the Madden 26 companion app and uses the exported data for future projects. 

## What is Madden? Why is this needed?

Madden is a multi-decade long American Football game that allows users to play as managers/coaches/players in the NFL. I am currently in whats called a "Connected Franchise" where me and some friends are building up different teams within the same "league". 

The stats/GUI of Madden leave much to be desired, so I thought it would be a fun project to reverse engineer and create a project that provides better data for our league. 

## Requirements
- You must have the madden companion app downloaded, or any other way to send a export request.  
- Docker installed

## To start
- pip install -r requirements.txt
- run docker-compose up and wait for it to finish starting up
- in a terminal, navigate to root and `bash run.sh` to get the cloudflare tunnel started. It will spit out a url that you can use to export to 
- in another terminal run `flask run --host=0.0.0.0 --debug 

Note: You don't need debug, but sense this is a pretty new project, and you might be fiddling probably helpful.

### Why Cloudflare Tunnel 
Honestly, right now its the easiest to run a temporary tunnel and send requests that way then to set up anything more solid. You are more than welcome to set up anything more concrete. 

## Models and Classes 
In my head, there are two types of data being sifted through/used. 

1. MaddenClasses `/models/madden_classes.py` - Types data exported from Madden, validated by pydantic
2. Custom SqlAlchemy Classes `models/Game|Event|DefensiveStat|KickStat|PassingStat|Player|PuntingStat|ReceivingStat|RushingStat|TeamInfo|TeamStats|TeamInfo.py`


These are separated when I was reverse engineering the responses. I think in the future I might just do a transform without going into pydantic models, but thats for the future. 

## Routes 
### `/` - GET
- Basic Health Check

### `/<platform>/<league_id>/team/<team_id>/roster`- POST
- This route is specifically used by the Madden Export to capture every roster.  To my understanding, the Madden Exporter sends out a POST for every team/free agent.
 
 ### `/<platform>/<league_id>/week/<type>/<num>/<resource>` - POST
- This route is specifically used by the Madden Export to capture every weekly "resource". This includes 
    - Weekly Defensive Stats
    - Weekly Kicking Stats
    - Weekly Passing Stats
    - Weekly Puntng Stats
    - Weekly Rushing Stats
    - Weekly Receiving Stats
    - Weekly "Schedule" information 
    - Weekly Team Information
    - Weekly Teamstat information 

 ### `/<platform>/<league_id>/<resource>` - POST
 - This route is specifically used by the Madden Export to capture every weekly League information or Standings 

 ### `/<path:path>` - GET | POST
 - This was used to be a catch-all to grab all information to start reverse engineering everything.

## Some old code that will be removed  
I have some old remnants of code that I have left over from my research and will have to be removed, mostly in the app.py as routes. They are there for now don't judge me too harshly. 

## Whats next

Thanks to @snallapa and his research which you can read at [here](https://nallapareddy.com/snallabot-post/)...he figured out a way to send API requests without the use of the app which is something that could really make this app sing. 

Some 'Bluesky' features I would like to implement


- Auto get updates from EA servers without my intervention
- Ability to automatically tell a league in Slack that the week advanced 
- Ability to create AI generated articles off the cuff based on `Events` such as a player having a record setting day, or an upset, or just random funny "tweets" based on the league to make the league feel more alive. 
- A fantasy'esk game using the stats week by week.