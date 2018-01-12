import glob
import sys
import os.path

from gpxaggregator import Aggregator

try:
    root = sys.argv[1]
    dest = sys.argv[2]
except Exception:
    print("Usage: gpx-day2day <folder name> <target filename>")
    sys.exit(1)

data = Aggregator()
for i in glob.glob(root + "/Archive/*.gpx"):
    #if True:
    if not os.path.isfile(i + '.processed'):
        data.add_file(i)
        open(i + '.processed', 'a').close()# touch
data.add_file(root + "/Current/Current.gpx")

data.separate_days()
data.save(data.seg, dest)
