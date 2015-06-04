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
    
def test001(desc="""test028"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # testx028
    # jclear
    # 1997-05-05
    # Extra tests on NIST database
    #
    stmt = """select empname from STAFF 
where grade = 12
and empname <> 'Don';	-- legal operator <>"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test028.exp""", 's1')
    # should return 'Alice'
    
    stmt = """select empname from STAFF 
where grade = 12
and empname != 'Don';	-- illegal operator !="""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test028.exp""", 's2')
    # should return 'Alice'
    #
    
    stmt = """select empname from VWSTAFF 
where grade = 12
and empname <> 'Don';	-- legal operator <>"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test028.exp""", 's3')
    # should return 'Alice'
    
    stmt = """select empname from VWSTAFF 
where grade = 12
and empname != 'Don';	-- illegal operator !="""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test028.exp""", 's4')
    # should return 'Alice'
    #
    
    _testmgr.testcase_end(desc)

