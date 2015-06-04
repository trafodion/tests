# @@@ START COPYRIGHT @@@
#
# (C) Copyright 2014 Hewlett-Packard Development Company, L.P.
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

from ...lib import hpdci
import defs

_testmgr = None
_testlist = []
_dci = None

def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci
    
    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()
    
    stmt = """Create Table b2uns09
(
char0_100           Character(5)  no default not null, -- len = 2,4
sbin0_100           Integer                     no default not null,
int0_dTOf6_n100     Interval day to second(6)          no default,
sdec0_nuniq         Decimal(9)                           no default,
time0_nuniq         Time                             ,    

dt1_mTOh_n20        Timestamp(0),
udec1_2             Decimal(9) unsigned      not null,
int1_h_n10          Interval hour(1)   default interval '8' hour,
ubin1_uniq          Numeric(9) unsigned      not null,
real1_uniq          Real                        no default not null,    

primary key  ( real1_uniq) not droppable
) no partition
store by primary key;"""
    output = _dci.cmdexec(stmt)
    #  attributes audit;
