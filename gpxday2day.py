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
data.save(dest)
print(glob.glob(root + "/*.gpx"))
