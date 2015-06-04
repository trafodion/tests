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
    stmt = """CREATE TABLE D1 (i1 INT UNSIGNED
, i2 INT UNSIGNED
, i3 INT UNSIGNED -- , KEY i1
) no partition;"""
    output = _dci.cmdexec(stmt)
    stmt = """CREATE TABLE D2 (i1 INT UNSIGNED
, i2 INT UNSIGNED
, i3 INT UNSIGNED -- , KEY i1
) no partition;"""
    output = _dci.cmdexec(stmt)
    stmt = """CREATE VIEW D3(i1,i2,i3) AS
SELECT i1,i2,i3 FROM D1 ;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO D1 VALUES (  11 ,  21 ,  61);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO D1 VALUES (  31 ,  41 ,  51);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO D1 VALUES (  51 ,  61 ,   1);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO D2 VALUES (  31 ,   10,  88);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO D2 VALUES (  51 ,   8 ,  66);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO D2 VALUES (  71 ,   6 ,  44);"""
    output = _dci.cmdexec(stmt)
    
    # ---------------------
    # Table BRANCH.
    # ---------------------
    
    stmt = """CREATE TABLE BRANCH (
regnum                 PIC 9(2)  not null,
branchnum              PIC 9(2)  not null,
branchname             VARCHAR (14)  not null,
manager                PIC 9(4) not null,
PRIMARY KEY ( regnum, branchnum )
)
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO BRANCH VALUES ( 1, 1,'NEW YORK'     ,  75);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO BRANCH VALUES ( 1, 2,'NEW JERSEY'   , 129);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO BRANCH VALUES ( 2, 1,'CHICAGO'      ,  23);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO BRANCH VALUES ( 2, 2,'HOUSTON'      , 109);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO BRANCH VALUES ( 2, 3,'ST. LOUIS'    , 111);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO BRANCH VALUES ( 3, 1,'DALLAS'       , 321);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO BRANCH VALUES ( 3, 2,'LOS ANGELES'  , 337);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO BRANCH VALUES ( 3, 3,'SAN FRANCISCO',  89);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO BRANCH VALUES ( 4, 1,'TORONTO'      , 178);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO BRANCH VALUES ( 4, 2,'VANCOUVER'    ,  93);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO BRANCH VALUES ( 5, 1,'FRANKFURT'    , 180);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO BRANCH VALUES ( 5, 2,'DUESSELDORF'  ,  39);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO BRANCH VALUES ( 5, 3,'MUENCHEN'     ,  32);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO BRANCH VALUES ( 6, 1,'LONDON'       ,  65);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO BRANCH VALUES (99, 1,'CUPERTINO'    ,  88);"""
    output = _dci.cmdexec(stmt)
    
    # ---------------------
    # Table EMPLOYEE.
    # ---------------------
    
    stmt = """CREATE TABLE EMPLOYEE (
empnum                 PIC 9(4)   not null,
empname                PIC X(18)  not null,
regnum                 PIC 9(2)     not null,
branchnum              PIC 9(2)     not null,
job                    VARCHAR (12)  not null,
age                    PIC 9(2) COMP not null,
salary                 PIC 9(6) COMP not null,
vacation               PIC 9(2) COMP   not null,
PRIMARY KEY (empnum)
)
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO EMPLOYEE VALUES (   1,'ROGER GREEN       ',99, 1,'MANAGER'   ,37, 39500, 2);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO EMPLOYEE VALUES (  23,'JERRY HOWARD      ', 2, 1,'MANAGER'   ,34, 37000,10);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO EMPLOYEE VALUES (  29,'JACK RAYMOND      ', 1, 1,'MANAGER'   ,39, 36000, 1);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO EMPLOYEE VALUES (  32,'THOMAS RUDLOFF    ', 5, 3,'MANAGER'   ,43, 38000, 4);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO EMPLOYEE VALUES (  39,'KLAUS SAFFERT     ', 5, 2,'MANAGER'   ,35, 35000,12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO EMPLOYEE VALUES (  43,'PAUL WINTER       ', 5, 1,'MANAGER'   ,41, 40000, 5);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO EMPLOYEE VALUES (  65,'SUSAN HENDERSON   ', 6, 1,'MANAGER'   ,45, 38000, 9);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO EMPLOYEE VALUES (  72,'GLENN THOMAS      ', 3, 1,'MANAGER'   ,48, 40000,14);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO EMPLOYEE VALUES (  75,'TIM WALKER        ', 1, 1,'MANAGER'   ,29, 32000, 7);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO EMPLOYEE VALUES (  87,'ERIC BROWN        ', 6, 1,'MANAGER'   ,31, 39000,10);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO EMPLOYEE VALUES (  89,'PETER SMITH       ', 3, 3,'MANAGER'   ,36, 37000, 4);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO EMPLOYEE VALUES (  93,'DONALD TAYLOR     ', 4, 2,'MANAGER'   ,31, 33000, 0);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO EMPLOYEE VALUES ( 104,'DAVID STRAND      ', 2, 1,'MANAGER'   ,32, 39000, 2);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO EMPLOYEE VALUES ( 109,'STEVE COOK        ', 2, 2,'MANAGER'   ,39, 38000,15);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO EMPLOYEE VALUES ( 111,'SHERRIE WONG      ', 2, 3,'MANAGER'   ,43, 40000, 0);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO EMPLOYEE VALUES ( 129,'TONY CRAFT        ', 1, 2,'MANAGER'   ,35, 37000, 5);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO EMPLOYEE VALUES ( 178,'LINDA JONES       ', 4, 1,'MANAGER'   ,40, 38000, 8);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO EMPLOYEE VALUES ( 180,'MANFRED CONRAD    ', 5, 1,'MANAGER'   ,30, 32000,14);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO EMPLOYEE VALUES ( 201,'JIM HERMAN        ', 1, 1,'SALESMAN'  ,27, 19000,13);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO EMPLOYEE VALUES ( 202,'LARRY CLARK       ', 1, 1,'SYS.-ANAL.',30, 25000, 7);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO EMPLOYEE VALUES ( 203,'KATHRYN DAY       ', 1, 1,'SECRETARY' ,24, 12000,12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO EMPLOYEE VALUES ( 204,'TOM HALL          ', 1, 1,'SALESMAN'  ,35, 26000, 0);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO EMPLOYEE VALUES ( 205,'GEORGE FORSTER    ', 1, 2,'SALESMAN'  ,39, 30000, 4);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO EMPLOYEE VALUES ( 206,'DAVE FISHER       ', 2, 1,'SALESMAN'  ,32, 25000, 7);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO EMPLOYEE VALUES ( 207,'MARK FOLEY        ', 2, 1,'SALESMAN'  ,27, 23000,10);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO EMPLOYEE VALUES ( 208,'SUE CRAMER        ', 2, 1,'SECRETARY' ,47, 19000, 6);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO EMPLOYEE VALUES ( 209,'SUSAN CHAPMAN     ', 2, 1,'PROGRAMMER',26, 17000, 0);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO EMPLOYEE VALUES ( 210,'RICHARD BARTON    ', 2, 2,'SALESMAN'  ,39, 29000, 7);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO EMPLOYEE VALUES ( 211,'JIMMY SCHNEIDER   ', 2, 3,'SYS.-ANAL.',34, 26000, 0);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO EMPLOYEE VALUES ( 212,'JONATHAN MITCHEL  ', 3, 1,'SALESMAN'  ,39, 32000,15);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO EMPLOYEE VALUES ( 213,'ROBERT WHITE      ', 3, 1,'ENGINEER'  ,29, 30000, 4);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO EMPLOYEE VALUES ( 214,'JULIA KELLY       ', 3, 1,'SECRETARY' ,21, 50000, 1);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO EMPLOYEE VALUES ( 215,'WALTER LANCASTER  ', 3, 2,'SALESMAN'  ,49, 33000,15);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO EMPLOYEE VALUES ( 216,'JOHN JONES        ', 3, 2,'SYS.-ANAL.',31, 30000, 7);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO EMPLOYEE VALUES ( 217,'MARLENE BONNY     ', 3, 3,'SYS.-ANAL.',25, 24000, 9);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO EMPLOYEE VALUES ( 218,'GEORGE FRENCHMAN  ', 3, 3,'SALESMAN'  ,35, 31000, 0);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO EMPLOYEE VALUES ( 219,'DAVID TERRY       ', 3, 3,'PROGRAMMER',37, 27000,12);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO EMPLOYEE VALUES ( 220,'JOHANN HUBER      ', 5, 1,'SYS.-ANAL.',35, 33000,10);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO EMPLOYEE VALUES ( 221,'OTTO SCHNABL      ', 5, 1,'SALESMAN'  ,39, 33000, 1);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO EMPLOYEE VALUES ( 222,'MARTIN SCHAEFER   ', 5, 1,'SALESMAN'  ,32, 31000, 1);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO EMPLOYEE VALUES ( 223,'HERBERT KARAJAN   ', 5, 1,'ENGINEER'  ,33, 29000, 6);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO EMPLOYEE VALUES ( 224,'MARIA JOSEF       ', 5, 1,'SECRETARY' ,19, 18000,10);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO EMPLOYEE VALUES ( 225,'KARL HELMSTED     ', 5, 2,'SALESMAN'  ,34, 32000,11);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO EMPLOYEE VALUES ( 226,'HEIDI WEIGL       ', 5, 2,'SECRETARY' ,55, 22000,14);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO EMPLOYEE VALUES ( 227,'XAVER SEDLMEYER   ', 5, 3,'SYST.-ANAL',30, 30000, 4);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO EMPLOYEE VALUES ( 228,'PETE WELLINGTON   ',99, 1,'SYST.-ANAL',39, 32000, 2);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO EMPLOYEE VALUES ( 229,'GEORGE STRICKER   ',99, 1,'SYST.-ANAL',36, 32222, 6);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO EMPLOYEE VALUES ( 230,'ROCKY LEWIS       ',99, 1,'PROGRAMMER',32, 24000, 0);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO EMPLOYEE VALUES ( 231,'HERB ALBERT       ',99, 1,'SALESMAN'  ,39, 33000, 2);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO EMPLOYEE VALUES ( 232,'THOMAS SPINNER    ',99, 1,'SALESMAN'  ,33, 30000, 5);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO EMPLOYEE VALUES ( 233,'TED MCDONNALDS    ',99, 1,'ENGINEER'  ,29, 29000, 0);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO EMPLOYEE VALUES ( 234,'MARY MILLER       ',99, 1,'SECRETARY' ,22, 16000, 9);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO EMPLOYEE VALUES ( 235,'MIRIAM KING       ',99, 1,'SECRETARY' ,24, 18000,11);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO EMPLOYEE VALUES ( 321,'BILL WINN         ', 3, 1,'MANAGER'   ,28, 32000, 0);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO EMPLOYEE VALUES ( 337,'DAVE CLARK        ', 3, 2,'MANAGER'   ,36, 37000, 2);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO EMPLOYEE VALUES ( 343,'ALAN TERRY        ', 4, 1,'MANAGER'   ,39, 39500, 0);"""
    output = _dci.cmdexec(stmt)
    
    # ---------------------
    # Table FROMSUP.
    # ---------------------
    
    stmt = """CREATE TABLE FROMSUP (
partnum                PIC 9(4)  not null,
suppnum                PIC 9(3)  not null,
partcost               PIC 9(8) COMP not null,
PRIMARY KEY ( partnum, suppnum )
)
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """set param ?p 92000.00;"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO FROMSUP VALUES ( 212,  1, ?p );"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO FROMSUP VALUES ( 244,  1, 87000.00);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO FROMSUP VALUES (1403,  1, 22000.00);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO FROMSUP VALUES (2001,  1,  1500.00);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO FROMSUP VALUES (2002,  1,  1000.00);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO FROMSUP VALUES (2003,  1,   500.00);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO FROMSUP VALUES (2402,  1,  7500.00);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO FROMSUP VALUES (2403,  1,  9600.00);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO FROMSUP VALUES (3102,  1,  4800.00);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO FROMSUP VALUES (3103,  1, 10500.00);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO FROMSUP VALUES (3201,  1,  4800.00);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO FROMSUP VALUES (3302,  1,  2800.00);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO FROMSUP VALUES (4101,  6,  6000.00);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO FROMSUP VALUES (4101, 15,  6000.00);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO FROMSUP VALUES (4102,  6, 10000.00);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO FROMSUP VALUES (4102,  8, 12000.00);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO FROMSUP VALUES (4102, 15, 11000.00);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO FROMSUP VALUES (4103,  6, 20100.00);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO FROMSUP VALUES (4103,  8, 19300.00);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO FROMSUP VALUES (4103, 15, 19500.00);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO FROMSUP VALUES (5101,  8,  5800.00);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO FROMSUP VALUES (5101, 15,  5900.00);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO FROMSUP VALUES (5103,  8,  6200.00);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO FROMSUP VALUES (5103, 15,  6250.00);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO FROMSUP VALUES (5502,  2,  9100.00);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO FROMSUP VALUES (5504,  2,  1600.00);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO FROMSUP VALUES (5504,  6,  1580.00);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO FROMSUP VALUES (5504, 15,  1620.00);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO FROMSUP VALUES (5505, 15, 33000.00);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO FROMSUP VALUES (6201,  1,  5800.00);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO FROMSUP VALUES (6301,  1,  2900.00);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO FROMSUP VALUES (6302,  1,  4300.00);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO FROMSUP VALUES (6401,  2,  1200.00);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO FROMSUP VALUES (6401,  3,  1100.00);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO FROMSUP VALUES (6402,  2,  1100.00);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO FROMSUP VALUES (6402,  3,  1200.00);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO FROMSUP VALUES (6603,  2,  2600.00);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO FROMSUP VALUES (7102, 10,  6000.00);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO FROMSUP VALUES (7301,  1,  2400.00);"""
    output = _dci.cmdexec(stmt)
    
    # ---------------------
    # Table PARTS.
    # ---------------------
    
    stmt = """CREATE TABLE PARTS (
partnum                PIC 9(4)  not null,
partname               PIC X(18) not null,
inventory              PIC S9(3) COMP   not null,
location               PIC X(3)  not null,
price                  PIC 9(6)V9(2) COMP not null,
PRIMARY KEY (partnum)
)
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO PARTS VALUES ( 212,'SYSTEM 192KB CORE ',    7,'J87', 92000.00);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PARTS VALUES ( 244,'SYSTEM 192KB SEMI ',    3,'B78', 87000.00);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PARTS VALUES (1403,'PROC     96KB SEMI',   21,'A21', 22000.00);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PARTS VALUES (2001,'DECIMAL ARITH     ', -100,'X10',  1500.00);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PARTS VALUES (2002,'ENSCRIBE MICRO    ',  200,'X11',  1000.00);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PARTS VALUES (2003,'COBOL MICRO       ',  200,'X12',   500.00);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PARTS VALUES (2402,'MEM MOD 64K MOS   ',  -34,'H87',  7500.00);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PARTS VALUES (2403,'MEM MOD 96K MOS   ',   12,'J88',  9600.00);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PARTS VALUES (3102,'DISC CONT SINGLE  ',   12,'H76',  4800.00);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PARTS VALUES (3103,'DISC CONT DUAL    ',   -4,'H87', 10500.00);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PARTS VALUES (3201,'MAG TAPE CONT 8/16',    6,'J65',  4800.00);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PARTS VALUES (3302,'LINE PRINTER CONT ',    9,'K94',  2800.00);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PARTS VALUES (4101,'DISC 10MB         ',   14,'K87',  8000.00);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PARTS VALUES (4102,'DISC 50MB         ',    9,'K45', 14500.00);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PARTS VALUES (4103,'DISK 160MB        ',    7,'K43', 24500.00);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PARTS VALUES (5101,'MAG TAPE DR 800BPI',    6,'K89',  7400.00);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PARTS VALUES (5103,'MAG TAPE DR 8/16  ',    8,'L98',  8000.00);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PARTS VALUES (5502,'LP  300 LPM       ',    6,'L98', 11500.00);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PARTS VALUES (5504,'LP  900 LPM       ',   -1,'L88', 21000.00);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PARTS VALUES (5505,'LP  1500LPM       ',    0,'L78', 42000.00);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PARTS VALUES (6201,'SYNC CONTROLLER   ',  -16,'A34',  5800.00);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PARTS VALUES (6301,'ASYNC CONTROLLER  ',  -21,'A35',  2900.00);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PARTS VALUES (6302,'ASYNC EXTENSION   ',   34,'A36',  4300.00);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PARTS VALUES (6401,'TERM CRT CHAR     ',   54,'V67',  1500.00);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PARTS VALUES (6402,'TERM CRT PAGE     ',  -32,'V68',  1500.00);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PARTS VALUES (6603,'TERM HARD COPY    ',   40,'V66',  3200.04);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PARTS VALUES (7102,'CABINET LARGE     ',   20,'F76', 68000.05);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO PARTS VALUES (7301,'POWER MODULE      ',   32,'H76',  2400.06);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table T1 ( ch7 varchar(7)
, ch2 char(2)
, nint integer
, nlarge largeint
, nnum9 numeric(9,0)
, nnum4 numeric(4,0)
)  no partition;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table T2 ( ch7 varchar(7)
, ch2 char(2)
, nint integer
, nlarge largeint
)  no partition;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table T3 ( vch15 varchar(15)
, nint integer
, ch3 char(3)
, nlarge largeint
)  no partition;"""
    output = _dci.cmdexec(stmt)
    
    #===================
    # Table UL TDEL
    #===================
    stmt = """create table TU ( vch15 varchar(15)
, nint integer
, ch3 char(3)
, nlarge largeint
)  no partition;"""
    output = _dci.cmdexec(stmt)
    # Make updateable view -- because of limitations of UNIX simulator,
    # insert rows here before making view.
    stmt = """insert into TU values ('1st orig value' ,99 , 'o'   , 1 ) ;"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into TU values ('2nd orig value' ,98 , 'ov'  , 2 ) ;"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into TU values ('3rd orig value' ,97 , 'ovc' , 3 ) ;"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into TU values ('4th orig value' ,96 , 'ov ' , 4 ) ;"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into TU values ('5th orig value' ,95 , 'o  ' , 5 ) ;"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into TU values ('6 is short'     ,97 , 'o'   , 6 ) ;"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into TU values ('7'              ,94 , 'OVC' , 7 ) ;"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into TU values ('8th orig value' ,93 , 'OV'  , 8 ) ;"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into TU values ('9th orig val  ' ,92 , 'O'   , 9 ) ;"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into TU values ('10th val'       ,92 , 'O'   , 9 ) ;"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into TU values ('11th val'       ,92 , 'O'   , 9 ) ;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create view VU as select * from TU;"""
    output = _dci.cmdexec(stmt)
    stmt = """select * from VU ;"""
    output = _dci.cmdexec(stmt)
    #
    # Create table to get rows removed from by delete.
    # drop table TDEL ;
    stmt = """create table TDEL ( vch15      varchar(15)
, rowcounter integer
, ch3        char(3)
, num1dp     Numeric(4,1) signed
)  no partition;"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into TDEL values ('1st orig value' , 1 , 'AAY' , 1.1 ) ;"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into TDEL values ('2nd orig value' , 2 , 'aa'  , 2.1 ) ;"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into TDEL values ('3rd orig value' , 3 , 'BA'  , 3.1 ) ;"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into TDEL values ('4th orig value' , 4 , 'CA'  , 4.1 ) ;"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into TDEL values ('5th orig value' , 5 , 'DA'  , 5.1 ) ;"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into TDEL values ('6 is short'     , 6 , 'EA'  , 6.1 ) ;"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into TDEL values ('7'              , 7 , 'AA'  , 7.1 ) ;"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into TDEL values ('8th orig value' , 8 , 'AB'  , 8.1 ) ;"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into TDEL values ('9th orig val  ' , 9 , 'ZAA' , 9.1 ) ;"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into TDEL values ('10th val'       ,10 , NULL  , 0.0 ) ;"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into TDEL values ('11th val'       ,11 , 'XAA' , 0.1 ) ;"""
    output = _dci.cmdexec(stmt)
    
    #======== table T for testcase a17
    stmt = """create table t (a int)  no partition;"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into t values (20), (10) ;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """Create Table BTA1P001 
