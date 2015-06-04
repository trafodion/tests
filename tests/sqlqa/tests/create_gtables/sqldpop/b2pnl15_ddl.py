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

# Single column Double key
# 150000 recs
def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci
    
    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()
    
    stmt = """create table b2pnl15
(
char0_100           Character(8)             not null,
sbin0_uniq          Integer                  not null,
sdec0_n10           Decimal(4)               default 9,
int0_yTOm_n1000     Interval year(2) to month         no default,
date0_nuniq         Date                     no default,
real1_uniq          Real                     not null,
ts1_n100            Timestamp                ,
ubin1_500           Numeric(4) unsigned      no default not null,
int1_dTOf6_nuniq    Interval day to second(6)       no default,
udec1_50p           Decimal(9) unsigned      not null,
primary key ( real1_uniq )
) no partition
store by primary key
attribute extent(1024,1024), maxextents 512;"""
    output = _dci.cmdexec(stmt)
