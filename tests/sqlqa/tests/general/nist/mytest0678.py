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

# TEST:0678 Data type semantics with NULL / NOT NULL!

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
    stmt = """CREATE TABLE CH1 (
CH1A CHARACTER (10) NOT NULL,
CH1B CHARACTER NOT NULL,
CH1C CHAR (10) NOT NULL
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    # PASS:0678 If table is created?
    
    #   COMMIT WORK;		-- XXXXX
    stmt = """CREATE TABLE NUM1 (
NUM1C1 NUMERIC (3, 2) NOT NULL,
NUM1C2 NUMERIC (2) NOT NULL,
NUM1C3 NUMERIC NOT NULL
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    # PASS:0678 If table is created?
    # stmt = """COMMIT WORK;"""
    # output = _dci.cmdexec(stmt)
    # _dci.expect_complete_msg(output)
    stmt = """INSERT INTO CH1 VALUES ('FOO', '', '0123456789');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    # PASS:0678 If 1 row is inserted?
    stmt = """SELECT CH1A, CH1B, CH1C
FROM CH1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0678.exp""", """test0678e""")
    
    # PASS:0678 If 1 row selected and CH1A = 'FOO       '?
    # PASS:0678 AND CH1B = ' ' and CH1C = '0123456789'?
    
    # NOTE:0678 One subtest deleted.
    stmt = """INSERT INTO CH1 VALUES ('FOO',
'F', 'LITTLETOOLONG');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8402')
    
    # PASS:0678 If ERROR, string data, right truncation, 0 rows selected?
    stmt = """DELETE FROM CH1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    stmt = """INSERT INTO CH1 VALUES ('FOO',
'F', 'BLANKS       ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    # PASS:0678 If 1 row is inserted?
    stmt = """SELECT CH1A, CH1B, CH1C
FROM CH1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0678.exp""", """test0678i""")
    
    # PASS:0678 If 1 row selected and CH1A = 'FOO       '?
    # PASS:0678 AND CH1B = 'F' and CH1C = 'BLANKS    '?
    stmt = """INSERT INTO NUM1 VALUES (9.99, -99, 9);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    # PASS:0678 If 1 row is inserted?
    stmt = """SELECT NUM1C1 * 100, NUM1C2, NUM1C3
FROM NUM1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0678.exp""", """test0678k""")
    
    # PASS:0678 If 1 row selected and values are 999, -99, 9?
    stmt = """DELETE FROM NUM1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    stmt = """INSERT INTO NUM1 VALUES (-10, 0, 0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8411')
    
    # PASS:0678 If ERROR, string data, numeric value out of range?
    # PASS:0678 AND 0 rows inserted?
    stmt = """INSERT INTO NUM1 VALUES (0, 100, 0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8411')
    # PASS:0678 If ERROR, string data, numeric value out of range?
    # PASS:0678 AND 0 rows inserted?
    stmt = """INSERT INTO NUM1 VALUES (0, 0, 0.1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    # PASS:0678 If 1 row is inserted?
    
    stmt = """SELECT NUM1C1 * 100, NUM1C2, NUM1C3
FROM NUM1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0678.exp""", """test0678p""")
    
    # PASS:0678 If 1 row selected and values are 0, 0, 0?
    
    #    ROLLBACK WORK;
    
    #   DROP TABLE NUM1 CASCADE;		-- XXXXX
    stmt = """DROP TABLE NUM1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #    COMMIT WORK;		-- XXXXX
    
    #   DROP TABLE CH1 CASCADE;		-- XXXXX
    stmt = """DROP TABLE CH1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #    COMMIT WORK;
    
    # END TEST >>> 0678 <<< END TEST
    
