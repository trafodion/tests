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
    
def test001(desc="""t005"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """set schema """ + defs.my_schema + """;"""
    output = _dci.cmdexec(stmt)
    
    # t005.1:
    # #runscript $test_dir/t005set1
    # script: t005set1
    stmt = """drop table t005t1;"""
    output = _dci.cmdexec(stmt)
    
    # t005set1.1: create table t005t1
    stmt = """create table t005t1 (
sbin0_500        PIC S9(18) COMP   not null,
varchar0_10      varchar(5)        not null,
udec0_2000       PIC 9(9)          not null,
ubin0_1000       PIC 9(9) COMP     not null,
sdec0_uniq       varchar(10)       not null,
varchar0_4       varchar(8)        not null,    

-- char0_10         PIC X(4)          not null,
-- sdec0_uniq       PIC S9(9)         not null,    

sbin1_100        Numeric(9)   signed   not null,
varchar1_4       varchar(6)   not null, -- len = 2,4
varchar1_10      varchar(10)  not null,
ubin1_4          Numeric(9)   unsigned not null,
sdec1_2          PIC S9(9)             not null,    

-- char1_4          PIC X(5)   not null, -- len = 2,4
-- udec1_10         PIC 9(9)              not null,    

sbin2_2          PIC S9(2) COMP   not null,
ubin2_4          PIC 9(2) COMP    not null,
sdec2_10         PIC S9(2)        not null,
varchar2_2       varchar(3)       not null,
varchar2_100     varchar(3)       not null,    

-- char2_2       PIC X(2)        not null,
-- udec2_100     PIC 9(2)         not null,    

sbin3_1000       Numeric(5) signed     not null,
udec3_2000       PIC 9(5)              not null,
varchar3_1000    varchar(300)          not null, -- len = 64,300
sdec3_500        PIC S9(5)             not null,
ubin3_uniq       Numeric(5) unsigned   not null,    

-- char3_1000       PIC X(300)   not null, -- len = 64,300    

varchar4_2          varchar(4) not null,
varchar4_4          varchar(4) not null,
varchar4_10         varchar(5) not null, -- len = 2,4
varchar4_1a         varchar(4) not null,
varchar4_2a         varchar(4) not null,
-- sbin4_2          Numeric(1,1) signed     not null,
-- ubin4_4          Numeric(1,1) unsigned   not null,
-- char4_10         Character(5)   not null, -- len = 2,4
-- sdec4_10         Decimal(1,1) signed     not null,
-- udec4_2          Decimal(1,1) unsigned   not null,    

sbin5_4          Numeric(4) signed     not null,
ubin5_20         Numeric(9) unsigned   not null,
udec5_20         Decimal(4) unsigned   not null,
-- varchar5_10      varchar(8)  not null,
varchar5_10      varchar(2048) not null,
varchar5_100     varchar(19)   not null,    

-- varchar5_10      Char(8)       not null,
-- sdec5_100        Decimal(18) signed    not null,    

sbin6_uniq       PIC S9(4) COMP   not null,
sdec6_2000       PIC S9(4)        not null,
udec6_500        PIC 9(4)         not null,
-- varchar6_20      varchar(8)         not null,
varchar6_20      varchar(8192)         not null,
ubin6_2          PIC 9(4) COMP    not null,    

-- char6_20         PIC X(8)         not null,    

sbin7_2          SMALLINT signed         not null,
sdec7_10         Decimal(4,1) signed     not null,
char7_uniq       varchar(100)   not null, -- len = 16
udec7_20         Decimal(4,1) unsigned   not null,
ubin7_100        SMALLINT unsigned       not null,    

-- char7_uniq       Character(100)   not null, -- len = 16    

sbin8_1000       Numeric(18) signed      not null,
varchar8_500     varchar(100)   not null, -- len = 16
sdec8_2000       PIC S9(3)V9             not null,
udec8_500        PIC 9(3)V9              not null,
ubin8_2          Numeric(4,1) unsigned   not null,    

-- char8_500        PIC X(100)   not null, -- len = 16    

sbin9_4          PIC S9(3)V9 COMP      not null,
varchar9_uniq    varchar(8)          not null,
varchar9_10      varchar(6) not null,
varchar9_20      varchar(6) not null,
ubin9_100        PIC 9(3)V9 COMP       not null,    

-- char9_uniq       Character(8)          not null,
-- udec9_10         Decimal(5) unsigned   not null,
-- sdec9_20         Decimal(5) signed     not null,    

sbin10_uniq      PIC S9(9) COMP   not null,
ubin10_1000      PIC 9(9) COMP    not null,
varchar10_20     varchar(5)       not null, -- len = 2,4
udec10_2000      PIC 9(9)         not null,
sdec10_500       PIC S9(18)       not null,    

-- char10_20        PIC X(5)   not null, -- len = 2,4    

sbin11_2000      PIC S9(5) COMP          not null,
sdec11_20        Decimal(5,5) signed     not null,
udec11_20        Decimal(5,5) unsigned   not null,
ubin11_2         PIC 9(5) COMP           not null,
varchar11_4      varchar(2)              not null,
-- char11_4         Character(2)            not null,    

varchar12_1000   varchar(10) not null,
varchar12_100    varchar(10) not null,
varchar12_10     varchar(2)  not null,
ubin12_10        Numeric(9) unsigned   not null,
udec12_1000      PIC 9(9)              not null,    

-- sbin12_1000      Numeric(9) signed     not null,
-- sdec12_100       PIC S9(9)             not null,
-- char12_10        PIC X(2)              not null,    

sbin13_uniq      PIC SV9(5) COMP       not null,
varchar13_100    varchar(5)   not null, -- len = 2,4
sdec13_uniq      Decimal(9) signed     not null,
ubin13_10        PIC V9(5) COMP        not null,
udec13_500       Decimal(9) unsigned   not null,    

-- char13_100       Character(5)   not null, -- len = 2,4    

varchar14_100    varchar(3) not null,
varchar14_2      varchar(3) not null,
varchar14_20     varchar(3) not null,
varchar14_10     varchar(3) not null,
varchar14_2a     varchar(3) not null,    

-- sbin14_100       Numeric(2) signed     not null,
-- ubin14_2         Numeric(2) unsigned   not null,
-- sdec14_20        Decimal(2) signed     not null,
-- udec14_10        Decimal(2) unsigned   not null,
-- char14_20        Character(2)          not null,    

sbin15_2         INTEGER signed          not null,
udec15_4         Decimal(9,2) unsigned   not null,
varchar15_uniq   varchar(8)              not null,
ubin15_uniq      INTEGER unsigned        not null,
sdec15_10        Decimal(9,2) signed     not null,    

-- varchar15_uniq   Char(8)         not null,    

sbin16_20        Numeric(9,2) signed     not null,
sdec16_100       PIC S9(7)V9(2)          not null,
ubin16_1000      Numeric(9,2) unsigned   not null,
udec16_1000      PIC 9(7)V9(2)           not null,
varchar16_uniq   varchar(8)              not null,    

-- char16_uniq      PIC X(8)                not null,    

sbin17_uniq      Numeric(10) signed    not null,
sdec17_20        Decimal(2) signed     ,
ubin17_2000      PIC 9(7)V9(2) COMP    ,
-- varchar17_100    varchar(100)   not null,
varchar17_100    varchar(1024) not null, -- len = 16
udec17_100       Decimal(2) unsigned   ,    

-- char17_100       Character(100)   not null, -- len = 16    

sbin18_uniq      Numeric(18) signed   not null,
-- varchar18_20     varchar(100)         not null, -- len = 16
varchar18_20     varchar(4096)        not null, -- len = 16
ubin18_20        PIC 9(2) COMP        not null,
sdec18_4         PIC S9(2)            not null,
udec18_4         PIC 9(2)             not null,    

-- char18_20        PIC X(100)           not null, -- len = 16    

sbin19_4         LARGEINT signed         not null,
char19_2         Character(8)            not null,
ubin19_10        SMALLINT unsigned       not null,
varchar19_100    varchar(5) not null,
varchar19_1000   varchar(5) not null,    

-- udec19_100       Decimal(4,1) signed     not null,
-- sdec19_1000      Decimal(4,1) unsigned   not null,    

sbin20_2000      PIC S9(16)V9(2) COMP   not null,
udec20_uniq      PIC 9(9)               not null,
ubin20_1000      PIC 9(3)V9 COMP        not null,
varchar20_10     varchar(300)           not null, -- len = 64,300
sdec20_uniq      PIC S9(9)              not null   -- range: 0-24999    

-- char20_10        PIC X(300)   not null, -- len = 64,300
, primary key (sdec20_uniq,
varchar2_2,     -- nonadjacent key
varchar4_2,     -- adjacent key
varchar4_4,     -- adjacent key
varchar4_10,    -- adjacent key
varchar9_uniq,  -- nonadjacent key
varchar9_10,    -- adjacent key
varchar13_100,
varchar15_uniq, -- nonadjacent key
varchar16_uniq, -- nonadjacent key
varchar19_100)  not droppable
)
store by primary key;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
  
    # #sh import ${test_schema1}.t005t1 -I ${test_dir}/uw00.dat
    # $SQL_inserted_msg 250
    # insert into ${test_schema1}.t005t1 select * from ${exereg_schema}.uw00;
 
    prop_template = defs.test_dir + '/../../lib/t4properties.template'
    prop_file = defs.work_dir + '/t4properties'
    hpdci.create_jdbc_propfile(prop_template, prop_file, defs.w_catalog, defs.w_schema)

    table = defs.my_schema + """.t005t1"""
    data_file = defs.test_dir + """/uw00.dat"""
    output = _testmgr.data_loader(defs.work_dir, prop_file, table, data_file, ',')
    _dci.expect_loaded_msg(output)
 
    stmt = """select count(*) from t005t1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, """250""")
    
    # t005.2: select single row - sdec20_uniq=10195
    # #runscript $test_dir/t0050sql
    # script: t0050sql
    # t0050.1:
    stmt = """select sdec20_uniq, sdec0_uniq, sdec13_uniq, udec20_uniq
from t005t1 order by sdec20_uniq;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t0050exp""", """s01""")
    
    # t0050.2:
    stmt = """select sdec20_uniq, ubin3_uniq, sbin6_uniq, sbin10_uniq
from t005t1 order by sdec20_uniq;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t0050exp""", """s02""")
    
    # t0050.3:
    stmt = """select sdec20_uniq, ubin15_uniq, sbin17_uniq, sbin18_uniq
from t005t1 order by sdec20_uniq;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t0050exp""", """s03""")
    
    # t0050.4:
    stmt = """select varchar14_100, varchar14_2, varchar14_20, varchar14_10,
varchar14_2a from t005t1 order by sdec20_uniq;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t0050exp""", """s04""")
    
    # t0050.5:
    stmt = """select varchar0_4, varchar1_4, varchar2_100, substring(varchar3_1000,1,25)
from t005t1 order by sdec20_uniq;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t0050exp""", """s05""")
    
    # t0050.6:
    stmt = """select substring(varchar5_10,1,8) as varchar5_10,
varchar5_100, substring(varchar8_500,1,25), varchar10_20
from t005t1 order by sdec20_uniq;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t0050exp""", """s06""")
    
    # t0050.7: 9 rows
    stmt = """select sdec20_uniq, varchar2_2, varchar9_uniq, varchar9_10, varchar13_100,
varchar15_uniq, varchar16_uniq, varchar19_100
from t005t1
where sdec20_uniq < 2000 and sdec20_uniq > 1000
and ubin3_uniq    = ubin15_uniq
and sbin10_uniq   = sbin18_uniq
and varchar9_uniq = varchar15_uniq
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t0050exp""", """s07""")
    
    # t0050.8:
    stmt = """select sdec20_uniq, varchar2_2, varchar9_uniq, varchar9_10, varchar13_100,
varchar15_uniq, varchar16_uniq, varchar19_100
from t005t1
where substring(varchar9_uniq,7,2)  = varchar13_100
and substring(varchar15_uniq,3,2) = varchar2_2 order by sdec20_uniq;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t0050exp""", """s08""")
    
    # t0050.9:
    stmt = """select sdec20_uniq, varchar2_2, varchar9_uniq, varchar9_10, varchar13_100,
varchar15_uniq, varchar16_uniq, varchar19_100
from t005t1
where sdec20_uniq = 10195
and varchar2_2  = 'BA'
and varchar4_2  = '0.1'
and varchar4_4  = '0.1'
and varchar4_10 = 'ABAA'
and varchar9_uniq  = 'BIAALAAB'
and varchar9_10    = '3'
and varchar13_100  = 'BGAA'
and varchar15_uniq = 'BIAALAAB'
and varchar16_uniq = 'BIAALAAB'
and varchar19_100  = '9.7' order by sdec20_uniq;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t0050exp""", """s09""")
    
    # t0050.11:
    stmt = """select sdec20_uniq, sbin0_500, varchar0_10, udec0_2000,
ubin0_1000, sdec0_uniq, varchar0_4
from t005t1
where sdec20_uniq = 10195
and (varchar9_uniq, varchar9_10, varchar13_100)
= ('BIAALAAB','3','BGAA') order by sdec20_uniq;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t0050exp""", """s11""")
    
    # t0050.12:
    stmt = """select sdec20_uniq, sbin3_1000, udec3_2000, varchar3_1000,
sdec3_500, ubin3_uniq
from t005t1
where sdec20_uniq = 10195
and (varchar4_10, varchar15_uniq, varchar16_uniq)
= ('ABAA','BIAALAAB','BIAALAAB') order by sdec20_uniq;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t0050exp""", """s12""")
    
    # t0050.13:
    stmt = """select sdec20_uniq, varchar4_2, varchar4_4, varchar4_10,
varchar4_1a, varchar4_2a
from t005t1
where sdec20_uniq = 10195
and (varchar4_2, varchar4_4, varchar4_10)
= ('0.1','0.1','ABAA') order by sdec20_uniq;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t0050exp""", """s13""")
    
    # t0050.14:
    stmt = """select sdec20_uniq, sbin5_4, ubin5_20, udec5_20,
substring(varchar5_10,1,8) as varchar5_10, varchar5_100
from t005t1
where sdec20_uniq = 10195
and (varchar9_uniq, varchar15_uniq, varchar16_uniq)
= ('BIAALAAB','BIAALAAB','BIAALAAB') order by sdec20_uniq;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t0050exp""", """s14""")
    
    # t0050.15:
    stmt = """select sdec20_uniq, varchar14_100, varchar14_2, varchar14_20,
varchar14_10, varchar14_2a
from t005t1
where sdec20_uniq = 10195
and (varchar9_uniq, varchar15_uniq, varchar16_uniq)
= ('BIAALAAB','BIAALAAB','BIAALAAB') order by sdec20_uniq;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t0050exp""", """s15""")
    
    # t0050.16:
    stmt = """select sdec20_uniq, sbin20_2000, udec20_uniq, ubin20_1000, varchar20_10
from t005t1
where sdec20_uniq = 10195
and (varchar9_uniq, varchar15_uniq, varchar16_uniq)
= ('BIAALAAB','BIAALAAB','BIAALAAB') order by sdec20_uniq;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t0050exp""", """s16""")
    
    # t005.3: select within a range between 22185 and 22385
    # 2 rows selected: 22186 and 22394
    # #runscript $test_dir/t0051sql
    # script: t0051sql
    
    stmt = """set param ?p1 22185;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p2 22395;"""
    output = _dci.cmdexec(stmt)
    
    # t0051.0:
    stmt = """select sbin0_500, varchar0_10, udec0_2000, ubin0_1000, sdec0_uniq, varchar0_4
from t005t1 where sdec20_uniq > cast (?p1 as integer)
and sdec20_uniq < cast (?p2 as integer) order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t0051exp""", """s00""")
    
    # t0051.1:
    stmt = """select sbin1_100, varchar1_4, varchar1_10, ubin1_4, sdec1_2
from t005t1 where sdec20_uniq > cast (?p1 as integer)
and sdec20_uniq < cast (?p2 as integer) order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t0051exp""", """s01""")
    
    # t0051.2:
    stmt = """select sbin2_2, ubin2_4, sdec2_10, varchar2_2, varchar2_100
from t005t1 where sdec20_uniq > cast (?p1 as integer)
and sdec20_uniq < cast (?p2 as integer) order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t0051exp""", """s02""")
    
    # t0051.3:
    stmt = """select sbin3_1000, udec3_2000,
substring(varchar3_1000,1,300) as varchar3_1000, sdec3_500, ubin3_uniq
from t005t1 where sdec20_uniq > cast (?p1 as integer)
and sdec20_uniq < cast (?p2 as integer) order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t0051exp""", """s03""")
    
    # t0051.4:
    stmt = """select varchar4_2, varchar4_4, varchar4_10, varchar4_1a, varchar4_2a
from t005t1 where sdec20_uniq > cast (?p1 as integer)
and sdec20_uniq < cast (?p2 as integer) order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t0051exp""", """s04""")
    
    # t0051.5:
    stmt = """select sbin5_4, ubin5_20, udec5_20,
substring(varchar5_10,1,8) as varchar5_10, varchar5_100
from t005t1 where sdec20_uniq > cast (?p1 as integer)
and sdec20_uniq < cast (?p2 as integer) order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t0051exp""", """s05""")
    
    # t0051.6:
    stmt = """select sbin6_uniq, sdec6_2000, udec6_500,
substring(varchar6_20,1,8) as varchar6_20, ubin6_2
from t005t1 where sdec20_uniq > cast (?p1 as integer)
and sdec20_uniq < cast (?p2 as integer) order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t0051exp""", """s06""")
    
    # t0051.7:
    stmt = """select sbin7_2, sdec7_10, char7_uniq, udec7_20, ubin7_100
from t005t1 where sdec20_uniq > cast (?p1 as integer)
and sdec20_uniq < cast (?p2 as integer) order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t0051exp""", """s07""")
    
    # t0051.8:
    stmt = """select sbin8_1000, varchar8_500, sdec8_2000, udec8_500, ubin8_2
from t005t1 where sdec20_uniq > cast (?p1 as integer)
and sdec20_uniq < cast (?p2 as integer) order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t0051exp""", """s08""")
    
    # t0051.9:
    stmt = """select sbin9_4, varchar9_uniq, varchar9_10, varchar9_20, ubin9_100
from t005t1 where sdec20_uniq > cast (?p1 as integer)
and sdec20_uniq < cast (?p2 as integer) order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t0051exp""", """s09""")
    
    # t0051.10:
    stmt = """select sbin10_uniq, ubin10_1000, varchar10_20, udec10_2000, sdec10_500
from t005t1 where sdec20_uniq > cast (?p1 as integer)
and sdec20_uniq < cast (?p2 as integer) order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t0051exp""", """s10""")
    
    # t0051.11:
    stmt = """select sbin11_2000, sdec11_20, udec11_20, ubin11_2, varchar11_4
from t005t1 where sdec20_uniq > cast (?p1 as integer)
and sdec20_uniq < cast (?p2 as integer) order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t0051exp""", """s11""")
    
    # t0051.12:
    stmt = """select varchar12_1000, varchar12_100, varchar12_10, ubin12_10, udec12_1000
from t005t1 where sdec20_uniq > cast (?p1 as integer)
and sdec20_uniq < cast (?p2 as integer) order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t0051exp""", """s12""")
    
    # t0051.13:
    stmt = """select sbin13_uniq, varchar13_100, sdec13_uniq, ubin13_10, udec13_500
from t005t1 where sdec20_uniq > cast (?p1 as integer)
and sdec20_uniq < cast (?p2 as integer) order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t0051exp""", """s13""")
    
    # t0051.14:
    stmt = """select varchar14_100, varchar14_2, varchar14_20, varchar14_10, varchar14_2a
from t005t1 where sdec20_uniq > cast (?p1 as integer)
and sdec20_uniq < cast (?p2 as integer) order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t0051exp""", """s14""")
    
    # t0051.15:
    stmt = """select sbin15_2, udec15_4, varchar15_uniq, ubin15_uniq, sdec15_10
from t005t1 where sdec20_uniq > cast (?p1 as integer)
and sdec20_uniq < cast (?p2 as integer) order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t0051exp""", """s15""")
    
    # t0051.16:
    stmt = """select sbin16_20, sdec16_100, ubin16_1000, udec16_1000, varchar16_uniq
from t005t1 where sdec20_uniq > cast (?p1 as integer)
and sdec20_uniq < cast (?p2 as integer) order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t0051exp""", """s16""")
    
    # t0051.17:
    stmt = """select sbin17_uniq, sdec17_20, ubin17_2000,
substring(varchar17_100,1,100) as varchar17_100, udec17_100
from t005t1 where sdec20_uniq > cast (?p1 as integer)
and sdec20_uniq < cast (?p2 as integer) order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t0051exp""", """s17""")
    
    # t0051.18:
    stmt = """select sbin18_uniq, substring(varchar18_20,1,100) as varchar18_20,
ubin18_20, sdec18_4, udec18_4
from t005t1 where sdec20_uniq > cast (?p1 as integer)
and sdec20_uniq < cast (?p2 as integer) order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t0051exp""", """s18""")
    
    # t0051.19:
    stmt = """select sbin19_4, char19_2, ubin19_10, varchar19_100, varchar19_1000
from t005t1 where sdec20_uniq > cast (?p1 as integer)
and sdec20_uniq < cast (?p2 as integer) order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t0051exp""", """s19""")
    
    # t0051.20:
    stmt = """select sbin20_2000, udec20_uniq, ubin20_1000, varchar20_10, sdec20_uniq
from t005t1 where sdec20_uniq > cast (?p1 as integer)
and sdec20_uniq < cast (?p2 as integer) order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t0051exp""", """s20""")
    
    stmt = """drop table t005tmp1;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table t005tmp2;"""
    output = _dci.cmdexec(stmt)
    
    # t005.5:
    stmt = """create table t005tmp1 like t005t1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    table = defs.my_schema + """.t005tmp1"""
    data_file = defs.test_dir + """/uw01.dat"""
    output = _testmgr.data_loader(defs.work_dir, prop_file, table, data_file, ',')
    _dci.expect_loaded_msg(output)
   
 
    # t005.8:
    stmt = """select count(*) from t005tmp1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, """249""")
    
    #expect purge
    stmt = """create index t005idx1 on t005t1 (varchar2_2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index t005idx2 on t005t1 (varchar4_2);"""
    output = _dci.cmdexec(stmt)
    stmt = """create index t005idx3 on t005t1 (varchar4_4);"""
    output = _dci.cmdexec(stmt)
    stmt = """create index t005idx4 on t005t1 (varchar4_10);"""
    output = _dci.cmdexec(stmt)
    stmt = """create index t005idx5 on t005t1 (varchar9_uniq);"""
    output = _dci.cmdexec(stmt)
    stmt = """create index t005idx6 on t005t1 (varchar9_10);"""
    output = _dci.cmdexec(stmt)
    stmt = """create index t005idx7 on t005t1 (varchar13_100);"""
    output = _dci.cmdexec(stmt)
    stmt = """create index t005idx8 on t005t1 (varchar15_uniq);"""
    output = _dci.cmdexec(stmt)
    stmt = """create index t005idx9 on t005t1 (varchar16_uniq);"""
    output = _dci.cmdexec(stmt)
    stmt = """create index t005idxa on t005t1 (varchar19_100);"""
    output = _dci.cmdexec(stmt)
    
    # t005.9: insert sdec20_uniq=22372
    # #runscript $test_dir/t005insert
    # script: t005insert
    
    stmt = """insert into t005t1 values (
-- 0
399,'BEAA',399,399,'2399','DAAAAAAA',
-- 1
43,'BAAA','3',3,1,
-- 2
1,1,5,'BA','65',
-- 3
961,961,'FHAAFAAMcKinleyAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',461,4961,
-- 4
'0.1','0.3','AEAA','0.9','0.1',
-- 5
3,3,3,'BEAAAAAA','43',
-- 6
4965,965,465,'DEAAAAAA',1,
-- 7
1,0.1,'FBAAHAAEAAAAAAAA',0.1,61,
-- 8
399,'FHAAFAAMcKinleyA',39.9,39.9,0.1,
-- 9
0.3,'FBAAHAAE','3','3',4.3,
-- 10
4965,965,'BEAA',965,465,
-- 11
961,0.00001,0.00001,1,'DA',
-- 12
'399','99','BE',9,399,
-- 13
0.01943,'BYAA',1943,0.00003,443,
-- 14
'65','1','5','5','DE',
-- 15
1,0.01,'FBAAHAAE',4961,0.01,
-- 16
0.19,0.99,3.99,3.99,'FBAAHAAE',
-- 17
1943,3,19.43,'DYAAMcKinleyAAAA',43,
-- 18
4965,'DEAAMcKinleyAAAA',5,1,1,
-- 19
1,'BAAAAAAA',1,'6.1','96.1',
-- 20
3.99,2399,39.9,'AEAAMcKinleyAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',22372);"""
    output = _dci.cmdexec(stmt)
    
    # t005.10: select a range of rows
    # 3 rows selected: 22186, 22372, and 22394
    # #runscript $test_dir/t0052sql
    # script: t0052sql
    
    stmt = """set param ?p1 22185;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p2 22395;"""
    output = _dci.cmdexec(stmt)
    
    # t0052.0:
    stmt = """select sbin0_500, varchar0_10, udec0_2000, ubin0_1000, sdec0_uniq, varchar0_4
from t005t1 where sdec20_uniq > ?p1 and sdec20_uniq < ?p2
order by sdec20_uniq;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t0052exp""", """s00""")
    
    # t0052.1:
    stmt = """select sbin1_100, varchar1_4, varchar1_10, ubin1_4, sdec1_2
from t005t1 where sdec20_uniq > ?p1 and sdec20_uniq < ?p2
order by sdec20_uniq;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t0052exp""", """s01""")
    
    # t0052.2:
    stmt = """select sbin2_2, ubin2_4, sdec2_10, varchar2_2, varchar2_100
from t005t1 where sdec20_uniq > ?p1 and sdec20_uniq < ?p2
order by sdec20_uniq;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t0052exp""", """s02""")
    
    # t0052.3:
    stmt = """select sbin3_1000, udec3_2000, varchar3_1000, sdec3_500, ubin3_uniq
from t005t1 where sdec20_uniq > ?p1 and sdec20_uniq < ?p2
order by sdec20_uniq;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t0052exp""", """s03""")
    
    # t0052.4:
    stmt = """select varchar4_2, varchar4_4, varchar4_10, varchar4_1a, varchar4_2a
from t005t1 where sdec20_uniq > ?p1 and sdec20_uniq < ?p2
order by sdec20_uniq;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t0052exp""", """s04""")
    
    # t0052.5:
    stmt = """select sbin5_4, ubin5_20, udec5_20,
substring(varchar5_10,1,8) as varchar5_10, varchar5_100
from t005t1 where sdec20_uniq > ?p1 and sdec20_uniq < ?p2
order by sdec20_uniq;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t0052exp""", """s05""")
    
    # t0052.6:
    stmt = """select sbin6_uniq, sdec6_2000, udec6_500,
substring(varchar6_20,1,8) as varchar6_20, ubin6_2
from t005t1 where sdec20_uniq > ?p1 and sdec20_uniq < ?p2
order by sdec20_uniq;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t0052exp""", """s06""")
    
    # t0052.7:
    stmt = """select sbin7_2, sdec7_10, char7_uniq, udec7_20, ubin7_100
from t005t1 where sdec20_uniq > ?p1 and sdec20_uniq < ?p2
order by sdec20_uniq;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t0052exp""", """s07""")
    
    # t0052.8:
    stmt = """select sbin8_1000, varchar8_500, sdec8_2000, udec8_500, ubin8_2
from t005t1 where sdec20_uniq > ?p1 and sdec20_uniq < ?p2
order by sdec20_uniq;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t0052exp""", """s08""")
    
    # t0052.9:
    stmt = """select sbin9_4, varchar9_uniq, varchar9_10, varchar9_20, ubin9_100
from t005t1 where sdec20_uniq > ?p1 and sdec20_uniq < ?p2
order by sdec20_uniq;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t0052exp""", """s09""")
    
    # t0052.10:
    stmt = """select sbin10_uniq, ubin10_1000, varchar10_20, udec10_2000, sdec10_500
from t005t1 where sdec20_uniq > ?p1 and sdec20_uniq < ?p2
order by sdec20_uniq;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t0052exp""", """s10""")
    
    # t0052.11:
    stmt = """select sbin11_2000, sdec11_20, udec11_20, ubin11_2, varchar11_4
from t005t1 where sdec20_uniq > ?p1 and sdec20_uniq < ?p2
order by sdec20_uniq;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t0052exp""", """s11""")
    
    # t0052.12:
    stmt = """select varchar12_1000, varchar12_100, varchar12_10, ubin12_10, udec12_1000
from t005t1 where sdec20_uniq > ?p1 and sdec20_uniq < ?p2
order by sdec20_uniq;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t0052exp""", """s12""")
    
    # t0052.13:
    stmt = """select sbin13_uniq, varchar13_100, sdec13_uniq, ubin13_10, udec13_500
from t005t1 where sdec20_uniq > ?p1 and sdec20_uniq < ?p2
order by sdec20_uniq;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t0052exp""", """s13""")
    
    # t0052.14:
    stmt = """select varchar14_100, varchar14_2, varchar14_20, varchar14_10, varchar14_2a
from t005t1 where sdec20_uniq > ?p1 and sdec20_uniq < ?p2
order by sdec20_uniq;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t0052exp""", """s14""")
    
    # t0052.15:
    stmt = """select sbin15_2, udec15_4, varchar15_uniq, ubin15_uniq, sdec15_10
from t005t1 where sdec20_uniq > ?p1 and sdec20_uniq < ?p2
order by sdec20_uniq;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t0052exp""", """s15""")
    
    # t0052.16:
    stmt = """select sbin16_20, sdec16_100, ubin16_1000, udec16_1000, varchar16_uniq
from t005t1 where sdec20_uniq > ?p1 and sdec20_uniq < ?p2
order by sdec20_uniq;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t0052exp""", """s16""")
    
    # t0052.17:
    stmt = """select sbin17_uniq, sdec17_20, ubin17_2000,
substring(varchar17_100,1,100) as varchar17_100, udec17_100
from t005t1 where sdec20_uniq > ?p1 and sdec20_uniq < ?p2
order by sdec20_uniq;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t0052exp""", """s17""")
    
    # t0052.18:
    stmt = """select sbin18_uniq, substring(varchar18_20,1,100) as varchar18_20,
ubin18_20, sdec18_4, udec18_4
from t005t1 where sdec20_uniq > ?p1 and sdec20_uniq < ?p2
order by sdec20_uniq;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t0052exp""", """s18""")
    
    # t0052.19:
    stmt = """select sbin19_4, char19_2, ubin19_10, varchar19_100, varchar19_1000
from t005t1 where sdec20_uniq > ?p1 and sdec20_uniq < ?p2
order by sdec20_uniq;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t0052exp""", """s19""")
    
    # t0052.20:
    stmt = """select sbin20_2000, udec20_uniq, ubin20_1000, varchar20_10, sdec20_uniq
from t005t1 where sdec20_uniq > ?p1 and sdec20_uniq < ?p2
order by sdec20_uniq;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t0052exp""", """s20""")
    
    # t005.11: create t005tmp2 table
    # #runscript $test_dir/t005set2
    # script: t005set2
    stmt = """drop table t005tmp2;"""
    output = _dci.cmdexec(stmt)
    
    # t005set2.1: create table t005tmp2
    stmt = """create table t005tmp2 (
sbinA_500        PIC S9(18) COMP   not null,
varcharA_10      varchar(5)        not null,
udecA_2000       PIC 9(9)          not null,
ubinA_1000       PIC 9(9) COMP     not null,
sdecA_uniq       varchar(10)       not null,
varcharA_4       varchar(8)        not null,    

-- char0_10         PIC X(4)          not null,
-- sdec0_uniq       PIC S9(9)         not null,    

sbinB_100        Numeric(9)   signed   not null,
varcharB_4       varchar(6)   not null, -- len = 2,4
varcharB_10      varchar(10)  not null,
ubinB_4          Numeric(9)   unsigned not null,
sdecB_2          PIC S9(9)             not null,    

-- char1_4          PIC X(5)   not null, -- len = 2,4
-- udec1_10         PIC 9(9)              not null,    

sbinC_2          PIC S9(2) COMP   not null,
ubinC_4          PIC 9(2) COMP    not null,
sdecC_10         PIC S9(2)        not null,
varcharC_2       varchar(3)       not null,
varcharC_100     varchar(3)       not null,    

-- char2_2       PIC X(2)        not null,
-- udec2_100     PIC 9(2)         not null,    

sbinD_1000       Numeric(5) signed     not null,
udecD_2000       PIC 9(5)              not null,
varcharD_1000    varchar(300)          not null, -- len = 64,300
sdecD_500        PIC S9(5)             not null,
ubinD_uniq       Numeric(5) unsigned   not null,    

-- char3_1000       PIC X(300)   not null, -- len = 64,300    

varcharE_2          varchar(4) not null,
varcharE_4          varchar(4) not null,
varcharE_10         varchar(5) not null, -- len = 2,4
varcharE_1a         varchar(4) not null,
varcharE_2a         varchar(4) not null,
-- sbin4_2          Numeric(1,1) signed     not null,
-- ubin4_4          Numeric(1,1) unsigned   not null,
-- char4_10         Character(5)   not null, -- len = 2,4
-- sdec4_10         Decimal(1,1) signed     not null,
-- udec4_2          Decimal(1,1) unsigned   not null,    

sbinF_4          Numeric(4) signed     not null,
ubinF_20         Numeric(9) unsigned   not null,
udecF_20         Decimal(4) unsigned   not null,
varcharF_10      varchar(8)  not null,
varcharF_100     varchar(19) not null,    

-- varchar5_10      Char(8)       not null,
-- sdec5_100        Decimal(18) signed    not null,    

sbinG_uniq       PIC S9(4) COMP   not null,
sdecG_2000       PIC S9(4)        not null,
udecG_500        PIC 9(4)         not null,
varcharG_20      varchar(8)         not null,
ubinG_2          PIC 9(4) COMP    not null,    

-- char6_20         PIC X(8)         not null,    

sbinH_2          SMALLINT signed         not null,
sdecH_10         Decimal(4,1) signed     not null,
charH_uniq       varchar(100)   not null, -- len = 16
udecH_20         Decimal(4,1) unsigned   not null,
ubinH_100        SMALLINT unsigned       not null,    

-- char7_uniq       Character(100)   not null, -- len = 16    

sbinI_1000       Numeric(18) signed      not null,
varcharI_500     varchar(100)   not null, -- len = 16
sdecI_2000       PIC S9(3)V9             not null,
udecI_500        PIC 9(3)V9              not null,
ubinI_2          Numeric(4,1) unsigned   not null,    

-- char8_500        PIC X(100)   not null, -- len = 16    

sbinJ_4          PIC S9(3)V9 COMP      not null,
varcharJ_uniq    varchar(8)          not null,
varcharJ_10      varchar(6) not null,
varcharJ_20      varchar(6) not null,
ubinJ_100        PIC 9(3)V9 COMP       not null,    

-- char9_uniq       Character(8)          not null,
-- udec9_10         Decimal(5) unsigned   not null,
-- sdec9_20         Decimal(5) signed     not null,    

sbinK_uniq      PIC S9(9) COMP   not null,
ubinK_1000      PIC 9(9) COMP    not null,
varcharK_20     varchar(5)       not null, -- len = 2,4
udecK_2000      PIC 9(9)         not null,
sdecK_500       PIC S9(18)       not null,    

-- char10_20        PIC X(5)   not null, -- len = 2,4    

sbinL_2000      PIC S9(5) COMP          not null,
sdecL_20        Decimal(5,5) signed     not null,
udecL_20        Decimal(5,5) unsigned   not null,
ubinL_2         PIC 9(5) COMP           not null,
varcharL_4      varchar(2)              not null,
-- char11_4         Character(2)            not null,    

varcharM_1000   varchar(10) not null,
varcharM_100    varchar(10) not null,
varcharM_10     varchar(2)  not null,
ubinM_10        Numeric(9) unsigned   not null,
udecM_1000      PIC 9(9)              not null,    

-- sbin12_1000      Numeric(9) signed     not null,
-- sdec12_100       PIC S9(9)             not null,
-- char12_10        PIC X(2)              not null,    

sbinN_uniq      PIC SV9(5) COMP       not null,
varcharN_100    varchar(5)   not null, -- len = 2,4
sdecN_uniq      Decimal(9) signed     not null,
ubinN_10        PIC V9(5) COMP        not null,
udecN_500       Decimal(9) unsigned   not null,    

-- char13_100       Character(5)   not null, -- len = 2,4    

varcharO_100    varchar(3) not null,
varcharO_2      varchar(3) not null,
varcharO_20     varchar(3) not null,
varcharO_10     varchar(3) not null,
varcharO_2a     varchar(3) not null,    

-- sbin14_100       Numeric(2) signed     not null,
-- ubin14_2         Numeric(2) unsigned   not null,
-- sdec14_20        Decimal(2) signed     not null,
-- udec14_10        Decimal(2) unsigned   not null,
-- char14_20        Character(2)          not null,    

sbinP_2         INTEGER signed          not null,
udecP_4         Decimal(9,2) unsigned   not null,
varcharP_uniq   varchar(8)              not null,
ubinP_uniq      INTEGER unsigned        not null,
sdecP_10        Decimal(9,2) signed     not null,    

-- varchar15_uniq   Char(8)         not null,    

sbinQ_20        Numeric(9,2) signed     not null,
sdecQ_100       PIC S9(7)V9(2)          not null,
ubinQ_1000      Numeric(9,2) unsigned   not null,
udecQ_1000      PIC 9(7)V9(2)           not null,
varcharQ_uniq   varchar(8)              not null,    

-- char16_uniq      PIC X(8)                not null,    

sbinR_uniq      Numeric(10) signed    not null,
sdecR_20        Decimal(2) signed     ,
ubinR_2000      PIC 9(7)V9(2) COMP    ,
varcharR_100    varchar(100)   not null, -- len = 16
udecR_100       Decimal(2) unsigned   ,    

-- char17_100       Character(100)   not null, -- len = 16    

sbinS_uniq      Numeric(18) signed   not null,
varcharS_20     varchar(100)         not null, -- len = 16
ubinS_20        PIC 9(2) COMP        not null,
sdecS_4         PIC S9(2)            not null,
udecS_4         PIC 9(2)             not null,    

-- char18_20        PIC X(100)           not null, -- len = 16    

sbinT_4         LARGEINT signed         not null,
charT_2         Character(8)            not null,
ubinT_10        SMALLINT unsigned       not null,
varcharT_100    varchar(5) not null,
varcharT_1000   varchar(5) not null,    

-- udec19_100       Decimal(4,1) signed     not null,
-- sdec19_1000      Decimal(4,1) unsigned   not null,    

sbinU_2000      PIC S9(16)V9(2) COMP   not null,
udecU_uniq      PIC 9(9)               not null,
ubinU_1000      PIC 9(3)V9 COMP        not null,
varcharU_10     varchar(300)           not null, -- len = 64,300
sdecU_uniq      PIC S9(9)              not null   -- range: 0-24999    

-- char20_10        PIC X(300)   not null, -- len = 64,300
, primary key (sdecU_uniq,
varcharC_2,     -- nonadjacent key
varcharE_2,     -- adjacent key
varcharE_4,     -- adjacent key
varcharE_10,    -- adjacent key
varcharJ_uniq,  -- nonadjacent key
varcharJ_10,    -- adjacent key
varcharN_100,
varcharP_uniq, -- nonadjacent key
varcharQ_uniq, -- nonadjacent key
varcharT_100)  not droppable
)
store by primary key;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t005.13:
    stmt = """insert into t005tmp2 (select * from t005t1);"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    _dci.expect_inserted_msg(output, 251)
    
    # t005.14:
    stmt = """select count(*) from t005tmp2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, """251""")
    
    # t005.15: select a range of rows
    # 3 rows selected: 22186, 22372, and 22394
    # #runscript $test_dir/t0053sql
    # script: t0053sql
    
    stmt = """set param ?p1 22185;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p2 22395;"""
    output = _dci.cmdexec(stmt)
    
    # t0053.0:
    stmt = """select sbinA_500, varcharA_10, udecA_2000, ubinA_1000, sdecA_uniq, varcharA_4
from t005tmp2 where sdecU_uniq > ?p1 and sdecU_uniq < ?p2
order by sdecU_uniq;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t0053exp""", """s00""")
    
    # t0053.1:
    stmt = """select sbinB_100, varcharB_4, varcharB_10, ubinB_4, sdecB_2
from t005tmp2 where sdecU_uniq > ?p1 and sdecU_uniq < ?p2
order by sdecU_uniq;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t0053exp""", """s01""")
    
    # t0053.2:
    stmt = """select sbinC_2, ubinC_4, sdecC_10, varcharC_2, varcharC_100
from t005tmp2 where sdecU_uniq > ?p1 and sdecU_uniq < ?p2
order by sdecU_uniq;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t0053exp""", """s02""")
    
    # t0053.3:
    stmt = """select sbinD_1000, udecD_2000, varcharD_1000, sdecD_500, ubinD_uniq
from t005tmp2 where sdecU_uniq > ?p1 and sdecU_uniq < ?p2
order by sdecU_uniq;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t0053exp""", """s03""")
    
    # t0053.4:
    stmt = """select varcharE_2, varcharE_4, varcharE_10, varcharE_1a, varcharE_2a
from t005tmp2 where sdecU_uniq > ?p1 and sdecU_uniq < ?p2
order by sdecU_uniq;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t0053exp""", """s04""")
    
    # t0053.5:
    stmt = """select sbinF_4, ubinF_20, udecF_20, varcharF_10, varcharF_100
from t005tmp2 where sdecU_uniq > ?p1 and sdecU_uniq < ?p2
order by sdecU_uniq;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t0053exp""", """s05""")
    
    # t0053.6:
    stmt = """select sbinG_uniq, sdecG_2000, udecG_500, varcharG_20, ubinG_2
from t005tmp2 where sdecU_uniq > ?p1 and sdecU_uniq < ?p2
order by sdecU_uniq;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t0053exp""", """s06""")
    
    # t0053.7:
    stmt = """select sbinH_2, sdecH_10, charH_uniq, udecH_20, ubinH_100
from t005tmp2 where sdecU_uniq > ?p1 and sdecU_uniq < ?p2
order by sdecU_uniq;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t0053exp""", """s07""")
    
    # t0053.8:
    stmt = """select sbinI_1000, varcharI_500, sdecI_2000, udecI_500, ubinI_2
from t005tmp2 where sdecU_uniq > ?p1 and sdecU_uniq < ?p2
order by sdecU_uniq;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t0053exp""", """s08""")
    
    # t0053.9:
    stmt = """select sbinJ_4, varcharJ_uniq, varcharJ_10, varcharJ_20, ubinJ_100
from t005tmp2 where sdecU_uniq > ?p1 and sdecU_uniq < ?p2
order by sdecU_uniq;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t0053exp""", """s09""")
    
    # t0053.10:
    stmt = """select sbinK_uniq, ubinK_1000, varcharK_20, udecK_2000, sdecK_500
from t005tmp2 where sdecU_uniq > ?p1 and sdecU_uniq < ?p2
order by sdecU_uniq;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t0053exp""", """s10""")
    
    # t0053.11:
    stmt = """select sbinL_2000, sdecL_20, udecL_20, ubinL_2, varcharL_4
from t005tmp2 where sdecU_uniq > ?p1 and sdecU_uniq < ?p2
order by sdecU_uniq;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t0053exp""", """s11""")
    
    # t0053.12:
    stmt = """select varcharM_1000, varcharM_100, varcharM_10, ubinM_10, udecM_1000
from t005tmp2 where sdecU_uniq > ?p1 and sdecU_uniq < ?p2
order by sdecU_uniq;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t0053exp""", """s12""")
    
    # t0053.13:
    stmt = """select sbinN_uniq, varcharN_100, sdecN_uniq, ubinN_10, udecN_500
from t005tmp2 where sdecU_uniq > ?p1 and sdecU_uniq < ?p2
order by sdecU_uniq;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t0053exp""", """s13""")
    
    # t0053.14:
    stmt = """select varcharO_100, varcharO_2, varcharO_20, varcharO_10, varcharO_2a
from t005tmp2 where sdecU_uniq > ?p1 and sdecU_uniq < ?p2
order by sdecU_uniq;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t0053exp""", """s14""")
    
    # t0053.15:
    stmt = """select sbinP_2, udecP_4, varcharP_uniq, ubinP_uniq, sdecP_10
from t005tmp2 where sdecU_uniq > ?p1 and sdecU_uniq < ?p2
order by sdecU_uniq;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t0053exp""", """s15""")
    
    # t0053.16:
    stmt = """select sbinQ_20, sdecQ_100, ubinQ_1000, udecQ_1000, varcharQ_uniq
from t005tmp2 where sdecU_uniq > ?p1 and sdecU_uniq < ?p2
order by sdecU_uniq;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t0053exp""", """s16""")
    
    # t0053.17:
    stmt = """select sbinR_uniq, sdecR_20, ubinR_2000, varcharR_100, udecR_100
from t005tmp2 where sdecU_uniq > ?p1 and sdecU_uniq < ?p2
order by sdecU_uniq;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t0053exp""", """s17""")
    
    # t0053.18:
    stmt = """select sbinS_uniq, varcharS_20, ubinS_20, sdecS_4, udecS_4
from t005tmp2 where sdecU_uniq > ?p1 and sdecU_uniq < ?p2
order by sdecU_uniq;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t0053exp""", """s18""")
    
    # t0053.19:
    stmt = """select sbinT_4, charT_2, ubinT_10, varcharT_100, varcharT_1000
from t005tmp2 where sdecU_uniq > ?p1 and sdecU_uniq < ?p2
order by sdecU_uniq;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t0053exp""", """s19""")
    
    # t0053.20:
    stmt = """select sbinU_2000, udecU_uniq, ubinU_1000, varcharU_10, sdecU_uniq
from t005tmp2 where sdecU_uniq > ?p1 and sdecU_uniq < ?p2
order by sdecU_uniq;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t0053exp""", """s20""")
    
    # t005.17:
    # #runscript $test_dir/t0056sql
    # script: t0056sql
    
    # 37 rows
    stmt = """prepare q01 from
select sdec20_uniq, varchar9_uniq,
max(varchar0_10) as max0,
min(varchar2_2)  as min2,
octet_length(varchar3_1000) as L3, count(*)
from t005t1
where
varchar14_100 < '25'
group by sdec20_uniq, varchar9_uniq, varchar3_1000
order by sdec20_uniq, varchar9_uniq
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' q01;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute q01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t0056exp""", """q01""")
    
    # 52 rows
    stmt = """prepare q02 from
select -- [first 1]
t1.sdec20_uniq,
p1.sdec20_uniq,
t1.varchar9_10,
p1.varchar9_10
from t005t1 t1, t005tmp1 p1
where t1.varchar2_2 = p1.varchar2_2
and t1.varchar14_2a like 'A%'
and t1.varchar14_20 =
(select max(varcharO_20) from t005tmp2)
and t1.varchar9_10 = p1.varchar9_10
order by t1.sdec20_uniq
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' q02;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute q02;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t0056exp""", """q02""")
    
    # 26 rows
    stmt = """prepare q03 from
select sdec20_uniq, sdecU_uniq, varchar9_uniq, varcharJ_uniq
from t005t1, t005tmp2
where varchar9_10 = varcharJ_10
and varcharA_10 like '%AA'
and varcharP_uniq = varcharQ_uniq
and varchar14_20 = (select max(varchar14_20) from t005tmp1)
and varchar2_2 between 'AA' and 'ZZ'
and sdec20_uniq < 2000
order by sdec20_uniq;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' q03;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute q03;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t0056exp""", """q03""")
    
    # 24 rows
    stmt = """prepare q04 from
select varchar9_uniq, count(*)
from t005t1, t005tmp2
where varchar14_100 >= '10'
and varchar14_100 < '20'
and exists (
select * from t005tmp1
where varchar9_uniq = varcharJ_uniq
and varchar14_2 between '0' and '9'
)
group by varchar9_uniq
order by varchar9_uniq
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' q04;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute q04;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t0056exp""", """q04""")
    
    # 10 rows
    stmt = """prepare q05 from
select sdecA_uniq, max(sdecU_uniq) as L_max
from t005t1 t1, t005tmp1 p1, t005tmp2
where t1.varchar0_4 = p1.varchar0_4
and t1.varchar2_2 = varcharC_2
and p1.varchar4_2 = varcharE_2
and varcharG_20 = 'AAAAAAAA'
and t1.varchar9_20 < '10'
and p1.varchar9_20 > '20'
group by sdecA_uniq
order by L_max
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' q05;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute q05;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t0056exp""", """q05""")
    
    stmt = """prepare q08 from
select ubin3,
max(case when sdec20 > 22300
then compress
else '00000000' end) as c2
from (
select cast(ubin3_uniq as varchar(8)) as ubin3,
substring(varchar8_500,1,8) as compress,
sdec20_uniq as sdec20
from t005t1, t005tmp2
where sdecA_uniq = sdec0_uniq
and ubinD_uniq = ubin15_uniq
and varcharP_uniq = varchar15_uniq
and varcharQ_uniq = varchar16_uniq
and varcharJ_uniq = varchar9_uniq
and varchar14_10 between '0' and '9'
and varchar20_10 like '%McKinley%'
) as temp
group by ubin3
order by ubin3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' q08;"""
    output = _dci.cmdexec(stmt)
    
    # 1 row selected: 4961, FHAAFAAM
    stmt = """execute q08;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t0056exp""", """q08""")
    
    # t005.20: update some rows
    # t0054sql & t0055sql are called by t005update
    # #runscript $test_dir/t005update
    # script: t005update
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """update t005t1 set
varchar14_100 = substring(varchar5_10,1,3),
varchar14_2   = substring(varchar5_100,2,3),
varchar14_20  = substring(varchar6_20,3,3),
varchar14_10  = varchar11_4,
varchar14_2a  = varchar12_10
where varchar2_2 in ('AA','AE','AG','AL')
and varchar9_uniq like '%AAAA%'
and varchar15_uniq = varchar16_uniq;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 10)
    
    stmt = """select sbin20_2000, udec20_uniq, ubin20_1000, varchar20_10, sdec20_uniq
