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

# TESTUNIT TAB008 HASH PARTITION tests
def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci
    
    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()
    
def test001(desc="""Hash partitioning and location"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """set schema """ + defs.my_schema + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #A008.1 Create hash partitioned table with location and "by"
    stmt = """Create table """ + defs.my_schema + """.a1t1(
sbin0_4             Integer  default 3 not null,
"time0_uniq"        Time not null not droppable,
varchar0_500        VarChar(11),
real0_20            Real not null not droppable,
int0_d2_4           Interval day(2)  not null,
ts1_n100            Timestamp,
ubin1_20            Numeric(9) unsigned not null not droppable,
primary key ("time0_uniq" asc, ubin1_20))
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """insert into """ + defs.my_schema + """.a1t1 values
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
    
    # #expectfile $test_dir/A001 A8s1a
    stmt = """select  * from """ + defs.my_schema + """.a1t1 order by \"time0_uniq\";"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
   
    if hpdci.tgtSQ(): 
        stmt = """select ap.partitioning_scheme,
ap.partitioning_key_length,
o.object_name
from
""" + defs.w_catalog + """.""" + gvars.definition_schema + """.access_paths ap,
""" + defs.w_catalog + """.""" + gvars.definition_schema + """.objects o
where
ap.table_uid = o.object_uid and
o.object_name like '%A1T1%';"""
        output = _dci.cmdexec(stmt)
        _dci.expect_selected_msg(output)
    
    # A008.2 Hash Partition on PK by default specifying extent and maxextent
    # ability to specify partition extents is now a post-eap feature
    stmt = """create table a1t2 (
sbin6_nuniq         Largeint            no default,
double6_n2          Float(23),
sdec6_4             Decimal(4) signed   no default not null not droppable
primary key descending not droppable,
char6_n100          Character(8)        no default,
date6_100           Date                not null)
attributes extent (1024,512) ,maxextents 16;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    if hpdci.tgtSQ(): 
        stmt = """select ap.partitioning_scheme, ap.partitioning_key_length,o.object_name    

from """ + gvars.definition_schema + """.objects o
,""" + gvars.definition_schema + """.access_paths
ap
where ap.table_uid = o.object_uid and
o.object_name like '%A1T2%';"""
        output = _dci.cmdexec(stmt)
        _dci.expect_selected_msg(output)
    
    #A001.3  Create hash partitions on same volumes
    stmt = """create table a1t3(
ubin8_10            Numeric(4) unsigned  not null,
int8_y_n1000        Interval year(3) not null,
date8_10            Date no default not null,
char8_n1000         Character(8) no default,
double8_n10         Double Precision no default,
sdec8_4             Decimal(9) unsigned not null,
primary key (date8_10))
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #A001.4 Create hash partitioned table
    stmt = """Create table """ + defs.my_schema + """.a1t4(
sbin0_4             Integer  default 3 not null,
time0_uniq          Time not null not droppable,
varchar0_500        VarChar(11),
real0_20            Real not null not droppable,
int0_d2_4           Interval day(2)  not null,
ts1_n100            Timestamp,
ubin1_20            Numeric(9) unsigned not null not droppable,
primary key (time0_uniq asc, ubin1_20))
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """insert into """ + defs.my_schema + """.a1t4 values
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
    
    stmt = """select [first 10] * from """ + defs.my_schema + """.a1t4 order by time0_uniq;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 10)
   
    if hpdci.tgtSQ(): 
        stmt = """select apc.position_in_row, apc.ordering, apc.part_key_seq_num,
c.column_name , o.object_name
from """ + defs.w_catalog + """.""" + gvars.definition_schema + """.access_path_cols apc,
""" + defs.w_catalog + """.""" + gvars.definition_schema + """.access_paths ap,
""" + defs.w_catalog + """.""" + gvars.definition_schema + """.objects o,
""" + defs.w_catalog + """.""" + gvars.definition_schema + """.cols c
where apc.access_path_uid = ap.access_path_uid and
ap.table_uid = o.object_uid and
c.object_uid = o.object_uid and
c.column_number = apc.column_number and
o.object_name like '%A1T4%'
order by apc.position_in_row;"""
        output = _dci.cmdexec(stmt)
        _dci.expect_selected_msg(output)
    
    #A001.5 Create Hash partitioned table with 247 byte clustering key
    stmt = """Create table """ + defs.my_schema + """.a1t5(
char1_40    char(40) not null not droppable,
char2_40    char(40) not null not droppable,
char3_40    char(40) not null not droppable,
char4_40    char(40) not null not droppable,
char5_40    char(40) not null not droppable,
char6_40    char(40) not null not droppable,
char7_7     char(7) not null not droppable,
char8_40    char(40) not null not droppable,
primary key (char1_40, char2_40 desc, char3_40, char4_40 desc, char5_40, char6_40 desc, char7_7)  )
location """ + gvars.g_disc6 + """
store by (char1_40, char2_40 desc, char3_40, char4_40 desc, char5_40, char6_40 desc, char7_7)
-- hash partition by (char1_40, char2_40, char3_40, char4_40, char5_40, char6_40, char7_7)
-- (add location """ + gvars.g_disc7 + """, add location """ + gvars.g_disc4 + """)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test002(desc="""Negative table HASH partitioning tests"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """set schema """ + defs.my_schema + """;"""
    output = _dci.cmdexec(stmt)
    
    #N001.1 HASH partition with FIRST KEY
    stmt = """create table n8t1(
time7_uniq          Time not null not droppable primary key,
sbin7_n20           Smallint                               no default,
char7_500           Character(8)                  no default not null,
int7_hTOs_nuniq     Interval hour(2) to second(0)        ,
udec7_n10           Decimal(4) unsigned                ,
real7_n4            Real )
location """ + gvars.g_disc6 + """
-- hash partition by (time7_uniq)
-- (add first key time '12:00:01' location """ + gvars.g_disc3 + """)
;"""
    output = _dci.cmdexec(stmt)
    # _dci.expect_error_msg(output, '3153')
    _dci.expect_complete_msg(output)

    #N001.2 HASH partition on SYSKEY
    stmt = """create table n8t2(
sdec9_uniq          Decimal(18) signed            no default not null,
real9_n20           Real                               ,
time9_n4            Time                               ,
char9_100           Character(2)                  no default not null,
int9_dTOf6_2000     Interval day to second(6)   no default not null,
ubin9_n4            Numeric(9) unsigned                    no default)
store by (syskey)
;"""
    output = _dci.cmdexec(stmt)
    if hpdci.tgtSQ():
        _dci.expect_error_msg(output, '1116')
    elif hpdci.tgtTR():
        _dci.expect_complete_msg(output)
    #N001.3 HASH partition by non-existing column
    # R2.5 NCI $err_msg 1009 TIME9_4
    stmt = """create table n8t3(
sdec9_uniq          Decimal(18) signed            no default not null,
real9_n20           Real                               ,
time9_n4            Time                               ,
char9_100           Character(2)                  no default not null,
int9_dTOf6_2000     Interval day to second(6)   no default not null,
ubin9_n4            Numeric(9) unsigned                    no default)
;"""
    output = _dci.cmdexec(stmt)
    if hpdci.tgtSQ():
        _dci.expect_error_msg(output, '1116')
    elif hpdci.tgtTR():
        _dci.expect_complete_msg(output)
    #N001.4 HASH partition by column > 255(?)
    stmt = """create table n8t4(
sdec9_uniq          Decimal(18) signed            no default not null,
real9_n20           Real                               ,
time9_n4            Time                               ,
char9_100           Character(256)                no default not null,
int9_dTOf6_2000     Interval day to second(6)     no default not null,
ubin9_n4            Numeric(9) unsigned           no default)
store by (char9_100)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #N001.5 HASH partition on non-existing volume
    # R2.5 NCI #expect any *ERROR[1057]*
    stmt = """create table n8t5(
sdec9_uniq            Decimal(18) signed no default not null,
real9_n20             Real,
time9_n4              Time,
char9_100             Character(2) no default not null,
int9_dTOf6_2000       Interval day to second(6) no default not null,
ubin9_n4              Numeric(9) unsigned not null not droppable)
store by (ubin9_n4)
;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #N001.6 HASH partition on superset of clustering key
    stmt = """create table n7t6
(     sdec4_n20           Decimal(4)                             no default,
int4_yTOm_uniq      Interval year(5) to month   not null,
sbin4_n1000         Smallint                           ,
time4_1000          Time                          no default not null,
char4_n10           Character(8)                           no default,
real4_2000          Real                       not null,
char5_n20           Character(8)                       ,
sdec5_10            Decimal(9) signed             no default not null,
ubin5_n500          Numeric(9) unsigned                    no default,
real5_uniq          Real                       not null,
dt5_yTOmin_n500     timestamp(0)            ,
int5_hTOs_500       Interval hour to second       no default not null,    

--      int6_dTOf6_nuniq    Interval day to fraction(6)            no default,
int6_dTOf6_nuniq    Interval day to second(6)            no default,
sbin6_nuniq         Largeint                               no default,
double6_n2          Float(23)                          ,
sdec6_4             Decimal(4) signed             no default not null,
char6_n100          Character(8)                           no default,
date6_100           Date                       not null
)
store by (int4_ytom_uniq, int5_htos_500)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    # N001.7 Hash partition on duplicate key
    stmt = """create table n7t6
(     sdec4_n20           Decimal(4)                             no default,
int4_yTOm_uniq      Interval year(5) to month   not null,
sbin4_n1000         Smallint                           ,
time4_1000          Time                          no default not null,
char4_n10           Character(8)                           no default,
real4_2000          Real                       not null,
char5_n20           Character(8)                       ,
sdec5_10            Decimal(9) signed             no default not null,
ubin5_n500          Numeric(9) unsigned                    no default,
real5_uniq          Real                       not null,
dt5_yTOmin_n500     timestamp(0)            ,
int5_hTOs_500       Interval hour to second       no default not null,    

int6_dTOf6_nuniq    Interval day to fraction(6)            no default,
sbin6_nuniq         Largeint                               no default,
double6_n2          Float(23)                          ,
sdec6_4             Decimal(4) signed             no default not null,
char6_n100          Character(8)                           no default,
date6_100           Date                       not null
)
store by (int4_ytom_uniq, int5_htos_500)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3195')
    
    _testmgr.testcase_end(desc)

def test003(desc="""hash partition"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """set schema """ + defs.my_schema + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #A003.1 Table with hash partition (location, extent, maxextent specified)
    stmt = """create table a3t1 (
sbin6_nuniq  Largeint            no default,
double6_n2   Float(23),
sdec6_4      Decimal(4) signed   no default not null not droppable
primary key descending not droppable,
char6_n100          Character(8)        no default,
date6_100           Date                not null)
attributes extent (1024,512) ,maxextents 16;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    ##expectfile $test_dir/a003 a3s1a
    if hpdci.tgtSQ():
        stmt = """select ap.partitioning_scheme, ap.partitioning_key_length,o.object_name
from
""" + gvars.definition_schema + """.objects o,
""" + gvars.definition_schema + """.access_paths ap
where ap.table_uid = o.object_uid and
o.object_name like '%A3T1%';"""
        output = _dci.cmdexec(stmt)
    
    ##expectfile $test_dir/a003 a3s1b
    if hpdci.tgtSQ():
        stmt = """select substring(object_name,1,10),  DATA_SOURCE ,
pri_ext, sec_ext, max_ext from
""" + gvars.definition_schema + """.objects o,
""" + gvars.definition_schema + """.partitions p
where o.object_uid = p.object_uid
and object_name like '%A3T1%';"""
        output = _dci.cmdexec(stmt)
       
    #A003.2a Table with hash partition (location, extent, maxextent specified)
    #$SQL_Complete_msg
    stmt = """create table a3t2a (
sbin6_nuniq  Largeint            no default,
double6_n2   Float(23),
sdec6_4      Decimal(4) signed   no default not null not droppable
primary key descending not droppable,
char6_n100          Character(8)        no default,
date6_100           Date                not null)
attributes extent (1024,512) ,maxextents 16;"""
    output = _dci.cmdexec(stmt)
    
    ##expectfile $test_dir/a003 a3s2aa
    if hpdci.tgtSQ():
        stmt = """select ap.partitioning_scheme, ap.partitioning_key_length,o.object_name
from
""" + gvars.definition_schema + """.objects o,
""" + gvars.definition_schema + """.access_paths ap
where ap.table_uid = o.object_uid and
o.object_name like '%A3T2A%';"""
        output = _dci.cmdexec(stmt)
    
    ##expectfile $test_dir/a003 a3s2ab
    if hpdci.tgtSQ():
        stmt = """select substring(object_name,1,10),  DATA_SOURCE,
pri_ext, sec_ext, max_ext from
""" + gvars.definition_schema + """.objects o,
""" + gvars.definition_schema + """.partitions p
where o.object_uid = p.object_uid
and object_name like '%A3T2%';"""
        output = _dci.cmdexec(stmt)
    
    #A003.2b Table with hash partition (location, extent, maxextent specified)
    #$SQL_Complete_msg
    stmt = """create table a3t2b (
sbin6_nuniq  Largeint            no default,
double6_n2   Float(23),
sdec6_4      Decimal(4) signed   no default not null not droppable
primary key descending not droppable,
char6_n100          Character(8)        no default,
date6_100           Date                not null)
location """ + gvars.g_disc7 + """
hash partition (
add location """ + gvars.g_disc5 + """ extent 0      maxextents 8,
add location """ + gvars.g_disc4 + """ extent (0,3)  maxextents 16
)
attributes extent (1024,512) ,maxextents 16;"""
    output = _dci.cmdexec(stmt)
    
    ##expectfile $test_dir/a003 a3s2ba
    if hpdci.tgtSQ():
        stmt = """select ap.partitioning_scheme, ap.partitioning_key_length,o.object_name
from
""" + gvars.definition_schema + """.objects o,
""" + gvars.definition_schema + """.access_paths ap
where ap.table_uid = o.object_uid and
o.object_name like '%A3T2%';"""
        output = _dci.cmdexec(stmt)
    
    ##expectfile $test_dir/a003 a3s2bb
    if hpdci.tgtSQ():
        stmt = """select substring(object_name,1,10),  DATA_SOURCE,
pri_ext, sec_ext, max_ext from
""" + gvars.definition_schema + """.objects o,
""" + gvars.definition_schema + """.partitions p
where o.object_uid = p.object_uid
and object_name like '%A3T2%';"""
        output = _dci.cmdexec(stmt)
    
    # Requires CAT_ERROR_ON_NOTNULL_STOREBY in order to avoid error
    #    for hash-partition without primary key
    
    stmt = """control query default CAT_ERROR_ON_NOTNULL_STOREBY 'off';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """Create table lu_shipper1 (shipper_id integer, shipper_desc varchar(51), contract_nbr integer);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into lu_shipper1 values (1, 'shipper', 2);"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    stmt = """select * from lu_shipper1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """1*shipper*2""")
    
    stmt = """Create table lu_shipper2 (shipper_id integer default null, shipper_desc varchar(51), contract_nbr integer);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into lu_shipper2(shipper_desc, contract_nbr) values ('shipper', 15);"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    stmt = """select * from lu_shipper2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """shipper*15""")
    
    stmt = """control query default CAT_ERROR_ON_NOTNULL_STOREBY 'on';"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test004(desc="""logical partition names"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #
    
    stmt = """set schema """ + defs.my_schema + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #A004.1 Create range partition table with partition name
    #showddl should show partition names
    stmt = """Create table a4t1 (
int_1        int   not null not droppable,
nchar_2      nchar (25) not null not droppable,
float_3      float (54)  not null not droppable,
date_4       date  not null not droppable,
interval_5   interval second (6) not null not droppable,
-- R2.5 NCI primary key (int_1, nchar_2, float_3, date_4, interval_5)
primary key (int_1, nchar_2, date_4, interval_5)
)
attribute
extent (1024, 1024),
maxextents 16;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showddl a4t1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #A004.2 Create hash partition table with parition name
    #showddl should show partition names
    #pic:s-signed,9(6)-(6)-# of digits for integer part,
    #v99-scale -# of digits right of the decimal
    #ex: 123456.22
    
    stmt = """create table a4t2 (
smallint_1 smallint     not null not droppable,
pic_2      pic xx       not null not droppable,
pic_3      pic s9(6)V99 not null not droppable,
double_precision_3  double precision not null,
time_4     time(6),
interval_5 interval year to month not null
)
-- R2.5 NCI store by (smallint_1, pic_2, double_precision_3, interval_5)
store by (smallint_1, pic_2, interval_5)
attribute
extent (1024, 1024),
maxextents 16;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showddl a4t2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #A004.3 Create range partition table with long partition name
    stmt = """Create table a4t3 (
int_1        int   not null not droppable,
nchar_2      nchar (25) not null not droppable,
float_3      float (54)  not null not droppable,
date_4       date  not null not droppable,
interval_5   interval second (6) not null not droppable,
-- primary key (int_1, nchar_2, float_3, date_4, interval_5)
primary key (int_1, nchar_2, date_4, interval_5)
)
attribute
extent (1024, 1024),
maxextents 16;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showddl a4t3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #A004.4 Create hash partition table with long partition name
    stmt = """create table a4t4 (
smallint_1 smallint     not null not droppable,
pic_2      pic xx       not null not droppable,
pic_3      pic s9(6)V99 not null not droppable,
double_precision_3  double precision not null,
time_4     time(6),
interval_5 interval year to month not null
)
-- R2.5 NCI store by (smallint_1, pic_2, double_precision_3, interval_5)
store by (smallint_1, pic_2, interval_5)
attribute
extent (1024, 512000),
maxextents 21;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showddl a4t4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #A004.6 Create hash partition table with delimited partition name
    stmt = """create table a4t6 (
smallint_1 smallint     not null not droppable,
pic_2      pic xx       not null not droppable,
pic_3      pic s9(6)V99 not null not droppable,
double_precision_3  double precision not null,
time_4     time(6),
interval_5 interval year to month not null
)
-- R2.5 NCI store by (smallint_1, pic_2, double_precision_3, interval_5)
store by (smallint_1, pic_2, interval_5)
attribute
extent (1024, 1024),
maxextents 16;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showddl a4t6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #A004.7  Create range partition table like
    stmt = """Create table a4t7a (
int_1        int   not null not droppable,
nchar_2      nchar (25) not null not droppable,
float_3      float (54)  not null not droppable,
date_4       date  not null not droppable,
interval_5   interval second (6) not null not droppable,
-- primary key (int_1, nchar_2, float_3, date_4, interval_5)
primary key (int_1, nchar_2, date_4, interval_5)
)
attribute
extent (1024, 1024),
maxextents 16;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table a4t7b like a4t7a
with partitions;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showddl a4t7b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #A004.8 create hash partition table like
    stmt = """create table a4t8a (
smallint_1 smallint     not null not droppable,
pic_2      pic xx       not null not droppable,
pic_3      pic s9(6)V99 not null not droppable,
double_precision_3  double precision not null,
time_4     time(6),
interval_5 interval year to month not null
)
-- R2.5 NCI store by (smallint_1, pic_2, double_precision_3, interval_5)
store by (smallint_1, pic_2, interval_5)
attribute
extent (1024, 1024),
maxextents 16;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table a4t8b like a4t8a
with partitions;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showddl a4t8b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #A004.9 Create range partition table with partition name, large extents, maxextents
    #showddl should show partition names
    stmt = """Create table a4t9 (
int_1        int   not null not droppable,
nchar_2      nchar (25) not null not droppable,
float_3      float (54)  not null not droppable,
date_4       date  not null not droppable,
interval_5   interval second (6) not null not droppable,
primary key (int_1, nchar_2, date_4, interval_5)
)
attribute
extent (1024, 1024),
maxextents 16;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showddl a4t9;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #A004.10 Create hash partition table with parition name, large extents, maxextents
    #showddl should show partition names
    #pic:s-signed,9(6)-(6)-# of digits for integer part,
    #v99-scale -# of digits right of the decimal
    #ex: 123456.22
    
    stmt = """create table a4t10 (
smallint_1 smallint     not null not droppable,
pic_2      pic xx       not null not droppable,
pic_3      pic s9(6)V99 not null not droppable,
double_precision_3  double precision not null,
time_4     time(6),
interval_5 interval year to month not null
)
-- R2.5 NCI store by (smallint_1, pic_2, double_precision_3, interval_5)
store by (smallint_1, pic_2, interval_5)
attribute
extent (1024, 1024),
maxextents 16;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showddl a4t10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #A004.11 Create range partition table with partition name, extents, maxextents
    #showddl should show partition names
    stmt = """Create table a4t11 (
int_1        int   not null not droppable,
nchar_2      nchar (25) not null not droppable,
float_3      float (54)  not null not droppable,
date_4       date  not null not droppable,
interval_5   interval second (6) not null not droppable,
primary key (int_1, nchar_2, date_4, interval_5)
)
attribute
extent (1024, 1024),
maxextents 16;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showddl a4t11;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #A004.12 Create hash partition table with parition name, extents, maxextents
    #showddl should show partition names
    #pic:s-signed,9(6)-(6)-# of digits for integer part,
    #v99-scale -# of digits right of the decimal
    #ex: 123456.22
    
    stmt = """create table a4t12 (
smallint_1 smallint     not null not droppable,
pic_2      pic xx       not null not droppable,
pic_3      pic s9(6)V99 not null not droppable,
double_precision_3  double precision not null,
time_4     time(6),
interval_5 interval year to month not null
)
-- R2.5 NCI store by (smallint_1, pic_2, double_precision_3, interval_5)
store by (smallint_1, pic_2, interval_5)
attribute
extent (1024, 1024),
maxextents 16;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showddl a4t12;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test005(desc="""Negative hash partition test"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """set schema """ + defs.my_schema + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #N003.1 Create hash partitioned table with large extent values
    # R2.5 NCI #expect any *ERROR[1115]*
    stmt = """create table n3t1 (
sbin6_nuniq  Largeint            no default,
double6_n2   Float(23),
sdec6_4      Decimal(4) signed   no default not null not droppable
primary key descending not droppable,
char6_n100          Character(8)        no default,
date6_100           Date                not null)
attributes extent (1024,512) ,maxextents 16;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #N003.2 Create hash partitioned table with large maxextents values
    # R2.5 NCI #expect any *ERROR[3191]*
    stmt = """create table N3t2 (
sbin6_nuniq  Largeint            no default,
double6_n2   Float(23),
sdec6_4      Decimal(4) signed   no default not null not droppable
primary key descending not droppable,
char6_n100          Character(8)        no default,
date6_100           Date                not null)
location """ + gvars.g_disc7 + """
attributes extent (1024,512) ,maxextents 16;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #N003.3 Create table with partition overlay where all location specified
    #doesn't exist
    
    #N003.4 Create table with some locations specified, some nonexisting volume
    
    #N003.5 Create table with partition overaly with large number of
    #partitions specified
    
    #N003.6
    stmt = """create table n3t6 (
sbin6_nuniq  Largeint            no default,
double6_n2   Float(23),
sdec6_4      Decimal(4) signed   no default not null not droppable
primary key descending not droppable,
char6_n100          Character(8)        no default,
date6_100           Date                not null)
store by primary key;"""
    _dci.expect_complete_msg(output)
    
    #N003.7 Create hash partitioned table with non-numeric maxextents values
    stmt = """create table N3t7 (
sbin6_nuniq  Largeint            no default,
double6_n2   Float(23),
sdec6_4      Decimal(4) signed   no default not null not droppable
primary key descending not droppable,
char6_n100          Character(8)        no default,
date6_100           Date                not null)
location """ + gvars.g_disc7 + """
hash partition (
add location """ + gvars.g_disc5 + """ extent 512         maxextents lm,
add location """ + gvars.g_disc4 + """ extent (1024,512)  maxextents 960
)
attributes extent (1024,512) ,maxextents 16;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    _testmgr.testcase_end(desc)

