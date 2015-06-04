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
    
    stmt = """Create Table b2unl13
(
date0_n100          Date                                   default null,
sbin0_4             Smallint                     not null,
sdec0_n100          Decimal(2)                           ,
int0_dTOf6_uniq     Interval day to second(6)     no default not null,
varchar0_n1000      varchar(8)                          no default,    

udec1_10p           Decimal(9) unsigned          not null,
real1_n100          Real                                 ,
ubin1_uniq          Numeric(9) unsigned             no default not null,
ts1_nuniq           Timestamp                                no default,
int1_yTOm_100       Interval year to month       not null,    

primary key ( int0_dTOf6_uniq ) not droppable
)
store by primary key    --  attributes audit;

;"""
    output = _dci.cmdexec(stmt)
