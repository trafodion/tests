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

# TEST:0156 Tables(Multi-sets), duplicate rows allowed!
def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci
    
    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()
    
    stmt = """cqd ATTEMPT_ESP_PARALLELISM 'off';"""
    output = _dci.cmdexec(stmt)
    
    # stmt = """begin work;"""
    # output = _dci.cmdexec(stmt)
    # _dci.expect_complete_msg(output)
    
    stmt = """DELETE FROM TEMP_S;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output)
    
    # setup
    stmt = """INSERT INTO TEMP_S
SELECT EMPNUM,GRADE,CITY
FROM VWSTAFF;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 5)
    # PASS:0156 If 5 rows are inserted?
    
    stmt = """SELECT COUNT(*)
FROM VWTEMP_S;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0156.exp""", """s1""")
    # PASS:0156 If count = 5?
    
    stmt = """INSERT INTO TEMP_S
SELECT EMPNUM,GRADE,CITY
FROM VWSTAFF;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8102')
    # PASS:0156 If 0 rows are inserted?
    
    stmt = """SELECT COUNT(*)
FROM VWTEMP_S;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0156.exp""", """s3""")
    # PASS:0156 If count = 5?
    
    stmt = """SELECT COUNT(DISTINCT EMPNUM)
FROM TEMP_S;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0156.exp""", """s4""")
    # PASS:0156 If count = 0?
    
    # restore
    # stmt = """ROLLBACK WORK;"""
    # output = _dci.cmdexec(stmt)
    # _dci.expect_complete_msg(output)
    stmt = """DELETE FROM TEMP_S;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output)
 
    stmt = """cqd ATTEMPT_ESP_PARALLELISM reset;"""
    output = _dci.cmdexec(stmt)
    # END TEST >>> 0156 <<< END TEST
    
