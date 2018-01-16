#!/usr/bin/env python3

import glob
import sys
import os.path

from gpxaggregator import Aggregator

try:
    root = sys.argv[1]
    dest = sys.argv[2]
except Exception:
    print("Usage: gpx-day2day <source dir> <target dir>")
    sys.exit(1)

data = Aggregator()
for i in sorted(glob.glob(root + "/Archive/*.gpx")):
    #if True:
    if not os.path.isfile(i + '.processed'):
        data.add_file(i)
        open(i + '.processed', 'a').close()# touch
i = root + "/Current/Current.gpx"
if os.path.isfile(i):
    data.add_file(i)

#data.save(data.seg, dest + '/test.gpx')
data.separate_days(dest)
