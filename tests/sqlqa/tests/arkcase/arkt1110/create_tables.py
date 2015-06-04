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
    
    # Create:
    
    # Primary key of contiguous columns.
    stmt = """create table TAB1 (
pkvca      varchar(13) not null
, nintb      smallint    not null
, vcc        varchar(21)
, noindexvcd varchar(11)
, vce        varchar(11)
, primary key (pkvca , nintb )
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # Primary key of dis-contiguous columns.
    stmt = """create table TAB2 (
vca         varchar(9)
, vcb         varchar(9)
, nintc       smallint   not null
, noindexvcd  varchar(9)
, vce         varchar(9) not null
, endcomposxf smallint   not null
, pkvcg       varchar(9) not null
, primary key ( pkvcg , nintc , vce )
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # Inserts.
    
    stmt = """insert into TAB1 values ( '01 No dup' , 1 , 'Duplicate allowed'
, 'd'  , 'e'
) ;"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into TAB1 values ( '03 No dup' , 4 , 'Duplicate allowed'
, 'dd' , 'ee'
) ;"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into TAB1 values ( '02 No dup' , 7 , 'Index col'
, 'ddd', 'eee'
) ;"""
    output = _dci.cmdexec(stmt)
    
    # Match TAB1 values on some non-primary cols.
    stmt = """insert into TAB2 values ( 'ddd', 'ee'
, 3 , 'd'
, 'e' , 7
, 'Dup Key 1'
) ;"""
    output = _dci.cmdexec(stmt)
    
    # First 2 columns of primary key (pkvcg , nintc) match
    # TAB1's primary key (pkvca , nintb).
    
    stmt = """insert into TAB2 values ( NULL, 'LONG1 c2'
, 1 , 'LONG1 c4'
, 'LONG1 c5', 101
, '01 No dup'
) ;"""
    output = _dci.cmdexec(stmt)
    
    # First 2 columns of primary key (pkvcg , nintc) match on another
    # TAB1's primary key (pkvca , nintb).
    
    stmt = """insert into TAB2 values (
'LONG1 c1' , 'LONG1 c2'
, 7 , 'LONG1 c4'
, 'LONG1 c5' , 101
, '02 No dup'
) ;"""
    output = _dci.cmdexec(stmt)
    
    # First 2 columns of primary key (pkvcg , nintc) match on another
    # TAB1's primary key (pkvca , nintb).
    stmt = """insert into TAB2 values (
'LONG1 c1' , 'LONG1 c2'
, 4 , NULL
, 'LONG1 c7' , 100
, '03 No dup'
) ;"""
    output = _dci.cmdexec(stmt)
    
    # Match between TAB2 and TAB1 on non-primary cols.
    stmt = """insert into TAB2 values (
'ddd'      , 'ee'
, 2 , 'LONG3 c4'
, 'LONG1 c5' , 5
, 'Dup Key 1'
) ;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select * from TAB1 order by 1;"""
    output = _dci.cmdexec(stmt)
    stmt = """select * from TAB2 order by 1;"""
    output = _dci.cmdexec(stmt)
    
    # Populate indexes.
    # Create index on column that is also part of a
    # composite key; leave one column (noindexvcd) un-indexed.
    
    stmt = """create index I1TAB1 on TAB1(vcc);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index I2TAB1 on TAB1(vce);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # Create simple (one-column each) indexes;
    # leave one column (noindexvcd) un-indexed.
    stmt = """create index I1TAB2 on TAB2(vca);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index I2TAB2 on TAB2(vcb, endcomposxf);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index I3TAB2 on TAB2(vce);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # Make tables like the above == but make the Pkey equal
    # to all cols in sequence.
    
    stmt = """create table TAB1K (
pkvca    varchar(21) not null
, nintb    int         not null
, vcc      varchar(21) not null
, indexvcd varchar(21) not null
, vce      varchar(21) not null
, primary key (pkvca , nintb, vcc, indexvcd, vce  )
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into TAB1K (select * from TAB1);"""
    output = _dci.cmdexec(stmt)
    stmt = """select * from TAB1K ;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table TAB2K (
vca         varchar(9) not null
, vcb         varchar(9) not null
, nintc       int        not null
, indexvcd    varchar(9) not null
, vce         varchar(9) not null
, endcomposxf int        not null
, pkvcg       varchar(9) not null
, primary key ( vca , vcb , nintc, indexvcd, vce
, endcomposxf , pkvcg )
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into TAB2K (
select * from TAB2 
where vca is not NULL and noindexvcd is not NULL
and vca <> 'NULL' and noindexvcd <> 'NULL'
);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select * from TAB2K;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """Create Table Twide1 
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
char3_1000       PIC X(200)        ,
ubin3_uniq       Numeric(5,0) unsigned  ,    

sbin4_2          Numeric(1,1) signed,
ubin4_4          Numeric(1,1) unsigned  ,
varchar4_1000    VarChar(16)        ,
sdec4_10         Numeric(1,1) signed    ,
udec4_2          Numeric(1,1) unsigned  ,    

sbin5_4          Numeric(4,0) signed,
ubin5_20         Numeric(9,0) unsigned  ,
udec5_20         Numeric(4,0) unsigned  ,
varchar5_4       VarChar(8)         ,
sdec5_100        Numeric(18,0) signed   ,    

varchar6_20      VarChar(32)        ,    

sbin7_2          SMALLINT signed    ,
sdec7_10         Numeric(4,1) signed    ,
char7_uniq       Char(100)          ,
udec7_20         Numeric(4,1) unsigned  ,
ubin7_100        SMALLINT unsigned  ,    

sbin8_1000       Numeric(18,0) signed   ,
varchar8_uniq    VarChar(32)        ,
ubin8_2          Numeric(4,1) unsigned  ,    

char9_uniq       Char(8)            ,
udec9_10         Numeric(5,0) unsigned  ,
sdec9_20         Numeric(5,0) signed    ,    

varchar10_20      VarChar(32)       ,    

sdec11_20        Numeric(5,5) signed    ,
varchar11_2      VarChar(32)        not null ,
char11_4         Char(2)            ,    

sbin12_1000      Numeric(9,0) signed,
varchar12_4      VarChar(32)        ,
ubin12_10        Numeric(9,0) unsigned  ,    

char13_100       Char(5)            ,
sdec13_uniq      Numeric(9,0) signed    ,
udec13_500       Numeric(9,0) unsigned  ,    

sbin14_100       Numeric(2,0) signed    ,
ubin14_2         Numeric(2,0) unsigned  ,
sdec14_20        Numeric(2,0) signed    ,
udec14_10        Numeric(2,0) unsigned  ,
varchar14_2000   VarChar(64)        ,    

sbin15_2         INTEGER signed     ,
udec15_4         Numeric(9,2) unsigned  ,
varchar15_uniq   VarChar(8)         not null ,
ubin15_uniq      INTEGER unsigned   ,
sdec15_10        Numeric(9,2) signed    ,    

sbin16_20        Numeric(9,2) signed,
ubin16_1000      Numeric(9,2) unsigned  ,
varchar16_100    VarChar(128)       ,    

sbin17_uniq      Numeric(10,0) signed   ,
sdec17_20        Numeric(2,0) signed    ,
char17_100       Char(100)          ,
varchar17_20     VarChar(200)       ,    

sbin18_uniq      Numeric(18,0) signed   ,
varchar18_uniq   VarChar(60)        ,    

sbin19_4         LARGEINT signed    ,
char19_2         Char(8)            ,
ubin19_10        SMALLINT unsigned  ,
udec19_100       Numeric(4,1) signed    ,
sdec19_1000      Numeric(4,1) unsigned  ,
varchar20_1000   VarChar(100)
, primary  key (
varchar11_2     DESC
, varchar2_10     ASC
, varchar15_uniq  ASC
)
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """Create View VUwide1 as SELECT * from Twide1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create unique index IWide102 on Twide1 ( char0_1000 DESC );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index IWide107 on Twide1 ( sbin1_100     );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index IWide108 on Twide1 ( char1_4       );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index IWide110 on Twide1 ( ubin1_4       );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index IWide115 on Twide1 ( varchar2_10   );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index IWide116 on Twide1 ( varchar2_100  );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index IWide117 on Twide1 ( sbin3_1000    );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    ##expectfile ${test_dir}/a01exp a01s0a
    stmt = """create index IWide118 on Twide1 ( char3_1000    );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create unique index IWide121 on Twide1 ( ubin3_uniq    );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index IWide122 on Twide1 ( sbin4_2       );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index IWide123 on Twide1 ( ubin4_4       );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index IWide124 on Twide1 ( varchar4_1000 );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index IWide125 on Twide1 ( sdec4_10      );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index IWide126 on Twide1 ( udec4_2       );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index IWide127 on Twide1 ( sbin5_4       );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index IWide128 on Twide1 ( ubin5_20      );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index IWide129 on Twide1 ( udec5_20      );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index IWide130 on Twide1 ( varchar5_4    );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index IWide131 on Twide1 ( sdec5_100     );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index IWide135 on Twide1 ( varchar6_20   );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index IWide137 on Twide1 ( sbin7_2       );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index IWide138 on Twide1 ( sdec7_10      );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create unique index IWide139 on Twide1 ( char7_uniq );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index IWide140 on Twide1 ( udec7_20      );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index IWide141 on Twide1 ( ubin7_100     );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index IWide142 on Twide1 ( sbin8_1000    );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index IWide143 on Twide1 ( varchar8_uniq );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index IWide146 on Twide1 ( ubin8_2       );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index IWide148 on Twide1 ( char9_uniq    );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index IWide149 on Twide1 ( udec9_10      );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index IWide150 on Twide1 ( sdec9_20      );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index IWide154 on Twide1 ( varchar10_20  );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index IWide158 on Twide1 ( sdec11_20     );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index IWide159 on Twide1 ( varchar11_2   );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index IWide161 on Twide1 ( char11_4      );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index IWide162 on Twide1 ( sbin12_1000   );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index IWide164 on Twide1 ( varchar12_4   );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index IWide165 on Twide1 ( ubin12_10     );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index IWide168 on Twide1 ( char13_100    );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index IWide169 on Twide1 ( sdec13_uniq   );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index IWide171 on Twide1 ( udec13_500    );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index IWide172 on Twide1 ( sbin14_100    );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index IWide173 on Twide1 ( ubin14_2      );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index IWide174 on Twide1 ( sdec14_20     );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index IWide175 on Twide1 ( udec14_10     );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index IWide176 on Twide1 ( varchar14_2000);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index IWide177 on Twide1 ( sbin15_2      );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index IWide178 on Twide1 ( udec15_4      );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index IWide179 on Twide1 ( varchar15_uniq);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index IWide180 on Twide1 ( ubin15_uniq   );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index IWide181 on Twide1 ( sdec15_10     );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index IWide182 on Twide1 ( sbin16_20     );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index IWide184 on Twide1 ( ubin16_1000   );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index IWide186 on Twide1 ( varchar16_100 );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index IWide187 on Twide1 ( sbin17_uniq   );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index IWide188 on Twide1 ( sdec17_20     );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index IWide190 on Twide1 ( char17_100    );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    ##expect any *--- SQL operation complete.*
    stmt = """create index IWide191 on Twide1 ( varchar17_20  );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index IWide192 on Twide1 ( sbin18_uniq   );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index IWide193 on Twide1 ( varchar18_uniq);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index IWide197 on Twide1 ( sbin19_4      );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index IWide198 on Twide1 ( char19_2      );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index IWide199 on Twide1 ( ubin19_10     );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index IWide1A0 on Twide1 ( udec19_100    );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index IWide1A1 on Twide1 ( sdec19_1000   );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index IWide1A5 on Twide1 ( varchar20_1000);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
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
    
    _testmgr.testcase_end(desc)

