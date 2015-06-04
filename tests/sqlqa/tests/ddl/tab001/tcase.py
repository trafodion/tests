# @@@ START COPYRIGHT @@@
#
# (C) Copyright 2014-2015 Hewlett-Packard Development Company, L.P.
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

#testunit TAB001
# create R2 table, headings, file options and attributes

def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci
    
    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()
    
def test001(desc="""table naming conventions"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    stmt = """set schema """ + defs.testcat + """.""" + defs.testsch2 + """;"""
    output = _dci.cmdexec(stmt)
    stmt = """create table """ + defs.testcat + """.""" + defs.testsch2 + """.a1t1c (col1 int, col2 int) no partition location """ + gvars.g_disc1 + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index a1i1index on """ + defs.testcat + """.""" + defs.testsch2 + """.a1t1c (col2 desc);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create view """ + defs.testcat + """.""" + defs.testsch2 + """.a1v1 as select col1 from """ + defs.testcat + """.""" + defs.testsch2 + """.a1t1c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """set schema """ + defs.testcat + """.""" + defs.testsch1 + """;"""
    output = _dci.cmdexec(stmt)
    stmt = """create table A1t2 (c1 int, c2 int, c3 date) no partition location """ + gvars.g_disc2 + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index A1i2 on A1t2 (c2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create view """ + defs.testcat + """.""" + defs.testsch1 + """.a1v2 as select c3 from """ + defs.testcat + """.""" + defs.testsch1 + """.a1t2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """set schema """ + defs.testcat + """.""" + defs.testsch2 + """;"""
    output = _dci.cmdexec(stmt)
    
    #A001.1 Create TABLE with name same as index in same schema
    stmt = """create table a1i1 (a int, b int) no partition location """ + gvars.g_disc3 + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #A001.2 Create TABLE with name same as table in other schema
    stmt = """create table """ + defs.testcat + """.""" + defs.testsch2 + """.a1t2 (a int, b int) no partition location """ + gvars.g_disc3 + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #A001.3 Create TABLE with name same as index in other schema
    stmt = """create table """ + defs.testcat + """.""" + defs.testsch2 + """.a1i2 (a int, b int) no partition location """ + gvars.g_disc3 + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #A001.4 Create TABLE with name same as view in other schema
    stmt = """create table """ + defs.testcat + """.""" + defs.testsch2 + """.a1v2 (a int, b int) no partition location """ + gvars.g_disc3 + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #A001.5 Create TABLE with SQL delimited name
    stmt = """create table """ + defs.testcat + """.""" + defs.testsch2 + """.\"1-%4&6'8(N)1+3*56:8;*1<3B4>6=8? 1[23]45_6,7|8.9+12\" (a int, b int) no partition location """ + gvars.g_disc3 + """;"""
    output = _dci.cmdexec(stmt)
    if hpdci.tgtSQ():
        _dci.expect_complete_msg(output)
    elif hpdci.tgtTR():
        _dci.expect_error_msg(output)
 
    #A001.6 Create TABLE with default catalog and schema and reserved word
    #       as SQL delimited identifier
    stmt = """create table \"create\" (a int, b int) no partition location """ + gvars.g_disc3 + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #A001.7 Create TABLE with default catalog and explicit schema
    stmt = """create table """ + defs.testsch2 + """.\"a1t2\" (a int, b int) no partition location """ + gvars.g_disc3 + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #A001.8 (doesn't drop)
    stmt = """create table
B123456789B123456789C123456789D123456789E123456789F123456789G123456789H123456789I123456789J123456789K123456789L123456789M1234567
(a int, b int) no partition location """ + gvars.g_disc3 + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    # cleanup
    stmt = """drop table """ + defs.testcat + """.""" + defs.testsch2 + """.a1i1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table """ + defs.testcat + """.""" + defs.testsch2 + """.a1t2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table """ + defs.testcat + """.""" + defs.testsch2 + """.a1i2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table """ + defs.testcat + """.""" + defs.testsch2 + """.a1v2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table """ + defs.testcat + """.""" + defs.testsch2 + """.\"1-%4&6'8(N)1+3*56:8;*1<3B4>6=8? 1[23]45_6,7|8.9+12\";"""
    output = _dci.cmdexec(stmt)
    if hpdci.tgtSQ():
        _dci.expect_complete_msg(output)
    elif hpdci.tgtTR():
        _dci.expect_error_msg(output)
    stmt = """drop table """ + defs.testcat + """.""" + defs.testsch2 + """.\"create\";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table """ + defs.testcat + """.""" + defs.testsch2 + """.\"a1t2\";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view """ + defs.testcat + """.""" + defs.testsch2 + """.a1v1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table """ + defs.testcat + """.""" + defs.testsch2 + """.a1t1c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop table
B123456789B123456789C123456789D123456789E123456789F123456789G123456789H123456789I123456789J123456789K123456789L123456789M1234567;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view """ + defs.testcat + """.""" + defs.testsch1 + """.a1v2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table """ + defs.testcat + """.""" + defs.testsch1 + """.a1t2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test002(desc="""TABLE file options"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # partition
    
    # A002.1 Store by Primary key
    stmt = """create table """ + defs.testcat + """.""" + defs.testsch1 + """.a2t1
(int1_y4        interval year(4),
date1_ytod    date not null not droppable,
time1_htom	 time,
primary key (date1_ytod desc) not droppable)
store by primary key
location """ + gvars.g_disc3 + """
range partition(add first key date '2002-03-14' location """ + gvars.g_disc4 + """,
add first key date '2002-02-03' location """ + gvars.g_disc5 + """)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into """ + defs.testcat + """.""" + defs.testsch1 + """.a2t1
values (interval '1999' year(4), date '2002-04-14', time '16:08:08');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into """ + defs.testcat + """.""" + defs.testsch1 + """.a2t1
values (interval '1888' year(4), date '2002-03-13', time '18:08:08');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into """ + defs.testcat + """.""" + defs.testsch1 + """.a2t1
values (interval '1777' year(4), date '2002-02-02', time '13:08:08');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select [first 3] * from """ + defs.testcat + """.""" + defs.testsch1 + """.a2t1 order by 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001.exp""", """A2s1a""")
    
    # A002.2 Store by clustering key
    stmt = """create table """ + defs.testcat + """.""" + defs.testsch1 + """.a2t2
(  real3_n1000         Real,
int3_yTOm_4         Interval year(1) to month,
date3_n2000         Date not null not droppable,
udec3_n100          Decimal(9) unsigned,
ubin3_n2000         Numeric(4) unsigned ,
char3_4             Character(8) not null not droppable,
primary key (char3_4) droppable) """
    if hpdci.tgtSQ():
        stmt = stmt + """location """ + gvars.g_disc1 + """
store by (date3_n2000 desc, char3_4)
range partition (add first key date '2002-04-05' location """ + gvars.g_disc2 + """,
add first key date '2003-04-05' location """ + gvars.g_disc3 + """)
;"""
    elif hpdci.tgtTR():
        stmt += """;""" 
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into """ + defs.testcat + """.""" + defs.testsch1 + """.a2t2 values
( 1.0019999E+002,interval '0-00' year(1) to month,date '2103-11-22',20,1420,  'AAAAAAAA'),
( 1.0127000E+000,interval '0-03' year(1) to month,date '2103-02-02',27,1127,  'DAAAAAAA'),
( 1.0020000E+000,interval '0-00' year(1) to month,date '2102-10-18',20,1020,  'AAAAAAAB'),
( 1.0166999E+004,interval '0-03' year(1) to month,date '2102-08-26',67, 967,  'DAAAAAAB'),
( 1.0059999E+004,interval '0-00' year(1) to month,date '2102-05-11',60, 860,  'AAAAAAAC'),
( 1.0167000E+000,interval '0-03' year(1) to month,date '2103-03-14',67,1167,  'DAAAAAAC'),
( 1.0000000E+002,interval '0-00' year(1) to month,date '2103-11-02', 0,1400,  'AAAAAAAD'),
( 1.0126999E+003,interval '0-03' year(1) to month,date '2104-09-24',27,1727,  'DAAAAAAD'),
( 1.0159999E+003,interval '0-00' year(1) to month,date '2102-01-31',60, 760,  'AAAAAAAE'),
( 1.0167000E+000,interval '0-03' year(1) to month,date '2100-06-17',67, 167,  'DAAAAAAE');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """select [first 10] * from """ + defs.testcat + """.""" + defs.testsch1 + """.a2t2 order by 6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001.exp""", """A2s2a""")
    
    # A002.3 Create table with droppable PK
    stmt = """create table """ + defs.testcat + """.""" + defs.testsch1 + """.a2t3(
sdec4_n20           Decimal(4) no default,
int4_yTOm_uniq      Interval year(5) to month not null not droppable primary key droppable,
sbin4_n1000         Smallint,
time4_1000          Time) no partition
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # A002.4 Create table with default droppable 255-byte PK
    # takes on value of PRIMARY_KEY_CONSTRAINT_DROPPABLE_OPTION default
    
    stmt = """showcontrol default PRIMARY_KEY,match partial;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """OFF""")
    
    stmt = """create table """ + defs.testcat + """.""" + defs.testsch1 + """.a2t4 (
"varchar1_1"  varchar(55) not null,
varchar1_2  varchar(100) not null,
varchar1_3  varchar(100) not null,
int1        int,
primary key ("varchar1_1",varchar1_2 desc, varchar1_3)) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """control query default  PRIMARY_KEY_CONSTRAINT_DROPPABLE_OPTION 'ON';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table """ + defs.testcat + """.""" + defs.testsch1 + """.a2t4A (
"varchar1_1"  varchar(55) not null,
varchar1_2  varchar(100) not null,
varchar1_3  varchar(100) not null,
int1        int,
primary key ("varchar1_1",varchar1_2 desc, varchar1_3)) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """control query default  PRIMARY_KEY_CONSTRAINT_DROPPABLE_OPTION 'OFF';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #A002.10 Create hash partitioned table
    stmt = """Create table """ + defs.testcat + """.""" + defs.testsch1 + """.a2t5(
sbin0_4             Integer  default 3 not null,
time0_uniq          Time not null not droppable,
varchar0_500        VarChar(11),
real0_20            Real not null not droppable,
int0_d2_4           Interval day(2)  not null,
ts1_n100            Timestamp,
ubin1_20            Numeric(9) unsigned not null not droppable,
primary key (time0_uniq asc, ubin1_20)) """
    if hpdci.tgtSQ():
        stmt = stmt + """location """ + gvars.g_disc5 + """
hash partition by (time0_uniq,ubin1_20)
(add location """ + gvars.g_disc2 + """, add location """ + gvars.g_disc3 + """);"""
    elif hpdci.tgtTR():
        stmt += """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into """ + defs.testcat + """.""" + defs.testsch1 + """.a2t5 values
(3,time '00:05:56','AAAABAAA',1.0000000E+000,  interval '21'  day(2),timestamp '2000-01-01 00:01:03.000000',0),
(2,time '00:14:51','AAAACAAA',1.0006999E+000,  interval '21'  day(2),timestamp '2000-01-01 00:01:42.375000',12),
(1,time '00:11:47','AAAABAAA',1.0000000E+000,  interval '21'  day(2),timestamp '2000-01-01 00:00:07.875000',16),
(0,time '01:18:30','AAAAFAAA',1.0006999E+000,  interval '21'  day(2),timestamp '2000-01-01 00:00:11.250000',4),
(1,time '01:05:35','AAAABAAA',1.0000000E+000,  interval '21'  day(2),timestamp '2000-01-01 00:00:39.375000',8),
(1,time '01:14:52','AAAAHAAA',1.0006999E+000,  interval '21'  day(2),timestamp '2000-01-01 00:01:43.500000',8),
(1,time '01:05:37','AAAACAAA',1.0000000E+000,  interval '21'  day(2),timestamp '2000-01-01 00:00:41.625000',4),
(2,time '01:13:51','AAAAIAAA',1.0006999E+000,  interval '21'  day(2),timestamp '2000-01-01 00:00:34.875000',0),
(2,time '01:01:59','AAAACAAA',1.0000000E+000,  interval '21'  day(2),timestamp '2000-01-01 00:00:21.375000',8),
(0,time '00:18:59','AAAAIAAA',1.0006999E+000,  interval '21'  day(2),timestamp '2000-01-01 00:00:43.875000',4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """select [first 10] * from """ + defs.testcat + """.""" + defs.testsch1 + """.a2t5 order by 2,7;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001.exp""", """A2s5a""")
    
    #A002.6 create table with clustering key = 247
    stmt = """Create table """ + defs.testcat + """.""" + defs.testsch1 + """.a2t6(
char1_40    char(40) not null not droppable,
char2_40    char(40) not null not droppable,
char3_40    char(40) not null not droppable,
char4_40    char(40) not null not droppable,
char5_40    char(40) not null not droppable,
char6_40    char(40) not null not droppable,
char7_7     char(7) not null not droppable,
char8_40    char(40) not null not droppable,
primary key (char6_40 descending) droppable) """
    if hpdci.tgtSQ():
        stmt = stmt + """location """ + gvars.g_disc6 + """
store by (char1_40, char2_40, char3_40, char4_40, char5_40, char6_40, char7_7)
range partition (add first key 'abcdefghijklmnopqrstuvwxyzxxxxxxxxxxxxxx' location """ + gvars.g_disc7 + """);"""
    elif hpdci.tgtTR():
        stmt += """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into """ + defs.testcat + """.""" + defs.testsch1 + """.a2t6 values
('baaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa','baaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
'baaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa','baaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
'baaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa','baaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
'baaaaaa','baaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'),
('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa','aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa','aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa','aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
'aaaaaaa','aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'),
('caaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa','caaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
'caaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa','caaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
'caaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa','caaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
'caaaaaa','caaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'),
('daaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa','daaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
'daaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa','daaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
'daaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa','daaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
'daaaaaa','daaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """select [first 4] * from """ + defs.testcat + """.""" + defs.testsch1 + """.a2t6 order by 6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001.exp""", """A2s6a""")
    
    #A002.7
    stmt = """create table """ + defs.testcat + """.""" + defs.testsch1 + """.a2t7 (
sdec4_n20           Decimal(4) not null,
int4_yTOm_uniq      Interval year(5) to month not null,
sbin4_n1000         Smallint not null,
time4_1000          Time no default not null,
-- vchar4_n10          varchar(20) default current_user,
vchar4_n10          varchar(20) default 'current user',
real4_2000          Real                       not null,
primary key (sbin4_n1000, time4_1000) droppable) no partition
location """ + gvars.g_disc7 + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """Insert into """ + defs.testcat + """.""" + defs.testsch1 + """.a2t7 values
(   6,interval '72-02'  year(4) to month,866,time '00:14:26','ABAAAAAA',    1.0066000E+002),
(  17,interval '368-01' year(4) to month,417,time '00:06:57','BCAAAAAA',    1.0017000E+001),
(   4,interval '137-02' year(4) to month,646,time '00:10:46','ABAAAAAA',    1.0045999E+004),
(   1,interval '110-01' year(4) to month,321,time '00:05:21','BBAAAAAA',    1.0120999E+003),
(   8,interval '95-08'  year(4) to month,148,time '00:02:28','ADAAAAAA',    1.0347999E+002),
(   2,interval '373-06' year(4) to month,482,time '00:08:02','ACAAAAAA',    1.0082000E+001),
(  14,interval '344-06' year(4) to month,134,time '00:02:14','AEAAAAAA',    1.0134000E+000),
(  11,interval '211-10' year(4) to month,542,time '00:09:02','ACAAAAAA',    1.0142000E+001);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """insert into """ + defs.testcat + """.""" + defs.testsch1 + """.a2t7
(sdec4_n20,int4_yTOm_uniq,sbin4_n1000,time4_1000,real4_2000)
values
(   5,interval '41-07'  year(4) to month,499,time '00:08:19',1.0099000E+001),
(  13,interval '351-07' year(4) to month,219,time '00:03:39',1.0218999E+000);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """select SDEC4_N20, INT4_YTOM_UNIQ, SBIN4_N1000, TIME4_1000, REAL4_2000 from """ + defs.testcat + """.""" + defs.testsch1 + """.a2t7 order by 3,4,2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001.exp""", """A2s7a""")
    
    # cleanup
    stmt = """drop table """ + defs.testcat + """.""" + defs.testsch1 + """.a2t1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table """ + defs.testcat + """.""" + defs.testsch1 + """.a2t2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table """ + defs.testcat + """.""" + defs.testsch1 + """.a2t3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table """ + defs.testcat + """.""" + defs.testsch1 + """.a2t4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table """ + defs.testcat + """.""" + defs.testsch1 + """.a2t5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table """ + defs.testcat + """.""" + defs.testsch1 + """.a2t6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    _testmgr.testcase_end(desc)

