import unittest

from datetime import datetime
import math
from lxml import html

import flightservice.xcontest as xcontest

class TestScraper(unittest.TestCase):


    RESULT_HTML_FRAGMENT = '''<tr id="flight-1346457" class="  ">
  <td title="FLID:1346457">1</td>
  <td title="submitted: 20.05. 00:51">19.05.18 <em>07:47</em>
  </td>
  <td><div class="full">
    <span class="cic" style="background-image:url(https://s.xcontest.net/img/flag/fi.gif);" title="Finland">FI</span><a class="plt" href="/world/en/pilots/detail:jmakko">Jouni Makkonen</a>
  </div></td>
  <td><div class="full">
    <span class="cic" style="background-image:url(https://s.xcontest.net/img/flag/fi.gif)" title="Finland">FI</span><a class="lau" href="/world/en/flights-search/?filter%5Bpoint%5D=23.05382%2063.11492&amp;list%5Bsort%5D=pts&amp;list%5Bdir%5D=down">EFKA</a> <span class="lau" style="color:green" title="registered takeoff">&#10004;</span>
  </div></td>
  <td><div class="disc-vp" title="free flight"><em class="hide">VP</em></div></td>
  <td class="km">
    <strong>337.56</strong> km</td>
    <td class="pts">
      <strong>337.56</strong> p.</td>
      <td class="cat-C"><div title="OZONE Enzo 3" class="sponsor ozone"><span class="hide">C</span></div></td>
      <td><div class="for-qw">
        <img class="qw" src="/img/eye-icon.gif" width="18" height="17" title="quick view"><div class="quickview">
          <br style="display: none" title="fl=1346457|rt=10962882"><div></div>
        </div>
      </div></td>
      <td class="detail-camera"><div>
        <span class="posts"></span><a class="detail" title="flight detail" href="/world/en/flights/detail:jmakko/19.5.2018/07:47">
          <span class="hide">flight detail</span>
        </a>
      </div></td>
    </tr> '''

    def setUp(self):

        self.rowelement = html.fragment_fromstring(TestScraper.RESULT_HTML_FRAGMENT)
        self.xcontestscraper = xcontest.XContestScraper()
        self.row = self.xcontestscraper.ResultRow(self.rowelement)


    def test_extract_launch_name(self):

        launchname = self.row.extract_launch_name()
        self.assertEqual(launchname, 'EFKA', msg=f'Expected launchname "EFKA", got {launchname}')

    def test_extract_distance(self):

        distance = self.row.extract_distance()
        self.assertTrue(math.isclose(distance, 337.56, rel_tol=1e-5), msg=f'Expected distance 337.56, got {distance}')

    def test_extract_launch_coordinates(self):

        latitude, longitude = self.row.extract_launch_coordinates()
        self.assertTrue(math.isclose(latitude, 23.05382, rel_tol=1e-5), msg=f'Expected latitude 23.05382, got {latitude}')
        self.assertTrue(math.isclose(longitude, 63.11492, rel_tol=1e-5), msg=f'Expected longitude 63.11492, got {longitude}')

    def test_extract_launch_is_registered(self):

        isregisteredlaunch = self.row.extract_launch_is_registered()

        self.assertTrue(isregisteredlaunch, msg=f'Expected registered_launch to be True. Is false.')

    def test_(self):

        launchtime = self.row.extract_launchtime()
        comparisontime = datetime.fromisoformat('2018-05-19 07:47')
        self.assertEqual(launchtime, comparisontime, msg=f'Expected {comparisontime}, got {launchtime}')