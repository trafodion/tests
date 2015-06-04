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
    
def test001(desc="""test055"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test055
    # DDunn
    # 1999-01-18
    # Testing random sampling with the "clusters of N blocks" clause.
    # Specifically testing for an error condition when I specify a WHERE clause.
    # A WHERE clause along with a "clusters of N blocks" clause is illegal.
    #
    stmt = """select empid, salary
from samptb054 
where salary < 200000.00
sample random 10 percent clusters of 2 blocks;"""
    output = _dci.cmdexec(stmt)
    # expect error 7003:
    # A plan using cluster sampling could not be produced for this query.
    
    _testmgr.testcase_end(desc)

