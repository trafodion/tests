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
    
def test001(desc="""create BAT database"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #  Test case name:     testA00
    #  Description:        This test creates the SQL database.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    
    stmt = """CREATE TABLE COURSE 
(
CNO     VARCHAR(3)       NOT NULL,
CNAME   VARCHAR(22)      NOT NULL,
CDESCP  VARCHAR(25)      NOT NULL,
CRED    INT,
CLABFEE NUMERIC(5,2),
CDEPT   VARCHAR(4)       NOT NULL
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """INSERT INTO COURSE VALUES
('C11', 'INTRO TO CS','FOR ROOKIES',3, 100, 'CIS');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO COURSE VALUES
('C22', 'DATA STRUCTURES','VERY USEFUL',3, 50, 'CIS');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO COURSE VALUES
('C33', 'DISCREET MATHEMATICS','ABSOLUTELY NECESSARY',3, 0, 'CIS');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO COURSE VALUES
('C44', 'DIGITAL CIRCUITS','AH HA!',3, 0, 'CIS');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO COURSE VALUES
('C55', 'COMPUTER ARCH.','VON NEUMANN''S MACH.',3, 100, 'CIS');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO COURSE VALUES
('C66', 'RELATIONAL DATABASES','THE ONLY WAY TO GO',3, 500, 'CIS');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO COURSE VALUES
('P11', 'EMPIRICISM','SEE IT-BELIEVE IT',3, 100, 'PHIL');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO COURSE VALUES
('P22', 'RATIONALISM','FOR CIS MAJORS',3, 50, 'PHIL');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO COURSE VALUES
('P33', 'EXISTENTIALISM','FOR CIS MAJORS',3, 200, 'PHIL');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO COURSE VALUES
('P44', 'SOLIPSISM','MY SELF AND I',6, 0, 'PHIL');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO COURSE VALUES
('T11', 'SCHOLASTICISM','FOR THE PIOUS',3, 150, 'THEO');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO COURSE VALUES
('T12', 'FUNDAMENTALISM','FOR THE CAREFREE',3, 90, 'THEO');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO COURSE VALUES
('T33', 'HEDONISM','FOR THE SANE',3, 0, 'THEO');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO COURSE VALUES
('T44', 'COMMUNISM','FOR THE GREEDY',6, 200, 'THEO');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """CREATE TABLE DEPART 
(
DEPT     CHAR(4)   NOT NULL,
DBLD     CHAR(2),
DROOM    CHAR(3),
DCHFNO   CHAR(2)
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """INSERT INTO DEPART VALUES ('THEO', 'HU', '200', '10');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO DEPART VALUES ('CIS', 'SC', '300', '80');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO DEPART VALUES ('MGT', 'SC', '100', NULL);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO DEPART VALUES ('PHIL', 'HU', '100', '60');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """CREATE TABLE STAFF 
(
ENAME      CHAR(10)    NOT NULL,
ETITLE     CHAR(10),
ESALARY    INT,
DEPT       CHAR(4)
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """INSERT INTO STAFF VALUES ('LUKE', 'EVANGLIST3',53 , 'THEO');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO STAFF VALUES ('MARK', 'EVANGLIST2',52 , 'THEO');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO STAFF VALUES ('MATTHEW', 'EVANGLIST1',51 , 'THEO');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO STAFF VALUES ('DICK NIX', 'CROOK',25001 , 'PHIL');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO STAFF VALUES ('HANK KISS', 'JESTER',25000 , 'PHIL');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO STAFF VALUES ('JOHN', 'EVANGLIST4',54 , 'THEO');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO STAFF VALUES ('EUCLID', 'LAB ASSIST',1000 , 'MATH');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO STAFF VALUES ('ARCHIMEDES', 'LAB ASSIST',200 , 'ENG');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO STAFF VALUES ('DA VINCI', 'LAB ASSIST',500 , NULL);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """CREATE TABLE STUDENT 
(
SNO     CHAR(3)      NOT NULL,
SNAME   CHAR(25)     NOT NULL,
SADDR   CHAR(25),
SPHNO   CHAR(12),
SBDATE  CHAR(6),
SIQ     INT,
SADVFNO CHAR(2),
SMAJ    CHAR(4)       NOT NULL
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """INSERT INTO STUDENT VALUES('235','CURLEY DUBAY','CONNECTICUT','203-123-4567','780517',
122 ,'10','THEO');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO STUDENT VALUES('150','LARRY DUBAY','CONNECTICUT','203-123-4567','780517',
121 ,'80','CIS');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO STUDENT VALUES('100','MEO DUBAY','CONNECTICUT','203-123-4567','780517',
120 ,'10','THEO');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO STUDENT VALUES('800','ROCKY BALBOA','PENNSYLVANIA','112-112-1122','461004',
99 ,'60','PHIL');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """CREATE TABLE CLASS1 
(
CNO          CHAR(3)   NOT NULL,
SEC          CHAR(2)   NOT NULL,
CINSTRFNO    CHAR(2),
CDAY         CHAR(2),
CTIME        CHAR(15),
CBLD         CHAR(2),
CROOM        CHAR(3)
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """INSERT INTO CLASS1 VALUES
('','','','','','','');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO CLASS1 VALUES
('C33','01','80','WE','09:00-10:30A.M.','SC','305');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO CLASS1 VALUES
('C55','01','85','TH','11:00-12:00A.M.','SC','306');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO CLASS1 VALUES
('C11','01','08','MO','08:00-09:00A.M.','SC','305');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO CLASS1 VALUES
('C11','02','08','TU','08:00-09:00A.M.','SC','306');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO CLASS1 VALUES
('P11','01','06','TH','09:00-10:00A.M.','HU','102');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO CLASS1 VALUES
('P33','01','06','FR','11:00-12:00A.M.','HU','201');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO CLASS1 VALUES
('T11','01','10','MO','10:00-11:00A.M.','HU','101');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO CLASS1 VALUES
('T11','02','65','MO','10:00-11:00A.M.','HU','102');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO CLASS1 VALUES
('T33','01','65','WE','11:00-12:00A.M.','HU','101');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """CREATE TABLE FACULTY 
(
FNO         CHAR(2)     NOT NULL,
FNAME       CHAR(20)    NOT NULL,
FADDR       CHAR(25),
FHIRE_DATE  CHAR(10),
FNUM_DEP    INT,
FSALARY     NUMERIC(7,2),
FDEPT       CHAR(4)
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """INSERT INTO FACULTY VALUES
('06','KATHY PEPE','7 STONEBRIDGE RD','1979-01-15',2, 35000,'PHIL');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO FACULTY VALUES
('10','JESSIE MARTYN','2135 EAST DR','1982-03-07',1, 45000,'THEO');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO FACULTY VALUES
('08','JOE COHN','BOX 1138','1979-07-09',2, 35000,'CIS');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO FACULTY VALUES
('85','AL HARTLEY','SILVER STREET','1979-09-05',7, 45000,'CIS');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO FACULTY VALUES
('60','JULIE MARTYN','2135 EAST DR','1978-05-17',1, 45000,'PHIL');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO FACULTY VALUES
('65','LISA BOBAK','77 LAUGHING LN','1981-09-17',1, 36000,'THEO');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO FACULTY VALUES
('80','BARB HLAVATY','489 SOUTH ROAD','1982-01-16',3, 35000,'CIS');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """CREATE TABLE regist 
(
CNO      CHAR(3)       NOT NULL,
SEC      CHAR(2)       NOT NULL,
SNO      CHAR(3)       NOT NULL,
REG_DATE DATE
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """INSERT INTO regist VALUES
('C11', '01', '325', DATE '1988-01-04');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO regist VALUES
('C11', '01', '800', DATE '1987-12-15');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO regist VALUES
('C11', '02', '100', DATE '1987-12-17');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO regist VALUES
('C11', '02', '150', DATE '1987-12-17');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO regist VALUES
('P33', '01', '100', DATE '1987-12-23');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO regist VALUES
('P33', '01', '800', DATE '1987-12-23');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO regist VALUES
('T11', '01', '100', DATE '1987-12-23');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO regist VALUES
('T11', '01', '150', DATE '1987-12-15');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO regist VALUES
('T11', '01', '800', DATE '1987-12-15');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO regist VALUES
('C11', '01', '111', DATE '1992-12-26');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """CREATE TABLE NULLTAB 
(
PKEY  INT,
COLA  INT,
COLB  INT,
COLC  INT
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """INSERT INTO NULLTAB VALUES (1,    10,     20,   5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO NULLTAB VALUES (2,    30,     30,   5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO NULLTAB VALUES (3,    160,   NULL,  10);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO NULLTAB VALUES (4,    NULL,   170,   5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO NULLTAB VALUES (5,    NULL,  NULL,  10);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO NULLTAB VALUES (6,    10,     40,   5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO NULLTAB VALUES (7,    30,     60,   5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO NULLTAB VALUES (8,    NULL,  NULL, NULL);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO NULLTAB VALUES (NULL, NULL,  NULL, NULL);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO NULLTAB VALUES (NULL, NULL,  NULL, NULL);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO NULLTAB VALUES (NULL, NULL,  NULL, NULL);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    _testmgr.testcase_end(desc)

def test002(desc="""Display some subset of rows and columns."""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     testA01
    #  Description:        This test verifies displaying an entire table.
    #                      The SELECT statement
    #                      Displaying an entire table.
    #                      WHERE clause
    #                      Displaying specified columns.
    #                      Display some subset of rows and columns.
    #                      DISTINCT keyword
    #                      Displaying CONSTANT data
    #                      COLUMN ALIASES
    #  Includes:
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    #  1.1
    
    stmt = """select * from COURSE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s0')
    
    #  --------------------------------
    #  WHERE clause
    #  --------------------------------
    
    #  1.2
    stmt = """select * from COURSE where clabfee = 0.00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s1')
    
    #  1.3
    stmt = """select * from COURSE where cdept = 'PHIL';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s2')
    
    #  1A
    stmt = """select * from COURSE where clabfee < 150;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s3')
    
    #  1B
    stmt = """select * from COURSE where cred > 3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s4')
    
    #  1C
    stmt = """select * from COURSE where cdept = 'THEO';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s5')
    
    # 1D
    stmt = """select * from COURSE where cname = 'RELATIONAL DATABASE';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    #  1E
    stmt = """select * from COURSE where cno = 'P44';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s6')
    
    #  1.4
    stmt = """select * from COURSE where cname > 'HEDONISM';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s7')
    
    #  1F
    stmt = """select * from COURSE where cno < 'P01';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s8')
    
    #  1G
    stmt = """select * from COURSE where cname > 'RATIONALISM';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s9')
    #  --------------------------------
    #  Displaying specified columns.
    #  --------------------------------
    #  1.5
    stmt = """SELECT CNO, CNAME, CDEPT FROM COURSE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s10')
    
    #  1.6
    stmt = """SELECT CDEPT, CNAME, CNO FROM COURSE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s11')
    
    #  1H
    stmt = """SELECT CNAME, CDESCP FROM COURSE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s12')
    
    #  1I
    stmt = """SELECT CDEPT, CNO, CLABFEE, CRED FROM COURSE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s13')
    #  -----------------------------------------
    #  Display some subset of rows and columns.
    #  -----------------------------------------
    
    #  1.7
    stmt = """SELECT CNO, CDEPT, CLABFEE
FROM   COURSE 
WHERE  CLABFEE < 100;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s14')
    
    #  1J
    stmt = """SELECT CNO, CLABFEE
FROM   COURSE 
WHERE  CLABFEE > 100;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s15')
    
    #  1K
    stmt = """SELECT  CNAME
FROM    COURSE 
WHERE   CDEPT = 'CIS';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s16')
    
    #  1.8
    stmt = """SELECT CDEPT FROM COURSE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s17')
    
    #  1L
    stmt = """SELECT CLABFEE FROM COURSE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s18')
    
    #  ------------------------------------
    #  DISTINCT keyword
    #  ------------------------------------
    #  1.9
    stmt = """SELECT DISTINCT CDEPT FROM COURSE ORDER BY CDEPT;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s19')
    
    #  1.10
    stmt = """SELECT CDEPT, CRED
FROM   COURSE 
WHERE  CLABFEE < 100;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s20')
    
    #  1.11
    stmt = """SELECT DISTINCT CDEPT, CRED
FROM   COURSE 
WHERE  CLABFEE < 100
ORDER BY CDEPT;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s21')
    
    #  ------------------------------------
    #  DISPLAYING CONSTANT DATA
    #  ------------------------------------
    stmt = """SELECT CNO, CNAME, 'EXPENSIVE'
FROM   COURSE 
WHERE  CLABFEE > 100;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s22')
    
    #  ------------------------------------
    #  COLUMN ALIASES
    #  ------------------------------------
    #  1.13
    
    stmt = """SELECT CNO CN, CNAME COURSE_NAME, CLABFEE
FROM   COURSE 
WHERE  CDEPT = 'PHIL';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s23')
    
    #  1P
    stmt = """SELECT * FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s24')
    
    #  1Q
    stmt = """SELECT * FROM STAFF WHERE ESALARY < 1000;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s25')
    
    #  1R
    stmt = """SELECT * FROM STAFF WHERE DEPT = 'THEO';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s26')
    
    #  1S
    stmt = """SELECT ENAME, ETITLE FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s27')
    
    #  1T
    stmt = """SELECT ENAME, ESALARY FROM STAFF WHERE ESALARY > 1000;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s28')
    
    #  1U
    stmt = """SELECT ENAME, ETITLE FROM STAFF WHERE ENAME < 'MARK';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s29')
    
    #  1V
    stmt = """SELECT DISTINCT ETITLE FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s30')
    
    _testmgr.testcase_end(desc)

def test003(desc="""Sorting the "Result" table with ORDER BY CLAUSE."""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     testA03
    #  Description:        This test verifies the SQL
    #                      Sorting the "Result" table
    #                      ORDER BY CLAUSE
    #                      ORDER BY COLUMN NUMBER
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    
    #  3.1
    stmt = """SELECT * FROM COURSE ORDER BY CLABFEE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s0')
    
    #  3A
    stmt = """SELECT * FROM COURSE ORDER BY CDEPT ASC;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s1')
    
    #  3.2
    stmt = """SELECT CNO, CNAME, CRED
FROM   COURSE 
WHERE  CDEPT = 'CIS'
ORDER BY CNO DESC;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s2')
    
    #
    stmt = """SELECT CNO, CNAME, CRED
FROM   COURSE 
WHERE  CDEPT = 'CIS'
ORDER BY CLABFEE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s3')
    
    #  3B
    stmt = """SELECT CNAME, CLABFEE
FROM COURSE 
WHERE CDEPT = 'PHIL'
ORDER BY CNAME DESC;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s4')
    
    #  ------------------------------------
    #  SORTING ON MULTIPLE COLUMNS
    #  ------------------------------------
    #  This is a two level sort.
    stmt = """SELECT  CDEPT, CNAME
FROM    COURSE 
ORDER BY  CDEPT, CNAME;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s5')
    
    #  This is a four level sort.
    stmt = """SELECT  CRED, CLABFEE, CDEPT, CNAME
FROM    COURSE 
ORDER BY CRED, CLABFEE, CDEPT, CNAME;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s6')
    
    #  3C
    #  Display the CNAME, CLABFEE,  CNO, AND CRED columns (in that order)
    #  for every row in the table. sort the displayed rows by CNO within
    #  CLABFEE.
    stmt = """SELECT   CNAME, CLABFEE, CNO, CRED
FROM     COURSE 
ORDER BY CLABFEE, CNO;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s7')
    
    #  ------------------------------------
    #  ORDER BY COLUMN NUMBER
    #  ------------------------------------
    #  3.4
    stmt = """SELECT CNO, CLABFEE, CRED
FROM   COURSE 
ORDER BY 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s8')
    
    #  3D
    #  Display the entire COURSE table sorted in descending sequence by the
    #  third column.
    stmt = """SELECT   *
FROM     COURSE 
ORDER BY  3 DESC;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s9')
    
    #  3.5
    stmt = """SELECT CDEPT, CLABFEE, CRED
FROM   COURSE 
ORDER BY CDEPT, 3 DESC, CLABFEE DESC;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s10')
    
    #  3E
    stmt = """SELECT CDEPT, CLABFEE, CNAME
FROM   COURSE 
WHERE  CRED = 3
ORDER BY  CDEPT, CLABFEE DESC, 3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s11')
    
    #  3F
    stmt = """SELECT *
FROM STAFF 
ORDER BY ENAME;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s12')
    
    #  3G
    stmt = """SELECT ENAME, ESALARY
FROM   STAFF 
WHERE  ESALARY < 1000
ORDER BY ESALARY DESC;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s13')
    
    #  3H
    stmt = """SELECT *
FROM STAFF 
WHERE DEPT = 'THEO'
ORDER BY ETITLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s14')
    
    #  3I
    stmt = """SELECT DEPT, ENAME, ESALARY
FROM STAFF 
ORDER BY DEPT, ESALARY;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s15')
    
    #  3J
    stmt = """SELECT DEPT, ETITLE, ESALARY
FROM   STAFF 
ORDER BY DEPT, ESALARY DESC;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s16')
    
    _testmgr.testcase_end(desc)

def test004(desc="""Boolean connectors i.e. AND, OR, NOT, IN, NOT IN"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     testA04
    #  Description:        Boolean connectors i.e. AND, OR, NOT, IN, NOT IN,
    #                      BETWEEN , NOT BETWEEN
    #                      AND connector, Multiple ANDs
    #                      OR connector, Multiple ORs
    #                      NOT keyword
    #                      Use of Parentheses
    #                      IN Keyword, NOT IN
    #                      BETWEEN keyword
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    
    #  4.1
    stmt = """SELECT *
FROM COURSE 
WHERE CLABFEE = 0
AND CDEPT = 'CIS';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s0')
    
    #  4A
    stmt = """SELECT *
FROM COURSE 
WHERE CRED = 3
AND CDEPT = 'PHIL';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s1')
    
    #  4.2
    #  LABFEE BETWEEN  ZERO AND 100 DOLLARS
    stmt = """SELECT *
FROM COURSE 
WHERE CLABFEE > 0
AND   CLABFEE < 100;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s2')
    
    #  4B
    #  LABFEE BETWEEN AND INCLUDING $100 AND $500
    
    stmt = """SELECT *
FROM COURSE 
WHERE CLABFEE >= 100
AND   CLABFEE <= 500;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s3')
    
    #  ----------------------------------------------
    #  Multiple ANDs
    #  ----------------------------------------------
    #  4.3
    stmt = """SELECT *
FROM COURSE 
WHERE CLABFEE > 0
AND   CLABFEE < 100
and   CDEPT = 'PHIL'
AND   CRED = 3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s4')
    
    #  4C
    stmt = """SELECT *
FROM COURSE 
WHERE CRED = 3
AND CDEPT = 'THEO'
AND CLABFEE <= 400
AND CLABFEE >= 100;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s5')
    
    #  ----------------------------------------------
    #  OR Connector
    #  ----------------------------------------------
    #  4.4
    stmt = """SELECT *
FROM   COURSE 
WHERE  CDEPT = 'CIS'
OR     CDEPT  = 'PHIL';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s6')
    
    #  4D
    stmt = """SELECT *
FROM   COURSE 
WHERE  CDEPT = 'THEO'
OR     CDEPT  = 'PHIL';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s7')
    
    #  4.5
    stmt = """SELECT *
FROM   COURSE 
WHERE  CDEPT = 'CIS'
OR     CLABFEE = 0.00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s8')
    
    #  ----------------------------------------------
    #  Multiple oRs
    #  ----------------------------------------------
    #  4.6
    stmt = """SELECT *
FROM   COURSE 
WHERE  CLABFEE = 50
OR     CLABFEE = 100
OR     CLABFEE = 150
OR     CLABFEE = 200;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s9')
    
    #  4F
    stmt = """SELECT *
FROM   COURSE 
WHERE  CLABFEE = 0
OR     CLABFEE = 90
OR     CLABFEE = 150;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s10')
    
    #  ----------------------------------------------
    #  NOT keyword
    #  ----------------------------------------------
    #  4.7
    stmt = """select cname, cdept
from COURSE 
where not cdept = 'CIS';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s11')
    
    #  The following queries should give the same result.
    
    stmt = """select cname, cdept
from COURSE 
where  cdept <> 'CIS';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s12')
    
    #  4G
    stmt = """SELECT CNO, CNAME, CLABFEE
FROM   COURSE 
WHERE  CLABFEE <> 100;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s13')
    
    stmt = """SELECT CNO, CNAME, CLABFEE
FROM   COURSE 
WHERE  NOT CLABFEE = 100;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s14')
    
    #  4.8
    stmt = """SELECT CNAME, CDEPT
FROM   COURSE 
WHERE NOT CDEPT = 'CIS'
AND   NOT CDEPT = 'PHIL';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s15')
    
    #  4H
    stmt = """SELECT CNO, CLABFEE
FROM COURSE 
WHERE NOT CLABFEE = 100
AND   NOT CLABFEE = 200;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s16')
    
    #  HIERARCHY OF Boolean OPERATORS
    #  NOT, AND , OR IS THE ORDER OF EVALUATION
    #  4.9
    #  Display all information about any theology course
    #  which has a zero labfee, or any course ( regardless
    #  of its department and labfee) which is worth 6 credits.
    
    stmt = """select *
from COURSE 
where  cdept = 'THEO'
and    clabfee = 0
or     cred = 6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s17')
    
    #  The following two queries are equivalent
    
    stmt = """select *
from COURSE 
where  cred = 6
or     cdept = 'THEO'
and    clabfee = 0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s18')
    
    stmt = """select *
from COURSE 
where  cred = 6
or     (cdept = 'THEO'and    clabfee = 0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s19')
    
    #  Use of Parentheses
    #  4.9
    #  Display all information about any theology course
    #  which have a zero labfee, or are worth 6 credits.
    stmt = """select *
from COURSE 
where  cdept = 'THEO'
and    (clabfee = 0 OR cred = 6 );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s20')
    
    #  The following query is equivalent
    stmt = """select *
from COURSE 
where  (cdept = 'THEO' AND cred = 6)
OR     (cdept = 'THEO' AND clabfee = 0 );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s21')
    
    #  4I
    #  Select all the information about any 6 credit philosophy
    #  course, or any course with a labfee which exceeds $200
    #  ( regardless of its department id or credits).
    
    stmt = """select *
from COURSE 
where  clabfee > 200
or     (cdept = 'PHIL' and cred = 6 );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s22')
    
    #  The following query is equivalent
    stmt = """select *
from COURSE 
where  (cdept = 'PHIL' AND cred = 6)
OR     (cdept = 'PHIL' AND clabfee = 0 );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s23')
    
    #  4J
    #  Select all the information about any 3 credit
    #  course with a labfee less than $100
    #  or greater than $300.
    
    stmt = """select *
from COURSE 
where  cred = 3
and    (clabfee < 100 OR clabfee > 300);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s24')
    
    #  The following query is equivalent
    stmt = """select *
from COURSE 
where  (cred = 3 and clabfee < 100)
or     (cred = 3 and clabfee > 300);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s25')
    
    #  4.11
    #  Display all information about all non-CIS courses
    #  or any course (regardless of the department) which
    #  has a zero labfee and worth 3 credits.
    
    stmt = """select   *
from COURSE 
where    NOT cdept = 'CIS'
or       clabfee = 0
and      cred = 3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s26')
    
    #  The following queries are equivalent
    stmt = """select   *
from COURSE 
where    NOT cdept = 'CIS'
or       (clabfee = 0 AND cred = 3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s27')
    
    stmt = """select   *
from COURSE 
where    (NOT cdept = 'CIS')
or       (clabfee = 0 AND cred = 3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s28')
    
    #  4K
    #  Select all information about any course with a labfee
    #  which is not greater than 100 or any other course, regardless
    #  of its labfee, which is offered by the Theology depart and
    #  is worth six credits.
    
    stmt = """select   *
from COURSE 
where    not clabfee > 100
or       cdept = 'THEO'
and cred = 6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s29')
    
    stmt = """select   *
from COURSE 
where    not clabfee > 100
or       ( cdept = 'THEO' and cred = 6);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s30')
    
    #  The following queries are equivalent
    stmt = """select   *
from COURSE 
where    (not clabfee > 100)
or       ( cdept = 'THEO' and cred = 6);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s31')
    
    #  4.12
    stmt = """select   *
from COURSE 
where    not (clabfee = 0 and cdept = 'CIS');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s32')
    
    #  The following queries are equivalent
    stmt = """select   *
from COURSE 
where    (not clabfee = 0 ) or (not cdept = 'CIS');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s33')
    
    stmt = """select   *
from COURSE 
where    clabfee <> 0 or cdept <> 'CIS';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s34')
    
    #  4L
    #  Select all information about any course except
    #  3 credit philosophy courses.
    
    stmt = """select   *
from COURSE 
where    NOT ( cdept = 'PHIL' and cred = 3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s35')
    
    #  The following queries are equivalent
    stmt = """select   *
from COURSE 
where    cdept <> 'PHIL' OR cred <> 3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s36')
    
    stmt = """select   *
from COURSE 
where    (NOT cdept = 'PHIL') OR ( NOT cred = 3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s37')
    
    #  -------------------------------------------
    #  IN Keyword
    #  -------------------------------------------
    #  4.13
    stmt = """select  cno, cdescp, cred
from COURSE 
where   cred in (2, 6, 9);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s38')
    
    #  4.14
    stmt = """select  cname, cdescp, cdept
from COURSE 
where   cdept not in ('THEO', 'CIS');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s39')
    
    #  The following queries are equivalent
    
    stmt = """select  cname, cdescp, cdept
from COURSE 
where   NOT cdept in ('THEO', 'CIS');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s40')
    
    stmt = """select  cname, cdescp, cdept
from COURSE 
where   not CDEPT ='THEO'
and     not CDEPT = 'CIS';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s41')
    
    stmt = """select  cname, cdescp, cdept
from COURSE 
where   CDEPT <> 'THEO'
and     CDEPT <> 'CIS';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s42')
    
    stmt = """select  cname, cdescp, cdept
from COURSE 
where   NOT ( CDEPT ='THEO' OR  CDEPT = 'CIS');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s43')
    
    #  ------------------------------------------------
    #  BETWEEN KEYWORD
    #  ------------------------------------------------
    
    #  4.15
    stmt = """Select cname, clabfee
from COURSE 
where  clabfee between 100.00 and 200.00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s44')
    
    #  4 M
    
    #  Display all information about any course which has
    #  a labfee equal to any value in the following set of values.
    
    stmt = """select   *
from COURSE 
where    clabfee in ( 12.12, 50.00, 75.00, 90.00, 100.00, 500.00);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s45')
    
    #  4N
    
    stmt = """select   *
from COURSE 
where    clabfee NOT in ( 12.12, 50.00, 75.00, 90.00, 100.00, 500.00);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s46')
    
    #  4N
    stmt = """select   *
from COURSE 
where    NOT clabfee in ( 12.12, 50.00, 75.00, 90.00, 100.00, 500.00);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s47')
    
    #  4O
    stmt = """Select cno, clabfee
from COURSE 
where  clabfee between 50.00 and 400.00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s48')
    
    #  4.16
    stmt = """select cname, clabfee
from COURSE 
where  clabfee not between 100 and 200;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s49')
    
    #  4P
    #  Display the course number and labfee of any course
    #  with a labfee which is less than $50 or greater than $400.
    
    stmt = """select cno, clabfee
from COURSE 
where  clabfee not between 50 and 400;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s50')
    
    #  Between can also identify a range of character string data.
    #  4.17
    stmt = """select cname, clabfee
from COURSE 
where  cname between 'D' and 'DZZZ';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s51')
    
    # 4Q
    stmt = """select cname, clabfee
from COURSE 
where  cname between 'FOR' and 'FORZ';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    #  4.19
    
    stmt = """select cdept, cname, clabfee
from COURSE 
where  cdept in ( 'CIS', 'THEO', 'MGT')
and    clabfee between 50 and 300
and    cred = 3
order by  cdept, cname;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s52')
    
    #  4R
    #  Display the department, course number, and description
    #  for any computer science or theology course with a labfee
    #  which is less than $100 or greater than $400. Sort the
    #  results by course number within the department.
    
    stmt = """select cdept, cno, cdescp
from COURSE 
where  cdept in ( 'CIS', 'THEO')
and    clabfee not between 100 and 400
order by  cdept, cno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s53')
    
    #  4S
    #  Display all information about any member of
    #  the Philosophy or Theology department.
    stmt = """select  *
from STAFF 
where   dept = 'THEO'
OR      dept = 'PHIL';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s54')
    
    #  4T
    #  Display all information about any member of
    #  the Theology department whose salary exceeds $52.
    stmt = """select  *
from STAFF 
where   dept = 'THEO'
and     esalary > 52;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s55')
    
    #  4U
    #  Display the name of any member of whose salary is
    #  greater than or equal to 52 but less that or equal to 1000.
    stmt = """select  ename
from STAFF 
where   esalary BETWEEN  52 and 1000;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s56')
    
    #  4V
    #  Display the name and title of any staff member assigned to
    #  the Theology depart who earns 51 or 54
    stmt = """select  ename, etitle
from STAFF 
where   dept = 'THEO'
and    esalary IN ( 51, 54);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s57')
    
    #  4W
    #  Display the name and salary of any staff member whose
    #  salalry equals one of the following values.
    
    stmt = """select ename, esalary
from STAFF 
where  esalary in ( 51, 53,100,200,25000);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s58')
    
    #  4X
    #  Display the name and salaries of staff members who earn
    #  less than 100 or more than 1000. Sort the result in
    #  ascending sequence by name.
    
    stmt = """select ename, esalary
from STAFF 
where  esalary not between 100 and 1000
order by ename asc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s59')
    
    #  Result should be same as above.
    
    stmt = """select ename, esalary
from STAFF 
where  esalary < 100
or esalary > 1000
order by ename asc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s60')
    
    #  4Y
    #  Display the department id of every department which
    #  employs a staff member whose salary exceeds $5000.
    #  Do not show duplicate department ids.
    
    stmt = """select distinct dept
from STAFF 
where  esalary > 5000;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s61')
    
    _testmgr.testcase_end(desc)

def test005(desc="""Verify the SQL PATTERN MATCHING -- '%', '_' """):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     testA06
    #  Description:        This test verifies the SQL PATTERN MATCHING
    #                      LIKE keyword
    #                      Use of Percent (%) symbol
    #                      Use of Underscore (_) symbol
    #                      Mixing wildcard symbols.
    #                      NOT LIKE
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    # =================== End Test Case Header  ===================
    
    #  ---------------------------------------
    #  Use of Percent (%) symbol
    #  ---------------------------------------
    #  6.1
    stmt = """select cno, cname
from COURSE 
where  cname like 'INTRO%';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s0')
    
    #  6A
    stmt = """select *
from COURSE 
where  CDESCP like 'FOR THE%';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s1')
    
    stmt = """SELECT * FROM COURSE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s2')
    
    #  6.2
    stmt = """select cname
from COURSE 
where  cname like '%CISM';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s3')
    
    #  6B
    stmt = """SELECT CNAME, CDESCP
FROM   COURSE 
WHERE  CDESCP LIKE '%E';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s4')
    
    #  6.3
    stmt = """select cname
from COURSE 
where  cname like '%SC%';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s5')
    
    #  6C
    stmt = """SELECT CNO, CDESCP
FROM   COURSE 
WHERE  CDESCP LIKE '%.%' or CDESCP LIKE '%-%' or CDESCP LIKE '%!%';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s6')
    #  ---------------------------------------
    #  Use of Underscore (_) symbol
    #  ---------------------------------------
    #  6.4
    stmt = """SELECT CNAME, CDEPT
FROM   COURSE 
WHERE  CDEPT LIKE '_H__';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s7')
    
    #  6D
    stmt = """SELECT CNAME, CDEPT
FROM   COURSE 
WHERE  CDEPT LIKE '___';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s8')
    
    #  ----------------------------------------
    #  Mixing WILDCARD symbols
    #  ----------------------------------------
    #  6.5
    stmt = """SELECT CNAME
FROM   COURSE 
WHERE  CNAME LIKE '_A%'
OR     CNAME LIKE '_E%'
OR     CNAME LIKE '_I%'
OR     CNAME LIKE '_O%'
OR     CNAME LIKE '_U%';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s9')
    
    #  6E
    stmt = """SELECT  CNAME, CDESCP
FROM    COURSE 
WHERE   CDESCP LIKE '____THE__A%';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s10')
    
    #  ----------------------------------------
    #  NOT LIKE
    #  ----------------------------------------
    
    #  6.5
    stmt = """SELECT  CNAME
FROM    COURSE 
WHERE   CNAME NOT LIKE '_A%'
AND     CNAME NOT LIKE '_E%'
AND     CNAME NOT LIKE '_I%'
AND     CNAME NOT LIKE '_O%'
AND     CNAME NOT LIKE '_U%';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s11')
    
    #  The following queries are equivalent.
    
    stmt = """SELECT  CNAME
FROM    COURSE 
WHERE   NOT CNAME LIKE '_A%'
AND     NOT CNAME LIKE '_E%'
AND     NOT CNAME LIKE '_I%'
AND     NOT CNAME LIKE '_O%'
AND     NOT CNAME LIKE '_U%';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s12')
    
    stmt = """SELECT CNAME
FROM   COURSE 
WHERE  NOT (CNAME LIKE '_A%'
OR     CNAME LIKE '_E%'
OR     CNAME LIKE '_I%'
OR     CNAME LIKE '_O%'
OR     CNAME LIKE '_U%');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s13')
    
    #  6.6
    stmt = """select cname, cdescp
from COURSE 
where  cname not like '%E'
and    cname not like '%S';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s14')
    
    #  The following queries are equivalent.
    
    stmt = """select cname, cdescp
from COURSE 
where  not cname like '%E'
and    not cname like '%S';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s15')
    
    stmt = """select cname, cdescp
from COURSE 
where  not (cname  like '%E'
or
cname  like '%S');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s16')
    
    #  6G
    stmt = """SELECT *
FROM STAFF 
WHERE ENAME LIKE 'MA%';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s17')
    
    #  6H
    stmt = """SELECT * FROM STAFF 
WHERE ETITLE LIKE '%1'
OR    ETITLE LIKE '%2'
OR    ETITLE LIKE '%3';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s18')
    
    #  6I
    stmt = """SELECT ENAME, ETITLE
FROM   STAFF 
WHERE  ENAME LIKE '%S%'
AND    ETITLE LIKE '%S%';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s19')
    
    #  6J
    
    stmt = """SELECT DISTINCT DEPT
FROM   STAFF 
WHERE  DEPT LIKE '__E%';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s20')
    
    #  6K
    stmt = """SELECT ENAME
FROM   STAFF 
WHERE  ENAME LIKE '____I%'
ORDER BY ENAME;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s21')
    
    _testmgr.testcase_end(desc)

def test006(desc="""Verify the SQL Arithmetic Expressions."""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     testA07
    #  Description:        This test verifies the SQL Arithmetic Expressions
    #                      Floating point numbers
    #                      Calculated Conditions
    #                      Hierarchy of Arithmetic operators
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    # Create LOG file
    
    #  What will be the labfee for each CIS course if the current labfee
    #  is increased by 25.00 ? Show course name, current labfee and new labfee.
    
    #  7.1
    stmt = """select  cname, clabfee, clabfee + 25
from COURSE 
where cdept = 'CIS';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s0')
    
    #  7.2
    stmt = """select  cname, clabfee, clabfee - 25.75
from COURSE 
where cdept = 'CIS';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s1')
    
    #  7.3
    stmt = """select  cname, clabfee, clabfee * 2.375
from COURSE 
where cdept = 'CIS';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s2')
    
    #  7.4
    stmt = """select  cname, cred, cred / 2
from COURSE 
where cdept = 'PHIL ';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s3')
    
    #  7A
    stmt = """select  cno, cred, cred * 2
from COURSE 
where cdept = 'PHIL ';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s4')
    
    #  7B
    stmt = """select cname, cred, cred * 10.5
from COURSE 
where cdept = 'THEO';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s5')
    
    #  7C
    stmt = """select cname,clabfee, clabfee * 0.50
from COURSE 
where  clabfee > 0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s6')
    
    #  7.5
    #  What is the average labfee per credit hour
    #  for courses offered by CIS department?
    stmt = """select cname, clabfee / cred
from COURSE 
where  cdept = 'CIS';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s7')
    
    #  What would be the average labfee per credit hour
    #  for courses offered by CIS department?
    stmt = """select cname, clabfee / cred
from COURSE 
where  cdept = 'CIS';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s8')
    
    #  7.7.1
    #  What would be the average labfee per credit hour
    #  for CIS courses if the labfee was increased by 25.00 ?
    stmt = """select cname, clabfee, cred, (clabfee + 25)/cred
from COURSE 
where  cdept = 'CIS';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s9')
    
    #  7D
    #  For any course with a lab fee less than 200.00, display
    #  its course number and its adjusted labfee which is 35 more than
    #  150% of the current labfee.
    
    stmt = """select cno, clabfee, (clabfee * 1.5) + 35
from COURSE 
where  clabfee > 200.00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s10')
    
    # --------------------------------------------
    # Floating point numbers
    # --------------------------------------------
    # 7.8
    stmt = """Select cname, clabfee, clabfee * 2E0
from COURSE 
where  cname = 'RELATIONAL DATABASE';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """Select cname, clabfee, clabfee * 2E0
from COURSE 
where  cname = 'RELATIONAL DATABASES';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s11')
    
    #  7.9
    #  For each philosophy course, multiply the credit value by
    #  one trillion.
    stmt = """Select cred, cred * 1000000000000
from COURSE 
where  cdept = 'PHIL' order by cred;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s12')
    
    #  --------------------------------------------
    #  Calculated Conditions
    #  --------------------------------------------
    
    #  7.10
    #  Which CIS course have an average labfee per credit hour
    #  value greater than 30
    stmt = """select cname, clabfee / cred
from COURSE 
where  (clabfee / cred ) > 30
and    cdept = 'CIS';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s13')
    
    #  7.11
    #  What would be the labfee for each computer science course
    #  if we increased it by 25 Order the result by the adjusted
    #  labfee value.
    
    stmt = """select  cname, clabfee, clabfee + 25
from COURSE 
where   cdept = 'CIS'
order by 3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s14')
    
    #  7E
    #  Assume all staff members are given a 100 raise. Display
    #  the name and the adjusted salary of every staff member.
    
    stmt = """select ename, esalary + 100
from STAFF;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s15')
    
    #  7F
    #  Assume all staff members are given a 15% raise. Display
    #  the name and the old and adjusted salary of every staff member.
    
    stmt = """select ename, esalary, esalary * 1.5
from STAFF;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s16')
    
    #  7E
    #  Assume salaries of all staff members are decreased by 100.
    #  Display the name and the adjusted salary of every staff member
    #  whose adjusted salary is less than 25,000.
    
    stmt = """select ename, esalary - 100
from STAFF 
where  (esalary - 100) < 25000;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s17')
    
    #  7H
    #  Consider only staff members whose current salary is less than
    #  25,000. Assume this group of staff members are given a salary
    #  increase of 1000. Display their names and adjusted salaries
    #  in descending salary sequence.
    
    stmt = """select ename, esalary + 1000
from STAFF 
where  esalary < 25000
order by 2 desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s18')
    #  ------------------------------------
    #  Hierarchy of Arithmetic operators
    #  ------------------------------------
    stmt = """select cname, 25 + clabfee
from COURSE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s19')
    
    stmt = """select cname, cred * 2
from COURSE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s20')
    
    stmt = """select cname, 25 + clabfee, clabfee * 2.5
from COURSE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s21')
    
    stmt = """select cname, 100 + clabfee, cred -1
from COURSE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s22')
    
    stmt = """select cname, clabfee * cred / 10
from COURSE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s23')
    
    #  result = 117
    stmt = """select 10 + 5 + 2 + 100
from COURSE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s24')
    
    #  result = 100
    stmt = """select 10 * 5 * 2
from COURSE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s25')
    
    #  result = 13
    stmt = """select 10 + 5 - 2
from COURSE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s26')
    
    #  result = 20
    stmt = """select 10 + 5 * 2
from COURSE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s27')
    
    #  result = 4
    stmt = """select 10 / 5 * 2
from COURSE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s28')
    
    #  result = 30
    stmt = """select (10 + 5) * 2
from COURSE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s29')
    
    #  result = 1
    stmt = """select 10 / (5 * 2)
from COURSE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s30')
    
    #  result = 180
    stmt = """select (10 + 5) * (10 + 2)
from COURSE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s31')
    
    #  result = 62
    stmt = """select 10 + 5 * 10 + 2
from COURSE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s32')
    
    #  result = 62
    stmt = """select (10 + 5 * 10) + 2
from COURSE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s33')
    
    #  result = 152
    stmt = """select (10 + 5) * 10 + 2
from COURSE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s34')
    
    _testmgr.testcase_end(desc)

def test007(desc="""Group functions -- AVG, DISTINCT, COUNT, HAVING"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     testA08
    #  Description:        This test verifies the SQL Group functions
    #                      AVG function.
    #                      MIN/MAX function.
    #                      DISTINCT function.
    #                      COUNT function.
    #                      Use of group functions with Arithmetic expressions.
    #                      GROUP BY clause
    #                      HAVING clause
    #                      MULTI-LEVEL GROUPS
    #                      NESTING GROUP FUNCTIONS.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    
    #  ----------------------------------------------
    #  AVG function.
    #  ----------------------------------------------
    
    #  Selects average lab fee which is 110.
    
    stmt = """SELECT AVG(CLABFEE) FROM COURSE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s0')
    
    #  Since average returns only single row
    #  using ORDER BY does not make sense but
    #  including it will not cause error.
    
    stmt = """SELECT AVG(CLABFEE) FROM COURSE ORDER BY 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s1')
    
    #  Using group by with above query so as to get
    #  average lab fee for each department.
    
    stmt = """SELECT AVG(CLABFEE) FROM COURSE GROUP BY CDEPT;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s2')
    
    #  ----------------------------------------------
    #  MIN/MAX function.
    #  ----------------------------------------------
    
    #  What is the minimum and maximum lab fees and
    #  minimum and maximum course numbers?
    #  Note that group function returns the result
    #  of the same data type as that of the column.
    #  The data type returned that of CNO is of type char.
    
    stmt = """SELECT MIN(CLABFEE), MAX(CLABFEE), MIN(CNO), MAX(CNO)
FROM COURSE 
WHERE CDEPT = 'PHIL';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s3')
    
    stmt = """SELECT MIN(CLABFEE), MAX(CLABFEE), MIN(CNO), MAX(CNO)
FROM COURSE 
WHERE CDEPT = 'CIS';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s4')
    
    stmt = """SELECT MIN(CLABFEE), MAX(CLABFEE), MIN(CNO), MAX(CNO)
FROM COURSE 
WHERE CDEPT = 'THEO';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s5')
    
    #  Sum of all the lab fee values for CIS courses.
    stmt = """SELECT SUM(CLABFEE)
FROM   COURSE 
WHERE  CDEPT = 'CIS';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s6')
    
    #  Display the first course name which appears
    #  in the alphabetic sequence.
    stmt = """SELECT MIN(CNAME)
FROM   COURSE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s7')
    
    #  Display the last course name which appears
    #  in the alphabetic sequence.
    stmt = """SELECT MAX(CNAME)
FROM   COURSE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s8')
    
    #  What is the total labfee for the courses offered by
    #  the philosophy department?
    stmt = """SELECT SUM(CLABFEE)
FROM   COURSE 
WHERE  CDEPT ='PHIL';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s9')
    
    #  Display the average, maximum, and minimum course labfees
    #  for those CIS courses which have nonzero labfees.
    stmt = """SELECT AVG(CLABFEE), MAX(CLABFEE), MIN(CLABFEE)
FROM   COURSE 
WHERE  CLABFEE > 0 AND CDEPT = 'CIS';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s10')
    
    #  Result of this query should be same as above.
    stmt = """SELECT AVG(CLABFEE), MAX(CLABFEE), MIN(CLABFEE)
FROM   COURSE 
WHERE  CLABFEE <> 0 AND CDEPT = 'CIS';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s11')
    
    #  ----------------------------------------------
    #  DISTINCT function.
    #  ----------------------------------------------
    #  What is the total of the unique labfee values
    #  for the CIS courses ?
    
    stmt = """SELECT SUM(DISTINCT CLABFEE)
FROM   COURSE 
WHERE  CDEPT ='CIS';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s12')
    #  ----------------------------------------------
    #  COUNT function.
    #  ----------------------------------------------
    #  There are 3 variations of the COUNT function.
    #  1. COUNT(*)      -- a count of selected rows.
    #  2. COUNT(column) -- a count of non-null values
    #                   -- in a selected column.
    #  3. COUNT(DISTINCT column) -- a count of DISTINCT
    #                            -- non-null values
    #                            -- in a selected column.
    
    #  THIS SHOULD RETURN 4.
    stmt = """SELECT COUNT(*) FROM DEPART;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s13')
    
    #  THIS SHOULD RETURN 3 AS ONE COLUMN HAS NULL VALUE.
    stmt = """SELECT COUNT(DCHFNO) FROM DEPART;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s14')
    
    #  THIS SHOULD RETURN 9.
    stmt = """SELECT COUNT(*) FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s15')
    
    #  THIS SHOULD RETURN 8 AS ONE COLUMN HAS NULL VALUE.
    stmt = """SELECT COUNT(DEPT) FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s16')
    
    #  How many theology courses are recorded in the COURSE table?
    stmt = """SELECT COUNT(*)
FROM   COURSE 
WHERE CDEPT = 'THEO';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s17')
    
    #  How many different acedemic departments offer courses?
    stmt = """SELECT COUNT(DISTINCT CDEPT)
FROM COURSE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s18')
    
    #   HOW MANY ROWS ARE THERE IN THE COURSE DEPARMENT?
    stmt = """SELECT COUNT(*) FROM COURSE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s19')
    
    #  Don't consider 0 labfees. How many distinct labfees are
    #  present in the COURSE table?
    stmt = """SELECT COUNT(DISTINCT CLABFEE)
FROM   COURSE 
WHERE  CLABFEE <> 0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s20')
    
    #  Use of group functions with Arithmetic expressions.
    #  Display two values.
    #  The first is the sum of all labfees assuming each
    #  has been increased by 25.
    #  The second is the result of adding 25 to the sum of all
    #  the labfees
    stmt = """SELECT SUM( CLABFEE + 25 ), SUM( CLABFEE ) + 25
FROM   COURSE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s21')
    
    #  New labfees are to be calculated at 50 for each credit.
    #  What would be the average labfee for the courses offered
    #  by the Theology department?
    stmt = """SELECT AVG(CRED * 50)
FROM   COURSE 
WHERE  CDEPT = 'THEO';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s22')
    
    #  GROUP BY clause
    #  For each department which offers courses, determine
    #  the average labfee for courses offered by the department.
    stmt = """SELECT CDEPT, AVG(CLABFEE)
FROM   COURSE 
GROUP BY CDEPT;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s23')
    
    #  This will cause an error as CDEPT should be referenced
    #  in the Group by clause.
    stmt = """SELECT CDEPT, AVG(CLABFEE)
FROM   COURSE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4021')
    
    #  This will cause an error as GROUP BY must reference
    #  a column by name.
    stmt = """SELECT CDEPT, AVG(CLABFEE)
FROM   COURSE 
GROUP BY 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s25')
    
    #  For each department which offer courses, determine the average
    #  labfee of all three-credit courses offered by the department.
    #  Display the output in ascending sequence by the department id.
    stmt = """SELECT CDEPT, AVG(CLABFEE)
FROM   COURSE 
WHERE  CRED = 3
GROUP BY CDEPT
ORDER BY CDEPT ASC;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s26')
    
    #  Sorting the above query result in descending order.
    stmt = """SELECT CDEPT, AVG(CLABFEE)
FROM   COURSE 
WHERE  CRED = 3
GROUP BY CDEPT
ORDER BY CDEPT DESC;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s27')
    
    #  Display the output in ascending sequence by AVG(CLABFEE) .
    stmt = """SELECT CDEPT, AVG(CLABFEE)
FROM   COURSE 
WHERE  CRED = 3
GROUP BY CDEPT
ORDER BY 2 ASC;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s28')
    
    #  Display the output in descending sequence by AVG(CLABFEE) .
    stmt = """SELECT CDEPT, AVG(CLABFEE)
FROM   COURSE 
WHERE  CRED = 3
GROUP BY CDEPT
ORDER BY 2 DESC;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s29')
    
    #  Output should be same without ORDER BY clause.
    stmt = """SELECT CDEPT, AVG(CLABFEE)
FROM   COURSE 
WHERE  CRED = 3
GROUP BY CDEPT;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s30')
    
    #  This is a negative test as ORDER BY should be
    #  last clause in the Select statement.
    stmt = """SELECT CDEPT, AVG(CLABFEE)
FROM   COURSE 
WHERE  CRED = 3
ORDER BY CDEPT ASC
GROUP BY CDEPT;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  For each department which offer courses, display the
    #  department id followed by the total number of credits
    #  offered by that department.
    stmt = """SELECT CDEPT, SUM(CRED)
FROM   COURSE 
GROUP BY CDEPT;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s32')
    
    #  For each department which offer courses, display the
    #  department id and the number of courses it offers.
    #  Sort the result by department id.
    stmt = """SELECT CDEPT, COUNT(CNO)
FROM   COURSE 
GROUP BY CDEPT
ORDER BY CDEPT ASC;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s33')
    
    #  Don't consider the 6 credit courses. For each department
    #  which offer courses, display the department id followed
    #  by the total of the labfees for the courses offered by the
    #  department. Sort the result by the total labfee in the
    #  descending sequence.
    stmt = """SELECT CDEPT, SUM(CLABFEE)
FROM   COURSE 
WHERE  CRED <> 6
GROUP BY CDEPT
ORDER BY 2 DESC;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s34')
    
    #  For each distinct labfee value, determine the total number
    #  of credits for courses having this labfee value. Sort the
    #  result by the labfee in the descending order.
    stmt = """SELECT CLABFEE, SUM(CRED)
FROM   COURSE 
GROUP BY CLABFEE
ORDER BY CLABFEE DESC;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s35')
    
    #  For each department which offers 6 credit courses, display
    #  the average labfee of the 6 credit courses.
    #  SELECT CDEPT, AVG(CLABFEE)
    #  FROM   COURSE
    #  WHERE  CRED = 6
    #  GROUP BY CDEPT;
    
    #  HAVING clause
    #  Display the department id and the average labfee for
    #  any department where that average exceeds $100.
    stmt = """SELECT CDEPT, AVG(CLABFEE)
FROM   COURSE 
GROUP BY CDEPT
HAVING AVG(CLABFEE) > 100;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s36')
    
    #  Boolean operator NOT with HAVING clause.
    #  Display the department id and the average labfee for
    #  any department where that average is less than or equal to $100.
    stmt = """SELECT CDEPT, AVG(CLABFEE)
FROM   COURSE 
GROUP BY CDEPT
HAVING NOT AVG(CLABFEE) > 100;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s37')
    
    #  Display the department id and maximum labfee for any department
    #  which offers a course where the labfee exceeds $300.
    stmt = """SELECT CDEPT, MAX(CLABFEE)
FROM   COURSE 
GROUP BY CDEPT
HAVING MAX(CLABFEE) > 300;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s38')
    
    #  Display the department id and TOTAL NUMBER OF CREDITS
    #  offered by the department if the total exceeds 15;
    stmt = """SELECT CDEPT, SUM(CRED)
FROM   COURSE 
GROUP BY CDEPT
HAVING SUM(CRED) > 15;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s39')
    
    #  Negative test. HAVING can only be applied if the
    #  statement contains GROUP BY clause.
    #  Following statement is without GROUP BY clause.
    stmt = """SELECT CDEPT, AVG(CLABFEE)
FROM   COURSE 
HAVING AVG(CLABFEE) > 100;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4005')
    
    #  Negative test. HAVING clause must immediately follow the
    #  GROUP BY clause.
    #  Following statement has them in the reverse order.
    stmt = """SELECT CDEPT, AVG(CLABFEE)
FROM   COURSE 
HAVING AVG(CLABFEE) > 100
GROUP BY CDEPT;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s41')
    
    #  For every department, except the Theology department, which has
    #  an average labfee over 100, display its department id followed
    #  by its average labfee.
    stmt = """SELECT CDEPT, AVG(CLABFEE)
FROM   COURSE 
WHERE  CDEPT <> 'THEO'
GROUP BY CDEPT
HAVING AVG(CLABFEE) > 100;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s42')
    
    #  RESULT SHOULD BE SAME AS ABOVE.
    stmt = """SELECT CDEPT, AVG(CLABFEE)
FROM   COURSE 
WHERE  NOT CDEPT = 'THEO'
GROUP BY CDEPT
HAVING AVG(CLABFEE) > 100;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s43')
    
    #  MULTI-LEVEL GROUPS
    #  Find the maximum, minimum, and average labfee values
    #  for all courses offered by each department. Within
    #  each department break down this information for each
    #  distinct credit value.
    #  SELECT CDEPT, CRED, MAX(CLABFEE), MIN(CLABFEE), AVG(CLABFEE)
    #  FROM COURSE
    #  GROUP BY CDEPT, CRED;
    
    #  NEGATIVE TEST AS  ONE NON-GROUPING COLUMN IS LEFT OUT
    #  GROUP BY IN THE QUERY.
    stmt = """SELECT CDEPT, CRED, MAX(CLABFEE), MIN(CLABFEE), AVG(CLABFEE)
FROM   COURSE 
GROUP  BY CDEPT;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4005')
    
    #8L Consider only the 3 credit courses. Display the department id
    # and the total labfee for courses offered by each department
    # if the total is less than or equal to 150.
    stmt = """SELECT CDEPT, SUM(CLABFEE)
FROM   COURSE 
WHERE  CRED = 3
GROUP  BY CDEPT
HAVING SUM(CLABFEE) <= 150;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    # 8M Do not consider courses with a labfee over 400.
    #  Display the department id and the maximum labfee
    #  charged by the department if that maximum exceed 175.
    stmt = """SELECT CDEPT, MAX(CLABFEE)
FROM   COURSE 
WHERE  CLABFEE >= 400
GROUP  BY CDEPT
HAVING MAX(CLABFEE) > 175;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s45')
    
    #  8.16 Extend the previous query by retrieving the average,
    #  maximum and minimum labfee values by credit within
    #  a department only for those groups which have a maximum
    #  labfee value greater than zero.
    stmt = """SELECT CDEPT, CRED, AVG(CLABFEE), MAX(CLABFEE), MIN(CLABFEE)
FROM   COURSE 
GROUP BY CDEPT, CRED
HAVING MAX(CLABFEE) > 0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s46')
    
    #  8.16. What is the average department labfee value for those departments
    #  where this average is greater than $100 and the department offers
    #  less than six courses?
    stmt = """SELECT  CDEPT, AVG(CLABFEE), COUNT(CNO)
FROM    COURSE 
GROUP   BY CDEPT
HAVING  AVG(CLABFEE) > 100 AND
COUNT(CNO) < 6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s47')
    
    #  8.17. The following query gives the same result.
    stmt = """SELECT  CDEPT, AVG(CLABFEE), COUNT(CNO)
FROM    COURSE 
GROUP   BY CDEPT
HAVING  AVG(CLABFEE) > 100 AND
COUNT(*) < 6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s48')
    
    #  NESTING GROUP FUNCTIONS.
    #  8.18. Display the smallest average departmental labfee.
    stmt = """SELECT CDEPT, MIN(AVG(CLABFEE))
FROM   COURSE 
GROUP  BY CDEPT;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4009')
    
    #  8N. Consider the total labfees for each department. Display the
    #  largest of these values.
    stmt = """SELECT CDEPT, MAX(SUM(CLABFEE))
FROM   COURSE 
GROUP  BY CDEPT;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4009')
    
    stmt = """SELECT CDEPT, CLABFEE
FROM   COURSE 
GROUP BY CDEPT, CLABFEE
HAVING CLABFEE > 0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s51')
    
    stmt = """SELECT CDEPT, AVG(CLABFEE)
FROM   COURSE 
GROUP BY CDEPT
HAVING CDEPT LIKE '_H__';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s52')
    #  8O. Display the sum and the average of all staff member
    #  salaries. Also display the individual largest and smallest
    #  individual salaries.
    stmt = """SELECT SUM(ESALARY), AVG(ESALARY), MAX(ESALARY), MIN(ESALARY)
FROM   STAFF;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s53')
    
    #  8P. How many staff members are employed by the Theology department?
    stmt = """SELECT COUNT(ENAME)
FROM   STAFF 
WHERE  DEPT = 'THEO';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s54')
    
    #  8Q. How many different kinds of job titles apply to staff members?
    stmt = """SELECT COUNT(DISTINCT ETITLE)
FROM   STAFF;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s55')
    
    #  8R. Asume a total of 5000 is allocated for staff member raises.
    stmt = """Select SUM(esalary) + 5000 from STAFF;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s56')
    
    #  8S
    stmt = """Select dept, avg(esalary) from STAFF group by dept order by dept;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s57')
    #  8T
    stmt = """Select dept, sum(esalary) from STAFF where esalary > 600
group by dept order by 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s58')
    
    _testmgr.testcase_end(desc)

def test008(desc="""Data manipulation statements."""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """drop table MYCOURSE;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE MYCOURSE 
(
CNO     VARCHAR(3)       NOT NULL,
CNAME   VARCHAR(22)      NOT NULL,
CDESCP  VARCHAR(25)      NOT NULL,
CRED    INT,
CLABFEE NUMERIC(5,2),
CDEPT   VARCHAR(4)       NOT NULL
) no partition
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO MYCOURSE VALUES
('C11', 'INTRO TO CS','FOR ROOKIES',3, 100, 'CIS');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO MYCOURSE VALUES
('C22', 'DATA STRUCTURES','VERY USEFUL',3, 50, 'CIS');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO MYCOURSE VALUES
('C33', 'DISCREET MATHEMATICS','ABSOLUTELY NECESSARY',3, 0, 'CIS');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO MYCOURSE VALUES
('C44', 'DIGITAL CIRCUITS','AH HA!',3, 0, 'CIS');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO MYCOURSE VALUES
('C55', 'COMPUTER ARCH.','VON NEUMANN''S MACH.',3, 100, 'CIS');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO MYCOURSE VALUES
('C66', 'RELATIONAL DATABASES','THE ONLY WAY TO GO',3, 500, 'CIS');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO MYCOURSE VALUES
('P11', 'EMPIRICISM','SEE IT-BELIEVE IT',3, 100, 'PHIL');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO MYCOURSE VALUES
('P22', 'RATIONALISM','FOR CIS MAJORS',3, 50, 'PHIL');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO MYCOURSE VALUES
('P33', 'EXISTENTIALISM','FOR CIS MAJORS',3, 200, 'PHIL');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO MYCOURSE VALUES
('P44', 'SOLIPSISM','MY SELF AND I',6, 0, 'PHIL');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO MYCOURSE VALUES
('T11', 'SCHOLASTICISM','FOR THE PIOUS',3, 150, 'THEO');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO MYCOURSE VALUES
('T12', 'FUNDAMENTALISM','FOR THE CAREFREE',3, 90, 'THEO');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO MYCOURSE VALUES
('T33', 'HEDONISM','FOR THE SANE',3, 0, 'THEO');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO MYCOURSE VALUES
('T44', 'COMMUNISM','FOR THE GREEDY',6, 200, 'THEO');"""
    output = _dci.cmdexec(stmt)
    
    stmt = """SELECT * FROM MYCOURSE;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE MYSTAFF 
(
ENAME      VARCHAR(10)    NOT NULL,
ETITLE     VARCHAR(10),
ESALARY    INT,
DEPT       VARCHAR(4)
) no partition;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO MYSTAFF VALUES ('LUKE', 'EVANGLIST3',53 , 'THEO');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO MYSTAFF VALUES ('MARK', 'EVANGLIST2',52 , 'THEO');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO MYSTAFF VALUES ('MATTHEW', 'EVANGLIST1',51 , 'THEO');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO MYSTAFF VALUES ('DICK NIX', 'CROOK',25001 , 'PHIL');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO MYSTAFF VALUES ('HANK KISS', 'JESTER',25000 , 'PHIL');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO MYSTAFF VALUES ('JOHN', 'EVANGLIST4',54 , 'THEO');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO MYSTAFF VALUES ('EUCLID', 'LAB ASSIST',1000 , 'MATH');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO MYSTAFF VALUES ('ARCHIMEDES', 'LAB ASSIST',200 , 'ENG');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO MYSTAFF VALUES ('DA VINCI', 'LAB ASSIST',500 , NULL);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """SELECT * FROM MYSTAFF;"""
    output = _dci.cmdexec(stmt)
    
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     testA15
    #  Description:        This test verifies the SQL Data
    #                      manipulation statements.
    #                      INSERT Statement
    #                      Specifying the column names
    #                      Inserting rows with unknown values.
    #                      UPDATE Statement
    #                      DELETE Statement
    #  Includes:
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    
    # 15.1
    stmt = """INSERT INTO MYCOURSE 
VALUES ('C77', 'INTRODUCTION TO SQL', 'GOOD STUFF!', 3, 150.00, 'CIS');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """SELECT * FROM MYCOURSE WHERE CNO = 'C77';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s0')
    
    # ----------------------------
    # Specifying the column names
    # ----------------------------
    # 15.2
    stmt = """INSERT INTO MYCOURSE (CNO, CNAME, CDESCP, CRED, CLABFEE, CDEPT)
VALUES ('C77', 'INTRODUCTION TO SQL', 'GOOD STUFF!' ,3, 150.00, 'CIS');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """SELECT * FROM MYCOURSE WHERE CNO = 'C77';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s1')
    
    # -----------------------------------
    # Inserting rows with unknown values.
    # -----------------------------------
    # 15.3
    stmt = """INSERT INTO MYCOURSE 
VALUES ('C78', 'EMBEDDED SQL', ' ', NULL, NULL
, 'CIS');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """SELECT * FROM MYCOURSE WHERE CNO = 'C78';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s2')
    
    stmt = """INSERT INTO MYCOURSE (CNO, CNAME, CDESCP, CRED, CLABFEE, CDEPT)
VALUES ('C78', 'EMBEDDED SQL', ' ', NULL, NULL
, 'CIS');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """SELECT * FROM MYCOURSE WHERE CNO = 'C78';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s3')
    
    # 15A
    stmt = """INSERT INTO MYSTAFF 
VALUES ('ALAN', 'LAB ASSIST', 3000, 'CIS');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """SELECT * FROM MYSTAFF WHERE ENAME = 'ALAN';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s4')
    
    # 15B
    stmt = """INSERT INTO MYSTAFF 
VALUES ('GEORGE', ' ', NULL, 'CIS');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """SELECT * FROM MYSTAFF WHERE ENAME = 'GEORGE';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s5')
    
    #  15.5
    
    stmt = """DROP TABLE ciscour;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE ciscour 
(
CISCNO     VARCHAR(3)       NOT NULL,
CISCNAME   VARCHAR(22)      NOT NULL,
CISCRED    INT,
CISCLABFEE NUMERIC(5,2)
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """INSERT INTO ciscour 
SELECT CNO, CNAME, CRED, CLABFEE
FROM   MYCOURSE 
WHERE  CDEPT = 'CIS';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 10)
    
    stmt = """SELECT * FROM ciscour;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s7')
    
    # --------------------------------
    # UPDATE STATEMENT
    # --------------------------------
    # 15.6
    
    stmt = """UPDATE MYCOURSE 
SET    CLABFEE = 175
WHERE  CNO = 'C77';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 2)
    
    stmt = """SELECT * FROM MYCOURSE WHERE CLABFEE = 175;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s8')
    
    stmt = """UPDATE ciscour SET CISCRED = 9;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 10)
    
    stmt = """SELECT * FROM ciscour;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s9')
    
    # 15.7
    stmt = """UPDATE MYCOURSE 
SET    CRED = 6,
CLABFEE = CLABFEE * 1.10,
CDESCP = 'THE LANGUAGE OF SQL'
WHERE CNO LIKE 'C7%';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 4)
    
    stmt = """SELECT * FROM MYCOURSE WHERE CNO LIKE 'C7%';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s10')
    
    # 15.8
    stmt = """UPDATE  ciscour 
SET     CISCLABFEE =
(
SELECT  MAX(CLABFEE)
FROM    MYCOURSE 
WHERE   CDEPT = 'CIS'
)
WHERE   CISCNO LIKE 'C7%';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 4)
    
    stmt = """SELECT * FROM ciscour WHERE CISCNO LIKE 'C7%';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s11')
    
    stmt = """UPDATE  ciscour 
SET     CISCRED = 4
WHERE   CISCLABFEE >
(
SELECT  MIN(ESALARY)
FROM    MYSTAFF 
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 7)
    
    stmt = """SELECT * FROM ciscour WHERE CISCNO LIKE 'C7%';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s12')
    
    # 15C
    stmt = """UPDATE MYSTAFF SET  ESALARY = 4000 WHERE  DEPT = 'CIS';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 2)
    
    stmt = """SELECT * FROM MYSTAFF WHERE DEPT = 'CIS';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s13')
    # --------------------------------
    # DELETE STATEMENT
    # --------------------------------
    
    # 15.9
    stmt = """DELETE FROM MYCOURSE WHERE CNO LIKE 'C7%';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 4)
    
    stmt = """SELECT * FROM MYCOURSE WHERE CNO LIKE 'C7%';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """DELETE FROM ciscour;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 10)
    
    stmt = """SELECT * FROM ciscour;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    # 15C
    stmt = """DELETE FROM MYSTAFF WHERE DEPT = 'CIS';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 2)
    
    stmt = """SELECT * FROM MYSTAFF WHERE DEPT = 'CIS';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    #  15 E
    
    stmt = """DROP TABLE expsive;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE expsive 
(
EXPCNO     VARCHAR(3)       NOT NULL,
EXPCNAME   VARCHAR(22)      NOT NULL,
EXPCLABFEE NUMERIC(5,2),
EXPCDEPT   VARCHAR(4)       NOT NULL
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """INSERT INTO expsive 
SELECT CNO, CNAME, CLABFEE, CDEPT
FROM   MYCOURSE 
WHERE  CLABFEE > 100;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 4)
    
    stmt = """SELECT * FROM expsive;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s15')
    
    stmt = """UPDATE expsive 
SET    EXPCLABFEE = EXPCLABFEE - 50
WHERE  EXPCLABFEE > 400;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """SELECT *
FROM expsive 
WHERE  EXPCLABFEE > 400;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s16')
    
    # 15G
    stmt = """DELETE FROM expsive WHERE EXPCDEPT = 'THEO';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 2)
    
    # 15H
    stmt = """INSERT INTO expsive VALUES( 'X99', ' ', NULL, 'XXX');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """SELECT * FROM expsive WHERE EXPCNO = 'X99';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s17')
    
    # 15I
    stmt = """UPDATE expsive SET EXPCNAME = 'JUNK';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 3)
    
    stmt = """SELECT * FROM expsive;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s18')
    
    # 15J
    stmt = """DELETE FROM expsive;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 3)
    
    stmt = """SELECT * FROM expsive;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    # 15K
    stmt = """DROP TABLE expsive;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """DROP TABLE MYCOURSE;"""
    output = _dci.cmdexec(stmt)
    stmt = """DROP TABLE MYSTAFF;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test009(desc="""NULL, NOT NULL functions."""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     testA16
    #  Description:        This test verifies the SQL NULL, NOT NULL
    #                      Calculating the NULL  values
    #                      Comparing with NULL  values
    #                      Sorting Null values
    #                      IS NULL
    #                      IS NOT NULL
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    
    #  16.1
    #  Any ARITHMETIC exppression will produce a null
    #  value if one or more of its operands is a null value.
    
    stmt = """SELECT PKEY, COLA, COLB, COLA+COLB, COLA - COLB
FROM   NULLTAB;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s0')
    
    #  16.2
    #  The group functions ignore null values i their calculations.
    
    stmt = """SELECT sum(COLA), avg(COLA), MAX(COLA), MIN(COLA)
FROM   NULLTAB;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s1')
    
    stmt = """SELECT sum(COLB), avg(COLB), MAX(COLB), MIN(COLB)
FROM   NULLTAB;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s2')
    
    #  16.3
    stmt = """SELECT COUNT(COLA), COUNT(*)
FROM   NULLTAB;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s3')
    
    #  16.4
    stmt = """SELECT SUM(COLA)+SUM(COLB), SUM(COLA+COLB)
FROM   NULLTAB;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s4')
    
    #  -----------------------------
    #  Comparing with NULL  values
    #  -----------------------------
    #  16.5
    stmt = """SELECT * FROM NULLTAB WHERE COLA = COLB;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s5')
    
    #  16A
    #  Display the average number of dependents and the total
    #  number of dependents for all faculty members together
    #  with the number of faculty members.
    
    stmt = """SELECT COUNT(*), SUM(FNUM_DEP), AVG(FNUM_DEP)
FROM FACULTY;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s6')
    
    #  16B
    #  Display the total of the salary and $250 for each dependent
    #  for all faculty members.
    stmt = """SELECT SUM( FSALARY + (FNUM_DEP * 250))
FROM FACULTY;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s7')
    
    #  16C
    #  Display any row in NULLTAB where the COLA value is
    #  not equal to the COLB value.
    
    stmt = """select * from NULLTAB where COLA <> COLB;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s8')
    
    #  16.6.1
    #  How many staff members are assigned to the Theology department?
    stmt = """select count(*)
from STAFF 
where  dept = 'THEO';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s9')
    
    #  16.6.2
    #  How many staff members are not assigned to the Theology department?
    stmt = """select count(*)
from STAFF 
where  dept <> 'THEO';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s10')
    
    #  Use of 'IS NULL'
    stmt = """select count(*)
from STAFF 
where  dept = 'THEO'
or     dept is null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s11')
    
    #  Three value logic
    #  16.7
    #  Display any row from nulltab where COLA is equal to COLB,
    #  or where COLA is greater than COLC.
    stmt = """SELECT *
FROM   NULLTAB 
WHERE  COLA = COLB
OR     COLA > COLC;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s12')
    
    #  -----------------------------
    #  Sorting Null values
    #  -----------------------------
    #  Display all rows of NULLTAB in ascending sequence by COLA.
    
    stmt = """SELECT PKEY, COLA
FROM   NULLTAB 
ORDER BY COLA;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s13')
    
    #  Dispaly the unique values( including null) found in COLA of NULLTAB.
    
    stmt = """SELECT DISTINCT COLA
FROM   NULLTAB;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s14')
    
    #  16D
    #  Display the name, faculty number, and number of dependents for all
    #  faculty members. Arrange the result in descending sequence by the
    #  number of dependents.
    
    stmt = """SELECT FNAME, FNO, FNUM_DEP
FROM   FACULTY 
ORDER BY FNUM_DEP DESC;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s15')
    
    # - 16.10
    #  Using the NULLTAB table, form groups of COLC values and display
    #  the sum of the COLA values for each group.
    
    stmt = """SELECT SUM(COLA)
FROM   NULLTAB 
GROUP BY COLC;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s16')
    
    #  16E
    #  Display the average salary of faculty members who have the
    #  same number of dependents.
    
    stmt = """select avg(fsalary)
from FACULTY 
group by fnum_dep;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s17')
    
    #  IS NULL
    #  It is possible to explicitly test for the presence of a
    #  null value in a row by using "IS NULL" in a WHERE clause.
    
    #  16.11
    #  Display any row in NULLTAB which has a null value in COLA.
    stmt = """SELECT *
FROM   NULLTAB 
WHERE COLA IS NULL;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s18')
    
    # 16F
    # Display the name, number of dependents, and department numbers
    # of all faculty members for whom it is NOT known whether they have
    # any dependents.
    
    stmt = """SELECT FNAME, FNUM_DEP, FNO
FROM   FACULTY 
WHERE  FNUM_DEP IS NULL;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    #  IS NOT NULL
    stmt = """SELECT SUM(COLA)+SUM(COLB), SUM(COLA+COLB)
FROM   NULLTAB 
WHERE  COLA IS NOT NULL
AND    COLB IS NOT NULL;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s19')
    
    #  16G
    #  Display the name and department of any staff member who is
    #  not assigned to a known department.
    
    stmt = """SELECT ENAME, DEPT
FROM   STAFF 
WHERE  DEPT IS NULL;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s20')
    
    #  16H
    #  For each department, display the department id and the number
    #  of staff members in the department.
    stmt = """select dept, count(*)
from STAFF 
group by dept;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s21')
    
    _testmgr.testcase_end(desc)

def test010(desc="""Join statement"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     testA17
    #  Description:        This test verifies the SQL Join
    #                      statement
    #  Includes:           Displaying a subset of the Join result.
    #                      Join based on Primary Key and Foreign Key values
    #                      Join of 3 tables.
    #                      Theta-Join
    #                      Multiple Join conditions
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    
    #  JOIN
    #  -------------------------------------------
    #  17.1
    # AR 2/7/07 Added order by
    stmt = """select  *
from STAFF, DEPART 
where   STAFF.dept = DEPART.dept order by ename,etitle;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s0')
    
    #  --------------------------------------------
    #  Displaying a subset of the Join result.
    #  --------------------------------------------
    #  17.2
    
    stmt = """select  ename, esalary, STAFF.dept, dbld, droom
from STAFF, DEPART 
where   STAFF.dept = DEPART.dept
and     esalary > 1000;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s1')
    
    #  -------------------------------------------------
    #  Join based on Primary Key and Foreign Key values
    #  ------------------------------------------------
    #  17.3
    stmt = """select cname, clabfee, dchfno
from DEPART, COURSE 
where  clabfee > 175
and    cdept = dept
order by cname;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s2')
    
    # AR Added order by
    #  17.4
    stmt = """select ename, etitle
from DEPART, STAFF 
where  STAFF.dept = DEPART.dept
and    dbld = 'HU' order by ename,etitle;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s3')
    
    #  17.5
    # AR 01/04/07 Added order by
    stmt = """select dbld, droom
from STAFF, DEPART 
where etitle like 'EVANGLIST%'
and   STAFF.dept = DEPART.dept;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s4')
    
    #  17A
    stmt = """select *
from COURSE, DEPART 
where  cdept = dept order by cno,cname,dept;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s5')
    
    #  17B
    # AR 01/04/07 Added order by
    stmt = """select dept, dbld, droom, dchfno, cno, cname, cdescp, cred, clabfee
from COURSE, DEPART 
where  cdept = dept order by dept,dbld,cno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s6')
    
    #  17C
    stmt = """select cname, clabfee, dchfno
from COURSE, DEPART 
where  cdept = dept
and    clabfee > 100 order by clabfee,dchfno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s7')
    
    #  17D
    stmt = """select cno, cname
from DEPART, COURSE 
where  COURSE.cdept = DEPART.dept
and    dchfno = '60'
order by cno desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s8')
    
    # 17E
    stmt = """select ename, esalary
from STAFF, DEPART 
where  STAFF.dept = DEPART.dept
and    dbld = 'SC';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    #  17 F
    
    stmt = """select distinct dbld, droom
from DEPART, STAFF 
where  STAFF.dept = DEPART.dept
and    esalary > 200;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s9')
    
    #  17.6
    stmt = """select  sum(esalary)
from STAFF, DEPART 
where   STAFF.dept = DEPART.dept
and     droom ='100' and dbld = 'HU';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s10')
    
    #  17.7
    stmt = """select   ename, esalary, cno, cred, esalary/cred
from STAFF, COURSE 
where    dept = cdept
order by ename, cno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s11')
    
    #  17.8
    stmt = """select avg(clabfee), avg(esalary)
from COURSE, STAFF 
where  cdept = dept
group by dept;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s12')
    
    #  17G
    stmt = """select max(clabfee), min(clabfee)
from COURSE, DEPART 
where  cdept = dept
and    dbld = 'SC';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s13')
    
    #  17H
    stmt = """select count(*)
from STAFF, DEPART 
where  STAFF.dept = DEPART.dept;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s14')
    
    #  17I
    stmt = """select ename, esalary, clabfee, clabfee - esalary
from STAFF, COURSE 
where  dept = cdept
and    clabfee - esalary >= 52;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s15')
    
    #  17J
    stmt = """select  DEPART.dept, sum(esalary), avg(esalary)
from STAFF, DEPART 
where   STAFF.dept = DEPART.dept
group by DEPART.dept;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s16')
    
    #  17K
    # AR 12/22/06 added order by
    stmt = """select cname, count(*)
from COURSE, STAFF 
where  cdept = dept
group by cname order by cname;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s17')
    
    #  17L
    
    stmt = """select DEPART.dept
from DEPART, STAFF 
where  DEPART.dept = STAFF.dept
group by DEPART.dept
having count(*) >=3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s18')
    
    #  17M
    stmt = """select DEPART.dept, count(*)
from DEPART, STAFF 
where  DEPART.dept = STAFF.dept
group by DEPART.dept
having count(*) >=1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s19')
    
    #  To check if the two give same results.
    stmt = """select DEPART.dept, count(*)
from DEPART, STAFF 
where  DEPART.dept = STAFF.dept
group by DEPART.dept;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s20')
    
    #  -----------------------------------------
    #  Join of 3 tables.
    #  ------------------------------------------
    #  17.9
    #  The following two queries should give the same output.
    
    stmt = """select cno, ename, etitle, dbld, droom
from STAFF, DEPART, COURSE 
where  cdept = STAFF.dept
and    STAFF.dept = DEPART.dept
order by cno, ename;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s21')
    
    stmt = """select cno, ename, etitle, dbld, droom
from STAFF, DEPART, COURSE 
where  cdept = STAFF.dept
and    cdept = DEPART.dept
order by cno, ename;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s22')
    
    #  -----------------------------------------
    #  Cross Product
    #  ------------------------------------------
    #  17.10
    # AR 01/04/07 Added order by
    stmt = """select * from STAFF, DEPART order by STAFF.ename,STAFF.dept,DEPART.dept;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s23')
    
    #  -----------------------------------------
    #  Joining a table by itself.
    #  ------------------------------------------
    #  17.11
    stmt = """select s1.dept, s1.ename, s2.ename
from STAFF s1, STAFF s2
where  s1.dept = s2.dept;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s24')
    
    #  17.12
    stmt = """select s1.dept, s1.ename, s2.ename
from STAFF s1, STAFF s2
where  s1.dept = s2.dept
and    s1.ename < s2.ename;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s25')
    
    stmt = """select s1.dept, s1.ename, s2.ename
from STAFF s1, STAFF s2
where  s1.dept = s2.dept
and    s1.ename > s2.ename;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s26')
    
    #  --------------------------------------------
    #  Theta-Join
    #  --------------------------------------------
    #  17.13
    # AR 12/22/06 added order by
    stmt = """select ename, esalary, cname, clabfee
from STAFF, COURSE 
where  esalary < clabfee order by 1,3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s27')
    
    stmt = """select ename, esalary, cname, clabfee
from STAFF, COURSE 
where  esalary > clabfee;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s28')
    
    #  --------------------------------------------
    #  Multiple Join conditions
    #  --------------------------------------------
    
    stmt = """select STAFF.dept, ename, esalary, cname, clabfee
from STAFF, COURSE 
where  STAFF.dept = cdept
and    esalary < clabfee;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s29')
    
    #  17.15
    stmt = """select *
from DEPART d1, DEPART d2
where  d1.dept = 'MGT'
and    d1.dbld = d2.dbld
and    d1.dept <> d2.dept;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s30')
    #  ------------------------------------------------
    #  17N
    #  Display the faculty number of any faculty member
    #  who chairs a department which offers a 6 credit course.
    stmt = """select dchfno
from DEPART, COURSE 
where  dept = cdept
and    cred = 6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s31')
    
    #  17O
    #  Display the course number, name, and section of
    #  every class1 which is offered on Monday.
    stmt = """select COURSE.cno, cname, sec
from COURSE, CLASS1 
where  CLASS1.cno = COURSE.cno
and    cday = 'MO';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s32')
    
    #  17 P
    #  Display the course number and name of every course
    #  that student 800 is registered for.
    stmt = """select  COURSE.cno, cname
from regist, COURSE 
where  regist.sno = '800'
and    regist.cno = COURSE.cno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s33')
    
    #  17Q
    #  Display all information about any scheduled class1 which
    #  has a labfee less than $100 and is not offered on Friday.
    stmt = """select   CLASS1.cno, sec, cinstrfno, cday, ctime, cbld, croom
from CLASS1, COURSE 
where    CLASS1.cno = COURSE.cno
and      CLASS1.cday <> 'FR'
and      COURSE.clabfee < 100;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s34')
    
    #  17R
    #  Display the student number and date of registration from
    #  all students who registered for at least one course
    #  offered by the Theology department.
    
    stmt = """select sno, reg_date
from regist, COURSE 
where  regist.cno = COURSE.cno
and    cdept = 'THEO';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s35')
    
    #  17S
    #  How many students are registered for all sections
    #  of the EXISTENTIALISM course?
    stmt = """select count(*)
from COURSE, regist 
where  cname = 'EXISTENTIALISM'
and    COURSE.cno =  regist.cno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s36')
    
    #  17T
    #  How many students have registered for all class1es offered
    #  by the philosophy department?
    
    stmt = """SELECT COUNT(*) FROM regist, COURSE 
WHERE regist.CNO = COURSE.CNO AND CDEPT = 'PHIL';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s37')
    
    #  17U
    #  Display the name and number of every faculty member who
    #  teaches a class1 which meets on a Monday or a Friday.
    #  Don't display duplicate rows.
    
    #  The result of following two queries should be same.
    stmt = """select distinct fname, fno
from FACULTY, CLASS1 
where  ( cday = 'MO' OR cday = 'FR')
and    cinstrfno = fno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s38')
    
    stmt = """select distinct fname, fno
from FACULTY, CLASS1 
where  cday in ( 'MO', 'FR')
and    cinstrfno = fno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s39')
    
    #  17V
    #  Display the name of any faculty member who chairs a
    #  department which offers a 6 credit course.
    stmt = """select  fname
from FACULTY, DEPART, COURSE 
where   cred =6
and     dchfno = fno
and     cdept = dept;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s40')
    
    #  17WA
    #  Produce a class1 list for the first section of the EXISTENTIALISM
    #  course. Display the course number, section number, course name,
    #  and faculty number of the instructor followed by the student number
    #  of every student registered for the class1.
    
    stmt = """select   COURSE.cno, cname, CLASS1.sec, cinstrfno, sno
from CLASS1, COURSE, regist 
where    cname = 'EXISTENTIALISM'
and      COURSE.cno = CLASS1.cno
and      CLASS1.cno = regist.cno
and      regist.sec = CLASS1.sec
and      CLASS1.sec = '01' order by sno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s41')
    
    #  17Wb
    #  Modify the above query. For each student, display the
    #  student's name followed by student's number.
    
    stmt = """select   COURSE.cno, cname, CLASS1.sec, cinstrfno, regist.sno, sname
from CLASS1, COURSE, regist , STUDENT 
where    cname = 'EXISTENTIALISM'
and      COURSE.cno = CLASS1.cno
and      CLASS1.cno = regist.cno
and      regist.sec = CLASS1.sec
and      CLASS1.sec = '01'
and      regist.sno = STUDENT.sno order by sname;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s42')
    
    #  17Wc
    #  Modify the above query. Display the faculty's name
    #  instead of faculty number.
    
    stmt = """select   COURSE.cno, cname, CLASS1.sec, fname, regist.sno, sname
from CLASS1, COURSE, regist , STUDENT, FACULTY 
where    cname = 'EXISTENTIALISM'
and      COURSE.cno = CLASS1.cno
and      CLASS1.cno = regist.cno
and      regist.sec = CLASS1.sec
and      CLASS1.sec = '01'
and      regist.sno = STUDENT.sno
and      cinstrfno = fno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s43')
    
    #  17X
    #  The following 3 queries should produce the same result.
    #  a. Join the COURSE and STAFF tables to get an intermediate result.
    #     Then Join this with the DEPART table.
    stmt = """select cno, cname, cdescp, cred, cdept, ename,
etitle, esalary, STAFF.dept,
 DEPART.dept, dbld, droom, dchfno
from COURSE, STAFF, DEPART 
where  cdept = STAFF.dept
and    STAFF.dept = DEPART.dept order by cno,cname,etitle,ename;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s44')
    
    #  b. Join the COURSE and DEPART tables to get an intermediate
    #     result. Then join this with the STAFF table.
    
    stmt = """select cno, cname, cdescp, cred, cdept, ename,
etitle, esalary, STAFF.dept,
 DEPART.dept, dbld, droom, dchfno
from COURSE, STAFF, DEPART 
where  cdept = DEPART.dept
and    cdept = STAFF.dept;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s45')
    
    #  c. Join the STAFF and DEPART tables to get an intermediate
    #     result. Then join this with the COURSE table.
    
    stmt = """select cno, cname, cdescp, cred, cdept, ename,
etitle, esalary, STAFF.dept,
 DEPART.dept, dbld, droom, dchfno
from COURSE, STAFF, DEPART 
where  DEPART.dept = STAFF.dept
and    STAFF.dept = cdept order by cname,etitle,ename;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s46')
    
    #  17Y
    stmt = """Select * from COURSE, FACULTY;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s47')
    
    #  Za
    stmt = """SELECT D1.DEPT, D2.DEPT
FROM DEPART D1, DEPART D2
WHERE D1.DBLD = D2.DBLD AND D1.DEPT < D2.DEPT;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s48')
    
    #  Zb
    stmt = """SELECT S1.ENAME, S1.ESALARY, S2.ENAME, S2.ESALARY, S1.ESALARY - S2.ESALARY
FROM STAFF S1, STAFF S2
WHERE (S1.ESALARY - S2.ESALARY) > 1000;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s49')
    
    # Zc
    stmt = """SELECT S1.ENAME, S1.ESALARY, S2.ENAME, S2.ESALARY, S1.ESALARY - S2.ESALARY
FROM STAFF S1, STAFF S2
WHERE (S1.ESALARY - S2.ESALARY) > 1000
AND S1.DEPT = S2.DEPT;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    # Zc
    stmt = """SELECT S1.ENAME, S1.ESALARY, S2.ENAME, S2.ESALARY, S1.ESALARY - S2.ESALARY
FROM STAFF S1, STAFF S2, DEPART 
WHERE (S1.ESALARY - S2.ESALARY) > 1000
AND S1.DEPT = S2.DEPT
AND DEPART.DEPT = S1.DEPT
AND DBLD = 'HU';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    _testmgr.testcase_end(desc)

def test011(desc="""Outer Join statement"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     testA18
    #  Description:        This test verifies the SQL Outer Join
    #                      statement
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    
    stmt = """Drop table table1;"""
    output = _dci.cmdexec(stmt)
    stmt = """Drop table table2;"""
    output = _dci.cmdexec(stmt)
    stmt = """Drop table table3;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """Create table table1 
( c1 char(1),
c2 int
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into table1 values ('A', 10);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into table1 values ('B', 45);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into table1 values ('C', 45);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into table1 values ('D', 20);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into table1 values ('E', 20);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """Create table table2 
( c1 int,
c2 char(1)
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into table2 values (10, 'S');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into table2 values (20, 'U');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into table2 values (35, 'Z');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """Create table table3 
( c2 int,
c1 char(1)
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into table3 values (10, 'S');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into table3 values (20, 'U');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into table3 values (35, 'Z');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # ------------
    # INNER JOIN
    # ------------
    # select  *
    # from table1 JOIN table2
    # USING   (table1.c1 , table2.c2);
    #
    # select  *
    # from table1 JOIN table2
    # USING   (table1.c2 , table2.c1);
    #
    stmt = """select  *
from table1 JOIN table2 
on      table1.c1 = table2.c2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """select  *
from table1 JOIN table2 
on      table1.c2 = table2.c1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a18exp""", 'a18s3')
    
    stmt = """select  *
from table1 LEFT OUTER JOIN table2 
on      table1.c2 = table2.c1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a18exp""", 'a18s4')
    
    stmt = """select  *
from table1 LEFT OUTER  JOIN table2 
on      table1.c1 = table2.c2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a18exp""", 'a18s5')
    
    stmt = """select  *
from table1 RIGHT OUTER JOIN table2 
on      table1.c2 = table2.c1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a18exp""", 'a18s6')
    
    stmt = """select  *
from table1 RIGHT OUTER  JOIN table2 
on      table1.c1 = table2.c2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a18exp""", 'a18s7')
    
    stmt = """select  *
from table1 LEFT JOIN table2 
on      table1.c2 = table2.c1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a18exp""", 'a18s8')
    
    stmt = """select  *
from table1 LEFT JOIN table2 
on      table1.c1 = table2.c2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a18exp""", 'a18s9')
    
    stmt = """select  *
from table1 RIGHT JOIN table2 
on      table1.c2 = table2.c1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a18exp""", 'a18s10')
    
    stmt = """select  *
from table1 RIGHT JOIN table2 
on      table1.c1 = table2.c2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a18exp""", 'a18s11')
    
    stmt = """select  *
from table1 NATURAL LEFT JOIN table3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a18exp""", 'a18s12')
    
    stmt = """select  *
from table1 NATURAL RIGHT JOIN table3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a18exp""", 'a18s13')
    
    stmt = """select  *
from table1 NATURAL JOIN table3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    #  ----------------------
    #  Nulls and Outer Joins
    #  ----------------------
    
    stmt = """drop table T1;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table T2;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """Create table T1 
( a int,
x char(1)
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """Create table T2 
( b int,
x char(1)
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """Insert into T1 values( 1, 'r');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """Insert into T1 values( 2, 'v');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """Insert into T1 values( 3, NULL);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """Select * from T1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a18exp""", 'a18s16')
    
    stmt = """Insert into T2 values( 7, 'r');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """Insert into T2 values( 8, 's');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """Insert into T2 values( 9, NULL);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """Select * from T2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a18exp""", 'a18s17')
    
    stmt = """Select *
From   T1 INNER JOIN T2 
ON     (T1.x = T2.x);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a18exp""", 'a18s18')
    
    stmt = """Select *
From   T1 LEFT OUTER JOIN T2 
ON     (T1.x = T2.x);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a18exp""", 'a18s19')
    
    stmt = """Select *
From   T1 Right JOIN T2 
ON     (T1.x = T2.x);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a18exp""", 'a18s20')
    
    #  Full Outer Join
    stmt = """Select * From  T1 LEFT OUTER JOIN T2 
ON     (T1.x = T2.x)
UNION
Select * From  T2 LEFT OUTER JOIN T1 
ON     (T1.x = T2.x)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a18exp""", 'a18s21')
    
    #  ---------------------------------------
    #  A NATURAL JOIN has only one copy of the
    #  common column pairs in the result.
    #  ---------------------------------------
    stmt = """Select *
From   T1 NATURAL LEFT OUTER JOIN T2 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a18exp""", 'a18s22')
    
    stmt = """Select *
From   T1 NATURAL RIGHT OUTER JOIN T2 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a18exp""", 'a18s23')
    
    #  ---------------------------------------
    #  The conditional OUTER JOIN has both
    #  of the original columns in the result.
    #  ---------------------------------------
    stmt = """Select *
From   T1 LEFT OUTER JOIN T2 
ON     (T1.x < T2.x);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a18exp""", 'a18s24')
    
    stmt = """Select *
From   T1 LEFT OUTER JOIN T2 
ON     (T1.x > T2.x);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a18exp""", 'a18s25')
    
    #  ----------------
    #  Self OUTER JOINS
    #  ----------------
    
    stmt = """DROP Table Credits;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """Create Table Credits 
