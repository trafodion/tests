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
    #  Test case name:     arkt0008 : A01
    #  Description:        This test verifies the SQL SELECT
    #                      statement
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
    
    stmt = """select char_1 from """ + gvars.g_schema_arkcasedb + """.btsel01 
order by binary_signed;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s0')
    stmt = """select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel01 
order by binary_signed;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s1')
    stmt = """select pic_x_1,pic_x_7 from """ + gvars.g_schema_arkcasedb + """.btsel01 
order by binary_signed;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s2')
    stmt = """select pic_x_7,pic_x_7 from """ + gvars.g_schema_arkcasedb + """.btsel01 
order by binary_signed;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s3')
    stmt = """select pic_x_7,binary_64_s,decimal_1
from """ + gvars.g_schema_arkcasedb + """.btsel01 
order by binary_signed;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s4')
    stmt = """select pic_x_long from """ + gvars.g_schema_arkcasedb + """.btsel01 
order by binary_signed;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s5')
    stmt = """select var_char from """ + gvars.g_schema_arkcasedb + """.btsel01 
order by binary_signed;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s6')
    stmt = """select binary_signed from """ + gvars.g_schema_arkcasedb + """.btsel01 
order by binary_signed;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s7')
    stmt = """select binary_32_u from """ + gvars.g_schema_arkcasedb + """.btsel01 
order by binary_signed;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s8')
    stmt = """select binary_64_s from """ + gvars.g_schema_arkcasedb + """.btsel01 
order by binary_signed;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s9')
    stmt = """select pic_comp_1 from """ + gvars.g_schema_arkcasedb + """.btsel01 
order by binary_signed;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s10')
    stmt = """select pic_comp_2 from """ + gvars.g_schema_arkcasedb + """.btsel01 
order by binary_signed;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s11')
    stmt = """select pic_comp_3 from """ + gvars.g_schema_arkcasedb + """.btsel01 
order by binary_signed;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s12')
    stmt = """select small_int from """ + gvars.g_schema_arkcasedb + """.btsel01 
order by binary_signed;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s13')
    stmt = """select medium_int from """ + gvars.g_schema_arkcasedb + """.btsel01 
order by binary_signed;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s14')
    stmt = """select large_int from """ + gvars.g_schema_arkcasedb + """.btsel01 
order by binary_signed;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s15')
    stmt = """select decimal_1 from """ + gvars.g_schema_arkcasedb + """.btsel01 
order by binary_signed;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s16')
    stmt = """select decimal_2_signed from """ + gvars.g_schema_arkcasedb + """.btsel01 
order by binary_signed;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s17')
    stmt = """select decimal_3_unsigned from """ + gvars.g_schema_arkcasedb + """.btsel01 
order by binary_signed;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s18')
    stmt = """select pic_decimal_1 from """ + gvars.g_schema_arkcasedb + """.btsel01 
order by binary_signed;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s19')
    stmt = """select pic_decimal_2 from """ + gvars.g_schema_arkcasedb + """.btsel01 
order by binary_signed;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s20')
    stmt = """select pic_decimal_3 from """ + gvars.g_schema_arkcasedb + """.btsel01 
order by binary_signed;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s21')
    stmt = """select pic_x_a from """ + gvars.g_schema_arkcasedb + """.btsel06 
order by pic_x_a, pic_x_b, pic_x_c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s22')
    stmt = """select pic_x_b from """ + gvars.g_schema_arkcasedb + """.btsel06 
order by pic_x_a, pic_x_b, pic_x_c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s23')
    stmt = """select pic_x_c from """ + gvars.g_schema_arkcasedb + """.btsel06 
order by pic_x_a, pic_x_b, pic_x_c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s24')
    stmt = """select col_1 from """ + gvars.g_schema_arkcasedb + """.btsel06 
order by pic_x_a, pic_x_b, pic_x_c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s25')
    stmt = """select col_3 from """ + gvars.g_schema_arkcasedb + """.btsel06 
order by pic_x_a, pic_x_b, pic_x_c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s26')
    stmt = """select col_5 from """ + gvars.g_schema_arkcasedb + """.btsel06 
