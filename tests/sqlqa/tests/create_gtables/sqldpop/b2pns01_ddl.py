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

#  1500 recs

def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci
    
    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()
    
    stmt = """create table b2pns01
(
char0_n10           Character(2)
default 'AD' heading 'char0_n10 with default AD',
sbin0_uniq          Smallint                       not null,
sdec0_n500          Decimal(18)                    ,
date0_uniq          Date                           no default not null,
int0_yTOm_nuniq     Interval year(5) to month      no default,
int1_hTOs_1000      Interval hour(2) to second     not null,
date1_n4            Date                           ,
real1_uniq          Real                           no default not null,
ubin1_n2            Numeric(4) unsigned            no default,
udec1_100           Decimal(2) unsigned            not null,
primary key (sbin0_uniq)
)
attribute extent(1024,1024), maxextents 512;"""
    output = _dci.cmdexec(stmt)
    
