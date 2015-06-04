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

import time
from ...lib import hpdci
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
    _dci.setup_schema(defs.my_schema)
    
    stmt = """env;"""
    output = _dci.cmdexec(stmt)
    stmt = """control query default UPD_SAVEPOINT_ON_ERROR 'OFF';"""
    output = _dci.cmdexec(stmt)
    #runscript $test_dir/setup
    stmt = """control query default POS 'OFF';"""
    output = _dci.cmdexec(stmt)
    stmt = """control query default UPDATE_CLUSTERING_OR_UNIQUE_INDEX_KEY  'OFF';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """DROP schema """+ defs.my_schema +""" cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """select * from "_MD_".objects where schema_name = 'SCH_ATOMIMXCI';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE SCHEMA """+ defs.my_schema +""";"""
    output = _dci.cmdexec(stmt)
    stmt = """set schema  """+ defs.my_schema +""";"""
    output = _dci.cmdexec(stmt)
    
    
    stmt = """CREATE TABLE target_row1 (
        char_3                 char(3),
        pic_x_8                pic x(8) upshift not null,
        binary_64_s            numeric(18, 3) signed,
        var_char_3             varchar(3) upshift,
        small_int              smallint signed,
        decimal_3_unsigned     decimal(3, 0) unsigned,
        var_char_2             varchar(2),
        medium_int             integer unsigned,
        pic_decimal_2          pic v999 display not null,
        float_basic            float (4),
        float_double_p         double precision not null,
        y_to_d                 date,
        iy_to_mo               interval year(4) to month,
        ih_to_s                interval hour to second not null,
        PRIMARY KEY (pic_x_8, pic_decimal_2, float_double_p, ih_to_s)
  );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """INSERT INTO target_row1 (char_3, pic_x_8, binary_64_s, var_char_3,
                           small_int, decimal_3_unsigned, var_char_2, 
                           medium_int, pic_decimal_2, float_basic,
                           float_double_p, y_to_d,
                           iy_to_mo,
                           ih_to_s)
                   VALUES ('XXX', 'TargRows', 123456789012345.123, 'Vc3',
                           32765, 123, 'vc', 
                           217483640,  .123, 1.72001E76,
                           1.72001E76, date '2003-08-01',
                           interval '9999-11' year(4) to month,
                           interval '99:59:59.999999' hour to second),

                          ('123', 'TargRow2', 6789012345.12, 'V32',
                           25, 23, 'v2',
                           4830,  .23, 1.22001E76,
                           1.22001E76, date '2003-02-01',
                           interval '2222-11' year(4) to month,
                           interval '22:22:29.222222' hour to second),

                          ('333', 'TargRow3', 12345.13, 'Vv3',
                           5, 3, 'v3',
                           217,  .3, 1.32001E76,
                           1.32001E76, date '2003-03-01',
                           interval '3333-11' year(4) to month,
                           interval '39:39:39.333333' hour to second);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 3)
    
    time.sleep(5)
    stmt = """select * from target_row1;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE target_rows (
        char_3                 char(3),
        pic_x_8                pic x(8) upshift not null,
        binary_64_s            numeric(18, 3) signed,
        var_char_3             varchar(3) upshift,
        small_int              smallint signed,
        decimal_3_unsigned     decimal(3, 0) unsigned,
        var_char_2             varchar(2),
        medium_int             integer unsigned,
        pic_decimal_2          pic v999 display not null,
        float_basic            float (4),
        float_double_p         double precision not null,
        y_to_d                 date,
        iy_to_mo               interval year(4) to month,
        ih_to_s                interval hour to second not null,
        -- PRIMARY KEY (pic_x_8, pic_decimal_2, float_double_p,ih_to_s)
        PRIMARY KEY (pic_x_8)
  );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """INSERT INTO target_rows (char_3, pic_x_8, binary_64_s, var_char_3,
                           small_int, decimal_3_unsigned, var_char_2,
                           medium_int, pic_decimal_2, float_basic,
                           float_double_p, y_to_d,
                           iy_to_mo,
                           ih_to_s)
                   VALUES ('AXX', 'TRowA', 13579135.13, 'Vc1',
                           32765, 123, 'v1',
                           217483640,  .123, 2.72001E76,
                           2.72001E76, date '2003-08-01',
                           interval '9999-11' year(4) to month,
                           interval '19:59:59.999999' hour to second), 

                          ('BXX', 'TRowB', 123456789012345.123, 'Vc2',
                           -32765, 321, 'v2',
                           27860,  .223, 1.72001E76,
                           1.72001E76, date '2023-08-01',
                           interval '2999-11' year(4) to month,
                           interval '29:29:29.222222' hour to second),

                          ('CXX', 'TRowC', 2468024.2, 'Vc3',
                           265, 123, 'vc',
                           217483640, 0.123, 3.72001E76,
                           3.72001E76, date '3003-08-01',
                           interval '9999-11' year(4) to month,
                           interval '39:59:59.333333' hour to second),

                          ('DXX', 'TRowD', 456012.123, 'Vc4',
                           65, 0, 'v4',
                           483, 0.3, 1.72001E76,
                           4.72001E76, date '2003-08-01',
                           interval '4999-11' year(4) to month,
                           interval '49:59:59.999999' hour to second),

                          ('EXX', 'TargRows', 123456789012345.123, 'Vc3',
                           32765, 123, 'vc',
                           217483640, 0.123, 1.72001E76,
                           1.72001E76, date '2003-08-01',
                           interval '9999-11' year(4) to month,
                           interval '59:59:59.999999' hour to second);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 5)
    
    time.sleep(5)
    
    stmt = """select * from target_rows;"""
    output = _dci.cmdexec(stmt)
    stmt = """SELECT * FROM Target_Rows WHERE pic_x_8 > 'AAA';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select * from target_rows where pic_x_8 = 'TARGROWS';"""
    output = _dci.cmdexec(stmt)
    stmt = """SELECT * FROM Target_Rows WHERE pic_x_8 > 'AAA' and
                                pic_x_8 < 'TROWC   ' and
                                pic_x_8 is not null;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE receiver1 (
        char_3                 char(3),
        pic_x_8                pic x(8) upshift not null,
        binary_64_s            numeric(18, 3) signed,
        var_char_3             varchar(3) upshift,
        small_int              smallint signed,
        decimal_3_unsigned     decimal(3, 0) unsigned,
        var_char_2             varchar(2),
        medium_int             integer unsigned,
        pic_decimal_2          pic v999 display not null,
        float_basic            float (4),
        float_double_p         double precision not null,
        y_to_d                 date,
        iy_to_mo               interval year(4) to month,
        ih_to_s                interval hour to second not null
      , PRIMARY KEY (pic_x_8)
        )
     ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """CREATE TABLE receiver2 (
        char_3                 char(3),
        pic_x_8                pic x(8) upshift not null,
        binary_64_s            numeric(18, 3) signed,
        var_char_3             varchar(3) upshift,
        small_int              smallint signed,
        decimal_3_unsigned     decimal(3, 0) unsigned,
        var_char_2             varchar(2),
        medium_int             integer unsigned,
        pic_decimal_2          pic v999 display not null,
        float_basic            float (4),
        float_double_p         double precision not null,
        y_to_d                 date,
        iy_to_mo               interval year(4) to month,
        ih_to_s                interval hour to second not null,
        PRIMARY KEY (pic_x_8, pic_decimal_2, float_double_p));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """CREATE TABLE receiver3 (
        char_3                 char(3) not null,
        pic_x_8                pic x(8) upshift not null,
        binary_64_s            numeric(18, 3) signed,
        var_char_3             varchar(3) upshift,
        small_int              smallint signed,
        decimal_3_unsigned     decimal(3, 0) unsigned,
        var_char_2             varchar(2),
        medium_int             integer unsigned,
        pic_decimal_2          pic v999 display not null,
        float_basic            float (4),
        float_double_p         double precision not null,
        y_to_d                 date,
        iy_to_mo               interval year(4) to month,
        ih_to_s                interval hour to second not null,
        PRIMARY KEY (char_3, pic_decimal_2, ih_to_s));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """Create view View_R1 as (select * from receiver1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """Create view View_R3 as (select * from receiver3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop table RI1A cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table RI1B cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table RI1C cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table RI2A cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table RI2B cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table RI3A cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table RI3B cascade;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table RI1A (ss_num char(11) not null unique, 
                   account int unsigned not null unique,
                   name char(20) not null) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from "_MD_".objects where schema_name = 'SCH_ATOMIMXCI';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table RI1B (ss_num char(11) not null unique constraint C111B1 
                        references RI1A(ss_num),
                   account int unsigned not null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from "_MD_".objects where schema_name = 'SCH_ATOMIMXCI';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table RI1C (ss_num char(11) not null constraint C111C1 
                        references RI1A(ss_num),
                   account int unsigned not null constraint 
                    C111C2 references RI1A(account));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table RI2A (ss_num char(11) not null unique, 
                   account int unsigned not null unique ,
                   name char(20) not null,
                   primary key(ss_num, account)) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table RI2B (ss_num char(11) not null unique constraint C121B1 
                        references RI2A(ss_num),
                   account int unsigned not null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table RI3A (ss_num char(11) not null unique, 
                   account int unsigned not null unique ,
                   name char(20) not null) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table RI3B (ss_num char(11) not null constraint C123B1 
                        references RI3A(ss_num),
                   account int unsigned not null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    
    stmt = """drop table trig_t1 cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table trig_t1A cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table trig_t2 cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table trig_t4 cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table trig_t4A cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table trig_t077 cascade;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table trig_t1 (a int not null, b varchar(20) not null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index idxt089_1 on trig_t1 (a);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index idxt089_2 on trig_t1 (b);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table trig_t1A (a int not null unique, b varchar(20) not null unique);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """alter table trig_t1 add constraint CN089 foreign key (b) references trig_t1A(b);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table trig_t2 (a int not null, b varchar(20) not null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index idxt094_1 on trig_t2 (a);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index idxt094_2 on trig_t2 (b);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table trig_t2A (a int not null unique, b varchar(20) not null unique);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """alter table trig_t2 add constraint CN094 foreign key (a) 
                        references trig_t2A (a);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """alter table trig_t2 add constraint CN094_1 foreign key (b)
                                                references trig_t2A (b);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # $err_msg 8103 "TRAFODION.SCH_ATOMIMXCI.CN094" "TRAFODION.SCH_ATOMIMXCI.TRIG_T2"
    stmt = """insert into trig_t2 values
 (2,'bb'),(4,'dd'),(6,'ff'),(8,'gg'),(10,'hh'),(13,'ii'),(14,'jj');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output,'8103') 
    
    stmt = """create table trig_t077 (a int, b varchar(20));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index idxt077 on trig_t077 (a,b);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table trig_t04 (a int not null, b varchar(20) not null);"""
    output = _dci.cmdexec(stmt)
    stmt = """create index idxt04_1 on trig_t04 (a);"""
    output = _dci.cmdexec(stmt)
    stmt = """create index idxt04_2 on trig_t04 (b);"""
    output = _dci.cmdexec(stmt)
    stmt = """create table trig_t04A (a int not null unique, b varchar(20) not null unique);"""
    output = _dci.cmdexec(stmt)
    stmt = """alter table trig_t04 add constraint CN04 foreign key (b) references trig_t04A(b);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select count(*) from target_row1;"""
    output = _dci.cmdexec(stmt)
    stmt = """select count(*) from target_rows;"""
    output = _dci.cmdexec(stmt)

def _init2(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci

    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()
    _dci.setup_schema(defs.my_schema)
    
    stmt = """control query default POS 'OFF';"""
    output = _dci.cmdexec(stmt)
    stmt = """control query default UPDATE_CLUSTERING_OR_UNIQUE_INDEX_KEY  'OFF';"""
    output = _dci.cmdexec(stmt)
    stmt = """set schema  """+ defs.my_schema +""";"""
    output = _dci.cmdexec(stmt)

    stmt = """drop table target_row1 cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table target_rows cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table receiver1 cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table receiver2 cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table receiver3 cascade;"""
    output = _dci.cmdexec(stmt)
   
    stmt = """CREATE TABLE target_row1 (
        char_3                 char(3),
        pic_x_8                pic x(8) upshift not null,
        binary_64_s            numeric(18, 3) signed,
        var_char_3             varchar(3) upshift,
        small_int              smallint signed,
        decimal_3_unsigned     decimal(3, 0) unsigned,
        var_char_2             varchar(2),
        medium_int             integer unsigned,
        pic_decimal_2          pic v999 display not null,
        float_basic            float (4),
        float_double_p         double precision not null,
        y_to_d                 date,
        iy_to_mo               interval year(4) to month,
        ih_to_s                interval hour to second not null,
        PRIMARY KEY (pic_x_8, pic_decimal_2, float_double_p)
  );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """INSERT INTO target_row1 (char_3, pic_x_8, binary_64_s, var_char_3,
                           small_int, decimal_3_unsigned, var_char_2, 
                           medium_int, pic_decimal_2, float_basic,
                           float_double_p, y_to_d,
                           iy_to_mo,
                           ih_to_s)
                   VALUES ('XXX', 'TargRows', 123456789012345.123, 'Vc3',
                           32765, 123, 'vc', 
                           217483640,  .123, 1.72001E76,
                           1.72001E76, date '2003-08-01',
                           interval '9999-11' year(4) to month,
                           interval '99:59:59.999999' hour to second),

                          ('123', 'TargRow2', 6789012345.12, 'V32',
                           25, 23, 'v2',
                           4830,  .23, 1.22001E76,
                           1.22001E76, date '2003-02-01',
                           interval '2222-11' year(4) to month,
                           interval '22:22:29.222222' hour to second),

                          ('333', 'TargRow3', 12345.13, 'Vv3',
                           5, 3, 'v3',
                           217,  .3, 1.32001E76,
                           1.32001E76, date '2003-03-01',
                           interval '3333-11' year(4) to month,
                           interval '39:39:39.333333' hour to second);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 3)
    
    time.sleep(5)
    stmt = """select * from target_row1;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE target_rows (
        char_3                 char(3),
        pic_x_8                pic x(8) upshift not null,
        binary_64_s            numeric(18, 3) signed,
        var_char_3             varchar(3) upshift,
        small_int              smallint signed,
        decimal_3_unsigned     decimal(3, 0) unsigned,
        var_char_2             varchar(2),
        medium_int             integer unsigned,
        pic_decimal_2          pic v999 display not null,
        float_basic            float (4),
        float_double_p         double precision not null,
        y_to_d                 date,
        iy_to_mo               interval year(4) to month,
        ih_to_s                interval hour to second not null,
        PRIMARY KEY (pic_x_8, pic_decimal_2, float_double_p)
  ); """
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """INSERT INTO target_rows (char_3, pic_x_8, binary_64_s, var_char_3,
                           small_int, decimal_3_unsigned, var_char_2,
                           medium_int, pic_decimal_2, float_basic,
                           float_double_p, y_to_d,
                           iy_to_mo,
                           ih_to_s)
                   VALUES ('AXX', 'TRowA', 13579135.13, 'Vc1',
                           32765, 123, 'v1',
                           217483640,  .123, 2.72001E76,
                           2.72001E76, date '2003-08-01',
                           interval '9999-11' year(4) to month,
                           interval '19:59:59.999999' hour to second), 

                          ('BXX', 'TRowB', 123456789012345.123, 'Vc2',
                           -32765, 321, 'v2',
                           27860,  .223, 1.72001E76,
                           1.72001E76, date '2023-08-01',
                           interval '2999-11' year(4) to month,
                           interval '29:29:29.222222' hour to second),

                          ('CXX', 'TRowC', 2468024.2, 'Vc3',
                           265, 123, 'vc',
                           217483640, 0.123, 3.72001E76,
                           3.72001E76, date '3003-08-01',
                           interval '9999-11' year(4) to month,
                           interval '39:59:59.333333' hour to second),

                          ('DXX', 'TRowD', 456012.123, 'Vc4',
                           65, 0, 'v4',
                           483, 0.3, 1.72001E76,
                           4.72001E76, date '2003-08-01',
                           interval '4999-11' year(4) to month,
                           interval '49:59:59.999999' hour to second),

                          ('EXX', 'TargRows', 123456789012345.123, 'Vc3',
                           32765, 123, 'vc',
                           217483640, 0.123, 1.72001E76,
                           1.72001E76, date '2003-08-01',
                           interval '9999-11' year(4) to month,
                           interval '59:59:59.999999' hour to second);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 5)
    
    time.sleep(5)
    
    stmt = """select * from target_rows;"""
    output = _dci.cmdexec(stmt)
    stmt = """SELECT * FROM Target_Rows WHERE pic_x_8 > upper('aaa');"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select * from target_rows where pic_x_8 = 'TARGROWS';"""
    output = _dci.cmdexec(stmt)
    stmt = """SELECT * FROM Target_Rows WHERE pic_x_8 > 'AAA' and
                                pic_x_8 < 'TROWC   ' and
                                pic_x_8 is not null;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE receiver1 (
        char_3                 char(3),
        pic_x_8                pic x(8) upshift not null,
        binary_64_s            numeric(18, 3) signed,
        var_char_3             varchar(3) upshift,
        small_int              smallint signed,
        decimal_3_unsigned     decimal(3, 0) unsigned,
        var_char_2             varchar(2),
        medium_int             integer unsigned,
        pic_decimal_2          pic v999 display not null,
        float_basic            float (4),
        float_double_p         double precision not null,
        y_to_d                 date,
        iy_to_mo               interval year(4) to month,
        ih_to_s                interval hour to second not null
      , PRIMARY KEY (pic_x_8)
        )
     ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """CREATE TABLE receiver2 (
        char_3                 char(3),
        pic_x_8                pic x(8) upshift not null,
        binary_64_s            numeric(18, 3) signed,
        var_char_3             varchar(3) upshift,
        small_int              smallint signed,
        decimal_3_unsigned     decimal(3, 0) unsigned,
        var_char_2             varchar(2),
        medium_int             integer unsigned,
        pic_decimal_2          pic v999 display not null,
        float_basic            float (4),
        float_double_p         double precision not null,
        y_to_d                 date,
        iy_to_mo               interval year(4) to month,
        ih_to_s                interval hour to second not null,
        PRIMARY KEY (pic_x_8, pic_decimal_2, float_double_p));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """CREATE TABLE receiver3 (
        char_3                 char(3) not null,
        pic_x_8                pic x(8) upshift not null,
        binary_64_s            numeric(18, 3) signed,
        var_char_3             varchar(3) upshift,
        small_int              smallint signed,
        decimal_3_unsigned     decimal(3, 0) unsigned,
        var_char_2             varchar(2),
        medium_int             integer unsigned,
        pic_decimal_2          pic v999 display not null,
        float_basic            float (4),
        float_double_p         double precision not null,
        y_to_d                 date,
        iy_to_mo               interval year(4) to month,
        ih_to_s                interval hour to second not null,
        PRIMARY KEY (char_3, pic_decimal_2));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select count(*) from target_row1;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select count(*) from target_rows;"""
    output = _dci.cmdexec(stmt)
