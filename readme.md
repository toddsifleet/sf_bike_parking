SF Bike Rack Finder
=============

A simple map based tool to help you find a place to park your bike in San Francisco.  Use it [here](http://162.243.251.147/)!

Features
========

-Automatically shows you bike racks close to your current location. 

-Search by address or coordinates

-API to look up spots by ID or coordinates


Possible Future Work
=====================

- Make the UI more mobile friendly
	
	- Remove the InfoWindow, and use a fixed div to show the summary information
	- Remove the Address bar if the device supports geolocation
		
- Give the user notifications (instead of console.log)

- On a desktop give a list of all parking spaces in a side bar.

- Sort /spot/bounds so we can automatically add directions to the closest parking spot.  This would require using postgis or someother method for calcualating distances between points.

- Add runtime/front ends test.

- Improve deduping process and group racks with the same coordinates.


Data
====

-Source: https://data.sfgov.org/Transportation/Bicycle-Parking-Public-/w969-5mn4

-Clean Up: Remove invalid characters

-Dedup: I remove any entry that had duplicate coordinates of another entry.


Stack
=====

-Flask

-Postgresql

-Mustache.js

-Jquery

-Google Maps API

-Hosted on Digital Ocean


API
===

Find By Id ([e.g.](http://162.243.251.147/spots/1)):
-----------
    URL: /spots/<spot_id>
    METHOD: GET
    ERROR RESPONSES:
    	CODE 404: Spot not Found
    	CODE 400: Invalid ID (must be an int)
    SUCCESS RESPONSE: {
        id: <id>,
        address: <address>,
        location: <location>,
        placement: <placement>,
        racks: <racks>,
        status: <status>,
        spaces: <spaces>,
        latitude: <latitude>,
        longitude: <longitude>
    }
  

Find In Bounds ([e.g.](http://162.243.251.147/spots/bounds?bounds=37.773713%2C-122.422849%2C37.776146%2C-122.415982)):
-----------
    URL: /spots/bounds
    PARAMATERS:
    	bounds: 
    		format: <min_lat>,<min_lng>,<max_lat>.<max_lng>
    		example: 37.773477,-122.423715,37.776454,-122.416849
    METHOD: GET
    ERROR RESPONSES:
    	CODE 400: Invalid Request
    SUCCESS RESPONSE: {results: [{
        id: <id>,
        latitude: <latitude>,
        longitude: <longitude>
    }]}


License:
-------

See LICENSE