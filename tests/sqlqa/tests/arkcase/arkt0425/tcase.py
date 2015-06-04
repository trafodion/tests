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
    #  Description:        Precedence tests.
    #                      Select expression precedence test-
    #                      this tests the accuracy of the
    #                      various precedence rules in the
    #                      processing of SQL expressions.
    # Detail:              Various SQL expressions are tested in SELECT
    #                      statements.  Most of the expressions contain
    #                      no parenthesis to check the accuracy
    #                      of the default precedence rules. Some expressions
    #                      with parenthesis are used to verify the ability of
    #                      parens to override the default precedence(s).
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    #  Notes:
    #  This test case incorporates features detailed in the "Title"
    #  by Ima Programmer (Version 1.1, <date>).
    #
    #  Revision History:
    #      12/10/96       Modified to remove use of params on right of NOT LIKE
    #      08/05/96       Converted from REGRESS test library
    #                      sqltsql:sqlqat25:testcase A0
    #	11/04/97	Took out the table path name
    #			from the query from clause.
    #			Changed from $volumn.table_
    #			name to table_name.
    # =================== End Test Case Header  ===================
    
    #   Boolean/comp op precedence
    
    #   check precedence of AND over OR
    #   correct answer: first 2 records (insertion order, based on SYSKEY)
    
    stmt = """select *
from """ + gvars.g_schema_arkcasedb + """.btsel06 
where col_42 <> col_43 AND
col_44 < col_45 OR
col_66 = col_67 AND
col_68 > col_69;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s0')
    
    #   check precedence of NOT over OR
    #   correct answer: all records
    stmt = """select *
from """ + gvars.g_schema_arkcasedb + """.btsel08 
where not pic_252 > pic_1 OR
pic_252 > pic_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s1')
    
    #  check precedence of NOT over AND
    #  correct answer: all records except last 2
    stmt = """select *
from """ + gvars.g_schema_arkcasedb + """.btsel06 
where col_2 > col_3 AND
NOT col_26 = col_27 AND
col_69 = col_70;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    #  check precedence of BETWEEN predicate and NOT BETWEEN
    stmt = """set param ?p 50;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p1 200;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p2 800;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p3 100;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p4 300;"""
    output = _dci.cmdexec(stmt)
    stmt = """select *
from """ + gvars.g_schema_arkcasedb + """.btsel06 
where NOT col_28 = ?p AND
NOT col_1 NOT BETWEEN ?p3 AND ?p2 AND
NOT col_70 <= ?p1 OR
col_69 NOT BETWEEN ?p3 AND ?p4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s2')
    
    #  check precedence of IN and NOT IN
    stmt = """set param ?p 50;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p1 150;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p2 250;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p3 100;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p4 300;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p5 1900;"""
    output = _dci.cmdexec(stmt)
    stmt = """select *
from """ + gvars.g_schema_arkcasedb + """.btsel06 
where NOT col_6 NOT IN (?p,?p1,?p2)
AND col_1 IN (?p3,200,?p4)
OR  col_3 IN (900,?p5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s3')
    
    #  check precedence of LIKE and NOT LIKE
    stmt = """set param ?p '__e';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p1 'Q';"""
    output = _dci.cmdexec(stmt)
    stmt = """select *
from """ + gvars.g_schema_arkcasedb + """.btsel06 
where NOT pic_x_a NOT LIKE '__e'
AND pic_x_c NOT LIKE 'in'
AND pic_x_b NOT LIKE 'Q'
OR  pic_x_b LIKE 'D';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s4')
    
    #  check precedence of NOT NOT NOT
    stmt = """set param ?p 100;"""
    output = _dci.cmdexec(stmt)
    
    # This is a negative test, the NOT NOT NOT is not
    # a correct syntax.
    stmt = """select *
from """ + gvars.g_schema_arkcasedb + """.btsel06 
where NOT NOT NOT col_6 < ?p;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  check precedence of NOT (NOT (NOT
    stmt = """set param ?p 100;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select *
from """ + gvars.g_schema_arkcasedb + """.btsel06 
where NOT (NOT (NOT col_6 < ?p));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s6')
    
    #   arithmetic precedence
    
    #   check pri of monadic -
    stmt = """select -large_int * medium_int + -small_int
from """ + gvars.g_schema_arkcasedb + """.btsel01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s7')
    
    #   check pri of monadic +
    stmt = """select +large_int * medium_int + +large_int
from """ + gvars.g_schema_arkcasedb + """.btsel01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s8')
    
    #   check pri of *, / vs. +, -
    stmt = """select binary_signed + binary_32_u - pic_comp_1
* decimal_1 / pic_decimal_3 + decimal_3_unsigned
from """ + gvars.g_schema_arkcasedb + """.btsel01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s9')
    
    #   check pri of * vs. / and + vs. - (should be same)
    stmt = """select binary_signed - binary_32_u + pic_comp_1
/ decimal_1 * pic_decimal_3 + decimal_3_unsigned
from """ + gvars.g_schema_arkcasedb + """.btsel01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s10')
    
    #   check pri of monadic -, preceded by subtraction operator
    stmt = """select -large_int * medium_int - -small_int
from """ + gvars.g_schema_arkcasedb + """.btsel01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s11')
    
    #   check pri of aggregates
    stmt = """select avg(small_int) + -max(large_int) *
sum(medium_int)
from """ + gvars.g_schema_arkcasedb + """.btsel01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s12')
    
    #   check pri of expr inside aggr.
    stmt = """select avg(binary_signed + binary_32_u - pic_comp_1
* decimal_1 / pic_decimal_3 + decimal_3_unsigned)
from """ + gvars.g_schema_arkcasedb + """.btsel01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s13')
    
    #  arithmetic/boolean/comp op
    
    #  complex query
    #  correct answer: all records except first 2.
    stmt = """set param ?p 1000;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p1 10000;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p2 2;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p3 8;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p4 '__%';"""
    output = _dci.cmdexec(stmt)
    
    # This is a negative test for parameter set a value which
    # exceeding the define data type value.
    stmt = """select *
from """ + gvars.g_schema_arkcasedb + """.btsel01 
where NOT small_int + medium_int - medium_int + medium_int
* small_int / pic_decimal_1 * pic_decimal_1 < large_int
AND binary_signed BETWEEN ?p and ?p1
AND pic_decimal_1 + pic_decimal_2 * ?p2 <= ?p3
--              OR  pic_x_7 NOT LIKE ?p4
OR  pic_x_7 NOT LIKE '__%'
OR  pic_decimal_3 <> ?p3
AND pic_decimal_3 >= 6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '29188')
    
    #   same as above, with parens that change the evaluation order
    stmt = """select *
from """ + gvars.g_schema_arkcasedb + """.btsel01 
where NOT small_int + medium_int - medium_int + medium_int
* small_int / pic_decimal_1 * pic_decimal_1 < large_int
AND binary_signed BETWEEN ?p and 10000
AND pic_decimal_1 + pic_decimal_2 * 2 <= ?p3
OR ( pic_x_7 NOT LIKE '__%'
OR  pic_decimal_3 <> ?p3)
AND pic_decimal_3 >= 6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s15')
    
    #   same as above, with meaningless parens
    # This is a negative test for the parameter set up a  value which
    # exceeding the limit of the defined data type.
    stmt = """select *
