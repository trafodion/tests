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

# TEST:0248 FIPS sizing - binary precision of FLOAT >= 20!

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
    
    # FIPS sizing TEST
    stmt = """DELETE FROM JJ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 0)
    # Making sure the table is empty
    
    # setup
    stmt = """INSERT INTO JJ
VALUES(0.1048575,1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    # PASS:0248 If 1 row is inserted?
    stmt = """SELECT FLOATTEST
FROM JJ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0248.exp""", """test0248c""")
    # PASS:0248 If FLOATTEST = 0.1048575 ?
    # PASS:0248 OR  is between 0.1048574 and 0.1048576 ?
    stmt = """SELECT COUNT(*) FROM JJ
WHERE FLOATTEST > 0.1048574 AND FLOATTEST < 0.1048576;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0248.exp""", """test0248d""")
    # PASS:0248 If count = 1?
    stmt = """DELETE FROM JJ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    # Making sure the table is empty
    
    # setup
    stmt = """INSERT INTO JJ
VALUES(-0.1048575,1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    # PASS:0248 If 1 row is inserted?
    stmt = """SELECT FLOATTEST
FROM JJ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0248.exp""", """test0248g""")
    # PASS:0248 If FLOATTEST = -0.1048575 ?
    # PASS:0248 OR  is between -0.1048576 and -0.1048574 ?
    stmt = """SELECT COUNT(*) FROM JJ
WHERE FLOATTEST > -0.1048576 AND FLOATTEST < -0.1048574;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0248.exp""", """test0248h""")
    # PASS:0248 If count = 1?
    
    # restore
    stmt = """ROLLBACK WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # END TEST >>> 0248 <<< END TEST
    
