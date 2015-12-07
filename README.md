# netScan


You'll need four things for this application to work:

1. Python-nmap which is a great tool to run nmap scans via python (which is obvious from the name). Found at: http://xael.org/pages/python-nmap-en.html
2. An NVD database that can be downloaded at: https://nvd.nist.gov/download.cfm and place them in a directory called: 'DB'. Unfortunately, these file names are hard-coded. This will eventually be changed and the README will be updated to reflect it
3. Python 2.7.*
4. A Linux platform. As the code is now, it only works on a Linux platform. This is because of the difference in finding subnet masks between Linux and other platforms

To run the application, run scan.py (ex: python scan.py). It can take awhile, so let it do its thing. And that's it!
