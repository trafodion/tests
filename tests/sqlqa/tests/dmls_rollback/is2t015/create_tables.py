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
    
    stmt = """create table t01tab (
a int not null, b largeint, c numeric(9,2) default 0.00,
d varchar(4), e char(8), f date default date '2001-09-11',
g interval hour(2) to second(2) default null
)
store by (a);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert with no rollback into t01tab values
(1,10,100,'d1','e1',date '2001-10-10',
interval '11:10:59.99' hour(2) to second(2)),
(2,20,200,'d2','e2',date '2002-10-10',
interval '12:10:59.99' hour(2) to second(2)),
(3,30,300,'d3','e3',date '2003-10-10',
interval '13:10:59.99' hour(2) to second(2))
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 3)
    
