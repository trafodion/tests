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
    
def test001(desc="""test102"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test102
    # Negative test for DIFF 2-argument functions
    # Diff used on identical values or constants should get a divide by zero error
    #	TCB tree error from DIFF functions when run on identical values
    #
    stmt = """create table seqtb102 (a int, b int, c int not null primary key);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into seqtb102 values (1, 1,1), (1, 1,2), (1, 1,3);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select diff1 (a, b) from seqtb102 sequence by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8419')
    
    stmt = """select diff2 (a, b) from seqtb102 sequence by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8419')
    
    stmt = """select diff1 (a, 2) from seqtb102 sequence by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8419')
    
    stmt = """select diff2 (a, 2) from seqtb102 sequence by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8419')
    
    _testmgr.testcase_end(desc)