def test006(desc="""Negative logical partition names"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """set schema """ + defs.my_schema + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #N004.1 Create hash partition table with duplicate partition name
    stmt = """create table n4t1 (
smallint_1 smallint     not null not droppable,
pic_2      pic xx       not null not droppable,
pic_3      pic s9(6)V99 not null not droppable,
double_precision_3  double precision not null,
time_4     time(6),
interval_5 interval year to month not null
)
store by (smallint_1, pic_2, double_precision_3, interval_5)
-- hash partition by (smallint_1)
-- (add location """ + gvars.g_disc4 + """ NAME partition1,
-- add location """ + gvars.g_disc5 + """ NAME partition1)
-- attribute
-- extent (1024, 1024),
-- maxextents 16
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #N004.2 create range partition table with duplicate partition name
    stmt = """Create table N4t2 (
int_1        int   not null not droppable,
nchar_2      nchar (25) not null not droppable,
float_3      float (54)  not null not droppable,
date_4       date  not null not droppable,
interval_5   interval second (6) not null not droppable,
primary key (int_1, nchar_2, float_3, date_4, interval_5)
)
-- range partition by (int_1)
-- (add first key 2   location """ + gvars.g_disc4 + """ NAME partition_1,
-- add first key 512 location """ + gvars.g_disc5 + """ NAME partition_1)
-- attribute
-- extent (1024, 1024),
-- maxextents 16
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #N004.3 Create hash partition table with reserve word partition name
    stmt = """create table n4t3 (
smallint_1 smallint     not null not droppable,
pic_2      pic xx       not null not droppable,
pic_3      pic s9(6)V99 not null not droppable,
double_precision_3  double precision not null,
time_4     time(6),
interval_5 interval year to month not null
)
store by (smallint_1, pic_2, double_precision_3, interval_5)
-- hash partition by (smallint_1)
-- (add location """ + gvars.g_disc4 + """ NAME sql,
-- add location """ + gvars.g_disc5 + """ NAME join)
-- attribute
-- extent (1024, 1024),
-- maxextents 16
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #N004.4 create range partition table with reserve word partition name
    stmt = """Create table n4t4 (
int_1        int   not null not droppable,
nchar_2      nchar (25) not null not droppable,
float_3      float (54)  not null not droppable,
date_4       date  not null not droppable,
interval_5   interval second (6) not null not droppable,
primary key (int_1, nchar_2, float_3, date_4, interval_5)
)
-- range partition by (int_1)
-- (add first key 2   location """ + gvars.g_disc4 + """ NAME sql,
-- add first key 512 location """ + gvars.g_disc5 + """ NAME join)
-- attribute
-- extent (1024, 1024),
-- maxextents 16
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #N004.5 Create hash partition table with long partition name ( > 128 char )
    stmt = """create table n4t5 (
smallint_1 smallint     not null not droppable,
pic_2      pic xx       not null not droppable,
pic_3      pic s9(6)V99 not null not droppable,
double_precision_3  double precision not null,
time_4     time(6),
interval_5 interval year to month not null
)
store by (smallint_1, pic_2, double_precision_3, interval_5)
-- hash partition by (smallint_1)
-- (add location """ + gvars.g_disc4 + """ NAME
-- partition1a123456789b123456789c123456789d123456789e123456789f123456789g123456789h123456789i123456789j123456789k12345678,
-- add location """ + gvars.g_disc5 + """ NAME
-- partition2a123456789b123456789c123456789d123456789e123456789f123456789g123456789h123456789i123456789j123456789k123456789m123456789i)
-- attribute
-- extent (1024, 512000),
-- maxextents 21
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #N004.6 create range partition tale with long partition name ( > 128 char )
    stmt = """Create table n4t6 (
int_1        int   not null not droppable,
nchar_2      nchar (25) not null not droppable,
float_3      float (54)  not null not droppable,
date_4       date  not null not droppable,
interval_5   interval second (6) not null not droppable,
primary key (int_1, nchar_2, float_3, date_4, interval_5)
)
-- range partition by (int_1)
-- (add first key 2   location """ + gvars.g_disc4 + """ NAME
-- partition1a123456789b123456789c123456789d123456789e123456789f123456789g123456789h123456789i123456789j123456789k12345678,
-- add first key 512 location """ + gvars.g_disc5 + """ NAME
-- partition2a123456789b123456789c123456789d123456789e123456789f123456789g123456789h123456789i123456789j123456789k123456789l12345678)
-- attribute
-- extent (1024, 1024),
-- maxextents 16
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test007(desc="""hash partition ==partition overlay"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """set schema """ + defs.my_schema + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #sh info_define all;
    #sh gtacl -c 'env';
    
    ##sh export vol1=`info_define all| grep "VOLUME"| awk ' { print $3} '`
    
    ##sh defvol=${vol1%.*}
    ##sh echo $defvol
    
    #a006.1 Table with hash partition (location, extent, maxextent specified)
    
    stmt = """control query default POS 'LOCAL_NODE';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """control query default POS_NUM_OF_PARTNS '10';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table a6t1 (
sbin6_nuniq  Largeint            no default,
double6_n2   Float(23),
sdec6_4      Decimal(4) signed   no default not null not droppable
primary key descending not droppable,
char6_n100          Character(8)        no default,
date6_100           Date                not null)    

location """ + gvars.g_disc4 + """
attributes extent (1024,512) ,maxextents 16;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showddl a6t1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    if hpdci.tgtSQ(): 
        stmt = """select substring(object_name,1,10), DATA_SOURCE,
pri_ext, sec_ext, max_ext from
""" + gvars.definition_schema + """.objects o,
""" + gvars.definition_schema + """.partitions p
where o.object_uid = p.object_uid
and object_name like '%A6T1%';"""
        output = _dci.cmdexec(stmt)
        _dci.expect_selected_msg(output)
    
    stmt = """showlabel a6t1, detail;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #a006.2 Table with hash partition (location, extent, maxextent specified)
    
    stmt = """control query default POS 'LOCAL_NODE';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """control query default POS_NUM_OF_PARTNS '10';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table A6T2 (
sbin6_nuniq  Largeint            no default,
double6_n2   Float(23),
sdec6_4      Decimal(4) signed   no default not null not droppable
primary key descending not droppable,
char6_n100          Character(8)        no default,
date6_100           Date                not null)
location """ + gvars.g_disc7 + """
attributes extent (512000000,5) ,maxextents 16;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showddl a6t2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    if hpdci.tgtSQ(): 
        stmt = """select substring(object_name,1,10), DATA_SOURCE,
pri_ext, sec_ext, max_ext from
""" + gvars.definition_schema + """.objects o,
""" + gvars.definition_schema + """.partitions p
where o.object_uid = p.object_uid
and object_name like '%A6T2%';"""
        output = _dci.cmdexec(stmt)
        _dci.expect_selected_msg(output)
    
    stmt = """showlabel a6t2, detail;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #a006.3 hash partition table using partition overlay,
    #locations specified, single column pk
    
    stmt = """control query default POS 'LOCAL_NODE';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """control query default POS_NUM_OF_PARTNS '4';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """control query default POS_LOCATIONS '""" + gvars.g_disc7 + """,""" + gvars.g_disc5 + """,""" + gvars.g_disc4 + """';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table A6T3 (
sbin6_nuniq  Largeint            no default,
double6_n2   Float(23),
sdec6_4      Decimal(4) signed   no default not null not droppable
primary key descending not droppable,
char6_n100          Character(8)        no default,
date6_100           Date                not null)
attributes extent (1024,512) ,
maxextents 16,
allocate 10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showddl a6t3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    if hpdci.tgtSQ(): 
        stmt = """select substring(object_name,1,10),DATA_SOURCE,
pri_ext, sec_ext, max_ext from
""" + gvars.definition_schema + """.objects o,
""" + gvars.definition_schema + """.partitions p
where o.object_uid = p.object_uid
and object_name like '%A6T3%';"""
        output = _dci.cmdexec(stmt)
        _dci.expect_selected_msg(output)
    
    stmt = """showlabel a6t3, detail;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #a006.4 hash partition table using partition overlay,
    #locations specified, multicolumn pk
    
    stmt = """control query default POS 'LOCAL_NODE';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """control query default POS_NUM_OF_PARTNS '4';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """control query default POS_LOCATIONS '""" + gvars.g_disc7 + """,""" + gvars.g_disc5 + """,""" + gvars.g_disc4 + """';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table A6T4 (
pic_char_1   pic x display upshift not null,
numeric_2    numeric (9,5) unsigned not null,
dec_3        dec(5,3) unsigned not null,
int_4        int not null ,
timestamp_5  timestamp(6) not null ,
int_6        Largeint,
primary key (dec_3,int_4,timestamp_5) not droppable)
attributes extent (16,512000) ,maxextents 1, allocate 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showddl A6T4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    if hpdci.tgtSQ(): 
        stmt = """select substring(object_name,1,10),  DATA_SOURCE,
pri_ext, sec_ext, max_ext from
""" + gvars.definition_schema + """.objects o,
""" + gvars.definition_schema + """.partitions p
where o.object_uid = p.object_uid
and object_name like '%A6T4%';"""
        output = _dci.cmdexec(stmt)
        _dci.expect_selected_msg(output)
    
    stmt = """showlabel a6t4, detail;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #a006.5 hash partition table using partition overlay,
    #locations specified, no pk, store by single column
    
    stmt = """control query default POS 'LOCAL_NODE';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """control query default POS_NUM_OF_PARTNS '20';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """control query default POS_LOCATIONS '""" + gvars.g_disc7 + """, """ + gvars.g_disc5 + """, """ + gvars.g_disc4 + """';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table A6T5 (
sbin6_nuniq  Largeint            no default,
double6_n2   Float(23),
sdec6_4      Decimal(4) signed   no default not null not droppable,
char6_n100   Character(8)        no default,
date6_100    Date                not null)
store by  (sdec6_4)
location """ + gvars.g_disc6 + """
attributes
extent (2,4) ,
maxextents 768,
blocksize 4096,
allocate 768;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showddl A6T5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    if hpdci.tgtSQ(): 
        stmt = """select substring(object_name,1,10), DATA_SOURCE,
pri_ext, sec_ext, max_ext from
""" + gvars.definition_schema + """.objects o,
""" + gvars.definition_schema + """.partitions p
where o.object_uid = p.object_uid
and object_name like '%A6T5%';"""
        output = _dci.cmdexec(stmt)
        _dci.expect_selected_msg(output)
    
    stmt = """showlabel a6t5, detail;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #a006.6 hash partition table using partition overlay,
    #locations specified, no pk, store by multicolumn
    
    stmt = """control query default POS 'LOCAL_NODE';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """control query default POS_NUM_OF_PARTNS '15';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """control query default POS_LOCATIONS '""" + gvars.g_disc7 + """,""" + gvars.g_disc5 + """,""" + gvars.g_disc4 + """';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table A6T6 (
pic_char_1   pic x display upshift not null,
numeric_2    numeric (9,5) unsigned not null,
dec_3        dec(5,3) unsigned not null not droppable,
float_4      float(11) not null not droppable,
timestamp_5  timestamp(6) not null not droppable,
int_6        Largeint)
store by (dec_3,timestamp_5)
attributes extent (1024,512) ,maxextents 16;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showddl A6T6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    if hpdci.tgtSQ(): 
        stmt = """select substring(object_name,1,10), DATA_SOURCE,
pri_ext, sec_ext, max_ext from
""" + gvars.definition_schema + """.objects o,
""" + gvars.definition_schema + """.partitions p
where o.object_uid = p.object_uid
and object_name like '%A6T6%';"""
        output = _dci.cmdexec(stmt)
        _dci.expect_selected_msg(output)
    
    stmt = """showlabel a6t6, detail;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #a006.7 hash partition table using partition overlay,
    #some locations specified, single column pk
    
    stmt = """control query default POS 'LOCAL_NODE';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """control query default POS_NUM_OF_PARTNS '8';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """control query default POS_LOCATIONS '""" + gvars.g_disc7 + """,""" + gvars.g_disc5 + """';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table A6T7 (
sbin6_nuniq  Largeint            no default,
double6_n2   Float(23),
sdec6_4      Decimal(4) signed   no default not null not droppable
primary key descending not droppable,
char6_n100   Character(8)        no default,
date6_100    Date                not null)
attributes extent (1024,512) ,maxextents 16;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showddl A6T7;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    if hpdci.tgtSQ(): 
        stmt = """select substring(object_name,1,10), DATA_SOURCE,
pri_ext, sec_ext, max_ext from
""" + gvars.definition_schema + """.objects o,
""" + gvars.definition_schema + """.partitions p
where o.object_uid = p.object_uid
and object_name like '%A6T7%';"""
        output = _dci.cmdexec(stmt)
        _dci.expect_selected_msg(output)
    
    stmt = """showlabel a6t7, detail;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #a006.8 hash partition table using partition overlay,
    #some locations specified, multicolumn pk
    
    stmt = """control query default POS 'LOCAL_NODE';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """control query default POS_NUM_OF_PARTNS '40';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """control query default POS_LOCATIONS '""" + gvars.g_disc7 + """,""" + gvars.g_disc5 + """';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table A6T8 (
pic_char_1   pic x display upshift not null,
numeric_2    numeric (9,5) unsigned not null,
dec_3        dec(5,3) unsigned not null,
int_4        float(11) not null ,
timestamp_5  timestamp(6) not null ,
int_6        Largeint,
primary key (dec_3,timestamp_5) not droppable)
attributes extent (16,16) ,maxextents 4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showddl A6T8;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    if hpdci.tgtSQ(): 
        stmt = """select substring(object_name,1,10), DATA_SOURCE,
pri_ext, sec_ext, max_ext from
""" + gvars.definition_schema + """.objects o,
""" + gvars.definition_schema + """.partitions p
where o.object_uid = p.object_uid
and object_name like '%A6T8%';"""
        output = _dci.cmdexec(stmt)
        _dci.expect_selected_msg(output)
    
    stmt = """showlabel a6t8, detail;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #a006.9 hash partition table using partition overlay,
    #some locations specified, no pk store by single column
    
    stmt = """control query default POS 'LOCAL_NODE';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """control query default POS_NUM_OF_PARTNS '5';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """control query default POS_LOCATIONS '""" + gvars.g_disc7 + """,""" + gvars.g_disc5 + """';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table A6T9 (
sbin6_nuniq  Largeint            no default,
double6_n2   Float(23),
sdec6_4      Decimal(4) signed   no default not null not droppable,
char6_n100   Character(8)        no default,
date6_100    Date                not null)
store by  (sdec6_4)
attributes extent (1024,512) ,maxextents 16;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showddl A6T9;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    if hpdci.tgtSQ(): 
        stmt = """select substring(object_name,1,10), DATA_SOURCE,
pri_ext, sec_ext, max_ext from
""" + gvars.definition_schema + """.objects o,
""" + gvars.definition_schema + """.partitions p
where o.object_uid = p.object_uid
and object_name like '%A6T9%';"""
        output = _dci.cmdexec(stmt)
        _dci.expect_selected_msg(output)
    
    stmt = """showlabel a6t9, detail;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #a006.10 hash partition table using partition overlay,
    #some locations specified, no pk store by multicolumn
    
    stmt = """control query default POS 'LOCAL_NODE';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """control query default POS_NUM_OF_PARTNS '5';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """control query default POS_LOCATIONS '""" + gvars.g_disc7 + """,""" + gvars.g_disc5 + """';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table A6T10 (
pic_char_1   pic x display upshift not null,
numeric_2    numeric (9,5) unsigned not null,
dec_3        dec(5,3) unsigned not null not droppable,
float_4      float(11) not null not droppable,
timestamp_5  timestamp(6) not null not droppable,
int_6        Largeint)
store by (dec_3,timestamp_5)
attributes extent (1024,512) ,maxextents 16;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showddl A6T10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    if hpdci.tgtSQ(): 
        stmt = """select substring(object_name,1,10), DATA_SOURCE,
pri_ext, sec_ext, max_ext from
""" + gvars.definition_schema + """.objects o,
""" + gvars.definition_schema + """.partitions p
where o.object_uid = p.object_uid
and object_name like '%A6T10%';"""
        output = _dci.cmdexec(stmt)
        _dci.expect_selected_msg(output)
    
    stmt = """showlabel a6t10, detail;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #a006.11 hash partition table using partition overlay,
    #no locations specified single column pk
    
    stmt = """control query default POS 'LOCAL_NODE';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """control query default POS_NUM_OF_PARTNS '5';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """control query default POS_LOCATIONS '';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table A6T11 (
sbin6_nuniq  Largeint            no default,
double6_n2   Float(23),
sdec6_4      Decimal(4) signed   no default not null not droppable
primary key descending not droppable,
char6_n100   Character(8)        no default,
date6_100    Date                not null)
location """ + gvars.g_disc4 + """
attributes extent (1024,512) ,maxextents 42;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showddl A6T11;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    if hpdci.tgtSQ(): 
        stmt = """select substring(object_name,1,10), DATA_SOURCE,
pri_ext, sec_ext, max_ext from
""" + gvars.definition_schema + """.objects o,
""" + gvars.definition_schema + """.partitions p
where o.object_uid = p.object_uid
and object_name like '%A6T11%';"""
        output = _dci.cmdexec(stmt)
        _dci.expect_selected_msg(output)
    
    stmt = """showlabel a6t11, detail;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #a006.12 hash partition table using partition overlay,
    #no locations specified multicolumn pk
    
    stmt = """control query default POS 'LOCAL_NODE';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """control query default POS_NUM_OF_PARTNS '5';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """control query default POS_LOCATIONS '';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table A6T12 (
pic_char_1   pic x display upshift not null,
numeric_2    numeric (9,5) unsigned not null,
dec_3        dec(5,3) unsigned not null,
float_4      float(11) not null ,
timestamp_5  timestamp(6) not null ,
int_6        Largeint,
primary key (dec_3,timestamp_5) not droppable)
location """ + gvars.g_disc6 + """
attributes extent (1024,512) ,maxextents 16;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showddl A6T12;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    if hpdci.tgtSQ(): 
        stmt = """select substring(object_name,1,10), DATA_SOURCE,
pri_ext, sec_ext, max_ext from
""" + gvars.definition_schema + """.objects o,
""" + gvars.definition_schema + """.partitions p
where o.object_uid = p.object_uid
and object_name like '%A6T12%';"""
        output = _dci.cmdexec(stmt)
        _dci.expect_selected_msg(output)
    
    stmt = """showlabel a6t12, detail;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #a006.13 hash partition table using partition overlay,
    #no locations specified no pk, store by single column
    
    stmt = """control query default POS 'LOCAL_NODE';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """control query default POS_NUM_OF_PARTNS '8';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """control query default POS_LOCATIONS '';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table A6T13 (
sbin6_nuniq  Largeint            no default,
double6_n2   Float(23),
sdec6_4      Decimal(4) signed   no default not null not droppable,
char6_n100   Character(8)        no default,
date6_100    Date                not null)
store by  (sdec6_4)
attributes extent (512000000,2) ,maxextents 4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showddl A6T13;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    if hpdci.tgtSQ(): 
        stmt = """select substring(object_name,1,10),  DATA_SOURCE,
pri_ext, sec_ext, max_ext from
""" + gvars.definition_schema + """.objects o,
""" + gvars.definition_schema + """.partitions p
where o.object_uid = p.object_uid
and object_name like '%A6T13%';"""
        output = _dci.cmdexec(stmt)
        _dci.expect_selected_msg(output)
    
    stmt = """showlabel a6t13, detail;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #a006.14 hash partition table using partition overlay,
    #no locations specified no pk, store by multicolumn
    
    stmt = """control query default POS 'LOCAL_NODE';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """control query default POS_NUM_OF_PARTNS '12';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """control query default POS_LOCATIONS '';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table A6T14 (
pic_char_1   pic x display upshift not null,
numeric_2    numeric (9,5) unsigned not null,
dec_3        dec(5,3) unsigned not null not droppable,
float_4      float(11) not null not droppable,
timestamp_5  timestamp(6) not null not droppable,
int_6        Largeint)
store by (dec_3,timestamp_5)
location """ + gvars.g_disc12 + """
attributes extent (4,512000000) ,maxextents 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showddl A6T14;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    if hpdci.tgtSQ(): 
        stmt = """select substring(object_name,1,10), DATA_SOURCE,
pri_ext, sec_ext, max_ext from
""" + gvars.definition_schema + """.objects o,
""" + gvars.definition_schema + """.partitions p
where o.object_uid = p.object_uid
and object_name like '%A6T14%';"""
        output = _dci.cmdexec(stmt)
        _dci.expect_selected_msg(output)
    
    stmt = """showlabel a6t14, detail;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # a006.15 hash partition table using partition overlay,
    # remote locations single column pk
    
    stmt = """control query default POS 'MULTI_NODE';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """control query default POS_NUM_OF_PARTNS '3';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """control query default POS_LOCATIONS '""" + gvars.g_disc1 + """,""" + gvars.g_disc2 + """,""" + gvars.g_disc3 + """';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table A6T15 (
sbin6_nuniq  Largeint            no default,
double6_n2   Float(23),
sdec6_4      Decimal(4) signed   no default not null not droppable
primary key descending not droppable,
char6_n100   Character(8)        no default,
date6_100    Date                not null)
attributes extent (1024,512) ,maxextents 16;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showddl A6T15;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    if hpdci.tgtSQ(): 
        stmt = """select substring(object_name,1,10), DATA_SOURCE,
pri_ext, sec_ext, max_ext from
""" + gvars.definition_schema + """.objects o,
""" + gvars.definition_schema + """.partitions p
where o.object_uid = p.object_uid
and object_name like '%A6T15%';"""
        output = _dci.cmdexec(stmt)
        _dci.expect_selected_msg(output)
    
    stmt = """showlabel a6t15, detail;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # a006.16 hash partition table using partition overlay,
    # remote locations multicolumn pk
    
    stmt = """control query default POS 'MULTI_NODE';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """control query default POS_NUM_OF_PARTNS '4';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """control query default POS_LOCATIONS '""" + gvars.g_disc1 + """,""" + gvars.g_disc2 + """,""" + gvars.g_disc3 + """,""" + gvars.g_disc4 + """';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table A6T16 (
pic_char_1   pic x display upshift not null,
numeric_2    numeric (9,5) unsigned not null,
dec_3        dec(5,3) unsigned not null,
float_4      float(11) not null ,
timestamp_5  timestamp(6) not null ,
int_6        Largeint,
primary key (dec_3,timestamp_5) not droppable)
attributes extent (64,512000) ,maxextents 16;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showddl A6T16;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    if hpdci.tgtSQ(): 
        stmt = """select substring(object_name,1,10),  DATA_SOURCE,
pri_ext, sec_ext, max_ext from
""" + gvars.definition_schema + """.objects o,
""" + gvars.definition_schema + """.partitions p
where o.object_uid = p.object_uid
and object_name like '%A6T16%';"""
        output = _dci.cmdexec(stmt)
        _dci.expect_selected_msg(output)
    
    stmt = """showlabel a6t16, detail;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #a006.17 hash partition table using partition overlay,
    #remote locations no pk, store by single column
    
    stmt = """control query default POS 'MULTI_NODE';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """control query default POS_NUM_OF_PARTNS '3';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """control query default POS_LOCATIONS '""" + gvars.g_disc1 + """,""" + gvars.g_disc2 + """,""" + gvars.g_disc3 + """';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table A6T17 (
sbin6_nuniq  Largeint            no default,
double6_n2   Float(23),
sdec6_4      Decimal(4) signed   no default not null not droppable,
char6_n100   Character(8)        no default,
date6_100    Date                not null)
store by  (sdec6_4)
attributes extent (1024,64) ,maxextents 16;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showddl A6T17;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    if hpdci.tgtSQ(): 
        stmt = """select substring(object_name,1,10), DATA_SOURCE,
pri_ext, sec_ext, max_ext from
""" + gvars.definition_schema + """.objects o,
""" + gvars.definition_schema + """.partitions p
where o.object_uid = p.object_uid
and object_name like '%A6T17%';"""
        output = _dci.cmdexec(stmt)
        _dci.expect_selected_msg(output)
    
    stmt = """showlabel a6t17, detail;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # a006.18 hash partition table using partition overlay,
    # remote locations no pk, store by multicolumn
    
    stmt = """control query default POS 'MULTI_NODE';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """control query default POS_NUM_OF_PARTNS '8';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """control query default POS_LOCATIONS '""" + gvars.g_disc1 + """,""" + gvars.g_disc2 + """,""" + gvars.g_disc3 + """,""" + gvars.g_disc4 + """,""" + gvars.g_disc5 + """,""" + gvars.g_disc6 + """,""" + gvars.g_disc7 + """,""" + gvars.g_disc8 + """';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table A6T18 (
pic_char_1   pic x display upshift not null,
numeric_2    numeric (9,5) unsigned not null,
dec_3        dec(5,3) unsigned not null not droppable,
float_4      float(11) not null not droppable,
timestamp_5  timestamp(6) not null not droppable,
int_6        Largeint)
store by (dec_3,timestamp_5)
attributes extent (1024,512) ,maxextents 16;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    ##expect any *LOCATION $g_disc1*
    ##expect any *LOCATION $g_disc2*
    ##expect any *LOCATION $g_disc3*
    ##expect any *LOCATION $g_disc4*
    ##expect any *LOCATION $g_disc5*
    ##expect any *LOCATION $g_disc6*
    ##expect any *LOCATION $g_disc7*
    ##expect any *LOCATION $g_disc8*
    
    stmt = """showddl A6T18;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    if hpdci.tgtSQ(): 
        stmt = """select substring(object_name,1,10),  DATA_SOURCE,
pri_ext, sec_ext, max_ext from
""" + gvars.definition_schema + """.objects o,
""" + gvars.definition_schema + """.partitions p
where o.object_uid = p.object_uid
and object_name like '%A6T18%';"""
        output = _dci.cmdexec(stmt)
        _dci.expect_selected_msg(output)
    
    stmt = """showlabel a6t18, detail;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #a006.19 turn off partition overlay with '1'
    
    stmt = """control query default POS 'LOCAL_NODE';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """control query default POS_NUM_OF_PARTNS '5';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """control query default POS_NUM_OF_PARTNS '1';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table A6T19 (
sbin6_nuniq  Largeint            no default,
double6_n2   Float(23),
sdec6_4      Decimal(4) signed   no default not null not droppable
primary key descending not droppable,
char6_n100   Character(8)        no default,
date6_100    Date                not null)
attributes extent (1024,512) ,maxextents 16;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showddl A6T19;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    if hpdci.tgtSQ(): 
        stmt = """select substring(object_name,1,10),  DATA_SOURCE,
pri_ext, sec_ext, max_ext from
""" + gvars.definition_schema + """.objects o,
""" + gvars.definition_schema + """.partitions p
where o.object_uid = p.object_uid
and object_name like '%A6T19%';"""
        output = _dci.cmdexec(stmt)
        _dci.expect_selected_msg(output)
    
    stmt = """showlabel a6t19, detail;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #a006.20 turn off partition overlay with '0'
    
    stmt = """control query default POS 'LOCAL_NODE';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """control query default POS_NUM_OF_PARTNS '5';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """control query default POS_NUM_OF_PARTNS '0';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table A6T20 (
sbin6_nuniq  Largeint            no default,
double6_n2   Float(23),
sdec6_4      Decimal(4) signed   no default not null not droppable
primary key descending not droppable,
char6_n100   Character(8)        no default,
date6_100    Date                not null)
attributes extent (1024,512) ,maxextents 16;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showddl A6T20;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    if hpdci.tgtSQ(): 
        stmt = """select substring(object_name,1,10),  DATA_SOURCE,
pri_ext, sec_ext, max_ext from
""" + gvars.definition_schema + """.objects o,
""" + gvars.definition_schema + """.partitions p
where o.object_uid = p.object_uid
and object_name like '%A6T20%';"""
        output = _dci.cmdexec(stmt)
        _dci.expect_selected_msg(output)
    
    stmt = """showlabel a6t20, detail;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #a006.21 turn off partition overlay with '-1'
    
    stmt = """control query default POS 'LOCAL_NODE';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """control query default POS_NUM_OF_PARTNS '5';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """control query default POS_NUM_OF_PARTNS '0';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """control query default POS_NUM_OF_PARTNS '-1';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '2055')
    
    stmt = """control query default POS_NUM_OF_PARTNS '1';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table A6T21 (
sbin6_nuniq  Largeint            no default,
double6_n2   Float(23),
sdec6_4      Decimal(4) signed   no default not null not droppable
primary key descending not droppable,
char6_n100   Character(8)        no default,
date6_100    Date                not null)
attributes extent (1024,512) ,maxextents 16;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showddl A6T21;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    if hpdci.tgtSQ(): 
        stmt = """select substring(object_name,1,10),  DATA_SOURCE,
