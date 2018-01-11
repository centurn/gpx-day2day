import glob
import sys

from gpxaggregator import Aggregator

try:
    root = sys.argv[1]
    dest = sys.argv[2]
except Exception:
    print("Usage: gpx-day2day <folder name> <target filename>")
    sys.exit(1)

data = Aggregator()
for i in glob.glob(root + "/Archive/*.gpx"):
    data.add_file(i)
data.add_file(root + "/Current/Current.gpx")

data.separate_days()
data.save(dest)
