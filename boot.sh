#!/bin/bash
sudo git checkout .
sudo git pull
export PYTHONPATH=.
python3 ./Bootloader/Main.py
