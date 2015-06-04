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

# TEST:0523 <value expression> for BETWEEN predicate!

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
    
    stmt = """SELECT COUNT(*)
FROM VWPROJ
WHERE 24 * 1000 BETWEEN BUDGET - 5000 AND 50000 / 1.7;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0523.exp""", """s1""")
    # PASS:0523 If count = 3?
    
    stmt = """SELECT PNAME
FROM VWPROJ
WHERE 'Tampa' NOT BETWEEN CITY AND 'Vienna'
AND PNUM > 'P2';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0523.exp""", """s2""")
    # PASS:0523 If PNAME = 'IRM'?
    
    stmt = """SELECT CITY, COUNT(*)
FROM VWPROJ
GROUP BY CITY
HAVING 50000 + 2 BETWEEN 33000 AND SUM(BUDGET) - 20;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0523.exp""", """s3""")
    # PASS:0523 If CITY = 'Deale' and count = 3?
    
    # restore
    stmt = """ROLLBACK WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # END TEST >>> 0523 <<< END TEST
    