def test003(desc="""File attributes"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """set schema """ + defs.testcat + """.""" + defs.testsch1 + """;"""
    output = _dci.cmdexec(stmt)
    
    # A003.0 check default file attributes
    stmt = """create table """ + defs.testcat + """.""" + defs.testsch1 + """.a3t0
(    time7_uniq          Time                       not null not droppable,
sbin7_n20           Smallint                               no default,
char7_500           Character(8)                  no default not null,
int7_hTOs_nuniq     Interval hour(2) to second         ,
primary key (time7_uniq))
location """ + gvars.g_disc6 + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    if hpdci.tgtSQ(): 
        stmt = """showlabel """ + defs.testcat + """.""" + defs.testsch1 + """.a3t0;"""
        output = _dci.cmdexec(stmt)
        _dci.unexpect_error_msg(output)
    
    # A003.2 check specified attributes
    stmt = """create table """ + defs.testcat + """.""" + defs.testsch1 + """.a3t2
(     ubin8_10            Numeric(4) unsigned           not null,
int8_y_n1000        Interval year(3)                   ,
date8_10            Date                          no default not null,
char8_n1000         Character(8)                  no default,
double8_n10         Double Precision              no default,
sdec8_4             Decimal(9) unsigned           not null)
no partition
location """ + gvars.g_disc4 + """
attributes
no auditcompress,
clearonpurge
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    if hpdci.tgtSQ(): 
        stmt = """showlabel """ + defs.testcat + """.""" + defs.testsch1 + """.a3t2;"""
        output = _dci.cmdexec(stmt)
        _dci.unexpect_error_msg(output)
    
    # A003.3 Specify maxextents and extents
    #(with explicit units -- not available in EAP1)
    
    stmt = """create table a3t3 (
real12_n20          Real,
ubin12_2            Numeric(4) unsigned no default not null,
dt12_mTOh_1000      Timestamp(0)        no default not null,
sdec12_n1000        Decimal(18) signed  no default not null,
char12_n2000        Character(8)        no default not null,
int12_yTOm_100      Interval year to month         not null,
primary key (int12_ytom_100 desc, char12_n2000 desc,
sdec12_n1000 desc, dt12_mtoh_1000 ascending))
location """ + gvars.g_disc4 + """
attributes
maxextents 3, extent (512,2048);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    if hpdci.tgtSQ(): 
        stmt = """showlabel """ + defs.testcat + """.""" + defs.testsch1 + """.a3t3;"""
        output = _dci.cmdexec(stmt)
        _dci.unexpect_error_msg(output)
    
    stmt = """drop table """ + defs.testcat + """.""" + defs.testsch1 + """.a3t0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table """ + defs.testcat + """.""" + defs.testsch1 + """.a3t2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table """ + defs.testcat + """.""" + defs.testsch1 + """.a3t3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test004(desc="""Table column names and headings"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """set schema """ + defs.testcat + """.""" + defs.testsch3 + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # A004.1 test max long column name in various places
    
    stmt = """create table a4t1
(g         int not null not droppable,
a123456789b123456789c123456789d123456789e123456789f123456789g123456789h123456789i123456789j123456789k123456789l123456789m1234567 int not null not droppable,
primary key (
g,a123456789b123456789c123456789d123456789e123456789f123456789g123456789h123456789i123456789j123456789k123456789l123456789m1234567) droppable)
store by (g, a123456789b123456789c123456789d123456789e123456789f123456789g123456789h123456789i123456789j123456789k123456789l123456789m1234567)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into a4t1 values (1,2), (2,1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 2)
    
    stmt = """select * from a4t1
order by
a123456789b123456789c123456789d123456789e123456789f123456789g123456789h123456789i123456789j123456789k123456789l123456789m1234567;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 2)
    
    stmt = """select max(g),
a123456789b123456789c123456789d123456789e123456789f123456789g123456789h123456789i123456789j123456789k123456789l123456789m1234567
from a4t1
group by
a123456789b123456789c123456789d123456789e123456789f123456789g123456789h123456789i123456789j123456789k123456789l123456789m1234567
order by
a123456789b123456789c123456789d123456789e123456789f123456789g123456789h123456789i123456789j123456789k123456789l123456789m1234567
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001.exp""", """A4s3""")
    
    stmt = """select max(a123456789b123456789c123456789d123456789e123456789f123456789g123456789h123456789i123456789j123456789k123456789l123456789m1234567)
as max3456789b123456789c123456789d123456789e123456789f123456789g123456789h123456789i123456789j123456789k123456789l123456789m1234567
from a4t1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001.exp""", """A4s4""")
    
    stmt = """delete from a4t1
where
a123456789b123456789c123456789d123456789e123456789f123456789g123456789h123456789i123456789j123456789k123456789l123456789m1234567
<> 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    # A004.2 test long delimited names
    stmt = """create table a4t2
("g"         int not null not droppable,
"p-|++56789&123456789*123456789<123456789?123456789,123456789?123456789+123456789()3456789[]3456789:=3456789;:3456789m1234567"
int not null not droppable,
primary key (
"g",
"p-|++56789&123456789*123456789<123456789?123456789,123456789?123456789+123456789()3456789[]3456789:=3456789;:3456789m1234567") droppable)
store by ("g", "p-|++56789&123456789*123456789<123456789?123456789,123456789?123456789+123456789()3456789[]3456789:=3456789;:3456789m1234567");"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into a4t2 values (1,2), (2,3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 2)
    
    stmt = """select * from a4t2
order by
"p-|++56789&123456789*123456789<123456789?123456789,123456789?123456789+123456789()3456789[]3456789:=3456789;:3456789m1234567";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001.exp""", """A4s5""")
    
    stmt = """select max("g"),
"p-|++56789&123456789*123456789<123456789?123456789,123456789?123456789+123456789()3456789[]3456789:=3456789;:3456789m1234567"
from a4t2
group by
"p-|++56789&123456789*123456789<123456789?123456789,123456789?123456789+123456789()3456789[]3456789:=3456789;:3456789m1234567"
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001.exp""", """A4s6""")
    
    stmt = """select max("p-|++56789&123456789*123456789<123456789?123456789,123456789?123456789+123456789()3456789[]3456789:=3456789;:3456789m1234567")
as "max3456789&123456789*123456789<123456789?123456789,123456789?123456789+123456789()3456789[]3456789:=3456789;:3456789m1234567"
from a4t2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001.exp""", """A4s7""")
    
    stmt = """delete from a4t2
where
"p-|++56789&123456789*123456789<123456789?123456789,123456789?123456789+123456789()3456789[]3456789:=3456789;:3456789m1234567"
<> 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    #A004.3 test short delimited names
    stmt = """set schema """ + defs.testcat2 + """.""" + defs.testsch3 + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    if hpdci.tgtSQ():
        stmt = """create table "a4t3"
("a%&'()*_+" int default 4 not null,
"-.,?:;<>b" int,
"=?[]_|?""c" int) no partition;"""
        output = _dci.cmdexec(stmt)
        _dci.expect_complete_msg(output)
    
        stmt = """insert into "a4t3" values (1,2,3),(4,5,6);"""
        output = _dci.cmdexec(stmt)
        _dci.expect_inserted_msg(output, 2)
    
        stmt = """select max("a%&'()*_+") as "y**()[]<>",
avg("-.,?:;<>b") as "????-+=",
"=?[]_|?""c" as "=?[]_|?""c"
from "a4t3"
where "a%&'()*_+" < 10 and "=?[]_|?""c" is not NULL
group by "=?[]_|?""c"
having "=?[]_|?""c" > 0
order by "=?[]_|?""c";"""
        output = _dci.cmdexec(stmt)
        _dci.expect_file(output, defs.test_dir + """/a001.exp""", """A4s8""")
    
        stmt = """insert into "a4t3" ("-.,?:;<>b","=?[]_|?""c") values (5,6);"""
        output = _dci.cmdexec(stmt)
        _dci.expect_inserted_msg(output, 1)
    
        stmt = """update statistics for table "a4t3" on ("-.,?:;<>b"),("=?[]_|?""c"),
("a%&'()*_+" ,"-.,?:;<>b");"""
        output = _dci.cmdexec(stmt)
        _dci.expect_complete_msg(output)
    
        stmt = """select * from "a4t3";"""
        output = _dci.cmdexec(stmt)
        _dci.expect_file(output, defs.test_dir + """/a001.exp""", """A4s9""")
    
        stmt = """update "a4t3" set "-.,?:;<>b" = 43,
"=?[]_|?""c" = "=?[]_|?""c" + 2
where "a%&'()*_+" < 100;"""
        output = _dci.cmdexec(stmt)
        _dci.expect_updated_msg(output, 3)
    
        stmt = """select * from "a4t3";"""
        output = _dci.cmdexec(stmt)
        _dci.expect_file(output, defs.test_dir + """/a001.exp""", """A4s10""")
    
        stmt = """delete from "a4t3"
where "a%&'()*_+" < 10 and "-.,?:;<>b" > 0 and "=?[]_|?""c" is not NULL;"""
        output = _dci.cmdexec(stmt)
        _dci.expect_deleted_msg(output, 3)
    
    # A004.5 Heading specifications
    stmt = """create table """ + defs.testcat2 + """.""" + defs.testsch3 + """.a4t4
("g"         int not null not droppable no heading,
"k*()%"     int heading '',
"h4[]???"   int heading '+',
"j+=:;>"    int heading
'a123456789b123456789c123456789d123456789e123456789f123456789g123456789h123456789i123456789j123456789k123456789l123456789m1234567')
no partition
location """ + gvars.g_disc1 + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into """ + defs.testcat2 + """.""" + defs.testsch3 + """.a4t4 values (1,2,3,4), (2,1,4,3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 2)
    
    stmt = """select * from """ + defs.testcat2 + """.""" + defs.testsch3 + """.a4t4
order by "j+=:;>";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001.exp""", """A4s11""")
    
    stmt = """set schema """ + defs.testcat2 + """.""" + defs.testsch3 + """;"""
    output = _dci.cmdexec(stmt)
    stmt = """create table "a4t5"
("g" int no heading,
"y&()" int heading '&',
"w2_+[]" int heading
'a123456789b123456789c123456789d123456789e123456789f123456789g123456789h123456789i123456789j123456789k123456789l123456789m1234567',
"col<4>" int,
"col5" int heading 'col5')
no partition
location """ + gvars.g_disc3 + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into "a4t5" values (1,2,3,4,5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select * from "a4t5";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001.exp""", """A4s12""")
    
    # A004.6 show invoke and showdd doesn't display headings
    
    stmt = """invoke "a4t5";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showddl "a4t5";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test005(desc="""Create table store by clause"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """set schema """ + defs.testcat + """.""" + defs.testsch2 + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # A005.1 no pk, no store by
    stmt = """create table """ + defs.testcat + """.""" + defs.testsch2 + """.a5t1 (
char3_4             Character(8)                  no default not null,
sdec4_n20           Decimal(4)                             no default,
int4_yTOm_uniq      Interval year(5) to month   not null,
sbin4_n1000         Smallint                           ,
time4_1000          Time                          no default not null)
no partition
location """ + gvars.g_disc3 + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into """ + defs.testcat + """.""" + defs.testsch2 + """.a5t1 values
('CAAAAAAA', 0 , interval '175-00' year(5) to month,100, time '00:01:40'),
('AAAAAAAA',13 , interval '127-09' year(5) to month,533, time '00:08:53'),
('AAAAAAAA', 0 , interval '300-00' year(5) to month,600, time '00:10:00'),
('DAAAAAAA',13 , interval '86-01'  year(5) to month, 33, time '00:00:33'),
('CAAAAAAA', 0 , interval '241-08' year(5) to month,900, time '00:15:00'),
('BAAAAAAA',13 , interval '244-05' year(5) to month,933, time '00:15:33'),
('AAAAAAAA', 0 , interval '408-04' year(5) to month,900, time '00:15:00'),
('BAAAAAAA',13 , interval '136-01' year(5) to month,633, time '00:10:33');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
   
    # Shouldn't see error. syskey should be there, for no pk, no store by 
    stmt = """select *,syskey from """ + defs.testcat + """.""" + defs.testsch2 + """.a5t1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 8)
   
    if hpdci.tgtSQ(): 
        stmt = """showlabel """ + defs.testcat + """.""" + defs.testsch2 + """.a5t1,detail;"""
        output = _dci.cmdexec(stmt)
        _dci.expect_any_substr(output, """Key Columns: 0 ASC""")
    
    # A005.2 mixed asc/desc PK store by pk
    stmt = """create table """ + defs.testcat + """.""" + defs.testsch2 + """.a5t2 (
char3_4             Character(8)                  no default not null,
sdec4_n20           Decimal(4)                    no default not null not droppable,
int4_yTOm_uniq      Interval year(5) to month   not null,
sbin4_n1000         Smallint                           ,
time4_1000          Time                          no default not null,
primary key (sdec4_n20 desc, time4_1000 asc))
location """ + gvars.g_disc2 + """
store by primary key;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into """ + defs.testcat + """.""" + defs.testsch2 + """.a5t2 values
('CAAAAAAA', 0 , interval '175-00' year(5) to month,100, time '00:01:40'),
('AAAAAPAA',13 , interval '127-09' year(5) to month,533, time '00:08:53'),
('AAYAAAAA', 4 , interval '300-00' year(5) to month,600, time '00:10:00'),
('DAAAAAAA',16 , interval '86-01'  year(5) to month, 33, time '00:00:33'),
('CAAAAAAA', 8 , interval '241-08' year(5) to month,900, time '00:15:00'),
('BAAAMAAA',17 , interval '244-05' year(5) to month,933, time '00:15:33'),
('AAABAAAA', 9 , interval '408-04' year(5) to month,900, time '00:15:00'),
('BAAAAAAA',18 , interval '136-01' year(5) to month,633, time '00:10:33');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """select * from """ + defs.testcat + """.""" + defs.testsch2 + """.a5t2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 8)
   
    if hpdci.tgtSQ(): 
        stmt = """showlabel """ + defs.testcat + """.""" + defs.testsch2 + """.a5t2,detail;"""
        output = _dci.cmdexec(stmt)
        _dci.expect_any_substr(output, """Key Columns: 1 DESC , 4 ASC""")
    
    # A005.3 mixed asc/desc 247-byte PK store by pk
    stmt = """create table """ + defs.testcat + """.""" + defs.testsch2 + """.a5t3 (
char3_4             Character(8)                  no default not null,
sdec4_n20           Decimal(4)                             no default,
int4_yTOm_uniq      Interval year(5) to month   not null,
sbin4_n1000         Smallint                           ,
time4_1000          Time                          no default not null not droppable,
charbig             Char(244)                     not null not droppable,
primary key (time4_1000 asc, charbig desc))
location """ + gvars.g_disc4 + """
store by primary key;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into """ + defs.testcat + """.""" + defs.testsch2 + """.a5t3
values
('CAAAAAAA', 0 , interval '175-00' year(5) to month,100, time '00:01:40',
'a123456789b123456789c123456789d123456789f123456789g123456789g123456789h12346789i123456789j123456789k123456789l123456789m123456789n123456789o123456789p123456789q123456789r123456789s123456789t123456789u123456789v123456789w123456789x123456789y123'),
('AAAAAPAA',13 , interval '127-09' year(5) to month,533, time '00:08:53',
'a123456789b123456789c123456789d123456789f123456789g123456789g123456789h12346789i123456789j123456789k123456789l123456789m123456789n123456789o123456789p123456789q123456789r123456789s123456789t123456789u123456789v123456789w123456789x123456789y124'),
('AAYAAAAA', 0 , interval '300-00' year(5) to month,600, time '00:10:00',
'a123456789b123456789c123456789d123456789f123456789g123456789g123456789h12346789i123456789j123456789k123456789l123456789m123456789n123456789o123456789p123456789q123456789r123456789s123456789t123456789u123456789v123456789w123456789x123456789y125'),
('DAAAAAAA',13 , interval '86-01'  year(5) to month, 33, time '00:00:33',
'a123456789b123456789c123456789d123456789f123456789g123456789g123456789h12346789i123456789j123456789k123456789l123456789m123456789n123456789o123456789p123456789q123456789r123456789s123456789t123456789u123456789v123456789w123456789x123456789y126'),
('CAAAAAAA', 0 , interval '241-08' year(5) to month,900, time '00:15:20',
'a123456789b123456789c123456789d123456789f123456789g123456789g123456789h12346789i123456789j123456789k123456789l123456789m123456789n123456789o123456789p123456789q123456789r123456789s123456789t123456789u123456789v123456789w123456789x123456789y127'),
('BAAAMAAA',13 , interval '244-05' year(5) to month,933, time '00:15:33',
'a123456789b123456789c123456789d123456789f123456789g123456789g123456789h12346789i123456789j123456789k123456789l123456789m123456789n123456789o123456789p123456789q123456789r123456789s123456789t123456789u123456789v123456789w123456789x123456789y128'),
('AAABAAAA', 0 , interval '408-04' year(5) to month,900, time '00:15:00',
'a123456789b123456789c123456789d123456789f123456789g123456789g123456789h12346789i123456789j123456789k123456789l123456789m123456789n123456789o123456789p123456789q123456789r123456789s123456789t123456789u123456789v123456789w123456789x123456789y129'),
('BAAAAAAA',13 , interval '136-01' year(5) to month,633, time '00:10:33',
'a123456789b123456789c123456789d123456789f123456789g123456789g123456789h12346789i123456789j123456789k123456789l123456789m123456789n123456789o123456789p123456789q123456789r123456789s123456789t123456789u123456789v123456789w123456789x123456789y12*')
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """select * from """ + defs.testcat + """.""" + defs.testsch2 + """.a5t3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 8)
   
    if hpdci.tgtSQ(): 
        stmt = """showlabel """ + defs.testcat + """.""" + defs.testsch2 + """.a5t3,detail;"""
        output = _dci.cmdexec(stmt)
        _dci.expect_any_substr(output, """Key Columns: 4 ASC , 5 DESC""")
    
    #A005.4 Create table with no PK,store by not null, not droppable keys
    stmt = """create table """ + defs.testcat + """.""" + defs.testsch2 + """.a5t4 (
char3_4             Varchar(8)                  no default not null not droppable,
sdec4_n20           Decimal(4)                  no default,
int4_yTOm_uniq      Interval year(5) to month   no default not null not droppable,
sbin4_n1000         Smallint                    ,
time4_1000          Time                        no default not null not droppable
)
no partition
location """ + gvars.g_disc2 + """
store by (time4_1000, int4_ytom_uniq, char3_4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into """ + defs.testcat + """.""" + defs.testsch2 + """.a5t4
values
('CAAAAAAA', 0 , interval '175-00' year(5) to month,100, time '00:01:40'),
('AAAAAPAA',13 , interval '127-09' year(5) to month,533, time '00:08:53'),
('AAYAAAAA', 0 , interval '300-00' year(5) to month,600, time '00:10:00'),
('DAAAAAAA',13 , interval '86-01'  year(5) to month, 33, time '00:00:33'),
('CAAAAAAA', 0 , interval '241-08' year(5) to month,900, time '00:15:01'),
('BAAAMAAA',13 , interval '244-05' year(5) to month,933, time '00:15:33'),
('AAABAAAA', 0 , interval '408-04' year(5) to month,900, time '00:15:00'),
('BAAAAAAA',13 , interval '136-01' year(5) to month,633, time '00:10:43');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """select *, syskey from """ + defs.testcat + """.""" + defs.testsch2 + """.a5t4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 8)
   
    if hpdci.tgtSQ(): 
        stmt = """showlabel """ + defs.testcat + """.""" + defs.testsch2 + """.a5t4,detail;"""
        output = _dci.cmdexec(stmt)
        _dci.expect_any_substr(output, """Key Columns: 5 ASC , 3 ASC , 1 ASC , 0 ASC""")
    
    # A005.5 Create table with no PK, store by not null, droppable keys
    stmt = """create table """ + defs.testcat + """.""" + defs.testsch2 + """.a5t5 (
char3_4             Varchar(8)                  no default not null,
sdec4_n20           Decimal(4)                  no default,
int4_yTOm_uniq      Interval year(5) to month   no default not null,
sbin4_n1000         Smallint                    ,
time4_1000          Time                        no default not null
)
no partition
location """ + gvars.g_disc1 + """
store by (int4_ytom_uniq, char3_4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into """ + defs.testcat + """.""" + defs.testsch2 + """.a5t5
values
('CAAAAAAA', 0 , interval '175-00' year(5) to month,100, time '00:01:40'),
('AAAAAPAA',13 , interval '127-09' year(5) to month,533, time '00:08:53'),
('AAYAAAAA', 0 , interval '300-00' year(5) to month,600, time '00:10:00'),
('DAAAAAAA',13 , interval '86-01'  year(5) to month, 33, time '00:00:33'),
('CAAAAAAA', 0 , interval '241-08' year(5) to month,900, time '00:15:01'),
('BAAAMAAA',13 , interval '244-05' year(5) to month,933, time '00:15:33'),
('AAABAAAA', 0 , interval '408-04' year(5) to month,900, time '00:15:00'),
('BAAAAAAA',13 , interval '136-01' year(5) to month,633, time '00:10:43');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """select *, syskey from """ + defs.testcat + """.""" + defs.testsch2 + """.a5t5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 8)
   
    if hpdci.tgtSQ(): 
        stmt = """showlabel """ + defs.testcat + """.""" + defs.testsch2 + """.a5t5,detail;"""
        output = _dci.cmdexec(stmt)
        _dci.expect_any_substr(output, """Key Columns: 3 ASC , 1 ASC , 0 ASC""")
    
    # A005.6 Create table with PK, store by not null, not droppable keys
    stmt = """create table """ + defs.testcat + """.""" + defs.testsch2 + """.a5t6 (
char3_4             Varchar(8)                  no default not null not droppable,
sdec4_n20           Decimal(4)                  no default,
int4_yTOm_uniq      Interval year(5) to month   no default not null not droppable,
sbin4_n1000         Smallint                    ,
time4_1000          Time                        no default not null,
primary key (time4_1000)
)
location """ + gvars.g_disc6 + """
store by primary key;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into """ + defs.testcat + """.""" + defs.testsch2 + """.a5t6
values
('CAAAAAAA', 0 , interval '175-00' year(5) to month,100, time '00:01:40'),
('AAAAAPAA',13 , interval '127-09' year(5) to month,533, time '00:08:53'),
('AAYAAAAA', 0 , interval '300-00' year(5) to month,600, time '00:10:00'),
('DAAAAAAA',13 , interval '86-01'  year(5) to month, 33, time '00:00:33'),
('CAAAAAAA', 0 , interval '241-08' year(5) to month,900, time '00:15:01'),
('BAAAMAAA',13 , interval '244-05' year(5) to month,933, time '00:15:33'),
('AAABAAAA', 0 , interval '408-04' year(5) to month,900, time '00:15:00'),
('BAAAAAAA',13 , interval '136-01' year(5) to month,633, time '00:10:43');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """select * from """ + defs.testcat + """.""" + defs.testsch2 + """.a5t6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 8)
   
    if hpdci.tgtSQ(): 
        stmt = """showlabel """ + defs.testcat + """.""" + defs.testsch2 + """.a5t6,detail;"""
        output = _dci.cmdexec(stmt)
        _dci.expect_any_substr(output, """Key Columns: 3 ASC , 1 ASC , 0 ASC""")
    
    # A005.7 Create table with PK not droppable, no store by clause
    stmt = """create table """ + defs.testcat + """.""" + defs.testsch2 + """.a5t7 (
char3_4             Varchar(8)                  no default not null droppable,
sdec4_n20           Decimal(4)                  no default,
int4_yTOm_uniq      Interval year(5) to month   no default not null droppable,
sbin4_n1000         Smallint                    not null not droppable,
time4_1000          Time                        no default not null not droppable,
primary key (time4_1000,sbin4_n1000)  not droppable
)
location """ + gvars.g_disc5 + """
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into """ + defs.testcat + """.""" + defs.testsch2 + """.a5t7
values
('CAAAAAAA', 0 , interval '175-00' year(5) to month,100, time '00:01:40'),
('AAAAAPAA',13 , interval '127-09' year(5) to month,533, time '00:08:53'),
('AAYAAAAA', 0 , interval '300-00' year(5) to month,600, time '00:10:00'),
('DAAAAAAA',13 , interval '86-01'  year(5) to month, 33, time '00:00:33'),
('CAAAAAAA', 0 , interval '241-08' year(5) to month,900, time '00:15:01'),
('BAAAMAAA',13 , interval '244-05' year(5) to month,933, time '00:15:33'),
('AAABAAAA', 0 , interval '408-04' year(5) to month,900, time '00:15:00'),
('BAAAAAAA',13 , interval '136-01' year(5) to month,633, time '00:10:43');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """select *, syskey from """ + defs.testcat + """.""" + defs.testsch2 + """.a5t7;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    stmt = """select * from """ + defs.testcat + """.""" + defs.testsch2 + """.a5t7;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 8)
    
    # A005.8 Create table with PK, droppable, no store by clause
    stmt = """create table """ + defs.testcat + """.""" + defs.testsch2 + """.a5t8 (
char3_4             Varchar(8)                  no default not null droppable,
sdec4_n20           Decimal(4)                  no default,
int4_yTOm_uniq      Interval year(5) to month   no default not null droppable,
sbin4_n1000         Smallint                    not null not droppable,
time4_1000          Time                        no default not null not droppable,
primary key (time4_1000,sbin4_n1000)  droppable
) no partition
location """ + gvars.g_disc2 + """
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into """ + defs.testcat + """.""" + defs.testsch2 + """.a5t8
values
('CAAAAAAA', 0 , interval '175-00' year(5) to month,100, time '00:01:40'),
('AAAAAPAA',13 , interval '127-09' year(5) to month,533, time '00:08:53'),
('AAYAAAAA', 0 , interval '300-00' year(5) to month,600, time '00:10:00'),
('DAAAAAAA',13 , interval '86-01'  year(5) to month, 33, time '00:00:33'),
('CAAAAAAA', 0 , interval '241-08' year(5) to month,900, time '00:15:01'),
('BAAAMAAA',13 , interval '244-05' year(5) to month,933, time '00:15:33'),
('AAABAAAA', 0 , interval '408-04' year(5) to month,900, time '00:15:00'),
('BAAAAAAA',13 , interval '136-01' year(5) to month,633, time '00:10:43');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """select * from """ + defs.testcat + """.""" + defs.testsch2 + """.a5t8;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 8)
   
    if hpdci.tgtSQ(): 
        stmt = """showlabel """ + defs.testcat + """.""" + defs.testsch2 + """.a5t8,detail;"""
        output = _dci.cmdexec(stmt)
        _dci.expect_any_substr(output, """Key Columns: 0 ASC""")
    
    stmt = """drop table """ + defs.testcat + """.""" + defs.testsch2 + """.a5t1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table """ + defs.testcat + """.""" + defs.testsch2 + """.a5t2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table """ + defs.testcat + """.""" + defs.testsch2 + """.a5t3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table """ + defs.testcat + """.""" + defs.testsch2 + """.a5t4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table """ + defs.testcat + """.""" + defs.testsch2 + """.a5t5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table """ + defs.testcat + """.""" + defs.testsch2 + """.a5t6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table """ + defs.testcat + """.""" + defs.testsch2 + """.a5t7;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table """ + defs.testcat + """.""" + defs.testsch2 + """.a5t8;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test006(desc="""Table constraints,"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """set schema """ + defs.testcat + """.""" + defs.testsch2 + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """Create table a6t1
(char_len1            char character set ISO88591 upshift not null,
pic_char_2           pic x display upshift not null,
char_vary_3          character varying (100) upshift not null,
var_char_4           varchar  (20) upshift not null,
numeric_5            numeric (9,5) unsigned not null not droppable,
small_6	          smallint unsigned not null,
int_7                integer unsigned not null,
large_8              largeint not null,
dec_9                dec(9,3) unsigned not null,
pic_10               picture s9(6)V99 display sign is leading not null not droppable,
date_14              date not null,
time6_15             time(6) not null unique,
timestamp_16         timestamp(6) not null unique,
int_17               interval year to month not null,
primary key (var_char_4, int_17) droppable,
unique  (char_len1, pic_char_2, char_vary_3, var_char_4, numeric_5),
unique  (small_6, int_7, large_8, dec_9, pic_10),
unique  (date_14, time6_15, timestamp_16, int_17)
)
location """ + gvars.g_disc4 + """
-- store by (numeric_5, pic_10)
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into a6t1 values
('a','a','a03','a20',1111.11111,1,1,1,111111.111,-1111.11,
date '2001-01-01', time '12:01:01.111111', timestamp '2001-01-01:01:01:01.111111',
interval '01-01' year to month),
('b','b','b03','b20',2111.11111,2,2,2,211111.111,-2111.11,
date '2001-01-02', time '12:02:01.111111', timestamp '2001-01-02:01:01:01.222222',
interval '02-02' year to month);"""
    output = _dci.cmdexec(stmt)
    
    # A006.2 create table with 255-byte unique constraint
    stmt = """create table a6t2 (
char200 char(200) not null not droppable,
char50 char(50) not null not droppable,
char5 char(5) not null not droppable,
unique (char200, char50, char5)) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into a6t2 values
('aaaaaaa','bbbbb','ccccc'),
('aaaaaaa','bbbb','ccccc');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 2)
    
    stmt = """insert into a6t2 values
('aaaaaaa','bbbbb','ccccc');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8102')
    
    stmt = """alter table a6t2 add primary key (char5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    stmt = """Create table a6t3
(char_len1            char upshift not null
constraint a6t3_1 check(char_len1 <> 'Z'),
pic_char_2           pic x display upshift not null
constraint a6t3_2 check(char_len1 <> pic_char_2),
char_vary_3          character varying (100) upshift not null
constraint a6t3_3 check(char_vary_3 not in ('Z01','Z02','Z03')),
var_char_4           varchar  (20) upshift not null
constraint """ + defs.testsch2 + """.a6t3_4 check(char_len1 <> 'P'),
numeric_5            numeric (9,5) unsigned not null not droppable
constraint a6t3_constraint check (numeric_5 between 0 and 6000),
small_6	      smallint unsigned not null
constraint a6t3_6 check (small_6 < 10000),
int_7                integer unsigned not null
constraint """ + defs.testcat + """.""" + defs.testsch2 + """.a6t3_7 check (int_7 > small_6),
large_8              largeint default 43 not null unique
constraint a6t3_8 check (large_8 between 0 and 32000),
dec_9                dec(9,3) unsigned
check (dec_9 > int_7 + 10),
pic_10               picture s9(6)V99 display sign is leading not null not droppable
check (pic_10+40 < 30),
date_14              date not null
check (date_14 > date '2000-01-06'),
time6_15             time(6) not null unique
constraint a6t3_15 check (hour(time6_15) < 13),
timestamp_16         timestamp(6) not null unique
constraint a6t3_16 check (dayofweek(timestamp_16) <> 1),
int_17               interval year to month not null
constraint a6t3_17 check (int_17 < interval '10-11' year to month),
primary key (var_char_4, int_17),
unique  (char_len1, pic_char_2, char_vary_3, var_char_4, numeric_5),
unique  (small_6, int_7, large_8, pic_10),
unique  (date_14, time6_15, timestamp_16, int_17)
)
location """ + gvars.g_disc4 + """
store by primary key;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
 
    stmt = """insert into a6t3 values
('x','a','a03','a20',1111.11111,1,10,1,111111.111,-1111.11,
date '2001-01-01', time '12:01:01.111111', timestamp '2001-01-01:01:01:01.111111',
interval '01-01' year to month),
('y','b','b03','b20',2111.11111,2,20,2,211111.111,-2111.11,
date '2001-01-02', time '12:02:01.111111', timestamp '2001-01-02:01:01:01.222222',
interval '02-02' year to month);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 2)
    
    stmt = """purgedata a6t3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # violate constraint a6t3_1
    # use #expect because constraint name changes
    stmt = """insert into a6t3 values
