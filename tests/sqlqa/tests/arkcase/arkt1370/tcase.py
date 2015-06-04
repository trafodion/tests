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
    #  Test case name:     arkt1370 : A01
    #  Original Test case: arkt0008 : A01
    #  Description:        This test verifies the SQL SELECT
    #                      statement using SELECT [FIRST <N>]
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    
    #      -- TESTCASE SUMMARY
    #         Select a column from base tables,
    #         protection views, shorthand views.
    #
    #          normal simple select test - select a column from base
    #          tables, protection views, shorthand views.
    #
    #          This testcase selects a random column from base tables
    #          1-11, protection views 1-4 and shorthand views 11-15. base
    #          tables 1 and 6 have all their column types selected to
    #          check that select works on all column types.
    #
    #
    
    stmt = """select [first 4]  char_1 from """ + gvars.g_schema_arkcasedb + """.btsel01 
order by binary_signed;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s0')
    stmt = """select [first 4]  pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel01 
order by binary_signed;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s1')
    stmt = """select [first 4]  pic_x_1,pic_x_7 from """ + gvars.g_schema_arkcasedb + """.btsel01 
order by binary_signed;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s2')
    stmt = """select [first 4]  pic_x_7,pic_x_7 from """ + gvars.g_schema_arkcasedb + """.btsel01 
order by binary_signed;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s3')
    stmt = """select [first 4]  pic_x_7,binary_64_s,decimal_1
from """ + gvars.g_schema_arkcasedb + """.btsel01 
order by binary_signed;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s4')
    stmt = """select [first 4]  pic_x_long from """ + gvars.g_schema_arkcasedb + """.btsel01 
order by binary_signed;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s5')
    stmt = """select [first 4]  var_char from """ + gvars.g_schema_arkcasedb + """.btsel01 
order by binary_signed;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s6')
    stmt = """select [first 4]  binary_signed from """ + gvars.g_schema_arkcasedb + """.btsel01 
order by binary_signed;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s7')
    stmt = """select [first 4]  binary_32_u from """ + gvars.g_schema_arkcasedb + """.btsel01 
order by binary_signed;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s8')
    stmt = """select [first 4]  binary_64_s from """ + gvars.g_schema_arkcasedb + """.btsel01 
order by binary_signed;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s9')
    stmt = """select [first 4]  pic_comp_1 from """ + gvars.g_schema_arkcasedb + """.btsel01 
order by binary_signed;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s10')
    stmt = """select [first 4]  pic_comp_2 from """ + gvars.g_schema_arkcasedb + """.btsel01 
order by binary_signed;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s11')
    stmt = """select [first 4]  pic_comp_3 from """ + gvars.g_schema_arkcasedb + """.btsel01 
order by binary_signed;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s12')
    stmt = """select [first 4]  small_int from """ + gvars.g_schema_arkcasedb + """.btsel01 
order by binary_signed;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s13')
    stmt = """select [first 4]  medium_int from """ + gvars.g_schema_arkcasedb + """.btsel01 
order by binary_signed;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s14')
    stmt = """select [first 4]  large_int from """ + gvars.g_schema_arkcasedb + """.btsel01 
order by binary_signed;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s15')
    stmt = """select [first 4]  decimal_1 from """ + gvars.g_schema_arkcasedb + """.btsel01 
order by binary_signed;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s16')
    stmt = """select [first 4]  decimal_2_signed from """ + gvars.g_schema_arkcasedb + """.btsel01 
order by binary_signed;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s17')
    stmt = """select [first 4]  decimal_3_unsigned from """ + gvars.g_schema_arkcasedb + """.btsel01 
order by binary_signed;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s18')
    stmt = """select [first 4]  pic_decimal_1 from """ + gvars.g_schema_arkcasedb + """.btsel01 
order by binary_signed;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s19')
    stmt = """select [first 4]  pic_decimal_2 from """ + gvars.g_schema_arkcasedb + """.btsel01 
order by binary_signed;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s20')
    stmt = """select [first 4]  pic_decimal_3 from """ + gvars.g_schema_arkcasedb + """.btsel01 
