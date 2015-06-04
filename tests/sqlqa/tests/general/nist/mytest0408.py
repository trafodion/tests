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

# TEST:0408 UPDATE references column value BEFORE update!

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
    stmt = """DELETE FROM WORKS1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 0)
    # Making sure the table is empty
    
    # setup
    stmt = """INSERT INTO WORKS1 SELECT * FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 12)
    stmt = """UPDATE WORKS1
SET HOURS = (HOURS + 3) * HOURS;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 12)
    stmt = """SELECT *
FROM WORKS1
WHERE PNUM = 'P2'
ORDER BY EMPNUM, PNUM ASC;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0408.exp""", """test0408d""")
    
    # PASS:0408 If FOR ROW #1, EMPNO1 = 'P2', PNUM1 = 'E1', HOURS1 = 460?
    # PASS:0408 If FOR ROW #2, EMPNO1 = 'P2', PNUM1 = 'E2',HOURS1 = 6640?
    # PASS:0408 If FOR ROW #3, EMPNO1 = 'P2', PNUM1 = 'E3', HOURS1 = 460?
    # PASS:0408 If FOR ROW #4, EMPNO1 = 'P2', PNUM1 = 'E4', HOURS1 = 460?
    
    # restore
    stmt = """ROLLBACK WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # END TEST >>> 0408 <<< END TEST
    