('z','a','a03','a20',1111.11111,1,10,1,111111.111,-1111.11,
date '2001-01-01', time '12:01:01.111111', timestamp '2001-01-01:01:01:01.111111',
interval '01-01' year to month);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8101')
    
    # violate constraint a6t3_2
    stmt = """insert into a6t3 values
('y','y','b03','b20',2111.11111,3,20,2,211111.111,-2111.11,
date '2001-01-02', time '12:02:01.111111', timestamp '2001-01-02:01:01:01.222222',
interval '02-02' year to month);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8101')
    #violate constraint a6t3_3
    stmt = """insert into a6t3 values
('y','j','z03','b20',2111.11111,3,20,2,211111.111,-2111.11,
date '2001-01-02', time '12:02:01.111111', timestamp '2001-01-02:01:01:01.222222',
interval '02-02' year to month);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8101')
    #violate constraint a6t3_4
    stmt = """insert into a6t3 values
('P','j','m03','b22',2111.11111,3,20,2,211111.111,-2111.12,
date '2001-01-02', time '12:02:01.111111', timestamp '2001-01-02:01:01:02.222222',
interval '02-03' year to month);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8101')
    # violate constraint a6t3
    stmt = """insert into a6t3 values
('g','a','a03','a20',6000.00001,1,10,1,111111.111,-1111.11,
date '2001-01-01', time '12:01:01.111111', timestamp '2001-01-01:01:01:01.111111',
interval '01-01' year to month);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8101')
    # violate constraint a6t3_6
    stmt = """insert into a6t3 values
('h','a','a03','a20',1111.11111,10001,10,1,111111.111,-1111.11,
date '2001-01-01', time '12:01:01.111111', timestamp '2001-01-01:01:01:01.111111',
interval '01-01' year to month);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8101')
    # violate constraint a6t3_7
    stmt = """insert into a6t3 values
('h','a','a03','a20',1111.11111,8000,10,1,111111.111,-1111.11,
date '2001-01-01', time '12:01:01.111111', timestamp '2001-01-01:01:01:01.111111',
interval '01-01' year to month);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8101')
    # violate constraint a6t3_8
    stmt = """insert into a6t3 values
('h','a','a03','a20',1111.11111,1,10,-1,111111.111,-1111.11,
date '2001-01-01', time '12:01:01.111111', timestamp '2001-01-01:01:01:01.111111',
interval '01-01' year to month);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8101')
    # violate constraint a6t3_9
    stmt = """insert into a6t3 values
('h','a','a03','a20',1111.11111,10,11,11,7.111,-1111.11,
date '2001-01-01', time '12:01:01.111111', timestamp '2001-01-01:01:01:01.111111',
interval '01-01' year to month);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8101')
    # violate constraint a6t3_10
    stmt = """insert into a6t3 values
('h','a','a03','a20',1111.11111,9,10,1,9.22,-10.22,
date '2001-01-01', time '12:01:01.111111', timestamp '2001-01-01:01:01:01.111111',
interval '01-01' year to month);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8101')
    # violate constraint a6t3_14
    stmt = """insert into a6t3 values
('h','a','a03','a20',1111.11111,1,10,1,111111.111,-1111.11,
date '2000-01-06', time '12:01:01.111111', timestamp '2001-01-01:01:01:01.111111',
interval '01-01' year to month);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8101')
    # violate constraint a6t3_15
    stmt = """insert into a6t3 values
('h','a','a03','a20',1111.11111,1,10,1,111111.111,-1111.11,
date '2001-01-01', time '13:01:01.111111', timestamp '2001-01-01:01:01:01.111111',
interval '01-01' year to month);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8101')
    # violate constraint a6t3_16
    stmt = """insert into a6t3 values
('h','a','a03','a20',1111.11111,1,10,1,111111.111,-1111.11,
date '2001-01-01', time '10:01:01.111111', timestamp '2002-08-18:01:01:01.111111',
interval '01-01' year to month);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8101')
    # violate constraint a6t3_17
    stmt = """insert into a6t3 values
('h','a','a03','a20',1111.11111,1,10,1,111111.111,-1111.11,
date '2001-01-01', time '11:01:01.111111', timestamp '2001-01-01:01:01:01.111111',
interval '11-00' year to month);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8101')
    
    # okay to insert NULL into column with calculated constraint
    stmt = """insert into a6t3 values
