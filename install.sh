#!/usr/bin/bash
#change this to the desired install path
BIN_PATH="~/bin/"
pyinstaller --distpath $BIN_PATH --clean -F nccm.py
#cleanup
rm -r build/
