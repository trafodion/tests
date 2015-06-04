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

def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci
    
    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()
    
def test001(desc="""a001"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO WORKS VALUES  ('E1','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P3',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P4',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P5',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P6',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P2',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E3','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P4',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P5',80);"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0001 SELECT with ORDER BY DESC!
    
    stmt = """SELECT EMPNUM,HOURS
FROM WORKS 
WHERE PNUM='P2'
ORDER BY EMPNUM DESC;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", 'a001s0')
    
    stmt = """delete from WORKS ;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test002(desc="""a002"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO WORKS VALUES  ('E1','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P3',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P4',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P5',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P6',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P2',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E3','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P4',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P5',80);"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0002 SELECT with ORDER BY integer ASC!
    
    stmt = """SELECT EMPNUM,HOURS
FROM WORKS 
WHERE PNUM='P2'
ORDER BY 2 ASC;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a002exp""", 'a002s0')
    
    stmt = """delete from WORKS ;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test003(desc="""a003"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO WORKS VALUES  ('E1','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P3',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P4',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P5',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P6',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P2',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E3','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P4',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P5',80);"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0003 SELECT with ORDER BY DESC integer, named column!
    
    stmt = """SELECT EMPNUM,HOURS
FROM WORKS 
WHERE PNUM = 'P2'
ORDER BY 2 DESC,EMPNUM DESC;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a003exp""", 'a003s0')
    
    stmt = """delete from WORKS ;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test004(desc="""a004"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    stmt = """DELETE FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO WORKS VALUES  ('E1','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P3',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P4',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P5',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P6',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P2',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E3','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P4',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P5',80);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO STAFF VALUES ('E1','Alice',12,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E2','Betty',10,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E3','Carmen',13,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E4','Don',12,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E5','Ed',13,'Akron');"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0004 SELECT with UNION, ORDER BY integer DESC!
    
    stmt = """SELECT WORKS.EMPNUM
FROM WORKS 
WHERE WORKS.PNUM = 'P2'
UNION
SELECT STAFF.EMPNUM
FROM STAFF 
WHERE STAFF.GRADE=13
ORDER BY 1 DESC;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a004exp""", 'a004s0')
    
    stmt = """DELETE FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test005(desc="""a005"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    stmt = """DELETE FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO WORKS VALUES  ('E1','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P3',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P4',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P5',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P6',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P2',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E3','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P4',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P5',80);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO STAFF VALUES ('E1','Alice',12,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E2','Betty',10,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E3','Carmen',13,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E4','Don',12,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E5','Ed',13,'Akron');"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0005 SELECT with UNION ALL!
    
    stmt = """SELECT WORKS.EMPNUM
FROM WORKS 
WHERE WORKS.PNUM = 'P2'
UNION ALL
SELECT STAFF.EMPNUM
FROM STAFF 
WHERE STAFF.GRADE = 13;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a005exp""", 'a005s0')
    
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    stmt = """DELETE FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test006(desc="""a009"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO WORKS VALUES  ('E1','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P3',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P4',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P5',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P6',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P2',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E3','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P4',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P5',80);"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0009 SELECT NULL value!
    
    # setup
    stmt = """INSERT INTO WORKS 
VALUES('E9','P9',NULL);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    #  PASS:0009 If 1 row is inserted?
    
    stmt = """SELECT EMPNUM
FROM WORKS 
WHERE HOURS IS NULL;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a009exp""", 'a009s0')
    #  PASS:0009 If EMPNUM = 'E9'?
    
    stmt = """SELECT EMPNUM, HOURS
FROM WORKS 
WHERE PNUM = 'P9'
ORDER BY EMPNUM DESC;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a009exp""", 'a009s1')
    
    stmt = """DELETE  FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test007(desc="""a016"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO WORKS VALUES  ('E1','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P3',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P4',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P5',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P6',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P2',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E3','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P4',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P5',80);"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0016 SELECT ALL syntax!
    
    stmt = """SELECT ALL EMPNUM
FROM WORKS 
WHERE HOURS = 12;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a016exp""", 'a016s0')
    
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test008(desc="""a017"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO WORKS VALUES  ('E1','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P3',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P4',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P5',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P6',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P2',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E3','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P4',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P5',80);"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0017 SELECT:checks DISTINCT!
    
    stmt = """SELECT DISTINCT EMPNUM
FROM WORKS 
WHERE HOURS = 12;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a017exp""", 'a017s0')
    
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test009(desc="""a019"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO WORKS VALUES  ('E1','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P3',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P4',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P5',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P6',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P2',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E3','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P4',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P5',80);"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0019 SQLCODE = 0, SELECT with data!
    
    stmt = """SELECT EMPNUM,HOURS
FROM WORKS 
WHERE EMPNUM = 'E1' AND PNUM = 'P4';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a019exp""", 'a019s0')
    
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test010(desc="""a020"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO WORKS VALUES  ('E1','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P3',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P4',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P5',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P6',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P2',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E3','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P4',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P5',80);"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0020 SELECT NULL value !
    
    # setup
    stmt = """INSERT INTO WORKS 
VALUES('E18','P18',NULL);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #  PASS:0020 If 1 row is inserted?
    
    stmt = """SELECT EMPNUM,HOURS
FROM   WORKS 
WHERE  EMPNUM='E18' AND PNUM='P18';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a020exp""", 'a020s0')
    # PASS:0020 If EMPNUM = 'E18' and HOURS is NULL?
    
    # restore
    #     ROLLBACK WORK;
    
    stmt = """DELETE FROM   WORKS 
WHERE  EMPNUM='E18' AND PNUM='P18';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    stmt = """SELECT EMPNUM,HOURS
FROM   WORKS 
WHERE  EMPNUM='E18' AND PNUM='P18';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test011(desc="""a022"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO WORKS VALUES  ('E1','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P3',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P4',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P5',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P6',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P2',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E3','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P4',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P5',80);"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0022 INSERT(column list) VALUES(literals and NULL)!
    
    # setup
    stmt = """INSERT INTO WORKS(PNUM,EMPNUM,HOURS)
VALUES ('P22','E22',NULL);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #  PASS:0022 If 1 row inserted?
    
    stmt = """SELECT EMPNUM,PNUM
FROM   WORKS 
WHERE  HOURS IS NULL;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a022exp""", 'a022s0')
    # PASS:0022 If EMPNUM = 'E22'?
    
    # restore
    #     ROLLBACK WORK;
    
    stmt = """DELETE FROM WORKS 
WHERE HOURS IS NULL;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    stmt = """SELECT EMPNUM,PNUM
FROM   WORKS 
WHERE  HOURS IS NULL;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test012(desc="""a023"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM TEMPXS;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO TEMPXS(EMPNUM,GRADE,CITY)
VALUES('E23',2323.4,'China');"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO TEMPXS 
VALUES('E23',23234,'China');"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0023 DEC precision >= col.def.: ERROR if left-truncate!
    
    stmt = """SELECT COUNT(*)
FROM TEMPXS;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a023exp""", 'a023s0')
    
    stmt = """DELETE FROM TEMPXS;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test013(desc="""a024"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """delete from TEMPXS;"""
    output = _dci.cmdexec(stmt)
    stmt = """delete from STAFF;"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0024 INSERT:<query spec.> is empty: SQLCODE = 100!
    
    # setup
    stmt = """INSERT INTO TEMPXS 
SELECT EMPNUM,GRADE,CITY
FROM STAFF 
WHERE GRADE > 13;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 0)
    
    stmt = """SELECT COUNT(*) FROM TEMPXS;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a024exp""", 'a024s0')
    
    stmt = """DELETE FROM TEMPXS;"""
    output = _dci.cmdexec(stmt)
    stmt = """DELETE FROM STAFF;"""
    output = _dci.cmdexec(stmt)
  
    _testmgr.testcase_end(desc)

def test014(desc="""a025"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """delete from TEMPXS;"""
    output = _dci.cmdexec(stmt)
    stmt = """delete from STAFF;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO STAFF VALUES ('E1','Alice',12,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E2','Betty',10,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E3','Carmen',13,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E4','Don',12,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E5','Ed',13,'Akron');"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0025 INSERT:<query spec.> is not empty!
    
    stmt = """DELETE FROM TEMPXS;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 0)
    
    # setup
    
    stmt = """INSERT INTO TEMPXS(EMPNUM,GRADE,CITY)
SELECT EMPNUM,GRADE,CITY
FROM STAFF 
WHERE GRADE > 12;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 2)
    #  PASS:0025 If 2 rows are inserted?
    
    stmt = """SELECT COUNT(*)
FROM TEMPXS;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a025exp""", 'a025s0')
    
    stmt = """DELETE FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    stmt = """DELETE FROM TEMPXS;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test015(desc="""a027"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """delete from TMP;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO TMP (T1, T2, T3)
VALUES ( 'xxxx',23,'xxxx');"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0027 INSERT short string in long col -- space padding !
    
    stmt = """SELECT *
FROM TMP 
WHERE T2 = 23 AND T3 = 'xxxx      ';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a027exp""", 'a027s0')
    
    stmt = """DELETE FROM TMP;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test016(desc="""a028"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """delete from TMP;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO TMP (T1, T2, T3)
VALUES ('xxxxxxxxxx', 23,'xxxxxxxxxx');"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0028 Insert String that fits Exactly in Column!
    
    stmt = """SELECT *
FROM TMP 
WHERE T2 = 23;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a028exp""", 'a028s0')
    # PASS:0028 If T1 = 'xxxxxxxxxx'?
    
    # restore
    #      ROLLBACK WORK;              XXXXX
    stmt = """delete from TMP;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    stmt = """select count (*) from TMP;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a028exp""", 'a028s1')
    
    stmt = """delete from TMP;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test017(desc="""a031"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM TMP;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO TMP (T2, T3, T1)
VALUES (NULL,'zz','z');"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0031 INSERT(column list) VALUES(NULL and literals)!
    
    stmt = """SELECT *
FROM   TMP 
WHERE  T2 IS NULL;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a031exp""", 'a031s0')
    
    stmt = """DELETE FROM TMP;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test018(desc="""a034"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO STAFF VALUES ('E1','Alice',12,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E2','Betty',10,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E3','Carmen',13,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E4','Don',12,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E5','Ed',13,'Akron');"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0034 UPDATE table with SET column in <WHERE clause>!
    
    # setup
    stmt = """UPDATE STAFF 
SET GRADE = 2*GRADE
WHERE GRADE = 13;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 2)
    #  PASS:0034 If 2 rows are updated?
    
    stmt = """SELECT COUNT(*)
FROM STAFF 
WHERE GRADE = 26;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a034exp""", 'a034s0')
    
    stmt = """DELETE FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test019(desc="""a039"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO WORKS VALUES  ('E1','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P3',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P4',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P5',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P6',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P2',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E3','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P4',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P5',80);"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0039 COUNT DISTINCT function!
    
    # setup
    stmt = """INSERT INTO WORKS 
VALUES('E5','P5',NULL);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #  PASS:0039 If 1 row inserted?
    
    stmt = """SELECT COUNT(DISTINCT HOURS)
FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a039exp""", 'a039s0')
    
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test020(desc="""a040"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO WORKS VALUES  ('E1','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P3',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P4',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P5',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P6',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P2',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E3','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P4',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P5',80);"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0040 SUM function with WHERE clause!
    
    stmt = """SELECT SUM(HOURS)
FROM WORKS 
WHERE PNUM = 'P2';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a040exp""", 'a040s0')
    
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test021(desc="""a041"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO STAFF VALUES ('E1','Alice',12,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E2','Betty',10,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E3','Carmen',13,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E4','Don',12,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E5','Ed',13,'Akron');"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0041 MAX function in subquery!
    
    stmt = """SELECT EMPNUM
FROM STAFF 
WHERE GRADE = (SELECT MAX(GRADE) FROM STAFF)
ORDER BY EMPNUM;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a041exp""", 'a041s0')
    
    stmt = """DELETE FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test022(desc="""a042"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO STAFF VALUES ('E1','Alice',12,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E2','Betty',10,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E3','Carmen',13,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E4','Don',12,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E5','Ed',13,'Akron');"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0042 MIN function in subquery!
    
    stmt = """SELECT EMPNUM
FROM STAFF 
WHERE GRADE =
(SELECT MIN(GRADE) FROM STAFF);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a042exp""", 'a042s0')
    
    stmt = """DELETE FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test023(desc="""a043"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """delete from STAFF;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO STAFF VALUES ('E1','Alice',12,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E2','Betty',10,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E3','Carmen',13,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E4','Don',12,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E5','Ed',13,'Akron');"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0043 AVG function!
    
    stmt = """SELECT AVG(GRADE)
FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a043exp""", 'a043s0')
    
    stmt = """DELETE FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test024(desc="""a044"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM TEMPXS;"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0044 AVG function - empty result NULL value!
    
    stmt = """SELECT AVG(GRADE)
FROM   TEMPXS;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a044exp""", 'a044s0')
    
    stmt = """DELETE FROM TEMPXS;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test025(desc="""a045"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM PROJ;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO PROJ VALUES  ('P1','MXSS','Design',10000,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P2','CALM','Code',30000,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P3','SDP','Test',30000,'Tampa');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P4','SDP','Design',20000,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P5','IRM','Test',10000,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P6','PAYR','Design',50000,'Deale');"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0045 BETWEEN predicate!
    
    stmt = """SELECT PNUM
FROM PROJ 
WHERE BUDGET BETWEEN 40000 AND 60000;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a045exp""", 'a045s0')
    #  PASS:0045 If PNUM = 'P6'?
    
    stmt = """SELECT PNUM
FROM PROJ 
WHERE BUDGET >= 40000 AND BUDGET <= 60000;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a045exp""", 'a045s1')
    
    stmt = """DELETE FROM PROJ;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test026(desc="""a046"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """delete from STAFF;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO STAFF VALUES ('E1','Alice',12,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E2','Betty',10,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E3','Carmen',13,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E4','Don',12,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E5','Ed',13,'Akron');"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0046 NOT BETWEEN predicate   !
    
    stmt = """SELECT CITY
FROM STAFF 
WHERE GRADE NOT BETWEEN 12 AND 13;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a046exp""", 'a046s0')
    #  PASS:0046 If CITY = 'Vienna'?
    
    stmt = """SELECT CITY
FROM STAFF 
WHERE NOT(GRADE BETWEEN 12 AND 13);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a046exp""", 'a046s1')
    
    stmt = """DELETE FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test027(desc="""a047"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    stmt = """DELETE FROM PROJ;"""
    output = _dci.cmdexec(stmt)
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO STAFF VALUES ('E1','Alice',12,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E2','Betty',10,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E3','Carmen',13,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E4','Don',12,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E5','Ed',13,'Akron');"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO PROJ VALUES  ('P1','MXSS','Design',10000,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P2','CALM','Code',30000,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P3','SDP','Test',30000,'Tampa');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P4','SDP','Design',20000,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P5','IRM','Test',10000,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P6','PAYR','Design',50000,'Deale');"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO WORKS VALUES  ('E1','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P3',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P4',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P5',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P6',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P2',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E3','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P4',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P5',80);"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0047 IN predicate!
    
    stmt = """SELECT STAFF.EMPNAME
