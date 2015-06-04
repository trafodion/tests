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
    
    stmt = """create table TTFONE (vchar1 varchar(3), nint integer) no partition;"""
    output = _dci.cmdexec(stmt)
    stmt = """create table TTF ( vch7 varchar(7)
, nint smallint
, ch3 char(3)
, nnum9 numeric(9,2)
, ch4 char(4)
, nnum5 numeric(5,1)
, vch5 varchar(5)
, nsint smallint signed
)  no partition;"""
    output = _dci.cmdexec(stmt)
    stmt = """create table TTF1( vch7 varchar(7)
, nint smallint
, ch3 char(3)
, nnum9 numeric(9,2)
, ch4 char(4)
, nnum5 numeric(5,1)
, vch5 varchar(5)
, nsint smallint signed
)  no partition;"""
    output = _dci.cmdexec(stmt)
    stmt = """create table TTF2( v1   varchar(7)
, n2   smallint
, c3   char(3)
, n4   numeric(9,2)
, c5   char(4)
, n6   numeric(5,1)
, v7   varchar(5)
, n8   smallint
)  no partition;"""
    output = _dci.cmdexec(stmt)
    #
    # Insert
    #
    stmt = """insert into TTFONE values ('cc', 2);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into TTF values
('a',      1,'a'  ,0.9,       NULL,NULL  ,NULL,0)
, ('cc'     ,2,'cc' ,2.00,      'cc',2.0   ,'cc',2)
, ('abcdefg',3,'cc' ,0.09,    'alph',2     ,'cc',1)
, ('b',      4,'c'  ,1234567.89,'e' ,1234.5,'c' ,12345)
, ('abcdefg',5,'cc' ,0.09,      'cc',2     ,'cc',2)
;"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into TTF1 values
('abcdefg',3,'cc',0.09,    'alph',2     ,'cc',1)
;"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into TTF2 select * from TTF ;"""
    output = _dci.cmdexec(stmt)
    
    # Empty table to be used in testcase TTFA09.
    
    stmt = """create table TTFA09 ( vch7 varchar(7)
, nint smallint
, ch3 char(3)
, nnum9 numeric(9,2)
, ch4 char(4)
, nnum5 numeric(5,1)
, vch5 varchar(5)
, nsint smallint signed
)  no partition;"""
    output = _dci.cmdexec(stmt)
    
    # Create table TTFX for testcase a10
    
    stmt = """create table TTFX  ( v1   varchar(7)
, n2   smallint
, c3   char(3)
, n4   numeric(9,2)
, c5   char(4)
, n6   numeric(9,2)
, v7   varchar(5)
, n8   smallint
)  no partition;"""
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
from BTA1P006 t1 ) t2
natural    join
(select sbin0_4 , sdec5_10 , sdec6_4 , varchar0_uniq
from BTA1P006 t3 ) t4
;"""
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
    
    _testmgr.testcase_end(desc)

