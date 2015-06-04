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

# TEST:0275 COMMIT and ROLLBACK of multiple tables!

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
    
    # setup
    stmt = """INSERT INTO STAFF1
SELECT * FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 5)
    # PASS:0275 If 5 rows are inserted?
    
    # setup
    stmt = """INSERT INTO WORKS1
SELECT * FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 12)
    # PASS:0275 If 12 rows are inserted?
    
    # setup
    stmt = """INSERT INTO PROJ1
SELECT * FROM PROJ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 6)
    # PASS:0275 If 6 rows are inserted?
    stmt = """UPDATE STAFF1
SET EMPNAME = 'Aalice'
WHERE EMPNAME = 'Alice';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    # PASS:0275 If 1 row is updated?
    stmt = """UPDATE WORKS1
SET HOURS = 11
WHERE EMPNUM = 'E3';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    # PASS:0275 If 1 row is updated?
    stmt = """UPDATE PROJ1
SET PNAME = 'P9'
WHERE PNUM = 'P2';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    # PASS:0275 If 1 row is updated?
    stmt = """COMMIT WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """SELECT COUNT(*)
FROM STAFF1,WORKS1,PROJ1
WHERE STAFF1.EMPNUM = 'E3' AND
STAFF1.EMPNUM = WORKS1.EMPNUM AND
PROJ1.PNUM = WORKS1.PNUM;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0275.exp""", """test0275h""")
    # PASS:0275 If count = 1?
    
    # restore
    
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    stmt = """DELETE FROM STAFF1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 5)
    stmt = """DELETE FROM PROJ1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 6)
    stmt = """DELETE FROM WORKS1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 12)
    stmt = """COMMIT WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # END TEST >>> 0275 <<< END TEST
    
