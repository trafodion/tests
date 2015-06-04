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

# TEST:0065 SELECT CHAR literal and term with numeric literal!

def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci
    
    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()
    
    stmt = """SELECT 'USER',PNAME
FROM VWPROJ
--           FROM HU.PROJ;		XXXXX
order by PNAME
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0065.exp""", """s1""")
    # PASS:0065 If 6 rows are selected and first column is value 'USER'?
    
    stmt = """SELECT PNUM,'BUDGET IN GRAMS IS ',BUDGET * 5
FROM VWPROJ
--           FROM HU.PROJ;		XXXXX
WHERE PNUM = 'P1';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0065.exp""", """s2""")
    # PASS:0065 If values are 'P1', 'BUDGET IN GRAMS IS ', 50000?
    
    # END TEST >>> 0065 <<< END TEST