( mystudent INTEGER NOT NULL,
 MYCOURSE  VARCHAR(8) NOT NULL
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """Insert into Credits values( 1, 'CS-101');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """Insert into Credits values( 1, 'CS-102');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """Insert into Credits values( 2, 'CS-101');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """Insert into Credits values( 3, 'CS-102');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """Select C1.mystudent, C1.mycourse, C2.mycourse
From   Credits as C1 LEFT OUTER JOIN Credits as C2
On     ((C1.mystudent = C2.mystudent)
AND     (C1.mycourse = 'CS-101')
AND     (C2.mycourse = 'CS-102')
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a18exp""", 'a18s27')
    
    # ---------------------------------------
    # Two or More OUTER JOINs
    # ---------------------------------------
    
    stmt = """drop table T1;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table T2;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table T3;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """Create table T1( a INTEGER NOT NULL,
b INTEGER NOT NULL
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """Insert into T1 values (1, 2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """Create table T2( a INTEGER NOT NULL,
c INTEGER NOT NULL
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """Insert into T2 values (100, 3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """Create table T3( b INTEGER NOT NULL,
c INTEGER NOT NULL
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """Insert into T3 values (2, 3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """Select * from T1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a18exp""", 'a18s29')
    stmt = """Select * from T2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a18exp""", 'a18s30')
    stmt = """Select * from T3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a18exp""", 'a18s31')
    
    stmt = """Select  *
From   (T1 NATURAL LEFT OUTER JOIN T2)
NATURAL LEFT OUTER JOIN T3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a18exp""", 'a18s32')
    stmt = """Select  *
From  (T1 NATURAL LEFT OUTER JOIN T3)
NATURAL LEFT OUTER JOIN T2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a18exp""", 'a18s33')
    stmt = """Select  *
From   (T2 NATURAL LEFT OUTER JOIN T3)
NATURAL LEFT OUTER JOIN T1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a18exp""", 'a18s34')
    stmt = """Select  *
From   (T1 NATURAL RIGHT OUTER JOIN T2)
NATURAL RIGHT OUTER JOIN T3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a18exp""", 'a18s35')
    stmt = """Select  *
From  (T1 NATURAL RIGHT OUTER JOIN T3)
NATURAL RIGHT OUTER JOIN T2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a18exp""", 'a18s36')
    stmt = """Select  *
From   (T2 NATURAL RIGHT OUTER JOIN T3)
NATURAL RIGHT OUTER JOIN T1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a18exp""", 'a18s37')
    
    #  ---------------------------------------
    #  LEFT OUTER JOIN
    #  ---------------------------------------
    stmt = """SELECT *
FROM   STAFF LEFT OUTER JOIN DEPART 
ON     (STAFF.DEPT = DEPART.DEPT);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a18exp""", 'a18s38')
    
    #  18A
    stmt = """SELECT *
FROM   COURSE LEFT OUTER JOIN STAFF 
ON     ( COURSE.CDEPT = STAFF.DEPT);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a18exp""", 'a18s39')
    
    #  ---------------------------------------
    #  NATURAL LEFT OUTER JOIN
    #  ---------------------------------------
    stmt = """SELECT *
FROM   STAFF NATURAL LEFT OUTER JOIN DEPART 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a18exp""", 'a18s40')
    
    stmt = """SELECT *
FROM   COURSE NATURAL LEFT OUTER JOIN STAFF 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a18exp""", 'a18s41')
    
    #  ---------------------------------------
    #  RIGHT OUTER JOIN
    #  ---------------------------------------
    stmt = """SELECT *
FROM   STAFF RIGHT OUTER JOIN DEPART 
ON     (STAFF.DEPT = DEPART.DEPT);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a18exp""", 'a18s42')
    
    #  18b
    stmt = """SELECT *
FROM   DEPART LEFT OUTER JOIN COURSE 
ON     ( DEPART.DEPT = COURSE.CDEPT);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a18exp""", 'a18s43')
    
    #  18C
    stmt = """Select *
FROM   DEPART LEFT OUTER JOIN FACULTY 
ON     (DEPART.DEPT = FACULTY.FDEPT);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a18exp""", 'a18s44')
    
    #  18D
    stmt = """Select *
FROM   FACULTY LEFT OUTER JOIN DEPART 
ON     (FACULTY.FDEPT = DEPART.DEPT);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a18exp""", 'a18s45')
    
    stmt = """Drop table table1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """Drop table table2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """Drop table table3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop table T1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table T2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table T3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test012(desc="""Union statement"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     testA19
    #  Description:        This test verifies the SQL UNION
    #                      statement
    #                      Simple UNION SELECT from base tables.
    #  Includes:           Column names the same.
    #                      Columns of same-length either side of UNION.
    #                      Some nonunique data values.
    #                      No NULL values.
    #                      UNION ALL
    #
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    
    #  UNION
    #  -------------------------------------------
    #  19.1
    
    stmt = """select fname
from FACULTY 
UNION
select ename
from STAFF;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a19exp""", 'a19s0')
    
    #  19.2
    #  This will not have duplicate values in the result.
    stmt = """select dept
from STAFF 
UNION
select fdept
from FACULTY;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a19exp""", 'a19s1')
    
    #  19.2.2
    #  This will have duplicate values in the result.
    stmt = """select dept
from STAFF 
UNION  all
select fdept
from FACULTY;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a19exp""", 'a19s2')
    
    #  19a
    stmt = """select esalary
from STAFF 
UNION
select fsalary
from FACULTY;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a19exp""", 'a19s3')
    
    #  19.3
    
    stmt = """select ename, dept, etitle
from STAFF 
where  dept = 'THEO'
UNION
select fname, fdept, faddr
from FACULTY 
where  fdept = 'THEO'
order by 1 desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a19exp""", 'a19s4')
    
    #  19B
    
    stmt = """select cdept, cred, cdescp
from COURSE 
where  cdept = 'PHIL'
UNION
select fdept, fnum_dep, faddr
from FACULTY 
where  fdept = 'PHIL';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a19exp""", 'a19s5')
    
    #  19.4
    
    stmt = """select 'lower', avg(clabfee)
from COURSE 
where  cno like '_1%'
or     cno like '_2%'
UNION
select 'intermediate', avg(clabfee)
from COURSE 
where  cno like '_3%'
or     cno like '_4%'
UNION
select 'upper', avg(clabfee)
from COURSE 
where  cno like '_5%'
or     cno like '_6%';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a19exp""", 'a19s6')
    
    #  19G
    #  Display the labfee value and number of credits for each CIS
    #  course together with a label of "course". Also display the rows
    #  which contain the salary and number of dependents for each faculty
    #  member from CIS department. Identify the faculty member from
    #  the CIS department. Identify  the faculty rows with atag of "faculty."
    
    stmt = """select 'course', clabfee, cred
from COURSE 
where   cdept = 'CIS'
union
select  'faculty', fsalary, fnum_dep
from FACULTY 
where   fdept = 'CIS';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a19exp""", 'a19s7')
    
    stmt = """select 'expensive', cname, cdept, clabfee
from COURSE 
where   clabfee >= 200
UNION
select 'cheap', cname, cdept, clabfee
from COURSE 
where   clabfee <= 50;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a19exp""", 'a19s8')
    
    #  ---------------------------------------------
    
    stmt = """drop table table1;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table table2;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table table3;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table table4;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table table1 ( col1 int ) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create table table2 ( col2 int ) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create table table3 ( col3 int ) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create table table4 ( col4 int ) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into table1 values(1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into table1 values(2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into table1 values(3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into table1 values(4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into table1 values(5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into table1 values(6);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into table1 values(7);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into table1 values(8);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into table1 values(9);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into table1 values(10);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into table1 values(11);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into table2 values(6);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into table2 values(7);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into table2 values(8);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into table2 values(9);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into table2 values(10);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into table2 values(11);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into table2 values(21);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into table2 values(22);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into table2 values(23);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into table2 values(24);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into table2 values(25);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into table3 values(21);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into table3 values(22);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into table3 values(23);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into table3 values(24);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into table3 values(25);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into table3 values(26);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into table3 values(27);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into table3 values(28);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into table3 values(29);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into table3 values(30);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into table3 values(31);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into table4 values(27);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into table4 values(28);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into table4 values(29);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into table4 values(30);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into table4 values(31);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into table4 values(32);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into table4 values(33);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into table4 values(34);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into table4 values(35);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into table4 values(36);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select * from table1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a19exp""", 'a19s13')
    stmt = """select * from table2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a19exp""", 'a19s14')
    stmt = """select * from table3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a19exp""", 'a19s15')
    
    #  This will only show the unique values.
    stmt = """select *
from table1 
UNION
select *
from table2 
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a19exp""", 'a19s16')
    
    stmt = """select *
from table2 
UNION
select *
from table3 
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a19exp""", 'a19s17')
    
    stmt = """select *
from table1 
UNION
select *
from table3 
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a19exp""", 'a19s18')
    
    stmt = """select *
from table1 
UNION
select *
from table2 
UNION
select *
from table3 
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a19exp""", 'a19s19')
    
    #  This will only show the duplicate values as well.
    
    stmt = """select *
from table1 
UNION all
select *
from table2 
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a19exp""", 'a19s20')
    
    stmt = """select *
from table2 
UNION all
select *
from table3 
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a19exp""", 'a19s21')
    
    stmt = """select *
from table1 
UNION all
select *
from table3 
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a19exp""", 'a19s22')
    
    stmt = """select *
from table1 
UNION all
select *
from table2 
UNION all
select *
from table3 
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a19exp""", 'a19s23')
    
    #  UNION ALL operation is associative.
    #  So the following two queries should give same result.
    
    stmt = """select *
from table1 
UNION
((Select *
from table2 
UNION all
Select *
from table3 
)
UNION all
select *
from table4)
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a19exp""", 'a19s24')
    
    stmt = """select *
from table1 
UNION
(Select *
from table2 
UNION all
(Select *
from table3 
UNION all
select *
from table4 
))
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a19exp""", 'a19s25')
    
    #  Using both Union and Union All
    
    stmt = """select col1 from table1 
union
select col2 from table2     

order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a19exp""", 'a19s26')
    
    stmt = """select col1 from table1 
union all
select col2 from table2     

order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a19exp""", 'a19s27')
    
    #  Using both Union and Union All with order by
    
    stmt = """select col1 from table1 
union
select col2 from table2 
order by col1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a19exp""", 'a19s28')
    
    stmt = """select col1 from table1 
union all
select col2 from table2 
order by col1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a19exp""", 'a19s29')
    #  A Union of table to itself.
    #  Result of following two queries should be same.
    
    stmt = """select col1 from table1 
union
select col1 from table1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a19exp""", 'a19s30')
    
    stmt = """select col1 from table1 
union
select col1 from table1 
order by col1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a19exp""", 'a19s31')
    
    stmt = """select distinct * from table1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a19exp""", 'a19s32')
    
    #  Order of execution test
    #  Order of execution is left to right.
    
    stmt = """select col1 from table1 
union
select col3 from table3 
union
select col2 from table2 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a19exp""", 'a19s33')
    
    stmt = """select col1 from table1 
union
select col2 from table2 
union
select col3 from table3 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a19exp""", 'a19s34')
    
    stmt = """select col1 from table1 
union all
select col2 from table2 
union
select col3 from table3 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a19exp""", 'a19s35')
    
    stmt = """select col1 from table1 
union all
select col2 from table2 
union all
select col3 from table3 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a19exp""", 'a19s36')
    
    #  Order of execution test with order by
    #  Order of execution is left to right.
    
    stmt = """select col1 from table1 
union
select col3 from table3 
union
select col2 from table2 
order by col1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a19exp""", 'a19s37')
    
    stmt = """select col1 from table1 
union
select col2 from table2 
union
select col3 from table3 
order by col1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a19exp""", 'a19s38')
    
    stmt = """select col1 from table1 
union all
select col2 from table2 
union
select col3 from table3 
order by col1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a19exp""", 'a19s39')
    
    stmt = """select col1 from table1 
union all
select col2 from table2 
union all
select col3 from table3 
order by col1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a19exp""", 'a19s40')
    
    # -----------------------------------------
    stmt = """drop table table1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table table2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table table3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test013(desc="""Subqueries containing WHERE clause."""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     testA20
    #  Description:        This test verifies the SQL Subqueries
    #                      Subqueries containing WHERE clause.
    #                      WHERE clause examines Multiple Unknown values.
    #                      The subquery returns multiple values.
    #                      Second Level of Nesting.
    #                      Using NOT IN with Subqueries.
    #                      Subquery returns more than one column.
    #                      ANY and ALL
    #  Includes:
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    
    #  1. Query 1
    #  Display the course number and name of the course(s)
    #  with the highest labfee.
    
    stmt = """Select CNO, CNAME
From COURSE 
Where CLABFEE =
(
Select MAX( CLABFEE )
From   COURSE 
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a20exp""", 'a20s0')
    #  2. 20A
    #  Display the course number, name and department of the
    #  course(s) with the smallest labfee.
    
    stmt = """Select CNO, CNAME, CDEPT
From COURSE 
Where CLABFEE =
(
Select MIN(CLABFEE)
From   COURSE 
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a20exp""", 'a20s1')
    #  Subqueries containing WHERE clause.
    
    #  3. 20.2
    #  Display the course number, name and labfee of the
    #  course(s) with the smallest nonzero labfee.
    
    stmt = """Select CNO, CNAME, CDEPT
From COURSE 
Where CLABFEE =
(
Select MIN(CLABFEE)
From   COURSE 
Where  NOT CLABFEE = 0
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a20exp""", 'a20s2')
    #  4. 20B
    #  Assuming that we know that the highest labfee is $500.00.
    #  Display the course number, name, department, and labfee of
    #  the course(s) having second highest labfee.
    
    stmt = """Select CNO, CNAME, CDEPT, CLABFEE
From COURSE 
Where CLABFEE =
(
Select MAX(CLABFEE)
From   COURSE 
Where  CLABFEE <> 500
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a20exp""", 'a20s3')
    #  5.
    #  The following query should give the same output.
    
    stmt = """Select CNO, CNAME, CDEPT, CLABFEE
From COURSE 
Where CLABFEE =
(
Select MAX(CLABFEE)
From   COURSE 
Where  CLABFEE < 500
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a20exp""", 'a20s4')
    #  6. 20C
    #  Assuming that we know that the lowest labfee is $0.00.
    #  Display the course number, name, department, and labfee of
    #  the course(s) having second lowest labfee.
    
    stmt = """Select CNO, CNAME, CDEPT, CLABFEE
From COURSE 
Where CLABFEE =
(
Select MIN(CLABFEE)
From   COURSE 
Where  CLABFEE <> 0
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a20exp""", 'a20s5')
    #  7.
    #  The following query should give the same output.
    
    stmt = """Select CNO, CNAME, CDEPT, CLABFEE
From COURSE 
Where CLABFEE =
(
Select MIN(CLABFEE)
From   COURSE 
Where  CLABFEE > 0
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a20exp""", 'a20s6')
    #  8. Query 2
    #  Display  the name and title of every staff member
    #  who works in the Humanities building.
    
    stmt = """Select ENAME, ETITLE
From   STAFF 
WHERE  DEPT IN
( Select DEPT
From   DEPART 
Where  DBLD = 'HU'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a20exp""", 'a20s7')
    
    #  The following query will give the same result.
    #  This query uses Join operation.
    
    stmt = """Select ENAME, ETITLE
From   STAFF, DEPART 
WHERE  STAFF.DEPT = DEPART.DEPT
AND    DBLD = 'HU';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a20exp""", 'a20s8')
    
    #  9. (20.3)
    #  Display the course number and name of the
    #  philosophy courses with the highest labfee.
    
    stmt = """Select CNO, CNAME
From   COURSE 
Where  CDEPT = 'PHIL' and
CLABFEE =
( Select MAX(CLABFEE)
From   COURSE 
Where  CDEPT = 'PHIL'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a20exp""", 'a20s9')
    #  10. (20D)
    #  Display the course number and name, department and labfee
    #  of the six credit courses with the highest labfee.
    
    stmt = """Select CNO, CNAME, CDEPT, CLABFEE
From   COURSE 
Where  CRED = 6 and
CLABFEE =
( Select MAX(CLABFEE)
From   COURSE 
Where  CRED = 6
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a20exp""", 'a20s10')
    #  11. (20.4)
    #  Display the course number and name of any non-CIS
    #  course with the smallest labfee of all courses.
    
    stmt = """Select CNO, CNAME, CDEPT, CLABFEE
From   COURSE 
Where  CDEPT <> 'CIS' and
CLABFEE =
( Select MIN(CLABFEE)
From   COURSE 
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a20exp""", 'a20s11')
    #  12.
    #  The follwing query should give the same result as above.
    
    stmt = """Select CNO, CNAME, CDEPT, CLABFEE
From   COURSE 
Where  NOT CDEPT = 'CIS' and
CLABFEE =
( Select MIN(CLABFEE)
From   COURSE 
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a20exp""", 'a20s12')
    #  13. (20.5)
    #  Do not consider CIS courses. Display the course number and
    #  name of the course(s) with the smallest labfee.
    
    stmt = """Select CNO, CNAME, CDEPT, CLABFEE
From   COURSE 
Where  NOT CDEPT = 'CIS' and
CLABFEE =
( Select MIN(CLABFEE)
From   COURSE 
Where  NOT CDEPT = 'CIS'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a20exp""", 'a20s13')
    #  14. (20.6)
    #  Display the course number, name, and labfee of any
    #  course with a labfee which is less than the overall
    #  average labfee.
    
    stmt = """Select CNO, CNAME, CLABFEE
From   COURSE 
Where  CLABFEE <
( Select AVG(CLABFEE)
From   COURSE 
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a20exp""", 'a20s14')
    #  15. (20E)
    #  Display the course number, name, and labfee of any
    #  course with a labfee which is less than the average
    #  labfee of courses offered by the Theology Dapartment.
    
    stmt = """Select CNO, CNAME, CLABFEE
From   COURSE 
Where  CLABFEE <
( Select AVG(CLABFEE)
From   COURSE 
Where  CDEPT = 'THEO'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a20exp""", 'a20s15')
    
    #  16. (20F)
    #  Display all the information about any course with a labfee
    #  which exceeds the maximum labfee for any theology or
    #  philosophy course.
    
    stmt = """Select *
From   COURSE 
Where  CLABFEE >
( Select MAX(CLABFEE)
From   COURSE 
Where  CDEPT = 'THEO' OR CDEPT = 'PHIL'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a20exp""", 'a20s16')
    #  17.
    #  The following should give the same result as above.
    
    stmt = """Select *
From   COURSE 
Where  CLABFEE >
( Select MAX(CLABFEE)
From   COURSE 
Where  CDEPT IN ('THEO','PHIL')
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a20exp""", 'a20s17')
    #  18. (20.7)
    #  Display the course number, name and labfee of any
    #  course which has a labfee greater than or equal to
    #  the salary of any staff member.
    
    stmt = """Select CNO, CNAME, CLABFEE
From   COURSE 
Where  CLABFEE >=
( Select MIN(ESALARY)
From   STAFF 
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a20exp""", 'a20s18')
    #  19. (20G)
    #  Display the employee name and salary of any staff member whose
    #  salary is less than or equal to the maximum course labfee.
    
    stmt = """Select ENAME, ESALARY
From   STAFF 
Where  ESALARY <=
( Select MAX(CLABFEE)
From   COURSE 
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a20exp""", 'a20s19')
    
    #  20. (20H)
    #  Display all the information about any CIS course with a  labfee
    #  which is less than the average salary of staff members assigned
    #  to Theology department.
    
    stmt = """Select *
From   COURSE 
Where  CDEPT = 'CIS' and
CLABFEE <
( Select AVG(ESALARY)
From   STAFF 
Where  DEPT = 'THEO'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a20exp""", 'a20s20')
    
    #  WHERE clause examines Multiple Unknown values.
    #  The subquery returns multiple values.
    #  21. (208)
    #  Display the name and title of every staff member who
    #  works in the Humanities building.
    
    stmt = """SELECT ENAME, ETITLE
FROM   STAFF 
WHERE  DEPT IN
( SELECT DEPT
FROM DEPART 
WHERE DBLD = 'HU');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a20exp""", 'a20s21')
    
    #  24.
    stmt = """SELECT DEPT, DCHFNO
FROM   DEPART 
WHERE  DEPT IN
( SELECT CDEPT
FROM   COURSE 
WHERE  CRED = 6);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a20exp""", 'a20s22')
    
    #  25. (209)
    #  Display the building and room of any acedemic department
    #  which employs a staff member whose title contains the
    #  character string "EVANGLIST".
    
    stmt = """select dbld, droom
from DEPART 
where  dept in
( select dept
from STAFF 
where  etitle like 'EVANGLIST%');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a20exp""", 'a20s23')
    
    #  26. (2010)
    #  Display the faculty number of any faculty member who serves
    #  as chairperson of any department which offers a 6-credit course.
    #  Don't display the duplicate values.
    
    stmt = """SELECT DISTINCT DCHFNO
FROM   DEPART 
WHERE  DEPT IN
( SELECT CDEPT
FROM   COURSE 
WHERE  CRED = 6
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a20exp""", 'a20s24')
    
    #  27. 20J
    #  Display the course number, section number, and building of
    #  any class1 which is offered in the same building where staff
    #  member  Dick Nix works.
    
    #  To check if this query works and ives same answer as
    #  the following two queries.
    
    stmt = """Select CNO, SEC, CBLD
FROM   CLASS1, DEPART 
WHERE  CBLD = DBLD and DEPT IN
( SELECT DEPT
FROM   STAFF 
WHERE  ename = 'DICK NIX');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a20exp""", 'a20s25')
    
    #  28. The following two are correct and should work and give same answer.
    
    stmt = """Select CNO, SEC, CBLD FROM CLASS1 
WHERE  CBLD = ( Select DBLD from DEPART, STAFF 
where  DEPART.DEPT = STAFF.DEPT
and ename = 'DICK NIX');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a20exp""", 'a20s26')
    #  29.
    stmt = """Select CNO, SEC, CBLD FROM CLASS1 
WHERE  CBLD = ( Select DBLD
from DEPART 
where  DEPT =
( Select DEPT
FROM   STAFF 
Where  ename = 'DICK NIX'
)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a20exp""", 'a20s27')
    
    #  30. (20.11)
    #  Display the faculty number and name of any faculty member
    #  who serves as chairperson of and department which offers a
    #  6-credit course.
    
    stmt = """Select FNO, FNAME
FROM   FACULTY 
WHERE  FNO IN
(  SELECT DISTINCT DCHFNO
FROM   DEPART 
WHERE  DEPT IN ( 'THEO', 'PHIL')
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a20exp""", 'a20s28')
    
    #  Second level of Nesting.
    
    #  31.
    #  The following query should also give the same result as above.
    
    stmt = """Select DISTINCT FNO, FNAME
FROM   FACULTY 
WHERE  FNO IN
(  SELECT DCHFNO
FROM   DEPART 
WHERE  DEPT IN
( SELECT CDEPT
FROM   COURSE 
WHERE  CRED = 6
)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a20exp""", 'a20s29')
    #  Using NOT IN with Subqueries.
    
    #  32. (20.12)
    #  Display the name, title, and department id of every staff member
    #  with a department id not found in the department table.
    
    stmt = """Select ename, etitle, dept
from STAFF 
where  dept not in
( Select Dept
from DEPART 
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a20exp""", 'a20s30')
    
    #  33. (20K)
    #  Display the name and  department of any faculty member who is not
    #  teaching a class1 this semester.
    
    stmt = """SELECT FNAME, FDEPT
FROM   FACULTY 
WHERE  FNO NOT IN
( Select CINSTRFNO
FROM   CLASS1 
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a20exp""", 'a20s31')
    
    #  Subquery within HAVING clause
    #  34. (20.13)
    #  For every department which offers courses, display the department
    #  idenifier and the average labfee of courses offered by the department
    #  if that average is  less than the overall average labfee for all courses.
    
    stmt = """SELECT CDEPT, AVG(CLABFEE)
FROM   COURSE 
GROUP BY CDEPT
HAVING AVG(CLABFEE) <
(
SELECT AVG(CLABFEE)
FROM   COURSE 
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a20exp""", 'a20s32')
    
    #  35. (20.14)
    #  For all departments recorded in the DEPART table which
    #  employ staff members, display the department id and the average
    #  salary of staff members in the department if that average is less
    #  than the largest labfee recorded in the course table.
    #  Sort the displayed result by department id.
    
    stmt = """SELECT STAFF.DEPT, AVG(ESALARY)
FROM   STAFF, DEPART 
where  STAFF.DEPT = DEPART.DEPT
GROUP BY STAFF.DEPT
HAVING AVG(ESALARY) <
( SELECT MAX(CLABFEE)
FROM   COURSE 
)
ORDER BY STAFF.DEPT;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a20exp""", 'a20s33')
    #  Subquery returns more than one column.
    
    #  36 (20.15)
    #  Display the department id, other than the Philosophy depart,
    #  of any department which offers a course with the same number of
    #  credits and labfee as any Philosophy course.
    
    stmt = """Select DISTINCT CDEPT
FROM   COURSE 
WHERE  CDEPT<> 'PHIL'
AND    CRED IN
( SELECT CRED
FROM   COURSE 
WHERE CDEPT = 'PHIL'
)
AND    CLABFEE IN
( SELECT CLABFEE
FROM   COURSE 
WHERE CDEPT = 'PHIL'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a20exp""", 'a20s34')
    
    #  37.
    #  This should give the same result as above.
    
    stmt = """Select DISTINCT CDEPT
FROM   COURSE 
WHERE  CDEPT<> 'PHIL'
AND    ( CRED, CLABFEE) IN
( SELECT CRED, CLABFEE
FROM   COURSE 
WHERE CDEPT = 'PHIL'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a20exp""", 'a20s35')
    
    #  ANY and ALL
    #  38. (20.16)
    #  Display the name and title of any staff member employed
    #  by an existing acedemic department.
    
    stmt = """SELECT ENAME, ETITLE
FROM   STAFF 
WHERE  DEPT = ANY
(SELECT DEPT
FROM   DEPART 
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a20exp""", 'a20s36')
    
    #  39. (20.17)
    #  Display the course number, name, and labfee of any course
    #  having a labfee less than all the salaries of staff members.
    
    stmt = """select cno, cname, clabfee
from COURSE 
where  clabfee <  ALL
( select esalary
from STAFF 
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a20exp""", 'a20s37')
    
    #  40. (20.18)
    
    #  Display the name and salary of any staff member whose salary
    #  is greater than or equal to all the courses labfee.
    
    stmt = """SELECT ENAME, ESALARY
FROM   STAFF 
WHERE  ESALARY  >=  ALL
( SELECT CLABFEE
FROM   COURSE 
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a20exp""", 'a20s38')
    
    #  41. (20L)
    
    stmt = """SELECT CNO, CNAME, CLABFEE
FROM   COURSE 
WHERE  CLABFEE > ANY
( SELECT  ESALARY
FROM    STAFF );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a20exp""", 'a20s39')
    
    #  42.
    #  THE ABOVE QUERY WITHOUT USING ">ANY"
    
    stmt = """SELECT CNO, CNAME, CLABFEE
FROM   COURSE 
WHERE  CLABFEE >
( SELECT  MIN(ESALARY)
FROM    STAFF );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a20exp""", 'a20s40')
    
    #  43. (20M)
    #   Display the name and number of dependants for faculty members who
    #   have as many dependents as the number is credits offered for any course.
    
    stmt = """select FNAME, FNUM_DEP
FROM   FACULTY 
WHERE  FNUM_DEP  = ANY
( SELECT CRED
FROM   COURSE 
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a20exp""", 'a20s41')
    
    #  44.
    stmt = """select FNAME, FNUM_DEP
FROM   FACULTY 
WHERE  FNUM_DEP  IN
( SELECT CRED
FROM   COURSE 
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a20exp""", 'a20s42')
    # 45.
    # Display the department id and average labfee of the acedemic department(s)
    # having the highest course labfee.
    
    stmt = """select cdept, avg(clabfee)
from COURSE 
group by cdept
having  AVG(clabfee) =
( select max(clabfee)
from COURSE 
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    #  46. ( 20N)
    #  Display the course number and name for every course that student 800 is registered for.
    
    stmt = """select COURSE.cno, cname
