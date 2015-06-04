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

# TEST:0221 FIPS sizing -- 120 bytes in ORDER BY!
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
VALUES('1','22','4442','666666','88888888','1010101010',
'20202020202020202020','303030303030303030303030303030',
'4040404040404040404040404040404040404040', '5050...50',111,112);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    # PASS:0221 If 1 row is inserted?
    stmt = """INSERT INTO T12
VALUES('1','22','4443','666666','88888888','1010101010',
'20202020202020202020','303030303030303030303030303030',
'4040404040404040404040404040404040404040', '5050...50',222,224);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    # PASS:0221 If 1 row is inserted?
    stmt = """INSERT INTO T12
VALUES('1','22','4441','666666','88888888','1010101010',
'20202020202020202020','303030303030303030303030303030',
'4040404040404040404040404040404040404040', '5050...50',333,336);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    # PASS:0221 If 1 row is inserted?
    stmt = """INSERT INTO T12
VALUES('1','22','4444','666666','88888888','1010101010',
'20202020202020202020','303030303030303030303030303030',
'4040404040404040404040404040404040404040', '5050...50',444,448);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    # PASS:0221 If 1 row is inserted?
    stmt = """SELECT COUNT(*)
FROM  T12;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0221.exp""", """test0221e""")
    # PASS:0221 If count = 4?
    stmt = """SELECT COL3,COL11,COL9,COL8,COL7,COL5,COL4
FROM T12
ORDER BY COL9,COL8,COL7,COL5,COL4,COL3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0221.exp""", """test0221f""")
    # PASS:0221 If 4 rows are selected ?
    # PASS:0221 If first row COL3 = 4441 and COL11 = 333?
    
    # restore
    stmt = """ROLLBACK WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select count (*) FROM T12;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0221.exp""", """test0221h""")
    # pass if count = 0
    
    # END TEST >>> 0221 <<< END TEST
    
