from __future__ import annotations
from dataclasses import dataclass
from lxml import html
from typing import List, Tuple
from datetime import datetime
from urllib import parse
import logging
import os
import requests
import sys
import settings # will get loaded

from flightservice.flight import Flight, Launch
from flightservice.flightcache import FlightCache

PARAMETER_FILTER_POINT = 'filter[point]'
PARAMETER_TITLE = 'title'
VALUE_REGISTERED_LAUNCH = 'registered takeoff'
FORMAT_LAUNCHTIME = '%d.%m.%y %H:%M'


class XContestScraper:
    '''
    Responsible for retrieving XContest flight search pages and scraping flight and launch site information from them.
    '''

    def __init__(self):

        self.xcontestsearchurl = os.getenv('XCONTEST_SEARCH_URL')


    @classmethod
    def fill_flights_cache(self, cache: FlightCache):
        '''
        Entrypoint for scraping flights data from XContest
        :return:
        '''
        scraper = XContestScraper()
        for flight in scraper.flights():

            print(flight)

            # TODO: cache fill


    def retrieve_xcontest_search_page(self, searchpageurl: str) -> html.HtmlElement:
        '''
        For given URL, retrieve HTML page and parse into HtmlElement
        :param searchpageurl: string
        :return: HtmlElement
        '''
        logging.info(f'Retrieving XContest search page at {searchpageurl}')
        searchpage = requests.get(searchpageurl)
        tree = html.fromstring(searchpage.content)

        return tree



    def results_page_url(self, searchpage: html.HtmlElement) -> str:
        '''
        If no page is yet retrieve, use envar set in XCONTEST_SEARCH_URL.
        If page is already retrieved, look for "next page" link and return that.
        Failing both, return None
        :param searchpage: HtmlElement
        :return: URL string or None
        '''

        nextpagelink = None

        if searchpage is not None:
            nextpagetags = searchpage.xpath('//a[@title="next page"]')
            if nextpagetags:
                nextpagelink = nextpagetags[0].attrib.get('href')
        else:
            nextpagelink = self.xcontestsearchurl

        return nextpagelink


    def flights(self) -> Flight:
        '''
        A generator for returning Flight objects for every result line found in all html results pages
        :return:
        '''
        searchpageelement = None
        searchpageurl = self.results_page_url(searchpageelement)

        while searchpageurl:
            searchpageelement = self.retrieve_xcontest_search_page(searchpageurl=searchpageurl)
            flightstable = self.scrape_flight_rows(searchpagetree=searchpageelement)

            for resultrowelement in flightstable:
                resultrow = self.ResultRow(resultrowelement)
                flight = resultrow.extractFlight() #self.html_flight_conversion(flightrow)
                yield flight

            searchpageurl = self.results_page_url(searchpageelement)


    def scrape_flight_rows(self, searchpagetree: html.HtmlElement) -> List[html.HtmlElement]:
        '''
        Find actual resultset amongst all other tags
        :param searchpagetree:
        :return:
        '''
        logging.info(f'Extracting flight data from resultpage')
        flightstable = searchpagetree.xpath('//tr[contains(@id, "flight-")]')

        return flightstable




    class ResultRow:
        '''
        Inner class for isolating result row values extraction
        '''

        def __init__(self, rowelement: html.HtmlElement):

            self.element = rowelement

        def extractFlight(self) -> Flight:

            # extract launch site data first. Extractors order and types must follow Launch class constructor signature
            launchextractorfunctions = [self.extract_launch_name, self.extract_launch_coordinates,
                                        self.extract_launch_is_registered]
            launchparameters = []
            for launchextractor in launchextractorfunctions:

                try:
                    launchparameters.append(launchextractor())
                except:
                    logging.fatal(
                        f'Unable to extract launch data func={launchextractor.__name__}. Gathered: {launchparameters}')
                    exit(1)

            launch = Launch(*launchparameters)

            # extract flight data
            flightextractors = [self.extract_launchtime, self.extract_distance]
            flightparameters = [launch]
            for flightextractor in flightextractors:
                try:
                    flightparameters.append(flightextractor())
                except:
                    logging.fatal(
                        f'Unable to extract flight data {flightextractor.__name__}. Gathered: {flightparameters}')

            flight = Flight(*flightparameters)

            return flight

        def extract_launch_name(self) -> str:

            launchlinkelements = self.element.xpath('td/div/a[@class="lau"]')

            # required, fail if missing
            return launchlinkelements[0].text_content()

        def extract_launch_coordinates(self) -> Tuple[float, float]:

            href = self.element.xpath('td/div/a[@class="lau"]')[0].attrib.get('href')
            queryparams = parse.parse_qs(parse.urlsplit(href).query)
            pointparam = queryparams.get(PARAMETER_FILTER_POINT)

            # required, fail if missing
            point = pointparam[0].split()
            longitude, latitude = [float(x) for x in point]

            return longitude, latitude

        def extract_launch_is_registered(self):

            return self.element.xpath('td/div/span[@class="lau"]')[0].attrib.get(PARAMETER_TITLE) == VALUE_REGISTERED_LAUNCH

        def extract_distance(self):

            # required, fail if missing
            distancestring = self.element.xpath('td[@class="km"]/strong')[0].text_content()

            return float(distancestring)

        def extract_launchtime(self):

            launchtimestring = self.element.xpath('td[contains(@title, "submitted:")]')[0].text_content().strip()
            launchtime = datetime.strptime(launchtimestring, FORMAT_LAUNCHTIME)

            return launchtime


if __name__ == '__main__':

    '''
    For command line XContest scrape entry. Stack trace on possible failure as error condition response.
    '''

    args = sys.argv # TODO: cli opts

    # Debug logging for cli invocation
    logging.getLogger().setLevel(logging.DEBUG)

    cache = FlightCache()
    XContestScraper.fill_flights_cache(cache)

