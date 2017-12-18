import glob
import sys

from gpxaggregator import Aggregator

try:
    root = sys.argv[1]
    dest = sys.argv[2]
except Exception:
    print("Usage: gpx-day2day <folder name> <target filename>")
    sys.exit(1)

data = Aggregator(root + "/Current/Current.gpx")
for i in reversed(glob.glob(root + "/Archive/*.gpx")):
    data.add_file(i)
data.save(dest)
#print(glob.glob(root + "Archive/*.gpx"))
