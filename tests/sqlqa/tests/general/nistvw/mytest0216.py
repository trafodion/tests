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

# TEST:0216 FIPS sizing -- 120 bytes in a UNIQUE constraint!
# FIPS sizing TEST
#      for the other things it does, and to check for the Unique warning (jc)

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
    
    stmt = """DELETE FROM T4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output)
    # Making sure the table is empty
    
    # setup
    stmt = """INSERT INTO T4 VALUES (
'This test is trying to test the limit on the total length of an index',
-123456, 'which is','not less than 120');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    # PASS:0216 If 1 row is inserted?
    
    stmt = """INSERT INTO T4 VALUES (
'This test is trying to test the limit on the total length of an index',
-123456,'which is','not less than 120');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8102')
    # PASS:0216 If ERROR, unique constraint, 0 rows inserted?
    
    stmt = """SELECT STR110
FROM VWT4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0216.exp""", """s2""")
    # PASS:0216 If STR110 starts with 'This test is trying to test the '?
    # PASS:0216 and ends with 'limit on the total length of an index'?
    
    # restore
    #     ROLLBACK WORK;
    
    stmt = """delete from VWT4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
