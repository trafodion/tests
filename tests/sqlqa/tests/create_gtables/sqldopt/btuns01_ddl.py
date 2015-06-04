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
    
    stmt = """control query default pos 'OFF';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """Create Table btuns01
(
char0_20            Character(8)          not null,
sbin0_2             Numeric(18) signed    not null,
udec0_10            Decimal(9) unsigned   not null,
varchar0_2          varchar(16)      not null,
sdec0_1000          PIC S9(9)             not null,
ubin0_20            PIC 9(7)V9(2) COMP    not null,    

char1_2             Character(16)         not null,
sdec1_uniq          Decimal(18) signed    not null,
sbin1_100           Numeric(4) signed     not null,
varchar1_uniq       varchar(8)       not null
)
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """control query default pos reset;"""
    output = _dci.cmdexec(stmt)
