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

# TEST:0613 <datetime value function> (static)!

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
    
    stmt = """CREATE TABLE TSSMALL (
SMALLD DATE,
SMALLT TIME,
SMALLTS TIMESTAMP
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    # PASS:0613 If table is created?
    
    #-   COMMIT WORK;		XXXXX
    stmt = """INSERT INTO TSSMALL VALUES (
CURRENT_DATE,
CURRENT_TIME,
CURRENT_TIMESTAMP
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    # PASS:0613 If 1 row is inserted?
    stmt = """SELECT COUNT(*)
FROM TSSMALL WHERE
EXTRACT (YEAR FROM SMALLD) = EXTRACT (YEAR FROM SMALLTS);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0613.exp""", """test0613c""")
    
    # PASS:0613 If count = 1?
    stmt = """SELECT COUNT(*)
FROM TSSMALL WHERE
EXTRACT (MONTH FROM SMALLD) = EXTRACT (MONTH FROM SMALLTS);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0613.exp""", """test0613d""")
    # PASS:0613 If count = 1?
    stmt = """SELECT COUNT(*)
FROM TSSMALL WHERE
EXTRACT (DAY FROM SMALLD) = EXTRACT (DAY FROM SMALLTS);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0613.exp""", """test0613e""")
    
    # PASS:0613 If count = 1?
    stmt = """SELECT COUNT(*)
FROM TSSMALL WHERE
EXTRACT (HOUR FROM SMALLT) = EXTRACT (HOUR FROM SMALLTS);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0613.exp""", """test0613f""")
    
    # PASS:0613 If count = 1?
    stmt = """SELECT COUNT(*)
FROM TSSMALL WHERE
EXTRACT (MINUTE FROM SMALLT) = EXTRACT (MINUTE FROM SMALLTS);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0613.exp""", """test0613g""")
    
    # PASS:0613 If count = 1?
    stmt = """SELECT COUNT(*)
FROM TSSMALL WHERE
EXTRACT (SECOND FROM SMALLT) -
EXTRACT (SECOND FROM SMALLTS) > -1
AND EXTRACT (SECOND FROM SMALLT) -
EXTRACT (SECOND FROM SMALLTS) < 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0613.exp""", """test0613h""")
    
    # PASS:0613 If count = 1?
    
    #-   ROLLBACK WORK;		XXXXX
    
    #   DROP TABLE TSSMALL CASCADE;	-- XXXXX
    stmt = """DROP TABLE TSSMALL;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #-    COMMIT WORK;		XXXXX
    # stmt = """rollback;"""
    # output = _dci.cmdexec(stmt)
    # _dci.expect_complete_msg(output)
    
    # END TEST >>> 0613 <<< END TEST
    
