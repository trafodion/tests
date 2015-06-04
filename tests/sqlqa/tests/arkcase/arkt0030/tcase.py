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
    #  Test case name:     arkt0030 : A01
    #  Description:        It just sets up the database which will be
    #                      used by the rest of the test unit.
    #  Test case inputs:   --
    #  Test case outputs:  --
    #  Expected Results:   Same as above
    #
    #  Notes:
    #  This test case incorporates features detailed in the "Title"
    #  by Ima Programmer (Version 1.1, <date>).
    #
    # =================== End Test Case Header  ===================
    
    stmt = """drop table table1;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table table1 (
-- Fixed length character string
char_1                 CHAR(1)
, char_10                CHAR(10)
, pic_x_1                PIC X(1)
, pic_x_7                PIC X(7)
, pic_x_long             PICTURE X(3  ) DISPLAY
-- Varying length character string.
, var_char               VARCHAR(253)
-- Binary
, binary_signed          NUMERIC (4) SIGNED NOT NULL
, binary_32_u            NUMERIC (9,2) UNSIGNED
, binary_64_s            NUMERIC (18,3) SIGNED
, pic_comp_1             PIC S9(10) COMP
, pic_comp_2             PIC SV9(2) COMP
, pic_comp_3             PIC S9(3)V9(5) COMP
, small_int              SMALLINT
, medium_int             INTEGER UNSIGNED
, large_int              LARGEINT SIGNED
-- Fixed length character string
, decimal_1              DECIMAL (1)
, decimal_2_signed       DECIMAL (2,2) SIGNED
, decimal_3_unsigned     DECIMAL (3,0) UNSIGNED
, pic_decimal_1          PIC S9(1)V9(1) DISPLAY  SIGN IS LEADING
, pic_decimal_2          PICTURE V999 DISPLAY
, pic_decimal_3          PIC S9 DISPLAY SIGN IS LEADING
,
PRIMARY KEY ( binary_signed)
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # Now create a view from the base table.
    
    stmt = """create view pview as
select * from table1 where ( char_1 = 'D' );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # Now Insert some data into the base table.
    
    stmt = """insert into table1 values ('A','steven','C','walter','bob',
'B',50,50,200,50,0.12,100.9,10,10000,
1000000000,4,.5,90,1.1,0.1,1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into table1 values ('A','bobby','A','bobby','bop','B',
60,60,1200,60,0.79,100.99,1000,8000,
-1000,5,.6,100,2.1,0.2,2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into table1 values ('D', 'steven','B','9','bat','thomas',
8000,70,2000,500,0.10,100.999,90,
10000,1000,7,.7,110,3.1,0.3,3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into table1 values ('D','melissa','C','7','pop','jimmy',
1000,80,1500,500,0.20,100.9999,80,
9000,999,5,.8,120,4.1,0.4,4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into table1 values ('E','monica','Q','sue','pat',
'christopher',2000,90,1200,3000,0.30,
100.99999,2000,8000,-1000000,1,.9,80,
5.1,0.5,5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into table1 values ('D','michelle','D','michael','rat',
'thomas',-5000,90,2000,500,0.40,
100.8,90,8000,200,7,.93,140,6.1,0.6,6);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into table1 values ('C','maureen','E','jimmy','rum',
'marilyn',3000,80,2000,500,0.50,
100.7,9000,1000,2000,8,.97,150,7.1,
0.7,7);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into table1 values ('C','marcia','Z','johnny','dum',
'thomas',4000,40,2000,50,0.60,
100.6,8000,5000,0,9,.99,110,8.1,0.8,8);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # 01/22/98 EL  Took out the comment from the this query
    stmt = """update statistics for table table1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #
    #  Display the tables and views just to make sure they are what is
    #  expected.
    #
    stmt = """select * from table1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s0')
    stmt = """select * from pview;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s1')
    
    _testmgr.testcase_end(desc)