FROM STAFF 
WHERE STAFF.EMPNUM IN
(SELECT WORKS.EMPNUM
FROM WORKS 
WHERE WORKS.PNUM IN
(SELECT PROJ.PNUM
FROM PROJ 
WHERE PROJ.CITY='Tampa'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a047exp""", 'a047s0')
    #  PASS:0047 If EMPNAME = 'Alice'?
    
    stmt = """SELECT STAFF.EMPNAME
FROM STAFF 
WHERE STAFF.EMPNUM = ANY
(SELECT WORKS.EMPNUM
FROM WORKS 
WHERE WORKS.PNUM IN
(SELECT PROJ.PNUM
FROM PROJ 
WHERE PROJ.CITY='Tampa'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a047exp""", 'a047s1')
    
    stmt = """DELETE FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    stmt = """DELETE FROM PROJ;"""
    output = _dci.cmdexec(stmt)
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test028(desc="""a048"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM PROJ;"""
    output = _dci.cmdexec(stmt)
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO PROJ VALUES  ('P1','MXSS','Design',10000,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P2','CALM','Code',30000,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P3','SDP','Test',30000,'Tampa');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P4','SDP','Design',20000,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P5','IRM','Test',10000,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P6','PAYR','Design',50000,'Deale');"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO WORKS VALUES  ('E1','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P3',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P4',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P5',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P6',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P2',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E3','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P4',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P5',80);"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0048 NOT IN predicate!
    
    stmt = """SELECT WORKS.HOURS
FROM WORKS 
WHERE WORKS.PNUM NOT IN
(SELECT PROJ.PNUM
FROM PROJ 
WHERE PROJ.BUDGET BETWEEN 5000 AND 40000);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a048exp""", 'a048s0')
    #  PASS:0048 If HOURS = 12?
    
    stmt = """SELECT WORKS.HOURS
FROM WORKS 
WHERE NOT (WORKS.PNUM IN
(SELECT PROJ.PNUM
FROM PROJ 
WHERE PROJ.BUDGET BETWEEN 5000 AND 40000));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a048exp""", 'a048s1')
    
    stmt = """DELETE FROM PROJ;"""
    output = _dci.cmdexec(stmt)
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test029(desc="""a049"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO WORKS VALUES  ('E1','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P3',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P4',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P5',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P6',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P2',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E3','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P4',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P5',80);"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0049 IN predicate value list!
    
    stmt = """SELECT HOURS
FROM WORKS 
WHERE PNUM NOT IN
(SELECT PNUM
FROM WORKS 
WHERE PNUM IN ('P1','P2','P4','P5','P6'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a049exp""", 'a049s0')
    #  PASS:0049 If HOURS = 80?
    
    stmt = """SELECT HOURS
FROM WORKS 
WHERE NOT (PNUM IN
(SELECT PNUM
FROM WORKS 
WHERE PNUM IN ('P1','P2','P4','P5','P6')));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a049exp""", 'a049s1')
    
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test030(desc="""a050"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E1','Alice',12,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E2','Betty',10,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E3','Carmen',13,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E4','Don',12,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E5','Ed',13,'Akron');"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0050 LIKE predicate -- %!
    
    stmt = """SELECT EMPNAME
FROM STAFF 
WHERE EMPNAME LIKE 'Al%';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a050exp""", 'a050s0')
    
    stmt = """DELETE FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test031(desc="""a051"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E1','Alice',12,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E2','Betty',10,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E3','Carmen',13,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E4','Don',12,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E5','Ed',13,'Akron');"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0051 LIKE predicate -- underscore!
    
    stmt = """SELECT CITY
FROM STAFF 
WHERE EMPNAME LIKE 'B__t%';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a051exp""", 'a051s0')
    
    stmt = """DELETE FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test032(desc="""a052"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO STAFF VALUES ('E1','Alice',12,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E2','Betty',10,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E3','Carmen',13,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E4','Don',12,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E5','Ed',13,'Akron');"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0052 LIKE predicate -- ESCAPE character!
    
    # setup
    stmt = """INSERT INTO STAFF 
VALUES('E36','Huyan',36,'Xi_an%');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #  PASS:0052 If 1 row is inserted?
    
    stmt = """SELECT CITY
FROM STAFF 
WHERE CITY LIKE 'XiS___S%%'
ESCAPE 'S';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a052exp""", 'a052s0')
    
    stmt = """DELETE FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test033(desc="""a053"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO STAFF VALUES ('E1','Alice',12,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E2','Betty',10,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E3','Carmen',13,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E4','Don',12,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E5','Ed',13,'Akron');"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0053 NOT LIKE predicate!
    
    # setup
    stmt = """INSERT INTO STAFF 
VALUES('E36','Huyan',36,'Xi_an%');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #  PASS:0053 If 1 row is inserted?
    
    stmt = """SELECT COUNT(*)
FROM STAFF 
WHERE EMPNUM  NOT LIKE '_36';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a053exp""", 'a053s0')
    #  PASS:0053 If count = 5?
    
    stmt = """SELECT COUNT(*)
FROM STAFF 
WHERE NOT(EMPNUM  LIKE '_36');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a053exp""", 'a053s1')
    
    stmt = """DELETE FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test034(desc="""a054"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO STAFF VALUES ('E1','Alice',12,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E2','Betty',10,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E3','Carmen',13,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E4','Don',12,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E5','Ed',13,'Akron');"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0054 IS NULL predicate!
    
    # setup
    stmt = """INSERT INTO STAFF 
VALUES('E36','Huyan',36,NULL);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #  PASS:0054 If 1 row is inserted?
    
    stmt = """SELECT EMPNAME
FROM STAFF 
WHERE CITY IS NULL;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a054exp""", 'a054s0')
    
    stmt = """DELETE FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test035(desc="""a055"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO STAFF VALUES ('E1','Alice',12,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E2','Betty',10,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E3','Carmen',13,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E4','Don',12,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E5','Ed',13,'Akron');"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0055 NOT NULL predicate!
    
    # setup
    stmt = """INSERT INTO STAFF 
VALUES('E36','Huyan',36,NULL);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #  PASS:0055 If 1 row is inserted?
    
    stmt = """SELECT COUNT(*)
FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a055exp""", 'a055s0')
    #  PASS:0055 If count = 6?
    
    stmt = """SELECT COUNT(*)
FROM STAFF 
WHERE CITY IS NOT NULL;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a055exp""", 'a055s1')
    #  PASS:0055 If count = 5?
    
    stmt = """SELECT COUNT(*)
FROM STAFF 
WHERE NOT (CITY IS NULL);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a055exp""", 'a055s2')
    
    stmt = """DELETE FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test036(desc="""a056"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    stmt = """DELETE FROM PROJ;"""
    output = _dci.cmdexec(stmt)
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO STAFF VALUES ('E1','Alice',12,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E2','Betty',10,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E3','Carmen',13,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E4','Don',12,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E5','Ed',13,'Akron');"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO PROJ VALUES  ('P1','MXSS','Design',10000,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P2','CALM','Code',30000,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P3','SDP','Test',30000,'Tampa');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P4','SDP','Design',20000,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P5','IRM','Test',10000,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P6','PAYR','Design',50000,'Deale');"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO WORKS VALUES  ('E1','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P3',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P4',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P5',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P6',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P2',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E3','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P4',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P5',80);"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0056 NOT EXISTS predicate!
    
    stmt = """SELECT STAFF.EMPNAME
FROM STAFF 
WHERE NOT EXISTS
(SELECT *
FROM PROJ 
WHERE NOT EXISTS
(SELECT *
FROM WORKS 
WHERE STAFF.EMPNUM = WORKS.EMPNUM
AND WORKS.PNUM=PROJ.PNUM));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a056exp""", 'a056s0')
    
    stmt = """DELETE FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    stmt = """DELETE FROM PROJ;"""
    output = _dci.cmdexec(stmt)
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test037(desc="""a057"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    stmt = """DELETE FROM PROJ;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO STAFF VALUES ('E1','Alice',12,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E2','Betty',10,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E3','Carmen',13,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E4','Don',12,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E5','Ed',13,'Akron');"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO PROJ VALUES  ('P1','MXSS','Design',10000,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P2','CALM','Code',30000,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P3','SDP','Test',30000,'Tampa');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P4','SDP','Design',20000,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P5','IRM','Test',10000,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P6','PAYR','Design',50000,'Deale');"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0057 ALL quantifier !
    
    stmt = """SELECT CITY
FROM PROJ 
WHERE BUDGET > ALL
(SELECT BUDGET
FROM PROJ 
WHERE CITY='Vienna');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a057exp""", 'a057s0')
    
    stmt = """DELETE FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    stmt = """DELETE FROM PROJ;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test038(desc="""a058"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    stmt = """DELETE FROM PROJ;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO STAFF VALUES ('E1','Alice',12,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E2','Betty',10,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E3','Carmen',13,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E4','Don',12,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E5','Ed',13,'Akron');"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO PROJ VALUES  ('P1','MXSS','Design',10000,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P2','CALM','Code',30000,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P3','SDP','Test',30000,'Tampa');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P4','SDP','Design',20000,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P5','IRM','Test',10000,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P6','PAYR','Design',50000,'Deale');"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0058 SOME quantifier!
    
    stmt = """SELECT EMPNAME
FROM STAFF 
WHERE GRADE < SOME
(SELECT BUDGET/1000 - 39
FROM PROJ 
WHERE CITY='Deale');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a058exp""", 'a058s0')
    
    stmt = """DELETE FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    stmt = """DELETE FROM PROJ;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test039(desc="""a059"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    stmt = """DELETE FROM PROJ;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO STAFF VALUES ('E1','Alice',12,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E2','Betty',10,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E3','Carmen',13,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E4','Don',12,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E5','Ed',13,'Akron');"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO PROJ VALUES  ('P1','MXSS','Design',10000,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P2','CALM','Code',30000,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P3','SDP','Test',30000,'Tampa');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P4','SDP','Design',20000,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P5','IRM','Test',10000,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P6','PAYR','Design',50000,'Deale');"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0059 ANY quantifier !
    
    stmt = """SELECT EMPNAME
FROM STAFF 
WHERE GRADE < ANY
(SELECT BUDGET/1000 - 39
FROM PROJ 
WHERE CITY = 'Deale');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a059exp""", 'a059s0')
    
    stmt = """DELETE FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    stmt = """DELETE FROM PROJ;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test040(desc="""a061"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM TEMPXS;"""
    output = _dci.cmdexec(stmt)
    stmt = """DELETE FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO STAFF VALUES ('E1','Alice',12,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E2','Betty',10,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E3','Carmen',13,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E4','Don',12,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E5','Ed',13,'Akron');"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO TEMPXS 
SELECT EMPNUM, GRADE, CITY
FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """SELECT COUNT(*)
FROM TEMPXS;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a061exp""", 'a061s0')
    
    stmt = """DELETE FROM TEMPXS;"""
    output = _dci.cmdexec(stmt)
    stmt = """DELETE FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test041(desc="""a065"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM PROJ;"""
    output = _dci.cmdexec(stmt)
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO PROJ VALUES  ('P1','MXSS','Design',10000,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P2','CALM','Code',30000,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P3','SDP','Test',30000,'Tampa');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P4','SDP','Design',20000,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P5','IRM','Test',10000,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P6','PAYR','Design',50000,'Deale');"""
    output = _dci.cmdexec(stmt)
    
    # NO_TEST:0172 SELECT USER into short variable!
    #  Tests Host Variable
    #  TEST:0065 SELECT CHAR literal and term with numeric literal!
    
    stmt = """SELECT 'USER',PNAME
FROM PROJ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a065exp""", 'a065s0')
    #  PASS:0065 If 6 rows are selected and first column is value 'USER'?
    
    stmt = """SELECT PNUM,'BUDGET IN GRAMS IS ',BUDGET * 5
FROM PROJ 
WHERE PNUM = 'P1';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a065exp""", 'a065s1')
    
    stmt = """DELETE FROM PROJ;"""
    output = _dci.cmdexec(stmt)
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test042(desc="""a066"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E1','Alice',12,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E2','Betty',10,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E3','Carmen',13,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E4','Don',12,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E5','Ed',13,'Akron');"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0066 SELECT numeric literal!
    
    stmt = """SELECT EMPNUM,10
FROM STAFF 
WHERE GRADE = 10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a066exp""", 'a066s0')
    #  PASS:0066 If 1 row with values 'E2' and 10?
    
    stmt = """SELECT EMPNUM, 10
FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a066exp""", 'a066s1')
    
    stmt = """DELETE FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test043(desc="""a069"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO WORKS VALUES  ('E1','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P3',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P4',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P5',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P6',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P2',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E3','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P4',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P5',80);"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0069 HAVING COUNT with WHERE, GROUP BY!
    
    stmt = """SELECT PNUM
FROM WORKS 
WHERE PNUM > 'P1'
GROUP BY PNUM
HAVING COUNT(*) > 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a069exp""", 'a069s0')
    
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test044(desc="""a070"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO WORKS VALUES  ('E1','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P3',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P4',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P5',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P6',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P2',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E3','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P4',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P5',80);"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0070 HAVING COUNT with GROUP BY!
    
    stmt = """SELECT PNUM
FROM WORKS 
GROUP BY PNUM
HAVING COUNT(*) > 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a070exp""", 'a070s0')
    
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test045(desc="""a071"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO WORKS VALUES  ('E1','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P3',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P4',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P5',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P6',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P2',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E3','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P4',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P5',80);"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0071 HAVING MIN, MAX with GROUP BY 3 columns!
    
    stmt = """SELECT EMPNUM, PNUM, HOURS
FROM WORKS 
GROUP BY PNUM, EMPNUM, HOURS
HAVING MIN(HOURS) > 12 AND MAX(HOURS) < 80;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a071exp""", 'a071s0')
    
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test046(desc="""a072"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    stmt = """DELETE FROM PROJ;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO WORKS VALUES  ('E1','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P3',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P4',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P5',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P6',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P2',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E3','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P4',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P5',80);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO PROJ VALUES  ('P1','MXSS','Design',10000,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P2','CALM','Code',30000,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P3','SDP','Test',30000,'Tampa');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P4','SDP','Design',20000,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P5','IRM','Test',10000,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P6','PAYR','Design',50000,'Deale');"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0072 Nested HAVING IN with no outer reference!
    
    stmt = """SELECT WORKS.PNUM
FROM WORKS 
GROUP BY WORKS.PNUM
HAVING WORKS.PNUM IN (SELECT PROJ.PNUM
FROM PROJ 
GROUP BY PROJ.PNUM
HAVING SUM(PROJ.BUDGET) > 25000);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a072exp""", 'a072s0')
    
    stmt = """DELETE FROM PROJ;"""
    output = _dci.cmdexec(stmt)
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test047(desc="""a073"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO WORKS VALUES  ('E1','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P3',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P4',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P5',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P6',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P2',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E3','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P4',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P5',80);"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0073 HAVING MIN with no GROUP BY!
    
    stmt = """SELECT SUM(HOURS)
FROM WORKS 
HAVING MIN(PNUM) > 'P0';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a073exp""", 'a073s0')
    
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test048(desc="""a074"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO WORKS VALUES  ('E1','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P3',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P4',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P5',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P6',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P2',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E3','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P4',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P5',80);"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0074 GROUP BY col with SELECT col., SUM!
    
    stmt = """SELECT PNUM, SUM(HOURS)
FROM WORKS 
GROUP BY PNUM;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a074exp""", 'a074s0')
    
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test049(desc="""a075"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO WORKS VALUES  ('E1','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P3',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P4',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P5',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P6',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P2',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E3','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P4',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P5',80);"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0075 GROUP BY clause!
    
    stmt = """SELECT EMPNUM
FROM WORKS 
GROUP BY EMPNUM;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a075exp""", 'a075s0')
    
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test050(desc="""a076"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO WORKS VALUES  ('E1','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P3',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P4',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P5',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P6',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P2',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E3','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P4',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P5',80);"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0076 GROUP BY 2 columns!
    
    stmt = """SELECT EMPNUM,HOURS
FROM WORKS 
GROUP BY EMPNUM,HOURS;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a076exp""", 'a076s0')
    
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test051(desc="""a077"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO WORKS VALUES  ('E1','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P3',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P4',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P5',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P6',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P2',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E3','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P4',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P5',80);"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0077 GROUP BY all columns with SELECT * !
    
    stmt = """SELECT *
FROM WORKS 
GROUP BY PNUM,EMPNUM,HOURS;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a077exp""", 'a077s0')
    
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test052(desc="""a078"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO WORKS VALUES  ('E1','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P3',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P4',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P5',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P6',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P2',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E3','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P4',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P5',80);"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0078 GROUP BY three columns, SELECT two!
    
    stmt = """SELECT PNUM,EMPNUM
FROM WORKS 
GROUP BY EMPNUM,PNUM,HOURS;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a078exp""", 'a078s0')
    
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test053(desc="""a080"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM PROJ;"""
    output = _dci.cmdexec(stmt)
    stmt = """DELETE FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO PROJ VALUES  ('P1','MXSS','Design',10000,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P2','CALM','Code',30000,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P3','SDP','Test',30000,'Tampa');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P4','SDP','Design',20000,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P5','IRM','Test',10000,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P6','PAYR','Design',50000,'Deale');"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO STAFF VALUES ('E1','Alice',12,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E2','Betty',10,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E3','Carmen',13,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E4','Don',12,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E5','Ed',13,'Akron');"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0080 Simple two-table join!
    
    stmt = """SELECT EMPNUM,EMPNAME,GRADE,STAFF.CITY, PNAME, PROJ.CITY
FROM STAFF, PROJ 
WHERE STAFF.CITY = PROJ.CITY;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a080exp""", 'a080s0')
    
    stmt = """DELETE FROM PROJ;"""
    output = _dci.cmdexec(stmt)
    stmt = """DELETE FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test054(desc="""a081"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM PROJ;"""
    output = _dci.cmdexec(stmt)
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    stmt = """DELETE FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO PROJ VALUES  ('P1','MXSS','Design',10000,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P2','CALM','Code',30000,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P3','SDP','Test',30000,'Tampa');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P4','SDP','Design',20000,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P5','IRM','Test',10000,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P6','PAYR','Design',50000,'Deale');"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO WORKS VALUES  ('E1','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P3',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P4',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P5',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P6',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P2',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E3','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P4',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P5',80);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO STAFF VALUES ('E1','Alice',12,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E2','Betty',10,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E3','Carmen',13,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E4','Don',12,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E5','Ed',13,'Akron');"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0081 Simple two-table join with filter!
    
    stmt = """SELECT EMPNUM,EMPNAME,GRADE,STAFF.CITY,PNUM,PNAME,
PTYPE,BUDGET,PROJ.CITY
FROM STAFF, PROJ 
WHERE STAFF.CITY = PROJ.CITY
AND GRADE <> 12;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a081exp""", 'a081s0')
    
    stmt = """DELETE FROM PROJ;"""
    output = _dci.cmdexec(stmt)
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    stmt = """DELETE FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test055(desc="""a082"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM PROJ;"""
    output = _dci.cmdexec(stmt)
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    stmt = """DELETE FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO PROJ VALUES  ('P1','MXSS','Design',10000,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P2','CALM','Code',30000,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P3','SDP','Test',30000,'Tampa');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P4','SDP','Design',20000,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P5','IRM','Test',10000,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P6','PAYR','Design',50000,'Deale');"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO WORKS VALUES  ('E1','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P3',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P4',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P5',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P6',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P2',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E3','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P4',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P5',80);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO STAFF VALUES ('E1','Alice',12,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E2','Betty',10,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E3','Carmen',13,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E4','Don',12,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E5','Ed',13,'Akron');"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0082 Join 3 tables!
    
    stmt = """SELECT DISTINCT STAFF.CITY, PROJ.CITY
FROM STAFF, WORKS, PROJ 
WHERE STAFF.EMPNUM = WORKS.EMPNUM
AND WORKS.PNUM = PROJ.PNUM;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a082exp""", 'a082s0')
    
    stmt = """DELETE FROM PROJ;"""
    output = _dci.cmdexec(stmt)
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    stmt = """DELETE FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test056(desc="""a083"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO STAFF VALUES ('E1','Alice',12,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E2','Betty',10,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E3','Carmen',13,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E4','Don',12,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E5','Ed',13,'Akron');"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0083 Join a table with itself!
    
    stmt = """SELECT FIRST1.EMPNUM, SECOND2.EMPNUM
FROM STAFF FIRST1, STAFF SECOND2
WHERE FIRST1.CITY = SECOND2.CITY
AND FIRST1.EMPNUM < SECOND2.EMPNUM;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a083exp""", 'a083s0')
    
    stmt = """DELETE FROM STAFF;"""     
    _testmgr.testcase_end(desc)

def test057(desc="""a084"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM AA;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO AA 
VALUES('abcdefghijklmnopqrst');"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0084 Data type CHAR(20)!
    
    stmt = """SELECT CHARTEST
FROM  AA;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a084exp""", 'a084s0')
    
    stmt = """DELETE FROM AA;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test058(desc="""a085"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM CC;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO CC 
VALUES('abcdefghijklmnopqrst');"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0085 Data type CHARACTER(20)!
    
    stmt = """SELECT CHARTEST
FROM CC;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a085exp""", 'a085s0')
    
    stmt = """DELETE FROM CC;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test059(desc="""a086"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM EE;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO EE 
VALUES(123456);"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0086 Data type INTEGER!
    
    stmt = """SELECT INTTEST
FROM EE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a086exp""", 'a086s0')
    
    stmt = """DELETE FROM EE;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test060(desc="""a087"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM FF;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO FF 
VALUES(123456);"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0087 Data type INT!
    
    stmt = """SELECT INTTEST
FROM FF;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a087exp""", 'a087s0')
    
    stmt = """DELETE FROM FF;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test061(desc="""a089"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM HH;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO HH 
VALUES(123);"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0089 Data type SMALLINT!
    
    stmt = """SELECT *
FROM HH;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a089exp""", 'a089s0')
    
    stmt = """DELETE FROM HH;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test062(desc="""a093"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM LL;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO LL 
VALUES(123456.123456);"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0093 Data type NUMERIC(13,6)!
    
    stmt = """SELECT *
FROM LL;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a093exp""", 'a093s0')
    #  PASS:0093 If NUMTEST = 123456.123456 ?
    #  PASS:0093 OR  is between 123456.123451 and 123456.123461 ?
    
    stmt = """SELECT *
FROM LL 
WHERE NUMTEST > 123456.123450 and NUMTEST < 123456.123462;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a093exp""", 'a093s1')
    
    stmt = """DELETE FROM LL;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test063(desc="""a096"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO STAFF VALUES ('E1','Alice',12,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E2','Betty',10,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E3','Carmen',13,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E4','Don',12,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E5','Ed',13,'Akron');"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0096 Subquery with MAX in < comparison predicate!
    
    stmt = """SELECT EMPNUM
FROM STAFF 
WHERE GRADE <
(SELECT MAX(GRADE)
FROM STAFF);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a096exp""", 'a096s0')
    
    stmt = """DELETE FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test064(desc="""a097"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO STAFF VALUES ('E1','Alice',12,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E2','Betty',10,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E3','Carmen',13,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E4','Don',12,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E5','Ed',13,'Akron');"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0097 Subquery with AVG - 1 in <= comparison predicate!
    
    stmt = """SELECT *
FROM STAFF 
WHERE GRADE <=
(SELECT AVG(GRADE)-1
FROM STAFF);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a097exp""", 'a097s0')
    
    stmt = """DELETE FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test065(desc="""a098"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO STAFF VALUES ('E1','Alice',12,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E2','Betty',10,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E3','Carmen',13,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E4','Don',12,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E5','Ed',13,'Akron');"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO WORKS VALUES  ('E1','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P3',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P4',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P5',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P6',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P2',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E3','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P4',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P5',80);"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0098 IN predicate with simple subquery!
    
    stmt = """SELECT EMPNAME
FROM STAFF 
WHERE EMPNUM IN
(SELECT EMPNUM
FROM WORKS 
WHERE PNUM = 'P2')
ORDER BY EMPNAME;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a098exp""", 'a098s0')
    
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    stmt = """DELETE FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test066(desc="""a099"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    stmt = """DELETE FROM PROJ;"""
    output = _dci.cmdexec(stmt)
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO STAFF VALUES ('E1','Alice',12,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E2','Betty',10,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E3','Carmen',13,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E4','Don',12,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E5','Ed',13,'Akron');"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO PROJ VALUES  ('P1','MXSS','Design',10000,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P2','CALM','Code',30000,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P3','SDP','Test',30000,'Tampa');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P4','SDP','Design',20000,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P5','IRM','Test',10000,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P6','PAYR','Design',50000,'Deale');"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO WORKS VALUES  ('E1','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P3',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P4',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P5',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P6',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P2',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E3','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P4',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P5',80);"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0099 Nested IN predicate - 2 levels!
    
    stmt = """SELECT EMPNAME
