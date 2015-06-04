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

# Creates the tables for all the NIST tests; nist, nistvw, nistcrvw & nistx

# This file defines the base tables used in most of the tests.

# This is a standard schema fdefinition.

def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci
    
    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()
    
    stmt = """CREATE TABLE STAFF5 (EMPNUM    CHAR(3) NOT NULL,
EMPNAME  CHAR(20),
GRADE DECIMAL(4),
CITY   CHAR(15),
PRIMARY KEY (EMPNUM),
CHECK (GRADE > 0 AND GRADE < 20));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE STAFF7 (EMPNUM    CHAR(3) NOT NULL,
EMPNAME  CHAR(20),
GRADE DECIMAL(4),
CITY   CHAR(15),
PRIMARY KEY (EMPNUM),
CHECK (GRADE BETWEEN 1 AND 20));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE STAFF8 (EMPNUM    CHAR(3) NOT NULL,
EMPNAME  CHAR(20),
GRADE DECIMAL(4),
CITY   CHAR(15),
PRIMARY KEY (EMPNUM),
CHECK (EMPNAME IS NOT NULL));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE STAFF9 (EMPNUM    CHAR(3) NOT NULL PRIMARY KEY,
EMPNAME  CHAR(20),
GRADE DECIMAL(4),
CITY   CHAR(15),
CHECK (EMPNAME NOT LIKE 'T%'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE CPBASE
(KC INT not null,
JUNK1 CHAR (10),
PRIMARY KEY (KC));"""
    output = _dci.cmdexec(stmt)
    
    # following CQD is added for Highlander R1 QCD-2 POS feature change
    #control query default pos_num_of_partns '0';
    
    stmt = """CREATE TABLE STAFF
(EMPNUM   CHAR(3) NOT NULL not droppable primary key,
EMPNAME  CHAR(20),
GRADE    DECIMAL(4),
CITY     CHAR(15));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE VIEW VWSTAFF
AS SELECT * FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE PROJ
(PNUM     CHAR(3) NOT NULL not droppable primary key,
PNAME    CHAR(20),
PTYPE    CHAR(6),
BUDGET   DECIMAL(9),
CITY     CHAR(15));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE VIEW VWPROJ
AS SELECT * FROM PROJ;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE WORKS
(EMPNUM   CHAR(3) NOT NULL,
PNUM     CHAR(3) NOT NULL,
HOURS    DECIMAL(5),
primary key(EMPNUM,PNUM));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE VIEW VWWORKS
AS SELECT * FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE STAFF1 (EMPNUM    CHAR(3) NOT NULL not droppable primary key,
EMPNAME  CHAR(20),
GRADE DECIMAL(4),
CITY   CHAR(15));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE VIEW VWSTAFF1
AS SELECT * FROM STAFF1;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE PROJ1 (PNUM    CHAR(3) NOT NULL not droppable primary key,
PNAME  CHAR(20),
PTYPE  CHAR(6),
BUDGET DECIMAL(9),
CITY   CHAR(15));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE VIEW VWPROJ1
AS SELECT * FROM PROJ1;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE WORKS1(EMPNUM    CHAR(3) NOT NULL,
PNUM    CHAR(3) NOT NULL,
HOURS   DECIMAL(5),
primary key(EMPNUM, PNUM));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE VIEW VWWORKS1
AS SELECT * FROM WORKS1;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE STAFF3 (EMPNUM    CHAR(3) NOT NULL ,
EMPNAME  CHAR(20) not null,
GRADE DECIMAL(4),
CITY   CHAR(15),
primary key( empnum) );"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE VIEW VWSTAFF3
AS SELECT * FROM STAFF3;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE PROJ3
(PNUM     CHAR(3) NOT NULL,
PNAME    CHAR(20),
PTYPE    CHAR(6),
BUDGET   DECIMAL(9),
CITY     CHAR(15),
primary key (PNUM));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE WORKS3
(EMPNUM   CHAR(3) NOT NULL not droppable primary key,
PNUM     CHAR(3) NOT NULL,
HOURS    DECIMAL(5),
FOREIGN KEY (EMPNUM) REFERENCES STAFF3(EMPNUM),
FOREIGN KEY (PNUM) REFERENCES PROJ3(PNUM));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE VIEW VWWORKS3
AS SELECT * FROM WORKS3;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE STAFF4 (EMPNUM    CHAR(3) NOT NULL not droppable primary key,
EMPNAME  CHAR(20),
GRADE DECIMAL(4),
CITY   CHAR(15));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE VIEW VWSTAFF4
AS SELECT * FROM STAFF4;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE STAFF6 (EMPNUM    CHAR(3) NOT NULL not droppable primary key,
EMPNAME  CHAR(20),
GRADE DECIMAL(4) CHECK (GRADE > 0 AND GRADE < 20),
CITY   CHAR(15));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE LONGINT (LONG_INT DECIMAL(15) not null not droppable primary key);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE VIEW VWLONGINT AS SELECT * FROM LONGINT;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE TEMP_S
(EMPNUM  CHAR(3) not null,
GRADE DECIMAL(4) not null,
CITY CHAR(15) not null,
primary key( EMPNUM, GRADE,CITY ));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE VIEW VWTEMP_S
AS SELECT * FROM TEMP_S;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE TMP
(T1 CHAR (10) not null not droppable primary key,
T2 DECIMAL(2),
T3 CHAR (10));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE VIEW VWTMP
AS SELECT * FROM TMP;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE AA (CHARTEST     CHAR(20) not null not droppable primary key);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE VIEW VWAA
AS SELECT * FROM AA;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE BB (CHARTEST     CHAR not null not droppable primary key);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE VIEW VWBB
AS SELECT * FROM BB;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE BBB (CHARTEST     CHAR ,
cnt int not null not droppable primary key);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE VIEW VWBBB
AS SELECT * FROM BBB;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE CC (CHARTEST     CHARACTER(20) not null not droppable primary key);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE VIEW VWCC
AS SELECT * FROM CC;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE DD (CHARTEST     CHARACTER not null not droppable primary key);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE VIEW VWDD
AS SELECT * FROM DD;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE EE (INTTEST     INTEGER not null not droppable primary key);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE VIEW VWEE
AS SELECT * FROM EE;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE EEE (INTTEST     INTEGER,
cnt int not null not droppable primary key);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE VIEW VWEEE
AS SELECT * FROM EEE;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE FF (INTTEST     INT not null not droppable primary key);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE VIEW VWFF
AS SELECT * FROM FF;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE GG (REALTEST    REAL ,
cnt int not null not droppable primary key);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE VIEW VWGG
AS SELECT * FROM GG;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE GGG (REALTEST     REAL,
cnt int not null not droppable primary key);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE VIEW VWGGG
AS SELECT * FROM GGG;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE HH (SMALLTEST  SMALLINT not null not droppable primary key);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE VIEW VWHH
AS SELECT * FROM HH;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE HHH (SMALLTEST  SMALLINT,
cnt int not null not droppable primary key);"""
    output = _dci.cmdexec(stmt)
    stmt = """CREATE VIEW VWHHH
AS SELECT * FROM HHH;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE II (DOUBLETEST  DOUBLE PRECISION,
cnt int not null not droppable primary key );"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE VIEW VWII
AS SELECT * FROM II;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE III (DOUBLETEST  DOUBLE PRECISION,
cnt int not null not droppable primary key );"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE VIEW VWIII
AS SELECT * FROM III;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE JJ (FLOATTEST  FLOAT,
cnt int not null not droppable primary key );"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE VIEW VWJJ
AS SELECT * FROM JJ;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE JJJ (FLOATTEST  FLOAT,
cnt int not null not droppable primary key );"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE VIEW VWJJJ
AS SELECT * FROM JJJ;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE KK (FLOATTEST  FLOAT(32),
cnt int not null not droppable primary key );"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE VIEW VWKK
AS SELECT * FROM KK;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE LL (NUMTEST  NUMERIC(13,6) not null not droppable primary key);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE VIEW VWLL
AS SELECT * FROM LL;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE MM (NUMTEST  NUMERIC not null not droppable primary key);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE VIEW VWMM
AS SELECT * FROM MM;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE MMM (NUMTEST  NUMERIC,
cnt int not null not droppable primary key );"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE VIEW VWMMM
AS SELECT * FROM MMM;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE MM2 (NUMTEST NUMERIC(10) not null not droppable primary key);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE VIEW VWMM2
AS SELECT * FROM MM2;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE NN (NUMTEST  NUMERIC(9) not null not droppable primary key);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE VIEW VWNN
AS SELECT * FROM NN;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE OO (NUMTEST  NUMERIC(9) not null not droppable primary key);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE VIEW VWOO
AS SELECT * FROM OO;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE PP (NUMTEST  DECIMAL(13,6) not null not droppable primary key);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE VIEW VWPP
AS SELECT * FROM PP;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE QQ (NUMTEST  DECIMAL not null not droppable primary key);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE VIEW VWQQ
AS SELECT * FROM QQ;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE RR (NUMTEST  DECIMAL(8) not null not droppable primary key);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE VIEW VWRR
AS SELECT * FROM RR;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE SS (NUMTEST  DEC(13,6) not null not droppable primary key);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE VIEW VWSS
AS SELECT * FROM SS;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE SSS (NUMTEST  DEC(13,6),
cnt int not null not droppable primary key );"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE VIEW VWSSS
AS SELECT * FROM SSS;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE P1 (NUMTEST  NUMERIC(1) not null not droppable primary key);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE VIEW VWP1
AS SELECT * FROM P1;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE P7 (NUMTEST  NUMERIC(7) not null not droppable primary key);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE VIEW VWP7
AS SELECT * FROM P7;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE P12 (NUMTEST  NUMERIC(12) not null not droppable primary key);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE VIEW VWP12
AS SELECT * FROM P12;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE P15 (NUMTEST  NUMERIC(15) not null not droppable primary key);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE VIEW VWP15
AS SELECT * FROM P15;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE FOUR_TYPES (
T_INT     INTEGER not null not droppable primary key,
T_CHAR    CHAR(10),
T_DECIMAL DECIMAL(10,2),
T_REAL    REAL
);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE VTABLE
(COL1   INTEGER ,
COL2   INTEGER,
COL3   INTEGER,
COL4   INTEGER,
COL5   DECIMAL(7,2),
cnt int not null not droppable primary key);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE VIEW VWVTABLE
AS SELECT * FROM VTABLE;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE UPUNIQ (
cnt      int not null not droppable primary key,
NUMKEY  DECIMAL(3) NOT NULL UNIQUE,
COL2    CHAR(2));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE VIEW VWUPUNIQ
AS SELECT * FROM UPUNIQ;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE TEXT80  (TEXXT CHAR(80) not null not droppable primary key);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE VIEW VWTEXT80
AS SELECT * FROM TEXT80;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE TEXT132  (TEXXT CHAR(132) not null not droppable primary key);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE VIEW VTEXT132
AS SELECT * FROM TEXT132;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE TEXT240  (TEXXT CHAR(240) not null not droppable primary key);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE VIEW VTEXT240
AS SELECT * FROM TEXT240;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE TEXT256  (TEXXT CHAR(256) not null not droppable primary key);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE VIEW VTEXT256
AS SELECT * FROM TEXT256;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE TEXT512  (TEXXT CHAR(512) not null not droppable primary key);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE VIEW VTEXT512
AS SELECT * FROM TEXT512;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE TEXT1024  (TEXXT CHAR(1024) not null not droppable primary key);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE VIEW VTX1024
AS SELECT * FROM TEXT1024;"""
    output = _dci.cmdexec(stmt)
    
    # The following tables are used to test the limitations (12-14-88)
    
    stmt = """CREATE TABLE T4 (
STR110 CHAR(110) NOT NULL,
NUM6   NUMERIC(6) NOT NULL,
COL3   CHAR(10),COL4 CHAR(20),
primary key(STR110,NUM6));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE VIEW VWT4
AS SELECT * FROM T4;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE T240(STR240 CHAR(240) not null not droppable primary key);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE VIEW VWT240
AS SELECT * FROM T240;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE DEC15(COL1 DECIMAL(15,7) not null not droppable primary key);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE VIEW VWDEC15
AS SELECT * FROM DEC15;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE FLO15(COL1 FLOAT(15),
cnt int not null not droppable primary key);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE VIEW VWFLO15
AS SELECT * FROM FLO15;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE INT10(COL1 INTEGER not null not droppable primary key, COL2 SMALLINT);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE VIEW VWINT10
AS SELECT * FROM INT10;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE T100(C1 CHAR(2) not null not droppable primary key,
C2 CHAR(2),C3 CHAR(2),C4 CHAR(2),
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
C97 CHAR(2),C98 CHAR(2),C99 CHAR(2),C100 CHAR(2));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE VIEW VWT100
AS SELECT * FROM T100;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE T2000(STR110 CHAR(110) not null not droppable primary key,
STR120 CHAR(120),
STR130 CHAR(130),STR140 CHAR(140),
STR150 CHAR(150),STR160 CHAR(160),
STR170 CHAR(170),STR180 CHAR(180),
STR190 CHAR(190),STR200 CHAR(200),
STR210 CHAR(210),STR216 CHAR(216));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE VIEW VWT2000
AS SELECT * FROM T2000;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE T8(COL1 CHAR(2) NOT NULL,COL2 CHAR(4) NOT NULL,
COL3 CHAR(6) NOT NULL,COL4 CHAR(8) NOT NULL,
COL5 CHAR(10) NOT NULL,COL6 CHAR(12) NOT NULL,
COL7 CHAR(14),COL8 CHAR(16),
primary key(COL1,COL2,COL3,COL4,COL5,COL6));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE VIEW VWT8
AS SELECT * FROM T8;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE T118(STR118 CHAR(118) NOT NULL not droppable primary key);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE VIEW VWT118
AS SELECT * FROM T118;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE T12(COL1 CHAR(1) not null ,
COL2 CHAR(2) not null,
COL3 CHAR(4) not null, COL4 CHAR(6) not null,
COL5 CHAR(8) not null, COL6 CHAR(10) not null,
COL7 CHAR(20) not null, COL8 CHAR(30) not null,
COL9 CHAR(40) not null, COL10 CHAR(50) not null,
COL11 INTEGER not null, COL12 INTEGER not null,
primary key (COL1,COL2,COL3,COL4,COL5,COL6,COL7,COL8,COL9,COL10,COL11,COL12) );"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE VIEW VWT12
AS SELECT * FROM T12;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE SV (NUMTEST NUMERIC(8,3) not null not droppable primary key);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE VIEW VWSV
AS SELECT * FROM SV;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE JJ_20 (FLOATTEST  FLOAT(20),
cnt int not null not droppable primary key);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE VIEW VWJJ_20
AS SELECT * FROM JJ_20;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE PP_15 (NUMTEST  DECIMAL(15,15) not null not droppable primary key);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE VIEW VWPP_15
AS SELECT * FROM PP_15;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE PP_7  (NUMTEST  DECIMAL(15,7) not null not droppable primary key);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE VIEW VWPP_7
AS SELECT * FROM PP_7;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE P15_15 (NUMTEST  NUMERIC(15,15) not null not droppable primary key);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE VIEW VWP15_15
AS SELECT * FROM P15_15;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE P15_7 (NUMTEST  NUMERIC(15,7) not null not droppable primary key);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE VIEW VWP15_7
AS SELECT * FROM P15_7;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE TABLEFGHIJKLMNOPQ19
(COL2  INTEGER not null not droppable primary key);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE SHORTTABLE
(COLUMN123456789IS19  INTEGER not null not droppable primary key);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE BASETABLE1 (COL1  INTEGER not null not droppable primary key);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE VIEW VIEWABCDEFGHIKLMN19 (COL3)
AS SELECT COL1 FROM BASETABLE1;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE SIZ1_P
(S1   CHAR(3) NOT NULL,
S2   CHAR(3) NOT NULL,
S3   DECIMAL(4) NOT NULL,
S4   CHAR(3) NOT NULL,
S5   DECIMAL(4) NOT NULL,
S6   CHAR(3) NOT NULL,
R1   CHAR(3),
R2   CHAR(3),
R3   DECIMAL(4),
primary key   (S1,S2,S3,S4,S5,S6));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE SIZ1_F
(F1   CHAR(3) NOT NULL ,
F2   CHAR(3) not null,
F3   DECIMAL(4) not null,
F4   CHAR(3) not null,
F5   DECIMAL(4) not null,
F6   CHAR(3) not null,
R1   CHAR(3) not null,
R2   DECIMAL(5) not null,
R3   DECIMAL(4)
,FOREIGN KEY   (F1,F2,F3,F4,F5,F6)
REFERENCES SIZ1_P(S1,S2,S3,S4,S5,S6),
primary key (F1,F2,F3,F4,F5,F6,R1,R2) );"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE TEMP_OBSERV (
YEAR_OBSERV  NUMERIC(4) ,
CITY         CHAR(10) default '1' not null not droppable primary key ,
MAX_TEMP     NUMERIC(5,2),
MIN_TEMP     NUMERIC(5,2));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE USIG (C1 INT not null not droppable primary key, C_1 INT);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE U_SIG (C1 INT not null not droppable primary key, C_1 INT);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE CHARACTER18TABLE18 (CHARS18NAME18CHARS CHAR(4), cnt int default 1 not null not droppable primary key);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE CPREF (
KCR INT not null not droppable primary key,
JUNK2 CHAR (10)
,FOREIGN KEY (KCR) REFERENCES CPBASE);"""
    output = _dci.cmdexec(stmt)
    
    # restore POS default
    #control query default pos_num_of_partns reset;
    
    stmt = """showcontrol default pos;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO SIZ1_P VALUES ('E1','TTT',1,'SSS',10,'RRR','HHH','YYY',20),
('E1','TTS',1,'SSS',10,'RRR','HHH','YYY',21),
('E2','TTT',1,'SSS',10,'RRR','HHH','YYY',22),
('E3','TTT',1,'SSS',11,'RRR','HHH','YYY',23),
('E4','TTT',2,'SSS',10,'RRR','HHH','YYY',24),
('E1','TTS',3,'SSS',10,'RRR','HHH','YYY',25),
('E2','TTT',1,'SSS',10,'TRR','HHH','YYY',26),
('E3','TTT',4,'SSS',11,'RRR','HHH','YYY',27);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO SIZ1_F VALUES ('E1','TTT',1,'SSS',10,'RRR','YYY',90,20),
('E1','TTS',1,'SSS',10,'RRR','YYY',91,20),
('E2','TTT',1,'SSS',10,'RRR','YYY',92,20),
('E3','TTT',1,'SSS',11,'RRR','YYY',93,20),
('E4','TTT',2,'SSS',10,'RRR','YYY',94,20),
('E1','TTS',3,'SSS',10,'RRR','YYY',95,20),
('E2','TTT',1,'SSS',10,'TRR','YYY',96,20),
('E2','TTT',1,'SSS',10,'TRR','YYY',97,20);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """SELECT COUNT(*) FROM SIZ1_P;"""
    output = _dci.cmdexec(stmt)
    # PASS:Setup if count = 8?
    
    stmt = """SELECT COUNT(*) FROM SIZ1_F;"""
    output = _dci.cmdexec(stmt)
    # PASS:Setup if count = 8?
    
    stmt = """CREATE VIEW V_WORKS1
