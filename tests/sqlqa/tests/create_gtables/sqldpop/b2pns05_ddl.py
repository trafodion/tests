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

# Single column Interval day to fraction(6) DESC key
# 1500 recs
def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci
    
    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()
    
    stmt = """create table b2pns05
(
date0_n10           Date
default date '01/09/2100'
heading 'date0_n10 with "default 01/09/2100"',
int0_dTOf6_uniq     Interval day to second(6)   no default not null,
char0_n2            Character(8)                no default,
sbin0_10            Largeint                    not null,
sdec0_nuniq         Decimal(4)                  ,
ubin1_10            Numeric(4) unsigned         no default not null,
udec1_nuniq         Decimal(9) unsigned         no default,
int1_d_100          Interval day                not null,
dt1_m_n10           Date                        ,
real1_500           Real                        no default not null,
primary key (int0_dTOf6_uniq DESC)
)
store by primary key
attribute extent(1024,1024), maxextents 512;"""
    output = _dci.cmdexec(stmt)
