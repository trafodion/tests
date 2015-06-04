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
    
    stmt = """CREATE TABLE btsel12 (
data_x3                PIC X(3)               not null not droppable
, data_93                PIC 9(3)               not null not droppable
, PRIMARY KEY ( data_x3 ) not droppable
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """CREATE INDEX btsel12a ON btsel12 ( data_93 );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into btsel12 values ('tom',100);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into btsel12 values ('bob',200);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into btsel12 values ('run',300);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into btsel12 values ('sun',400);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into btsel12 values ('fun',500);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into btsel12 values ('gun',600);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into btsel12 values ('nun',700);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into btsel12 values ('pun',800);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """update statistics for table btsel12 on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """CREATE TABLE btsel16 (
small_int              SMALLINT               not null not droppable
, data_93                PIC 9(3)               not null not droppable
) no partition
-- Defaults to SYSKEY
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """CREATE INDEX btsel16a ON btsel16 ( small_int );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into btsel16 values (1000,167);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into btsel16 values (2000,168);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into btsel16 values (8500,169);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into btsel16 values (8501,170);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into btsel16 values (8502,171);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into btsel16 values (8503,172);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into btsel16 values (8504,173);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into btsel16 values (8505,174);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """update statistics for table btsel16 on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """CREATE TABLE btemprel ( some_data PIC 9(3) not null not droppable ) no partition
--        STORE BY ENTRY ORDER
--        ATTRIBUTE
--                NO AUDIT
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """CREATE INDEX btempre0 ON btemprel (some_data) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
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
    _dci.expect_complete_msg(output)
    
    stmt = """insert into btsel03 values ('A',5,'make',90,200);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into btsel03 values ('7',6,'joe',80,1200);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into btsel03 values ('8',6,'joe',80,1200);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into btsel03 values ('5',1000,'5',100,1000);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into btsel03 values ('michael',50,'dave',50,1500);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into btsel03 values ('7',6,'john',80,2000);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into btsel03 values ('B',6,'mark',80,3000);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into btsel03 values ('michael',70,'joan',50,4000);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """update statistics for table btsel03 on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """CREATE TABLE btsel04 (
var_char               VARCHAR(251)           not null not droppable
, medium_int             INTEGER SIGNED         not null not droppable
, pic_x_7                PIC X(7)               not null not droppable
, pic_comp_1             numeric (10,0) signed  not null not droppable
) no partition
--      STORE BY ENTRY ORDER
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """CREATE INDEX btsel04a ON btsel04 ( pic_x_7 );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # Limit of 251 byte on UNIQUE VARCHAR for alternate index.
    stmt = """CREATE UNIQUE INDEX btsel04b 
--     CREATE INDEX btsel04b
ON btsel04 ( var_char )
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """CREATE VIEW pvsel04 
AS SELECT *
FROM btsel04 
WHERE ( pic_comp_1 > 100 )
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into btsel04 values ('tom',1000,'7',200);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into btsel04 values ('bob',999,'A',300);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into btsel04 values ('sue',200,'sue',100);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into btsel04 values ('bobby',200,'sue',100);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into btsel04 values ('bill',2000,'B',500);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into btsel04 values ('christopher',1000,'white',1000);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into btsel04 values ('william',1000,'black',2000);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into btsel04 values ('marilyn',2000,'green',3000);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """update statistics for table btsel04 on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """CREATE TABLE btsel02 (
pic_x_1                PIC X(1)  not null not droppable
) no partition
--      STORE BY ENTRY ORDER
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into btsel02 values ('B');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into btsel02 values ('C');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into btsel02 values ('B');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into btsel02 values ('Q');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into btsel02 values ('B');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into btsel02 values ('C');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into btsel02 values ('Q');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into btsel02 values ('Q');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """update statistics for table btsel02 on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
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
    
    # Index the table with 3_column index, reversing order of columns:
    
    stmt = """CREATE INDEX btsel05a 
