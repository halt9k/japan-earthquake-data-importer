# Japan earthquake data importer
This script:
- unpacks in memory *.tar.gz archives with text tables (K-NET ASCII format)
- parses them
- places parsed tables into multiple auto-created Excel pages,  
based on pre-defined anchors from the template Excel file.  

This allows not just simple import, but intended to be used with custom prepared Excel template, 
which already have calculation routines figured out. 
Excel will recalcuate eveything immidiately after import without additional manual steps.