order by binary_signed;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s21')
    stmt = """select [first 4]  pic_x_a from """ + gvars.g_schema_arkcasedb + """.btsel06 
order by pic_x_a, pic_x_b, pic_x_c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s22')
    stmt = """select [first 4]  pic_x_b from """ + gvars.g_schema_arkcasedb + """.btsel06 
order by pic_x_a, pic_x_b, pic_x_c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s23')
    stmt = """select [first 4]  pic_x_c from """ + gvars.g_schema_arkcasedb + """.btsel06 
order by pic_x_a, pic_x_b, pic_x_c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s24')
    stmt = """select [first 4]  col_1 from """ + gvars.g_schema_arkcasedb + """.btsel06 
order by pic_x_a, pic_x_b, pic_x_c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s25')
    stmt = """select [first 4]  col_3 from """ + gvars.g_schema_arkcasedb + """.btsel06 
order by pic_x_a, pic_x_b, pic_x_c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s26')
    stmt = """select [first 4]  col_5 from """ + gvars.g_schema_arkcasedb + """.btsel06 
order by pic_x_a, pic_x_b, pic_x_c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s27')
    stmt = """select [first 4]  col_7 from """ + gvars.g_schema_arkcasedb + """.btsel06 
order by pic_x_a, pic_x_b, pic_x_c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s28')
    stmt = """select [first 4]  col_21 from """ + gvars.g_schema_arkcasedb + """.btsel06 
order by pic_x_a, pic_x_b, pic_x_c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s29')
    stmt = """select [first 4]  col_23 from """ + gvars.g_schema_arkcasedb + """.btsel06 
order by pic_x_a, pic_x_b, pic_x_c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s30')
    stmt = """select [first 4]  col_25 from """ + gvars.g_schema_arkcasedb + """.btsel06 
order by pic_x_a, pic_x_b, pic_x_c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s31')
    stmt = """select [first 4]  col_27 from """ + gvars.g_schema_arkcasedb + """.btsel06 
order by pic_x_a, pic_x_b, pic_x_c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s32')
    stmt = """select [first 4]  col_29 from """ + gvars.g_schema_arkcasedb + """.btsel06 
order by pic_x_a, pic_x_b, pic_x_c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s33')
    stmt = """select [first 4]  col_41 from """ + gvars.g_schema_arkcasedb + """.btsel06 
order by pic_x_a, pic_x_b, pic_x_c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s34')
    stmt = """select [first 4]  col_43 from """ + gvars.g_schema_arkcasedb + """.btsel06 
order by pic_x_a, pic_x_b, pic_x_c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s35')
    stmt = """select [first 4]  col_45 from """ + gvars.g_schema_arkcasedb + """.btsel06 
order by pic_x_a, pic_x_b, pic_x_c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s36')
    stmt = """select [first 4]  col_47 from """ + gvars.g_schema_arkcasedb + """.btsel06 
order by pic_x_a, pic_x_b, pic_x_c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s37')
    stmt = """select [first 4]  col_61 from """ + gvars.g_schema_arkcasedb + """.btsel06 
order by pic_x_a, pic_x_b, pic_x_c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s38')
    stmt = """select [first 4]  col_63 from """ + gvars.g_schema_arkcasedb + """.btsel06 
order by pic_x_a, pic_x_b, pic_x_c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s39')
    stmt = """select [first 4]  col_65 from """ + gvars.g_schema_arkcasedb + """.btsel06 
order by pic_x_a, pic_x_b, pic_x_c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s40')
    stmt = """select [first 4]  col_67 from """ + gvars.g_schema_arkcasedb + """.btsel06 
order by pic_x_a, pic_x_b, pic_x_c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s41')
    stmt = """select [first 4]  col_69 from """ + gvars.g_schema_arkcasedb + """.btsel06 
order by pic_x_a, pic_x_b, pic_x_c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s42')
    stmt = """select [first 4]  pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