from regist, COURSE 
where  sno = '800'
and    regist.cno = COURSE.cno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a20exp""", 'a20s43')
    
    stmt = """select cno
from COURSE 
where  cno IN
(  select cno
from regist 
where  sno = '800'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a20exp""", 'a20s44')
    
    #  47, (20 O)
    #  Display all information about any scheduled class1 which has a labfee less than $100
    #  and is not offered on a Friday.
    
    stmt = """select *
from CLASS1 
where cday <> 'FR'
and   cno in
( select cno
from COURSE 
where  clabfee < 100
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a20exp""", 'a20s45')
    
    #  48. (20 P)
    #  Display the student number and date of registration for all students who are registered
    #  for at least one course offered by a department located in the science (SC) building.
    
    stmt = """select sno, reg_date
from regist 
where  cno in
( select cno
from COURSE 
where cdept in
(  select cdept
from DEPART 
where dbld = 'SC'
)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a20exp""", 'a20s46')
    
    #  49. (20Q)
    #  Assume that you don't know the highest labfee. Write a select statement which will
    #  display the course number, name, department, and labfee of the courses having the
    #  second highest labfee.
    
    stmt = """select cno, cname, cdept, clabfee
from COURSE 
where  clabfee =
(select max(clabfee)
from COURSE 
where  clabfee <>
(select max(clabfee)
from COURSE 
)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a20exp""", 'a20s47')
    
    #  50. (20R)
    #  Display the name and number of dependents for faculty members who have fewer
    #  dependents than the number of credits offered offered for all corses.
    stmt = """select fname, fnum_dep
from FACULTY 
where fnum_dep <  (select min(cred)
From COURSE 
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a20exp""", 'a20s48')
    
    #  51. (20S)
    stmt = """SELECT C1.CNO, C1.CNAME
FROM   COURSE C1, COURSE C2
GROUP BY C1.CNO, C1.CNAME, C1.CLABFEE
HAVING C1.CLABFEE = MAX(C2.CLABFEE);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a20exp""", 'a20s49')
    
    _testmgr.testcase_end(desc)

def test014(desc="""Correlated Subqueries"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     testA21
    #  Description:        This test verifies the SQL
    #                      Correlated Subqueries
    #                      EXISTS keyword
    #                      NOT EXISTS keyword
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    
    #  21.1
    #  For each department which offers courses, display the
    #  department's identifier followed by the number, name,
    #  and labfee of the department-sponsored course having
    #  the largest labfee.
    
    stmt = """select cdept, cno, cname, clabfee
from COURSE cx
where  clabfee =
( Select    max(clabfee)
From      COURSE 
where     cdept = cx.cdept
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a21exp""", 'a21s0')
    
    #  21A
    #  Display the name, department id, and salary for those
    #  faculty members who have a salary which is greater than
    #  the average faculty salary for their department.
    
    stmt = """select fname, fdept, fsalary
from FACULTY fx
where  fsalary >
( select avg(fsalary)
from FACULTY 
where  fx.fdept = fdept
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a21exp""", 'a21s1')
    
    #  21.2
    #  For each department which offer courses, display the
    #  department id, number, name, and labfee of any department
    #  sponsored course having a labfee which exceeds the salary
    #  of the highest paid  staff member employed by that department.
    
    stmt = """select cdept, cno, cname, clabfee
from COURSE 
where  clabfee >
( Select    max(esalary)
From      STAFF 
where     dept = COURSE.cdept
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a21exp""", 'a21s2')
    #  21B
    #  Display the name and department id for those
    #  faculty members who have a number of dependents greater than
    #  the average number of credits for the courses offered by their department.
    
    stmt = """select fname, fdept
from FACULTY 
where  fNUM_DEP >
( select avg(cred)
from COURSE 
where  fdept = cdept
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a21exp""", 'a21s3')
    
    #  ---------------------------------------------
    #  EXISTS keyword
    #  ---------------------------------------------
    #  21.3
    #  Display the name and title of any staff member assigned to an existing department.
    
    stmt = """select ename, etitle
from STAFF 
where  Exists
(select *
from DEPART 
where  STAFF.dept = DEPART.dept
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a21exp""", 'a21s4')
    #  Following queries will give same results.
    
    stmt = """Select ename, etitle
from STAFF, DEPART 
where STAFF.dept = DEPART.dept;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a21exp""", 'a21s5')
    
    stmt = """Select ename, etitle
from STAFF 
where dept in
( select dept
from DEPART 
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a21exp""", 'a21s6')
    
    #  21C
    #  Display the name and department id of any faculty member
    #  assigned to a department which offers a 6 credit course.
    
    stmt = """select fname, fdept
from FACULTY 
where  EXISTS
( select *
from COURSE 
where  cred = 6
and    fdept = cdept
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a21exp""", 'a21s7')
    
    #  Following queries will give same results.
    
    stmt = """select fname, fdept
from FACULTY 
where  fdept in
( select cdept
from COURSE 
where  cred = 6
and    fdept = cdept
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a21exp""", 'a21s8')
    
    stmt = """select fname, fdept
from FACULTY, COURSE 
where  cred = 6
and    fdept = cdept;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a21exp""", 'a21s9')
    
    #  21.4
    #  Display the course number, name, and labfee of any
    #  course where there exists some staff member whose salary
    #  is less than that labfee.
    
    stmt = """select cno, cname, clabfee
from COURSE 
where  exists
(select *
from STAFF 
where  STAFF.esalary < COURSE.clabfee
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a21exp""", 'a21s10')
    
    #  Correlation variables are explictly defined
    
    stmt = """select cno, cname, clabfee
from COURSE c
where  exists
(select *
from STAFF s
where  s.esalary < c.clabfee
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a21exp""", 'a21s11')
    
    #  21D
    #  The same query using self contained subquery
    stmt = """select cno, cname, clabfee
from COURSE c
where  clabfee >
(select min(esalary)
from STAFF s
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a21exp""", 'a21s12')
    
    #  The same query using Join operation
    stmt = """select distinct cno, cname, clabfee
from COURSE, STAFF 
where  esalary < clabfee;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a21exp""", 'a21s13')
    
    #  NOT EXISTS
    
    #  21.5
    #  Display the name, title, and department id of any staff member
    #  who is not assigned to an existing department.
    stmt = """select ename, etitle, dept
from STAFF 
where  not exists
( select *
from DEPART 
where  DEPART.dept = STAFF.dept
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a21exp""", 'a21s14')
    
    #  Equivalent query using IN
    stmt = """select ename, etitle, dept
from STAFF 
where  dept not in
( select dept
from DEPART 
)
OR DEPT IS NULL;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a21exp""", 'a21s15')
    
    #  21E
    #  Display the name and department id of any faculty member
    #  in a department which doesn't offer a six-credit course.
    stmt = """select fname, fdept
from FACULTY 
where  NOT EXISTS
( select *
from COURSE 
where  cred =6 and fdept = cdept
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a21exp""", 'a21s16')
    
    #  The output of the following query should be same as that of avove.
    stmt = """select fname, fdept
from FACULTY 
where  fdept NOT IN
( select cdept
from COURSE 
where  cred =6
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a21exp""", 'a21s17')
    
    #  21.6
    #  Display the course number, name, and labfee of any course which
    #  has a unique labfee. This is a labfee which doesn't equal any other course.
    
    stmt = """select cno, cname, clabfee
from COURSE cx
where  not exists
( Select *
from COURSE cy
where  cx.clabfee = cy.clabfee
and    cx.cno <> cy.cno
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a21exp""", 'a21s18')
    
    #  An alternative query where subquery is self contained
    
    stmt = """select cno, cname, clabfee
from COURSE 
where  cno not in
( Select ca.cno
from COURSE ca, COURSE cb
where  ca.clabfee = cb.clabfee
and    ca.cno <> cb.cno
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a21exp""", 'a21s19')
    
    #  Outer Join using Correlated Subquery
    
    #  21.7
    #  For every staff member recorded in the STAFF table, display his
    #  name, title, salary, and department id along with all information
    #  about the department to which he is assingned (i.e., the
    #  department's identifier, building, room, and faculty number or
    #  the department chairperson).If the staff member is not assigned to
    #  an existing department, or if the assignment is unknown (null),
    #  display the blanks for department information.
    
    stmt = """select ename, etitle, esalary, STAFF.dept, DEPART.dept , dbld, droom, dchfno
from STAFF, DEPART 
where  STAFF.dept = DEPART.dept
UNION
select ename, etitle, esalary, STAFF.dept , ' ', ' ', ' ', ' '
from STAFF 
where  not exists
( select *
from DEPART 
where DEPART.dept = STAFF.dept
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a21exp""", 'a21s20')
    #  "FOR ALL" i.e "for all the values in a column, there exists ....".
    #  Since FOR ALL doesn't exist we use NOT EXISTS twice.
    
    #  21.8
    #  Are there any students who are taking a course from every department
    #  which offers courses? If so, disply the name of each student.
    #  result should be two rows { MEO DUBAY } { ROCKY BALBOA }
    
    stmt = """select   sname
from STUDENT S
where    not exists
(     select *
from DEPART D
where D.dept in
( select cdept from COURSE)
and not exists
( select *
from regist R, COURSE C, CLASS1 CL
where  R.CNO = C.CNO
and    R.CNO = CL.CNO
and    R.SEC = CL.SEC
and    C.CDEPT = D.DEPT
and    R.SNO = S.SNO
)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a21exp""", 'a21s21')
    
    #  21F
    #  Display the course name, department id, and labfee for
    #  each course which has the largest labfee of all courses in that department.
    
    stmt = """select cname, cdept, clabfee
from COURSE cx
where  clabfee =
(select max(clabfee)
from COURSE cy
where  cx.cdept = cy.cdept
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a21exp""", 'a21s22')
    
    #  21G
    #  Display a list for each department of all class1es offered by the department.
    #  The list contains department id and department building and room location,
    #  followed by course number and names of the courses offered by the deparment,
    #  followed by the section number and day of any class1es on these courses.
    #  If a department does not offer any course , or a course has no class1 offerings,
    #  display spaces in the respective positions.
    
    #  21H
    stmt = """select distinct dept
from STAFF 
where exists
( select *
from DEPART 
where dept = STAFF.dept
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a21exp""", 'a21s23')
    
    #  21I
    stmt = """select distinct dept
from STAFF 
where not exists
( select *
from COURSE 
where cdept = STAFF.dept
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a21exp""", 'a21s24')
    
    _testmgr.testcase_end(desc)

