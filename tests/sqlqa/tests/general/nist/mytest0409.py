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

# TEST:0409 Effective outer join -- with 2 cursors!

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
    stmt = """INSERT INTO STAFF
VALUES('E6','Lendle',17,'Potomac');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """SELECT PNUM, WORKS.EMPNUM, EMPNAME, HOURS
FROM WORKS, STAFF
WHERE STAFF.EMPNUM = WORKS.EMPNUM
ORDER BY 2, 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0409.exp""", """test0409b""")
    
    # PASS:0409 If twelve rows are selected with ROW #9 as follows?
    # PASS:0409 PNUM   WORKS.EMPNUM   EMPNAME    HOURS?
    # PASS:0409  P2         E3         Carmen     20?
    stmt = """SELECT 'ZZ', EMPNUM, EMPNAME, -99
FROM STAFF
WHERE NOT EXISTS (SELECT * FROM WORKS
WHERE WORKS.EMPNUM = STAFF.EMPNUM)
ORDER BY EMPNUM;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0409.exp""", """test0409c""")
    
    # PASS:0409 If 2 rows are selected in the following order?
    # PASS:0409 'ZZ'     STAFF.EMPNUM     EMPNAME     HOURS?
    # PASS:0409  ZZ          E5              Ed        -99?
    # PASS:0409  ZZ          E6            Lendle      -99?
    
    # restore
    stmt = """ROLLBACK WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # END TEST >>> 0409 <<< END TEST
    
