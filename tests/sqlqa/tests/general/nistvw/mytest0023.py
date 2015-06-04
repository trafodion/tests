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

# TEST:0023 DEC precision >= col.def.: ERROR if left-truncate!

# setup
def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci
    
    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()
    
    stmt = """DELETE FROM TEMP_S;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output)
    
    #      COMMIT WORK;
    
    # setup
    stmt = """INSERT INTO TEMP_S(EMPNUM,GRADE,CITY)
VALUES('E23',2323.4,'China');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    # PASS:0023 If 1 row inserted?
    
    stmt = """SELECT COUNT(*)
FROM VWTEMP_S;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0023.exp""", """s1""")
    # PASS:0023 If count = 1?
    
    # setup
    stmt = """INSERT INTO TEMP_S
VALUES('E23',23234,'China');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8411')
    # PASS:0023 If 1 row inserted or ?
    # PASS:0023 insert fails due to precision of 23234?
    
    stmt = """SELECT COUNT(*)
FROM VWTEMP_S;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0023.exp""", """s3""")
    # PASS:0023 If count = 1 or 2 (depending on previous insertion)?
    
    # restore
    #      ROLLBACK WORK;
    
    stmt = """delete from TEMP_S;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output)
    
    stmt = """select count (*) from VWTEMP_S;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0023.exp""", """s4""")
    # pass if count = 0;
    
    # END TEST >>> 0023 <<< END TEST
    
