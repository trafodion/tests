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

# TEST:0285 INSERT, SELECT integer with various formats!

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
    
    #-   INSERT INTO STAFF(EMPNUM,GRADE)      -- XXXXXX
    #-          VALUES ('E6',25);
    stmt = """INSERT INTO STAFF(EMPNUM,EMPNAME,GRADE,CITY)
VALUES ('E6', null, 25, null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    #-   INSERT INTO STAFF(EMPNUM,GRADE)      -- XXXXXX
    #-          VALUES ('E7',25.0);
    stmt = """INSERT INTO STAFF(EMPNUM,EMPNAME,GRADE,CITY)
VALUES ('E7', null, 25.0, null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    #-   INSERT INTO STAFF(EMPNUM,GRADE)      -- XXXXXX
    #-          VALUES ('E8',-25);
    stmt = """INSERT INTO STAFF(EMPNUM,EMPNAME,GRADE,CITY)
VALUES ('E8', null, -25, null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    #-   INSERT INTO STAFF(EMPNUM,GRADE)      -- XXXXXX
    #-          VALUES ('E9',25.000);
    stmt = """INSERT INTO STAFF(EMPNUM,EMPNAME,GRADE,CITY)
VALUES ('E9', null, 25.000, null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """UPDATE STAFF
SET GRADE = -GRADE
WHERE GRADE < 0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """SELECT COUNT(*) FROM VWSTAFF
WHERE GRADE = 25;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0285.exp""", """s1""")
    
    # PASS:0285 If count = 4?
    
    # restore
    stmt = """ROLLBACK WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select count (*) from VWSTAFF;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0285.exp""", """s2""")
    # pass if count = 5
    
    # END TEST >>> 0285 <<< END TEST
    
