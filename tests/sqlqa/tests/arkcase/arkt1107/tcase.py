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
    #  Test case name:     T1107:A01
    #  Description:        This test verifies the SQL INSERT and
    #                      UPDATE features. It also tests for Derived
    #                      Tables.
    #
    # =================== End Test Case Header  ===================
    #
    # To start with empty objects, clean up what this testcase uses;
    # should be 0 rows (i.e. empty already).
    
    stmt = """delete from TAB1;"""
    output = _dci.cmdexec(stmt)
    stmt = """delete from TAB4;"""
    output = _dci.cmdexec(stmt)
    #
    #  Expect 6 rows,
    #  N1                    C2  C3  C4
    #  --------------------  --  --  --------
    #
    #                 -4344  AA  BA  BA
    #                 -3552  BA  AA  AA
    #                 -2789  DA  EA         ?
    #                 -2389  BA  AA  AA
    #                     ?   ?  BA  BA
    #                     ?   ?  DA  DA
    stmt = """select * from V5fixed order by 1, 3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s0')
    #
    stmt = """select CHAR5_N20, CHAR6_N100, CHAR7_500
, CHAR12_N2000, CHAR15_100, CHAR16_N20
from T5fixed 
order by 1, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s1')
    #
    #  Expect { AA}.
    stmt = """select * from (select min(c4) from V5fixed) dt ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s2')
    #
    # ---------------------------
    # Insert into single column.
    # ---------------------------
    #      Id: IN.001      Insert select-of-degree-1 into 1-col table
    #      Id: RV.001      RVC: Insert 1 expression.
    #			Note: Syntax error if subquery placed in values:
    #			e.g. insert into TAB1 values
    #			     (select max(c4) from V5fixed) ;
    #      Id: DT.032      Insert values selected via Derived Table on view containing outer join.
    #
    stmt = """insert into TAB1 
select min(c4)
from V5fixed 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into TAB1 
( select max(c4) from V5fixed 
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #  Expect ((AA) (DA))
    stmt = """select * from TAB1 order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s3')
    stmt = """delete from TAB1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 2)
    #
    # ---------------------------
    #      Id: IN.002      Insert set of single values into 1-col table
    # ---------------------------
    # 97/10/01 insert ... values (DEFAULT) not supported.
    #
    stmt = """set param ?param1 'param one' ;"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into TAB1 values
('1 literal')
, (DEFAULT)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 2)
    stmt = """insert into TAB1 values
('2 literal')
, (?param1)
, (NULL)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 3)
    #  Expect 5 rows.
    stmt = """select * from TAB1 order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s4')
    stmt = """delete from TAB1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 5)
    #
    # ---------------------------
    #      Id: TV.001      Insert into <table> values <TVC> (multiple rows).
    # ---------------------------
    stmt = """insert into TAB1 values
('3 literal')
, ('4 literal')
, ('5 literal')
, ('6 literal')
, ('7 literal')
, ('8 literal')
, (?param1)
, ('9 literal')
, ('10 literal')
, ('11 literal')
, ('12 literal')
, ('13 literal')
, ('14 literal')
, ('15 literal')
, ('16 literal')
, ('17 literal')
, ('18 literal')
, (NULL)
, ('19 literal')
, ('20 literal')
, ('21 literal')
, ('22 literal')
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 22)
    #  Expect 22 rows.
    stmt = """select * from TAB1 order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s5')
    stmt = """delete from TAB1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 22)
    #
    #  ---------------------------
    #       Id: IN.003      Insert multiple values from SELECTs into 1-col table
    #  ---------------------------
    #
    stmt = """select c2 from V5fixed 
union all
select c3 from V5fixed 
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s6')
    stmt = """insert into TAB1 
select c2 from V5fixed 
union all
select c3 from V5fixed 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 12)
    #  Expect 5 rows.
    stmt = """select * from TAB1 order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s7')
    stmt = """delete from TAB1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 12)
    #
    stmt = """select c2 from V5fixed 
union
select c3 from V5fixed 
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s8')
    stmt = """insert into TAB1 
select * from
( select c2 from V5fixed 
union
select c3 from V5fixed 
) dt
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 5)
    #  Expect 5 rows ( (AA) (BA) (DA) (EA) (?) ).
    stmt = """select * from TAB1 order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s9')
    stmt = """delete from TAB1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 5)
    #
    stmt = """insert into TAB1 
( select c2 from V5fixed) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 6)
    #  Expect 6 rows ( (AA) (BA) (BA) (DA) (?) (?) ).
    stmt = """select * from TAB1 order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s10')
    stmt = """delete from TAB1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 6)
    #
    # ---------------------------
    # Insert into multiple columns.
    # ---------------------------
    #      Id: IN.011      Insert 1 row from select-of-degree-2 into 2 cols of a table.
    # ---------------------------
    # Remember the default values for TAB4:
    # vc9 varchar(10) DEFAULT '9 varchar'
    # vc7 varchar(11) DEFAULT '11 varchar'
    # vc5 varchar(5)  DEFAULT '5 var'
    # vc3 varchar(3)  DEFAULT '3 v'
    #
    stmt = """insert into TAB4 (vc9, vc7)
select min(c4), max(c4) from V5fixed 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #
    #  Expect (('AA' 'DA' '5 var' '3 v'))
    stmt = """select * from TAB4 order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s11')
    stmt = """delete from TAB4 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    #
    # ---------------------------
    #      Id: IN.012      Insert multiple rows into 3 cols of a table.
    # ---------------------------
    #
    stmt = """set param ?param1 'param val' ;"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into TAB4 (vc9, vc7, vc3) values
('01 literal', ?param1 , NULL)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #  Expect (('01 literal' 'param val' '5 var' ?))
    stmt = """select * from TAB4 order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s12')
    stmt = """delete from TAB4 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    #
    # ---------------------------
    #      Id: TV.003      Insert into <table> SELECT <select-list> FROM VALUES
    #                      <TVC>, includes expressions.
    # ---------------------------
    #
    stmt = """set param ?pl ' literal' ;"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into TAB4 (vc9, vc7, vc3) values
(?param1     , '04'|| ?pl , '0'|| '5' )
, ('06 literal', '07'|| ?pl , '08')
, (?param1     , '09 literal' , '10')
, ('11 literal', '12'|| ?pl , '13')
, ('14'|| ?pl  , '15'|| ?pl , ' ' || '16' )
, ('17 literal', '18 literal', NULL)
, ('19 literal', '20 literal', ' 21')
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 7)
    #  Expect 7 rows.
    stmt = """select * from TAB4 order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s14')
    stmt = """delete from TAB4 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 7)
    #
    #  ---------------------------
    #       Id: IN.013      Insert multiple values from SELECTs into 1-col table
    #  ---------------------------
    #
    stmt = """select c2,c4 from V5fixed 
union all
select c3,c4 from V5fixed 
order by 1,2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s15')
    stmt = """insert into TAB4  (vc9, vc5)
select c2,c4 from V5fixed 
union all
select c3,c4 from V5fixed 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 12)
    #  Expect 12 rows with values from view, and column defaults
    #  where no value is inserted.
    stmt = """select vc9, vc7, vc5, vc3 from TAB4 order by 1,3 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s16')
    stmt = """delete from TAB4 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 12)
    #
    stmt = """select c2,c4 from V5fixed 
union
select c3,c4 from V5fixed 
order by 1,2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s17')
    stmt = """insert into TAB4 (vc9, vc7)
select * from
( select c2,c4 from V5fixed 
union
select c3,c4 from V5fixed 
) dt
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 9)
    #  Expect 9 rows omitting duplicate values from view; expect column defaults
    #  where no value is inserted.
    stmt = """select vc9, vc7, vc5, vc3 from TAB4 order by 1,2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s18')
    stmt = """delete from TAB4 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 9)
    #
    #  Expect (('DAAAAAAA'))
    stmt = """select CHAR5_N20  from T5fixed 
