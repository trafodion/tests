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

# TEST:0433 Empty subquery in ALL, SOME, ANY!
def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci
    
    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()
    
    stmt = """SELECT COUNT(*) FROM PROJ
WHERE PNUM = ALL (SELECT PNUM
FROM WORKS WHERE EMPNUM = 'E8');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0433.exp""", """test0433a""")
    # PASS:0433 If count = 6?
    stmt = """SELECT COUNT(*) FROM PROJ
WHERE PNUM <> ALL (SELECT PNUM
FROM WORKS WHERE EMPNUM = 'E8');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0433.exp""", """test0433b""")
    # PASS:0433 If count = 6?
    stmt = """SELECT COUNT(*) FROM PROJ
WHERE PNUM = ANY (SELECT PNUM
FROM WORKS WHERE EMPNUM = 'E8');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0433.exp""", """test0433c""")
    # PASS:0433 If count = 0?
    stmt = """SELECT COUNT(*) FROM PROJ
WHERE PNUM <> ANY (SELECT PNUM
FROM WORKS WHERE EMPNUM = 'E8');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0433.exp""", """test0433d""")
    # PASS:0433 If count = 0?
    stmt = """SELECT COUNT(*) FROM PROJ
WHERE PNUM = SOME (SELECT PNUM
FROM WORKS WHERE EMPNUM = 'E8');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0433.exp""", """test0433e""")
    # PASS:0433 If count = 0?
    stmt = """SELECT COUNT(*) FROM PROJ
WHERE PNUM <> SOME (SELECT PNUM
FROM WORKS WHERE EMPNUM = 'E8');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0433.exp""", """test0433f""")
    # PASS:0433 If count = 0?
    
    # END TEST >>> 0433 <<< END TEST
    
