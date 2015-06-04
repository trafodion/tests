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
    
def test001(desc="""test058"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test058
    # DDunn
    # 1999-01-18
    # Testing sample FIRST
    # if we use the FIRST nn rows and there are only nn - 4 available
    # then we should return the nn - 4 rows.
    #In this example, we have 10 rows inserted into the table.  We will ask for 14 rows.
    #The expected result is 10 rows.
    #
    stmt = """select cast (salary as largeint)
from samptb058 
sample first 14 rows
sort by salary desc;"""
    output = _dci.cmdexec(stmt)
    # expect 10 rows with the follownig values in order:
    #         60000
    #         55000
    #         50000
    #         45000
    #         40000
    #         40000
    #         36000
    #         30000
    #         25000
    #         20000
    
    _testmgr.testcase_end(desc)