def test015(desc="""Views -- Grouped View, defined as join of tables"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     testA23
    #  Description:        This test verifies the SQL VIEWS
    #                      Specifying column names for a view.
    #                      View defined as a statistical summary.
    #                      Grouped View
    #                      View defined as join of tables.
    #                      View defined on UNION of two tables.
    #                      View defined on another view.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    
    stmt = """Drop View CISC;"""
    output = _dci.cmdexec(stmt)
    stmt = """Drop View vexpcour;"""
    output = _dci.cmdexec(stmt)
    stmt = """Drop VIEW VCSTAT;"""
    output = _dci.cmdexec(stmt)
    stmt = """Drop VIEW VSCD;"""
    output = _dci.cmdexec(stmt)
    stmt = """Drop VIEW VSCD2;"""
    output = _dci.cmdexec(stmt)
    stmt = """Drop View theoemp;"""
    output = _dci.cmdexec(stmt)
    stmt = """Drop View FPAYROLL;"""
    output = _dci.cmdexec(stmt)
    
    # 23.1
    
    stmt = """Create View CISC as
SELECT CNAME, CNO, CRED, CLABFEE, CDESCP
FROM   COURSE 
WHERE  CDEPT = 'CIS';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #  23.2
    stmt = """SELECT *  FROM CISC;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a23exp""", 'a23s7')
    
    #  23A
    #  Create a view called FPAYROLL on the FACULTY table.
    #  The view is to contain the FNAME, FSALARY, FHIRE_DATE, and
    #  FNUM_DEP columns. Then select from this view.
    
    stmt = """SELECT * FROM FACULTY;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a23exp""", 'a23s8')
    
    stmt = """CREATE VIEW FPAYROLL AS
SELECT FNAME, FSALARY, FHIRE_DATE, FNUM_DEP
FROM   FACULTY;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """SELECT * FROM FPAYROLL;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a23exp""", 'a23s9')
    
    #  23.3
    #  For any row in the CISC table with a labfee greater
    #  than or equal to $100, display its name followed by its labfee.
    #  Sort the result by course name in the ascending sequence.
    stmt = """SELECT CNAME, CLABFEE
