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

# TEST:0149 CREATE Table with NOT NULL Unique!
def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci
    
    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()
    
    stmt = """INSERT INTO PROJ1(PNUM,PNAME,BUDGET)
VALUES('P10','IRM',10000);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # PASS:0149 If 1 row is inserted ?
    stmt = """SELECT COUNT(*)
FROM PROJ1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0149.exp""", """test0149b""")
    
    # PASS:0149 If count = 1 ?
    stmt = """INSERT INTO PROJ1(PNUM,PNAME,PTYPE)
VALUES('P10','SDP','Test');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8102')
    
    # PASS:0149 If ERROR, unique constraint, 0 rows inserted?
    stmt = """SELECT COUNT(*)
FROM PROJ1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0149.exp""", """test0149d""")
    
    # PASS:0149 If count = 1?
    
    # restore
    #      ROLLBACK WORK;
    stmt = """delete from proj1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    # END TEST >>> 0149 <<< END TEST
    
