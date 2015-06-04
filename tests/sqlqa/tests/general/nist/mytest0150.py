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

# TEST:0150 CREATE Table with Unique(...), INSERT Values!

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
    stmt = """INSERT INTO WORKS1
VALUES('E1','P2',20);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # PASS:0150 If 1 row is inserted?
    stmt = """INSERT INTO WORKS1
VALUES('E1','P3',40);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # PASS:0150 If 1 row is inserted?
    stmt = """SELECT COUNT(*)
FROM  WORKS1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0150.exp""", """test0150c""")
    
    # PASS:0150 If count = 2?
    stmt = """INSERT INTO WORKS1
VALUES('E1','P2',80);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8102')
    
    # PASS:0150 If ERROR, unique constraint, 0 rows inserted?
    # NOTE:0150 Duplicates for (EMPNUM, PNUM) are not allows.
    stmt = """SELECT COUNT(*)
FROM   WORKS1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0150.exp""", """test0150e""")
    
    # PASS:0150 If count = 2?
    
    # restore
    stmt = """ROLLBACK WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # END TEST >>> 0150 <<< END TEST
    
