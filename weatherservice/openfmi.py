from io import StringIO, BytesIO
from datetime import datetime

from owslib.wfs import WebFeatureService
from owslib.util import ResponseWrapper
from lxml import etree

class FMIDataAccess:

    FMIWFS = 'http://opendata.fmi.fi/wfs?service=WFS'
    FMIWFS_VERSION = '2.0.0'
    FMIWFS_STORED_QUERY_ID = 'fmi::observations::weather::simple'

    def discovery(self, fmisid: int, starttime: datetime, endtime: datetime):

        queryparams = {
            'fmisid': fmisid, # Kiikala fmisid: 100967
            'starttime': starttime,
            'endtime': endtime,
            'timestep': 60
        }

        breakpoint()
        wfs = WebFeatureService(FMIDataAccess.FMIWFS, version=FMIDataAccess.FMIWFS_VERSION)
        response = wfs.getfeature(storedQueryID=FMIDataAccess.FMIWFS_STORED_QUERY_ID, storedQueryParams=queryparams)

        tree = self.tree_from_response(responsebody=response)
        resultstring = etree.tostring(tree).decode('utf-8')

        # TODO: rem debug out
        #f=open('/Users/tommi/Desktop/out.xml', 'w+')
        #f.write(resultstring)
        #f.close()

        return resultstring

    def tree_from_response(self, responsebody: StringIO):

        xmlbytes = responsebody.getvalue().encode('utf-8')
        parser = etree.XMLParser(ns_clean=True, recover=True, encoding='utf-8')
        root = etree.parse(BytesIO(xmlbytes), parser)

        return root