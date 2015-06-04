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

# TEST:0225 FIPS sizing -- ten tables in FROM clause!
# FIPS sizing TEST

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
    _dci.expect_complete_msg(output)
    
    # setup
    stmt = """DELETE FROM STAFF3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output)
    
    stmt = """INSERT INTO STAFF3
SELECT *
FROM   STAFF;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 5)
    
    stmt = """INSERT INTO TEMP_S
SELECT EMPNUM,GRADE,CITY
FROM STAFF
WHERE GRADE > 11;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 4)
    # PASS:0225 If 4 rows are inserted ?
    
    stmt = """INSERT INTO STAFF1
SELECT *
FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 5)
    # PASS:0225 If 5 rows are inserted?
    
    stmt = """INSERT INTO WORKS1
SELECT *
FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 12)
    # PASS:0225 If 12 rows are inserted?
    
    stmt = """INSERT INTO STAFF4
SELECT *
FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 5)
    # PASS:0225 If 5 rows are inserted?
    
    stmt = """INSERT INTO PROJ1
SELECT *
FROM PROJ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 6)
    # PASS:0225 If 6 rows are inserted?
    
    stmt = """SELECT STAFF.EMPNUM,PROJ.PNUM,WORKS.HOURS,
STAFF3.GRADE,STAFF4.CITY,WORKS1.HOURS,
TEMP_S.GRADE,PROJ1.PNUM,STAFF1.GRADE,
UPUNIQ.COL2
FROM   STAFF,PROJ,WORKS,STAFF3,STAFF4,WORKS1,
TEMP_S,PROJ1,STAFF1,UPUNIQ
WHERE  STAFF.EMPNUM = WORKS.EMPNUM    AND
PROJ.PNUM = WORKS.PNUM         AND
STAFF3.EMPNUM = WORKS.EMPNUM   AND
STAFF4.EMPNUM = WORKS.EMPNUM   AND
WORKS1.EMPNUM = WORKS.EMPNUM   AND
WORKS1.PNUM = WORKS.PNUM       AND
TEMP_S.EMPNUM = WORKS.EMPNUM   AND
PROJ1.PNUM = WORKS.PNUM        AND
STAFF1.EMPNUM = WORKS.EMPNUM   AND
UPUNIQ.COL2 = 'A'
ORDER BY STAFF.EMPNUM, PROJ.PNUM;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0225.exp""", """s1""")
    # PASS:0225 If 10 rows are selected ?
    # PASS:0225 If first STAFF.EMPNUM='E1',PROJ.PNUM='P1',WORKS.HOURS=40?
    # PASS:0225 If last  STAFF.EMPNUM='E4',PROJ.PNUM='P5',WORKS.HOURS=80?
    
    # restore
    stmt = """ROLLBACK WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # END TEST >>> 0225 <<< END TEST
    
