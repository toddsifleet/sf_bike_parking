SF Bike Rack Finder
=============

A simple map based tool to help you find a place to park your bike in San Francisco.  Use it [here](http://162.243.251.147/)!

Features
========

-Automatically shows you bike racks close to your current location. 

-Search by address or coordinates


Stack
=====

-Flask

-Postgresql

-Mustache.js

-Jquery

-Google Maps API

-Hosted on Digital Ocean


API:
===

Find By Id:
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

Find In Bounds:
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