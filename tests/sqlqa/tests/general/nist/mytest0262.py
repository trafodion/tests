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

# TEST:0262 WHERE clause with computation, ANY/ALL subqueries!

def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci
    
    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()
    
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    stmt = """UPDATE VTABLE
SET COL1 = 1
WHERE COL1 = 0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    # PASS:0262 If 1 row is updated?
    stmt = """SELECT COL1, COL2
FROM VTABLE
WHERE (COL3 * COL2/COL1) > ALL
(SELECT HOURS FROM WORKS)
OR -(COL3 * COL2/COL1) > ANY
(SELECT HOURS FROM WORKS)
ORDER BY COL1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0262.exp""", """test0262b""")
    # PASS:0262 If 2 rows are selected?
    # PASS:0262 If first row is  ( 100,   200)?
    # PASS:0262 If second row is (1000, -2000)?
    
    # restore
    stmt = """ROLLBACK WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # END TEST >>> 0262 <<< END TEST
    
