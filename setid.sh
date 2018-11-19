#!/bin/bash

function usage() {
cat <<_EOT_
Usage:
  $0 [your_view_id]
Description:
  Set [your_view_id]
Options:
_EOT_
exit 1
}

if [ $# -ne 1 ]; then
  usage
fi

sed -i "s/^co2=.*/co2=$1/" send2monitor.ini
