#!/bin/bash
# @@@ START COPYRIGHT @@@
#
# (C) Copyright 2015 Hewlett-Packard Development Company, L.P.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
# @@@ END COPYRIGHT @@@

#Script Name: ha_config.sh

function makeDir
{
        echo -e "INFO: Creating $1 directory."
        mkdir $1 &> /dev/null
        chmod -R 755 $1
}

function existDir
{
        echo -e "INFO: Directory $1 already exist!"
	chmod -R 755 $1
}

timestamp1=$1
my_home=$2

log_home=$my_home/logs
if [ ! -d $log_home ]
then
        makeDir "$log_home"
else
        existDir "$log_home"
fi

log_dest_dir=$log_home/$timestamp1
if [ ! -d $log_dest_dir ]
then
        makeDir "$log_dest_dir"
else
        existDir "$log_dest_dir"
fi