FROM   CISC 
WHERE  CLABFEE >= 100
ORDER BY CNAME;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a23exp""", 'a23s10')
    
    # Specifying column names for a view
    
    # 23.4
    # Create a view called vexpcour which corresponds
    # to rows from the COURSE table where the labfee exceeds
    # $150. the columns of the view correspond to  CNO, CNAME
    # and CLABFEE. Their respective names in the view are
    # CNUMBER, COURSE_NUMBER, COURSE_NAME AND EXPENSIVE_LABFEE.
    
    stmt = """CREATE VIEW vexpcour (CNUMBER, COURSE_NAME, EXPENSIVE_LABFEE)
AS SELECT CNO, CNAME, CLABFEE
FROM   COURSE 
WHERE  CLABFEE > 150;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """SELECT * FROM vexpcour;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a23exp""", 'a23s11')
    
    #  23.5
    #  Display the course name and the labfee values from the vexpcour
    #  table. Display the result in the course name sequence.
    stmt = """SELECT COURSE_NAME, EXPENSIVE_LABFEE
FROM   vexpcour 
ORDER BY COURSE_NAME;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a23exp""", 'a23s12')
    
    # -------------------------------------------------
    # View defined as a statistical summary
    # THIS IS GROUPED VIEW.
    # -------------------------------------------------
    # 23.6
    # Create a view called VCSTAT which has one row for each
    # department which offers courses. The columns are the department id
    # followed by the sum and the average labfee values for each department.
    # THIS IS GROUPED VIEW.
    
    stmt = """CREATE VIEW VCSTAT 
( CDEPT, SUM_CLABFEE, AVG_CLABFEE) AS
SELECT CDEPT, SUM(CLABFEE), AVG(CLABFEE)
FROM   COURSE 
GROUP BY CDEPT;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #  23.7.1
    #  Display the average labfee for courses offered by the Philosophy
    #  and Theology departments. Sort the result by the average labfee
    #  in the descending sequence.
    
    stmt = """SELECT AVG_CLABFEE
