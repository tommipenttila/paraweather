## Paragliding weather predictor

This is a mashup between 
[The Finnish Meteorological Institute open weather data](https://en.ilmatieteenlaitos.fi/open-data-manual)
and
[XContest](https://www.xcontest.org/world/en/flights-search/?filter%5Bpoint%5D=24.553391+61.732953&filter%5Bradius%5D=200000&filter%5Bmode%5D=START&filter%5Bdate_mode%5D=dmy&filter%5Bdate%5D=&filter%5Bvalue_mode%5D=dst&filter%5Bmin_value_dst%5D=&filter%5Bcatg%5D=&filter%5Broute_types%5D=&filter%5Bavg%5D=&filter%5Bpilot%5D=&list%5Bsort%5D=pts&list%5Bdir%5D=down) paragliding cross contry flights database.

The purpose is to predict the probablility of a good cross country
paragliding day on previous weather information. 

#### Main structures

The web directory contains simple React frontend for querying
good flight conditions probablility depending on the specified
aerodrome.

The webservice is the middle restful layer between browser and
other services.

The flightservice contains code for scraping data off the 
XContest, since no direct API is provided by XContest.

The weatherservice contains accessors to FMI's OGC Rest service.

The model creates a predictor by combining weather and flight
information. The model is queried by  


#### TODO:
- XContest data cache
- FMI data cache
- react
- build
- circleci
- aws