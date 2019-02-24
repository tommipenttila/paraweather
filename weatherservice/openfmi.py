from owslib.wfs import WebFeatureService

class FMIDataAccess:


    def discovery(self):

        wfs = WebFeatureService('http://opendata.fmi.fi/wfs?service=WFS', version='2.0.0')
        xmlio = wfs.getfeature(storedQueryID='fmi::avi::observations::finland::iwxxm')

        xml=xmlio.getvalue().encode('utf-8')
        parser = etree.XMLParser(ns_clean=True, recover=True, encoding='utf-8')
        root = etree.fromstring(e, parser)