from t005t1
where varchar2_2 in ('AA','AE','AG','AL')
and varchar9_uniq like '%AAAA%'
and varchar15_uniq = varchar16_uniq order by sdec20_uniq;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t005updexp""", """s01""")
    
    stmt = """select sbin13_uniq, varchar13_100, sdec13_uniq, ubin13_10, udec13_500
from t005t1
where varchar2_2 in ('AA','AE','AG','AL')
and varchar9_uniq like '%AAAA%'
and varchar15_uniq = varchar16_uniq order by sdec20_uniq;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t005updexp""", """s02""")
    
    stmt = """select varchar14_100, varchar14_2, varchar14_20, varchar14_10, varchar14_2a
from t005t1
where varchar2_2 in ('AA','AE','AG','AL')
and varchar9_uniq like '%AAAA%'
and varchar15_uniq = varchar16_uniq order by sdec20_uniq;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t005updexp""", """s03""")
    
    stmt = """select sbin15_2, udec15_4, varchar15_uniq, ubin15_uniq, sdec15_10
from t005t1
where varchar2_2 in ('AA','AE','AG','AL')
and varchar9_uniq like '%AAAA%'
and varchar15_uniq = varchar16_uniq order by sdec20_uniq;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t005updexp""", """s04""")
    
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """set param ?p1 'BIAAFAAA';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p2 'BIAA';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p3 'FAAA';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p4 'BI';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p5 'AA';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """set param ?p6 'Mount McKinley or Denali in Alaska is the highest mountain peak in North America, at a height of approximately 20,320 feet (6,194 m). It is the centerpiece of Denali National Park. The mountain is also known as Bolshaya Gora, meaning Big Mountain, in Russian.';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p7 0;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p8 'zz';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p9 'ZZZZZZZZ';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p10 '1234567890';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """update t005t1 set
sbin0_500      = ?p7,
varchar0_10    = upper(cast(?p8 as varchar(2))),
udec0_2000     = 0,
ubin0_1000     = ?p7,
sdec0_uniq     = cast(?p10 as varchar(10)),
varchar0_4     = cast(?p8 as varchar(2)),
sbin1_100      = 1,
varchar1_4     = 'ZZ',
varchar1_10    = cast(?p10 as varchar(10)),
ubin1_4        = 1,
sdec1_2        = 1,
sbin2_2        = 2,
ubin2_4        = 2,
sdec2_10       = 2,
varchar2_100   = 'zz',
sbin3_1000     = 333,
udec3_2000     = 333,
varchar3_1000  = substring(cast(?p6 as varchar(259)),1,200),
sdec3_500      = 333,
ubin3_uniq     = 333,
varchar4_1a    = 'ZZ',
varchar4_2a    = 'zz',
sbin5_4        = 5,
ubin5_20       = 5,
udec5_20       = 5,
varchar5_10    = concat(cast(?p8 as varchar(2)),upper(cast(?p8 as varchar(2)))),
varchar5_100   = substring(cast(?p6 as varchar(259)),1,18),
sbin6_uniq     = 6,
sdec6_2000     = 6,
udec6_500      = 6,
varchar6_20    = cast(?p5 as varchar(2)) || cast(?p8 as varchar(2)),
ubin6_2        = 6,
sbin7_2        = 7,
sdec7_10       = 0.7,
char7_uniq     = substring(cast(?p6 as varchar(259)),1,100),
udec7_20       = 7,
ubin7_100      = 7,
sbin8_1000     = 8,
varchar8_500   = substring(cast(?p6 as varchar(259)),1,100),
sdec8_2000     = 8.0,
udec8_500      = 8.0,
ubin8_2        = 0.8,
sbin9_4        = .9,
varchar9_20    = cast(?p8 as varchar(2)),
ubin9_100      = 9.9,
sbin10_uniq    = 10,
ubin10_1000    = 10,
varchar10_20   = 'zz',
udec10_2000    = 10,
sdec10_500     = 10,
sbin11_2000    = 11,
sdec11_20      = .11,
udec11_20      = .11,
ubin11_2       = 11,
varchar11_4    = 'ZZ',
varchar12_1000 = cast(?p9 as varchar(8)),
varchar12_100  = cast(?p9 as varchar(8)),
varchar12_10   = substring(cast(?p9 as varchar(8)),3,2),
ubin12_10      = 12,
udec12_1000    = 12,
sbin13_uniq    = .13,
sdec13_uniq    = 13,
ubin13_10      = .13,
udec13_500     = 13,
varchar14_100  = '0z5',
varchar14_2    = '1z6',
varchar14_20   = '2z7',
varchar14_10   = '3z8',
varchar14_2a   = '4z9',
sbin15_2       = 15,
udec15_4       = .15,
ubin15_uniq    = 15,
sdec15_10      = .15,
sbin16_20      = .16,
sdec16_100     = .16,
ubin16_1000    = 1.6,
udec16_1000    = 1.6,
sbin17_uniq    = 17,
sdec17_20      = 17,
ubin17_2000    = 17,
varchar17_100  = substring(cast(?p6 as varchar(259)),1,100),
udec17_100     = 17,
sbin18_uniq    = 18,
varchar18_20   = substring(cast(?p6 as varchar(259)),1,100),
ubin18_20      = 18,
sdec18_4       = 18,
udec18_4       = 18,
sbin19_4       = 19,
char19_2       = cast(?p8 as varchar(2)),
ubin19_10      = 19,
varchar19_1000 = cast(?p8 as varchar(2)),
sbin20_2000    = 20.00,
udec20_uniq    = 20,
ubin20_1000    = 2.0,
varchar20_10   = substring(cast(?p6 as varchar(259)),1,300)
where sdec20_uniq = 60
and varchar2_2  = varchar4_10  -- 'AA'
and varchar4_2  = varchar4_4   -- '0.0'
and varchar9_uniq  = ?p1       -- 'BIAAFAAA'
and varchar9_10    = '8'
and varchar13_100  = 'AP'
and varchar15_uniq = concat(?p2,?p3)   -- 'BIAAFAAA'
and varchar16_uniq = ?p4 || ?p5 || ?p3 -- 'BIAAFAAA'
and varchar19_100  = '9.4'
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output)
    
    # #runscript $test_dir/t0054sql
    # script: t0054sql
    
    stmt = """set param ?p1 60;"""
    output = _dci.cmdexec(stmt)
    
    # t0054.0:
    stmt = """select sbin0_500, varchar0_10, udec0_2000, ubin0_1000, sdec0_uniq, varchar0_4
from t005t1 where sdec20_uniq = ?p1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t0054exp""", """s00""")
    
    # t0054.1:
    stmt = """select sbin1_100, varchar1_4, varchar1_10, ubin1_4, sdec1_2
from t005t1 where sdec20_uniq = ?p1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t0054exp""", """s01""")
    
    # t0054.2:
    stmt = """select sbin2_2, ubin2_4, sdec2_10, varchar2_2, varchar2_100
from t005t1 where sdec20_uniq = ?p1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t0054exp""", """s02""")
    
    # t0054.3:
    stmt = """select sbin3_1000, udec3_2000,
substring(varchar3_1000,1,300) as varchar3_1000, sdec3_500, ubin3_uniq
from t005t1 where sdec20_uniq = ?p1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t0054exp""", """s03""")
    
    # t0054.4:
    stmt = """select varchar4_2, varchar4_4, varchar4_10, varchar4_1a, varchar4_2a
from t005t1 where sdec20_uniq = ?p1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t0054exp""", """s04""")
    
    # t0054.5:
    stmt = """select sbin5_4, ubin5_20, udec5_20,
substring(varchar5_10,1,8) as varchar5_10, varchar5_100
from t005t1 where sdec20_uniq = ?p1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t0054exp""", """s05""")
    
    # t0054.6:
    stmt = """select sbin6_uniq, sdec6_2000, udec6_500,
substring(varchar6_20,1,8) as varchar6_20, ubin6_2
from t005t1 where sdec20_uniq = ?p1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t0054exp""", """s06""")
    
    # t0054.7:
    stmt = """select sbin7_2, sdec7_10, char7_uniq, udec7_20, ubin7_100
from t005t1 where sdec20_uniq = ?p1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t0054exp""", """s07""")
    
    # t0054.8:
    stmt = """select sbin8_1000, varchar8_500, sdec8_2000, udec8_500, ubin8_2
from t005t1 where sdec20_uniq = ?p1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t0054exp""", """s08""")
    
    # t0054.9:
    stmt = """select sbin9_4, varchar9_uniq, varchar9_10, varchar9_20, ubin9_100
from t005t1 where sdec20_uniq = ?p1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t0054exp""", """s09""")
    
    # t0054.10:
    stmt = """select sbin10_uniq, ubin10_1000, varchar10_20, udec10_2000, sdec10_500
from t005t1 where sdec20_uniq = ?p1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t0054exp""", """s10""")
    
    # t0054.11:
    stmt = """select sbin11_2000, sdec11_20, udec11_20, ubin11_2, varchar11_4
from t005t1 where sdec20_uniq = ?p1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t0054exp""", """s11""")
    
    # t0054.12:
    stmt = """select varchar12_1000, varchar12_100, varchar12_10, ubin12_10, udec12_1000
from t005t1 where sdec20_uniq = ?p1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t0054exp""", """s12""")
    
    # t0054.13:
    stmt = """select sbin13_uniq, varchar13_100, sdec13_uniq, ubin13_10, udec13_500
from t005t1 where sdec20_uniq = ?p1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t0054exp""", """s13""")
    
    # t0054.14:
    stmt = """select varchar14_100, varchar14_2, varchar14_20, varchar14_10, varchar14_2a
from t005t1 where sdec20_uniq = ?p1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t0054exp""", """s14""")
    
    # t0054.15:
    stmt = """select sbin15_2, udec15_4, varchar15_uniq, ubin15_uniq, sdec15_10
from t005t1 where sdec20_uniq = ?p1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t0054exp""", """s15""")
    
    # t0054.16:
    stmt = """select sbin16_20, sdec16_100, ubin16_1000, udec16_1000, varchar16_uniq
from t005t1 where sdec20_uniq = ?p1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t0054exp""", """s16""")
    
    # t0054.17:
    stmt = """select sbin17_uniq, sdec17_20, ubin17_2000,
substring(varchar17_100,1,100) as varchar17_100, udec17_100
from t005t1 where sdec20_uniq = ?p1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t0054exp""", """s17""")
    
    # t0054.18:
    stmt = """select sbin18_uniq, substring(varchar18_20,1,100) as varchar18_20,
ubin18_20, sdec18_4, udec18_4
from t005t1 where sdec20_uniq = ?p1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t0054exp""", """s18""")
    
    # t0054.19:
    stmt = """select sbin19_4, char19_2, ubin19_10, varchar19_100, varchar19_1000
from t005t1 where sdec20_uniq = ?p1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t0054exp""", """s19""")
    
    # t0054.20:
    stmt = """select sbin20_2000, udec20_uniq, ubin20_1000, varchar20_10, sdec20_uniq
from t005t1 where sdec20_uniq = ?p1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t0054exp""", """s20""")
    
    # #runscript $test_dir/t0055sql
    # script: t0055sql
    
    stmt = """select sdec20_uniq, varchar2_2, varchar9_uniq from t005t1
where sbin0_500      = ?p7
and varchar0_10    = upper(cast(?p8 as varchar(2)))
and udec0_2000     = 0
and ubin0_1000     = ?p7
and sdec0_uniq     = cast(?p10 as varchar(10))
and varchar0_4     = cast(?p8 as varchar(2))
and sbin1_100      = 1
and varchar1_4     = 'ZZ'
and varchar1_10    = cast(?p10 as varchar(10))
and ubin1_4        = 1
and sdec1_2        = 1
and sbin2_2        = 2
and ubin2_4        = 2
and sdec2_10       = 2
and varchar2_100   = 'zz'
and sbin3_1000     = 333
and udec3_2000     = 333
and varchar3_1000  = substring(cast(?p6 as varchar(259)),1,200)
and sdec3_500      = 333
and ubin3_uniq     = 333
and varchar4_1a    = 'ZZ'
and varchar4_2a    = 'zz'
and sbin5_4        = 5
and ubin5_20       = 5
and udec5_20       = 5
and varchar5_10    = concat(cast(?p8 as varchar(2)),upper(cast(?p8 as varchar(2))))
and varchar5_100   = substring(cast(?p6 as varchar(259)),1,18)
and sbin6_uniq     = 6
and sdec6_2000     = 6
and udec6_500      = 6
and varchar6_20    = ?p5 || cast(?p8 as varchar(2))
and ubin6_2        = 6
and sbin7_2        = 7
and sdec7_10       = 0.7
and char7_uniq     = substring(cast(?p6 as varchar(259)),1,100)
and udec7_20       = 7
and ubin7_100      = 7
and sbin8_1000     = 8
and varchar8_500   = substring(cast(?p6 as varchar(259)),1,100)
and sdec8_2000     = 8.0
and udec8_500      = 8.0
and ubin8_2        = 0.8
and sbin9_4        = .9
and varchar9_20    = cast(?p8 as varchar(2))
and ubin9_100      = 9.9
and sbin10_uniq    = 10
and ubin10_1000    = 10
and varchar10_20   = 'zz'
and udec10_2000    = 10
and sdec10_500     = 10
and sbin11_2000    = 11
and sdec11_20      = .11
and udec11_20      = .11
and ubin11_2       = 11
and varchar11_4    = 'ZZ'
and varchar12_1000 = cast(?p9 as varchar(8))
and varchar12_100  = cast(?p9 as varchar(8))
and varchar12_10   = substring(cast(?p9 as varchar(8)),3,2)
and ubin12_10      = 12
and udec12_1000    = 12
and sbin13_uniq    = .13
and sdec13_uniq    = 13
and ubin13_10      = .13
and udec13_500     = 13
and varchar14_100  = '0z5'
and varchar14_2    = '1z6'
and varchar14_20   = '2z7'
and varchar14_10   = '3z8'
and varchar14_2a   = '4z9'
and sbin15_2       = 15
and udec15_4       = .15
and ubin15_uniq    = 15
and sdec15_10      = .15
and sbin16_20      = .16
and sdec16_100     = .16
and ubin16_1000    = 1.6
and udec16_1000    = 1.6
and sbin17_uniq    = 17
and sdec17_20      = 17
and ubin17_2000    = 17
and varchar17_100  = substring(cast(?p6 as varchar(259)),1,100)
and udec17_100     = 17
and sbin18_uniq    = 18
and varchar18_20   = substring(cast(?p6 as varchar(259)),1,100)
and ubin18_20      = 18
and sdec18_4       = 18
and udec18_4       = 18
and sbin19_4       = 19
and char19_2       = cast(?p8 as varchar(2))
and ubin19_10      = 19
and varchar19_1000 = cast(?p8 as varchar(2))
and sbin20_2000    = 20.00
and udec20_uniq    = 20
and ubin20_1000    = 2.0
and varchar20_10   = substring(cast(?p6 as varchar(259)),1,300)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t0055exp""", """s01""")
    
    # t005.21:
    # #runscript $test_dir/t005delete
    # script: t005delete
    
    stmt = """set param ?p1 'BIAAFAAA';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p2 'BIAA';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p3 'FAAA';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p4 'BI';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p5 'AA';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """set param ?p6 'Mount McKinley or Denali in Alaska is the highest mountain peak in North America, at a height of approximately 20,320 feet (6,194 m). It is the centerpiece of Denali National Park. The mountain is also known as Bolshaya Gora, meaning Big Mountain, in Russian.';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p7 0;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p8 'zz';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p9 'ZZZZZZZZ';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p10 '1234567890';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """delete from t005t1
where sbin0_500      = ?p7
and varchar0_10    = upper(cast(?p8 as varchar(2)))
and udec0_2000     = 0
and ubin0_1000     = ?p7
and sdec0_uniq     = cast(?p10 as varchar(10))
and varchar0_4     = cast(?p8 as varchar(2))
and sbin1_100      = 1
and varchar1_4     = 'ZZ'
and varchar1_10    = cast(?p10 as varchar(10))
and ubin1_4        = 1
and sdec1_2        = 1
and sbin2_2        = 2
and ubin2_4        = 2
and sdec2_10       = 2
and varchar2_100   = 'zz'
and sbin3_1000     = 333
and udec3_2000     = 333
and varchar3_1000  = substring(cast(?p6 as varchar(259)),1,200)
and sdec3_500      = 333
and ubin3_uniq     = 333
and varchar4_1a    = 'ZZ'
and varchar4_2a    = 'zz'
and sbin5_4        = 5
and ubin5_20       = 5
and udec5_20       = 5
and varchar5_10    = concat(cast(?p8 as varchar(2)),upper(cast(?p8 as varchar(2))))
and varchar5_100   = substring(cast(?p6 as varchar(259)),1,18)
and sbin6_uniq     = 6
and sdec6_2000     = 6
and udec6_500      = 6
and varchar6_20    = ?p5 || cast(?p8 as varchar(2))
and ubin6_2        = 6
and sbin7_2        = 7
and sdec7_10       = 0.7
and char7_uniq     = substring(cast(?p6 as varchar(259)),1,100)
and udec7_20       = 7
and ubin7_100      = 7
and sbin8_1000     = 8
and varchar8_500   = substring(cast(?p6 as varchar(259)),1,100)
and sdec8_2000     = 8.0
and udec8_500      = 8.0
and ubin8_2        = 0.8
and sbin9_4        = .9
and varchar9_20    = cast(?p8 as varchar(2))
and ubin9_100      = 9.9
and sbin10_uniq    = 10
and ubin10_1000    = 10
and varchar10_20   = 'zz'
and udec10_2000    = 10
and sdec10_500     = 10
and sbin11_2000    = 11
and sdec11_20      = .11
and udec11_20      = .11
and ubin11_2       = 11
and varchar11_4    = 'ZZ'
and varchar12_1000 = cast(?p9 as varchar(8))
and varchar12_100  = cast(?p9 as varchar(8))
and varchar12_10   = substring(cast(?p9 as varchar(8)),3,2)
and ubin12_10      = 12
and udec12_1000    = 12
and sbin13_uniq    = .13
and sdec13_uniq    = 13
and ubin13_10      = .13
and udec13_500     = 13
and varchar14_100  = '0z5'
and varchar14_2    = '1z6'
and varchar14_20   = '2z7'
and varchar14_10   = '3z8'
and varchar14_2a   = '4z9'
and sbin15_2       = 15
and udec15_4       = .15
and ubin15_uniq    = 15
and sdec15_10      = .15
and sbin16_20      = .16
and sdec16_100     = .16
and ubin16_1000    = 1.6
and udec16_1000    = 1.6
and sbin17_uniq    = 17
and sdec17_20      = 17
and ubin17_2000    = 17
and varchar17_100  = substring(cast(?p6 as varchar(259)),1,100)
and udec17_100     = 17
and sbin18_uniq    = 18
and varchar18_20   = substring(cast(?p6 as varchar(259)),1,100)
and ubin18_20      = 18
and sdec18_4       = 18
and udec18_4       = 18
and sbin19_4       = 19
and char19_2       = cast(?p8 as varchar(2))
and ubin19_10      = 19
and varchar19_1000 = cast(?p8 as varchar(2))
and sbin20_2000    = 20.00
and udec20_uniq    = 20
and ubin20_1000    = 2.0
and varchar20_10   = substring(cast(?p6 as varchar(259)),1,300)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output)
    
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # 27 rows
    stmt = """delete from t005tmp2
