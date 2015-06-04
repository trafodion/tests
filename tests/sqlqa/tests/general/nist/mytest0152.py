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

# TEST:0152 CREATE VIEW with Check Option!

def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci
    
    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()
    
    stmt = """INSERT INTO STAFFV2
VALUES('E6','Ling',15,'Xian');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    # PASS:0152 If 1 row is inserted?
    stmt = """SELECT COUNT(*)
FROM STAFFV2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0152.exp""", """test0152b""")
    # PASS:0152 If count = 5?
    stmt = """INSERT INTO STAFFV2
VALUES('E7','Gallagher',10,'Rockville');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8105')
    # PASS:0152 If ERROR, view check constraint, 0 rows inserted?
    stmt = """SELECT COUNT(*)
FROM STAFFV2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0152.exp""", """test0152d""")
    # PASS:0152 If count = 5?
    stmt = """SELECT COUNT(*)
FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0152.exp""", """test0152e""")
    # PASS:0152 If count = 6?
    
    # restore
    #      ROLLBACK WORK;
    stmt = """delete from staff where empnum = 'E6';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    # END TEST >>> 0152 <<< END TEST
    