FROM STAFF 
WHERE EMPNUM IN
(SELECT EMPNUM
FROM WORKS 
WHERE PNUM IN
(SELECT PNUM
FROM PROJ 
WHERE PTYPE = 'Design'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a099exp""", 'a099s0')
    
    stmt = """DELETE FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    stmt = """DELETE FROM PROJ;"""
    output = _dci.cmdexec(stmt)
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test067(desc="""a100"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM PROJ;"""
    output = _dci.cmdexec(stmt)
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    stmt = """DELETE FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO PROJ VALUES  ('P1','MXSS','Design',10000,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P2','CALM','Code',30000,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P3','SDP','Test',30000,'Tampa');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P4','SDP','Design',20000,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P5','IRM','Test',10000,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P6','PAYR','Design',50000,'Deale');"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO WORKS VALUES  ('E1','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P3',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P4',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P5',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P6',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P2',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E3','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P4',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P5',80);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO STAFF VALUES ('E1','Alice',12,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E2','Betty',10,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E3','Carmen',13,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E4','Don',12,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E5','Ed',13,'Akron');"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0100 Nested IN predicate - 6 levels!
    
    stmt = """SELECT EMPNUM, EMPNAME
FROM STAFF 
WHERE EMPNUM IN
(SELECT EMPNUM
FROM WORKS 
WHERE PNUM IN
(SELECT PNUM
FROM PROJ 
WHERE PTYPE IN
(SELECT PTYPE
FROM PROJ 
WHERE PNUM IN
(SELECT PNUM
FROM WORKS 
WHERE EMPNUM IN
(SELECT EMPNUM
FROM WORKS 
WHERE PNUM IN
(SELECT PNUM
FROM PROJ 
WHERE PTYPE = 'Design'))))))
ORDER BY EMPNUM;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a100exp""", 'a100s0')
    
    stmt = """DELETE FROM PROJ;"""
    output = _dci.cmdexec(stmt)
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    stmt = """DELETE FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test068(desc="""a101"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO WORKS VALUES  ('E1','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P3',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P4',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P5',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P6',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P2',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E3','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P4',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P5',80);"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0101 Quantified predicate <= ALL with AVG in GROUP BY!
    
    stmt = """SELECT EMPNUM,PNUM
FROM   WORKS 
WHERE  HOURS <= ALL
(SELECT AVG(HOURS)
FROM   WORKS 
GROUP BY PNUM);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a101exp""", 'a101s0')
    
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test069(desc="""a102"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO WORKS VALUES  ('E1','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P3',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P4',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P5',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P6',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P2',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E3','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P4',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P5',80);"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0102 Nested NOT EXISTS with correlated subquery and DISTINCT!
    
    stmt = """SELECT DISTINCT EMPNUM
FROM WORKS WORKSX
WHERE NOT EXISTS
(SELECT *
FROM WORKS WORKSY
WHERE EMPNUM = 'E2'
AND NOT EXISTS
(SELECT *
FROM WORKS WORKSZ
WHERE WORKSZ.EMPNUM = WORKSX.EMPNUM
AND WORKSZ.PNUM = WORKSY.PNUM));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a102exp""", 'a102s0')
    
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test070(desc="""a103"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    stmt = """DELETE FROM PROJ;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO STAFF VALUES ('E1','Alice',12,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E2','Betty',10,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E3','Carmen',13,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E4','Don',12,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E5','Ed',13,'Akron');"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO PROJ VALUES  ('P1','MXSS','Design',10000,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P2','CALM','Code',30000,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P3','SDP','Test',30000,'Tampa');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P4','SDP','Design',20000,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P5','IRM','Test',10000,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P6','PAYR','Design',50000,'Deale');"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0103 Subquery with comparison predicate!
    
    stmt = """SELECT PNUM
FROM PROJ 
WHERE PROJ.CITY =
(SELECT STAFF.CITY
FROM STAFF 
WHERE EMPNUM = 'E1');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a103exp""", 'a103s0')
    
    stmt = """DELETE FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    stmt = """DELETE FROM PROJ;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test071(desc="""a104"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    stmt = """DELETE FROM PROJ;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO STAFF VALUES ('E1','Alice',12,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E2','Betty',10,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E3','Carmen',13,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E4','Don',12,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E5','Ed',13,'Akron');"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO PROJ VALUES  ('P1','MXSS','Design',10000,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P2','CALM','Code',30000,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P3','SDP','Test',30000,'Tampa');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P4','SDP','Design',20000,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P5','IRM','Test',10000,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P6','PAYR','Design',50000,'Deale');"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0104 SQLCODE < 0, subquery with more than 1 value!
    
    ##expectfile ${test_dir}/a104exp a104s0
    stmt = """SELECT PNUM
FROM PROJ 
WHERE PROJ.CITY =
(SELECT STAFF.CITY
FROM STAFF 
WHERE EMPNUM > 'E1' );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8401')
    
    stmt = """DELETE FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    stmt = """DELETE FROM PROJ;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test072(desc="""a105"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    stmt = """DELETE FROM PROJ;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO STAFF VALUES ('E1','Alice',12,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E2','Betty',10,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E3','Carmen',13,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E4','Don',12,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E5','Ed',13,'Akron');"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO PROJ VALUES  ('P1','MXSS','Design',10000,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P2','CALM','Code',30000,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P3','SDP','Test',30000,'Tampa');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P4','SDP','Design',20000,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P5','IRM','Test',10000,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P6','PAYR','Design',50000,'Deale');"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0105 Subquery in comparison predicate is empty!
    
    stmt = """SELECT COUNT(*)
FROM STAFF 
WHERE STAFF.CITY =
(SELECT PROJ.CITY
FROM PROJ 
WHERE PNUM > 'P7');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a105exp""", 'a105s0')
    #  PASS:0105 If count = 0?
    
    stmt = """SELECT COUNT(*)
FROM STAFF 
WHERE NOT (STAFF.CITY =
(SELECT PROJ.CITY
FROM PROJ 
WHERE PNUM > 'P7' ));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a105exp""", 'a105s1')
    
    stmt = """DELETE FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    stmt = """DELETE FROM PROJ;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test073(desc="""a106"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM PROJ;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO PROJ VALUES  ('P1','MXSS','Design',10000,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P2','CALM','Code',30000,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P3','SDP','Test',30000,'Tampa');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P4','SDP','Design',20000,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P5','IRM','Test',10000,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P6','PAYR','Design',50000,'Deale');"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0106 Comparison predicate <> !
    
    stmt = """SELECT PNUM
FROM PROJ 
WHERE CITY <> 'Deale';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a106exp""", 'a106s0')
    
    stmt = """DELETE FROM PROJ;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test074(desc="""a107"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO WORKS VALUES  ('E1','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P3',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P4',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P5',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P6',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P2',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E3','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P4',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P5',80);"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0107 Comp predicate with short string logically blank padded!
    
    stmt = """SELECT COUNT(*)
FROM WORKS 
WHERE EMPNUM = 'E1';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a107exp""", 'a107s0')
    #  PASS:0107 If count = 6 ?
    
    stmt = """SELECT COUNT(*)
FROM WORKS 
WHERE EMPNUM = 'E1' AND EMPNUM = 'E1 ';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a107exp""", 'a107s1')
    
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test075(desc="""a108"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO STAFF VALUES ('E1','Alice',12,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E2','Betty',10,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E3','Carmen',13,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E4','Don',12,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E5','Ed',13,'Akron');"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0108 Search condition true OR NOT(true)!
    
    stmt = """SELECT EMPNUM,CITY
FROM   STAFF 
WHERE  EMPNUM='E1' OR NOT(EMPNUM='E1');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a108exp""", 'a108s0')
    
    stmt = """DELETE FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test076(desc="""a114"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO WORKS VALUES  ('E1','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P3',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P4',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P5',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P6',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P2',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E3','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P4',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P5',80);"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0114 Set functions without GROUP BY returns 1 row!
    
    stmt = """SELECT SUM(HOURS),AVG(HOURS),MIN(HOURS),MAX(HOURS)
FROM    WORKS 
WHERE   EMPNUM='E1';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a114exp""", 'a114s0')
    
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test077(desc="""a117"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO WORKS VALUES  ('E1','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P3',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P4',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P5',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P6',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P2',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E3','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P4',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P5',80);"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0117 GROUP BY column, set functions with several groups!
    
    stmt = """SELECT PNUM,AVG(HOURS),MIN(HOURS),MAX(HOURS)
FROM    WORKS 
GROUP BY PNUM
ORDER BY PNUM;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a117exp""", 'a117s0')
    
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test078(desc="""a118"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """delete from WORKS;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO WORKS VALUES  ('E1','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P3',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P4',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P5',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P6',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P2',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E3','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P4',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P5',80);"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0118 Monadic arithmetic operator +!
    
    stmt = """SELECT +MAX(DISTINCT HOURS)
FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a118exp""", 'a118s0')
    
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test079(desc="""a119"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """delete from WORKS;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO WORKS VALUES  ('E1','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P3',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P4',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P5',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P6',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P2',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E3','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P4',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P5',80);"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0119 Monadic arithmetic operator -!
    
    stmt = """SELECT -MAX(DISTINCT HOURS)
FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a119exp""", 'a119s0')
    
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test080(desc="""a120"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM WORKS1;"""
    output = _dci.cmdexec(stmt)
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO WORKS VALUES  ('E1','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P3',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P4',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P5',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P6',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P2',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E3','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P4',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P5',80);"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0120 Value expression with NULL primary IS NULL!
    
    # setup
    stmt = """INSERT INTO WORKS1 
SELECT *
FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 12)
    # PASS:0120 If 12 rows are inserted ?
    
    # setup
    stmt = """INSERT INTO WORKS1 
VALUES('E9','P1',NULL);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #  PASS:0120 If 1 row is inserted?
    
    stmt = """SELECT EMPNUM
FROM WORKS1 
WHERE HOURS IS NULL;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a120exp""", 'a120s0')
    # PASS:0120 If EMPNUM = 'E9'?
    
    # NOTE:0120 we insert into WORKS from WORKS1
    
    # setup
    stmt = """INSERT INTO WORKS 
SELECT EMPNUM,'P9',20+HOURS
FROM WORKS1 
WHERE EMPNUM='E9';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #  PASS:0120 If 1 row is inserted?
    
    stmt = """SELECT COUNT(*)
FROM WORKS 
WHERE EMPNUM='E9';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a120exp""", 'a120s1')
    #  PASS:0120 If count = 1      ?
    
    stmt = """SELECT COUNT(*)
FROM WORKS 
WHERE HOURS IS NULL;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a120exp""", 'a120s2')
    
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    stmt = """DELETE FROM WORKS1;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test081(desc="""a121"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM VTABLE;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO VTABLE VALUES(10,+20,30,40,10.50);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO VTABLE VALUES(0,1,2,3,4.25);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO VTABLE VALUES(100,200,300,400,500.01);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO VTABLE VALUES(1000,-2000,3000,NULL,4000.00);"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0121 Dyadic operators +, -, *, /!
    
    stmt = """SELECT COUNT(*)
FROM VTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a121exp""", 'a121s0')
    #  PASS:0121 If count = 4 ?
    
    stmt = """SELECT +COL1+COL2 - COL3*COL4/COL1
FROM VTABLE 
WHERE COL1=10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a121exp""", 'a121s1')
    
    stmt = """DELETE FROM VTABLE;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test082(desc="""a122"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM VTABLE;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO VTABLE VALUES(10,+20,30,40,10.50);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO VTABLE VALUES(0,1,2,3,4.25);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO VTABLE VALUES(100,200,300,400,500.01);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO VTABLE VALUES(1000,-2000,3000,NULL,4000.00);"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0122 Divisor shall not be zero!
    
    ##expectfile ${test_dir}/a122exp a122s0
    stmt = """SELECT COL2/COL1+COL3
FROM VTABLE 
WHERE COL4=3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8419')
    
    stmt = """DELETE FROM VTABLE;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test083(desc="""a123"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM VTABLE;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO VTABLE VALUES(10,+20,30,40,10.50);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO VTABLE VALUES(0,1,2,3,4.25);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO VTABLE VALUES(100,200,300,400,500.01);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO VTABLE VALUES(1000,-2000,3000,NULL,4000.00);"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0123 Evaluation order of expression!
    
    stmt = """SELECT (-COL2+COL1)*COL3 - COL3/COL1
FROM VTABLE 
WHERE COL4 IS NULL;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a123exp""", 'a123s0')
    
    stmt = """DELETE FROM VTABLE;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test084(desc="""a129"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO STAFF VALUES ('E1','Alice',12,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E2','Betty',10,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E3','Carmen',13,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E4','Don',12,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E5','Ed',13,'Akron');"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0129 Double quote work in character string literal!
    
    # setup
    stmt = """INSERT INTO STAFF 
VALUES('E8','Yang Ling',15,'Xi''an');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #  PASS:0129 If 1 row is inserted?
    
    stmt = """SELECT GRADE,CITY
FROM STAFF 
WHERE EMPNUM = 'E8';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a129exp""", 'a129s0')
    
    stmt = """DELETE FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test085(desc="""a135"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO WORKS VALUES  ('E1','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P3',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P4',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P5',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P6',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P2',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E3','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P4',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P5',80);"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0135 Upper and loer case letters are distinct!
    
    # setup
    stmt = """INSERT INTO WORKS 
VALUES('UPP','low',100);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #  PASS:0135 If 1 row is inserted?
    
    stmt = """SELECT EMPNUM,PNUM
FROM WORKS 
WHERE EMPNUM='UPP' AND PNUM='low';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a135exp""", 'a135s0')
    # PASS:0135 If EMPNUM = 'UPP' and PNUM = 'low'?
    
    ##expect any *--- 0 row(s) selected.*
    stmt = """SELECT EMPNUM,PNUM
FROM WORKS 
WHERE EMPNUM='upp' OR PNUM='LOW';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test086(desc="""a151"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """delete from STAFF;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO STAFF VALUES ('E1','Alice',12,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E2','Betty',10,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E3','Carmen',13,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E4','Don',12,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E5','Ed',13,'Akron');"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0151 CREATE VIEW!
    
    stmt = """SELECT COUNT(*)
FROM STAFFV1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a151exp""", 'a151s0')
    
    stmt = """delete from STAFF ;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test087(desc="""a158"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert INTO STAFF VALUES ('E1','Alice',12,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """insert INTO STAFF VALUES ('E2','Betty',10,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """insert INTO STAFF VALUES ('E3','Carmen',13,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """insert INTO STAFF VALUES ('E4','Don',12,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """insert INTO STAFF VALUES ('E5','Ed',13,'Akron');"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO WORKS VALUES  ('E1','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P3',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P4',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P5',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P6',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P2',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E3','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P4',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P5',80);"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0158 SELECT with UNION and NOT EXISTS subquery!                        Z
    
    stmt = """SELECT EMPNAME,PNUM,HOURS
FROM STAFF,WORKS 
WHERE STAFF.EMPNUM = WORKS.EMPNUM
UNION
SELECT EMPNAME,PNUM,HOURS
FROM STAFF,WORKS 
WHERE NOT EXISTS
(SELECT HOURS
FROM WORKS 
WHERE STAFF.EMPNUM = WORKS.EMPNUM);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a158exp""", 'a158s0')
    
    stmt = """DELETE FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test088(desc="""a159"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P3',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P4',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P5',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P6',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P2',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E3','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P4',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P5',80);"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0159 SELECT with 2 UNIONs, ORDER BY 2 integers!
    
    stmt = """SELECT PNUM,EMPNUM,HOURS
FROM WORKS 
WHERE HOURS=80
UNION
SELECT PNUM,EMPNUM,HOURS
FROM WORKS 
WHERE HOURS=40
UNION
SELECT PNUM,EMPNUM,HOURS
FROM WORKS 
WHERE HOURS=20
ORDER BY 3,1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a159exp""", 'a159s0')
    
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test089(desc="""a160"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO WORKS VALUES  ('E1','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P3',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P4',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P5',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P6',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P2',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E3','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P4',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P5',80);"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0160 SELECT with parenthesized UNION, UNION ALL!
    
    stmt = """SELECT PNUM,EMPNUM,HOURS
FROM WORKS 
WHERE HOURS=12
UNION ALL
(SELECT PNUM,EMPNUM,HOURS
FROM WORKS 
UNION
SELECT PNUM,EMPNUM,HOURS
FROM WORKS 
WHERE HOURS=80)
ORDER BY 2,1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a160exp""", 'a160s0')
    
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test090(desc="""a164"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P3',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P4',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P5',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P6',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P2',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E3','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P4',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P5',80);"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0164 SELECT:default is ALL, not DISTINCT!
    
    stmt = """SELECT EMPNUM
FROM WORKS 
WHERE HOURS = 12;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a164exp""", 'a164s0')
    
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test091(desc="""a168"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO WORKS VALUES  ('E1','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P3',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P4',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P5',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P6',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P2',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E3','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P4',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P5',80);"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0168 SUM function!
    
    # setup
    stmt = """INSERT INTO WORKS 
VALUES('E5','P5',NULL);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #  PASS:0168 If 1 row is inserted?
    
    stmt = """SELECT SUM(HOURS)
FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a168exp""", 'a168s0')
    
    stmt = """DELET FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test092(desc="""a169"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO WORKS VALUES  ('E1','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P3',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P4',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P5',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P6',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P2',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E3','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P4',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P5',80);"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0169 COUNT(*) function !
    
    # setup
    stmt = """INSERT INTO WORKS 
VALUES('E5','P5',NULL);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #  PASS:0169 If 1 row is inserted?
    
    stmt = """SELECT COUNT(*)
FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a169exp""", 'a169s0')
    
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test093(desc="""a170"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P3',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P4',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P5',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P6',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P2',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E3','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P4',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P5',80);"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0170 SUM DISTINCT function with WHERE clause!
    
    stmt = """SELECT SUM(DISTINCT HOURS)
FROM WORKS 
WHERE PNUM = 'P2';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a170exp""", 'a170s0')
    
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test094(desc="""a171"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P3',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P4',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P5',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P6',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P2',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E3','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P4',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P5',80);"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0171 SUM(column) + value!
    
    stmt = """SELECT SUM(HOURS)+10
FROM WORKS 
WHERE PNUM = 'P2';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a171exp""", 'a171s0')
    
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test095(desc="""a173"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM BB;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO BB 
VALUES('a');"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0173 Data type CHAR!
    
    stmt = """SELECT CHARTEST
FROM BB;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a173exp""", 'a173s0')
    
    stmt = """DELETE FROM BB;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test096(desc="""a174"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM DD;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO DD 
VALUES('a');"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0174 Data type CHARACTER!
    
    stmt = """SELECT CHARTEST
FROM DD;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a174exp""", 'a174s0')
    
    stmt = """DELETE FROM DD;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test097(desc="""a202"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM TEXT240;"""
    output = _dci.cmdexec(stmt)
    
    # NO_TEST:0202 Host variable names same as column name!
    
    # Testing host identifier
    
    # TEST:0234 SQL-style comments with SQL statements!
    # OPTIONAL TEST
    
    stmt = """DELETE  -- we empty the table
FROM TEXT240;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 0)
    
    stmt = """INSERT INTO TEXT240   -- This is the test for the rules
VALUES         -- for the placement
('SQL-STYLE COMMENTS') -- of
-- SQL-style comments
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #  PASS:0234 If 1 row is inserted?
    
    stmt = """SELECT *
FROM TEXT240;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a202exp""", 'a202s0')
    
    stmt = """DELETE FROM TEXT240;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test098(desc="""a205"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    stmt = """DELETE FROM PROJ;"""
    output = _dci.cmdexec(stmt)
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO STAFF VALUES ('E1','Alice',12,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E2','Betty',10,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E3','Carmen',13,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E4','Don',12,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E5','Ed',13,'Akron');"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO PROJ VALUES  ('P1','MXSS','Design',10000,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P2','CALM','Code',30000,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P3','SDP','Test',30000,'Tampa');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P4','SDP','Design',20000,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P5','IRM','Test',10000,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P6','PAYR','Design',50000,'Deale');"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO WORKS VALUES  ('E1','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P3',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P4',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P5',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P6',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P2',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E3','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P4',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P5',80);"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0205 Cartesian product is produced without WHERE clause!
    
    stmt = """SELECT GRADE, HOURS, BUDGET
FROM STAFF, WORKS, PROJ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a205exp""", 'a205s0')
    
    stmt = """DELETE FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    stmt = """DELETE FROM PROJ;"""
    output = _dci.cmdexec(stmt)
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test099(desc="""a208"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO STAFF VALUES ('E1','Alice',12,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E2','Betty',10,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E3','Carmen',13,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E4','Don',12,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E5','Ed',13,'Akron');"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0208 Upper and lower case in LIKE predicate!
    
    # setup
    stmt = """INSERT INTO STAFF 
VALUES('E7', 'yanping',26,'China');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    # PASS:0208 If 1 row is inserted?
    
    stmt = """INSERT INTO STAFF 
VALUES('E8','YANPING',30,'NIST');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #  PASS:0208 If 1 row is inserted?
    
    stmt = """SELECT CITY
FROM STAFF 
WHERE EMPNAME LIKE 'yan____%';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a208exp""", 'a208s0')
    #  PASS:0208 If CITY = 'China'?
    
    stmt = """SELECT CITY
FROM STAFF 
WHERE EMPNAME LIKE 'YAN____%';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a208exp""", 'a208s1')
    
    stmt = """DELETE FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test100(desc="""a215"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM T8;"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0215 FIPS sizing -- 6 columns in a UNIQUE constraint!
    
    # FIPS sizing TEST
    
    # setup
    stmt = """INSERT INTO T8 
VALUES('th','seco','third3','fourth_4','fifth_colu',
'sixth_column','seventh_column','last_column_of_t');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #  PASS:0215 If 1 row is inserted?
    
    ##expectfile ${test_dir}/a215exp a215s0
    stmt = """INSERT INTO T8 
VALUES('th','seco','third3','fourth_4','fifth_colu',
'sixth_column','column_seventh','column_eighth_la');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8102')
    #  PASS:0215 If ERROR, unique constraint, 0 rows inserted?
    
    stmt = """SELECT COL1,COL2,COL3,COL4,COL5,COL6,COL7,COL8
FROM T8;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a215exp""", 'a215s1')
    
    stmt = """DELETE FROM T8;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test101(desc="""a218"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM T12;"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0218 FIPS sizing -- 6 columns in GROUP BY!
    
    # FIPS sizing TEST
    
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
    #  PASS:0218 If 1 row is inserted?
    
    stmt = """SELECT COUNT(*)
FROM  T12;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a218exp""", 'a218s0')
    #  PASS:0218 If count = 4?
    
    stmt = """SELECT COL6,SUM(COL11),MAX(COL12)
FROM T12 
GROUP BY COL1,COL5,COL3,COL6,COL2,COL4
ORDER BY COL6 DESC;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a218exp""", 'a218s1')
    
    stmt = """DELETE FROM T12;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test102(desc="""a219"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM T12;"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0219 FIPS sizing -- 120 bytes in GROUP BY!
    
    # FIPS sizing TEST
    
    # setup
    stmt = """INSERT INTO T12 
VALUES('1','22','4444','666666','88888888','1010101010',
'20202020202020202020','303030303030303030303030303030',
'4040404040404040404040404040404040404040', '5050...50',111,112);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    # PASS:0219 If 1 row is inserted?
    
    stmt = """INSERT INTO T12 
VALUES('1','22','4444','666666','88888889','1010101010',
'20202020202020202020','303030303030303030303030303030',
'4040404040404040404040404040404040404040', '5050...50',333,336);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    # PASS:0219 If 1 row is inserted?
    
    stmt = """INSERT INTO T12 
VALUES('1','22','4444','666666','88888889','1010101010',
'20202020202020202020','303030303030303030303030303030',
'4040404040404040404040404040404040404040', '5050...50',444,448);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    # PASS:0219 If 1 row is inserted?
    
    stmt = """INSERT INTO T12 
VALUES('1','22','4444','666666','88888888','1010101010',
'20202020202020202020','303030303030303030303030303030',
'4040404040404040404040404040404040404040', '5050...50',222,224);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #  PASS:0219 If 1 row is inserted?
    
    stmt = """SELECT COUNT(*)
FROM  T12;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a219exp""", 'a219s0')
    #  PASS:0219 If count = 4?
    
    stmt = """SELECT COL5,SUM(COL11),MAX(COL12)
FROM T12 
GROUP BY COL9,COL5,COL7,COL4,COL3,COL8
ORDER BY COL5 DESC;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a219exp""", 'a219s1')
    
    stmt = """DELETE FROM T12;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test103(desc="""a220"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM T12;"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0220 FIPS sizing -- 6 column in ORDER BY!
    
    # FIPS sizing TEST
    
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
    #  PASS:0220 If 1 row is inserted?
    
    stmt = """SELECT COUNT(*)
FROM  T12;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a220exp""", 'a220s0')
    #  PASS:0220 If count = 4?
    
    stmt = """SELECT COL5,COL6,COL11,COL3,COL4,COL7,COL8
FROM T12 
ORDER BY COL7,COL8,COL3,COL4,COL6,COL5 DESC;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a220exp""", 'a220s1')
    
    stmt = """DELETE FROM T12;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test104(desc="""a221"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM T12;"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0221 FIPS sizing -- 120 bytes in ORDER BY!
    
    # FIPS sizing TEST
    
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
    #  PASS:0221 If 1 row is inserted?
    
    stmt = """SELECT COUNT(*)
FROM  T12;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a221exp""", 'a221s0')
    #  PASS:0221 If count = 4?
    
    stmt = """SELECT COL3,COL11,COL9,COL8,COL7,COL5,COL4
FROM T12 
ORDER BY COL9,COL8,COL7,COL5,COL4,COL3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a221exp""", 'a221s1')
    
    stmt = """DELETE FROM T12;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test105(desc="""a222"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM T240;"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0222 FIPS sizing -- Length(240) of a character string!
    
    # FIPS sizing TEST
    # NOTE:0222 Literal length is only 78
    
    # setup
    stmt = """INSERT INTO T240 VALUES(
'Now is the time for all good men and women to come to the aid of their country'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #  PASS:0222 If 1 row is inserted?
    
    stmt = """SELECT *
FROM T240;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a222exp""", 'a222s0')
    
    stmt = """DELETE FROM T240;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test106(desc="""a226"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    stmt = """DELETE FROM PROJ;"""
    output = _dci.cmdexec(stmt)
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO STAFF VALUES ('E1','Alice',12,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E2','Betty',10,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E3','Carmen',13,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E4','Don',12,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E5','Ed',13,'Akron');"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO PROJ VALUES  ('P1','MXSS','Design',10000,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P2','CALM','Code',30000,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P3','SDP','Test',30000,'Tampa');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P4','SDP','Design',20000,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P5','IRM','Test',10000,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P6','PAYR','Design',50000,'Deale');"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO WORKS VALUES  ('E1','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P3',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P4',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P5',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P6',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P2',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E3','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P4',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P5',80);"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0226 FIPS sizing - 10 tables in SQL statement!
    
    #  FIPS sizing TEST
    
    stmt = """SELECT EMPNUM, EMPNAME
FROM STAFF 
WHERE EMPNUM IN
(SELECT EMPNUM  FROM WORKS 
WHERE PNUM IN
(SELECT PNUM  FROM PROJ 
WHERE PTYPE IN
(SELECT PTYPE  FROM PROJ 
WHERE PNUM IN
(SELECT PNUM  FROM WORKS 
WHERE EMPNUM IN
(SELECT EMPNUM  FROM WORKS 
WHERE PNUM IN
(SELECT PNUM   FROM PROJ 
WHERE PTYPE IN
(SELECT PTYPE  FROM PROJ 
WHERE CITY IN
(SELECT CITY  FROM STAFF 
WHERE EMPNUM IN
(SELECT EMPNUM  FROM WORKS 
WHERE HOURS = 20
AND PNUM = 'P2' )))))))));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a226exp""", 'a226s0')
    
    stmt = """DELETE FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    stmt = """DELETE FROM PROJ;"""
    output = _dci.cmdexec(stmt)
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test107(desc="""a227"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM PROJ;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO PROJ VALUES  ('P1','MXSS','Design',10000,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P2','CALM','Code',30000,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P3','SDP','Test',30000,'Tampa');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P4','SDP','Design',20000,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P5','IRM','Test',10000,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P6','PAYR','Design',50000,'Deale');"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0227 BETWEEN predicate with character string values!
    
    stmt = """SELECT PNUM
FROM   PROJ 
WHERE  PNAME BETWEEN 'A' AND 'F';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a227exp""", 'a227s0')
    #  PASS:0227 If PNUM = 'P2'?
    
    stmt = """SELECT PNUM
FROM   PROJ 
WHERE PNAME >= 'A' AND PNAME <= 'F';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a227exp""", 'a227s1')
    
    stmt = """DELETE FROM PROJ;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test108(desc="""a228"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM PROJ;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO STAFF VALUES ('E1','Alice',12,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E2','Betty',10,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E3','Carmen',13,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E4','Don',12,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E5','Ed',13,'Akron');"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0228 NOT BETWEEN predicate with character string values!
    
    stmt = """SELECT CITY
FROM   STAFF 
WHERE  EMPNAME NOT BETWEEN 'A' AND 'E';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a228exp""", 'a228s0')
    #  PASS:0228 If CITY = 'Akron'?
    
    stmt = """SELECT CITY
FROM   STAFF 
WHERE  NOT( EMPNAME BETWEEN 'A' AND 'E' );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a228exp""", 'a228s1')
    
    stmt = """DELETE FROM PROJ;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test109(desc="""a229"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO STAFF VALUES ('E1','Alice',12,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E2','Betty',10,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E3','Carmen',13,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E4','Don',12,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E5','Ed',13,'Akron');"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0229 Case-sensitive LIKE predicate!
    
    # setup
    stmt = """INSERT INTO STAFF 
VALUES('E6','ALICE',11,'Gaithersburg');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #  PASS:0229 If 1 row is inserted?
    
    stmt = """SELECT EMPNAME
FROM   STAFF 
WHERE  EMPNAME LIKE 'Ali%';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a229exp""", 'a229s0')
    #  PASS:0229 If 1 row is returned and EMPNAME = 'Alice' (not 'ALICE')?
    
    stmt = """SELECT EMPNAME
FROM   STAFF 
WHERE  EMPNAME LIKE 'ALI%';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a229exp""", 'a229s1')
    
    stmt = """DELETE FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test110(desc="""a233"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM TEMPXS;"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0233 Table as multiset of rows - INSERT duplicate VALUES()!
    
    # setup
    stmt = """INSERT INTO TEMPXS 
VALUES('E1',11,'Deale');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    # PASS:0233 If 1 row is inserted?
    
    stmt = """INSERT INTO TEMPXS 
VALUES('E1',11,'Deale');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #  PASS:0233 If 1 row is inserted?
    
    stmt = """SELECT COUNT(*)
FROM TEMPXS 
WHERE EMPNUM='E1' AND GRADE=11 AND CITY='Deale';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a233exp""", 'a233s0')
    
    stmt = """DELETE FROM TEMPXS;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test111(desc="""a234"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM TEXT240;"""
    output = _dci.cmdexec(stmt)
    
    # NO_TEST:0202 Host variable names same as column name!
    
    # Testing host identifier
    
    # TEST:0234 SQL-style comments with SQL statements!
    # OPTIONAL TEST
    
    stmt = """DELETE  -- we empty the table
FROM TEXT240;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 0)
    
    stmt = """INSERT INTO TEXT240   -- This is the test for the rules
VALUES         -- for the placement
('SQL-STYLE COMMENTS') -- of
-- SQL-style comments
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #  PASS:0234 If 1 row is inserted?
    
    stmt = """SELECT *
FROM TEXT240;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a234exp""", 'a234s0')
    
    stmt = """DELETE FROM TEXT240;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test112(desc="""a243"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM HH;"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0243 FIPS sizing - precision of SMALLINT >= 4!
    
    # FIPS sizing TEST
    
    stmt = """DELETE FROM HH;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 0)
    # Making sure the table is empty
    
    # setup
    stmt = """INSERT INTO HH 
VALUES(9999);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #  PASS:0243 If 1 row is inserted?
    
    stmt = """SELECT COUNT(*)
FROM HH 
WHERE SMALLTEST = 9999;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a243exp""", 'a243s0')
    # PASS:0243 If count = 1?
    
    # setup
    stmt = """INSERT INTO HH 
VALUES(-9999);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #  PASS:0243 If 1 row is inserted?
    
    stmt = """SELECT SMALLTEST
FROM HH 
WHERE SMALLTEST = -9999;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a243exp""", 'a243s1')
    
    stmt = """DELETE FROM HH;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test113(desc="""a244"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM EE;"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0244 FIPS sizing - precision of INTEGER >= 9!
    
    # FIPS sizing TEST
    
    stmt = """DELETE FROM EE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 0)
    # Making sure the table is empty
    
    # setup
    stmt = """INSERT INTO EE 
VALUES(999999999);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #  PASS:0244 If 1 row is inserted?
    
    stmt = """SELECT INTTEST
FROM EE 
WHERE INTTEST = 999999999;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a244exp""", 'a244s0')
    # PASS:0244 If INTTEST = 999999999?
    
    # setup
    stmt = """INSERT INTO EE 
VALUES(-999999999);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #  PASS:0244 If 1 row is inserted?
    
    stmt = """SELECT COUNT(*)
FROM EE 
WHERE INTTEST = -999999999;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a244exp""", 'a244s1')
    
    stmt = """DELETE FROM EE;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test114(desc="""a246"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM T100;"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0246 FIPS sizing - 100 values in INSERT!
    
    # FIPS sizing TEST
    
    stmt = """DELETE FROM T100;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 0)
    # Making sure the table is empty
    
    # setup
    stmt = """INSERT INTO T100 
VALUES('ZA','ZB','CA','ZC','ZD','AA','ZE','ZF','BA','ZG',
'YA','YB','CB','YC','YD','AB','YE','YF','BB','YG',
'XA','XB','CC','XC','XD','AC','XE','XF','BC','XG',
'UA','UB','CD','UC','UD','AD','UE','UF','BD','UG',
'VA','VB','CE','VC','VD','AE','VE','VF','BE','VG',
'WA','WB','CF','WC','WD','AF','WE','WF','BF','WG',
'LA','LB','CG','LC','LD','AG','LE','LF','BG','LG',
'MA','MB','CH','MC','MD','AH','ME','MF','BH','MG',
'NA','NB','CI','NC','ND','AI','NE','NF','BI','NG',
'OA','OB','CJ','OC','OD','AJ','OE','OF','BJ','OG');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #  PASS:0246 If 1 row is inserted?
    
    stmt = """SELECT C6, C16, C26, C36, C46, C56, C66, C76, C86, C96, C100
FROM T100 
WHERE C1 = 'ZA' AND C2 = 'ZB';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a246exp""", 'a246s0')
    
    stmt = """DELETE FROM T100;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test115(desc="""a247"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM T100;"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0247 FIPS sizing - 20 values in update SET clause!
    
    # FIPS sizing TEST
    
    stmt = """DELETE FROM T100;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 0)
    # Making sure the table is empty
    
    # setup
    stmt = """INSERT INTO T100 
VALUES('ZA','ZB','CA','ZC','ZD','AA','ZE','ZF','BA','ZG',
'YA','YB','CB','YC','YD','AB','YE','YF','BB','YG',
'XA','XB','CC','XC','XD','AC','XE','XF','BC','XG',
'UA','UB','CD','UC','UD','AD','UE','UF','BD','UG',
'VA','VB','CE','VC','VD','AE','VE','VF','BE','VG',
'WA','WB','CF','WC','WD','AF','WE','WF','BF','WG',
'LA','LB','CG','LC','LD','AG','LE','LF','BG','LG',
'MA','MB','CH','MC','MD','AH','AE','AF','BH','BG',
'NA','NB','CI','NC','ND','AI','NE','NF','BI','NG',
'OA','OB','CJ','OC','OD','AJ','OE','OF','BJ','OG');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    # PASS:0247 If 1 row is inserted?
    
    stmt = """UPDATE T100 
SET C5 = 'BA', C10 = 'ZP', C15 = 'BB', C20 = 'YP', C25 = 'BC',
C30 = 'XP', C35 = 'BD', C40 = 'UP', C45 = 'BE', C50 = 'VP',
C55 = 'BF', C60 = 'WP', C65 = 'BG', C70 = 'LP', C75 = 'BH',
C80 = 'MP', C85 = 'BI', C90 = 'NP', C95 = 'BJ', C100 = 'OP';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    #  PASS:0247 If 1 row is updated ?
    
    stmt = """SELECT C5, C20, C35, C40, C55, C60, C75, C80, C90, C95, C100
FROM T100 
WHERE C1 = 'ZA' AND C2 = 'ZB';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a247exp""", 'a247s0')
    
    stmt = """DELETE FROM T100;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test116(desc="""a254"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM PROJ;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO PROJ VALUES  ('P1','MXSS','Design',10000,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P2','CALM','Code',30000,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P3','SDP','Test',30000,'Tampa');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P4','SDP','Design',20000,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P5','IRM','Test',10000,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P6','PAYR','Design',50000,'Deale');"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0254 Column name in SET clause!
    
    stmt = """DELETE FROM PROJ1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 0)
    # Making sure the table is empty
    
    # setup
    stmt = """INSERT INTO PROJ1 
SELECT *
FROM PROJ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 6)
    # PASS:0254 If 6 rows are inserted?
    
    stmt = """UPDATE PROJ1 
SET CITY = PTYPE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 6)
    #  PASS:0254 If 6 rows are updated?
    
    stmt = """SELECT CITY
FROM PROJ1 
WHERE PNUM = 'P1';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a254exp""", 'a254s0')
    
    stmt = """DELETE FROM PROJ;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test117(desc="""a257"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM VTABLE;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO VTABLE VALUES(10,+20,30,40,10.50);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO VTABLE VALUES(0,1,2,3,4.25);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO VTABLE VALUES(100,200,300,400,500.01);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO VTABLE VALUES(1000,-2000,3000,NULL,4000.00);"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0257 SELECT MAX, MIN (COL1 + or - COL2)!
    
    # setup
    stmt = """INSERT INTO VTABLE 
VALUES(10,11,12,13,15);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    # PASS:0257 If 1 row is inserted?
    
    # setup
    stmt = """INSERT INTO VTABLE 
VALUES(100,111,1112,113,115);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #  PASS:0257 If 1 row is inserted?
    
    stmt = """SELECT COL1, MAX(COL2 + COL3), MIN(COL3 - COL2)
FROM VTABLE 
GROUP BY COL1
ORDER BY COL1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a257exp""", 'a257s0')
    
    stmt = """DELETE from VTABLE;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test118(desc="""a258"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM VTABLE;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO VTABLE VALUES(10,+20,30,40,10.50);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO VTABLE VALUES(0,1,2,3,4.25);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO VTABLE VALUES(100,200,300,400,500.01);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO VTABLE VALUES(1000,-2000,3000,NULL,4000.00);"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0258 SELECT SUM(2*COL1*COL2) in HAVING SUM(COL2*COL3)!
    
    # setup
    stmt = """INSERT INTO VTABLE 
VALUES (10,11,12,13,15);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    # PASS:0258 if 1 row is inserted?
    
    # setup
    stmt = """INSERT INTO VTABLE 
VALUES (100,111,1112,113,115);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #  PASS:0258 if 1 row is inserted ?
    
    stmt = """SELECT COL1,SUM(2 * COL2 * COL3)
FROM VTABLE 
GROUP BY COL1
HAVING SUM(COL2 * COL3) > 2000
OR SUM(COL2 * COL3) < -2000
ORDER BY COL1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a258exp""", 'a258s0')
    
    stmt = """DELETE FROM VTABLE;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test119(desc="""a259"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM VTABLE;"""
    output = _dci.cmdexec(stmt)
    stmt = """DELETE FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO VTABLE VALUES(10,+20,30,40,10.50);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO VTABLE VALUES(0,1,2,3,4.25);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO VTABLE VALUES(100,200,300,400,500.01);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO VTABLE VALUES(1000,-2000,3000,NULL,4000.00);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO STAFF VALUES ('E1','Alice',12,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E2','Betty',10,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E3','Carmen',13,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E4','Don',12,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E5','Ed',13,'Akron');"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO WORKS VALUES  ('E1','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P3',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P4',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P5',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P6',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P2',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E3','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P4',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P5',80);"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0259 SOME, ANY in HAVING clause!
    
    # setup
    stmt = """INSERT INTO VTABLE 
VALUES(10,11,12,13,15);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    # PASS:0259 If 1 row is inserted?
    
    # setup
    stmt = """INSERT INTO VTABLE 
VALUES(100,111,1112,113,115);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #  PASS:0259 If 1 row is inserted?
    
    stmt = """SELECT COL1, MAX(COL2)
FROM VTABLE 
GROUP BY COL1
HAVING MAX(COL2) > ANY (SELECT GRADE FROM STAFF)
AND MAX(COL2) < SOME (SELECT HOURS FROM WORKS)
ORDER BY COL1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a259exp""", 'a259s0')
    
    stmt = """DELETE FROM VTABLE;"""
    output = _dci.cmdexec(stmt)
    stmt = """DELETE FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test120(desc="""a261"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM VTABLE;"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO VTABLE VALUES(10,+20,30,40,10.50);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO VTABLE VALUES(0,1,2,3,4.25);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO VTABLE VALUES(100,200,300,400,500.01);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO VTABLE VALUES(1000,-2000,3000,NULL,4000.00);"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0261 WHERE (2 * (c1 - c2)) BETWEEN!
    
    stmt = """SELECT COL1, COL2
FROM VTABLE 
WHERE(2*(COL3 - COL2)) BETWEEN 5 AND 200
ORDER BY COL1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a261exp""", 'a261s0')
    
    stmt = """DELETE FROM VTABLE;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test121(desc="""a262"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    stmt = """DELETE FROM VTABLE;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO WORKS VALUES  ('E1','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P3',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P4',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P5',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P6',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P2',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E3','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P4',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P5',80);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO VTABLE VALUES(10,+20,30,40,10.50);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO VTABLE VALUES(0,1,2,3,4.25);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO VTABLE VALUES(100,200,300,400,500.01);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO VTABLE VALUES(1000,-2000,3000,NULL,4000.00);"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0262 WHERE clause with computation, ANY/ALL subqueries!
    
    stmt = """UPDATE VTABLE 
SET COL1 = 1
WHERE COL1 = 0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    #  PASS:0262 If 1 row is updated?
    
    stmt = """SELECT COL1, COL2
FROM VTABLE 
WHERE (COL3 * COL2/COL1) > ALL
(SELECT HOURS FROM WORKS)
OR -(COL3 * COL2/COL1) > ANY
(SELECT HOURS FROM WORKS)
ORDER BY COL1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a262exp""", 'a262s0')
    
    stmt = """DELETE FROM VTABLE;"""
    output = _dci.cmdexec(stmt)
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test122(desc="""a263"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM VTABLE;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO VTABLE VALUES(10,+20,30,40,10.50);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO VTABLE VALUES(0,1,2,3,4.25);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO VTABLE VALUES(100,200,300,400,500.01);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO VTABLE VALUES(1000,-2000,3000,NULL,4000.00);"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0263 Computed column in ORDER BY!
    
    stmt = """SELECT COL1, (COL3 * COL2/COL1 - COL2 + 10)
FROM VTABLE 
WHERE COL1 > 0
ORDER BY 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a263exp""", 'a263s0')
    
    stmt = """DELETE FROM VTABLE;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test123(desc="""a264"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM VTABLE;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO VTABLE VALUES(10,+20,30,40,10.50);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO VTABLE VALUES(0,1,2,3,4.25);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO VTABLE VALUES(100,200,300,400,500.01);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO VTABLE VALUES(1000,-2000,3000,NULL,4000.00);"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0264 WHERE, HAVING without GROUP BY!
    
    stmt = """SELECT SUM(COL1)
FROM VTABLE 
WHERE 10 + COL1 > COL2
HAVING MAX(COL1) > 100;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a264exp""", 'a264s0')
    #  PASS:0264 If SUM(COL1) = 1000?
    
    stmt = """SELECT SUM(COL1)
FROM VTABLE 
WHERE 1000 + COL1 >= COL2
HAVING MAX(COL1) > 100;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a264exp""", 'a264s1')
    
    stmt = """DELETE FROM VTABLE;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test124(desc="""a269"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO WORKS VALUES  ('E1','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P3',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P4',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P5',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P6',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P2',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E3','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P4',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P5',80);"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0269 BETWEEN value expressions in wrong order!
    
    stmt = """SELECT COUNT(*)
FROM WORKS 
WHERE HOURS BETWEEN 80 AND 40;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a269exp""", 'a269s0')
    # PASS:0269 If count = 0   ?
    
    # setup
    stmt = """INSERT INTO WORKS 
VALUES('E6','P6',-60);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """SELECT COUNT(*)
FROM WORKS 
WHERE HOURS BETWEEN -40 AND -80;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a269exp""", 'a269s1')
    #  PASS:0269 If count = 0?
    
    stmt = """SELECT COUNT(*)
FROM WORKS 
WHERE HOURS BETWEEN -80 AND -40;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a269exp""", 'a269s2')
    
    stmt = """DELETE FROM VTABLE;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test125(desc="""a270"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P3',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P4',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P5',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P6',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P2',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E3','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P4',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P5',80);"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0270 BETWEEN approximate and exact numeric values!
    
    stmt = """SELECT COUNT(*)
FROM WORKS 
WHERE HOURS BETWEEN 11.999 AND 12 OR
HOURS BETWEEN 19.999 AND 2.001E1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a270exp""", 'a270s0')
    
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test126(desc="""a271"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO STAFF VALUES ('E1','Alice',12,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E2','Betty',10,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E3','Carmen',13,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E4','Don',12,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E5','Ed',13,'Akron');"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO WORKS VALUES  ('E1','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P3',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P4',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P5',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P6',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P2',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E3','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P4',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P5',80);"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0271 COUNT(*) with Cartesian product subset !
    
    stmt = """SELECT COUNT(*)
FROM WORKS, STAFF 
WHERE WORKS.EMPNUM = 'E1';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a271exp""", 'a271s0')
    
    stmt = """DELETE FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test127(desc="""a323"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    # setup
    stmt = """DELETE  FROM WORKS3;"""
    output = _dci.cmdexec(stmt)
    stmt = """DELETE  FROM STAFF3;"""
    output = _dci.cmdexec(stmt)
    stmt = """DELETE  FROM PROJ3;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO PROJ3 
VALUES ('P1','MASS','Design',10000,'Deale');"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO STAFF3 
SELECT * FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO WORKS3 
VALUES ('E1','P1',40);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO WORKS3 
VALUES ('E2','P1',40);"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0323 (2 pr.,1 son),both P.K e, F.K e,insert another F.K!
    
    stmt = """SELECT COUNT(*) FROM WORKS3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a323exp""", 'a323s0')
    
    stmt = """DELETE  FROM WORKS3;"""
    output = _dci.cmdexec(stmt)
    stmt = """DELETE  FROM STAFF3;"""
    output = _dci.cmdexec(stmt)
    stmt = """DELETE  FROM PROJ3;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test128(desc="""a326"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO STAFF VALUES ('E1','Alice',12,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E2','Betty',10,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E3','Carmen',13,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E4','Don',12,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E5','Ed',13,'Akron');"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0326 (2 pr.,1 son),P.K e, no F.K, modify P.K!
    
    # setup
    stmt = """DELETE  FROM WORKS3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 0)
    
    stmt = """DELETE  FROM STAFF3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 0)
    
    stmt = """INSERT INTO STAFF3 
SELECT * FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 5)
    
    stmt = """SELECT EMPNUM FROM STAFF3 
WHERE EMPNUM = 'E1';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a326exp""", 'a326s0')
    # PASS:0326 If 1 row selected and EMPNUM = E1?
    
    stmt = """UPDATE STAFF3 
SET EMPNUM = 'E9'
WHERE EMPNUM = 'E1';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """SELECT EMPNUM FROM STAFF3 
WHERE EMPNUM = 'E1';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """DELETE FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test129(desc="""a331"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    stmt = """DELETE FROM STAFF3;"""
    output = _dci.cmdexec(stmt)
    stmt = """DELETE FROM PROJ;"""
    output = _dci.cmdexec(stmt)
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO STAFF VALUES ('E1','Alice',12,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E2','Betty',10,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E3','Carmen',13,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E4','Don',12,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E5','Ed',13,'Akron');"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO STAFF3 
SELECT *
FROM   STAFF;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO PROJ VALUES  ('P1','MXSS','Design',10000,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P2','CALM','Code',30000,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P3','SDP','Test',30000,'Tampa');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P4','SDP','Design',20000,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P5','IRM','Test',10000,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P6','PAYR','Design',50000,'Deale');"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO WORKS VALUES  ('E1','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P3',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P4',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P5',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P6',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P2',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E3','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P4',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P5',80);"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0331 (2 pr.,1 son),modify F.K to P.K corr. value!
    
    # setup
    stmt = """DELETE  FROM WORKS3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 0)
    
    stmt = """DELETE  FROM STAFF3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 5)
    
    stmt = """DELETE  FROM PROJ3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 0)
    
    stmt = """INSERT INTO STAFF3 
SELECT * FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 5)
    
    stmt = """INSERT INTO PROJ3 
