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

# TEST:0258 SELECT SUM(2*COL1*COL2) in HAVING SUM(COL2*COL3)!

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
    stmt = """INSERT INTO VTABLE
VALUES (10,11,12,13,15,5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    # PASS:0258 if 1 row is inserted?
    
    # setup
    stmt = """INSERT INTO VTABLE
VALUES (100,111,1112,113,115,6);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    # PASS:0258 if 1 row is inserted ?
    stmt = """SELECT COL1,SUM(2 * COL2 * COL3)
FROM VTABLE
GROUP BY COL1
HAVING SUM(COL2 * COL3) > 2000
OR SUM(COL2 * COL3) < -2000
ORDER BY COL1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0258.exp""", """test0258c""")
    
    # PASS:0258 If 2 rows are selected?
    # PASS:0258 If first row has values (100, 366864)    ?
    # PASS:0258 If second row has values (1000, -12000000)    ?
    
    # restore
    stmt = """ROLLBACK WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """select count (*) from vtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0258.exp""", """test0258e""")
    # pass if count = 4
    
    # END TEST >>> 0258 <<< END TEST
    
