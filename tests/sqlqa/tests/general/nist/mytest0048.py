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

# TEST:0048 NOT IN predicate!
def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci
    
    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()
    
    stmt = """SELECT WORKS.HOURS
FROM WORKS
WHERE WORKS.PNUM NOT IN
(SELECT PROJ.PNUM
FROM PROJ
WHERE PROJ.BUDGET BETWEEN 5000 AND 40000);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0048.exp""", """test0048a""")
    # PASS:0048 If HOURS = 12?
    stmt = """SELECT WORKS.HOURS
FROM WORKS
WHERE NOT (WORKS.PNUM IN
(SELECT PROJ.PNUM
FROM PROJ
WHERE PROJ.BUDGET BETWEEN 5000 AND 40000));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0048.exp""", """test0048b""")
    # PASS:0048 If HOURS = 12?
    
    # END TEST >>> 0048 <<< END TEST
    
