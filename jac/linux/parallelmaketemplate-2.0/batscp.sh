#!/bin/bash
srcPath=$1
shift
username=$1
shift
password=$1
shift
makeInc=$1
shift
until [ $# -eq 0 ]
do
    $makeInc/autoscp.sh $srcPath $srcPath.$$$$ $username $password $1 $makeInc 1>/dev/null &
    shift
done