order by pic_x_a, pic_x_b, pic_x_c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s27')
    stmt = """select col_7 from """ + gvars.g_schema_arkcasedb + """.btsel06 
order by pic_x_a, pic_x_b, pic_x_c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s28')
    stmt = """select col_21 from """ + gvars.g_schema_arkcasedb + """.btsel06 
order by pic_x_a, pic_x_b, pic_x_c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s29')
    stmt = """select col_23 from """ + gvars.g_schema_arkcasedb + """.btsel06 
order by pic_x_a, pic_x_b, pic_x_c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s30')
    stmt = """select col_25 from """ + gvars.g_schema_arkcasedb + """.btsel06 
order by pic_x_a, pic_x_b, pic_x_c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s31')
    stmt = """select col_27 from """ + gvars.g_schema_arkcasedb + """.btsel06 
order by pic_x_a, pic_x_b, pic_x_c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s32')
    stmt = """select col_29 from """ + gvars.g_schema_arkcasedb + """.btsel06 
order by pic_x_a, pic_x_b, pic_x_c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s33')
    stmt = """select col_41 from """ + gvars.g_schema_arkcasedb + """.btsel06 
order by pic_x_a, pic_x_b, pic_x_c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s34')
    stmt = """select col_43 from """ + gvars.g_schema_arkcasedb + """.btsel06 
order by pic_x_a, pic_x_b, pic_x_c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s35')
    stmt = """select col_45 from """ + gvars.g_schema_arkcasedb + """.btsel06 
order by pic_x_a, pic_x_b, pic_x_c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s36')
    stmt = """select col_47 from """ + gvars.g_schema_arkcasedb + """.btsel06 
order by pic_x_a, pic_x_b, pic_x_c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s37')
    stmt = """select col_61 from """ + gvars.g_schema_arkcasedb + """.btsel06 
order by pic_x_a, pic_x_b, pic_x_c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s38')
    stmt = """select col_63 from """ + gvars.g_schema_arkcasedb + """.btsel06 
order by pic_x_a, pic_x_b, pic_x_c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s39')
    stmt = """select col_65 from """ + gvars.g_schema_arkcasedb + """.btsel06 
order by pic_x_a, pic_x_b, pic_x_c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s40')
    stmt = """select col_67 from """ + gvars.g_schema_arkcasedb + """.btsel06 
order by pic_x_a, pic_x_b, pic_x_c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s41')
    stmt = """select col_69 from """ + gvars.g_schema_arkcasedb + """.btsel06 
order by pic_x_a, pic_x_b, pic_x_c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s42')
    stmt = """select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
order by syskey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s43')
    stmt = """select binary_32_u from """ + gvars.g_schema_arkcasedb + """.btsel03 
order by syskey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s44')
    stmt = """select var_char from """ + gvars.g_schema_arkcasedb + """.btsel04 
order by syskey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s45')
    stmt = """select col_4 from """ + gvars.g_schema_arkcasedb + """.btsel05 
order by syskey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s46')
    stmt = """select pic_x_c from """ + gvars.g_schema_arkcasedb + """.btsel07 
order by pic_x_c, pic_x_b, pic_x_a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s47')
    stmt = """select pic_252 from """ + gvars.g_schema_arkcasedb + """.btsel08 
order by large_int;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s48')
    stmt = """select pic_x_7 from """ + gvars.g_schema_arkcasedb + """.btsel09 
order by pic_x_a desc, pic_x_6 desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s49')
    stmt = """select binary_32_signed from """ + gvars.g_schema_arkcasedb + """.btsel10 
order by pic_9_7 asc, pic_x_7 desc, pic_x_a asc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s50')
    stmt = """select char_10 from """ + gvars.g_schema_arkcasedb + """.btsel11 
order by decimal_10 desc, pic_x_a asc, pic_9_7 desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s51')
    stmt = """select medium_int from """ + gvars.g_schema_arkcasedb + """.pvsel01 
order by pic_decimal_3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s52')
    stmt = """select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.pvsel02 
order by pic_x_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s53')
    stmt = """select new_name_2 from """ + gvars.g_schema_arkcasedb + """.pvsel03 
order by new_name_4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s54')
    stmt = """select pic_comp_1 from """ + gvars.g_schema_arkcasedb + """.pvsel04 
