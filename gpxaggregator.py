from lxml import etree
from xml.etree import ElementTree
from lxml.etree import Element

xmlns = '{http://www.topografix.com/GPX/1/1}'

class Aggregator:
    def __init__(self, base_filename):
        self.data = etree.parse(base_filename)
        tracks = self.data.findall(xmlns+"trk")
        self.gpx = self.data.getroot()
        for track in tracks:
            self.gpx.remove(track)

        self.track = Element(xmlns+"trk")
        self.gpx.append(self.track)
        self.seg = Element(xmlns+"trkseg")

        self.mintime = "9999-99-99T00:00:00Z"
        self.maxtime = "0000-00-00T00:00:00Z"

        for track in tracks:
            for segment in track.findall(xmlns+'trkseg'):
                self.append_seg(segment)

    def append_seg(self, segment):
        first = segment.xpath('*[1]')
        time = first[0].find(xmlns+'time')
        last = segment.xpath('*[last()]')
        f2 = [x for x in segment.iterchildren()]
        print(first)
        #firsttime = first.iter()

    def save(self, filename):
        self.track.append(self.seg)
        self.data.write(filename, xml_declaration=True, encoding='utf-8')

