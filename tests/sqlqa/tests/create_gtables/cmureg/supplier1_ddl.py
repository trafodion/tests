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
    
    stmt = """Create table supplier1  (
s_suppkey           int                not null not droppable,
s_name              char(25)           not null not droppable,
s_address           varchar(40)        not null not droppable,
s_nationkey         int                not null not droppable,
s_phone             char(15)           not null not droppable,
s_acctbal           numeric(12,2)      not null not droppable,
s_comment           varchar(101)       not null not droppable,
primary key (s_suppkey)  not droppable)
store by primary key
attribute extent 2048, maxextents 768
hash partition (
add location """ + gvars.g_disc1 + """,
add location """ + gvars.g_disc2 + """,
add location """ + gvars.g_disc3 + """,
add location """ + gvars.g_disc4 + """)
;"""
    output = _dci.cmdexec(stmt)