SELECT * FROM PROJ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 6)
    
    stmt = """INSERT INTO WORKS3 
SELECT * FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 12)
    
    stmt = """SELECT COUNT(*) FROM WORKS 
WHERE EMPNUM = 'E1';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a331exp""", 'a331s0')
    # PASS:0331 If count = 6?
    
    stmt = """UPDATE WORKS3 
SET EMPNUM = 'E2'
WHERE EMPNUM = 'E1';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 6)
    
    stmt = """SELECT COUNT(*) FROM WORKS3 
WHERE EMPNUM = 'E1';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a331exp""", 'a331s1')
    
    stmt = """DELETE FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    stmt = """DELETE FROM STAFF3;"""
    output = _dci.cmdexec(stmt)
    stmt = """DELETE FROM PROJ;"""
    output = _dci.cmdexec(stmt)
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test130(desc="""a393"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    stmt = """DELETE FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO WORKS VALUES  ('E1','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P3',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P4',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P5',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P6',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P2',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E3','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P4',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P5',80);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO STAFF VALUES ('E1','Alice',12,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E2','Betty',10,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E3','Carmen',13,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E4','Don',12,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E5','Ed',13,'Akron');"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0393 SUM, MAX on Cartesian product!
    
    stmt = """SELECT SUM(HOURS), MAX(HOURS)
FROM  STAFF, WORKS;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a393exp""", 'a393s0')
    
    stmt = """DELETE FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test131(desc="""a394"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P3',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P4',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P5',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P6',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P2',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E3','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P4',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P5',80);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """DELETE FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E1','Alice',12,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E2','Betty',10,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E3','Carmen',13,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E4','Don',12,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E5','Ed',13,'Akron');"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0394 AVG, MIN on joined table with WHERE without GROUP!
    
    stmt = """SELECT AVG(HOURS), MIN(HOURS)
FROM  STAFF, WORKS 
WHERE STAFF.EMPNUM = 'E2'
AND STAFF.EMPNUM = WORKS.EMPNUM;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a394exp""", 'a394s0')
    
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    stmt = """DELETE FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test132(desc="""a395"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    stmt = """DELETE FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO WORKS VALUES  ('E1','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P3',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P4',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P5',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P6',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P2',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E3','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P4',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P5',80);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO STAFF VALUES ('E1','Alice',12,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E2','Betty',10,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E3','Carmen',13,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E4','Don',12,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E5','Ed',13,'Akron');"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0395 SUM, MIN on joined table with GROUP without WHERE!
    
    stmt = """SELECT STAFF.EMPNUM, SUM(HOURS), MIN(HOURS)
FROM  STAFF, WORKS 
GROUP BY STAFF.EMPNUM
ORDER BY 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a395exp""", 'a395s0')
    
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    stmt = """DELETE FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test133(desc="""a396"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E1','Alice',12,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E2','Betty',10,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E3','Carmen',13,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E4','Don',12,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E5','Ed',13,'Akron');"""
    output = _dci.cmdexec(stmt)
    
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P3',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P4',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P5',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P6',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P2',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E3','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P4',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P5',80);"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0396 SUM, MIN on joined table with WHERE, GROUP BY, HAVING!
    
    stmt = """SELECT STAFF.EMPNUM, AVG(HOURS), MIN(HOURS)
FROM  STAFF, WORKS 
WHERE STAFF.EMPNUM IN ('E1','E4','E3') AND
 STAFF.EMPNUM = WORKS.EMPNUM
GROUP BY STAFF.EMPNUM
HAVING COUNT(*) > 1
ORDER BY STAFF.EMPNUM;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a396exp""", 'a396s0')
    
    stmt = """DELETE FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test134(desc="""a397"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    stmt = """DELETE FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO WORKS VALUES  ('E1','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P3',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P4',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P5',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P6',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P2',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E3','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P4',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P5',80);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO STAFF VALUES ('E1','Alice',12,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E2','Betty',10,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E3','Carmen',13,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E4','Don',12,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E5','Ed',13,'Akron');"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0397 Grouped view!
    
    stmt = """SELECT EMP1, EMPXAVG, EMPXMAX
FROM SETXTEST 
ORDER BY EMP1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a397exp""", 'a397s0')
    
    stmt = """DELETE FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test135(desc="""a409"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    stmt = """DELETE FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO WORKS VALUES  ('E1','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P3',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P4',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P5',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P6',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P2',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E3','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P4',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P5',80);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO STAFF VALUES ('E1','Alice',12,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E2','Betty',10,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E3','Carmen',13,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E4','Don',12,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E5','Ed',13,'Akron');"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0409 Effective outer join -- with 2 cursors!
    
    # setup
    stmt = """INSERT INTO STAFF 
VALUES('E6','Lendle',17,'Potomac');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """SELECT PNUM, WORKS.EMPNUM, EMPNAME, HOURS
FROM WORKS, STAFF 
WHERE STAFF.EMPNUM = WORKS.EMPNUM
ORDER BY 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a409exp""", 'a409s0')
    
    #  PASS:0409 If twelve rows are selected with ROW #9 as follows?
    #  PASS:0409 PNUM   WORKS.EMPNUM   EMPNAME    HOURS?
    #  PASS:0409  P2         E3         Carmen     20?
    
    stmt = """SELECT 'ZZ', EMPNUM, EMPNAME, -99
