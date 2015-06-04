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

# TEST:0180 NULLs sort together in ORDER BY!

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
    
    # setup
    stmt = """UPDATE STAFF
SET GRADE = NULL
WHERE EMPNUM = 'E1' OR EMPNUM = 'E3' OR EMPNUM = 'E5';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 3)
    # PASS:0180 If 3 rows are updated?
    
    stmt = """SELECT EMPNUM,GRADE
FROM   VWSTAFF
ORDER  BY GRADE,EMPNUM;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0180.exp""", """s1""")
    # PASS:0180 If 5 rows are selected with NULLs together ?
    # PASS:0180 If first EMPNUM is either 'E1' or 'E2'?
    # PASS:0180 If last EMPNUM is either 'E4' or 'E5?
    
    # restore
    stmt = """ROLLBACK WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from VWSTAFF
order by EMPNUM
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0180.exp""", """s2""")
    # pass if 5 rows selected with the following values:
    # E1, Alice,  12, Deale
    # E2, Betty,  10, Vienna
    # E3, Carmen, 13, Vienna
    # E4, Don,    12, Deale
    # E5, Ed,     13, Akron
    
    # END TEST >>> 0180 <<< END TEST
    
