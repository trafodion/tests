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
    
def test001(desc="""test082"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test082
    # DDunn
    # 1999-01-18
    # Test balance with First-N sampling with ROWS SINCE.
    #
    stmt = """select rows since (I1 is null) as ROWS_SINCE_NULL
from samptb082 
sequence by i3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test082.exp""", 's1')
    # expect 1 null followed by two ones & numbers 2-10
    
    stmt = """select rows since (I1 is null) as ROWS_SINCE_NULL
from samptb082 
sample first 5 rows sort by i3
sequence by i3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test082.exp""", 's2')
    # expect 1 null followed by two ones & numbers 2-3
    
    stmt = """select rows since (I1 is not null) as ROWS_SINCE_NULL
from samptb082 
sample first 5 rows sort by i3
sequence by i3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test082.exp""", 's3')
    # expect 3 nulls followed by two 1's
    
    stmt = """select rows since (not I1 is null) as ROWS_SINCE_NULL
from samptb082 
sample first 5 rows sort by i3
sequence by i3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test082.exp""", 's4')
    # expect 3 nulls followed by two 1's
    
    _testmgr.testcase_end(desc)