FROM STAFF 
WHERE NOT EXISTS (SELECT * FROM WORKS 
WHERE WORKS.EMPNUM = STAFF.EMPNUM)
ORDER BY EMPNUM;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a409exp""", 'a409s1')
    
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    stmt = """DELETE FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test136(desc="""a411"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO WORKS VALUES  ('E1','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P3',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P4',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P5',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P6',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P2',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E3','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P4',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P5',80);"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0411 Effective set difference!
    
    stmt = """SELECT W1.EMPNUM FROM WORKS W1
WHERE W1.PNUM = 'P2'
AND NOT EXISTS (SELECT * FROM WORKS W2
WHERE W2.EMPNUM = W1.EMPNUM
AND W2.PNUM = 'P1')
ORDER BY 1 ASC;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a411exp""", 'a411s0')
    
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test137(desc="""a412"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO WORKS VALUES  ('E1','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P3',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P4',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P5',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P6',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P2',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E3','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P4',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P5',80);"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0412 Effective set intersection!
    
    stmt = """SELECT W1.EMPNUM FROM WORKS W1
WHERE W1.PNUM = 'P2'
AND EXISTS (SELECT * FROM WORKS W2
WHERE W1.EMPNUM = W2.EMPNUM
AND W2.PNUM = 'P1')
ORDER BY EMPNUM ASC;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a412exp""", 'a412s0')
    
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test138(desc="""a417"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM STAFF1;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """DELETE FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E1','Alice',12,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E2','Betty',10,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E3','Carmen',13,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E4','Don',12,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E5','Ed',13,'Akron');"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0417 Cartesian product GROUP BY 2 columns with NULLs!
    
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
GROUP BY STAFF1.CITY, STAFF.CITY;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a417exp""", 'a417s0')
    
    stmt = """DELETE FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    stmt = """DELETE FROM STAFF1;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test139(desc="""a420"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO WORKS VALUES  ('E1','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P3',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P4',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P5',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P6',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P2',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E3','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P4',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P5',80);"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0420 View with multiple SELECT of same column!
    
    stmt = """SELECT EMP1, HOURS, HOURSX2
FROM DUPXCOL 
WHERE EMP1 = 'E3';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a420exp""", 'a420s0')
    
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test140(desc="""a431"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    stmt = """DELETE FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO WORKS VALUES  ('E1','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P3',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P4',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P5',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P6',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P2',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E3','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P4',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P5',80);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO STAFF VALUES ('E1','Alice',12,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E2','Betty',10,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E3','Carmen',13,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E4','Don',12,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E5','Ed',13,'Akron');"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0431 Redundant rows in IN subquery!
    
    stmt = """SELECT COUNT (*) FROM STAFF 
WHERE EMPNUM IN
(SELECT EMPNUM FROM WORKS);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a431exp""", 'a431s0')
    # PASS:0431 If count = 4?
    
    stmt = """INSERT INTO STAFF1 
SELECT * FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 5)
    
    stmt = """SELECT COUNT (*) FROM STAFF1 