def test002(desc="""a02"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0030 : A02
    #  Description:        UPDATE positive tests using Params
    #                      Testcase A02  performs positive UPDATE
    #                      tests for SQLCI only.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   Same as above
    #
    #  Notes:
    #  This test case incorporates features detailed in the "Title"
    #  by Ima Programmer (Version 1.1, <date>).
    #
    # =================== End Test Case Header  ===================
    
    stmt = """set param ?value1 'A';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?value2 33;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """set param ?value3 'B';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?value4 304;"""
    output = _dci.cmdexec(stmt)
    
    # show param ?value1 ;
    # show param ?value2 ;
    # show param ?value3 ;
    # show param ?value4 ;
    
    stmt = """show param;"""
    output = _dci.cmdexec(stmt)
    
    # Update without using any params.
    
    stmt = """update table1 set char_10 = 'ABCDEFGHIJ'
where pic_x_1 = 'A';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    # Update using TACL-set params in Where clauses.
    
    stmt = """update table1 set pic_x_1 = 'K'
where char_1 = ?value1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 2)
    
    # Update using TACL-set params in Set clauses.
    
    stmt = """update table1 set binary_32_u = ?value2 * 3
where binary_signed = 4000;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    # Update using SQLCI-set params in Where clauses.
    
    stmt = """update table1 set pic_x_1 = 'b'
where pic_x_1 = ?value3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    # Update using SQLCI-set params in Set clauses.
    
    stmt = """update table1 set pic_comp_1 = ?value4
where binary_signed = 8000;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    #  Display the tables and views.
    stmt = """select * from table1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s0')
    
    stmt = """select * from pview;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s1')
    
    _testmgr.testcase_end(desc)

def test003(desc="""a03"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0030 : A03
    #  Description:        Update negative tests
    #                      Testcase A03 checks handling of negative
    #                      Update commands. Most tests simply attempt
    #                      to determine that preprocessor-only syntax forms
    #                      get trapped as an error. There a very few
    #                      tests here because semantic negative testing
    #                      occurs in SQLCI/PREPROCESSOR tests.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   Same as above
    #
    #  Notes:
    #  This test case incorporates features detailed in the "Title"
    #  by Ima Programmer (Version 1.1, <date>).
    #
    # =================== End Test Case Header  ===================
    #  Update should be rejected for a non-existing record in a table.
    
    stmt = """update table1 set char_1 = 'K'
where char_1 = '\$';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 0)
    
    #   Update should be rejected when a CURRENT OF clause appears.
    
    # #expectfile ${test_dir}/a03exp a03s0
    stmt = """update table1 set char_1 = 'x'
where current of y;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    #   Update should be rejected when a host variable is used in SQLCI.
    
    stmt = """update table1 set char_1 = :var
where char_1 <> 'x';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3049')
    
    #  Update should be rejected when a set param is used as a table name.
    
    stmt = """set param ?tabname table1;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """update ?tabname set char_1 = 'Q'
where char_1 <> 'x';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  Update should be rejected when a set param is used as a
    #  column name.
    
    stmt = """set param ?colname char_1;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """update table1 set ?colname = 'F'
where char_1 <> 'x';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  Update should be rejected when a set param is used as a
    #  value with the wrong type.
    
    stmt = """set param ?value10  'X';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """update table1 set binary_32_u = ?value10
where char_1 = 'A';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '29433')
    
    stmt = """set param ?value11  8000;"""
    output = _dci.cmdexec(stmt)
    
    ##expectfile ${test_dir}/a03exp a03s5
    stmt = """update table1 set pic_x_1 = '?'
where char_1 = ?value11;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    #  Display the tables and views to see that what's inside is what's
    #  expected.
    stmt = """select * from table1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s6')
    stmt = """select * from pview;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s7')
    
    #  11/08/01 EL  Added following queries for testing.
    stmt = """update table1 set pic_x_7 = '123', pic_x_7 = '999' where pic_x_7 = '7';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4022')
    
    stmt = """update table1 set pic_decimal_2 = .001, pic_decimal_2 = .009
where pic_decimal_2 = .3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4022')
    
    stmt = """drop view pview;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop table table1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #              End of test case ARKT0030
    _testmgr.testcase_end(desc)

