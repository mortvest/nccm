# nccm
KU North Campus (University of Copenhagen) Canteen Menu aggregator
## Requirements
python3 
### Python libraries
* PyPDF2
* shutil
* requests
* html.parser
* pyinstaller (for installation)
## Installation
run install.sh (change the install path if needed)
## Usage
python nccm.py [-h] [-w | -t] [-c] [-d]
### optional arguments:
* -h (--help):  show this help message and exit
* -w (--week):  show menu for week and exit
* -t (--today):  show menu for today and exit (default)
* -c (--clean):  reduce the amount of printing to minimum
* -d (--debug):  print all error messages
