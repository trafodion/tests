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

#Script Name: get_sys_info.sh

my_home=$1
timestamp1=$2
log_home=$my_home/logs
log_dest_dir=$log_home/$timestamp1
node_name=`uname -a | cut -d" " -f2`
SYS_INFO_LOG=$log_dest_dir/sys_info_$node_name.log

echo -e "INFO: Executing $my_home/get_sys_info.sh on node $node_name..." >> $SYS_INFO_LOG

echo -e "\n ********************* Output of the command: jps *********************" >> $SYS_INFO_LOG
echo -e "System info of node $node_name is available in $SYS_INFO_LOG"
date '+%Y-%m-%d_%H.%M.%S' >> $SYS_INFO_LOG
jps >> $SYS_INFO_LOG

date '+%Y-%m-%d_%H.%M.%S' >> $SYS_INFO_LOG
echo -e "\n ********************* Output of the command: jps *********************" >> $SYS_INFO_LOG

date '+%Y-%m-%d_%H.%M.%S' >> $SYS_INFO_LOG
echo -e "\n ********************* Output of the command: netstat -anp | sed '/^.*:2181[ ]*ESTABLISHED.*/!d' *********************" >> $SYS_INFO_LOG
netstat -anp | sed '/^.*:2181[ ]*ESTABLISHED.*/!d' >> $SYS_INFO_LOG

date '+%Y-%m-%d_%H.%M.%S' >> $SYS_INFO_LOG
echo -e "\n ********************* Output of the command: netstat -anp | sed '/^.*:60000[ ]*ESTABLISHED.*/!d' *********************" >> $SYS_INFO_LOG
netstat -anp | sed '/^.*:60000[ ]*ESTABLISHED.*/!d' >> $SYS_INFO_LOG

date '+%Y-%m-%d_%H.%M.%S' >> $SYS_INFO_LOG
echo -e "\n ********************* Output of the command: netstat -anp | sed '/^.*:60020[ ]*ESTABLISHED.*/!d' *********************" >> $SYS_INFO_LOG
netstat -anp | sed '/^.*:60020[ ]*ESTABLISHED.*/!d' >> $SYS_INFO_LOG

date '+%Y-%m-%d_%H.%M.%S' >> $SYS_INFO_LOG
echo -e "\n ********************* Output of the command: netstat -anp | sed '/^.*:50010[ ]*ESTABLISHED.*/!d' *********************" >> $SYS_INFO_LOG
netstat -anp | sed '/^.*:50010[ ]*ESTABLISHED.*/!d' >> $SYS_INFO_LOG

date '+%Y-%m-%d_%H.%M.%S' >> $SYS_INFO_LOG
echo -e "\n ********************* Output of the command: netstat -anp | sed '/^.*:8020[ ]*ESTABLISHED.*/!d' *********************" >> $SYS_INFO_LOG
netstat -anp | sed '/^.*:8020[ ]*ESTABLISHED.*/!d' >> $SYS_INFO_LOG

#date '+%Y-%m-%d_%H.%M.%S' >> $SYS_INFO_LOG
#echo -e "\n ********************* Output of the command: jps | grep 'HMaster' *********************" >> $SYS_INFO_LOG
#jps | grep 'HMaster' >> $SYS_INFO_LOG

#date '+%Y-%m-%d_%H.%M.%S' >> $SYS_INFO_LOG
#echo -e "\n ********************* Output of the command: jps | grep 'HRegionServer' *********************" >> $SYS_INFO_LOG
#jps | grep 'HRegionServer' >> $SYS_INFO_LOG

#date '+%Y-%m-%d_%H.%M.%S' >> $SYS_INFO_LOG
#echo -e "\n ********************* Output of the command: jps | grep 'QuorumPeerMain' *********************" >> $SYS_INFO_LOG
#jps | grep 'QuorumPeerMain'

#date '+%Y-%m-%d_%H.%M.%S'
#echo -e "\n ********************* Output of the command: jps | grep 'NameNode' *********************" >> $SYS_INFO_LOG
#jps | grep 'NameNode'

#date '+%Y-%m-%d_%H.%M.%S'
#echo -e "\n ********************* Output of the command: jps | grep 'DataNode' *********************" >> $SYS_INFO_LOG
#jps | grep 'DataNode'

#date '+%Y-%m-%d_%H.%M.%S'
#echo -e "\n ********************* Output of the command: jps | grep 'NodeManager' *********************" >> $SYS_INFO_LOG
#jps | grep 'NodeManager'

#date '+%Y-%m-%d_%H.%M.%S'
#echo -e "\n ********************* Output of the command: jps | grep 'AmbariServer' *********************" >> $SYS_INFO_LOG
#jps | grep 'AmbariServer'

#End of file
