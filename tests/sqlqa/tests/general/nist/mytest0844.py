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

# TEST:0844 Outer join predicates !

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
    stmt = """CREATE TABLE SEVEN_TYPES (
T_INT     INTEGER,
T_CHAR    CHAR(10),
T_SMALL   SMALLINT,
T_DECIMAL DECIMAL(10,2),
T_REAL    REAL,
T_FLOAT   FLOAT,
T_DOUBLE  DOUBLE PRECISION) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    # stmt = """COMMIT WORK;"""
    # output = _dci.cmdexec(stmt)
    # _dci.expect_complete_msg(output)
    
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    
    # setup
    stmt = """DELETE FROM SEVEN_TYPES;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 0)
    stmt = """INSERT INTO SEVEN_TYPES VALUES (1, 'E1',-11,   2,  3,   4,   5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO SEVEN_TYPES VALUES (2, 'E2', -5,  13, 33,-444, -55);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO SEVEN_TYPES VALUES (3, 'E6', -3,-222,333,  44, 555);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO SEVEN_TYPES VALUES (12,'DUP', 0,   0, -1,   1,1E+1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO SEVEN_TYPES VALUES (12,'DUP', 0,   0, -1,   1,1E+1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # NOTE:0844 BETWEEN predicate
    stmt = """SELECT EMPNAME, CITY, T_DECIMAL
FROM STAFF LEFT OUTER JOIN SEVEN_TYPES
ON -GRADE / 11 BETWEEN T_REAL AND T_DECIMAL
ORDER BY EMPNAME;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0844.exp""", """test0844i""")
    
    # PASS:0844 If 6 rows selected with ordered rows and column values ?
    # PASS:0844    Alice  Deale  NULL  ?
    # PASS:0844    Betty  Vienna    0  ?
    # PASS:0844    Betty  Vienna    0  ?
    # PASS:0844    Carmen Vienna NULL  ?
    # PASS:0844    Don    Deale  NULL  ?
    # PASS:0844    Ed     Akron  NULL  ?
    
    # NOTE:0844 comparable CHAR types
    # NOTE:0844 IN predicate, with literals and variable value
    stmt = """SELECT T_INT, T_CHAR, EMPNAME, EMPNUM, GRADE
FROM SEVEN_TYPES RIGHT JOIN STAFF
ON GRADE IN (10, 11, 13) AND EMPNUM = T_CHAR
ORDER BY EMPNAME, T_INT;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0844.exp""", """test0844j""")
    
    # PASS:0844 If 5 rows selected with ordered rows and column values ?
    # PASS:0844    NULL NULL Alice  E1 12  ?
    # PASS:0844       2 E2   Betty  E2 10  ?
    # PASS:0844    NULL NULL Carmen E3 13  ?
    # PASS:0844    NULL NULL Don    E4 12  ?
    # PASS:0844    NULL NULL Ed     E5 13  ?
    
    # NOTE:0844 subquery with outer reference and correlation names
    stmt = """SELECT XX.PNUM, BUDGET, HOURS, EMPNUM
FROM PROJ XX LEFT JOIN WORKS YY
ON  XX.PNUM = YY.PNUM AND
HOURS * BUDGET / 160000 > (SELECT GRADE FROM STAFF
WHERE YY.EMPNUM = STAFF.EMPNUM)
ORDER BY PNUM;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0844.exp""", """test0844k""")
    
    # PASS:0844 If 6 rows selected with ordered rows and column values ?
    # PASS:0844    P1 10000 NULL NULL ?
    # PASS:0844    P2 30000   80 E2   ?
    # PASS:0844    P3 30000   80 E1   ?
    # PASS:0844    P4 20000 NULL NULL ?
    # PASS:0844    P5 10000 NULL NULL ?
    # PASS:0844    P6 50000 NULL NULL ?
    stmt = """SELECT STAFF.CITY,EMPNAME,PNAME,BUDGET
