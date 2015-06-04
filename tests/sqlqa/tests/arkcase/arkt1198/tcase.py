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
    
def test001(desc="""a01"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     T1198:A01
    #  Description:        This test verifies the creation and population
    #                      of SQL Partitioned DB#11 Global Table 1
    #                      and its view; includes INSERT, SELECT.
    #
    # =================== End Test Case Header  ===================
    #
    # Make sure all transactions are small by committing each statement
    # immediately (default behavior in Release 1).
    stmt = """Set Transaction Autocommit On;"""
    output = _dci.cmdexec(stmt)
    #
    # DDL: Create Table, view.
    
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
not droppable
) number of partitions 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    # Create View of all rows and columns; updateable.
    stmt = """Create view VUA1P001 
As Select * From BTA1P001 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    #   No indexes.
    #
    # Create Like, with same partitions.
    stmt = """Create Table BTALike1 
Like BTA1P001 
With CONSTRAINTS
with partitions
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # DML: Insert, select.
    #
    # Table 1
    #
    stmt = """Set Transaction Autocommit On;"""
    output = _dci.cmdexec(stmt)
    #
    # INSERT.
    #
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
    #
    stmt = """Update Statistics For Table BTA1P001 on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    #  SELECT.
    #
    stmt = """SELECT varchar5_10, ubin15_uniq, char0_10
FROM BTA1P001 
ORDER BY 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s0')
    
    stmt = """SELECT varchar5_10, ubin15_uniq, char0_10
FROM VUA1P001 
ORDER BY 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s1')
    #
    #  Aggregates.
    #  Expect {6} for each.
    stmt = """SELECT count(*) from BTA1P001;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s2')
    stmt = """SELECT count(*) from VUA1P001;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s3')
    #
    # Set Insert and Select.
    #
    stmt = """Insert Into BTALike1 
Select * From BTA1P001 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 6)
    #
    stmt = """Select varchar5_10, ubin15_uniq, char0_10
From BTALike1 
Order By 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s4')
    
    stmt = """create table range_partition_test 
(number largeint not null not droppable,
text char (20),
primary key (number))
range partition (add first key (1000000000) location """ + gvars.g_disc1 + """);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # G06.25 R2 ABO mx0121 RoadRunner: rand() is not supported
    stmt = """insert into range_partition_test 
select rand(),'' from (values((1)),((1)),((1)),((1)),((1)),((1)),((1)),
((1)),((1)),((1))) as t1(t);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4313')
    
    stmt = """select * from range_partition_test;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """select * from range_partition_test where number = 1097974834;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """create table single_partition_test (number largeint not null not droppable
, primary key (number));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into single_partition_test select rand() from (values((1)),((1)),
((1)),((1)),((1)),((1)),((1)),((1)),((1)),((1))) as t1(t),(values((1)),((1))
,((1)),((1)),((1)),((1)),((1)),((1)),((1)),((1))) as t2(t),
(values((1)),((1)),((1)),((1)),((1)),((1)),((1)),((1)),((1)),((1))) as t3(t);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4313')
    
    stmt = """create table hash_partition_test (number largeint not null not droppable,
primary key (number)) hash partition (add location """ + gvars.g_disc1 + """);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into hash_partition_test select rand() from
(values((1)),((1)),((1)),((1)),((1)),((1)),((1)),((1)),((1)),((1))) as t1(t),
(values((1)),((1)),((1)),((1)),((1)),((1)),((1)),((1)),((1)),((1))) as t2(t),
(values((1)),((1)),((1)),((1)),((1)),((1)),((1)),((1)),((1)),((1))) as t3(t);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4313')
    
    # ERROR[2005] Internal error: from compilation, no errors in diagnostics yet f
    # statement: showplan insert into range_partition_test   select rand(),'' from
    # values((1)),((1))) as t1(t);
    stmt = """showplan insert into range_partition_test 
select rand(),'' from (values((1)),((1))) as t1(t);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4313')
    
    _testmgr.testcase_end(desc)

def test002(desc="""a02"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     T1198:A02
    #  Description:        This test verifies the creation and population
    #                      of SQL Partitioned DB#11 Global Table 2
    #                      and its view; includes INSERT, SELECT.
    #
    # =================== End Test Case Header  ===================
    #
    # Make sure all transactions are small by committing each statement
    # immediately (default behavior in Release 1).
    stmt = """Set Transaction Autocommit On;"""
    output = _dci.cmdexec(stmt)
    #
    # DDL: Create Table, view.
    # Similar to table of same name in arkt1199.
    #
    # Table 2 and Create Like.
    #
    
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
) number of partitions 3
ATTRIBUTE --NO AUDIT,
NO AUDITCOMPRESS
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    stmt = """Create View VNA1P002 As
Select cast(char17_100 as varchar(20)) as char17_100
, udec17_100
From BTA1P002 
Group By char17_100 , udec17_100
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    stmt = """Create INDEX IXA1P002a ON BTA1P002 ( varchar0_4 )
LOCATION """ + gvars.g_disc2 + """
RANGE PARTITION ( ADD first key ('C') LOCATION """ + gvars.g_disc3 + """ )
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """Create INDEX IXA1P002b ON BTA1P002 ( sdec13_uniq )
LOCATION """ + gvars.g_disc3 + """
RANGE PARTITION ( ADD first key (2000) LOCATION """ + gvars.g_disc2 + """ )
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    # Create Like, with same partitions.
    stmt = """Create Table BTALike2 
Like BTA1P002 
With CONSTRAINTS
With Partitions
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """Set Transaction Autocommit On;"""
    output = _dci.cmdexec(stmt)
    #
    # INSERT.
    
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
    #
    stmt = """Update Statistics For Table BTA1P002 on every column;"""
    output = _dci.cmdexec(stmt)
    #
    #  SELECT.
    #
    #  Look at table.
    #
    #  Check values in the primary key, defined as DESC.
    stmt = """select ubin3_uniq
from BTA1P002 
order by 1 DESC ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s0')
    #
    #  Check rows in base table used in view.
    stmt = """select cast(char17_100 as varchar(20)) as char17_100
, udec17_100
from BTA1P002 
group by char17_100 , udec17_100
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s1')
    #
    stmt = """select ubin3_uniq -- DESC key.
from BTA1P002 
order by 1 DESC ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s2')
    #
    #  Sample some columns in indexes.
    stmt = """select varchar0_4, char0_20, sdec13_uniq
from BTA1P002 order by 1, 2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s3')
    #
    #  Check view.
    # select *
    stmt = """Select cast(char17_100 as varchar(20)) as char17_100
, udec17_100
from VNA1P002 
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s4')
    #
    #  Aggregates.
    #  Expect ( (7) ) for each.
    stmt = """SELECT count(*) from BTA1P002;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s5')
    stmt = """SELECT count(*) from VNA1P002;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s6')
    #
    # Set Insert and Select.
    #
    stmt = """Insert Into BTALike2 
Select * From BTA1P002 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 7)
    #
    stmt = """select cast(char17_100 as varchar(20)) as char17_100
, udec17_100
, cast(char20_10 as varchar(40)) as char20_10
from BTALike2 
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s7')
    
    _testmgr.testcase_end(desc)

def test003(desc="""a03"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     T1198:A03
    #  Description:        This test verifies the creation and population
    #                      of SQL Partitioned DB#11 Global Table 3
    #                      and its view; includes INSERT, SELECT.
    #
    # =================== End Test Case Header  ===================
    #
    # Make sure all transactions are small by committing each statement
    # immediately (default behavior in Release 1).
    stmt = """Set Transaction Autocommit On;"""
    output = _dci.cmdexec(stmt)
    #
    # DDL: Create Table, view.
    # Similar to table of same name in arkt1199.
    #
    # Table 3 and Create Like.
    
    stmt = """Create Table BTA1P003 
(
varchar0_100     VarChar(1000)        ,
char0_1000       PIC X(32)            ,    

sbin1_100        Numeric(9,0) signed  ,
char1_4          PIC X(5)             ,
ubin1_4          Numeric(9,0) unsigned,    

char2_2          Char(2)              ,
varchar2_10      VarChar(15) not null ,
varchar2_100     VarChar(25)          ,    

sbin3_1000       Numeric(5,0) signed  ,
char3_1000       PIC X(240)           ,
ubin3_uniq       Numeric(5,0) unsigned,    

sbin4_2          Numeric(1,1) signed  ,
ubin4_4          Numeric(1,1) unsigned,
varchar4_1000    VarChar(16)          ,
sdec4_10         Numeric(1,1) signed  ,
udec4_2          Numeric(1,1) unsigned,    

sbin5_4          Numeric(4,0) signed  ,
ubin5_20         Numeric(9,0) unsigned,
udec5_20         Numeric(4,0) unsigned,
varchar5_4       VarChar(8)           ,
sdec5_100        Numeric(18,0) signed ,    

varchar6_20      VarChar(32)          ,    

sbin7_2          SMALLINT signed      ,
sdec7_10         Numeric(4,1) signed  ,
char7_uniq       Char(100)            ,
udec7_20         Numeric(4,1) unsigned,
ubin7_100        SMALLINT unsigned    ,    

sbin8_1000       Numeric(18,0) signed ,
varchar8_uniq    VarChar(32)          ,
ubin8_2          Numeric(4,1) unsigned,    

char9_uniq       Char(8)              ,
udec9_10         Numeric(5,0) unsigned,
sdec9_20         Numeric(5,0) signed  ,    

varchar10_20     VarChar(32)          ,    

sdec11_20        Numeric(5,5) signed  ,
varchar11_2      VarChar(32) not null ,
char11_4         Char(2)              ,    

sbin12_1000      Numeric(9,0) signed  ,
varchar12_4      VarChar(32)          ,
ubin12_10        Numeric(9,0) unsigned,    

char13_100       Char(5)              ,
sdec13_uniq      Numeric(9,0) signed  ,
udec13_500       Numeric(9,0) unsigned,    

sbin14_100       Numeric(2,0) signed  ,
ubin14_2         Numeric(2,0) unsigned,
sdec14_20        Numeric(2,0) signed  ,
udec14_10        Numeric(2,0) unsigned,
varchar14_2000   VarChar(64)          ,    

sbin15_2         INTEGER signed       ,
udec15_4         Numeric(9,2) unsigned,
varchar15_uniq   VarChar(8)  not null ,
ubin15_uniq      INTEGER unsigned     ,
sdec15_10        Numeric(9,2) signed  ,    

sbin16_20        Numeric(9,2) signed  ,
ubin16_1000      Numeric(9,2) unsigned,
varchar16_100    VarChar(128)         ,    

sbin17_uniq      Numeric(10,0) signed ,
sdec17_20        Numeric(2,0) signed  ,
char17_100       Char(100)            ,
varchar17_20     VarChar(240)         ,    

sbin18_uniq      Numeric(18,0) signed ,
varchar18_uniq   VarChar(60)          ,    

sbin19_4         LARGEINT signed      ,
char19_2         Char(8)              ,
ubin19_10        SMALLINT unsigned    ,
udec19_100       Numeric(4,1) signed  ,
sdec19_1000      Numeric(4,1) unsigned,    

varchar20_1000   VarChar(100)    

-- The following column sequence gives more than one
-- identical value in the first column of the primary key.
, primary  key ( varchar11_2 DESC
, varchar2_10     ASC
, varchar15_uniq  ASC
) NOT DROPPABLE
) number of partitions 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    # Create View of a few rows, all columns; should be updateable.
    stmt = """create view  VUA1P003 as
