from dataclasses import dataclass
from lxml import html
from typing import List
from datetime import datetime
import os
import requests

import settings # will get loaded

@dataclass
class XContestFlight:

    starttime: datetime
    location:
    takeoff: str


class XContestScraper:


    def __init__(self):

        self.xcontestsearchurl = os.getenv('XCONTEST_SEARCH_URL')



    def retrieve_xcontest_search_page(self) -> html.HtmlElement:

        searchpage = requests.get(self.xcontestsearchurl)
        tree = html.fromstring(searchpage.content)

        return tree

    def flights(self) -> tuple(datetime, str, str, bool, float):

        flighthtml = self.scrape_flights(searchpagetree=retrieve_xcontest_search_page())
        for flight in flighthtml:
            # TODO: starttime, location, launch, officiallaunch, distance
            yield (datetime.now(), flight.text, flight.attrib['href'], True, 123.123)


    def scrape_flights(self, searchpagetree: html.HtmlElement) -> List[html.HtmlElement]:

        flights = searchpagetree.xpath('//a[@class="lau"]')

        return flights