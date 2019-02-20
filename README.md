# nccm
KU North Campus (University of Copenhagen) Canteen Menu aggregator
## Requirements
python3 (should work out of the box)
### Python libraries
* requests
* html.parser
* pyinstaller (for installation)
## Installation
run install.sh (change the install path if needed)
## Usage
python nccm.py [-h] [-w | -t] [-c]
### optional arguments:
* -w, (--week):   show menu for week and exit
* -t, (--today):  show menu for today and exit (default)
* -h, (--help):   show help and exit
* -c, (--clean):  reduce the amount of printing