order by pic_comp_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s55')
    stmt = """select col_4 from """ + gvars.g_schema_arkcasedb + """.svsel11 
order by col_4, col_8;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s56')
    stmt = """select new_name_3 from """ + gvars.g_schema_arkcasedb + """.svsel13 
order by new_name_4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s57')
    stmt = """select new_name_1 from """ + gvars.g_schema_arkcasedb + """.svsel14 
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
    #  Test case name:     arkt0008 : A02
    #  Description:        This test verifies the SQL SELECT
    #                      statement
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    #
    
    #  Create LOG file
    
    stmt = """select distinct char_1 from """ + gvars.g_schema_arkcasedb + """.btsel01 
order by char_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s0')
    stmt = """select all char_1 from """ + gvars.g_schema_arkcasedb + """.btsel01 
order by binary_signed;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s1')
    stmt = """select distinct var_char from """ + gvars.g_schema_arkcasedb + """.btsel01 
order by var_char;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s2')
    stmt = """select all var_char from """ + gvars.g_schema_arkcasedb + """.btsel01 
order by binary_signed;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s3')
    stmt = """select distinct medium_int from """ + gvars.g_schema_arkcasedb + """.btsel01 
order by medium_int;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s4')
    stmt = """select all medium_int from """ + gvars.g_schema_arkcasedb + """.btsel01 
order by binary_signed;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s5')
    stmt = """select distinct pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
order by pic_x_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s6')
    stmt = """select all pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
order by syskey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s7')
    stmt = """select distinct * from """ + gvars.g_schema_arkcasedb + """.btsel02 
order by pic_x_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s8')
    stmt = """select all * from """ + gvars.g_schema_arkcasedb + """.btsel02 
order by syskey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s9')
    stmt = """select distinct binary_32_u from """ + gvars.g_schema_arkcasedb + """.btsel03 
order by binary_32_u;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s10')
    stmt = """select all binary_32_u from """ + gvars.g_schema_arkcasedb + """.btsel03 
order by syskey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s11')
    stmt = """select distinct * from """ + gvars.g_schema_arkcasedb + """.btsel03 
order by pic_x_7, pic_x4_a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s12')
    stmt = """select all * from """ + gvars.g_schema_arkcasedb + """.btsel03 
order by syskey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s13')
    stmt = """select distinct medium_int from """ + gvars.g_schema_arkcasedb + """.btsel04 
order by medium_int;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s14')
    stmt = """select all medium_int from """ + gvars.g_schema_arkcasedb + """.btsel04 
order by syskey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s15')
    stmt = """select distinct col_1 from """ + gvars.g_schema_arkcasedb + """.btsel05 
order by col_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s16')
    stmt = """select all col_1 from """ + gvars.g_schema_arkcasedb + """.btsel05 
order by syskey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s17')
    stmt = """select distinct col_6 from """ + gvars.g_schema_arkcasedb + """.btsel06 
order by col_6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s18')
    stmt = """select all col_6 from """ + gvars.g_schema_arkcasedb + """.btsel06 
order by pic_x_a, pic_x_b, pic_x_c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s19')
    stmt = """select distinct pic_x_a from """ + gvars.g_schema_arkcasedb + """.btsel07 
order by pic_x_a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s20')
    stmt = """select all pic_x_a from """ + gvars.g_schema_arkcasedb + """.btsel07 
order by pic_x_c, pic_x_b, pic_x_a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s21')
    stmt = """select distinct large_int from """ + gvars.g_schema_arkcasedb + """.btsel08 
order by large_int;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s22')
    stmt = """select all large_int from """ + gvars.g_schema_arkcasedb + """.btsel08 
order by large_int;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s23')
    stmt = """select distinct pic_x_6 from """ + gvars.g_schema_arkcasedb + """.btsel09 
order by pic_x_6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s24')
    stmt = """select all pic_x_6 from """ + gvars.g_schema_arkcasedb + """.btsel09 
order by pic_x_a desc, pic_x_6 desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s25')
    stmt = """select distinct binary_unsigned,binary_32_signed
from """ + gvars.g_schema_arkcasedb + """.btsel10 
order by binary_unsigned,binary_32_signed;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s26')
    stmt = """select all binary_unsigned,binary_32_signed
from """ + gvars.g_schema_arkcasedb + """.btsel10 
order by pic_9_7 asc, pic_x_7 desc, pic_x_a asc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s27')
    stmt = """select distinct decimal_10,binary_unsigned,binary_32_signed
