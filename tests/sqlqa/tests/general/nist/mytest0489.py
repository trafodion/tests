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

# TEST:0489 SQLSTATE 02000: no data!
def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci
    
    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()
    
    stmt = """SELECT GRADE
FROM STAFF
WHERE EMPNUM = 'xx';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    # PASS:0489 If 0 rows selected?
    # PASS:0489 OR SQLSTATE = 02000: no data OR SQLCODE = 100?
    
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    stmt = """DELETE FROM STAFF
WHERE GRADE = 11;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 0)
    
    # PASS:0489 If 0 rows deleted?
    # PASS:0489 OR SQLSTATE = 02000: no data OR SQLCODE = 100?
    stmt = """INSERT INTO STAFF (EMPNUM,GRADE)
SELECT EMPNUM, 9
FROM WORKS
WHERE PNUM = 'x9';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 0)
    
    # PASS:0489 If 0 rows inserted?
    # PASS:0489 OR SQLSTATE = 02000: no data OR SQLCODE = 100?
    stmt = """UPDATE STAFF SET CITY = 'Ho'
WHERE GRADE = 15;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 0)
    
    # PASS:0489 If 0 rows updated?
    # PASS:0489 OR SQLSTATE = 02000: no data OR SQLCODE = 100?
    
    # restore
    stmt = """ROLLBACK WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # END TEST >>> 0489 <<< END TEST
    
