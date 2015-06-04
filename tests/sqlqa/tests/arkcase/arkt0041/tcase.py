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
    
def test001(desc="""a02"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     A02
    #  Description:       select expression arithmetic overflow test
    #                     this tests overflow from addition and
    #                     subtraction in select expressions
    #                     of column values only (no literals).
    #
    #                     Testing of overflow from the operations of
    #                     addition and subtraction is tested.  There
    #                     are four different levels of overflow: no
    #                     overflow, possible overflow, precision
    #                     overflow, and actual overflow. Possible overflow
    #                     means the computed precision of the result
    #                     exceeds 18. Precision overflow means that the
    #                     precision of the actual runtime result exceeded
    #                     18, but did not exceed the maximum value that
    #                     can be stored in a binary 64 variable.
    #                     Actual overflow means the actual runtime result
    #                     exceeded the maximum value that can be stored
    #                     in a binary 64 variable. Expressions involving
    #                     only columns are tested. Signed and unsigned
    #                     column values are tested, as are binary and decimal
    #                     column values.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    #  Notes:
    #  This test case incorporates features detailed in the "Title"
    #  by Ima Programmer (Version 1.1, <date>).
    #
    #  Revision History:
    #      07/03/96       Converted from MP test library sqlt041:TESTS:A1
    # =================== End Test Case Header  ===================
    
    #  column/column
    #  signed
    
    #  possible overflow, binary columns, actual values small -> no overflow
    stmt = """select large_bin_1 + large_bin_2
from """ + gvars.g_schema_arkcasedb + """.btsel26 
where selector = 'A';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s0')
    
    #  possible overflow, decimal columns, actual values small ->
    #  no overflow
    stmt = """select large_dec_1 + large_dec_2
from """ + gvars.g_schema_arkcasedb + """.btsel26 
where selector = 'A';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s1')
    
    #  possible overflow, binary columns, actual values large
    #  (result should be one less than precision overflow)
    stmt = """select large_bin_1 + large_bin_2
from """ + gvars.g_schema_arkcasedb + """.btsel26 
where selector = 'D';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s2')
    
    #  same as above, with decimal columns
    stmt = """select large_dec_1 + large_dec_2
from """ + gvars.g_schema_arkcasedb + """.btsel26 
where selector = 'D';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s3')
    
    #  precision overflow, binary columns, result positive
    stmt = """select large_bin_1 + large_bin_2
from """ + gvars.g_schema_arkcasedb + """.btsel26 
where selector = 'B';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s4')
    
    #  precision overflow, decimal columns, result positive
    stmt = """select large_dec_1 + large_dec_2
from """ + gvars.g_schema_arkcasedb + """.btsel26 
where selector = 'B';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s5')
    
    #  precision overflow, binary columns, result negative
    #  (underflow)
    #  large_bin length increased by 1,
    #    -- * 10 to get overflow, 10/11/89
    stmt = """select large_bin_1, large_bin_2,
(large_bin_1 - large_bin_2) * 10
from """ + gvars.g_schema_arkcasedb + """.btsel26 
where selector = 'C';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8411')
    
    #  precision overflow, dec cols, result negative
    #  (underflow)
    #  large_dec length increased by 1,
    #    -- * 10 to get overflow, 10/11/89
    stmt = """select large_dec_1, large_dec_2,
(large_dec_1 - large_dec_2) * 10
from """ + gvars.g_schema_arkcasedb + """.btsel26 
where selector = 'C';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8411')
    
    #  precision overflow, binary columns, scale 18
    #  (add .9 + .2, scales of both = .18)
    stmt = """select small_bin_1 + small_bin_2
from """ + gvars.g_schema_arkcasedb + """.btsel26 
where selector = 'A';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s8')
    
    #  same as above, dec columns
    stmt = """select small_dec_1 + small_dec_2
from """ + gvars.g_schema_arkcasedb + """.btsel26 
where selector = 'A';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s9')
    
    #  precision overflow, binary columns
    stmt = """select small_bin_1 + small_bin_2
from """ + gvars.g_schema_arkcasedb + """.btsel26 
where selector = 'B';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s10')
    
    #  same, dec columns
    stmt = """select small_dec_1 + small_dec_2
from """ + gvars.g_schema_arkcasedb + """.btsel26 
where selector = 'B';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s11')
    
    #  precision overflow, bin columns
    stmt = """select small_bin_1 + small_bin_2
from """ + gvars.g_schema_arkcasedb + """.btsel26 
where selector = 'C';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s12')
    
    #  same , dec columns
    stmt = """select small_dec_1 + small_dec_2
from """ + gvars.g_schema_arkcasedb + """.btsel26 
where selector = 'C';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s13')
    
    #  no overflow possible, bin cols, result positive
    stmt = """select semi_large_bin_1 + semi_large_bin_2
from """ + gvars.g_schema_arkcasedb + """.btsel26 
where selector = 'A';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s14')
    
    #  no overflow possible, bin cols, result negative
    stmt = """select semi_large_bin_1 - semi_large_bin_2
from """ + gvars.g_schema_arkcasedb + """.btsel26 
where selector = 'B';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s15')
    
    #  precision overflow, binary columns
    stmt = """select one_nine_bin + nine_one_bin
from """ + gvars.g_schema_arkcasedb + """.btsel26 
where selector = 'A';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s16')
    
    #  overflow possible, result largest value possible with no
    #  precision overflow
    stmt = """select one_nine_bin + nine_one_bin
from """ + gvars.g_schema_arkcasedb + """.btsel26 
where selector = 'B';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s17')
    
    #  actual overflow, cols bin, result positive
    stmt = """select large_bin_1, small_bin_1,
large_bin_1 + small_bin_1
from """ + gvars.g_schema_arkcasedb + """.btsel26 
where selector = 'B';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s18')
    
    #  same as above, dec cols
    stmt = """select large_dec_1, small_dec_1,
large_dec_1 + small_dec_1
from """ + gvars.g_schema_arkcasedb + """.btsel26 
where selector = 'B';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s19')
    
    #  actual overflow, cols bin, result negative
    #  (underflow)
    stmt = """select large_bin_1, small_bin_1,
large_bin_1 - small_bin_1
from """ + gvars.g_schema_arkcasedb + """.btsel26 
where selector = 'C';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s20')
    
    #  overflow possible (technically but not really), binary cols,
    #  actual values small - no overflow
    stmt = """select nine_zero_bin_u , zero_nine_bin_u,
nine_zero_bin_u + zero_nine_bin_u
from """ + gvars.g_schema_arkcasedb + """.btsel26 
where selector  = 'A';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s21')
    
    #  same as above, dec cols
    stmt = """select nine_zero_dec_u + zero_nine_dec_u
from """ + gvars.g_schema_arkcasedb + """.btsel26 
where selector  = 'A';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s22')
    
    #  possible overflow, bin cols, actual values large
    #  result should be .000 000 001 less than overflow
    stmt = """select nine_zero_bin_u + zero_nine_bin_u
from """ + gvars.g_schema_arkcasedb + """.btsel26 
where selector = 'B';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s23')
    
    #  same as above, dec cols
    stmt = """select nine_zero_dec_u + zero_nine_dec_u
from """ + gvars.g_schema_arkcasedb + """.btsel26 
where selector = 'B';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s24')
    
    #  actual overflow, binary cols
    stmt = """select nine_zero_bin_u + zero_nine_bin_u
+ zero_nine_bin_u
from """ + gvars.g_schema_arkcasedb + """.btsel26 
where selector = 'B';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s25')
    
    #  same as above, dec cols
    stmt = """select nine_zero_dec_u + zero_nine_dec_u
+ zero_nine_dec_u
from """ + gvars.g_schema_arkcasedb + """.btsel26 
where selector = 'B';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s26')
    
    #  precision underflow, bin cols
    #  pic comp length increased by 1,
    #   -- * 10 to get overflow, 10/11/89
    stmt = """select (-nine_zero_bin_u - zero_nine_bin_u
- zero_nine_bin_u) *10
from """ + gvars.g_schema_arkcasedb + """.btsel26 
where selector = 'B';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s27')
    
    _testmgr.testcase_end(desc)

def test002(desc="""a03"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     A03
    #  Description:        This test is Select expression arithmetic
    #                      overflow test - this tests overflow from
    #                      addition and subtraction in select expressions
    #                      of column values and literals, and select
    #                      expressions of literals and literals.
    #
    #                      Testing of overflow from the operations of
    #                      addition and subtraction is tested.
    #                      Expressions involving a column with a literal and
    #                      literal/literal expressions are tested.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    #  Notes:
    #  This test case incorporates features detailed in the "Title"
    #  by Ima Programmer (Version 1.1, <date>).
    #
    #  Revision History:
    #      07/03/96       Converted from MP test library sqlt041:TESTS:A2
    # =================== End Test Case Header  ===================
    
    #  column/literal
    
    #  precision overflow, binary column
    #  add .9 + .2, scale of column = .18
    stmt = """select small_bin_1 + .200000000000000000
from """ + gvars.g_schema_arkcasedb + """.btsel26 
where selector = 'A';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s0')
    
    #  precision overflow, binary column
    #  add .9 + .2, scale of column = .18, scale of literal = 1
    stmt = """select small_bin_1 + .2
from """ + gvars.g_schema_arkcasedb + """.btsel26 
where selector = 'A';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s1')
    
    #  precision overflow, dec column
    stmt = """select small_dec_1 + .000000000000000001
from """ + gvars.g_schema_arkcasedb + """.btsel26 
where selector = 'B';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s2')
    
    #  precision overflow, dec column
    stmt = """select small_dec_1 + .000000000000000002
from """ + gvars.g_schema_arkcasedb + """.btsel26 
where selector = 'C';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s3')
    
    #  literal/literal
    
    #  precision overflow ?
    stmt = """select .900000000000000000 + .200000000000000000
from """ + gvars.g_schema_arkcasedb + """.btsel26;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s4')
    
    #  precision overflow
    stmt = """select .999999999999999999 + .000000000000000001
from """ + gvars.g_schema_arkcasedb + """.btsel26;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s5')
    
    #  precision overflow
    stmt = """select .999999999999999999 + .000000000000000002
from """ + gvars.g_schema_arkcasedb + """.btsel26 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s6')
    
    #  actual overflow
    stmt = """select 10.0 + .900000000000000000
from """ + gvars.g_schema_arkcasedb + """.btsel26;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s7')
    
    #  literal exceeding 18 digits error
    stmt = """select .90000000000000000000
from """ + gvars.g_schema_arkcasedb + """.btsel26;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s8')
    
    #  literal exceeding 18 digits error
    stmt = """select 10.999999999999999999
from """ + gvars.g_schema_arkcasedb + """.btsel26;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s9')
    
    _testmgr.testcase_end(desc)

def test003(desc="""a06"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     A06
    #  Description:       This testcase is an arithmetic overflow test
    #                     for aggregates.
    #
    #                     min, max, count are tested to ensure the proper
    #                     precision and scale of the result. Note no
    #                     overflow is possible for these aggregates.
    #                     Most of the tests here are for SUM and
    #                     AVG. For SUM - there are two kinds of overflow
    #                     - overflow in the computation and overflow
    #                     in the result. Note that there can never be
    #                     overflow in the result for AVG.
    #  Test case inputs:  Global Database objects.
    #  Test case outputs: Displays the selected objects.
    #  Expected Results:  Same as above.
    #
    #  Notes:
    #  This test case incorporates features detailed in the "Title"
    #  by Ima Programmer (Version 1.1, <date>).
    #
    #  Revision History:
    #      07/03/96       Converted from MP test library sqlt041:TESTS:A5
    # =================== End Test Case Header  ===================
    
    #  MAX, MIN
    #  max, scale = 0
    
    stmt = """select max(large_bin_1)
from """ + gvars.g_schema_arkcasedb + """.btsel26;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s0')
    
    #  max, scale = 9
    stmt = """select max(one_nine_bin)
from """ + gvars.g_schema_arkcasedb + """.btsel26;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s1')
    
    #  min, scale = 0
    stmt = """select min(large_bin_1)
from """ + gvars.g_schema_arkcasedb + """.btsel26;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s2')
    
    #  min, scale = 9
    stmt = """select min(one_nine_bin)
from """ + gvars.g_schema_arkcasedb + """.btsel26;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s3')
    
    #  COUNT
    
    #  count, original scale = 0
    stmt = """select count(distinct large_bin_1)
from """ + gvars.g_schema_arkcasedb + """.btsel26;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s4')
    
    #  count, original scale = 9
    stmt = """select count(distinct one_nine_bin)
from """ + gvars.g_schema_arkcasedb + """.btsel26;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s5')
    
    #  count(*)
    stmt = """select count(*)
from """ + gvars.g_schema_arkcasedb + """.btsel26;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s6')
    
    #  SUM
    
    #  sum, no overflow, scale = 0
    stmt = """select sum(semi_large_bin_1)
from """ + gvars.g_schema_arkcasedb + """.btsel26;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s7')
    
    #  sum, no overflow in result, overflow possible in calculation
    stmt = """select sum(large_bin_1)
from """ + gvars.g_schema_arkcasedb + """.btsel26 
where (selector <> 'O') and (selector <>  'P');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s8')
    
    #  sum, no underflow in result, underflow possible in calculation
    #  large_bin length increased by 1,
    #    -- * 10 to get overflow, 10/11/89
    stmt = """select sum(-large_bin_1) * 10
from """ + gvars.g_schema_arkcasedb + """.btsel26 
where (selector <> 'O') and (selector <> 'P');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8411')
    
    #  sum, no overflow, scale > 0
    stmt = """select sum(small_dec_2)
from """ + gvars.g_schema_arkcasedb + """.btsel26;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s10')
    
    #  sum, overflow in calculation and result, scale > 0
    stmt = """select sum(small_dec_1)
from """ + gvars.g_schema_arkcasedb + """.btsel26;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8411')
    
    #  AVG
    
    #  avg, no overflow, scale = 0
    stmt = """select avg(semi_large_bin_1)
from """ + gvars.g_schema_arkcasedb + """.btsel26;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s12')
    
    #  avg, no overflow in result, overflow in calculation
    #  (impossible to get overflow in result)
    stmt = """select avg(large_bin_1)
from """ + gvars.g_schema_arkcasedb + """.btsel26 
where (selector <> 'C') and (selector <> 'O') and (selector <>  'P');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8411')
    
    #  avg, underflow in calculation
    stmt = """select avg(-large_bin_1)
from """ + gvars.g_schema_arkcasedb + """.btsel26 
where (selector <> 'C') and (selector <> 'O') and (selector <> 'P');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s14')
    
    #  avg, no overflow, scale > 0
    stmt = """select avg(small_dec_2)
from """ + gvars.g_schema_arkcasedb + """.btsel26;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s15')
    
    #  avg, overflow in calculation , scale > 0
    stmt = """select avg(small_dec_1)
from """ + gvars.g_schema_arkcasedb + """.btsel26;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8411')
    
    #  SUM, overflow based on order records are evaluated
    
    #  sum, overflow in calculation or result IF the calculation
    #  is done in 'insertion' order (file with SYSKEY)
    stmt = """select sum(large_dec_1)
from """ + gvars.g_schema_arkcasedb + """.btsel26;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s17')
    
    #  sum, no overflow in result, overflow in calculation
    #  IF the calculation done based on alternate index on large_dec_1
    stmt = """select sum(large_dec_1)
from """ + gvars.g_schema_arkcasedb + """.btsel26 
where large_dec_1 <> 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s18')
    
    _testmgr.testcase_end(desc)

def test004(desc="""a07"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     A07
    #  Description:        This testcase tests type propagation of
    #                      expressions.
    #                      Type propagation tests are conducted for
    #                      various data types and resultant data types
    #  Test case inputs:   Global Database objects.
    #  Test case outputs:  Displays the selected objects.
    #  Expected Results:   Same as above.
    #
    #  Notes:
    #  This test case incorporates features detailed in the "Title"
    #  by Ima Programmer (Version 1.1, <date>).
    #
    #  Revision History:
    #      07/03/96       Converted from MP test library sqlt041:TESTS:A6
    # =================== End Test Case Header  ===================
    
    #  sbin data
    
    #  result bin 16
    #  p = 3, s = 2
    stmt = """select pic_comp_2 + pic_comp_2
from """ + gvars.g_schema_arkcasedb + """.btsel01 
where binary_signed = 60;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s0')
    
    #  result bin 16
    #  p = 4, s = 4
    stmt = """select pic_comp_2 * pic_comp_2
from """ + gvars.g_schema_arkcasedb + """.btsel01 
where binary_signed = 60;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s1')
    
    #  result bin 32
    #  p = 9, s = 0
    stmt = """select (binary_signed + small_int) * small_int
from """ + gvars.g_schema_arkcasedb + """.btsel01 
where binary_signed = 60;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s2')
    
    #  result bin 64
    #  p = 18, s = 8
    stmt = """select (binary_signed + small_int) / binary_64_s
from """ + gvars.g_schema_arkcasedb + """.btsel01 
where binary_signed = 60;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s3')
    
    #  unsigned data
    
    #  result bin 16
    #  p = 4, s = 0
    stmt = """select decimal_3_unsigned + decimal_3_unsigned
from """ + gvars.g_schema_arkcasedb + """.btsel01 
where binary_signed = 60;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s4')
    
    #  result bin 32
    #  p = 9, s = 0
    stmt = """select (col_2 + col_7) * col_6
from """ + gvars.g_schema_arkcasedb + """.btsel06 
where pic_x_b = 'Q';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s5')
    
    #  result bin 64
    #  p = 12, s = 2
    stmt = """select binary_32_u * decimal_3_unsigned
from """ + gvars.g_schema_arkcasedb + """.btsel01 
where binary_signed = 60;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s6')
    
    #  sdec data
    
    #  result bin 16
    #  p =   3, s = 1
    stmt = """select pic_decimal_1 - pic_decimal_3
from """ + gvars.g_schema_arkcasedb + """.btsel01 
where pic_decimal_1 = 1.1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s7')
    
    #  result bin 32
    #  p = 9, s = 0
    stmt = """select col_9 * col_10 + col_9
from """ + gvars.g_schema_arkcasedb + """.btsel06 
where pic_x_b = 'Q';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s8')
    
    #  result bin 64
    #  p = 18, s = 9
    stmt = """select col_47 / col_48 * col_70
from """ + gvars.g_schema_arkcasedb + """.btsel06 
where pic_x_b = 'Q';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s9')
    
    #  constant data
    
    #  result bin 16
    #  p = 4, s = 2
    stmt = """select decimal_2_signed + 4.7
from """ + gvars.g_schema_arkcasedb + """.btsel01 
where binary_32_u = 60;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s10')
    
    #  result bin 32
    #  p = 8, s = 2
    stmt = """select decimal_3_unsigned * 9.08 + 10000
from """ + gvars.g_schema_arkcasedb + """.btsel01 
where binary_32_u = 60;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s11')
    
    #  result bin 64
    #  p = 18, s = 16
    stmt = """select (17.496 / 85) + (63 * medium_int) - small_int
from """ + gvars.g_schema_arkcasedb + """.btsel01 
where binary_32_u = 60;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s12')
    
    #  mixed/complex/aggregates
    
    #  result bin 16
    stmt = """select pic_comp_2 - decimal_2_signed * pic_decimal_3
from """ + gvars.g_schema_arkcasedb + """.btsel01 
where binary_32_u = 60;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s13')
    
    #  result bin 16
    stmt = """select max(pic_comp_2) - min(decimal_2_signed) *
max(pic_decimal_3)
from """ + gvars.g_schema_arkcasedb + """.btsel01 
where binary_32_u = 60;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s14')
    
    #  result bin 32
    stmt = """select decimal_3_unsigned + small_int - decimal_1
from """ + gvars.g_schema_arkcasedb + """.btsel01 
where binary_32_u = 60;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s15')
    
    #  result bin 64
    stmt = """select ((decimal_1 + decimal_3_unsigned) *
binary_32_u - pic_comp_2
) / pic_comp_1 + pic_comp_3 * decimal_2_signed
from """ + gvars.g_schema_arkcasedb + """.btsel01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s16')
    
    #  result bin 64
    stmt = """select sum(pic_comp_3) + sum(large_int) + avg(binary_32_u)
from """ + gvars.g_schema_arkcasedb + """.btsel01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s17')
    
    _testmgr.testcase_end(desc)

