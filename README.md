# Japan earthquake data importer
This script:
- unpacks in memory *.tar.gz archives with text tables
- parses them
- places parsed tables into multiple auto-created Excel pages 

Last step uses pre-defined anchors from the template xlsx file.  
This allows not just simple import, but intended to be used with custom prepared Excel template, 
which already have calculation routines figured out. 
Excel will recalcuate eveything immidiately after improt without additional manual steps.