FROM   VCSTAT 
WHERE  CDEPT = 'PHIL' OR CDEPT = 'THEO'
ORDER BY AVG_CLABFEE DESC;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a23exp""", 'a23s13')
    
    #  23.7.2
    #  Display the department id and average labfee for
    #  any course having an average labfee less than $100.00
    
    stmt = """SELECT CDEPT, AVG_CLABFEE
FROM   VCSTAT 
WHERE  AVG_CLABFEE < 100;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a23exp""", 'a23s14')
    
    # -------------------------------------------
    # View defined as join of tables.
    # -------------------------------------------
    # This view is a join of COURSE, STAFF, DEPART tables.
    
    stmt = """CREATE VIEW VSCD AS
SELECT CNO, CNAME, CDESCP, CRED, CLABFEE,
 DEPART.DEPT, DBLD, DROOM,
DCHFNO, ENAME, ETITLE, ESALARY
FROM   COURSE, STAFF, DEPART 
WHERE  CDEPT = DEPART.DEPT
AND    CDEPT = STAFF.DEPT;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # There are 3 identical columns containing the department
    # id values. Therefore we have to code the department id
    # column names so that they are unique. Furthermore,
    # we must explicitly name the view columns because
    # inheritance would imply that two columns would be
    # named DEPT, which is invalid.
    
    stmt = """CREATE VIEW VSCD2 (CNO, CNAME, CDESCP, CRED, CLABFEE,
CDEPT, DDEPT, DBLD, DROOM,
DCHFNO, SDEPT, ENAME, ETITLE, ESALARY)
AS
SELECT CNO, CNAME, CDESCP, CRED, CLABFEE,
CDEPT, DEPART.DEPT, DBLD, DROOM,
DCHFNO, STAFF.DEPT, ENAME, ETITLE, ESALARY
FROM   COURSE, STAFF, DEPART 
WHERE  CDEPT = DEPART.DEPT
AND    CDEPT = STAFF.DEPT;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #  23.9
    #  For any staff member who can tutor philosophy courses, display
    #  his name, the name of the course he can tutor, and his building
    #  and room location. Sort the result by the staff member name.
    
    stmt = """SELECT ename, cname, dbld, droom