WHERE EMPNUM IN
(SELECT EMPNUM FROM WORKS);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a431exp""", 'a431s1')
    
    stmt = """DELETE FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test141(desc="""a432"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    stmt = """DELETE FROM PROJ;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO STAFF VALUES ('E1','Alice',12,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E2','Betty',10,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E3','Carmen',13,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E4','Don',12,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E5','Ed',13,'Akron');"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO PROJ VALUES  ('P1','MXSS','Design',10000,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P2','CALM','Code',30000,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P3','SDP','Test',30000,'Tampa');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P4','SDP','Design',20000,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P5','IRM','Test',10000,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P6','PAYR','Design',50000,'Deale');"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0432 Unknown comparison predicate in ALL, SOME, ANY!
    
    # setup
    
    stmt = """UPDATE PROJ SET CITY = NULL
WHERE PNUM = 'P3';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """SELECT COUNT(*)
FROM STAFF 
WHERE CITY = ALL (SELECT CITY
FROM PROJ 
WHERE PNAME = 'SDP');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a432exp""", 'a432s0')
    #  PASS:0432 If count = 0?
    
    stmt = """SELECT COUNT(*)
FROM STAFF 
WHERE CITY <> ALL (SELECT CITY
FROM PROJ 
WHERE PNAME = 'SDP');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a432exp""", 'a432s1')
    #  PASS:0432 If count = 0?
    
    stmt = """SELECT COUNT(*)
FROM STAFF 
WHERE CITY = ANY (SELECT CITY
FROM PROJ 
WHERE PNAME = 'SDP');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a432exp""", 'a432s2')
    #  PASS:0432 If count = 2?
    
    stmt = """SELECT COUNT(*)
FROM STAFF 
WHERE CITY <> ANY (SELECT CITY
FROM PROJ 
WHERE PNAME = 'SDP');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a432exp""", 'a432s3')
    #  PASS:0432 If count = 3?
    
    stmt = """SELECT COUNT(*)
FROM STAFF 
WHERE CITY = SOME (SELECT CITY
FROM PROJ 
WHERE PNAME = 'SDP');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a432exp""", 'a432s4')
    #  PASS:0432 If count = 2?
    
    stmt = """SELECT COUNT(*)
FROM STAFF 
WHERE CITY <> SOME (SELECT CITY
FROM PROJ 
WHERE PNAME = 'SDP');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a432exp""", 'a432s5')
    
    stmt = """DELETE FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    stmt = """DELETE FROM PROJ;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test142(desc="""a433"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    stmt = """DELETE FROM PROJ;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO WORKS VALUES  ('E1','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P3',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P4',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P5',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P6',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P2',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E3','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P4',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P5',80);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO PROJ VALUES  ('P1','MXSS','Design',10000,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P2','CALM','Code',30000,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P3','SDP','Test',30000,'Tampa');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P4','SDP','Design',20000,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P5','IRM','Test',10000,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P6','PAYR','Design',50000,'Deale');"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0433 Empty subquery in ALL, SOME, ANY!
    
    stmt = """SELECT COUNT(*) FROM PROJ 
WHERE PNUM = ALL (SELECT PNUM
FROM WORKS WHERE EMPNUM = 'E8');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a433exp""", 'a433s0')
    #  PASS:0433 If count = 6?
    
    stmt = """SELECT COUNT(*) FROM PROJ 
WHERE PNUM <> ALL (SELECT PNUM
FROM WORKS WHERE EMPNUM = 'E8');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a433exp""", 'a433s1')
    #  PASS:0433 If count = 6?
    
    stmt = """SELECT COUNT(*) FROM PROJ 
WHERE PNUM = ANY (SELECT PNUM
FROM WORKS WHERE EMPNUM = 'E8');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a433exp""", 'a433s2')
    #  PASS:0433 If count = 0?
    
    stmt = """SELECT COUNT(*) FROM PROJ 
WHERE PNUM <> ANY (SELECT PNUM
FROM WORKS WHERE EMPNUM = 'E8');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a433exp""", 'a433s3')
    #  PASS:0433 If count = 0?
    
    stmt = """SELECT COUNT(*) FROM PROJ 
WHERE PNUM = SOME (SELECT PNUM
FROM WORKS WHERE EMPNUM = 'E8');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a433exp""", 'a433s4')
    #  PASS:0433 If count = 0?
    
    stmt = """SELECT COUNT(*) FROM PROJ 
WHERE PNUM <> SOME (SELECT PNUM
FROM WORKS WHERE EMPNUM = 'E8');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a433exp""", 'a433s5')
    
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    stmt = """DELETE FROM PROJ;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test143(desc="""a434"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    stmt = """DELETE FROM PROJ;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO WORKS VALUES  ('E1','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P3',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P4',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P5',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P6',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P2',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E3','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P4',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P5',80);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO PROJ VALUES  ('P1','MXSS','Design',10000,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P2','CALM','Code',30000,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P3','SDP','Test',30000,'Tampa');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P4','SDP','Design',20000,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P5','IRM','Test',10000,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P6','PAYR','Design',50000,'Deale');"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0434 GROUP BY with HAVING EXISTS-correlated set function!
    
    stmt = """SELECT PNUM, SUM(HOURS) FROM WORKS 
GROUP BY PNUM
HAVING EXISTS (SELECT PNAME FROM PROJ 
WHERE PROJ.PNUM = WORKS.PNUM AND
SUM(WORKS.HOURS) > PROJ.BUDGET / 200);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a434exp""", 'a434s0')
    
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    stmt = """DELETE FROM PROJ;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test144(desc="""a435"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM BB;"""
    output = _dci.cmdexec(stmt)
    stmt = """DELETE FROM EE;"""
    output = _dci.cmdexec(stmt)
    stmt = """DELETE FROM GG;"""
    output = _dci.cmdexec(stmt)
    stmt = """DELETE FROM HH;"""
    output = _dci.cmdexec(stmt)
    stmt = """DELETE FROM II;"""
    output = _dci.cmdexec(stmt)
    stmt = """DELETE FROM JJ;"""
    output = _dci.cmdexec(stmt)
    stmt = """DELETE FROM MM;"""
    output = _dci.cmdexec(stmt)
    stmt = """DELETE FROM SS;"""
    output = _dci.cmdexec(stmt)
    
    # NO_TEST:0435 Host variables in UPDATE WHERE CURRENT!
    
    # Testing cursors <update statement:positioned>
    
    # TEST:0436 NULL values for various SQL data types!
    
    stmt = """INSERT INTO BB VALUES(NULL);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO EE VALUES(NULL);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO GG VALUES(NULL);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO HH VALUES(NULL);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO II VALUES(NULL);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO JJ VALUES(NULL);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO MM VALUES(NULL);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO SS VALUES(NULL);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """SELECT CHARTEST