AS SELECT * FROM WORKS
WHERE HOURS > 15
WITH CHECK OPTION;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE VIEW V_WORKS2
AS SELECT * FROM V_WORKS1
WHERE EMPNUM = 'E1'
OR EMPNUM = 'E6';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE VIEW V_WORKS3
AS SELECT * FROM V_WORKS2
WHERE PNUM = 'P2'
OR PNUM = 'pP7'
WITH CHECK OPTION;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO USIG VALUES (0,2), (1,3), (4,6), (5,7);"""
    output = _dci.cmdexec(stmt)
    
    # ************* create view statements follow *************
    
    stmt = """CREATE VIEW SET_TEST (EMP1, EMP_AVG, EMP_MAX) AS
SELECT STAFF.EMPNUM, AVG(HOURS), MAX(HOURS)
FROM STAFF, WORKS
GROUP BY STAFF.EMPNUM;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE VIEW DUP_COL (EMP1, PNO, HOURS, HOURS_2) AS
SELECT EMPNUM, PNUM, HOURS, HOURS * 2
FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE VIEW STAFFV1
AS SELECT * FROM STAFF
WHERE  GRADE >= 12;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE VIEW STAFFV2
AS SELECT * FROM STAFF
WHERE  GRADE >= 12
WITH CHECK OPTION;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE VIEW STAFF_WORKS_DESIGN (NAM, COST, PROJECT)
AS SELECT EMPNAME,HOURS*2*GRADE,PNAME
FROM   PROJ,STAFF,WORKS
WHERE  STAFF.EMPNUM=WORKS.EMPNUM
AND WORKS.PNUM=PROJ.PNUM
AND PTYPE='Design';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE VIEW TEMP_SS(EMPNUM,GRADE,CITY)
AS SELECT EMPNUM,GRADE,CITY
FROM   STAFF
WHERE  GRADE > 12
WITH CHECK OPTION;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE VIEW  CHARACTERS18VIEW18 (LONGNAME18LONGNAME)
AS SELECT CHARS18NAME18CHARS
FROM CHARACTER18TABLE18
WHERE CHARS18NAME18CHARS <> 'long';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE VIEW VWSTAFF9
AS SELECT * FROM STAFF9;"""
    output = _dci.cmdexec(stmt)
    
    # ************* End of Schema *************
    
    # NIST SQL Test Suite, V5.0, Interactive SQL, vdata.sql
    
    # assumes the tables are fresh created
    
    #   This routine initializes the contents of tables:
    #        STAFF, PROJ, WORKS, STAFF3, VTABLE, and UPUNIQ
    #   This routine may be run at any time to re-initialize tables.
    
    stmt = """INSERT INTO STAFF VALUES ('E1','Alice',12,'Deale'),