where substring(varcharD_1000,5,8) =
(select min(case when sdec20_uniq < 100
then 'ZZZZZZZZ'
else substring(varchar8_500,1,8) end) as c2
from t005t1);"""
    output = _dci.cmdexec(stmt)
    
    # 14 rows
    stmt = """delete from t005t1
where varchar0_4 = substring(varchar3_1000,5,8)
and (varchar1_4 = substring(varchar0_4,7,2)
or varchar1_4 = substring(varchar0_4,1,2)
or substring(varchar0_4,1,4) = concat(varchar1_4,'AA'))
and varchar2_100 < '99'
and varchar14_10 between '0' and '9'
and varchar14_2a between 'AA' and 'ZZ'
and sbin6_uniq = sbin10_uniq;"""
    output = _dci.cmdexec(stmt)
    
    # 70 rows
    stmt = """delete from t005t1
where varchar9_uniq = varchar15_uniq
and concat(varchar9_uniq,varchar2_2) =
varchar16_uniq || varchar2_2
and varchar2_2 in ('AA', 'BA')
and varchar4_2 = varchar4_4
and varchar4_10 like '%AA'
and varchar9_10 between '0' and '9'
and varchar13_100 in (select distinct(varchar13_100) from t005tmp1)
and varchar19_100 like '%.%'
and sdec20_uniq < 25000
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """set param ?p1 'BIAAFAAA';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p2 'BIAA';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p3 'FAAA';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p4 'BI';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p5 'AA';"""
    output = _dci.cmdexec(stmt)
    
    # 1 rows
    stmt = """delete from t005tmp2
where sdecU_uniq = 60
and varcharC_2  = varcharE_10  -- 'AA'
and varcharE_2  = varcharE_4   -- '0.0'
and varcharJ_uniq  = ?p1       -- 'BIAAFAAA'
and varcharJ_10    = '8'
and varcharN_100  = 'AP'
and varcharP_uniq = concat(?p2,?p3)   -- 'BIAAFAAA'
and varcharQ_uniq = ?p4 || ?p5 || ?p3 -- 'BIAAFAAA'
and varcharT_100  = '9.4'
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select count(*) from t005t1;"""
    output = _dci.cmdexec(stmt)
    stmt = """select count(*) from t005tmp2;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """control query default MDAM_SCAN_METHOD 'ON';"""
    output = _dci.cmdexec(stmt)
    stmt = """control table * MDAM 'ON';"""
    output = _dci.cmdexec(stmt)
    
    # t005.23:
    # #runscript $test_dir/t0057sql
    # script: t0057sql
    # t0057.1: 37 rows
    stmt = """prepare q01 from