pri_ext, sec_ext, max_ext from
""" + gvars.definition_schema + """.objects o,
""" + gvars.definition_schema + """.partitions p
where o.object_uid = p.object_uid
and object_name like '%A6T21%';"""
        output = _dci.cmdexec(stmt)
        _dci.expect_selected_msg(output)
    
    stmt = """showlabel a6t21, detail;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #a006.22 create table with no primary key and no store by
    #should create a non-paritioned table
    
    stmt = """control query default POS 'LOCAL_NODE';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """control query default POS_NUM_OF_PARTNS '4';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """control query default POS_LOCATIONS '';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """control query default POS 'OFF';"""
    output = _dci.cmdexec(stmt)
    stmt = """create table A6T22 (
sbin6_nuniq  Largeint            no default,
double6_n2   Float(23),
sdec6_4      Decimal(4) signed   no default not null not droppable,
char6_n100          Character(8)        no default,
date6_100           Date                not null)
attributes extent (1024,512) ,maxextents 16;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showddl A6T22;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    if hpdci.tgtSQ(): 
        stmt = """select substring(object_name,1,10),  DATA_SOURCE,
pri_ext, sec_ext, max_ext from
""" + gvars.definition_schema + """.objects o,
""" + gvars.definition_schema + """.partitions p
where o.object_uid = p.object_uid
and object_name like '%A6T22%';"""
        output = _dci.cmdexec(stmt)
        _dci.expect_selected_msg(output)
    
    stmt = """showlabel a6t22, detail;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #a006.23 hash partition by droppable primary key
    #should create a non-paritioned table ( I think)
    
    stmt = """control query default POS 'LOCAL_NODE';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """control query default POS_NUM_OF_PARTNS '4';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """control query default POS_LOCATIONS '';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """control query default POS 'OFF';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table A6T23 (
sdec4_n20           Decimal(4) not null,
int4_yTOm_uniq      Interval year(5) to month not null,
sbin4_n1000         Smallint not null,
time4_1000          Time no default not null,
vchar4_n10          varchar(20), -- default current_user,
real4_2000          Real                       not null,
primary key (sbin4_n1000 desc, time4_1000 descending) not droppable)
store by primary key;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # R2.5 NCI #expectfile $test_dir/a006 a6s23a
    stmt = """showddl A6T23;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    if hpdci.tgtSQ(): 
        stmt = """select substring(object_name,1,10), DATA_SOURCE,
pri_ext, sec_ext, max_ext from
""" + gvars.definition_schema + """.objects o,
""" + gvars.definition_schema + """.partitions p
where o.object_uid = p.object_uid
and object_name like '%A6T23%';"""
        output = _dci.cmdexec(stmt)
        _dci.expect_selected_msg(output)
    
    stmt = """showlabel a6t23, detail;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #a006.24 create table with no primary key, no store by
    #and a unique column
    
    stmt = """control query default POS 'LOCAL_NODE';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """control query default POS_NUM_OF_PARTNS '4';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """control query default POS_LOCATIONS '';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table A6T24 (
sbin6_nuniq  Largeint            no default,
double6_n2   Float(23),
sdec6_4      Decimal(4) signed   no default not null not droppable,
char6_n100   Character(8)        no default,
date6_100    Date                not null,
unique (sdec6_4))
store by (sdec6_4)
attributes extent (1024,512) ,maxextents 32
allocate 32;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showddl A6T24;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    if hpdci.tgtSQ(): 
        stmt = """select substring(object_name,1,10), DATA_SOURCE,
pri_ext, sec_ext, max_ext from
""" + gvars.definition_schema + """.objects o,
""" + gvars.definition_schema + """.partitions p
where o.object_uid = p.object_uid
and object_name like '%A6T24%';"""
        output = _dci.cmdexec(stmt)
        _dci.expect_selected_msg(output)
    
    stmt = """showlabel a6t24, detail;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #a006.25 create table with no primary key, no store by
    #and a check constraint
    
    stmt = """control query default POS 'LOCAL_NODE';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """control query default POS_NUM_OF_PARTNS '4';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """control query default POS_LOCATIONS '';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table A6T25 (
sbin6_nuniq  Largeint            no default,
double6_n2   Float(23),
sdec6_4      Decimal(4) signed   no default not null ,
char6_n100   Character(8)        no default,
date6_100    Date                not null,
constraint c1 check (date6_100 > date '2000-10-11')
)
store by (date6_100)
attributes extent (1024,512) ,maxextents 16;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showddl A6T25;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    if hpdci.tgtSQ(): 
        stmt = """select substring(object_name,1,10), DATA_SOURCE,
pri_ext, sec_ext, max_ext from
""" + gvars.definition_schema + """.objects o,
""" + gvars.definition_schema + """.partitions p
where o.object_uid = p.object_uid
and object_name like '%A6T25%';"""
        output = _dci.cmdexec(stmt)
        _dci.expect_selected_msg(output)
    
    stmt = """showlabel a6t25, detail;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #a006.26 create table 30 partitions
    
    stmt = """control query default POS 'LOCAL_NODE';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """control query default POS_NUM_OF_PARTNS '30';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """control query default POS_LOCATIONS '';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table A6T26 (
sbin6_nuniq  Largeint            no default,
double6_n2   Float(23),
sdec6_4      Decimal(4) signed   no default not null not droppable
primary key descending not droppable,
char6_n100   Character(8)        no default,
date6_100    Date                not null)
store by (sdec6_4 desc)
location """ + gvars.g_disc4 + """
attributes extent (16,64) ,maxextents 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showddl A6T26;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    if hpdci.tgtSQ(): 
        stmt = """select substring(object_name,1,10), DATA_SOURCE,
pri_ext, sec_ext, max_ext from
""" + gvars.definition_schema + """.objects o,
""" + gvars.definition_schema + """.partitions p
where o.object_uid = p.object_uid
and object_name like '%A6T26%';"""
        output = _dci.cmdexec(stmt)
        _dci.expect_selected_msg(output)
    
    stmt = """showlabel a6t26, detail;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #a006.27 POS enabled during compilation but disabled during execution
    #POS should not be applied
    
    stmt = """control query default POS 'LOCAL_NODE';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """control query default POS_NUM_OF_PARTNS '4';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """prepare xx from
