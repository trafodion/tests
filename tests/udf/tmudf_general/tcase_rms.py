# @@@ START COPYRIGHT @@@
#
# (C) Copyright 2015 Hewlett-Packard Development Company, L.P.
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
    
def test001(desc="""TMUDF & RMS"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """select c_integer, c_char from
UDF(qaTmudfGeneral(TABLE(select * from myFullTable
partition by c_integer_unsigned order by c_integer_unsigned),
'TEST_RUNTIME_EMIT_X_ROWS',
'1')) XO;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    # Only make sure that get statistics works.
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)


