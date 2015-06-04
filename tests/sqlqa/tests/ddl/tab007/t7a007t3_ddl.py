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
from ...lib import gvars
import defs

_testmgr = None
_testlist = []
_dci = None

# single-column Timestamp key
# 150000 recs
# formerly b2pnl11
def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci
    
    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()
    
    stmt = """create table t7a007t3
(
int0_yTOm_uniq      Interval year(5) to month  no default not null,
sbin0_20p           Largeint                   no default not null,
sdec0_nuniq         Decimal(18)                default null,
ts0_uniq            Timestamp                  not null,
char0_uniq          Character(8)               not null,
udec1_n2            Decimal(4) unsigned        ,
dt1_yTOmin_n100     timestamp(0)               ,
real1_uniq          Real                       no default not null,
ubin1_1000          Numeric(4) unsigned        no default not null,
int1_dTOf6_n10      Interval day to second(6)  no default,
primary key (ts0_uniq   asc)
)
store by primary key;"""
    output = _dci.cmdexec(stmt)
    