FROM   VSCD 
WHERE  DEPT = 'PHIL'
ORDER BY ENAME;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a23exp""", 'a23s15')
    
    # -------------------------------------------
    # View defined on UNION of two tables
    # -------------------------------------------
    # Create a view which contains the name, department, and salary of all
    # staff and faculty members assigned to the Theology department.
    
    stmt = """Create View theoemp 
AS   Select  ENAME, DEPT, ESALARY
From    STAFF 
Where   DEPT = 'THEO'    

UNION    

Select  FNAME, FDEPT, FSALARY
From    FACULTY 
Where   FDEPT = 'THEO';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """SELECT * FROM theoemp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a23exp""", 'a23s16')
    # -------------------------------------------
    
    stmt = """Drop View CISC;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """Drop View vexpcour;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """Drop VIEW VCSTAT;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """Drop VIEW VSCD;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """Drop VIEW VSCD2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """Drop View theoemp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """Drop View FPAYROLL;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test016(desc="""View defined on another view."""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     testA24
    #  Description:        This test verifies the SQL VIEWS
    #                      View defined on another view.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    
    stmt = """Drop View vccisc;"""
    output = _dci.cmdexec(stmt)
    stmt = """DROP VIEW VINSTR;"""
    output = _dci.cmdexec(stmt)
    stmt = """DROP VIEW vttotal;"""
    output = _dci.cmdexec(stmt)
    stmt = """DROP VIEW vtstaff;"""
    output = _dci.cmdexec(stmt)
    stmt = """DROP VIEW vastaff;"""
    output = _dci.cmdexec(stmt)
    
    # 23C
    # Create a view of the FACULTY  table, called VFSAL
    # which present the highest and lowest salaries of the
    # faculty members by department. The columns in the
    # view will have the name of the DEPART,
    # HIGHEST_SALARY, AND LOWEST_SALARY.
    
    stmt = """Create View VFSAL (DEPARTMENT, HIGHEST_SALARY, LOWEST_SALARY)
