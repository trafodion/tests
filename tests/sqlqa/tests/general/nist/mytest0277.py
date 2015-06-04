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

# TEST:0277 Computation with NULL value specification!

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
    stmt = """UPDATE WORKS
SET HOURS = NULL  WHERE EMPNUM = 'E1';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 6)
    # PASS:0277 If 6 rows are updated?
    stmt = """UPDATE WORKS
SET HOURS = HOURS - (3 + -17);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 12)
    # PASS:0277 If 12 rows are updated?
    stmt = """UPDATE WORKS
SET HOURS = 3 / -17 * HOURS;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 12)
    # PASS:0277 If 12 rows are updated?
    stmt = """UPDATE WORKS
SET HOURS = HOURS + 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 12)
    # PASS:0277 If 12 rows are updated?
    stmt = """SELECT COUNT(*)
FROM WORKS
WHERE HOURS IS NULL;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0277.exp""", """test0277e""")
    # PASS:0277 If count = 6?
    
    # restore
    stmt = """ROLLBACK WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # END TEST >>> 0277 <<< END TEST
    
