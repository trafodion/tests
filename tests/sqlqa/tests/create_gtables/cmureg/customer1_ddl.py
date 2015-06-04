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

def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci
    
    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()
    
    stmt = """Create table customer1 (
c_custkey           int                not null not droppable,
c_name              varchar(25)        not null not droppable,
c_address           varchar(40)        not null not droppable,
c_nationkey         int                not null not droppable,
c_phone             char(15)           not null not droppable,
c_acctbal           numeric(12,2)      not null not droppable,
c_mktsegment        char(10)           not null not droppable,
c_comment           varchar(117)       not null not droppable,
primary key (c_custkey)  not droppable)
store by primary key
attribute extent 2048, maxextents 768
hash partition (
add location """ + gvars.g_disc1 + """,
add location """ + gvars.g_disc2 + """,
add location """ + gvars.g_disc3 + """,
add location """ + gvars.g_disc4 + """)
;"""
    output = _dci.cmdexec(stmt)
