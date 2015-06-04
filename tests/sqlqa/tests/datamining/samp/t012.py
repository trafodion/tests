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
    
def test001(desc="""test012"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test012
    # JClear
    # 1998-11-12
    # Sampling tests: tests on a hash partitioned table (samptb4 & vwsamptb4)
    # 1. First-N
    #
    stmt = """select * from vwsamptb4 
sample first 10 rows
sort by a
order by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test012.exp""", 's1')
    # expect 10 rows with a values from 1-10
    
    stmt = """select * from vwsamptb4 
sample first 10 rows
sort by a asc
order by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test012.exp""", 's2')
    # expect 10 rows with a values from 1-10
    
    stmt = """select * from vwsamptb4 
sample first 10 rows
sort by a desc
order by a desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test012.exp""", 's3')
    # expect 10 rows with a values from 100-91
    
    stmt = """select * from vwsamptb4 
sample first 10 rows
sort by a desc
order by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test012.exp""", 's4')
    # expect 10 rows with a values from 91-100
    
    stmt = """select * from vwsamptb4 
where a between -50 and 50
sample first 10 rows
sort by a
order by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test012.exp""", 's5')
    # expect 10 rows with a values from 1-10
    
    stmt = """select avg (b) from vwsamptb4 
where a is not null and a > 0
sample first 10 rows
sort by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test012.exp""", 's6')
    # expect avg of b = 21290.2
    
    _testmgr.testcase_end(desc)