from """ + gvars.g_schema_arkcasedb + """.btsel11 
order by decimal_10,binary_unsigned,binary_32_signed;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s28')
    stmt = """select all decimal_10,binary_unsigned,binary_32_signed
from """ + gvars.g_schema_arkcasedb + """.btsel11 
order by decimal_10 desc, pic_x_a asc, pic_9_7 desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s29')
    stmt = """select distinct medium_int from """ + gvars.g_schema_arkcasedb + """.pvsel01 
order by medium_int;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s30')
    stmt = """select all medium_int from """ + gvars.g_schema_arkcasedb + """.pvsel01 
order by pic_decimal_3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s31')
    stmt = """select distinct pic_x_1 from """ + gvars.g_schema_arkcasedb + """.pvsel02 
order by pic_x_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s32')
    stmt = """select all pic_x_1 from """ + gvars.g_schema_arkcasedb + """.pvsel02 
order by pic_x_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s33')
    stmt = """select distinct new_name_2 from """ + gvars.g_schema_arkcasedb + """.pvsel03 
order by new_name_2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s34')
    stmt = """select all new_name_2 from """ + gvars.g_schema_arkcasedb + """.pvsel03 
order by new_name_4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s35')
    stmt = """select distinct medium_int from """ + gvars.g_schema_arkcasedb + """.pvsel04 
order by medium_int;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s36')
    stmt = """select all medium_int from """ + gvars.g_schema_arkcasedb + """.pvsel04 
order by pic_comp_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s37')
    stmt = """select distinct col_3 from """ + gvars.g_schema_arkcasedb + """.svsel11 
order by col_3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s38')
    stmt = """select all col_3 from """ + gvars.g_schema_arkcasedb + """.svsel11 
order by col_4, col_8;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s39')
    stmt = """select distinct pic_comp_1 from """ + gvars.g_schema_arkcasedb + """.svsel13 
order by pic_comp_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s40')
    stmt = """select all pic_comp_1 from """ + gvars.g_schema_arkcasedb + """.svsel13 
order by new_name_4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s41')
    stmt = """select distinct new_name_1 from """ + gvars.g_schema_arkcasedb + """.svsel14 
order by new_name_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s42')
    stmt = """select all new_name_1 from """ + gvars.g_schema_arkcasedb + """.svsel14 
order by new_name_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s43')
    
    _testmgr.testcase_end(desc)

def test003(desc="""a03"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0008 : A03
    #  Description:        This test verifies the SQL SELECT
    #                      statement
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    #
    #  Create LOG file
    
    stmt = """select SYSKEY from """ + gvars.g_schema_arkcasedb + """.btsel02 
order by syskey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 8)
    
    stmt = """select *,SYSKEY from """ + gvars.g_schema_arkcasedb + """.btsel02 
order by syskey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 8)
    
    stmt = """select SYSKEY from """ + gvars.g_schema_arkcasedb + """.btsel03 
order by syskey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 8)
    
    stmt = """select SYSKEY,* from """ + gvars.g_schema_arkcasedb + """.btsel03 
order by syskey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 8)
    
    stmt = """select SYSKEY from """ + gvars.g_schema_arkcasedb + """.btsel04 
order by syskey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 8)
    
    stmt = """select *,SYSKEY from """ + gvars.g_schema_arkcasedb + """.btsel04 
order by syskey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 8)
    
    stmt = """select SYSKEY, 'anchor literal for SYSKEY'
from """ + gvars.g_schema_arkcasedb + """.btsel05 
order by syskey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 8)
    
    stmt = """select *,SYSKEY, 'anchor literal for SYSKEY'
from """ + gvars.g_schema_arkcasedb + """.btsel05 
order by syskey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 8)
    
    stmt = """select new_name_4 from """ + gvars.g_schema_arkcasedb + """.pvsel03 
order by new_name_4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 4)
    
    stmt = """select *,new_name_4 from """ + gvars.g_schema_arkcasedb + """.pvsel03 