where CHAR5_N20  > 'D' ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s19')
    #  Expect (('ACAAAAAA'))
    stmt = """select CHAR15_100 from T5fixed 
where CHAR15_100 < 'AT' ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s20')
    #  Expect (('ACA')) -- the warning message looks bogus;
    #  why get a warning when we are CASTing?
    stmt = """select cast(CHAR15_100 as varchar(3))
from T5fixed 
where CHAR15_100 < 'AT'
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s21')
    stmt = """insert into TAB4 (vc3)
( select cast(CHAR15_100 as char(3))
from T5fixed 
where CHAR15_100 < 'AT'
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into TAB4 (vc9)
select * from (
select CHAR5_N20 from T5fixed 
where CHAR5_N20 > 'D'
union all
select CHAR15_100 from T5fixed 
where CHAR15_100 < 'AT'
) dt1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 2)
    #  Expect 3 rows:
    #  (('9 varchar'  '11 varchar'  '5 var'  'ACA')
    #  ('ACAAAAAA'  '11 varchar'  '5 var'  '3 v' )
    #  ('DAAAAAAA' '11 varchar'  '5 var'  '3 v' ))
    stmt = """select * from TAB4 order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s23')
    stmt = """delete from TAB4 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 3)
    #
    stmt = """insert into TAB4 (vc9, vc7)
select * from (
select CHAR5_N20, CHAR15_100
from T5fixed where CHAR5_N20 <> 'a'
union all
select CHAR15_100, CHAR5_N20
from T5fixed where CHAR15_100 <> 'c'
) dt1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 12)
    #  Expect 12 rows (6 + 6 rows from original table).
    stmt = """select * from TAB4 order by 1, 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s24')
    stmt = """delete from TAB4 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 12)
    
    _testmgr.testcase_end(desc)

def test002(desc="""a02"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     T1107:A02
    #  Description:        This test verifies the SQL INSERT and
    #                      UPDATE features, specifically DEFAULT.
    #
    # =================== End Test Case Header  ===================
    #
    #
    # To start with empty objects, clean up what this testcase uses;
    # should be 0 rows (i.e. empty already).
    
    stmt = """delete from TAB1;"""
    output = _dci.cmdexec(stmt)
    stmt = """delete from TAB4;"""
    output = _dci.cmdexec(stmt)
    #
    # ---------------------------
    #      Id: IN.021      Insert DEFAULT VALUES; table has implicit DEFAULT values
    #      Id: IN.024      Insert DEFAULT VALUES; table has "a few" columns
    #      Id: IN.031      Insert DEFAULT VALUES; table is key-sequenced with SYSKEY.
    # Also:
    #      Id: UP.023      Update with DEFAULT VALUES; table has "a few" columns
    #      Id: UP.025      Update with DEFAULT VALUES; table is key-sequenced with SYSKEY.
    # ---------------------------
    stmt = """insert into TAB1 values ('a value');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #  Expect 1 row.
    stmt = """select * from TAB1 order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s0')
    #
    # Null default values.
    stmt = """insert into TAB4 (vc9, vc7, vc3) values
('01 literal', '01 vc7', NULL)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into TAB4 values
('vc9 02', 'vc7 02', 'vc502', 'vc3')
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    # Insert into non-empty table.
    stmt = """insert into TAB4 DEFAULT VALUES ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #  Expect 3 rows.
    stmt = """select * from TAB4 order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s1')
    #
    # Update non-DEFAULT values to default.
    # 5/7/98 Use NULLs until DEFAULT is supported.
    stmt = """UPDATE TAB4 SET vc7 = (SELECT vc FROM TAB1)
--    , vc5 = DEFAULT
, vc5 = NULL
, vc3 = (SELECT cast(vc as varchar(3)) FROM TAB1)
--    , vc9 = DEFAULT ;
, vc9 = NULL;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 3)
    #  Expect 3*(NULL  'a value'  NULL  'a v') at 1998 Beta.
    stmt = """select * from TAB4 order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s2')
    # UPDATE TAB4 SET vc7 = DEFAULT
    stmt = """UPDATE TAB4 SET vc7 = NULL
--    , vc5 = DEFAULT, vc3 = DEFAULT, vc9 = DEFAULT ;
, vc5 = NULL, vc3 = NULL, vc9 = NULL ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 3)
    #  Expect 3 rows of NULL values at 1998 Beta.
    stmt = """select * from TAB4 order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s3')
    #
    stmt = """delete from TAB4 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 3)
    #
    # Insert into empty table.
    stmt = """insert into TAB4 DEFAULT VALUES ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #  Expect 3 rows.
    stmt = """select * from TAB4 order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s4')
    #
    # Cleanup.
    stmt = """delete from TAB1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    stmt = """delete from TAB4 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    #
    # ---------------------------
    #      Id: IN.022      Insert DEFAULT VALUES; table has explicit, non-NULL DEFAULT values.
    #      Id: IN.025      Insert DEFAULT VALUES; table has 1 column.
    #      Id: IN.027      Insert DEFAULT VALUES into updateable view.
    # Also:
    #      Id: UP.024      Update with DEFAULT VALUES; table has 1 column.
    #      Id: UP.027      Update with DEFAULT VALUES into updateable view.
    # ---------------------------
    #
    # Make temporary 1-column table.
    stmt = """create table TABTEMP (i int default 3) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """insert into TABTEMP DEFAULT VALUES ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """create view VTEMP as select * from TABTEMP ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into VTEMP DEFAULT VALUES ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #  Expect (3).
    stmt = """select * from TABTEMP order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s5')
    #
    stmt = """insert into VTEMP values (54) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    # UPDATE VTEMP SET i = DEFAULT ;
    stmt = """UPDATE VTEMP SET i = NULL ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 3)
    #  Expect ((3),(3)) -- but until Default supported expect ((3), (54))
    stmt = """select * from TABTEMP order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s6')
    #
    stmt = """drop view  VTEMP ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table TABTEMP ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    stmt = """create table TABTEMP (v varchar(4) default 'def') no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """insert into TABTEMP DEFAULT VALUES ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """create view  VTEMP as select * from TABTEMP ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #  Expect ('def').
    stmt = """select * from TABTEMP order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s7')
    #
    stmt = """insert into VTEMP values ('four') ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    # UPDATE VTEMP SET v = DEFAULT ;
    stmt = """UPDATE VTEMP SET v = NULL ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 2)
    #  Expect (def), (def)
    #  but until Default supported expect ((def), (four))
    stmt = """select * from TABTEMP order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s8')
    #
    stmt = """drop view  VTEMP ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table TABTEMP ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    # ---------------------------
    #      Id: IN.032      Insert DEFAULT VALUES; key-sequenced table with user-defined key
    #      Id: UP.026      Update with DEFAULT VALUES; key-sequenced table with user-defined key
    # ---------------------------
    # Make temporary table with user key.
    stmt = """create table TABTEMP (i1 int
, i2 int default 21 not null
, i3 int
, i4 int default 42 not null
, primary key (i4, i2) );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    stmt = """insert into TABTEMP VALUES (1,2,3,4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into TABTEMP DEFAULT VALUES;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #  Do not attempt to update columns of primary key -- update not
    #  supported in 1997 releases.
    #  Expect 2 rows.
    stmt = """select * from TABTEMP order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s9')
    #
    stmt = """drop table TABTEMP ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test003(desc="""a03"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     T1107:A03
    #  Description:        This test verifies the SQL INSERT and UPDATE
    #                      features, with update using subquery that uses a
    #                      new feature.  Because of SQL architecture, not
    #                      all new constructs need be tested, e,g,: INSERT
    #                      INTO <sometable> SELECT that contains CASE
    #
    # =================== End Test Case Header  ===================
    #
    #
    # To start with empty objects, clean up what this testcase uses;
    # should be 0 rows (i.e. empty already).
    
    stmt = """delete from TAB4;"""
    output = _dci.cmdexec(stmt)
    
    #  Expect 6 rows,
    #  N1                    C2  C3  C4
    #  --------------------  --  --  --------
    #
    #                 -2789  DA  EA         ?
    #                 -2389  BA  AA  AA
    #                     ?   ?  BA  BA
    #                     ?   ?  DA  DA
    #                 -3552  BA  AA  AA
    #                 -4344  AA  BA  BA
    stmt = """select * from V5fixed 
order by 1, 3 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s0')
    stmt = """select count(*) from V5fixed ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s1')
    #    select * from T5fixed ;
    stmt = """select count(*) from T5fixed ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s2')
    stmt = """select CHAR5_N20, CHAR6_N100, CHAR7_500, CHAR12_N2000
, CHAR15_100, CHAR16_N20
from T5fixed 
order by 1, 3 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s3')
    #
    #  Expect ( AA )
    stmt = """select * from (select min(c4) from V5fixed) dt ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s4')
    #
    # ---------------------------
    #      Id: IN.041      INSERT INTO <table> SELECT that contains CASE
    # ---------------------------
    #
    stmt = """insert into TAB4 (vc7) select
-- Simple CASE:
CASE count(*) WHEN 1 THEN 'Value A'
WHEN 2 THEN 'Value B'
WHEN 3 THEN 'Value C'
ELSE 'Value D'
END
from T5fixed 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #  Expect ( 'Value D' )
    stmt = """select * from TAB4 order by 1,2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s5')
    #
    stmt = """insert into TAB4 (vc9) select
-- Searched CASE:
CASE when CHAR7_500 = 'DAAAGAAA' then lower( CHAR7_500 )
when CHAR7_500 < 'EGAAGAAA' then CHAR7_500
else 'out of it'
END
from T5fixed 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 6)
    #  Expect the addition of 11 rows, with one row lower case and
    #  one row with the explicit text literal shown above.
    stmt = """select * from TAB4 order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s6')
    #
    stmt = """select  cast (sum(a) as char(9) )
