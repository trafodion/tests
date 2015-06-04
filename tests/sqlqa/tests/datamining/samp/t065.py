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
    
def test001(desc="""test065"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test065
    # DDunn
    # 1999-01-18
    # Testing sampling when SET LIST_COUNT is used.
    #
    stmt = """set list_count 5;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select empid, salary
from samptb051 
sample first 10 rows sort by empid;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test065.exp""", 's1')
    # expect the first 5 of these exprcted 10 rows:
    #         123     25000.00
    #        1234     20000.00
    #        2345     36000.00
    #        3455     45000.00
    #        4567     30000.00
    #        4900     45000.00
    #        4907     45000.00
    #        5678     50000.00
    #        6012     40000.00
    #        6123     25000.00
    
    stmt = """set list_count 0;"""
    output = _dci.cmdexec(stmt)
    _testmgr.testcase_end(desc)

