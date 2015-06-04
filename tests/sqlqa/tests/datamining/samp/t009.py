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
    
def test001(desc="""test009"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test009
    # JClear
    # 1998-11-02
    # Sampling tests: tests on an empty table & view (samptb2 & vwsamptb2)
    # 1. First-N
    #
    # 1. First-N
    stmt = """select * from vwsamptb2 
sample first 10 rows
order by a asc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    # expect 0 rows
    
    stmt = """select * from vwsamptb2 
where a < 50
sample first 10 rows
order by a desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    # expect 0 rows
    
    stmt = """select avg (a) from vwsamptb2 
where a is not null and a > 0
sample first 10 rows
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test009.exp""", 's3')
    # expect avg = null
    
    _testmgr.testcase_end(desc)

