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
    
def test001(desc="""test028"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test028
    # JClear
    # 1998-12-15
    # more first 10 tests: aggregate functions
    #
    stmt = """select count (b) from vwsamptb1 
sample first 10 rows
sort by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test028.exp""", 's1')
    # expect count = 10
    
    stmt = """select count (distinct b) from vwsamptb1 
sample first 10 rows
sort by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test028.exp""", 's2')
    # expect count = 10
    
    stmt = """select avg (b) from vwsamptb1 
sample first 10 rows
sort by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test028.exp""", 's3')
    # expect avg = 21290.20
    
    stmt = """select avg (distinct b) from vwsamptb1 
sample first 10 rows
sort by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test028.exp""", 's4')
    # expect avg = 21290.20
    
    stmt = """select min (b) from vwsamptb1 
sample first 10 rows
sort by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test028.exp""", 's5')
    # expect min = 250
    
    stmt = """select min (distinct b) from vwsamptb1 
sample first 10 rows
sort by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test028.exp""", 's6')
    # expect min = 250
    
    stmt = """select max (b) from vwsamptb1 
sample first 10 rows
sort by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test028.exp""", 's7')
    # expect max = 31145
    
    stmt = """select max (distinct b) from vwsamptb1 
sample first 10 rows
sort by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test028.exp""", 's8')
    # expect max = 31145
    
    stmt = """select sum (b) from vwsamptb1 
sample first 10 rows
sort by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test028.exp""", 's9')
    # expect sum = 212902
    
    _testmgr.testcase_end(desc)

