## unfinished app
The app was intended to find out if a user's gpu is powerful enough to reach the minimun requirements of a game they want to get/play.
At present, it only does the above.
The user can choose from 200 of the most common and power ful GPUs from roughly the last 10 years. This list was taken from a site that rates gpus by power.

### What it can do

* Regex was used to make patterns that will extract, from steam api, gpus made by AMD and Nvidia that are less powerful than all gpus on the users gpu selection list.

If found on the selected games steam api doc, the user is told that they can play the game.

* If this doesn't find anything, a mongo collection holding over a large list gpus from nvidia, amd, and intel is searched.

If a match is found, the user is notified they can play the game because all gpus on this list are weaker than the 200 users gpus. 


* If the gpu is above that range, or is intel, regex patterns are used to find and format the gpus name and search the 200 user gpus on mongo.

Each GPU has a rating, and if the gpu selected by the user has a higher rating, then they are told they can play the game. If not, they are told they can't.

* Before all of above searches, a search to see if the selected game's requirements are in MB. These are old games and GPUs.

If the graphics card n the steam page is described in MB, it will be under 1gb, therefore less powerful than the user's, and the user is told they can play it.(This was meant to have a limit of 512mb incase od 1024mb cards.)

#### Testing

* Every variation of name from AMD Nvidea, and Intel was tested. And example of this is in text.txt.

This was put in place of the steam variable in app_2.py and all the different gpu types will be found, sorted, and corrected. It


#### What was left out

* The user being able to login to leave and edit information about the Graphocs settings and FPS achieved while playing the game on their gpu. Remnants of this is in the drawingboard.py file.

* User having a list of games compatible with their gpu

* Heroku is crashing so to use the app, gitpod or another IDE will have to be used