FROM BB;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a435exp""", 'a435s0')
    #  PASS:0436 If CHARTEST is NULL (Implementor defined print format)?
    
    stmt = """SELECT INTTEST
FROM EE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a435exp""", 'a435s1')
    #  PASS:0436 If INTTEST is NULL (Implementor defined print format)?
    
    stmt = """SELECT REALTEST
FROM GG;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a435exp""", 'a435s2')
    #  PASS:0436 If REALTEST is NULL (Implementor defined print format)?
    
    stmt = """SELECT COUNT(*)
FROM GG 
WHERE REALTEST IS NULL;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a435exp""", 'a435s3')
    #  PASS:0436 If count = 1?
    
    stmt = """SELECT SMALLTEST
FROM HH;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a435exp""", 'a435s4')
    #  PASS:0436 If SMALLTEST is NULL (Implementor defined print format)?
    
    stmt = """SELECT DOUBLETEST
FROM II;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a435exp""", 'a435s5')
    #  PASS:0436 If DOUBLETEST is NULL (Implementor defined print format)?
    
    stmt = """SELECT COUNT(*)
FROM II 
WHERE DOUBLETEST IS NULL;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a435exp""", 'a435s6')
    #  PASS:0436 If count = 1?
    
    stmt = """SELECT FLOATTEST
