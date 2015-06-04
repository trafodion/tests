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

# TEST:0254 Column name in SET clause!

def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci
    
    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()
    
    stmt = """DELETE FROM PROJ1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output)
    # Making sure the table is empty
    
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # setup
    stmt = """INSERT INTO PROJ1
SELECT *
FROM VWPROJ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 6)
    # PASS:0254 If 6 rows are inserted?
    
    stmt = """UPDATE PROJ1
SET CITY = PTYPE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 6)
    # PASS:0254 If 6 rows are updated?
    
    stmt = """SELECT CITY
FROM VWPROJ1
WHERE PNUM = 'P1';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0254.exp""", """s1""")
    # PASS:0254 If CITY = 'Design'?
    
    # restore
    stmt = """ROLLBACK WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select count (*) from VWPROJ1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0254.exp""", """s2""")
    # pass if count = 0;
    
    # END TEST >>> 0254 <<< END TEST
    