create table A6T27 (
sbin6_nuniq  Largeint            no default,
double6_n2   Float(23),
sdec6_4      Decimal(4) signed   no default not null not droppable
primary key descending not droppable,
char6_n100          Character(8)        no default,
date6_100           Date                not null)
attributes extent (1024,512) ,maxextents 16;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #turn off POS
    
    stmt = """control query default POS 'LOCAL_NODE';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """control query default POS_NUM_OF_PARTNS '1';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showddl A6T27;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    if hpdci.tgtSQ(): 
        stmt = """select substring(object_name,1,10), DATA_SOURCE,
pri_ext, sec_ext, max_ext from
""" + gvars.definition_schema + """.objects o,
""" + gvars.definition_schema + """.partitions p
where o.object_uid = p.object_uid
and object_name like '%A6T27%';"""
        output = _dci.cmdexec(stmt)
        _dci.expect_selected_msg(output)
    
    stmt = """showlabel a6t27, detail;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #a006.28 POS disabled during compilation but enabled during execution
    #POS applied
    
    stmt = """control query default POS 'LOCAL_NODE';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """control query default POS_NUM_OF_PARTNS '1';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """prepare xx from
create table A6T28 (
sbin6_nuniq  Largeint            no default,
double6_n2   Float(23),
sdec6_4      Decimal(4) signed   no default not null not droppable
primary key descending not droppable,
char6_n100          Character(8)        no default,
date6_100           Date                not null)
attributes extent (1024,512) ,maxextents 16;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #turn on POS
    
    stmt = """control query default POS 'LOCAL_NODE';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """control query default POS_NUM_OF_PARTNS '4';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showddl A6T28;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    if hpdci.tgtSQ(): 
        stmt = """select substring(object_name,1,10),  DATA_SOURCE,
pri_ext, sec_ext, max_ext from
""" + gvars.definition_schema + """.objects o,
""" + gvars.definition_schema + """.partitions p
where o.object_uid = p.object_uid
and object_name like '%A6T28%';"""
        output = _dci.cmdexec(stmt)
        _dci.expect_selected_msg(output)
    
    stmt = """showlabel a6t28, detail;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # a006.29 hash partition table using partition overlay,
    # remote locations multicolumn pk
    # all attributes
    
    stmt = """control query default POS 'MULTI_NODE';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """control query default POS_NUM_OF_PARTNS '11';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """control query default POS_LOCATIONS '""" + gvars.g_disc1 + """,""" + gvars.g_disc2 + """,""" + gvars.g_disc3 + """,""" + gvars.g_disc4 + """,""" + gvars.g_disc5 + """,""" + gvars.g_disc6 + """,""" + gvars.g_disc7 + """,""" + gvars.g_disc8 + """,""" + gvars.g_disc9 + """,""" + gvars.g_disc10 + """';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table A6T29 (
pic_char_1   pic x display upshift not null,
numeric_2    numeric (9,5) unsigned not null,
dec_3        dec(5,3) unsigned not null,
float_4      float(11) not null ,
timestamp_5  timestamp(6) not null ,
int_6        Largeint,
primary key (dec_3,timestamp_5) not droppable)
location """ + gvars.g_disc0 + """
attributes extent (64,64) ,maxextents 4
allocate 4,
blocksize 4096,
no clearonpurge;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # R2.5 NCI #expectfile $test_dir/a006 a6s29a
    stmt = """showddl A6T29;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    if hpdci.tgtSQ(): 
        stmt = """select substring(object_name,1,10),  DATA_SOURCE,
pri_ext, sec_ext, max_ext from
""" + gvars.definition_schema + """.objects o,
""" + gvars.definition_schema + """.partitions p
where o.object_uid = p.object_uid
and object_name like '%A6T29%';"""
        output = _dci.cmdexec(stmt)
        _dci.expect_selected_msg(output)
    
    stmt = """showlabel a6t29, detail;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #cleanup ====
    #tables======
    #A6T1 - A6T29
    
    stmt = """control query default POS_NUM_OF_PARTNS '0';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

