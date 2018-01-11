import sys

from datetime import datetime
from datetime import timedelta
from lxml import etree
from lxml.etree import Element
import os

xmlns = '{http://www.topografix.com/GPX/1/1}'
TIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
STOP_TRESHOLD = timedelta(hours=4)

class Aggregator:
    def __init__(self):
        self.track = Element(xmlns+"trk")
        self.seg = Element(xmlns+"trkseg")
        self.mintime = "9999-99-99T00:00:00Z"
        self.maxtime = "0000-00-00T00:00:00Z"

    def append_tracks(self, tracks):
        for track in tracks:
            for segment in track.findall(xmlns+'trkseg'):
                self.append_seg(segment)

    def append_seg(self, segment):
        first = segment.xpath('*[1]')
        firsttime = first[0].find(xmlns+'time').text
        last = segment.xpath('*[last()]')
        lasttime = last[0].find(xmlns+'time').text

        if firsttime > self.maxtime:# whole segment is later than our max time
            self.seg.extend(segment)
            self.maxtime = lasttime
            self.mintime = min(firsttime, self.mintime)
            return

        if lasttime < self.mintime:# whole segment is earlier than our min time
            self.seg, segment = segment, self.seg
            self.seg.extend(segment)
            self.maxtime = max(lasttime, self.maxtime)
            self.mintime = firsttime
            return

        # TODO: segments intersection
        sys.stderr.write("time overlaps!\n")

    def add_file(self, filename):
        print('Adding ' + filename)
        data = etree.parse(filename)
        tracks = data.findall(xmlns+"trk")
        self.append_tracks(tracks)

    def separate_days(self):
        first = self.seg.xpath('*[1]')
        firsttime = first[0].find(xmlns+'time').text
        prevtime = datetime.strptime(firsttime, TIME_FORMAT)
        stops_count = 0
        for point in self.seg.iterchildren():
            curtime = datetime.strptime(point.find(xmlns+'time').text, TIME_FORMAT)
            if curtime - prevtime > STOP_TRESHOLD:
                wpt = Element(xmlns+"wpt")
                wpt.set('lat', prevp.get('lat'))
                wpt.set('lon', prevp.get('lon'))
                name = Element(xmlns+"name")
                stops_count += 1
                name.text = 'Ночёвка ' + str(stops_count)
                wpt.append(name)
                prev_ele = prevp.find(xmlns+'ele')
                if prev_ele is not None:
                    ele = Element(xmlns+'ele')
                    ele.text = prev_ele.text
                    wpt.append(ele)
                #self.gpx.append(wpt)
                print('Stop begin', prevtime)
            prevtime = curtime
            prevp = point

    def save(self, filename):
        result = etree.parse(os.path.dirname(os.path.realpath(__file__)) + '/template.gpx')
        gpx = result.getroot()
        gpx.append(self.track)
        self.track.append(self.seg)
        result.write(filename, xml_declaration=True, encoding='utf-8')
        gpx.remove(self.track)
