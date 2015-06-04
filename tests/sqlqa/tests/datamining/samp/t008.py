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
    
def test001(desc="""test008"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test008
    # JClear
    # 1998-11-11
    # Sampling tests: tests on a vertically partitioned table (samptb3 & vwsamptb3)
    # Periodic sampling (with variations on SORT BY)
    #
    stmt = """select * from vwsamptb3 
sample periodic 5 rows every 20 rows
sort by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test008.exp""", 's1')
    # expect 25 rows with a values from 1-5, 21-25, 41-45, 61-65 & 81-85
    
    stmt = """select * from vwsamptb3 
where a is not null
sample periodic 5 rows every 20 rows
sort by a asc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test008.exp""", 's2')
    # expect 25 rows with a values from 1-5, 21-25, 41-45, 61-65 & 81-85
    
    stmt = """select * from vwsamptb3 
sample periodic 5 rows every 20 rows
sort by a desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test008.exp""", 's3')
    # expect 25 rows with a values from 100-96, 80-76, 60-56, 40-36 & 20-16
    
    stmt = """select * from vwsamptb3 
sample periodic 5 rows every 20 rows
sort by a
order by a desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test008.exp""", 's4')
    # expect 25 rows with a values from 85-81, 65-61, 45-41, 25-21, 5-1
    _testmgr.testcase_end(desc)