from ( select SBIN0_UNIQ from T5fixed 
) dt(a)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s7')
    stmt = """select cast (sum(a) as char(9) )
from ( select SBIN0_UNIQ from T5fixed 
--  Searched CASE in predicate:
where 0 < CASE
when CHAR7_500 < 'EGAAGAAA' then 1
when CHAR7_500 = 'DAAAGAAA' then 100
else 10000
end
) dt(a)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s8')
    stmt = """insert into TAB4 (vc9)
select cast (sum(a) as char(9) )
from ( select SBIN0_UNIQ from T5fixed 
-- Searched CASE in predicate:
where 0 < CASE
when CHAR7_500 < 'EGAAGAAA' then 1
when CHAR7_500 = 'DAAAGAAA' then 100
else 10000
end
) dt(a)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #
    #  ---------------------------
    #       Id: IN.043      INSERT INTO <table> SELECT that contains NATURAL JOIN.
    #  ---------------------------
    #
    stmt = """select * from V5fixed natural join V5fixed v
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s9')
    #
    stmt = """insert into TAB4 
select c2, c3, c4, c2 from V5fixed natural join V5fixed v;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 3)
    #
    stmt = """select * from TAB4 order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s10')
    stmt = """delete from TAB4 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 11)
    #
    #  ---------------------------
    #       Id: IN.044      INSERT INTO <table> SELECT that contains RIGHT JOIN.
    #  ---------------------------
    #
    stmt = """select
sbin0_uniq    ,
sbin2_nuniq   ,
sbin6_nuniq   ,
sdec9_uniq    ,
char10_nuniq  ,
udec10_uniq   ,
char11_uniq   ,
sbinneg15_nuniq ,
sdec16_uniq   ,
sbin17_uniq   ,
sdec17_nuniq
from T5fixed 
order by 1, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s11')
    stmt = """select * from V5fixed 
natural join V5fixed v
order by 1, 3 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s12')
    #
    stmt = """select c2, c3, c4, c2 from V5fixed v1
natural right outer join V5fixed v2
where c2 is not null
order by 1, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s13')
    stmt = """insert into TAB4 (vc9)
select c2 from V5fixed v1
natural right outer join V5fixed v2
where c2 is not null
group by c2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 3)
    stmt = """select * from TAB4 order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s14')
    #
    stmt = """insert into TAB4 (vc9, vc7)
select v1.c2, v2.c2 from V5fixed v1
right outer join V5fixed v2
on v1.c2 is not null and v1.c3=v2.c3
where v1.c2 is not null
group by v1.c2, v2.c2, v1.c3, v2.c3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 4)
    #
    stmt = """select * from TAB4 order by vc9, vc7 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s15')
    stmt = """delete from TAB4 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 7)
    
    _testmgr.testcase_end(desc)

def test004(desc="""a04"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     T1107:A04
    #  Description:        This test verifies the SQL INSERT and
    #                      UPDATE features.
    #
    #
    # =================== End Test Case Header  ===================
    #
    #
    # To start with empty objects, clean up what this testcase uses;
    # should be 0 rows (i.e. empty already).
    
    stmt = """delete from TAB1;"""
    output = _dci.cmdexec(stmt)
    stmt = """delete from TAB4;"""
    output = _dci.cmdexec(stmt)
    
    #  Expect 6 rows,
    #  N1                    C2  C3  C4
    #  --------------------  --  --  --------
    #
    #                 -4344  AA  BA  BA
    #                 -3552  BA  AA  AA
    #                 -2789  DA  EA         ?
    #                 -2389  BA  AA  AA
    #                     ?   ?  BA  BA
    #                     ?   ?  DA  DA
    stmt = """select * from V5fixed order by 2, 1, 3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s0')
    #  Expect ( (DA ) ( EA ) ( AA ) ( DA ) )
    stmt = """select max(c2), max(c3), min(c4), max(c4)
from V5fixed ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s1')
    #  Expect ( DDAAAAAAA )
    stmt = """select CHAR5_N20, CHAR6_N100, CHAR7_500
, CHAR12_N2000, CHAR15_100, CHAR16_N20
from T5fixed ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s2')
    stmt = """select max(CHAR5_N20) from T5fixed ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s3')
    stmt = """select CHAR5_N20 from T5fixed ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s4')
    #
    # ---------------------------
    #      Id: UP.001      UPDATE one row, one column with literals.
    # ---------------------------
    stmt = """insert into TAB1 VALUES ('a') ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """select * from TAB1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s5')
    stmt = """update TAB1 SET vc = 'BigString' ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select * from TAB1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s6')
    stmt = """update TAB1 SET vc = 'Short' ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select * from TAB1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s7')
    #
    # ---------------------------
    #      Id: UP.002      UPDATE one row, one column with result of subquery.
    #			UPDATE <table name> SET <column name> = <subquery>
    # ---------------------------
    stmt = """update TAB1 
SET vc = ( select max(c4) from V5fixed )
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    #  Expect ( (DA) )
    stmt = """select * from TAB1 order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s8')
    stmt = """delete from TAB1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    #
    # ---------------------------
    #      Id: UP.003      UPDATE one-row table, many columns with literals.
    # ---------------------------
    #
    stmt = """insert into TAB4 VALUES ('a1', 'b1', 'c1', 'd1') ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """update TAB4 
SET vc9 = ( 'zodiac') , vc7 = 'yakhead'
, vc5 = 'xrays' , vc3 = 'vex'
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select * from TAB4 order by 1, 2  ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s9')
    #
    # ---------------------------
    #      Id: UP.004      UPDATE one-row table, many columns with results of subqueries.
    # ---------------------------
    #
    stmt = """update TAB4 
SET vc9 = (select max(c4) from V5fixed)
, vc3 = (select min(c4) from V5fixed)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select * from TAB4 order by 1, 2  ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s10')
    stmt = """delete from TAB4 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    #
    # ---------------------------
    #      Id: UP.005      UPDATE one many-column row of several, with literals.
    # ---------------------------
    #
    stmt = """insert into TAB4 VALUES ('a1', 'b1', 'c1', 'd1'),
('a2', 'b2', 'c2', 'd2'),
('a3', 'b3', 'c3', 'd3'),
('a4', 'b4', 'c4', 'd4'),
('a5', 'b5', 'c5', 'd5')
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 5)
    stmt = """select * from TAB4 order by 1, 2  ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s11')
    stmt = """update TAB4 
