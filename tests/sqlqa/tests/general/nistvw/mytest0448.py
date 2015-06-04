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

# TEST:0448 PRIMARY KEY implies UNIQUE!
def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci
    
    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()
    
    stmt = """DELETE FROM STAFF9;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output)
    
    stmt = """INSERT INTO STAFF9(EMPNUM,EMPNAME)
VALUES('D1','Muddley');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    # PASS:0448 If 1 row inserted?
    
    stmt = """INSERT INTO STAFF9(EMPNUM,EMPNAME)
VALUES('D1','Muddley');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8102')
    # PASS:0448 If ERROR, unique constraint, 0 rows inserted?
    
    stmt = """SELECT COUNT(*)
FROM VWSTAFF9;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0448.exp""", """s2""")
    # PASS:0448 If count = 2?
    
    #    ROLLBACK WORK;
    
    stmt = """delete from VWSTAFF9;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output)
    
    # END TEST >>> 0448 <<< END TEST
    
