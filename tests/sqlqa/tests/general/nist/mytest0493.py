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

# TEST:0493 SQLSTATE 22025: data exception/invalid escape seq.!

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
    stmt = """DELETE FROM CPBASE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 0)
    stmt = """INSERT INTO CPBASE
VALUES(82,'Per%X&und_');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """SELECT COUNT(*)
FROM CPBASE WHERE JUNK1
LIKE 'P%X%%X' ESCAPE 'X';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8410')
    
    # PASS:0493 If ERROR, data exception/invalid escape seq.?
    # PASS:0493 0 rows selected OR SQLSTATE = 22025 OR SQLCODE < 0?
    stmt = """SELECT COUNT(*)
FROM CPBASE WHERE JUNK1
LIKE 'P%X%%' ESCAPE 'X';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0493.exp""", """test0493d""")
    
    # PASS:0493 If count = 1?
    stmt = """INSERT INTO STAFF
SELECT 'E12','ff',KC,'gg'
FROM CPBASE
WHERE JUNK1 LIKE '%X%%Xd_' ESCAPE 'X';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8410')
    
    # PASS:0493 If ERROR, data exception/invalid escape seq.?
    # PASS:0493 0 rows inserted OR SQLSTATE = 22025 OR SQLCODE < 0?
    stmt = """INSERT INTO STAFF
SELECT 'E13','ff',KC,'gg'
FROM CPBASE
WHERE JUNK1 LIKE '%X%%X_' ESCAPE 'X';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # PASS:0493 If 1 row is inserted?
    stmt = """UPDATE CPBASE
SET KC = -1
WHERE JUNK1 LIKE '%?X%' ESCAPE '?';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8410')
    
    # PASS:0493 If ERROR, data exception/invalid escape seq.?
    # PASS:0493 0 rows updated OR SQLSTATE = 22025 OR SQLCODE < 0?
    ##expectfile ${test_dir}/test0493.exp test0493g
    stmt = """UPDATE CPBASE
SET KC = -1
WHERE JUNK1 LIKE '%?%X%' ESCAPE '?';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    # PASS:0493 If 1 row is updated?
    # gets an error, try this:
    stmt = """select * from CPBASE
WHERE JUNK1 LIKE '%?%X%' ESCAPE '?';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0493.exp""", """test0493h""")
    
    # pass if 1 row selected with VALUES(82,'Per%X&und_') as above
    stmt = """DELETE FROM CPBASE
WHERE JUNK1 LIKE '_e%&u%' ESCAPE '&';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8410')
    
    # PASS:0493 If ERROR, data exception/invalid escape seq.?
    # PASS:0493 0 rows deleted OR SQLSTATE = 22025 OR SQLCODE < 0?
    stmt = """DELETE FROM CPBASE
WHERE JUNK1 LIKE '_e%&&u%' ESCAPE '&';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    # PASS:0493 If 1 row is deleted?
    
    # restore
    stmt = """ROLLBACK WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # END TEST >>> 0493 <<< END TEST
    