('h','a','a03','a20',1111.11111,1,10,1,NULL,-1111.11,
date '2001-01-01', time '11:01:01.111111', timestamp '2001-01-01:01:01:01.111111',
interval '10-00' year to month);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """create table a6t4 (
char_len1            char upshift not null
constraint a6t4_1 check(char_len1 <> 'Z'),
pic_char_2           pic x display upshift not null
constraint a6t4_2 check(char_len1 <> pic_char_2),
char_vary_3          character varying (100) upshift not null
constraint a6t4_3 check(char_vary_3 not in ('Z01','Z02','Z03')),
var_char_4           varchar  (20) upshift not null
constraint """ + defs.testsch2 + """.a6t4_4 check(char_len1 <> 'P'),
numeric_5            numeric (9,5) unsigned not null not droppable
constraint a6t4_constraint check (numeric_5 between 0 and 6000),
small_6	      smallint unsigned not null
constraint a6t4_6 check (small_6 < 10000),
int_7                integer unsigned not null
constraint """ + defs.testcat + """.""" + defs.testsch2 + """.a6t4_7 check (int_7 > small_6),
large_8              largeint default 43 not null unique
constraint a6t4_8 check (large_8 between 0 and 32000),
dec_9                dec(9,3) unsigned
check (dec_9 > int_7 + 10),
pic_10               picture s9(6)V99 display sign is leading not null not droppable
check (pic_10+40 < 30),
date_14              date not null
check (date_14 > date '2000-01-06'),
time6_15             time(6) not null unique
constraint a6t4_15 check (hour(time6_15) < 13),
timestamp_16         timestamp(6) not null unique
constraint a6t4_16 check (dayofweek(timestamp_16) <> 1),
int_17               interval year to month not null
constraint a6t4_17 check (int_17 < interval '10-11' year to month),
primary key (var_char_4, int_17),
check (large_8 > int_7 and int_7 > small_6),
check (dayofweek(timestamp_16) > dayofweek(date_14))
)
location """ + gvars.g_disc4 + """
store by primary key;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
 
    stmt = """insert into a6t4 values
('h','a','a03','a20',1111.11111,1,10,20,21,-1111.11,
date '2001-01-01', time '11:01:01.111111', timestamp '2001-01-02:01:01:01.111111',
interval '10-00' year to month);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """purgedata a6t4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # violate first constraint
    stmt = """insert into a6t4 values
('h','a','a03','a20',1111.11111,1,10,10,NULL,-1111.11,
date '2001-01-01', time '11:01:01.111111', timestamp '2001-01-02:01:01:01.111111',
interval '10-00' year to month);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8101')
    
    # violate second constraint
    stmt = """insert into a6t4 values
('h','a','a03','a20',1111.11111,1,10,20,NULL,-1111.11,
date '2001-01-03', time '11:01:01.111111', timestamp '2001-01-02:01:01:01.111111',
interval '10-00' year to month);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8101')
    
    # violate third constraint
    stmt = """insert into a6t4 values
('h','a','Z01','a20',1111.11111,1,10,20,NULL,-1111.11,
date '2001-01-01', time '11:01:01.111111', timestamp '2001-01-02:01:01:01.111111',
interval '10-00' year to month);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8101')
    
    stmt = """drop table """ + defs.testcat + """.""" + defs.testsch2 + """.a6t1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table """ + defs.testcat + """.""" + defs.testsch2 + """.a6t2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table """ + defs.testcat + """.""" + defs.testsch2 + """.a6t3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table """ + defs.testcat + """.""" + defs.testsch2 + """.a6t4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test007(desc="""Column defaults,UNIQUE, constraints"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """set schema """ + defs.testcat + """.""" + defs.testsch2 + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #A007.1 Table with defaults: Null, current_date, current_time,
    #current_timestamp, current_user, user
    stmt = """create table a7t1 (
d1  date         no default not null not droppable,
d2  date         default CURRENT_DATE not null not droppable,
t1  time         no default,
t2  time         default CURRENT_TIME not null not droppable,
ts1 timestamp(3) ,
ts2 timestamp(4) default CURRENT_TIMESTAMP,
i1  int          no default,
i2  int          default 43,
u1  varchar(20)  not null not droppable,
-- u2  varchar(20)  default CURRENT_USER,
-- u3  varchar(20)  default USER,
u2  varchar(20)  default 'CURRENT USER',
u3  varchar(20)  default 'USER',
l1  largeint     no default not null not droppable,
l2  largeint     default NULL,
primary key (d1,u1))
location """ + gvars.g_disc4 + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into """ + defs.testcat + """.""" + defs.testsch2 + """.a7t1 (d1,t1,ts1,i1,u1,l1) values
(date '2003-01-15',time '11:11:11',timestamp '2004-04-15:12:12:12.121',
69,'qadev.teg',127),
(current_date, current_time, current_timestamp, NULL, current_user,
43);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """select * from """ + defs.testcat + """.""" + defs.testsch2 + """.a7t1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    # truncating scale portion of numeric value is okay
    stmt = """create table a7t1a (
n2  numeric(6,2)     default 567.333 not null,
n3  numeric(6,2)     no default not null) no partition;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into a7t1a (n3) values (5678.999);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select * from a7t1a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '567.33')
    _dci.expect_str_token(output, '5678.99')
    
    stmt = """create table a7t2 (
d1  date         no default check (d1 < date '2005-12-15'),
d2  date) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #-----------------------------------------------
    _testmgr.testcase_end(desc)

