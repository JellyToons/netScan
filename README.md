netScan
-------

# Prerequisites
  * MonogDB is installed

# Installation

* git clone https://https://github.com/bhealy/netScan.git
* pip install .

# Configuration
* In user's directory, create directory by name `.netScan`
* Create a file inside this directory and name it as `netScan.conf`
* Write your mongo URL here! As simple as that!

### Instance:
$: cat /home/bhealy/.netScan/netScan.conf
`mongo_url mongodb://localhost:27017/`

netScan
=======

## About
* netScan scans
* portScan to CPE match
* And what? Brain will map CPE to CVE and CWE.

## Database update with CPEs
  * run `python nvdcpes.py`
  * ensure mongod is running before running
  * Future iterations will include this changes from CLI instead of python script

# CONTRIBUTING

* I hold the copyright
* Contributors get the copyright too
* This project will soon have some sort of a OSS License.
* As long as it is free (OR) you can buy the author(s) beer if you get to meet them (BEERWARE LICENSE IT IS).
