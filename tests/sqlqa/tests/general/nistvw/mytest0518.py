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

def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci
    
    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()
   
    # stmt = """begin work;"""
    # output = _dci.cmdexec(stmt)
    # _dci.expect_complete_msg(output)
    
    # TEST:0518 CREATE VIEW with DISTINCT!
   
    stmt = """CREATE VIEW DV1 AS
SELECT DISTINCT HOURS FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
 
    stmt = """SELECT COUNT(*)
FROM DV1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0518.exp""", """s1""")
    # PASS:0518 If count = 4?
    
    stmt = """SELECT HOURS FROM DV1
ORDER BY HOURS DESC;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0518.exp""", """s2""")
    # PASS:0518 If 4 rows selected AND first HOURS = 80?
    # PASS:0518 AND second HOURS = 40 AND third HOURS = 20?
    # PASS:0518 AND fourth HOURS = 12?
    
    # restore
    # stmt = """ROLLBACK WORK;"""
    # output = _dci.cmdexec(stmt)
    # _dci.expect_complete_msg(output)
    
    # END TEST >>> 0518 <<< END TEST;
    