from """ + gvars.g_schema_arkcasedb + """.btsel01 
where NOT small_int + medium_int - medium_int + medium_int
* small_int / pic_decimal_1 * pic_decimal_1 < large_int
AND binary_signed BETWEEN 1000 and ?p1
AND pic_decimal_1 + pic_decimal_2 * ?p2 <= 8
OR  pic_x_7 NOT LIKE '__%'
OR  (pic_decimal_3 <> ?p3
AND pic_decimal_3 >= 6) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '29188')
    
    #   select a huge arithmetic expression with parens
    stmt = """select ((binary_signed * (binary_64_s + pic_comp_1) -
(pic_comp_2 + pic_comp_3) * small_int
) * medium_int - large_int / decimal_1
) + decimal_2_signed * decimal_3_unsigned / pic_decimal_3
from """ + gvars.g_schema_arkcasedb + """.btsel01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s17')
    
    _testmgr.testcase_end(desc)

def test002(desc="""a02"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     A02
    #  Description:        Addition/subtraction overflow (column values only)
    #                      Select expression arithmetic
    #                      overflow test - this tests
    #                      overflow from addition and
    #                      subtraction in select expressions
    #                      of column values only (no literals).
    #  Detail:             Testing of overflow from the operations of addition
    #                      and subtraction is tested.  There are four different
    #                      levels of overflow: no overflow, possible overflow,
    #                      precision overflow, and actual overflow. Possible
    #                      overflow means the computed precision of the result
    #                      exceeds 18. Precision overflow means that the
    #                      precision of the actual runtime result exceeded 18,
    #                      but did not exceed the maximum value that can be
    #                      stored in a binary 64 variable.
    #                      Actual overflow means the actual runtime result
    #                      exceeded the maximum value that can be stored in
    #                      a binary 64 variable.
    #                      Expressions involving only columns are tested.
    #                      Signed and unsigned column values are tested,
    #                      as are binary and decimal column values.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    #  Notes:
    #  This test case incorporates features detailed in the "Title"
    #  by Ima Programmer (Version 1.1, <date>).
    #
    #  Revision History:
    #      08/05/96       Converted from REGRESS test library
    #                      sqltsql:sqlqat25:testcase A1
    #	11/04/97	Added obey cidefs.
    #			Took out the table path name from
    #			the query from clause.  Changed
    #			from $volumn.table_name to table_
    #			name.
    # =================== End Test Case Header  ===================
    
    #  column/column
    #  signed
    
    #  possible overflow, binary columns,
    #  actual values small -> no overflow
    stmt = """set param ?p 'A';"""
    output = _dci.cmdexec(stmt)
    stmt = """select large_bin_1, large_bin_2,
large_bin_1 + large_bin_2
from """ + gvars.g_schema_arkcasedb + """.btsel26 
where selector = ?p;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s0')
    
    #   possible overflow, decimal columns,
    #   actual values small -> no overflow
    stmt = """select large_dec_1, large_dec_2,
large_dec_1 + large_dec_2
from """ + gvars.g_schema_arkcasedb + """.btsel26 
where selector = ?p;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s1')
    
    #  possible overflow, binary columns, actual values large
    #  (result should be one less than precision overflow)
    stmt = """set param ?p 'D';"""
    output = _dci.cmdexec(stmt)
    stmt = """select large_bin_1, large_bin_2,
large_bin_1 + large_bin_2
from """ + gvars.g_schema_arkcasedb + """.btsel26 
where selector = ?p;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s2')
    
    #   same as above, with decimal columns
    stmt = """select large_dec_1, large_dec_2,
large_dec_1 + large_dec_2
from """ + gvars.g_schema_arkcasedb + """.btsel26 
where selector = ?p;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s3')
    
    #  precision overflow, binary columns, result positive
    stmt = """set param ?p 'B';"""
    output = _dci.cmdexec(stmt)
    stmt = """select large_bin_1, large_bin_2,
large_bin_1 + large_bin_2
from """ + gvars.g_schema_arkcasedb + """.btsel26 
where selector = ?p;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s4')
    
    #   precision overflow, decimal columns, result positive
    stmt = """select large_dec_1, large_dec_2,
large_dec_1 + large_dec_2
from """ + gvars.g_schema_arkcasedb + """.btsel26 
where selector = ?p;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s5')
    
    #  precision overflow, binary columns, result negative
    #  (underflow)
    stmt = """set param ?p 'C';"""
    output = _dci.cmdexec(stmt)
    stmt = """select large_bin_1, large_bin_2,
large_bin_1 - large_bin_2
from """ + gvars.g_schema_arkcasedb + """.btsel26 
where selector = ?p;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s6')
    
    #   precision overflow, dec cols, result negative
    #   (underflow)
    stmt = """select large_dec_1, large_dec_2,
large_dec_1 - large_dec_2
from """ + gvars.g_schema_arkcasedb + """.btsel26 
where selector = ?p;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s7')
    
    #  precision overflow, binary columns, scale 18
    #  (add .9 + .2, scales of both = .18)
    stmt = """set param ?p 'A';"""
    output = _dci.cmdexec(stmt)
    stmt = """select small_bin_1, small_bin_2,
small_bin_1 + small_bin_2
from """ + gvars.g_schema_arkcasedb + """.btsel26 
where selector = ?p;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s8')
    
    #   same as above, dec columns
    stmt = """select small_dec_1 , small_dec_2,
small_dec_1 + small_dec_2
from """ + gvars.g_schema_arkcasedb + """.btsel26 
where selector = ?p;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s9')
    
    #  precision overflow, binary columns
    stmt = """set param ?p 'B';"""
    output = _dci.cmdexec(stmt)
    stmt = """select small_bin_1 , small_bin_2,
small_bin_1 + small_bin_2
from """ + gvars.g_schema_arkcasedb + """.btsel26 
where selector = ?p;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s10')
    
    #   same, dec columns
    stmt = """select small_dec_1 , small_dec_2,
small_dec_1 + small_dec_2
from """ + gvars.g_schema_arkcasedb + """.btsel26 
where selector = ?p;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s11')
    
    #  precision overflow, bin columns
    stmt = """set param ?p 'C';"""
    output = _dci.cmdexec(stmt)
    stmt = """select small_bin_1 , small_bin_2,
small_bin_1 + small_bin_2
from """ + gvars.g_schema_arkcasedb + """.btsel26 
where selector = ?p;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s12')
    
    #   same , dec columns
    stmt = """select small_dec_1 , small_dec_2,
small_dec_1 + small_dec_2
from """ + gvars.g_schema_arkcasedb + """.btsel26 
where selector = ?p;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s13')
    
    #  no overflow possible, bin cols, result positive
    stmt = """set param ?p 'A';"""
    output = _dci.cmdexec(stmt)
    stmt = """select semi_large_bin_1 , semi_large_bin_2,
semi_large_bin_1 + semi_large_bin_2
from """ + gvars.g_schema_arkcasedb + """.btsel26 
where selector = ?p;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s14')
    
    #  no overflow possible, bin cols, result negative
    stmt = """set param ?p 'B';"""
    output = _dci.cmdexec(stmt)
    stmt = """select semi_large_bin_1 , semi_large_bin_2,
semi_large_bin_1 - semi_large_bin_2
from """ + gvars.g_schema_arkcasedb + """.btsel26 
where selector = ?p;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s15')
    
    #  precision overflow, binary columns
    stmt = """set param ?p 'A';"""
    output = _dci.cmdexec(stmt)
    stmt = """select one_nine_bin , nine_one_bin,
one_nine_bin + nine_one_bin
from """ + gvars.g_schema_arkcasedb + """.btsel26 
where selector = ?p;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s16')
    
    #  overflow possible, result largest value possible with no
    #  precision overflow
    stmt = """set param ?p 'B';"""
    output = _dci.cmdexec(stmt)
    stmt = """select one_nine_bin , nine_one_bin,
one_nine_bin + nine_one_bin
from """ + gvars.g_schema_arkcasedb + """.btsel26 
where selector = ?p;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s17')
    
    #   actual overflow, cols bin, result positive
    stmt = """select large_bin_1 , small_bin_1,
large_bin_1 + small_bin_1
from """ + gvars.g_schema_arkcasedb + """.btsel26 
where selector = ?p;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s18')
    
    #   same as above, dec cols
    stmt = """select large_dec_1 , small_dec_1,