select *
from BTA1P003 
where ubin15_uniq > 1000
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    # 2 Indexes.
    # ? Hanging on varchar index.
    stmt = """Create Index IXA1P003a On BTA1P003 ( varchar2_100 Desc )
Location """ + gvars.g_disc1 + """
range Partition ( ADD First Key ('B') Location """ + gvars.g_disc2 + """
, ADD First Key ('D') Location """ + gvars.g_disc3 + """
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    # ? Hanging on varchar index.
    stmt = """Create Index IXA1P003b On BTA1P003 ( varchar2_10 Desc )
Location """ + gvars.g_disc3 + """
range Partition ( ADD First Key ('AB') Location """ + gvars.g_disc2 + """
, ADD First Key ('BA') Location """ + gvars.g_disc1 + """
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    # Create Like, with same partitions.
    stmt = """Create Table BTALike3 
Like BTA1P003 
With Partitions
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # DML: Insert, select.
    stmt = """Set Transaction Autocommit On;"""
    output = _dci.cmdexec(stmt)
    #
    # INSERT.
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
    stmt = """Update Statistics For Table BTA1P003 on every column;"""
    output = _dci.cmdexec(stmt)
    #
    #  SELECT.
    #
    #  Look at table.
    #
    #  Check values in the primary key, defined as DESC/ASC/ASC.
    stmt = """Select varchar11_2
, varchar2_10
, varchar15_uniq
From BTA1P003 
Order By 1, 2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s0')
    #
    #  Check values in indexes.
    stmt = """Select varchar2_10
From BTA1P003 
Order By 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s1')
    stmt = """Select varchar2_100
From BTA1P003 
Order By 1 Desc ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s2')
    #  Some CHAR and VARCHAR columns:
    stmt = """Select varchar0_100
From BTA1P003 
Order By 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s3')
    stmt = """Select char0_1000 , char1_4
From BTA1P003 
Order By 1, 2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s4')
    stmt = """Select sbin18_uniq , udec19_100 , sdec19_1000
From BTA1P003 
Order By 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s5')
    #
    #  Check value of view predicate column.
    #
    stmt = """select ubin15_uniq from BTA1P003 Order By 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s6')
    stmt = """select ubin15_uniq from VUA1P003 Order By 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s7')
    #
    #  Look at view.
    #
    stmt = """select varchar0_100
From VUA1P003 
Order By 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s8')
    #
    stmt = """select ubin3_uniq , udec4_2 , char9_uniq , varchar16_100
From VUA1P003 
Order By 1, 2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s9')
    #
    stmt = """select varchar20_1000
From VUA1P003 
Order By 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s10')
    #
    #  Aggregates.
    #  Expect ( (4) ) for table, ( (3) ) for view.
    stmt = """SELECT count(*) from BTA1P003;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s11')
    stmt = """SELECT count(*) from VUA1P003;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s12')
    # updateable.
    #
    # Set Insert and Select.
    #
    stmt = """Insert Into BTALike3 
Select * From BTA1P003 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 4)
    #
    stmt = """Select varchar11_2
, varchar2_10
, varchar15_uniq
From BTALike3 
Order By 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s13')
    
    _testmgr.testcase_end(desc)

def test004(desc="""a04"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     T1198:A04
    #  Description:        This test verifies the creation and population
    #                      of SQL Partitioned DB#11 Global Table 4
    #                      and its view; includes INSERT, SELECT.
    #
    # =================== End Test Case Header  ===================
    #
    # Make sure all transactions are small by committing each statement
    # immediately (default behavior in Release 1).
    stmt = """Set Transaction Autocommit On;"""
    output = _dci.cmdexec(stmt)
    #
    # DDL: Create Table, view.
    # Similar to table of same name in arkt1199.
    #
    # Table 4 and Create Like.
    #
    
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
) number of partitions 3
ATTRIBUTE NO AUDITCOMPRESS
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    # Create View; non-updateable, because of grouping operations.
    # Purpose: (1) test multi-column row value constructor in HAVING.
    #          (2) provide a view whose use tests Grouped Views
    #              for no extra cost of testware development.
    stmt = """Create View VNA1P004 as
select varchar0_4     , char0_1000 , sbin7_2
, varchar5_10    , char6_20   , ubin15_uniq
, varchar15_uniq , char16_uniq
from BTA1P004 
where ubin15_uniq > 1000
group by   varchar0_4     , char0_1000 , sbin7_2
, varchar5_10    , char6_20   , ubin15_uniq
, varchar15_uniq , char16_uniq
having (  varchar0_4 , 'ACAAA' , varchar15_uniq )
<> ( 'CAA' , varchar5_10 , 'EJAAJAA' )
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    # 2 Indexes.
    stmt = """Create Index IXA1P004a On BTA1P004 ( char0_1000 )
Location """ + gvars.g_disc2 + """
range Partition ( ADD First Key ('BJ') Location """ + gvars.g_disc3 + """
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    stmt = """Create Index IXA1P004b On BTA1P004 ( varchar0_4 )
Location """ + gvars.g_disc2 + """
range Partition ( ADD First Key ('J') Location """ + gvars.g_disc1 + """
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    # Create Like, with same partitions.
    stmt = """Create Table BTALike4 
Like BTA1P004 
--      With Horizontal Partitions
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """Set Transaction Autocommit On;"""
    output = _dci.cmdexec(stmt)
    #
    # INSERT.
    #
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
    # Added the last 4 rows as in unpartitioned global database #11 so that
    # data matches in the partitioned and unpartitioned databases!
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
    #
    stmt = """Update Statistics For Table BTA1P004 on every column;"""
    output = _dci.cmdexec(stmt)
    #
    #  SELECT.
    #
    #  Look at table:
    #
    #  Check values in the primary key.
    stmt = """select varchar13_100
, sdec13_uniq
, char14_20
, varchar15_uniq
from BTA1P004 
order by 1 DESC, 2, 3, 4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s0')
    #
    #  Indexes.
    #
    stmt = """Select char0_1000
From BTA1P004 
Order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s1')
    stmt = """Select varchar0_4
From BTA1P004 
Order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s2')
    #
    stmt = """select varchar0_4     , char0_1000 , sbin7_2
, varchar5_10    , char6_20   , ubin15_uniq
, varchar15_uniq , char16_uniq
from BTA1P004 order by 1, 2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s3')
    #
    stmt = """select sbin5_4 , ubin5_20 , udec5_20 , varchar5_10 , sdec5_100
from BTA1P004 order by 1,2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s4')
    #
    stmt = """select sbin18_uniq   , char18_20
from BTA1P004 order by 1,2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s5')
    #
    #  Look at view:
    #
    #  Expected result of view is 12 of 13 rows in table, with
    #  this row is omitted:
    #  CAA         1  ACAAA        CCAAAAAA         3889  EJAAJAA         EJAAJAAC
    #
    stmt = """select varchar0_4 , sbin7_2
, varchar5_10    , char6_20   , ubin15_uniq
, varchar15_uniq , char16_uniq
from VNA1P004 order by 1, 2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s6')
    #
    #  Aggregates.
    #  Expect ( (13) ) for table, ( (12) ) for view.
    stmt = """SELECT count(*) from BTA1P004;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s7')
    stmt = """SELECT count(*) from VNA1P004;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s8')
    #
    # Set Insert and Select.
    #
    stmt = """Insert Into BTALike4 
Select * From BTA1P004 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 13)
    #
    stmt = """Select sbin19_4 , char19_2 , ubin19_10 , udec19_100
, sdec19_1000 , char20_10
From BTALike4 
Order By 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s9')
    stmt = """Select varchar0_4 , char0_1000 , sbin1_100
, char1_4 , ubin1_4
From BTALike4 t1
Order By 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s10')
    
    _testmgr.testcase_end(desc)

def test005(desc="""a05"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     T1198:A05
    #  Description:        This test verifies the creation and population
    #                      of SQL Partitioned DB#11 Global Table 5
    #                      and its view; includes INSERT, SELECT.
    #
    # =================== End Test Case Header  ===================
    #
    # Make sure all transactions are small by committing each statement
    # immediately (default behavior in Release 1).
    stmt = """Set Transaction Autocommit On;"""
    output = _dci.cmdexec(stmt)
    #
    # DDL: Create Table, view.
    # Similar to table of same name in arkt1199.
    # Table 5 and Create Like.
    #
    
    stmt = """Create Table BTA1P005 
(
char0_n10           Char(2)
default 'AD'
heading 'char0_n10 with default AD'    

, sbin0_uniq          Smallint not null,
sdec0_n500          Numeric(18,0) ,    

ubin1_n2            Numeric(4,0) unsigned
, udec1_100           Numeric(2,0) unsigned not null,    

char2_2             Char(2)               not null,
sbin2_nuniq         Largeint              ,
sdec2_500           Numeric(9,0) signed   not null,    

udec3_n100          Numeric(9,0) unsigned ,
ubin3_n2000         Numeric(4,0) unsigned ,
char3_4             Char(8)               not null    

, sdec4_n20           Numeric(4,0)          ,
sbin4_n1000         Smallint              ,
char4_n10           Char(8)               ,    

char5_n20           Char(8)               ,
sdec5_10            Numeric(9,0) signed   not null,
ubin5_n500          Numeric(9,0) unsigned    

, sbin6_nuniq         Largeint              ,
sdec6_4             Numeric(4,0) signed   not null,
char6_n100          Char(8)               ,    

sbin7_n20           Smallint              ,
char7_500           Char(8)               not null,
udec7_n10           Numeric(4,0) unsigned    

, ubin8_10            Numeric(4,0) unsigned not null,
char8_n1000         Char(8)               ,
sdec8_4             Numeric(9,0) unsigned not null,    

sdec9_uniq          Numeric(18,0) signed  not null,
char9_100           Char(2)               not null,
ubin9_n4            Numeric(9,0) unsigned    

, ubin10_n2           Numeric(4,0) unsigned ,
char10_nuniq        Char(8)               ,
udec10_uniq         Numeric(9,0) unsigned not null,    

cReal               REAL                  not null,
cFloat              FLOAT(10)             not null,    

udec11_2000         Numeric(9,0) unsigned not null,
sbin11_100          Integer               not null,
char11_uniq         Char(8)               not null    

, ubin12_2            Numeric(4,0) unsigned not null    

, sdec12_n1000        Numeric(18,0) signed  ,
char12_n2000        Char(8)    

, udec13_500          Numeric(9,0) unsigned not null,
char13_1000         Char(8)               not null    

, sbin14_1000         Integer               not null,
udec14_100          Numeric(4,0) unsigned not null,
char14_n500         Char(8)               ,    

sbinneg15_nuniq     Largeint              ,
sdecneg15_100       Numeric(9,0) signed   not null,
char15_100          Char(8)               not null    

, ubin16_n10          Numeric(4,0) unsigned
, sdec16_uniq         Numeric(18,0) signed  not null,
char16_n20          Char(5)
,   -- len = 2,4    

sbin17_uniq         Largeint              not null,
sdec17_nuniq        Numeric(18,0)
, char17_2            Char(8)               not null    

--   , primary key ( cReal, cFloat )
, primary key ( sdecneg15_100, sdec16_uniq)
) number of partitions 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    # View.
    stmt = """Create View VNA1P005 ( n1, c2, c3, c4 ) as
select cast( max(t1.sbinneg15_nuniq) as smallint signed )
, min(t1.char2_2)
, min(t2.char2_2)
, max(t3.char3_4)
from BTA1P005 t1
right join BTA1P005 t2 on t1.char2_2 = t2.char3_4
left  join BTA1P005 t3 on t2.char2_2 = t3.char3_4
group by t1.sbinneg15_nuniq , t1.char2_2 , t2.char2_2 , t3.char3_4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    # 2 Indexes.
    stmt = """Create Index IXA1P005a On BTA1P005 ( char0_n10 )
Location """ + gvars.g_disc1 + """
range Partition ( ADD First Key ('J') Location """ + gvars.g_disc3 + """
, ADD First Key ('T') Location """ + gvars.g_disc2 + """
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    stmt = """Create Index IXA1P005b On BTA1P005 ( sdec4_n20 )
Location """ + gvars.g_disc2 + """
range Partition ( ADD First Key (100) Location """ + gvars.g_disc1 + """
, ADD First Key (1000) Location """ + gvars.g_disc3 + """
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    # Create Like, with same partitions.
    stmt = """Create Table BTALike5 
Like BTA1P005 
With Partitions
--      With Horizontal Partitions
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """Set Transaction Autocommit On;"""
    output = _dci.cmdexec(stmt)
    #
    # INSERT.
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
--     cReal               REAL                  not null,
--     cFloat              FLOAT(10)             not null,
1, 1,
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
--     cReal               REAL                  not null,
--     cFloat              FLOAT(10)             not null,
-- 2nd PARTITION first key ( 100,10E4 )
100, 10E4 ,
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
    _dci.expect_error_msg(output, '8102')
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
--     cReal               REAL                  not null,
--     cFloat              FLOAT(10)             not null,
-- 3rd partition first key ( 500,10E4  )
500, 10E4,
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
--     cReal               REAL                  not null,
--     cFloat              FLOAT(10)             not null,
1, 10E4 ,
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
--     cReal               REAL                  not null,
--     cFloat              FLOAT(10)             not null,
500, 1,
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
--     cReal               REAL                  not null,
--     cFloat              FLOAT(10)             not null,
1E10, 1E5,
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
    stmt = """Update Statistics For Table BTA1P005 on every column;"""
    output = _dci.cmdexec(stmt)
    #
    #  SELECT.
    #
    #  Look at table.
    #
    #  Check values in the primary key.
    stmt = """Select cReal, cFloat
From BTA1P005 
Order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s0')
    #
    #  Indexes.
    #
    stmt = """Select char0_n10
From BTA1P005 
Order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s1')
    stmt = """Select sdec4_n20
From BTA1P005 
Order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s2')
    #
    stmt = """Select sbinneg15_nuniq , char2_2 , char3_4
from BTA1P005 t1
order by 1, 2, 3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s3')
    #
    stmt = """Select t1.sbinneg15_nuniq , t1.char2_2 , t2.char2_2
from BTA1P005 t1
right join BTA1P005 t2
on t1.char2_2 = t2.char3_4
order by 1, 2, 3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s4')
    #
    stmt = """Select t1.sbinneg15_nuniq , t1.char2_2 , t2.char2_2
from BTA1P005 t2
left join BTA1P005 t1
on t1.char2_2 = t2.char3_4
order by 1, 2, 3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s5')
    #
    stmt = """Select t2.char2_2, t3.char3_4
from BTA1P005 t2
left join BTA1P005 t3
on t2.char2_2 = t3.char3_4
order by 1, 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s6')
    #
    #  Check join results:
    stmt = """Select max(t1.sbinneg15_nuniq) , min(t1.char2_2)
, min(t2.char2_2) , max(t3.char3_4)
from BTA1P005 t1
right join BTA1P005 t2 on t1.char2_2 = t2.char3_4
left  join BTA1P005 t3 on t2.char2_2 = t3.char3_4
group by t1.sbinneg15_nuniq , t1.char2_2 , t2.char2_2 , t3.char3_4
order by 1, 2, 3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s7')
    #
    stmt = """Select max(t1.sbinneg15_nuniq) , min(t1.char2_2)
, min(t2.char2_2) , max(t3.char3_4)
from BTA1P005 t2
left join BTA1P005 t1 on t1.char2_2   = t2.char3_4
left join BTA1P005 t3 on t2.char2_2   = t3.char3_4
group by t1.sbinneg15_nuniq,t1.char2_2,t2.char2_2 , t3.char3_4
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s8')
    #
    #  Look at view.
    #
    stmt = """Select * from VNA1P005 
order by 1, 2, 3 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s9')
    #
    #  Aggregates.
    #  Expect ( (6) ) for each.
    stmt = """SELECT count(*) from BTA1P005;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s10')
    stmt = """SELECT count(*) from VNA1P005;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s11')
    #
    # Set Insert and Select.
    #
    stmt = """Insert Into BTALike5 
Select * From BTA1P005 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 5)
    #
    stmt = """Select cReal, cFloat
From BTALike5 
Order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s12')
    #
    stmt = """Select sbinneg15_nuniq , char2_2 , char3_4
From BTALike5 
Order By 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s13')
    #
    stmt = """Select t1.sbinneg15_nuniq , t1.char2_2 , t2.char2_2
from BTA1P005 t1
right join BTALike5 t2
on t1.char2_2 = t2.char3_4
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s14')
    #
    stmt = """Select t2.char2_2, t3.char3_4
from BTA1P005 t2
left join BTALike5 t3
on t2.char2_2 = t3.char3_4
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s15')
    
    _testmgr.testcase_end(desc)

def test006(desc="""a06"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     T1198:A06
    #  Description:        This test verifies the creation and population
    #                      of SQL Partitioned DB#11 Global Table 6
    #                      and its view; includes INSERT, SELECT.
    #
    # =================== End Test Case Header  ===================
    #
    # Make sure all transactions are small by committing each statement
    # immediately (default behavior in Release 1).
    stmt = """Set Transaction Autocommit On;"""
    output = _dci.cmdexec(stmt)
    #
    # DDL: Create Table, view.
    # Similar to table of same name in arkt1199.
    # Table 6 and Create Like.
    #
    
    stmt = """Create Table BTA1P006 
(
sbin0_4             Integer      not null,
varchar0_uniq       VarChar(8)   not null,
sdec0_100           Numeric(9,0) not null,
sdec1_20            Numeric(5,0) not null,
udec1_nuniq         Numeric(4,0) unsigned not null,    

char2_2             Char(2)      not null,
sbin2_nuniq         Largeint     ,
sdec2_500           Numeric(9,0) signed   not null,
udec3_n100          Numeric(9,0) unsigned,
ubin3_n2000         Numeric(4,0) unsigned,
char3_4             Char(8)      not null,    

sdec4_n20           Numeric(4,0) ,
sbin4_n1000         Smallint     ,
char4_n10           Char(8)      ,
char5_n20           Char(8)      ,
sdec5_10            Numeric(9,0) signed   not null,
ubin5_n500          Numeric(9,0) unsigned ,    

sbin6_nuniq         Largeint     ,
sdec6_4             Numeric(4,0) signed   not null,
char6_n100          Char(8)      ,
sbin7_n20           Smallint     ,
char7_500           Char(8)      not null,
udec7_n10           Numeric(4,0) unsigned,    

ubin8_10            Numeric(4,0) unsigned not null,
char8_n1000         Char(8)      ,
sdec8_4             Numeric(9,0) unsigned not null,
sdec9_uniq          Numeric(18,0) signed  not null,
char9_100           Char(2)      not null,    

char10_nuniq        Char(8)      ,
udec10_uniq         Numeric(9,0) unsigned not null,
udec11_2000         Numeric(9,0) unsigned not null,
sbin11_100          Integer      not null,
char11_uniq         Char(8)      not null,    

ubin12_2            Numeric(4,0) unsigned not null,
sdec12_n1000        Numeric(18,0) signed ,
char12_n2000        Char(8)      ,
udec13_500          Numeric(9,0) unsigned not null,
char13_1000         Char(8)      not null,    

sbin14_1000         Integer      not null,
udec14_100          Numeric(4,0) unsigned not null,
char14_n500         Char(8)      ,
sbinneg15_nuniq     Largeint     ,
sdecneg15_100       Numeric(9,0) signed not null,
char15_100          VarChar(8)   not null,    

ubin16_n10          Numeric(4,0) unsigned  ,
sdec16_uniq         Numeric(18,0) signed not null,
char16_n20          Char(5)      ,
sbin17_uniq         Largeint     not null,
sdec17_nuniq        Numeric(18,0),
char17_2            VarChar(7)   not null    

, primary key ( sdec9_uniq ASC
, sdec0_100 DESC
, udec1_nuniq ASC )
) number of partitions 3
ATTRIBUTE NO AUDITCOMPRESS
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    # Create View that contains Natural Join.
    #
    stmt = """create view  VNA1P006 as
select * from
(select sbin0_4 , sdec5_10 , sdec6_4 , varchar0_uniq
from BTA1P006 t1 ) t2
natural    join
(select sbin0_4 , sdec5_10 , sdec6_4 , varchar0_uniq
from BTA1P006 t3 ) t4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    # 1 Index of 2 adjacent columns.
    #
    stmt = """Create Index IXA1P006a On BTA1P006 ( char16_n20 , sbin17_uniq )
Location """ + gvars.g_disc3 + """
range Partition ( ADD First Key ('J',1) Location """ + gvars.g_disc1 + """
, ADD First Key ('T',1) Location """ + gvars.g_disc2 + """
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    # Create Like, with same partitions.
    #
    stmt = """Create Table BTALike6 
Like BTA1P006 
--      With Horizontal Partitions
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    # DML: Insert, select.
    #
    
    # Table 6
    stmt = """Set Transaction Autocommit On;"""
    output = _dci.cmdexec(stmt)
    #
    # INSERT.
    #
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
    #
    stmt = """Update Statistics For Table BTA1P006 on every column;"""
    output = _dci.cmdexec(stmt)
    #
    #  SELECT.
    #
    #  Look at data in table.
    #  Check values in the primary key.
    stmt = """select sdec9_uniq , sdec0_100 , sdec1_20
from BTA1P006 
order by 1, 2 DESC, 3 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s0')
    #
    #  Look at data in Index.
    stmt = """Select char16_n20 , sbin17_uniq
From BTA1P006 
Order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s1')
    #
    stmt = """select sbin0_4 , varchar0_uniq , sdec0_100
from BTA1P006 order by 1, 2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s2')
    #
    stmt = """select sdec1_20 , udec1_nuniq
, char10_nuniq , udec10_uniq
from BTA1P006 order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s3')
    #
    stmt = """select sbin17_uniq , sdec17_nuniq , char17_2
, char2_2 , sbin2_nuniq , sdec2_500
from BTA1P006 order by 1, 2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s4')
    #
    #  Look at data in view.
    #
    stmt = """select * from VNA1P006 order by 1, 2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s5')
    #
    #  Check columns in view.
    stmt = """select sbin0_4
, sdec5_10
, sdec6_4
, varchar0_uniq
from BTA1P006 t1
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s6')
    #
    #  Aggregates.
    #  Expect ( (4) ) for each.
    stmt = """SELECT count(*) from BTA1P006;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s7')
    stmt = """SELECT count(*) from VNA1P006;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s8')
    # Set Insert and Select.
    #
    stmt = """Insert Into BTALike6 
Select * From BTA1P006 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 4)
    #
    stmt = """Select sdec9_uniq
, sdec0_100
, sdec1_20
From BTALike6 
Order By 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s9')
    stmt = """Select sbin0_4
, sdec5_10
, sdec6_4
, varchar0_uniq
From BTALike6 t1
Order By 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s10')
    
    _testmgr.testcase_end(desc)

def test007(desc="""a07"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     T1198:A07
    #  Description:        This test verifies the creation and population
    #                      of SQL Partitioned DB#11 Global Table 7
    #                      and its view; includes INSERT, SELECT.
    #
    # =================== End Test Case Header  ===================
    #
    # Make sure all transactions are small by committing each statement
    # immediately (default behavior in Release 1).
    stmt = """Set Transaction Autocommit On;"""
    output = _dci.cmdexec(stmt)
    #
    # DDL: Create Table, view.
    # Similar to table of same name in arkt1199.
    #
    # Table 7 and Create Like.
    #
    
    stmt = """Create Table BTA1P007 
(
varchar0_nuniq      VarChar(11)                        ,
sbin0_uniq          Smallint                   not null,
sdec0_n500          Numeric(18,0)                      ,    

ubin1_n2            Numeric(4,0) unsigned              ,
udec1_100           Numeric(2,0) unsigned      not null,    

char2_2             Char(2)                    not null,
sbin2_nuniq         Largeint                           ,
sdec2_500           Numeric(9,0) signed        not null,    

udec3_n100          Numeric(9,0) unsigned              ,
ubin3_n2000         Numeric(4,0) unsigned              ,
char3_4             Char(9)                    not null,    

sdec4_n20           Numeric(4,0)                       ,
sbin4_n1000         Smallint                           ,
char4_n10           Char(8)                            ,    

char5_n20           Char(9)                            ,
sdec5_10            Numeric(9,0) signed        not null,
ubin5_n500          Numeric(9,0) unsigned              ,    

sbin6_nuniq         Largeint                           ,
sdec6_4             Numeric(4,0) signed        not null,
char6_n100          Char(8)                            ,    

sbin7_n20           Smallint                           ,
char7_500           Char(9)                    not null,
udec7_n10           Numeric(4,0) unsigned              ,    

ubin8_10            Numeric(4,0) unsigned      not null,
char8_n1000         Char(8)                            ,
sdec8_4             Numeric(9,0) unsigned      not null,    

sdec9_uniq          Numeric(18,0) signed       not null,
char9_100           Char(3)                    not null,
ubin9_n4            Numeric(9,0) unsigned              ,    

ubin10_n2           Numeric(4,0) unsigned              ,
char10_nuniq        Char(8)                            ,
udec10_uniq         Numeric(9,0) unsigned      not null,    

udec11_2000         Numeric(9,0) unsigned      not null,
sbin11_100          Integer                    not null,
char11_uniq         Char(9)                    not null,    

ubin12_2            Numeric(4,0) unsigned      not null,
sdec12_n1000        Numeric(18,0) signed               ,
char12_n2000        Char(8)                            ,    

sbin13_n100         Numeric (10,0) signed              ,
char13_1000         Char(9)                    not null,    

sbin14_1000         Integer                    not null,
udec14_100          Numeric(4,0) unsigned      not null,
char14_n500         Char(8)                            ,    

sbinneg15_nuniq     Largeint                           ,
sdecneg15_100       Numeric(9,0) signed        not null,
char15_100          Char(9)                    not null,    

ubin16_n10          Numeric(4,0) unsigned              ,
sdec16_uniq         Numeric(18,0) signed       not null,
char16_n20          Char(5)                            ,    

sbin17_uniq         Largeint                   not null,
sdec17_nuniq        Numeric(18,0)                      ,
char17_2            Char(8)                    not null    

-- 08/21/98. JZ. Interval and Date added for primary key and
--               index checking.
--               INTERVAL { start-field TO end-field | single-field }
--               specifies a column that represents a duration of
--               time as either a year-month or day-time range or
--               a single-field.
--               If the interval is specified as a range, the
--               start-field and end-field must be in one of these
--               categories:
--                  YEAR, MONTH
--                  DAY, HOUR, MINUTE, SECOND [(fractional-precision)]
--               A start-field can have a leading-precision up to
--               18 digits (the maximum depends on the number of
--               fields in the interval). The leading-precision is
--               the number of digits allowed in the start-field.
--               If the end-field is SECOND, it can have a fractional-
--               precision up to 6 digits. The fractional-precision is
--               the number of digits of precision after the decimal
--               point. The default for leading-precision is 2, and
--               the default for fractional-precision is 6.    

, cIntervalYM         Interval year to month     not null
, cIntervalDS         Interval day to second(6)  not null
, cDate               Date                       not null
, primary key (cIntervalYM, cIntervalDS)
) number of partitions 3
ATTRIBUTE CLEARONPURGE
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    # Create View; non-updateable, because of string operations.
    # Purpose: (1) test ANSI string features and
    #          (2) provide a view whose use tests string manipulation
    #              for no extra cost of testware development.
    #
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
    #
    # 1 Index of DATE column.
    stmt = """Create Index IXA1P007a On BTA1P007 ( cDate )
Location """ + gvars.g_disc1 + """
range Partition ( ADD First Key (Date '1998-08-27')
Location """ + gvars.g_disc2 + """
, ADD First Key (Date '1998-08-30')
Location """ + gvars.g_disc3 + """
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    # Create Like, with same partitions.
    stmt = """Create Table BTALike7 
Like BTA1P007 
--      With Horizontal Partitions
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """Set Transaction Autocommit On;"""
    output = _dci.cmdexec(stmt)
    #
    # INSERT.
    #
    stmt = """Insert Into BTA1P007 -- comment out till bug fixed -- TEST FAILS!
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
'GGAAKAAB',    .3,
'DDAADAAA',   505,    5,
'BBAABAAA', -3812,  -12,
'AMAAAAAA',     1, 2701,
'BBAA ',   149840,    3,
'BAAAAAAA'
-- Additional columns for partitioned table 7.
--   , cIntervalYM         Interval year(4) to month  not null
--   , cIntervalMin        Interval MINUTE            not null
--   , cDate               Date                       not null
, interval '0-1' year to month
, interval '00:07:00:00.000001' day to second(6)
, Date '1998-08-26'
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
, interval '0-1' year to month
, interval '07:00:00:00.000001' day to second(6)
, Date '1998-08-27'
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
, interval '0-0' year to month
, interval '00:07:00:00.000001' day to second(6)
, Date '1998-08-28'
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
, interval '1-1' year to month
, interval '00:07:00:00.000001' day to second(6)
, Date '1998-08-29'
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
, interval '0-0' year to month
, interval '00:07:00:00.000002' day to second(6)
, Date '1998-08-30'
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
, interval '0-1' year to month
, interval '00:07:00:00.000002' day to second(6)
, Date '1998-08-31'
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #
    stmt = """Update Statistics For Table BTA1P007 on every column;"""
    output = _dci.cmdexec(stmt)
    #
    #  SELECT.
    #
    #  Look at table.
    #
    #  Check values in the primary key.
    stmt = """Select cIntervalYM, cIntervalDS
from BTA1P007 order by 1, 2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s0')
    #  Check values in the index.
    stmt = """Select cDate
from BTA1P007 order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s1')
    #
    stmt = """Select ubin1_n2 , udec1_100 , char2_2 , sbin2_nuniq
from BTA1P007 order by 1, 2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s2')
    #
    #  Look at view.
    #
    stmt = """Select cLower, cUpper, cChar_length   from VNA1P007 
order by 1, 2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s3')
    stmt = """Select cSubstring ,    cTrim          from VNA1P007 
order by 1, 2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s4')
    stmt = """Select cConcatChar ,   cConcatVarchar from VNA1P007 
order by 1, 2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s5')
    #
    #  Aggregates.
    #  Expect ( (6) ) for each.
    stmt = """SELECT count(*) from BTA1P007;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s6')
    stmt = """SELECT count(*) from VNA1P007;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s7')
    #
    # Set insert and select.
    #
    stmt = """Insert Into BTALike7 
Select * from BTA1P007 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 6)
    #
    stmt = """Select udec3_n100 , ubin3_n2000 , char3_4, cIntervalYM, cIntervalDS
From BTALike7 
Order By 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s8')
    stmt = """Select char3_4 , varchar0_nuniq , sdec2_500 , sdec5_10
From BTALike7 
Order By 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s9')
    stmt = """Select sbin17_uniq , sdec17_nuniq , char17_2
From BTALike7 
Order By 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s10')
    
    _testmgr.testcase_end(desc)

def test008(desc="""a08"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     T1198:A08
    #  Description:        This test verifies the creation and population
    #                      of SQL Partitioned DB#11 Global Table 8
    #                      and its view; includes INSERT, SELECT.
    #
    # =================== End Test Case Header  ===================
    #
    # Make sure all transactions are small by committing each statement
    # immediately (default behavior in Release 1).
    stmt = """Set Transaction Autocommit On;"""
    output = _dci.cmdexec(stmt)
    #
    # DDL: Create Table, view.
    # Similar to table of same name in arkt1199.
    #
    # Table 8 and Create Like.
    #
    
    stmt = """Create Table BTA1P008 
(
sbin0_4             Integer  default 3    not null    

, cTime               Time                  not null
, cDate               Date                  not null    

, varchar0_500        VarChar(11)  default 'GDAAIAAA'
not null
heading 'varchar0_500 no nulls'    

, ubin1_20            Numeric(9,0) unsigned not null,
udec1_nuniq         Numeric(4,0) unsigned         ,    

char2_2             Char(2)               not null,
sbin2_nuniq         Largeint                      ,
sdec2_500           Numeric(9,0) signed   not null,    

udec3_n100          Numeric(9,0) unsigned         ,
ubin3_n2000         Numeric(4,0) unsigned         ,
char3_4             Char(8)               not null,    

sdec4_n20           Numeric(4,0)                  ,
sbin4_n1000         Smallint                      ,
char4_n10           Char(8)                       ,    

char5_n20           Char(8)                       ,
sdec5_10            Numeric(9,0) signed   not null,
ubin5_n500          Numeric(9,0) unsigned         ,    

sbin6_nuniq         Largeint                      ,
sdec6_4             Numeric(4,0) signed   not null,
char6_n100          Char(8)                       ,    

sbin7_n20           Smallint                      ,
char7_500           Char(8)               not null,
udec7_n10           Numeric(4,0) unsigned         ,    

ubin8_10            Numeric(4,0) unsigned not null,
char8_n1000         Char(8)                       ,
sdec8_4             Numeric(9,0) unsigned not null,    

sdec9_uniq          Numeric(18,0) signed  not null,
char9_100           Char(2)               not null,
ubin9_n4            Numeric(9,0) unsigned         ,    

ubin10_n2           Numeric(4,0) unsigned         ,
char10_nuniq        Char(8)                       ,
udec10_uniq         Numeric(9,0) unsigned not null,    

udec11_2000         Numeric(9,0) unsigned not null,
sbin11_100          Integer               not null,
char11_uniq         Char(8)               not null,    

ubin12_2            Numeric(4,0) unsigned not null,
sdec12_n1000        Numeric(18,0) signed          ,
char12_n2000        Char(8)                       ,    

udec13_500          Numeric(9,0) unsigned not null,
char13_1000         Char(8)               not null,    

sbin14_1000         Integer               not null,
udec14_100          Numeric(4,0) unsigned not null,
char14_n500         Char(8)                       ,    

sbinneg15_nuniq     Largeint                      ,
sdecneg15_100       Numeric(9,0) signed   not null,
char15_100          Char(8)               not null,    

ubin16_n10          Numeric(4,0) unsigned         ,
sdec16_uniq         Numeric(18,0) signed  not null,
char16_n20          Char(5)                       ,    

sbin17_uniq         Largeint              not null,
sdec17_nuniq        Numeric(18,0)                 ,
char17_2            Char(8)               not null
, primary key ( cDate )
) number of partitions 3
ATTRIBUTE CLEARONPURGE
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    # View gets all columns, omitting only the row where
    # sdec16_uniq is between 2500 and 3000.
    stmt = """create view VNA1P008 
as select * from BTA1P008 where sdec16_uniq > 3000
union select * from BTA1P008 where sdec16_uniq < 2500
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    # 1 Index of TIME column.
    stmt = """Create Index IXA1P008a On BTA1P008 ( cTime )
Location """ + gvars.g_disc3 + """
range Partition ( ADD First Key (Time '01:00:01')
Location """ + gvars.g_disc2 + """
, ADD First Key (Time '02:59:59')
Location """ + gvars.g_disc1 + """
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    # Create Like, with same partitions.
    stmt = """Create Table BTALike8 
Like BTA1P008 
--      With Horizontal Partitions
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """Set Transaction Autocommit On;"""
    output = _dci.cmdexec(stmt)
    #
    # INSERT.
    #
    stmt = """Insert Into BTA1P008 
Values ( 1,
Time '01:01:01' , Date '1900-01-01',
'ACAABAAA   ', 2, 0,
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
Values ( 1,
Time '02:02:02' , Date '1998-01-01',
'BBAAFAAA   ', 9, 1,
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
Values ( 3,
Time '00:00:00' , Date '1910-10-17',
'CAAAGAAA   ', 4, 5,
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
Values ( 1,
Time '02:00:00' , Date '1776-06-04',
'BBAABAAA   ', 5, 3,
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
Values ( 1,
Time '01:00:00' , Date '1776-06-07',
'BBAADAAA   ', 5, 2,
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
Values ( 0,
Time '03:03:03' , Date '2000-01-01',
'BDAAAAAA   ', 3, 4,
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
    #
    stmt = """Update Statistics For Table BTA1P008 on every column;"""
    output = _dci.cmdexec(stmt)
    #
    #  SELECT.
    #
    #  Check values in the primary key.
    #
    stmt = """select cDate from BTA1P008 order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s0')
    stmt = """select cDate from VNA1P008 order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s1')
    #
    #  Compare table and view, looking at predicate column.
    #
    stmt = """select sdec16_uniq from BTA1P008 order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s2')
    stmt = """select sdec16_uniq from VNA1P008 order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s3')
    #
    #  Look at table.
    #
    stmt = """select sdec16_uniq
from BTA1P008 
where sdec16_uniq > 3000 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s4')
    stmt = """select sbinneg15_nuniq , char15_100
from BTA1P008 
where sdec16_uniq > 3000
union all
select sdec17_nuniq , char17_2
from BTA1P008 
where sdec16_uniq > 3000
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s5')
    #
    #  Look at view.
    #
    stmt = """select sbin0_4 , varchar0_500 , ubin1_20 , udec1_nuniq
from VNA1P008 
order by 1, 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s6')
    stmt = """select char2_2 , sbin2_nuniq , sdec2_500
, udec3_n100 , ubin3_n2000 , char3_4
from VNA1P008 
order by 1, 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s7')
    #
    #  Aggregates.
    #  Expect ( (6) ) for table, ( (5) ) for view.
    stmt = """SELECT count(*) from BTA1P008;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s8')
    stmt = """SELECT count(*) from VNA1P008;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s9')
    #
    # Set insert and UNION select.
    #
    stmt = """Insert Into BTALike8 
Select * from BTA1P008 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 6)
    #
    stmt = """Select char3_4 , varchar0_500 , sdec2_500 , char3_4
, sdec5_10 , char7_500
From VNA1P008 
Union
Select char3_4 , varchar0_500 , sdec2_500 , char3_4
, sdec5_10 , char7_500
From BTALike8 
Order By 1, 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s10')
    
    _testmgr.testcase_end(desc)

def test009(desc="""a09"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     T1198:A09
    #  Description:        This test verifies the creation and population
    #                      of SQL Partitioned DB#11 Global Table 9
    #                      and its view; includes INSERT, SELECT.
    #
    # =================== End Test Case Header  ===================
    #
    #
    # Make sure all transactions are small by committing each statement
    # immediately (default behavior in Release 1).
    stmt = """Set Transaction Autocommit On;"""
    output = _dci.cmdexec(stmt)
    # Similar to table of same name in arkt1199.
    #
    # Table 9 and Create Like.
    # Includes BIT PRECISION INTEGER added after odd-length char field,
    # for primary key and index checking. Syntax:
    #     BIT PRECISION INT[EGER] (bit-length) UNSIGNED
    #         where bit-length is 1 to 15.
    # BIT PRECISION INTEGER specifies the range of an unsigned integer
    # data type as the number of bits allowed in the value of the
    # column. For bit-length b, the range of values is between
    # 0 and 2^b - 1. For bit-length of 7, the column corresponds to
    # an unsigned integer data type with a range between 0 and 127.
    #
    
    stmt = """create table BTA1P009(
rownum   integer not null
, ch1n     char -- length defaults to 1.    

, cBitPK   BIT PRECISION INTEGER (5) UNSIGNED  not null
, cBitIX   BIT PRECISION INTEGER (15) UNSIGNED    

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
, primary key ( cBitPK ) NOT DROPPABLE    

) number of partitions 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    # Create View using columns from a discontiguous-column index.
    stmt = """create view  VNA1P009 (csimple, csearched) as select
-- Simple CASE:
CASE rownum WHEN 1 THEN 'Value A'
WHEN 2 THEN 'Value B'
WHEN 3 THEN 'Value C'
ELSE 'Value D -- Rowcount > 3'
END
-- Searched CASE:
,   CASE when rownum > 10    then 'rownum over 10'
when sint = -32768  then 'sint is the lowest'
else 'the great unknown'
END
from BTA1P009 
where rownum < CASE
when rownum  between 7 and 12  then 2222
when rownum  between 1 and 2   then rownum+1
else rownum
end
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    # Index creation.
    stmt = """Create INDEX IXA1P009a ON BTA1P009 ( cBitIX )
LOCATION """ + gvars.g_disc1 + """
RANGE PARTITION ( ADD first key ( 5 )
LOCATION """ + gvars.g_disc2 + """
, ADD first key ( 10 )
LOCATION  """ + gvars.g_disc3 + """ )
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    # Create Like, with same partitions.
    stmt = """Create Table BTALike9 
Like BTA1P009 
With CONSTRAINTS
With Partitions
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """Set Transaction Autocommit On ;"""
    output = _dci.cmdexec(stmt)
    stmt = """Set Warnings Off ;"""
    output = _dci.cmdexec(stmt)
    #
    # INSERT.
    #
    # Insert 14 rows
    stmt = """Insert Into BTA1P009 Values (
1, 'S',
11, 1,
'This is a 50 character field', 'This is a 49 character field',
'V',  'This is a 50 character varchar field aaaaaaaaaaaaa',
'This is a 49 character varchar field bbbbbbbbbbbb',
-1, 123456789012345678, -0.123456789012345678, 123456789, 0.123456789,
-999.45678, 999.45678, -32768, 32766,   4294967295, -2147483648, -9.2233 ,
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
    stmt = """Insert Into BTA1P009 Values (
2, 'S',
12, 2,
'This is a 50 character field', 'This is a 49 character field',
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
    stmt = """Insert Into BTA1P009 Values (
3, 'S',
13, 3,
'This is a 50 character field', 'This is a 49 character field',
'V',  'This is a 50 character varchar field aaaaaaaaaaaaa',
'This is a 49 character varchar field bbbbbbbbbbbb',
-1, 123456789012345678, -0.123456789012345678, 123456789, 0.123456789,
-999.45678, 999.45678, -32768, 32767,   4294967295, -2147483648, -9.2233 ,
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
    stmt = """Insert Into BTA1P009 Values (
4, 'A',
14, 4,
'This is a 50 character field', 'This is a 49 character field',
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
    stmt = """Insert Into BTA1P009 Values (
5, 'A',
1, 5,
'This is a 50 character field', 'This is a 49 character field',
'V',  'This is a 50 character varchar field aaaaaaaaaaaaa',
'This is a 49 character varchar field cccccccccccc',
-1, 123456789012345678, -0.123456789012345678, 123456789, 0.123456789,
-999.45678, 999.45678, -32768, 30000,   4294967295, -2147483648, -9.2233 ,
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
    stmt = """Insert Into BTA1P009 Values (
6, 'A',
2, 6,
'This is a 50 character field',
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
    stmt = """Insert Into BTA1P009 Values (
7, 'A',
3, 7,
'This is a 50 character field',
'This is a 49 character field',
'V',  'This is a 50 character varchar field aaaaaaaaaaaaa',
'This is a 49 character varchar field cccccccccccc',
-1, 123456789012345678, -0.123456789012345678, 123456789, 0.123456789,
-999.45678, 999.45678, -32768, 30000,   4294967295, -2147483648, -9.2233 ,
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
    stmt = """Insert Into BTA1P009 Values (
8, 'A',
4, 8,
'This is a 50 character field',
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
    stmt = """Insert Into BTA1P009 Values (
9, 'A',
5, 9,
'This is a 50 character field',
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
    stmt = """Insert Into BTA1P009 Values (
10, 'A',
10, 10,
'This is a 50 character field', 'This is a 49 character field',
'V',  'This is a 50 character varchar field aaaaaaaaaaaaa',
'This is a 49 character varchar field cccccccccccc',
-1, 123456789012345678, -0.123456789012345678, 123456789, 0.123456789,
-999.45678, 999.45678, -32767, 32767,   4294967295, -2147483648, -9.2233 ,
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
    stmt = """Insert Into BTA1P009 Values (
11, 'A',
20, 10,
'This is a 50 character field', 'This is a 49 character field',
'V',  'This is a 50 character varchar field aaaaaaaaaaaaa',
'This is a 49 character varchar field bbbbbbbbbbbb',
-1, 123456789012345678, -0.123456789012345678, 123456789, 0.123456789,
-999.45678, 999.45678, -32767, 32767,   4294967295, -2147483648, -9.2233 ,
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
    stmt = """Insert Into BTA1P009 Values (
12, 'S',
30, 10,
'This is a 50 character field', 'This is a 49 character field',
'V',  'This is a 50 character varchar field aaaaaaaaaaaaa',
'This is a 49 character varchar field bbbbbbbbbbbb',
-1, 123456789012345678, -0.123456789012345678, 123456789, 0.123456789,
-999.45678, 999.45678, -32767, 32767,   4294967295, -2147483648, -9.2233 ,
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
    stmt = """Insert Into BTA1P009 Values (
13, 'A',
31, 10,
'This is a 50 character field', 'This is a 49 character field',
'V',  'This is a 50 character varchar field aaaaaaaaaaaaa',
'This is a 49 character varchar field bbbbbbbbbbbb',
-1, 123456789012345678, -0.123456789012345678, 123456789, 0.123456789,
-999.45678, 999.45678, -32767, 32767,   4294967295, -2147483648, -9.2233 ,
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
    stmt = """Insert Into BTA1P009 Values (
14, 'A',
29, 10,
'This is a 50 character field', 'This is a 49 character field',
'V',  'This is a 50 character varchar field aaaaaaaaaaaaa',
'This is a 49 character varchar field bbbbbbbbbbbb',
-1, 123456789012345678, -0.123456789012345678, 123456789, 0.123456789,
-999.45678, 999.45678, -32767, 32767,   4294967295, -2147483648, -9.2233 ,
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
    #
    stmt = """Update Statistics For Table BTA1P009 on every column;"""
    output = _dci.cmdexec(stmt)
    #
    #  SELECT.
    #
    #  Table:
    #
    #  Check values in the primary key.
    stmt = """Select cBitPK From BTA1P009 
Order By 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s0')
    #
    #  Check values in the index.
    stmt = """Select cBitIX From BTA1P009 
Order By 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s1')
    #
    stmt = """Select vc50n, rownum
From BTA1P009 
Order By 1, 2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s2')
    #
    stmt = """Select rownum, vc49n, sint
From BTA1P009 
Order By 1, 2, 3 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s3')
    #
    #  Select CASEs:
    #  (a)  Simple CASE in SELECT list:
    stmt = """Select
CASE rownum WHEN 1 THEN 'Value A'
WHEN 2 THEN 'Value B'
WHEN 3 THEN 'Value C'
ELSE 'Value D -- Rowcount > 3'
END
From BTA1P009 
Order By 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s4')
    #
    #  (b) Searched CASE or 'CASE with searched conditions'
    #      in SELECT list.
    #  Allows multiple conditions to be evaluated in a single query.
    #        SYNTAX: <case specification> ::= <searched case> ::=
    #                    CASE
    #                         WHEN <search condition> THEN
    #                        [  <result expression> | NULL ]
    #                         ...
    #                       [ ELSE <result> ]
    #                    END
    stmt = """Select
CASE when rownum > 10 then 'rownum over 10'
when sint  = -32768 then 'sint is the lowest'
else 'the great unknown'
END
From BTA1P009 
Order By 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s5')
    #
    #  (c) Searched CASE or 'CASE with searched conditions'
    #      in predicate.
    stmt = """Select rownum From BTA1P009 
where rownum < CASE
when rownum between 7 and 12  then 2222
when rownum between 1 and 2   then rownum+1
else rownum
end
Order By 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s6')
    #
    #  View:
    #
    stmt = """Select * From VNA1P009 
Order By csimple, csearched
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s7')
    #
    #  Aggregates.
    #  Expect ( (14) ) for table, ( (8) ) for view.
    stmt = """SELECT count(*) from BTA1P009;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s8')
    stmt = """SELECT count(*) from VNA1P009;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s9')
    #
    # Set Insert and Select.
    #
    stmt = """Insert Into BTALike9 
Select * From BTA1P009 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 14)
    #
    stmt = """Select rownum, ch49n
, vc1n
, nm1n
From BTA1P009 
Order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s10')
    #
    stmt = """Select rownum, iyearn
, idayn
, iyear
, iday
From BTA1P009 
Order By 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s11')
    
    _testmgr.testcase_end(desc)

def test010(desc="""a10"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     T1198:A10
    #  Description:        This test verifies the creation and population
    #                      of SQL Partitioned DB#11 Global Tables
    #                      and Views for JRAN-generated tests;
    #                      includes INSERT and SELECT.
    #
    # =================== End Test Case Header  ===================
    #
    # Make sure all transactions are small by committing each statement
    # immediately (default behavior in Release 1).
    stmt = """Set Transaction Autocommit On;"""
    output = _dci.cmdexec(stmt)
    #
    # DDL: Create Table, view.
    #
    # Create partitioned tables and views upon them,
    # for Parallel execution of JRAN scripts.
    #
    # Create three tables.
    
    stmt = """drop table btd1;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table btd2;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table btd3;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """Create Table btd1 (
vc1 VARCHAR(51)  NOT NULL
, i1  INT UNSIGNED NOT NULL
, i2  INT UNSIGNED NOT NULL
, i3  INT UNSIGNED
, c1  CHAR(91)  NOT NULL
, PRIMARY KEY ( vc1, i1, c1 )
) number of partitions 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    # First partition is to be empty.
    stmt = """Create Table btd2 (
i1 INT UNSIGNED
, vc1 VARCHAR(129)
, cDate DATE NOT NULL
, i2 INT UNSIGNED
, i3 INT UNSIGNED
, PRIMARY KEY ( cDate DESC )
) number of partitions 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    stmt = """Create Table btd3 (
i1 INT UNSIGNED
, vc1 VARCHAR(123)  NOT NULL
, i2 INT UNSIGNED
, vc2 VARCHAR(121)  NOT NULL
, i3 INT UNSIGNED
, PRIMARY KEY ( vc2 DESC, vc1 )
) number of partitions 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    stmt = """CREATE INDEX indexOnBTD1 on btd1 ( c1 ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """CREATE INDEX indexOnBTD2 on btd2 ( vc1 ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    # Create a view.
    stmt = """CREATE VIEW d1(i1,i2,i3) AS
SELECT t1.i1, t1.i2, t2.i3
FROM btd1 t1
LEFT OUTER JOIN btd2 t2
ON t1.vc1 = t2.vc1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    stmt = """CREATE VIEW d2(i1,i2,i3) AS
SELECT t1.i1, t1.i2, t2.i3
FROM btd1 t1
INNER JOIN btd2 t2
ON t1.c1 = t2.vc1
AND cDate > DATE '1910-10-17'
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    stmt = """CREATE VIEW d3(i1,i2,i3) AS
SELECT t2.i2, t3.i2, t3.i3
FROM btd3 t3
LEFT OUTER JOIN btd2 t2
ON t2.vc1 BETWEEN t3.vc1 AND t3.vc2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    #---------------------------------------
    # The end.
    #---------------------------------------
    #
    # DML: Insert, select.
    #
    
    # Populate partitioned tables
    # for Parallel execution of JRAN scripts.
    #
    # Put data into table in all three partitions.
    # btd1 columns are: VARCHAR(121), 3 * INT, CHAR(123)
    stmt = """INSERT INTO btd1 VALUES ( 'Data1', 11 , 21 , 61, 'Data1' );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO btd1 VALUES ( 'A Partition 1'
, 1 , 2 , 3
, 'Ancient History' );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO btd1 VALUES ( 'A Partition 1'
, 4 , 5 , 6
, 'More Ancient History' );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO btd1 VALUES ( 'M Partition 2'
, 7 , 8 , NULL
, 'History' );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO btd1 VALUES ( 'M Partition 2'
, 0 , 9, NULL
, 'More History' );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO btd1 VALUES ( 'T Partition 3'
, 1 , 2 , 3
, 'Future' );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO btd1 VALUES ( 'T Partition 3'
, 4 , 5 , 6
, 'Future' );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #
    # btd2 columns are: INT, VARCHAR(129), DATE, 2 * INT
    stmt = """INSERT INTO btd2 VALUES ( 1 , 'Data1', DATE '1998-08-21', 41 , 51);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO btd2 VALUES ( 2 , 'A Partition 1', DATE '0001-01-01', 41 , 51);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO btd2 VALUES ( 3 , 'A Partition 1', DATE '1015-12-12', 41 , 51);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO btd2 VALUES ( 4 , 'M Partition 2', DATE '1776-07-04', 41 , 51);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO btd2 VALUES ( 5 , 'M Partition 2', DATE '1776-07-05', 41 , 51);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO btd2 VALUES ( 31 , 'T Partition 3', DATE '2001-12-12', 41 , 51);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO btd2 VALUES ( 31 , 'T Partition 3', DATE '2010-01-01', 41 , 51);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #
    # btd3 columns are: INT , VARCHAR(123), INT,  VARCHAR(121), INT
    stmt = """INSERT INTO btd3 VALUES ( 1 , 'Row 1',  7 , 'A Partition 1', 1 );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO btd3 VALUES ( 2 , 'Row 2',  8 , 'A Partition 1', 1 );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO btd3 VALUES ( 3 , 'Row 3',  9 , 'A Partition 1', 1 );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO btd3 VALUES ( 4 , 'Row 1', 10 , 'M Partition 2', 1 );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO btd3 VALUES ( 5 , 'Row 2', 11 , 'M Partition 2', 1 );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO btd3 VALUES ( 6 , 'Row 3', 12 , 'M Partition 2', 1 );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #
    # Modify Statistics:
    stmt = """Update Statistics For Table btd1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '9213')
    stmt = """Update Statistics For Table btd2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '9213')
    stmt = """Update Statistics For Table btd3 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '9213')
    #
    #  Check contents of data objects:
    stmt = """Select i1,i2,i3 From d1 Order By i1, i2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s0')
    stmt = """Select i1,i2,i3 From d2 Order By i1, i2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s1')
    stmt = """Select i1,i2,i3 From d3 Order By i1, i2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s2')
    
    _testmgr.testcase_end(desc)

def test011(desc="""modstat"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     T1198:ModStat
    #  Description:        This test Modifies the Statistics on the
    #                      SQL Partitioned DB#11 Global Tables 1-9.
    #                      This unusual situation of having one test
    #                      case depend upon another is in order
    #                      to localize this statistics modification.
    #
    # =================== End Test Case Header  ===================
    #
    # Make sure all transactions are small by committing each statement
    # immediately (default behavior in Release 1), until we start modifying
    # the database.
    stmt = """Set Transaction Autocommit On ;"""
    output = _dci.cmdexec(stmt)
    #
    #------------------------------------------------
    # Addition 1998-10-22.
    #------------------------------------------------
    
    # Begin with table BT
    # (A) Modify Histogram Tables: Change the ROWCOUNT and TOTAL_UEC.
    # See on-line help info:
    # UPDATE STATISTICS FOR TABLE SALES.MAILINGS
    #    ON EVERY COLUMN
    #    SAMPLE 2000 ROWS
    #    SET ROWCOUNT 2.72E4;
    #
    # Update Statistics
    # Require ON EVERY COLUMN in order to SET ROWCOUNT ...
    #
    # 981120FCS: Apparently this works ok, despite looping on other updates.
    stmt = """Update Statistics For Table BTA1P001 
ON EVERY COLUMN
SAMPLE SET ROWCOUNT 1E6
;"""
    output = _dci.cmdexec(stmt)
    #
    stmt = """Update Statistics For Table BTA1P002 
ON EVERY COLUMN
SAMPLE SET ROWCOUNT 1E6
;"""
    output = _dci.cmdexec(stmt)
    #
    # Loops 981120FCS awaits fix for DESC PK.
    stmt = """Update Statistics For Table BTA1P003 
ON EVERY COLUMN
SAMPLE SET ROWCOUNT 1E6
;"""
    output = _dci.cmdexec(stmt)
    #
    # Loops 981120FCS awaits fix for DESC PK.
    stmt = """Update Statistics For Table BTA1P004 
ON EVERY COLUMN
SAMPLE SET ROWCOUNT 1E6
;"""
    output = _dci.cmdexec(stmt)
    #
    stmt = """Update Statistics For Table BTA1P005 
ON EVERY COLUMN
SAMPLE SET ROWCOUNT 1E6
;"""
    output = _dci.cmdexec(stmt)
    #
    # Loops 981120FCS awaits fix for DESC PK.
    stmt = """Update Statistics For Table BTA1P006 
ON EVERY COLUMN
SAMPLE SET ROWCOUNT 1E6
;"""
    output = _dci.cmdexec(stmt)
    #
    stmt = """Update Statistics For Table BTA1P007 
ON EVERY COLUMN
SAMPLE SET ROWCOUNT 1E6
;"""
    output = _dci.cmdexec(stmt)
    #
    stmt = """Update Statistics For Table BTA1P008 
ON EVERY COLUMN
SAMPLE SET ROWCOUNT 1E6
;"""
    output = _dci.cmdexec(stmt)
    #
    stmt = """Update Statistics For Table BTA1P009 
ON EVERY COLUMN
SAMPLE SET ROWCOUNT 1E6
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """control query default HIST_NO_STATS_REFRESH_INTERVAL '0';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """control query default query_cache '0';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop table sta;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table sta (a int not null, primary key (a));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into sta values (12), (24), (36);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 3)
    
    stmt = """prepare XX from
select * from sta;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """SELECT cast (seq_num             as numeric(2))    as seq_num,
cast (operator            as char(17))      as operator,
cast (left_child_seq_num  as numeric(2))    as L_Child,
cast (right_child_seq_num as numeric(2))    as R_Child,
cast (tname               as char(20))      as Table_Name,
cast (operator_cost       as numeric(16,6)) as Operator_Cost,
cast (total_cost          as numeric(16,6)) as RollUp_Cost,
cast (cardinality         as numeric(16,2)) as Cardinality
FROM TABLE (explain(NULL, 'XX'))
ORDER BY seq_num DESC;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """update statistics for table sta on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """prepare XX from
select * from sta;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #  The CARDINALITY should be 3.
    stmt = """SELECT cast (seq_num             as numeric(2))    as seq_num,
cast (operator            as char(17))      as operator,
cast (left_child_seq_num  as numeric(2))    as L_Child,
cast (right_child_seq_num as numeric(2))    as R_Child,
cast (tname               as char(20))      as Table_Name,
cast (operator_cost       as numeric(16,6)) as Operator_Cost,
cast (total_cost          as numeric(16,6)) as RollUp_Cost,
cast (cardinality         as numeric(16,2)) as Cardinality
FROM TABLE (explain(NULL, 'XX'))
ORDER BY seq_num DESC;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """Create Table BTA1P005_A 
(
char0_n10           Char(2)
default 'AD'
heading 'char0_n10 with default AD'    

, sbin0_uniq          Smallint not null,
sdec0_n500          Numeric(18,0) ,    

ubin1_n2            Numeric(4,0) unsigned
, udec1_100           Numeric(2,0) unsigned not null,    

char2_2             Char(2)               not null,
sbin2_nuniq         Largeint              ,
sdec2_500           Numeric(9,0) signed   not null,    

udec3_n100          Numeric(9,0) unsigned ,
ubin3_n2000         Numeric(4,0) unsigned ,
char3_4             Char(8)               not null    

, sdec4_n20           Numeric(4,0)          ,
sbin4_n1000         Smallint              ,
char4_n10           Char(8)               ,    

char5_n20           Char(8)               ,
sdec5_10            Numeric(9,0) signed   not null,
ubin5_n500          Numeric(9,0) unsigned    

, sbin6_nuniq         Largeint              ,
sdec6_4             Numeric(4,0) signed   not null,
char6_n100          Char(8)               ,    

sbin7_n20           Smallint              ,
char7_500           Char(8)               not null,
udec7_n10           Numeric(4,0) unsigned    

, ubin8_10            Numeric(4,0) unsigned not null,
char8_n1000         Char(8)               ,
sdec8_4             Numeric(9,0) unsigned not null,    

sdec9_uniq          Numeric(18,0) signed  not null,
char9_100           Char(2)               not null,
ubin9_n4            Numeric(9,0) unsigned    

, ubin10_n2           Numeric(4,0) unsigned ,
char10_nuniq        Char(8)               ,
udec10_uniq         Numeric(9,0) unsigned not null,    

cReal               REAL                  not null,
cFloat              FLOAT(10)             not null,    

udec11_2000         Numeric(9,0) unsigned not null,
sbin11_100          Integer               not null,
char11_uniq         Char(8)               not null    

, ubin12_2            Numeric(4,0) unsigned not null    

, sdec12_n1000        Numeric(18,0) signed  ,
char12_n2000        Char(8)    

, udec13_500          Numeric(9,0) unsigned not null,
char13_1000         Char(8)               not null    

, sbin14_1000         Integer               not null,
udec14_100          Numeric(4,0) unsigned not null,
char14_n500         Char(8)               ,    

sbinneg15_nuniq     Largeint              ,
sdecneg15_100       Numeric(9,0) signed   not null,
char15_100          Char(8)               not null    

, ubin16_n10          Numeric(4,0) unsigned
, sdec16_uniq         Numeric(18,0) signed  not null,
char16_n20          Char(5)
,   -- len = 2,4    

sbin17_uniq         Largeint              not null,
sdec17_nuniq        Numeric(18,0)
, char17_2            Char(8)               not null    

, primary key ( cReal, cFloat )
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """Update Statistics For Table BTA1P005_A 
ON EVERY COLUMN
SAMPLE SET ROWCOUNT 1E6;"""
    output = _dci.cmdexec(stmt)
    # TRAF now treats an empty sample set for the SAMPLE option as an
    # 9207 error. 
    # _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