SET vc9 = ( 'change1') , vc7 = 'change2' where vc3 = 'd1'
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """update TAB4 
SET vc9 = ( 'change3') , vc5 =  NULL     where vc3 = 'd2'
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select * from TAB4 order by 1, 2  ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s12')
    stmt = """update TAB4 SET
vc9 = (select max(c4) from V5fixed),
vc7 = vc7 ,
vc5 = NULL
where vc3 = 'd3'
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select * from TAB4 order by 1, 2  ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s13')
    #
    # ---------------------------
    #      Id: UP.006      UPDATE one many-column row of several, with subqueries.
    # ---------------------------
    #
    stmt = """update TAB4 SET vc5 =  NULL ,
vc9 = (select max(c4) from V5fixed),
vc7 = 'change5'
where vc3 = 'd3'
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select * from TAB4 order by 1, 2  ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s14')
    stmt = """update TAB4 
SET vc9 = (select max(c4) from V5fixed),
vc7 = 'change6',
vc5 = NULL,
vc3 = (select min(c4) from V5fixed)
where vc3 = 'd4'
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select * from TAB4 order by 1, 2  ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s15')
    #
    stmt = """update TAB4 
SET vc9 = (select max(c4) from V5fixed)
, vc7 = 'change7'
where vc3 = 'd5'
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select * from TAB4 order by 1, 2  ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s16')
    #
    stmt = """update TAB4 
SET vc5 =(select max(c4) from V5fixed)
, vc3 = (select max(c4) from V5fixed)
where vc3 = 'd5'
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select * from TAB4 order by 1, 2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s17')
    stmt = """delete from TAB4 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 5)
    
    _testmgr.testcase_end(desc)

def test005(desc="""a05"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     T1107:A05
    #  Description:        This test verifies the SQL INSERT and
    #                      UPDATE features.
    #
    # =================== End Test Case Header  ===================
    #
    #
    stmt = """Set Warnings Off ;"""
    output = _dci.cmdexec(stmt)
    #
    # To start with empty objects, clean up what this testcase uses;
    # should be 0 rows (i.e. empty already).
    
    stmt = """delete from TAB1;"""
    output = _dci.cmdexec(stmt)
    stmt = """delete from TAB4;"""
    output = _dci.cmdexec(stmt)
    
    # Make explicit the Autocommit ON.
    stmt = """Set Transaction Autocommit On;"""
    output = _dci.cmdexec(stmt)
    #
    #  Expect 6 rows,
    #  N1                    C2  C3  C4
    #  --------------------  --  --  --------
    #
    #                 -4344  AA  BA  BA
    #                 -3552  BA  AA  AA
    #                 -2389  BA  AA  AA
    #                 -2789  DA  EA         ?
    #                     ?   ?  BA  BA
    #                     ?   ?  DA  DA
    stmt = """select * from V5fixed order by 2, 1, 3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s0')
    #
    #  Expect ( (DA ) ( EA ) ( AA ) ( DA ) )
    stmt = """select max(c2), max(c3), min(c4), max(c4)
from V5fixed order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s1')
    #
    #  Expect ( DAAAAAAA )
    stmt = """select max(CHAR5_N20) from T5fixed ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s2')
    stmt = """select CHAR5_N20 from T5fixed order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s3')
    #
    # ---------------------------
    # UPDATE of many columns.
    # ---------------------------
    #      Id: UP.011       UPDATE of many rows, 1 column; UPDATE allows <value
    #			expression> to be a <subquery> when specified in:
    #			<set clause> ::= <column name> = <value expression>
    #			within: <update statement: searched>
    #			::= UPDATE <table name> SET  <set clause> [ ,... ]
    #			UPDATE tabmanyrows SET c = (SELECT colx FROM t)
    # ---------------------------
    # Rows are deleted from TAB1 in pretestxxx;
    stmt = """insert into TAB1 VALUES ('a'), ('b'), ('c'), ('d'), ('e') ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 5)
    stmt = """insert into TAB1 VALUES ('f'), ('g'), ('h'), ('i'), ('j') ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 5)
    stmt = """insert into TAB1 VALUES ('k'), ('l'), ('m'), ('n'), ('o') ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 5)
    #  Expect ('a' to 'o').
    stmt = """select * from TAB1 order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s4')
    #
    stmt = """update TAB1 
SET vc = ( select max(c4) from V5fixed )
where vc in ('b', 'c', 'g', 'm')
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 4)
    stmt = """update TAB1 
SET vc = ( select min(c4) from V5fixed )
where vc between 'j' and 'l'
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 3)
    #  Expect ((AA) (AA) (AA) (DA) (DA) (DA) (DA) (a) (d) (e) (f) (h) (i) (n) (o))
    stmt = """select * from TAB1 order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s5')
    #
    stmt = """delete from TAB1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 15)
    #
    stmt = """insert into TAB4 VALUES ('a1', 'b1', 'c1', 'd1'),
('a2', 'b2', 'c2', 'd2'),
('a3', 'b3', 'c3', 'd3'),
('a4', 'b4', 'c4', 'd4')
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 4)
    stmt = """UPDATE TAB4 
SET vc7 = (SELECT MAX(c2) FROM V5fixed) ||
(SELECT MAX(c3) FROM V5fixed)
where vc9 between 'a2' and 'a4'
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 3)
    #  Expect (('a1', 'b1', 'c1', 'd1') ('a2', 'DAEA', 'c2', 'd2')
    #          ('a3', 'DAEA', 'c3', 'd3') ('a4', 'DAEA', 'c4', 'd4'))
    stmt = """select * from TAB4 order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s6')
    #
    stmt = """delete from TAB4 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 4)
    #
    # ---------------------------
    #      Id: UP.012       UPDATE many rows, many columns:
    #                       Take values from 1-row table.
    # ---------------------------
    #
    stmt = """set param ?param1 'param one' ;"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into TAB1 VALUES ('j') ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into TAB4 VALUES ('a1', 'b1', 'c1', 'd1'),
('a2', 'b2', 'c2', 'd2'),
('a3', 'b3', 'c3', 'd3'),
('a4', 'b4', 'c4', 'd4')
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 4)
    #
    # To allow us to use these results then roll back to them:
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    # Expect 4* ( 'param one', 'j', 'param', 'j')
    # 05/29/09 For NCI, When your query is prepared, the types and max lengths for each parameter
    #  are sent to the client.  NDCS creates a network buffer format based on this information
    # and the max lengths for the parameters can not be extended.
    # following cast(?param1 as char(5)) will fail in NCI, modified the query to cast to longer
    # length
    stmt = """UPDATE TAB4 
SET vc7 = (SELECT cast( vc as char(7) ) FROM TAB1)
--     , vc5 = cast( ?param1 as char(5) )
, vc5 = cast( cast(?param1 as char(9) ) as char(5))
, vc3 = (SELECT cast( vc as char(3) ) FROM TAB1)
, vc9 = cast( ?param1 as char(9) )
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 4)
    stmt = """select * from TAB4 order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s7')
    stmt = """rollback work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    stmt = """set param ?param1 'par one' ;"""
    output = _dci.cmdexec(stmt)
    # To allow us to use these results then roll back to them:
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    # Expect 4* ( 'par one', 'j', 'par o', 'j')
    stmt = """UPDATE TAB4 
SET vc7 = (SELECT cast( vc as char(7) ) FROM TAB1)
, vc9 = cast( ?param1 as char(9) )
, vc3 = (SELECT cast( vc as char(3) ) FROM TAB1)
, vc5 = cast( ?param1 as char(5) )
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 4)
    stmt = """select * from TAB4 order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s8')
    stmt = """rollback work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """select vc9, ?param1
From TAB4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s9')
    stmt = """select vc9, cast(cast( ?param1 as char(9) ) as char(2))
From TAB4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s10')
    stmt = """UPDATE TAB4 
