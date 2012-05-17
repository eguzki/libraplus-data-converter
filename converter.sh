#!/bin/bash

# stop if any statement returns non-true value
set -e

get_abs_path()
{
    local PARENT_DIR=$(dirname "$1")
    echo "`cd $PARENT_DIR; pwd`/$(basename $1)"
}

usage() 
{
    cat << EOF
Usage: `basename $0` [-v] [-f logfile] [-e encoding] libraplus_data_filename"

This script parses Libraplus data filename and converts to Gesfincas format

OPTIONS
 -h Show this message
 -v verbose mode
 -f log file name
 -e encoding. Ex. latin1, utf8
EOF
    exit $E_BADARGS
} 

LOG_LEVEL="info"
LOG_FILE="log/converter_`date +%Y.%m.%d-%H.%M.%S`.log"
ENCODING="latin1"

while getopts "vf:e:h" opt; do
    case $opt in
        v)
            LOG_LEVEL="debug"
            ;;
        f)
            LOG_FILE=$OPTARG
            ;;
        e)
            ENCODING=$OPTARG
            ;;
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
mkdir -p `dirname "$LOG_FILE"`
LOG_FILE=$(get_abs_path $LOG_FILE)

echo "log_level: $LOG_LEVEL"
echo "log_file: $LOG_FILE"
echo "encoding: $ENCODING"
echo "data_file: $DATA_FILE"


#NEW_PATH="`dirname $(get_abs_path $0)`/workspace/euskadikokutxa"
#export PYTHONPATH=$PYTHONPATH:$NEW_PATH
OUTPUT_DIR="`dirname "$0"`/OUTPUT_`date +%Y.%m.%d-%H.%M.%S`"

python workspace/euskadikokutxa/converter.py -l $LOG_LEVEL -f "$LOG_FILE" -e $ENCODING -o $OUTPUT_DIR $DATA_FILE