order by syskey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s43')
    stmt = """select [first 4]  binary_32_u from """ + gvars.g_schema_arkcasedb + """.btsel03 
order by syskey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s44')
    stmt = """select [first 4]  var_char from """ + gvars.g_schema_arkcasedb + """.btsel04 
order by syskey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s45')
    stmt = """select [first 4]  col_4 from """ + gvars.g_schema_arkcasedb + """.btsel05 
order by syskey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s46')
    stmt = """select [first 4]  pic_x_c from """ + gvars.g_schema_arkcasedb + """.btsel07 
order by pic_x_c, pic_x_b, pic_x_a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s47')
    stmt = """select [first 4]  pic_252 from """ + gvars.g_schema_arkcasedb + """.btsel08 
order by large_int;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s48')
    stmt = """select [first 4]  pic_x_7 from """ + gvars.g_schema_arkcasedb + """.btsel09 
order by pic_x_a desc, pic_x_6 desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s49')
    stmt = """select [first 4]  binary_32_signed from """ + gvars.g_schema_arkcasedb + """.btsel10 
order by pic_9_7 asc, pic_x_7 desc, pic_x_a asc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s50')
    stmt = """select [first 4]  char_10 from """ + gvars.g_schema_arkcasedb + """.btsel11 
order by decimal_10 desc, pic_x_a asc, pic_9_7 desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s51')
    stmt = """select [first 4]  medium_int from """ + gvars.g_schema_arkcasedb + """.pvsel01 
order by pic_decimal_3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s52')
    stmt = """select [first 4]  pic_x_1 from """ + gvars.g_schema_arkcasedb + """.pvsel02 
order by pic_x_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s53')
    stmt = """select [first 4]  new_name_2 from """ + gvars.g_schema_arkcasedb + """.pvsel03 
order by new_name_4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s54')
    stmt = """select [first 4]  pic_comp_1 from """ + gvars.g_schema_arkcasedb + """.pvsel04 
order by pic_comp_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s55')
    stmt = """select [first 4]  col_4 from """ + gvars.g_schema_arkcasedb + """.svsel11 
order by col_4, col_8;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s56')
    stmt = """select [first 4]  new_name_3 from """ + gvars.g_schema_arkcasedb + """.svsel13 
order by new_name_4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s57')
    stmt = """select [first 4]  new_name_1 from """ + gvars.g_schema_arkcasedb + """.svsel14 
order by new_name_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s58')
    
    _testmgr.testcase_end(desc)

def test002(desc="""a02"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt1370 : A02
    #  Original Test case: arkt0008 : A02
    #  Description:        This test verifies the SQL SELECT
    #                      statement using SELECT [FIRST <N>]
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    
    stmt = """select [first 3] SYSKEY from """ + gvars.g_schema_arkcasedb + """.btsel02 
order by syskey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 3)
    
    stmt = """select [first 3] *,SYSKEY from """ + gvars.g_schema_arkcasedb + """.btsel02 
order by syskey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 3)
    
    stmt = """select [first 3] SYSKEY from """ + gvars.g_schema_arkcasedb + """.btsel03 
order by syskey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 3)
    
    stmt = """select [first 3] SYSKEY,* from """ + gvars.g_schema_arkcasedb + """.btsel03 
order by syskey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 3)
    
    stmt = """select [first 3] SYSKEY from """ + gvars.g_schema_arkcasedb + """.btsel04 
order by syskey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 3)
    
    stmt = """select [first 3] *,SYSKEY from """ + gvars.g_schema_arkcasedb + """.btsel04 
order by syskey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 3)
    
    stmt = """select [first 3] SYSKEY, 'anchor literal for SYSKEY'
from """ + gvars.g_schema_arkcasedb + """.btsel05 
order by syskey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 3)
    
    stmt = """select [first 3] *,SYSKEY, 'anchor literal for SYSKEY'
