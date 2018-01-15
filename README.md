# gpx-day2day
## Split Garmin archive by days

Collects the GPX data from multiple files and splits them by days.
Intended use: automatic collecting of data from archive in Garmin device 
during large bike trips and splitting by activity days for future upload.
It marks already processed Archive files by empty flag files - 
they are ignored on next run.

More precisely, the split is done by large stops. 
This is because in endurance races or large brevets, 
the rest could be any time, not necessary night.