FROM STAFF LEFT JOIN PROJ
ON STAFF.CITY = PROJ.CITY
AND STAFF.CITY <> 'Vienna'
AND EMPNAME <> 'Don'
WHERE BUDGET > 15000 OR BUDGET IS NULL
ORDER BY STAFF.CITY, EMPNAME, BUDGET;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0844.exp""", """test0844l""")
    
    # PASS:0844 If 6 rows selected with ordered rows and column values ?
    # PASS:0844    Akron   Ed     NULL NULL   ?
    # PASS:0844    Deale   Alice  SDP  20000  ?
    # PASS:0844    Deale   Alice  PAYR 50000  ?
    # PASS:0844    Deale   Don    NULL NULL   ?
    # PASS:0844    Vienna  Betty  NULL NULL   ?
    # PASS:0844    Vienna  Carmen NULL NULL   ?
    
    # NOTE:0844 difference between WHERE and ON
    stmt = """SELECT STAFF.CITY,EMPNAME,PNAME,BUDGET
FROM STAFF LEFT JOIN PROJ
ON STAFF.CITY = PROJ.CITY
AND STAFF.CITY <> 'Vienna'
WHERE (BUDGET > 15000 OR BUDGET IS NULL)
AND EMPNAME <> 'Don'
ORDER BY STAFF.CITY, EMPNAME, BUDGET;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0844.exp""", """test0844m""")
    
    # PASS:0844 If 5 rows selected with ordered rows and column values ?
    # PASS:0844    Akron   Ed     NULL NULL   ?
    # PASS:0844    Deale   Alice  SDP  20000  ?
    # PASS:0844    Deale   Alice  PAYR 50000  ?
    # PASS:0844    Vienna  Betty  NULL NULL   ?
    # PASS:0844    Vienna  Carmen NULL NULL   ?
    
    # NOTE:0844 correlation name with self-JOIN
    stmt = """SELECT XX.T_INT, YY.T_INT
FROM SEVEN_TYPES XX RIGHT OUTER JOIN SEVEN_TYPES YY
ON XX.T_INT = YY.T_INT +1
ORDER BY YY.T_INT;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0844.exp""", """test0844n""")
    
    # PASS:0844 If 5 rows selected with ordered rows and column values ?
    # PASS:0844    2      1  ?
    # PASS:0844    3      2  ?
    # PASS:0844    NULL   3  ?
    # PASS:0844    NULL  12  ?
    # PASS:0844    NULL  12  ?
    
    # NOTE:0844 nested booleans
    # NOTE:0844 data types are merely comparable
    stmt = """SELECT GRADE, T_FLOAT, T_DOUBLE
FROM STAFF LEFT JOIN SEVEN_TYPES T7
ON GRADE * -40 > T7.T_FLOAT
OR (T_DOUBLE -542.5 < GRADE AND T_DOUBLE -541.5 > GRADE)
ORDER BY GRADE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0844.exp""", """test0844o""")
    
    # PASS:0844 If 5 rows selected with ordered rows and column values ?
    # PASS:0844    10 -444 (aproximately)  -55 (aproximately) ?
    # PASS:0844    12 NULL                 NULL                 ?
    # PASS:0844    12 NULL                 NULL                 ?
    # PASS:0844    13   44 (aproximately)  555 (aproximately) ?
    # PASS:0844    13   44 (aproximately)  555 (aproximately) ?
    stmt = """ROLLBACK WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    time.sleep(2)
    # stmt = """begin work;"""
    # output = _dci.cmdexec(stmt)
    # DROP TABLE SEVEN_TYPES CASCADE;	-- XXXXX
    stmt = """DROP TABLE SEVEN_TYPES;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # stmt = """COMMIT WORK;"""
    # output = _dci.cmdexec(stmt)
    # _dci.expect_complete_msg(output)
    
    # END TEST >>> 0844 <<< END TEST
    
