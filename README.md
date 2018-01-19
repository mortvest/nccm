# nccm
North Campus (University of Copenhagen) Canteen Menu aggregator
## Requirements
python3.6 (should work out of the box)
### Python libraries
* requests
* html.parser
## Usage
python nccm.py [-h] [-w | -t] [-c]
### optional arguments:
* -w, (--week):   show menu for week and exit
* -t, (--today):  show menu for today and exit (default)
* -h, (--help):   show help and exit
* -c, (--clean):  reduce the amount of printing
