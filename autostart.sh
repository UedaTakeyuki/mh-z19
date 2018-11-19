#!/bin/bash

################################################################
# 
# Autostart setting
# 
# usage: ./autostart.sh --on/--off
#
#
# @author Dr. Takeyuki UEDA
# @copyright Copyright© Atelier UEDA 2018 - All rights reserved.
#
. autostart.ini
CMD=$cmd
SCRIPT_DIR=$(cd $(dirname $0); pwd)
#echo $cwd

usage_exit(){
	echo "Usage: $0 [--on]/[--off]" 1>&2
  echo "  [--on]:               Set autostart as ON. " 			1>&2
  echo "  [--off]:              Set autostart as OFF. " 		1>&2
  echo "  [--status]:           Show current status. " 		  1>&2
  exit 1
}

on(){
	sed -i "s@^WorkingDirectory=.*@WorkingDirectory=${SCRIPT_DIR}@" ${CMD}.service
	sudo ln -s ${SCRIPT_DIR}\/${CMD}.service /etc/systemd/system/${CMD}.service
	sudo systemctl daemon-reload
	sudo systemctl enable ${CMD}.service
	sudo systemctl start ${CMD}.service
}

off(){
	sudo systemctl stop ${CMD}.service
	sudo systemctl disable ${CMD}.service
}

status(){
	sudo systemctl status ${CMD}.service
}
while getopts ":-:" OPT
do
  case $OPT in
    -)
				case "${OPTARG}" in
					on)
								on
								;;
					off)
								off
								;;
					status)
								status
								;;
				esac
				;;
    \?) usage_exit
        ;;
  esac
done
