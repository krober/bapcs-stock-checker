#!/bin/bash

# get directory of script and cd - should be project root
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# start python virtual env
source ./bin/activate

cd $DIR/src

# move current logfile to log-archives, create new logfile
file_ext=log
current_name=logfile.$file_ext
current_time=$(date "%Y%m%d_%H%M")
archive_dir=./log-archive
mkdir -p -- "$backup_dir"
mv ./$current_name.$file_ext $backup_dir/$current_name-$current_time.$file_ext
touch $current_name.$file_ext

# start program
# may need to edit python version depending on system
python3.6 main.py

exit 0