--   SET vc9 = cast( ?param1 as char(2) )
SET vc9 = cast( cast(?param1 as char(9)) as char(2) )
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 4)
    stmt = """select * from TAB4 order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s11')
    stmt = """rollback work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """UPDATE TAB4 
SET vc5 = cast(cast( ?param1 as char(10) ) as char(2))
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 4)
    stmt = """select * from TAB4 order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s12')
    stmt = """rollback work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    # ---------------------------
    #      Id: UP.013       UPDATE many rows, many columns:
    #   	                   Aggregates of values from multi-row table.
    #                       Switch column names in AS clause, e.g.:
    #          UPDATE tabmanyrow SET (a,b,c) =
    #	      (SELECT MIN(cx) as a FROM t2
    #        ,  SELECT AVG(cx) as c FROM t2
    #        ,  SELECT MAX(cx) as b FROM t2);
    # ---------------------------
    #
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """select * from TAB4 order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s13')
    stmt = """UPDATE TAB4 
SET vc7 = (SELECT MAX(c2) FROM V5fixed) ||
(SELECT MAX(c3) FROM V5fixed)
, vc9 = 'change6'
, vc5 = NULL
--     , vc3 = cast( ?param1 as char(3) )
, vc3 = cast( cast(?param1 as char(9)) as char(3) )
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 4)
    #  Expect 4* ( 'change6', 'DAEA', NULL, 'par' )
    stmt = """select * from TAB4 order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s14')
    #
    stmt = """set param ?param1 'third value' ;"""
    output = _dci.cmdexec(stmt)
    stmt = """UPDATE TAB4 
SET vc7 = (SELECT MAX(c2) FROM V5fixed) ||
(SELECT MAX(c3) FROM V5fixed)
, vc9 = 'change6'
, vc5 = NULL
--     , vc3 = cast( ?param1 as char(3) )
, vc3 = cast( cast(?param1 as char(11)) as char(3) )
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 4)
    #  Expect 4* ( 'change6', 'DAEA', NULL, 'thi' )
    stmt = """select * from TAB4 order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s15')
    #
    stmt = """update TAB4 
SET vc9 = (select max(c2) from V5fixed)
, vc7 = (select max(c3) from V5fixed)
, vc5 = (select max(c4) from V5fixed)
, vc3 = (select min(c4) from V5fixed)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 4)
    #  Expect 4* ( 'DA', 'EA', 'DA', 'AA' )
    stmt = """select * from TAB4 order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s16')
    #
    # Commit the system transaction; then make transactions, and
    # roll them back
    stmt = """commit work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    stmt = """select * from TAB4 order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s17')
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """update TAB4 
SET vc9 = (select max(c4) from V5fixed)
, vc3 = (select min(c4) from V5fixed)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 4)
    #  Expect 4* ( 'DA', 'EA', 'DA', 'AA' )
    stmt = """select * from TAB4 order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s18')
    stmt = """rollback work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    # Use column without nulls from view.
    stmt = """update TAB4 
SET vc9 = (select max(c3) from V5fixed)
, vc3 = (select min(c3)||'.' from V5fixed)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 4)
    #  Expect 4* ( 'EA', 'EA', 'DA', 'AA.' )
    stmt = """select * from TAB4 order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s19')
    stmt = """rollback work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    # Use column without nulls from base table.
    stmt = """update TAB4 
SET vc9 = (select max(CHAR5_N20) from T5fixed)
, vc3 = (select cast( max( CHAR5_N20) as char(3) ) from T5fixed)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 4)
    #  Expect 4* ( 'DAAAAAAA', 'EA', 'DA', 'DAA' )
    stmt = """select * from TAB4 order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s20')
    stmt = """rollback work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """update TAB4 
SET vc9 = (select max(c4)||' x' from V5fixed)
, vc7 = (select min(c4)||' n' from V5fixed)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 4)
    #  Expect 4* ( 'DA       x', 'AA       n', 'DA', 'AA' )
    stmt = """select * from TAB4 order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s21')
    stmt = """rollback work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """update TAB4 
SET vc9 = (select max(c4)||' X' from V5fixed)
, vc5 = (select min(c4) from V5fixed)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 4)
    #  Expect 4* ( 'DA X', 'EA', 'AA', 'AA' )
    stmt = """select * from TAB4 order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s22')
    stmt = """rollback work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """update TAB4 
SET vc9 = (select max(c4) from V5fixed)
, vc5 = NULL
, vc3 = (select min(c4) from V5fixed)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 4)
    #  Expect 4* ( 'DA', 'EA', NULL, 'AA' )
    stmt = """select * from TAB4 order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s23')
    stmt = """rollback work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #  Expect original values, 4* ( 'DA', 'EA', 'DA', 'AA' )
    stmt = """select * from TAB4 order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s24')
    stmt = """update TAB4 
SET vc9 = (select max(c4) from V5fixed)
, vc7 = 'change6'
, vc3 = (select min(c4) from V5fixed)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 4)
    #  Expect 4* ( 'DA', 'change6', 'DA', 'AA' )
    stmt = """select * from TAB4 order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s25')
    stmt = """rollback work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    stmt = """update TAB4 
SET vc9 = (select max(c4) from V5fixed)
, vc7 = 'change6'
, vc5 = NULL
, vc3 = (select min(c4) from V5fixed)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 4)
    #  Expect 4* ( 'DA', 'change6', NULL, 'AA' )
    stmt = """select * from TAB4 order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s26')
    #
    # Cleanup at end.
    #
    stmt = """delete from TAB4 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 4)
    
    _testmgr.testcase_end(desc)

def test006(desc="""a06"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     T1107:A06
    #  Description:        This test verifies the SQL INSERT and
    #                      UPDATE features.
    #
    # =================== End Test Case Header  ===================
    #
    #
    # To start with empty objects, clean up what this testcase uses;
    # should be 0 rows (i.e. empty already).
    
    stmt = """delete from TAB4;"""
    output = _dci.cmdexec(stmt)
    
    # Specify the same value as the first-release default.
    stmt = """set transaction autocommit on;"""
    output = _dci.cmdexec(stmt)
    #
    #  Expect 6 rows.
    stmt = """select CHAR5_N20 from T5fixed order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s0')
    #
    #  Expect 6 rows,
    #  N1                    C2  C3  C4
    #  --------------------  --  --  --------
    #
    #                 -4344  AA  BA  BA
    #                 -3552  BA  AA  AA
    #                 -2389  BA  AA  AA
    #                 -2789  DA  EA         ?
    #                     ?   ?  BA  BA
    #                     ?   ?  DA  DA
    stmt = """select * from V5fixed order by 2,1, 3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s1')
    #
    stmt = """set transaction autocommit on;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?pa 'AA' ;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p2 'd2' ;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p4 'd4' ;"""
    output = _dci.cmdexec(stmt)
    #
    #  Expect ( ('DA' ) ( 'EA' ) ( 'AA' ) ( 'DA' ) )
    stmt = """select max(c2), max(c3), min(c4), max(c4)
from V5fixed ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s2')
    #
    #  Expect ( ('BA' ) )
    stmt = """select min(c3) from V5fixed 
where not ( c3 = ?pa ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s3')
    #
    #  Expect ( 'DAAAAAAA' )
    stmt = """select max(CHAR5_N20) from T5fixed ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s4')
    #
    # ---------------------------
    # UPDATE of many columns.
    # ---------------------------
    #      Id: UP.041      UPDATE with same items in WHERE and update expressions;
    #                      WHERE <search condition> uses names of params,
    #                      columns, and literals that also appear in subquery
    #                      within <value expression> of <update source>
    # ---------------------------
    stmt = """set transaction autocommit off;"""
    output = _dci.cmdexec(stmt)
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    # Transaction is started so that it can be committed.
    stmt = """insert into TAB4 VALUES ('a1', 'b1', 'c1', 'd1'),
('a2', 'b2', 'c2', 'd2'),
('a3', 'b3', 'c3', 'd3'),
('a4', 'b4', 'c4', 'd4')
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 4)
    stmt = """select * from TAB4 order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s5')
    # Commit the Inserts.
    stmt = """commit work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    # Start new transaction so can rollback updates.
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    # Expect update in 3 rows.
    stmt = """UPDATE TAB4 SET vc7 = 'X3'
where vc3 between 'd1' and 'd3' ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 3)
    stmt = """select * from TAB4 order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s6')
    #
    # Expect update in 3 rows.
    stmt = """UPDATE TAB4 SET vc5 = ?p2||?p4
where vc3 between ?p2 and ?p4 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 3)
    stmt = """select * from TAB4 order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s7')
    #
    # Roll back the updates.
    stmt = """rollback work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    # Start new transaction so can rollback more updates.
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """select min(c3) from V5fixed 
where not ( c3 = 'ZA' );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s8')
    stmt = """UPDATE TAB4 
SET vc5 = 'ZA' || ' ' || (
select min(c3) from V5fixed where not ( c3 = 'ZA' )
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 4)
    stmt = """select * from TAB4 order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s9')
    stmt = """select min(c3) from V5fixed 
where not ( c3 = ?pa );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s10')
    stmt = """UPDATE TAB4 
