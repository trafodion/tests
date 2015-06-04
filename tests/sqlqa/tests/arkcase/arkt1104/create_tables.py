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
    
    # ---------------------------
    # Description:  Create order-entry database with Grouped views.
    # ---------------------------
    
    stmt = """CREATE TABLE FROMSUP (
partnum                PIC 9(4)  not null,
suppnum                PIC 9(3)  not null,
partcost               PIC 9(6)V9(2) COMP not null,
PRIMARY KEY ( partnum, suppnum )
)
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE SUPPLIER (
suppnum                PIC 9(3)   not null,
suppname               PIC X(18)  not null,
address                PIC X(22)  not null,
city                   PIC X(14)  not null,
state                  PIC X(12)  not null,
PRIMARY KEY (suppnum)
)
;"""
    output = _dci.cmdexec(stmt)
    # Jan 15, 1998 == comment out INdex to avoid SQL death.
    # Feb 12 (980106Beta) Fixed Jan 30 (good luck!)
    stmt = """CREATE INDEX SUPPLYR0 ON SUPPLIER ( suppname ) ;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """set param ?p 92000.00;"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO FROMSUP VALUES ( 212,  1, ?p );"""
    output = _dci.cmdexec(stmt)
    # INSERT INTO FROMSUP VALUES ( 212,  1, 92000.00);
    
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
    #
    stmt = """update statistics for table FROMSUP;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO SUPPLIER VALUES (1,'TANDEM COMPUTERS'
,'19333 VALLCO PARKWAY','CUPERTINO     ','CALIFORNIA  ');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO SUPPLIER VALUES (2,'DATA TERMINAL CO'
,'2000 BAKER STREET   ','IRVINE        ','CALIFORNIA  ');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO SUPPLIER VALUES (3,'DISPLAY INC'
,'7600 EMERSON        ','PALO ALTO     ','CALIFORNIA  ');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO SUPPLIER VALUES (6,'INFORMATION STORAG'
,'1000 INDUSTRY DRIVE ','LEXINGTON','MASS        ');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO SUPPLIER VALUES (8,'MAGNETICS CORP'
,'7777 FOUNTAIN WAY   ','SEATTLE       ','WASHINGTON  ');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO SUPPLIER VALUES (10,'STEELWORK INC'
,'6000 LINCOLN LANE   ','SUNNYVALE','CALIFORNIA  ');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO SUPPLIER VALUES (15,'DATADRIVE'
,'100  MACARTHUR      ','DALLAS        ','TEXAS       ');"""
    output = _dci.cmdexec(stmt)
    
    stmt = """update statistics for table SUPPLIER;"""
    output = _dci.cmdexec(stmt)
    stmt = """select * from SUPPLIER;"""
    output = _dci.cmdexec(stmt)
    
    # ---------------------------
    # Description:  Create order-entry database: CREATE GROUPED VIEWs.
    # ---------------------------
    
    stmt = """CREATE VIEW GFROMSUP as
select * from FROMSUP 
GROUP BY partnum, suppnum, partcost
;"""
    output = _dci.cmdexec(stmt)
    stmt = """CREATE VIEW GSUPPLY( suppnum, suppname, address, city, state) as
select max(suppnum), suppname, address, min(city), min(state)
from SUPPLIER 
GROUP BY suppnum, suppname, address, city, state
;"""
    output = _dci.cmdexec(stmt)
    
    # Create tables; views are created in testcase scripts.
    
    stmt = """create table T1A ( vch7 varchar(7)
, nint integer
, ch3 char(3)
, nnum9 numeric(9,2)
, ch4 char(4)
, nnum5 numeric(5,1)
, vch5 varchar(5)
, nsint smallint signed
) no partition;"""
    output = _dci.cmdexec(stmt)
    
    # Because of bug reported for testA11, enter these values
    # for varchar of different length separately.
    
    # Use literal blank until DEFAULT supported.
    #                     ('a',      1,'c' ,0.9,   DEFAULT ,NULL  ,NULL,0)
    
    stmt = """insert into T1A values
('a',      1,'c' ,0.9,       ''  ,NULL  ,NULL,0)
, ('b',      4,'c' ,1234567.89,'e' ,1234.5,'c' ,12345)
;"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into T1A values
('abcdefg',3,'cc',0.09,    'alph',2     ,'cc',1)
, ('AbCdEfG',5,'cC',0.09,      'Cc',2     ,'cc',2)
;"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into T1A values
('cc'     ,2,'cc',2.00,      'cc',2.0   ,'cc',2)
;"""
    output = _dci.cmdexec(stmt)
    stmt = """select * from T1A 
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    stmt = """select nint , nnum9 , nnum5 , nsint from T1A 
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    stmt = """select vch7||'w', ch3||'x' , ch4||'y' , vch5||'z' from T1A 
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    stmt = """invoke T1A 
;"""
    output = _dci.cmdexec(stmt)
    stmt = """showddl T1A 
;"""
    output = _dci.cmdexec(stmt)
    
    # ---------------------------
    # INSERT and UPDATE of updateable views with data from Grouped Views.
    # Create table and view to receive data for INSERT into updateable view
    # of the result of Single-row and multi-row Selects executed.
    # ---------------------------
    
    stmt = """create table T4INSERT 
( v1   varchar(8)
, n2   integer
, c3   char(3)
, n4   numeric(9,2)
, c5   char(4)
, n6   numeric(5,1)
, v7   varchar(5)
, n8   smallint
) no partition;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create view V4INSERT as
select v1,v7,n2,n4,n6,n8,c3,c5 from T4INSERT 
where n2 < 100
;"""
    output = _dci.cmdexec(stmt)
    
    # Empty table, also to be used for inserts.
    stmt = """create table TEMPT 
( ch3  char(3)
, vch5 varchar(5)
) no partition
;"""
    output = _dci.cmdexec(stmt)
    
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
-- audit
-- extent (2500,64)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
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
    #
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
    
    stmt = """create view  VNA1P005 ( n1, c2, c3, c4 ) as
select cast( max(t1.sbinneg15_nuniq) as smallint signed )
, min(t1.char2_2)
, min(t2.char2_2)
, max(t3.char3_4)
from BTA1P005 t1
right join BTA1P005 t2 on t1.char2_2   = t2.char3_4
left  join BTA1P005 t3 on t2.char2_2   = t3.char3_4
group by t1.sbinneg15_nuniq , t1.char2_2 , t2.char2_2 , t3.char3_4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

