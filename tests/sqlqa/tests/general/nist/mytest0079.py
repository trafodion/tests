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

# TEST:0079 GROUP BY NULL value!

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
    
    stmt = """INSERT INTO staff(empnum,empname,grade)
VALUES('E6','WANG',40);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    # PASS:0079 If 1 row is inserted?
    
    stmt = """INSERT INTO staff(empnum,empname,grade)
VALUES('E7','SONG',50);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    # PASS:0079 If 1 row is inserted?
    
    stmt = """select count (*) from staff;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0079.exp""", """test0079c""")
    # pass if row count now = 7
    
    stmt = """select sum(grade)
from staff
where city IS NULL
group by city;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0079.exp""", """test0079d""")
    # PASS:0079 If SUM(GRADE) = 90?
    
    # clean up
    stmt = """delete from staff
where city IS NULL;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 2)
    
    stmt = """select count (*) from staff;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0079.exp""", """test0079f""")
    # pass if row count now = 5
    
    # END TEST >>> 0079 <<< END TEST
    