SET vc7 = ?pa || ' ' || (
select min(c3) from V5fixed where not ( c3 = ?pa )
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 4)
    stmt = """select * from TAB4 order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s12')
    stmt = """rollback work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    # Now use autocommit.
    stmt = """set transaction autocommit on;"""
    output = _dci.cmdexec(stmt)
    stmt = """select min(vc3) from TAB4 where not ( vc3 > ?p2 ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s13')
    
    stmt = """UPDATE TAB4 
SET vc3 = (
select min(vc3) from TAB4 where not ( vc3 > ?p2 )
)
where vc3 = ?p2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select * from TAB4 order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s14')
    #
    stmt = """update TAB4 
SET vc9 = (select max(c4) from V5fixed)
, vc7 = 'change6'
, vc5 = NULL
, vc3 = (select min(c4) from V5fixed)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 4)
    stmt = """select * from TAB4 order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s15')
    #
    # Cleanup at end.
    #
    stmt = """delete from TAB4 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 4)
    
    #  07/12/00 EL  Added following queries to test the outer reference causing
    #               internal error.
    
    stmt = """insert into TAB4  (vc9, vc5)
select c2,c4 from V5fixed 
union all
select c3,c4 from V5fixed 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 12)
    
    stmt = """update TAB4 set vc9 = (select max(c4) from V5fixed where TAB4.vc9 <> c3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 12)
    
    stmt = """update TAB4 set vc9 = (select max(c4) from V5fixed where vc9 <> c3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 12)
    
    stmt = """select * from TAB4 order by vc9;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s18')
    
    stmt = """update TAB4 set vc9 = (select max(c4) from V5fixed where 'EA' = TAB4.vc9);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 12)
    
    stmt = """update TAB4 set vc9 = (select max(c4) from V5fixed where 'EA' = vc9);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 12)
    
    stmt = """update TAB4 set vc9 = (select max(c4) from V5fixed 
where TAB4.vc9 <> V5fixed.c3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 12)
    
    stmt = """select * from TAB4 order by vc9;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s22')
    
    _testmgr.testcase_end(desc)

def test007(desc="""a07"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     T1107:A07
    #  Description:        This test verifies the SQL INSERT and
    #                      UPDATE features with subquery in more
    #                      places
    #
    # =================== End Test Case Header  ===================
    #
    #
    # To start with empty objects, clean up what this testcase uses;
    # should be 0 rows (i.e. empty already).
    
    stmt = """delete from TAB4;"""
    output = _dci.cmdexec(stmt)
    
    #  Expect 6 rows,
    #  N1                    C2  C3  C4
    #  --------------------  --  --  --------
    #
    #                 -4344  AA  BA  BA
    #                 -3552  BA  AA  AA
    #                 -2789  DA  EA         ?
    #                 -2389  BA  AA  AA
    #                     ?   ?  BA  BA
    #                     ?   ?  DA  DA
    #
    stmt = """select * from V5fixed order by 1, 2, 3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s0')
    #
    # ---------------------------
    # Test OR.061 for Orthogonality moved to 1107:B07
    #             because of memory access error with 970927 build.
    # ---------------------------
    #
    # ---------------------------
    #      Id: OR.062      Orthogonality: allow row subqueries to appear almost anywhere, e.g.:
    #			select (select a from t) + c from t
    #			where (select b from t) > 2 * (select (select c from t) from t);
    # ---------------------------
    #
    stmt = """delete from TAB4 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 0)
    #
    #  Expect ( 'EA'  -2389  -4344 )
    stmt = """select max(c3), max(n1), min(n1) from V5fixed ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s1')
    #
    #  Expect ( ('EA test orthog') )
    stmt = """select distinct
