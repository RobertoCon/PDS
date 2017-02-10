#!/bin/bash
sudo git checkout .
sudo git pull
sudo chmod +x boot.sh
export PYTHONPATH=.
python3 ./Bootloader/Main.py