ON btsel05 ( pic_x_c , pic_x_b , pic_x_a );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into btsel05 values ('joe','A','al','pablo','david',
'amy','amy','steve','steve','walt',
'mojo','joe','percy');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into btsel05 values ('sue','A','in','peggy','diane',
'zora','cathy','mary','mary',
'rhoda','debra','sue','madge');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into btsel05 values ('deb','D','jo','lowry','mary',
'sunny','debra','junk','junk',
'junk','junk','junk','junk');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into btsel05 values ('can','D','by','lowry','steve',
'slope','debby','junk','junk',
'junk','junk','junk','junk');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into btsel05 values ('box','C','to','howie','debra',
'snow','debbi','junk','junk',
'junk','junk','junk','junk');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into btsel05 values ('red','B','go','lowry','sue',
'ski','cammy','junk','junk',
'junk','junk','junk','junk');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into btsel05 values ('why','B','so','lowry','amy',
'squaw','tammy','junk','junk',
'junk','junk','junk','junk');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into btsel05 values ('not','B','on','lowry','mary',
'mogul','pammy','junk','junk',
'junk','junk','junk','junk');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """CREATE TABLE btsel07 (
pic_x_a                PIC X(3)           not null not droppable
, pic_x_b                PIC X(1)           not null not droppable
, pic_x_c                PIC X(2)           not null not droppable
, PRIMARY KEY ( pic_x_c, pic_x_b, pic_x_a ) not droppable
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """CREATE INDEX btsel07a ON btsel07 ( pic_x_a );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into btsel07 values  ('jo','Z','jo');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into btsel07 values  ('al','Q','al');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into btsel07 values  ('P','P','P');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into btsel07 values  ('B','A','ed');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into btsel07 values  ('jo','C','ek');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into btsel07 values  ('JO','D','em');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into btsel07 values  ('al','E','bo');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into btsel07 values  (' al','F','di');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into btsel07 values  ('al ','F','al');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into btsel07 values  (' al','F','al');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """update statistics for table btsel07 on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
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
    _dci.expect_complete_msg(output)
    
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
ATTRIBUTE
blocksize 4096
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # Index the table with simple, 1-column indexes:
    
    stmt = """CREATE INDEX btsel01a ON btsel01 ( pic_x_1 );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """CREATE INDEX btsel01b ON btsel01 ( decimal_2_signed );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """CREATE INDEX btsel01c ON btsel01 ( pic_comp_3 );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """CREATE INDEX btsel01d ON btsel01 ( pic_x_long );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into btsel01 values ('A','steven','C','walter','bob',
'B',50,50,200,50,0.12,100.9,
10,10000,1000000000,4,.5,90,
1.1,0.1,1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into btsel01 values ('A','bobby','A','bobby','bop',
'B',60,60,1200,60,0.79,100.99,
1000,8000,-1000,5,.6,100,
2.1,0.2,2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into btsel01 values
('D','steven','B','9','bat','thomas',
8000,70,2000,500,0.10,100.999,
90,10000,1000,7,.7,110,
3.1,0.3,3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into btsel01 values
('D','melissa','C','7','pop','jimmy',
1000,80,1500,500,0.20,100.9999,
80,9000,999,5,.8,120,
4.1,0.4,4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into btsel01 values ('E','monica','Q','sue','pat',
'christopher',
2000,90,1200,3000,0.30,100.99999,
2000,8000,-1000000,1,.9,80,
5.1,0.5,5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into btsel01 values
('D','michelle','D','michael','rat',
'thomas',
-5000,90,2000,500,0.40,100.8,
90,8000,200,7,.93,140,
6.1,0.6,6);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into btsel01 values ('C','maureen','E','jimmy','rum',
'marilyn',
3000,80,2000,500,0.50,100.7,
9000,1000,2000,8,.97,150,
7.1, 0.7,7);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into btsel01 values ('C','marcia','Z','johnny','dum',
'thomas',
4000,40,2000,50,0.60,100.6,
8000,5000,0,9,.99,110,
8.1,0.8,8);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """update statistics for table btsel01 on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
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
    _dci.expect_complete_msg(output)
    
    stmt = """insert into btsel06 values  ('joe','Z','in',100,200,100,200,
200,100,100,100,50,100,100,200,
100,200,200,100,100,100,50,100,
100,200,100,200,200,100,100,100,
100,200,100,200,200,100,100,100,
50,100);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into btsel06 values
('sue','Q','on',200,400,100,100,400,
100,100,50,100,200,200,400,100, 100,
400,100,100,50,100,200,200,400, 100,
100,400,100,100,50,200,400,100, 100,
400,100,100,50,100,200);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into btsel06 values
('pam','D','al',900,1000,900,1000,1000,
50,1000,1000,1000,1000,1000,1000,1000,
1000,1000,1000,1000,1000,1000,1000,1000,
1000,1000,1000,1000,1000,1000,1000,1000,
1000,1000,1000,1000,1000,1000,1000,1000,
1000);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into btsel06 values
('sue','C','by',300,1000,500,1000,1000,
50,1000,1000,1000,1000,1000,1000,1000,
1000,1000,1000,1000,1000,1000,1000,1000,
1000,1000,1000,1000,1000,1000,1000,1000,
1000,1000,1000,1000,1000,1000,1000,1000,
1000);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into btsel06 values
('joe','A','jo',100,1000,200,1000,1000,
50,1000,1000,1000,1000,1000,1000,1000,
1000,1000,1000,1000,1000,1000,1000,1000,
1000,1000,1000,1000,1000,1000,1000,1000,
1000,1000,1000,1000,1000,1000,1000,1000,
1000);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into btsel06 values
('joe','B','to',300,1000,400,1000,1000,
50,1000,1000,1000,1000,1000,1000,1000,
1000,1000,1000,1000,1000,1000,1000,1000,
1000,1000,1000,1000,1000,1000,1000,1000,
1000,1000,1000,1000,1000,1000,1000,1000,
1000);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into btsel06 values
('joe','C','go',100,1000,200,1000,1000,
50,1000,1000,1000,1000,1000,1000,1000,
1000,1000,1000,1000,1000,1000,1000,1000,
1000,1000,1000,1000,1000,1000,1000,1000,
1000,1000,1000,1000,1000,1000,1000,1000,
1000);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into btsel06 values
('sue','D','so',200,1000,300,1000,1000,
50,1000,1000,1000,1000,1000,1000,1000,
1000,1000,1000,1000,1000,1000,1000,1000,
1000,1000,1000,1000,1000,1000,1000,1000,
1000,1000,1000,1000,1000,1000,1000,1000,
1000);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """update statistics for table btsel06 on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """CREATE TABLE btempkey ( some_data PIC 9(3) not null not droppable) no partition
--  ATTRIBUTE
--         NO AUDIT
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """CREATE TABLE region (
regnum                 PIC 9(2)     not null not droppable,
regname                PIC X(12)    not null not droppable,
location               VARCHAR (14) not null not droppable,
manager                PIC 9(4)     not null not droppable,
PRIMARY KEY (regnum) not droppable
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """CREATE INDEX region0 ON region (regname);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """INSERT INTO  region VALUES ( 1,'EAST        ',
'NEW YORK' ,  29);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO  region VALUES ( 2,'CENTRAL     ',
'CHICAGO'  , 104);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO  region VALUES ( 3,'WEST        ',
'DALLAS'   ,  72);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO  region VALUES ( 4,'CANADA      ',
'TORONTO'  , 343);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO  region VALUES ( 5,'GERMANY     ',
'FRANKFURT',  43);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO  region VALUES ( 6,'ENGLAND     ',
'LONDON'   ,  87);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO  region VALUES (99,'HEADQUARTERS',
'CUPERTINO',   1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """update statistics for table  region on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
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
    _dci.expect_complete_msg(output)
    
    stmt = """CREATE INDEX btsel10a ON btsel10 ( pic_x_a );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into btsel10 values
('tom','tom',3,'abadefih',100,100,-100);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into btsel10 values
('bob','bobby',2,'ebediih',90,100,-1000);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into btsel10 values
('sue','sue',1,'ebedafiih',110,80,100);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into btsel10 values
('rod','for',400,'inside',25,60,0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into btsel10 values
('don','who',50,'outside',10000,100,-100);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into btsel10 values
('jon','does',1000,'offsides',50000, 500,100);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into btsel10 values
('ron','they',2000,'onsides',10000,100, -100);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into btsel10 values
('rob','bobby',2,'ebediih',90,100,-1000);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """update statistics for table btsel10 on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
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
    _dci.expect_complete_msg(output)
    
    stmt = """insert into btsel11 values
('bob','bob', 100,'abadefih', 160,200,200);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into btsel11 values
('dan','sue', 100,'ebediih', 100,100,60);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into btsel11 values
('boe','tommy', 200,'ebedafiih', 200,50,50);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into btsel11 values
('bar','where', 300,'gone', 200,9999,-100);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into btsel11 values
('car','who', 400,'done', 160,500,500);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into btsel11 values
('tar','what', 500,'none', 100,8888,0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into btsel11 values
('jar','how', 600,'inside', 160,500,500);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into btsel11 
values ('mar','why', 50,'house', 50,7777,0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """update statistics for table btsel11 on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """CREATE TABLE btsel15 (
small_int              SMALLINT               not null not droppable
, data_93                PIC 9(3)               not null not droppable
, PRIMARY KEY ( data_93 ) not droppable
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into btsel15 values (1000,100);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into btsel15 values (2000,200);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into btsel15 values (1111,90);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into btsel15 values (2222,80);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into btsel15 values (3333,70);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into btsel15 values (4444,60);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into btsel15 values (5555,50);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into btsel15 values (6666,40);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """update statistics for table btsel15 on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """CREATE TABLE btempent ( some_data PIC 9(3) not null not droppable ) no partition
--        STORE BY ENTRY ORDER
;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