from """ + gvars.g_schema_arkcasedb + """.btsel05 
order by syskey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 3)
    
    stmt = """select [first 3] new_name_4 from """ + gvars.g_schema_arkcasedb + """.pvsel03 
order by new_name_4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 3)
    
    stmt = """select [first 3] new_name_4 from """ + gvars.g_schema_arkcasedb + """.svsel13 
order by new_name_4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 3)
    
    stmt = """select [first 3] new_name_1,new_name_4 from """ + gvars.g_schema_arkcasedb + """.pvsel03 
order by new_name_4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 3)
    
    stmt = """select [first 3] new_name_1,new_name_4 from """ + gvars.g_schema_arkcasedb + """.svsel13 
order by new_name_4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 3)
    
    stmt = """select [first 3] new_name_1,new_name_4 , new_name_2,
(new_name_4 * new_name_2)
from """ + gvars.g_schema_arkcasedb + """.pvsel03 
order by new_name_4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 3)
    
    stmt = """select [first 3] new_name_1,(new_name_4 + 100) from """ + gvars.g_schema_arkcasedb + """.svsel13 
order by new_name_4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 3)
    
    _testmgr.testcase_end(desc)

def test003(desc="""a03"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt1370 : A03
    #  Original Test case: arkt0008 : A03
    #  Description:        This test verifies the SQL SELECT
    #                      statement using SELECT [FIRST <N>]
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    
    stmt = """select [first 4] medium_int,medium_int
from """ + gvars.g_schema_arkcasedb + """.btsel01 
order by binary_signed;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s0')
    
    stmt = """select [first 4] distinct (medium_int * medium_int)
from """ + gvars.g_schema_arkcasedb + """.btsel01 
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s1')
    stmt = """select [first 4] all (medium_int * medium_int)
from """ + gvars.g_schema_arkcasedb + """.btsel01 
order by binary_signed;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s2')
    stmt = """select [first 4] +large_int from """ + gvars.g_schema_arkcasedb + """.btsel01 
order by binary_signed;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s3')
    stmt = """select [first 4] (+large_int) from """ + gvars.g_schema_arkcasedb + """.btsel01 
order by binary_signed;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s4')
    stmt = """select [first 4] -large_int from """ + gvars.g_schema_arkcasedb + """.btsel01 
order by binary_signed;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s5')
    stmt = """select [first 4] (-large_int) from """ + gvars.g_schema_arkcasedb + """.btsel01 
order by binary_signed;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s6')
    stmt = """select [first 4] (binary_32_u*2) from """ + gvars.g_schema_arkcasedb + """.btsel01 
order by binary_signed;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s7')
    stmt = """select [first 4] pic_9_7+binary_64_s from """ + gvars.g_schema_arkcasedb + """.btsel03 
order by syskey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s8')
    stmt = """select [first 4] medium_int - 100,pic_comp_1 - 100
from """ + gvars.g_schema_arkcasedb + """.btsel04 
order by syskey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s9')
    stmt = """select [first 4] (pic_x_5 / 2),pic_x_6 from """ + gvars.g_schema_arkcasedb + """.btsel09 
order by pic_x_a desc, pic_x_6 desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s10')
    stmt = """select [first 4] (decimal_10 + binary_unsigned),(binary_unsigned +
binary_32_signed) from """ + gvars.g_schema_arkcasedb + """.btsel10 
order by pic_9_7 asc, pic_x_7 desc, pic_x_a asc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s11')
    stmt = """select [first 4] (decimal_10 + 100) from """ + gvars.g_schema_arkcasedb + """.btsel11 
order by decimal_10 desc, pic_x_a asc, pic_9_7 desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s12')
    stmt = """select [first 4] (new_name_1 - 1000),(new_name_2 + 1000)
from """ + gvars.g_schema_arkcasedb + """.svsel13 
order by new_name_4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s13')
    stmt = """select [first 4] (medium_int * pic_comp_1) from """ + gvars.g_schema_arkcasedb + """.pvsel04 
order by pic_comp_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s14')
    stmt = """select [first 4] 'large_int = ',large_int
from """ + gvars.g_schema_arkcasedb + """.btsel01 
order by binary_signed;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s15')
    stmt = """select [first 4] medium_int,'char_1 = ',char_1
from """ + gvars.g_schema_arkcasedb + """.btsel01 
order by binary_signed;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s16')
    stmt = """select [first 4] '100 =',100,'small_int =',small_int
from """ + gvars.g_schema_arkcasedb + """.btsel01 
order by binary_signed;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s17')
    stmt = """select [first 4] '100 * 10 =',100 * 10,'small_int =',small_int
from """ + gvars.g_schema_arkcasedb + """.btsel01 
order by binary_signed;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s18')
    stmt = """select [first 4] 'only a constant'
from """ + gvars.g_schema_arkcasedb + """.btsel01 
order by binary_signed;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s19')
    
    stmt = """select [first 4] ''
from """ + gvars.g_schema_arkcasedb + """.btsel01 
order by binary_signed;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s20')
    
    stmt = """select [first 4] ''
from """ + gvars.g_schema_arkcasedb + """.btsel01 
order by binary_signed;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s21')
    
    _testmgr.testcase_end(desc)

def test004(desc="""a04"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt1370 : A04
    #  Original Test case: arkt0008 : A04
    #  Description:        This test verifies the SQL SELECT
    #                      statement using SELECT [FIRST <N>]
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    
    #  *** audited tables ***
    stmt = """select [first 6] * from """ + gvars.g_schema_arkcasedb + """.btsel01 
for read uncommitted access
order by binary_signed;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s0')
    
    stmt = """select [first 6] * from """ + gvars.g_schema_arkcasedb + """.btsel02 
for read committed access
order by syskey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s1')
    
    stmt = """select [first 6] * from """ + gvars.g_schema_arkcasedb + """.btsel03 
for serializable access
order by syskey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s2')
    
    #   *** non-audited table ***
    
    stmt = """select [first 6] * from """ + gvars.g_schema_arkcasedb + """.btsel05 
for read uncommitted access
order by syskey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s3')
    
    stmt = """select [first 6] * from """ + gvars.g_schema_arkcasedb + """.btsel05 
for read committed access
order by syskey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s4')
    
    stmt = """select [first 6] * from """ + gvars.g_schema_arkcasedb + """.btsel05 
for serializable access
order by syskey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s5')
    
    #   *** views ***
    
    stmt = """select [first 6] * from """ + gvars.g_schema_arkcasedb + """.pvsel01 
for read uncommitted access
order by pic_decimal_3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s6')
    
    stmt = """select [first 6] * from """ + gvars.g_schema_arkcasedb + """.pvsel01 
for read committed access
order by pic_decimal_3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s7')
    
    stmt = """select [first 6] * from """ + gvars.g_schema_arkcasedb + """.pvsel01 
for serializable access
order by pic_decimal_3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s8')
    
    #  svsel15 must be accessed for read uncommitted access (mixed view)
    stmt = """select [first 6] * from """ + gvars.g_schema_arkcasedb + """.svsel15 
for read uncommitted access
order by mixed_13;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s9')
    
    stmt = """select [first 6] * from """ + gvars.g_schema_arkcasedb + """.svsel14 
for read uncommitted access
order by new_name_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s10')
    
    stmt = """select [first 6] * from """ + gvars.g_schema_arkcasedb + """.svsel13 
for read uncommitted access
order by new_name_4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 4)
    
    _testmgr.testcase_end(desc)

