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

# TEST:0120 Value expression with NULL primary IS NULL!

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
    stmt = """INSERT INTO WORKS1
SELECT *
FROM VWWORKS;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 12)
    # PASS:0120 If 12 rows are inserted ?
    
    # setup
    stmt = """INSERT INTO WORKS1
VALUES('E9','P1',NULL);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    # PASS:0120 If 1 row is inserted?
    
    stmt = """SELECT EMPNUM
FROM VWWORKS1
WHERE HOURS IS NULL;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0120.exp""", """s1""")
    # PASS:0120 If EMPNUM = 'E9'?
    
    # NOTE:0120 we insert into WORKS from VWWORKS1
    
    # setup
    stmt = """INSERT INTO WORKS
SELECT EMPNUM,'P9',20+HOURS
FROM VWWORKS1
WHERE EMPNUM='E9';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    # PASS:0120 If 1 row is inserted?
    
    stmt = """SELECT COUNT(*)
FROM VWWORKS
WHERE EMPNUM='E9';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0120.exp""", """s2""")
    # PASS:0120 If count = 1      ?
    
    stmt = """SELECT COUNT(*)
FROM VWWORKS
WHERE HOURS IS NULL;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0120.exp""", """s3""")
    # PASS:0120 If count = 1 ?
    
    # restore
    stmt = """ROLLBACK WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select count (*) from VWWORKS;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0120.exp""", """s4""")
    # pass if count = 12
    
    stmt = """select count (*) from VWWORKS1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0120.exp""", """s5""")
    # pass if count = 0
    
    # END TEST >>> 0120 <<< END TEST
    
