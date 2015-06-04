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

# TEST:0253 TEST0124 workaround (key = key+1)!

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
    
    stmt = """SELECT NUMKEY
FROM VWUPUNIQ
ORDER BY NUMKEY DESC;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0253.exp""", """s1""")
    # PASS:0253 If 6 rows are selected and first NUMKEY = 8 ?
    
    stmt = """UPDATE UPUNIQ
SET NUMKEY = 8 + 1
WHERE NUMKEY = 8;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    # PASS:0253 If 1 row is updated?
    
    stmt = """UPDATE UPUNIQ
SET NUMKEY = 6 + 1
WHERE NUMKEY = 6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    # PASS:0253 If 1 row is updated?
    
    stmt = """UPDATE UPUNIQ
SET NUMKEY = 4 + 1
WHERE NUMKEY = 4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    # PASS:0253 If 1 row is updated?
    
    stmt = """UPDATE UPUNIQ
SET NUMKEY = 3 + 1
WHERE NUMKEY = 3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    # PASS:0253 If 1 row is updated?
    
    stmt = """UPDATE UPUNIQ
SET NUMKEY = 2 + 1
WHERE NUMKEY = 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    # PASS:0253 If 1 row is updated?
    
    stmt = """UPDATE UPUNIQ
SET NUMKEY = 1 + 1
WHERE NUMKEY = 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    # PASS:0253 If 1 row is updated?
    
    stmt = """SELECT MAX(NUMKEY), MIN(NUMKEY)
FROM VWUPUNIQ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0253.exp""", """s2""")
    # PASS:0253 If MAX(NUMKEY) = 9 AND MIN(NUMKEY) = 2?
    
    # restore
    stmt = """ROLLBACK WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # END TEST >>> 0253 <<< END TEST
    