def test005(desc="""a05"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt1370 : A05
    #  Original Test case: arkt0008 : A05
    #  Description:        This test verifies the SQL SELECT
    #                      statement using SELECT [FIRST <N>]
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    
    #  select ALL
    stmt = """select [first 1] count(*)
from """ + gvars.g_schema_arkcasedb + """.btsel01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s0')
    
    stmt = """select [first 1] avg(medium_int)
from """ + gvars.g_schema_arkcasedb + """.pvsel01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s1')
    
    #  test use of white space inside aggregate
    stmt = """select [first 1] avg (ALL pic_comp_1)
from """ + gvars.g_schema_arkcasedb + """.svsel13;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s2')
    
    stmt = """select [first 1] max(
binary_64_s)
from """ + gvars.g_schema_arkcasedb + """.btsel01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s3')
    
    stmt = """select [first 1] max(ALL
large_int)
from """ + gvars.g_schema_arkcasedb + """.pvsel01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s4')
    
    stmt = """select [first 1] min(col_2
)
from """ + gvars.g_schema_arkcasedb + """.svsel11;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s5')
    
    stmt = """select [first 1] min
(ALL decimal_2_signed)
from """ + gvars.g_schema_arkcasedb + """.btsel01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s6')
    
    stmt = """select [first 1] sum(new_name_2)
from """ + gvars.g_schema_arkcasedb + """.pvsel03;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s7')
    
    stmt = """select [first 1] sum(ALL col_4)
from """ + gvars.g_schema_arkcasedb + """.svsel11;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s8')
    
    stmt = """select [first 1] max(pic_x_1)
from """ + gvars.g_schema_arkcasedb + """.btsel02;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s9')
    
    stmt = """select [first 1] max(ALL new_name_3)
from """ + gvars.g_schema_arkcasedb + """.pvsel03;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s10')
    
    stmt = """select [first 1] min(var_char)
from """ + gvars.g_schema_arkcasedb + """.svsel13;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s11')
    
    stmt = """select [first 1] min(ALL pic_x_a)
from """ + gvars.g_schema_arkcasedb + """.btsel05;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s12')
    
    #  select [first 1] DISTINCT
    stmt = """select [first 1] AVG(distinct binary_32_u)
from """ + gvars.g_schema_arkcasedb + """.btsel01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s13')
    
    stmt = """select [first 1] MAX(distinct medium_int)
from """ + gvars.g_schema_arkcasedb + """.pvsel01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s14')
    
    stmt = """select [first 1] MIN(distinct new_name_1)
from """ + gvars.g_schema_arkcasedb + """.svsel13;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s15')
    
    stmt = """select [first 1] SUM(distinct binary_64_s)
from """ + gvars.g_schema_arkcasedb + """.btsel01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s16')
    
    stmt = """select [first 1] count(distinct medium_int)
from """ + gvars.g_schema_arkcasedb + """.pvsel01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s17')
    
    stmt = """select [first 1] count(distinct var_char)
from """ + gvars.g_schema_arkcasedb + """.svsel13;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s18')
    
    stmt = """select [first 1] max(distinct pic_x_long)
from """ + gvars.g_schema_arkcasedb + """.btsel01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s19')
    
    stmt = """select [first 1] min(distinct var_char)
from """ + gvars.g_schema_arkcasedb + """.btsel01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s20')
    
    #  select [first 1] an expression inside an aggregate
    stmt = """select [first 1] avg(binary_32_u * 2)
from """ + gvars.g_schema_arkcasedb + """.btsel01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s21')
    
    stmt = """select [first 1] avg(ALL binary_32_u + pic_comp_1)
from """ + gvars.g_schema_arkcasedb + """.btsel01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s22')
    
    stmt = """select [first 1] max(new_name_1 * new_name_1)
from """ + gvars.g_schema_arkcasedb + """.pvsel03;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s23')
    
    stmt = """select [first 1] max(ALL new_name_1 / new_name_2)
from """ + gvars.g_schema_arkcasedb + """.svsel13;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s24')
    
    stmt = """select [first 1] min((-binary_signed) - decimal_3_unsigned)
from """ + gvars.g_schema_arkcasedb + """.btsel01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s25')
    
    stmt = """select [first 1] min(ALL large_int * small_int)
from """ + gvars.g_schema_arkcasedb + """.pvsel01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s26')
    
    stmt = """select [first 1] sum ((col_1 + col_4) + 1000)
from """ + gvars.g_schema_arkcasedb + """.svsel11;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s27')
    
    stmt = """select [first 1] sum(ALL -1000 + small_int)
from """ + gvars.g_schema_arkcasedb + """.btsel01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s28')
    
    #  The table btsel03 is created on without STORE BY ENTRY ORDER,
    #  so the SYSKEY has a large number.  Should see ERROR[8411] for
    #  now.  Plan to create it with STORE BY ENTRY ORDER when MX
    #  supports DDL.
    #  select [first 1] an expression with SYSKEY in an aggregate
    stmt = """select [first 1] avg(SYSKEY + binary_64_s)
from """ + gvars.g_schema_arkcasedb + """.btsel03;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select [first 1] max(SYSKEY / 3 + medium_int)
from """ + gvars.g_schema_arkcasedb + """.btsel04;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select [first 1] min(new_name_4 * 2 + 1000)
from """ + gvars.g_schema_arkcasedb + """.pvsel03;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select [first 1] sum(new_name_4 + new_name_4)
from """ + gvars.g_schema_arkcasedb + """.svsel13;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select [first 1] COUNT(DISTINCT SYSKEY)
from """ + gvars.g_schema_arkcasedb + """.btsel04;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s33')
    
    stmt = """select [first 1] AVG(DISTINCT SYSKEY)
from """ + gvars.g_schema_arkcasedb + """.btsel04;"""
    output = _dci.cmdexec(stmt)
    
    #  select [first 1] expression of aggregates
    stmt = """select [first 1] AVG(pic_decimal_1)
from """ + gvars.g_schema_arkcasedb + """.btsel01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s35')
    
    stmt = """select [first 1] (sum(pic_decimal_1) / count(*))
from """ + gvars.g_schema_arkcasedb + """.btsel01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s36')
    
    stmt = """select [first 1] max(binary_32_u) + min(binary_32_u)
from """ + gvars.g_schema_arkcasedb + """.btsel01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s37')
    
    stmt = """select [first 1] (sum(pic_decimal_3) + sum(small_int)) / 100
from """ + gvars.g_schema_arkcasedb + """.pvsel01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s38')
    
    stmt = """select [first 1] avg(pic_comp_1 ) + sum(pic_comp_1)
from """ + gvars.g_schema_arkcasedb + """.svsel13;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s39')
    
    stmt = """select [first 1] sum(decimal_1) + sum(decimal_1)
from """ + gvars.g_schema_arkcasedb + """.btsel01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s40')
    
    #  select [first 1] multiple aggregates
    stmt = """select [first 1] avg(decimal_3_unsigned),avg(decimal_1)
from """ + gvars.g_schema_arkcasedb + """.btsel01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s41')
    
    stmt = """select [first 1] sum(pic_decimal_3),avg(pic_decimal_3),max(pic_decimal_3),
min(pic_decimal_3),count(distinct pic_decimal_3),count(*)
from """ + gvars.g_schema_arkcasedb + """.pvsel01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s42')
    
    stmt = """select [first 1] sum(new_name_1), avg(new_name_2), max(new_name_3)
from """ + gvars.g_schema_arkcasedb + """.svsel13;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s43')
    
    stmt = """select [first 1] sum(binary_32_u), sum(distinct binary_32_u)
from """ + gvars.g_schema_arkcasedb + """.btsel01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s44')
    
    stmt = """select [first 1] avg(binary_32_u), max(distinct binary_32_u)
from """ + gvars.g_schema_arkcasedb + """.btsel01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s45')
    
    _testmgr.testcase_end(desc)

def test006(desc="""a06"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt1370 : A06
    #  Original Test case: arkt0008 : A06
    #  Description:        This test verifies the SQL SELECT
    #                      statement using SELECT [FIRST <N>]
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    
    stmt = """create table a7tab1 
(col_1 char(2) upshift NOT NULL
, primary key (col_1));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into a7tab1 values ('aB');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a7tab1 values ('aa');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # Should get 0 row since values are upshifted.
    stmt = """select [first 5] * from a7tab1 
where col_1 = 'aa';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """drop table a7tab1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

