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

# TEST:0272 Statement rollback for integrity!

def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci
    
    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()

    # stmt = """begin work;"""
    # output = _dci.cmdexec(stmt)

    stmt = """UPDATE WORKS
SET EMPNUM = 'E7'
WHERE EMPNUM = 'E1' OR EMPNUM = 'E4';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)

    # PASS:0272 If ERROR, unique constraint, 0 rows updated?
    stmt = """INSERT INTO WORKS
SELECT 'E3',PNUM,17 FROM PROJ FOR READ COMMITTED ACCESS;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)

    # PASS:0272 If ERROR, unique constraint, 0 rows inserted?
    stmt = """UPDATE V_WORKS1
SET HOURS = HOURS - 9;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)

    # PASS:0272 If ERROR, view check constraint, 0 rows updated?
    stmt = """SELECT COUNT(*)
FROM WORKS
WHERE EMPNUM = 'E7' OR HOURS = 31 OR HOURS = 17;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0272.exp""", """test0272d""")
    # PASS:0272 If count = 0?
    
    # restore
    # stmt = """ROLLBACK WORK;"""
    # output = _dci.cmdexec(stmt)
    # _dci.expect_complete_msg(output)
    
    # END TEST >>> 0272 <<< END TEST
    