AS select FDEPT, MAX(FSALARY), MIN(FSALARY)
from FACULTY 
GROUP BY FDEPT;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """SELECT * FROM VFSAL;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a24exp""", 'a24s5')
    stmt = """DROP VIEW VFSAL;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # 23D
    # Create a view on the view FPAYROLL which presents the
    # average faculty salary and average number of dependents.
    # Call the view fages and use the column names
    # FAVG_SAL and FAVG_NUM_DEP.
    
    stmt = """CREATE VIEW FPAYROLL AS
SELECT FNAME, FSALARY, FHIRE_DATE, FNUM_DEP
FROM   FACULTY;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """CREATE VIEW fages ( FAVG_SAL, FAVG_NUM_DEP)
AS   SELECT AVG(FSALARY), AVG(FNUM_DEP)
FROM   FPAYROLL;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """SELECT * FROM fages;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a24exp""", 'a24s6')
    
    stmt = """DROP VIEW  FPAYROLL;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1047')
    
    stmt = """SELECT * FROM fages;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a24exp""", 'a24s8')
    
    # 23G
    # Create a view called vtstaff based on the STAFF table.
    # It is to reflect the ENAME, ESALARY, and ETITLE information
    # for all staff members assigned to the THEO department.
    
    stmt = """Create View vtstaff 
as     SELECT ENAME, ESALARY, ETITLE
FROM   STAFF 
WHERE  DEPT = 'THEO';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """SELECT * FROM vtstaff;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a24exp""", 'a24s9')
    
    # 23H
    # Create a view which presents the average salary of all staff
    # members assigned to each department. The view will be called
    # vastaff and will have the column names of the DEPT and
    # AVERAGE_SALARY.
    
    stmt = """Create View vastaff ( DEPT, AVERAGE_SALARY)
as     SELECT DEPT, AVG(ESALARY)
FROM   STAFF 
GROUP BY DEPT;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """SELECT * FROM vastaff;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a24exp""", 'a24s10')
    
    #  23I
    #  Create a view which is based on the vtstaff VIEW
    #  which presents the total of salaries for all staff members in the THEO department.
    
    stmt = """Create View vttotal (ESALARY) AS
SELECT SUM( ESALARY )
FROM   vtstaff;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """SELECT * FROM vttotal;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a24exp""", 'a24s12')
    
    # 23J
    # Create a view which reflects the join of the FACULTY, COURSE,
    # and CLASS1 tables.
    # The view is to present the name of the faculty member teaching
    # the class1 and name
    # of the course for all courses for which there are class1 offerings.
    # Use the column names of INSTRUCTOR and COURSE_NAME. The view
    # will be called VINSTR.
    
    stmt = """CREATE VIEW VINSTR ( INSTRUCTOR, COURSE_NAME)
AS     Select DISTINCT FNAME, CNAME
from CLASS1, COURSE, FACULTY 
WHERE  CLASS1.CNO = COURSE.CNO
AND FNO = CINSTRFNO;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """SELECT * FROM VINSTR;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a24exp""", 'a24s13b')
    
    # -------------------------------------------
    # View defined on another view
    # -------------------------------------------
    # Create a view called vccisc, which contains rows for
    # CIS courses with a cheap labfee. These are CIS courses
    # with a labfee less than $100. The View should contain
    # CNAME AND CLABFEE columns and inherit those column names.
    
    stmt = """Create View CISC as
SELECT CNAME, CNO, CRED, CLABFEE, CDESCP
FROM   COURSE 
WHERE  CDEPT = 'CIS';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """Create View VCHEAPCISC 
as   Select CNAME, CLABFEE
FROM   CISC 
WHERE  CLABFEE < 100;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """Select * from VCHEAPCISC;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a24exp""", 'a24s14')
    
    # -------------------------------------------
    
    stmt = """Drop View VCHEAPCISC;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """DROP VIEW VINSTR;"""
    output = _dci.cmdexec(stmt)
    stmt = """DROP VIEW vttotal;"""
    output = _dci.cmdexec(stmt)
    stmt = """DROP VIEW vastaff;"""
    output = _dci.cmdexec(stmt)
    stmt = """DROP VIEW vtstaff;"""
    output = _dci.cmdexec(stmt)
    
    #          End of test cases ARKT0004
    _testmgr.testcase_end(desc)

