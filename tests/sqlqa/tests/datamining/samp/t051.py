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
    
def test001(desc="""test051"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test051
    # DDunn
    # 1999-01-18
    #QA Sampling Test #DD002
    # Testing that the same set of rows are returned for each execution
    # when the FIRST and PERIODIC sampling methods are used with the
    # SORT BY option where there are not duplicates in the specified column
    # combination for the sort.
    # The results should be the same for each "first" query and the same
    # for each "periodic" query.
    #
    stmt = """select salary
from samptb051 
sample first 10 rows
sort by age
order by salary;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test051.exp""", 's1')
    # expect 10 rows with the following values in this order
    #       40000.00
    #       45000.00
    #       55000.00
    #       25000.00
    #       30000.00
    #       40000.00
    #       36000.00
    #       60000.00
    #       20050.00
    #       20000.00
    
    stmt = """select salary
from samptb051 
sample periodic 2 rows every 10 rows
sort by age
order by salary;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test051.exp""", 's2')
    # expect 8 rows with the following values in this order
    #       40000.00
    #       45000.00
    #       20050.00
    #       60000.00
    #       45000.00
    #       50000.00
    #       60000.00
    #       45000.00
    
    stmt = """select salary
from samptb051 
sample first 10 rows
sort by age
order by salary;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test051.exp""", 's3')
    # expect the same 10 rows as above
    
    stmt = """select salary
from samptb051 
sample periodic 2 rows every 10 rows
sort by age
order by salary;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test051.exp""", 's4')
    # expect the same 8 rows as above
    
    _testmgr.testcase_end(desc)

