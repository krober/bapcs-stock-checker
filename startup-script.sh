#!/bin/bash

echo "Prepping project"

# get directory of script and cd - should be project root
BASE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

cd $BASE_DIR
pwd

# start python virtual env
# source $BASE_DIR/bin/activate
# echo "VENV activated"

src_dir=$BASE_DIR/src
cd $src_dir
pwd

echo "Checking logfiles"

# move current logfile to log-archives, create new logfile
file_ext=log
current_name=logfile
current_time=$(date "+%Y%m%d_%H%M")
archive_dir=$src_dir/log-archive
mkdir -p -- "$archive_dir"
mv $src_dir/$current_name.$file_ext $archive_dir/$current_name-$current_time.$file_ext
touch $current_name.$file_ext

echo "Logfiles copied/created"

# start program
# may need to edit python version depending on system

echo "Starting program..."
python3 main.py

exit 0
