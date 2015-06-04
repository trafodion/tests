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

# TEST:0395 SUM, MIN on joined table with GROUP without WHERE!
def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci
    
    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()
    
    stmt = """SELECT STAFF.EMPNUM, SUM(HOURS), MIN(HOURS)
FROM  STAFF, WORKS
GROUP BY STAFF.EMPNUM
ORDER BY 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0395.exp""", """test0395""")
    
    # PASS:0395 If 5 rows are selected with the following order?
    # PASS:0395 STAFF.EMPNUM  SUM(HOURS)  MIN(HOURS)?
    # PASS:0395    'E1'         464          12?
    # PASS:0395    'E2'         464          12?
    # PASS:0395    'E3'         464          12?
    # PASS:0395    'E4'         464          12?
    # PASS:0395    'E5'         464          12?
    
    # END TEST >>> 0395 <<< END TEST
    
