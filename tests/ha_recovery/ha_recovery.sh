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

#Script Name: ha_recovery.sh

function verifyNodeAccessibility
{
	node_count=$(echo $1 | wc -w)
	if [ $node_count -gt 1 ]
	then
		PDSH_CMD="pdsh -S $MY_NODES"
	else
		if [ $node_count -eq 0 ]; then
	                echo -e "Environment variable NODE_LIST is not defined or is empty"
	        else
	                PDSH_CMD=""
	        fi
	fi

	bad_nodes=""
	MY_NODES=""

	for node in $1
	do
		# Use BatchMode so it just gives an error instead of prompting for the password
		ssh -oStrictHostKeyChecking=no -oBatchMode=yes $node hostname &> /dev/null

		if [ $? != 0 ]; then
			bad_nodes="$bad_nodes $node"
			echo -e "***DEBUG: Node $node is NOT accessible!"

			if [ $node == $1 ]
			then
				echo -e "***ERROR: Script aborted!"
				exit -1
			fi
		else
			echo -e "Node $node is accessible..."
		fi

		# Build MY_NODES environment variable
		MY_NODES="$MY_NODES -w $node"
	done

	if [ -n "$bad_nodes" ]; then
		echo -e "***DEBUG: Unable to access all nodes in the node list with passwordless ssh!"
		echo -e "***DEBUG: Problem nodes: $bad_nodes \n"
	fi
}

function validateInputs
{
	input_string="$(echo -e "$1" | sed -e 's/[[:space:]]*$//')"
	input_length_temp=`echo $input_string | wc -m`
	input_length=`expr $input_length_temp - 1`

	#Verify HRegionServer process
	if [ $input_length -lt 1 ]; then
	        echo -e "***ERROR: Please provide which node's HRegionServer you want to kill."
	        exit
	else
	        rs_node=$1
	        rs_exist=`pdsh -w $rs_node "jps | grep 'HRegionServer' | wc -l" | awk '{print $2}'`

	        if [ $rs_exist -lt 1 ]
	        then
	                echo -e "***DEBUG: HRegionServer does not exist on node $rs_node!"
	                exit -1
	        else
	                if [ $rs_exist -gt 1 ]
	                then
	                        echo -e "***DEBUG: More than one HRegionServer exist on node $rs_node!"
	                        exit -1
	                fi
	        fi
	fi
}

function killRS
{
	rs_node=$1
	rs_pid=$2
	rs_node_date=`pdsh -w $rs_node "date +%F" | awk '{print $2}'`
	rs_node_hour=`pdsh -w $rs_node "date +%H" | awk '{print $2}'`
	rs_node_min=`pdsh -w $rs_node "date +%M" | awk '{print $2}'`
	rs_node_sec=`pdsh -w $rs_node "date +%S" | awk '{print $2}'`
	rs_node_nano=`pdsh -w $rs_node "date +%3N" | awk '{print $2}'`

	rs_kill_time_min="$rs_node_date $rs_node_hour:$rs_node_min"
	rs_kill_time_sec="$rs_kill_time_min:$rs_node_sec"
	rs_kill_time_nano="$rs_kill_time_sec,$rs_node_nano"

	echo -e "INFO: Killing PID $rs_pid on node $rs_node at $rs_kill_time_nano"
	pdsh -w $rs_node "kill -9 $rs_pid"
}

input_node=$1
table_name=$2
timestamp1=`date +%F_%H-%M`
my_home=$PWD
log_home=$my_home/logs
log_dest_dir=$log_home/$timestamp1
current_node=`uname -a | cut -d" " -f2`

echo -e "\n"
echo -e "INFO: Executing $my_home/ha.sh on from $current_node..."

# Validate provided input values
echo -e "INFO: Checking validity of input node: $input_node"
validateInputs "$input_node"

# Verify accessibility of a node using passwordless ssh
echo -e "INFO: Checking accessibility of each node in: $NODE_LIST"
verifyNodeAccessibility "$NODE_LIST"

# Create log directories
echo -e "\n"
$my_home/makedir.sh $timestamp1 $my_home

CP_LOG=$log_dest_dir/copy_log_$timestamp1.log
touch $CP_LOG
chmod 755 $CP_LOG

echo -e "\n"
echo -e "INFO: Copy log is available in $log_dest_dir/copy_log_$timestamp1.log file"

hregion_server_old_log=$log_dest_dir/hregion_server_old_$timestamp1.log
hregion_server_new_log=$log_dest_dir/hregion_server_new_$timestamp1.log
hregion_info_old_log=$log_dest_dir/hregion_info_old_$timestamp1.log
hregion_info_new_log=$log_dest_dir/hregion_info_new_$timestamp1.log

