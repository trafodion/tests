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
    
    stmt = """Create Table b2uns07
(
sdec0_20            Decimal(4)            not null,
ts0_nuniq           Timestamp                     ,
sbin0_uniq          Smallint                 no default not null,
int0_d_uniq         Interval day(6)          no default not null,
char0_n500          Character(8)                      no default,    

double1_10          Double Precision   default 1.0004E1 not null,
ubin1_4             Numeric(4) unsigned      no default not null,
dt1_yTOmin_nuniq    Timestamp(0),
udec1_500           Decimal(4) unsigned   not null,
int1_y_nuniq        Interval year(4)              ,    

primary key ( int0_d_uniq DESC ) not droppable
)
store by primary key;"""
    output = _dci.cmdexec(stmt)
    #  attributes audit;