large_dec_1 + small_dec_1
from """ + gvars.g_schema_arkcasedb + """.btsel26 
where selector = ?p;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s19')
    
    #  actual overflow, cols bin, result negative
    #  (underflow)
    stmt = """set param ?p 'C';"""
    output = _dci.cmdexec(stmt)
    stmt = """select large_bin_1 , small_bin_1,
large_bin_1 - small_bin_1
from """ + gvars.g_schema_arkcasedb + """.btsel26 
where selector = ?p;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s20')
    
    #  actual overflow by 1
    stmt = """set param ?p 'G';"""
    output = _dci.cmdexec(stmt)
    stmt = """select large_bin_1 , small_bin_2,
large_bin_1 + small_bin_2
from """ + gvars.g_schema_arkcasedb + """.btsel26 
where selector = ?p;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s21')
    
    #   one less than actual overflow
    stmt = """select large_bin_1 , small_bin_1,
large_bin_1 + small_bin_1
from """ + gvars.g_schema_arkcasedb + """.btsel26 
where selector = ?p;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s22')
    
    #  overflow possible (technically but not really), binary cols,
    #  actual values small - no overflow
    stmt = """set param ?p 'A';"""
    output = _dci.cmdexec(stmt)
    stmt = """select nine_zero_bin_u , zero_nine_bin_u,
nine_zero_bin_u + zero_nine_bin_u
from """ + gvars.g_schema_arkcasedb + """.btsel26 
where selector  = ?p;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s23')
    
    #   same as above, dec cols
    stmt = """select nine_zero_dec_u , zero_nine_dec_u,
nine_zero_dec_u + zero_nine_dec_u
from """ + gvars.g_schema_arkcasedb + """.btsel26 
where selector  = ?p;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s24')
    
    #  possible overflow, bin cols, actual values large
    #  result should be .000 000 001 less than overflow
    stmt = """set param ?p 'B';"""
    output = _dci.cmdexec(stmt)
    stmt = """select nine_zero_bin_u , zero_nine_bin_u,
nine_zero_bin_u + zero_nine_bin_u
from """ + gvars.g_schema_arkcasedb + """.btsel26 
where selector = ?p;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s25')
    
    #   same as above, dec cols
    stmt = """select nine_zero_dec_u, zero_nine_dec_u,
nine_zero_dec_u + zero_nine_dec_u
from """ + gvars.g_schema_arkcasedb + """.btsel26 
where selector = ?p;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s26')
    
    #   actual overflow, binary cols
    stmt = """select nine_zero_bin_u, zero_nine_bin_u,
zero_nine_bin_u,
nine_zero_bin_u + zero_nine_bin_u
+ zero_nine_bin_u
from """ + gvars.g_schema_arkcasedb + """.btsel26 
where selector = ?p;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s27')
    
    #   same as above, dec cols
    stmt = """select nine_zero_dec_u, zero_nine_dec_u,
zero_nine_dec_u,
nine_zero_dec_u + zero_nine_dec_u
+ zero_nine_dec_u
from """ + gvars.g_schema_arkcasedb + """.btsel26 
where selector = ?p;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s28')
    
    #   actual underflow, bin cols
    stmt = """select -nine_zero_bin_u, - zero_nine_bin_u,
- zero_nine_bin_u,
-nine_zero_bin_u - zero_nine_bin_u
- zero_nine_bin_u
from """ + gvars.g_schema_arkcasedb + """.btsel26 
where selector = ?p;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s29')
    
    _testmgr.testcase_end(desc)

