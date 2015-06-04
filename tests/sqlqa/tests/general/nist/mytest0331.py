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

# TEST:0331 (2 pr.,1 son),modify F.K to P.K corr. value!

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
    stmt = """DELETE  FROM WORKS3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 0)
    stmt = """DELETE  FROM STAFF3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 0)
    stmt = """DELETE  FROM PROJ3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 0)
    stmt = """INSERT INTO STAFF3
SELECT * FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 5)
    stmt = """INSERT INTO PROJ3
SELECT * FROM PROJ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 6)
    stmt = """INSERT INTO WORKS3
SELECT * FROM WORKS
where EMPNUM = 'E1' and PNUM = 'P1'
or EMPNUM = 'E2' and PNUM = 'P1'
or EMPNUM = 'E3' and PNUM = 'P2'
or EMPNUM = 'E4' and PNUM = 'P2';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 4)
    stmt = """SELECT COUNT(*) FROM WORKS
WHERE EMPNUM = 'E1';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0331.exp""", """test0331g""")
    # PASS:0331 If count = 6?
    stmt = """UPDATE WORKS3
SET PNUM = 'P2'
WHERE PNUM = 'P1';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 2)
    stmt = """SELECT COUNT(*) FROM WORKS3
WHERE PNUM = 'P1';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0331.exp""", """test0331i""")
    # PASS:0331 If count = 0?
    
    #-   COMMIT WORK;
    
    # cleanup
    stmt = """rollback work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # END TEST >>> 0331 <<< END TEST
    
