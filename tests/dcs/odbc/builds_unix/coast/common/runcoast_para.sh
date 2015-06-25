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


client=$1
sut=$2
server=$3
datasource=$4

maindir="/h/wuzho/ODBC/"
testdir=$maindir"autorun/"
alllogdir=$maindir"/coastlogs/"

env=$client"sut"$sut

case $client in
  l32|l64|lia64) ulimit -c unlimited
  ;;
esac   

case $server in
  bsa) cmd=coastwm
  ;;
  *) cmd=coast
  ;;
esac

lastlogdir=$alllogdir$server"/"
currtime=`date +%y`-`date +%m`-`date +%d`_`date +%H`-`date +%M`
logdir="Coast_"$currtime"_"$server"_"$client"_sut"$sut
mkdir $logdir 

wholelog="coast_"$server"_"$client"_sut"$sut"_all.log"
sumtext="coast_"$server"_"$client"_sut"$sut"_temp.sum"
sumtextlast="coast_"$server"_"$client"_sut"$sut"_all.sum"

. $testdir/usetup $client

while read line                                
do 
  apiname=`echo $line|awk '{print $1;}'`
  run=`echo $line|awk '{print $2;}'`
  if [[ $run = "YES" ]]
  then
    echo "****Start to run $apiname****"
    if [[ $client = "lia64" ]]
    then  
      prctl --unaligned=silent ./$cmd -d $datasource -u role.user -p hp4Binfo -c ASCII -m $env -f API $apiname
    else
      ./$cmd -d $datasource -u role.user -p hp4Binfo -c ASCII -m $env -f API $apiname 
    fi
   
   logname=`ls -tr coast*.log|tail -1`
   echo $logname|xargs cat >> $wholelog
   
   ifcore=0
   test -f core*
   if [[ $? -eq 0 ]]
   then
     corename=`ls -tr core*|tail -1`    
     mv $corename core_$apiname
     mv core_$apiname $logdir
     apisum=$apiname"	segfault	segfault"
     echo $apisum >> $sumtext
     ifcore=1
   fi
   
   if [[ $ifcore = 0 ]]
   then
     grep "Total Tests" $logname > /dev/null
     if [[ $? -eq 0 ]] 
     then
       totalNum=`grep "Total Tests" $logname|awk '{if (NF<5) print $0}'|cut -d " " -f 4|cut -d "=" -f 2`
       failedNum=`grep "Total Tests" $logname|awk '{if (NF<5) print $0}'|cut -d " " -f 6|cut -d "=" -f 2`
       apisum=$apiname"	"$totalNum"	"$failedNum
       echo $apisum >> $sumtext
     else
       apisum=$apiname"	error	error"
       echo $apisum >> $sumtext
     fi
   fi
   mv $logname $logdir   
   
  elif [[ $run = "NO" ]]
  then
    echo "***Do not need to run $apiname***"
     apisum=$apiname"	norun	norun"
     echo $apisum >> $sumtext
  fi
                                
done<tests

cd $logdir                                                                                        
grep "Total Tests" coast_*log|sed 's/=./=/g' |grep -v "Failed=0"|cut -f 2- |awk '{if (NF>4) print $0}'  > failedAPIs.sum
grep "Total Tests" coast_*log|sed 's/=./=/g' |grep "Failed=0"|cut -f 2- |awk '{if (NF>4) print $0}'  > successedAPIs.sum
ls -tr core* > coreAPIs.sum

cd ..                                                                        
mv $wholelog $logdir
mv $sumtext $logdir
mv tracefile* $logdir

cd $logdir
grep "Total Tests" $wholelog |sed 's/=./=/g' |cut -f 2- |awk '{if (NF>4) print $0}'  > allAPIs.sum 
awk  '{for(i=1;i<=NF;i++) if(i!=NF) printf("%-25s",$i); else print $i}' $sumtext >> $sumtextlast 
rm $sumtext
echo $server" "$client
cat $sumtextlast
cd ..
chmod 777 $logdir
mv $logdir $lastlogdir
                                            