select sdec20_uniq, varchar9_uniq,
max(varchar0_10) as max0,
min(varchar2_2)  as min2,
octet_length(varchar3_1000) as L3, count(*)
from t005t1
where
varchar14_100 < '25'
group by sdec20_uniq, varchar9_uniq, varchar3_1000
order by sdec20_uniq, varchar9_uniq
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' q01;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute q01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t0057exp""", """q01""")
    
    # t0057.2: 0 rows
    stmt = """prepare q02 from
select -- [first 1]
t1.sdec20_uniq,
p1.sdec20_uniq,
t1.varchar9_10,
p1.varchar9_10
from t005t1 t1, t005tmp1 p1
where t1.varchar2_2 = p1.varchar2_2
and t1.varchar14_2a like 'A%'
and t1.varchar14_20 =
(select max(varcharO_20) from t005tmp2)
and t1.varchar9_10 = p1.varchar9_10
order by t1.sdec20_uniq
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' q02;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute q02;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t0057exp""", """q02""")
    
    # t0057.3: 26 rows
    stmt = """prepare q03 from
select sdec20_uniq, sdecU_uniq, varchar9_uniq, varcharJ_uniq
from t005t1, t005tmp2
where varchar9_10 = varcharJ_10
and varcharA_10 like '%AA'
and varcharP_uniq = varcharQ_uniq
and varchar14_20 = (select max(varchar14_20) from t005tmp1)
and varchar2_2 between 'AA' and 'ZZ'
and sdec20_uniq < 2000
order by sdec20_uniq;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' q03;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute q03;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    # t0057.4: 24 rows
    stmt = """prepare q04 from
