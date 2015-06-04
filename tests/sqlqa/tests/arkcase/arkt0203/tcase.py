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
    #  Test case name:     arkt0203 : A01
    #  Description:        Select with multi-valued predicates.
    #                      CAST, IS NULL, IS NOT NULL
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   Same as above.
    #
    #  Notes:
    #  This test case incorporates features detailed in the "Title"
    #  by Ima Programmer (Version 1.1, <date>).
    #
    # =================== End Test Case Header  ===================
    stmt = """drop table a1table1;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table a1table1 
( c1 integer default null
, c2 integer default null
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #                        catalog ;
    
    stmt = """insert into a1table1 
values ( 1 ,   1 ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a1table1 
values ( 1 ,   2 ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a1table1 
values ( 1 ,   null ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a1table1 
values ( 2 ,   1 ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a1table1 
values ( 2 ,   2 ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a1table1 
values ( 2 ,   null ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a1table1 
values ( null, 1 ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a1table1 
values ( null, 2 ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a1table1 
values ( null, null ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # This fails because you cannot use the keyword NULL in an expression:
    
    stmt = """insert into a1table1 
values ( cast(null as int), 1 ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select *  from a1table1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s1')
    
    stmt = """select *  from a1table1 
where cast(c1 as int) > 0 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s2')
    
    stmt = """select *  from a1table1 
where cast(c1 as int) > 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s3')
    
    stmt = """select *  from a1table1 
where cast(c1 as int) > 2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """select *  from a1table1 
where cast(c2 as real ) > 0 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s4')
    
    stmt = """select *  from a1table1 
where cast(c2 as float) > 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s5')
    
    stmt = """select *  from a1table1 
where cast(c2 as float) > 2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """select *  from a1table1 
where cast(c1 as int) , cast(c2 as float) > 0 , 0 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s6')
    
    stmt = """select *  from a1table1 
where cast(c1 as int) , cast(c2 as float) > 0 , 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s7')
    
    stmt = """select *  from a1table1 
where cast(c1 as int) , cast(c2 as float) > 0 , 2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s8')
    
    stmt = """select *  from a1table1 
where cast(c1 as int) , cast(c2 as float(10)) > 1 , 0 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s9')
    
    stmt = """select *  from a1table1 
where cast(c1 as int) , cast(c2 as float) > 1 , 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s10')
    
    stmt = """select *  from a1table1 
where cast(c1 as int) , cast(c2 as float) > 1 , 2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s11')
    
    stmt = """select *  from a1table1 
where cast(c1 as int) , cast(c2 as float) > 2 , 0 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s12')
    
    stmt = """select *  from a1table1 
where cast(c1 as int) , cast(c2 as float) > 2 , 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s13')
    
    stmt = """select *  from a1table1 
where cast(c1 as int) , cast(c2 as float) > 2 , 2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """select * from a1table1 
where cast (c1 as varchar(5)) ,
cast (cast (c2 as char) as char) is null ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s14')
    
    stmt = """select * from a1table1 
where cast (c2 as char) , cast (c1 as varchar(5)) is null ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s15')
    
    stmt = """select * from a1table1 
where cast (c1 as varchar(5)) , cast (c2 as char) is not null ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s16')
    
    stmt = """create index a1index1 on
 a1table1 (c1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    # catalog ;
    
    stmt = """create index a1index2 on
 a1table1 (c2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #  catalog ;
    
    stmt = """select * from a1table1 
where cast (c1 as char) , cast (c2 as char) is null ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s17')
    
    stmt = """select * from a1table1 where
cast (c2 as char) , cast (c1 as char) is null ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s18')
    
    stmt = """select * from a1table1 where
cast (c1 as char) , cast (c2 as char) is not null ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s19')
    
    # ----------------------------
    # Cleanup:
    # ----------------------------
    stmt = """drop table a1table1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test002(desc="""a02"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    # Test case name:	pretsta02
    # Description:		This test creates the tables and inserts data into
    #		 	the tables btre201, btre202, btre203, btre204,
    #			btre205, btre208.
    # Expected Results:
    #
    
    stmt = """drop table btre201;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table btre201 (
ordering            smallint   not null
, alwaysnull          smallint                default null
, char_1              char(1)                 default null
, pic_x_8             pic x(8)                default null
, var_char_2          varchar(2)              default null
, var_char_3          varchar(3)              default null
, binary_signed       numeric (4) signed      default null
, binary_32_u         numeric (9,2) unsigned  default null
, binary_64_s         numeric (18,3) signed   default null
, pic_comp_1          pic s9(10) comp         default null
, pic_comp_2          pic sv9(2) comp         default null
, pic_comp_3          pic s9(3)v9(5) comp     default null
, small_int           smallint                default null
, medium_int          integer unsigned        default null
, large_int           largeint signed         default null
, decimal_1           decimal (1)             default null
, decimal_2_signed    decimal (2,2) signed    default null
, decimal_3_unsigned  decimal (3,0) unsigned  default null
, pic_decimal_1       pic s9(1)v9(1)          default null
, pic_decimal_2       picture v999 display    default null
, pic_decimal_3       pic s9                  default null
, float_basic         float (4)               default null
, float_real          real                    default null
, float_double_p      double precision        default null
--    , y_to_d              datetime year to day    default null
, y_to_d              date                    default null
, y_to_d_2            date                    default null
--    , h_to_f              datetime hour to fraction(3) default null
, h_to_f              time(3)                 default null
, time1               time                    default null
, iy_to_mo            interval year(4) to month  default null
, ih_to_s             interval hour to second default null
, primary key (ordering)
)
ATTRIBUTES
--    audit
-- 1/25/99 For now the only blocksize supported is 4096
blocksize 4096
;"""
    output = _dci.cmdexec(stmt)
    
    #  Create INDEXES for table BTRE201.
    stmt = """create index btre201a 
on btre201 (ordering)
-- 1/25/99 For now the only blocksize supported is 4096
ATTRIBUTES
blocksize 4096
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create index btre201b 
on btre201 (char_1, alwaysnull, binary_signed)
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create index btre201c 
on btre201 (var_char_3, large_int)
-- 1/25/99 For now the only blocksize supported is 4096
ATTRIBUTES
blocksize 4096
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create index btre201d 
on btre201 (decimal_3_unsigned, pic_decimal_1)
-- 1/25/99 For now the only blocksize supported is 4096
ATTRIBUTES
blocksize 4096
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create index btre201e 
on btre201 (pic_x_8, iy_to_mo, y_to_d, medium_int)
ATTRIBUTES
allocate 2,
auditcompress,
blocksize 4096 ,
--      no buffered
clearonpurge,

--      no dcompress,
extent (32,128),
--      no icompress,
maxextents 320
--    maxsize 320
--      serialwrites
--      no verifiedwrites
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create index btre201f 
on btre201 (ih_to_s)
ATTRIBUTES
--    keytag 34
-- 1/25/99 For now the only blocksize supported is 4096
blocksize 4096
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create index btre201g 
on btre201 (time1 DESC, float_real ASC, pic_comp_3)
ATTRIBUTES
--    keytag 'ka'
allocate 4,
no auditcompress
-- 1/25/99 For now the only blocksize supported is 4096
blocksize 4096,
--      buffered
no clearonpurge,
--      no dcompress,
extent (16,32)
--      icompress,
--      maxsize 6
maxextents 6
--    no serialwrites
--    verifiedwrites
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create index btre201h 
on btre201 (y_to_d_2 DESC)
-- 1/25/99 For now the only blocksize supported is 4096
--      ATTRIBUTES
--      blocksize 512
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create index btre201i 
on btre201 (float_double_p ASC)
--      ATTRIBUTES
-- 1/25/99 For now the only blocksize supported is 4096
--      blocksize 512
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create index btre201j 
on btre201 (h_to_f)
-- 1/25/99 For now the only blocksize supported is 4096
--      ATTRIBUTES
--      blocksize 512
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create index btre201k 
on btre201 (decimal_1, pic_decimal_3 DESC)
-- 1/25/99 For now the only blocksize supported is 4096
--      ATTRIBUTES
--      blocksize 512
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create index btre201l 
on btre201 (decimal_2_signed ASC, small_int DESC,
var_char_2, binary_32_u, pic_comp_1,
float_basic DESC)
-- 1/25/99 For now the only blocksize supported is 4096
--      ATTRIBUTES
--      blocksize 512
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create index btre201m 
on btre201 (pic_comp_2, binary_64_s)
-- 1/25/99 For now the only blocksize supported is 4096
--      ATTRIBUTES
--      blocksize 512
;"""
    output = _dci.cmdexec(stmt)
    
    #  Insert values needed for T139 (NULLs and DML):
    stmt = """insert into btre201 (ordering , pic_comp_2 ,
pic_comp_3 , char_1 , pic_x_8 , var_char_2, var_char_3
, small_int , large_int , decimal_2_signed
, decimal_1
)
values ( 1, .1, 1
, 'a' , 'Abcdefgh' , 'aB' , 'AbC'
, NULL , 1 , .1
, 1
) ;"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into btre201 (ordering , pic_comp_2 ,
pic_comp_3 , var_char_2, var_char_3
, small_int , large_int , decimal_2_signed
, decimal_1
)
values ( 2, null, 2
, 'az' , 'zz'
, NULL , NULL , .2
, 1
) ;"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into btre201 (ordering , pic_comp_2 ,
pic_comp_3 , var_char_2, var_char_3
, small_int , large_int , decimal_2_signed
)
values ( 3, null, 2
, 'zy' , 'zy'
, NULL , 10 , NULL
) ;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """drop table btre202;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table btre202 (
char_1              char(1)                 default null
, var_char_3          varchar(3)              default null
, small_int           smallint                default null
, medium_int          integer unsigned        default null
, large_int           largeint signed         default null
, float_basic         float (4)               default null
, y_to_d              date                    default null
) no partition
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into btre202 
values (
--    , char_1              char(1)                 default null
--    , var_char_3          varchar(3)              default null
'C' ,'rum'
--    , small_int           smallint                default null
--    , medium_int          integer unsigned        default null
--    , large_int           largeint signed         default null
,9000 ,1000 ,2000
--    , float_basic         float (4)               default null
,1.2E+0
--    , y_to_d              datetime year to day    default null
,date '1975-01-01'
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into btre202 (char_1) values ( NULL ) ;"""
    output = _dci.cmdexec(stmt)
    stmt = """update statistics for table btre202 ;"""
    output = _dci.cmdexec(stmt)
    stmt = """select * from btre202 
order by char_1;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """drop table btre203;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table btre203 (
col_numeric        smallint     default null
, col_varchar        varchar (3)  default null
, col_date           date         default null
, col_float          float (5)    default null
, col_string         pic x        default null
, col_numeric2       smallint     default 8      not null
, col_varchar2       varchar (3)  default '?'    not null
, col_date2          date         not null
--      , col_date2          date         default system not null
, col_float2         float (5)                   not null
, col_string2        pic x        no default     not null
, col_string3        pic x
) no partition;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """drop table btre204;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table btre204 (
char_1              char(1)                 not null
, pic_x_8             pic x(8)                not null
, var_char_2          varchar(2)              not null
, var_char_3          varchar(3)              not null
, binary_signed       numeric (4) signed      not null
, binary_32_u         numeric (9,2) unsigned  not null
, binary_64_s         numeric (18,3) signed   not null
, pic_comp_1          pic s9(10) comp         not null
, pic_comp_2          pic sv9(2) comp         not null
, pic_comp_3          pic s9(3)v9(5) comp     not null
, small_int           smallint                not null
, medium_int          integer unsigned        not null
, large_int           largeint signed         not null
, decimal_1           decimal (1)             not null
, decimal_2_signed    decimal (2,2) signed    not null
, decimal_3_unsigned  decimal (3,0) unsigned  not null
, pic_decimal_1       pic s9(1)v9(1)          not null
, pic_decimal_2       picture v999 display    not null
, pic_decimal_3       pic s9                  not null
, float_basic         float (4)               not null
, float_real          real                    not null
, float_double_p      double precision        not null
, y_to_d              date        not null
, y_to_d_2            date                    not null
, h_to_f              time(3) not null
, time1               time                    not null
, iy_to_mo            interval year(4) to month  not null
, ih_to_s             interval hour to second not null
, ordering            smallint not null
, primary key (ordering)
)
--    ATTRIBUTES
--    audit
-- 1/25/99 For now the only blocksize supported is 4096
--    blocksize 2048
;"""
    output = _dci.cmdexec(stmt)
    
    #  Insert a record needed for T149 (JOIN) -
    #  to match btre208 and btsel01; need values for all columns:
    stmt = """insert into btre204 
values (
'C' ,'maureen' ,'E' ,'rum'
,3000 ,80 ,2000 ,500
,0.50 ,100.7
,9000 ,1000 ,2000 ,8 ,.97 ,150
,7.1 ,0.7 ,7
,1.2 ,0.0001 ,0.0002
,date '1975-01-01'
,date '1980-01-01'
,time '15:00:00'
,time '13:11:59'
,interval '1900-01' year(4) to month
,interval '1:2:3' hour to second
, 1
);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """update statistics for table btre204 ;"""
    output = _dci.cmdexec(stmt)
    stmt = """select * from btre204 
order by ordering;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """drop table btre205;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table btre205 (
ordering            smallint
, col_1               smallint    default null
, col_2               smallint    default null
) no partition ;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into btre205 values ( 1 , 1    , 2 ) ;"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into btre205 values ( 2 , 1    , 9 ) ;"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into btre205 values ( 3 , 1    , null ) ;"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into btre205 values ( 4 , 9    , 2 ) ;"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into btre205 values ( 5 , 9    , 9 ) ;"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into btre205 values ( 6 , 9    , null ) ;"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into btre205 values ( 7 , null , 2 ) ;"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into btre205 values ( 8 , null , 9 ) ;"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into btre205 values ( 9 , null , null ) ;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """update statistics for table btre205 ;"""
    output = _dci.cmdexec(stmt)
    stmt = """select * from btre205 
order by ordering;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """drop table btre208;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table btre208 (
ordering            smallint
, alwaysnull          smallint                default null
--  Needs 1 duplicate value for ORDER BY.
, var_char_2          varchar(2)              not     null
, var_char_3          varchar(3)              not     null
, pic_decimal_2       decimal (2,2) signed    not     null
, float_double_p      double precision        not     null
, y_to_d              date                    not     null
, ih_to_s             interval hour to second(0) not     null
, headed_pic_x        pic x                   default null
heading 'long'
, headed_numeric      numeric (9,2) unsigned  default null
heading 'short'
) no partition ;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into btre208 
values (
--      ordering            smallint
1
--    , alwaysnull          smallint                default null
, Null
--  Needs 1 duplicate value for ORDER BY.
--    , var_char_2          varchar(2)              not     null
, 'E'
--    , var_char_3          varchar(3)              not     null
, 'E'
--    , pic_decimal_2       pic v999 display        not     null
, .002
--    , float_double_p      double precision        not     null
, 1.2E+0
--    , y_to_d              datetime year to day    not     null
,date '1975-01-01'
--    , ih_to_s             interval hour to second not     null
,interval '1:2:3' hour to second
--    , headed_pic_x        pic x                   default null
--                                                     heading 'long'
, 'z'
--    , headed_numeric      numeric (9,2) unsigned  default null
--                                                     heading 'short'
, 1
) ;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """update statistics for table btre208 ;"""
    output = _dci.cmdexec(stmt)
    stmt = """select * from btre208 
order by ordering;"""
    output = _dci.cmdexec(stmt)
    
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0203 : A02
    #  Description:        Tests CAST adapted from T148 case A5,
    #                      UNION - multiple and combining,
    #                      UNION(distinct) and UNION ALL.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   As above.
    #
    #  Notes:
    #  This test case incorporates features detailed in the "Title"
    #  by Ima Programmer (Version 1.1, <date>).
    #
    # =================== End Test Case Header  ===================
    
    stmt = """select binary_signed  from btre201 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s0')
    stmt = """select small_int      from btre202 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s1')
    
    stmt = """select col_float      from btre203 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """select binary_64_s    from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s2')
    stmt = """select col_1          from btre205 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s3')
    stmt = """select headed_numeric from btre208 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s4')
    
    #  ---------------------------
    #  Union all of increasing number of tables:
    #  ---------------------------
    
    #  NOTE:  The ORDER is not specified, so sometimes the expected order
    #  is changed, check all the elements are there, and move Logaa02 to Logea02
    
    stmt = """select cast ( binary_signed  as char(20) )
from btre201 
union all
select cast ( small_int      as char(20) )
from btre202 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s5')
    
    stmt = """select cast ( col_float      as char(20) )
from btre203 
union all
select cast ( binary_64_s    as char(20) )
from btre204 
union all
select cast ( col_1          as char(20) )
from btre205 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s6')
    
    stmt = """select cast ( col_float      as varchar(20) )
from btre203 
union all
select cast ( binary_64_s    as varchar(20) )
from btre204 
union all
select cast ( col_1          as varchar(20) )
from btre205 
union all
select cast ( headed_numeric as varchar(20) )
from btre208 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s7')
    
    stmt = """select cast ( binary_signed  as char(20) )
from btre201 
union all
select cast ( small_int      as char(20) )
from btre202 
union all
select cast ( col_float      as char(20) )
from btre203 
union all
select cast ( binary_64_s    as char(20) )
from btre204 
union all
select cast ( col_1          as char(20) )
from btre205 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s8')
    
    #  NOTE:  The ORDER is not specified, so sometimes the expected order
    #  is changed, check all the elements are there, and move Logaa02 to Logea02
    
    stmt = """select cast ( binary_signed  as char(20) )
from btre201 
union all
select cast ( small_int      as char(20) )
from btre202 
union all
select cast ( col_float      as varchar(20) )
from btre203 
union all
select cast ( binary_64_s    as varchar(20) )
from btre204 
union all
select cast ( col_1          as char(20) )
from btre205 
union all
select cast ( headed_numeric as char(20) )
from btre208 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s9')
    
    #  ---------------------------
    #  Union (distinct) of increasing number of tables:
    #  ---------------------------
    
    #  NOTE:  The ORDER is not specified, so sometimes the expected order
    #  is changed, check all the elements are there, and move Logaa02 to Logea02
    
    stmt = """select cast ( binary_signed  as char(20) )
from btre201 
union
select cast ( small_int      as char(20) )
from btre202 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s10')
    
    #  NOTE:  The ORDER is not specified, so sometimes the expected order
    #  is changed, check all the elements are there, and move Logaa02 to Logea02
    
    stmt = """select cast ( binary_signed  as char(20) )
from btre201 
union all
select cast ( small_int      as char(20) )
from btre202 
union all
select cast ( col_float      as varchar(21) )
from btre203 
union all
select cast ( binary_64_s    as varchar(21) )
from btre204 
union all
select cast ( col_1          as char(20) )
from btre205 
union all
select cast ( headed_numeric as char(20) )
from btre208 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s11')
    
    #  ---------------------------
    #  Mixed union (distinct) and UNION ALL:
    #  ---------------------------
    
    #  NOTE:  The ORDER is not specified, so sometimes the expected order
    #  is changed, check all the elements are there, and move Logaa02 to Logea02
    
    stmt = """select cast ( binary_signed  as char(20) )
from btre201 
union
select cast ( small_int      as char(20) )
from btre202 
union all
select cast ( col_float      as char(20) )
from btre203 
union
select cast ( binary_64_s    as char(20) )
from btre204 
union all
select cast ( col_1          as char(20) )
from btre205 
union
select cast ( headed_numeric as char(20) )
from btre208 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s12')
    
    stmt = """select cast ( binary_signed  as char(20) )
from btre201 
union all
select cast ( small_int      as char(20) )
from btre202 
union
select cast ( col_float      as char(20) )
from btre203 
union all
select cast ( binary_64_s    as char(20) )
from btre204 
union
select cast ( col_1          as char(20) )
from btre205 
union all
select cast ( headed_numeric as char(20) )
from btre208 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s13')
    
    #  NOTE:  The ORDER is not specified, so sometimes the expected order
    #  is changed, check all the elements are there, and move Logaa02 to Logea02
    
    stmt = """select cast ( binary_signed  as char(20) )
from btre201 
union
select cast ( small_int      as char(20) )
from btre202 
union
select cast ( col_float      as char(20) )
from btre203 
union all
select cast ( binary_64_s    as char(20) )
from btre204 
union all
select cast ( col_1          as char(20) )
from btre205 
union
select cast ( headed_numeric as char(20) )
from btre208 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s14')
    
    #  ---------------------------
    #  Mixed use of parens:
    #  ---------------------------
    
    #  NOTE:  The ORDER is not specified, so sometimes the expected order
    #  is changed, check all the elements are there, and move Logaa02 to Logea02
    
    stmt = """select cast ( binary_signed  as char(20) )
from btre201 
union
( select cast ( small_int      as char(20) )
from btre202 
union
select cast ( binary_64_s    as char(20) )
from btre204 
)
union
select cast ( col_1          as char(20) )
from btre205 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s15')
    
    #  NOTE:  The ORDER is not specified, so sometimes the expected order
    #  is changed, check all the elements are there, and move Logaa02 to Logea02
    
    stmt = """select cast ( binary_signed  as char(20) )
from btre201 
union all
select cast ( small_int      as char(20) )
from btre202 
union all
( select cast ( binary_64_s    as char(20) )
from btre204 
union all
select cast ( col_1          as char(20) )
from btre205 
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s16')
    
    stmt = """( select cast ( binary_signed  as char(20) )
from btre201 
union all
select cast ( small_int      as char(20) )
from btre202 
)
union all
select cast ( binary_64_s    as char(20) )
from btre204 
union all
select cast ( col_1          as char(20) )
from btre205 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s17')
    
    _testmgr.testcase_end(desc)

def test003(desc="""a03"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0203 : A03
    #  Description:        This test verifies cast in JOINs.
    #  Test case inputs:   --
    #  Test case outputs:  --
    #  Expected Results:   As above
    #
    #  Notes:
    #  This test case incorporates features detailed in the "Title"
    #  by Ima Programmer (Version 1.1, <date>).
    #
    # =================== End Test Case Header  ===================
    #
    
    # ---------------------------
    # Move to volume for temporary SQL objects:
    # ---------------------------
    # VOLUME ;
    # CATALOG ;
    
    #  Create tables to be used:
    
    stmt = """CREATE TABLE a3table1 (
suppnum                PIC 9(3)  default 0  not null
, suppname               PIC X(18) --default ' ' not null
, address                PIC X(22) --default ' ' not null
, city                   PIC X(14) --default ' ' not null
, state                  PIC X(12) --default ' ' not null
, PRIMARY KEY (suppnum)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    # catalog
    
    stmt = """CREATE TABLE a3table2 (
suppnum                PIC 9(3)  default 0 not null
, suppname               PIC X(18) --default ' ' not null
, address                PIC X(22) --default ' ' not null
, city                   PIC X(14) --default ' ' not null
, state                  PIC X(12) --default ' ' not null
, PRIMARY KEY (suppnum)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    # catalog
    
    stmt = """create table a3table3 (
suppnum  pic 999
, suppname pic x(18)
, address  pic x(22)
, city     pic x(14)
, state    pic x(12)
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #  catalog
    
    stmt = """create table a3table4 (
suppnum  pic 999
, suppname pic x(18)
, address  pic x(22)
, city     pic x(14)
, state    pic x(12)
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #  catalog
    
    stmt = """create table a3table5 (
suppnum  pic 999
, suppname pic x(18)
, address  pic x(22)
, city     pic x(14)
, state    pic x(12)
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #  catalog
    
    stmt = """create table a3table6 (
suppnum  pic 999
, suppname pic x(18)
, address  pic x(22)
, city     pic x(14)
, state    pic x(12)
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #  catalog
    
    stmt = """create table a3table7 (
suppnum  pic 999
, suppname pic x(18)
, address  pic x(22)
, city     pic x(14)
, state    pic x(12)
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #  catalog
    
    stmt = """create table a3table8 (
suppnum  pic 999
, suppname pic x(18)
, address  pic x(22)
, city     pic x(14)
, state    pic x(12)
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #  catalog
    
    #  Populate tables to be used:
    
    stmt = """insert into a3table1 
select * from """ + gvars.g_schema_arkcasedb + """.supplier 
where cast(suppnum as float) <= 10 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 6)
    
    stmt = """select * from a3table1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s0')
    
    stmt = """insert into a3table2 
select * from """ + gvars.g_schema_arkcasedb + """.supplier 
where suppnum >= 10 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 2)
    
    stmt = """select * from a3table2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s1')
    
    #   Insert using LEFT JOIN in a select:
    
    stmt = """select a3table1.suppnum, a3table1.suppname , a3table2.address
, a3table2.city   , a3table2.state
from       a3table1 
left  join a3table2 
on cast(a3table1.suppnum as float) =
cast(a3table2.suppnum as numeric (2) )
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s2')
    
    stmt = """insert into a3table3 
select a3table1.suppnum, a3table1.suppname , a3table2.address
, a3table2.city   , a3table2.state
from       a3table1 
left  join a3table2 
on cast(a3table1.suppnum as char(20)) =
cast(a3table2.suppnum as varchar(20))
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 6)
    
    stmt = """select * from a3table3 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s3')
    
    #   Insert using RIGHT JOIN in a select:
    stmt = """select        a.suppnum,        a.suppname
,        b.address
,        b.city   ,        b.state
from       a3table2 b
left join  a3table1 a
on cast(a.suppnum as    char(20)) =
cast(b.suppnum as varchar(20))
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s4')
    stmt = """insert into a3table4 
select        a.suppnum,        a.suppname
,        b.address
,        b.city   ,        b.state
from       a3table2 b
left join  a3table1 a
on cast(a.suppnum as varchar(20)) =
cast(b.suppnum as    char(20))
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 2)
    stmt = """select * from a3table4 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s5')
    
    #   Insert using UNION of LEFT JOINs (see far below!).
    
    #   The two simple selects:
    stmt = """select a3table1.suppnum, a3table1.suppname
from       a3table1 
order by suppnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s6')
    stmt = """select a3table2.address , a3table2.city , a3table2.state
from       a3table2 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s7')
    
    #   The two JOINs:
    stmt = """select a3table1.suppnum, a3table1.suppname
, a3table2.address , a3table2.city , a3table2.state
from       a3table2 
left  join a3table1 
on cast(a3table1.suppnum as char(20)) =
cast(a3table2.suppnum as varchar(20))
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s8')
    stmt = """select a3table1.suppnum, a3table1.suppname
, a3table2.address
, a3table2.city   , a3table2.state
from       a3table1 
left  join a3table2 
on cast(a3table1.suppnum as numeric (3)) =
cast(a3table2.suppnum as numeric (3))
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s9')
    
    #   The UNION:
    stmt = """select a3table1.suppnum, a3table1.suppname
, a3table2.address
, a3table2.city   , a3table2.state
from       a3table2 
left  join a3table1 
on cast(a3table1.suppnum as char(20)) =
cast(a3table2.suppnum as varchar(20))    

union    

select a3table1.suppnum, a3table1.suppname
, a3table2.address
, a3table2.city   , a3table2.state
from       a3table1 
left  join a3table2 
on cast(a3table1.suppnum as numeric (3)) =
cast(a3table2.suppnum as numeric (3))
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s10')
    
    #  The insert using UNION of LEFT JOINs:
    stmt = """insert into a3table6 
select a3table1.suppnum, a3table1.suppname
, a3table2.address
, a3table2.city   , a3table2.state
from       a3table2 
left  join a3table1 
on cast(a3table1.suppnum as char(20)) =
cast(a3table2.suppnum as varchar(20))    

union    

select a3table1.suppnum, a3table1.suppname
, a3table2.address
, a3table2.city   , a3table2.state
from       a3table1 
left  join a3table2 
on cast(a3table1.suppnum as numeric (3)) =
cast(a3table2.suppnum as numeric (3))
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 7)
    
    stmt = """select * from a3table6 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s11')
    
    #   Insert using UNION of LEFT and INNER JOIN (see far below!):
    
    #   The two simple selects:
    stmt = """select a3table1.suppnum, a3table1.suppname
from       a3table1 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s12')
    stmt = """select a3table2.address , a3table2.city , a3table2.state
from       a3table2 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s13')
    
    #   The two JOINs:
    
    stmt = """select        a.suppnum,        a.suppname
,        b.address
,        b.city   ,        b.state
from       a3table1 a
left  join a3table2 b
on        a.suppnum =        b.suppnum
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s14')
    
    stmt = """select a3table1.suppnum, a3table1.suppname
, a3table2.address
, a3table2.city   , a3table2.state
from        a3table2 
inner join  a3table1 
on a3table1.suppnum = a3table2.suppnum
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s15')
    
    #   The UNION:
    
    stmt = """select        a.suppnum,        a.suppname
,        b.address
,        b.city   ,        b.state
from       a3table1 a
left  join a3table2 b
on        a.suppnum =        b.suppnum    

union    

select a3table1.suppnum, a3table1.suppname
, a3table2.address
, a3table2.city   , a3table2.state
from        a3table2 
inner join  a3table1 
on a3table1.suppnum = a3table2.suppnum
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s16')
    
    #   From Test unit SQLT149, case a7.
    #   Show base tables:
    stmt = """select a.char_1 , a.char_10 , a.binary_signed
, a.pic_comp_1 , a.small_int
from      """ + gvars.g_schema_arkcasedb + """.btsel01 a
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s17')
    stmt = """select cast (a.char_1        as varchar( 5) )
, cast (a.char_10       as varchar( 7) )
, cast (a.binary_signed as varchar(10) )
, cast (a.pic_comp_1    as varchar(10) )
, cast (a.small_int     as varchar(10) )
from      """ + gvars.g_schema_arkcasedb + """.btsel01 a
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s18')
    stmt = """select cast (b.char_1        as varchar( 5) )
, cast (b.pic_x_8       as varchar( 7) )
, cast (b.binary_signed as varchar(10) )
, cast (b.pic_comp_1    as varchar(10) )
, cast (b.small_int     as varchar(10) )
from      btre201 b
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s19')
    
    #   JOIN with some columns from global database:
    stmt = """log """ + defs.work_dir + """/a03s20log cmdtext off, clear;"""
    output = _dci.cmdexec(stmt)
    stmt = """select a.char_1 , a.char_10
, b.char_1 , b.pic_x_8
from      """ + gvars.g_schema_arkcasedb + """.btsel01 a
left join btre201 b
on  cast (a.char_1 as varchar( 5) )
= cast (b.char_1 as varchar( 5) )
and cast (a.char_10 as varchar( 7) )
= cast (b.pic_x_8  as varchar( 7) )
and cast (a.binary_signed as varchar(10) )
= cast (b.binary_signed as varchar(10) )
and cast (a.pic_comp_1 as varchar(10) )
= cast (b.pic_comp_1 as varchar(10) )
and cast (a.small_int as varchar(10) )
= cast (b.small_int as varchar(10) )
;"""
    output = _dci.cmdexec(stmt)
    stmt = """log off;"""
    output = _dci.cmdexec(stmt)
    output = _testmgr.shell_call("""cat """ + defs.work_dir + """/a03s20log | grep -e WARNING | cut -c 1-81 | uniq""")
    _dci.expect_warning_msg(output, '8402')
    
    output = _testmgr.shell_call("""cat """ + defs.work_dir + """/a03s20log | sed '/WARNING/d'""")
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s20')
    
    #  JOIN with many columns from global database:
    stmt = """select a.char_1 ,  a.char_10 , b.char_1 , b.pic_x_8
, b.ordering
from      """ + gvars.g_schema_arkcasedb + """.btsel01 a
,         btre201 b
where  cast (a.char_1 as varchar( 5) )
= cast (b.char_1 as varchar( 5) )
and cast (a.char_10 as varchar( 7) )
= cast (b.pic_x_8  as varchar( 7) )
and cast (a.pic_x_1 as varchar( 2) )
= cast (b.var_char_2 as varchar( 2) )
and cast (a.binary_signed as varchar(10) )
= cast (b.binary_signed as varchar(10) )
and cast (a.binary_32_u  as varchar(10) )
= cast (b.binary_32_u  as varchar(10) )
and cast (a.binary_64_s  as varchar(10) )
= cast (b.binary_64_s  as varchar(10) )
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """select a.char_1 , a.char_10 , b.char_1 , b.pic_x_8
, b.ordering
from      """ + gvars.g_schema_arkcasedb + """.btsel01 a
,         btre201 b
where cast (a.pic_comp_1 as char(13) )
= cast (b.pic_comp_1 as char(13) )
or cast (a.pic_comp_2 as char( 6) )
= cast (b.pic_comp_2 as varchar( 6) )
or cast (a.pic_comp_3 as char(12) )
= cast (b.pic_comp_3 as varchar(12) )
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s21a')
    stmt = """select a.char_1 , a.char_10 , b.char_1 , b.pic_x_8
, b.ordering
from      """ + gvars.g_schema_arkcasedb + """.btsel01 a
,         btre201 b
where cast (a.small_int  as char(10) )
= cast (b.small_int  as char(10) )
or cast (a.medium_int as char(10) )
= cast (b.medium_int as char(10) )
or cast (a.large_int  as char(20) )
= cast (b.large_int  as char(20) )
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """select a.char_1 , a.char_10 , b.char_1 , b.pic_x_8
, b.ordering
from      """ + gvars.g_schema_arkcasedb + """.btsel01 a
,         btre201 b
where cast (a.decimal_1 as char(20) )
= cast (b.decimal_1 as char(20) )
or cast (a.decimal_2_signed as char(20) )
= cast (b.decimal_2_signed as char(20) )
or cast (a.decimal_3_unsigned as char(20) )
= cast (b.decimal_3_unsigned as char(20) )
or cast (a.pic_decimal_1 as char(20) )
= cast (b.pic_decimal_1 as char(20) )
or cast (a.pic_decimal_2 as char(20) )
= cast (b.pic_decimal_2 as char(20) )
or cast (a.pic_decimal_3 as char(20) )
= cast (b.pic_decimal_3 as char(20) )
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s22')
    
    stmt = """select a.char_1 , a.char_10 , b.char_1 , b.pic_x_8
, b.ordering
from      """ + gvars.g_schema_arkcasedb + """.btsel01 a
left join btre201 b
on cast (a.char_1        as char(20) )
= cast (b.char_1         as char(20) )
or cast (a.char_10       as char(20) )
= cast (b.pic_x_8        as char(20) )
or cast (a.pic_x_1       as char(20) )
= cast (b.var_char_2     as char(20) )
or cast (a.binary_signed as char(20) )
= cast (b.binary_signed  as char(20) )
or cast (a.binary_32_u   as char(20) )
= cast (b.binary_32_u    as char(20) )
or cast (a.binary_64_s   as char(20) )
= cast (b.binary_64_s    as char(20) )
or cast (a.pic_comp_1    as char(20) )
= cast (b.pic_comp_1     as char(20) )
or cast (a.pic_comp_2    as char(20) )
= cast (b.pic_comp_2     as char(20) )
or cast (a.pic_comp_3    as char(20) )
= cast (b.pic_comp_3     as char(20) )
or cast (a.small_int     as char(20) )
= cast (b.small_int      as char(20) )
or cast (a.medium_int    as char(20) )
= cast (b.medium_int     as char(20) )
or cast (a.large_int     as char(20) )
= cast (b.large_int      as char(20) )
or cast (a.decimal_1     as char(20) )
= cast (b.decimal_1      as char(20) )
or cast (a.decimal_2_signed   as char(20) )
= cast (b.decimal_2_signed   as char(20) )
or cast (a.decimal_3_unsigned as char(20) )
= cast (b.decimal_3_unsigned as char(20) )
or cast (a.pic_decimal_1 as char(20) )
= cast (b.pic_decimal_1 as char(20) )
or cast (a.pic_decimal_2 as char(20) )
= cast (b.pic_decimal_2 as char(20) )
or cast (a.pic_decimal_3 as char(20) )
= cast (b.pic_decimal_3 as char(20) )
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s23')
    
    # ----------------------------
    # Cleanup:
    # ----------------------------
    
    stmt = """drop table a3table1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table a3table2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table a3table3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table a3table4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table a3table5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table a3table6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table a3table7;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table a3table8;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table oja(a int not null, primary key (a));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table ojb(b int not null, primary key (b));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table ojc(c int not null, primary key (c));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select a,c
from ojb inner join ojc on b = c,
 oja where a = c ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """drop table oja;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table ojb;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table ojc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test004(desc="""a04"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0203 : A04
    #  Description:        This test verifies insert statements with
    #                      params as NULL in indicator.
    #                      Since indicator is nor supported, those
    #                      SQLCI statements using indicator have
    #                      been commented out.
    #  Test case inputs:   --
    #  Test case outputs:  --
    #  Expected Results:   same as above.
    #
    #  Notes:
    #  This test case incorporates features detailed in the "Title"
    #  by Ima Programmer (Version 1.1, <date>).
    #
    # =================== End Test Case Header  ===================
    # --------------------------------
    # Create the Log file.
    # --------------------------------
    
    # ---------------------------
    # Move to volume for temporary SQL objects:
    # ---------------------------
    # VOLUME ;
    # CATALOG ;
    
    stmt = """create table a4table1 
(varchar7 varchar(7) ) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #catalog ;
    
    stmt = """set param  ?p1 'abcdefg' ;"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into a4table1 (varchar7)
values(cast(?p1 as varchar(7)) ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """set param  ?p2a 'angle'   ;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param  ?p2b 'bangle'   ;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param  ?p2d 'dangle'   ;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param  ?p3 2         ;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param  ?pm -1        ;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into a4table1 (varchar7)
values(cast(?p2a as char(7)              ) ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into a4table1 (varchar7)
values(cast(?p2b as char(6) ) ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    #    insert into a4table1 (varchar7)
    #               values(cast(?p2d indicator ?pm as char(5) ) ) ;
    
    stmt = """insert into a4table1 (varchar7)
values(cast(?p2d as char(5) ) ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    stmt = """set param  ?p4 'black'   ;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into a4table1 (varchar7)
values(cast(?p4 as varchar(7) ) ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #   insert into a4table1 (varchar7)
    #              values(cast(?p4 indicator ?p3 as varchar(7) ) ) ;
    # The following gives an error - Indicator must be a parameter
    # alone:
    #   insert into a4table1 (varchar7)
    #              values(cast(?p4
    #              indicator cast(?p3 as smallint) as varchar(7)
    #              ) ) ;
    
    stmt = """set param  ?hvnlo  40 ;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param  ?hvch2  2  ;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param  ?hvchm  -9 ;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into a4table1 (varchar7)
values(cast(?hvnlo as varchar(7)) ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    #     insert into a4table1 (varchar7)
    #        values(cast(?hvnlo indicator ?hvch2 as varchar(7) ) ) ;
    #     insert into a4table1 (varchar7)
    #        values(cast(?hvnlo indicator ?hvchm as varchar(7) ) ) ;
    #
    #  ----------------------------
    #  Cleanup:
    #  ----------------------------
    stmt = """select * from a4table1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s1')
    stmt = """drop table a4table1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test005(desc="""a05"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0203 : A05
    #  Description:        IS NULL and IS NOT NULL.
    #                      additional null tests.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    #  Notes:
    #  This test case incorporates features detailed in the "Title"
    #  by Ima Programmer (Version 1.1, <date>).
    # =================== End Test Case Header  ===================
    #
    # set catalog ;
    # set schema  ;
    stmt = """select char_1, ordering from
 btre201 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s0')
    
    stmt = """select char_1, ordering from
 btre201 
where cast (char_1 as varchar(3)) is null ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s1')
    
    stmt = """select char_1, ordering from btre201 
where cast (char_1 as varchar(3)) is null
or    cast (char_1 as varchar(3)) is not null ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s2')
    
    stmt = """select char_1, ordering from btre201 
where cast ('1' as varchar(3)) is null
or    cast ('1' as varchar(3)) is not null ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s3')
    
    _testmgr.testcase_end(desc)

def test006(desc="""a06"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0203 : A06
    #  Description:        Special characters in param values.
    #
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   As above.
    #
    #  Notes:
    #  This test case incorporates features detailed in the "Title"
    #  by Ima Programmer (Version 1.1, <date>).
    #
    # =================== End Test Case Header  ===================
    # --------------------------------
    # Create the Log file.
    # --------------------------------
    
    # ---------------------------
    # Move to volume for temporary SQL objects:
    # ---------------------------
    # VOLUME  ;
    # CATALOG  ;
    # ---------------------------
    
    stmt = """set param ?h 1.2 ;"""
    output = _dci.cmdexec(stmt)
    stmt = """show param;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select char_1 from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s0')
    
    stmt = """select char_1, cast(+?h as integer)
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s1')
    
    stmt = """select char_1
from btre204 
where cast(+?h as integer) > 3 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """select char_1, cast(+?h as largeint)
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s2')
    
    stmt = """select char_1, cast(+?h as char(8))
from btre204 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s3')
    stmt = """select char_1, cast(+?h as char(7))
from btre204 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s4')
    stmt = """select char_1, cast(+?h as pic s99999v9999999      )
from btre204 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s5')
    stmt = """select char_1, cast(+?h as pic s99999v9999999 comp )
from btre204 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s6')
    stmt = """select char_1, cast(+?h as decimal (12,6) )
from btre204 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s7')
    stmt = """select char_1, cast(+?h as float (4) )
from btre204 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s8')
    stmt = """select char_1
from btre204 
where cast(+?h as float(4) ) > 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    _testmgr.testcase_end(desc)

def test007(desc="""a07"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0203 : A07
    #  Description:        CAST with VIEW columns.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   As above.
    #
    #  Notes:
    #  This test case incorporates features detailed in the "Title"
    #  by Ima Programmer (Version 1.1, <date>).
    #
    # =================== End Test Case Header  ===================
    
    stmt = """drop view pvre201;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create view pvre201 as
select ordering , alwaysnull , char_1
from btre201 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from pvre201 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s1')
    
    stmt = """select cast(ordering as char(5))
, cast(alwaysnull as int)
, cast(char_1 as varchar(3))
from pvre201 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s2')
    
    stmt = """insert into pvre201 values (
cast ('9' as int)
, null
, cast(8 as varchar(1))
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select * from pvre201 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s3')
    
    stmt = """drop view pvre201b;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create view pvre201b as
select ordering, small_int, y_to_d
from btre201 
where small_int is NOT NULL and
y_to_d = date '1975-01-01'
--       catalog
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from pvre201b ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """select cast(ordering as char(5))
, cast(small_int as int)
, cast(y_to_d as varchar(10) )
from pvre201b ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """insert into pvre201b values (
cast ('10' as int)
, cast ('   10   ' as int)
--        , cast('01-01-01' as date)
, cast('1998-01-01' as date)
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select * from pvre201b ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """drop view pvre201c;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create view pvre201c as
select ordering, small_int, var_char_3
from btre201 
where small_int is NULL
--     catalog
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from pvre201c ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s6')
    
    stmt = """select cast(ordering as char(5))
, cast(small_int as int)
, cast(var_char_3 as varchar(3) )
from pvre201c ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s7')
    
    stmt = """update pvre201c 
set small_int = cast (' -3 ' as int)
, var_char_3 = cast (' 4.' as varchar(3))
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 4)
    
    stmt = """select * from pvre201c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """drop view pvre204a;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create view pvre204a as
select ordering, time1, float_real
from btre204 
where ordering is NOT NULL
and time1 is NOT NULL
and float_real is NOT NULL
--       catalog
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from pvre204a ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s9')
    
    stmt = """select cast(ordering as char(5))
, cast(time1    as char(8))
, cast(float_real as varchar(20) )
from pvre204a ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s10')
    
    #   Columns underlying view are required to be NOT NULL => insert
    #   rejected (correctly):
    stmt = """insert into pvre204a values (
cast ('13' as int)
, cast ('10:11:12' as time)
, cast('  - 1e5 ' as real)
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4027')
    stmt = """select * from pvre204a ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s12')
    
    stmt = """drop view svre201;"""
    output = _dci.cmdexec(stmt)
    stmt = """create view svre201 as
select ordering , alwaysnull , btre201.char_1
, btre202.small_int , btre202.medium_int
from btre201, btre202 
--        catalog
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from svre201 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s14')
    
    stmt = """select cast(ordering as char(5))
, cast(alwaysnull as int)
, cast(char_1     as varchar(8) )
, cast(small_int  as varchar(8) )
, cast(medium_int as varchar(8) )
from svre201 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s15')
    
    stmt = """drop view svre201b;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create view svre201b as
select t2.ordering,t2.float_basic,t2.y_to_d,t1.ih_to_s
from btre201 t1,
 btre204 t2
where t1.ih_to_s = t2.ih_to_s
--     catalog
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    ##process mpci
    #select * from \$blue01.mxd0203.svre201;
    
    ##process defsqlcimx
    stmt = """select * from svre201b ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """select cast(ordering as char(5))
, cast(float_basic as int)
, cast(y_to_d as varchar(10))
--         cannot cast interval!
from svre201b ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """drop view svre201c;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create view svre201c as
select ordering, alwaysnull,char_1
from btre201 
where alwaysnull IS NULL
and char_1 IS NOT NULL
and ordering = 4
--      catalog
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    ##process mpci
    #select * from \$blue01.mxd0203.svre201;
    
    ##process defsqlcimx
    stmt = """select * from svre201c ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """select cast(ordering as char(5))
, cast(alwaysnull as int)
, cast(char_1 as varchar(8) )
from svre201c ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """drop view svre201d;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create view svre201d 
(small_int, float_basic, y_to_d) as
select ordering,float_basic,y_to_d
from btre201 
union all
select small_int,float_basic,y_to_d
from btre202 
union all
select ordering,float_basic,y_to_d
from btre204 
--       catalog
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    ##process mpci
    #select * from \$blue01.mxd0203.svre201;
    
    ##process defsqlcimx
    stmt = """select * from svre201d ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s19')
    
    stmt = """select cast(small_int as char(5))
, cast(float_basic as varchar(20))
, cast(y_to_d as varchar(10))
from svre201d ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s20')
    
    stmt = """drop view svre201e;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create view svre201e as
select t1.var_char_3,t1.pic_comp_3,t1.ih_to_s,t2.y_to_d
from btre201 t1
left join
 btre202 t2
on t1.y_to_d = t2.y_to_d
--        catalog
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    ##process mpci
    #select * from \$blue01.mxd0203.svre201;
    
    ##process defsqlcimx
    stmt = """select * from svre201e ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s22')
    
    #  Around Jan/99 The query below did not give the expected results
    #  See the following bug for more details:
    #  Cast of char(3) into char(1) works through a view
    #          1) The select from table as well as view works correctly in both
    #          cases. It returns a string truncation warning from the CAST when
    #          selected from table and doesn't return when selected from view.
    #          A returned warning is different than a returned error: the former
    #          is a successful completion whereas the latter is not.
    #          2) It is rare and not advisable to use a cast to truncate data.
    #          3) truncation warnings are useful when data is being inserted or
    #          updated, or when it is being fetched into a hostvar in a program.
    #          In all these cases, truncation warning is returned correctly.
    #          The reason for this regression is that the access plan got changed.
    #          And the hash join operator was not propagating the warnings correctly.
    
    stmt = """select cast(var_char_3 as char(1))
, cast(pic_comp_3 as varchar(9))
--        cannot cast interval!
, cast(y_to_d     as varchar(10))
from svre201e ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s23')
    
    _testmgr.testcase_end(desc)

def test008(desc="""a08"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0203 : A08
    #  Description:        CAST with params and PREPARE/EXECUTE.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   As above.
    #
    #  Notes:
    #  This test case incorporates features detailed in the "Title"
    #  by Ima Programmer (Version 1.1, <date>).
    #
    # =================== End Test Case Header  ===================
    
    # ---------------------------
    # Move to volume for temporary SQL objects:
    # ---------------------------
    # VOLUME ;
    # CATALOG ;
    
    stmt = """create table a8table1 
( float_basic         float (4)
default null
, float_double_p      float (54)              default null
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    _dci.expect_complete_msg(output)
    _dci.expect_complete_msg(output)
    _dci.expect_complete_msg(output)
    _dci.expect_complete_msg(output)
    _dci.expect_complete_msg(output)
    _dci.expect_complete_msg(output)
    _dci.expect_complete_msg(output)
    _dci.expect_complete_msg(output)
    _dci.expect_complete_msg(output)
    # catalog
    
    stmt = """set param  ?a '9';"""
    output = _dci.cmdexec(stmt)
    stmt = """prepare p   from insert into a8table1 
(float_double_p) values(cast((?a + 0) as float( 20   )) ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """execute p;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """set param  ?a 1;"""
    output = _dci.cmdexec(stmt)
    stmt = """prepare p   from insert into a8table1 
(float_double_p) values(cast((?a + 0) as float( 20   )) ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """execute p;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """set param  ?hvch1 '9' ;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare p1  from insert into a8table1 
(float_double_p) values(cast( ?hvch1 as float( 20   )) ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """execute p1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """set param  ?hvnin 1 ;"""
    output = _dci.cmdexec(stmt)
    stmt = """prepare p2  from insert into a8table1 
(float_double_p) values(cast( ?hvnin as float( 20   )) )  ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """execute p2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """set param  ?c  '9' ;"""
    output = _dci.cmdexec(stmt)
    stmt = """prepare q   from  insert into a8table1 
(float_double_p) values (cast( ?c  as float(20)) )  ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """execute q;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """set param  ?c  1;"""
    output = _dci.cmdexec(stmt)
    stmt = """prepare q   from  insert into a8table1 
(float_double_p) values (cast( ?c  as float(20)) )  ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """execute q;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """set param  ?c  a;"""
    output = _dci.cmdexec(stmt)
    stmt = """prepare q   from  insert into a8table1 
(float_double_p) values (cast( ?c  as float(20)) )  ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """execute q;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '29433')
    
    stmt = """set param  ?c  'b';"""
    output = _dci.cmdexec(stmt)
    stmt = """prepare q   from  insert into a8table1 
(float_double_p) values (cast( ?c  as float(20)) )  ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """execute q;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '29433')
    
    stmt = """set param  ?c  :hv;"""
    output = _dci.cmdexec(stmt)
    stmt = """prepare q   from  insert into a8table1 
(float_double_p) values (cast( ?c  as float(20)) )  ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """execute q;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '29433')
    
    stmt = """set param  ?r '(cast( 1  as float(20)) )' ;"""
    output = _dci.cmdexec(stmt)
    stmt = """prepare r from insert into a8table1 
(float_double_p) values ( ?r ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """execute r;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '29433')
    
    stmt = """insert into a8table1 
(float_double_p) values ( (cast( 1  as float(20)) ) );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """set param  ?p1 1 ;"""
    output = _dci.cmdexec(stmt)
    stmt = """prepare r   from insert into a8table1 
(float_double_p) values ( cast ( ?p1 as float(20)) )  ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """execute r;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """set param  ?p1 2 ;"""
    output = _dci.cmdexec(stmt)
    stmt = """prepare r   from insert into a8table1 
(float_double_p) values ( cast ( ?p1 as float(20)) )  ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """execute r;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into a8table1 
(float_double_p) values ( (cast( 1  as float(20)) ) );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select * from a8table1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s4')
    
    stmt = """create table a8table2 
( c pic xxx, v varchar(2) ) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #      catalog
    
    stmt = """set param  ?a '1';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param  ?b '2';"""
    output = _dci.cmdexec(stmt)
    stmt = """prepare s   from
insert into a8table2 
values(cast(?a as pic x(1)),cast(?b as pic x(2)) );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """set param  ?a 3;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param  ?b '4';"""
    output = _dci.cmdexec(stmt)
    stmt = """prepare s   from
insert into a8table2 
values(cast(?a as pic x(1)),cast(?b as pic x(2)) );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select * from a8table2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s5')
    
    # ----------------------------
    # Cleanup:
    # ----------------------------
    
    stmt = """drop table a8table1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table a8table2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

