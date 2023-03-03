# Japan earthquake data importer
This script:
- unpacks in memory *.tar.gz archives with text tables (K-NET ASCII format)
- parses them, converts formats and transforms rows/columns
- places parsed tables into multiple auto-created Excel pages,  
based on pre-defined anchors from the template Excel file.  

This allows not just simple import, but intended to be used with custom prepared Excel template, 
which already have calculation routines figured out. 
Excel will recalcuate eveything immidiately after import without additional manual steps.

Preview:

<p float="left"; vertical-align="top">
  <img src="https://raw.githubusercontent.com/halt9k/japan-earthquake-data-importer/main/docs/preview.png" width="400" align="center"/>
</p>
</div>
