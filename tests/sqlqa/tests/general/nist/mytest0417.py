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

# TEST:0417 Cartesian product GROUP BY 2 columns with NULLs!

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
    stmt = """DELETE FROM STAFF1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 0)
    # Making sure the table is empty
    
    # setup
    stmt = """INSERT INTO STAFF VALUES ('E6', 'David', 17, NULL);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO STAFF VALUES ('E7', 'Tony', 18, NULL);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO STAFF1 SELECT * FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 7)
    
    stmt = """SELECT MAX(STAFF1.GRADE), SUM(STAFF1.GRADE)
FROM STAFF1, STAFF
GROUP BY STAFF1.CITY, STAFF.CITY
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0417.exp""", """test0417e""")
    
    # PASS:0417 If 16 rows are selected in any order?
    # PASS:0417 Including the following four rows?
    # PASS:0417 MAX(STAFF1.GRADE) = 18 and SUM(STAFF1.GRADE) = 35?
    # PASS:0417 MAX(STAFF1.GRADE) = 18 and SUM(STAFF1.GRADE) = 70?
    # PASS:0417 MAX(STAFF1.GRADE) = 18 and SUM(STAFF1.GRADE) = 70?
    # PASS:0417 MAX(STAFF1.GRADE) = 18 and SUM(STAFF1.GRADE) = 70?
    
    # restore
    stmt = """ROLLBACK WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """select count (*) FROM STAFF1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0417.exp""", """test0417g""")
    # pass if count = 0
    stmt = """select count (*) FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0417.exp""", """test0417h""")
    # pass if count = 5
    
    # END TEST >>> 0417 <<< END TEST
    
