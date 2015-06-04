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

# TEST:0250 FIPS sizing - bin. precision of DOUBLE >= 30!

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
    stmt = """DELETE FROM II;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 0)
    # Making sure the table is empty
    
    # setup
    stmt = """INSERT INTO II
VALUES(0.1073741823,1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    # PASS:0250 If 1 row is inserted?
    stmt = """SELECT DOUBLETEST
FROM II;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0250.exp""", """test0250c""")
    # PASS:0250 If DOUBLETEST = 0.1073741823 ?
    # PASS:0250 OR  is between  0.1073741822 and 0.1073741824 ?
    stmt = """SELECT COUNT(*) FROM II
WHERE DOUBLETEST > 0.1073741822 AND DOUBLETEST < 0.1073741824;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0250.exp""", """test0250d""")
    # PASS:0250 If count = 1?
    stmt = """DELETE FROM II;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    # Making sure the table is empty
    
    # setup
    stmt = """INSERT INTO II
VALUES(-0.1073741823,1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    # PASS:0250 If 1 row is inserted?
    stmt = """SELECT DOUBLETEST
FROM II;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0250.exp""", """test0250g""")
    # PASS:0250 If DOUBLETEST = -0.1073741823 ?
    # PASS:0250 OR  is between  -0.1073741824 and -0.1073741822 ?
    stmt = """SELECT COUNT(*) FROM II
WHERE DOUBLETEST > -0.1073741824 AND DOUBLETEST < -0.1073741822;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0250.exp""", """test0250h""")
    # PASS:0250 If count = 1?
    
    # restore
    stmt = """ROLLBACK WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # END TEST >>> 0250 <<< END TEST
    
