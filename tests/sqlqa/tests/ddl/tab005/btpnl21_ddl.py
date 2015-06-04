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

# multi-column contiguous key (reverse order)
# 150,000 recs
def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci
    
    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()
    
    stmt = """Create Table btpnl21
(
ubin0_2             PIC 9(7)V9(2) COMP    not null,
sbin0_100           Numeric(18) signed    not null,
sdec0_10            PIC S9(9)             not null,
varchar0_uniq       varchar(16)      not null,
udec0_uniq          Decimal(9) unsigned   not null,
char0_10            Character(8)          not null,
char1_20            Character(32)         not null,
varchar1_4          varchar(8)       not null,
sdec1_uniq          Decimal(18) signed    not null,
sbin1_100           Numeric(4) signed     not null,
primary key  ( sbin1_100        ASC,
sdec1_uniq       ASC,
varchar1_4       DESC ) not droppable
)
store by primary key
;"""
# location """ + gvars.g_disc1 + """
# range partition (add first key  (33,0,'DAAAAAAA') location """ + gvars.g_disc2 + """,
# add first key  (67,0,'DAAAAAAA') location """ + gvars.g_disc3 + """)    
# ;"""
    output = _dci.cmdexec(stmt)