order by new_name_4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4004')
    
    stmt = """select new_name_4 from """ + gvars.g_schema_arkcasedb + """.svsel13 
order by new_name_4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 4)
    
    stmt = """select *,new_name_4 from """ + gvars.g_schema_arkcasedb + """.svsel13 
order by new_name_4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4004')
    
    stmt = """select new_name_1,new_name_4 from """ + gvars.g_schema_arkcasedb + """.pvsel03 
order by new_name_4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 4)
    
    stmt = """select new_name_1,new_name_4 from """ + gvars.g_schema_arkcasedb + """.svsel13 
order by new_name_4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 4)
    
    stmt = """select new_name_1,new_name_4 , new_name_2,
(new_name_4 * new_name_2)
from """ + gvars.g_schema_arkcasedb + """.pvsel03 
order by new_name_4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 4)
    
    stmt = """select new_name_1,(new_name_4 + 100) from """ + gvars.g_schema_arkcasedb + """.svsel13 
order by new_name_4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 4)
    
    _testmgr.testcase_end(desc)

def test004(desc="""a04"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0008 : A04
    #  Description:        This test verifies the SQL SELECT
    #                      statement
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    #
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.btsel01 
order by binary_signed;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s0')
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.btsel02 
order by syskey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s1')
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.btsel03 
order by syskey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s2')
    stmt = """select *
from """ + gvars.g_schema_arkcasedb + """.btsel04 
order by syskey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s3')
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.btsel05 
order by syskey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s4')
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.btsel06 
order by pic_x_a, pic_x_b, pic_x_c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s5')
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.btsel07 
order by pic_x_c, pic_x_b, pic_x_a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s6')
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.btsel08 
order by large_int;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s7')
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.btsel09 
order by pic_x_a desc, pic_x_6 desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s8')
    
    #         select *,* from btsel09
    #          order by pic_x_a desc, pic_x_6 desc;
    
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.btsel10 
order by pic_9_7 asc, pic_x_7 desc, pic_x_a asc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s9')
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.btsel11 
order by decimal_10 desc, pic_x_a asc, pic_9_7 desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s10')
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.pvsel01 
order by pic_decimal_3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s11')
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.pvsel02 
order by pic_x_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s12')
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.pvsel03 
order by new_name_4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 4)
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.pvsel04 
order by pic_comp_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s14')
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.svsel11 
order by col_4, col_8;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s15')
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.svsel12 
order by col_3, col_5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s16')
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.svsel13 
order by new_name_4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 4)
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.svsel14 
order by new_name_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s18')
    
    _testmgr.testcase_end(desc)

