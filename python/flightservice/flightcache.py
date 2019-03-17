import os
import sys

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from flightservice.flight import Flight, Launch, LaunchNames


class FlightCache:

    def __init__(self, postgisurl: str):

        self.postgisurl = postgisurl
        self.engine = create_engine(self.postgisurl, echo=True)
        self.session = None

    def get_session(self):

        if not self.session:

            Session = sessionmaker(bind=self.engine)
            self.session = Session()

        return self.session

    def reset(self):

        session = self.get_session()
        '''
        Flight.__table__.drop(self.engine)
        LaunchNames.__table__.drop(self.engine)
        Launch.__table__.drop(self.engine)

        Launch.__table__.create(self.engine)
        Flight.__table__.create(self.engine)
        LaunchNames.__table__.create(self.engine)

        launch = Launch(latitude=66.0, longitude=66.3)
        launchname = LaunchNames(name='foolaunch')
        launch.launchnames.append(launchname)
        '''
        breakpoint()


    def addFlight(self, launch: Launch, launchname: str, flight: Flight):
        '''
        :parameter: See Flight/Launch dataclasses for required members
        :return:
        '''
        breakpoint()
        session = self.get_session()

        '''
        TODO: cylinder of 5000m instead

        paraweather=> SELECT ST_Distance(                                                                             
        ST_Transform('SRID=4326;POINT(23.05382 63.11492)'::geometry, 3857),                                           
        ST_Transform('SRID=4326;POINT(23.04962 63.11798)'::geometry, 3857)                                            );
        );
        '''
        launchforflight = session.query(Launch).filter(Launch.latitude == launch.latitude and Launch.longitude == launch.longitude).first()

        if not launchforflight: # TODO: cylinder calc
            launchforflight = launch
            launchforflight.launchnames.append(launchname)
            session.add(launchforflight)
        else:
            storedlaunchname = session.query(LaunchNames).filter(LaunchNames.name == launchname).first()
            if not storedlaunchname:
                launch.launchnames.append(launchname)



        launchforflight.flights.append(flight)


        session.commit()





def main(argv):

    flightcache = FlightCache(os.getenv('POSTGISURL', 'postgres://paraweather:paraweather@localhost:5432/paraweather'))
    flightcache.reset()

if __name__ == '__main__':

    main(sys.argv)