echo -e "\n"
echo -e "INFO: Executing $my_home/get_sys_info.sh..."
pdsh $MY_NODES $my_home/get_sys_info.sh $my_home $timestamp1
echo -e "INFO: Execution of $my_home/get_sys_info.sh finished."

echo -e "\n"
echo -e "INFO: Executing HBase Shell commands..."
echo -e "\nINFO: Executing HBase Shell commands..." >> $CP_LOG

echo -e "INFO: Details of HBase server info is stored in $hregion_server_old_log \n" >> $CP_LOG
hbase shell $my_home/hshell_server.sh >> $hregion_server_old_log

echo -e "\n" >> $CP_LOG
echo -e "############################################################################################################### \n" >> $CP_LOG
echo -e "\n" >> $CP_LOG

region_num_old=`cat $hregion_server_old_log | grep $table_name | wc -l`
rserver_num_old=`cat $hregion_server_old_log | grep $table_name | awk '!x[$4]++' | awk '{print $4}' FS="=" | awk '{print $1}' FS="." | wc -l`
echo -e "\nINFO: Table $table_name has $region_num_old regions on $rserver_num_old nodes:"
cat $hregion_server_old_log | grep $table_name | awk '!x[$4]++' | awk '{print $4}' FS="=" | awk '{print $1}' FS="."

rs_pid=`grep -E "HRegionServer" $log_dest_dir/sys_info_$input_node.log | cut -d' ' -f1`
echo -e "\n"
echo "INFO: Killing HRegionServer (PID $rs_pid) on $input_node..."
killRS $input_node $rs_pid
echo "INFO: HRegionServer (PID $rs_pid) on $input_node has been killed successfully."

echo -e "\n"
wait_sec=60
echo -e "INFO: Regions are being moved. Waiting for $wait_sec seconds..."
sleep $wait_sec

echo -e "\n"
echo -e "INFO: Executing $my_home/cplog.sh on $current_node..."
pdsh $MY_NODES $my_home/cplog.sh $timestamp1 $my_home | dshbak >> $CP_LOG
echo -e "INFO: Execution of $my_home/cplog.sh on $current_node finished."
echo -e "INFO: Log files copied under $my_home/logs/$timestamp1"

echo -e "***** Contents of $log_dest_dir directory *****" >> $CP_LOG
ls -la $log_dest_dir >> $CP_LOG

chmod -R 755 $log_dest_dir
echo -e "\nINFO: Log destination directory: $log_dest_dir"
echo -e "\n"

echo -e "INFO: Executing HBase Shell commands..."
echo -e "\nINFO: Executing HBase Shell commands..." >> $CP_LOG
echo -e "INFO: Details of HBase server info is stored in $hregion_server_new_log \n" >> $CP_LOG

#Add the code to check availability of regionserver before execute hbase shell command
hbase shell $my_home/hshell_server.sh >> $hregion_server_new_log

hmaster_log_date=`grep -E "^${rs_kill_time_min}.* DISCONNECTING" $log_dest_dir/hbase-hbase-master-*.log | cut -d' ' -f1`
hmaster_log_time=`grep -E "^${rs_kill_time_min}.* DISCONNECTING" $log_dest_dir/hbase-hbase-master-*.log | cut -d' ' -f2`

echo -e "\n"
echo -e "INFO: HRegionServer on $input_node was killed at $rs_kill_time_nano"
echo -e "INFO: The event was notified to HBaseMaster at $hmaster_log_date $hmaster_log_time"

echo -e "\n"
wait_sec=30
echo -e "INFO: Waiting for $wait_sec seconds..."
sleep $wait_sec

last_region_up_date=`cat $log_dest_dir/hbase-hbase-master-*.log | grep 'Onlined ' | grep "$table_name" | awk 'END{print}' | cut -d' ' -f1`
last_region_up_time=`cat $log_dest_dir/hbase-hbase-master-*.log | grep 'Onlined ' | grep "$table_name" | awk 'END{print}' | cut -d' ' -f2`
echo "INFO: All regions for table $table_name came up at $last_region_up_date $last_region_up_time"

region_num_new=`cat $hregion_server_new_log | grep $table_name | wc -l`
rserver_num_new=`cat $hregion_server_new_log | grep $table_name | awk '!x[$4]++' | awk '{print $4}' FS="=" | awk '{print $1}' FS="." | wc -l`

echo -e "\nINFO: Table $table_name has $region_num_new regions on $rserver_num_new nodes:"
cat $hregion_server_new_log | grep $table_name | awk '!x[$4]++' | awk '{print $4}' FS="=" | awk '{print $1}' FS="."

echo -e "\n*** End of the script *** \n"

#End of file
