# Flight Tracker
A Python routine that uses the Opensky Network API (https://opensky-network.org/) to identify flights passing over a specified latitude/longitude box, and then scrapes SpotterLead (https://en.spotterlead.net/) for additional details about the flight and prints the information out to the console. I came up with this project after noticing that there was a constant stream of planes passing in front of my apartment while flying into LaGuardia. 

### Software Requirements
- This code was written using Python 3.10
- an Opensky Network account
- Latitude and longitude coordinates of the area you want to check for flights over. I used bboxfinder (http://bboxfinder.com)