def test005(desc="""a05"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0008 : A05
    #  Description:        This test verifies the SQL SELECT
    #                      statement
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    #
    stmt = """select medium_int,medium_int
from """ + gvars.g_schema_arkcasedb + """.btsel01 
order by binary_signed;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s0')
    
    stmt = """select distinct (medium_int * medium_int)
from """ + gvars.g_schema_arkcasedb + """.btsel01 
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s1')
    stmt = """select all (medium_int * medium_int)
from """ + gvars.g_schema_arkcasedb + """.btsel01 
order by binary_signed;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s2')
    stmt = """select +large_int from """ + gvars.g_schema_arkcasedb + """.btsel01 
order by binary_signed;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s3')
    stmt = """select (+large_int) from """ + gvars.g_schema_arkcasedb + """.btsel01 
order by binary_signed;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s4')
    stmt = """select -large_int from """ + gvars.g_schema_arkcasedb + """.btsel01 
order by binary_signed;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s5')
    stmt = """select (-large_int) from """ + gvars.g_schema_arkcasedb + """.btsel01 
order by binary_signed;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s6')
    stmt = """select (binary_32_u*2) from """ + gvars.g_schema_arkcasedb + """.btsel01 
order by binary_signed;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s7')
    stmt = """select pic_9_7+binary_64_s from """ + gvars.g_schema_arkcasedb + """.btsel03 
order by syskey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s8')
    stmt = """select medium_int - 100,pic_comp_1 - 100
from """ + gvars.g_schema_arkcasedb + """.btsel04 
order by syskey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s9')
    stmt = """select (pic_x_5 / 2),pic_x_6 from """ + gvars.g_schema_arkcasedb + """.btsel09 
order by pic_x_a desc, pic_x_6 desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s10')
    stmt = """select (decimal_10 + binary_unsigned),(binary_unsigned +
binary_32_signed) from """ + gvars.g_schema_arkcasedb + """.btsel10 
order by pic_9_7 asc, pic_x_7 desc, pic_x_a asc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s11')
    stmt = """select (decimal_10 + 100) from """ + gvars.g_schema_arkcasedb + """.btsel11 
order by decimal_10 desc, pic_x_a asc, pic_9_7 desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s12')
    stmt = """select (new_name_1 - 1000),(new_name_2 + 1000)
from """ + gvars.g_schema_arkcasedb + """.svsel13 
order by new_name_4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s13')
    stmt = """select (medium_int * pic_comp_1) from """ + gvars.g_schema_arkcasedb + """.pvsel04 
order by pic_comp_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s14')
    stmt = """select 'large_int = ',large_int
from """ + gvars.g_schema_arkcasedb + """.btsel01 
order by binary_signed;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s15')
    stmt = """select medium_int,'char_1 = ',char_1
from """ + gvars.g_schema_arkcasedb + """.btsel01 
order by binary_signed;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s16')
    stmt = """select '100 =',100,'small_int =',small_int
from """ + gvars.g_schema_arkcasedb + """.btsel01 
order by binary_signed;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s17')
    stmt = """select '100 * 10 =',100 * 10,'small_int =',small_int
from """ + gvars.g_schema_arkcasedb + """.btsel01 
order by binary_signed;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s18')
    stmt = """select 'only a constant'
from """ + gvars.g_schema_arkcasedb + """.btsel01 
order by binary_signed;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s19')
    
    stmt = """select 'test of double quote (") '
from """ + gvars.g_schema_arkcasedb + """.btsel01 
order by binary_signed;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s20')
    
    stmt = """select 'test of single quote ('') '
from """ + gvars.g_schema_arkcasedb + """.btsel01 
order by binary_signed;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s21')
    
    stmt = """select ''
from """ + gvars.g_schema_arkcasedb + """.btsel01 
order by binary_signed;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s22')
    
    stmt = """select ''
from """ + gvars.g_schema_arkcasedb + """.btsel01 
order by binary_signed;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s23')
    
    _testmgr.testcase_end(desc)

def test006(desc="""a06"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0008 : A06
    #  Description:        This test verifies the SQL SELECT
    #                      statement
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    
    #  *** audited tables ***
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.btsel01 
for read uncommitted access
order by binary_signed;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s0')
    
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.btsel02 
for read committed access
order by syskey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s1')
    
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.btsel03 
for serializable access
order by syskey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s2')
    
    #   *** non-audited table ***
    
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.btsel05 
for read uncommitted access
order by syskey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s3')
    
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.btsel05 
for read committed access
order by syskey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s4')
    
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.btsel05 
for serializable access
order by syskey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s5')
    
    #   *** views ***
    
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.pvsel01 
for read uncommitted access
order by pic_decimal_3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s6')
    
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.pvsel01 
for read committed access
order by pic_decimal_3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s7')
    
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.pvsel01 
for serializable access
order by pic_decimal_3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s8')
    
    #  svsel15 must be accessed for read uncommitted access (mixed view)
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.svsel15 
for read uncommitted access
order by mixed_13;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s9')
    
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.svsel14 
for read uncommitted access
order by new_name_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s10')
    
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.svsel13 
for read uncommitted access
order by new_name_4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 4)
    
    _testmgr.testcase_end(desc)

