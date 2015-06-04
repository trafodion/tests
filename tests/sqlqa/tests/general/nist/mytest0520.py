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

# TEST:0520 CREATE VIEW with DISTINCT!

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
    
    #-    CREATE TABLE USIG (C1 INT, C_1 INT);
    
    #-    CREATE TABLE U_SIG (C1 INT, C_1 INT);
    stmt = """delete from usig;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 4)
    stmt = """delete from u_sig;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 0)
    
    stmt = """INSERT INTO USIG VALUES (0,2);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO USIG VALUES (1,3);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO U_SIG VALUES (4,6);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO U_SIG VALUES (5,7);"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0520 Underscores are legal an significant!
    stmt = """SELECT COUNT(*)
FROM USIG
WHERE C1 = 0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0520.exp""", """test0520a""")
    
    # PASS:0520 If count = 1?
    stmt = """SELECT COUNT(*)
FROM USIG
WHERE C1 = 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0520.exp""", """test0520b""")
    
    # PASS:0520 If count = 0?
    stmt = """SELECT COUNT(*)
FROM USIG
WHERE C_1 = 0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0520.exp""", """test0520c""")
    
    # PASS:0520 If count = 0?
    stmt = """SELECT COUNT(*)
FROM USIG
WHERE C_1 = 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0520.exp""", """test0520d""")
    
    # PASS:0520 If count = 1?
    stmt = """SELECT COUNT(*)
FROM USIG
WHERE C1 = 4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0520.exp""", """test0520e""")
    
    # PASS:0520 If count = 0?
    stmt = """SELECT COUNT(*)
FROM U_SIG
WHERE C1 = 0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0520.exp""", """test0520f""")
    
    # PASS:0520 If count = 0?
    stmt = """SELECT COUNT(*)
FROM U_SIG
WHERE C1 = 4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0520.exp""", """test0520g""")
    
    # PASS:0520 If count = 1?
    stmt = """SELECT COUNT(*)
FROM STAFF U_CN
WHERE U_CN.GRADE IN
(SELECT UCN.GRADE
FROM STAFF UCN
WHERE UCN.GRADE > 10);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0520.exp""", """test0520h""")
    
    # PASS:0520 If count = 4?
    stmt = """SELECT COUNT(*)
FROM STAFF
WHERE GRADE > 10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0520.exp""", """test0520i""")
    
    # PASS:0520 If count = 4?
    stmt = """SELECT COUNT(*)
FROM STAFF
WHERE GRADE < 10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0520.exp""", """test0520j""")
    
    # PASS:0520 If count = 0?
    
    # restore
    stmt = """ROLLBACK WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # END TEST >>> 0520 <<< END TEST;
    
