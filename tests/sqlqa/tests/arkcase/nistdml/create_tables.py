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
    
def test001(desc="""create tables"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    stmt = """CREATE TABLE STAFF 
(EMPNUM   CHAR(3) NOT NULL,
EMPNAME  CHAR(20),
GRADE    int,
CITY     CHAR(15),
PRIMARY KEY (EMPNUM)
) ;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE PROJ 
(PNUM     CHAR(3) NOT NULL,
PNAME    CHAR(20),
PTYPE    CHAR(6),
BUDGET   int,
CITY     CHAR(15),
PRIMARY KEY (PNUM)
) ;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE WORKS 
(EMPNUM   CHAR(3) NOT NULL,
PNUM     CHAR(3) NOT NULL,
HOURS    int,
primary key (EMPNUM,PNUM)
) ;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE STAFF1 (EMPNUM    CHAR(3) NOT NULL,
EMPNAME  CHAR(20),
GRADE int,
CITY   CHAR(15)) no partition;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE PROJ1 (
PNUM    CHAR(3) NOT NULL,
PNAME  CHAR(20),
PTYPE  CHAR(6),
BUDGET int,
CITY   CHAR(15),
PRIMARY KEY (PNUM)
) ;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE WORKS1 (
EMPNUM    CHAR(3) NOT NULL,
PNUM    CHAR(3) NOT NULL,
HOURS   int,
primary key (EMPNUM, PNUM)
) ;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE STAFF3 (EMPNUM    CHAR(3) NOT NULL,
EMPNAME  CHAR(20),
GRADE int,
CITY   CHAR(15)) no partition ;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE PROJ3 
(PNUM     CHAR(3) NOT NULL,
PNAME    CHAR(20),
PTYPE    CHAR(6),
BUDGET   int,
CITY     CHAR(15),
PRIMARY KEY (PNUM)
) no partition ;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE WORKS3 
(EMPNUM   CHAR(3) NOT NULL,
PNUM     CHAR(3) NOT NULL,
HOURS    int) no partition;"""
    output = _dci.cmdexec(stmt)
    #      FOREIGN KEY (EMPNUM) REFERENCES STAFF3(EMPNUM),          XXXXX
    #      FOREIGN KEY (PNUM) REFERENCES PROJ3(PNUM)) ;             XXXXX
    
    stmt = """CREATE TABLE STAFF4 (EMPNUM    CHAR(3) NOT NULL,
EMPNAME  CHAR(20),
GRADE int,
CITY   CHAR(15)) no partition ;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE LONGINT (LONGXINT float) no partition ;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE TEMPXS 
(EMPNUM  CHAR(3),
GRADE int,
CITY CHAR(15)) no partition;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE TMP 
(T1 CHAR (10),
T2 int,
T3 CHAR (10)) no partition;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE AA (CHARTEST     CHAR(20))  no partition;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE BB (CHARTEST     CHAR (1))  no partition;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE CC (CHARTEST     CHAR (20))  no partition;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE DD (CHARTEST     CHAR (1))  no partition;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE EE (INTTEST     INTEGER)  no partition;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE FF (INTTEST     INT)  no partition;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE GG (REALTEST     REAL)  no partition;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE HH (SMALLTEST  SMALLINT)  no partition;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE II (DOUBLETEST  DOUBLE PRECISION)  no partition;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE JJ (FLOATTEST  FLOAT)  no partition;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE KK (FLOATTEST  FLOAT(32))  no partition;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE LL (NUMTEST  NUMERIC(13,6))  no partition;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE MM (NUMTEST  float)  no partition;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE MM2 (NUMTEST float)  no partition;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE NN (NUMTEST  float)  no partition;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE OO (NUMTEST  float)  no partition;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE PP (NUMTEST  float)  no partition;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE QQ (NUMTEST  float)  no partition;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE RR (NUMTEST  float)  no partition;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE SS (NUMTEST  float)  no partition;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE P1 (NUMTEST  float)  no partition;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE P7 (NUMTEST  float)  no partition;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE P12 (NUMTEST  float)  no partition;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE P15 (NUMTEST  float)  no partition;"""
    output = _dci.cmdexec(stmt)
    
    #  NIST SQL Test Suite, V5.0, Schema Definition, schema.sql
    #  This file defines the base tables used in most of the tests.
    
    stmt = """CREATE TABLE VTABLE 
(COL1   INTEGER,
COL2   INTEGER,
COL3   INTEGER,
COL4   INTEGER,
COL5   DECIMAL(7,2))  no partition;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE UPUNIQ (
NUMKEY  int not null,
COL2    CHAR(2),
PRIMARY KEY (NUMKEY))  no partition;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE TEXT80  (TEXXT CHAR(80))  no partition;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE TEXT132  (TEXXT CHAR(132))  no partition;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE TEXT240  (TEXXT CHAR(240))  no partition;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE TEXT256  (TEXXT CHAR(256))  no partition;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE TEXT512  (TEXXT CHAR(512))  no partition;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE TEXT1024  (TEXXT CHAR(1024))  no partition;"""
    output = _dci.cmdexec(stmt)
    
    #  The following tables are used to test the limitations (12-14-88)
    
    stmt = """CREATE TABLE T240(STR240 CHAR(240))  no partition;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE DEC15(COL1 DECIMAL(15,7))  no partition;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE FLO15(COL1 FLOAT(15))  no partition;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE INT10(COL1 INTEGER, COL2 SMALLINT)  no partition;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE T100(C1 CHAR(2),C2 CHAR(2),C3 CHAR(2),C4 CHAR(2),
C5 CHAR(2),C6 CHAR(2),C7 CHAR(2),C8 CHAR(2),
C9 CHAR(2),C10 CHAR(2),C11 CHAR(2),C12 CHAR(2),
C13 CHAR(2),C14 CHAR(2),C15 CHAR(2),C16 CHAR(2),
C17 CHAR(2),C18 CHAR(2),C19 CHAR(2),C20 CHAR(2),
C21 CHAR(2),C22 CHAR(2),C23 CHAR(2),C24 CHAR(2),
C25 CHAR(2),C26 CHAR(2),C27 CHAR(2),C28 CHAR(2),
C29 CHAR(2),C30 CHAR(2),C31 CHAR(2),C32 CHAR(2),
C33 CHAR(2),C34 CHAR(2),C35 CHAR(2),C36 CHAR(2),
C37 CHAR(2),C38 CHAR(2),C39 CHAR(2),C40 CHAR(2),
C41 CHAR(2),C42 CHAR(2),C43 CHAR(2),C44 CHAR(2),
C45 CHAR(2),C46 CHAR(2),C47 CHAR(2),C48 CHAR(2),
C49 CHAR(2),C50 CHAR(2),C51 CHAR(2),C52 CHAR(2),
C53 CHAR(2),C54 CHAR(2),C55 CHAR(2),C56 CHAR(2),
C57 CHAR(2),C58 CHAR(2),C59 CHAR(2),C60 CHAR(2),
C61 CHAR(2),C62 CHAR(2),C63 CHAR(2),C64 CHAR(2),
C65 CHAR(2),C66 CHAR(2),C67 CHAR(2),C68 CHAR(2),
C69 CHAR(2),C70 CHAR(2),C71 CHAR(2),C72 CHAR(2),
C73 CHAR(2),C74 CHAR(2),C75 CHAR(2),C76 CHAR(2),
C77 CHAR(2),C78 CHAR(2),C79 CHAR(2),C80 CHAR(2),
C81 CHAR(2),C82 CHAR(2),C83 CHAR(2),C84 CHAR(2),
C85 CHAR(2),C86 CHAR(2),C87 CHAR(2),C88 CHAR(2),
C89 CHAR(2),C90 CHAR(2),C91 CHAR(2),C92 CHAR(2),
C93 CHAR(2),C94 CHAR(2),C95 CHAR(2),C96 CHAR(2),
C97 CHAR(2),C98 CHAR(2),C99 CHAR(2),C100 CHAR(2))  no partition;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE T2000(STR110 CHAR(110),STR120 CHAR(120),
STR130 CHAR(130),STR140 CHAR(140),
STR150 CHAR(150),STR160 CHAR(160),
STR170 CHAR(170),STR180 CHAR(180),
STR190 CHAR(190),STR200 CHAR(200),
STR210 CHAR(210),STR216 CHAR(216))  no partition;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE T8(COL1 CHAR(2) NOT NULL,COL2 CHAR(4) NOT NULL,
COL3 CHAR(6) NOT NULL,COL4 CHAR(8) NOT NULL,
COL5 CHAR(10) NOT NULL,COL6 CHAR(12) NOT NULL,
COL7 CHAR(14),COL8 CHAR(16),
primary key (COL1,COL2,COL3,COL4,COL5,COL6))  no partition;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE T118(STR118 CHAR(118) NOT NULL,
primary key (str118)) no partition;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE T4(STR110 CHAR(110) NOT NULL,
NUM6   float not null,
COL3   CHAR(10),COL4 CHAR(20),
primary key (STR110,NUM6)
) ;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE T12(COL1 CHAR(1), COL2 CHAR(2),
COL3 CHAR(4), COL4 CHAR(6),
COL5 CHAR(8), COL6 CHAR(10),
COL7 CHAR(20), COL8 CHAR(30),
COL9 CHAR(40), COL10 CHAR(50),
COL11 INTEGER, COL12 INTEGER)  no partition;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE NEXTKEY (KEYNUM INTEGER,
AUTHOR CHAR(1),
DOLLARS INTEGER)  no partition;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE SV (NUMTEST float)  no partition;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE JJX20 (FLOATTEST  FLOAT(20))  no partition;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE PPX15 (NUMTEST  float)  no partition;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE PPX7  (NUMTEST  float)  no partition;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE P15X15 (NUMTEST  float)  no partition;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE P15X7 (NUMTEST  float)  no partition;"""
    output = _dci.cmdexec(stmt)
    
    # CREATE TABLE TEMPXOBSERV                             XXXXX
    stmt = """CREATE TABLE TOSERV 
(YEARXOBSERV  float,
CITY         CHAR(10),
MAXXTEMP     float,
MINXTEMP     float)  no partition;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE TOKENS 
(PROGXNO INT, TOKENXNO INT)  no partition;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE ECCO (C1 CHAR(2)) no partition;"""
    output = _dci.cmdexec(stmt)
    
    #  ************* create view statements follow *************
    
    #    CREATE VIEW CELSIUSXOBSERV (CITY, YEARXOBSERV, MINXC, MAXXC)
    #       AS SELECT CITY, YEARXOBSERV, (MINXTEMP - 32) * 5 / 9,
    #                 (MAXXTEMP - 32) * 5 / 9
    #          FROM TEMPXOBSERV ;       XXXXX
    #          FROM TOSERV ;
    #
    #    CREATE VIEW MULTIXYEARXOBSERV (CITY, HIGH, LOW)
    #       AS SELECT CITY, AVG(MAXXTEMP), AVG(MINXTEMP)
    #             FROM TEMPXOBSERV      XXXXX
    #             FROM TOSERV
    #             GROUP BY CITY ;
    #
    #    CREATE VIEW EXTREMEXTEMPS (YEARXOBSERV, HIGH, LOW)
    #       AS SELECT YEARXOBSERV, MAX(MAXXTEMP), MIN(MINXTEMP)
    #             FROM TEMPXOBSERV      XXXXX
    #             FROM TOSERV
    #             GROUP BY YEARXOBSERV ;
    #
    stmt = """CREATE VIEW SETXTEST (EMP1, EMPXAVG, EMPXMAX) AS
SELECT STAFF.EMPNUM, AVG(HOURS), MAX(HOURS)
FROM STAFF, WORKS 
GROUP BY STAFF.EMPNUM ;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE VIEW DUPXCOL (EMP1, PNO, HOURS, HOURSX2) AS
SELECT EMPNUM, PNUM, HOURS, HOURS * 2
FROM WORKS ;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE VIEW STAFFV1 
AS SELECT * FROM STAFF 
WHERE  GRADE >= 12 ;"""
    output = _dci.cmdexec(stmt)
    
    #   CREATE VIEW STAFFV2
    #            AS SELECT * FROM STAFF
    #               WHERE  GRADE >= 12 ;
    # --            WITH CHECK OPTION ;            XXXXX
    #
    #   CREATE VIEW STAFFV2XVIEW
    #            AS SELECT *
    #               FROM   STAFFV2
    #               WHERE  CITY = 'Vienna' ;
    #
    #   CREATE VIEW DOMAINXVIEW
    #            AS SELECT *
    #               FROM   WORKS
    #               WHERE  EMPNUM = 'E1' AND HOURS = 80
    #                   OR EMPNUM = 'E2' AND HOURS = 40
    #                   OR EMPNUM = 'E4' AND HOURS = 20 ;
    # --               WITH CHECK OPTION ;         XXXXX
    #
    #   CREATE VIEW STAFF2
    #            AS SELECT *
    #               FROM   STAFF ;
    # --            WITH CHECK OPTION ;            XXXXX
    #
    #   CREATE VIEW STAFFXWORKSXDESIGN (NAME,COST,PROJECT)
    stmt = """CREATE VIEW STXWOXDE (NAME1,COST,PROJECT)
AS SELECT EMPNAME,HOURS*2*GRADE,PNAME
FROM   PROJ,STAFF,WORKS 
WHERE  STAFF.EMPNUM=WORKS.EMPNUM
AND WORKS.PNUM=PROJ.PNUM
AND PTYPE='Design' ;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE VIEW SUBSP (EMPNUM,PNUM,HOURS)
AS SELECT EMPNUM,PNUM,HOURS
FROM   WORKS 
WHERE  EMPNUM='E3' ;"""
    output = _dci.cmdexec(stmt)
    # -       WITH CHECK OPTION ;          XXXXX
    #
    stmt = """CREATE VIEW TEMPXSS(EMPNUM,GRADE,CITY)
AS SELECT EMPNUM,GRADE,CITY
FROM   STAFF 
WHERE  GRADE > 12 ;"""
    output = _dci.cmdexec(stmt)
    #          WITH CHECK OPTION ;          XXXXX
    #
    #   CREATE VIEW VXWORKS1
    #            AS SELECT * FROM WORKS
    #               WHERE HOURS > 15 ;
    # --            WITH CHECK OPTION ;            XXXXX
    #
    #   CREATE VIEW VXWORKS2
    #            AS SELECT * FROM VXWORKS1
    #               WHERE EMPNUM = 'E1'
    #                  OR EMPNUM = 'E6' ;
    #
    #   CREATE VIEW VXWORKS3
    #            AS SELECT * FROM VXWORKS2
    #               WHERE PNUM = 'P2'
    #                  OR PNUM = 'P7' ;
    # --            WITH CHECK OPTION ;            XXXXX
    #
    #   CREATE VIEW UPDATEXVIEW1
    #             AS SELECT ALL CITY
    #                      FROM PROJ ;
    #
    #   CREATE VIEW UPDATEXVIEW2
    #             AS SELECT HOURS, EMPNUM, PNUM
    #                      FROM WORKS
    #                      WHERE HOURS IN (10, 20, 40) ;
    #
    #   CREATE VIEW UPDATEXVIEW3
    #             AS SELECT *
    #                      FROM WORKS
    #                      WHERE PNUM BETWEEN 'P2' AND 'P4'
    #                      AND not EMPNUM BETWEEN 'E2' AND 'E3' ;
    #                      -- AND EMPNUM NOT BETWEEN 'E2' AND 'E3' ;  XXXXX
    #
    #   CREATE VIEW UPDATEXVIEW4
    #             AS SELECT PNUM, EMPNUM
    #                      FROM WORKS
    #                      WHERE PNUM LIKE 'X2%' ;
    #
    #   CREATE VIEW UPDATEXVIEW5
    #             AS SELECT *
    #                      FROM STAFF
    #                      WHERE EMPNAME IS NOT NULL AND CITY IS NULL ;
    #
    #   CREATE VIEW UPDATEXVIEW6
    #             AS SELECT EMPNAME, CITY, GRADE
    #                      FROM STAFF
    #                      WHERE EMPNAME >= 'Betty' AND EMPNUM < 'E35'
    #                        OR CITY <= 'Deale' AND GRADE > 12
    #                        OR GRADE = 13 AND CITY <> 'Akron' ;
    #
    #   CREATE VIEW UPDATEXVIEW7
    #             AS SELECT EMPNAME, CITY, GRADE
    #                      FROM STAFFV2
    #                      WHERE EMPNAME >= 'Betty' AND EMPNUM < 'E35'
    #                        OR CITY <= 'Deale' AND GRADE > 12
    #                        OR GRADE = 13 AND CITY <> 'Akron' ;
    #
    #   CREATE VIEW UPDATEXVIEW8
    #             AS SELECT MYTABLE.EMPNUM, MYTABLE.EMPNAME
    #                      FROM STAFF MYTABLE
    #                      WHERE MYTABLE.GRADE = 12 ;
    #
    #   CREATE VIEW UPDATEXVIEW9
    #             AS SELECT EMPNAME, CITY, GRADE
    #                      FROM STAFF
    #                      WHERE NOT EMPNAME >= 'Betty' AND EMPNUM <= 'E35'
    #                        OR NOT (CITY <= 'Deale') AND GRADE > 9
    #                        AND NOT (GRADE = 13 AND CITY <> 'Akron')
    #                        OR NOT CITY IN ('Vienna','New York','Deale') ;
    #
    #    CREATE VIEW VSTAFF3 AS SELECT * FROM STAFF3 ;
    #
    # CREATE TABLE CHARACTER18TABLE18 (CHARS18NAME18CHARS CHAR(4)) ;
    #
    # CREATE VIEW  CHARACTERS18VIEW18 (LONGNAME18LONGNAME)
    #              AS SELECT CHARS18NAME18CHARS
    #                   FROM CHARACTER18TABLE18
    #                  WHERE CHARS18NAME18CHARS <> 'long' ;
    #
    #  more from schema8.std
    
    stmt = """CREATE TABLE STAFF14 (EMPNUM    CHAR(3) NOT NULL,
EMPNAME  CHAR(20),
--  -- DEFAULT USER,                XXXXX
--  EMPNAME CHAR precision may be changed to implementation-defined
--               precision for value of USER
GRADE int,
CITY   CHAR(15))  no partition;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE STAFF5 (EMPNUM    CHAR(3) NOT NULL,
EMPNAME  CHAR(20),
GRADE int,
CITY   CHAR(15),
PRIMARY KEY (EMPNUM)
) ;"""
    output = _dci.cmdexec(stmt)
    #       , CHECK (GRADE > 0 AND GRADE < 20)) ;                           XXXXX
    
    stmt = """CREATE TABLE STAFF6 (EMPNUM    CHAR(3) NOT NULL,
EMPNAME  CHAR(20),
GRADE int,
CITY   CHAR(15))  no partition;"""
    output = _dci.cmdexec(stmt)
    #       CHECK (GRADE > 0 AND GRADE < 20),       -- DECIMAL(4) CHECK (GRADE > 0 AND GRADE < 20),
    
    stmt = """CREATE TABLE STAFF7 (EMPNUM    CHAR(3) NOT NULL,
EMPNAME  CHAR(20),
GRADE int,
CITY   CHAR(15),
PRIMARY KEY (EMPNUM)
) ;"""
    output = _dci.cmdexec(stmt)
    #          CHECK (GRADE BETWEEN 1 AND 20)) ;            XXXXX
    
    stmt = """CREATE TABLE STAFF8 (EMPNUM    CHAR(3) NOT NULL,
EMPNAME  CHAR(20),
GRADE int,
CITY   CHAR(15),
PRIMARY KEY (EMPNUM)
) ;"""
    output = _dci.cmdexec(stmt)
    #          CHECK (EMPNAME IS NOT NULL)) ;               XXXXX
    
    stmt = """CREATE TABLE STAFF9 (EMPNUM    CHAR(3) NOT NULL,
EMPNAME  CHAR(20) NOT NULL,
GRADE int,
CITY   CHAR(15),
--          CHECK (EMPNAME NOT LIKE 'T%')
PRIMARY KEY (EMPNAME)
) ;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE STAFF10 (EMPNUM    CHAR(3) NOT NULL,
EMPNAME  CHAR(20),
GRADE int,
CITY   CHAR(15),
PRIMARY KEY (EMPNUM)
) ;"""
    output = _dci.cmdexec(stmt)
    #          CHECK (GRADE NOT IN (5,22))) ;               XXXXX
    
    stmt = """CREATE TABLE STAFF11 (EMPNUM    CHAR(3) NOT NULL,
EMPNAME  CHAR(20),
GRADE int,                      -- DECIMAL(4),                  XXXXX
CITY   CHAR(15),
PRIMARY KEY (EMPNUM)
) ;"""
    output = _dci.cmdexec(stmt)
    #          CHECK (GRADE NOT IN (5,22)           XXXXX
    #                      AND EMPNAME NOT LIKE 'T%')) ;            XXXXX
    
    stmt = """CREATE TABLE STAFF12 (EMPNUM    CHAR(3) NOT NULL,
EMPNAME  CHAR(20),
GRADE int,
CITY   CHAR(15),
PRIMARY KEY (EMPNUM)
) ;"""
    output = _dci.cmdexec(stmt)
    #          CHECK (NOT GRADE IN (5,22)           XXXXX
    #                      AND NOT EMPNAME LIKE 'T%')) ;            XXXXX
    
    stmt = """CREATE TABLE STAFF13 (EMPNUM    CHAR(3) NOT NULL,
EMPNAME  CHAR(20),
GRADE int,
CITY   CHAR(15),
PRIMARY KEY (EMPNUM)
) ;"""
    output = _dci.cmdexec(stmt)
    #          CHECK (NOT EMPNAME IS NULL)) ;               XXXXX
    
    stmt = """CREATE TABLE STAFF15 (EMPNUM    CHAR(3),
EMPNAME  CHAR(20) NOT NULL,
GRADE int,
CITY   CHAR(15))  no partition;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE STAFF16 (EMPNUM    CHAR(3) NOT NULL,
EMPNAME  CHAR(20),              -- DEFAULT NULL,                XXXXX
GRADE int NOT NULL,
CITY   CHAR(15),
PRIMARY KEY (GRADE,EMPNUM)
) ;"""
    output = _dci.cmdexec(stmt)
    #  DECIMAL(4) NOT NULL CHECK (GRADE IN (100,150,200)),          XXXXX
    
    #  The following tables, STAFFXM and PROJXM reference each other.
    #  Table STAFFXM has a "forward reference" to PROJXM.
    
    #  CREATE TABLE STAFFXM
    #     (EMPNUM   CHAR(3) NOT NULL,
    #      EMPNAME  CHAR(20),
    #      GRADE    int,                    -- DECIMAL(4),                  XXXXX
    #      CITY     CHAR(15),
    #      PRIXWK   CHAR(3),
    #      UNIQUE   (EMPNUM),
    #      FOREIGN KEY (PRIXWK)
    #      REFERENCES PROJXM(PNUM))  no partition;
    #
    #  CREATE TABLE PROJXM
    #     (PNUM     CHAR(3) NOT NULL,
    #      PNAME    CHAR(20),
    #      PTYPE    CHAR(6),
    #      BUDGET   int,                    -- DECIMAL(9),                  XXXXX
    #      CITY     CHAR(15),
    #      MGR   CHAR(3),
    #      UNIQUE (PNUM),
    #      FOREIGN KEY (MGR)
    #      REFERENCES STAFFXM(EMPNUM))  no partition;
    #
    # --     The following table is self-referencing.
    
    #  CREATE TABLE STAFFXC
    #     (EMPNUM   CHAR(3) NOT NULL,
    #      EMPNAME  CHAR(20),
    #      GRADE    int,                    -- DECIMAL(4),                  XXXXX
    #      CITY     CHAR(15),
    #      MGR   CHAR(3),
    #      UNIQUE   (EMPNUM),
    #      FOREIGN KEY (MGR)
    #      REFERENCES STAFFXC(EMPNUM))  no partition;
    #
    
    stmt = """CREATE TABLE STAFFXP 
(EMPNUM   CHAR(3) NOT NULL,
EMPNAME  CHAR(20),
GRADE    int,
CITY     CHAR(15),
primary key (EMPNUM)
) ;"""
    output = _dci.cmdexec(stmt)
    #      UNIQUE  (EMPNUM)) ;              XXXX
    
    stmt = """CREATE TABLE PROJXP 
(PNUM     CHAR(3) NOT NULL,
PNAME    CHAR(20),
PTYPE    CHAR(6),
BUDGET   int,
CITY     CHAR(15),
primary key (PNUM)
) ;"""
    output = _dci.cmdexec(stmt)
    
    #     CREATE VIEW STAFF6XWITHXGRADES AS
    #         SELECT EMPNUM,EMPNAME,GRADE,CITY
    #         -- FROM STAFF6
    #         from vwstaff6
    #         WHERE GRADE > 0 AND GRADE < 20 ;
    #         -- WITH CHECK OPTION ;                       XXXXX
    
    #  ************* End of Schema *************
    
    _testmgr.testcase_end(desc)

