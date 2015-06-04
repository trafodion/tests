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
    
def test001(desc="""test062"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test062
    # DDunn
    # 1999-01-18
    # Testing periodic sampling -- number of rows returned.
    # The number should be FLOOR (N/p) * s + MIN (MOD (N,p), s)
    # The table has 13 rows,  the query calls for 2 of every 3 rows.
    # Therefore, the number of rows returned should be 9 rows.
    #
    # 1. check the available data
    stmt = """select empid from samptb062 
order by empid;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test062.exp""", 's1')
    # expect 13 rows in order with these values:
    #         123
    #        1234
    #        2345
    #        3455
    #        4567
    #        4900
    #        5678
    #        6234
    #        6789
    #        6798
    #        8901
    #        9012
    #        9123
    
    stmt = """select empid, salary
from samptb062 
sample periodic 2 rows every 3 rows
sort by empid;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test062.exp""", 's2')
    # expect 9 rows in order with these values:
    #         123     25000.00
    #        1234     20000.00
    #        3455     45000.00
    #        4567     30000.00
    #        5678     50000.00
    #        6234     20000.00
    #        6798     60000.00
    #        8901     40000.00
    #        9123     20050.00
    
    _testmgr.testcase_end(desc)