def test008(desc="""TABLE SPECIAL NAMES negative tests"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #-----------------------------------------------
    
    stmt = """set schema """ + defs.testcat + """.""" + defs.testsch2 + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
  
    if hpdci.tgtSQ(): 
        #N001.1 Create TABLE named HISTOGRAMS
        stmt = """create table HISTOGRAMS
(c1 interval year to month,
c2 interval day  to hour,
c3 interval hour to minute) no partition;"""
        output = _dci.cmdexec(stmt)
        _dci.expect_error_msg(output, '1055')
   
        #N001.2 Create TABLE named HISTOGRAM_INTERVALS
        stmt = """create table HISTOGRAM_INTERVALS
( c1 interval year(4),
c2 interval year(3) to month,
c3 interval day to minute) no partition;"""
        output = _dci.cmdexec(stmt)
        _dci.expect_error_msg(output, '1055')
    
        #N001.3 Drop TABLE HISTOGRAMS
        stmt = """drop table HISTOGRAMS;"""
        output = _dci.cmdexec(stmt)
        _dci.expect_error_msg(output, '1119')
    
        # N001.4 Drop TABLE HISTOGRAM_INTERVALS
        stmt = """drop table HISTOGRAM_INTERVALS;"""
        output = _dci.cmdexec(stmt)
        _dci.expect_error_msg(output, '1119')
    
        # N001.6 Create user table in metadata schema
        stmt = """Create table """ + gvars.definition_schema + """.mytab (c1 int, c2 int) no partition;"""
        output = _dci.cmdexec(stmt)
        _dci.expect_error_msg(output, '1118')
    
        # N001.6 create table with invalid delimited identifier
        stmt = """create table """ + defs.testcat + """.""" + defs.testsch2 + """.\"a(&'()*+,-\:< =>?[] |\${}\"
(a int, b int) no partition;"""
        output = _dci.cmdexec(stmt)
        _dci.expect_complete_msg(output)
    
        stmt = """create table """ + defs.testcat + """.""" + defs.testsch2 + """.\" tab1 \" (a int, \"a(&'()*+,-\:< =>?[] |\${}\" int) no partition;"""
        output = _dci.cmdexec(stmt)
        _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test009(desc="""FILE OPTIONS negative tests"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """set schema """ + defs.testcat + """.""" + defs.testsch2 + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    # N002.1 Create TABLE with vertical partitions
    stmt = """create table t1 (c1 int not null not droppable, c2 int, c3 int, primary key (c1))
separate by column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # N002.2 Create non-audited table
    # TRAF: This is ignored by Traf right now
    stmt = """create table t2 (c1 int, c2 int) no partition attributes no audit;"""
    output = _dci.cmdexec(stmt)
    if hpdci.tgtSQ():
        _dci.expect_error_msg(output, '3070')
    elif hpdci.tgtTR():
        _dci.expect_complete_msg(output)
 
    # N002.3 Create TABLE with partition on non-existent disk
    # TRAF: This is ignored by Traf right now
    stmt = """create table t3 (c1 int not null not droppable, c2 int, primary key (c1))
location """ + gvars.g_disc4 + """
range partition (add first key 43 location $nodisk);"""
    output = _dci.cmdexec(stmt)
    if hpdci.tgtSQ():
        _dci.expect_error_msg(output, '1057')
    elif hpdci.tgtTR():
        _dci.expect_complete_msg(output)

    # N002.4 Misspell partition
    stmt = """create table t4 (c1 int not null, c2 int not null, primary key (c1))
location """ + gvars.g_disc5 + """
parition (add first key 43 location """ + gvars.g_disc6 + """);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    # N002.5 Create TABLE with hash partition specifying first key
    stmt = """create table t5 (c1 int not null not droppable, c2 int not null, primary key (c1))
location """ + gvars.g_disc2 + """
hash partition  by (c1) (add first key 43 location """ + gvars.g_disc4 + """);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3153')

    # N002.6 Create TABLE with SYSKEY where partitions are specified
    # TRAF: This is ignored by Traf right now
    stmt = """create table t6 (c1 int not null, c2 int)
location """ + gvars.g_disc4 + """
range partition (add first key 43 location """ + gvars.g_disc5 + """);"""
    output = _dci.cmdexec(stmt)
    if hpdci.tgtSQ():
        _dci.expect_error_msg(output, '1116')
    elif hpdci.tgtTR():
        _dci.expect_complete_msg(output)

    # N002.7 Create TABLE with store by syskey
    stmt = """create table t7 (c1 int, c2 int) store by syskey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    # N002.8 Create TABLE with non-existent disk location specified
    # N002.9 Create TABLE misspell location
    stmt = """create table t9 (c1 int not null not droppable primary key, c2 int)
locaton """ + gvars.g_disc5 + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    #N002.10 Create table with duplicate column specified in PK
    # TRAF: This is ignored by Traf right now
    stmt = """create table t10 (c1 int not null not droppable, c2 int, c3 int not null not droppable,
primary key (c1,c3,c1));"""
    output = _dci.cmdexec(stmt)
    if hpdci.tgtSQ():
        _dci.expect_error_msg(output, '1016')
    elif hpdci.tgtTR():
        _dci.expect_complete_msg(output)
 
    #N002.11 Create table with primary key and insert NULL values into PK cols
    stmt = """create table t11 (c1 int not null not droppable, c2 int, c3 int not null not droppable,
primary key (c1, c3));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    #ERROR[4122] NULL cannot be assigned to NOT NULL column R3TABS.T001B.T11.C3.
    stmt = """insert into t11 values (1,2,3),(2,3,NULL);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4122')
    stmt = """drop table t11;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #N002.12 Create table with primary key and insert duplicate values into PK cols
    stmt = """create table t12 (c1 int not null not droppable, c2 int, c3 int not null not droppable,
primary key (c1, c3));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """insert into t12 values (1,2,3),(2,3,4),(1,5,3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8102')
    stmt = """drop table t12;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #N002.13 Create table with PK specified both on column level and table level
    stmt = """create table t13 (c1 int not null not droppable primary key,
c2 int not null not droppable,
primary key (c1));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3106')
    
    #N002.15 Create table with droppable primary key and update PK column
    stmt = """create table t15 (c1 int not null not droppable primary key droppable,
c2 int) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    ##expect any *ERROR[4033]*
    #Behavior change, PK is now updatable
    stmt = """update t15 set c1 = c1+1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 0)
    
    stmt = """drop table t15;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    #N002.16 Create table with PK on nullable columns
    # R2.5 NCI This is supported in mode special 1, but not in the regular mode.
    # R2.5 NCI $err_msg 1135 C1
    stmt = """create table t16 (c1 varchar(16), c2 int not null,
primary key (c2,c1));"""
    output = _dci.cmdexec(stmt)
    
    #N002.17 Create table with droppable PK and STORE BY Primary key clause
    stmt = """create table t17 (c1 int not null not droppable primary key droppable,
c2 int)
store by primary key;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3065')
    
    # N002.18 Create table with not droppable pk > 255
    stmt = """create table t18 (
"varchar1_1"  varchar(56) not null,
varchar1_2  varchar(100) not null,
varchar1_3  varchar(100) not null,
int1        int,
primary key ("varchar1_1",varchar1_2 desc, varchar1_3) not droppable);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test010(desc="""ATTRIBUTES negative tests"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """set schema """ + defs.testcat + """.""" + defs.testsch2 + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    # N003.1 Create table misspell AUDITCOMPRESS
    stmt = """create table t1 (c1 int, c2 int) attributes auditcomp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    # N003.2 Create table BLOCKSIZE > 4096
    stmt = """create table t2 (c1 int, c2 int) attributes blocksize 5000;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3058')
    # N003.3 Create table Blocksize <>4096
    stmt = """create table t3 (c1 int, c2 int) attributes blocksize 512;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3058')
    # N003.4 Create table Blocksize misspelled
    stmt = """create table t4 (c1 int, c2 int) attributes block 4096;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    # N003.5 Create table CLEARONPURGE misspelled
    stmt = """create table t5 (c1 int, c2 int) attributes clearpurge;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    # N003.6 Create table with dcompress
    stmt = """create table t6 (c1 int, c2 int) attributes dcompress;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    # N003.7 Create table with icompress
    stmt = """create table t7 (c1 int, c2 int) no partition attributes icompress;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table t7;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #CR fixed in MX1021
    # N003.8 Create table with maxsize
    stmt = """create table t8 (c1 int, c2 int) attributes maxsize 4G;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # N003.9 Create table with several attributes, not separated by comma
    # 6/9/03 comma now optional
    ##expect any *ERROR[3026]*
    stmt = """create table t9 (c1 int, c2 int) attributes clearonpurge auditcompress;"""
    output = _dci.cmdexec(stmt)
    
    #N003.10 Create TABLE with MAXEXTENT > 959
    stmt = """create table n10 (c1 varchar(23), c2 varchar(43))
location """ + gvars.g_disc7 + """
attributes
maxextents 960;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3191')
    #N003.11 Create TABLE with MAXEXTENT < 1
    stmt = """create table n11 (c1 varchar(23), c2 varchar(43))
location """ + gvars.g_disc2 + """
attributes
maxextents 0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3191')
    #N003.12 Create TABLE omitting value for MAXEXTENTS
    stmt = """create table n12 (c1 varchar(23), c2 varchar(43))
location """ + gvars.g_disc1 + """
attributes
maxextents ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    #N003.13 Create TABLE  specifying FORMAT 2
    stmt = """create table n13 (c1 interval year(3), c2 interval day(3),
c3 interval month(3))
attributes format 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #N003.14 Create TABLE with 0 extents (rounds to 2 to meet
    #minimum requirements), so we expect ext(2,64)
    stmt = """create table n14 (c1 interval year to month,
c2 interval day to hour,
c3 interval hour to minute)
no partition
attributes
extent (0,64);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #N003.15 Create table with 7 extents (rounds to 8, a multiple of blocksize)
    stmt = """create table n15 (c1 interval year to month,
c2 interval day  to hour,
c3 interval hour to minute)
no partition
attributes
extent (2,7);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #N003.16 Create table with extents(1,9) (rounds to 2,10)
    stmt = """create table n16 (c1 int, c2 int, c3 int)
no partition
attributes extent(1,9);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)

def test011(desc="""Column and Heading negative tests"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #----------------------------------------------
    
    stmt = """set schema """ + defs.testcat + """.""" + defs.testsch2 + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # N004.1 Omit columns for table
    stmt = """create table t1 () attributes clearonpurge, maxextents 43;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    # N004.2 Invalid SQL identifier for column name
    stmt = """create table t2 (c1 int, c2*2 int);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    # N004.3 Duplicate column names in same create
    stmt = """create table t3 (c1 int, c2 int, c1 int);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    # N004.4 Column name is reserved word
    stmt = """create table t4 (c1 int, insert int);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # N004.5 Invalid Delimited name specified
    # #expect any *ERROR[3127]*
    stmt = """create table t5 (c5 int not null not droppable primary key, "l@(7" int);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # N004.6 Column name > 128 characters
    stmt = """create table t6 (c6 int,
q1qqqqqqqq2wwwwwwwww3eeeeeeeee4rrrrrrrrr5ttttttttt6yyyyyyyyy7uuuuuuuuu8iiiiiiiii9ooooooooo10pppppppp11aaaaaaaa12ssssssss13ddddddd int)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3118')
    # N004.7 Column name cannot be SYSKEY if SYSKEY generated by system
    stmt = """create table t7 (c1 int not null not droppable, c2 int, syskey largeint)
store by (c1, c2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1080')
    
    # N004.8a Invalid column type
    stmt = """create table t8a (c1 interval year(3) to month, c2 datetime hour to minute,
c3 datetime);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # N004.8 Heading value not in single quotes
    stmt = """create table t7 (c7 int, c8 int heading "c9");"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    # N004.9 Heading keyword without heading value
    stmt = """create table t8 (c8 int, c8  int c0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    # N004.10 Heading > 128 chars
    stmt = """create table t9 (c9 int, c8 int heading
'q1qqqqqqqq2wwwwwwwww3eeeeeeeee4rrrrrrrrr5ttttttttt6yyyyyyyyy7uuuuuuuuu8iiiiiiiii9ooooooooo10pppppppp11aaaaaaaa12ssssssss13ddddddd'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3132')
    _testmgr.testcase_end(desc)

def test012(desc="""STORE BY negative tests"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """set schema """ + defs.testcat + """.""" + defs.testsch2 + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #N005.1 store by primary key when there isn't one
    stmt = """create table n5a1
( c1 int not null not droppable,
c2 int not null not droppable,
c3 int not null not droppable)
store by primary key;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3188')
    
    #N005.2 store by droppable pk
    stmt = """create table n5a2
(c1 int not null droppable,
c2 int not null not droppable,
c3 int not null not droppable,
primary key (c1,c3))
store by primary key;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1135')
    
    # parameter to following error message changes between testruns
    # so just expect error #   (kk)
    #N005.3 store by entry order
    ##expect any *ERROR[1115]*
    stmt = """create table n5a3
(c1 int not null not droppable,
c2 int not null not droppable,
c3 int not null not droppable,
primary key (c2))
store by entry order;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #N005.4 missspell keyword
    stmt = """create table n5a4
(c1 int not null not droppable,
c2 int not null not droppable,
primary key (c1))
stroe by primary key;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #N005.6 store by not null, droppable keys
    stmt = """create table n5a6
(c1 char(32) not null droppable,
c2 char(8) not null droppable,
c3 char(8) not null not droppable,
primary key (c3) droppable)
store by (c1,c2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    # N005.7 store by non-existent column
    stmt = """Create table """ + defs.testcat + """.""" + defs.testsch2 + """.a2t3(
char2_2            Character(2)not null,
sbin2_uniq         Largeint not null not droppable,
sdec2_500          Decimal(9) signed
--, primary key (sbin2_uniq) droppable
)
location """ + gvars.g_disc3 + """
store by (char2,sbin2_uniq);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    #N005.8 store by syskey
    # The behaviour got changed in R2.2. So changing the expected result.
    # #expect any *ERROR[1088]*
    stmt = """create table """ + defs.testcat + """.""" + defs.testsch2 + """.n5t8
( char4_30           character(4) not null,
sdec7_80           decimal(9) signed)
store by (SYSKEY, char4_30);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test013(desc="""UNIQUE negative tests"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """set schema """ + defs.testcat + """.""" + defs.testsch2 + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # N006.1 1 Create UNIQUE constraint which contains same column twice
    stmt = """create table n6a1
( c1 varchar(31) not null not droppable,
c2 varchar(8)  not null not droppable,
c3 char(43)    not null not droppable,
unique (c2, c3, c2)) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1016')
    
    #N006.2 Create UNIQUE constraint on Table which is identical to primary key
    stmt = """create table n6a2
( c1 varchar(31) not null not droppable,
c2 varchar(8)  not null not droppable,
c3 char(43)    not null not droppable,
primary key (c2, c3, c1),
unique (c2, c3, c1));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1254')
    
    #N006.3 Create UNIQUE constraint on table which is identical to another UNIQUE constraint
    stmt = """create table n6a3
(c1 date not null not droppable,
c2 time not null not droppable,
c3 timestamp not null not droppable,
unique (c2,c1),
unique (c2,c1)) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1254')
    
    #N006.4 Create UNIQUE constraint on table which contains columns NULLABLE
    # TRAF: This is ignored by Traf right now
    stmt = """create table n6a4
(c1 interval year(2) to month,
c2 interval year to month,
c3 interval hour to minute,
unique (c2,c3)) no partition;"""
    output = _dci.cmdexec(stmt)
    if hpdci.tgtSQ():
        _dci.expect_error_msg(output, '1042')
    elif hpdci.tgtTR():
        _dci.expect_complete_msg(output)
 
    #N006.5 Create UNIQUE constraint on table which has more than 255 bytes
    # okay in current release (kk)
    stmt = """create table n6a5
(c1 char(40) not null not droppable,
c2 char(150) not null not droppable,
c3 char(60) not null not droppable,
c4 char(6) not null not droppable,
c5 char(106) not null not droppable,
unique (c4, c3, c1, c2)) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # N006.6 Create table UNIQUE constraint on table  same as column constraint
    stmt = """create table n6a6
(c1 date not null not droppable unique,
c2 time not null not droppable,
c3 timestamp not null not droppable,
unique (c2,c1),
unique (c1)) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1254')
    
    # N006.7 Create check constraint containing subquery
    stmt = """Create table n6t7
(char_len1            char upshift not null
constraint n6t7_1 check(char_len1 <> 'Z'),
pic_char_2           pic x display upshift not null
constraint n6t7_2 check(char_len1 <> pic_char_2),
char_vary_3          character varying (100) upshift not null
constraint n6t7_3 check(char_vary_3 not in ('Z01','Z02','Z03')),
var_char_4           varchar  (20) upshift not null
constraint """ + defs.testsch2 + """.n6t7_4 check(char_len1 <> 'P'),
numeric_5            numeric (9,5) unsigned not null not droppable
constraint n6t7_constraint check (numeric_5 between 0 and 6000),
small_6	      smallint unsigned not null
constraint n6t7_6 check (small_6 < 32769),
int_7                integer unsigned not null
constraint """ + defs.testcat + """.""" + defs.testsch2 + """.n6t7_7 check (int_7 > small_6),
large_8              largeint default 43 not null unique
constraint n6t7_8 check (large_8 >= (select min(int_7) from n6t7)),
dec_9                dec(9,3) unsigned not null
check (dec_9 > int_7 + 10),
pic_10               picture s9(6)V99 display sign is leading not null not droppable
check (pic_10+40 < 30),
float_11             float(11) not null unique
constraint n6t7_11 check (float_11 <> small_6),
real_12              real not null
check (real_12 is not null),
double_13            double precision not null
constraint a6t13 check (double_13 <> 4.3e11),
date_14              date not null
check (date_14 > date '2000-01-06'),
time6_15             time(6) not null unique
constraint n6t7_15 check (hour(time6_15) < 13),
timestamp_16         timestamp(6) not null unique
constraint n6t7_16 check (timestamp_16 < timestamp '2010-04-15:16:17:18.999999'),
int_17               interval year to month not null
constraint n6t7_17 check (int_17 < interval '10-11' year to month),
primary key (var_char_4, int_17),
unique  (char_len1, pic_char_2, char_vary_3, var_char_4, numeric_5),
unique  (small_6, int_7, large_8, dec_9, pic_10, float_11,real_12),
unique  (double_13, date_14, time6_15, timestamp_16, int_17)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4089')
    
    #N006.8 constraint has different catalog name
    stmt = """create table n6t8 (
double_13            double precision not null
constraint nocat.sch.a6t13 check (double_13 <> 4.3e11),
date_14              date not null
check (date_14 > date '2000-01-06'),
time6_15             time(6) not null unique
constraint n6t7_15 check (hour(time6_15) < 13));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3050')
    
    #N006.9 constraint has different schema name
    stmt = """create table n6t9 (
double_13            double precision not null
constraint sch23.a6t13 check (double_13 <> 4.3e11),
date_14              date not null
check (date_14 > date '2000-01-06'),
time6_15             time(6) not null unique
constraint n6t7_15 check (hour(time6_15) < 13));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3050')
    
    #N006.10 drop non-existent constraint
    stmt = """create table n6t10
(
double_13            double precision not null
constraint cs13 check (double_13 <> 4.3e11),
date_14              date not null
check (date_14 > date '2000-01-06'),
time6_15             time(6) not null unique
constraint cs14 check (hour(time6_15) < 13)) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """alter table n6t10 drop constraint cs43;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1005')
    
    _testmgr.testcase_end(desc)

def test014(desc="""negative constraint, default, UNIQUE tests"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """set schema """ + defs.testcat + """.""" + defs.testsch2 + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # N007.1 truncating mantissa portion of numeric value is not okay
    stmt = """create table n7t1 (
n2  numeric(6,2)     default 56667.33 not null,
n3  numeric(6,2)     no default not null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1186')
    
    # N007.2 incorrect datatype for default
    stmt = """create table n7t2 (
i1 interval hour to minute default interval '10-01' year to month
not null not droppable);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1186')
    
    # N007.3 incorrect datatype in check constraint
    # R2.5 NCI $err_msg 4001 CHAR_LEN NUMERIC(1)
    stmt = """create table n7t3 (
char_len1 char(1)  not null not droppable
constraint n1 check(char_len1 <> 7)) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4041')
    
    # N007.4 non-existent column referenced in check constraint
    # $err_msg 4001 CHAR_LEN $testcat.$testsch2.N7T4
    stmt = """create table n7t4 (
char_len1 char(1) not null not droppable
constraint n2 check (char_len < 'z')) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    # N007.5 Unique constraint on PK
    stmt = """create table n7t5 (
char_len1 char(1) not null not droppable unique,
char_len2 char(2) not null not droppable,
primary key (char_len1));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1254')
    
    # N007.6 Drop not null constraint
    if hpdci.tgtSQ():
        stmt = """create table n7t6 (
c1 int constraint c43 check (c1 is not null) not droppable,
c2 int) no partition;"""
        output = _dci.cmdexec(stmt)
        _dci.expect_complete_msg(output)
    
        stmt = """alter table n7t6 drop constraint c43;"""
        output = _dci.cmdexec(stmt)
        _dci.expect_error_msg(output, '1049')
    
    #N007.7 add constraint to metadata table
    if hpdci.tgtSQ():
        stmt = """alter table """ + gvars.definition_schema + """.partitions
add constraint cpart check (max_size > 43);"""
        output = _dci.cmdexec(stmt)
        _dci.expect_error_msg(output, '1040')
    
    #N007.8 default string value too long for column
    stmt = """create table n7t8 (c1 char(4) default 'nnnnn' not null) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    #N007.9 add UNIQUE constraint on SYSKEY
    stmt = """create table n7t9 (c1 int, c2 int, unique(SYSKEY)) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1147')
    
    #N007.10 Add default current_timestamp for column date
    # TRAF: This is not a restriction in Traf
    stmt = """create table n7t10 (d1 date default current_timestamp);"""
    output = _dci.cmdexec(stmt)
    if hpdci.tgtSQ():
        _dci.expect_error_msg(output, '1186')
    elif hpdci.tgtTR():
        _dci.expect_complete_msg(output)
 
    #N007.11 Add default current_date for column time
    # TRAF: This is not a restriction in Traf
    stmt = """create table n7t11 (t1 time default current_date);"""
    output = _dci.cmdexec(stmt)
    if hpdci.tgtSQ():
        _dci.expect_error_msg(output, '1186')
    elif hpdci.tgtTR():
        _dci.expect_complete_msg(output)
  
    #N007.12 Add default current_time for column timestamp
    # TRAF: This is not a restriction in Traf
    stmt = """create table n7t12 (ts1 timestamp(6) default current_time);"""
    output = _dci.cmdexec(stmt)
    if hpdci.tgtSQ(): 
        _dci.expect_error_msg(output, '1186')
    elif hpdci.tgtTR():
        _dci.expect_complete_msg(output)
 
    #N007.13 Add default current_user for char(4) column
    stmt = """create table n7t13 (c1 char(4) default current_user, c2 char(2)) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    stmt = """create table n7t131 (c1 char(2) default current_user, c2 char(2));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    #N007.14 Add default timestamp(6) for timestamp(2) column
    ##expect any *ERROR[1186]*
    # succeeds
    stmt = """create table n7t14 (ts2 timestamp(2) default timestamp '2002-01-01:12:12:12.123456') no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #N007.15 Add default 7.1234 for numeric(5,2) column
    stmt = """create table n7t15 (n1 numeric (5,2) default 7.1234, c2 char(2)) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test015(desc="""negative limits tests"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """set schema """ + defs.testcat + """.""" + defs.testsch2 + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #N009.2 Create table with 98 partitions on same disk
    #(EAP limit, FCS limit is at least 1024)
    stmt = """CREATE TABLE n9t2
(
UNIQUE1                          INT NO DEFAULT NOT NULL NOT DROPPABLE
, UNIQUE2                          INT NO DEFAULT NOT NULL NOT DROPPABLE
, TWO                              INT NO DEFAULT NOT NULL NOT DROPPABLE
, FOUR                             INT NO DEFAULT NOT NULL NOT DROPPABLE
, TEN                              INT NO DEFAULT NOT NULL NOT DROPPABLE
, TWENTY                           INT NO DEFAULT NOT NULL NOT DROPPABLE
, ONEPERCENT                       INT NO DEFAULT NOT NULL NOT DROPPABLE
, TENPERCENT                       INT NO DEFAULT NOT NULL NOT DROPPABLE
, TWENTYPERCENT                    INT NO DEFAULT NOT NULL NOT DROPPABLE
, FIFTYPERCENT                     INT NO DEFAULT NOT NULL NOT DROPPABLE
, UNIQUE3                          INT NO DEFAULT NOT NULL NOT DROPPABLE
, EVENONEPERCENT                   INT NO DEFAULT NOT NULL NOT DROPPABLE
, ODDONEPERCENT                    INT NO DEFAULT NOT NULL NOT DROPPABLE
, STRINGU1                         CHAR(52) NO DEFAULT NOT NULL NOT DROPPABLE
, STRINGU2                         CHAR(52) NO DEFAULT NOT NULL NOT DROPPABLE
, STRING4                          CHAR(54) NO DEFAULT NOT NULL NOT DROPPABLE
, PRIMARY KEY (UNIQUE2)
)
range partition (
add first key (10000) location """ + gvars.g_disc7 + """,
add first key (20000) location """ + gvars.g_disc7 + """,
add first key (30000) location """ + gvars.g_disc7 + """,
add first key (40000) location """ + gvars.g_disc7 + """,
add first key (50000) location """ + gvars.g_disc7 + """,
add first key (60000) location """ + gvars.g_disc7 + """,
add first key (70000) location """ + gvars.g_disc7 + """,
add first key (80000) location """ + gvars.g_disc7 + """,
add first key (90000) location """ + gvars.g_disc7 + """,
add first key (100000) location """ + gvars.g_disc7 + """,
add first key (110000) location """ + gvars.g_disc7 + """,
add first key (120000) location """ + gvars.g_disc7 + """,
add first key (130000) location """ + gvars.g_disc7 + """,
add first key (140000) location """ + gvars.g_disc7 + """,
add first key (150000) location """ + gvars.g_disc7 + """,
add first key (160000) location """ + gvars.g_disc7 + """,
add first key (170000) location """ + gvars.g_disc7 + """,
add first key (180000) location """ + gvars.g_disc7 + """,
add first key (190000) location """ + gvars.g_disc7 + """,
add first key (200000) location """ + gvars.g_disc7 + """,
add first key (210000) location """ + gvars.g_disc7 + """,
add first key (220000) location """ + gvars.g_disc7 + """,
add first key (230000) location """ + gvars.g_disc7 + """,
add first key (240000) location """ + gvars.g_disc7 + """,
add first key (250000) location """ + gvars.g_disc7 + """,
add first key (260000) location """ + gvars.g_disc7 + """,
add first key (270000) location """ + gvars.g_disc7 + """,
add first key (280000) location """ + gvars.g_disc7 + """,
add first key (290000) location """ + gvars.g_disc7 + """,
add first key (300000) location """ + gvars.g_disc7 + """,
add first key (310000) location """ + gvars.g_disc7 + """,
add first key (320000) location """ + gvars.g_disc7 + """,
add first key (330000) location """ + gvars.g_disc7 + """,
add first key (340000) location """ + gvars.g_disc7 + """,
add first key (350000) location """ + gvars.g_disc7 + """,
add first key (360000) location """ + gvars.g_disc7 + """,
add first key (370000) location """ + gvars.g_disc7 + """,
add first key (380000) location """ + gvars.g_disc7 + """,
add first key (390000) location """ + gvars.g_disc7 + """,
add first key (400000) location """ + gvars.g_disc7 + """,
add first key (410000) location """ + gvars.g_disc7 + """,
add first key (420000) location """ + gvars.g_disc7 + """,
add first key (430000) location """ + gvars.g_disc7 + """,
add first key (440000) location """ + gvars.g_disc7 + """,
add first key (450000) location """ + gvars.g_disc7 + """,
add first key (460000) location """ + gvars.g_disc7 + """,
add first key (470000) location """ + gvars.g_disc7 + """,
add first key (480000) location """ + gvars.g_disc7 + """,
add first key (490000) location """ + gvars.g_disc7 + """,
add first key (500000) location """ + gvars.g_disc7 + """,
add first key (510000) location """ + gvars.g_disc7 + """,
add first key (520000) location """ + gvars.g_disc7 + """,
add first key (530000) location """ + gvars.g_disc7 + """,
add first key (540000) location """ + gvars.g_disc7 + """,
add first key (550000) location """ + gvars.g_disc7 + """,
add first key (560000) location """ + gvars.g_disc7 + """,
add first key (570000) location """ + gvars.g_disc7 + """,
add first key (580000) location """ + gvars.g_disc7 + """,
add first key (590000) location """ + gvars.g_disc7 + """,
add first key (600000) location """ + gvars.g_disc7 + """,
add first key (610000) location """ + gvars.g_disc7 + """,
add first key (620000) location """ + gvars.g_disc7 + """,
add first key (630000) location """ + gvars.g_disc7 + """,
add first key (640000) location """ + gvars.g_disc7 + """,
add first key (650000) location """ + gvars.g_disc7 + """,
add first key (660000) location """ + gvars.g_disc7 + """,
add first key (670000) location """ + gvars.g_disc7 + """,
add first key (680000) location """ + gvars.g_disc7 + """,
add first key (690000) location """ + gvars.g_disc7 + """,
add first key (700000) location """ + gvars.g_disc7 + """,
add first key (710000) location """ + gvars.g_disc7 + """,
add first key (720000) location """ + gvars.g_disc7 + """,
add first key (730000) location """ + gvars.g_disc7 + """,
add first key (740000) location """ + gvars.g_disc7 + """,
add first key (750000) location """ + gvars.g_disc7 + """,
add first key (760000) location """ + gvars.g_disc7 + """,
add first key (770000) location """ + gvars.g_disc7 + """,
add first key (780000) location """ + gvars.g_disc7 + """,
add first key (790000) location """ + gvars.g_disc7 + """,
add first key (800000) location """ + gvars.g_disc7 + """,
add first key (810000) location """ + gvars.g_disc7 + """,
add first key (820000) location """ + gvars.g_disc7 + """,
add first key (830000) location """ + gvars.g_disc7 + """,
add first key (840000) location """ + gvars.g_disc7 + """,
add first key (850000) location """ + gvars.g_disc7 + """,
add first key (860000) location """ + gvars.g_disc7 + """,
add first key (870000) location """ + gvars.g_disc7 + """,
add first key (880000) location """ + gvars.g_disc7 + """,
add first key (890000) location """ + gvars.g_disc7 + """,
add first key (900000) location """ + gvars.g_disc7 + """,
add first key (910000) location """ + gvars.g_disc7 + """,
add first key (920000) location """ + gvars.g_disc7 + """,
add first key (930000) location """ + gvars.g_disc7 + """,
add first key (940000) location """ + gvars.g_disc7 + """,
add first key (950000) location """ + gvars.g_disc7 + """,
add first key (960000) location """ + gvars.g_disc7 + """,
add first key (970000) location """ + gvars.g_disc7 + """,
add first key (980000) location """ + gvars.g_disc7 + """,
add first key (990000) location """ + gvars.g_disc7 + """,
add first key (1000000) location """ + gvars.g_disc7 + """,
add first key (1010000) location """ + gvars.g_disc7 + """,
add first key (1020000) location """ + gvars.g_disc7 + """,
add first key (1030000) location """ + gvars.g_disc7 + """,
add first key (1040000) location """ + gvars.g_disc7 + """,
add first key (1050000) location """ + gvars.g_disc7 + """,
add first key (1060000) location """ + gvars.g_disc7 + """,
add first key (1070000) location """ + gvars.g_disc7 + """,
add first key (1080000) location """ + gvars.g_disc7 + """,
add first key (1090000) location """ + gvars.g_disc7 + """,
add first key (1100000) location """ + gvars.g_disc7 + """,
add first key (1110000) location """ + gvars.g_disc7 + """,
add first key (1120000) location """ + gvars.g_disc7 + """,
add first key (1130000) location """ + gvars.g_disc7 + """,
add first key (1140000) location """ + gvars.g_disc7 + """,
add first key (1150000) location """ + gvars.g_disc7 + """,
add first key (1160000) location """ + gvars.g_disc7 + """,
add first key (1170000) location """ + gvars.g_disc7 + """,
add first key (1180000) location """ + gvars.g_disc7 + """,
add first key (1190000) location """ + gvars.g_disc7 + """,
add first key (1200000) location """ + gvars.g_disc7 + """,
add first key (1210000) location """ + gvars.g_disc7 + """,
add first key (1220000) location """ + gvars.g_disc7 + """,
add first key (1230000) location """ + gvars.g_disc7 + """,
add first key (1240000) location """ + gvars.g_disc7 + """,
add first key (1250000) location """ + gvars.g_disc7 + """,
add first key (1260000) location """ + gvars.g_disc7 + """,
add first key (1270000) location """ + gvars.g_disc7 + """,
add first key (1280000) location """ + gvars.g_disc7 + """);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #N009.3 Create table with 209 partitions on different disks
    #(EAP supported limit 128, FCS limit is at least 1024)
    stmt = """CREATE TABLE n9t3
(
UNIQUE1                          INT NO DEFAULT NOT NULL NOT DROPPABLE
, UNIQUE2                          INT NO DEFAULT NOT NULL NOT DROPPABLE
, TWO                              INT NO DEFAULT NOT NULL NOT DROPPABLE
, FOUR                             INT NO DEFAULT NOT NULL NOT DROPPABLE
, TEN                              INT NO DEFAULT NOT NULL NOT DROPPABLE
, TWENTY                           INT NO DEFAULT NOT NULL NOT DROPPABLE
, ONEPERCENT                       INT NO DEFAULT NOT NULL NOT DROPPABLE
, TENPERCENT                       INT NO DEFAULT NOT NULL NOT DROPPABLE
, TWENTYPERCENT                    INT NO DEFAULT NOT NULL NOT DROPPABLE
, FIFTYPERCENT                     INT NO DEFAULT NOT NULL NOT DROPPABLE
, UNIQUE3                          INT NO DEFAULT NOT NULL NOT DROPPABLE
, EVENONEPERCENT                   INT NO DEFAULT NOT NULL NOT DROPPABLE
, ODDONEPERCENT                    INT NO DEFAULT NOT NULL NOT DROPPABLE
, STRINGU1                         CHAR(52) NO DEFAULT NOT NULL NOT DROPPABLE
, STRINGU2                         CHAR(52) NO DEFAULT NOT NULL NOT DROPPABLE
, STRING4                          CHAR(54) NO DEFAULT NOT NULL NOT DROPPABLE
, PRIMARY KEY (UNIQUE2)
)
range partition (
add first key (10000) location """ + gvars.g_disc7 + """  extent (4096,4096),
add first key (20000) location """ + gvars.g_disc7 + """ extent (4096,4096),
add first key (30000) location """ + gvars.g_disc6 + """ extent (4096,4096),
add first key (40000) location """ + gvars.g_disc15 + """ extent (4096,4096),
add first key (50000) location """ + gvars.g_disc1 + """  extent (4096,4096),
add first key (60000) location """ + gvars.g_disc8 + """ extent (4096,4096),
add first key (70000) location """ + gvars.g_disc4 + """  extent (4096,4096),
add first key (80000) location """ + gvars.g_disc10 + """ extent (4096,4096),
add first key (90000) location """ + gvars.g_disc14 + """ extent (4096,4096),
add first key (100000) location """ + gvars.g_disc9 + """ extent (4096,4096),
add first key (110000) location """ + gvars.g_disc7 + """  extent (4096,4096),
add first key (120000) location """ + gvars.g_disc7 + """ extent (4096,4096),
add first key (130000) location """ + gvars.g_disc6 + """ extent (4096,4096),
add first key (140000) location """ + gvars.g_disc15 + """ extent (4096,4096),
add first key (150000) location """ + gvars.g_disc1 + """  extent (4096,4096),
add first key (160000) location """ + gvars.g_disc8 + """ extent (4096,4096),
add first key (170000) location """ + gvars.g_disc4 + """  extent (4096,4096),
add first key (180000) location """ + gvars.g_disc10 + """ extent (4096,4096),
add first key (190000) location """ + gvars.g_disc14 + """ extent (4096,4096),
add first key (200000) location """ + gvars.g_disc9 + """ extent (4096,4096),
add first key (210000) location """ + gvars.g_disc7 + """  extent (4096,4096),
add first key (220000) location """ + gvars.g_disc7 + """ extent (4096,4096),
add first key (230000) location """ + gvars.g_disc6 + """ extent (4096,4096),
add first key (240000) location """ + gvars.g_disc15 + """ extent (4096,4096),
add first key (250000) location """ + gvars.g_disc1 + """  extent (4096,4096),
add first key (260000) location """ + gvars.g_disc8 + """ extent (4096,4096),
add first key (270000) location """ + gvars.g_disc4 + """  extent (4096,4096),
add first key (280000) location """ + gvars.g_disc10 + """ extent (4096,4096),
add first key (290000) location """ + gvars.g_disc14 + """ extent (4096,4096),
add first key (300000) location """ + gvars.g_disc9 + """ extent (4096,4096),
add first key (310000) location """ + gvars.g_disc7 + """  extent (4096,4096),
add first key (320000) location """ + gvars.g_disc7 + """ extent (4096,4096),
add first key (330000) location """ + gvars.g_disc6 + """ extent (4096,4096),
add first key (340000) location """ + gvars.g_disc15 + """ extent (4096,4096),
add first key (350000) location """ + gvars.g_disc1 + """  extent (4096,4096),
add first key (360000) location """ + gvars.g_disc8 + """ extent (4096,4096),
add first key (370000) location """ + gvars.g_disc4 + """  extent (4096,4096),
add first key (380000) location """ + gvars.g_disc10 + """ extent (4096,4096),
add first key (390000) location """ + gvars.g_disc14 + """ extent (4096,4096),
add first key (400000) location """ + gvars.g_disc9 + """ extent (4096,4096),
add first key (410000) location """ + gvars.g_disc7 + """ extent (4096,4096),
add first key (420000) location """ + gvars.g_disc7 + """ extent (4096,4096),
add first key (430000) location """ + gvars.g_disc6 + """ extent (4096,4096),
add first key (440000) location """ + gvars.g_disc15 + """ extent (4096,4096),
add first key (450000) location """ + gvars.g_disc1 + """  extent (4096,4096),
add first key (460000) location """ + gvars.g_disc8 + """ extent (4096,4096),
add first key (470000) location """ + gvars.g_disc4 + """  extent (4096,4096),
add first key (480000) location """ + gvars.g_disc10 + """ extent (4096,4096),
add first key (490000) location """ + gvars.g_disc14 + """ extent (4096,4096),
add first key (500000) location """ + gvars.g_disc9 + """ extent (4096,4096),
add first key (510000) location """ + gvars.g_disc7 + """  extent (4096,4096),
add first key (520000) location """ + gvars.g_disc7 + """ extent (4096,4096),
add first key (530000) location """ + gvars.g_disc6 + """ extent (4096,4096),
add first key (540000) location """ + gvars.g_disc15 + """ extent (4096,4096),
add first key (550000) location """ + gvars.g_disc1 + """  extent (4096,4096),
add first key (560000) location """ + gvars.g_disc8 + """ extent (4096,4096),
add first key (570000) location """ + gvars.g_disc4 + """  extent (4096,4096),
add first key (580000) location """ + gvars.g_disc10 + """ extent (4096,4096),
add first key (590000) location """ + gvars.g_disc14 + """ extent (4096,4096),
add first key (600000) location """ + gvars.g_disc9 + """ extent (4096,4096),
add first key (610000) location """ + gvars.g_disc7 + """  extent (4096,4096),
add first key (620000) location """ + gvars.g_disc7 + """ extent (4096,4096),
add first key (630000) location """ + gvars.g_disc6 + """ extent (4096,4096),
add first key (640000) location """ + gvars.g_disc15 + """ extent (4096,4096),
add first key (650000) location """ + gvars.g_disc1 + """  extent (4096,4096),
add first key (660000) location """ + gvars.g_disc8 + """ extent (4096,4096),
add first key (670000) location """ + gvars.g_disc4 + """  extent (4096,4096),
add first key (680000) location """ + gvars.g_disc10 + """ extent (4096,4096),
add first key (690000) location """ + gvars.g_disc14 + """ extent (4096,4096),
add first key (700000) location """ + gvars.g_disc9 + """ extent (4096,4096),
add first key (710000) location """ + gvars.g_disc7 + """  extent (4096,4096),
add first key (720000) location """ + gvars.g_disc7 + """ extent (4096,4096),
add first key (730000) location """ + gvars.g_disc6 + """ extent (4096,4096),
add first key (740000) location """ + gvars.g_disc15 + """ extent (4096,4096),
add first key (750000) location """ + gvars.g_disc1 + """  extent (4096,4096),
add first key (760000) location """ + gvars.g_disc8 + """ extent (4096,4096),
add first key (770000) location """ + gvars.g_disc4 + """  extent (4096,4096),
add first key (780000) location """ + gvars.g_disc10 + """ extent (4096,4096),
add first key (790000) location """ + gvars.g_disc14 + """ extent (4096,4096),
add first key (800000) location """ + gvars.g_disc9 + """ extent (4096,4096),
add first key (810000) location """ + gvars.g_disc7 + """ extent (4096,4096),
add first key (820000) location """ + gvars.g_disc7 + """ extent (4096,4096),
add first key (830000) location """ + gvars.g_disc6 + """ extent (4096,4096),
add first key (840000) location """ + gvars.g_disc15 + """ extent (4096,4096),
add first key (850000) location """ + gvars.g_disc1 + """  extent (4096,4096),
add first key (860000) location """ + gvars.g_disc8 + """ extent (4096,4096),
add first key (870000) location """ + gvars.g_disc4 + """  extent (4096,4096),
add first key (880000) location """ + gvars.g_disc10 + """ extent (4096,4096),
add first key (890000) location """ + gvars.g_disc14 + """ extent (4096,4096),
add first key (900000) location """ + gvars.g_disc9 + """ extent (4096,4096),
add first key (910000) location """ + gvars.g_disc7 + """  extent (4096,4096),
add first key (920000) location """ + gvars.g_disc7 + """ extent (4096,4096),
add first key (930000) location """ + gvars.g_disc6 + """ extent (4096,4096),
add first key (940000) location """ + gvars.g_disc15 + """ extent (4096,4096),
add first key (950000) location """ + gvars.g_disc1 + """  extent (4096,4096),
add first key (960000) location """ + gvars.g_disc8 + """ extent (4096,4096),
add first key (970000) location """ + gvars.g_disc4 + """  extent (4096,4096),
add first key (980000) location """ + gvars.g_disc10 + """ extent (4096,4096),
add first key (990000) location """ + gvars.g_disc14 + """ extent (4096,4096),
add first key (1000000) location """ + gvars.g_disc9 + """ extent (4096,4096),
add first key (1010000) location """ + gvars.g_disc9 + """ extent (4096,4096),
add first key (1020000) location """ + gvars.g_disc7 + """ extent (4096,4096),
add first key (1030000) location """ + gvars.g_disc6 + """ extent (4096,4096),
add first key (1040000) location """ + gvars.g_disc15 + """ extent (4096,4096),
add first key (1050000) location """ + gvars.g_disc1 + """  extent (4096,4096),
add first key (1060000) location """ + gvars.g_disc8 + """ extent (4096,4096),
add first key (1070000) location """ + gvars.g_disc4 + """  extent (4096,4096),
add first key (1080000) location """ + gvars.g_disc10 + """ extent (4096,4096),
add first key (1090000) location """ + gvars.g_disc14 + """ extent (4096,4096),
add first key (1100000) location """ + gvars.g_disc9 + """ extent (4096,4096),
add first key (1110000) location """ + gvars.g_disc7 + """  extent (4096,4096),
add first key (1120000) location """ + gvars.g_disc7 + """ extent (4096,4096),
add first key (1130000) location """ + gvars.g_disc6 + """ extent (4096,4096),
add first key (1140000) location """ + gvars.g_disc15 + """ extent (4096,4096),
add first key (1150000) location """ + gvars.g_disc1 + """  extent (4096,4096),
add first key (1160000) location """ + gvars.g_disc8 + """ extent (4096,4096),
add first key (1170000) location """ + gvars.g_disc4 + """  extent (4096,4096),
add first key (1180000) location """ + gvars.g_disc10 + """ extent (4096,4096),
add first key (1190000) location """ + gvars.g_disc14 + """ extent (4096,4096),
add first key (1200000) location """ + gvars.g_disc9 + """ extent (4096,4096),
add first key (1210000) location """ + gvars.g_disc7 + """  extent (4096,4096),
add first key (1220000) location """ + gvars.g_disc7 + """ extent (4096,4096),
add first key (1230000) location """ + gvars.g_disc6 + """ extent (4096,4096),
add first key (1240000) location """ + gvars.g_disc15 + """ extent (4096,4096),
add first key (1250000) location """ + gvars.g_disc1 + """  extent (4096,4096),
add first key (1260000) location """ + gvars.g_disc8 + """ extent (4096,4096),
add first key (1270000) location """ + gvars.g_disc4 + """  extent (4096,4096),
add first key (1280000) location """ + gvars.g_disc10 + """ extent (4096,4096),
add first key (1290000) location """ + gvars.g_disc14 + """ extent (4096,4096),
add first key (1300000) location """ + gvars.g_disc9 + """ extent (4096,4096),
add first key (1310000) location """ + gvars.g_disc7 + """  extent (4096,4096),
add first key (1320000) location """ + gvars.g_disc7 + """ extent (4096,4096),
add first key (1330000) location """ + gvars.g_disc6 + """ extent (4096,4096),
add first key (1340000) location """ + gvars.g_disc15 + """ extent (4096,4096),
add first key (1350000) location """ + gvars.g_disc1 + """  extent (4096,4096),
add first key (1360000) location """ + gvars.g_disc8 + """ extent (4096,4096),
add first key (1370000) location """ + gvars.g_disc4 + """  extent (4096,4096),
add first key (1380000) location """ + gvars.g_disc10 + """ extent (4096,4096),
add first key (1390000) location """ + gvars.g_disc14 + """ extent (4096,4096),
add first key (1400000) location """ + gvars.g_disc9 + """ extent (4096,4096),
add first key (1410000) location """ + gvars.g_disc7 + """  extent (4096,4096),
add first key (1420000) location """ + gvars.g_disc7 + """ extent (4096,4096),
add first key (1430000) location """ + gvars.g_disc6 + """ extent (4096,4096),
add first key (1440000) location """ + gvars.g_disc15 + """ extent (4096,4096),
add first key (1450000) location """ + gvars.g_disc1 + """  extent (4096,4096),
add first key (1460000) location """ + gvars.g_disc8 + """ extent (4096,4096),
add first key (1470000) location """ + gvars.g_disc4 + """  extent (4096,4096),
add first key (1480000) location """ + gvars.g_disc10 + """ extent (4096,4096),
add first key (1490000) location """ + gvars.g_disc14 + """ extent (4096,4096),
add first key (1500000) location """ + gvars.g_disc9 + """ extent (4096,4096),
add first key (1510000)  location """ + gvars.g_disc7 + """ extent (4096,4096),
add first key (1520000) location """ + gvars.g_disc7 + """ extent (4096,4096),
add first key (1530000) location """ + gvars.g_disc6 + """ extent (4096,4096),
add first key (1540000) location """ + gvars.g_disc15 + """ extent (4096,4096),
add first key (1550000) location """ + gvars.g_disc1 + """  extent (4096,4096),
add first key (1560000) location """ + gvars.g_disc8 + """ extent (4096,4096),
add first key (1570000) location """ + gvars.g_disc4 + """  extent (4096,4096),
add first key (1580000) location """ + gvars.g_disc10 + """ extent (4096,4096),
add first key (1590000) location """ + gvars.g_disc14 + """ extent (4096,4096),
add first key (1600000) location """ + gvars.g_disc9 + """ extent (4096,4096),
add first key (1610000) location """ + gvars.g_disc7 + """  extent (4096,4096),
add first key (1620000) location """ + gvars.g_disc7 + """ extent (4096,4096),
add first key (1630000) location """ + gvars.g_disc6 + """ extent (4096,4096),
add first key (1640000) location """ + gvars.g_disc15 + """ extent (4096,4096),
add first key (1650000) location """ + gvars.g_disc1 + """  extent (4096,4096),
add first key (1660000) location """ + gvars.g_disc8 + """ extent (4096,4096),
add first key (1670000) location """ + gvars.g_disc4 + """  extent (4096,4096),
add first key (1680000) location """ + gvars.g_disc10 + """ extent (4096,4096),
add first key (1690000) location """ + gvars.g_disc14 + """ extent (4096,4096),
add first key (1700000) location """ + gvars.g_disc9 + """ extent (4096,4096),
add first key (1710000) location """ + gvars.g_disc7 + """  extent (4096,4096),
add first key (1720000) location """ + gvars.g_disc7 + """ extent (4096,4096),
add first key (1730000) location """ + gvars.g_disc6 + """ extent (4096,4096),
add first key (1740000) location """ + gvars.g_disc15 + """ extent (4096,4096),
add first key (1750000) location """ + gvars.g_disc1 + """  extent (4096,4096),
add first key (1760000) location """ + gvars.g_disc8 + """ extent (4096,4096),
add first key (1770000) location """ + gvars.g_disc4 + """  extent (4096,4096),
add first key (1780000) location """ + gvars.g_disc10 + """ extent (4096,4096),
add first key (1790000) location """ + gvars.g_disc14 + """ extent (4096,4096),
add first key (1800000) location """ + gvars.g_disc9 + """ extent (4096,4096),
add first key (1810000) location """ + gvars.g_disc7 + """  extent (4096,4096),
add first key (1820000) location """ + gvars.g_disc7 + """ extent (4096,4096),
add first key (1830000) location """ + gvars.g_disc6 + """ extent (4096,4096),
add first key (1840000) location """ + gvars.g_disc15 + """ extent (4096,4096),
add first key (1850000) location """ + gvars.g_disc1 + """  extent (4096,4096),
add first key (1860000) location """ + gvars.g_disc8 + """ extent (4096,4096),
add first key (1870000) location """ + gvars.g_disc4 + """  extent (4096,4096),
add first key (1880000) location """ + gvars.g_disc10 + """ extent (4096,4096),
add first key (1890000) location """ + gvars.g_disc14 + """ extent (4096,4096),
add first key (1900000) location """ + gvars.g_disc9 + """ extent (4096,4096),
add first key (1910000) location """ + gvars.g_disc7 + """  extent (4096,4096),
add first key (1920000) location """ + gvars.g_disc7 + """ extent (4096,4096),
add first key (1930000) location """ + gvars.g_disc6 + """ extent (4096,4096),
add first key (1940000) location """ + gvars.g_disc15 + """ extent (4096,4096),
add first key (1950000) location """ + gvars.g_disc1 + """  extent (4096,4096),
add first key (1960000) location """ + gvars.g_disc8 + """ extent (4096,4096),
add first key (1970000) location """ + gvars.g_disc4 + """  extent (4096,4096),
add first key (1980000) location """ + gvars.g_disc10 + """ extent (4096,4096),
add first key (1990000) location """ + gvars.g_disc14 + """ extent (4096,4096),
add first key (2000000) location """ + gvars.g_disc9 + """ extent (4096,4096),
add first key (2010000) location """ + gvars.g_disc9 + """ extent (4096,4096),
add first key (2020000) location """ + gvars.g_disc7 + """ extent (4096,4096),
add first key (2030000) location """ + gvars.g_disc6 + """ extent (4096,4096),
add first key (2040000) location """ + gvars.g_disc15 + """ extent (4096,4096),
add first key (2050000) location """ + gvars.g_disc1 + """  extent (4096,4096),
add first key (2060000) location """ + gvars.g_disc8 + """ extent (4096,4096),
add first key (2070000) location """ + gvars.g_disc4 + """  extent (4096,4096),
add first key (2080000) location """ + gvars.g_disc10 + """ extent (4096,4096),
add first key (2090000) location """ + gvars.g_disc14 + """ extent (4096,4096))
attributes
extent (4096,4096)
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into """ + defs.testsch2 + """.n9t3
values (1,2,3,4,5,6,7,8,9,10,11,12,13,'a','b','c');"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    stmt = """update statistics for table n9t3 on stringu1 sample;"""
    output = _dci.cmdexec(stmt)
    stmt = """select max(stringu1) from n9t3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #N009.4 Create table with not null char column > 4040 bytes, an old limit
    stmt = """create table n9t4 (
char_1000a   char(4029) no default not null not droppable
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #N009.5 Create table with not null varchar column > 4036 bytes
    stmt = """create table n9t5 (
char_1000a   varchar(4021) no default not null not droppable
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #N009.6 Create table with null varchar column > 4036 bytes
    stmt = """create table n9t5a (
char_1000a   varchar(4019) no default
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #N009.7 Create table with null char column > 4040 bytes
    stmt = """create table n9t7 (
char_1000a   char(4027) no default
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #N009.8 Create table with column character set kanji
    stmt = """Create Table n9t8
(
nchar0_09_n100      char(8)                   default null,
nchar0_100          char(8)                   no default not null,
nvarchar0_az_uniq   Varchar(8) CHARACTER SET Kanji
no default not null,
nvarchar0_az_10     Varchar(8) CHARACTER SET Kanji
not null,
sdec0_nuniq         Decimal(4)                ,    

nvarchar1_20        char Varying (8)         no default not null,
char1_AaZzb_n4      char(8)              no default,
primary key (nvarchar0_az_uniq));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3010')
    
    #N009.9 Create table with collation set other than binary
    stmt = """create table n9t9 (
char1_az_upshift_20 Char(8) UPSHIFT,
char1_isoasc_colisoasc_500
Char(8) not null COLLATE iso,
varchar1_AaZy_shiftLU_4
Varchar(8) not null COLLATE iso);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    _testmgr.testcase_end(desc)

def test016(desc="""table naming conventions"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    #continued from A001
    
    #set schema R3tabs.T001a;
    #set schema $testcat.$testsch1;
    
    stmt = """set schema """ + defs.testcat + """.""" + defs.testsch1 + """;"""
    output = _dci.cmdexec(stmt)
    
    #A008.1 create tables with same name as metadata table name within a user schema
    
    stmt = """create table objects (a int, b int) no partition location """ + gvars.g_disc3 + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table catsys (a int, b int) no partition location """ + gvars.g_disc3 + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table MP_partitions (a int, b int) no partition location """ + gvars.g_disc3 + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table ref_constraints (a int, b int) no partition location """ + gvars.g_disc3 + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #A008.2 create tables with reserve words
    
    stmt = """create table "avg" (a int, b int) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create table "all" (a int, b int) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create table "any" (a int, b int) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create table "case" (a int, b int) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create table "check" (a int, b int) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create table "count" (a int, b int) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create table "date" (a int, b int) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create table "order" (a int, b int) no partition;"""
    output = _dci.cmdexec(stmt)
    
    #A008.6 create table with space in the name
    stmt = """create table "my table" (c1 int, c2 int) no partition;"""
    output = _dci.cmdexec(stmt)
    if hpdci.tgtSQ():
        _dci.expect_complete_msg(output)
    elif hpdci.tgtTR():
        _dci.expect_error_msg(output, '1422')
 
    #A008.7 create table with an underscore in the name
    
    stmt = """create table tab_A127_ (c1 int, c2 int) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #A008.8 create table with long name and primary key specified
    stmt = """create table
a123456789b123456789c123456789d123456789e123456789f123456789g123456789h123456789i123456789j123456789k123456789l123456789m1234567
(c1 int, c2 int, c3 int not null not droppable, primary key (c3))
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #cleanup
    
    stmt = """drop table objects;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table catsys;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table MP_partitions;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table ref_constraints;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """drop table "avg";"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table "all" ;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table "any" ;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table "case" ;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table "check" ;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table "count" ;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table "date" ;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table "order" ;"""
    output = _dci.cmdexec(stmt)
    
    #drop table \"%&'()*+,-./:;<=>?[]^|\${}%&'()*+,-./:;<=>?[]^|\${}%&'()*+,-./:;<=>?[]^|\${}%&'()*+,-./:;<=>?[]^|\${}%&'()*+,-./:;<=>?[]^|\${}%&'\" ;
    #drop table \"$\";
    #drop table \"\"\"\"
    stmt = """drop table "my table" ;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table tab_A127_ ;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table a123456789b123456789c123456789d123456789e123456789f123456789g123456789h123456789i123456789j123456789k123456789l123456789m1234567;"""
    output = _dci.cmdexec(stmt)
    
    #---------------------------------
    _testmgr.testcase_end(desc)

def test017(desc="""File attribute"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #---------------------------------
    
    stmt = """control query default POS_NUM_OF_PARTNS '4';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """set schema """ + defs.a009_cat1 + """.""" + defs.a009_cat1_sch1 + """;"""
    output = _dci.cmdexec(stmt)
    
    #A009.1 create table with blocksize specified
    
    stmt = """create table A009t1 (
real12_n20          Real,
ubin12_2            Numeric(4) unsigned no default not null,
dt12_mTOh_1000      Timestamp(0)        no default not null,
sdec12_n1000        Decimal(18) signed  no default not null,
char12_n2000        Character(8)        no default not null,
int12_yTOm_100      Interval year to month         not null,
primary key (int12_ytom_100 desc, char12_n2000 desc,
sdec12_n1000 desc, dt12_mtoh_1000 ascending))
location """ + gvars.g_disc4 + """
attribute
blocksize 4096;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    ##expect any *Block Length: 4096*
    if hpdci.tgtSQ():
        stmt = """showlabel A009t1;"""
        output = _dci.cmdexec(stmt)
        _dci.expect_any_substr(output, """Block Length: """ + defs.default_blocksize)
    
    #A009.2 create table with extent 0
    #extent should be (2,64)
    stmt = """create table a009t2 (
real12_n20          Real,
ubin12_2            Numeric(4) unsigned no default not null,
dt12_mTOh_1000      Timestamp(0)        no default not null,
sdec12_n1000        Decimal(18) signed  no default not null,
char12_n2000        Character(8)        no default not null,
int12_yTOm_100      Interval year to month         not null,
primary key (int12_ytom_100 desc, char12_n2000 desc,
sdec12_n1000 desc, dt12_mtoh_1000 ascending))
location """ + gvars.g_disc4 + """
attribute
extent (0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #A009.3 create table with extent 0
    #extent should be (2,4)
    stmt = """create table a009t3 (
real12_n20          Real,
ubin12_2            Numeric(4) unsigned no default not null,
dt12_mTOh_1000      Timestamp(0)        no default not null,
sdec12_n1000        Decimal(18) signed  no default not null,
char12_n2000        Character(8)        no default not null,
int12_yTOm_100      Interval year to month         not null,
primary key (int12_ytom_100 desc, char12_n2000 desc,
sdec12_n1000 desc, dt12_mtoh_1000 ascending))
location """ + gvars.g_disc4 + """
attribute
extent (2,3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #A009.4 create table with extent 2
    #extent size (2,64)
    stmt = """create table a009t4 (
real12_n20          Real,
ubin12_2            Numeric(4) unsigned no default not null,
dt12_mTOh_1000      Timestamp(0)        no default not null,
sdec12_n1000        Decimal(18) signed  no default not null,
char12_n2000        Character(8)        no default not null,
int12_yTOm_100      Interval year to month         not null,
primary key (int12_ytom_100 desc, char12_n2000 desc,
sdec12_n1000 desc, dt12_mtoh_1000 ascending))
location """ + gvars.g_disc4 + """
attribute
extent (2,64);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #A009.5 create table with extent (2,4)
    #extent size (2,4)
    stmt = """create table a009t5 (
real12_n20          Real,
ubin12_2            Numeric(4) unsigned no default not null,
dt12_mTOh_1000      Timestamp(0)        no default not null,
sdec12_n1000        Decimal(18) signed  no default not null,
char12_n2000        Character(8)        no default not null,
int12_yTOm_100      Interval year to month         not null,
primary key (int12_ytom_100 desc, char12_n2000 desc,
sdec12_n1000 desc, dt12_mtoh_1000 ascending))
location """ + gvars.g_disc4 + """
attribute
extent (2,4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #A009.6 create table with extent (409600)
    #extent (409600,64)
    stmt = """create table a009t6 (
real12_n20          Real,
ubin12_2            Numeric(4) unsigned no default not null,
dt12_mTOh_1000      Timestamp(0)        no default not null,
sdec12_n1000        Decimal(18) signed  no default not null,
char12_n2000        Character(8)        no default not null,
int12_yTOm_100      Interval year to month         not null,
primary key (int12_ytom_100 desc, char12_n2000 desc,
sdec12_n1000 desc, dt12_mtoh_1000 ascending))
location """ + gvars.g_disc4 + """
attribute
--extent (409600);
extent (409600,64);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #extent (409600,64)
    
    #A009.7 create table with extent (512000000)
    stmt = """create table a009t7 (
real12_n20          Real,
ubin12_2            Numeric(4) unsigned no default not null,
dt12_mTOh_1000      Timestamp(0)        no default not null,
sdec12_n1000        Decimal(18) signed  no default not null,
char12_n2000        Character(8)        no default not null,
int12_yTOm_100      Interval year to month         not null,
primary key (int12_ytom_100 desc, char12_n2000 desc,
sdec12_n1000 desc, dt12_mtoh_1000 ascending))
location """ + gvars.g_disc4 + """
attribute
extent (512000000,64);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #A009.8 create table with extent (64,512000000)
    #extent  (64,512000000)
    stmt = """create table a009t8 (
real12_n20          Real,
ubin12_2            Numeric(4) unsigned no default not null,
dt12_mTOh_1000      Timestamp(0)        no default not null,
sdec12_n1000        Decimal(18) signed  no default not null,
char12_n2000        Character(8)        no default not null,
int12_yTOm_100      Interval year to month         not null,
primary key (int12_ytom_100 desc, char12_n2000 desc,
sdec12_n1000 desc, dt12_mtoh_1000 ascending))
location """ + gvars.g_disc4 + """
attribute
extent (64,512000000),
maxextents 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #A009.9 create table with maxextents 1
    stmt = """create table a009t9 (
real12_n20          Real,
ubin12_2            Numeric(4) unsigned no default not null,
dt12_mTOh_1000      Timestamp(0)        no default not null,
sdec12_n1000        Decimal(18) signed  no default not null,
char12_n2000        Character(8)        no default not null,
int12_yTOm_100      Interval year to month         not null,
primary key (int12_ytom_100 desc, char12_n2000 desc,
sdec12_n1000 desc, dt12_mtoh_1000 ascending))
location """ + gvars.g_disc4 + """
attribute
maxextents 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #A009.10 create table with maxextents 470
    stmt = """create table a009t10 (
real12_n20          Real,
ubin12_2            Numeric(4) unsigned no default not null,
dt12_mTOh_1000      Timestamp(0)        no default not null,
sdec12_n1000        Decimal(18) signed  no default not null,
char12_n2000        Character(8)        no default not null,
int12_yTOm_100      Interval year to month         not null,
primary key (int12_ytom_100 desc, char12_n2000 desc,
sdec12_n1000 desc, dt12_mtoh_1000 ascending))
location """ + gvars.g_disc4 + """
attribute
maxextents 470;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #A009.11 create table with maxextents 768
    #new maxextents value 768
    stmt = """create table a009t11 (
real12_n20          Real,
ubin12_2            Numeric(4) unsigned no default not null,
dt12_mTOh_1000      Timestamp(0)        no default not null,
sdec12_n1000        Decimal(18) signed  no default not null,
char12_n2000        Character(8)        no default not null,
int12_yTOm_100      Interval year to month         not null,
primary key (int12_ytom_100 desc, char12_n2000 desc,
sdec12_n1000 desc, dt12_mtoh_1000 ascending))
location """ + gvars.g_disc4 + """
attribute
maxextents 768;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #Feature available in FCS
    
    #A009.12 create table with allocate 1
    stmt = """create table a009t12 (
real12_n20          Real,
ubin12_2            Numeric(4) unsigned no default not null,
dt12_mTOh_1000      Timestamp(0)        no default not null,
sdec12_n1000        Decimal(18) signed  no default not null,
char12_n2000        Character(8)        no default not null,
int12_yTOm_100      Interval year to month         not null,
primary key (int12_ytom_100 desc, char12_n2000 desc,
sdec12_n1000 desc, dt12_mtoh_1000 ascending))
location """ + gvars.g_disc4 + """
attribute
ALLOCATE 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #A009.13 create table with allocate 160
    stmt = """create table a009t13 (
real12_n20          Real,
ubin12_2            Numeric(4) unsigned no default not null,
dt12_mTOh_1000      Timestamp(0)        no default not null,
sdec12_n1000        Decimal(18) signed  no default not null,
char12_n2000        Character(8)        no default not null,
int12_yTOm_100      Interval year to month         not null,
primary key (int12_ytom_100 desc, char12_n2000 desc,
sdec12_n1000 desc, dt12_mtoh_1000 ascending))
location """ + gvars.g_disc4 + """
attribute
ALLOCATE 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #ALLOCATE 160; but ERROR 43 disk space
    
    stmt = """drop table a009t1;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table a009t2;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table a009t3;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table a009t4;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table a009t5;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table a009t6;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table a009t7;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table a009t8;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table a009t9;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table a009t10;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table a009t11;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table a009t12;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table a009t13;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test018(desc="""table file attribute"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    #continued from A004
    
    stmt = """set schema """ + defs.testcat + """.""" + defs.testsch1 + """;"""
    output = _dci.cmdexec(stmt)
    
    #A010.1 create table with column names containing underscore
    stmt = """create table a010t1 (my_col_1 int, my_col_2 int) no partition location """ + gvars.g_disc3 + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #A010.2 create table with column names containg space
    stmt = """create table a010t2 (\"my col 1\" int, \"my col 2\" int) no partition location """ + gvars.g_disc3 + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #A010.3 create table with no default specified for columns
    stmt = """create table a010t3 (mycol1 int no default, mycol2 int no default) no partition location """ + gvars.g_disc3 + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop table a010t1;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table a010t2;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table a010t3;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test019(desc="""table constraints"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    #continued from A006
    
    stmt = """set schema """ + defs.testcat + """.""" + defs.testsch1 + """;"""
    output = _dci.cmdexec(stmt)
    
    #a012.1 column with string literal default 228 characters
    stmt = """create table a012t1 (
int1        int not null not droppable,
char3_4     Character(241) default 'a123456789b123456789c123456789d123456789e123456789f123456789g123456789h123456789i123456789j123456789k123456789l123456789m123456789n123456789o123456789p123456789q123456789r123456789s123456789t123456789u123456789v123456789w1234567',
primary key (int1 desc) not droppable
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #a012.2 column with not null, not null not droppable, not null not droppable
    stmt = """create table a012t2
(  int1       int not null,
varchar1   VarChar(11) not null not droppable,
char3_4    Character(8) not null not droppable,
primary key (char3_4)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #a012.3 primary key column
    stmt = """create table a012t3
(  int1       int not null,
varchar1   VarChar(11) not null not droppable,
char3_4    Character(8) primary key not null
)
no partition
location """ + gvars.g_disc7 + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #a012.4 primary key ASC, droppable
    if hpdci.tgtSQ():
        stmt = """create table a012t4
(  int1       int not null,
varchar1   VarChar(11) not null not droppable,
char3_4    Character(8) primary key ASC droppable not null droppable
)
no partition
location """ + gvars.g_disc7 + """;"""
    elif hpdci.tgtTR():
        stmt = """create table a012t4
(  int1       int not null,
varchar1   VarChar(11) not null not droppable,
char3_4    Character(8) primary key ASC droppable not null not droppable
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
 
    #a012.5 primary key ASCENDING, NOT DROPPABLE
    stmt = """create table a012t5
(  int1       int not null,
varchar1   VarChar(11) not null not droppable,
char3_4    Character(8) primary key ASCENDING not droppable not null not droppable
)
location """ + gvars.g_disc7 + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #a012.6 primary key DESC, NOT DROPPABLE
    stmt = """create table a012t6
(  int1       int not null,
varchar1   VarChar(11) not null not droppable,
char3_4    Character(8) primary key DESC not droppable not null not droppable
)
location """ + gvars.g_disc7 + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #a012.7 primary key DESC, DROPPABLE
    if hpdci.tgtSQ():
        stmt = """create table a012t7
(  int1       int not null,
varchar1   VarChar(11) not null not droppable,
char3_4    Character(8) PRIMARY KEY DESC droppable not null droppable
) no partition
location """ + gvars.g_disc7 + """;"""
    elif hpdci.tgtTR():
        stmt = """create table a012t7
(  int1       int not null,
varchar1   VarChar(11) not null not droppable,
char3_4    Character(8) PRIMARY KEY DESC droppable not null not droppable
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #a012.8 default 0, datatype numeric
    stmt = """create table a012t8
(  int1       int not null,
numeric1   numeric(1,1) default 0,
char3_4    Character(8) PRIMARY KEY not null not droppable
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table a012t9
(  int1       int not null,
numeric1   numeric(1,1) default 0.0,
char3_4    Character(8) PRIMARY KEY not null not droppable
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table a012t10
(  int1       int not null,
numeric1   numeric(1,1) default .1,
char3_4    Character(8) PRIMARY KEY not null not droppable
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table a012t11
(  int1       int not null,
numeric1   numeric(2,1) default 0,
char3_4    Character(8) PRIMARY KEY not null not droppable
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """Create table a012t12(
int_0               integer unsigned not null not droppable,
char_len1           char                    upshift default ' ',
pic_char_2          pic x display upshift           default 'b',
char_vary_3         character varying (100) upshift
default 'a123456789b123456789c123456789d123456789e123456789f123456789g123456789h123456789i123456789j123456789',
var_char_4          varchar  (20) upshift           default 'a123456789b[]$%^&*()',
numeric_5           numeric (9,5) unsigned          default 0.00001,
small_6             smallint unsigned               default 65535,
small_7             smallint signed                 default -32768,
small_8             smallint signed                 default  32767,
int_9               integer  unsigned               default 4294967295,
int_10              integer  signed                 default -2147483648,
int_11              integer  signed                 default  2147483647,
large_12            largeint                        default 9.223E18,
dec_13              dec(9,3) unsigned               default 123496.001,
pic_14              picture s9(6)V99 display sign is leading default -999999.99,
float_15            float(22)                       default 2.225E39,
real_16             real                            default 3.402823466e38,
double_17           double precision                default 11.13e-13,
date_18             date                            default date '0004-02-29',
date_19             date                            default date '9999-12-31',
time6_20            time(6)                         default time '00:01:01.000001',
time6_21            time(6)                         default time '23:59:59.999999',
timestamp_22        timestamp(6)                    default timestamp '0004-02-29:01:01:01.000001',
timestamp_23        timestamp(6)                    default timestamp '9999-12-31:23:59:59.999999',
int_24              interval year to month          default interval '10-00' year to month,
primary key (int_0)
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table tab1 (
float_1  float(54) default  2.225E38,
float_2  float(54) default  2.225E38,
float_3  float(54) default  1.797E38,
float_4  float(54) default  1.797E38,
real_1   real      default -1.175494351E-38,
real_2   real      default  1.175494351E38,
real_3   real      default -3.402823466E38,
real_4   real      default  3.402823466E38,
double_1 double precision default 2.225E38,
double_2 double precision default 2.225E38,
double_3 double precision default 1.797E38,
double_4 double precision default 1.797E38
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #cleanup==
    
    stmt = """drop table a012t1;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table a012t2;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table a012t3;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table a012t4;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table a012t5;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table a012t6;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table a012t7;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """drop table a012t8;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table a012t9;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table a012t10;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table a012t11;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table a012t12;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table a012t13;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test020(desc="""Table file attribute negative tests"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    #continued from N003
    
    #N010.1 block size- neg value
    stmt = """create table N010t1 (
real12_n20          Real,
ubin12_2            Numeric(4) unsigned no default not null,
dt12_mTOh_1000      Timestamp(0)        no default not null,
sdec12_n1000        Decimal(18) signed  no default not null,
char12_n2000        Character(8)        no default not null,
int12_yTOm_100      Interval year to month         not null,
primary key (int12_ytom_100 desc, char12_n2000 desc,
sdec12_n1000 desc, dt12_mtoh_1000 ascending))
attribute
blocksize -4096;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #N010.2 block size -non numeric value
    stmt = """create table N010t2 (
real12_n20          Real,
ubin12_2            Numeric(4) unsigned no default not null,
dt12_mTOh_1000      Timestamp(0)        no default not null,
sdec12_n1000        Decimal(18) signed  no default not null,
char12_n2000        Character(8)        no default not null,
int12_yTOm_100      Interval year to month         not null,
primary key (int12_ytom_100 desc, char12_n2000 desc,
sdec12_n1000 desc, dt12_mtoh_1000 ascending))
attribute
blocksize -4o96;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #N010.3 table with maxextents <0
    stmt = """create table N010t3 (
c1 datetime year to month,
c2 datetime year to hour,
c3 datetime month to minute)
attributes
maxextents -20;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #N010.4 table with decimal value maxextents
    stmt = """create table N010t4 (
c1 datetime year to month,
c2 datetime year to hour,
c3 datetime month to minute)
attributes
maxextents 1.5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #N010.5 table with non numeric value maxextents
    stmt = """create table N010t5 (
c1 datetime year to month,
c2 datetime year to hour,
c3 datetime month to minute)
attributes
maxextents 2o;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #N010.6 table with extents <0
    stmt = """create table N010t6 (
c1 datetime year to month,
c2 datetime year to hour,
c3 datetime month to minute)
attributes
extent (0,-2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3195')
    
    #N010.7 table with decimal value extents
    stmt = """create table N010t7 (
c1 datetime year to month,
c2 datetime year to hour,
c3 datetime month to minute)
attributes
extent (1.5,2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #N010.8 table with non numeric value extents
    stmt = """create table N010t8 (
c1 datetime year to month,
c2 datetime year to hour,
c3 datetime month to minute)
attributes
extent (2,8o);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #N010.9 table with unsupported attribute -BUFFERED
    # TRAF: This is ignored by Traf right now
    stmt = """create table N010t9 (
c1 int,
c2 int)
attributes
BUFFERED;"""
    output = _dci.cmdexec(stmt)
    if hpdci.tgtSQ():
        _dci.expect_error_msg(output, '3073')
    elif hpdci.tgtTR():
        _dci.expect_complete_msg(output)
 
    #N010.11 table with unsupported attribute -VERIFIEDWRITES
    stmt = """create table N010t11 (
c1 int,
c2 int)
attributes
VERIFIEDWRITES ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #N010.12 table with unsupported attribute -SERIALWRITES
    stmt = """create table N010t12 (
c1 int,
c2 int)
attributes
SERIALWRITES ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #N010.13 table with unsupported attribute -TABLECODE
    stmt = """create table N010t13 (
c1 int,
c2 int)
attributes
TABLECODE 0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #N010.14 create table with new maxextents +1 (768+1)
    stmt = """create table n1014 (c1 varchar(23), c2 varchar(43))
attributes
maxextents 769;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3191')
    
    #N010.15 create table with old maxextenets 959
    stmt = """create table n1015 (c1 varchar(23), c2 varchar(43))
attributes
maxextents 959;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3191')
    
    _testmgr.testcase_end(desc)

def test021(desc="""table constraint and unique negative tests"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    #continued from N006
    
    #N011.1 table with constraint current_date
    stmt = """create table N011t1(
double_13            double precision not null,
date_14              date not null,
time6_15             time(6) not null unique,
constraint c1 check (date_14 > CURRENT_DATE)
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4131')
    
    #N011.2 table with constraint current_time
    stmt = """create table N011t2(
double_13            double precision not null,
date_14              TIME not null,
time6_15             time(6) not null unique,
constraint c1 check (date_14 > CURRENT_TIME)
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4131')
    
    #N011.3 table with constraint current_timestamp
    stmt = """create table N011t3(
double_13            double precision not null,
date_14              TIMESTAMP not null,
time6_15             time(6) not null unique,
constraint c1 check (date_14 > CURRENT_TIMESTAMP)
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4131')
    
    #-------------------------------------
    _testmgr.testcase_end(desc)

def test022(desc="""Tests for fixes"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #-------------------------------------
    
    #create table ${catddlA013}.${schA013}.\"%\\&()*+,-/:;< =>?[]^|\${}\" (a int, b int);
    stmt = """create table """ + defs.catddlA013 + """.""" + defs.schA013 + """.\"%?&()*+,-?:;< =>?[]|\${}p\" (a int, b int) no partition;"""
    output = _dci.cmdexec(stmt)
    if hpdci.tgtSQ():
        _dci.expect_complete_msg(output)
    elif hpdci.tgtTR():
        _dci.expect_error_msg(output, '1422')
 
    # A013.1 Error message doesn't have table name.
    
    stmt = """set schema """ + defs.a013_2_cat1 + """.""" + defs.a013_2_cat1_sch1 + """;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table cycle ( a int, b int);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3128')
    
    stmt = """create table first ( a int, b int);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # A013.3 Wrong error message returned for duplicate attributes
    stmt = """create table taba133 ( a int)
attributes
clearonpurge,
clearonpurge,
auditcompress,
blocksize 4096,
EXTENT 1024,
MAXEXTENTS 124
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3086')
    
    stmt = """create table taba133 ( a int)
attributes
clearonpurge,
auditcompress,
auditcompress,
blocksize 4096,
EXTENT 1024,
MAXEXTENTS 124
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3083')
    
    stmt = """create table taba133 ( a int)
attributes
clearonpurge,
auditcompress,
blocksize 4096,
blocksize 4096,
EXTENT 1024,
MAXEXTENTS 124
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3092')
    
    stmt = """create table taba133 ( a int)
attributes
clearonpurge,
auditcompress,
blocksize 4096,
EXTENT 1024,
EXTENT 1024
MAXEXTENTS 124
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3079')
    
    stmt = """create table taba133 ( a int)
attributes
clearonpurge,
auditcompress,
blocksize 4096,
EXTENT 1024,
MAXEXTENTS 124,
MAXEXTENTS 124
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3079')
    
    #A013.4 can't create catalog, schema, table that start with a backslash
    
    #$SQL_complete_msg
    stmt = """create catalog "\\a";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    #$SQL_complete_msg
    stmt = """create schema """ + defs.aa11 + """."\\b";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    #$SQL_complete_msg
    stmt = """create table """ + defs.aa11 + """."bb"."\tab1" (a int);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    stmt = """create table """ + defs.aa11 + """."bb"."tab1" (a int) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #A013.5 cannot insert into table in delimited catalog
    
    stmt = """set schema """ + defs.a013_5_cat1 + """.""" + defs.a013_5_cat1_sch1 + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table a02t1
(
-- "c^1" varchar(230) not null,
"c 1" varchar(230) not null,
"c+ < n2" char(230),
"c3" int not null,
primary key ("c 1","c3") not droppable
)
location """ + gvars.g_disc4 + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into a02t1 values
('bbbbbbbbbbbbbbb','cccccccccccccccccc',1001),
('fffffffffffffff','dddddddddddddddddd',1111),
('yyyyyyyyyyyyyyy','ssssssssssssssssss',2222),
('zzzzzzzzzzzzzzz','rrrrrrrrrrrrrrrrrr',10000);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 4)
    
    stmt = """insert into """ + defs.a013_5_cat1 + """.""" + defs.a013_5_cat1_sch1 + """.a02t1 values
('bbbbbbbbbbbbbbb','cccccccccccccccccc',3001),
('fffffffffffffff','dddddddddddddddddd',3111),
('yyyyyyyyyyyyyyy','ssssssssssssssssss',3222),
('zzzzzzzzzzzzzzz','rrrrrrrrrrrrrrrrrr',30000);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 4)
    
    #A13.6 need Error message for extent size greater than 512000000
    
    stmt = """set schema """ + defs.a013_6_cat1 + """.""" + defs.a013_6_cat1_sch1 + """;"""
    output = _dci.cmdexec(stmt)
    
    #should get a out of range error for extent size, not
    # TRAF: This is ignored by Traf right now
    stmt = """create table tab1 ( a int ) attributes extent (513000000) no partition;"""
    output = _dci.cmdexec(stmt)
    if hpdci.tgtSQ():
        _dci.expect_error_msg(output)
    elif hpdci.tgtTR():
        _dci.expect_complete_msg(output)
 
    stmt = """create table tab2 ( a int ) no partition attributes extent (1,513000000), maxextents 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #The problem is with schema, 127 characters work.
    #A13.7 create catalog, schema, and table with 128 characters each.
  
    # TRAF: Trafodion does not guarantee that schema and table names can each
    # use up to 128 characters.  It actualy hangs on HortonWorks (not Cloudera)
    # Launchpad bug #1389791 documents this.  In order to allow tests going, 
    # skip this test for now. 
    if hpdci.tgtSQ(): 
        stmt = """create table
""" + defs.a013_7_cat1 + """.""" + defs.a013_7_cat1_sch1 + """.Y123456789B123456789C123456789D123456789E123456789F123456789G123456789H123456789I123456789J123456789K123456789L123456789M1234567
( a int) no partition;"""
        output = _dci.cmdexec(stmt)
        _dci.expect_complete_msg(output)
    
    #now try schema with only 127 characters
    
        stmt = """create table
""" + defs.a013_7_cat1 + """.""" + defs.a013_7_cat1_sch2 + """.Y123456789B123456789C123456789D123456789E123456789F123456789G123456789H123456789I123456789J123456789K123456789L123456789M1234567
( a int) no partition;"""
        output = _dci.cmdexec(stmt)
        _dci.expect_complete_msg(output)
    
    #a13.8 can create table with delimited name but can't use it
    #for long catalog and schema.
    
    stmt = """set schema """ + defs.a013_7_cat1 + """.""" + defs.a013_7_cat1_sch1 + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table "tab_1" ( a int, b int) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into "tab_1" values ( 1,2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """select * from "tab_1";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #cleanup
    stmt = """CONTROL QUERY DEFAULT SAVE_DROPPED_TABLE_DDL 'OFF';"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

