#!/bin/bash
srcPath=$1
shift
destPath=$1
shift
username=$1
shift
password=$1
shift
makeInc=$1
shift
until [ $# -eq 0 ]
do
    $makeInc/autoscp.sh $srcPath $destPath $username $password $1 1>/dev/null &
    shift
done