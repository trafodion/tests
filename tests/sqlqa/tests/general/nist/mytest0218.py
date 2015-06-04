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

# TEST:0218 FIPS sizing -- 6 columns in GROUP BY!
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
VALUES('1','22','4444','666666','88888888','0101010101',
'2020...20','3030...30','4040...40','5050...50',44,48);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    # PASS:0218 If 1 row is inserted?
    stmt = """INSERT INTO T12
VALUES('1','22','4444','666666','88888888','1010101010',
'2020...20','3030...30','4040...40','5050...50',11,12);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    # PASS:0218 If 1 row is inserted?
    stmt = """INSERT INTO T12
VALUES('1','22','4444','666666','88888888','1010101010',
'2020...20','3030...30','4040...40','5050...50',22,24);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    # PASS:0218 If 1 row is inserted?
    stmt = """INSERT INTO T12
VALUES('1','22','4444','666666','88888888','0101010101',
'2020...20','3030...30','4040...40','5050...50',33,36);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    # PASS:0218 If 1 row is inserted?
    stmt = """SELECT COUNT(*)
FROM  T12;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0218.exp""", """test0218e""")
    # PASS:0218 If count = 4?
    stmt = """SELECT COL6,SUM(COL11),MAX(COL12)
FROM T12
GROUP BY COL1,COL5,COL3,COL6,COL2,COL4
ORDER BY COL6 DESC;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0218.exp""", """test0218f""")
    # PASS:0218 If 2 rows are selected and second COL6 = 0101010101 and ?
    # PASS:0218 second SUM(COL11) = 77 and second MAX(COL12) = 48?
    
    # restore
    stmt = """ROLLBACK WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """select count (*) FROM T12;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0218.exp""", """test0218h""")
    # pass if count = 0
    
    # END TEST >>> 0218 <<< END TEST
    