FROM JJ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a435exp""", 'a435s7')
    #  PASS:0436 If FLOATTEST is NULL (Implementor defined print format)?
    
    stmt = """SELECT COUNT(*)
FROM JJ 
WHERE FLOATTEST IS NULL;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a435exp""", 'a435s8')
    #  PASS:0436 If count = 1?
    
    stmt = """SELECT NUMTEST
FROM MM;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a435exp""", 'a435s9')
    #  PASS:0436 If NUMTEST is NULL (Implementor defined print format)?
    
    stmt = """SELECT NUMTEST
FROM SS;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a435exp""", 'a435s10')
    
    stmt = """DELETE FROM BB;"""
    output = _dci.cmdexec(stmt)
    stmt = """DELETE FROM EE;"""
    output = _dci.cmdexec(stmt)
    stmt = """DELETE FROM GG;"""
    output = _dci.cmdexec(stmt)
    stmt = """DELETE FROM HH;"""
    output = _dci.cmdexec(stmt)
    stmt = """DELETE FROM II;"""
    output = _dci.cmdexec(stmt)
    stmt = """DELETE FROM JJ;"""
    output = _dci.cmdexec(stmt)
    stmt = """DELETE FROM MM;"""
    output = _dci.cmdexec(stmt)
    stmt = """DELETE FROM SS;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test145(desc="""a442"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM PROJ;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO PROJ VALUES  ('P1','MXSS','Design',10000,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P2','CALM','Code',30000,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P3','SDP','Test',30000,'Tampa');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P4','SDP','Design',20000,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P5','IRM','Test',10000,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P6','PAYR','Design',50000,'Deale');"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0442 DISTINCT with GROUP BY, HAVING!
    
    stmt = """SELECT PTYPE, CITY FROM PROJ 
GROUP BY PTYPE, CITY
HAVING AVG(BUDGET) > 21000;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a442exp""", 'a442s0')
    #  PASS:0442 If 3 rows selected with PTYPE/CITY values(in any order):?
    #  PASS:0442 Code/Vienna, Design/Deale, Test/Tampa?
    
    stmt = """SELECT DISTINCT PTYPE, CITY FROM PROJ 
GROUP BY PTYPE, CITY
HAVING AVG(BUDGET) > 21000;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a442exp""", 'a442s1')
    #  PASS:0442 If 3 rows selected with PTYPE/CITY values(in any order):?
    #  PASS:0442 Code/Vienna, Design/Deale, Test/Tampa?
    
    stmt = """SELECT DISTINCT SUM(BUDGET) FROM PROJ 
GROUP BY PTYPE, CITY
HAVING AVG(BUDGET) > 21000;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a442exp""", 'a442s2')
    
    stmt = """DELETE FROM PROJ;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test146(desc="""a452"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO STAFF VALUES ('E1','Alice',12,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E2','Betty',10,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E3','Carmen',13,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E4','Don',12,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E5','Ed',13,'Akron');"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0452 Order of precedence, left-to-right in UNION [ALL]!
    
    stmt = """SELECT EMPNAME FROM STAFF 
UNION
SELECT EMPNAME FROM STAFF 
UNION ALL
SELECT EMPNAME FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a452exp""", 'a452s0')
    #  PASS:0452 If 10 rows selected?
    
    stmt = """SELECT EMPNAME FROM STAFF 
UNION ALL
SELECT EMPNAME FROM STAFF 
UNION
SELECT EMPNAME FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a452exp""", 'a452s1')
    
    stmt = """DELETE FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test147(desc="""a453"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    stmt = """DELETE FROM PROJ;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO STAFF VALUES ('E1','Alice',12,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E2','Betty',10,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E3','Carmen',13,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E4','Don',12,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E5','Ed',13,'Akron');"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO PROJ VALUES  ('P1','MXSS','Design',10000,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P2','CALM','Code',30000,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P3','SDP','Test',30000,'Tampa');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P4','SDP','Design',20000,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P5','IRM','Test',10000,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P6','PAYR','Design',50000,'Deale');"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0453 NULL with empty subquery of ALL, SOME, ANY!
    
    stmt = """UPDATE PROJ 
SET CITY = NULL WHERE PNAME = 'IRM';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """SELECT COUNT(*)
FROM PROJ 
WHERE CITY IS NULL;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a453exp""", 'a453s0')
    #  PASS:0453 If count = 1?
    
    stmt = """SELECT COUNT(*)
FROM PROJ 
WHERE CITY = ALL (SELECT CITY
FROM STAFF 
WHERE EMPNUM = 'E8');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a453exp""", 'a453s1')
    #  PASS:0453 If count = 6?
    
    stmt = """SELECT COUNT(*)
FROM PROJ 
WHERE CITY <> ALL (SELECT CITY
FROM STAFF 
WHERE EMPNUM = 'E8');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a453exp""", 'a453s2')
    #  PASS:0453 If count = 6?
    
    stmt = """SELECT COUNT(*)
FROM PROJ 
WHERE CITY = ANY (SELECT CITY
FROM STAFF 
WHERE EMPNUM = 'E8');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a453exp""", 'a453s3')
    #  PASS:0453 If count = 0?
    
    stmt = """SELECT COUNT(*)
FROM PROJ 
WHERE CITY <> ANY (SELECT CITY
FROM STAFF 
WHERE EMPNUM = 'E8');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a453exp""", 'a453s4')
    #  PASS:0453 If count = 0?
    
    stmt = """SELECT COUNT(*)
FROM PROJ 
WHERE CITY = SOME (SELECT CITY
FROM STAFF 
WHERE EMPNUM = 'E8');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a453exp""", 'a453s5')
    #  PASS:0453 If count = 0?
    
    stmt = """SELECT COUNT(*)
FROM PROJ 
WHERE CITY <> SOME (SELECT CITY
FROM STAFF 
WHERE EMPNUM = 'E8');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a453exp""", 'a453s6')
    
    stmt = """DELETE FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    stmt = """DELETE FROM PROJ;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test148(desc="""a455"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    stmt = """DELETE FROM PROJ;"""
    output = _dci.cmdexec(stmt)
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO STAFF VALUES ('E1','Alice',12,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E2','Betty',10,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E3','Carmen',13,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E4','Don',12,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E5','Ed',13,'Akron');"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO PROJ VALUES  ('P1','MXSS','Design',10000,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P2','CALM','Code',30000,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P3','SDP','Test',30000,'Tampa');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P4','SDP','Design',20000,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P5','IRM','Test',10000,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P6','PAYR','Design',50000,'Deale');"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO WORKS VALUES  ('E1','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P3',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P4',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P5',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P6',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P2',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E3','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P4',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P5',80);"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0455 Relaxed union compatability rules for columns!
    
    #  NOTE:  OPTIONAL FIPS Flagger test
    #  FIPS Flagger Test.Support for this feature is not required.
    #  If supported, this feature must be flagged as an extension to the standard.
    
    stmt = """SELECT EMPNUM, CITY  FROM STAFF 
UNION
SELECT PTYPE, CITY  FROM PROJ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a455exp""", 'a455s0')
    
    #  PASS:0455 If 9 rows are selected?
    #  NOTE:0455 Shows support for UNION of CHAR columns
    #  NOTE:0455   with different lengths.
    
    stmt = """SELECT EMPNUM, CITY  FROM STAFF 
UNION
SELECT 'e1 ', CITY  FROM PROJ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a455exp""", 'a455s1')
    
    #  PASS:0455 If 8 rows selected?
    #  NOTE:0455 Shows support for UNION of Char column
    #  NOTE:0455   with CHAR literal.
    
    stmt = """SELECT EMPNUM, GRADE  FROM STAFF 
UNION
SELECT EMPNUM, HOURS  FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a455exp""", 'a455s2')
    
    stmt = """DELETE FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    stmt = """DELETE FROM PROJ;"""
    output = _dci.cmdexec(stmt)
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test149(desc="""a512"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    stmt = """DELETE FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    stmt = """DELETE FROM PROJ;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO WORKS VALUES  ('E1','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P3',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P4',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P5',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E1','P6',12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P1',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E2','P2',80);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E3','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P2',20);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P4',40);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO WORKS VALUES  ('E4','P5',80);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO STAFF VALUES ('E1','Alice',12,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E2','Betty',10,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E3','Carmen',13,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E4','Don',12,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO STAFF VALUES ('E5','Ed',13,'Akron');"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO PROJ VALUES  ('P1','MXSS','Design',10000,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P2','CALM','Code',30000,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P3','SDP','Test',30000,'Tampa');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P4','SDP','Design',20000,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P5','IRM','Test',10000,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P6','PAYR','Design',50000,'Deale');"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0512 <value expression> for IN predicate!
    
    stmt = """SELECT MIN(PNAME)
FROM PROJ, WORKS, STAFF 
WHERE PROJ.PNUM = WORKS.PNUM
AND WORKS.EMPNUM = STAFF.EMPNUM
AND BUDGET - GRADE * HOURS * 100 IN
(-4400, -1000, 4000);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a512exp""", 'a512s0')
    #  PASS:0512 If PNAME = 'CALM'?
    
    stmt = """SELECT CITY, COUNT(*)
FROM PROJ 
GROUP BY CITY
HAVING (MAX(BUDGET) - MIN(BUDGET)) / 2
IN (2, 20000, 10000)
ORDER BY CITY DESC;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a512exp""", 'a512s1')
    
    stmt = """DELETE FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    stmt = """DELETE FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    stmt = """DELETE FROM PROJ;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test150(desc="""a523"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM PROJ;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO PROJ VALUES  ('P1','MXSS','Design',10000,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P2','CALM','Code',30000,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P3','SDP','Test',30000,'Tampa');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P4','SDP','Design',20000,'Deale');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P5','IRM','Test',10000,'Vienna');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PROJ VALUES  ('P6','PAYR','Design',50000,'Deale');"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0523 <value expression> for BETWEEN predicate!
    
    stmt = """SELECT COUNT(*)
FROM PROJ 
WHERE 24 * 1000 BETWEEN BUDGET - 5000 AND 50000 / 1.7;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a523exp""", 'a523s0')
    #  PASS:0523 If count = 3?
    
    stmt = """SELECT PNAME
FROM PROJ 
WHERE 'Tampa' NOT BETWEEN CITY AND 'Vienna'
AND PNUM > 'P2';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a523exp""", 'a523s1')
    #  PASS:0523 If PNAME = 'IRM'?
    
    stmt = """SELECT CITY, COUNT(*)
FROM PROJ 
GROUP BY CITY
HAVING 50000 + 2 BETWEEN 33000 AND SUM(BUDGET) - 20;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a523exp""", 'a523s2')
    
    stmt = """DELETE FROM PROJ;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test151(desc="""a524"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DELETE FROM T100;"""
    output = _dci.cmdexec(stmt)
    
    # TEST:0524 FIPS sizing:  100 Items in a SELECT list!
    
    stmt = """delete from T100;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 0)
    
    stmt = """insert into T100 values ('00', '01', '02',
'03', '04', '05', '06', '07', '08', '09', '0a', '0b', '0c',
'0d', '0e', '0f', '10', '11', '12', '13', '14', '15', '16',
'17', '18', '19', '1a', '1b', '1c', '1d', '1e', '1f', '20',
'21', '22', '23', '24', '25', '26', '27', '28', '29', '2a',
'2b', '2c', '2d', '2e', '2f', '30', '31', '32', '33', '34',
'35', '36', '37', '38', '39', '3a', '3b', '3c', '3d', '3e',
'3f', '40', '41', '42', '43', '44', '45', '46', '47', '48',
'49', '4a', '4b', '4c', '4d', '4e', '4f', '50', '51', '52',
'53', '54', '55', '56', '57', '58', '59', '5a', '5b', '5c',
'5d', '5e', '5f', '60', '61', '62', '63');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #  PASS:0524 If 1 row is inserted?
    
    stmt = """SELECT
C1, C2, C3, C4, C5, C6, C7, C8, C9, C10, C11, C12, C13, C14,
C15, C16, C17, C18, C19, C20, C21, C22, C23, C24, C25, C26,
C27, C28, C29, C30, C31, C32, C33, C34, C35, C36, C37, C38,
C39, C40, C41, C42, C43, C44, C45, C46, C47, C48, C49, C50,
C51, C52, C53, C54, C55, C56, C57, C58, C59, C60, C61, C62,
C63, C64, C65, C66, C67, C68, C69, C70, C71, C72, C73, C74,
C75, C76, C77, C78, C79, C80, C81, C82, C83, C84, C85, C86,
C87, C88, C89, C90, C91, C92, C93, C94, C95, C96, C97, C98,
C99, C100
from T100;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a524exp""", 'a524s0')
    
    stmt = """DELETE FROM T100;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

