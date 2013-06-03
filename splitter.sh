#!/bin/bash

# stop if any statement returns non-true value
set -e

get_abs_path()
{
    if [ -d $1 ] ; then
        # It's a dir
        local PARENT_DIR="$1"
        echo "`cd $PARENT_DIR; pwd`"
    else 
        # It's a file
        local PARENT_DIR=$(dirname "$1")
        echo "`cd $PARENT_DIR; pwd`/$(basename $1)"
    fi
}

usage() 
{
    cat << EOF
Usage: `basename $0` libraplus_data_filename

This script parses Libraplus data filename and splits into several files 

OPTIONS
    No options available
EOF
    exit $E_BADARGS
} 

CURR_DIR=$(get_abs_path `pwd`)

while getopts "h" opt; do
    case $opt in
        h)
            usage
            ;;
        \?)
            echo "Invalid option: -$OPTARG" >&2
            usage
            ;;
    esac
done

# Change index to read script operands
shift $((OPTIND-1)); OPTIND=1

if [ "X$1" =  "X" ]
then
    echo "libraplus data filename missing" >&2
    usage
fi

DATA_FILE=$(get_abs_path $1)

# Create log directory
WORKSPACE=$(get_abs_path `dirname "$0"`)

echo "data_file: $DATA_FILE"

cd $WORKSPACE
python workspace/euskadikokutxa/splitter.py $DATA_FILE

