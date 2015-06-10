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

#Script Name: cplog.sh

timestamp1=$1
my_home=$2

timestamp=`date +%F\ %H:%M:%S,%3N`

node_name=`uname -a | cut -d" " -f2`
echo -e "Timestamp on this node ($node_name) is : $timestamp"

# Create destination directories, if it does not exist
$my_home/makedir.sh $timestamp1 $my_home

log_home=$my_home/logs
log_dest_dir=$log_home/$timestamp1
hbase_log_dir=/var/log/hbase
hdfs_log_dir=/var/log/hadoop/hdfs
zookeeper_log_dir=/var/log/zookeeper
#bashrc_dest_dir=$my_home/bashrc/$timestamp
#history_dest_dir=$my_home/history/$timestamp

CP_LOG=$log_dest_dir/COPY_LOGS_$timestamp1.log

if [ -s $hbase_log_dir/hbase-hbase-regionserver-*.log ]
then
	echo -e "   INFO: $node_name: Copying $hbase_log_dir/hbase-hbase-regionserver-*.log to $log_dest_dir/"
	cp $hbase_log_dir/hbase-hbase-regionserver-*.log $log_dest_dir/
	#echo $?
else
	echo -e "***DEBUG: $node_name: $hbase_log_dir/hbase-hbase-regionserver-*.log does not exist!"
fi

if [ -s $hbase_log_dir/hbase-hbase-master-*.log ]
then
	echo -e "   INFO: $node_name: Copying $hbase_log_dir/hbase-hbase-master-*.log to $log_dest_dir/"
	cp $hbase_log_dir/hbase-hbase-master-*.log $log_dest_dir/
	#echo $?
else
        echo -e "***DEBUG: $node_name: $hbase_log_dir/hbase-hbase-master-*.log does not exist!"
fi

if [ -s $zookeeper_log_dir/zookeeper.out ]
then
        echo -e "   INFO: $node_name: Copying $zookeeper_log_dir/zookeeper.out as $log_dest_dir/zookeeper_$node_name.out"
	cp $zookeeper_log_dir/zookeeper.out $log_dest_dir/zookeeper_$node_name.out
	#echo $?
else
        echo -e "***DEBUG: $node_name: $zookeeper_log_dir/zookeeper.out does not exist!"
fi

if [ -s $hdfs_log_dir/hadoop-hdfs-datanode-*.log ]
then
        echo -e "   INFO: $node_name: Copying $hdfs_log_dir/hadoop-hdfs-datanode-*.log to $log_dest_dir/"
	cp $hdfs_log_dir/hadoop-hdfs-datanode-*.log $log_dest_dir
	#echo $?
else
        echo -e "***DEBUG: $node_name: $hdfs_log_dir/hadoop-hdfs-datanode-*.log does not exist!"
fi

echo -e "\n"

if [ -d $log_dest_dir ]
then
        chmod -R 755 $log_dest_dir/*
fi

#End of file
