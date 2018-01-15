#!/bin/sh

# Just a part of real test. Maybe make full autotest when get appropriate source archive sample
# Uses https://github.com/tinuzz/gpx-tools to measure resulting gpx files length
./gpxday2day.py /home/centurn/cen2/gpx_test /home/centurn/temp/test_gpx
for i in /home/centurn/temp/test_gpx/*.gpx; do python ~/_null/gpx-tools-master/gpx-info $i; done | grep "Total distance"

