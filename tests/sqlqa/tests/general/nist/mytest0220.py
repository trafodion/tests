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

# TEST:0220 FIPS sizing -- 6 column in ORDER BY!
# FIPS sizing TEST

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
    
    # setup
    stmt = """INSERT INTO T12
VALUES('1','22','4444','666666','88888884','1010101010',
'2020...20','3030...30','4040...40','5050...50',11,12);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    # PASS:0220 If 1 row is inserted?
    stmt = """INSERT INTO T12
VALUES('1','22','4444','666666','88888883','1010101010',
'2020...20','3030...30','4040...40','5050...50',22,24);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    # PASS:0220 If 1 row is inserted?
    stmt = """INSERT INTO T12
VALUES('1','22','4444','666666','88888882','0101010101',
'2020...20','3030...30','4040...40','5050...50',33,36);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    # PASS:0220 If 1 row is inserted?
    stmt = """INSERT INTO T12
VALUES('1','22','4444','666666','88888881','0101010101',
'2020...20','3030...30','4040...40','5050...50',44,48);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    # PASS:0220 If 1 row is inserted?
    stmt = """SELECT COUNT(*)
FROM  T12;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0220.exp""", """test0220e""")
    # PASS:0220 If count = 4?
    stmt = """SELECT COL5,COL6,COL11,COL3,COL4,COL7,COL8
FROM T12
ORDER BY COL7,COL8,COL3,COL4,COL6,COL5 DESC;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0220.exp""", """test0220f""")
    # PASS:0220 If 4 rows are selected and first row?
    # PASS:0220 COL5 = 88888882, COL6 = 0101010101 and COL11 = 33?
    
    # restore
    stmt = """ROLLBACK WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """select count (*) FROM T12;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0220.exp""", """test0220h""")
    # pass if count = 0
    
    # END TEST >>> 0220 <<< END TEST
    