('E2','Betty',10,'Vienna'),
('E3','Carmen',13,'Vienna'),
('E4','Don',12,'Deale'),
('E5','Ed',13,'Akron');"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO PROJ VALUES ('P1','MXSS','Design',10000,'Deale'),
('P2','CALM','Code',30000,'Vienna'),
('P3','SDP','Test',30000,'Tampa'),
('P4','SDP','Design',20000,'Deale'),
('P5','IRM','Test',10000,'Vienna'),
('P6','PAYR','Design',50000,'Deale');"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO WORKS VALUES ('E1','P1',40),
('E1','P2',20),
('E1','P3',80),
('E1','P4',20),
('E1','P5',12),
('E1','P6',12),
('E2','P1',40),
('E2','P2',80),
('E3','P2',20),
('E4','P2',20),
('E4','P4',40),
('E4','P5',80);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """SELECT COUNT (*) FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    # PASS:Setup if count = 5?
    
    stmt = """SELECT COUNT (*) FROM PROJ;"""
    output = _dci.cmdexec(stmt)
    # PASS:Setup if count = 6?
    
    stmt = """SELECT COUNT (*) FROM WORKS;"""
    output = _dci.cmdexec(stmt)
    # PASS:Setup if count = 12?
    
    stmt = """INSERT INTO STAFF3
