from __future__ import annotations

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, Float, String, Boolean, ForeignKey, DateTime

Base = declarative_base()

class Foo(Base):

    __tablename__='foo'
    id = Column(Integer, primary_key=True)
    foo = Column(String)

class Flight(Base):
    '''
        launch: A Launch instance for this flight
        launchtime: Datetime of launch
        distance: Distance in kilometers
    '''
    __tablename__ = 'flights'

    id = Column(Integer, primary_key=True)
    launchtime = Column(DateTime, nullable=False)
    distance = Column(Float, nullable=False)

    launch_id = Column(Integer, ForeignKey('launches.id'))
    launch = relationship('Launch', back_populates='flights')
    #launch = relationship('Launch', back_populates='flights')
    #launch = relationship('Launch', back_populates='launches')

class LaunchNames(Base):
    '''
    XContest has free text input element for launch name.
    This can result in one launch having multiple names.
    name: Name given in flight input form
    '''

    __tablename__ = 'launchnames'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    launch_id = Column(Integer, ForeignKey('launches.id'))
    launch = relationship('Launch', back_populates='launchnames')

class Launch(Base):
    '''
    launchname: Launchsite name string, given by pilot
    latitude:  (https://en.wikipedia.org/wiki/Decimal_degrees)
    longitude:  (https://en.wikipedia.org/wiki/Decimal_degrees)
    registered: Whether this launch site has been recognized as official launch site or not
    '''
    __tablename__ = 'launches'

    id = Column(Integer, primary_key=True)

    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    registered = Column(Boolean)

    launchnames = relationship('LaunchNames', back_populates='launch')
    flights = relationship('Flight', back_populates='launch')

