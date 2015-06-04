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

# TEST:0026 INSERT into view with check option and unique violation!
def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci
    
    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()
    
    stmt = """SELECT COUNT(*) FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0026.exp""", """test0026a""")
    # PASS:0026 If count = 5?
    
    # setup
    stmt = """INSERT INTO TEMP_SS
SELECT EMPNUM,GRADE,CITY
FROM STAFF3
WHERE GRADE = 10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8105')
    # PASS:0026 If ERROR, view check constraint, 0 rows inserted  OR ?
    # PASS:0026 If ERROR, unique constraint, 0 rows inserted?
    stmt = """SELECT COUNT(*) FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0026.exp""", """test0026c""")
    # PASS:0026 If count = 5?
    
    # restore
    #      ROLLBACK WORK;
    
    # END TEST >>> 0026 <<< END TEST
    
