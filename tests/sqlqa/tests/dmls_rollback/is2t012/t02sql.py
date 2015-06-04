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
    
    stmt = """prepare s from
create table t02tabB (
a int not null, b int, c int,
d char(10), e varchar(10), f char(10),
v1 int not null,
v2 int not null,
v3 int not null,
v4 int not null,
v5 int not null
)
store by (a, v1, v2, v3, v4, v5)
AS (
select * from t12tab
transpose 10 as v1
transpose 100,22,222    as v2
transpose 1000,33,333   as v3
transpose 10000,44,444  as v4
transpose 100000,55,555 as v5
)
;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    stmt = """update statistics for table t02tabB on every column;"""
    output = _dci.cmdexec(stmt)
    
