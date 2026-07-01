# Madden 26 Exporter 
This repo uses the Madden 26 companion app and uses the exported data for future projects. 

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