def test007(desc="""a07"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0008 : A07
    #  Description:        This test verifies the SQL SELECT
    #                      statement
    #                      Order by clauses with aggregates is non
    #                      ANSI. Testware correction made on oct22
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    
    #  select ALL
    stmt = """select count(*)
from """ + gvars.g_schema_arkcasedb + """.btsel01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s0')
    #       order by binary_signed;
    
    stmt = """select avg(medium_int)
from """ + gvars.g_schema_arkcasedb + """.pvsel01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s1')
    #       order by pic_decimal_3;
    
    #  test use of white space inside aggregate
    stmt = """select avg (ALL pic_comp_1)
from """ + gvars.g_schema_arkcasedb + """.svsel13;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s2')
    #       order by new_name_4;
    
    stmt = """select max(
binary_64_s)
from """ + gvars.g_schema_arkcasedb + """.btsel01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s3')
    #       order by binary_signed;
    
    stmt = """select max(ALL
large_int)
from """ + gvars.g_schema_arkcasedb + """.pvsel01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s4')
    #      order by pic_decimal_3;
    
    stmt = """select min(col_2
)
from """ + gvars.g_schema_arkcasedb + """.svsel11;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s5')
    #       order by col_4, col_8;
    
    stmt = """select min
(ALL decimal_2_signed)
from """ + gvars.g_schema_arkcasedb + """.btsel01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s6')
    #       order by binary_signed;
    
    stmt = """select sum(new_name_2)
from """ + gvars.g_schema_arkcasedb + """.pvsel03;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s7')
    #       order by new_name_4;
    
    stmt = """select sum(ALL col_4)
from """ + gvars.g_schema_arkcasedb + """.svsel11;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s8')
    #       order by col_4, col_8;
    
    stmt = """select max(pic_x_1)
from """ + gvars.g_schema_arkcasedb + """.btsel02;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s9')
    #       order by syskey;
    
    stmt = """select max(ALL new_name_3)
from """ + gvars.g_schema_arkcasedb + """.pvsel03;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s10')
    #       order by new_name_4;
    
    stmt = """select min(var_char)
from """ + gvars.g_schema_arkcasedb + """.svsel13;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s11')
    #       order by new_name_4;
    
    stmt = """select min(ALL pic_x_a)
from """ + gvars.g_schema_arkcasedb + """.btsel05;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s12')
    #       order by syskey;
    
    #  select DISTINCT
    stmt = """select AVG(distinct binary_32_u)
from """ + gvars.g_schema_arkcasedb + """.btsel01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s13')
    #       order by binary_32_u;
    
    stmt = """select MAX(distinct medium_int)
from """ + gvars.g_schema_arkcasedb + """.pvsel01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s14')
    #       order by medium_int;
    
    stmt = """select MIN(distinct new_name_1)
from """ + gvars.g_schema_arkcasedb + """.svsel13;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s15')
    #       order by new_name_1;
    
    stmt = """select SUM(distinct binary_64_s)
from """ + gvars.g_schema_arkcasedb + """.btsel01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s16')
    #       order by binary_64_s;
    
    stmt = """select count(distinct medium_int)
from """ + gvars.g_schema_arkcasedb + """.pvsel01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s17')
    #       order by medium_int;
    
    stmt = """select count(distinct var_char)
from """ + gvars.g_schema_arkcasedb + """.svsel13;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s18')
    #       order by var_char;
    
    stmt = """select max(distinct pic_x_long)
from """ + gvars.g_schema_arkcasedb + """.btsel01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s19')
    #       order by pic_x_long;
    
    stmt = """select min(distinct var_char)
from """ + gvars.g_schema_arkcasedb + """.btsel01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s20')
    #       order by var_char;
    
    #  select an expression inside an aggregate
    stmt = """select avg(binary_32_u * 2)
from """ + gvars.g_schema_arkcasedb + """.btsel01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s21')
    #       order by binary_signed;
    
    stmt = """select avg(ALL binary_32_u + pic_comp_1)
from """ + gvars.g_schema_arkcasedb + """.btsel01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s22')
    #       order by binary_signed;
    
    stmt = """select max(new_name_1 * new_name_1)
from """ + gvars.g_schema_arkcasedb + """.pvsel03;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s23')
    #       order by new_name_4;
    
    stmt = """select max(ALL new_name_1 / new_name_2)
from """ + gvars.g_schema_arkcasedb + """.svsel13;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s24')
    #       order by new_name_4;
    
    stmt = """select min((-binary_signed) - decimal_3_unsigned)
from """ + gvars.g_schema_arkcasedb + """.btsel01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s25')
    #       order by binary_signed;
    
    stmt = """select min(ALL large_int * small_int)
from """ + gvars.g_schema_arkcasedb + """.pvsel01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s26')
    #       order by pic_decimal_3;
    
    stmt = """select sum ((col_1 + col_4) + 1000)
from """ + gvars.g_schema_arkcasedb + """.svsel11;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s27')
    #       order by col_4, col_8;
    
    stmt = """select sum(ALL -1000 + small_int)
from """ + gvars.g_schema_arkcasedb + """.btsel01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s28')
    #       order by binary_signed;
    
    #  select an expression with SYSKEY in an aggregate
    stmt = """select avg(SYSKEY + binary_64_s)
from """ + gvars.g_schema_arkcasedb + """.btsel03;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8411')
    #       order by syskey;
    
    stmt = """select max(SYSKEY / 3 + medium_int)
from """ + gvars.g_schema_arkcasedb + """.btsel04;"""
    output = _dci.cmdexec(stmt)
    #       order by syskey;
    
    stmt = """select min(new_name_4 * 2 + 1000)
from """ + gvars.g_schema_arkcasedb + """.pvsel03;"""
    output = _dci.cmdexec(stmt)
    #       order by new_name_4;
    
    stmt = """select sum(new_name_4 + new_name_4)
from """ + gvars.g_schema_arkcasedb + """.svsel13;"""
    output = _dci.cmdexec(stmt)
    #       order by new_name_4;
    
    stmt = """select COUNT(DISTINCT SYSKEY)
from """ + gvars.g_schema_arkcasedb + """.btsel04;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s33')
    #       order by SYSKEY;
    
    stmt = """select AVG(DISTINCT SYSKEY)
from """ + gvars.g_schema_arkcasedb + """.btsel04;"""
    output = _dci.cmdexec(stmt)
    #       order by SYSKEY;
    
    #  select expression of aggregates
    stmt = """select AVG(pic_decimal_1)
from """ + gvars.g_schema_arkcasedb + """.btsel01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s35')
    #       order by binary_signed;
    
    stmt = """select (sum(pic_decimal_1) / count(*))
from """ + gvars.g_schema_arkcasedb + """.btsel01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s36')
    #       order by binary_signed;
    
    stmt = """select max(binary_32_u) + min(binary_32_u)
from """ + gvars.g_schema_arkcasedb + """.btsel01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s37')
    #       order by binary_signed;
    
    stmt = """select (sum(pic_decimal_3) + sum(small_int)) / 100
from """ + gvars.g_schema_arkcasedb + """.pvsel01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s38')
    #       order by pic_decimal_3;
    
    stmt = """select avg(pic_comp_1 ) + sum(pic_comp_1)
from """ + gvars.g_schema_arkcasedb + """.svsel13;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s39')
    #       order by new_name_4;
    
    stmt = """select sum(decimal_1) + sum(decimal_1)
from """ + gvars.g_schema_arkcasedb + """.btsel01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s40')
    #       order by binary_signed;
    
    #  select multiple aggregates
    stmt = """select avg(decimal_3_unsigned),avg(decimal_1)
from """ + gvars.g_schema_arkcasedb + """.btsel01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s41')
    #       order by binary_signed;
    
    stmt = """select sum(pic_decimal_3),avg(pic_decimal_3),max(pic_decimal_3),
min(pic_decimal_3),count(distinct pic_decimal_3),count(*)
from """ + gvars.g_schema_arkcasedb + """.pvsel01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s42')
    #       order by pic_decimal_3;
    
    stmt = """select sum(new_name_1), avg(new_name_2), max(new_name_3)
from """ + gvars.g_schema_arkcasedb + """.svsel13;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s43')
    #       order by new_name_4;
    
    stmt = """select sum(binary_32_u), sum(distinct binary_32_u)
from """ + gvars.g_schema_arkcasedb + """.btsel01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s44')
    #       order by binary_32_u;
    
    stmt = """select avg(binary_32_u), max(distinct binary_32_u)
from """ + gvars.g_schema_arkcasedb + """.btsel01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s45')
    
    _testmgr.testcase_end(desc)

def test008(desc="""a08"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0008 : 8
    #  Description:        This test verifies the SQL/K SELECT
    #                      statement
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    
    stmt = """set schema """ + defs.w_catalog + """.""" + defs.w_schema + """;"""
    output = _dci.cmdexec(stmt)
    
    # Create LOG file
    
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
    
    # m0: Should get 0 row since values are upshifted.
    stmt = """select * from a7tab1 
where col_1 = 'aa';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """drop table a7tab1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

