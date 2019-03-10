import os
import redis
from flightservice.flightcache import FlightCache

REDIS_URL_ENV = 'REDIS_URL'
REDIS_FLIGHTS_DATABASE_ENV = 'REDIS_FLIGHTS_DATABASE'



class Redis(FlightCache):

    def __init__(self):

        self.redisUrl = os.getenv(REDIS_URL_ENV)


    def addFlight(self):

