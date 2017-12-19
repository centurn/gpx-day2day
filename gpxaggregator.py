import sys

import time

import datetime
from datetime import datetime
from datetime import timedelta
from lxml import etree
from xml.etree import ElementTree
from lxml.etree import Element

xmlns = '{http://www.topografix.com/GPX/1/1}'
TIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
STOP_TRESHOLD = timedelta(hours=2)

class Aggregator:
    def __init__(self, base_filename):
        print('Tnit from ' + base_filename)
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
        self.append_tracks(tracks)

    def append_tracks(self, tracks):
        for track in tracks:
            for segment in reversed(track.findall(xmlns+'trkseg')):
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
        for point in self.seg.iterchildren():
            curtime = datetime.strptime(point.find(xmlns+'time').text, TIME_FORMAT)
            if curtime - prevtime > STOP_TRESHOLD:
                print('Stop begin', prevtime)
            prevtime = curtime

    def save(self, filename):
        self.track.append(self.seg)
        self.data.write(filename, xml_declaration=True, encoding='utf-8')
