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

# TEST:0252 ROLLBACK cancels changes of current transaction!

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
    stmt = """DELETE FROM STAFF1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 0)
    # Making sure the table is empty
    
    # setup
    stmt = """INSERT INTO STAFF1
SELECT *
FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 5)
    # PASS:0252 If 5 rows are inserted?
    stmt = """COMMIT WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF1
VALUES('E10','Tom',50,'London');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    # PASS:0252 If 1 row is inserted?
    stmt = """UPDATE STAFF1
SET GRADE = 40
WHERE EMPNUM = 'E1';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    # PASS:0252 If 1 row is updated?
    stmt = """DELETE FROM STAFF1
WHERE EMPNUM = 'E2';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    # PASS:0252 If 1 row is deleted?
    stmt = """ROLLBACK WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    
    # verify
    stmt = """SELECT SUM(GRADE)
FROM STAFF1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0252.exp""", """test0252h""")
    # PASS:0252 If SUM(GRADE) = 60?
    
    # restore
    stmt = """DELETE FROM STAFF1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 5)
    stmt = """COMMIT WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # END TEST >>> 0252 <<< END TEST
    
