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

import time
from ...lib import hpdci
from ...lib import gvars
import defs

_testmgr = None
_testlist = []
_dci = None

# TEST:0591 NATURAL JOIN (feature 4) (static)!

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

    stmt = """CREATE TABLE GROUPS1
(EMPNUM INT, GRP INT) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    # PASS:0591 If table is created?
    stmt = """CREATE TABLE NAMES1
(EMPNUM INT, NAM CHAR(5)) no partition;  -- changed NAME to NAM throughout"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    # PASS:0591 If table is created?
    stmt = """CREATE VIEW NAMGRP1 AS
SELECT * FROM NAMES1 NATURAL JOIN GROUPS1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    # PASS:0591 If view is created?
    # stmt = """COMMIT WORK;"""
    # output = _dci.cmdexec(stmt)
    # _dci.expect_complete_msg(output)
    
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO GROUPS1 VALUES (0, 10);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)

    # PASS:0591 If 1 row is inserted?
    stmt = """INSERT INTO GROUPS1 VALUES (1, 20);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    # PASS:0591 If 1 row is inserted?
    stmt = """INSERT INTO GROUPS1 VALUES (2, 30);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    # PASS:0591 If 1 row is inserted?
    stmt = """INSERT INTO GROUPS1 VALUES (3, 40);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    # PASS:0591 If 1 row is inserted?
    stmt = """INSERT INTO NAMES1 VALUES (5, 'HARRY');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    # PASS:0591 If 1 row is inserted?
    stmt = """INSERT INTO NAMES1 VALUES (1, 'MARY');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    # PASS:0591 If 1 row is inserted?
    stmt = """INSERT INTO NAMES1 VALUES (7, 'LARRY');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    # PASS:0591 If 1 row is inserted?
    stmt = """INSERT INTO NAMES1 VALUES (0, 'KERI');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    # PASS:0591 If 1 row is inserted?
    stmt = """INSERT INTO NAMES1 VALUES (9, 'BARRY');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    # PASS:0591 If 1 row is inserted?
    stmt = """SELECT EMPNUM
FROM NAMGRP1
WHERE NAM = 'KERI'
AND GRP = 10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0591.exp""", """test0591n""")
    # PASS:0591 If 1 row is selected and EMPNUM = 0?
    stmt = """SELECT EMPNUM
FROM NAMGRP1
WHERE NAM = 'MARY'
AND GRP = 20;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0591.exp""", """test0591o""")
    # PASS:0591 If 1 row is selected and EMPNUM = 1?
    stmt = """SELECT COUNT(*)
FROM NAMGRP1
WHERE (NAM <> 'MARY'
AND NAM <> 'KERI')
OR GRP <> 20
AND GRP <> 10
OR EMPNUM <> 0
AND EMPNUM <> 1
OR NAM IS NULL
OR GRP IS NULL
OR EMPNUM IS NULL;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0591.exp""", """test0591p""")
    # PASS:0591 If count = 0?
    stmt = """ROLLBACK WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    time.sleep(2)
    # stmt = """begin work;"""
    # output = _dci.cmdexec(stmt)
    stmt = """DROP VIEW NAMGRP1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #-    DROP TABLE NAMES1 CASCADE;	XXXXXX
    stmt = """DROP TABLE NAMES1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    # PASS:0591 If table and view are dropped?
    
    #-    DROP TABLE GROUPS1 CASCADE;	XXXXXX
    stmt = """DROP TABLE GROUPS1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    # PASS:0591 If table is dropped?
    # stmt = """COMMIT WORK;"""
    # output = _dci.cmdexec(stmt)
    # _dci.expect_complete_msg(output)
    
    # END TEST >>> 0591 <<< END TEST
    
