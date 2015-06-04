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
    
def test001(desc="""test023"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test023
    # JClear
    # 1998-11-03
    # Sampling tests: oversampling first tests
    #
    stmt = """select * from vwsamptb1 
sample first 150 rows
sort by a
order by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test023.exp""", 's1')
    # expect 100 rows with a values from 1-100
    
    stmt = """select * from vwsamptb1 
sample first 200 rows
sort by a asc
order by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test023.exp""", 's2')
    # expect 100 rows with a values from 1-100
    
    stmt = """select count (*) from vwsamptb1 
sample first 1000 rows;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test023.exp""", 's3')
    # expect count = 100
    
    stmt = """select avg (b) from vwsamptb1 
sample first 200 rows;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test023.exp""", 's4')
    # expect avg of b = 14870.80
    
    stmt = """select sum (b) from vwsamptb1 
sample first 200 rows;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test023.exp""", 's5')
    # expect sum of b = 1487080
    
    _testmgr.testcase_end(desc)

