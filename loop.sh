#!/bin/bash
SCRIPT_DIR=$(cd $(dirname $0); pwd)
while true; do sudo python ${SCRIPT_DIR}/read.py; sleep 5m; done