SELECT *
FROM   STAFF;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO VTABLE VALUES (10,+20,30,40,10.50,1),
(0,1,2,3,4.25,2),
(100,200,300,400,500.01,3),
(1000,-2000,3000,NULL,4000.00,4);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO UPUNIQ VALUES (1,1,'A'),
(2,2,'B'),
(3,3,'C'),
(4,4,'D'),
(5,6,'F'),
(6,8,'H');"""
    output = _dci.cmdexec(stmt)
    
    stmt = """SELECT COUNT (*) FROM STAFF3;"""
    output = _dci.cmdexec(stmt)
    # PASS:Setup if count = 5?
    
    stmt = """SELECT COUNT (*) FROM VTABLE;"""
    output = _dci.cmdexec(stmt)
    # PASS:Setup if count = 4?
    
    stmt = """SELECT COUNT (*) FROM UPUNIQ;"""
    output = _dci.cmdexec(stmt)
    # PASS:Setup if count = 6?
    
    # Elena Krotkova (03_21_07)--
    stmt = """create table dt_mth_d
( CLDR_MTH_STRT_DT  Date,
startday     Date not null primary key,
lastday      Date
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into  dt_mth_d	values
(date '2005-03-31', date '2005-02-28', date '2005-03-30');"""
    output = _dci.cmdexec(stmt)