(
char0_10         PIC X(4)                not null,
udec0_2000       PIC 9(9)                not null,
ubin0_1000       PIC 9(9) COMP           not null,
varchar0_4       varchar(8)              not null,    

sbin1_100        Numeric(9,0) signed     not null,
char1_4          PIC X(5)                not null,
udec1_10         PIC 9(9)                not null,
ubin1_4          Numeric(9,0) unsigned   not null,    

ubin2_4          PIC 9(2) COMP           not null,
char2_2          PIC X(2)                not null,
udec2_100        PIC 9(2)                not null,    

sbin3_1000       Numeric(5,0) signed     not null,
udec3_2000       PIC 9(5)                not null,
char3_1000       PIC X(240)              not null,
ubin3_uniq       Numeric(5,0) unsigned   not null,    

sbin4_2          Numeric(1,1) signed     not null,
ubin4_4          Numeric(1,1) unsigned   not null,
char4_10         Char(5)                 not null,
sdec4_10         Numeric(1,1) signed     not null,
udec4_2          Numeric(1,1) unsigned   not null,    

sbin5_4          Numeric(4,0) signed     not null,
ubin5_20         Numeric(9,0) unsigned   not null,
udec5_20         Numeric(4,0) unsigned   not null,
varchar5_10      VarChar(9)       not null,  -- Made odd length
-- for odd leading
-- field in key.
sdec5_100        Numeric(18,0) signed    not null,    

udec6_500        PIC 9(4)                not null,
char6_20         PIC X(8)                not null,
ubin6_2          PIC 9(4) COMP           not null,    

sbin7_2          SMALLINT signed         not null,
sdec7_10         Numeric(4,1) signed     not null,
char7_uniq       Char(100)               not null,
udec7_20         Numeric(4,1) unsigned   not null,
ubin7_100        SMALLINT unsigned       not null,    

sbin8_1000       Numeric(18,0) signed    not null,
char8_500        PIC X(100)              not null,
ubin8_2          Numeric(4,1) unsigned   not null,    

char9_uniq       Char(8)                 not null,
udec9_10         Numeric(5,0) unsigned   not null,
sdec9_20         Numeric(5,0) signed     not null,    

ubin10_1000      PIC 9(9) COMP           not null,
char10_20        PIC X(5)                not null,
udec10_2000      PIC 9(9)                not null,    

sdec11_20        Numeric(5,5) signed     not null,
udec11_20        Numeric(5,5) unsigned   not null,
ubin11_2         PIC 9(5) COMP           not null,
char11_4         Char(2)                 not null,    

sbin12_1000      Numeric(9,0) signed     not null,
char12_10        PIC X(2)                not null,
ubin12_10        Numeric(9,0) unsigned   not null,
udec12_1000      PIC 9(9)                not null,    

char13_100       Char(5)                 not null,
sdec13_uniq      Numeric(9,0) signed     not null,
udec13_500       Numeric(9,0) unsigned   not null,    

sbin14_100       Numeric(2,0) signed     not null,
ubin14_2         Numeric(2,0) unsigned   not null,
sdec14_20        Numeric(2,0) signed     not null,
udec14_10        Numeric(2,0) unsigned   not null,
char14_20        Char(2)                 not null,    

sbin15_2         INTEGER signed          not null,
udec15_4         Numeric(9,2) unsigned   not null,
varchar15_uniq   VarChar(9)              not null,
ubin15_uniq      INTEGER unsigned        not null,
sdec15_10        Numeric(9,2) signed     not null,    

sbin16_20        Numeric(9,2) signed     not null,
ubin16_1000      Numeric(9,2) unsigned   not null,
char16_uniq      PIC X(8)                not null,    

sbin17_uniq      Numeric(10,0) signed    not null,
sdec17_20        Numeric(2,0) signed     not null,
char17_100       Char(100)               not null,
udec17_100       Numeric(2,0) unsigned   not null,    

sbin18_uniq      Numeric(18,0) signed    not null,
char18_20        PIC X(100)              not null,
ubin18_20        PIC 9(2) COMP           not null,
udec18_4         PIC 9(2)                not null,    

sbin19_4         LARGEINT signed         not null,
char19_2         Char(8)                 not null,
ubin19_10        SMALLINT unsigned       not null,
udec19_100       Numeric(4,1) signed     not null,
sdec19_1000      Numeric(4,1) unsigned   not null,    

udec20_uniq      PIC 9(9)                not null,
char20_10        PIC X(240)              not null    

, primary key ( varchar5_10, ubin15_uniq , char0_10 )
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """Insert Into BTA1P001 
Values (
'ABAA', 0, 0, 'CAAAAAAA', -- (0)
68, 'AAAA', 1, 0,
2, 'AA', 2,
11, 3, 'BCAAHAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
11,
.0, .2, 'ABAA', .6, .0,
0, 8, 8, 'AA', 68,        -- (5)
6, 'CBAAAAAA', 6,
1, .1,
'BIAAAAABAAAAAAAA', 1.1, 11, 626,
'BCAAHAAAAAAAAAAA', .0,
'BIAAAAAB', 8, 8, 10,
'ABAA', 10, .00011, .00011 , 11,
'CA', 626,
'AB', 6, 12,
'ABAA', 1968, 468, 69, 1, 9, 9,
'CB', 1, .03,
'ABAA', 11, .01, .06, 6.26,
'BIAAAAAB', 1968, 8,
'CBAAAAAAAAAAAAAA', 68, 2369,
'CBAAAAAAAAAAAAAA', 18, 18, 3,
'AAAAAAAA', 1, 1.1, 1.1,20,
'ABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """Insert Into BTA1P001 
Values ('ACAA', 0, 0,
'CAAAAAAA', 9,
'AAAA', 1, 1, 2,
'BA', 2, 6, 3,
'EGAADAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
6, .0, .2,
'ACAA', .2, .0, 1, 9, 9,
'ACAAAAAAI', 9, 6,
'CCAAAAAA', 6, 0, .6,
'EEAAJAACAAAAAAAA', .6, 6, 622,
'EGAADAAAAAAAAAAA', .0,
'EEAAJAAC', 9, 9, 10,
'ACAA', 10, .00006, .00006, 11,
'CA', 622,
'AC', 2, 12,
'AWAA', 3509, 9, 85, 1, 5, 5,
'CC', 0, .02,
'AX', 6, .06, .02, 6.22,
'EEAAJAAC', 3509, 9,
'CWAAAAAAAAAAAAAA', 9, 585,
'CCAAAAAAAAAAAAAA', 18, 18, 2,
'AAAAAAAA', 6, .6, .6, 20,
'ACAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """Insert Into BTA1P001 
Values ('ADAA', 0, 0,
'CAAAAAAA', 63,
'AE', 1, 3, 2,
'AA', 2, 12, 3,
'CGAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
12, .0, .2,
'AD', .8, .0, 3, 3, 3,
'ABC', 63, 6,
'CDAAAAAA', 6, 0, .2,
'CAAADAADAAAAAAAA', 1.2, 12, 198,
'CGAAAAAAAAAAAAAA', .0,
'CAAADAAD', 3, 3, 10,
'AD', 10, .00012, .00012, 11,
'CA', 198,
'AD', 8, 12,
'AX', 2963, 463, 7, 1, 7, 7,
'CD', 0, .00,
'AAAA', 12, .02, .18, 1.98,
'CAAADAAD', 2963, 3,
'CXAAAAAAAAAAAAAA', 63, 4607,
'CDAAAAAAAAAAAAAA', 18, 18, 0,
'AAAAAAAA', 2, 1.2, 1.2, 20,
'ADAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """Insert Into BTA1P001 
Values ('AAAA', 0, 0,
'CAAAAAAA', 23,
'AAAA', 1, 3, 2,
'BE', 2, 8, 3,
'BGAAFAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
8, .0, .2,
'AAAA', .0, .0, 3, 3, 3,
'ABB', 23, 6,
'CAAAAAAA', 6, 0, .8,
'BCAAIAAAAAAAAAAA', .8, 8, 830,
'BGAAFAAAAAAAAAAA', .0,
'BCAAIAAA', 3, 3, 10,
'AAAA', 10, .00008, .00008, 11,
'CA', 830,
'AA', 0, 12,
'AFAA', 3123, 123, 92, 0, 12, 2,
'CA', 0, .00,
'AX', 8, .08, .10, 8.30,
'BCAAIAAA', 3123, 3,
'CFAAAAAAAAAAAAAA', 23, 4292,
'CAAAAAAAAAAAAAAA', 18,18, 0,
'AAAAAAAA', 8, .8, .8, 20,
'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """Insert Into BTA1P001 
Values ('AAAA', 0, 0,
'CAAAAAAA', 18,
'AAAA', 1, 2, 2,
'BB', 2, 10, 3,
'GCAABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
10, .0, .2,
'AAAA', .0, .0, 2, 18, 18,
'AAB', 18, 6,
'CAAAAAAA', 6, 0, .0,
'GIAAEAAAAAAAAAAA', 1.0, 10, 890,
'GCAABAAAAAAAAAAA', .0,
'GIAAEAAA', 8, 18, 10,
'AAAA', 10, .00010, .00010, 11,
'CA', 890,
'AA', 0, 12,
'APAA', 418, 418, 30, 0, 10, 0,
'CA', 0, .02,
'GIAAEAAA', 10, .00, .10, 8.90,
'GIAAEAAA', 418, 18,
'CPAAAAAAAAAAAAAA', 18, 3930,
'CAAAAAAAAAAAAAAA', 18, 18, 2,
'AAAAAAAA', 0, 1.0, 1.0, 20,
'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """Insert Into BTA1P001 
Values ('ABAA', 0, 0,
'CAAAAAAA', 92,
'AAAA', 1, 0, 2,
'AA', 2, 3, 3,
'ACAAGAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
3, .0, .2,
'ABAA', .6, .0, 0, 12, 12,
'ABAAAAAA', 92, 6,
'CBAAAAAA', 6, 1, .3,
'AHAAAAABAAAAAAAA', .3, 3, 546,
'ACAAGAAAAAAAAAAA', .0,
'AHAAAAAB', 2, 12, 10,
'ABAA', 10, .00003, .00003, 11,
'CA', 546,
'AB', 6, 12,
'AVAA', 92, 92, 14, 0, 14, 4,
'CB', 1, .03,
'AHAAAAAB', 3, .03, .06, 5.46,
'AHAAAAAB', 92, 12,
'CVAAAAAAAAAAAAAA', 92, 914,
'CBAAAAAAAAAAAAAA', 18, 18, 3,
'AAAAAAAA', 3, .3, .3, 20,
'ABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """create view VUA1P001 as select * from BTA1P001 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """Create Table BTA1P002 
(
varchar0_4       varchar(8)             ,
char0_20         PIC X(8)               ,    

sbin1_100        Numeric(9,0) signed    ,
char1_4          PIC X(5)               ,
ubin1_4          Numeric(9,0) unsigned  ,    

char2_2          PIC X(2)               ,    

sbin3_1000       Numeric(5,0) signed    ,
char3_1000       PIC X(240)             ,
ubin3_uniq       Numeric(5,0) unsigned not null ,    

sbin4_2          Numeric(1,1) signed    ,
ubin4_4          Numeric(1,1) unsigned  ,
char4_10         Char(5)                ,
sdec4_10         Numeric(1,1) signed    ,
udec4_2          Numeric(1,1) unsigned  ,    

udec5_20         Numeric(4,0) unsigned  ,
varchar5_10      VarChar(8)             ,
sdec5_100        Numeric(18,0) signed   ,    

char6_20         PIC X(8)               ,    

sbin7_2          SMALLINT signed        ,
sdec7_10         Numeric(4,1) signed    ,
char7_uniq       Char(240)              ,
udec7_20         Numeric(4,1) unsigned  ,
ubin7_100        SMALLINT unsigned      ,    

sbin8_1000       Numeric(18,0) signed   ,
char8_500        PIC X(100)             ,
ubin8_2          Numeric(4,1) unsigned  ,    

char9_uniq       Char(8)                ,
udec9_10         Numeric(5,0) unsigned  ,
sdec9_20         Numeric(5,0) signed    ,    

char10_20        PIC X(5)               ,    

sdec11_20        Numeric(5,5) signed    ,
udec11_20        Numeric(5,5) unsigned  ,
char11_4         Char(2)                ,    

sbin12_1000      Numeric(9,0) signed    ,
char12_10        PIC X(2)               ,
ubin12_10        Numeric(9,0) unsigned  ,    

char13_100       Char(5)                ,
sdec13_uniq      Numeric(9,0) signed    ,
udec13_500       Numeric(9,0) unsigned  ,    

sbin14_100       Numeric(2,0) signed    ,
ubin14_2         Numeric(2,0) unsigned  ,
sdec14_20        Numeric(2,0) signed    ,
udec14_10        Numeric(2,0) unsigned  ,
char14_20        Char(2)                ,    

sbin15_2         INTEGER signed         ,
udec15_4         Numeric(9,2) unsigned  ,
varchar15_uniq   VarChar(8)             ,
ubin15_uniq      INTEGER unsigned       ,
sdec15_10        Numeric(9,2) signed    ,    

sbin16_20        Numeric(9,2) signed    ,
ubin16_1000      Numeric(9,2) unsigned  ,
char16_uniq      PIC X(8)               ,    

sbin17_uniq      Numeric(10,0) signed   ,
sdec17_20        Numeric(2,0) signed    ,
char17_100       Char(100)              ,
udec17_100       Numeric(2,0) unsigned  ,    

sbin18_uniq      Numeric(18,0) signed   ,
char18_20        PIC X(100)             ,    

sbin19_4         LARGEINT signed        ,
char19_2         Char(8)                ,
ubin19_10        SMALLINT unsigned      ,
udec19_100       Numeric(4,1) signed    ,
sdec19_1000      Numeric(4,1) unsigned  ,    

char20_10        PIC X(240)    

, primary key ( ubin3_uniq DESC )
)
-- audit
-- extent (1700,64)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """Insert Into BTA1P002 
Values ('DAAAAAAA',
'DDAAAAAA', 24,
'BA   ', 0,
'BA', 1,
'AHAAEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
1, .1, .3,
'AD   ', .3, .1, 4,
'BDAAAAAA', 24,
'DDAAAAAA', 1, .1,
'AHAALAADAAAAAAAA                                                ',
.1, 1, 703,
'AHAAEAAAAAAAAAAA                                                ',
.1,
'AHAALAAD', 4, 4,
'BD   ', .00001, .00001,
'DA', 703,
'BD', 3,
'BD   ', 2724, 224, 6, 0, 6, 6,
'DD', 1, .01,
'AHAALAAD', 1, .01, .03, 7.03,
'AHAALAAD', 2724, 4,
'DDAAAAAAAAAAAAAA                                                ',
24, 4806,
'DDAAAAAAAAAAAAAA                                                ',
1,
'BAAAAAAA', 1, .1, .1,
'ADAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """Insert Into BTA1P002 
Values ('BAAAAAAA',
'BBAAAAAA', 78,
'BA   ', 2,
'BA', 0,
'GFAADAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
3000, .1, .1,
'AB   ', .1, .1, 18,
'BBAAAAAA', 78,
'BBAAAAAA', 0, .0,
'GFAALAABAAAAAAAA                                                ',
.0, 0, 261,
'GFAADAAAAAAAAAAA                                                ',
.1,
'GFAALAAB', 8, 18,
'BB   ', .00000, .00000,
'BA', 261,
'BB', 1,
'BL   ', 4178, 178, 28, 0, 8, 8,
'BB', 0, .00,
'GFAALAAB', 3000, .00, .01, 2.61,
'GFAALAAB', 4178, 18,
'BLAAAAAAAAAAAAAA                                                ',
78, 428,
'BBAAAAAAAAAAAAAA                                                ',
0,
'BAAAAAAA', 0, .0, .0,
'ABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """Insert Into BTA1P002 
Values ('CAAAAAAA',
'CBAAAAAA', 46,
'AA   ', 2,
'AA', 500,
'BGAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
1500, .0, .2,
'AB   ', .6, .0, 6,
'ABAAAAAA', 46,
'CBAAAAAA', 0, .0,
'BBAACAABAAAAAAAA                                                ',
.0, 0, 926,
'BGAAAAAAAAAAAAAA                                                ',
.0,
'BBAACAAB', 6, 6,
'AB   ', .00000, .00000,
'CA', 926,
'AB', 6,
'AB   ', 746, 246, 90, 0, 10, 0,
'CB', 0, .00,
'BBAACAAB', 1500, .00, .06, 9.26,
'BBAACAAB', 746, 6,
'CBAAAAAAAAAAAAAA                                                ',
46, 2590,
'CBAAAAAAAAAAAAAA                                                ',
0,
'AAAAAAAA', 0, .0, 50.0,
'ABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """Insert Into BTA1P002 
Values ('CAAAAAAA',
'CCAAAAAA', 57,
'AAAA ', 1,
'AA', 499,
'DCAACAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
1499, .0, .2,
'ACAA ', .2, .0, 17,
'ACAAAAAA', 57,
'CCAAAAAA', 1, .9,
'DJAAIAACAAAAAAAA                                                ',
1.9, 99, 802,
'DCAACAAAAAAAAAAA                                                ',
.0,
'DJAAIAAC', 7, 17,
'ACAA ', .00019, .00019,
'CA', 802,
'AC', 2,
'ACAA ', 4357, 357, 22, 0, 2, 2,
'CC', 1, .03,
'DJAAIAAC', 1499, .09, .02, 8.02,
'DJAAIAAC', 4357, 17,
'CCAAAAAAAAAAAAAA                                                ',
57, 2022,
'CCAAAAAAAAAAAAAA                                                ',
3,
'AAAAAAAA', 9, 9.9, 49.9,
'ACAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """Insert Into BTA1P002 
Values ('DAAAAAAA',
'DCAAAAAA', 85,
'BA   ', 1,
'BA', 498,
'AHAAEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
1498, .1, .3,
'AC   ', .7, .1, 5,
'BCAAAAAA', 85,
'DCAAAAAA', 0, .8,
'AEAAKAACAAAAAAAA                                                ',
1.8, 98, 687,
'AHAAEAAAAAAAAAAA                                                ',
.1,
'AEAAKAAC', 5, 5,
'BC   ', .00018, .00018,
'DA', 687,
'BC', 7,
'BM   ', 85, 85, 59, 1, 19, 9,
'DC', 0, .02,
'AEAAKAAC', 1498, .08, .07, 6.87,
'AEAAKAAC', 85, 5,
'DMAAAAAAAAAAAAAA                                                ',
85, 3659,
'DCAAAAAAAAAAAAAA                                                ',
2,
'BAAAAAAA',
8, 9.8, 49.8,
'ACAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """Insert Into BTA1P002 
Values ('AAAAAAAA',
'ACAAAAAA', 27,
'AAAA ', 3,
'AA', 999,
'BAAABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
2999, .0, .0,
'ACAA ', .2, .0, 7,
'ACAAAAAA', 27,
'ACAAAAAA', 1, .9,
'BFAAGAACAAAAAAAA                                                ',
1.9, 99, 72,
'BAAABAAAAAAAAAAA                                                ',
.0,
'BFAAGAAC', 7, 7,
'ACAA ', .00019, .00019,
'AA', 72,
'AC', 2,
'AWAA ', 3527, 27, 5, 1, 5, 5,
'AC', 1, .03,
'BFAAGAAC', 2999, .09, .12, .72,
'BFAAGAAC', 3527, 7,
'AWAAAAAAAAAAAAAA                                                ',
27, 3905,
'ACAAAAAAAAAAAAAA                                                ',
3,
'AAAAAAAA', 9, 9.9, 99.9,
'ACAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """Insert Into BTA1P002 
Values ('CAAAAAAA',
'CCAAAAAA', 16,
'AA   ', 0,
'AA', 998,
'GGAACAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
2998, .0, .2,
'AC   ', .2, .0, 16,
'ACAAAAAA', 16,
'CCAAAAAA', 0, .8,
'GAAAFAACAAAAAAAA                                                ',
1.8, 98, 902,
'GGAACAAAAAAAAAAA                                                ',
.0,
'GAAAFAAC',
6, 16,
'AC   ', .00018, .00018,
'CA', 902,
'AC', 2,
'AC   ', 16, 16, 13, 1, 13, 3,
'CC', 0, .02,
'GAAAFAAC', 2998, .08, .02, 9.02,
'GAAAFAAC', 16, 16,
'CCAAAAAAAAAAAAAA                                                ',
16,3513,
'CCAAAAAAAAAAAAAA                                                ',
2,
'AAAAAAAA', 8, 9.8, 99.8,
'ACAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """create view VNA1P002 as
select cast(char17_100 as varchar(20)) as char17_100
, udec17_100
from BTA1P002 
group by char17_100 , udec17_100
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """Create Table            BTA1P003 
(
varchar0_100     VarChar(1000)     ,
char0_1000       PIC X(32)         ,    

sbin1_100        Numeric(9,0) signed  ,
char1_4          PIC X(5)          ,
ubin1_4          Numeric(9,0) unsigned,    

char2_2          Char(2)           ,
varchar2_10      VarChar(15)       not null ,
varchar2_100     VarChar(25)       ,    

sbin3_1000       Numeric(5,0) signed ,
char3_1000       PIC X(240)        ,
ubin3_uniq       Numeric(5,0) unsigned ,    

sbin4_2          Numeric(1,1) signed,
ubin4_4          Numeric(1,1) unsigned ,
varchar4_1000    VarChar(16)        ,
sdec4_10         -- Decimal
Numeric(1,1) signed                 ,
udec4_2          -- Decimal
Numeric(1,1) unsigned               ,    

sbin5_4          Numeric(4,0) signed,
ubin5_20         Numeric(9,0) unsigned ,
udec5_20         -- Decimal
Numeric(4,0) unsigned               ,
varchar5_4       VarChar(8)         ,
sdec5_100        -- Decimal
Numeric(18,0) signed                ,    

varchar6_20      VarChar(32)        ,    

sbin7_2          SMALLINT signed    ,
sdec7_10         -- Decimal
Numeric(4,1) signed                 ,
char7_uniq       Char(100)          ,
udec7_20         -- Decimal
Numeric(4,1) unsigned               ,
ubin7_100        SMALLINT unsigned  ,    

sbin8_1000       Numeric(18,0) signed  ,
varchar8_uniq    VarChar(32)        ,
ubin8_2          Numeric(4,1) unsigned ,    

char9_uniq       Char(8)            ,
udec9_10         -- Decimal
Numeric(5,0) unsigned               ,
sdec9_20         -- Decimal
Numeric(5,0) signed                 ,    

varchar10_20      VarChar(32)       ,    

sdec11_20        -- Decimal
Numeric(5,5) signed                 ,
varchar11_2      VarChar(32)        not null ,
char11_4         Char(2)            ,    

sbin12_1000      Numeric(9,0) signed,
varchar12_4      VarChar(32)        ,
ubin12_10        Numeric(9,0) unsigned ,    

char13_100       Char(5)            ,
sdec13_uniq      -- Decimal
Numeric(9,0) signed                 ,
udec13_500       -- Decimal
Numeric(9,0) unsigned               ,    

sbin14_100       Numeric(2,0) signed   ,
ubin14_2         Numeric(2,0) unsigned ,
sdec14_20        -- Decimal
Numeric(2,0) signed                 ,
udec14_10        -- Decimal
Numeric(2,0) unsigned               ,
varchar14_2000   VarChar(64)        ,    

sbin15_2         INTEGER signed     ,
udec15_4         -- Decimal
Numeric(9,2) unsigned               ,
varchar15_uniq   VarChar(8)         not null ,
ubin15_uniq      INTEGER unsigned   ,
sdec15_10        -- Decimal
Numeric(9,2) signed                 ,
sbin16_20        Numeric(9,2) signed,
ubin16_1000      Numeric(9,2) unsigned ,
varchar16_100    VarChar(128)       ,    

sbin17_uniq      Numeric(10,0) signed  ,
sdec17_20        -- Decimal
Numeric(2,0) signed                 ,
char17_100       Char(100)          ,
varchar17_20     VarChar(240)       ,    

sbin18_uniq      Numeric(18,0) signed  ,
varchar18_uniq   VarChar(60)        ,    

sbin19_4         LARGEINT signed    ,
char19_2         Char(8)            ,
ubin19_10        SMALLINT unsigned  ,
udec19_100       -- Decimal
Numeric(4,1) signed                 ,
sdec19_1000      -- Decimal
Numeric(4,1) unsigned               ,    

varchar20_1000   VarChar(100)    

-- The following column sequence gives more than one
-- identical value in the first column of the primary key.
, primary  key ( varchar11_2 DESC
, varchar2_10     ASC
, varchar15_uniq  ASC
)
)
-- catalog <global_dbvolume_part1>
-- organization K
-- audit
-- extent (2500,64)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    # Insert before making views (was previously OBEY file OBEYIN02).
    #
    stmt = """Insert Into BTA1P003 
Values ('BQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
'CCAAKAAAAAAAAAAAAAAAAAAAAAAAAAAA',
40, 'BAAA ', 0,
'AB', 'BB             ','DQAAAAAAAAAAAAAA         ',
7,
'CHAAIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
7,
.1, .3,'CCAAKAAAAAAAAAAA', .1, .1,
0, 0, 0, 'DAAAAAAA',         40,
'DBAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
1, .7,'CCAAKAABAAAAAAAA                                                ', .7, 7,
391,'CCAAKAABAAAAAAAA                ', .1,
'CCAAKA  ', 0, 0,
'DBAAAAAA                        ', .00007,
'BAAA                            ',
'DA', 391,
'DAAAAAAAAAAAAAAA                ', 1,
'BQAA ', 3540, 40, 94, 0, 14, 4,
'CCAAKAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
1, .03,
'CCAAKAAB', 7, .07, .11, 3.91,
'BQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
3540, 0,
'DQAAAAAAAAAAAAAA                                                ',
'DBAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
1194,
'CCAAKAAB                                                    ',
3,
'BAAAAAAA', 7, .7, .7,
'CHAAIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """Insert Into BTA1P003 
Values ('ATAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
'DEAACAAAAAAAAAAAAAAAAAAAAAAAAAAA', 16,
'AAAA ', 0,
'AE', 'AE             ',
'ATAAAAAAAAAAAAAA         ', 995,
'DEAADAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
1995, .0, .0,
'DEAACAAAAAAAAAAA', .4, .0, 0, 16, 16,
'AAAAAAAA', 16,
'AEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA', 1, .5,
'DEAACAAEAAAAAAAA                                                ',
1.5, 95, 444,
'DEAACAAEAAAAAAAA                ', .0,
'DEAACA  ', 6, 16,
'AEAAAAAA                        ', .00015,
'AAAA                            ',
'A ', 444,
'AAAAAAAAAAAAAAAA                ', 4,
'ATAA ', 3516, 16, 93, 1, 13, 3,
'DEAACAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
1, .03,
'DEAACAAE', 1995, .05, .04, 4.44,
'ATAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
3516, 16,
'ATAAAAAAAAAAAAAA                                                ',
'AEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
3493,
'DEAACAAE                                                    ',
3,
'AAAAAAAA', 5, 9.5, 99.5,
'DEAADAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """Insert Into BTA1P003 
Values ('AYAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
'FGAADAAAAAAAAAAAAAAAAAAAAAAAAAAA', 87,
'AAAA ', 3,
'AA', 'AB',
'AYAAAAAAAAAAAAAA         ', 997,
'FEAADAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
1997, .0, .0,
'FGAADAAAAAAAAAAA', .4, .0, 3, 7, 7,
'AAAAAAAA', 87,
'AEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA', 1, .7,
'FGAADAAEAAAAAAAA                                                ',
1.7, 97, 524,
'FGAADAAEAAAAAAAA                ', .0,
'FGAADA  ', 7, 7,
'AEAAAAAA                        ', .00017,
'AAAA                            ',
'A ', 524,
'AAAAAAAAAAAAAAAA                ', 4,
'AYAA ', 987, 487, 72, 0, 12, 2,
'FGAADAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
1, .01,
'FGAADAAE', 1997, .07, .04, 5.24,
'AYAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
987, 7,
'AYAAAAAAAAAAAAAA                                                ',
'AEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
2772,
'FGAADAAE                                                    ',
1,
'AAAAAAAA', 7, 9.7, 99.7,
'FEAADAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """Insert Into BTA1P003 
Values ('AIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
'DDAABAAAAAAAAAAAAAAAAAAAAAAAAAAA', 9,
'AAAA ', 1,
'BA', 'AA',
'CIAAAAAAAAAAAAAA         ', 996,
'DGAAGAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
1996, .0, .2,
'DDAABAAAAAAAAAAA', .8, .0, 1, 9, 9,
'CAAAAAAA', 9,
'CDAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA', 0, .6,
'DDAABAADAAAAAAAA                                                ',
1.6, 96, 158,
'DDAABAADAAAAAAAA                ', .0,
'DDAABA  ', 9, 9,
'CDAAAAAA                        ', .00016,
'AAAA                            ',
'CA', 158,
'CAAAAAAAAAAAAAAA                ', 8,
'AIAA ', 2809, 309, 39, 1, 19, 9,
'DDAABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
0, .00,
'DDAABAAD', 1996, .06, .18, 1.58,
'AIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
2809, 9,
'CIAAAAAAAAAAAAAA                                                ',
'CDAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
3239,
'DDAABAAD                                                    ',
0,
'AAAAAAAA', 6, 9.6, 99.6,
'DGAAGAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #
    # Create View of a few rows, all columns; should be updateable.
    #
    stmt = """create view  VUA1P003 as
select *
from BTA1P003 
where ubin15_uniq > 1000
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """Create Table BTA1P004 
(
varchar0_4       varchar(3)   not null,
char0_1000       PIC X(64)    not null,    

sbin1_100        Numeric(9,0) signed     not null,
char1_4          PIC X(5)     not null,
ubin1_4          Numeric(9,0) unsigned   not null,    

char2_2          PIC X(2)     not null,    

sbin3_1000       Numeric(5,0) signed     not null,
char3_1000       PIC X(240)   not null,
ubin3_uniq       Numeric(5,0) unsigned   not null,    

sbin4_2          Numeric(2,1) signed     not null,
ubin4_4          Numeric(2,1) unsigned   not null,
char4_10         Char(5)      not null,
sdec4_10         Numeric(2,1) signed     not null,
udec4_2          Numeric(2,1) unsigned   not null,    

sbin5_4          Numeric(4,0) signed     not null,
ubin5_20         Numeric(9,0) unsigned   not null,
udec5_20         Numeric(4,0) unsigned   not null,
varchar5_10      VarChar(8)   not null,
sdec5_100        Numeric(18,0) signed    not null,    

char6_20         PIC X(8)                not null,    

sbin7_2          SMALLINT signed         not null,
sdec7_10         Numeric(4,1) signed     not null,
char7_uniq       Char(100)    not null,
udec7_20         Numeric(4,2) unsigned   not null,
ubin7_100        SMALLINT     unsigned   not null,    

sbin8_1000       Numeric(18,0) signed    not null,
char8_500        PIC X(100)   not null,
ubin8_2          Numeric(4,1) unsigned   not null,    

char9_uniq       Char(8)      not null,
udec9_10         Numeric(5,0) unsigned   not null,
sdec9_20         Numeric(5,0) signed     not null,    

char10_20        PIC X(5)     not null,    

sdec11_20        Numeric(5,5) signed     not null,
udec11_20        Numeric(5,5) unsigned   not null,
char11_4         Char(2)      not null,    

sbin12_1000      Numeric(9,0) signed     not null,
char12_10        PIC X(2)     not null,
ubin12_10        Numeric(9,0) unsigned   not null,    

varchar13_100    VarChar(5)   not null,
sdec13_uniq      Numeric(9,0) signed     not null,
udec13_500       Numeric(9,0) unsigned   not null,    

sbin14_100       Numeric(2,0) signed     not null,
ubin14_2         Numeric(2,0) unsigned   not null,
sdec14_20        Numeric(2,0) signed     not null,
udec14_10        Decimal (2,0) unsigned   not null,
char14_20        Char(2)      not null,    

sbin15_2         INTEGER      signed     not null,
udec15_4         Decimal(9,2) unsigned   not null,
varchar15_uniq   VarChar(9)   not null,
ubin15_uniq      INTEGER      unsigned   not null,
sdec15_10        Decimal(9,2) signed     not null,    

sbin16_20        Numeric(9,2) signed     not null,
ubin16_1000      Numeric(9,2) unsigned   not null,
char16_uniq      PIC X(8)     not null,    

sbin17_uniq      Numeric(10,0) signed    not null,
sdec17_20        Decimal(3,0) signed     not null, --3<2
char17_100       Char(100)    not null,
udec17_100       Decimal(3,0) unsigned   not null, --3<2    

sbin18_uniq      Numeric(18,0) signed    not null,
char18_20        PIC X(100)   not null,    

sbin19_4         LARGEINT     signed     not null,
char19_2         Char(8)      not null,
ubin19_10        SMALLINT     unsigned   not null,
udec19_100       Numeric(4,1) signed     not null,
sdec19_1000      Numeric(4,1) unsigned   not null,    

char20_10        PIC X(240)   not null    

-- leading odd-length column on key.
, primary key
( varchar13_100 DESC
, sdec13_uniq    ASC
, char14_20
, varchar15_uniq
)
)    

-- catalog <global_dbvolume_part1>
-- organization K
;"""
    output = _dci.cmdexec(stmt)
    
    # Insert before making views (was previously OBEY file OBEYIN04).
    stmt = """Insert Into BTA1P004 
Values ('A',
'FJAAGAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
12,
'AAAA ', 0,
'AA', 559,
'FAAAHAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
4559, .0, .0,
'AEAA ', .4, .0, 0, 12, 12,
'AEAAAAA', 12,
'AEAAAAAA',
-- 7
1, .9,
'FJAAGAAEAAAAAAAA                                                ',
1.9, 59, 384,
'FAAAHAAAAAAAAAAA                                                ',
.0,
'FJAAGAAE', 2, 12,
'AEAA ', .00019, .00019,
'AA',
--12
384,
'AE', 4,
'AJAA ', 3112, 112, 9, 1, 9, 9,
'AE',
-- 15
1, .03,
'FJAAGAA', 4559, .09, .04, 3.84,
'FJAAGAAE',
--17
3112, 12,
'AJAAAAAAAAAAAAAA                                                ',
12,  9,
'AEAAAAAAAAAAAAAA                                                ',
3,
'AAAAAAAA', 9, 5.9, 55.9,
'AEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """Insert Into BTA1P004 
Values ('CAA',
'EJAAJAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
13,
'AAAA ', 1,
'AA', 889,
'ECAAFAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
3889, .0, .2,
'ACAA ', .2, .0, 1, 13, 13,
'ACAAA', 13,
'CCAAAAAA', 1, .9,
'EJAAJAACAAAAAAAA                                                ',
.9, 89, 442,
'ECAAFAAAAAAAAAAA                                                ',
.0,
'EJAAJAAC', 3, 13,
'ACAA ', .00009, .00009,
'CA', 442,
'AC', 2,
'ARAA ', 1413, 413, 8, 0, 8, 8,
'CC', 1, .01,
'EJAAJAA', 3889, .09, .02, 4.42,
'EJAAJAAC', 1413, 13,
'CRAAAAAAAAAAAAAA                                                ',
13, 8,
'CCAAAAAAAAAAAAAA                                                ',
1,
'AAAAAAAA', 9, 8.9, 88.9,
'ACAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """Insert Into BTA1P004 
Values ('AAA',
'FGAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
17,
'AA   ', 1,
'AA', 188,
'FEAACAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
1188, .0, .0,
'AB   ', .6, .0, 1, 17, 17,
'ABAAAAAA', 17,
'ABAAAAAA', 0, .8,
'FGAAAAABAAAAAAAA                                                ',
.8, 88, 756,
'FEAACAAAAAAAAAAA                                                ',
.0,
'FGAAAAAB', 7, 17,
'AB   ', .00008, .00008,
'AA', 756,
'AB', 6,
'AG', 4217, 217, 95, 1, 15, 5,
'AB', 0, .00,
'FGAAAAAB', 1188, .08, .16, 7.56,
'FGAAAAAB', 4217, 17,
'AGAAAAAAAAAAAAAA                                                ',
17,  1995,
'ABAAAAAAAAAAAAAA                                                ',
0,
'AAAAAAAA', 8, 8.8, 18.8,
'ABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """Insert Into BTA1P004 
Values ('A',
'BEAAGAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
30,
'AA   ', 2,
'AA', 412,
'BAAAFAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
4412, .0, .0,
'AC   ', .2, .0, 2, 10, 10,
'ACAAA', 30,
'ACAAAAAA', 0, .2,
'BEAAGAACAAAAAAAA                                                ',
1.2, 12, 712,
'BAAAFAAAAAAAAAAA                                                ',
.0,
'BEAAGAAC', 0, 10,
'AC   ', .00012, .00012,
'AA', 712,
'AC', 2,
'AM', 3030, 30, 7, 1, 7, 7,
'AC', 0, .00,
'BEAAGAAC', 4412, .02, .12, 7.12,
'BEAAGAAC', 3030, 10,
'AMAAAAAAAAAAAAAA                                                ',
30, 7,
'ACAAAAAAAAAAAAAA                                                ',
0,
'AAAAAAAA', 2, 1.2, 41.2,
'ACAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """Insert Into BTA1P004 
Values ('E',
'BE', 5,
'AE', 5,
'AE', 5,
'BE', 5, .5, .5,
'AE', .5, .5, 5, 5, 5,
'AE', 5,
'AE', 5, .5,
'BE', 5.5, 5, 5,
'BE', .5,
'BE', 5, 5,
'AE', .00005, .00005,
'AE', 5,
'AE', 5,
'AM',
3030, 50, 5, 5, 5, 5,
'AC', 0, .00,
'BEAAGAAD', 5000, .05, .05, 5.05,
'BF', 5050, 50,
'AE', 50, 5,
'AE', 5,
'AE', 5, 0.5, 50.5,
'AE'
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #
    # This is row 6:
    #
    stmt = """Insert Into BTA1P004 
Values ('F',
'BF', 6,
'AF', 6,
'AF', 6,
'BF', 6, .6, .6,
'AF', .6, .6, 6, 6, 6,
'AF', 6,
'AF', 6, .6,
'BF', 6.6, 6, 6,
'BF', .6,
'BF', 6, 6,
'AF', .00006, .00006,
'AF', 6,
'AF', 6,
'AM',
3030, 60, 6, 6, 6, 6,
'AE', 0, .00,
'BEAAGAAC', 6000, .06, .06, 6.06,
'BF', 6060, 60,
'AF', 60, 6,
'AF', 6,
'AF', 6, 0.6, 60.6,
'AF'
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #
    # This is row 7:
    #
    stmt = """Insert Into BTA1P004 
Values ('G',
'BG', 7,
'AG', 7,
'AG', 7,
'BG', 7, .7, .7,
'AG', .7, .7, 7, 7, 7,
'AG', 7,
'AG', 7, .7,
'BG', 7.7, 7, 7,
'BG', .7,
'BG', 7, 7,
'AG', .00007, .00007,
'AG', 7,
'AG', 7,
'AM',
3030, 70, 7, 7, 7, 7,
'AE', 0, .00,
'BEAAGAAE', 7000, .07, .07, 7.07,
'BG', 7070, 70,
'AG', 70, 7,
'AG', 7,
'AG', 7, 0.7, 70.7,
'AG'
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    #
    # This is row 8:
    #
    stmt = """Insert Into BTA1P004 
Values ('H',
'BH', 8,
'AH', 8,
'AH', 8,
'BH', 8, .8, .8,
'AH', .8, .8, 8, 8, 8,
'AH', 8,
'AH', 8, .8,
'BH', 8.8, 8, 8,
'BH', .8,
'BH', 8, 8,
'AH', .00008, .00008,
'AH', 8,
'AH', 8,
'AM',
3031, 80, 8, 8, 8, 8,
'AC', 0, .00,
'BEAAGAAC', 8000, .08, .08, 8.08,
'BH', 8080, 80,
'AH', 80, 8,
'AH', 8,
'AH', 8, 0.8, 80.8,
'AH'
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #
    # This is row 9:
    #
    stmt = """Insert Into BTA1P004 
Values ('I',
'BI', 9,
'AI', 9,
'AI', 9,
'BI', 9, .9, .9,
'AI', .9, .9, 9, 9, 9,
'AI', 9,
'AI', 9, .9,
'BI', 9.9, 9, 9,
'BI', .9,
'BI', 9, 9,
'AI', .00009, .00009,
'AI', 9,
'AI', 9,
'AM',
3031, 90, 9, 9, 9, 9,
'AC', 0, .00,
'BEAAGAAF', 9000, .09, .09, 9.09,
'BI', 9090, 90,
'AI', 90, 9,
'AI', 9,
'AI', 9, 0.9, 90.9,
'AI'
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    #
    # This is row 10:
    #
    stmt = """Insert Into BTA1P004 
Values ('J',
'BJ', 10,
'AJ', 10,
'AJ', 10,
'BJ', 10, 1.0, 1.0,
'AJ', 1.0, 1.0, 10, 10, 10,
'AJ', 10,
'AJ', 10, 1.0,
'BJ', 10.10, 10, 10,
'BJ', 1.0,
'BJ', 10, 10,
'AJ', .00010, .00010,
'AJ', 10,
'AJ', 10,
'AM',
3031, 100, 10, 10, 10, 10,
'AC', 0, .00,
'BEAAGAAG', 10000, .10, .10, 10.10,
'BJ', 10100, 100,
'AJ', 100, 10,
'AJ', 10,
'AJ', 10, 1.0, 101.0,
'AJ'
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #
    # This is row 11:
    #
    stmt = """Insert Into BTA1P004 
Values ('K',
'BK', 11,
'AK', 11,
'AK', 11,
'BK', 11, 1.1, 1.1,
'AK', 1.1, 1.1, 11, 11, 11,
'AK', 11,
'AK', 11, 1.1,
'BK', 10.11, 11, 11,
'BK', 1.1,
'BK', 11, 11,
'AK', .00011, .00011,
'AK', 11,
'AK', 11,
'AM',
3031, 110, 11, 11, 11, 11,
'AD', 0, .00,
'BEAAGAAD', 11000, .11, .11, 11.11,
'BK', 10110, 110,
'AK', 110, 11,
'AK', 11,
'AK', 11, 1.1, 101.1,
'AK'
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    #
    # This is row 12:
    #
    stmt = """Insert Into BTA1P004 
Values ('L',
'BL', 12,
'AL', 12,
'AL', 12,
'BL', 12, 1.2, 1.2,
'AL', 1.2, 1.2, 12, 12, 12,
'AL', 12,
'AL', 12, 1.2,
'BL', 10.12, 12, 12,
'BL', 1.2,
'BL', 12, 12,
'AL', .00012, .00012,
'AL', 12,
'AL', 12,
'AM',
3050, 120, 12, 12, 12, 12,
'AC', 0, .00,
'BEAAGAAC', 12000, .12, .12, 12.12,
'BL', 10120, 120,
'AL', 120, 12,
'AL', 12,
'AL', 12, 1.2, 101.2,
'AL'
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #
    # This is row 13:
    #
    stmt = """Insert Into BTA1P004 
Values ('M',
'BM', 13,
'AM', 13,
'AM', 13,
'BM', 13, 1.3, 1.3,
'AM', 1.3, 1.3, 13, 13, 13,
'AM', 13,
'AM', 13, 1.3,
'BM', 10.13, 13, 13,
'BM', 1.3,
'BM', 13, 13,
'AM', .00013, .00013,
'AM', 13,
'AM', 13,
'AN',
3030, 130, 13, 13, 13, 13,
'AC', 0, .00,
'BEAAGAAC', 13000, .13, .13, 13.13,
'BM', 10130, 130,
'AM', 130, 13,
'AM', 13,
'AM', 13, 1.3, 101.3,
'AM'
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """create view  VNA1P004 as
select varchar0_4     , char0_1000 , sbin7_2
, varchar5_10    , char6_20   , ubin15_uniq
, varchar15_uniq , char16_uniq
from BTA1P004 
where ubin15_uniq > 1000
group by   varchar0_4     , char0_1000 , sbin7_2
, varchar5_10    , char6_20   , ubin15_uniq
, varchar15_uniq , char16_uniq
having
(  varchar0_4,'ACAAA' , varchar15_uniq )
<>
( 'CAA' , varchar5_10 , 'EJAAJAA' )
-- catalog <global_dbvolume_part1>
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """Create Table BTA1P005 
(
char0_n10           Char(2)
-- default 'AD'
-- heading 'char0_n10 with default AD'
,
sbin0_uniq          Smallint not null,
sdec0_n500          Numeric(18,0) ,    

ubin1_n2            Numeric(4,0) unsigned
,
udec1_100           Numeric(2,0) unsigned not null,    

char2_2             Char(2)               not null,
sbin2_nuniq         Largeint              ,
sdec2_500           Numeric(9,0) signed   not null,    

udec3_n100          Numeric(9,0) unsigned ,
ubin3_n2000         Numeric(4,0) unsigned ,
char3_4             Char(8)               not null
,    

sdec4_n20           Numeric(4,0)          ,
sbin4_n1000         Smallint              ,
char4_n10           Char(8)               ,    

char5_n20           Char(8)               ,
sdec5_10            Numeric(9,0) signed   not null,
ubin5_n500          Numeric(9,0) unsigned
,    

sbin6_nuniq         Largeint              ,
sdec6_4             Numeric(4,0) signed   not null,
char6_n100          Char(8)               ,    

sbin7_n20           Smallint              ,
char7_500           Char(8)               not null,
udec7_n10           Numeric(4,0) unsigned
,    

ubin8_10            Numeric(4,0) unsigned not null,
char8_n1000         Char(8)               ,
sdec8_4             Numeric(9,0) unsigned not null,    

sdec9_uniq          Numeric(18,0) signed  not null,
char9_100           Char(2)               not null,
ubin9_n4            Numeric(9,0) unsigned
,    

ubin10_n2           Numeric(4,0) unsigned ,
char10_nuniq        Char(8)               ,
udec10_uniq         Numeric(9,0) unsigned not null,    

udec11_2000         Numeric(9,0) unsigned not null,
sbin11_100          Integer               not null,
char11_uniq         Char(8)               not null
,    

ubin12_2            Numeric(4,0) unsigned not null
,
sdec12_n1000        Numeric(18,0) signed  ,
char12_n2000        Char(8)
,    

udec13_500          Numeric(9,0) unsigned not null,
char13_1000         Char(8)               not null
,    

sbin14_1000         Integer               not null,
udec14_100          Numeric(4,0) unsigned not null,
char14_n500         Char(8)               ,    

sbinneg15_nuniq     Largeint              ,
sdecneg15_100       Numeric(9,0) signed   not null,
char15_100          Char(8)               not null
,    

ubin16_n10          Numeric(4,0) unsigned
,
sdec16_uniq         Numeric(18,0) signed  not null,
char16_n20          Char(5)
,   -- len = 2,4    

sbin17_uniq         Largeint              not null,
sdec17_nuniq        Numeric(18,0)
,
char17_2            Char(8)               not null    

, primary key ( sbin0_uniq )
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    # Insert before making views.
    #
    stmt = """Insert Into BTA1P005 
Values ( NULL , -200, -266,
NULL , 60,
'AA', -3766, -266,
44, 344, 'BA',
-9, -509, NULL ,
'AAAAAAAA', -0, 60, -- (5)
-3766, -2, 'CQAAAAAA',
-4, 'EAAAGAAA', NULL ,
9, 'DBAAAAAA', 1,
-60, 'AK', NULL ,
NULL , 'AEAAJAAB', 3766, -- (10)
344, -44, 'EKAACAAE',
1, -509, 'DBAAAAAB',
60, 'EFAAIAAA',
-766, 66, 'AGAAEAAA',
-4344, -44, 'ATAAAAAA', -- (15)
NULL , -2509, 'BE   ',
-37055, -60, 'AAAAAAAA'
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    #
    # 3/13/96.  Added aggregates to view VNA1P005;
    #           To allow for duplicate data values, replaced data in row
    #           with primary key -201 with columns that are
    #           the same as data for row with primary key -200.
    #           (except make primary key field be -201.)
    stmt = """Insert Into BTA1P005 
Values ( NULL , -201, -266,
NULL , 60,
'AA', -3766, -266,
44, 344, 'BA',
-9, -509, NULL     ,
'AAAAAAAA', -0, 60, -- (5)
-3766, -2, 'CQAAAAAA',
-4, 'EAAAGAAA', NULL ,
9, 'DBAAAAAA', 1,
-60, 'AK', NULL ,
NULL , 'AEAAJAAB', 3766, -- (10)
344, -44, 'EKAACAAE',
1, -509, 'DBAAAAAB',
60, 'EFAAIAAA',
-766, 66, 'AGAAEAAA',
-4344, -44, 'ATAAAAAA', -- (15)
NULL , -2509, 'BE   ',
-37055, -60, 'AAAAAAAA'
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """Insert Into BTA1P005 
Values ( NULL , -101, -272,
NULL , 86,
'BA', -772, -272,
52, 1552, 'AA',
-18, -678, NULL ,
'CBAAAAAA', -6, 86, -- (5)
-772, -0, 'AWAAAAAA',
-12, 'DAAAGAAA', NULL ,
8, 'DEAAMAAA', 2,
-2086, 'CL', NULL ,
NULL , 'CCAAFAAC', 772, -- (10)
1552, -52, 'DKAADAAC',
0, -678, 'DEAAMAAA',
86, 'AHAAGAAA',
-772, 72, 'CEAAHAAA',
-3552, -52, 'ACAAAAAA', -- (15)
NULL , -3678, 'ADAA ',
-49700, -2086, 'AAAAAAAA'
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """Insert Into BTA1P005 
Values ( NULL , -100, -65,
NULL , 12,
'BA', -2065, -65,
89, 389, 'CA',
-14, -594, NULL ,
'ACAAAAAA', -2, 312, -- (5)
-2065, -1, 'BPAAAAAA',
-9, 'CFAAEAAA', NULL ,
4, 'FKAAIAAA', 2,
-812, 'AM', NULL ,
NULL , 'AIAALAAA', 2065, -- (10)
389, -89, 'CCAAKAAE',
0, -594, 'FKAAIAAA',
312, 'AJAAGAAA',
-65, 65, 'ABAAEAAA',
-2389, -89, 'BOAAAAAA', -- (15)
NULL , -1594, 'AE   ',
-15935, -812, 'AAAAAAAA'
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """Insert Into BTA1P005 
Values ( NULL , -1, -36,
NULL , 95,
'DA', -2536, -36,
89, 789, 'CA',
-17, -417, NULL     ,
'DAAAAAAA', -5, 495, -- (5)
-2536, -0, 'ALAAAAAA',
-9, 'DFAAIAAA', NULL ,
7, 'AGAAKAAA', 1,
-4495, 'DU', NULL     ,
NULL , 'CGAABAAB', 2536, -- (10)
789, -89, 'DGAAHAAE',
1, -417, 'AGAAKAAB',
495, 'BHAAKAAA',
-536, 36, 'CAAAHAAA',
-2789, -89, 'BOAAAAAA', -- (15)
NULL , -4417, 'BCAA ',
-81017, -4495, 'BAAAAAAA'
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """Insert Into BTA1P005 
Values ( NULL , -0, -284,
NULL , 2,
'EA', -284, -284,
50, 1950, 'DA',
-6, -866, NULL ,
'CCAAAAAA', -2, 302, -- (5)
-284, -0, 'AJAAAAAA',
-10, 'EGAAGAAA', NULL ,
6, 'FIAAIAAA', 2,
-1802, 'CC', NULL ,
NULL , 'EJAALAAE', 284, -- (10)
1950, -50, 'EDAAAAAA',
0, -866, 'FIAAIAAA',
302, 'DJAAIAAA',
-284, 84, 'EEAAFAAA',
-1950, -50, 'CAAAAAAA', -- (15)
NULL , -866, 'AB   ',
-48764, -1802, 'AAAAAAAA'
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #
    # Create View of some rows and columns; non-updateable because it
    # involves joins (left and right).
    # Expected to return 6 rows:
    #
    # (EXPR)                (EXPR)  (EXPR)  (EXPR)
    # --------------------  ------  ------  --------
    #
    # -               2789  DA      EA             ?
    # -               3552  BA      AA      AA
    # -               4344  AA      BA      BA
    # -               2389  BA      AA      AA
    #                    ?       ?  BA      BA
    #                    ?       ?  DA      DA
    #
    #
    stmt = """create view  VNA1P005 ( n1, c2, c3, c4 ) as
select cast( max(T1.sbinneg15_nuniq) as smallint signed )
, min(T1.char2_2)
, min(T2.char2_2)
, max(T3.char3_4)
from BTA1P005 T1 
right join BTA1P005 T2 on T1.char2_2   = T2.char3_4
left  join BTA1P005 T3 on T2.char2_2   = T3.char3_4
group by T1.sbinneg15_nuniq , T1.char2_2 , T2.char2_2 , T3.char3_4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """Create Table BTA1P006 
(
sbin0_4             Integer      not null,
varchar0_uniq       VarChar(8)   not null,
sdec0_100           Numeric(9,0) not null,
sdec1_20            Numeric(5,0) not null,
udec1_nuniq         Numeric(4,0) unsigned,    

char2_2             Char(2)      not null,
sbin2_nuniq         Largeint     ,
sdec2_500           Numeric(9,0) signed       not null,
udec3_n100          Numeric(9,0) unsigned,
ubin3_n2000         Numeric(4,0) unsigned,
char3_4             Char(8)      not null,    

sdec4_n20           Numeric(4,0) ,
sbin4_n1000         Smallint     ,
char4_n10           Char(8)      ,
char5_n20           Char(8)      ,
sdec5_10            Numeric(9,0) signed       not null,
ubin5_n500          Numeric(9,0) unsigned ,    

sbin6_nuniq         Largeint     ,
sdec6_4             Numeric(4,0) signed       not null,
char6_n100          Char(8)      ,
sbin7_n20           Smallint     ,
char7_500           Char(8)      not null,
udec7_n10           Numeric(4,0) unsigned,    

ubin8_10            Numeric(4,0) unsigned not null,
char8_n1000         Char(8)      ,
sdec8_4             Numeric(9,0) unsigned not null,
sdec9_uniq          Numeric(18,0) signed      not null,
char9_100           Char(2)      not null,    

char10_nuniq        Char(8)      ,
udec10_uniq         Numeric(9,0) unsigned     not null,
udec11_2000         Numeric(9,0) unsigned     not null,
sbin11_100          Integer      not null,
char11_uniq         Char(8)      not null,    

ubin12_2            Numeric(4,0) unsigned     not null,
sdec12_n1000        Numeric(18,0) signed ,
char12_n2000        Char(8)      ,
udec13_500          Numeric(9,0) unsigned     not null,
char13_1000         Char(8)      not null,    

sbin14_1000         Integer      not null,
udec14_100          Numeric(4,0) unsigned not null,
char14_n500         Char(8)      ,
sbinneg15_nuniq     Largeint     ,
sdecneg15_100       Numeric(9,0) signed not null,
char15_100          VarChar(8)   not null,    

ubin16_n10          Numeric(4,0) unsigned  ,
sdec16_uniq         Numeric(18,0) signed   not null,
char16_n20          Char(5)      ,
sbin17_uniq         Largeint   not null,
sdec17_nuniq        Numeric(18,0) ,
char17_2            VarChar(7)    not null    

, primary key ( sdec9_uniq ASC
, sdec0_100 DESC
, sdec1_20 ASC )
)
-- catalog <global_dbvolume_part1>
-- organization K
-- audit
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    # Insert before making views (was previously OBEY file OBEYIN06).
    
    stmt = """Insert Into BTA1P006 
Values (
-0, 'CJAAAAAC', -81, -2, 1973,
'AA', -702, -202, 81, 81, 'BAAAAAAA',
-4, -724, NULL , 'BDAAAAAA', -3, 473, -- (5)
-702, -2, 'CCAAAAAA', -1, 'ABAAEAAA', NULL ,
4, 'GFAAFAAA', 0, -201, 'BX',
'CJAAAAAC', 702, 81, -81, 'AAAAMAAB', -- (10)
0, -724, 'GFAAFAAA', 473, 'GEAAKAAA',
-702, 2, 'CGAAAAAA', -4081, -81, 'BGAAAAAA', -- (15)
NULL , -4724, 'AEAA', -76757, -1973, 'BAAA'
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """Insert Into BTA1P006 
Values (
-1, 'AEAAJAAB', -44, -6, 60,
'AA', -3766, -266, 44, 344, 'AAAAAAAA',
-9, -509,  NULL , 'AAAAAAAA', -0, 60, -- (5)
-3766, -2, 'CQAAAAAA', -4, 'EAAAGAAA', NULL ,
9, 'DBAAAAAA', 1, -200, 'AK',
'AEAAJAAB', 3766, 344, -44, 'EKAACAAE', -- (10)
1, -509, 'DBAAAAAB', 60, 'EFAAIAAA',
-766, 66, 'AGAAEAAA', -4344, -44, 'ATAAAAA', -- (15)
NULL , -2509, 'BE   ', -37055, -60, 'AAAA'
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """Insert Into BTA1P006 
Values (
-2, 'CCAAFAAC', -52, -12, 2086,
'AA', -772, -272, 52, 1552, 'AAAAAAAA',
-18, -678, NULL , 'CBAAAAAA', -6, 86, -- (5)
-772, -0, 'AWAAAAAA', -12, 'DAAAGAAA', NULL ,
8, 'DEAAMAAA', 2, -101, 'CL',
'CCAAFAAC', 772, 1552, -52, 'DKAADAAC', -- (10)
0, -678, 'DEAAMAAA', 86, 'AHAAGAAA',
-772, 72, 'CEAAHAAA', -3552, -52, 'ACAAAAAA', -- (15)
NULL , -3678, 'AB', -49700, -2086, 'AAAAAA'
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """Insert Into BTA1P006 
Values (
-2, 'AIAALAAA', -89, -5, 812,
'BA', -2065, -65, 89, 389, 'BAAAAAAA',
-14, -594, NULL , 'ACAAAAAA', -2, 312, -- (5)
-2065, -1, 'BPAAAAAA', -9, 'CFAAEAAA', NULL ,
4, 'FKAAIAAA', 2, -100, 'AM',
'AIAALAAA', 2065, 389, -89, 'CCAAKAAE', -- (10)
0, -594, 'FKAAIAAA', 312, 'AJAAGAAA',
-65, 65, 'ABAAEAAA', -2389, -89, 'BOAAAAA',
NULL , -1594, 'AA', -15935, -812, 'AAAAAAA' -- (15)
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # Create View of some rows and columns; non-updateable, because of
    # joins.
    # Natural join is equijoin with duplicate column omitted.
    #
    # Purpose: Create Global view that contains Natural Join.
    
    stmt = """create view  VNA1P006 as
select * from
(select sbin0_4 , sdec5_10 , sdec6_4 , varchar0_uniq
from BTA1P006 T1 ) T2 
natural    join
(select sbin0_4 , sdec5_10 , sdec6_4 , varchar0_uniq
from BTA1P006 T3 ) t4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """Create Table BTA1P007 
(
varchar0_nuniq      VarChar(11)            ,
sbin0_uniq          Smallint               not null,
sdec0_n500          Numeric(18,0)          ,    

ubin1_n2            Numeric(4,0) unsigned  ,
udec1_100           Numeric(2,0) unsigned  not null,    

char2_2             Char(2)                not null,
sbin2_nuniq         Largeint               ,
sdec2_500           Numeric(9,0) signed    not null,    

udec3_n100          Numeric(9,0) unsigned  ,
ubin3_n2000         Numeric(4,0) unsigned  ,
char3_4             Char(9)                not null,    

sdec4_n20           Numeric(4,0)           ,
sbin4_n1000         Smallint               ,
char4_n10           Char(8)                ,    

char5_n20           Char(9)                ,
sdec5_10            Numeric(9,0) signed    not null,
ubin5_n500          Numeric(9,0) unsigned  ,    

sbin6_nuniq         Largeint               ,
sdec6_4             Numeric(4,0) signed    not null,
char6_n100          Char(8)                ,    

sbin7_n20           Smallint               ,
char7_500           Char(9)                not null,
udec7_n10           Numeric(4,0) unsigned  ,    

ubin8_10            Numeric(4,0) unsigned  not null,
char8_n1000         Char(8)                ,
sdec8_4             Numeric(9,0) unsigned  not null,    

sdec9_uniq          Numeric(18,0) signed   not null,
char9_100           Char(3)                not null,
ubin9_n4            Numeric(9,0) unsigned  ,    

ubin10_n2           Numeric(4,0) unsigned  ,
char10_nuniq        Char(8)                ,
udec10_uniq         Numeric(9,0) unsigned  not null,    

udec11_2000         Numeric(9,0) unsigned  not null,
sbin11_100          Integer                not null,
char11_uniq         Char(9)                not null,    

ubin12_2            Numeric(4,0) unsigned  not null,
sdec12_n1000        Numeric(18,0) signed   ,
char12_n2000        Char(8)                ,    

sbin13_n100         Numeric (10,0) signed  ,
char13_1000         Char(9)                not null,    

sbin14_1000         Integer                not null,
udec14_100          Numeric(4,0) unsigned  not null,
char14_n500         Char(8)                ,    

sbinneg15_nuniq     Largeint               ,
sdecneg15_100       Numeric(9,0) signed    not null,
char15_100          Char(9)                not null,    

ubin16_n10          Numeric(4,0) unsigned  ,
sdec16_uniq         Numeric(18,0) signed   not null,
char16_n20          Char(5)                ,    

sbin17_uniq         Largeint               not null,
sdec17_nuniq        Numeric(18,0)          ,
char17_2            Char(8)                not null    

) no partition
--  organization E
--  audit
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    # Insert before making views (was previously OBEY file OBEYIN07).
    #
    stmt = """Insert Into BTA1P007 
Values ('GGAAKAAB   ',  3,    5, NULL,    3,
'BA',         505,    5,   12, 1812,
'AAAAAAAA',     1,  701,
'BBAAAAAA',
'DDAAAAAA',     3,    3,  505,    1,
'BFAAAAAA',    12,
'EEAAFAAA',     2,    1,
'GGAAKAAA',     1,    3,
'DD',        NULL, NULL,
'BKAALAAA',   505, 1812,   12,
'EGAADAAC',     1,  701,
'GGAAKAAB',    .3,  -- Change pic S9(9)V9 to Numeric(10,1)
'DDAADAAA',   505,    5,
'BBAABAAA', -3812,  -12,
'AMAAAAAA',     1, 2701,
'BBAA ',   149840,    3,
'BAAAAAAA'
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """Insert Into BTA1P007 
Values ('AA'         ,  1,  389, NULL,    1,
'BA',        3389,  389,   86,  186,
'CAAAAAAA',    13,  293,
'BDAAAAAA',
'BBAAAAAA',     1,    1, 3389,    1,
'BOAAAAAA',     6,
'ECAAGAAA',     6,    3,
'DEAAEAAA',     1,    1,
'BB',        NULL, NULL,
'BBAAJAAE',  3389,  186,   86,
'EKAAEAAB',     1,  293,
'DEAAEAAB',    .1,
'BBAABAAA',   389,   89,
'BFAAFAAA',  -186,  -86,
'CLAAAAAA',     3, 3293,
'BD   ',    32293,    1,
'BAAAAAAA'
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """Insert Into BTA1P007 
Values ('ABC'        ,  0,  442, NULL,    0,
'BE',        4942,  442,   84, 1584,
'AAAAAAAA',    13,  993,
'BDAAAAAA',
'AAAAAAAA',     0,    0, 4942,    2,
'CRAAAAAA',     4,
'AAAACAAA',     4,    3,
'FCAAEAAA',     1,    0,
'AA',        NULL, NULL,
'ADAACAAC',  4942, 1584,   84,
'AJAAJAAE',     1,  993,
'FCAAEAAB',    .0,
'AAAAAAAA',   942,   42,
'AGAABAAA', -3584,  -84,
'AJAAAAAA',     3, 1993,
'BDAA ',    42154,    0,
'AAAAAAAA'
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """Insert Into BTA1P007 
Values ('AEAAEAAB   ',  5,  264, NULL,    5,
'AA',        3264,  264,   91,  591,
'DAAAAAAA',    11,  151,
'BBAAAAAA',
'BAAAAAAA',     5,    5, 3264,    0,
'AOAAAAAA',    11,
'BHAAIAAA',     1,    1,
'AEAAEAAA',     3,    5,
'BF',        NULL, NULL,
'CIAABAAE',  3264,  591,   91,
'BGAAEAAB',     1,  151,
'AEAAEAAB',    .5,
'FFAAFAAA',   264,   64,
'CAAAGAAA', -2591,  -91,
'DQAAAAAA',     1, 4151,
'BB   ',   109174,    5,
'BAAAAAAA'
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """Insert Into BTA1P007 
Values ('BA'         ,  4,  103, NULL,    4,
'AB',         603,  103,   97,  697,
'BAAAAAAA',     8,   28,
'ADAAAAAA',
'AEAAAAAA',     4,    4,  603,    3,
'DDAAAAAA',    17,
'CBAAGAAA',     7,    8,
'FEAAAAAA',     0,    4,
'AE',        NULL, NULL,
'BJAAFAAD',   603,  697,   97,
'CCAAGAAC',     0,   28,
'FEAAAAAA',    .4,
'EEAAEAAA',   603,    3,
'BDAAAAAA', -2697,  -97,
'BWAAAAAA',     8, 2028,
'AD   ',    56017,    4,
'AAAAAAAA'
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """Insert Into BTA1P007 
Values ('EBAAEAAC   ',  2,   85, NULL,    2,
'BA',        3585,   85,   13, 1013,
'BAAAAAAA',    17,  917,
'BCAAAAAA',
'CCAAAAAA',     2,    2, 3585,    1,
'BKAAAAAA',    13,
'FFAAFAAA',     3,    7,
'EBAAEAAA',     1,    2,
'CC',        NULL, NULL,
'BKAAKAAA',  3585, 1013,   13,
'FBAAMAAD',     1,  917,
'EBAAEAAB',    .2,
'CCAACAAA',   585,   85,
'BBAADAAA', -1013,  -13,
'BNAAAAAA',     7, 3917,
'BCAA ',    59492,    2,
'AAAAAAAA'
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """create view  VNA1P007 ( cUpper, cLower, cChar_length
, cOctet_length,  cPosition
, cSubstring ,    cTrim
, cConcatChar ,   cConcatVarchar)
as select upper(lower( varchar0_nuniq || varchar0_nuniq ))
, lower(upper( varchar0_nuniq || varchar0_nuniq ))
, 1 * char_length (char2_2 || char9_100 || varchar0_nuniq )
-- Expect char_length of 5 plus up to 9 for Varchar.
, 1 * octet_length (char2_2 || char9_100 || varchar0_nuniq)
, position  ( ' ' in varchar0_nuniq )
, substring ( varchar0_nuniq from 1 )
, trim ('   trim leading spaces ' || varchar0_nuniq)
, '2_2:' || char2_2 || ' 3_4:' || char3_4 || ' 4_n10:' || char4_n10 || ' 5_n20:' || char5_n20
, varchar0_nuniq || varchar0_nuniq
from BTA1P007 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """Create Table BTA1P008 
(
sbin0_4             Integer   --   default 3
not null
, varchar0_500        VarChar(11)  default 'GDAAIAAA'
not null
heading 'varchar0_500 no nulls'    

, ubin1_20            Numeric(9,0) unsigned        not null,
udec1_nuniq         Numeric(4,0) unsigned                ,    

char2_2             Char(2)               not null,
sbin2_nuniq         Largeint                           ,
sdec2_500           Numeric(9,0) signed          not null,    

udec3_n100          Numeric(9,0) unsigned                ,
ubin3_n2000         Numeric(4,0) unsigned                ,
char3_4             Char(8)                   not null,    

sdec4_n20           Numeric(4,0)                             ,
sbin4_n1000         Smallint                           ,
char4_n10           Char(8)                           ,    

char5_n20           Char(8)                       ,
sdec5_10            Numeric(9,0) signed          not null,
ubin5_n500          Numeric(9,0) unsigned                    ,    

sbin6_nuniq         Largeint                               ,
sdec6_4             Numeric(4,0) signed          not null,
char6_n100          Char(8)                           ,    

sbin7_n20           Smallint                               ,
char7_500           Char(8)                      not null,
udec7_n10           Numeric(4,0) unsigned                ,    

ubin8_10            Numeric(4,0) unsigned        not null,
char8_n1000         Char(8)                           ,
sdec8_4             Numeric(9,0) unsigned        not null,    

sdec9_uniq          Numeric(18,0) signed         not null,
char9_100           Char(2)                      not null,
ubin9_n4            Numeric(9,0) unsigned                    ,    

ubin10_n2           Numeric(4,0) unsigned                    ,
char10_nuniq        Char(8)                       ,
udec10_uniq         Numeric(9,0) unsigned        not null,    

udec11_2000         Numeric(9,0) unsigned        not null,
sbin11_100          Integer                      not null,
char11_uniq         Char(8)               not null,    

ubin12_2            Numeric(4,0) unsigned        not null,
sdec12_n1000        Numeric(18,0) signed                     ,
char12_n2000        Char(8)                           ,    

udec13_500          Numeric(9,0) unsigned        not null,
char13_1000         Char(8)               not null,    

sbin14_1000         Integer                      not null,
udec14_100          Numeric(4,0) unsigned        not null,
char14_n500         Char(8)                       ,    

sbinneg15_nuniq     Largeint                           ,
sdecneg15_100       Numeric(9,0) signed          not null,
char15_100          Char(8)               not null,    

ubin16_n10          Numeric(4,0) unsigned                    ,
sdec16_uniq         Numeric(18,0) signed         not null,
char16_n20          Char(5)        ,    

sbin17_uniq         Largeint   not null,
sdec17_nuniq        Numeric(18,0)                           ,
char17_2            Char(8)               not null
) no partition
--  catalog <global_dbvolume_part1>
--  organization R
--  audit
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    # Insert before making views (was previously OBEY file OBEYIN08).
    #
    stmt = """Insert Into BTA1P008 
Values ( 1, 'ACAABAAA   ', 2, 0,
'AA', 4942, 442, 84, 1584, 'AAAAAAAA',
13, 993, 'BDAAAAAA', 'AAAAAAAA', 0, 0, -- (5)
4942, 2, 'CRAAAAAA', 4, 'AAAACAAA', 4,
3, 'FCAAEAAA', 1, 0, 'AA', NULL,
NULL , 'ADAACAAC', 4942, 1584, 84, 'AJAAJAAE', -- (10)
1, 993, 'FCAAEAAB', 0, 'AAAAAAAA',
942, 42, 'AGAABAAA', -3584, -84, 'AJAAAAAA', -- (15)
3, 1993, 'BDAA ', 42154, 0, 'AAAAAAAA'
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """Insert Into BTA1P008 
Values ( 1, 'BBAAFAAA   ', 9, 1,
'BA', 3389, 389, 86, 186, 'CAAAAAAA',
13, 293, 'BDAAAAAA', 'BBAAAAAA', 1, 1, -- (5)
3389, 1, 'BOAAAAAA', 6, 'ECAAGAAA', 6,
3, 'DEAAEAAA', 1, 1, 'BB', NULL,
NULL, 'BBAAJAAE', 3389, 186, 86, 'EKAAEAAB', -- (10)
1, 293, 'DEAAEAAB', 1, 'BBAABAAA',
389, 89, 'BFAAFAAA', -186, -86, 'CLAAAAAA', -- (15)
3, 3293, 'BD   ', 32293, 1, 'BAAAAAAA'
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """Insert Into BTA1P008 
Values ( 3, 'CAAAGAAA   ', 4, 5,
'AA', 3264, 264, 91, 591, 'DAAAAAAA',
11, 151, 'BBAAAAAA', 'BAAAAAAA', 5, 5, -- (5)
3264, 0, 'AOAAAAAA', 11, 'BHAAIAAA', 1,
1, 'AEAAEAAA', 3, 5, 'BF', NULL,
NULL , 'CIAABAAE', 3264, 591, 91, 'BGAAEAAB', -- (10)
1, 151, 'AEAAEAAB', 5, 'FFAAFAAA',
264, 64, 'CAAAGAAA', -2591, -91, 'DQAAAAAA',
1, 4151, 'BB   ', 109174, 5, 'BAAAAAAA'
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """Insert Into BTA1P008 
Values ( 1, 'BBAABAAA   ', 5, 3,
'BA', 505, 5, 12, 1812, 'AAAAAAAA',
1, 701, 'BBAAAAAA', 'DDAAAAAA', 3, 3, -- (5)
505, 1, 'BFAAAAAA', 12, 'EEAAFAAA', 2,
1, 'GGAAKAAA', 1, 3, 'DD', NULL ,
NULL , 'BKAALAAA', 505, 1812, 12, 'EGAADAAC', -- (10)
1, 701, 'GGAAKAAB', 3, 'DDAADAAA',
505, 5, 'BBAABAAA', -3812, -12, 'AMAAAAAA',
1, 2701, 'BBAA ', 149840, 3, 'BAAAAAAA'
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """Insert Into BTA1P008 
Values ( 1, 'BBAADAAA   ', 5, 2,
'BA', 3585, 85, 13, 1013, 'BAAAAAAA',
17, 917, 'BCAAAAAA', 'CCAAAAAA', 2, 2, -- (5)
3585, 1, 'BKAAAAAA', 13, 'FFAAFAAA', 3,
7, 'EBAAEAAA', 1, 2, 'CC', NULL ,
NULL , 'BKAAKAAA', 3585, 1013, 13, 'FBAAMAAD', -- (10)
1, 917, 'EBAAEAAB', 2, 'CCAACAAA',
585, 85, 'BBAADAAA', -1013, -13, 'BNAAAAAA',
7, 3917, 'BCAA ', 59492, 2, 'AAAAAAAA'
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """Insert Into BTA1P008 
Values ( 0, 'BDAAAAAA   ', 3, 4,
'BA', 603, 103, 97, 697, 'BAAAAAAA',
8, 28, 'ADAAAAAA', 'AEAAAAAA', 4, 4, -- (5)
603, 3, 'DDAAAAAA', 17, 'CBAAGAAA', 7,
8, 'FEAAAAAA', 0, 4, 'AE', NULL ,
NULL , 'BJAAFAAD', 603, 697, 97, 'CCAAGAAC', -- (10)
0, 28, 'FEAAAAAA', 4, 'EEAAEAAA', 603,
3, 'BDAAAAAA', -2697, -97, 'BWAAAAAA',
8, 2028, 'AD   ', 56017, 4, 'AAAAAAAA'
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """create view  VNA1P008 
as  select * from BTA1P008 where sdec16_uniq > 3000
union -- CORRESPONDING
select * from BTA1P008 where sdec16_uniq < 2500
-- catalog <global_dbvolume_part1>
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table BTA1P009(
rownum   integer not null
, ch1n     char -- length defaults to 1.
, ch50n    char(50)
, ch49n    char(49)    

, vc1n     varchar(1) -- Requires explicit length
, vc50n    varchar(50) not null
, vc49n    varchar(49) not null    

, nm1n     numeric(1,0) -- 6/30/95 added precision & scale.
, nm180n   numeric(18,0)
, nm18n    numeric(18,18)
, nm90n    numeric(9,0) unsigned
, nm9n     numeric(9,9) unsigned    

, nm85n    numeric(8,5)
, nm85u    numeric(8,5) unsigned
-- Column name 'sin' changed to sint because 'sin'
-- was made into a reserved word in July 1998 for FCS.
, sint     smallint
, siun     smallint unsigned
, inun     integer unsigned
, inn      integer
, lin      largeint    

, dcn      numeric(1,0)
, dc180n   numeric(18,0)
, dc18n    numeric(18,18)
, dc90n    numeric(9,0) unsigned
, dc9n     numeric(9,9) unsigned    

, dc85n    numeric(8,5)
, dc85un   numeric(8,5) unsigned    

, iyearn   interval year to month
, idayn    interval day to second(2)
, ch287    char(287) not null
, ch288    char(288) not null
, vc287    varchar(287) not null
, vc288    varchar(288) not null    

, iyear    interval year to month not null
, iday     interval day to second -- fraction not null
, primary key (vc49n, vc50n, rownum)
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into BTA1P009 values (
1,
'S',  'This is a 50 character field', 'This is a 49 character field',
'V',  'This is a 50 character varchar field aaaaaaaaaaaaa',
'This is a 49 character varchar field bbbbbbbbbbbb',
-1, 123456789012345678, -0.123456789012345678, 123456789, 0.123456789,
-999.45678, 999.45678, -32768, 32766,   4294967295, -2147483648, -9.2233
,
0, 876543210987654321, -0.876543210987654321, 987654321, 0.987654321,
-999.54321, 999.54321,
null, null,
'This is a 287 character field', 'This is a 288 character field',
--       x x x x 1 x x x x 2 x x x x 3 x x x x 4 x x x x 5 x x x x 6 x x x x 7
'This is a 287 character varchar field cccccccccccccccccccccccccccccccc' ||
'cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc' ||
'cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc' ||
'cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc' ||
'ccccccc' ,
--       x x x x 1 x x x x 2 x x x x 3 x x x x 4 x x x x 5 x x x x 6 x x x x 7
'This is a 288 character varchar field dddddddddddddddddddddddddddddddd' ||
'dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd' ||
'dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd' ||
'dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd' ||
'dddddddd'
, interval '0-1' year to month
, interval '00:00:00:00.000001' day to second(6)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into BTA1P009 values (
2,
'S',  'This is a 50 character field', 'This is a 49 character field',
'V',  'This is a 50 character varchar field aaaaaaaaaaaaa',
'This is a 49 character varchar field bbbbbbbbbbbb',
-1, 123456789012345678, -0.123456789012345678, 123456789, 0.123456789,
-999.45678, 999.45678, 32767, 32760,   4294967295, -2147483648, -9.2233 ,
0, 876543210987654321, -0.876543210987654321, 987654321, 0.987654321,
-999.54321, 999.54321,
null, null,
'This is a 287 character field', 'This is a 288 character field',
--       x x x x 1 x x x x 2 x x x x 3 x x x x 4 x x x x 5 x x x x 6 x x x x 7
'This is a 287 character varchar field cccccccccccccccccccccccccccccccc' ||
'cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc' ||
'cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc' ||
'cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc' ||
'ccccccc' ,
--       x x x x 1 x x x x 2 x x x x 3 x x x x 4 x x x x 5 x x x x 6 x x x x 7
'This is a 288 character varchar field dddddddddddddddddddddddddddddddd' ||
'dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd' ||
'dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd' ||
'dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd' ||
'dddddddd'
, interval '1-08' year to month
, interval '00:00:00:00.0001' day to second(4)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into BTA1P009 values (
3,
'S',  'This is a 50 character field', 'This is a 49 character field',
'V',  'This is a 50 character varchar field aaaaaaaaaaaaa',
'This is a 49 character varchar field bbbbbbbbbbbb',
-1, 123456789012345678, -0.123456789012345678, 123456789, 0.123456789,
-999.45678, 999.45678, -32768, 32767,   4294967295, -2147483648, -9.2233
,
0, 876543210987654321, -0.876543210987654321, 987654321, 0.987654321,
-999.54321, 999.54321,
null, null,
'This is a 287 character field', 'This is a 288 character field',
--       x x x x 1 x x x x 2 x x x x 3 x x x x 4 x x x x 5 x x x x 6 x x x x 7
'This is a 287 character varchar field cccccccccccccccccccccccccccccccc' ||
'cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc' ||
'cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc' ||
'cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc' ||
'ccccccc' ,
--       x x x x 1 x x x x 2 x x x x 3 x x x x 4 x x x x 5 x x x x 6 x x x x 7
'This is a 288 character varchar field dddddddddddddddddddddddddddddddd' ||
'dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd' ||
'dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd' ||
'dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd' ||
'dddddddd'
, interval '1-1' year to month
, interval '00:00:00:00.0001' day to second(4)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into BTA1P009 values (
4,
'A',  'This is a 50 character field', 'This is a 49 character field',
'V',  'This is a 50 character varchar field aaaaaaaaaaaaa',
'This is a 49 character varchar field bbbbbbbbbbbb',
-1, 123456789012345678, -0.123456789012345678, 123456789, 0.123456789,
-999.45678, 999.45678, 32767, 32767,   4294967295, -2147483648, -9.2233 ,
0, 876543210987654321, -0.876543210987654321, 987654321, 0.987654321,
-999.54321, 999.54321,
null, null,
'This is a 287 character field', 'This is a 288 character field',
--       x x x x 1 x x x x 2 x x x x 3 x x x x 4 x x x x 5 x x x x 6 x x x x 7
'This is a 287 character varchar field cccccccccccccccccccccccccccccccc' ||
'cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc' ||
'cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc' ||
'cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc' ||
'ccccccc' ,
--       x x x x 1 x x x x 2 x x x x 3 x x x x 4 x x x x 5 x x x x 6 x x x x 7
'This is a 288 character varchar field dddddddddddddddddddddddddddddddd' ||
'dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd' ||
'dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd' ||
'dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd' ||
'dddddddd'
, interval '1-1' year to month
, interval '00:00:00:00.000001' day to second(6)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into BTA1P009 values (
5,
'A',  'This is a 50 character field', 'This is a 49 character field',
'V',  'This is a 50 character varchar field aaaaaaaaaaaaa',
'This is a 49 character varchar field cccccccccccc',
-1, 123456789012345678, -0.123456789012345678, 123456789, 0.123456789,
-999.45678, 999.45678, -32768, 30000,   4294967295, -2147483648, -9.2233
,
0, 876543210987654321, -0.876543210987654321, 987654321, 0.987654321,
-999.54321, 999.54321,
null, null,
'This is a 287 character field', 'This is a 288 character field',
--       x x x x 1 x x x x 2 x x x x 3 x x x x 4 x x x x 5 x x x x 6 x x x x 7
'This is a 287 character varchar field cccccccccccccccccccccccccccccccc' ||
'cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc' ||
'cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc' ||
'cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc' ||
'ccccccc' ,
--       x x x x 1 x x x x 2 x x x x 3 x x x x 4 x x x x 5 x x x x 6 x x x x 7
'This is a 288 character varchar field dddddddddddddddddddddddddddddddd' ||
'dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd' ||
'dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd' ||
'dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd' ||
'dddddddd'
, interval '1-1' year to month
, interval '00:00:00:00.000001' day to second(6)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into BTA1P009 values (
6,
'A',  'This is a 50 character field',
'This is a 49 character field',
'V',  'This is a 50 character varchar field aaaaaaaaaaaaa',
'This is a 49 character varchar field cccccccccccc',
-1, 123456789012345678, -0.123456789012345678, 123456789, 0.123456789,
-999.45678, 999.45678, 32767, 30000,   4294967295, -2147483648, -9.2233 ,
0, 876543210987654321, -0.876543210987654321, 987654321, 0.987654321,
-999.54321, 999.54321,
null, null,
'This is a 287 character field', 'This is a 288 character field',
--       x x x x 1 x x x x 2 x x x x 3 x x x x 4 x x x x 5 x x x x 6 x x x x 7
'This is a 287 character varchar field cccccccccccccccccccccccccccccccc' ||
'cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc' ||
'cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc' ||
'cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc' ||
'ccccccc' ,
--       x x x x 1 x x x x 2 x x x x 3 x x x x 4 x x x x 5 x x x x 6 x x x x 7
'This is a 288 character varchar field dddddddddddddddddddddddddddddddd' ||
'dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd' ||
'dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd' ||
'dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd' ||
'dddddddd'
, interval '0-1' year to month
, interval '00:00:00:00.000001' day to second(6)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into BTA1P009 values (
7,
'A',  'This is a 50 character field',
'This is a 49 character field',
'V',  'This is a 50 character varchar field aaaaaaaaaaaaa',
'This is a 49 character varchar field cccccccccccc',
-1, 123456789012345678, -0.123456789012345678, 123456789, 0.123456789,
-999.45678, 999.45678, -32768, 30000,   4294967295, -2147483648, -9.2233
,
0, 876543210987654321, -0.876543210987654321, 987654321, 0.987654321,
-999.54321, 999.54321,
null, null,
'This is a 287 character field', 'This is a 288 character field',
--       x x x x 1 x x x x 2 x x x x 3 x x x x 4 x x x x 5 x x x x 6 x x x x 7
'This is a 287 character varchar field cccccccccccccccccccccccccccccccc' ||
'cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc' ||
'cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc' ||
'cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc' ||
'ccccccc' ,
--       x x x x 1 x x x x 2 x x x x 3 x x x x 4 x x x x 5 x x x x 6 x x x x 7
'This is a 288 character varchar field dddddddddddddddddddddddddddddddd' ||
'dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd' ||
'dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd' ||
'dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd' ||
'dddddddd'
, interval '1-08' year to month
, interval '00:00:00:00.0001' day to second(4)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into BTA1P009 values (
8,
'A',  'This is a 50 character field',
'This is a 49 character field',
'V',  'This is a 50 character varchar field aaaaaaaaaaaaa',
'This is a 49 character varchar field cccccccccccc',
-1, 123456789012345678, -0.123456789012345678, 123456789, 0.123456789,
-999.45678, 999.45678, 32767, 30000,   4294967295, -2147483648, -9.2233 ,
0, 876543210987654321, -0.876543210987654321, 987654321, 0.987654321,
-999.54321, 999.54321,
null, null,
'This is a 287 character field', 'This is a 288 character field',
--       x x x x 1 x x x x 2 x x x x 3 x x x x 4 x x x x 5 x x x x 6 x x x x 7
'This is a 287 character varchar field cccccccccccccccccccccccccccccccc' ||
'cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc' ||
'cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc' ||
'cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc' ||
'ccccccc' ,
--       x x x x 1 x x x x 2 x x x x 3 x x x x 4 x x x x 5 x x x x 6 x x x x 7
'This is a 288 character varchar field dddddddddddddddddddddddddddddddd' ||
'dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd' ||
'dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd' ||
'dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd' ||
'dddddddd'
, interval '0-1' year to month
, interval '00:00:00:00.000001' day to second(6)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into BTA1P009 values (
9,
'A',  'This is a 50 character field',
'This is a 49 character field',
'V',  'This is a 50 character varchar field aaaaaaaaaaaaa',
'This is a 49 character varchar field bbbbbbbbbbbb',
-1, 123456789012345678, -0.123456789012345678, 123456789, 0.123456789,
-999.45678, 999.45678, -32768, 30000, 4294967295, -2147483648, -9.2233 ,
0, 876543210987654321, -0.876543210987654321, 987654321, 0.987654321,
-999.54321, 999.54321,
null, null,
'This is a 287 character field', 'This is a 288 character field',
--       x x x x 1 x x x x 2 x x x x 3 x x x x 4 x x x x 5 x x x x 6 x x x x 7
'This is a 287 character varchar field cccccccccccccccccccccccccccccccc' ||
'cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc' ||
'cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc' ||
'cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc' ||
'ccccccc' ,
--       x x x x 1 x x x x 2 x x x x 3 x x x x 4 x x x x 5 x x x x 6 x x x x 7
'This is a 288 character varchar field dddddddddddddddddddddddddddddddd' ||
'dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd' ||
'dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd' ||
'dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd' ||
'dddddddd'
, interval '0-1' year to month
, interval '00:00:00:00.000001' day to second(6)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into BTA1P009 values (
10,
'A',  'This is a 50 character field', 'This is a 49 character field',
'V',  'This is a 50 character varchar field aaaaaaaaaaaaa',
'This is a 49 character varchar field cccccccccccc',
-1, 123456789012345678, -0.123456789012345678, 123456789, 0.123456789,
-999.45678, 999.45678, -32767, 32767,   4294967295, -2147483648, -9.2233
,
0, 876543210987654321, -0.876543210987654321, 987654321, 0.987654321,
-999.54321, 999.54321,
null, null,
'This is a 287 character field', 'This is a 288 character field',
--       x x x x 1 x x x x 2 x x x x 3 x x x x 4 x x x x 5 x x x x 6 x x x x 7
'This is a 287 character varchar field cccccccccccccccccccccccccccccccc' ||
'cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc' ||
'cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc' ||
'cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc' ||
'ccccccc' ,
--       x x x x 1 x x x x 2 x x x x 3 x x x x 4 x x x x 5 x x x x 6 x x x x 7
'This is a 288 character varchar field dddddddddddddddddddddddddddddddd' ||
'dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd' ||
'dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd' ||
'dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd' ||
'dddddddd'
, interval '0-1' year to month
, interval '00:00:00:00.000001' day to second(6)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into BTA1P009 values (
11,
'A',  'This is a 50 character field', 'This is a 49 character field',
'V',  'This is a 50 character varchar field aaaaaaaaaaaaa',
'This is a 49 character varchar field bbbbbbbbbbbb',
-1, 123456789012345678, -0.123456789012345678, 123456789, 0.123456789,
-999.45678, 999.45678, -32767, 32767,   4294967295, -2147483648, -9.2233
,
0, 876543210987654321, -0.876543210987654321, 987654321, 0.987654321,
-999.54321, 999.54321,
null, null,
'This is a 287 character field', 'This is a 288 character field',
--       x x x x 1 x x x x 2 x x x x 3 x x x x 4 x x x x 5 x x x x 6 x x x x 7
'This is a 287 character varchar field cccccccccccccccccccccccccccccccc' ||
'cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc' ||
'cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc' ||
'cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc' ||
'ccccccc' ,
--       x x x x 1 x x x x 2 x x x x 3 x x x x 4 x x x x 5 x x x x 6 x x x x 7
'This is a 288 character varchar field dddddddddddddddddddddddddddddddd' ||
'dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd' ||
'dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd' ||
'dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd' ||
'dddddddd'
, interval '99-11' year to month
, interval '99:23:59:59.999999' day to second(6)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into BTA1P009 values (
12,
'S',  'This is a 50 character field', 'This is a 49 character field',
'V',  'This is a 50 character varchar field aaaaaaaaaaaaa',
'This is a 49 character varchar field bbbbbbbbbbbb',
-1, 123456789012345678, -0.123456789012345678, 123456789, 0.123456789,
-999.45678, 999.45678, -32767, 32767,   4294967295, -2147483648, -9.2233
,
0, 876543210987654321, -0.876543210987654321, 987654321, 0.987654321,
-999.54321, 999.54321,
null, null,
'This is a 287 character field', 'This is a 288 character field',
--       x x x x 1 x x x x 2 x x x x 3 x x x x 4 x x x x 5 x x x x 6 x x x x 7
'This is a 287 character varchar field cccccccccccccccccccccccccccccccc' ||
'cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc' ||
'cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc' ||
'cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc' ||
'ccccccc' ,
--       x x x x 1 x x x x 2 x x x x 3 x x x x 4 x x x x 5 x x x x 6 x x x x 7
'This is a 288 character varchar field dddddddddddddddddddddddddddddddd' ||
'dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd' ||
'dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd' ||
'dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd' ||
'dddddddd'
, interval '99-11' year to month
, interval '99:23:59:59.999999' day to second(6)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into BTA1P009 values (
13,
'A',  'This is a 50 character field', 'This is a 49 character field',
'V',  'This is a 50 character varchar field aaaaaaaaaaaaa',
'This is a 49 character varchar field bbbbbbbbbbbb',
-1, 123456789012345678, -0.123456789012345678, 123456789, 0.123456789,
-999.45678, 999.45678, -32767, 32767,   4294967295, -2147483648, -9.2233
,
0, 876543210987654321, -0.876543210987654321, 987654321, 0.987654321,
-999.54321, 999.54321,
null, null,
'This is a 287 character field', 'This is a 288 character field',
--       x x x x 1 x x x x 2 x x x x 3 x x x x 4 x x x x 5 x x x x 6 x x x x 7
'This is a 287 character varchar field cccccccccccccccccccccccccccccccc' ||
'cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc' ||
'cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc' ||
'cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc' ||
'ccccccc' ,
--       x x x x 1 x x x x 2 x x x x 3 x x x x 4 x x x x 5 x x x x 6 x x x x 7
'This is a 288 character varchar field dddddddddddddddddddddddddddddddd' ||
'dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd' ||
'dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd' ||
'dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd' ||
'dddddddd'
, interval '99-11' year to month
, interval '99:23:59:59.999999' day to second(6)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into BTA1P009 values (
14,
'A',  'This is a 50 character field', 'This is a 49 character field',
'V',  'This is a 50 character varchar field aaaaaaaaaaaaa',
'This is a 49 character varchar field bbbbbbbbbbbb',
-1, 123456789012345678, -0.123456789012345678, 123456789, 0.123456789,
-999.45678, 999.45678, -32767, 32767,   4294967295, -2147483648, -9.2233
,
0, 876543210987654321, -0.876543210987654321, 987654321, 0.987654321,
-999.54321, 999.54321,
null, null,
'This is a 287 character field', 'This is a 288 character field',
--       x x x x 1 x x x x 2 x x x x 3 x x x x 4 x x x x 5 x x x x 6 x x x x 7
'This is a 287 character varchar field cccccccccccccccccccccccccccccccc' ||
'cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc' ||
'cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc' ||
'cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc' ||
'ccccccc' ,
--       x x x x 1 x x x x 2 x x x x 3 x x x x 4 x x x x 5 x x x x 6 x x x x 7
'This is a 288 character varchar field dddddddddddddddddddddddddddddddd' ||
'dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd' ||
'dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd' ||
'dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd' ||
'dddddddd'
, interval '99-11' year to month
, interval '99:23:59:59.999999' day to second(6)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """create view  VNA1P009 (csimple, csearched) as select
-- Simple CASE:
CASE rownum WHEN 1 THEN 'Value A'
WHEN 2 THEN 'Value B'
WHEN 3 THEN 'Value C'
ELSE 'Value D -- Rowcount > 3'
END
-- Searched CASE:
,   CASE when rownum > 10 then 'rownum over 10'
when sint  = -32768 then 'sint is the lowest'
else 'the great unknown'
END
from BTA1P009 
where rownum < CASE
when rownum between 7 and 12   then 2222
when rownum between 1 and 2   then rownum+1
else rownum
end
--  catalog <global_dbvolume_part1>
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

