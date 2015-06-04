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
    
def test001(desc="""test032"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test032
    # jclear
    # 1999-01-14
    # Sampling tests: Varchar First-N
    #
    stmt = """select * from vwsamptb32 
where lname is not null
sample first 9 rows
sort by upperc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test032.exp""", 's1')
    # expect 9 rows with a values from 1-9 & B
    
    stmt = """select * from vwsamptb32 
where lname is null
sample first 7 rows
sort by lowerc asc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test032.exp""", 's2')
    # expect 7 rows with a values 1 3 A D G O R
    
    stmt = """select * from vwsamptb32 
sample first 11 rows
sort by upperc desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test032.exp""", 's3')
    # expect 11 rows with a values from Z-P, 36-26
    
    stmt = """select * from vwsamptb32 
sample first 12 rows
sort by lowerc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test032.exp""", 's4')
    # expect 12 rows with a values from 0-9 & AB
    
    stmt = """select * from vwsamptb32 
where lname is not null
sample first 13 rows
sort by upperc asc
order by lowerc desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test032.exp""", 's5')
    # expect 13 rows with a values from H F E C B 9 8 7 6 5 4 2 1
    
    _testmgr.testcase_end(desc)