select varchar9_uniq, count(*)
from t005t1, t005tmp2
where varchar14_100 >= '10'
and varchar14_100 < '20'
and exists (
select * from t005tmp1
where varchar9_uniq = varcharJ_uniq
and varchar14_2 between '0' and '9'
)
group by varchar9_uniq
order by varchar9_uniq
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' q04;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute q04;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t0057exp""", """q04""")
    
    # t0057.5: 10 rows
    stmt = """prepare q05 from
select sdecA_uniq, max(sdecU_uniq) as L_max
from t005t1 t1, t005tmp1 p1, t005tmp2
where t1.varchar0_4 = p1.varchar0_4
and t1.varchar2_2 = varcharC_2
and p1.varchar4_2 = varcharE_2
and varcharG_20 = 'AAAAAAAA'
and t1.varchar9_20 < '10'
and p1.varchar9_20 > '20'
group by sdecA_uniq
order by L_max
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' q05;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute q05;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t0057exp""", """q05""")
    
    stmt = """prepare q08 from
select ubin3,
max(case when sdec20 > 22300
then compress
else '00000000' end) as c2
from (
select cast(ubin3_uniq as varchar(8)) as ubin3,
substring(varchar8_500,1,8) as compress,
sdec20_uniq as sdec20
from t005t1, t005tmp2
where sdecA_uniq = sdec0_uniq
and ubinD_uniq = ubin15_uniq
and varcharP_uniq = varchar15_uniq
and varcharQ_uniq = varchar16_uniq
and varcharJ_uniq = varchar9_uniq
and varchar14_10 between '0' and '9'
and varchar20_10 like '%McKinley%'
) as temp
group by ubin3
order by ubin3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' q08;"""
    output = _dci.cmdexec(stmt)
    
    # t0057.8: 1 row selected - 4961, FHAAFAAM
    stmt = """execute q08;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t0057exp""", """q08""")
    
    stmt = """control query default MDAM_SCAN_METHOD reset;"""
    output = _dci.cmdexec(stmt)
    stmt = """control table * MDAM reset;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

