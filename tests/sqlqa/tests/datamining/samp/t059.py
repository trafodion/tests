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
    
def test001(desc="""test059"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test059
    # DDunn
    # 1999-01-18
    # Testing sample FIRST
    # if we say FIRST 6 ROWS and there are more than 6 available rows,
    # then we should return only 6 rows.
    # Since we have SORT BY the same rows should be returned each time
    # we execute the same query.
    #
    stmt = """select empid, salary
from samptb058 
order by empid;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test059.exp""", 's1')
    # expect the following 10 rows in order:
    #       25000.00
    #       20000.00
    #       36000.00
    #       45000.00
    #       30000.00
    #       50000.00
    #       55000.00
    #       60000.00
    #       40000.00
    #       40000.00
    
    stmt = """select empid, salary
from samptb058 
sample first 6 rows
sort by empid;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test059.exp""", 's2')
    # expect the first 6 rows as above
    
    stmt = """select empid, salary
from samptb058 
sample first 6 rows
sort by empid desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test059.exp""", 's3')
    # expect the last 6 rows in as above
    
    _testmgr.testcase_end(desc)

