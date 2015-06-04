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
    #  Test case name:     A01
    #  Description:        This test verifies the SQL <specify>
    #                      feature.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    
    # Table BTRE209 - a table with columns like btre202
    #                 (one of each data type and default null);
    #                 values defined for CAST tests (T199, T200)
    #                 particularly with numbers in character cols.
    
    stmt = """create table btre209 (
char_1              char(1)                 default null
, var_char_3          varchar(3)              default null
, small_int           smallint                default null
, medium_int          integer unsigned        default null
, large_int           largeint signed         default null
, float_basic         float (4)               default null
, y_to_d              date                    default null
) no partition
--  organization r
--  organization key sequenced
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #-------------------------
    #  Insert:
    #-------------------------
    stmt = """insert into btre209 
values (
'1' , '123'
, 3  , 4     , 5
, 6.2
,date '1991-09-28'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into btre209 
values (
'2' , '246'
, 33 , 44    , 5
, 66.2
,date '1991-12-27'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into btre209 
values (
'3' , '333'
, 333, 333   , 333
, 333.0
,date '1933-03-03'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into btre209 (char_1) values ( NULL ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #-------------------------
    # Load small_int, medium_int, and large_int with largest
    # positive integer values.
    #-------------------------
    stmt = """insert into btre209 
values (
'5' , '55'
, 32767, 2147483647 , 9223372036854775807
, 333.0
, date '1999-12-12'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #-------------------------
    # Load small_int and large_int with largest
    # negative integer values.
    #-------------------------
    stmt = """insert into btre209 
values (
'9' , '999'    
, -32768, 0 , -9223372036854775808
, -5125e-1
, date '2000-01-01'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #     update all statistics for table btre209 ;
    #     update statistics for table btre209 ;
    
    stmt = """select * from btre209 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s0')
    
    _testmgr.testcase_end(desc)

def test002(desc="""a02"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    # Test case name:	pretsta02
    # Description:		This test creates the table btre202, and btre204,
    #			and inserts the values into the table. Also created
    #			views pvre201, pvre201b, pvre204a, svre201.
    # Expected Results:
    
    
    stmt = """drop table btre202;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table btre202 (
char_1              char(1)                 default null
, var_char_3          varchar(3)              default null
, small_int           smallint                default null
, medium_int          integer unsigned        default null
, large_int           largeint                default null
, float_basic         float (4)               default null
, y_to_d              date                default null
) no partition
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into btre202 
values (
'C' ,'rum'
,9000 ,1000 ,2000
,1.2
,date '1975-01-01'
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into btre202 (char_1) values ( NULL ) ;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """update statistics for table btre202 on every column;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select * from btre202 order by char_1;"""
    output = _dci.cmdexec(stmt)
    
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
;"""
    output = _dci.cmdexec(stmt)
    
    #  Create INDEXES for table BTRE201.
    stmt = """create index btre201a 
on btre201 (ordering)
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create index btre201b 
on btre201 (char_1, alwaysnull, binary_signed)
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create index btre201c 
on btre201 (var_char_3, large_int)
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create index btre201d 
on btre201 (decimal_3_unsigned, pic_decimal_1)
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create index btre201e 
on btre201 (pic_x_8, iy_to_mo, y_to_d, medium_int)
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create index btre201f 
on btre201 (ih_to_s)
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create index btre201g 
on btre201 (time1 DESC, float_real ASC, pic_comp_3)
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create index btre201h 
on btre201 (y_to_d_2 DESC)
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create index btre201i 
on btre201 (float_double_p ASC)
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create index btre201j 
on btre201 (h_to_f)
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create index btre201k 
on btre201 (decimal_1, pic_decimal_3 DESC)
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create index btre201l 
on btre201 (decimal_2_signed ASC, small_int DESC,
var_char_2, binary_32_u, pic_comp_1,
float_basic DESC)
;"""
    output = _dci.cmdexec(stmt)
    stmt = """create index btre201m 
on btre201 (pic_comp_2, binary_64_s)
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
    
    stmt = """create view pvre201 as
select ordering , alwaysnull , char_1
from btre201 
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select * from pvre201 
order by ordering;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create view pvre201b as
select ordering, small_int, y_to_d
from btre201 
where small_int is NOT NULL and
y_to_d = date '1975-01-01'
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select * from pvre201b 
order by ordering;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create view svre201 as
select ordering , alwaysnull , btre201.char_1
, btre202.small_int , btre202.medium_int
from btre201, btre202;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select * from svre201 
order by ordering;"""
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
    
    stmt = """update statistics for table btre204 on every column;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select * from btre204 
order by ordering;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create view pvre204a as
select ordering, time1, float_real
from btre204 
where ordering is NOT NULL
and time1 is NOT NULL
and float_real is NOT NULL
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select * from pvre204a 
order by ordering;"""
    output = _dci.cmdexec(stmt)
    
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     A02
    #  Description:        CAST at all places where expressions can appear.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    
    #----------------------
    # Initialize parameters:
    #----------------------
    stmt = """set param ?a1param1 1  ;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?a1param2 6.2 ;"""
    output = _dci.cmdexec(stmt)
    
    # ----------------------
    #  create temporary table with column name cast:
    # ----------------------
    
    stmt = """drop   table a1table1;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table a1table1 ( cast1 pic x ) no partition ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into a1table1 values ( 'a' );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a1table1 (cast1) values ( 'b' );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """select *    from a1table1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s1')
    stmt = """select cast1 from a1table1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s2')
    stmt = """select cast(cast1 as pic xx) from a1table1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s3')
    
    stmt = """drop   table a1table1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # ----------------------
    #  select list, 1 table.
    # ----------------------
    
    #  literal:
    stmt = """select cast ( '   123   ' as int   )
from btre202;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s4')
    
    #  one col; convert to same then different data type:
    stmt = """select        small_int
from btre202;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s5')
    stmt = """select cast ( small_int   as smallint )
from btre202;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s6')
    stmt = """select cast ( small_int   as float    )
from btre202;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s7')
    
    #  all cols; convert to same then different data type:
    
    stmt = """select * from btre202 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s8')
    
    stmt = """select cast ( char_1      as char(1)    )
, cast ( var_char_3  as varchar(3) )
, cast ( small_int   as smallint   )
, cast ( medium_int  as integer    )
, cast ( large_int   as largeint   )
, cast ( float_basic as float(4)   )
, cast ( y_to_d      as date       )
from btre202 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s9')
    
    #  all cols; convert to different data type:
    stmt = """select * from btre209 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s10')
    
    stmt = """select cast ( char_1      as smallint )
, cast ( var_char_3  as smallint )
, cast ( small_int   as float )
, cast ( medium_int  as float )
, cast ( large_int   as float )
, cast ( float_basic as real  )
, cast ( y_to_d      as char(10) )
from btre209 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s11')
    
    # ----------------------
    #  select list, multiple tables:
    # ----------------------
    stmt = """select        t2.small_int
,        t4.binary_32_u
, cast ( t2.small_int   as float    )
, cast ( t4.binary_32_u as smallint )
from btre202 t2 ,
 btre204 t4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s12')
    
    # ----------------------
    #  select predicate:
    # ----------------------
    #  where cast .. one col
    stmt = """select char_1      from btre209 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s13')
    stmt = """select char_1      from btre209 
where char_1 = cast ( 1 as pic x );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s14')
    
    stmt = """select var_char_3  from btre209 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s15')
    stmt = """select var_char_3  from btre209 
where cast ( 123 as varchar(3) ) = var_char_3 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s16')
    stmt = """select var_char_3  from btre209 
where var_char_3 = cast ( 246 as pic xxx );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s17')
    
    stmt = """select small_int   from btre209 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s18')
    stmt = """select small_int   from btre209 
where small_int = cast ( '3' as smallint );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s19')
    
    stmt = """select medium_int  from btre209 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s20')
    stmt = """select medium_int  from btre209 
where medium_int = cast ( '44' as integer );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s21')
    
    stmt = """select large_int   from btre209 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s22')
    
    stmt = """select large_int   from btre209 
where large_int = cast ( '5' as largeint );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s23')
    
    stmt = """select float_basic , cast ( float_basic as float ) ,
cast( '66.2' as float ) from btre209 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s24')
    
    stmt = """select float_basic from btre209 
where float_basic = cast ( '66.2' as float );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    
    stmt = """select y_to_d      from btre209 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s25')
    stmt = """select y_to_d      from btre209 
where cast ( '1991-12-01' as date ) = y_to_d ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """select *
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s26')
    
    stmt = """select cast(date '01/01/1990'    as timestamp)
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s27')
    #   select cast(time1            as datetime minute to second )
    #      from btre204 ;
    
    # where cast .. many cols
    stmt = """select * from btre209 
where char_1      = cast ( 1 as pic x )
and var_char_3  = cast ( 123 as varchar(3) )
and small_int   = cast ( '3' as smallint )
and medium_int  = cast ( '4' as integer )
and large_int   = cast ( '5' as largeint )
and cast ( '1991-01-01' as date ) = y_to_d
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    #  cast on views - select list and where predicate
    stmt = """select        ordering
,        alwaysnull
,        char_1
from pvre201;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s28')
    
    stmt = """select cast ( ordering   as float   )
, cast ( alwaysnull as char    )
--         , cast ( char_1     as varchar )
, cast ( char_1     as varchar(3) )
from pvre201;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s29')
    
    stmt = """select        small_int
,        y_to_d
from pvre201b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """select cast ( small_int  as float   )
, cast ( y_to_d     as char(15))
from pvre201b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """select        time1
,        float_real
from pvre204a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s30')
    
    stmt = """select cast ( time1      as varchar(13) )
, cast ( float_real as largeint)
from pvre204a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s31')
    
    # AR 2/7/07 Added order by
    stmt = """select        char_1
,        small_int
,        medium_int
from svre201 order by char_1,small_int,medium_int;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s32')
    
    stmt = """select cast ( char_1     as varchar(3) )
, cast ( small_int  as char(15))
, cast ( medium_int as char(15))
from svre201 order by 1,2,3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s33')
    
    stmt = """show param;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select ?a1param1 from btre209 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s34')
    
    stmt = """select cast ( ?a1param1 as integer )
from btre209 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s35')
    
    stmt = """select float_basic, cast ( ?a1param2 as real )
from btre209 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s36')
    
    stmt = """select float_basic, cast ( ?a1param2 as float )
from btre209 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s37')
    
    stmt = """select * from btre209 
where float_basic = cast ( ?a1param2 as float )
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    
    stmt = """create table a1table1 (
char_1              char(1)                 default null
, var_char_3          varchar(3)              default null
, small_int           smallint                default null
, medium_int          integer unsigned        default null
, large_int           largeint signed         default null
, float_basic         float (4)               default null
, y_to_d              date                    default null
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #----------------------
    # insert list, casting to same data type:
    #----------------------
    stmt = """insert into a1table1 (
char_1
, var_char_3
, small_int
, medium_int
, large_int
, float_basic
, y_to_d
)    

values (
cast ( 'a'             as char(1)  )
, cast ( 'bc'            as pic xx   )
, cast ( 3               as smallint )
, cast ( 4               as int unsigned )
, cast ( 5               as largeint signed )
, cast ( 6               as float (4) )
, cast ( date '01/01/1980' as date     )
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """select * from a1table1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s38')
    
    #  QA has protested removal of truncation warning:
    stmt = """insert into a1table1 (
char_1
, var_char_3
, small_int
, medium_int
, large_int
, float_basic
, y_to_d
)
values (
cast ( 'xyz'           as char(1)  )
, cast ( 'qrs'           as pic xx   )
, cast ( 7               as smallint )
, cast ( 1               as int unsigned )
, cast ( 52              as largeint signed )
, cast ( 62              as float (4) )
, cast ( timestamp '01/01/1980 12:30:00' as date )
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """select * from a1table1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s40')
    
    #----------------------
    # insert list, casting to different data type:
    #----------------------
    stmt = """insert into a1table1 (
char_1
, var_char_3
, small_int
, medium_int
, large_int
, float_basic
, y_to_d
)
values (
cast ( 0               as char(1)  )
, cast ( 2               as pic xx   )
, cast ( '3'             as smallint )
, cast ( '1'             as int unsigned )
, cast ( ' 5 '           as largeint signed )
, cast ( '6e1'           as float (4) )
, cast ( '08/09/1989'      as date     )
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # insert cast param
    # show param ?a1param1 ;
    stmt = """show param;"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into a1table1 ( small_int )
values ( cast(?a1param1 as integer ) )
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """select * from a1table1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s41')
    
    # ----------------------
    #  update set list:
    # ----------------------
    #  Expect truncation warning:

    stmt = """update a1table1 
set var_char_3 = cast (date '1996-09-06' as varchar(3) )
where char_1 = 'a'
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8402')
    stmt = """select * from a1table1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s43')
    
    stmt = """show param;"""
    output = _dci.cmdexec(stmt)
    stmt = """update a1table1 
--     set var_char_3  = ?a1param1
set var_char_3 = cast(?a1param1 as varchar(3))
, medium_int  = cast ( ?a1param1 as int unsigned )
where char_1 = 'a'
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select * from a1table1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s44')
    
    # Expect truncation warning:
    stmt = """update a1table1 
set char_1      = cast ('a'             as pic x    )
, var_char_3  = cast ( 2              as pic xxx  )
, small_int   = cast ( '3'            as smallint )
, medium_int  = cast ( '4000'         as int unsigned )
, large_int   = cast ( '-5 '          as largeint signed )
, float_basic = cast ( 16e2           as float (4))
, y_to_d      = cast ( '12/12/1938'   as date     )
where char_1 = 'a'
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select * from a1table1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s45')
    
    #----------------------
    # update predicate:
    #----------------------
    stmt = """update a1table1 set char_1      = 'u'
where char_1      = cast ( 0 as pic x )
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select * from a1table1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s46')
    stmt = """update a1table1 
set small_int = cast ( '7' as smallint)
where char_1      = cast ( 'u' as pic x )
and var_char_3  = cast ( 2     as varchar(3) )
and small_int   = cast ( '3' as smallint )
and medium_int  = cast ( '1' as integer )
and large_int   = cast ( '5' as largeint )
and float_basic = cast ( '60' as float )
and cast ( '1989-08-09' as date ) = y_to_d
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select * from a1table1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s47')
    
    stmt = """update a1table1 set
var_char_3  = cast(?a1param1 as varchar(3))
where medium_int > cast ( ?a1param1 as int unsigned )
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select * from a1table1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s48')
    
    #----------------------
    # delete predicate:
    #----------------------
    # one col
    stmt = """delete from a1table1 
where small_int = cast ( '7' as integer ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 2)
    stmt = """select * from a1table1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s49')
    # many cols
    stmt = """delete from a1table1 
where char_1       = cast ( 0      as char(1) )
and var_char_3  = cast ( 1      as char(1) )
and small_int   = cast ( '3'    as smallint )
and medium_int  = cast ( '4'    as int unsigned )
and large_int   = cast ( ' 5 '  as largeint signed )
and float_basic = cast ( '6e1'  as float (4) )
and cast ( '1989-08-09' as date ) = y_to_d
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 0)
    stmt = """delete from a1table1 
where char_1       = cast ( 0      as char(1) )
and var_char_3  = cast ( 1      as char(1) )
and small_int   = cast ( '3'    as smallint )
and medium_int  = cast ( '4'    as int unsigned )
and large_int   = cast ( ' 5 '  as largeint signed )
and cast ( '1989-08-09' as date ) = y_to_d
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 0)
    stmt = """select * from a1table1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s50')
    # with param
    # show param ?a1param1 ;
    stmt = """show param;"""
    output = _dci.cmdexec(stmt)
    stmt = """delete from a1table1 
where large_int < cast ( ?a1param1 as largeint signed )
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    stmt = """select * from a1table1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s51')
    
    #----------------------
    # cleanup here:
    #----------------------
    
    stmt = """drop table a1table1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #  Above here, local database is being altered.
    
    # ----------------------
    #  with arithmetic operator
    # ----------------------
    stmt = """select char_1 , var_char_3
, cast ( char_1 as smallint )
+ cast ( var_char_3 as smallint )
from btre209;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s52')
    stmt = """select small_int , medium_int
, cast ( small_int   as float )
+ cast ( medium_int  as float )
from btre209;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s53')
    
    stmt = """select char_1, extract(year from y_to_d)
, cast ( char_1 as smallint ) +
cast(extract(year from y_to_d) as smallint)
from btre209;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s54')
    
    stmt = """select char_1 , var_char_3
, cast ( char_1 as smallint )
- cast ( var_char_3 as smallint )
from btre209;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s55')
    stmt = """select large_int , float_basic
, cast ( large_int   as float )
- cast ( float_basic as float )
from btre209;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s56')
    stmt = """select cast ( large_int   as float )
- cast ( float_basic as float )
from btre209;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s57')
    
    stmt = """select cast ( char_1 as smallint )
* cast ( var_char_3 as smallint )
from btre209;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s58')
    
    stmt = """select cast ( char_1 as smallint )
/ cast ( var_char_3 as smallint )
from btre209;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s59')
    #
    #  CAST picks a (18,6) as the format for the output.
    #  This causes an arithmetic error for the 999 ** 9
    #  value.
    #
    # ----------------------
    #  with logical operator (AND/OR/NOT)
    # ----------------------
    stmt = """select * from btre209;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s60')
    
    stmt = """select cast ( char_1 as smallint ) ,
cast ( var_char_3 as smallint )
from btre209;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s61')
    
    stmt = """select * from btre209 
where ( cast ( char_1 as smallint ) = 2 )
and ( cast ( var_char_3 as smallint ) = 246 )
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s62')
    stmt = """select * from btre209 
where ( cast ( extract ( year from y_to_d) as integer) = 1999 )
or ( cast ( small_int as largeint ) = 3 )
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s63')
    stmt = """select * from btre209 
where ( not cast (extract(year from y_to_d ) as smallint ) = 1991 )
or (     cast ( small_int as largeint ) = 3 )
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s64')
    stmt = """select * from btre209 
--  where ( cast ( y_to_d units year as smallint ) = 1991 )
where ( cast (extract(year from y_to_d ) as smallint ) = 1991 )
and not ( cast ( small_int as largeint ) = 3 )
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s65')
    stmt = """select * from btre209 
where cast ( small_int as largeint ) > 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s66')
    stmt = """select * from btre209 
where not cast ( small_int as largeint ) > 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s67')
    
    # ----------------------
    #  with like operator
    # ----------------------
    stmt = """select small_int , cast ( small_int as char(6) )
from btre209 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s68')
    stmt = """select small_int from btre209 
where cast ( small_int as char(6) ) like '3'
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """select small_int from btre209 
where cast ( small_int as char(6) ) like '3%'
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s69')
    stmt = """select small_int from btre209 
where '4' not like cast ( medium_int as char(10) )
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s70')
    stmt = """select small_int from btre209 
where cast ( small_int as char(6) )
like cast ( small_int as char(6) )
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s71')
    stmt = """select small_int from btre209 
where cast ( medium_int as char(10) )
not like cast ( medium_int as char(10) )
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    # ----------------------
    #  with between operator
    # ----------------------
    stmt = """select char_1, small_int, medium_int, large_int from btre209 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s72')
    stmt = """select small_int, medium_int from btre209 
where medium_int
between cast (small_int as int) and 40
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s73')
    stmt = """select small_int, medium_int from btre209 
where medium_int
not between cast (small_int as int) and 40
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s74')
    stmt = """select char_1, small_int, large_int from btre209 
where small_int
between cast (char_1 as smallint) and cast (large_int as largeint)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s75')
    stmt = """select char_1, small_int, large_int from btre209 
where cast ( small_int as int)
between cast (char_1 as smallint) and cast (large_int as largeint)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s76')
    stmt = """select char_1, small_int, large_int from btre209 
where cast ( small_int as int)
not between cast (char_1 as smallint) and cast (large_int as largeint)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s77')
    
    # ----------------------
    #  comparison predicate
    # ----------------------
    stmt = """select char_1, var_char_3, small_int, large_int
from btre209 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s78')
    
    stmt = """select char_1 from btre209 
where cast (large_int  as largeint) =  cast (large_int as largeint);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s79')
    
    stmt = """select char_1 from btre209 
where cast (large_int  as largeint) = cast (large_int as largeint);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s80')
    
    stmt = """select cast (var_char_3 as smallint)
from btre209 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s81')
    
    stmt = """select cast (char_1 as largeint)
from btre209 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s82')
    
    stmt = """select char_1 from btre209 
where cast (var_char_3 as smallint) <  cast (char_1 as largeint);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """select char_1 from btre209 
where cast (var_char_3 as smallint) >  cast (char_1 as largeint);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s83')
    
    stmt = """select char_1 from btre209 
where cast (large_int  as largeint ) <= cast (large_int as largeint);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s84')
    
    stmt = """select char_1 from btre209 
where cast (large_int  as largeint ) >= cast (small_int as largeint);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s85')
    
    # ----------------------
    #  in predicate with expression list:
    #              : where ... in cast
    #              : where cast ... not in ...
    #              : where ... not in cast
    # ----------------------
    stmt = """select char_1 from btre209 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s86')
    
    stmt = """select char_1 from btre209 
where char_1 in ( cast ( 3 as char) ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s87')
    
    stmt = """select char_1 from btre209 
where cast ( char_1 as int ) in ( 3 ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s88')
    
    stmt = """select char_1 from btre209 
where cast ( char_1 as int ) not in ( cast ( '3' as int) )
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s89')
    
    # ----------------------
    #  in predicate with subquery:
    #              : where ... in (subq ... cast   )
    #              : where ... not in (subq ... cast   )
    # ----------------------
    stmt = """select char_1, small_int from btre209 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s90')
    
    stmt = """select char_1, small_int from btre209 
where char_1 in
( select cast (small_int as char(6))
from btre209 ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s91')
    
    stmt = """select char_1, small_int from btre209 
where 3 in ( 333 ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """select char_1, small_int from btre209 
where cast('3' as int) in ( 333 ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """select char_1, small_int from btre209 
where char_1 not in
( select cast (small_int as char(6))
from btre209 ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """select char_1, small_int from btre209 
where cast(char_1 as varchar(3)) not in
( select cast (small_int as char(6))
from btre209 ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    # ----------------------
    #  = or <> SUBQUERY returning one value
    # ----------------------
    stmt = """select small_int, cast (small_int as char(6))
from btre209 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s92')
    
    stmt = """select char_1   , cast (char_1 as smallint)
from btre209 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s93')
    
    stmt = """select char_1, var_char_3, cast (small_int as char)
from btre209 
where var_char_3 = '123';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s94')
    
    stmt = """select char_1, small_int
from btre209 
where char_1 = ( select cast (small_int as char)
from btre209 
where var_char_3 = '123');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s95')
    
    stmt = """select char_1, small_int
from btre209 
where small_int <> ( select cast (char_1 as smallint)
from btre209 
where var_char_3 = '123');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s96')
    
    # ----------------------
    #  Quantified predicate before =all, <any, >= some
    #  Compares the value of an expression to the single row returned
    #  by a quantified predicate.
    #  ALL is True only if the comparison is true for EVERY value
    #  generated by the subquery.
    #  ANY is True      if the comparison is true for AT LEAST ONE value
    #  generated by the subquery.
    #  SOME is synonymous with ANY.
    # ----------------------
    stmt = """select char_1, small_int from btre209 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s97')
    
    stmt = """select char_1, small_int from btre209 
where char_1
= all ( select cast (small_int as char(6))
from btre209);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """select char_1, small_int from btre209 
where small_int < any ( select cast('400' as integer)
from btre209) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s98')
    
    stmt = """select char_1, small_int from btre209 
where small_int >= some ( select cast(char_1 as smallint)
from btre209) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s99')
    
    stmt = """select char_1, small_int from btre209 
where small_int <= some ( select cast(char_1 as smallint)
from btre209);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s100')
    
    #----------------------
    # null predicate:
    #----------------------
    
    stmt = """create table a1table2 (
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
    _dci.expect_complete_msg(output)
    
    stmt = """insert into a1table2 
values (
'1' , '123'
, 3  , 4     , 5
, 6.2
,date '1991-09-28'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a1table2 
values (
'2' , '246'
, 33 , 44    , 5
, 66.2
,date '1991-12-27'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a1table2 
values (
'3' , '333'
, 333, 333   , 333
, 333.0
,date '1933-03-03'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a1table2 (char_1) values ( NULL ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select char_1, large_int
from a1table2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s101')
    
    stmt = """delete from a1table2 
where large_int > cast ( '1000000' as largeint signed )
or large_int < cast ( '-1000000' as largeint signed ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 0)
    
    stmt = """select char_1, large_int
from a1table2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s102')
    
    stmt = """select cast (large_int  as smallint)
from a1table2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s103')
    
    stmt = """select char_1 from a1table2 
where cast (large_int   as smallint) is null ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s104')
    
    stmt = """select char_1 from btre209 
where cast (large_int   as largeint) is not null ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s105')
    
    stmt = """select char_1 from a1table2 
where cast (char_1      as date) is null ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s106')
    
    stmt = """select char_1 from btre209 
where cast (float_basic as varchar (20) ) is not null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s107')
    
    stmt = """drop table a1table2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop view pvre201;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view pvre201b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view pvre204a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view svre201;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop view pvre201;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop view pvre201b;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop view pvre204a;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop view svre201;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test003(desc="""a03"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # Test case name:	pretsta03
    # Description:		This test creates the table btre211, and inserts
    #			the values into the table.
    # Expected Results:
    
    
    stmt = """drop table BTRE211;"""
    output = _dci.cmdexec(stmt)
    
    # Table BTRE211 - a table of data type DATETIME.
    stmt = """CREATE TABLE   BTRE211 (
Y_to_D      DATE,
Y_to_S      TIMESTAMP(0),
Y_to_F      TIMESTAMP(6),
H_to_S      TIME,
H_to_F      TIME(6)
) no partition
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO BTRE211 VALUES (
date '1988-01-01' ,
timestamp '1988-01-01 12:35:30' ,
timestamp '1988-01-01 12:35:30.333' ,
time '10:15:30' ,
time '10:15:30.555'
) ;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO BTRE211 VALUES (
date '1977-03-02' ,
timestamp '1979-06-05 14:40:45' ,
timestamp '1980-07-06 15:45:50.678' ,
time '03:53:56' ,
time '04:54:57.345'
) ;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO BTRE211 VALUES (
date '0802-09-07' ,
timestamp '0805-12-10 07:59:03' ,
timestamp '0806-01-11 08:01:04.789' ,
time '18:08:09' ,
time '19:09:10.234'
) ;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO BTRE211 VALUES (
date '0100-01-01' ,
timestamp '0100-01-01 00:00:00' ,
timestamp '0100-01-01 00:00:00.00' ,
time '00:00:00' ,
time '00:00:00.0'
) ;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """update statistics for table BTRE211 on every column;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select * from BTRE211;"""
    output = _dci.cmdexec(stmt)
    
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     A03
    #  Description:        CAST within functions
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    
    # ----------------------------
    #  upshift function:
    # ----------------------------
    
    stmt = """select char_1, upshift(cast (char_1      as char ) )
from btre209 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s0')
    
    stmt = """select var_char_3, upshift(cast (var_char_3  as char(3) ) )
from btre209 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s1')
    
    stmt = """select               small_int
, upshift(cast (small_int   as char(6) ) )
,               medium_int
, upshift(cast (medium_int  as varchar(10) ) )
,               large_int
, upshift(cast (large_int   as char(20)  ) )
from btre209;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s2')
    
    stmt = """select               float_basic
, upshift(cast (float_basic as char(25)     ) )
,               y_to_d
, upshift(cast (y_to_d      as char(10)    ) )
, upshift(cast (y_to_d      as varchar(11) ) )
from btre209;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s3')
    
    stmt = """select               char_1
, upshift(cast (char_1      as char(8)    ) )
, upshift(cast (char_1      as varchar(1) ) )
,               var_char_3
, upshift(cast (var_char_3  as char(8)    ) )
, upshift(cast (var_char_3  as varchar(3) ) )
from btre201;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s4')
    
    # ----------------------------
    #  within aggregate functions:
    # ----------------------------
    stmt = """select                 char_1
from btre209 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s5')
    
    stmt = """select avg(     cast ( char_1 as smallint ) )
from btre209 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s6')
    
    stmt = """select max( all cast ( char_1 as largeint ) )
from btre209 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s7')
    
    stmt = """select min( all cast ( char_1 as integer  ) )
from btre209 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s8')
    
    stmt = """select sum(     cast ( char_1 as float    ) )
from btre209 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s9')
    
    #  CAST not legal inside COUNT - see negative tests.
    
    # ----------------------------
    #  within datetime functions:
    # ----------------------------
    # -------------------
    #  juliantimestamp  : datetime -> largeint
    #  converttimestamp : largeint -> datetime
    # -------------------
    #  *** 12 June 1990 6pm - Tom reviewed these julian/convert fns;
    #  ***                    He blvs they should work.
    
    stmt = """select y_to_d, juliantimestamp (y_to_d)
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s10')
    
    stmt = """select juliantimestamp( cast( '1975-01-01' as date) )
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s11')
    
    stmt = """select converttimestamp( cast( juliantimestamp(
cast( '1975-01-01' as date)
) as largeint ) )
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s12')
    stmt = """select converttimestamp( cast( juliantimestamp(
cast( y_to_d as date)
) as largeint ) )
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s13')
    
    stmt = """select converttimestamp(juliantimestamp (y_to_d))
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s14')
    
    stmt = """select converttimestamp( cast( juliantimestamp (y_to_d) as largeint) )
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s15')
    
    stmt = """select cast ( '211024526400000000' as largeint )
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s16')
    
    stmt = """select converttimestamp( cast( '211024526400000000' as largeint ) )
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s17')
    
    stmt = """select cast (  211024526400000000  as largeint )
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s18')
    
    stmt = """select converttimestamp( cast(  211024526400000000  as largeint ) )
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s19')
    
    stmt = """select converttimestamp( cast( juliantimestamp (y_to_d) as largeint) )
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s20')
    
    stmt = """select converttimestamp (juliantimestamp (y_to_d))
from BTRE211 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s21')
    stmt = """select converttimestamp( cast(juliantimestamp(y_to_d) as largeint))
from BTRE211 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s22')
    stmt = """select converttimestamp( cast( '211434753600000000' as largeint) )
from BTRE211 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s23')
    stmt = """select converttimestamp( cast(  211434753600000000  as largeint) )
from BTRE211 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s24')
    #  *** 12 June 1990 6pm - End of Tom's review
    
    # -------------------
    #  dateformat
    # -------------------
    stmt = """select dateformat(cast('1990-06-11' as date),default)
from btre204;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s25')
    stmt = """selECT dateformat(cast('1990-06-11' as date),usa    )
from btre204;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s26')
    stmt = """select dateformat(cast('1990-06-11' as date),european)
from btre204;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s27')
    
    # -------------------
    #  dayofweek => Tuesday (represented by 3)
    # -------------------
    stmt = """select dayofweek ( cast('1990-06-12' as date) )
from btre204;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s28')
    
    # -------------------
    #  extend => extend to the right with initial (not current) values
    # -------------------
    
    # ----------------------------
    #  cast within cast function:
    # ----------------------------
    stmt = """select              char_1
from btre209;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s29')
    
    stmt = """select        cast (char_1    as varchar(1) )
from btre209;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s30')
    
    stmt = """select cast ( cast (char_1    as varchar(1) ) as pic x )
from btre209;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s31')
    
    stmt = """select              small_int
from btre209;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s32')
    
    stmt = """select        cast (small_int as char(6) )
from btre209;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s33')
    
    stmt = """select cast ( cast (small_int as char(6) ) as smallint )
from btre209;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s34')
    
    stmt = """select cast ( cast (
cast ( cast (small_int as char(6) ) as smallint )
as char(6) ) as smallint )
from btre209;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s35')
    
    stmt = """select cast ( cast (
cast ( cast (
cast ( cast (small_int as char(6) ) as smallint )
as char(6) ) as smallint )
as char(6) ) as smallint )
from btre209;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s36')
    
    stmt = """select cast ( cast (
cast ( cast (
cast ( cast (small_int as char(20) ) as largeint )
as char(20) ) as largeint )
as char(20) ) as largeint )
from btre209;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s37')
    
    _testmgr.testcase_end(desc)

def test004(desc="""a04"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # Test case name:	pretsta04
    # Description:		This test creates the table btre220, its index,
    #			and insert the values into the table.
    # Expected Results:
    
    
    stmt = """drop table btre220;"""
    output = _dci.cmdexec(stmt)
    
    # Table BTRE220 - a table of data type FLOAT
    stmt = """CREATE TABLE btre220 
(
float1     FLOAT(1),
float22    FLOAT(22),
float23    FLOAT(23) DEFAULT 23e0,
float54    FLOAT(54) DEFAULT 1234567890.123456,
real1      REAL      DEFAULT 22.03,
double1    DOUBLE PRECISION  DEFAULT 2.3450000e56,
double2    FLOAT     DEFAULT 56
) no partition
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create index btre220a 
on btre220 (float1,real1,double2 DESC)
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create index btre220b 
on btre220 (float54 DESC, double1 ASC)
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create index btre220c 
on btre220 (float23, real1 DESC)
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO btre220 
VALUES (1.11, 2.22e22, 3.33e-33, 0.004, 5.55e+37,
.66660000E66, 777.00000E-7);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO btre220 
(float1) VALUES (0.0);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO btre220 
(float1, double1) VALUES (0, 1.1111100E+63);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """update statistics for table btre220 every column;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """SELECT * FROM btre220;"""
    output = _dci.cmdexec(stmt)
    
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     A04
    #  Description:        Limited complexity of source expressions
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    
    # Test case A3: limited complexity of source expressions
    # within cast.
    
    # Individual column name, literal, parameter name, function
    # tested in cases A1 and A2.
    
    #----------------------
    # Initialize parameters:
    #----------------------
    stmt = """set param ?a3value1 3 ;"""
    output = _dci.cmdexec(stmt)
    
    # ----------------------
    #  Numeric expressions, unary operators:
    # ----------------------
    stmt = """select + float1
, - float22
, cast (   float1 as char(14) )
, cast ( + float1 as char(14) )
, cast ( - float22 as char(14) )
from btre220 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s0')
    
    #  NOTE: The above CAST loses the space before the number for columns 2 & 3
    
    stmt = """select decimal_1 , + decimal_1
, cast ( decimal_1 as smallint )
from btre201 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s1')
    
    stmt = """select small_int , - small_int
, cast ( - small_int as smallint )
from btre202 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s2')
    
    stmt = """select medium_int , - medium_int
, cast ( - medium_int as integer )
from btre202 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s3')
    
    stmt = """select large_int , + large_int
, cast ( + large_int as largeint )
from btre202 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s4')
    
    stmt = """select binary_32_u , + binary_32_u
, cast ( + binary_32_u as largeint )
from btre204 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s5')
    
    stmt = """select pic_comp_3 , + pic_comp_3
, cast ( + pic_comp_3 as largeint )
from btre204 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s6')
    
    stmt = """select decimal_2_signed , + decimal_2_signed
, cast ( + decimal_2_signed as largeint )
from btre204 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s7')
    
    stmt = """select pic_decimal_1 , + pic_decimal_1
, cast ( + pic_decimal_1 as largeint )
from btre204 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s8')
    
    stmt = """select pic_decimal_2 , + pic_decimal_2
, cast ( + pic_decimal_2 as largeint )
from btre201 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s9')
    
    stmt = """select float1 , + float1 , cast ( + float1 as largeint )
from btre220 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s10')
    
    stmt = """select float22 , + float22 , cast ( + float22 as float )
from btre220 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s11')
    
    stmt = """select + float1
, - float22
, cast (   float1 as char(14) )
, cast ( + float1 as char(14) )
, cast ( - float22 as char(14) )
from btre220 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s12')
    
    #  NOTE: The above CAST loses the space before the number for columns 2 & 3
    
    # ----------------------
    #  Numeric expressions, binary operators:
    # ----------------------
    #  Answers returned should be virtually identical.  The numbers
    #  combine the very large and very small REAL numbers, so the
    #  the answer should be the very large number.  The problem is
    #  the answer is shown in DOUBLE PRECISION and the answer when
    #  an expression is used is different then when a CAST is used.
    
    stmt = """select float1 + float22
, float1 - float22
, cast ( float22 + float1 as char(24) )
, cast ( float22 - float1 as char(24) )
from btre220 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s13')
    stmt = """select decimal_1
, ordering
, 2 * ordering
, decimal_1 * ordering
, cast ( (2 * ordering)         as char(5) )
, cast ( (decimal_1 * ordering) as char(5) )
from btre201 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s14')
    stmt = """select 0
, cast ( 0 as decimal (11,9) )
, cast ( 0 as char(11) )
from btre204 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s15')
    stmt = """select '.000000000'
, cast ( '.000000000' as decimal (11,9) )
, cast ( '.000000000' as char(11) )
from btre204 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s16')
    stmt = """select decimal_1
, ordering
, ?a3value1 / ordering
, decimal_1 / ordering
, cast ( (?a3value1 / ordering) as char(20) )
, cast ( (decimal_1 / ordering) as char(20) )
from btre201 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s17')
    
    stmt = """select max(ordering)
, cast ( max(ordering) as char(5) )
, cast ( (2 * max(ordering) ) as char(5) )
from btre201 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s18')
    
    # ----------------------
    #  containing an aggregate function:
    # ----------------------
    stmt = """select small_int , medium_int , large_int
from btre202 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s19')
    stmt = """select cast ( avg (small_int ) as smallint )
from btre202 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s20')
    stmt = """select cast ( max ( all large_int ) as integer )
from btre202 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s21')
    stmt = """select cast ( min ( medium_int ) as smallint )
from btre202 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s22')
    stmt = """select cast ( sum ( large_int ) as smallint )
from btre202 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s23')
    stmt = """select cast ( count( distinct small_int) as largeint )
from btre202 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s24')
    
    # ----------------------------
    #  containing datetime functions:
    # ----------------------------
    
    # -------------------
    #  juliantimestamp  : datetime -> largeint
    #  converttimestamp : largeint -> datetime
    # -------------------
    
    stmt = """select juliantimestamp(y_to_d),
converttimestamp(juliantimestamp(y_to_d))
from BTRE211 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s25')
    
    stmt = """select cast ( juliantimestamp (y_to_d)  as largeint )
from BTRE211 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s26')
    
    stmt = """select cast ( '211434753600000000' as largeint )
from BTRE211 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s27')
    stmt = """select cast (  211434753600000000  as largeint )
from BTRE211 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s28')
    
    # -------------------
    #  dateformat
    # -------------------
    stmt = """select cast(dateformat(cast('1990-06-11' as date),default) as date)
from btre204;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s29')
    stmt = """select cast(dateformat(cast('1990-06-11' as date),usa ) as date)
from btre204;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s30')
    stmt = """select cast(dateformat(cast('1990-06-11' as date),european) as date)
from btre204;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s31')
    
    stmt = """select dateformat ( timestamp '1990-06-11 07:00:02.000000', usa)
from btre202 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s32')
    
    stmt = """select dateformat ( date '1990-06-11' , usa )
from btre202 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s33')
    
    stmt = """select cast(dateformat(timestamp '1990-06-11 07:00:09.00', usa)
as char(19))
from btre202 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s34')
    
    # -------------------
    #  dayofweek => Tuesday (represented by 3)
    # -------------------
    stmt = """select dayofweek ( cast('1990-06-12' as date) )
from btre204;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s35')
    stmt = """select cast (dayofweek ( cast('1990-06-12' as date) )
as smallint)
from btre204;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s36')
    
    stmt = """select  dayofweek( timestamp '1990-06-12 07:00:07.00' )
from btre202 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s37')
    
    stmt = """select cast (dayofweek(timestamp '1990-06-12 07:00:00.00')
as smallint)
from btre202 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s38')
    
    stmt = """drop table btre220;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table BTRE211;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test005(desc="""a05"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     A05
    #  Description:        CAST - conversion of/to INTERVAL.
    #                      CAST conversion rules in Release 2 (C30) IPM #1.
    #                      Errors in conversion of/to INTERVAL.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    
    # ----------------------------
    #  Interval -> interval:
    # ----------------------------
    
    stmt = """select cast(interval '99-11' year to month
as interval year to month )
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s0')
    
    stmt = """select cast(interval '01:02:03' day to minute
as interval day to minute )
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s1')
    
    # ----------------------------
    #  Interval -> numeric, string, datetime:
    # ----------------------------
    
    stmt = """select cast(interval '01:02:03' day to minute as char(9) )
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s2')
    stmt = """select cast(interval '01:02:03' day to minute as varchar(10) )
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s3')
    
    stmt = """select cast(1190             as interval day(4) )
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s4')
    stmt = """select binary_32_u , float_real
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s5')
    stmt = """select cast(binary_32_u      as interval hour    )
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s6')
    
    stmt = """select cast('1990-01'    as interval year(4) to month )
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s7')
    stmt = """select char_1 , var_char_3
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s8')

    stmt = """select cast(var_char_3       as interval day     )
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8413')

    stmt = """select cast(char_1           as interval month   )
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8413')
    
    _testmgr.testcase_end(desc)

def test006(desc="""a06"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:         A04
    #  Description:            CAST function
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:        (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    
    stmt = """create table t1 (a varchar(27)) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """set param ?p0 '-1';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """set param ?p1 ' -1 ';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p2 ' -01.234567e0 ';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p3 ' -01.2345678e0 ';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p4 '1980-01-01';"""
    output = _dci.cmdexec(stmt)
    
    #  CAST AS character
    
    stmt = """insert into t1 (a) values (cast ('Hi' as char));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 (a) values (cast ('Hi' as char(2)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 (a) values (cast ('Hi' as char(3) upshift));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 (a) values (cast ('Hi' as character(27)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 (a) values (cast ('Hi' as character(28)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 (a) values (cast ('Hi ' as pic x));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 (a) values (cast ('Hi ' as pic xx));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 (a) values (cast ('Hi ' as pic xxx display upshift));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 (a) values (cast ('Hi ' as picture x(27)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 (a) values (cast ('Hi ' as picture xx(27)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """select a from t1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s2')
    stmt = """delete from t1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 10)
    
    stmt = """insert into t1 (a) values (cast (01 as char));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 (a) values (cast (01.0 as char(3)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 (a) values (cast (01.234567 as char(9)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 (a) values (cast (-01.234567 as char(9)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 (a) values (cast (01.234567e0 as char(14)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 (a) values (cast (-01.234567e0 as char(14)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 (a) values (cast (01.2345678e0 as char(24)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 (a) values (cast (-01.2345678e0 as char(24)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into t1 (a) values (cast (date '01/01/1980' as char(10)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 (a) values (cast (?p0 as char(2)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 (a) values (cast (cast (?p1 as varchar(27)) as char(2)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 (a) values (cast (cast (?p2 as varchar(27)) as char(14)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 (a) values (cast (?p3 as char(24)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into t1 (a) values (cast (cast (?p4 as date) as char(11)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select a from t1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s4')
    stmt = """delete from t1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 14)
    
    #  CAST AS varcharacter
    stmt = """insert into t1 (a) values (cast ('Hi' as varchar(1)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 (a) values (cast ('Hi' as varchar(2)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 (a) values (cast ('Hi' as varchar(3) upshift));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into t1 (a) values (cast ('Hi' as varchar(27)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 (a) values (cast ('Hi' as varchar(28)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into t1 (a) values (cast ('Hi ' as varchar(1)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 (a) values (cast ('Hi ' as varchar(2)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 (a) values (cast ('Hi ' as varchar(3) upshift));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 (a) values (cast ('Hi ' as varchar(27)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 (a) values (cast ('Hi ' as varchar(28)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """select a from t1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s7')
    stmt = """delete from t1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 10)
    
    stmt = """insert into t1 (a) values (cast (01 as varchar(1)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 (a) values (cast (01.0 as varchar(3)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 (a) values (cast (01.234567 as varchar(9)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 (a) values (cast (-01.234567 as varchar(9)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 (a) values (cast (01.234567e0 as varchar(14)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 (a) values (cast (-01.234567e0 as varchar(14)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 (a) values (cast (01.2345678e0 as varchar(24)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 (a) values (cast (-01.2345678e0 as varchar(24)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into t1 (a) values (cast (date '01/01/1980' as varchar(10)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 (a) values (cast (?p0 as varchar(2)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 (a) values (cast (cast (?p1 as varchar(27)) as varchar(2)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 (a) values (cast (cast (?p2 as varchar(27)) as varchar(14)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 (a) values (cast (?p3 as varchar(24)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into t1 (a) values (cast (cast (?p4 as date) as char(11)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select a from t1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s9')
    stmt = """delete from t1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 14)
    
    # CAST AS exact numeric
    
    stmt = """insert into t1 (a) values
(cast (cast (' 01.0 ' as smallint) as varchar(27)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into t1 (a) values
(cast (cast (01.0 as smallint unsigned) as varchar(27)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into t1 (a) values
(cast (cast (-0123456789.1 as int) as varchar(27)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into t1 (a) values
(cast (cast (01.234567890e8 as integer unsigned) as varchar(27)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into t1 (a) values
(cast (cast (-01.234567891e8 as largeint signed) as varchar(27)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into t1 (a) values
(cast (cast (' - 01.0 ' as numeric) as varchar(27)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into t1 (a) values
(cast (cast (-012.30 as numeric(3,1) signed) as varchar(27)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into t1 (a) values
(cast (cast (01.23456e1 as numeric(5,3) unsigned) as varchar(27)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into t1 (a) values
(cast (cast (01.23456789012e1 as numeric(11,9)) as varchar(27)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into t1 (a) values
(cast (cast (' - 0123 ' as dec(3)) as varchar(27)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8411')
    
    stmt = """insert into t1 (a) values
(cast (cast (012.3456 as decimal(5,3) unsigned) as varchar(27)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into t1 (a) values
(cast (cast (-010e-1 as pic s9 display sign is leading) as varchar(27)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into t1 (a) values
(cast (cast (' 01234.50 ' as picture 999(2)v9 display) as varchar(27)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into t1 (a) values
(cast (cast (-0.123456789012 as picture sv999(9) comp) as varchar(27)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into t1 (a) values
(cast (cast (cast (?p1 as varchar(27)) as int) as varchar(27)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select a from t1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s11')
    stmt = """delete from t1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 14)
    
    # CAST AS approximate numeric
    
    stmt = """insert into t1 (a) values
(cast (cast (1.2345678 as float) as varchar(27)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into t1 (a) values
(cast (cast (1.2345678e0 as float(15)) as varchar(27)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into t1 (a) values
(cast (cast (' 1.234567e0 ' as float(35)) as varchar(27)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into t1 (a) values
(cast (cast (' -1.2345678e0 ' as real) as varchar(27)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into t1 (a) values
(cast (cast (' -1.2345678e0 ' as double precision) as varchar(27)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into t1 (a) values
(cast (cast (cast (?p1 as varchar(27)) as real) as varchar(27)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into t1 (a) values
(cast (cast (cast(?p2 as varchar(27)) as real) as varchar(27)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into t1 (a) values
(cast (cast (cast(?p3 as varchar(27)) as real) as varchar(27)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select a from t1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s12')
    stmt = """delete from t1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 8)
    
    # CAST AS datetime
    
    stmt = """insert into t1 (a) values
(cast (cast ('01/01/1980' as date) as varchar(27)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into t1 (a) values
(cast (cast ('09:30:00 pm' as time) as varchar(27)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into t1 (a) values
(cast (cast ('01/01/1980 09:30:00.123456 pm' as timestamp) as varchar(27)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # insert into t1 (a) values
    # (cast (cast ('01/01' as datetime month to day) as varchar(27)));
    
    stmt = """insert into t1 (a) values
-- (cast (cast ('9:30:00.123' as datetime hour to fraction(3)) as varchar(27)));
(cast (cast ('09:30:00' as time) as varchar(27)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # insert into t1 (a) values
    # (cast (cast (date '01/01/1980' as datetime month to day) as varchar(27)));
    
    # insert into t1 (a) values
    # (cast (cast (datetime '01/01' month to day as time) as varchar(27)));
    
    stmt = """insert into t1 (a) values
(cast (cast (?p4 as date) as varchar(27)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select a from t1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s13')
    
    stmt = """delete from t1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 5)
    
    stmt = """create view v1 (c1) as select cast (1 as int) from t1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop view v1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create view v1 as select * from t1 where a = cast (1 as varchar(27));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """alter table t1 
add constraint cc check (a > cast (1 as varchar(27)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #  CAST type incompatibilities
    
    stmt = """insert into t1 (a) values (cast (interval '1' year as char));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8402')
    stmt = """insert into t1 (a) values (cast (interval '1' year as varchar(1)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8402')
    stmt = """insert into t1 (a) values (cast (interval '1' year as int));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4039')
    stmt = """insert into t1 (a) values (cast (interval '1' year as real));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4035')
    stmt = """insert into t1 (a) values (cast (interval '1' year as date));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4035')
    stmt = """insert into t1 (a) values (cast (interval '1' year as interval year));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4039')
    stmt = """insert into t1 (a) values (cast ('1' as interval year));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4039')
    stmt = """insert into t1 (a) values (cast (1 as interval year));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4039')
    stmt = """insert into t1 (a) values (cast (1e0 as interval year));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4035')
    
    stmt = """insert into t1 (a) values (cast (interval '1' year as interval year));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4039')
    
    stmt = """insert into t1 (a) values (cast (date '01/01/1980' as int));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4039')
    stmt = """insert into t1 (a) values (cast (date '01/01/1980' as real));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4039')
    #  insert into t1 (a) values (cast (1980 as datetime year));
    #  insert into t1 (a) values (cast (1980e0 as datetime year));
    stmt = """insert into t1 (a) values (cast (1980 as date));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4035')
    stmt = """insert into t1 (a) values (cast (1980e0 as date));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4035')
    
    #  OTHER ERRORS
    
    #  CAST AS character
    
    stmt = """insert into t1 (a) values (cast (10 as char));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8402')
    stmt = """insert into t1 (a) values (cast (1. as char(2)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8101')
    stmt = """insert into t1 (a) values (cast (-1.234567 as char(8)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8402')
    stmt = """insert into t1 (a) values (cast (-1.234567e0 as char(13)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8101')
    stmt = """insert into t1 (a) values (cast (-1.2345678e0 as char(23)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8101')
    stmt = """insert into t1 (a) values (cast (date '01/01/1980' as char(9)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8402')
    
    #  CAST AS varcharacter
    stmt = """insert into t1 (a) values (cast (10 as varchar(1)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8402')

    stmt = """insert into t1 (a) values (cast (1. as varchar(2)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8101')

    stmt = """insert into t1 (a) values (cast (-1.234567 as varchar(8)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8402')

    stmt = """insert into t1 (a) values (cast (-1.234567e0 as varchar(13)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8101')

    stmt = """insert into t1 (a) values (cast (-1.2345678e0 as varchar(23)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8101')
    
    stmt = """insert into t1 (a) values (cast (date '01/01/1980' as varchar(9)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8402')
    
    # CAST AS exact numeric
    
    stmt = """insert into t1 (a) values (cast (cast ('10' as numeric) as char(99)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 (a) values (cast (cast (10 as numeric) as char(99)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 (a) values (cast (cast (1e1 as numeric(2,1)) as char(99)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8411')
    stmt = """insert into t1 (a) values (cast (cast ('-1' as int unsigned) as char(99)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8411')
    stmt = """insert into t1 (a) values (cast (cast ('1.1' as smallint) as char(99)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8101')
    stmt = """insert into t1 (a) values (cast (cast ('1e2' as dec(3)) as char(99)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 (a) values (cast (cast ('1. 2' as decimal(2,1)) as char(99)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8413')
    stmt = """insert into t1 (a) values (cast (cast (-1.1 as pic 9v9 comp) as char(99)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8432')
    stmt = """insert into t1 (a) values (cast (cast (cast (?p2 as varchar(27)) as int) as
char(99)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8101')
    
    #  CAST AS approximate numeric
    
    stmt = """insert into t1 (a) values (cast (cast ('-1.234567 e0' as real) as char(99)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8413')
    
    #  CAST AS datetime
    
    stmt = """insert into t1 (a) values (cast (cast ('1/1' as date) as char(9)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8415')
    
    stmt = """create table t (i decimal(2,2) no default not null) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into t values (.22), (.33), (.44);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 3)
    
    stmt = """select * from t;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s48')
    
    stmt = """select cast(i as varchar(2)) from t;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8402')
    
    stmt = """select cast(i as char(2)) from t;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8402')
    
    stmt = """drop view v1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table t1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table t;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test007(desc="""n06"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     N06
    #  Description:        CAST - negative tests of conversion
    #                      rules in Release 2 (C30) IPM #1.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    
    #  Loss of leading significant digits causes conversion
    #  error; to smallint.
    
    stmt = """select cast(-1     as smallint unsigned)
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8432')
    stmt = """select cast( 0     as smallint unsigned)
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n06exp""", 'n06s1')
    stmt = """select cast( 65535 as smallint unsigned)
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n06exp""", 'n06s2')
    stmt = """select cast( 65536 as smallint unsigned)
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8411')
    stmt = """select cast( 32767 as smallint   signed)
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n06exp""", 'n06s4')
    stmt = """select cast( 32768 as smallint   signed)
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8411')
    stmt = """select cast(-32768 as smallint   signed)
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n06exp""", 'n06s6')
    stmt = """select cast(-32769 as smallint   signed)
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8411')
    
    #  Loss of leading significant digits causes conversion
    #  error; to int.
    stmt = """select cast(-1     as integer  unsigned)
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8432')
    stmt = """select cast( 0     as integer  unsigned)
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n06exp""", 'n06s9')
    stmt = """select cast( 4294967295 as integer unsigned)
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n06exp""", 'n06s10')
    stmt = """select cast( 4294967296 as integer unsigned)
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8411')
    stmt = """select cast(-2147483648 as integer    signed)
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n06exp""", 'n06s12')
    stmt = """select cast(-2147483649 as integer    signed)
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8411')
    stmt = """select cast( 2147483647 as integer    signed)
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n06exp""", 'n06s14')
    stmt = """select cast( 2147483648 as integer    signed)
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8411')
    
    #  Loss of leading significant digits causes conversion
    #  error; to largeint.
    stmt = """select cast(-1        as largeint signed)
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n06exp""", 'n06s16')
    stmt = """select cast( 0        as largeint signed)
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n06exp""", 'n06s17')
    #
    #  When 7 or less digits are used, a real (float(22)) is
    #  used for internal calculations, making the answer less
    #  precise.
    #
    stmt = """select cast(9.224e18 as largeint signed)
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8411')
    stmt = """select cast(9.223e18 as largeint signed)
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n06exp""", 'n06s19')
    stmt = """select cast( 9.2221e18 as largeint   signed)
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n06exp""", 'n06s20')
    #
    #  When 8 or more digits are used, a double precision (float(54))
    #  is used for internal calculations, making the answer more
    #  precise.
    #
    stmt = """select cast( 4.61168602e18 as largeint   signed)
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n06exp""", 'n06s21')
    stmt = """select cast(-9.2220000e18 as largeint   signed)
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n06exp""", 'n06s22')
    stmt = """select cast(-9.22300000000000000e18 as largeint   signed)
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n06exp""", 'n06s23')
    
    #  Loss of trailing significant digits causes conversion
    #  warning.
    #  ??? standard ???
    stmt = """select cast(0.1 as smallint unsigned)
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n06exp""", 'n06s24')
    stmt = """select cast(0.1 as integer    signed)
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n06exp""", 'n06s25')
    stmt = """select cast(0.1 as largeint         )
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n06exp""", 'n06s26')
    stmt = """select      binary_32_u
, cast(binary_32_u      as smallint   signed)
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n06exp""", 'n06s27')
    stmt = """select      pic_comp_3
, cast(pic_comp_3       as integer          )
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n06exp""", 'n06s28')
    stmt = """select      decimal_2_signed
, cast(decimal_2_signed as largeint signed)
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n06exp""", 'n06s29')
    stmt = """select      pic_decimal_1
, cast(pic_decimal_1    as smallint         )
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n06exp""", 'n06s30')
    stmt = """select      pic_decimal_2
, cast(pic_decimal_2    as largeint   signed)
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n06exp""", 'n06s31')
    
    # ----------------------------
    #  Rule 2, character -> numeric or datetime.
    # ----------------------------
    #  Character -> numeric.
    stmt = """select cast('a' as smallint unsigned)
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8413')
    stmt = """select cast(' %' as integer    signed)
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8413')
    stmt = """select cast('+ ' as largeint         )
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8413')
    stmt = """select cast(char_1           as smallint   signed)
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8413')
    stmt = """select cast(var_char_2       as integer          )
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8413')
    stmt = """select cast(var_char_3       as largeint signed)
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8413')
    
    #  Character -> datetime.
    stmt = """select cast('a' as date )
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8415')
    stmt = """select cast('%' as time )
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8415')
    stmt = """select cast('+' as timestamp        )
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8415')
    stmt = """select cast(char_1           as date    )
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8415')
    stmt = """select cast(pic_x_8          as date             )
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8415')
    stmt = """select cast(var_char_2       as time             )
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8415')
    stmt = """select cast(var_char_3       as timestamp        )
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8415')
    stmt = """select cast ( '1991-12-01' as date ) from btre209 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n06exp""", 'n06s45')
    stmt = """select y_to_d      from btre209 
where y_to_d = cast ( '1991' as date );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8415')
    
    # ---------------------------
    #  Rule 3, numeric or datetime -> fixed-length character.
    # ----------------------------
    
    #  Data longer than target -> executor errors
    
    #  Numeric -> fixed-length character.
    stmt = """select cast(12               as char(1) )
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8402')
    
    #  value 80.00 should be convertable to 5 characters.
    stmt = """select      binary_32_u
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n06exp""", 'n06s48')
    stmt = """select cast(binary_32_u      as char(1)          )
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8402')
    stmt = """select cast(binary_32_u      as char(4)          )
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8402')
    stmt = """select cast(binary_32_u      as char(5)          )
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n06exp""", 'n06s51')
    
    #  value 100.70000 should be convertable to 9 characters.
    stmt = """select cast(pic_comp_3       as char(5)          )
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8402')
    stmt = """select cast(pic_comp_3       as char(8)          )
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8402')
    stmt = """select cast(pic_comp_3       as pic x(9)         )
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n06exp""", 'n06s54')
    
    stmt = """select      1e5
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n06exp""", 'n06s55')
    stmt = """select cast(1e5              as char(12) )
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n06exp""", 'n06s56')
    stmt = """select cast(1e5              as char(13) )
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n06exp""", 'n06s57')
    stmt = """select      float_basic
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n06exp""", 'n06s58')
    stmt = """select cast(float_basic      as char(13) )
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n06exp""", 'n06s59')
    stmt = """select      float_real
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n06exp""", 'n06s60')
    stmt = """select cast(float_real       as char(13) )
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n06exp""", 'n06s61')
    stmt = """select      float_double_p
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n06exp""", 'n06s62')
    stmt = """select cast(float_double_p   as char(13) )
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n06exp""", 'n06s63')
    
    #  Datetime -> fixed-length character.
    stmt = """select cast(date '01/01/1990'    as char(9)       )
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8402')
    
    stmt = """select cast(date '01.01.1990'    as char(10)      )
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n06exp""", 'n06s65')
    
    stmt = """select cast(timestamp '1990-01-02:12:45:59' as char(19))
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n06exp""", 'n06s66')

    stmt = """select cast(timestamp '11/22/1990 04:05:06.07' as char(22))
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n06exp""", 'n06s67')

    stmt = """select cast(timestamp '11/22/1990 04:05:06.07' as char(23))
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n06exp""", 'n06s68')

    stmt = """select cast(timestamp '22.01.1990 01:01:01.123456' as char(26))
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3047')

    stmt = """select cast(timestamp '22.01.1990 01:01:01.123456' as char(27))
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3047')

    stmt = """select cast(timestamp '22.01.1990 01:01:01.123456' as char(25))
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3047')

    stmt = """select cast(time '15.03.59'    as char(1)   )
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8402')

    stmt = """select cast(time '15:02:59'    as char(7)   )
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8402')
    stmt = """select cast(time '03:01:59 pm'  as char(8)   )
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n06exp""", 'n06s74')

    stmt = """select cast(y_to_d           as char(9)          )
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8402')
    stmt = """select cast(y_to_d           as char(10)         )
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n06exp""", 'n06s76')

    stmt = """select cast(y_to_d_2         as char(1)       )
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8402')
    stmt = """select cast(y_to_d_2         as char(10)       )
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n06exp""", 'n06s78')
    #
    stmt = """select cast(h_to_f           as char(11)      )
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n06exp""", 'n06s79')
    stmt = """select cast(h_to_f           as char(12)      )
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n06exp""", 'n06s80')
    #
    stmt = """select cast(time1            as char(07)      )
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8402')
    stmt = """select cast(time1            as char(08)      )
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n06exp""", 'n06s82')
    
    # ----------------------------
    #  Rule 4, character -> fixed character.
    # ----------------------------
    
    stmt = """select cast('   '       as char(1) )
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n06exp""", 'n06s83')
    stmt = """select cast('abc'       as char(2) )
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n06exp""", 'n06s84')
    stmt = """select cast('%%'        as pic x upshift)
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n06exp""", 'n06s85')
    #  Should fit in 7 characters:
    stmt = """select cast(pic_x_8     as pic xxxxxx upshift  )
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n06exp""", 'n06s86')
    stmt = """select cast(pic_x_8     as pic xxxxxxx )
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n06exp""", 'n06s87')
    #  Should fit in 3 characters:
    stmt = """select cast(var_char_3  as pic x )
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n06exp""", 'n06s88')
    stmt = """select cast(var_char_3  as pic xx )
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n06exp""", 'n06s89')
    stmt = """select cast(var_char_3  as pic xxx )
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n06exp""", 'n06s90')
    
    # ----------------------------
    #  Rule 5, numeric or datetime -> variable-length character.
    # ----------------------------
    
    #  Source data longer than target -> executor errors
    
    #  Numeric -> variable-length character.
    stmt = """select cast(12               as varchar(2) )
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n06exp""", 'n06s91')
    #  Should be convertable to 14 characters (13 plus sign).
    stmt = """select      1e5
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n06exp""", 'n06s92')
    stmt = """select cast(1e5              as char(13) )
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n06exp""", 'n06s93')
    stmt = """select cast(1e5              as char(14) )
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n06exp""", 'n06s94')
    #  value .97 should be convertable to 3 characters.
    stmt = """select      decimal_2_signed
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n06exp""", 'n06s95')
    stmt = """select cast(decimal_2_signed as varchar(2)       )
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8402')
    stmt = """select cast(decimal_2_signed as varchar(3)       )
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n06exp""", 'n06s97')
    #  value 7.1 should be convertable to 3 characters.
    stmt = """select      pic_decimal_1
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n06exp""", 'n06s98')
    stmt = """select cast(pic_decimal_1    as varchar(2)       )
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8402')
    stmt = """select cast(pic_decimal_1    as varchar(3)       )
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n06exp""", 'n06s100')
    #  value .700 should be convertable to 4 characters.
    stmt = """select      pic_decimal_2
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n06exp""", 'n06s101')
    stmt = """select cast(pic_decimal_2    as varchar(2)       )
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8402')
    stmt = """select cast(pic_decimal_2    as varchar(4)       )
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n06exp""", 'n06s103')
    #  value 80.00 should be convertable to 5 characters.
    stmt = """select      binary_32_u
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n06exp""", 'n06s104')
    stmt = """select cast(binary_32_u      as varchar(2)          )
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8402')
    stmt = """select cast(binary_32_u      as varchar(5)          )
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n06exp""", 'n06s106')
    #  value 100.70000 should be convertable to 9 characters.
    stmt = """select      pic_comp_3
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n06exp""", 'n06s107')
    stmt = """select cast(pic_comp_3       as varchar(5)          )
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8402')
    stmt = """select cast(pic_comp_3       as varchar(9)          )
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n06exp""", 'n06s109')
    #
    stmt = """select      float_basic
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n06exp""", 'n06s110')
    stmt = """select cast(float_basic      as varchar(13) )
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n06exp""", 'n06s111')
    stmt = """select cast(float_basic      as varchar(15) )
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n06exp""", 'n06s112')
    #
    stmt = """select      float_real
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n06exp""", 'n06s113')
    stmt = """select cast(float_real       as varchar(14) )
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n06exp""", 'n06s114')
    stmt = """select cast(float_real       as varchar(15) )
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n06exp""", 'n06s115')
    #
    stmt = """select      float_double_p
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n06exp""", 'n06s116')
    stmt = """select cast(float_double_p   as varchar(10) )
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n06exp""", 'n06s117')
    stmt = """select cast(float_double_p   as varchar(15) )
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n06exp""", 'n06s118')
    
    #  Datetime -> variable-length character.
    stmt = """select cast(date '01/01/1990'    as varchar( 9)      )
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8402')
    stmt = """select cast(date '01/01/1990'    as varchar(10)      )
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n06exp""", 'n06s120')
    #
    stmt = """select cast(date '01.01.1990'    as varchar( 9)      )
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8402')
    stmt = """select cast(date '01.01.1990'    as varchar(11)      )
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n06exp""", 'n06s122')

    stmt = """select cast(timestamp '1990-01-02:12:45:59' as varchar(18))
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8402')
    stmt = """select cast(timestamp '1990-01-02:12:45:59' as varchar(19))
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n06exp""", 'n06s124')

    stmt = """select cast(timestamp '11/22/1990 04:05:06.07' as varchar(21))
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n06exp""", 'n06s125')

    stmt = """select cast(time '03:01:59 pm'  as varchar(7)   )
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8402')

    stmt = """select cast(time '15.03.59'    as varchar(7)   )
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8402')

    stmt = """select cast(y_to_d           as varchar(9)          )
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8402')
    stmt = """select cast(y_to_d           as varchar(10)         )
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n06exp""", 'n06s129')

    stmt = """select cast(y_to_d_2         as varchar(1)       )
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8402')
    stmt = """select cast(y_to_d_2         as varchar(10)       )
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n06exp""", 'n06s131')

    stmt = """select cast(h_to_f           as varchar(11)      )
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n06exp""", 'n06s132')

    stmt = """select cast(h_to_f           as varchar(12)      )
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n06exp""", 'n06s133')

    stmt = """select cast(time1            as varchar(07)      )
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8402')

    stmt = """select cast(time1            as varchar(08)      )
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n06exp""", 'n06s135')
    
    stmt = """create table n1table1(
char_1              char(1)                 default null
, var_char_3          varchar(3)              default null
, small_int           smallint                default null
, medium_int          integer unsigned        default null
, large_int           largeint signed         default null
, float_basic         float (4)               default null
, y_to_d              date                    default null
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into n1table1 
( char_1 , var_char_3 , small_int , medium_int ,
large_int , float_basic , y_to_d)
values (
cast ( 'a'             as char(1)  )
, cast ( 'bc'            as pic xx   )
, cast ( 3               as smallint )
, cast ( 4               as int unsigned )
, cast ( 5               as largeint signed )
, cast ( 6               as float (4) )
, cast ( date '01/01/1980' as date     )
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """select * from n1table1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n06exp""", 'n06s136')

    stmt = """update n1table1 
set var_char_3 = cast (date '06/12/1990' as varchar(3) )
where char_1 = 'a';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8402')
    stmt = """select * from n1table1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n06exp""", 'n06s138')
    
    stmt = """drop table n1table1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # ----------------------------
    #  Rule 6, character -> variable-length character.
    # ----------------------------
    
    stmt = """select cast('abc'            as varchar(2) )
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n06exp""", 'n06s139')
    
    stmt = """select cast('%%'             as varchar(1) upshift )
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n06exp""", 'n06s140')

    stmt = """select cast(pic_x_8          as varchar(5) )
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n06exp""", 'n06s141')

    stmt = """select cast(pic_x_8          as varchar(7) upshift )
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n06exp""", 'n06s142')

    stmt = """select cast(var_char_3       as varchar(1) )
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n06exp""", 'n06s143')

    stmt = """select cast(var_char_3       as varchar(3) upshift )
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n06exp""", 'n06s144')
    
    _testmgr.testcase_end(desc)

def test008(desc="""n07"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     N07
    #  Description:        CAST - negative tests
    #                      in DDL and report writer.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    
    # Tables to be used below:
    
    stmt = """create table n2table1 (c pic x) no partition ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into n2table1 values ('7' ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """create table n2table2 (c pic x) no partition ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into n2table2 values ('7' ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # ----------------------------
    #  In Report writer:
    # ----------------------------
    
    #    set list_count 1;
    
    stmt = """select [first 1] c from n2table1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n07exp""", 'n07s0')
    
    stmt = """select [first 1] c from n2table1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n07exp""", 'n07s1')
    
    stmt = """select cast(c as int) from n2table1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n07exp""", 'n07s2')
    
    #----------------------------
    # In CREATE VIEW:
    #----------------------------
    stmt = """create view n2view1 as
select c from n2table1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select cast(c as int) from n2table1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n07exp""", 'n07s3')
    
    stmt = """create view n2view2 (cv) as
select cast(c as int) from n2table1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create view n2view3 as
select c from n2table1 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select cast(c as pic x) from n2table1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n07exp""", 'n07s4')
    
    stmt = """create view n2view4 (vp) as
select cast(c as pic x) from n2table1 
--      for protection
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create view n2view5 (a,b) as
select ta.c, tb.c
from n2table1 ta,
 n2table2 tb
where ta.c=tb.c ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select cast(ta.c as pic x), cast(tb.c as pic x)
from n2table1 ta,
 n2table2 tb
where ta.c=tb.c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n07exp""", 'n07s5')
    
    stmt = """create view n2view6 (a,b) as
select cast(ta.c as pic x), cast(tb.c as pic x)
from n2table1 ta,
 n2table2 tb
where ta.c=tb.c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # ----------------------------
    #  In CREATE CONSTRAINT:
    # ----------------------------
    stmt = """alter table n2table1 
add check cast(c as int) > 100;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    #----------------------------
    # Cleanup:
    #----------------------------
    
    stmt = """drop view n2view1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view n2view2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view n2view3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view n2view4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view n2view5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view n2view6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop table n2table1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table n2table2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test009(desc="""n08"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     N08
    #  Description:        CAST - negative tests of limited complexity
    #                      of source expressions within cast.
    #                      Errors in source expressions or attempted
    #                      conversions.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    
    #  Divide by 0 in source expression:
    
    stmt = """select decimal_1
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n08exp""", 'n08s0')
    
    stmt = """select decimal_1 / 0
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8419')
    
    stmt = """select cast ( (decimal_1 / 0) as char(20) )
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8419')
    
    # Insert empty string into numeric:
    
    stmt = """create table n3table1 (
char_1              char(1)                 default null
, var_char_3          varchar(3)              default null
, small_int           smallint                default null
, medium_int          integer unsigned        default null
, large_int           largeint signed         default null
, float_basic         float (4)               default null
, y_to_d              date                    default null
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select cast ( '' as smallint ) from n3table1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """insert into n3table1 ( small_int  )
values ( cast ( '' as smallint ) ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8413')

    stmt = """insert into n3table1 ( medium_int )
values ( cast ( '' as integer  ) ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8413')

    stmt = """insert into n3table1 ( large_int  )
values ( cast ( '' as largeint ) ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8413')

    stmt = """insert into n3table1 ( float_basic)
values ( cast ( '' as float    ) ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8413')
    stmt = """select * from n3table1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """select y_to_d from btre209 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n08exp""", 'n08s7')

    stmt = """select cast ( '1991-12' as date )
from btre209 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8415')

    stmt = """select y_to_d from btre209 
where y_to_d = cast ( '1991' as date );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8415')
    
    # ----------------------------
    #  Errors in target data type (string too short or long).
    # ----------------------------
    
    stmt = """select medium_int from btre209 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n08exp""", 'n08s10')

    stmt = """select cast ( medium_int as char )
from btre209 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8402')
    
    #  Release 2 shows char as 1 to 4061 or 4072 characters,
    stmt = """select cast ( 1 as char(0) )
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3003')
    #  Release 2 shows varchar as 1 to 4059 or 4070 characters,
    stmt = """select cast ( 1 as varchar(0) )
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3003')
    
    # ----------------------------
    #  Errors in attempted conversions.
    # ----------------------------
    #  See I1 for Interval -> numeric, string, datetime, interval.
    #  See I1 for Numeric, string, datetime -> interval.
    
    # ----------------------------
    #  CAST not legal inside COUNT aggregate function.
    # ----------------------------
    stmt = """select count (  cast ( char_1 as largeint ) )
from btre209 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n08exp""", 'n08s14')
    stmt = """select count( distinct cast ( char_1 as largeint ) )
from btre209;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n08exp""", 'n08s15')
    
    stmt = """drop table btre209;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table n3table1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test010(desc="""n09"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     N09
    #  Description:        CAST char(0), ordering by.
    #                      Test for Order By on CAST to string of length 0.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    
    #  Could not sort using a null string as an ordering column:
    
    stmt = """select char_1 , var_char , pic_comp_1
from """ + gvars.g_schema_arkcasedb + """.btsel01 
group by char_1 , var_char , pic_comp_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n09exp""", 'n09s0')
    
    stmt = """select cast ( char_1      as char(0)    )
, cast ( var_char  as varchar(0) )
, cast ( pic_comp_1  as pic s9(0)  )
from """ + gvars.g_schema_arkcasedb + """.btsel01 
group by char_1 , var_char , pic_comp_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3003')
    
    stmt = """select cast ( char_1      as char(0)    )
from """ + gvars.g_schema_arkcasedb + """.btsel01 
group by char_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3003')
    
    stmt = """select cast ( var_char  as varchar(0) )
from """ + gvars.g_schema_arkcasedb + """.btsel01 
group by var_char;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3003')
    
    stmt = """select cast ( pic_comp_1  as pic s9(0)  )
from """ + gvars.g_schema_arkcasedb + """.btsel01 
group by pic_comp_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3003')
    
    stmt = """select        float_basic
from btre202 
group by float_basic;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n09exp""", 'n09s5')
    
    stmt = """select cast ( float_basic as float(0)   )
from btre202 
group by float_basic;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3003')
    
    stmt = """set param ?p 100 ;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select pic_x_7 from """ + gvars.g_schema_arkcasedb + """.btsel04 order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n09exp""", 'n09s7')
    
    #  NOTE:  The table btsel04 is created in arkt0000, but then
    # 	 it is updated in arkt0025, so if missing abcdefg & abc123d
    # 	 need to run arkt0025 to get the values
    #  Null string constant expressed via a parameter.
    #  Null string parameter is first sort key column (sort for order by):
    stmt = """select cast(?p as char(0)), pic_x_7 from
 """ + gvars.g_schema_arkcasedb + """.btsel04 order by 1, pic_x_7;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3003')
    
    #  Null string parameter is second sort key column (sort for order
    #  by):
    stmt = """select cast(?p as char(0)), pic_x_7 from
 """ + gvars.g_schema_arkcasedb + """.btsel04 order by pic_x_7, 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3003')
    
    #  Null string parameter is first sort key column  (sort for
    #  distinct):
    stmt = """select distinct cast(?p as char(0)), pic_x_7 from
 """ + gvars.g_schema_arkcasedb + """.btsel04;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3003')
    
    #  Null string parameter is second sort key column  (sort for
    #  distinct):
    stmt = """select distinct pic_x_7, cast(?p as char(0)) from
 """ + gvars.g_schema_arkcasedb + """.btsel04;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3003')
    
    stmt = """select distinct char_1 , cast(?p as char(0)) from
 """ + gvars.g_schema_arkcasedb + """.btsel01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3003')
    
    #  Null string parameter is first sort key column  (sort for group
    #  by):
    stmt = """select pic_x_7, cast(?p as char(0)), count(*) from
 """ + gvars.g_schema_arkcasedb + """.btsel04 
--    group by 2,1;
group by ?p, pic_x_7;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3003')
    
    #  Null string parameter is second sort key column (sort for group
    #  by):
    stmt = """select pic_x_7, cast(?p as char(0)), count(*) from
 """ + gvars.g_schema_arkcasedb + """.btsel04 
group by pic_x_7, ?p;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3003')
    
    #  Null string parameter in the argument of an aggregate function:
    stmt = """select pic_x_7,     min(cast(?p as char(0)))
from """ + gvars.g_schema_arkcasedb + """.btsel04 group by pic_x_7;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3003')
    
    stmt = """select pic_x_7,     max(cast(?p as char(0)))
from """ + gvars.g_schema_arkcasedb + """.btsel04 
group by pic_x_7;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3003')
    
    stmt = """select pic_x_7, '', min(cast(?p as char(0)))
from """ + gvars.g_schema_arkcasedb + """.btsel04 
group by pic_x_7,'';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3003')
    
    stmt = """select pic_x_7, '', min(cast(?p as char(0)))
from """ + gvars.g_schema_arkcasedb + """.btsel04 
group by '',pic_x_7;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3003')
    
    stmt = """select pic_x_7, '', max(cast(?p as char(0)))
from """ + gvars.g_schema_arkcasedb + """.btsel04 
group by pic_x_7,'';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3003')
    
    stmt = """select pic_x_7, '', max(cast(?p as char(0)))
from """ + gvars.g_schema_arkcasedb + """.btsel04 
group by '',pic_x_7;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3003')
    
    #  Null string parameter in the argument of an UPSHIFT function:
    stmt = """select pic_x_7, upshift(cast(?p as char(0)))
from """ + gvars.g_schema_arkcasedb + """.btsel04 
group by pic_x_7, ?p;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3003')
    
    stmt = """select pic_x_7, upshift(cast(?p as char(0)))
from """ + gvars.g_schema_arkcasedb + """.btsel04 
group by ?p,pic_x_7;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3003')
    
    stmt = """select distinct pic_x_7, upshift(cast(?p as char(0)))
from """ + gvars.g_schema_arkcasedb + """.btsel04;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3003')
    
    stmt = """select distinct upshift(cast(?p as char(0))), pic_x_7
from """ + gvars.g_schema_arkcasedb + """.btsel04;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3003')
    
    stmt = """select char_1, upshift(cast(?p as char(0)))
from """ + gvars.g_schema_arkcasedb + """.btsel01 
group by ?p, char_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3003')
    
    stmt = """select distinct char_1, upshift(cast(?p as char(0)))
from """ + gvars.g_schema_arkcasedb + """.btsel01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3003')
    
    _testmgr.testcase_end(desc)

def test011(desc="""n10"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     N10
    #  Description:        CAST - Two extreme test cases
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   Two long lines of dashes
    #
    
    stmt = """log """ + defs.work_dir + """/n10s0.log clear;"""
    output = _dci.cmdexec(stmt)
    stmt = """select cast ( 1 as char(4100) )
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    stmt = """log off;"""
    output = _dci.cmdexec(stmt)

    output = _testmgr.shell_call("""grep '^-' """ + defs.work_dir + """/n10s0.log | grep -v '1 row' | wc --char""")
    # Trafci seems to truncate the header to 128+1 bytes (only the header, not
    # the data), while sqlci still shows 4100+1 bytes of '-' as the header.
    # For now, skip this check for Trafodion.
    if hpdci.tgtSQ():
        _dci.expect_str_token(output, '4101')

    #  Release 2 shows varchar as 1 to 4059 or 4070 characters,
    stmt = """log """ + defs.work_dir + """/n10s1.log clear;"""
    output = _dci.cmdexec(stmt)
    stmt = """select cast ( 1 as varchar(4100) )
from btre204 ;"""
    output = _dci.cmdexec(stmt)
    stmt = """log off;"""
    output = _dci.cmdexec(stmt)

    output = _testmgr.shell_call("""grep '^-' """ + defs.work_dir + """/n10s0.log | grep -v '1 row' | wc --char""")
    # Trafci seems to truncate the header to 128+1 bytes (only the header, not
    # the data), while sqlci still shows 4100+1 bytes of '-' as the header. 
    # For now, skip this check for Trafodion.
    if hpdci.tgtSQ():
        _dci.expect_str_token(output, '4101')
 
    _testmgr.shell_call("""rm """ + defs.work_dir + """/n10s0.log """ + defs.work_dir + """/n10s1.log""")
    _testmgr.testcase_end(desc)

