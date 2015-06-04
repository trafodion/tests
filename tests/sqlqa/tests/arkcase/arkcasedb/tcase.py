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

def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci
    
    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()
    
def test001(desc="""a00"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # Filename: D0US00K
    # 06 Dec 1989.  JZ.
    # SQLCI source for global database Release 2; based on DATETIME
    # and INTERVAL data types in T140, T142, T151, T159, T167, T181.
    #
    # Modified by BH, April 30, 1990, to create indexes and views:
    # UNIQUE and regular INDEXES on singular and multiple columns
    #  (R1 and R2 data types) with ASC, DESC and default options.
    # PROTECTION VIEWS with predicate clauses IS (NOT) NULL  and IS
    #  (NOT) NULL with other clauses.
    # SHORTHAND VIEWS with equality between NULLable columns, between
    #  NULLable columns in conjunction with other clauses, containing
    #  (LEFT) UNION clauses.
    
    #
    # OBJECTIVE: The SQLCI Test Library environment depends
    #            on the availablity of a 'global' database, accessible
    #            to all test units.  This test unit creates and
    #            populates Release 2 tables and views.
    #
    # METHOD:    Take table definitions from null test units;
    #            these are also used for testing UNION and OUTER JOIN.
    #
    #
    #
    # Table btre201 - a table with all data types and default null;
    #                 includes Release 1 as well as Release 2 types.
    #                 Key-sequenced with user key.
    #                 Values defined for T139 (NULLs and DML);
    #                 table also used by T138, T148, T149, T155.
    
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
--    ATTRIBUTES
--    blocksize 4096
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    #  Create INDEXES for table BTRE201.
    
    stmt = """create index btre201a
on btre201 (ordering)
--      ATTRIBUTES
--      blocksize 4096
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """create index btre201b
on btre201 (char_1, alwaysnull, binary_signed)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """create index btre201c
on btre201 (var_char_3, large_int)
--      ATTRIBUTES
--      blocksize 4096
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """create index btre201d
on btre201 (decimal_3_unsigned, pic_decimal_1)
--      ATTRIBUTES
--      blocksize 4096
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
#    stmt = """create index btre201e
#on btre201 (pic_x_8, iy_to_mo, y_to_d, medium_int)
#--      ATTRIBUTES
#--      maxsize 320
#;"""
#    output = _dci.cmdexec(stmt)
#    _dci.expect_any_substr(output, '*15001*')
    
    stmt = """create index btre201e
on btre201 (pic_x_8, iy_to_mo, y_to_d, medium_int)
ATTRIBUTES
--      allocate 2,
auditcompress,
--      blocksize 4096,
--      no buffered,
clearonpurge,
--      no dcompress,
extent (32,128),
--      no icompress,
maxextents 320
--      maxsize 320
--      serialwrites
--      no verifiedwrites
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """create index btre201f
on btre201 (ih_to_s)
-- ATTRIBUTES
--    keytag 34
--      blocksize 4096
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """create index btre201g
on btre201 (time1 DESC, float_real ASC, pic_comp_3)
ATTRIBUTES
--    keytag 'ka'
--    allocate 4,
no auditcompress,
--      blocksize 4096,
--      buffered,
no clearonpurge,
--      no dcompress,
extent (16,32),
--      icompress,
--      maxsize 6,
maxextents 6
--    no serialwrites
--    verifiedwrites
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """create index btre201h
on btre201 (y_to_d_2 DESC)
--      ATTRIBUTES
--      blocksize 4096
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """create index btre201i
on btre201 (float_double_p ASC)
--      ATTRIBUTES
--      blocksize 4096
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """create index btre201j
on btre201 (h_to_f)
--      ATTRIBUTES
--      blocksize 4096
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """create index btre201k
on btre201 (decimal_1, pic_decimal_3 DESC)
--      ATTRIBUTES
--      blocksize 4096
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """create index btre201l
on btre201 (decimal_2_signed ASC, small_int DESC,
var_char_2, binary_32_u, pic_comp_1,
float_basic DESC)
--      ATTRIBUTES
--      blocksize 4096
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """create index btre201m
on btre201 (pic_comp_2, binary_64_s)
--      ATTRIBUTES
--      blocksize 4096
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
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
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
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
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btre201 (ordering , pic_comp_2 ,
pic_comp_3 , var_char_2, var_char_3
, small_int , large_int , decimal_2_signed
)
values ( 3, null, 2
, 'zy' , 'zy'
, NULL , 10 , NULL
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    #  insert values that corespond to BTSEL01; values for all columns:
    
    stmt = """insert into btre201 
values ( 4, NULL
--    , char_1              char(1)                 default null
--    , pic_x_8             pic x(8)                default null
--    , var_char_2          varchar(2)              default null
--    , var_char_3          varchar(3)              default null
,'C' ,'maureen' ,'E' ,'rum'
--    , binary_signed       numeric (4) signed      default null
--    , binary_32_u         numeric (9,2) unsigned  default null
--    , binary_64_s         numeric (18,3) signed   default null
--    , pic_comp_1          pic s9(10) comp         default null
,3000 ,80 ,2000 ,500
--    , pic_comp_2          pic sv9(2) comp         default null
--    , pic_comp_3          pic s9(3)v9(5) comp     default null
,0.50 ,100.7
--    , small_int           smallint                default null
--    , medium_int          integer unsigned        default null
--    , large_int           largeint signed         default null
--    , decimal_1           decimal (1)             default null
--    , decimal_2_signed    decimal (2,2) signed    default null
--    , decimal_3_unsigned  decimal (3,0) unsigned  default null
,9000 ,1000 ,2000 ,8 ,.97 ,150
--    , pic_decimal_1       pic s9(1)v9(1)          default null
--    , pic_decimal_2       picture v999 display    default null
--    , pic_decimal_3       pic s9                  default null
,7.1 ,0.7 ,7
--    , float_basic         float (4)               default null
--    , float_real          real                    default null
--    , float_double_p      double precision        default null
,1.2 ,0.0001 ,0.0002
--    , y_to_d              datetime year to day    default null
--    , y_to_d_2            date                    default null
--    , h_to_f              datetime hour to fraction(3) default null
--    , time1               time                    default null
,date '1975-01-01'
,date '1980-01-01'
,time '15:00:00'
,time '13:11:59'
--    , iy_to_mo            interval year(4) to month  default null
--    , ih_to_s             interval hour to second default null
,interval '1900-01' year(4) to month
,interval '1:2:3' hour to second
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btre201 (ordering , pic_comp_2 ,
pic_comp_3 , large_int , decimal_1 , decimal_2_signed
)
values ( 5, .3, null
, 2 , 0 , NULL
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btre201 (ordering , pic_comp_2 ,
pic_comp_3 , large_int , decimal_1 , decimal_2_signed
)
values ( 6, .3, null
, 2 , NULL , .1
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btre201 (ordering , pic_comp_2 ,
pic_comp_3 , large_int , decimal_1 , decimal_2_signed
)
values ( 7, null, null
, 2 , NULL , NULL
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btre201 (ordering ) values ( 8 ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """update statistics for table btre201 on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """select * from btre201 
order by ordering;"""
    output = _dci.cmdexec(stmt)
    
    # Table btre202 - a table with fewer columns than btre201
    #                 with one of each data type and default null;
    #                 values defined for T149 (JOIN);
    #                 table also used by T138, T139, T148.
    
    stmt = """create table btre202 (
char_1              char(1)                 default null
, var_char_3          varchar(3)              default null
, small_int           smallint                default null
, medium_int          integer unsigned        default null
, large_int           largeint                default null
, float_basic         float (4)               default null
, y_to_d              date                default null
) no partition
--    organization r
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    #  Insert ONE record value needed for T149 (JOIN)
    #  to match btre201 and btsel01; and one record of NULLs:
    
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
,1.2
--    , y_to_d              datetime year to day    default null
,date '1975-01-01'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btre202 (char_1) values ( NULL ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """update statistics for table btre202 on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """select * from btre202 
order by char_1;"""
    output = _dci.cmdexec(stmt)
    
    # Table BTRE203 - a table with fewer columns than btre201,
    #                 and some NOT NULL columns;
    #                 table used by T138, T139.
    
    stmt = """create table btre203 (
col_numeric        smallint     default null
, col_varchar        varchar (3)  default null
, col_date           date         default null
, col_float          float (5)    default null
, col_string         pic x        default null
, col_numeric2       smallint     default 8      not null
, col_varchar2       varchar (3)  default '?'    not null
, col_date2          date         not null
, col_float2         float (5)                   not null
, col_string2        pic x        not null
, col_string3        pic x
) no partition
--  organization e
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    #  Empty table.
    #
    # Table BTRE204 - a table with
    #                 differerent column types (including R2 types),
    #                 and all NOT NULL:
    #                 values defined for T149 (JOIN);
    #                 table also used by T139, T148.
    
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
--    blocksize 4096
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    #  Insert a record needed for T149 (JOIN) -
    #  to match btre208 and btsel01; need values for all columns:
    
    stmt = """insert into btre204 
values (
--    , char_1              char(1)                 default null
--    , pic_x_8             pic x(8)                default null
--    , var_char_2          varchar(2)              default null
--    , var_char_3          varchar(3)              default null
'C' ,'maureen' ,'E' ,'rum'
--    , binary_signed       numeric (4) signed      default null
--    , binary_32_u         numeric (9,2) unsigned  default null
--    , binary_64_s         numeric (18,3) signed   default null
--    , pic_comp_1          pic s9(10) comp         default null
--    , pic_comp_2          pic sv9(2) comp         default null
--    , pic_comp_3          pic s9(3)v9(5) comp     default null
,3000 ,80 ,2000 ,500
--    , pic_comp_2          pic sv9(2) comp         default null
--    , pic_comp_3          pic s9(3)v9(5) comp     default null
,0.50 ,100.7
--    , small_int           smallint                default null
--    , medium_int          integer unsigned        default null
--    , large_int           largeint signed         default null
--    , decimal_1           decimal (1)             default null
--    , decimal_2_signed    decimal (2,2) signed    default null
--    , decimal_3_unsigned  decimal (3,0) unsigned  default null
,9000 ,1000 ,2000 ,8 ,.97 ,150
--    , pic_decimal_1       pic s9(1)v9(1)          default null
--    , pic_decimal_2       picture v999 display    default null
--    , pic_decimal_3       pic s9                  default null
,7.1 ,0.7 ,7
--    , float_basic         float (4)               default null
--    , float_real          real                    default null
--    , float_double_p      double precision        default null
,1.2 ,0.0001 ,0.0002
--    , y_to_d              datetime year to day    default null
--    , y_to_d_2            date                    default null
--    , h_to_f              datetime hour to fraction(3) default null
--    , time1               time                    default null
,date '1975-01-01'
,date '1980-01-01'
,time '15:00:00'
,time '13:11:59'
--    , iy_to_mo            interval year to month  default null
--    , ih_to_s             interval hour to second default null
,interval '1900-01' year(4) to month
,interval '1:2:3' hour to second
--    , ordering            smallint
, 1
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """update statistics for table btre204 on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """select * from btre204 
order by ordering;"""
    output = _dci.cmdexec(stmt)
    
    # Table BTRE205 - a table with fewer columns than btre201,
    #  Set up table needed for Boolean truth values (testcase
    #  H1 in Testunit T139).
    #  Clustering key added 20 June 1989 (JZ).
    
    stmt = """create table btre205 (
ordering            smallint
, col_1               smallint    default null
, col_2               smallint    default null
) no partition
--      clustering key ordering
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    #  Insert values needed for T139 (NULLs and DML), case H1:
    
    stmt = """insert into btre205 values ( 1 , 1    , 2 ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btre205 values ( 2 , 1    , 9 ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btre205 values ( 3 , 1    , null ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btre205 values ( 4 , 9    , 2 ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btre205 values ( 5 , 9    , 9 ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btre205 values ( 6 , 9    , null ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btre205 values ( 7 , null , 2 ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btre205 values ( 8 , null , 9 ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btre205 values ( 9 , null , null ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """update statistics for table btre205 on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """select * from btre205 
order by ordering;"""
    output = _dci.cmdexec(stmt)
    
    # Table BTRE206 - a table like REGION table in global database, with
    #                 addition of default null; used for testing
    #                 'IN' in T139 (J1); values defined for T139 (NULLs
    #                 and DML); table not used elsewhere (1 May 1989).
    
    stmt = """create table btre206 (
regnum              PIC 99       default null
, regname             PIC X(12)    default null
, location            VARCHAR (14) default null
, manager             PIC 9(4)     default null
) no partition
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """create index btre206i on
 btre206 ( regname );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    #  Insert values needed for T139 (NULLs and DML):
    
    stmt = """insert into btre206 
values ( 1,'EAST        ', 'NEW YORK' ,  29);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btre206 
values ( 2,'CENTRAL     ', 'CHICAGO'  , 104);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btre206 
values ( 3,'WEST        ', 'DALLAS'   ,  72);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btre206 
values ( 4,'CANADA      ', 'TORONTO'  , null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btre206 
values ( 5,'GERMANY     ', 'FRANKFURT',  43);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btre206 
values ( 6,'ENGLAND     ', 'LONDON'   ,  87);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btre206 
values (99,'HEADQUARTERS', 'CUPERTINO',   1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btre206 
values (77,'PUMPKINS    ', 'CUPERTINO', null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """update statistics for table btre206 on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """select * from btre206 
order by regnum;"""
    output = _dci.cmdexec(stmt)
    
    # Table BTRE207 - a table like EMPLOYEE table in global database,
    #                 with addition of default null;
    #                 used for testing 'IN' in T139 (J1);
    #                 values defined for T139 (NULLs and DML);
    #                 Clustering key added 20 June 1989 (JZ).
    
    stmt = """create table btre207 (
empnum              PIC 9(4)     not null
, empname             PIC X(18)    default null
, regnum              PIC 99       default null
, branchnum           PIC 99       default null
, job                 VARCHAR (12) not null,
primary key ( empnum , job ))
--      clustering key ( empnum , job )
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """create index btre207i on
 btre207 ( empname );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """create index btre207j on
 btre207 ( regnum, branchnum );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    #  Insert values needed for T139 (NULLs and DML);
    #  a SUBSET of records:
    
    stmt = """insert into btre207 
values (   1,'ROGER GREEN',   99, null, 'UNKNOWN' ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btre207 
values (  23,'JERRY HOWARD',   2, 1, 'MANAGER' ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btre207 
values (  29,'JACK RAYMOND',   1, 1, 'MANAGER' ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btre207 
values (  43,'PAUL WINTER',    5, 1, 'MANAGER' ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btre207 
values (  78,'SPOT TO FILL',  77, 7, 'PROGRAMMER' ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btre207 
values (  79,'SPOT TO FILL',  77, 8, 'SECRETARY' ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btre207 
values (1001,       null , null , null , 'UNKNOWN' ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """update statistics for table btre207 on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """select * from btre207 
order by empnum;"""
    output = _dci.cmdexec(stmt)
    
    # Table BTRE208 - a table for UNION Test unit T148.
    
    stmt = """create table btre208 (
ordering            smallint
, alwaysnull          smallint                default null
--  Needs 1 duplicate value for ORDER BY.
, var_char_2          varchar(2)              not     null
, var_char_3          varchar(3)              not     null
, pic_decimal_2       pic v999 display        not     null
, float_double_p      double precision        not     null
, y_to_d              date    not     null
, ih_to_s             interval hour to second not     null
, headed_pic_x        pic x                   default null
heading 'long'
, headed_numeric      numeric (9,2) unsigned  default null
heading 'short'
) no partition
--      clustering key ordering
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    #  Insert values:
    #  Values to be determined after/with btre204.
    
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
, 1.2
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
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """update statistics for table btre208 on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """select * from btre208 
order by ordering;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE   BTRE211 (
Y_to_D      DATE,
Y_to_S      TIMESTAMP(0),
Y_to_F      TIMESTAMP(6),
H_to_S      TIME,
H_to_F      TIME(6)
) no partition
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """INSERT INTO BTRE211 VALUES (
date '1988-01-01' ,
timestamp '1988-01-01 12:35:30' ,
timestamp '1988-01-01 12:35:30.333' ,
time '10:15:30' ,
time '10:15:30.555'
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO BTRE211 VALUES (
date '1977-03-02' ,
timestamp '1979-06-05 14:40:45' ,
timestamp '1980-07-06 15:45:50.678' ,
time '03:53:56' ,
time '04:54:57.345'
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO BTRE211 VALUES (
date '0802-09-07' ,
timestamp '0805-12-10 07:59:03' ,
timestamp '0806-01-11 08:01:04.789' ,
time '18:08:09' ,
time '19:09:10.234'
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO BTRE211 VALUES (
date '0100-01-01' ,
timestamp '0100-01-01 00:00:00' ,
timestamp '0100-01-01 00:00:00.00' ,
time '00:00:00' ,
time '00:00:00.0'
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """update statistics for table BTRE211 on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """select * from BTRE211;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE    BTRE213 
(
DATE1       DATE,
TIME1       TIME
)  no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    stmt = """INSERT INTO BTRE213 VALUES ( date '1988-10-25', time '10:10:10' );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO BTRE213 VALUES ( date '1900-01-01', time '00:00:00' );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO BTRE213 VALUES ( date '1900-01-01', time '23:59:59' );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO BTRE213 VALUES ( date '1954-05-06', time '22:23:24' );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """CREATE index btre213a on BTRE213 (DATE1, TIME1 DESC);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    #  Protection view with nulls:
    # This is where the core comes from
    stmt = """create view pvre201 as
select ordering , alwaysnull , char_1
from btre201 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """select * from pvre201 
order by ordering;"""
    output = _dci.cmdexec(stmt)
    
    #  pvre201b:   ordering      small_int       y_to_d
    #               4            9000        1975-01-01
    
    stmt = """create view pvre201b as
select ordering, small_int, y_to_d
from btre201 
where small_int is NOT NULL and
y_to_d = date '1975-01-01'
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """select * from pvre201b 
order by ordering;"""
    output = _dci.cmdexec(stmt)
    
    #  pvre201c:   ordering      small_int     var_char_3
    #               1             ?             AbC
    #               2             ?             zz
    #               3             ?             zy
    #               5             ?             ?
    #               6             ?             ?
    #               7             ?             ?
    #               8             ?             ?
    
    stmt = """create view pvre201c as
select ordering, small_int, var_char_3
from btre201 
where small_int is NULL
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """select * from pvre201c 
order by ordering;"""
    output = _dci.cmdexec(stmt)
    
    #  Cause of warning: NOT NULL columns in the underlying tables.
    #
    #  pvre204a:   ordering      time1          float_real
    #                 1        13:11:59       0.1000000E-03
    
    stmt = """create view pvre204a as
select ordering, time1, float_real
from btre204 
where ordering is NOT NULL
and time1 is NOT NULL
and float_real is NOT NULL
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """select * from pvre204a 
order by ordering;"""
    output = _dci.cmdexec(stmt)
    
    #  Shorthand view with nulls:
    
    stmt = """create view svre201 as
select ordering , alwaysnull , btre201.char_1
, btre202.small_int , btre202.medium_int
from btre201, btre202;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """select * from svre201 
order by ordering;"""
    output = _dci.cmdexec(stmt)
    
    #  Shorthand view with nullable columns:
    #
    #  svre201b:   ordering     float_basic      y_to_d     ih_to_s
    #                  1       0.1200000E+01   1975-01-01   01:02:03
    
    stmt = """create view svre201b as
select t2.ordering,t2.float_basic,t2.y_to_d,t1.ih_to_s
from btre201 t1,
 btre204 t2
where t1.ih_to_s = t2.ih_to_s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """select * from svre201b 
order by ordering;"""
    output = _dci.cmdexec(stmt)
    
    #  svre201c:   ordering     alwaysnull       char_1
    #                     4              ?       C
    
    stmt = """create view svre201c as
select ordering, alwaysnull,char_1
from btre201 
where alwaysnull IS NULL
and char_1 IS NOT NULL
and ordering = 4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """select * from svre201c;"""
    output = _dci.cmdexec(stmt)
    
    #  svre201d:   ordering     float_basic      y_to_d
    #
    #                  1                   ?   ?
    #                  1       0.1200000E+01   1975-01-01
    #                  2                   ?   ?
    #                  3                   ?   ?
    #                  4       0.1200000E+01   1975-01-01
    #                  5                   ?   ?
    #                  6                   ?   ?
    #                  7                   ?   ?
    #                  8                   ?   ?
    #               9000       0.1200000E+01   1975-01-01
    #                  ?                   ?   ?
    
    stmt = """create view svre201d 
(small_int, float_basic, y_to_d) as
select ordering,float_basic,y_to_d
from btre201 
union all
select small_int,float_basic,y_to_d
from btre202 
union all
select ordering,float_basic,y_to_d
from btre204;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """select * from svre201d 
order by small_int;"""
    output = _dci.cmdexec(stmt)
    
    # svre201e:    VAR_CHAR_3  PIC_COMP_3    IH_TO_S    Y_TO_D
    #            ----------  ------------  ---------  ----------
    #
    #              AbC              1.00000  ?          ?
    #              zz               2.00000  ?          ?
    #              zy               2.00000  ?          ?
    #              rum            100.70000   01:02:03  1975-01-01
    #              ?                      ?  ?          ?
    #              ?                      ?  ?          ?
    #              ?                      ?  ?          ?
    #              ?                      ?  ?          ?
    #
    
    stmt = """create view svre201e as
select t1.var_char_3,t1.pic_comp_3,t1.ih_to_s,t2.y_to_d
from btre201 t1
left join
 btre202 t2
on t1.y_to_d = t2.y_to_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """select * from svre201e 
order by pic_comp_3;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE TINY(
C1      CHAR(13000)) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """CREATE TABLE TINY(
C1      CHAR(13000)) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    stmt = """CREATE TABLE TINY(
C1      CHAR(4058)) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    stmt = """CREATE TABLE TINY(        C1      CHAR(4058)) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    stmt = """CREATE TABLE TINY(        C1      CHAR(4048)) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    stmt = """CREATE TABLE TINY(        C1      CHAR(4027)) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    stmt = """Create Table btuns01 
(
char0_20            Character(8)          not null,
sbin0_2             Numeric(18) signed    not null,
udec0_10            Decimal(9) unsigned   not null,
varchar0_2          varchar(16)      not null,
sdec0_1000          PIC S9(9)             not null,
ubin0_20            PIC 9(7)V9(2) COMP    not null,    

char1_2             Character(16)         not null,
sdec1_uniq          Decimal(18) signed    not null,
sbin1_100           Numeric(4) signed     not null,
varchar1_uniq       varchar(8)       not null
)
attribute no audit;"""
    output = _dci.cmdexec(stmt)
    # _dci.expect_any_substr(output, '*ERROR[3070]*')
    
    stmt = """create unique index btuns01a
on btuns01 (sdec0_1000,sdec1_uniq);"""
    output = _dci.cmdexec(stmt)
    # _dci.expect_any_substr(output, '*ERROR[1004]*')
    
    stmt = """showlabel btuns01a;"""
    output = _dci.cmdexec(stmt)
    # _dci.expect_any_substr(output, '*ERROR[3225]*')
    
    _testmgr.testcase_end(desc)

def test002(desc="""a01"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """CREATE TABLE orders (
ordernum               PIC 9(3)   not null not droppable,
omonth                 PIC 9(2)   not null not droppable,
oday                   PIC 9(2)   not null not droppable,
oyear                  PIC 9(2)   not null not droppable,
dmonth                 PIC 9(2)   not null not droppable,
dday                   PIC 9(2)   not null not droppable,
dyear                  PIC 9(2)   not null not droppable,
salesman               PIC 9(4)   not null not droppable,
custnum                PIC 9(4)   not null not droppable,
PRIMARY KEY (ordernum) not droppable
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """CREATE INDEX order0 ON orders (salesman);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """CREATE INDEX order1 ON orders (custnum);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """CREATE TABLE customer (
custnum                PIC 9(4)  not null not droppable,
custname               PIC X(18) not null not droppable,
address                PIC X(22) not null not droppable,
city                   PIC X(14) not null not droppable,
state                  PIC X(12) not null not droppable,
PRIMARY KEY (custnum) not droppable
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """CREATE INDEX custome0 ON customer (custname);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """CREATE TABLE fromsup (
partnum                PIC 9(4)  not null not droppable,
suppnum                PIC 9(3)  not null not droppable,
partcost               PIC 9(6)V9(2) COMP not null not droppable,
PRIMARY KEY ( partnum, suppnum ) not droppable
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """CREATE TABLE odetail (
ordernum               PIC 9(3)  not null not droppable,
partnum                PIC 9(4)  not null not droppable,
quantity               PIC 9(3) COMP not null not droppable,
PRIMARY KEY ( ordernum, partnum ) not droppable
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """CREATE TABLE parts (
partnum                PIC 9(4)  not null not droppable,
partname               PIC X(18) not null not droppable,
inventory              PIC S9(3) COMP   not null not droppable,
location               PIC X(3)  not null not droppable,
price                  PIC 9(6)V9(2) COMP not null not droppable,
PRIMARY KEY (partnum) not droppable
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """CREATE INDEX parts0 ON  parts (partname);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """CREATE TABLE supplier (
suppnum                PIC 9(3)   not null not droppable,
suppname               PIC X(18)  not null not droppable,
address                PIC X(22)  not null not droppable,
city                   PIC X(14)  not null not droppable,
state                  PIC X(12)  not null not droppable,
PRIMARY KEY (suppnum) not droppable
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """CREATE INDEX supplyr0 ON supplier (suppname);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """CREATE TABLE region (
regnum                 PIC 9(2)     not null not droppable,
regname                PIC X(12)    not null not droppable,
location               VARCHAR (14) not null not droppable,
manager                PIC 9(4)     not null not droppable,
PRIMARY KEY (regnum) not droppable
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """CREATE INDEX region0 ON region (regname);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """CREATE TABLE branch (
regnum                 PIC 9(2)  not null not droppable,
branchnum              PIC 9(2)  not null not droppable,
branchname             VARCHAR (14)  not null not droppable,
manager                PIC 9(4) not null not droppable,
PRIMARY KEY ( regnum, branchnum ) not droppable
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """CREATE TABLE employee (
empnum                 PIC 9(4)   not null not droppable,
empname                PIC X(18)  not null not droppable,
regnum                 PIC 9(2)     not null not droppable,
branchnum              PIC 9(2)     not null not droppable,
job                    VARCHAR (12)  not null not droppable,
age                    PIC 9(2) COMP not null not droppable,
salary                 PIC 9(6) COMP not null not droppable,
vacation               PIC 9(2) COMP   not null not droppable,
PRIMARY KEY (empnum) not droppable
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """CREATE INDEX employe0 ON employee (empname);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """CREATE INDEX employe1 ON employee (regnum,branchnum);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    _testmgr.testcase_end(desc)

def test003(desc="""a02"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """CREATE VIEW empone AS SELECT
empnum
FROM employee;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """CREATE VIEW emppub AS SELECT
empnum
, empname
, regnum
, branchnum
, job
, vacation
FROM employee;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """CREATE VIEW expfroms AS SELECT
partnum
, suppnum
, partcost
FROM fromsup 
WHERE (partcost > 10000);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    _testmgr.testcase_end(desc)

def test004(desc="""a03"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """CREATE VIEW partsfor 
( col_1
, col_2
, col_3
, col_4
, col_5
, col_6
, col_7
, col_8
, col_9
, col_10
, col_11
, col_12
)
AS SELECT
partname
,        location
,        price
,        orders.ordernum
,        oyear
,        omonth
,        oday
,        dyear
,        dmonth
,        dday
,        salesman
,        custnum
FROM orders, odetail,
 parts 
WHERE orders.ordernum  = odetail.ordernum AND
( odetail.partnum = parts.partnum )
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """CREATE VIEW salecust 
AS SELECT empname
,        regnum
,        branchnum
,        custname
,        address
,        city
,        state
FROM orders, emppub,
 customer 
WHERE orders.salesman = emppub.empnum AND
( orders.custnum  = customer.custnum )
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """CREATE VIEW salecub 
AS SELECT
empname
,        branchname
,        custname
,        city
FROM branch,
 salecust 
WHERE salecust.branchnum = branch.branchnum
AND ( salecust.regnum    = branch.regnum    )
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """CREATE VIEW fsdetail 
( col_1
, col_2
, col_3
, col_4
, col_5
, col_6
)
AS SELECT fromsup.partnum
,                suppnum
,                partcost
,                ordernum
,        odetail.partnum
,                quantity
FROM odetail, fromsup 
WHERE ( odetail.partnum = fromsup.partnum )
AND ( quantity > 20 )
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    _testmgr.testcase_end(desc)

def test005(desc="""a04"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """INSERT INTO  orders 
VALUES ( 21, 1,10,78, 4,10,78, 205,1234);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  orders 
VALUES ( 25, 1,23,78, 6,15,78, 212,7777);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  orders 
VALUES ( 30, 2, 6,78, 7, 1,78, 222, 926);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  orders 
VALUES ( 32, 2,17,78, 7,20,78, 204,  21);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  orders 
VALUES ( 35, 3, 3,78, 8,10,78, 231, 543);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  orders 
VALUES ( 38, 3,19,78, 8,20,78, 218, 123);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  orders 
VALUES ( 41, 3,27,78, 9, 1,78, 207,7654);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  orders 
VALUES ( 45, 4,20,78, 9,15,78, 212, 324);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  orders 
VALUES ( 48, 5,12,78,10,10,78, 225,3333);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  orders 
VALUES ( 51, 6, 1,78,10,20,78, 210, 143);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  orders 
VALUES ( 66, 7, 9,78,11, 1,78, 205,3210);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  orders 
VALUES (122, 7,21,78,12,15,78, 221,5635);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """update statistics for table  orders on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """INSERT INTO  customer 
VALUES (  21,'CENTRAL UNIVERSITY',
'UNIVERSITY WAY        ','PHILADELPHIA  ','PENN        ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  customer 
VALUES ( 123,'BROWN MEDICAL CO  ',
'100 CALIFORNIA STREET ','SAN FRANCISCO ','CALIFORNIA  ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  customer 
VALUES ( 143,'STEVENS SUPPLY    ',
'2020 HARRIS STREET    ','DENVER        ','COLORADO    ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  customer 
VALUES ( 324,'PREMIER INSURANCE ',
'3300 WARBASH          ','LUBBOCK       ','TEXAS       ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  customer 
VALUES ( 543,'FRESNO STATE BANK ',
'2300 BROWN BLVD       ','FRESNO        ','CALIFORNIA  ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  customer 
VALUES ( 926,'METALL-AG.        ',
'12 WAGNERRING         ','FRANKFURT     ','GERMANY     ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  customer 
VALUES (1234,'DATASPEED         ',
'300 SAN GABRIEL WAY   ','NEW YORK      ','NEW YORK    ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  customer 
VALUES (3210,'BESTFOOD MARKETS  ',
'3333 PLELPS STREET    ','LINCOLN       ','NEBRASKA    ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  customer 
VALUES (3333,'DEUTSCHE STAHL    ',
'SIEMENS-STRASSE       ','DUISBURG      ','GERMANY     ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  customer 
VALUES (5635,'VEREINIGTE CHEMIE ',
'45 FRANKENSTRASSE     ','MUENCHEN      ','GERMANY     ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  customer 
VALUES (7654,'MOTOR DISTRIBUTING',
'2345 FIRST STREET     ','CHICAGO       ','ILLINOIS    ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  customer 
VALUES (7777,'SLEEPWELL HOTELS  ',
'9000 PETERS AVENUE    ','DALLAS        ','TEXAS       ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """update statistics for table  customer on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """INSERT INTO  fromsup VALUES ( 212,  1, 92000.00);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  fromsup VALUES ( 244, 1, 87000.00);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  fromsup VALUES (1403,  1, 22000.00);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  fromsup VALUES (2001,  1,  1500.00);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  fromsup VALUES (2002,  1,  1000.00);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  fromsup VALUES (2003,  1, 500.00);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  fromsup VALUES (2402, 1,  7500.00);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  fromsup VALUES (2403,  1,  9600.00);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  fromsup VALUES (3102,  1,  4800.00);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  fromsup VALUES (3103,  1, 10500.00);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  fromsup VALUES (3201,  1, 4800.00);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  fromsup VALUES (3302, 1,  2800.00);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  fromsup VALUES (4101,  6,  6000.00);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  fromsup VALUES (4101, 15,  6000.00);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  fromsup VALUES (4102,  6, 10000.00);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  fromsup VALUES (4102,  8, 12000.00);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  fromsup VALUES (4102, 15, 11000.00);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  fromsup VALUES (4103,  6, 20100.00);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  fromsup VALUES (4103,  8, 19300.00);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  fromsup VALUES (4103, 15, 19500.00);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  fromsup VALUES (5101,  8, 5800.00);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  fromsup VALUES (5101, 15,  5900.00);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  fromsup VALUES (5103,  8,  6200.00);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  fromsup VALUES (5103, 15,  6250.00);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  fromsup VALUES (5502,  2,  9100.00);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  fromsup VALUES (5504,  2, 1600.00);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  fromsup VALUES (5504, 6,  1580.00);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  fromsup VALUES (5504, 15,  1620.00);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  fromsup VALUES (5505, 15, 33000.00);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  fromsup VALUES (6201,  1,  5800.00);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  fromsup VALUES (6301,  1, 2900.00);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  fromsup VALUES (6302, 1,  4300.00);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  fromsup VALUES (6401,  2,  1200.00);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  fromsup VALUES (6401,  3,  1100.00);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  fromsup VALUES (6402,  2,  1100.00);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  fromsup VALUES (6402,  3, 1200.00);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  fromsup VALUES (6603, 2,  2600.00);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  fromsup VALUES (7102, 10,  6000.00);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  fromsup VALUES (7301,  1,  2400.00);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """update statistics for table  fromsup on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """INSERT INTO  odetail VALUES ( 21, 244,  1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  odetail VALUES ( 21,2001,  2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  odetail VALUES ( 21,2403,  2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  odetail VALUES ( 21,4103,  2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  odetail VALUES ( 25, 244,  1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  odetail VALUES ( 25,5103,  1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  odetail VALUES ( 25,6301,  2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  odetail VALUES ( 25,6402, 10);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  odetail VALUES ( 30, 244,  1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  odetail VALUES ( 30,2001,  2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  odetail VALUES ( 30,2002,  2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  odetail VALUES ( 30,2003,  2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  odetail VALUES ( 30,3102,  2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  odetail VALUES ( 30,4101,  2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  odetail VALUES ( 30,6302,  1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  odetail VALUES ( 32, 244,  1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  odetail VALUES ( 32,2001,  2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  odetail VALUES ( 32,2402,  6);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  odetail VALUES ( 32,3102,  1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  odetail VALUES ( 32,3202,  1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  odetail VALUES ( 32,3302,  1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  odetail VALUES ( 32,4102,  1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  odetail VALUES ( 32,5103,  1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  odetail VALUES ( 32,5504,  1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  odetail VALUES ( 32,6201,  1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  odetail VALUES ( 32,6301,  1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  odetail VALUES ( 32,6302,  1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  odetail VALUES ( 35, 244,  1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  odetail VALUES ( 35,2001,  2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  odetail VALUES ( 35,2403,  4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  odetail VALUES ( 35,3103,  2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  odetail VALUES ( 35,3302,  1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  odetail VALUES ( 35,4103,  2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  odetail VALUES ( 35,5503,  1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  odetail VALUES ( 35,6301,  1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  odetail VALUES ( 35,6302,  2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  odetail VALUES ( 38, 244,  1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  odetail VALUES ( 38,2402,  3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  odetail VALUES ( 38,3102,  1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  odetail VALUES ( 38,4102,  1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  odetail VALUES ( 38,5502,  1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  odetail VALUES ( 38,6201,  1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  odetail VALUES ( 38,6302,  1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  odetail VALUES ( 38,6402,  2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  odetail VALUES ( 41, 244,  1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  odetail VALUES ( 41,1403,  1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  odetail VALUES ( 41,2001,  3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  odetail VALUES ( 41,2002,  3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  odetail VALUES ( 41,2003,  3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  odetail VALUES ( 41,2403, 10);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  odetail VALUES ( 41,3103,  2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  odetail VALUES ( 41,3302,  2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  odetail VALUES ( 41,4103,  4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  odetail VALUES ( 41,5504,  2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  odetail VALUES ( 41,6201,  1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  odetail VALUES ( 41,6301,  4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  odetail VALUES ( 41,6302, 10);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  odetail VALUES ( 41,7301,  3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  odetail VALUES ( 45, 212,  1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  odetail VALUES ( 45,1403,  1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  odetail VALUES ( 45,2001,  2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  odetail VALUES ( 45,2002,  2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  odetail VALUES ( 45,2402,  6);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  odetail VALUES ( 45,2403,  2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  odetail VALUES ( 45,3102,  1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  odetail VALUES ( 45,4102,  3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  odetail VALUES ( 45,6301,  1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  odetail VALUES ( 45,6302,  3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  odetail VALUES ( 45,7301,  1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  odetail VALUES ( 48, 244,  1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  odetail VALUES ( 48,1403,  2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  odetail VALUES ( 48,2001,  2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  odetail VALUES ( 48,2002,  2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  odetail VALUES ( 48,2003,  2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  odetail VALUES ( 48,2403,  6);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  odetail VALUES ( 48,3103,  2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  odetail VALUES ( 48,3302,  1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  odetail VALUES ( 48,4103,  3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  odetail VALUES ( 48,5103,  1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  odetail VALUES ( 48,5504,  1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  odetail VALUES ( 48,6201,  1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  odetail VALUES ( 48,6302,  1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  odetail VALUES ( 48,7102,  1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  odetail VALUES ( 48,7301,  2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  odetail VALUES ( 51,1403,  4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  odetail VALUES ( 51,2001,  4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  odetail VALUES ( 51,2002,  4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  odetail VALUES ( 51,2003,  4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  odetail VALUES ( 51,2403, 16);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  odetail VALUES ( 51,3103,  5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  odetail VALUES ( 51,3202,  2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  odetail VALUES ( 51,3302,  1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  odetail VALUES ( 51,4103, 11);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  odetail VALUES ( 51,5103,  1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  odetail VALUES ( 51,5505,  1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  odetail VALUES ( 51,6301,  2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  odetail VALUES ( 51,6302,  2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  odetail VALUES ( 51,6402,  8);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  odetail VALUES ( 51,7102,  1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  odetail VALUES ( 66, 244,  1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  odetail VALUES ( 66,1403,  3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  odetail VALUES ( 66,2001,  5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  odetail VALUES ( 66,2403,  8);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  odetail VALUES ( 66,3102,  3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  odetail VALUES ( 66,3202,  1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  odetail VALUES ( 66,3302,  3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  odetail VALUES ( 66,4101,  1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  odetail VALUES ( 66,4102,  6);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  odetail VALUES ( 66,4103,  2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  odetail VALUES ( 66,5101,  1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  odetail VALUES ( 66,5502,  8);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  odetail VALUES ( 66,5504,  3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  odetail VALUES ( 66,6201,  1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  odetail VALUES ( 66,6301,  4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  odetail VALUES ( 66,6302,  5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  odetail VALUES ( 66,6401,  6);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  odetail VALUES ( 66,6402, 22);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  odetail VALUES ( 66,7102,  1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  odetail VALUES ( 66,7301,  2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  odetail VALUES (122,1403, 10);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  odetail VALUES (122,2002, 10);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  odetail VALUES (122,2403, 30);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  odetail VALUES (122,3103, 20);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  odetail VALUES (122,3201,  3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  odetail VALUES (122,4103, 40);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  odetail VALUES (122,5103,  3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  odetail VALUES (122,7102,  7);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  odetail VALUES (122,7301,  8);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """update statistics for table  odetail on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """INSERT INTO  parts 
VALUES ( 212,'SYSTEM 192KB CORE ',    7,'J87', 92000.00);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  parts 
VALUES ( 244,'SYSTEM 192KB SEMI ',    3,'B78', 87000.00);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  parts 
VALUES (1403,'PROC     96KB SEMI',   21,'A21', 22000.00);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  parts 
VALUES (2001,'DECIMAL ARITH     ', -100,'X10',  1500.00);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  parts 
VALUES (2002,'ENSCRIBE MICRO    ',  200,'X11',  1000.00);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  parts 
VALUES (2003,'COBOL MICRO       ',  200,'X12',   500.00);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  parts 
VALUES (2402,'MEM MOD 64K MOS   ',  -34,'H87',  7500.00);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  parts 
VALUES (2403,'MEM MOD 96K MOS   ',   12,'J88',  9600.00);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  parts 
VALUES (3102,'DISC CONT SINGLE  ',   12,'H76',  4800.00);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  parts 
VALUES (3103,'DISC CONT DUAL    ',   -4,'H87', 10500.00);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  parts 
VALUES (3201,'MAG TAPE CONT 8/16',    6,'J65',  4800.00);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  parts 
VALUES (3302,'LINE PRINTER CONT ',    9,'K94',  2800.00);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  parts 
VALUES (4101,'DISC 10MB         ',   14,'K87',  8000.00);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  parts 
VALUES (4102,'DISC 50MB         ',    9,'K45', 14500.00);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  parts 
VALUES (4103,'DISK 160MB        ',    7,'K43', 24500.00);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  parts 
VALUES (5101,'MAG TAPE DR 800BPI',    6,'K89',  7400.00);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  parts 
VALUES (5103,'MAG TAPE DR 8/16  ',    8,'L98',  8000.00);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  parts 
VALUES (5502,'LP  300 LPM       ',    6,'L98', 11500.00);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  parts 
VALUES (5504,'LP  900 LPM       ',   -1,'L88', 21000.00);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  parts 
VALUES (5505,'LP  1500LPM       ',    0,'L78', 42000.00);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  parts 
VALUES (6201,'SYNC CONTROLLER   ',  -16,'A34',  5800.00);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  parts 
VALUES (6301,'ASYNC CONTROLLER  ',  -21,'A35',  2900.00);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  parts 
VALUES (6302,'ASYNC EXTENSION   ',   34,'A36',  4300.00);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  parts 
VALUES (6401,'TERM CRT CHAR     ',   54,'V67',  1500.00);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  parts 
VALUES (6402,'TERM CRT PAGE     ',  -32,'V68',  1500.00);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  parts 
VALUES (6603,'TERM HARD COPY    ',   40,'V66',  3200.04);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  parts 
VALUES (7102,'CABINET LARGE     ',   20,'F76', 68000.05);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  parts 
VALUES (7301,'POWER MODULE      ',   32,'H76',  2400.06);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """update statistics for table  parts on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """INSERT INTO  supplier 
VALUES (  1,'TANDEM COMPUTERS  ',
'19333 VALLCO PARKWAY  ','CUPERTINO     ','CALIFORNIA  ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  supplier 
VALUES (  2,'DATA TERMINAL CO  ',
'2000 BAKER STREET     ','IRVINE        ','CALIFORNIA  ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  supplier 
VALUES (  3,'DISPLAY INC       ',
'7600 EMERSON          ','PALO ALTO     ','CALIFORNIA  ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  supplier 
VALUES (  6,'INFOMATION STORAGE',
'1000 INDUSTRY DRIVE   ','LEXINGTON     ','MASS        ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  supplier 
VALUES (  8,'MAGNETICS CORP    ',
'7777 FOUNTAIN WAY     ','SEATTLE       ','WASHINGTON  ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  supplier 
VALUES ( 10,'STEELWORK INC     ',
'6000 LINCOLN LANE     ','SUNNYVALE     ','CALIFORNIA  ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  supplier 
VALUES ( 15,'DATADRIVE         ',
'100  MACARTHUR        ','DALLAS        ','TEXAS       ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """update statistics for table  supplier on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """INSERT INTO  region VALUES ( 1,'EAST        ',
'NEW YORK' ,  29);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  region VALUES ( 2,'CENTRAL     ',
'CHICAGO'  , 104);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  region VALUES ( 3,'WEST        ',
'DALLAS'   ,  72);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  region VALUES ( 4,'CANADA      ',
'TORONTO'  , 343);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  region VALUES ( 5,'GERMANY     ',
'FRANKFURT',  43);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  region VALUES ( 6,'ENGLAND     ',
'LONDON'   ,  87);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  region VALUES (99,'HEADQUARTERS',
'CUPERTINO',   1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """update statistics for table  region on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """INSERT INTO  branch 
VALUES ( 1, 1,'NEW YORK'     ,  75);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  branch 
VALUES ( 1, 2,'NEW JERSEY'   , 129);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  branch 
VALUES ( 2, 1,'CHICAGO'      ,  23);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  branch 
VALUES ( 2, 2,'HOUSTON'      , 109);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  branch 
VALUES ( 2, 3,'ST. LOUIS'    , 111);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  branch 
VALUES ( 3, 1,'DALLAS'       , 321);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  branch 
VALUES ( 3, 2,'LOS ANGELES'  , 337);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  branch 
VALUES ( 3, 3,'SAN FRANCISCO',  89);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  branch 
VALUES ( 4, 1,'TORONTO'      , 178);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  branch 
VALUES ( 4, 2,'VANCOUVER'    ,  93);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  branch 
VALUES ( 5, 1,'FRANKFURT'    , 180);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  branch 
VALUES ( 5, 2,'DUESSELDORF'  ,  39);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  branch 
VALUES ( 5, 3,'MUENCHEN'     ,  32);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  branch 
VALUES ( 6, 1,'LONDON'       ,  65);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  branch 
VALUES (99, 1,'CUPERTINO'    ,  88);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """update statistics for table  branch on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """INSERT INTO  employee 
VALUES (   1,'ROGER GREEN       ',99, 1,'MANAGER'   ,37, 39500, 2)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  employee 
VALUES (  23,'JERRY HOWARD      ', 2, 1,'MANAGER'   ,34, 37000,10)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  employee 
VALUES (  29,'JACK RAYMOND      ', 1, 1,'MANAGER'   ,39, 36000, 1)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  employee 
VALUES (  32,'THOMAS RUDLOFF    ', 5, 3,'MANAGER'   ,43, 38000, 4)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  employee 
VALUES (  39,'KLAUS SAFFERT     ', 5, 2,'MANAGER'   ,35, 35000,12)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  employee 
VALUES (  43,'PAUL WINTER       ', 5, 1,'MANAGER'   ,41, 40000, 5)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  employee 
VALUES (  65,'SUSAN HENDERSON   ', 6, 1,'MANAGER'   ,45, 38000, 9)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  employee 
VALUES (  72,'GLENN THOMAS      ', 3, 1,'MANAGER'   ,48, 40000,14)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  employee 
VALUES (  75,'TIM WALKER        ', 1, 1,'MANAGER'   ,29, 32000, 7)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  employee 
VALUES (  87,'ERIC BROWN        ', 6, 1,'MANAGER'   ,31, 39000,10)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  employee 
VALUES (  89,'PETER SMITH       ', 3, 3,'MANAGER'   ,36, 37000, 4)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  employee 
VALUES (  93,'DONALD TAYLOR     ', 4, 2,'MANAGER'   ,31, 33000, 0)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  employee 
VALUES ( 104,'DAVID STRAND      ', 2, 1,'MANAGER'   ,32, 39000, 2)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  employee 
VALUES ( 109,'STEVE COOK        ', 2, 2,'MANAGER'   ,39, 38000,15)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  employee 
VALUES ( 111,'SHERRIE WONG      ', 2, 3,'MANAGER'   ,43, 40000, 0)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  employee 
VALUES ( 129,'TONY CRAFT        ', 1, 2,'MANAGER'   ,35, 37000, 5)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  employee 
VALUES ( 178,'LINDA JONES       ', 4, 1,'MANAGER'   ,40, 38000, 8)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  employee 
VALUES ( 180,'MANFRED CONRAD    ', 5, 1,'MANAGER'   ,30, 32000,14)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  employee 
VALUES ( 201,'JIM HERMAN        ', 1, 1,'SALESMAN'  ,27, 19000,13)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  employee 
VALUES ( 202,'LARRY CLARK       ', 1, 1,'SYS.-ANAL.',30, 25000, 7)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  employee 
VALUES ( 203,'KATHRYN DAY       ', 1, 1,'SECRETARY' ,24, 12000,12)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  employee 
VALUES ( 204,'TOM HALL          ', 1, 1,'SALESMAN'  ,35, 26000, 0)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  employee 
VALUES ( 205,'GEORGE FORSTER    ', 1, 2,'SALESMAN'  ,39, 30000, 4)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  employee 
VALUES ( 206,'DAVE FISHER       ', 2, 1,'SALESMAN'  ,32, 25000, 7)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  employee 
VALUES ( 207,'MARK FOLEY        ', 2, 1,'SALESMAN'  ,27, 23000,10)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  employee 
VALUES ( 208,'SUE CRAMER        ', 2, 1,'SECRETARY' ,47, 19000, 6)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  employee 
VALUES ( 209,'SUSAN CHAPMAN     ', 2, 1,'PROGRAMMER',26, 17000, 0)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  employee 
VALUES ( 210,'RICHARD BARTON    ', 2, 2,'SALESMAN'  ,39, 29000, 7)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  employee 
VALUES ( 211,'JIMMY SCHNEIDER   ', 2, 3,'SYS.-ANAL.',34, 26000, 0)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  employee 
VALUES ( 212,'JONATHAN MITCHEL  ', 3, 1,'SALESMAN'  ,39, 32000,15)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  employee 
VALUES ( 213,'ROBERT WHITE      ', 3, 1,'ENGINEER'  ,29, 30000, 4)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  employee 
VALUES ( 214,'JULIA KELLY       ', 3, 1,'SECRETARY' ,21, 50000, 1)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  employee 
VALUES ( 215,'WALTER LANCASTER  ', 3, 2,'SALESMAN'  ,49, 33000,15)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  employee 
VALUES ( 216,'JOHN JONES        ', 3, 2,'SYS.-ANAL.',31, 30000, 7)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  employee 
VALUES ( 217,'MARLENE BONNY     ', 3, 3,'SYS.-ANAL.',25, 24000, 9)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  employee 
VALUES ( 218,'GEORGE FRENCHMAN  ', 3, 3,'SALESMAN'  ,35, 31000, 0)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  employee 
VALUES ( 219,'DAVID TERRY       ', 3, 3,'PROGRAMMER',37, 27000,12)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  employee 
VALUES ( 220,'JOHANN HUBER      ', 5, 1,'SYS.-ANAL.',35, 33000,10)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  employee 
VALUES ( 221,'OTTO SCHNABL      ', 5, 1,'SALESMAN'  ,39, 33000, 1)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  employee 
VALUES ( 222,'MARTIN SCHAEFER   ', 5, 1,'SALESMAN'  ,32, 31000, 1)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  employee 
VALUES ( 223,'HERBERT KARAJAN   ', 5, 1,'ENGINEER'  ,33, 29000, 6)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  employee 
VALUES ( 224,'MARIA JOSEF       ', 5, 1,'SECRETARY' ,19, 18000,10)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  employee 
VALUES ( 225,'KARL HELMSTED     ', 5, 2,'SALESMAN'  ,34, 32000,11)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  employee 
VALUES ( 226,'HEIDI WEIGL       ', 5, 2,'SECRETARY' ,55, 22000,14)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  employee 
VALUES ( 227,'XAVER SEDLMEYER   ', 5, 3,'SYST.-ANAL',30, 30000, 4)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  employee 
VALUES ( 228,'PETE WELLINGTON   ',99, 1,'SYST.-ANAL',39, 32000, 2)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  employee 
VALUES ( 229,'GEORGE STRICKER   ',99, 1,'SYST.-ANAL',36, 32222, 6)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  employee 
VALUES ( 230,'ROCKY LEWIS       ',99, 1,'PROGRAMMER',32, 24000, 0)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  employee 
VALUES ( 231,'HERB ALBERT       ',99, 1,'SALESMAN'  ,39, 33000, 2)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  employee 
VALUES ( 232,'THOMAS SPINNER    ',99, 1,'SALESMAN'  ,33, 30000, 5)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  employee 
VALUES ( 233,'TED MCDONNALDS    ',99, 1,'ENGINEER'  ,29, 29000, 0)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  employee 
VALUES ( 234,'MARY MILLER       ',99, 1,'SECRETARY' ,22, 16000, 9)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  employee 
VALUES ( 235,'MIRIAM KING       ',99, 1,'SECRETARY' ,24, 18000,11)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  employee 
VALUES ( 321,'BILL WINN         ', 3, 1,'MANAGER'   ,28, 32000, 0)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  employee 
VALUES ( 337,'DAVE CLARK        ', 3, 2,'MANAGER'   ,36, 37000, 2)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """INSERT INTO  employee 
VALUES ( 343,'ALAN TERRY        ', 4, 1,'MANAGER'   ,39, 39500, 0)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """update statistics for table  employee on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    _testmgr.testcase_end(desc)

def test006(desc="""a05"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """CREATE TABLE btempkey ( some_data PIC 9(3) not null not droppable) no partition
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """CREATE TABLE btemprel ( some_data PIC 9(3) not null not droppable ) no partition
--        STORE BY ENTRY ORDER
--        ATTRIBUTE
--                NO AUDIT
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """CREATE INDEX btempre0 ON btemprel (some_data) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """CREATE TABLE btempent ( some_data PIC 9(3) not null not droppable ) no partition
--        STORE BY ENTRY ORDER
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE btsel01 (
-- Fixed length character string
char_1                 CHAR(1)           not null not droppable
, char_10                CHAR(10)          not null not droppable
, pic_x_1                PIC X(1)          not null not droppable
, pic_x_7                PIC X(7)          not null not droppable
, pic_x_long             PIC X(200)        not null not droppable
-- Varying length character string.
, var_char               VARCHAR(253)      not null not droppable
-- Binary
, binary_signed          numeric (4, 0) signed not null not droppable
, binary_32_u            numeric (9,2) UNSIGNED not null not droppable
, binary_64_s            numeric (18,3) SIGNED not null not droppable
, pic_comp_1             numeric(10,0) signed  not null not droppable
, pic_comp_2             numeric(2,2) signed   not null not droppable
, pic_comp_3             numeric(8,5) signed   not null not droppable
, small_int              SMALLINT              not null not droppable
, medium_int             INTEGER UNSIGNED      not null not droppable
, large_int              LARGEINT              not null not droppable
-- Fixed length character string
, decimal_1              DECIMAL (1, 0)        not null not droppable
, decimal_2_signed       DECIMAL (2,2) SIGNED  not null not droppable
, decimal_3_unsigned     DECIMAL (3,0) UNSIGNED    not null not droppable
, pic_decimal_1          decimal(2,1) not null not droppable
, pic_decimal_2          DECIMAL(3,3) signed not null not droppable
, pic_decimal_3          DECIMAL(1,0) signed not null not droppable
, PRIMARY KEY (binary_signed) not droppable
)
-- Physical specs
-- ATTRIBUTE
--    blocksize 4096
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    # Index the table with simple, 1-column indexes:
    
    stmt = """CREATE INDEX btsel01a ON btsel01 ( pic_x_1 );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """CREATE INDEX btsel01b ON btsel01 ( decimal_2_signed );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """CREATE INDEX btsel01c ON btsel01 ( pic_comp_3 );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """CREATE INDEX btsel01d ON btsel01 ( pic_x_long );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """CREATE TABLE btsel02 (
pic_x_1                PIC X(1)  not null not droppable
) no partition
--      STORE BY ENTRY ORDER
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """CREATE TABLE btsel03 (
pic_x_7        PIC X(7)            not null not droppable
, binary_32_u    numeric (9,2) UNSIGNED  not null not droppable
-- Check on default for strings.
, pic_x4_a       PIC X(4)                 not null not droppable
, pic_9_7        PIC 9(7)                    not null not droppable
, binary_64_s    numeric (18,2) SIGNED      not null not droppable
) no partition
--      STORE BY ENTRY ORDER
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """CREATE TABLE btsel04 (
var_char               VARCHAR(251)           not null not droppable
, medium_int             INTEGER SIGNED         not null not droppable
, pic_x_7                PIC X(7)               not null not droppable
, pic_comp_1             numeric (10,0) signed  not null not droppable
) no partition
--      STORE BY ENTRY ORDER
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """CREATE INDEX btsel04a ON btsel04 ( pic_x_7 );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    # Limit of 251 byte on UNIQUE VARCHAR for alternate index.
    stmt = """CREATE UNIQUE INDEX btsel04b
--     CREATE INDEX btsel04b
ON btsel04 ( var_char )
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """CREATE TABLE btsel05 (
pic_x_a                PIC X(3)           not null not droppable
, pic_x_b                PIC X(1)           not null not droppable
, pic_x_c                PIC X(2)           not null not droppable
, col_1                  CHAR(5)            not null not droppable
, col_2                  CHAR(5)            not null not droppable
, col_3                  PIC X(5)           not null not droppable
, col_4                  PIC X(5)           not null not droppable
, col_5                  PIC X(5)           not null not droppable
, col_6                  PIC X(5)           not null not droppable
, col_7                  PIC X(5)           not null not droppable
, col_8                  PIC X(5)           not null not droppable
, col_9                  VARCHAR(5)         not null not droppable
, col_10                 VARCHAR(5)         not null not droppable
) no partition
--      STORE BY ENTRY ORDER
--      ATTRIBUTE
--        NO AUDIT
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    # Index the table with 3_column index, reversing order of columns:
    
    stmt = """CREATE INDEX btsel05a
ON btsel05 ( pic_x_c , pic_x_b , pic_x_a );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """CREATE TABLE btsel06 (
pic_x_a                PIC X(3)           not null not droppable
, pic_x_b                PIC X(1)           not null not droppable
, pic_x_c                PIC X(2)           not null not droppable
-- Stored in 1 word
, col_1                  numeric (4, 0) UNSIGNED   not null not droppable
, col_2                  numeric (4, 0) UNSIGNED   not null not droppable
, col_3                  PIC     9(4) COMP      not null not droppable
, col_4                  PIC     9(4) COMP      not null not droppable
, col_5                  SMALLINT    UNSIGNED   not null not droppable
, col_6                  SMALLINT    UNSIGNED   not null not droppable
, col_7                  DECIMAL (4,0) UNSIGNED   not null not droppable
, col_8                  DECIMAL (4, 0) UNSIGNED   not null not droppable
, col_9                  PIC    9(4)            not null not droppable
, col_10                 PIC    9(4)            not null not droppable
-- Stored in 2 words (Double word).
, col_21                 numeric (9, 0) SIGNED     not null not droppable
, col_22                 numeric (9, 0) SIGNED     not null not droppable
, col_23                 numeric(9,0)     not null not droppable
, col_24                 numeric(9,0)     not null not droppable
, col_25                 INTEGER     SIGNED     not null not droppable
, col_26                 INTEGER     SIGNED     not null not droppable
, col_27                 DECIMAL (9, 0) SIGNED     not null not droppable
, col_28                 DECIMAL (9, 0) SIGNED     not null not droppable
, col_29                   decimal(9,0)         not null not droppable
, col_30                 decimal(9,0)          not null not droppable
-- Stored in 2 words (Double word, involving scale).
, col_41                 numeric (9, 2) UNSIGNED not null not droppable
, col_42                 numeric (9, 2) UNSIGNED not null not droppable
, col_43                 numeric(9,2) unsigned   not null not droppable
, col_44                 numeric(9,2) unsigned  not null not droppable
, col_45                 DECIMAL (9,2) UNSIGNED not null not droppable
, col_46                 DECIMAL (9,2) UNSIGNED not null not droppable
, col_47                 decimal(9,2) unsigned  not null not droppable
, col_48                 decimal(9,2) unsigned  not null not droppable
-- Stored in 4 words (Quad word).
, col_61                 numeric (18, 0)   SIGNED  not null not droppable
, col_62                 numeric (18, 0)   SIGNED  not null not droppable
, col_63                 numeric(18,0)     not null not droppable
, col_64                 numeric(18,0)     not null not droppable
, col_65                 LARGEINT      SIGNED   not null not droppable
, col_66                 LARGEINT      SIGNED   not null not droppable
, col_67                 DECIMAL (18,0)  SIGNED   not null not droppable
, col_68                 DECIMAL (18,0)  SIGNED   not null not droppable
, col_69                 decimal(18,0)          not null not droppable
, col_70                 decimal(18,0)         not null not droppable
, PRIMARY KEY ( pic_x_a, pic_x_b, pic_x_c ) not droppable
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """CREATE TABLE btsel07 (
pic_x_a                PIC X(3)           not null not droppable
, pic_x_b                PIC X(1)           not null not droppable
, pic_x_c                PIC X(2)           not null not droppable
, PRIMARY KEY ( pic_x_c, pic_x_b, pic_x_a ) not droppable
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    # Simple index:
    
    stmt = """CREATE INDEX btsel07a ON btsel07 ( pic_x_a );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """CREATE TABLE btsel08 (
large_int              LARGEINT    not null not droppable
, pic_252                PIC X(246)     not null not droppable
, pic_1                  PIC X          not null not droppable
, PRIMARY KEY ( large_int DESC ) not droppable
--      , PRIMARY KEY ( large_int )
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    # Index the table with fields adding up to maximum:
    
    stmt = """CREATE INDEX btsel08a ON btsel08 ( pic_252 , pic_1 );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """CREATE TABLE btsel09 (
pic_x_a                PIC X(3)       not null not droppable
, pic_x_2                PIC X(4)       not null not droppable
, pic_x_3                PIC X(1)       not null not droppable
, pic_x_4                PIC X(5)       not null not droppable
, pic_x_5                PIC 9(1)       not null not droppable
, pic_x_6                PIC 9(2)       not null not droppable
, pic_x_7                PIC 9(3)       not null not droppable
, PRIMARY KEY ( pic_x_a DESC, pic_x_6 DESC ) not droppable
--     , PRIMARY KEY ( pic_x_a, pic_x_6)
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """CREATE INDEX btsel09a
ON btsel09 ( pic_x_a )
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """CREATE TABLE btsel10 (
pic_x_a                PIC X(3)           not null not droppable
, pic_x_7                PIC X(7)               not null not droppable
, pic_9_7                PIC 9(7)               not null not droppable
, char_10                CHAR(10)               not null not droppable
, decimal_10             DECIMAL (10, 0)           not null not droppable
, binary_unsigned        numeric (4, 0) unsigned   not null not droppable
, binary_32_signed       numeric (9, 0) SIGNED     not null not droppable
, PRIMARY KEY ( pic_9_7 ASC, pic_x_7 DESC, pic_x_a ASC) not droppable
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """CREATE INDEX btsel10a ON btsel10 ( pic_x_a );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """CREATE TABLE btsel11 (
pic_x_a                PIC X(3)           not null not droppable
, pic_x_7                PIC X(7)               not null not droppable
, pic_9_7                PIC 9(7)               not null not droppable
, char_10                CHAR(10)               not null not droppable
, decimal_10             DECIMAL (10, 0)           not null not droppable
, binary_unsigned        numeric (4, 0) unsigned   not null not droppable
, binary_32_signed       numeric (9, 0) SIGNED     not null not droppable
, PRIMARY KEY ( decimal_10 DESC, pic_x_a ASC, pic_9_7 DESC) not droppable
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """CREATE TABLE btsel12 (
data_x3                PIC X(3)               not null not droppable
, data_93                PIC 9(3)               not null not droppable
, PRIMARY KEY ( data_x3 ) not droppable
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """CREATE INDEX btsel12a ON btsel12 ( data_93 );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """CREATE TABLE btsel13 (
data_93                PIC 9(3)               not null not droppable
, PRIMARY KEY ( data_93 ) not droppable
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """CREATE TABLE btsel14 (
data_93                PIC 9(3)               not null not droppable
, PRIMARY KEY ( data_93 ) not droppable
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """CREATE TABLE btsel15 (
small_int              SMALLINT               not null not droppable
, data_93                PIC 9(3)               not null not droppable
, PRIMARY KEY ( data_93 ) not droppable
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """CREATE TABLE btsel16 (
small_int              SMALLINT               not null not droppable
, data_93                PIC 9(3)               not null not droppable
) no partition
-- Defaults to SYSKEY
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """CREATE INDEX btsel16a ON btsel16 ( small_int );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """CREATE TABLE btsel17 (
small_int              SMALLINT               not null not droppable
, data_93                PIC 9(3)               not null not droppable
) no partition
--      STORE BY ENTRY ORDER
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """CREATE INDEX btsel17a ON btsel17 ( small_int );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """CREATE TABLE btsel18 (
binary_signed          numeric (4, 0) signed     not null not droppable
, small_int              SMALLINT               not null not droppable
, data_93                PIC 9(3)               not null not droppable
) no partition
--      STORE BY ENTRY ORDER
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """CREATE INDEX btsel18a ON btsel18 ( small_int );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """CREATE TABLE btsel19 (
binary_signed          numeric (4, 0) signed     not null not droppable
, data_93                PIC 9(3)               not null not droppable
, PRIMARY KEY (binary_signed) not droppable
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """CREATE TABLE btsel20 (
binary_signed          numeric (4, 0) signed     not null not droppable
, data_93                PIC 9(3)               not null not droppable
, PRIMARY KEY (binary_signed) not droppable
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """CREATE TABLE btsel21 (
pic_comp_2             numeric(2,2)       not null not droppable
, binary_signed          numeric (4, 0) signed     not null not droppable
, data_93                PIC 9(3)               not null not droppable
, PRIMARY KEY (pic_comp_2) not droppable
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """CREATE INDEX btsel21a ON btsel21 ( binary_signed );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """CREATE TABLE btsel22 (
pic_comp_2             numeric(2,2)       not null not droppable
, data_93                PIC 9(3)               not null not droppable
, PRIMARY KEY (pic_comp_2) not droppable
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """CREATE TABLE btsel23 (
pic_comp_2             numeric(2,2)     not null not droppable
, data_93                PIC 9(3)               not null not droppable
, PRIMARY KEY (data_93) not droppable
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """CREATE INDEX btsel23a ON btsel23 ( pic_comp_2 );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """CREATE TABLE btsel24 (
pic_comp_2             numeric(2,2)      not null not droppable
, data_x3                PIC X(3)               not null not droppable
, PRIMARY KEY (pic_comp_2) not droppable
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """CREATE TABLE btsel25 (
--       column pic_x_1 can be linked with btsel01, btsel05.
pic_x_1                PIC X(1)            not null not droppable
--       column pic_x_3 can be linked with same in btsel05/7 and 9/11.
, pic_x_3                PIC X(3)           not null not droppable
) no partition    

-- Defaults to SYSKEY
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """CREATE TABLE btsel26 (
selector                  char(1)            not null not droppable
, large_bin_1               largeint           not null not droppable
, large_bin_2               numeric (18, 0) signed  not null not droppable
, large_dec_1               decimal (18, 0) signed  not null not droppable
, large_dec_2               decimal(18,0)           not null not droppable
, small_bin_1               numeric(18,18)          not null not droppable
, small_bin_2               numeric (18,18) signed  not null not droppable
, small_dec_1               decimal (18,18)         not null not droppable
, small_dec_2               decimal(18,18)          not null not droppable
, semi_large_bin_1          numeric(17,0)           not null not droppable
, semi_large_bin_2          numeric(17,0)           not null not droppable
, eight_one_bin             numeric(9,1)            not null not droppable
, one_nine_bin              numeric(10,9)           not null not droppable
, nine_one_bin              numeric (10,1)          not null not droppable
, one_eight_bin             numeric(9,8)            not null not droppable
, nine_zero_bin_u           numeric(9,0) unsigned   not null not droppable
, zero_nine_bin_u           numeric(9,9) unsigned   not null not droppable
, nine_zero_dec_u           decimal (9, 0) unsigned not null not droppable
, zero_nine_dec_u           decimal(9,9)   unsigned not null not droppable
, zero_one_bin              numeric(1,1)            not null not droppable
) no partition
-- Defaults to SYSKEY
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """CREATE INDEX btsel26a ON btsel26 ( large_dec_1 );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """CREATE TABLE btsel27 (
selector                  char(1)                not null not droppable
, two_four_bin              numeric(6,4) not null not droppable
, one_one_bin               numeric(2,1)   not null not droppable
) no partition    

-- Defaults to SYSKEY
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    _testmgr.testcase_end(desc)

def test007(desc="""a06"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """CREATE VIEW pvsel01 
AS SELECT
binary_signed
, large_int
, medium_int
, pic_decimal_3
, pic_x_1
, pic_x_7
, small_int
FROM btsel01 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """CREATE VIEW pvsel02 
AS SELECT *
FROM btsel02 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """CREATE VIEW pvsel03 
( new_name_1
, new_name_2
, new_name_3
, new_name_4
)
AS SELECT
pic_9_7
, binary_32_u
, pic_x_7
, SYSKEY
FROM btsel03 
WHERE ( pic_9_7 < 100) AND
NOT ( binary_32_u BETWEEN 10 AND pic_9_7 ) AND
pic_x_7 IN ( '7' , 'A', 'B' )
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """CREATE VIEW pvsel04 
AS SELECT *
FROM btsel04 
WHERE ( pic_comp_1 > 100 )
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    _testmgr.testcase_end(desc)

def test008(desc="""a07"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """CREATE VIEW svsel01 
AS SELECT *
FROM btsel10 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """CREATE VIEW svsel02 
AS SELECT
binary_unsigned
, pic_x_a
, pic_x_7
, decimal_10
FROM btsel10 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """CREATE VIEW svsel03 
AS SELECT *
FROM btsel10 
WHERE ( decimal_10 > 100 )
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """CREATE VIEW svsel04 
( new_name_1
, new_name_2
, new_name_3
)
AS SELECT
pic_x_a
, pic_x_7
, char_10
FROM btsel10 
WHERE ( pic_x_7 < 'the' ) AND
NOT ( decimal_10 BETWEEN 10 AND pic_9_7 )
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """CREATE VIEW svsel05 
( new_name_ks_s
, new_name_ks_x
, new_name_es_s
, new_name_es_x
)
AS SELECT
 btsel05.SYSKEY
, btsel05.pic_x_b
, btsel25.SYSKEY
, btsel25.pic_x_1
FROM btsel05, btsel25 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """CREATE VIEW svsel06 
( new_name_ks_x
, new_name_es_x
)
AS SELECT
 btsel05.pic_x_b
, btsel25.pic_x_1
FROM btsel05, btsel25 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """CREATE VIEW svsel07 
( count_all
, avg_distinct
, avg_all
, max_all
, min_all
, sum_all
)
AS SELECT
count (*)
, avg   ( distinct binary_32_u )
, avg   ( all binary_32_u )
, max   ( all (binary_32_u + pic_9_7 ) )
, min   ( (pic_9_7 - binary_32_u) / binary_64_s )
, sum   ( all (binary_32_u - pic_9_7 ) )
FROM btsel03 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """CREATE VIEW svsel08 
( max_distinct )
AS SELECT
max   ( distinct binary_32_u )
FROM btsel03 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """CREATE VIEW svsel09 
( min_distinct )
AS SELECT
min   ( distinct binary_32_u )
FROM btsel03 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """CREATE VIEW svsel10 
( count_distinct )
AS SELECT
count ( distinct binary_32_u )
FROM btsel03 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """CREATE VIEW svsel11 
( col_1
, col_2
, col_3
, col_4
, col_5
, col_6
, col_7
, col_8
)
AS SELECT
 btsel01.binary_signed
, btsel01.large_int
, btsel01.medium_int
, btsel01.pic_decimal_3
, btsel01.pic_x_1
, btsel01.pic_x_7
, btsel01.small_int
, btsel03.pic_x_7
FROM btsel01, btsel03 
-- For shorthand VIEW (unlike protection VIEW) WHERE clause can
-- reference columns not found in SELECT list:
WHERE btsel01.binary_64_s = btsel03.binary_64_s
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """CREATE VIEW svsel12 (
col_1
, col_3
, col_4
, col_5
)
AS SELECT
sum (distinct btsel01.binary_signed)
, AVG (btsel01.pic_decimal_3)
, MAX (btsel01.pic_x_1)
, MIN (btsel01.pic_x_7)
FROM btsel01, btsel03 
-- For shorthand VIEW (unlike protection VIEW) WHERE clause can
-- reference columns not found in SELECT list:
WHERE btsel01.binary_64_s > btsel03.binary_64_s AND
( btsel01.pic_x_7 <> btsel03.pic_x_7 )
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """CREATE VIEW svsel13(new_name_1, new_name_2, new_name_3, new_name_4,
var_char, medium_int, pic_x_7, pic_comp_1)
AS SELECT *
FROM pvsel03, pvsel04 
WHERE pvsel03.new_name_3 = pvsel04.pic_x_7
--   CATALOG <subvol_for_data>
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """CREATE VIEW svsel14 
AS SELECT
new_name_1, new_name_3
FROM svsel13 
GROUP BY
new_name_1, new_name_3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """CREATE VIEW svsel15 
-- For columns for btsel05
( mixed_1 , mixed_2 , mixed_3 , mixed_4 , mixed_5
-- For columns for btsel06
, mixed_11, mixed_12, mixed_13
-- For columns for btsel07
, mixed_21, mixed_22, mixed_23
)
AS SELECT btsel05.pic_x_a , btsel05.pic_x_b , btsel05.pic_x_c
, btsel05.col_1   , btsel05.col_2
, btsel06.pic_x_a , btsel06.pic_x_b , btsel06.pic_x_c
, btsel07.*
FROM btsel05, btsel06,
 btsel07 
WHERE btsel05.pic_x_a = btsel06.pic_x_a
AND btsel06.pic_x_b = btsel07.pic_x_b
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """CREATE VIEW svsel16 
AS SELECT btsel12.data_x3
, btsel12.data_93
, btsel15.small_int
, btsel18.binary_signed
, btsel23.pic_comp_2
FROM btsel12, btsel13,
 btsel14, btsel15,
 btsel16, btsel17,
 btsel18, btsel19,
 btsel20, btsel21,
 btsel22, btsel23 
WHERE  btsel12.data_93 = btsel13.data_93
AND (btsel12.data_93 = btsel14.data_93)
AND (btsel12.data_93 = btsel15.data_93)
AND (btsel15.small_int = btsel16.small_int)
AND (btsel15.small_int = btsel17.small_int)
AND (btsel15.small_int = btsel18.small_int)
AND (btsel18.binary_signed = btsel19.binary_signed)
AND (btsel18.binary_signed = btsel20.binary_signed)
AND (btsel18.binary_signed = btsel21.binary_signed)
AND (btsel21.pic_comp_2    = btsel22.pic_comp_2)
AND (btsel21.pic_comp_2 = btsel23.pic_comp_2 )
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """CREATE VIEW  svsel17 
( a , b , c )
AS SELECT svsel16.data_x3
, svsel16.pic_comp_2
, btsel24.data_x3
FROM svsel16, btsel24 
WHERE svsel16.data_x3 = btsel24.data_x3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """CREATE   VIEW svsel18 
AS SELECT btsel12.data_x3
, btsel12.data_93
, btsel15.small_int
, btsel18.binary_signed
FROM btsel12, btsel13,
 btsel14, btsel15,
 btsel16, btsel17,
 btsel18, btsel19,
 btsel20 
WHERE btsel12.data_93   = btsel13.data_93
AND (btsel12.data_93       = btsel14.data_93)
AND (btsel12.data_93       = btsel15.data_93)
AND (btsel15.small_int     = btsel16.small_int)
AND (btsel15.small_int     = btsel17.small_int)
AND (btsel15.small_int     = btsel18.small_int)
AND (btsel18.binary_signed = btsel19.binary_signed)
AND (btsel18.binary_signed = btsel20.binary_signed)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """CREATE   VIEW svsel19 
AS SELECT btsel12.data_x3
, btsel12.data_93
, btsel15.small_int
, btsel18.binary_signed
, btsel23.pic_comp_2
FROM btsel12, btsel13,
 btsel14, btsel15,
 btsel16, btsel17,
 btsel18, btsel19,
 btsel20, btsel21,
 btsel22, btsel23 
WHERE btsel12.data_93   = btsel13.data_93
AND (btsel12.data_93       = btsel14.data_93)
AND (btsel12.data_93       = btsel15.data_93)
AND (btsel15.small_int     = btsel16.small_int)
AND (btsel15.small_int     = btsel17.small_int)
AND (btsel15.small_int     = btsel18.small_int)
AND (btsel18.binary_signed = btsel19.binary_signed)
AND (btsel18.binary_signed = btsel20.binary_signed)
AND (btsel18.binary_signed = btsel21.binary_signed)
AND (btsel21.pic_comp_2    = btsel22.pic_comp_2)
AND (btsel21.pic_comp_2    = btsel23.pic_comp_2)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    _testmgr.testcase_end(desc)

def test009(desc="""a08"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """insert into btsel01 values ('A','steven','C','walter','bob',
'B',50,50,200,50,0.12,100.9,
10,10000,1000000000,4,.5,90,
1.1,0.1,1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel01 values ('A','bobby','A','bobby','bop',
'B',60,60,1200,60,0.79,100.99,
1000,8000,-1000,5,.6,100,
2.1,0.2,2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel01 values
('D','steven','B','9','bat','thomas',
8000,70,2000,500,0.10,100.999,
90,10000,1000,7,.7,110,
3.1,0.3,3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel01 values
('D','melissa','C','7','pop','jimmy',
1000,80,1500,500,0.20,100.9999,
80,9000,999,5,.8,120,
4.1,0.4,4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel01 values ('E','monica','Q','sue','pat',
'christopher',
2000,90,1200,3000,0.30,100.99999,
2000,8000,-1000000,1,.9,80,
5.1,0.5,5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel01 values
('D','michelle','D','michael','rat',
'thomas',
-5000,90,2000,500,0.40,100.8,
90,8000,200,7,.93,140,
6.1,0.6,6);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel01 values ('C','maureen','E','jimmy','rum',
'marilyn',
3000,80,2000,500,0.50,100.7,
9000,1000,2000,8,.97,150,
7.1, 0.7,7);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel01 values ('C','marcia','Z','johnny','dum',
'thomas',
4000,40,2000,50,0.60,100.6,
8000,5000,0,9,.99,110,
8.1,0.8,8);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """update statistics for table btsel01 on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """insert into btsel02 values ('B');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel02 values ('C');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel02 values ('B');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel02 values ('Q');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel02 values ('B');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel02 values ('C');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel02 values ('Q');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel02 values ('Q');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """update statistics for table btsel02 on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """insert into btsel03 values ('A',5,'make',90,200);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel03 values ('7',6,'joe',80,1200);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel03 values ('8',6,'joe',80,1200);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel03 values ('5',1000,'5',100,1000);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel03 values ('michael',50,'dave',50,1500);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel03 values ('7',6,'john',80,2000);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel03 values ('B',6,'mark',80,3000);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel03 values ('michael',70,'joan',50,4000);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """update statistics for table btsel03 on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """insert into btsel04 values ('tom',1000,'7',200);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel04 values ('bob',999,'A',300);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel04 values ('sue',200,'sue',100);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel04 values ('bobby',200,'sue',100);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel04 values ('bill',2000,'B',500);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel04 values ('christopher',1000,'white',1000);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel04 values ('william',1000,'black',2000);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel04 values ('marilyn',2000,'green',3000);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """update statistics for table btsel04 on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """insert into btsel05 values ('joe','A','al','pablo','david',
'amy','amy','steve','steve','walt',
'mojo','joe','percy');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel05 values ('sue','A','in','peggy','diane',
'zora','cathy','mary','mary',
'rhoda','debra','sue','madge');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel05 values ('deb','D','jo','lowry','mary',
'sunny','debra','junk','junk',
'junk','junk','junk','junk');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel05 values ('can','D','by','lowry','steve',
'slope','debby','junk','junk',
'junk','junk','junk','junk');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel05 values ('box','C','to','howie','debra',
'snow','debbi','junk','junk',
'junk','junk','junk','junk');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel05 values ('red','B','go','lowry','sue',
'ski','cammy','junk','junk',
'junk','junk','junk','junk');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel05 values ('why','B','so','lowry','amy',
'squaw','tammy','junk','junk',
'junk','junk','junk','junk');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel05 values ('not','B','on','lowry','mary',
'mogul','pammy','junk','junk',
'junk','junk','junk','junk');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel06 values  ('joe','Z','in',100,200,100,200,
200,100,100,100,50,100,100,200,
100,200,200,100,100,100,50,100,
100,200,100,200,200,100,100,100,
100,200,100,200,200,100,100,100,
50,100);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel06 values
('sue','Q','on',200,400,100,100,400,
100,100,50,100,200,200,400,100, 100,
400,100,100,50,100,200,200,400, 100,
100,400,100,100,50,200,400,100, 100,
400,100,100,50,100,200);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel06 values
('pam','D','al',900,1000,900,1000,1000,
50,1000,1000,1000,1000,1000,1000,1000,
1000,1000,1000,1000,1000,1000,1000,1000,
1000,1000,1000,1000,1000,1000,1000,1000,
1000,1000,1000,1000,1000,1000,1000,1000,
1000);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel06 values
('sue','C','by',300,1000,500,1000,1000,
50,1000,1000,1000,1000,1000,1000,1000,
1000,1000,1000,1000,1000,1000,1000,1000,
1000,1000,1000,1000,1000,1000,1000,1000,
1000,1000,1000,1000,1000,1000,1000,1000,
1000);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel06 values
('joe','A','jo',100,1000,200,1000,1000,
50,1000,1000,1000,1000,1000,1000,1000,
1000,1000,1000,1000,1000,1000,1000,1000,
1000,1000,1000,1000,1000,1000,1000,1000,
1000,1000,1000,1000,1000,1000,1000,1000,
1000);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel06 values
('joe','B','to',300,1000,400,1000,1000,
50,1000,1000,1000,1000,1000,1000,1000,
1000,1000,1000,1000,1000,1000,1000,1000,
1000,1000,1000,1000,1000,1000,1000,1000,
1000,1000,1000,1000,1000,1000,1000,1000,
1000);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel06 values
('joe','C','go',100,1000,200,1000,1000,
50,1000,1000,1000,1000,1000,1000,1000,
1000,1000,1000,1000,1000,1000,1000,1000,
1000,1000,1000,1000,1000,1000,1000,1000,
1000,1000,1000,1000,1000,1000,1000,1000,
1000);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel06 values
('sue','D','so',200,1000,300,1000,1000,
50,1000,1000,1000,1000,1000,1000,1000,
1000,1000,1000,1000,1000,1000,1000,1000,
1000,1000,1000,1000,1000,1000,1000,1000,
1000,1000,1000,1000,1000,1000,1000,1000,
1000);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """update statistics for table btsel06 on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """insert into btsel07 values  ('jo','Z','jo');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel07 values  ('al','Q','al');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel07 values  ('P','P','P');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel07 values  ('B','A','ed');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel07 values  ('jo','C','ek');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel07 values  ('JO','D','em');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel07 values  ('al','E','bo');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel07 values  (' al','F','di');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel07 values  ('al ','F','al');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel07 values  (' al','F','al');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """update statistics for table btsel07 on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """insert into btsel08 values (3000,'george','D');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel08 values (100,'carltons','E');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel08 values (1000,'harveys','B');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel08 values (300,'Q','X');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel08 values (2000,'alexander','B');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel08 values (400,'joseph','X');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel08 values (200,'squaw','X');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel08 values (4000,'valley','D');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """update statistics for table btsel08 on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """insert into btsel09 values
('sue','mary','Z','MARY',3,10,20);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel09 values
('deb','bill','Y','BILL',4,10,30);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel09 values
('can','come','X','TED',7,77,77);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel09 values
('joe','over','W','maria',7,90,100);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel09 values
('box','here','R','debby',5,11,50);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel09 values
('red','long','S','tommy',5,15,70);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel09 values
('not','time','P','diane',7,20,40);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel09 values
('why','gone','R','billy',7,15,30);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel09 values
('\ts','t_go','j','to%go',0,0,0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel09 values
('\t_','junk','j','\%',0,0,0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel09 values
('_t%','junk','j','_%',0,0,0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel09 values
('%t_','junk','j','%_',0,0,0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """update statistics for table btsel09 on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """insert into btsel10 values
('tom','tom',3,'abadefih',100,100,-100);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel10 values
('bob','bobby',2,'ebediih',90,100,-1000);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel10 values
('sue','sue',1,'ebedafiih',110,80,100);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel10 values
('rod','for',400,'inside',25,60,0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel10 values
('don','who',50,'outside',10000,100,-100);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel10 values
('jon','does',1000,'offsides',50000, 500,100);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel10 values
('ron','they',2000,'onsides',10000,100, -100);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel10 values
('rob','bobby',2,'ebediih',90,100,-1000);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """update statistics for table btsel10 on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """insert into btsel11 values
('bob','bob', 100,'abadefih', 160,200,200);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel11 values
('dan','sue', 100,'ebediih', 100,100,60);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel11 values
('boe','tommy', 200,'ebedafiih', 200,50,50);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel11 values
('bar','where', 300,'gone', 200,9999,-100);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel11 values
('car','who', 400,'done', 160,500,500);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel11 values
('tar','what', 500,'none', 100,8888,0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel11 values
('jar','how', 600,'inside', 160,500,500);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel11 
values ('mar','why', 50,'house', 50,7777,0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """update statistics for table btsel11 on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """insert into btsel12 values ('tom',100);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel12 values ('bob',200);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel12 values ('run',300);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel12 values ('sun',400);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel12 values ('fun',500);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel12 values ('gun',600);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel12 values ('nun',700);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel12 values ('pun',800);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """update statistics for table btsel12 on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """insert into btsel13 values (100);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel13 values (200);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel13 values (250);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel13 values (350);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel13 values (450);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel13 values (550);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel13 values (650);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel13 values (750);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """update statistics for table btsel13 on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """insert into btsel14 values (100);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel14 values (200);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel14 values (125);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel14 values (150);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel14 values (175);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel14 values (225);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel14 values (275);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel14 values (325);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """update statistics for table btsel14 on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """insert into btsel15 values (1000,100);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel15 values (2000,200);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel15 values (1111,90);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel15 values (2222,80);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel15 values (3333,70);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel15 values (4444,60);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel15 values (5555,50);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel15 values (6666,40);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """update statistics for table btsel15 on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """insert into btsel16 values (1000,167);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel16 values (2000,168);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel16 values (8500,169);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel16 values (8501,170);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel16 values (8502,171);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel16 values (8503,172);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel16 values (8504,173);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel16 values (8505,174);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """update statistics for table btsel16 on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """insert into btsel17 values (1000,248);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel17 values (2000,249);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel17 values (7500,250);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel17 values (7501,251);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel17 values (7502,252);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel17 values (7503,253);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel17 values (7504,254);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel17 values (7505,255);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """update statistics for table btsel17 on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """insert into btsel18 values (-5000,1000,401);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel18 values (8000,2000,402);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel18 values (2001,6001,403);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel18 values (2002,6002,404);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel18 values (2003,6003,405);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel18 values (2004,6004,406);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel18 values (2005,6005,407);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel18 values (2006,6006,408);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """update statistics for table btsel18 on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """insert into btsel19 values (-5000,409);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel19 values (8000,410);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel19 values (2007,411);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel19 values (2008,412);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel19 values (2009,413);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel19 values (2010,414);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel19 values (2011,415);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel19 values (2012,416);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """update statistics for table btsel19 on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """insert into btsel20 values (-5000,417);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel20 values (8000,418);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel20 values (2013,419);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel20 values (2014,420);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel20 values (2015,421);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel20 values (2016,422);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel20 values (2017,423);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel20 values (2018,424);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """update statistics for table btsel20 on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """insert into btsel21 values (0.12,-5000,425);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel21 values (-0.25,8000,426);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel21 values (0.01,5000,427);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel21 values (0.02,5001,428);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel21 values (0.03,5002,429);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel21 values (0.04,5003,430);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel21 values (0.05,5004,431);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel21 values (0.06,5005,432);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """update statistics for table btsel21 on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """insert into btsel22 values (0.12,433);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel22 values (-0.25,434);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel22 values (0.07,435);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel22 values (0.08,436);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel22 values (0.09,437);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel22 values (0.10,438);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel22 values (0.11,439);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel22 values (0.92,440);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """update statistics for table btsel22 on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """insert into btsel23 values (0.12,441);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel23 values (-0.25,442);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel23 values (0.13,443);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel23 values (0.14,444);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel23 values (0.15,445);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel23 values (0.16,446);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel23 values (0.17,447);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel23 values (0.18,448);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """update statistics for table btsel23 on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """insert into btsel24 values (0.79,'tom');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel24 values (0.19,'bob');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel24 values (0.20,'toe');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel24 values (0.21,'woe');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel24 values (0.22,'pin');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel24 values (0.23,'sin');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel24 values (0.24,'win');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel24 values (0.25,'kin');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """update statistics for table btsel24 on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """insert into btsel25 values ('B', 'joe');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel25 values ('C', 'why');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel25 values ('D', 'not');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel25 values ('E', ' al');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel25 values ('Q', 'al ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel25 values ('B', 'bar');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel25 values ('C', 'car');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel25 values ('D', '   ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel25 values ('E', 'joe');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel25 values ('Q', 'sue');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel25 values (' ', 'sue');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """update statistics for table btsel25 on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """insert into btsel26 values
( 'A', 2, 2, 2, 2, .9, .2, .9, .2, 99999999999999999,
99999999999999999, 99999999.9, 1.1, 999999999.1, 9.99999999, 2,
.2, 2, .2, 0
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel26 values
( 'B', 999999999999999999, 1, 999999999999999999, 1,
.999999999999999999, .000000000000000001 , .999999999999999999,
.00000000000001, -99999999999999999, 99999999999999999,
-99999999.9, 1.899999999, 999999998.1, 9.99999999, 999999999,
.999999999, 999999999, .999999999, 0
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel26 values
( 'C', -999999999999999999, 1, -999999999999999999, 1,
.999999999999999999, .000000000000000002, .999999999999999999,
.00000000000002, 0, 99999999, 99999999.9, 9.999999999,
-999999999.9, 9.99999999, 0, 0, 0, 0, .9
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel26 values
( 'D', 100000000000000000, 899999999999999999, 100000000000000000,
899999999999999999, .999999999999999999, .1, .999999999999999999,
.000000000000000002, 0, 100, 9999999.9, 4.4, 0, 8, 0, 0, 0, 0, .1
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel26 values
( 'E', 999999999999999999, 3, 999999999999999999,
100000000000000000, .000000000000000001, .9, .999999999999999999,
0, 10, 99999999999999999, 0, 3, 0, 0, 0, 0, 0, 0, 0
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel26 values
( 'F', 999999999999999999, 2, 999999999999999999,
-999999999999999999, .1, 0, .999999999999999999, 0,
99999999999999999, 0, 0, 2.5, 0, 0, 0, 0, 0, 0, 0
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel26 values
( 'G', 92233720368547758, 999999999999999999, 999999999999999999, 0,
.08, .09, .999999999999999999, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
0
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel26 values
( 'H', 999999999999999999, 999999999999999999, 999999999999999999,
0, 0, 0, .999999999999999999, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel26 values
( 'I', 999999999999999999, 0, 999999999999999999, 0, 0, 0,
.999999999999999999, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel26 values
( 'J', 999999999999999999, 0, 999999999999999999,
0, 0, 0, .999999999999999999, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel26 values
( 'K', 999999999999999999, 0, 999999999999999999,
0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel26 values
( 'L', 999999999999999999, 0, 999999999999999999,
0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel26 values
( 'M', 999999999999999999, 0, 999999999999999999,
0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel26 values
( 'N', 999999999999999999, 0, 0,
0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel26 values
( 'O', -999999999999999999, 0, 0,
0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel26 values
('P', -999999999999999999, 0, 0,
0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """update statistics for table btsel26 on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """insert into btsel27 values
('A', 1.1001, 1.1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel27 values
('B', 1.0016, .1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into btsel27 values
('C', .0001, 9.9);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """update statistics for table btsel27 on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    _testmgr.testcase_end(desc)

def test010(desc="""a09"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """SELECT count(*) FROM orders ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '12')

    stmt = """SELECT count(*) FROM customer ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '12')
    
    stmt = """SELECT count(*) FROM fromsup ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '39')
    
    stmt = """SELECT count(*) FROM odetail ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '128')
    
    stmt = """SELECT count(*) FROM parts ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '28')
    
    stmt = """SELECT count(*) FROM supplier ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '7')
    
    stmt = """SELECT count(*) FROM region ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '7')
    
    stmt = """SELECT count(*) FROM branch ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '15')
    
    stmt = """SELECT count(*) FROM employee ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '56')
    
    _testmgr.testcase_end(desc)

def test011(desc="""a10"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """SELECT count(*) FROM empone;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '56')
    
    stmt = """SELECT count(*) FROM emppub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '56')
    
    stmt = """SELECT count(*) FROM expfroms;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '10')
    
    _testmgr.testcase_end(desc)

def test012(desc="""a11"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """SELECT count(*) FROM partsfor;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '124')
    
    stmt = """SELECT count(*) FROM salecust;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '12')
    
    stmt = """SELECT count(*) FROM salecub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '12')
    
    stmt = """SELECT count(*) FROM fsdetail;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '6')
    
    _testmgr.testcase_end(desc)

def test013(desc="""a12"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """SELECT count(*) FROM orders;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '12')
    
    stmt = """SELECT count(*) FROM customer;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '12')
    
    stmt = """SELECT count(*) FROM fromsup;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '39')
    
    stmt = """SELECT count(*) FROM odetail;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '128')
    
    stmt = """SELECT count(*) FROM parts;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '28')
    
    stmt = """SELECT count(*) FROM supplier;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '7')
    
    stmt = """SELECT count(*) FROM region;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '7')
    
    stmt = """SELECT count(*) FROM branch;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '15')
    
    stmt = """SELECT count(*) FROM employee;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '56')
    
    stmt = """SELECT count(*) FROM empone;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '56')
    
    stmt = """SELECT count(*) FROM emppub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '56')
    
    stmt = """SELECT count(*) FROM expfroms;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '10')
    
    stmt = """SELECT count(*) FROM partsfor;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '124')
    
    stmt = """SELECT count(*) FROM salecust;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '12')
    
    stmt = """SELECT count(*) FROM salecub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '12')
    
    stmt = """SELECT count(*) FROM fsdetail;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '6')
    
    _testmgr.testcase_end(desc)

def test014(desc="""a13"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """SELECT count(*) FROM btempkey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '0')
    
    stmt = """SELECT count(*) FROM btemprel;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '0')
    
    stmt = """SELECT count(*) FROM btempent;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '0')
    
    stmt = """SELECT count(*) FROM btsel01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '8')
    
    stmt = """SELECT count(*) FROM btsel02;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '8')
    
    stmt = """SELECT count(*) FROM btsel03;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '8')
    
    stmt = """SELECT count(*) FROM btsel04;""" 
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '8')
    
    stmt = """SELECT count(*) FROM btsel05;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '8')
    
    stmt = """SELECT count(*) FROM btsel06;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '8')
    
    stmt = """SELECT count(*) FROM btsel07;""" 
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '10')
    
    stmt = """SELECT count(*) FROM btsel08;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '8')
    
    stmt = """SELECT count(*) FROM btsel09;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '12')
    
    stmt = """SELECT count(*) FROM btsel10;""" 
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '8')
    
    stmt = """SELECT count(*) FROM btsel11;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '8')
    
    stmt = """SELECT count(*) FROM btsel12;""" 
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '8')
    
    stmt = """SELECT count(*) FROM btsel13;""" 
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '8')
    
    stmt = """SELECT count(*) FROM btsel14;""" 
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '8')
    
    stmt = """SELECT count(*) FROM btsel15;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '8')
    
    stmt = """SELECT count(*) FROM btsel16;""" 
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '8')
    
    stmt = """SELECT count(*) FROM btsel17;""" 
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '8')
    
    stmt = """SELECT count(*) FROM btsel18;""" 
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '8')
    
    stmt = """SELECT count(*) FROM btsel19;""" 
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '8')
    
    stmt = """SELECT count(*) FROM btsel20;""" 
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '8')
    
    stmt = """SELECT count(*) FROM btsel21;""" 
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '8')
    
    stmt = """SELECT count(*) FROM btsel22;""" 
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '8')
    
    stmt = """SELECT count(*) FROM btsel23;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '8')
    
    stmt = """SELECT count(*) FROM btsel24;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '8')
    
    stmt = """SELECT count(*) FROM btsel25;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '11')
    
    stmt = """SELECT count(*) FROM btsel26;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '16')
    
    stmt = """SELECT count(*) FROM btsel27;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '3')
    
    stmt = """SELECT count(*) FROM pvsel01 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '8')
    
    stmt = """SELECT count(*) FROM pvsel02 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '8')
    
    stmt = """SELECT count(*) FROM pvsel03 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '4')
    
    stmt = """SELECT count(*) FROM pvsel04;""" 
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '6')
    
    stmt = """SELECT count(*) FROM svsel01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '8')
    
    stmt = """SELECT count(*) FROM svsel02;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '8')
    
    stmt = """SELECT count(*) FROM svsel03;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '4')
    
    stmt = """SELECT count(*) FROM svsel04;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '4')
    
    stmt = """SELECT count(*) FROM svsel05;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '88')
    
    stmt = """SELECT count(*) FROM svsel06;""" 
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '88')
    
    stmt = """SELECT count(*) FROM svsel07;""" 
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '1')
    
    stmt = """SELECT count(*) FROM svsel08;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '1')
    
    stmt = """SELECT count(*) FROM svsel09;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '1')
    
    stmt = """SELECT count(*) FROM svsel10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '1')
    
    stmt = """SELECT count(*) FROM svsel11;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '10')
    
    stmt = """SELECT count(*) FROM svsel12;""" 
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '1')
    
    stmt = """SELECT count(*) FROM svsel13;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '4')
    
    stmt = """SELECT count(*) FROM svsel14;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '3')
    
    stmt = """SELECT count(*) FROM svsel15;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '6')
    
    _testmgr.testcase_end(desc)

def test015(desc="""a14"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """select count(*) from btre201;""" 
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '8')
    
    stmt = """select count(*) from btre202;""" 
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '2')
    
    stmt = """select count(*) from btre204;""" 
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '1')
    
    stmt = """select count(*) from btre205;""" 
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '9')
    
    stmt = """select count(*) from btre206;""" 
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '8')
    
    stmt = """select count(*) from btre207;""" 
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '7')
    
    stmt = """select count(*) from btre208;""" 
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '1')
    
    stmt = """select count(*) from pvre201;""" 
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '8')
    
    stmt = """select count(*) from pvre201b;""" 
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '1')
    
    stmt = """select count(*) from pvre201c;""" 
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '7')
    
    stmt = """select count(*) from pvre204a;""" 
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '1')
    
    stmt = """select count(*) from svre201;""" 
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '16')
    
    stmt = """select count(*) from svre201b;""" 
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '1')
    
    stmt = """select count(*) from svre201c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '1')
    
    stmt = """select count(*) from svre201d;""" 
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '11')
    
    stmt = """select count(*) from svre201e;""" 
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '8')
    
    _testmgr.testcase_end(desc)

def test016(desc="""a15 Create tables for test units arkt11##."""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
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
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
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
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
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
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
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
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
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
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
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
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
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
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """create view VUA1P001 as select * from BTA1P001 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
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
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    #
    # Insert before making views (was previously OBEY file OBEYIN02).
    #
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
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
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
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
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
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
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
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
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
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
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
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
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
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """create view VNA1P002 as
select cast(char17_100 as varchar(20)) as char17_100
, udec17_100
from BTA1P002 
group by char17_100 , udec17_100
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """Create Table            BTA1P003 
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
char3_1000       PIC X(240)        ,
ubin3_uniq       Numeric(5,0) unsigned ,    

sbin4_2          Numeric(1,1) signed,
ubin4_4          Numeric(1,1) unsigned ,
varchar4_1000    VarChar(16)        ,
sdec4_10         -- Decimal
Numeric(1,1) signed                 ,
udec4_2          -- Decimal
Numeric(1,1) unsigned               ,    

sbin5_4          Numeric(4,0) signed,
ubin5_20         Numeric(9,0) unsigned ,
udec5_20         -- Decimal
Numeric(4,0) unsigned               ,
varchar5_4       VarChar(8)         ,
sdec5_100        -- Decimal
Numeric(18,0) signed                ,    

varchar6_20      VarChar(32)        ,    

sbin7_2          SMALLINT signed    ,
sdec7_10         -- Decimal
Numeric(4,1) signed                 ,
char7_uniq       Char(100)          ,
udec7_20         -- Decimal
Numeric(4,1) unsigned               ,
ubin7_100        SMALLINT unsigned  ,    

sbin8_1000       Numeric(18,0) signed  ,
varchar8_uniq    VarChar(32)        ,
ubin8_2          Numeric(4,1) unsigned ,    

char9_uniq       Char(8)            ,
udec9_10         -- Decimal
Numeric(5,0) unsigned               ,
sdec9_20         -- Decimal
Numeric(5,0) signed                 ,    

varchar10_20      VarChar(32)       ,    

sdec11_20        -- Decimal
Numeric(5,5) signed                 ,
varchar11_2      VarChar(32)        not null ,
char11_4         Char(2)            ,    

sbin12_1000      Numeric(9,0) signed,
varchar12_4      VarChar(32)        ,
ubin12_10        Numeric(9,0) unsigned ,    

char13_100       Char(5)            ,
sdec13_uniq      -- Decimal
Numeric(9,0) signed                 ,
udec13_500       -- Decimal
Numeric(9,0) unsigned               ,    

sbin14_100       Numeric(2,0) signed   ,
ubin14_2         Numeric(2,0) unsigned ,
sdec14_20        -- Decimal
Numeric(2,0) signed                 ,
udec14_10        -- Decimal
Numeric(2,0) unsigned               ,
varchar14_2000   VarChar(64)        ,    

sbin15_2         INTEGER signed     ,
udec15_4         -- Decimal
Numeric(9,2) unsigned               ,
varchar15_uniq   VarChar(8)         not null ,
ubin15_uniq      INTEGER unsigned   ,
sdec15_10        -- Decimal
Numeric(9,2) signed                 ,    

sbin16_20        Numeric(9,2) signed,
ubin16_1000      Numeric(9,2) unsigned ,
varchar16_100    VarChar(128)       ,    

sbin17_uniq      Numeric(10,0) signed  ,
sdec17_20        -- Decimal
Numeric(2,0) signed                 ,
char17_100       Char(100)          ,
varchar17_20     VarChar(240)       ,    

sbin18_uniq      Numeric(18,0) signed  ,
varchar18_uniq   VarChar(60)        ,    

sbin19_4         LARGEINT signed    ,
char19_2         Char(8)            ,
ubin19_10        SMALLINT unsigned  ,
udec19_100       -- Decimal
Numeric(4,1) signed                 ,
sdec19_1000      -- Decimal
Numeric(4,1) unsigned               ,    

varchar20_1000   VarChar(100)    

-- The following column sequence gives more than one
-- identical value in the first column of the primary key.
, primary  key ( varchar11_2 DESC
, varchar2_10     ASC
, varchar15_uniq  ASC
)
)
-- catalog <global_dbvolume_part1>
-- organization K
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    #
    # Insert before making views (was previously OBEY file OBEYIN02).
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
1, .7,
'CCAAKAABAAAAAAAA', .7, 7,
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
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
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
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
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
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
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
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    #
    # Create View of a few rows, all columns; should be updateable.
    #
    stmt = """create view  VUA1P003 as
select *
from BTA1P003 
where ubin15_uniq > 1000
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
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
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    # Insert before making views (was previously OBEY file OBEYIN04).
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
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
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
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
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
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
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
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
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
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
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
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
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
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
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
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
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
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
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
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
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
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
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
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
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
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
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
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """Create Table BTA1P005 
(
char0_n10           Char(2),
-- default 'AD'
-- heading 'char0_n10 with default AD' ,
sbin0_uniq          Smallint not null,
sdec0_n500          Numeric(18,0) ,    

ubin1_n2            Numeric(4,0) unsigned ,
udec1_100           Numeric(2,0) unsigned not null,    

char2_2             Char(2)               not null,
sbin2_nuniq         Largeint              ,
sdec2_500           Numeric(9,0) signed   not null,    

udec3_n100          Numeric(9,0) unsigned ,
ubin3_n2000         Numeric(4,0) unsigned ,
char3_4             Char(8)               not null ,    

sdec4_n20           Numeric(4,0)          ,
sbin4_n1000         Smallint              ,
char4_n10           Char(8)               ,    

char5_n20           Char(8)               ,
sdec5_10            Numeric(9,0) signed   not null,
ubin5_n500          Numeric(9,0) unsigned ,    

sbin6_nuniq         Largeint              ,
sdec6_4             Numeric(4,0) signed   not null,
char6_n100          Char(8)               ,    

sbin7_n20           Smallint              ,
char7_500           Char(8)               not null,
udec7_n10           Numeric(4,0) unsigned ,    

ubin8_10            Numeric(4,0) unsigned not null,
char8_n1000         Char(8)               ,
sdec8_4             Numeric(9,0) unsigned not null,    

sdec9_uniq          Numeric(18,0) signed  not null,
char9_100           Char(2)               not null,
ubin9_n4            Numeric(9,0) unsigned ,    

ubin10_n2           Numeric(4,0) unsigned ,
char10_nuniq        Char(8)               ,
udec10_uniq         Numeric(9,0) unsigned not null,    

udec11_2000         Numeric(9,0) unsigned not null,
sbin11_100          Integer               not null,
char11_uniq         Char(8)               not null ,    

ubin12_2            Numeric(4,0) unsigned not null ,
sdec12_n1000        Numeric(18,0) signed  ,
char12_n2000        Char(8) ,    

udec13_500          Numeric(9,0) unsigned not null,
char13_1000         Char(8)               not null ,    

sbin14_1000         Integer               not null,
udec14_100          Numeric(4,0) unsigned not null,
char14_n500         Char(8)               ,    

sbinneg15_nuniq     Largeint              ,
sdecneg15_100       Numeric(9,0) signed   not null,
char15_100          Char(8)               not null ,    

ubin16_n10          Numeric(4,0) unsigned ,
sdec16_uniq         Numeric(18,0) signed  not null,
char16_n20          Char(5) ,   -- len = 2,4    

sbin17_uniq         Largeint              not null,
sdec17_nuniq        Numeric(18,0) ,
char17_2            Char(8)               not null    

, primary key ( sbin0_uniq )
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    #
    # Insert before making views.
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
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
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
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
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
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
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
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
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
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
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
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
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
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
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
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
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
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
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
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
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
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
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
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """create view  VNA1P006 as
select * from
(select sbin0_4 , sdec5_10 , sdec6_4 , varchar0_uniq
from BTA1P006 t1 ) t2
natural    join
(select sbin0_4 , sdec5_10 , sdec6_4 , varchar0_uniq
from BTA1P006 t3 ) t4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """Create Table BTA1P007 
(
varchar0_nuniq      VarChar(11)            ,
sbin0_uniq          Smallint               not null,
sdec0_n500          Numeric(18,0)          ,    

ubin1_n2            Numeric(4,0) unsigned  ,
udec1_100           Numeric(2,0) unsigned  not null,    

char2_2             Char(2)                not null,
sbin2_nuniq         Largeint               ,
sdec2_500           Numeric(9,0) signed    not null,    

udec3_n100          Numeric(9,0) unsigned  ,
ubin3_n2000         Numeric(4,0) unsigned  ,
char3_4             Char(9)                not null,    

sdec4_n20           Numeric(4,0)           ,
sbin4_n1000         Smallint               ,
char4_n10           Char(8)                ,    

char5_n20           Char(9)                ,
sdec5_10            Numeric(9,0) signed    not null,
ubin5_n500          Numeric(9,0) unsigned  ,    

sbin6_nuniq         Largeint               ,
sdec6_4             Numeric(4,0) signed    not null,
char6_n100          Char(8)                ,    

sbin7_n20           Smallint               ,
char7_500           Char(9)                not null,
udec7_n10           Numeric(4,0) unsigned  ,    

ubin8_10            Numeric(4,0) unsigned  not null,
char8_n1000         Char(8)                ,
sdec8_4             Numeric(9,0) unsigned  not null,    

sdec9_uniq          Numeric(18,0) signed   not null,
char9_100           Char(3)                not null,
ubin9_n4            Numeric(9,0) unsigned  ,    

ubin10_n2           Numeric(4,0) unsigned  ,
char10_nuniq        Char(8)                ,
udec10_uniq         Numeric(9,0) unsigned  not null,    

udec11_2000         Numeric(9,0) unsigned  not null,
sbin11_100          Integer                not null,
char11_uniq         Char(9)                not null,    

ubin12_2            Numeric(4,0) unsigned  not null,
sdec12_n1000        Numeric(18,0) signed   ,
char12_n2000        Char(8)                ,    

sbin13_n100         Numeric (10,0) signed  ,
char13_1000         Char(9)                not null,    

sbin14_1000         Integer                not null,
udec14_100          Numeric(4,0) unsigned  not null,
char14_n500         Char(8)                ,    

sbinneg15_nuniq     Largeint               ,
sdecneg15_100       Numeric(9,0) signed    not null,
char15_100          Char(9)                not null,
ubin16_n10          Numeric(4,0) unsigned  ,
sdec16_uniq         Numeric(18,0) signed   not null,
char16_n20          Char(5)                ,    

sbin17_uniq         Largeint               not null,
sdec17_nuniq        Numeric(18,0)          ,
char17_2            Char(8)                not null    

) no partition
--  organization E
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """Insert Into BTA1P007 
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
'GGAAKAAB',    .3,  -- Change pic S9(9)V9 to Numeric(10,1)
'DDAADAAA',   505,    5,
'BBAABAAA', -3812,  -12,
'AMAAAAAA',     1, 2701,
'BBAA ',   149840,    3,
'BAAAAAAA'
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
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
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
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
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
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
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
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
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
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
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
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
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
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
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
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
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
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
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
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
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
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
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
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
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
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
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """create view  VNA1P008 
as  select * from BTA1P008 where sdec16_uniq > 3000
union -- CORRESPONDING
select * from BTA1P008 where sdec16_uniq < 2500
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    stmt = """create table BTA1P009(
rownum   integer not null
, ch1n     char -- length defaults to 1.
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
-- Column name 'sin' changed to sint because 'sin'
-- was made into a reserved word in July 1998 for FCS.
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
, primary key (vc49n, vc50n, rownum)
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    # Insert 14 rows
    
    stmt = """insert into BTA1P009 values (
1,
'S',  'This is a 50 character field', 'This is a 49 character field',
'V',  'This is a 50 character varchar field aaaaaaaaaaaaa',
'This is a 49 character varchar field bbbbbbbbbbbb',
-1, 123456789012345678, -0.123456789012345678, 123456789, 0.123456789,
-999.45678, 999.45678, -32768, 32766,   4294967295, -2147483648, -9.2233,
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
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into BTA1P009 values (
2,
'S',  'This is a 50 character field', 'This is a 49 character field',
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
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into BTA1P009 values (
3,
'S',  'This is a 50 character field', 'This is a 49 character field',
'V',  'This is a 50 character varchar field aaaaaaaaaaaaa',
'This is a 49 character varchar field bbbbbbbbbbbb',
-1, 123456789012345678, -0.123456789012345678, 123456789, 0.123456789,
-999.45678, 999.45678, -32768, 32767,   4294967295, -2147483648, -9.2233,
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
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into BTA1P009 values (
4,
'A',  'This is a 50 character field', 'This is a 49 character field',
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
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into BTA1P009 values (
5,
'A',  'This is a 50 character field', 'This is a 49 character field',
'V',  'This is a 50 character varchar field aaaaaaaaaaaaa',
'This is a 49 character varchar field cccccccccccc',
-1, 123456789012345678, -0.123456789012345678, 123456789, 0.123456789,
-999.45678, 999.45678, -32768, 30000,   4294967295, -2147483648, -9.2233,
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
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into BTA1P009 values (
6,
'A',  'This is a 50 character field',
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
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into BTA1P009 values (
7,
'A',  'This is a 50 character field',
'This is a 49 character field',
'V',  'This is a 50 character varchar field aaaaaaaaaaaaa',
'This is a 49 character varchar field cccccccccccc',
-1, 123456789012345678, -0.123456789012345678, 123456789, 0.123456789,
-999.45678, 999.45678, -32768, 30000,   4294967295, -2147483648, -9.2233,
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
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into BTA1P009 values (
8,
'A',  'This is a 50 character field',
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
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into BTA1P009 values (
9,
'A',  'This is a 50 character field',
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
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into BTA1P009 values (
10,
'A',  'This is a 50 character field', 'This is a 49 character field',
'V',  'This is a 50 character varchar field aaaaaaaaaaaaa',
'This is a 49 character varchar field cccccccccccc',
-1, 123456789012345678, -0.123456789012345678, 123456789, 0.123456789,
-999.45678, 999.45678, -32767, 32767,   4294967295, -2147483648, -9.2233,
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
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into BTA1P009 values (
11,
'A',  'This is a 50 character field', 'This is a 49 character field',
'V',  'This is a 50 character varchar field aaaaaaaaaaaaa',
'This is a 49 character varchar field bbbbbbbbbbbb',
-1, 123456789012345678, -0.123456789012345678, 123456789, 0.123456789,
-999.45678, 999.45678, -32767, 32767,   4294967295, -2147483648, -9.2233,
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
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into BTA1P009 values (
12,
'S',  'This is a 50 character field', 'This is a 49 character field',
'V',  'This is a 50 character varchar field aaaaaaaaaaaaa',
'This is a 49 character varchar field bbbbbbbbbbbb',
-1, 123456789012345678, -0.123456789012345678, 123456789, 0.123456789,
-999.45678, 999.45678, -32767, 32767,   4294967295, -2147483648, -9.2233,
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
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into BTA1P009 values (
13,
'A',  'This is a 50 character field', 'This is a 49 character field',
'V',  'This is a 50 character varchar field aaaaaaaaaaaaa',
'This is a 49 character varchar field bbbbbbbbbbbb',
-1, 123456789012345678, -0.123456789012345678, 123456789, 0.123456789,
-999.45678, 999.45678, -32767, 32767,   4294967295, -2147483648, -9.2233,
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
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """insert into BTA1P009 values (
14,
'A',  'This is a 50 character field', 'This is a 49 character field',
'V',  'This is a 50 character varchar field aaaaaaaaaaaaa',
'This is a 49 character varchar field bbbbbbbbbbbb',
-1, 123456789012345678, -0.123456789012345678, 123456789, 0.123456789,
-999.45678, 999.45678, -32767, 32767,   4294967295, -2147483648, -9.2233,
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
    _dci.expect_any_substr(output, '*--- 1 row(s) inserted.*')
    
    stmt = """create view  VNA1P009 (csimple, csearched) as select
-- Simple CASE:
CASE rownum WHEN 1 THEN 'Value A'
WHEN 2 THEN 'Value B'
WHEN 3 THEN 'Value C'
ELSE 'Value D -- Rowcount > 3'
END
-- Searched CASE:
,   CASE when rownum > 10 then 'rownum over 10'
when sint  = -32768 then 'sint is the lowest'
else 'the great unknown'
END
from BTA1P009 
where rownum < CASE
when rownum between 7 and 12   then 2222
when rownum between 1 and 2   then rownum+1
else rownum
end
--  catalog <global_dbvolume_part1>
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '*--- SQL operation complete.*')
    
    #             End of test case ARKT0000
    _testmgr.testcase_end(desc)

def test017(desc='grant privileges'):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    tablelist = ['btre201', 'btre202', 'btre203', 'btre204', 'btre205', 'btre206', 'btre207', 'btre208', 'BTRE211', 'BTRE213', 'TINY', 'btuns01', 'orders', 'customer', 'fromsup', 'odetail', 'parts', 'supplier', 'region', 'branch', 'employee', 'btempkey', 'btemprel', 'btempent', 'btsel01', 'btsel02', 'btsel03', 'btsel04', 'btsel05', 'btsel06', 'btsel07', 'btsel08', 'btsel09', 'btsel10', 'btsel11', 'btsel12', 'btsel13', 'btsel14', 'btsel15', 'btsel16', 'btsel17', 'btsel18', 'btsel19', 'btsel20', 'btsel21', 'btsel22', 'btsel23', 'btsel24', 'btsel25', 'btsel26', 'btsel27', 'BTA1P001', 'BTA1P002', 'BTA1P003', 'BTA1P004', 'BTA1P005', 'BTA1P006', 'BTA1P007', 'BTA1P008', 'BTA1P009']

    for table in tablelist:
        # set privilege
        stmt = 'revoke all on table ' + table + ' from PUBLIC;'
        output = _dci.cmdexec(stmt)
        _dci.expect_complete_msg(output)

        stmt = 'grant select on table ' + table + ' to PUBLIC;'
        output = _dci.cmdexec(stmt)
        _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)

