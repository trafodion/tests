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

# TEST:0215 FIPS sizing -- 6 columns in a UNIQUE constraint!
# FIPS sizing TEST

# setup
def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci
    
    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()
    
    stmt = """INSERT INTO T8
VALUES('th','seco','third3','fourth_4','fifth_colu',
'sixth_column','seventh_column','last_column_of_t');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    # PASS:0215 If 1 row is inserted?
    stmt = """INSERT INTO T8
VALUES('th','seco','third3','fourth_4','fifth_colu',
'sixth_column','column_seventh','column_eighth_la');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8102')
    # PASS:0215 If ERROR, unique constraint, 0 rows inserted?
    stmt = """SELECT COL1,COL2,COL3,COL4,COL5,COL6,COL7,COL8
FROM T8;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0215.exp""", """test0215c""")
    # PASS:0215 If COL1 = 'th'?
    
    # restore
    # ROLLBACK WORK;
    stmt = """delete FROM T8;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    # END TEST >>> 0215 <<< END TEST
    
