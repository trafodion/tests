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
    #  Test case name:         A01
    #  Description:            HEADING attribute -- Positive test
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:        (provide a high-level description)
    #
    #  Notes:
    #  This test case incorporates features detailed in the "Title"
    #  by Ima Programmer (Version 1.1, <date>).
    #
    # =================== End Test Case Header  ===================
    #  |                                                     |
    #  |  Test Case Name:  A1                                |
    
    #   ---------------------------
    #   Create table with 1 col, heading 'string':
    #   ---------------------------
    stmt = """CREATE TABLE a1table1 
( col_string   PIC X        HEADING 'some heading string'
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #    Select from empty table then populate it:
    
    stmt = """SELECT * FROM a1table1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """INSERT INTO a1table1 VALUES ( 'A' ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """UPDATE STATISTICS FOR TABLE a1table1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """SELECT * FROM a1table1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s0')
    
    #   ----------------------------
    #   Create table with several columns, with heading of 0, 1, 78,79
    #   chars:
    #   ----------------------------
    stmt = """CREATE TABLE a1table2 
( col_numeric  SMALLINT     HEADING '1' NOT NULL
, col_varchar VARCHAR (3) DEFAULT 'aaa' HEADING ''
, col_date     DATE         DEFAULT NULL   HEADING
'123456789 123456789 123456789 123456789 123456789 123456789'
'123456789 12345678'
, col_float    FLOAT (5)    DEFAULT 9      HEADING
'123456789 123456789 123456789 123456789 123456789 123456789'
'123456789 123456789'
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """INSERT INTO a1table2 VALUES ( 2 ,'3' , DATE '1988-08-29' , 5.123 );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """UPDATE STATISTICS FOR TABLE a1table2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """SELECT * FROM a1table2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s1')
    
    #    Alter that table to add columns, with heading of 77, 80 chars.
    #     ALTER TABLE a1table2 ADD COLUMN
    #         col_numeric_77 SMALLINT DEFAULT 77 HEADING
    #       '123456789 123456789 123456789 123456789 123456789 123456789'
    #      &'123456789 1234567'
    #         catalog
    
    #    ----------------------------
    #    Alter that table to add column with NO HEADING:
    #    ----------------------------
    
    stmt = """SELECT * FROM a1table2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s2')
    
    #   Create table with one linefeed in heading:
    
    stmt = """CREATE TABLE a1table3 
( col_numeric SMALLINT DEFAULT 99 NOT NULL HEADING '/'
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """INSERT INTO a1table3 VALUES ( 3 ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """UPDATE STATISTICS FOR TABLE a1table3 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """SELECT * FROM a1table3 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s3')
    
    #   Create table with 2 linefeeds in heading:
    
    stmt = """CREATE TABLE a1table4 
( col_numeric  SMALLINT DEFAULT 1 NOT NULL
HEADING 'a/b/c'
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """INSERT INTO a1table4 VALUES ( 4 ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """UPDATE STATISTICS FOR TABLE a1table4 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """SELECT * FROM a1table4 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s4')
    
    #   Create table with 132 chars in heading:
    stmt = """CREATE TABLE a1table5 
( col_numeric  SMALLINT     HEADING
'123456789 123456789 123456789 123456789 123456789 123456789 '
'123456789 123456789 123456789 123456789 123456789 123456789 '
'12345678'
--   '123456789 12'
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """INSERT INTO a1table5 VALUES ( 5 ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """UPDATE STATISTICS FOR TABLE a1table5 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """SELECT * FROM a1table5 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s5')
    
    #   ----------------------------
    #   Create table with 132 linefeeds in heading:
    #   ----------------------------
    stmt = """CREATE TABLE a1table6 
( col_numeric  SMALLINT     HEADING
'////////////////////////////////////////////////////////////'
'////////////////////////////////////////////////////////////'
'////////'
--  '////////////'
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """INSERT INTO a1table6 VALUES ( 6 ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """UPDATE STATISTICS FOR TABLE a1table6 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """SELECT * FROM a1table6 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s6')
    
    #   ----------------------------
    #   Create table with multiple columns, with and without headings,
    #   then put view on it, to inherit headings; then change
    #   table headings; they should not change on view:
    #   ----------------------------
    stmt = """CREATE TABLE a1table7 
( col_numeric  SMALLINT     DEFAULT 1   HEADING '1'
, col_varchar  VARCHAR (3)  DEFAULT 'a' HEADING ''
, col_date     DATE         DEFAULT DATE '1996-08-22' NO HEADING
, col_float    FLOAT (5)    DEFAULT 1.11111 HEADING
'1/3/5/7/9/1/3/5/7/9/1/3/5/7/9/1/3/5/7/9/1/3/5/7/9/1/3/5/7/9/'
, col_key      CHAR NOT NULL  HEADING 'key'
, PRIMARY KEY (col_key)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """INSERT INTO a1table7 
VALUES ( 7 ,'7' , DATE '1988-08-29' , 5.123 , 'G' ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO a1table7 
VALUES ( 7 , NULL , NULL , NULL , 'H' ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    #     CREATE VIEW a1view7p
    #        AS SELECT *
    #        FROM a1table7 FOR PROTECTION
    #        WITH HEADINGS
    #        ;
    
    stmt = """CREATE VIEW a1view7p 
( col_numeric  HEADING '1'
, col_varchar  HEADING ''
, col_date     NO HEADING
, col_float    HEADING
'1/3/5/7/9/1/3/5/7/9/1/3/5/7/9/1/3/5/7/9/1/3/5/7/9/1/3/5/7/9/'
, col_key     HEADING 'key'
)
AS SELECT *
FROM a1table7;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #       CREATE VIEW a1view7p
    #          AS SELECT *
    #          FROM a1table7
    #          WITH HEADINGS
    #       ;
    
    stmt = """CREATE VIEW a1view7s 
( col_numeric HEADING '1'
, col_varchar HEADING ''
, col_date    NO HEADING
, col_float   HEADING
'1/3/5/7/9/1/3/5/7/9/1/3/5/7/9/1/3/5/7/9/1/3/5/7/9/1/3/5/7/9/'
, col_key     HEADING 'key'
)
AS SELECT col_numeric, col_varchar, col_date, col_float, col_key
FROM a1table7;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """UPDATE STATISTICS FOR TABLE a1table7 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """SELECT * FROM a1table7 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s7')
    
    stmt = """SELECT * FROM a1view7p ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s8')
    
    stmt = """SELECT * FROM a1view7s ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s9')
    
    #      ALTER TABLE a1table7 COLUMN col_numeric  NO HEADING ;
    #      ALTER TABLE a1table7 COLUMN col_numeric  HEADING 'longer';
    #      ALTER TABLE a1table7 COLUMN col_date     HEADING 'a';
    #      ALTER TABLE a1table7 COLUMN col_float    HEADING 'b';
    #      ALTER TABLE a1table7 COLUMN col_key      HEADING 'c';
    #      SELECT * FROM a1table7 ;
    #      SELECT * FROM a1view7p ;
    #      SELECT * FROM a1view7s ;
    #
    #   ---------------------------
    #   Create another view containing expressions and functions:
    #   ---------------------------
    #      CREATE VIEW a1view7e (col_agg, col_varchar, col_max_key)
    #         AS SELECT (col_numeric + col_float)
    #                   , col_varchar
    #                   , MAX (col_key)
    #         FROM a1table7
    #         GROUP BY col_numeric
    #         WITH HEADINGS
    #      ;
    
    stmt = """CREATE VIEW a1view7e 
(col_agg HEADING '1 + 1/3/5/7/9/1/3/5/7/9/1/3/5/7/9/1/3/5/7/9/1/3/5/7/9/1/3/5/7/9/'
, col_varchar HEADING ''
, col_max_key HEADING 'key')
AS SELECT (col_numeric + col_float)
, col_varchar
, MAX (col_key)
FROM a1table7 
GROUP BY col_numeric,
col_float,
col_varchar;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #        WITH HEADINGS
    #       catalog
    
    # 04/13/09 added order by
    stmt = """SELECT * FROM a1view7e group by col_varchar, col_max_key, col_agg ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s10')
    
    stmt = """SELECT * FROM a1view7e group by col_varchar, col_max_key, col_agg ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s11')
    
    stmt = """SELECT * FROM a1view7e group by col_varchar, col_agg, col_max_key;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s12')
    
    stmt = """DROP   VIEW  a1view7e;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #      CREATE VIEW a1view7e (col_agg, col_varchar, col_max_key)
    #         AS SELECT (col_numeric + col_float)
    #                   , col_varchar
    #                   , MAX (col_key)
    #         FROM a1table7
    #         GROUP BY col_numeric, col_float, col_varchar
    #         WITH HEADINGS
    #      ;
    
    stmt = """CREATE VIEW a1view7e 
(col_agg HEADING '1 + 1/3/5/7/9/1/3/5/7/9/1/3/5/7/9/1/3/5/7/9/1/3/5/7/9/1/3/5/7/9/'
, col_varchar HEADING ''
, col_max_key HEADING 'key')
AS SELECT (col_numeric + col_float)
, col_varchar
, MAX (col_key)
FROM a1table7 
GROUP BY col_numeric, col_float, col_varchar;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #          WITH HEADINGS
    #         catalog
    
    stmt = """SELECT * FROM a1view7e group by col_varchar, col_max_key, col_agg ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s13')
    
    stmt = """SELECT * FROM a1view7e group by col_varchar, col_agg, col_max_key;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s14')
    
    #   ---------------------------
    #   Create a table with & without headings LIKE an existing table:
    #   ---------------------------
    #      CREATE TABLE a1table8 LIKE \columba.$talon.yugal2.a1table7 NO AUDIT ;
    #      LOAD a1table7 , \columba.$talon.yugal2.a1table8 ;
    #      ALTER TABLE a1table8 AUDIT ;
    #      UPDATE HISTOGRAM STATISTICS FOR TABLE a1table8 ;
    #      SELECT * FROM a1table8 ;
    #
    #      CREATE TABLE a1table9 LIKE \columba.$talon.yugal2.a1table7 WITH HEADINGS NO AUDIT ;
    #      LOAD a1table7 , \columba.$talon.yugal2.a1table9 ;
    #      ALTER TABLE a1table9 AUDIT ;
    #      UPDATE HISTOGRAM STATISTICS FOR TABLE a1table9 ;
    #      SELECT * FROM a1table9 ;
    #
    #   ---------------------------
    #   Check catalog table COLUMNS for HEADING information on
    #   all A1 tables and views:
    #   ---------------------------
    #    UPDATE STATISTICS FOR TABLE columns ;

    stmt = """DROP VIEW a1view7p;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """DROP VIEW a1view7s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """DROP VIEW a1view7e;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """DROP TABLE a1table1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """DROP TABLE a1table2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """DROP TABLE a1table3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """DROP TABLE a1table4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """DROP TABLE a1table5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """DROP TABLE a1table6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """DROP TABLE a1table7;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test002(desc="""a05"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # Test case name:	pretsta05
    # Description:		This test creates the table btre201, and its
    #			indes, and inserts the values into the table.
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
, y_to_d              date                    default null
, h_to_f              datetime hour to fraction(3) default null
, time1               time                    default null
, iy_to_mo            interval year(4) to month  default null
, ih_to_s             interval hour to second default null
, primary key (ordering)
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3195')
    
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
, y_to_d              date                    default null
, h_to_f              time(3) 		    default null
, time1               time                    default null
, iy_to_mo            interval year(4) to month  default null
, ih_to_s             interval hour to second default null
, primary key (ordering)
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #  Create INDEXES for table BTRE201.
    stmt = """create index btre201a 
on btre201 (ordering)
-- 1/25/99 For now the only blocksize supported is 4096
--      ATTRIBUTES
--      blocksize 512
;"""
    output = _dci.cmdexec(stmt)
    stmt = """create index btre201b 
on btre201 (char_1, alwaysnull, binary_signed)
;"""
    output = _dci.cmdexec(stmt)
    stmt = """create index btre201c 
on btre201 (var_char_3, large_int)
-- 1/25/99 For now the only blocksize supported is 4096
--      ATTRIBUTES
--      blocksize 512
;"""
    output = _dci.cmdexec(stmt)
    stmt = """create index btre201d 
on btre201 (decimal_3_unsigned, pic_decimal_1)
-- 1/25/99 For now the only blocksize supported is 4096
--      ATTRIBUTES
--      blocksize 512
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
on btre201 (y_to_d DESC)
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
    
    stmt = """CREATE table btsel05 
(
pic_x_a picture x(3)  not null
, pic_x_b pic     x     not null
, pic_x_c pic     x(2)  not null
, col_1   char     (5)  not null
, col_2   char     (5)  not null
, col_3   pic     x(5)  not null
, col_4   pic     x(5)  not null
, col_5   pic     xxxxx not null
, col_6   pic     xxxxx not null
, col_7   pic     x(4)x not null
, col_8   pic   x(1)x(4) not null
, col_9   varchar  (5)  not null
, col_10  varchar  (5)  not null
) no partition;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT into btsel05 values ('joe','A','al','pablo','david',
'amy','amy','steve','steve','walt',
'mojo','joe','percy');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT into btsel05 values ('sue','A','in','peggy','diane',
'zora','cathy','mary','mary',
'rhoda','debra','sue','madge');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT into btsel05 values ('deb','D','jo','lowry','mary',
'sunny','debra','junk','junk',
'junk','junk','junk','junk');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT into btsel05 values ('can','D','by','lowry','steve',
'slope','debby','junk','junk',
'junk','junk','junk','junk');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT into btsel05 values ('box','C','to','howie','debra',
'snow','debbi','junk','junk',
'junk','junk','junk','junk');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT into btsel05 values ('red','B','go','lowry','sue',
'ski','cammy','junk','junk',
'junk','junk','junk','junk');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT into btsel05 values ('why','B','so','lowry','amy',
'squaw','tammy','junk','junk',
'junk','junk','junk','junk');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT into btsel05 values ('not','B','on','lowry','mary',
'mogul','pammy','junk','junk',
'junk','junk','junk','junk');"""
    output = _dci.cmdexec(stmt)
    
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:         A05
    #  Description:            UPSHIFT function (Positive).
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:        (provide a high-level description)
    #
    #  Notes:
    #  Set the variable seldbvol before running
    #  this test.
    #  This test case incorporates features detailed in the "Title"
    #  by Ima Programmer (Version 1.1, <date>).
    #
    # =================== End Test Case Header  ===================
    
    #  ---------------------------
    #  Select from all types of data, with UPSHIFT function on columns:
    #  ---------------------------
    stmt = """SELECT ordering
FROM btre201 
ORDER BY ordering
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s0')
    stmt = """SELECT ordering, upshift( char_1)
FROM btre201 
ORDER BY ordering
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s1')
    stmt = """SELECT ordering, upshift( pic_x_8 )
FROM btre201 
ORDER BY ordering
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s2')
    stmt = """SELECT ordering, upshift( var_char_2 )
FROM btre201 
ORDER BY ordering
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s3')
    stmt = """SELECT ordering, upshift( var_char_3 )
FROM btre201 
ORDER BY ordering
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s4')
    
    #  ---------------------------
    #  Select with UPSHIFT of column in WHERE clause with LIKE:
    #  ---------------------------
    stmt = """SELECT pic_x_a
, col_4
FROM btsel05 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s5')
    stmt = """SELECT pic_x_a
, col_4
FROM btsel05 
WHERE UPSHIFT(col_4) LIKE '_AMMY%'
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s6')
    
    #  ---------------------------
    #  Select with UPSHIFT of column in WHERE clause with param:
    #  ---------------------------
    
    stmt = """SELECT pic_x_a
, col_1
FROM btsel05 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s7')
    
    stmt = """SET PARAM ?myparam1 'Lowry' ;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """SELECT pic_x_a
, col_1
FROM btsel05 
WHERE UPSHIFT(col_1) = UPSHIFT(?myparam1)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s8')
    
    stmt = """RESET PARAM;"""
    output = _dci.cmdexec(stmt)
    
    #  ---------------------------
    #  Select with UPSHIFT of column in WHERE clause with param:
    #  ---------------------------
    stmt = """SET PARAM ?myparam1 'Lowry' ;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """SELECT pic_x_a
, col_1
FROM btsel05 
WHERE UPSHIFT(col_1) = UPSHIFT(?myparam1)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s9')
    
    stmt = """RESET PARAM;"""
    output = _dci.cmdexec(stmt)
    
    #  ---------------------------
    #  Select with UPSHIFT of param in select list:
    #  ---------------------------
    stmt = """SET PARAM ?myparam1 'Lowry';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """SELECT pic_x_a , col_1 , UPSHIFT(col_1)
FROM btsel05 
ORDER BY pic_x_a, col_1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s10')
    stmt = """SELECT pic_x_a , col_1 , UPSHIFT('Lowry')
FROM btsel05 
ORDER BY pic_x_a, col_1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s11')
    stmt = """SELECT pic_x_a , col_1 , UPSHIFT(?myparam1)
FROM btsel05 
ORDER BY pic_x_a, col_1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s12')
    stmt = """SELECT pic_x_a , col_1
FROM btsel05 
ORDER BY pic_x_a, col_1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s13')
    
    stmt = """show param ?myparam1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s14')
    
    stmt = """drop index btre201a;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index btre201b;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index btre201c;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index btre201d;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index btre201e;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index btre201f;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index btre201g;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index btre201h;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index btre201i;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index btre201j;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index btre201k;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index btre201l;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index btre201m;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """drop table btre201;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test003(desc="""n06"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # Test case name:	pretstn06
    # Description:		This test creates the table btre201, and its
    #			indes, and inserts the values into the table.
    # Expected Results:
    
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
, y_to_d              date                    default null
--      , h_to_f              datetime hour to fraction(3) default null
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
on btre201 (y_to_d DESC)
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create index btre201i 
on btre201 (float_double_p ASC)
;"""
    output = _dci.cmdexec(stmt)
    
    #    create index btre201j
    #      on btre201 (h_to_f) ;
    
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
    
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:         N06
    #  Description:            UPSHIFT function  (Negative)
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:        (provide a high-level description)
    #
    #  Notes:
    #  Set the environment variable seldbvol
    #  before running the test.
    #  This test case incorporates features detailed in the "Title"
    #  by Ima Programmer (Version 1.1, <date>).
    #
    # =================== End Test Case Header  ===================
    #  ---------------------------------
    #   Attempt to upshift non-character fields:
    #  ---------------------------------
    
    stmt = """SELECT ordering, upshift(alwaysnull )
FROM btre201 
ORDER BY ordering
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4043')
    stmt = """SELECT ordering, upshift( binary_signed )
FROM btre201 
ORDER BY ordering
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4043')
    stmt = """SELECT ordering, upshift( pic_comp_3 )
FROM btre201 
ORDER BY ordering
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4043')
    stmt = """SELECT ordering, upshift( small_int )
FROM btre201 
ORDER BY ordering
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4043')
    stmt = """SELECT ordering, upshift( medium_int )
FROM btre201 
ORDER BY ordering
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4043')
    stmt = """SELECT ordering, upshift( decimal_1 )
FROM btre201 
ORDER BY ordering
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4043')
    stmt = """SELECT ordering, upshift( float_basic )
FROM btre201 
ORDER BY ordering
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4043')
    stmt = """SELECT ordering, upshift( float_real )
FROM btre201 
ORDER BY ordering
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4043')
    stmt = """SELECT ordering, upshift( float_double_p )
FROM btre201 
ORDER BY ordering
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4043')
    stmt = """SELECT ordering, upshift( y_to_d )
FROM btre201 
ORDER BY ordering
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4043')

    stmt = """SELECT ordering , UPSHIFT( time1 )
FROM btre201 
ORDER BY ordering
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4043')
    stmt = """SELECT ordering , UPSHIFT( iy_to_mo )
FROM btre201 
ORDER BY ordering
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4043')
    stmt = """SELECT ordering , UPSHIFT( ih_to_s )
FROM btre201 
ORDER BY ordering
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4043')
    
    #  ---------------------------------
    #   Attempt to upshift functions:
    #  ---------------------------------
    stmt = """SELECT UPSHIFT ( MAX (pic_x_a) )
FROM btsel05 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n06exp""", 'n06s14')
    stmt = """SELECT MAX ( UPSHIFT (pic_x_a) )
FROM btsel05 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n06exp""", 'n06s15')
    
    # Test case name:	psttstn06
    # Test case author:
    # Description:		This test drops the table btre201, and its index.
    # Expected Results:
    #
    
    stmt = """drop index btre201a;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index btre201b;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index btre201c;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index btre201d;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index btre201e;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index btre201f;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index btre201g;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index btre201h;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index btre201i;"""
    output = _dci.cmdexec(stmt)
    #    drop index btre201j;
    stmt = """drop index btre201k;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index btre201l;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index btre201m;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """drop table btre201;"""
    output = _dci.cmdexec(stmt)
    
    #               End of test case ARKT0155
    _testmgr.testcase_end(desc)

