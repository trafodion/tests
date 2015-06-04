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

# TEST:0245 FIPS sizing - precision of DECIMAL >= 15!
# FIPS sizing TEST

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
    
    stmt = """DELETE FROM PP_15;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output)
    # Making sure the table is empty
    
    # setup
    stmt = """INSERT INTO PP_15
VALUES(.123456789012345);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    # PASS:0245 If 1 row is inserted?
    
    stmt = """SELECT NUMTEST
FROM VWPP_15;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0245.exp""", """s1""")
    # PASS:0245 If NUMTEST = 0.123456789012345?
    
    stmt = """SELECT COUNT(*) FROM VWPP_15
WHERE NUMTEST = 0.123456789012345;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0245.exp""", """s2""")
    # PASS:0245 If count = 1?
    
    stmt = """DELETE FROM PP_15;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    # PASS:0245 If 1 row is deleted?
    
    # setup
    stmt = """INSERT INTO PP_15
VALUES(-.912345678901234);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    # PASS:0245 If 1 row is inserted?
    
    stmt = """SELECT COUNT(*)
FROM VWPP_15
WHERE NUMTEST = -0.912345678901234;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0245.exp""", """s3""")
    # PASS:0245 If count = 1?
    
    # restore
    stmt = """ROLLBACK WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select count (*) from VWPP_15;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0245.exp""", """s4""")
    # pass if count = 0
    
    # END TEST >>> 0245 <<< END TEST
    