def test003(desc="""a03"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     A03
    #  Description:        Select expression arithmetic overflow test
    #                      - this tests overflow from addition and
    #                      subtraction in select expressions of column
    #                      values and literals, and select expressions
    #                      of literals and literals.
    #  Detail:             Testing of overflow from the operations of
    #                      addition and subtraction is tested.
    #                      Expressions involving a column with a literal
    #                      and literal/literal expressions are tested.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    #  Notes:
    #  This test case incorporates features detailed in the "Title"
    #  by Ima Programmer (Version 1.1, <date>).
    #
    #  Revision History:
    #      08/05/96       Converted from REGRESS test library
    #                      sqltsql:sqlqat25:testcase A2
    #	11/04/97	Added obey cidefs
    #			Took out the table path name from
    #			the query from clause.  Changed
    #			from $volumn.table_name to table_
    #			name.
    # =================== End Test Case Header  ===================
    
    #  column/literal
    #  precision overflow, binary column
    #  add .9 + .2, scale of column = .18
    stmt = """set param ?p .200000000000000000;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?a 'A';"""
    output = _dci.cmdexec(stmt)
    stmt = """select small_bin_1 + ?p
from """ + gvars.g_schema_arkcasedb + """.btsel26 
where selector = ?a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s0')
    
    #  precision overflow, binary column
    #  add .9 + .2, scale of column = .18, scale of literal = 1
    stmt = """set param ?p .2;"""
    output = _dci.cmdexec(stmt)
    stmt = """select small_bin_1 + ?p
from """ + gvars.g_schema_arkcasedb + """.btsel26 
where selector = ?a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s1')
    
    #  precision overflow, dec column
    stmt = """set param ?b 'B';"""
    output = _dci.cmdexec(stmt)
    stmt = """select small_dec_1 + .000000000000000001
from """ + gvars.g_schema_arkcasedb + """.btsel26 
where selector = ?b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s2')
    
    #   precision overflow, dec column
    stmt = """select small_dec_1 + .000000000000000002
from """ + gvars.g_schema_arkcasedb + """.btsel26 
where selector = 'C';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s3')
    
    #  literal/literal
    
    #  precision overflow ?
    stmt = """set param ?p .900;"""
    output = _dci.cmdexec(stmt)
    stmt = """select  ?p +   .200000000000000000
from """ + gvars.g_schema_arkcasedb + """.btsel26;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s4')
    
    #   precision overflow
    stmt = """select .999999999999999999 + .000000000000000001
from """ + gvars.g_schema_arkcasedb + """.btsel26;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s5')
    
    #   precision overflow
    stmt = """select  .999999999999999999 +
.000000000000000002
from """ + gvars.g_schema_arkcasedb + """.btsel26 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s6')
    
    #  actual overflow ?
    stmt = """set param ?p1 10.0;"""
    output = _dci.cmdexec(stmt)
    stmt = """select ?p1 + .900000000000000000
from """ + gvars.g_schema_arkcasedb + """.btsel26;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s7')
    
    #   actual overflow ?
    stmt = """select .90000000000000000000
from """ + gvars.g_schema_arkcasedb + """.btsel26;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s8')
    
    #   actual overflow ?
    stmt = """select 10.999999999999999999
from """ + gvars.g_schema_arkcasedb + """.btsel26;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s9')
    
    _testmgr.testcase_end(desc)

def test004(desc="""a04"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     A04
    #  Description:        Multiplication overflow.
    #                      Select expression arithmetic overflow test
    #                      - this tests overflow from multiplication
    #                      in select expressions  of column values only
    #                      (no literals).
    # Detail:              Testing of overflow from multiplication is tested.
    #                      There are four different levels of overflow:
    #                      no overflow, possible overflow, precision overflow,
    #                      and actual overflow.
    #                      Possible overflow means the computed precision
    #                      of the result exceeds 18.
    #                      Precision overflow means that the precision of the
    #                      actual runtime result exceeded 18, but did not
    #                      exceed the maximum value that can be stored in
    #                      a binary 64 variable.
    #                      Actual overflow means the actual runtime result
    #                      exceeded the maximum value that can be stored
    #                      in a binary 64 variable.
    #                      Expressions involving only columns are tested.
    #                      Signed and unsigned column values are tested,
    #                      as are binary and decimal column values.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    #  Notes:
    #  This test case incorporates features detailed in the "Title"
    #  by Ima Programmer (Version 1.1, <date>).
    #
    #  Revision History:
    #      08/05/96       Converted from REGRESS test library
    #                      sqltsql:sqlqat25:testcase A3
    #	11/04/97	Added obey cidefs.
    #			Took out the table path name from
    #			the query from clause.  Changed from
    #			$volumn.table_name to table_name.
    # =================== End Test Case Header  ===================
    
    #  signed
    #  no overflow possible, result positive
    stmt = """set param ?p 'A';"""
    output = _dci.cmdexec(stmt)
    stmt = """select eight_one_bin, one_eight_bin,
eight_one_bin * one_eight_bin
from """ + gvars.g_schema_arkcasedb + """.btsel26 
where selector = ?p;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s0')
    
    #  no overflow possible, result negative
    stmt = """set param ?p 'B';"""
    output = _dci.cmdexec(stmt)
    stmt = """select eight_one_bin, one_eight_bin,
eight_one_bin * one_eight_bin
from """ + gvars.g_schema_arkcasedb + """.btsel26 
where selector = ?p;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s1')
    
    #  overflow possible, result positive
    stmt = """set param ?p 'D';"""
    output = _dci.cmdexec(stmt)
    stmt = """select eight_one_bin, one_nine_bin,
eight_one_bin * one_nine_bin
from """ + gvars.g_schema_arkcasedb + """.btsel26 
where selector = ?p;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s2')
    
    #  actual overflow, result positive
    stmt = """set param ?p 'A';"""
    output = _dci.cmdexec(stmt)
    stmt = """select nine_one_bin, one_eight_bin,
nine_one_bin * one_eight_bin
from """ + gvars.g_schema_arkcasedb + """.btsel26 
where selector = ?p;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s3')
    
    #  actual overflow, result negative (underflow)
    stmt = """set param ?p 'C';"""
    output = _dci.cmdexec(stmt)
    stmt = """select nine_one_bin, one_eight_bin,
nine_one_bin * one_eight_bin
from """ + gvars.g_schema_arkcasedb + """.btsel26 
where selector = ?p;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s4')
    
    #  actual overflow, scale 18; bin cols.
    stmt = """set param ?p 'D';"""
    output = _dci.cmdexec(stmt)
    stmt = """select one_nine_bin, one_nine_bin,
one_nine_bin * one_nine_bin
from """ + gvars.g_schema_arkcasedb + """.btsel26 
where selector = ?p;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s5')
    
    #   possible overflow only, scale 18; bin cols.
    stmt = """select one_nine_bin, one_nine_bin,
one_nine_bin * one_nine_bin
from """ + gvars.g_schema_arkcasedb + """.btsel26 
where selector = ?p;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s6')
    
    #   actual overflow (right end only), result positive
    #   scale = 36
    stmt = """select small_bin_1, small_bin_2,
small_bin_1 * small_bin_2
from """ + gvars.g_schema_arkcasedb + """.btsel26 
where selector = ?p;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s7')
    
    #   actual overflow (right end only), result negative
    #   scale = 36
    stmt = """select small_bin_1, -small_bin_2,
small_bin_1 * -small_bin_2
from """ + gvars.g_schema_arkcasedb + """.btsel26 
where selector = ?p;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s8')
    
    #   actual overflow (left end only) result positive
    stmt = """select large_bin_1, large_bin_2,
large_bin_1 * large_bin_2
from """ + gvars.g_schema_arkcasedb + """.btsel26 
where selector = ?p;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8411')
    
    #   actual overflow (left end only) result negative
    stmt = """select large_bin_1, -large_bin_2,
large_bin_1 * -large_bin_2
from """ + gvars.g_schema_arkcasedb + """.btsel26 
where selector = ?p;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8411')
    
    #   actual overflow (scale > 18), precision = 19
    stmt = """select small_bin_1, zero_one_bin,
small_bin_1 * zero_one_bin
from """ + gvars.g_schema_arkcasedb + """.btsel26 
where selector = ?p;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s11')
    
    #  actual overflow (scale > 18) precision = 20
    stmt = """set param ?p 'C';"""
    output = _dci.cmdexec(stmt)
    stmt = """select small_bin_1, zero_one_bin,
small_bin_1 * zero_one_bin
from """ + gvars.g_schema_arkcasedb + """.btsel26 
where selector = ?p;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s12')
    
    #   unsigned
    
    #   actual overflow, bin cols
    stmt = """select nine_zero_bin_u, zero_nine_bin_u,
nine_zero_bin_u,
nine_zero_bin_u * zero_nine_bin_u
* nine_zero_bin_u
from """ + gvars.g_schema_arkcasedb + """.btsel26 
where selector = 'B';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s13')
    
    #   actual underflow, bin cols
    stmt = """select nine_zero_bin_u, -zero_nine_bin_u,
nine_zero_bin_u,
nine_zero_bin_u * -zero_nine_bin_u
* nine_zero_bin_u
from """ + gvars.g_schema_arkcasedb + """.btsel26 
where selector = 'B';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s14')
    
    #   actual overflow, dec cols
    stmt = """select nine_zero_dec_u, zero_nine_dec_u,
nine_zero_dec_u,
nine_zero_dec_u * zero_nine_dec_u
* nine_zero_dec_u
from """ + gvars.g_schema_arkcasedb + """.btsel26 
where selector = 'B';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s15')
    
    #   actual underflow, dec cols
    stmt = """select nine_zero_dec_u, -zero_nine_dec_u,
nine_zero_dec_u,
nine_zero_dec_u * -zero_nine_dec_u
* nine_zero_dec_u
from """ + gvars.g_schema_arkcasedb + """.btsel26 
where selector = 'B';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s16')
    
    _testmgr.testcase_end(desc)

def test005(desc="""a05"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     A05
    #  Description:        Division overflow.
    #                      Select expression arithmetic overflow test
    #                      - this tests overflow from division
    #                      in select expressions of column values
    #                      only (no literals).
    # Detail:
    #         Testing of overflow from division is tested.
    #       There are three different levels of overflow: no overflow,
    #       precision overflow, and actual overflow.
    #       Precision overflow means that the precision of the
    #       actual runtime result exceeded 18, but did not exceed the
    #       maximum value that can be stored in a binary 64 variable.
    #       Actual overflow means the actual runtime result exceeded
    #       the maximum value that can be stored in a binary 64 variable.
    #       Expressions involving only binary columns are tested.k
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    #  Notes:
    #  This test case incorporates features detailed in the "Title"
    #  by Ima Programmer (Version 1.1, <date>).
    #
    #  Revision History:
    #      08/05/96       Converted from REGRESS test library
    #                      sqltsql:sqlqat25:testcase A4
    #	11/04/97	Added obey cidefs.
    #			Took out the table path name from the
    #			query from clause.  Changed from
    #			$volumn.table_name to table_name.
    # =================== End Test Case Header  ===================
    
    #   no left overflow or right truncation, scale positive
    
    stmt = """select large_bin_1 , large_bin_2,
large_bin_1 / large_bin_2
from """ + gvars.g_schema_arkcasedb + """.btsel26 
where selector = 'E';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s0')
    
    #   right truncation, scale 0
    stmt = """select large_bin_1 , large_bin_2,
large_bin_1 / large_bin_2
from """ + gvars.g_schema_arkcasedb + """.btsel26 
where selector = 'F' ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s1')
    
    #   precision overflow (precision > 18)
    stmt = """select large_bin_1 , small_bin_2,
large_bin_1 / small_bin_2
from """ + gvars.g_schema_arkcasedb + """.btsel26 
where selector = 'D';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s2')
    
    #   actual left overflow, result positive , scale negative
    stmt = """select large_bin_1 , small_bin_1,
large_bin_1 / small_bin_1
from """ + gvars.g_schema_arkcasedb + """.btsel26 
where selector = 'F';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8411')
    
    #   actual left overflow, result negative, scale negative
    stmt = """select -large_bin_1 , small_bin_1,
-large_bin_1 / small_bin_1
from """ + gvars.g_schema_arkcasedb + """.btsel26 
where selector = 'F';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8411')
    
    #   right truncation, result positive
    #   scale positive
    stmt = """select small_bin_1 , semi_large_bin_1,
small_bin_1 / semi_large_bin_1
from """ + gvars.g_schema_arkcasedb + """.btsel26 
where selector = 'E';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s5')
    
    #   right truncation, result negative
    #   scale positive
    stmt = """select -small_bin_1 , semi_large_bin_1,
-small_bin_1 / semi_large_bin_1
from """ + gvars.g_schema_arkcasedb + """.btsel26 
where selector = 'E';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s6')
    
    #   no left overflow, scale negative
    stmt = """select semi_large_bin_1 , small_bin_1,
semi_large_bin_1 / small_bin_1
from """ + gvars.g_schema_arkcasedb + """.btsel26 
where selector = 'F';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s7')
    
    #   right truncation, scale negative
    stmt = """select large_bin_1 , one_nine_bin,
large_bin_1 / one_nine_bin
from """ + gvars.g_schema_arkcasedb + """.btsel26 
where selector = 'F';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s8')
    
    #   no left overflow or right truncation, decimal places in result
    stmt = """select semi_large_bin_2 , one_eight_bin,
semi_large_bin_2 / one_eight_bin
from """ + gvars.g_schema_arkcasedb + """.btsel26 
where selector = 'D';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s9')
    
    _testmgr.testcase_end(desc)

def test006(desc="""a06"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     A06
    #  Description:        Aggregate overflow
    #                      This testcase is an arithmetic
    #                      overflow test for aggregates
    #  Detail:
    #      min, max, count are tested to ensure the proper precision
    #      and scale of the result. Note no overflow is possible for
    #      these aggregates.  Most of the tests here are for SUM and
    #      AVG. For SUM - there are two kinds of overflow - overflow
    #      in the computation and overflow in the result. Note that
    #      there can never be overflow in the result for AVG.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    #  Notes:
    #  This test case incorporates features detailed in the "Title"
    #  by Ima Programmer (Version 1.1, <date>).
    #
    #  Revision History:
    #      08/05/96       Converted from REGRESS test library
    #                      sqltsql:sqlqat25:testcase A4
    #	11/04/97	Added obey cidefs.
    #			Took out the table path name from the
    #			query from clause.  Changed from
    #			$volumn.table_name to table_name.
    # =================== End Test Case Header  ===================
    
    #   MAX, MIN
    #   max, scale = 0
    
    stmt = """select max(large_bin_1)
from """ + gvars.g_schema_arkcasedb + """.btsel26;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s0')
    
    #   max, scale = 9
    stmt = """select max(one_nine_bin)
from """ + gvars.g_schema_arkcasedb + """.btsel26;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s1')
    
    #   min, scale = 0
    stmt = """select min(large_bin_1)
from """ + gvars.g_schema_arkcasedb + """.btsel26;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s2')
    
    #   min, scale = 9
    stmt = """select min(one_nine_bin)
from """ + gvars.g_schema_arkcasedb + """.btsel26;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s3')
    
    #   COUNT
    
    #   count, original scale = 0
    stmt = """select count(distinct large_bin_1)
from """ + gvars.g_schema_arkcasedb + """.btsel26;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s4')
    
    #   count, original scale = 9
    stmt = """select count(distinct one_nine_bin)
from """ + gvars.g_schema_arkcasedb + """.btsel26;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s5')
    
    #   count(*)
    stmt = """select count(*)
from """ + gvars.g_schema_arkcasedb + """.btsel26;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s6')
    
    #   SUM
    
    #   sum, no overflow, scale = 0
    stmt = """select semi_large_bin_1
from """ + gvars.g_schema_arkcasedb + """.btsel26;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s7')
    
    stmt = """select sum(semi_large_bin_1)
from """ + gvars.g_schema_arkcasedb + """.btsel26;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s8')
    
    #   sum, overflow in calculation and result
    stmt = """select large_bin_1
from """ + gvars.g_schema_arkcasedb + """.btsel26 
where (selector <> 'O') and (selector <> 'P');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s9')
    
    stmt = """select sum(large_bin_1)
from """ + gvars.g_schema_arkcasedb + """.btsel26 
where (selector <> 'O') and (selector <> 'P');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s10')
    
    #   sum, overflow in calculation only
    stmt = """select large_bin_1
from """ + gvars.g_schema_arkcasedb + """.btsel26;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s11')
    
    stmt = """select  sum(large_bin_1)
from """ + gvars.g_schema_arkcasedb + """.btsel26;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s12')
    
    #  sum, underflow in calculation and result
    stmt = """set param ?p 'O';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p1 'P';"""
    output = _dci.cmdexec(stmt)
    stmt = """select -large_bin_1
from """ + gvars.g_schema_arkcasedb + """.btsel26 
where (selector <> ?p ) and (selector <> ?p1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s13')
    
    stmt = """select sum(-large_bin_1)
from """ + gvars.g_schema_arkcasedb + """.btsel26 
where (selector <> ?p ) and (selector <> ?p1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s14')
    
    #   sum, no overflow, scale > 0
    stmt = """select small_dec_2
from """ + gvars.g_schema_arkcasedb + """.btsel26;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s15')
    
    stmt = """select  sum(small_dec_2)
from """ + gvars.g_schema_arkcasedb + """.btsel26;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s16')
    
    #   sum, overflow in calculation and result, scale > 0
    stmt = """select small_dec_1
from """ + gvars.g_schema_arkcasedb + """.btsel26;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s17')
    
    stmt = """select sum(small_dec_1)
from """ + gvars.g_schema_arkcasedb + """.btsel26;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8411')
    
    #   AVG
    
    #   avg, no overflow, scale = 0
    stmt = """select sum(semi_large_bin_1),
avg(semi_large_bin_1)
from """ + gvars.g_schema_arkcasedb + """.btsel26;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s19')
    
    #  avg, no overflow in result, overflow in calculation
    #  (impossible to get overflow in result)
    stmt = """set param ?p 'O';"""
    output = _dci.cmdexec(stmt)
    stmt = """select sum(large_bin_1), avg(large_bin_1)
from """ + gvars.g_schema_arkcasedb + """.btsel26 
where (selector <> ?p) and (selector <> 'P');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s20')
    
    #   avg, underflow in calculation
    stmt = """select  -large_bin_1
from """ + gvars.g_schema_arkcasedb + """.btsel26;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s21')
    
    stmt = """select  sum(-large_bin_1), avg(-large_bin_1)
from """ + gvars.g_schema_arkcasedb + """.btsel26;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s22')
    
    #   avg, no overflow, scale > 0
    stmt = """select small_dec_2
from """ + gvars.g_schema_arkcasedb + """.btsel26;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s23')
    
    stmt = """select avg(small_dec_2)
from """ + gvars.g_schema_arkcasedb + """.btsel26;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s24')
    
    #   avg, overflow, scale > 0
    stmt = """select small_dec_1
from """ + gvars.g_schema_arkcasedb + """.btsel26;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s25')
    
    stmt = """select avg(small_dec_1)
from """ + gvars.g_schema_arkcasedb + """.btsel26;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8411')
    
    #   SUM, overflow based on order records are evaluated
    
    #   sum, no overflow in calculation or result IF the calculation
    #   is done in 'insertion' order (file with SYSKEY)
    stmt = """select large_dec_1
from """ + gvars.g_schema_arkcasedb + """.btsel26;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s27')
    
    stmt = """select  sum(large_dec_1)
from """ + gvars.g_schema_arkcasedb + """.btsel26;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s28')
    
    #  sum, no overflow in result, overflow in calculation
    #  IF the calculation done based on alternate index on large_dec_1
    stmt = """set param ?p 2;"""
    output = _dci.cmdexec(stmt)
    stmt = """select large_dec_1
from """ + gvars.g_schema_arkcasedb + """.btsel26 
where large_dec_1 <> ?p;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s29')
    
    stmt = """select sum(large_dec_1)
from """ + gvars.g_schema_arkcasedb + """.btsel26 
where large_dec_1 <> ?p;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s30')
    
    _testmgr.testcase_end(desc)

def test007(desc="""a07"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     A07
    #  Description:        Type propagation.
    #                      This testcase tests type propagation of
    #                      expressions.
    #  Detail:             Type propagation tests are conducted for
    #                      various data types and resultant data types
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    #  Notes:
    #  This test case incorporates features detailed in the "Title"
    #  by Ima Programmer (Version 1.1, <date>).
    #
    #  Revision History:
    #      08/05/96       Converted from REGRESS test library
    #                      sqltsql:sqlqat25:testcase A6
    #	11/04/97	Added obey cidefs.
    #			Took out the table path name from
    #			the query from clause.  Changed
    #			from $volumn.table_name to table_
    #			name.
    # =================== End Test CaseHeader  ===================
    
    #  sbin data
    #  result bin 16
    #  p = 3, s = 2
    stmt = """set param ?p 60;"""
    output = _dci.cmdexec(stmt)
    stmt = """select pic_comp_2 + pic_comp_2
from """ + gvars.g_schema_arkcasedb + """.btsel01 
where binary_signed = ?p;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s0')
    
    #   result bin 16
    #   p = 4, s = 4
    stmt = """select pic_comp_2 * pic_comp_2
from """ + gvars.g_schema_arkcasedb + """.btsel01 
where binary_signed = 60;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s1')
    
    #   result bin 32
    #   p = 9, s = 0
    stmt = """select (binary_signed + small_int) * small_int
from """ + gvars.g_schema_arkcasedb + """.btsel01 
where binary_signed = ?p;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s2')
    
    #   result bin 64
    #   p = 18, s = 8
    stmt = """select (binary_signed + small_int) / binary_64_s
from """ + gvars.g_schema_arkcasedb + """.btsel01 
where binary_signed = 60;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s3')
    
    #   unsigned data
    
    #   result bin 16
    #   p = 4, s = 0
    stmt = """select decimal_3_unsigned + decimal_3_unsigned
from """ + gvars.g_schema_arkcasedb + """.btsel01 
where binary_signed = 60;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s4')
    
    #  result bin 32
    #  p = 9, s = 0
    stmt = """set param ?p 'Q';"""
    output = _dci.cmdexec(stmt)
    stmt = """select (col_2 + col_7) * col_6
from """ + gvars.g_schema_arkcasedb + """.btsel06 
where pic_x_b = ?p;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s5')
    
    #   result bin 64
    #   p = 12, s = 2
    stmt = """select binary_32_u * decimal_3_unsigned
from """ + gvars.g_schema_arkcasedb + """.btsel01 
where binary_signed = 60;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s6')
    
    #   sdec data
    
    #   result bin 16
    #   p =   3, s = 1
    stmt = """select pic_decimal_1 - pic_decimal_3
from """ + gvars.g_schema_arkcasedb + """.btsel01 
where pic_decimal_1 = 1.1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s7')
    
    #   result bin 32
    #   p = 9, s = 0
    stmt = """select col_9 * col_10 + col_9
from """ + gvars.g_schema_arkcasedb + """.btsel06 
where pic_x_b = 'Q';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s8')
    
    #   result bin 64
    #   p = 18, s = 9
    stmt = """select col_47 / col_48 * col_70
from """ + gvars.g_schema_arkcasedb + """.btsel06 
where pic_x_b = 'Q';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s9')
    
    #   constant data
    
    #   result bin 16
    #   p = 4, s = 2
    stmt = """select decimal_2_signed + 4.7
from """ + gvars.g_schema_arkcasedb + """.btsel01 
where binary_32_u = 60;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s10')
    
    #  result bin 32
    #  p = 8, s = 2
    stmt = """set param ?p 9.08;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p1 10000;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p2 60;"""
    output = _dci.cmdexec(stmt)
    stmt = """select decimal_3_unsigned * ?p + ?p1
from """ + gvars.g_schema_arkcasedb + """.btsel01 
where binary_32_u = ?p2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s11')
    
    #  result bin 64
    #  p = 18, s = 16
    stmt = """set param ?p 17.496;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p1 63;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p2 60;"""
    output = _dci.cmdexec(stmt)
    stmt = """select (?p / 85) + (?p1 * medium_int) - small_int
from """ + gvars.g_schema_arkcasedb + """.btsel01 
where binary_32_u = ?p2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s12')
    
    #   mixed/complex/aggregates
    
    #   result bin 16
    stmt = """select pic_comp_2 - decimal_2_signed * pic_decimal_3
from """ + gvars.g_schema_arkcasedb + """.btsel01 
where binary_32_u = 60;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s13')
    
    #  result bin 16
    stmt = """set param ?p 60;"""
    output = _dci.cmdexec(stmt)
    stmt = """select max(pic_comp_2) - min(decimal_2_signed) *
max(pic_decimal_3)
from """ + gvars.g_schema_arkcasedb + """.btsel01 
where binary_32_u = ?p;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s14')
    
    #   result bin 32
    stmt = """select decimal_3_unsigned + small_int - decimal_1
from """ + gvars.g_schema_arkcasedb + """.btsel01 
where binary_32_u = 60;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s15')
    
    #   result bin 64
    stmt = """select ((decimal_1 + decimal_3_unsigned) *
binary_32_u - pic_comp_2
) / pic_comp_1 + pic_comp_3 * decimal_2_signed
from """ + gvars.g_schema_arkcasedb + """.btsel01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s16')
    
    #   result bin 64
    stmt = """select sum(pic_comp_3) + sum(large_int) + avg(binary_32_u)
from """ + gvars.g_schema_arkcasedb + """.btsel01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s17')
    
    _testmgr.testcase_end(desc)

def test008(desc="""a08"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     A08
    #  Description:        Insert statement assignment truncation.
    #                      This testcase tests assignment truncation
    #                      using INSERT stmts.
    #  Detail:             Truncation assignment is tested by first
    #                      creating a temporary table, trunctmp, using the
    #                      seldbvol catalog.  Test statements that insert
    #                      various values into the various columns are run.
    #                      Only one column is tested per test statement
    #                      - all other column values are set to 0.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    #  Notes:
    #  This test case incorporates features detailed in the "Title"
    #  by Ima Programmer (Version 1.1, <date>).
    #
    #  Revision History:
    #      08/05/96       Converted from REGRESS test library
    #                      sqltsql:sqlqat25:testcase A7
    #	11/04/97	Added obey cidefs
    #			Took out the table path name from
    #			the query from clause.  Changed
    #			from $volumn.table_name to table_name.
    #	11/06/97	Took out the CATALOG attribute from
    #			the create table clause.
    #			In the insert clauses, changed insert
    #			values to be the correct data length.
    #			Added a test_dec column to make it easier
    #			following the inserted records sequence.
    # =================== End Test Case Header  ===================
    
    stmt = """create table trunctmp (
two_three_bin      pic S9(2)V9(3) COMP
, smallest_bin       pic SV9(18) COMP
, smallest_dec       pic SV9(18)
, largest_bin        pic S9(18) COMP
, largest_dec        pic S9(18)
, semi_large_bin     pic S9(17) COMP
, semi_large_dec     pic S9(17)
, test_dec		  pic 9(2)
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #  test first field :  +- 2.3 bin
    
    stmt = """set param ?p 0;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p1 1.0001;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """Insert into trunctmp 
values (?p1,?p,?p,?p,?p,?p,?p,1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """set param ?p1 1.1001;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """Insert into trunctmp 
values (?p1,?p,?p,?p,?p,?p,?p,2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """set param ?p1 1.0016;"""
    output = _dci.cmdexec(stmt)
    stmt = """Insert into trunctmp 
values (?p1,?p,?p,?p,?p,?p,?p,3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """set param ?p1 .0001;"""
    output = _dci.cmdexec(stmt)
    stmt = """Insert into trunctmp 
values (?p1,?p,?p,?p,?p,?p,?p,4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    #  second field : +- .18 bin
    
    stmt = """set param ?p 0;"""
    output = _dci.cmdexec(stmt)
    stmt = """Insert into trunctmp 
values (?p,.000000000000000001,?p,?p,?p,?p,?p,5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """Insert into trunctmp 
values (?p,.0000000000000000001,?p,?p,?p,?p,?p,6);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """Insert into trunctmp 
values (?p,.1000000000000000001,?p,?p,?p,?p,?p,7);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """Insert into trunctmp 
values (?p,.1000000000000000016,?p,?p,?p,?p,?p,8);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """set param ?p1 1.1;"""
    output = _dci.cmdexec(stmt)
    stmt = """Insert into trunctmp 
values (?p,?p1,?p,?p,?p,?p,?p,9);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '29188')
    
    stmt = """Insert into trunctmp 
values (?p,1.100000000000000001,?p,?p,?p,?p,?p,10);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8411')
    
    stmt = """set param ?p1 9.9;"""
    output = _dci.cmdexec(stmt)
    stmt = """Insert into trunctmp 
values (?p,?p1,?p,?p,?p,?p,?p,11);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '29188')
    
    #  third field : +- .18 dec
    
    #EL 01/07/98==  Begin==
    # This is the negative test for the param size to be set
    # out of the default limit (18,6).
    stmt = """set param ?p1 .000000000000000001;"""
    output = _dci.cmdexec(stmt)
    stmt = """Insert into trunctmp 
values (?p,?p,?p1,?p,?p,?p,?p,12);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """set param ?p1 .0000000000000000001;"""
    output = _dci.cmdexec(stmt)
    #hpdci has its own implementation for "set param", so won't get warning[8411] as sqlci
    stmt = """Insert into trunctmp 
values (?p,?p,?p1,?p,?p,?p,?p,13);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """set param ?p1 .1000000000000000001;"""
    output = _dci.cmdexec(stmt)
    stmt = """Insert into trunctmp 
values (?p,?p,?p1,?p,?p,?p,?p,14);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """set param ?p1 .1000000000000000016;"""
    output = _dci.cmdexec(stmt)
    stmt = """Insert into trunctmp 
values (?p,?p,?p1,?p,?p,?p,?p,15);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """Insert into trunctmp 
values (0,0,1.1,0,0,0,0,16);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8411')
    
    stmt = """Insert into trunctmp 
values (0,0,1.100000000000000001,0,0,0,0,17);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8411')
    
    #   fourth field : +- 18.0 bin
    
    stmt = """Insert into trunctmp 
values (0,0,0,1000000000000000000,0,0,0,18);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8411')
    
    stmt = """Insert into trunctmp 
values (0,0,0,9900000000000000000,0,0,0,19);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8411')
    
    stmt = """Insert into trunctmp 
values (0,0,0,1.1,0,0,0,20);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """Insert into trunctmp 
values (0,0,0,.1,0,0,0,21);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    #  fifth field +- 18.0 (dec)
    
    stmt = """Insert into trunctmp 
values (0,0,0,0,1000000000000000000,0,0,22);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8411')
    
    stmt = """Insert into trunctmp 
values (0,0,0,0,1.1,0,0,23);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """Insert into trunctmp 
values (0,0,0,0,.1,0,0,24);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    #   sixth field : +- 17.0 bin
    
    stmt = """Insert into trunctmp 
values (?p,?p,?p,?p,?p,100000000000000000,?p,25);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8411')
    
    #   seventh field : +- 17.0 dec
    
    stmt = """Insert into trunctmp 
values (0,0,0,0,0,0,100000000000000000,26);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8411')
    
    stmt = """select * from trunctmp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s13')
    
    stmt = """insert into trunctmp (two_three_bin) values ('12.3');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4039')
    
    stmt = """insert into trunctmp (smallest_bin) values ('99.98');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4039')
    
    stmt = """insert into trunctmp (largest_bin) values ('34.7');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4039')
    
    stmt = """insert into trunctmp (two_three_bin, smallest_bin, largest_bin, test_dec)
values (1.2, 76, 23, '33');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4039')
    
    stmt = """insert into trunctmp (two_three_bin, smallest_bin, largest_bin, test_dec)
values ('1.2', 78, 11, '22');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4039')
    
    #  drop table trunctmp
    stmt = """drop table trunctmp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test009(desc="""a09"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     A09
    #  Description:        This testcase tests assignment truncation
    #                      using UPDATE stmts.
    #
    #  Detail:            Truncation assignment is tested by first creating
    #                     a temporary table, trunctmp, using the
    #                     Test statements that update various values of the
    #                     various columns are run. Only one column is tested
    #                     per test statement - all other column values are
    #                     set to 0.
    #
    #
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    #  Notes:
    #  This test case incorporates features detailed in the "Title"
    #  by Ima Programmer (Version 1.1, <date>).
    #
    #  Revision History:
    #      08/05/96       Converted from REGRESS test library
    #                      sqltsql:sqlqat25:testcase A8
    #	11/04/97	Added obey cidefs.
    #			Took out the table path name from
    #			the query clause.  Changed from
    #			$volumn.table_name to table_name.
    #	11/07/96	Took out the catalog clause from
    #			the create table query clause.
    #			The attribute catalog is not
    #			supported in the create table
    #			clause.
    #			Added the word ATTRIBUTE before
    #			the NO AUDIT option.
    # =================== End Test Case Header  ===================
    
    stmt = """create table trunctmp (
selector           char(1)
, two_three_bin      pic S9(2)V9(3) COMP
, smallest_bin       pic SV9(18) COMP
, smallest_dec       pic SV9(18)
, largest_bin        pic S9(18) COMP
, largest_dec        pic S9(18)
, semi_large_bin     pic S9(17) COMP
, semi_large_dec     pic S9(17)
) no partition
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # insert blank records into table
    
    stmt = """Insert into trunctmp 
values ('A',0,0,0,0,0,0,0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """Insert into trunctmp 
values ('B',0,0,0,0,0,0,0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """Insert into trunctmp 
values ('C',0,0,0,0,0,0,0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """Insert into trunctmp 
values ('D',0,0,0,0,0,0,0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """Insert into trunctmp 
values ('E',0,0,0,0,0,0,0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """Insert into trunctmp 
values ('F',0,0,0,0,0,0,0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """Insert into trunctmp 
values ('G',0,0,0,0,0,0,0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    #   test first field :  +- 2.3 bin
    
    stmt = """set param ?p  1.0001;"""
    output = _dci.cmdexec(stmt)
    stmt = """Update trunctmp 
set two_three_bin = ?p
where selector = 'A';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """set param ?p 1.1001;"""
    output = _dci.cmdexec(stmt)
    stmt = """Update trunctmp 
set two_three_bin = ?p
where selector = 'B';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """Update trunctmp 
set two_three_bin = 1.0016
where selector = 'C';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """Update trunctmp 
set two_three_bin = .0001
where selector = 'D';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    #   second field : +- .18 bin
    
    stmt = """Update trunctmp 
set smallest_bin = .000000000000000001
where selector = 'A';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """Update trunctmp 
set smallest_bin = .000000000000000001
where selector = 'B';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """Update trunctmp 
set smallest_bin = .100000000000000001
where selector = 'C';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """Update trunctmp 
set smallest_bin = .100000000000000016
where selector = 'D';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """Update trunctmp 
set smallest_bin = 1.1
where selector = 'E';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8411')
    
    stmt = """Update trunctmp 
set smallest_bin = 1.100000000000000001
where selector = 'F';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8411')
    
    stmt = """Update trunctmp 
set smallest_bin = 9.9
where selector = 'G';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8411')
    
    #   third field : +- .18 dec
    
    #  smallest_dec should be set to .000000000000000001
    stmt = """set param ?p 1;"""
    output = _dci.cmdexec(stmt)
    stmt = """Update trunctmp 
set smallest_dec = ?p / 100000000000000000
where selector = 'A';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """Update trunctmp 
set smallest_dec = .000000000000000001
where selector = 'B';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """Update trunctmp 
set smallest_dec = .100000000000000001
where selector = 'C';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """Update trunctmp 
set smallest_dec = .100000000000000016
where selector = 'D';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """set param ?p 1.1;"""
    output = _dci.cmdexec(stmt)
    stmt = """Update trunctmp 
set smallest_dec = ?p
where selector = 'E';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '29188')
    
    stmt = """Update trunctmp 
set smallest_dec = 1.100000000000000001
where selector = 'F';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8411')
    
    #   fourth field : +- 18.0 bin
    
    stmt = """Update trunctmp 
set largest_bin = 100000000000000000
where selector = 'A';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """Update trunctmp 
set largest_bin = 990000000000000000
where selector = 'B';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    #  largest_bin should be set to 1.1
    stmt = """set param ?p .1;"""
    output = _dci.cmdexec(stmt)
    stmt = """SET param ?p1 'C';"""
    output = _dci.cmdexec(stmt)
    stmt = """Update trunctmp 
set largest_bin = ?p + 1
where selector = ?p1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """set param ?p .1;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p1 'D';"""
    output = _dci.cmdexec(stmt)
    stmt = """Update trunctmp 
set largest_bin = ?p
where selector = ?p1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    #   fifth field +- 18.0 (dec)
    
    stmt = """Update trunctmp 
set largest_dec = 100000000000000000
where selector = 'A';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """set param ?p 1.1;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p1 'B';"""
    output = _dci.cmdexec(stmt)
    stmt = """Update trunctmp 
set largest_dec = ?p
where selector = ?p1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """set param ?p .1;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p1 'C';"""
    output = _dci.cmdexec(stmt)
    stmt = """Update trunctmp 
set largest_dec = ?p
where selector = ?p1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    #   sixth field : +- 17.0 bin
    
    stmt = """set param ?p  'A';"""
    output = _dci.cmdexec(stmt)
    stmt = """Update trunctmp 
set semi_large_bin = 100000000000000000
where selector = ?p;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8411')
    
    #   seventh field : +- 17.0 dec
    
    stmt = """set param ?p   'A';"""
    output = _dci.cmdexec(stmt)
    stmt = """Update trunctmp 
set semi_large_dec = 100000000000000000
where selector = ?p ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8411')
    
    stmt = """select * from trunctmp for serializable access;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s9')
    
    #   Drop table trunctmp
    stmt = """Drop table trunctmp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test010(desc="""a10"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     A10
    #  Description:        Select into assignment truncation
    #                      test - this tests the accuracy
    #                      of assignment truncation when
    #                      values are selected from a SQL
    #                      table and assigned to a host var.
    #  Detail:             Select into statements are executed for
    #                      various SQL types and host variable types.
    #                      The host variables are then inserted into a
    #                      SQL dummy table which is displayed in
    #                      the display code.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    #  Notes:
    #  This test case incorporates features detailed in the "Title"
    #  by Ima Programmer (Version 1.1, <date>).
    #
    # =================== End Test Case Header  ===================
    
    #  create dummy table seltemp
    stmt = """drop table seltemp;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table seltemp (
test_seq		 pic 9(02)
, two_four_bin       pic S9(2)V9(4) COMP
, zero_eighteen_bin  pic SV9(18) COMP
, zero_eighteen_dec  pic SV9(18)
, eighteen_zero_bin  pic S9(18) COMP
, eighteen_zero_dec  pic S9(18)
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select two_four_bin from """ + gvars.g_schema_arkcasedb + """.btsel27 
where selector = 'A';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s1')
    
    stmt = """select two_four_bin from """ + gvars.g_schema_arkcasedb + """.btsel27 
where selector = 'A';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s2')
    
    stmt = """set param ?twoThreeBinVar 1.1001;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into seltemp values (1,?twoThreeBinVar,0,0,0,0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select two_four_bin from """ + gvars.g_schema_arkcasedb + """.btsel27 
where selector = 'B';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s3')
    
    stmt = """set param ?twoThreeBinVar 1.0016;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into seltemp values (2,?twoThreeBinVar,0,0,0,0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select two_four_bin from """ + gvars.g_schema_arkcasedb + """.btsel27 
where selector = 'C' ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s4')
    
    stmt = """set param ?twoThreeBinVar .0001;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into seltemp values (3,?twoThreeBinVar,0,0,0,0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select one_one_bin from """ + gvars.g_schema_arkcasedb + """.btsel27 
where selector = 'A';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s5')
    
    stmt = """set param ?eighteenZerobinVar 1.1;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into seltemp values (4,0,0,0,?eighteenZeroBinVar,0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '29464')
    
    stmt = """select one_one_bin from """ + gvars.g_schema_arkcasedb + """.btsel27 
where selector = 'B';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s7')
    
    stmt = """set param ?eighteenZeroBinVar .1;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into seltemp values (5,0,0,0,?eighteenZeroBinVar,0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select one_one_bin from """ + gvars.g_schema_arkcasedb + """.btsel27 
where selector = 'A';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s8')
    
    stmt = """set param ?eighteenZeroDecVar 1.1;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into seltemp values (6,0,0,0,0,?eighteenZeroDecVar);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select one_one_bin from """ + gvars.g_schema_arkcasedb + """.btsel27 
where selector = 'B';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s10')
    
    stmt = """set param ?eighteenZeroDecVar .1;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into seltemp values (7,0,0,0,0,?eighteenZeroDecVar);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    #   precision overflow
    
    stmt = """select one_one_bin from """ + gvars.g_schema_arkcasedb + """.btsel27 
where selector = 'A';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s12')
    
    stmt = """set param ?zeroEighteenBinVar 1.1;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into seltemp values (8,0,?zeroEighteenBinVar,0,0,0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '29188')
    
    #   actual overflow
    
    stmt = """select one_one_bin from """ + gvars.g_schema_arkcasedb + """.btsel27 
where selector = 'C';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s14')
    
    stmt = """set param ?zeroEighteenBinVar 9.9;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into seltemp values (9,0,?zeroEighteenBinVar,0,0,0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '29188')
    
    #   actual overflow
    
    stmt = """select one_one_bin from """ + gvars.g_schema_arkcasedb + """.btsel27 
where selector = 'A';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s16')
    
    stmt = """set param ?zeroEighteenDecVar 1.1;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into seltemp values (10,0,?zeroEighteenDecVar,0,0,0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '29188')
    
    #   actual overflow
    
    stmt = """select one_one_bin from """ + gvars.g_schema_arkcasedb + """.btsel27 
where selector = 'C';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s18')
    
    stmt = """set param ?zeroEighteenDecVar 9.9;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into seltemp values (11,0,?zeroEighteenDecVar,0,0,0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '29188')
    
    #   precision overflow
    
    stmt = """select large_bin_1 * 10 from """ + gvars.g_schema_arkcasedb + """.btsel26 
where selector = 'D';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s20')
    
    stmt = """set param ?eighteenZeroBinVar 1000000000000000000;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into seltemp values (12,0,0,0,?eighteenZeroBinVar,0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '29188')
    
    #   actual overflow
    
    stmt = """select large_bin_1 * 10 from """ + gvars.g_schema_arkcasedb + """.btsel26 
where selector = 'D';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s22')
    
    stmt = """set param ?eighteenZeroDecVar 1000000000000000000;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into seltemp values (13,0,0,0,0,?eighteenZeroDecVar);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '29188')
    
    stmt = """select * from seltemp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s24')
    
    stmt = """drop table seltemp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