(select max(c3) from V5fixed) ||
' test orthog' from V5fixed 
where (select max(n1) from V5fixed ) <>
2 * (select min(n1) from V5fixed )
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s2')
    #
    stmt = """insert into TAB4 ( vc9 ) (
select distinct
(select max(c3) from V5fixed) || ' test o'
from V5fixed 
where (select max(n1) from V5fixed) <>
2 * (select min(n1) from V5fixed)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #
    stmt = """insert into TAB4 ( vc9 ) (
select distinct
cast(
( (select max(c3) from V5fixed)||' test orthog' )
as varchar(10))
from V5fixed 
where (select max(n1) from V5fixed) <>
2 * (select min(n1) from V5fixed)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #
    #  Expect 2 rows: ( ('EA test o') ('EA test or') )
    stmt = """select vc9 from TAB4 order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s3')
    #
    #  Expect 6 rows of: ('EA test orthog')
    stmt = """select (select max(c3) from V5fixed) ||
' test orthog' from V5fixed 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s4')
    #  Expect ( ('AA') )
    stmt = """select min(c4) from V5fixed 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s5')
    # Expect 0 rows.
    stmt = """select
(select max(c3) from V5fixed) ||
' test orthog' from V5fixed 
where (select max(c3) from V5fixed ) =
'A' || (select min(c4) from V5fixed )
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    #
    # Cleanup at end.
    #
    stmt = """delete from TAB4 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 2)
    
    _testmgr.testcase_end(desc)

def test008(desc="""a08"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     T1107:A08
    #  Description:        This test verifies the SQL INSERT and
    #                      UPDATE features, specifically DEFAULT.
    #
    # =================== End Test Case Header  ===================
    #
    #
    # To start with empty objects, clean up what this testcase uses;
    # should be 0 rows (i.e. empty already).
    
    stmt = """delete from TAB4;"""
    output = _dci.cmdexec(stmt)
    
    # ---------------------------
    #      Id: IN.023      Insert DEFAULT VALUES; table has many (over 50) columns
    #      Id: IN.026      Insert DEFAULT VALUES; many data types
    #      Id: IN.028      VALUES clause includes simple elements and one subquery.
    #      Id: IN.029      VALUES clause includes simple elements and multiple subqueries.
    #      Id: RV.003      RVC: Insert many (~25) expression.
    # Also:
    #      Id: UP.022      Update with DEFAULT VALUES; table has many (over 50) columns
    #      Id: UP.028      Update with DEFAULT VALUES; many data types
    # ---------------------------
    stmt = """Create Table TABTEMP 
(
char0_n10           Char(2)      default 'AD'
-- heading 'char0_n10 with default AD'
,
sbin0_uniq          Smallint     default 0 not null,
sdec0_n500          Numeric(18,0) default 0 ,    

ubin1_n2            Numeric(4,0) unsigned default 1 ,
udec1_100           Numeric(2,0) unsigned default 1 not null ,    

char2_2             VarChar(2)   default 'b',
sbin2_nuniq         Largeint     default 2 ,
sdec2_500           Numeric(9,0) signed default 2,    

udec3_n100          Numeric(9,0) unsigned default 3 ,
ubin3_n2000         Numeric(4,0) unsigned default 3 ,
char3_4             Char(8)      default 'not null' not null ,    

sdec4_n20           Numeric(4,0) default 4 ,
sbin4_n1000         Smallint     default 4 ,
char4_n10           Char(8)      default 'd' ,    

char5_n20           VarChar(8)   default 'e' ,
sdec5_10            Numeric(9,0) signed default 5 not null ,
ubin5_n500          Numeric(9,0) unsigned default 5 ,    

sbin6_nuniq         Largeint     default 6 ,
sdec6_4             Numeric(4,0) signed default 6 not null ,
char6_n100          Char(8)      default 'f' ,    

sbin7_n20           Smallint     default 7 ,
char7_500           Char(8)      default 'g' not null ,
udec7_n10           Numeric(4,0) unsigned default 7 ,    

ubin8_10            Numeric(4,0) unsigned default 81 not null ,
char8_n1000         Char(8)                ,
sdec8_4             Numeric(9,0) unsigned default 82 not null ,    

sdec9_uniq          Numeric(18,0) signed  default 9 not null ,
char9_100           Char(2)               default 'i' not null ,
ubin9_n4            Numeric(9,0) unsigned  ,    

ubin10_n2           Numeric(4,0) unsigned  ,
char10_nuniq        Char(8)                ,
udec10_uniq         Numeric(9,0) unsigned default 10 not null ,    

udec11_2000         Numeric(9,0) unsigned default 111 not null ,
sbin11_100          Integer               default 112 not null ,
char11_uniq         Char(8)      default 'k' not null ,    

ubin12_2            Numeric(4,0) unsigned default 12 not null ,
sdec12_n1000        Numeric(18,0) signed  ,
char12_n2000        Char(8)   ,    

udec13_500          Numeric(9,0) unsigned default 131 not null ,
char13_1000         Char(8)               default 'm' not null ,    

sbin14_1000         Integer               default 141 not null ,
udec14_100          Numeric(4,0) unsigned default 142 not null ,
char14_n500         Char(8)               ,    

sbinneg15_nuniq     Largeint              ,
sdecneg15_100       Numeric(9,0) signed   default 151 not null ,
char15_100          Char(8)               default 'o' not null ,    

ubin16_n10          Numeric(4,0) unsigned  ,
sdec16_uniq         Numeric(18,0) signed  default 16 not null ,
char16_n20          Char(5)  ,    

sbin17_uniq         Largeint              default 17 not null ,
sdec17_nuniq        Numeric(18,0)  ,
char17_2            Char(8)               default 'q' not null
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # 980813Beta2 supports "STORE BY store-option" which:
    # specifies the order of rows within the physical file that holds
    # the table and determines the physical organization of the table
    # and the ways you can partition the table. The storage key is sometimes
    # referred to as the clustering key. "store-option" can be:
    #
    #    PRIMARY KEY         stores rows by value of primary key; allows
    # partitioning by primary key.
    #
    #    key-column-list     stores rows by value of key columns; allows
    # partitioning by key columns. A SYSKEY is appended
    # automatically to ensure uniqueness of the clustering key.
    #
    # Insert
    #
    # Insert into empty table.
    stmt = """insert into TABTEMP DEFAULT VALUES ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """select sbin0_uniq, char0_n10 , char2_2 , sbin4_n1000 , sbin14_1000
from TABTEMP order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s0')
    #
    # Expect 1 row.
    stmt = """Insert Into TABTEMP 
Values (
NULL , -- char0_n10, check column values
-200, -266,
NULL , 60,
'AA', --  char2_2, check column values
-3766, -266,
44, 344, 'BA',
-9, -509, -- sbin4_n1000, check column values
NULL ,
'AAAAAAAA', -0, 60, -3766, -2,
'CQAAAAAA', -4,
'EAAAGAAA',  NULL , 9,
'DBAAAAAA',  1, -60,
'AK',  NULL  ,  NULL  ,
'AEAAJAAB', 3766, 344, -44,
'EKAACAAE', 1, -509,
'DBAAAAAB', 60,
'EFAAIAAA',
-766, -- sbin14_1000
66, 'AGAAEAAA',
-4344, -44, 'ATAAAAAA',
NULL  , -2509,'BE   ',
-37055, -60, 'AAAAAAAA'
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #
    stmt = """Insert Into TABTEMP ( sbin0_uniq, char0_n10, char2_2
, sbin4_n1000, sbin14_1000 )
VALUES ( 1, 'hu', 'ry', 123, 4567)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """Insert Into TABTEMP 
Values (
'0a' , -- char0_n10, check column values
200, -266,
NULL , 60,
'2b', --  char2_2, check column values
-3766, -266,
44, 344, 'BA',
-9, 137, -- sbin4_n1000, check column values
NULL ,
'AAAAAAAA', -0, 60, -3766, -2,
'CQAAAAAA', -4,
'EAAAGAAA',  NULL , 9,
'DBAAAAAA',  1, -60,
'AK',  NULL  ,  NULL  ,
'AEAAJAAB', 3766, 344, -44,
'EKAACAAE', 1, -509,
'DBAAAAAB', 60,
'EFAAIAAA',
-137, -- sbin14_1000
66, 'AGAAEAAA',
-4344, -44, 'ATAAAAAA',
NULL  , -2509,'BE   ',
-37055, -60, 'AAAAAAAA'
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #  Expect 4 rows.
    stmt = """select sbin0_uniq, char0_n10 , char2_2 , sbin4_n1000
, sbin14_1000, sdec6_4
from TABTEMP order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s1')
    #
    stmt = """insert into TAB4 values
('01vc9', '01vc7', '01vc5', 'vc3')
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into TAB4 values
('vc9.2', 'vc7.2', 'vc5.2', '3.2')
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into TAB4 values
('03vc9', '03vc7', '03vc5', '3.3')
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """select * from TAB4 order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s2')
    #
    # Without setting warnings off, we get unwanted warnings here.
    stmt = """SET WARNINGS OFF;"""
    output = _dci.cmdexec(stmt)
    stmt = """select 3
, cast( vc9 as varchar(2) )
, cast( vc7 as char(2) )
from TAB4 
order by vc9
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s3')
    #
    stmt = """Insert INTO TABTEMP (sbin0_uniq, char0_n10 , char2_2)
( select 3
, cast( vc9 as varchar(2) )
, cast( vc7 as char(2) )
from TAB4 
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 3)
    #
    #  Expect 7 rows with 3 rows including defaults from last addition.
    stmt = """select sbin0_uniq, char0_n10 , char2_2 , sbin4_n1000
, sbin14_1000, sdec6_4
from TABTEMP order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s4')
    #
    stmt = """Insert INTO TABTEMP (sbin0_uniq, sbin4_n1000 , sbin14_1000)
(select 4, count(vc9), count(vc7) from TAB4)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #
    #  Expect 8 rows with 1 row from last addition.
    stmt = """select sbin0_uniq, char0_n10 , char2_2 , sbin4_n1000
, sbin14_1000, sdec6_4
from TABTEMP order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s5')

    stmt = """Insert INTO TABTEMP (sbin0_uniq,char0_n10,sdec0_n500)
values (2001
, (select cast(min(vc3) as char(2)) from TAB4)
, 3 )
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #
    #  Expect 9 rows with 1 row from last addition.
    stmt = """select sbin0_uniq, char0_n10 , char2_2 , sbin4_n1000
, sbin14_1000, sdec6_4
from TABTEMP order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s6')
    #
    stmt = """select min(vc3) as min_vc3
, max(vc3) as max_vc3
, min(vc5) as min_vc5
from TAB4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s7')
    stmt = """select min(vc7) as min_vc7
, max(vc7) as max_vc7
, min(vc9) as min_vc9
from TAB4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s8')
    stmt = """select vc9, vc7, vc5 from TAB4 where vc3='3.2' ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s9')
    stmt = """select vc9, vc7, vc5 from TAB4 where vc3='3.3' ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s10')
    #
    stmt = """Insert INTO TABTEMP 
(
char0_n10   ,
sbin0_uniq  ,
sdec0_n500  ,
ubin1_n2    ,
udec1_100   ,    

char2_2     ,
sbin2_nuniq ,
sdec2_500   ,
udec3_n100  ,
ubin3_n2000 ,    

char3_4     ,
sdec4_n20   ,
sbin4_n1000
)
values ( -- begin row value constructor.
(select Cast( min(vc3) as Char(2) ) from TAB4) , 1 , 2 , 3 , 4
,  (select Cast( max(vc3) as Char(2) ) from TAB4) , 5 , 6 , 7 , 8
,  (select vc7 from TAB4 where vc3='3.2' ) , 9 , 10
) -- end row value constructor.
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #
    #  Expect 10 rows with 1 row from last addition.
    stmt = """select sbin0_uniq, char0_n10 , char2_2 , sbin4_n1000
, sbin14_1000, sdec6_4
from TABTEMP order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s11')
    #
    stmt = """Insert INTO TABTEMP 
(
char0_n10   ,
sbin0_uniq  ,
sdec0_n500  ,
ubin1_n2    ,
udec1_100   ,    

char2_2     ,
sbin2_nuniq ,
sdec2_500   ,
udec3_n100  ,
ubin3_n2000 ,    

char3_4     ,
sdec4_n20   ,
sbin4_n1000 ,    

char4_n10   ,    

char5_n20   ,
sdec5_10    ,
ubin5_n500  ,
sbin6_nuniq ,
sdec6_4     ,    

char6_n100  ,
sbin7_n20   ,    

char7_500   ,
udec7_n10
)
values ( -- begin row value constructor.
(select Cast( vc5 as Char(2) ) from TAB4 where vc3='3.2' ) , 1 , 2 , 3 , 4
,  (select Cast( max(vc3) as Char(2) ) from TAB4) , 5 , 6 , 7 , 8
,  (select min(vc7) from TAB4) , 9 , 10
,  (select max(vc7) from TAB4)
,  (select min(vc7) from TAB4) , 11, 12, 13, 14
,  ( select vc7 from TAB4 where vc3='3.2' ) , 15
,  ( select vc7 from TAB4 where vc3='3.3' ) , 16
) -- end row value constructor.
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #
    #  Expect 11 rows with 1 row from last addition.
    stmt = """select sbin0_uniq, char0_n10 , char2_2 , sbin4_n1000
, sbin14_1000, sdec6_4
from TABTEMP order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s12')
    #
    stmt = """Insert INTO TABTEMP 
values ( -- begin row value constructor.
(select Cast( min(vc3) as Char(2) ) from TAB4) , 1 , 2 , 3 , 4
,  (select Cast( max(vc3) as Char(2) ) from TAB4) , 5 , 6 , 7 , 8
,  (select min(vc7) from TAB4) , 9 , 10
,  (select max(vc7) from TAB4)
,  (select min(vc7) from TAB4) , 11, 12, 13, 14
,  (select max(vc7) from TAB4) , 15
,  (select min(vc7) from TAB4) , 16, 17
,  (select max(vc7) from TAB4) , 18, 19
,  (select Cast( min(vc7) as Char(2) ) from TAB4) , 20, 21
,  (select max(vc7) from TAB4) , 22, 23, 24
,  (select min(vc7) from TAB4) , 25, 26
,  (select max(vc7) from TAB4) , 27
,  (select Cast( min(vc9) as Char(8) ) from TAB4) , 28, 29
,  (select min(vc7) from TAB4) , 30, 31
,  (select max(vc7) from TAB4) , 31, 32
,  (select min(vc5) from TAB4) , 33, 34
,  (select min(vc7) from TAB4)
) -- end row value constructor.
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #
    #  Expect 12 rows with 1 row from last addition.
    stmt = """select sbin0_uniq, char0_n10 , char2_2 , sbin4_n1000
, sbin14_1000, sdec6_4
from TABTEMP order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s13')
    #
    # Restore warnings.
    stmt = """SET WARNINGS OFF;"""
    output = _dci.cmdexec(stmt)
    #
    stmt = """select CHAR0_N10, SBIN0_UNIQ, SDEC0_N500
, UBIN1_N2, UDEC1_100, CHAR2_2
from TABTEMP order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s14')
    stmt = """select SBIN2_NUNIQ, SDEC2_500, UDEC3_N100
, UBIN3_N2000, CHAR3_4
from TABTEMP order by 1, CHAR3_4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s15')
    stmt = """select SDEC4_N20, SBIN4_N1000, CHAR4_N10
, CHAR5_N20, SDEC5_10, UBIN5_N500
from TABTEMP order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s16')
    stmt = """select CHAR16_N20, SBIN17_UNIQ, SDEC17_NUNIQ, CHAR17_2
from TABTEMP order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s17')
    #
    # Clean up.
    #
    stmt = """drop table TABTEMP ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """delete from TAB4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 3)
    
    _testmgr.testcase_end(desc)

def test009(desc="""a09"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     T1107:A09
    #  Description:        This test verifies the SQL INSERT and UPDATE
    #                      features with subquery in more places
    #
    # =================== End Test Case Header  ===================
    #
    
    # To start with empty objects, clean up what this testcase uses;
    # should be 0 rows (i.e. empty already).
    
    stmt = """delete from TAB4;"""
    output = _dci.cmdexec(stmt)
    
    #  Expect 6 rows,
    #  N1                    C2  C3  C4
    #  --------------------  --  --  --------
    #
    #                 -4344  AA  BA  BA
    #                 -3552  BA  AA  AA
    #                 -2789  DA  EA         ?
    #                 -2389  BA  AA  AA
    #                     ?   ?  BA  BA
    #                     ?   ?  DA  DA
    #
    stmt = """select * from V5fixed order by 1, 2, 3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s0')
    #
    #  Expect { AA}.
    stmt = """select * from (select min(c4) from V5fixed) dt ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s1')
    #
    #  ---------------------------
    #       Id: OR.061      Orthogonality: an element of an RVC can be a subquery that returns a single value, e.g.:
    #                       in comparison of RVC with query returning single row,
    #                       like (a,b)=Select y,z From ..
    #  ---------------------------
    #
    #  View:
    #  Expect ( AA BA EA )
    stmt = """select min(c2), 'BA', max(c3) from V5fixed ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s2')
    #
    #  Expect all rows from view as predicate is true.
    stmt = """select n1, c2, c3, c4 from V5fixed 
where ('AA')
= (select min(c2) from V5fixed)
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s3')
    #
    #  Expect all rows from view as predicate is true.
    stmt = """select n1, c2, c3, c4 from V5fixed 
where ('BA' )
= (select distinct 'BA' from V5fixed)
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s4')
    #
    #  Expect all rows from view as predicate is true.
    stmt = """select n1, c2, c3, c4 from V5fixed 
where ((select max(c3) from V5fixed) )
= (select max(c3) from V5fixed)
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s5')
    #
    #  Expect all rows from view as predicate is true.
    stmt = """select n1, c2, c3, c4 from V5fixed 
where ('AA', 'BA', (select max(c3) from V5fixed) )
= ((select min(c2), 'BA', max(c3) from V5fixed))
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s6')
    stmt = """select n1, c2, c3, c4 from V5fixed 
where ('AA', 'BA', 'EA')
= ('AA', 'BA', 'EA')
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s7')
    #
    stmt = """select n1, c2, c3, c4 from V5fixed 
where ('AA')
= ((select min(c2) from V5fixed))
and   ('BA')
= ('BA')
and   ((select max(c3) from V5fixed))
= ((select max(c3) from V5fixed))
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s8')
    #
    #  Insert those rows just displayed.
    stmt = """insert into TAB4(vc9 , vc7 , vc5 )
(
select c2, c3, c4 from V5fixed 
where ('AA', 'BA', (select max(c3) from V5fixed) )
= (( select min(c2), 'BA', max(c3) from V5fixed))
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 6)
    stmt = """insert into TAB4(vc9 , vc7 , vc5 )
(
select c2, c3, c4 from V5fixed 
where ('AA')
= ((select min(c2) from V5fixed))
and   ('BA')
= ('BA')
and   ((select max(c3) from V5fixed) )
= ((select max(c3) from V5fixed))
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 6)
    #
    stmt = """select * from TAB4 order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s10')
    
    _testmgr.testcase_end(desc)

