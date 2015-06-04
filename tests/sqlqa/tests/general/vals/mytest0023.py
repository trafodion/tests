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

# test0023
# JClear
# 1999-04-07
# VALUES tests: using NIST test0023
#
# TEST:0023 DEC precision >= col.def.: ERROR if left-truncate!

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
    _dci.expect_complete_msg(output)
    
    # setup
    stmt = """DELETE FROM TEMP_S;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output)
    
    stmt = """COMMIT WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # setup
    stmt = """INSERT INTO TEMP_S(EMPNUM,GRADE,CITY)
VALUES('E23',2323.4,'China');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    # PASS:0023 If 1 row inserted?
    
    stmt = """values ((
SELECT COUNT(*)
FROM TEMP_S
));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test023.exp""", """test023b""")
    # PASS:0023 If count = 1?
    
    # setup
    stmt = """INSERT INTO TEMP_S
VALUES('E23',23234,'China');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8411')
    # PASS:0023 If 1 row inserted or ?
    # PASS:0023 insert fails due to precision of 23234?
    
    stmt = """values ((
SELECT COUNT(*)
FROM TEMP_S
));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test023.exp""", """test023d""")
    # PASS:0023 If count = 1 or 2 (depending on previous insertion)?
    
    # restore
    #      ROLLBACK WORK;
    
    stmt = """delete from TEMP_S;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output)
    
    stmt = """values ((
select count(*) from TEMP_S
));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test023.exp""", """test023e""")
    # pass if count = 0
    
    # END TEST >>> 0023 <<< END TEST
    
