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
    #  Test case name:     arkt0009 : A01
    #  Description:        This test verifies the SQL SELECT
    #                      statement with WHERE clause
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    #
    # ---------------------------------
    # Set up default catalog and schema
    # ---------------------------------
    #set catalog $global_catalog_A;
    #set schema  $global_schema_A;
    
    #         normal where clause select statement test case - this tests
    #         the use of a where predicate that compares a column with
    #         a constant.
    #
    
    stmt = """select * from  """ + gvars.g_schema_arkcasedb + """.btsel01 
where char_1 = 'A'
order by binary_signed;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s0')
    
    stmt = """select * from  """ + gvars.g_schema_arkcasedb + """.btsel01 
where 'A' <> var_char
order by binary_signed;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s1')
    
    stmt = """select * from  """ + gvars.g_schema_arkcasedb + """.btsel01 
where not ('A' = var_char)
order by binary_signed;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s2')
    
    stmt = """select * from  """ + gvars.g_schema_arkcasedb + """.btsel01 
where binary_32_u < 100
order by binary_signed;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s3')
    
    stmt = """select * from  """ + gvars.g_schema_arkcasedb + """.btsel01 
where decimal_3_unsigned <= 100
order by binary_signed;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s4')
    
    stmt = """select * from  """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 > 'A'
order by syskey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s5')
    
    stmt = """select * from  """ + gvars.g_schema_arkcasedb + """.btsel03 
where binary_32_u >= 5.0
order by syskey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s6')
    
    stmt = """select * from  """ + gvars.g_schema_arkcasedb + """.btsel03 
where pic_9_7 = 80
order by syskey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s7')
    
    stmt = """select * from  """ + gvars.g_schema_arkcasedb + """.btsel03 
where pic_x_7 <> '8'
order by syskey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s8')
    
    stmt = """select * from  """ + gvars.g_schema_arkcasedb + """.btsel04 
where var_char < 'pam'
order by syskey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s9')
    
    stmt = """select * from  """ + gvars.g_schema_arkcasedb + """.btsel04 
where medium_int <= 1000
order by syskey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s10')
    
    stmt = """select * from  """ + gvars.g_schema_arkcasedb + """.btsel04 
where pic_x_7 <= '8'
order by syskey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s11')
    
    stmt = """select * from  """ + gvars.g_schema_arkcasedb + """.btsel05 
where pic_x_a > 'abe'
order by syskey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s12')
    
    stmt = """select * from  """ + gvars.g_schema_arkcasedb + """.btsel05 
where col_9 > 'abe'
order by syskey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s13')
    
    stmt = """select * from  """ + gvars.g_schema_arkcasedb + """.btsel06 
where col_1 >= 100
order by pic_x_a, pic_x_b, pic_x_c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s14')
    
    stmt = """select * from  """ + gvars.g_schema_arkcasedb + """.btsel06 
where 100 = col_7
order by pic_x_a, pic_x_b, pic_x_c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s15')
    
    stmt = """select * from  """ + gvars.g_schema_arkcasedb + """.btsel06 
where 'joe' <> pic_x_a
order by pic_x_a, pic_x_b, pic_x_c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s16')
    
    stmt = """select * from  """ + gvars.g_schema_arkcasedb + """.btsel07 
where pic_x_b < 'Q'
order by pic_x_c, pic_x_b, pic_x_a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s17')
    
    stmt = """select * from  """ + gvars.g_schema_arkcasedb + """.btsel08 
where large_int <= 1000
order by large_int;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s18')
    
    stmt = """select * from  """ + gvars.g_schema_arkcasedb + """.btsel08 
where pic_1 > 'C'
order by large_int;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s19')
    
    stmt = """select * from  """ + gvars.g_schema_arkcasedb + """.btsel09 
where pic_x_4 >= 'JOE'
order by pic_x_a desc, pic_x_6 desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s20')
    
    stmt = """select * from  """ + gvars.g_schema_arkcasedb + """.btsel09 
where pic_x_6 = 10
order by pic_x_a desc, pic_x_6 desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s21')
    
    stmt = """select * from  """ + gvars.g_schema_arkcasedb + """.btsel10 
where pic_x_a <> 'tom'
order by pic_9_7 asc, pic_x_7 desc, pic_x_a asc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s22')
    
    stmt = """select * from  """ + gvars.g_schema_arkcasedb + """.btsel10 
where binary_32_signed < 0
order by pic_9_7 asc, pic_x_7 desc, pic_x_a asc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s23')
    
    stmt = """select * from  """ + gvars.g_schema_arkcasedb + """.btsel10 
where decimal_10 <= 100
order by pic_9_7 asc, pic_x_7 desc, pic_x_a asc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s24')
    
    stmt = """select * from  """ + gvars.g_schema_arkcasedb + """.btsel11 
where pic_x_a > 'bob'
order by decimal_10 desc, pic_x_a asc, pic_9_7 desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s25')
    
    stmt = """select * from  """ + gvars.g_schema_arkcasedb + """.btsel11 
where binary_unsigned >= 100
order by decimal_10 desc, pic_x_a asc, pic_9_7 desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s26')
    
    stmt = """select * from  """ + gvars.g_schema_arkcasedb + """.btsel11 
where pic_9_7 = 100
order by decimal_10 desc, pic_x_a asc, pic_9_7 desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s27')
    
    stmt = """select * from  """ + gvars.g_schema_arkcasedb + """.pvsel01 
where binary_signed > 50
order by pic_decimal_3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s28')
    
    stmt = """select * from  """ + gvars.g_schema_arkcasedb + """.svsel11 
where col_1 > 50
order by col_4, col_8;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s29')
    
    #  *** test use of SYSKEY in the where clause ***
    
    stmt = """select * from  """ + gvars.g_schema_arkcasedb + """.btsel02 
where SYSKEY <> 0
order by syskey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s30')
    
    #  *** new_name_4 is SYSKEY in these views ***
    
    stmt = """select * from  """ + gvars.g_schema_arkcasedb + """.pvsel03 
where new_name_4 <> 0
order by new_name_4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 4)
    
    stmt = """select * from  """ + gvars.g_schema_arkcasedb + """.svsel13 
where new_name_4 <> 0
order by new_name_4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 4)
    
    stmt = """create table t1016 (c1 int not null, c2 char(20), primary key (c1));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into t1016 values (1,'aa');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1016 values (2,'aa');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1016 values (3,'aa');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1016 values (4,'aa');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1016 values (5,'aa');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """prepare s from
select * from t1016 
where c1 = ? and c1 = ?;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """execute s using 4, 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """prepare s from
select * from t1016 
where c1 = ? or  c1 = ?;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """execute s using 4, 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s34')
    
    _testmgr.testcase_end(desc)

def test002(desc="""a02"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0009 : A02
    #  Description:        This test verifies the SQL SELECT
    #                      statement with WHERE clause
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    #
    
    #         normal where clause select statement - this tests the use
    #         of a where predicate where columns are compared.
    #
    
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.btsel01 
where binary_32_u = pic_comp_1
order by binary_signed;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s0')
    
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.btsel01 
where decimal_1 <> decimal_3_unsigned
order by binary_signed;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s1')
    
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.btsel01 
where not (decimal_1 = decimal_3_unsigned)
order by binary_signed;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s2')
    
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.btsel01 
where decimal_3_unsigned < binary_64_s
order by binary_signed;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s3')
    
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.btsel01 
where char_10 <= pic_x_7
order by binary_signed;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s4')
    
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.btsel01 
where var_char > char_1
order by binary_signed;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s5')
    
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.btsel03 
where binary_64_s >= binary_32_u
order by syskey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s6')
    
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.btsel03 
where pic_9_7 = (binary_64_s - 1120)
order by syskey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s7')
    
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.btsel03 
where not (pic_x_7 <> pic_x4_a)
order by syskey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s8')
    
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.btsel04 
where (pic_comp_1 < medium_int) and
(var_char <= pic_x_7)
order by syskey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s9')
    
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.btsel05 
where (col_1 > col_2) and
(col_3 >= col_4) and
(col_5 = col_6) and
(col_9 <> col_10)
order by syskey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s10')
    
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.btsel05 
where (col_3 < col_2) and
(col_4 <= col_5) and
(col_7 > col_6)
order by syskey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s11')
    
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.btsel05 
where ((col_8 >= col_9) or
(col_9 = pic_x_a)) and
(col_7 = col_7)
order by syskey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s12')
    
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.btsel06 
where (col_1 < col_2) and
(col_3 <= col_4) and
(col_5 > col_6) and
(col_7 >= col_8) and
((col_9 * 2) = col_10)
order by pic_x_a, pic_x_b, pic_x_c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s13')
    
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.btsel06 
where (col_2 < col_22) and
(col_23 <= col_24) and
(col_25 > col_26) and
(col_27 >= col_28) and
((col_29 * 2) = col_30)
order by pic_x_a, pic_x_b, pic_x_c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.btsel06 
where (col_22 <> col_23) and
(col_24 <= col_25) and
((col_26 * 2) = (col_27 + 100)) and
((col_28>col_29) or (col_29 > col_28))
order by pic_x_a, pic_x_b, pic_x_c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s14')
    
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.btsel06 
where (col_41 < col_42) and
(col_43 <= col_44) and
(col_45 > col_46) and
(col_47 >= col_48)
order by pic_x_a, pic_x_b, pic_x_c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s15')
    
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.btsel06 
where (col_42 <> col_43) and
(col_44 <= col_45) and
((col_46 * 2) = (col_47 + 100))
order by pic_x_a, pic_x_b, pic_x_c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s16')
    
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.btsel06 
where (col_61 < col_62) and
(col_63 <= col_64) and
(col_65 > col_66) and
(col_67 >= col_68) and
((col_69 * 2) = col_70)
order by pic_x_a, pic_x_b, pic_x_c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s17')
    
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.btsel06 
where (col_62 <> col_63) and
(col_64 <= col_65) and
((col_66 * 2) = (col_67 + 100)) and
((col_68 > col_69) or (col_69 > col_68))
order by pic_x_a, pic_x_b, pic_x_c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s18')
    
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.btsel07 
where pic_x_a = pic_x_c
order by pic_x_c, pic_x_b, pic_x_a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s19')
    
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.btsel08 
where (pic_252 > pic_1) or
(not (pic_252 > pic_1))
order by large_int;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s20')
    
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.btsel09 
where (pic_x_2 = pic_x_4) or
(pic_x_6 = pic_x_7)
order by pic_x_a desc, pic_x_6 desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s21')
    
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.btsel10 
where (pic_x_a = pic_x_7) and
(decimal_10 > binary_32_signed) and
(binary_unsigned > binary_32_signed)
order by pic_9_7 asc, pic_x_7 desc, pic_x_a asc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s22')
    
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.btsel11 
where (pic_x_a = pic_x_7) or
(decimal_10 = binary_unsigned) or
(binary_unsigned = binary_32_signed)
order by decimal_10 desc, pic_x_a asc, pic_9_7 desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s23')
    
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.pvsel02 
where pic_x_1 = 'B'
order by pic_x_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s24')
    
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.svsel13 
where medium_int = 1000
order by new_name_4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 2)
    
    _testmgr.testcase_end(desc)

def test003(desc="""a03"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0009 : A03
    #  Description:        This test verifies the SQL SELECT
    #                      statement with WHERE clause
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    #
    
    # Create LOG file
    
    #         select normal where clause test case - this tests the use of
    #         a BETWEEN predicate in a where clause.
    #
    
    stmt = """SELECT * from """ + gvars.g_schema_arkcasedb + """.btsel01 
where binary_32_u between pic_comp_1 and binary_64_s
order by binary_signed;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s0')
    
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 between 'A' and 'D'
order by syskey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s1')
    
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.btsel03 
where binary_64_s between pic_9_7 and 1201
order by syskey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s2')
    
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.btsel04 
where 150 between 100 and pic_comp_1
order by syskey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s3')
    
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.btsel05 
where 'mike' between col_9 and col_10
order by syskey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s4')
    
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.btsel06 
where (col_1 * 2) between col_3 and col_2
order by pic_x_a, pic_x_b, pic_x_c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s5')
    
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.btsel07 
where pic_x_b NOT between pic_x_a and pic_x_c
order by pic_x_c, pic_x_b, pic_x_a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s6')
    
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.btsel08 
where pic_252 between 'A' and pic_1
order by large_int;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s7')
    
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.btsel09 
where pic_x_6 between (pic_x_5 + 5) and pic_x_7
order by pic_x_a desc, pic_x_6 desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s8')
    
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.btsel10 
where decimal_10 between binary_unsigned and
(binary_32_signed + 100)
order by pic_9_7 asc, pic_x_7 desc, pic_x_a asc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s9')
    
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.btsel10 
where (decimal_10 * 2) not between binary_32_signed
and binary_unsigned
order by pic_9_7 asc, pic_x_7 desc, pic_x_a asc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s10')
    
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.btsel10 
where not ((decimal_10 * 2) between binary_32_signed
and binary_unsigned)
order by pic_9_7 asc, pic_x_7 desc, pic_x_a asc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s11')
    
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.btsel11 
where decimal_10 between binary_unsigned - 50
and binary_32_signed + 50
order by decimal_10 desc, pic_x_a asc, pic_9_7 desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s12')
    
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.pvsel03 
where new_name_2 between 5 and 7
order by new_name_4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 4)
    
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.pvsel03 
where new_name_2 between 7 and 5
order by new_name_4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.svsel13 
where medium_int between pic_comp_1 and 1000
order by new_name_4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 3)
    
    _testmgr.testcase_end(desc)

def test004(desc="""a04"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0009 : A04
    #  Description:        This test verifies the SQL SELECT
    #                      statement with WHERE clause
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    #
    
    #         select normal where clause test case - this tests the use of
    #         an IN predicate in the where clause.
    #
    
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.btsel01 
where binary_signed in (binary_32_u,pic_comp_1,
decimal_2_signed)
order by binary_signed;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s0')
    
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in ('B','C')
order by syskey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s1')
    
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.btsel03 where
((pic_9_7 + 1120) in (binary_64_s,120)) or
(((pic_9_7 * 2) + 20) in (binary_64_s, 120))
order by syskey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s2')
    
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.btsel04 
where (medium_int / 2) not in (pic_comp_1,500)
order by syskey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s3')
    
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.btsel05 
where 'mary' in (col_2,col_5,col_6)
order by syskey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s4')
    
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.btsel06 
where col_1 in (col_2,col_3,col_21,col_9 * 2)
order by pic_x_a, pic_x_b, pic_x_c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s5')
    
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.btsel07 
where pic_x_a not in ('jo','al')
order by pic_x_c, pic_x_b, pic_x_a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s6')
    
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.btsel07 
where not (pic_x_a in ('jo','al'))
order by pic_x_c, pic_x_b, pic_x_a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s7')
    
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.btsel08 
where 1000 in (large_int,500)
order by large_int;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s8')
    
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.btsel09 
where pic_x_7 in ((pic_x_6 * 2),30)
order by pic_x_a desc, pic_x_6 desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s9')
    
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.btsel10 
where decimal_10 in (binary_unsigned,110,25)
order by pic_9_7 asc, pic_x_7 desc, pic_x_a asc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s10')
    
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.btsel11 
where pic_9_7 not in (decimal_10,binary_unsigned,
binary_32_signed)
order by decimal_10 desc, pic_x_a asc, pic_9_7 desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s11')
    
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.pvsel04 
where pic_comp_1 in (200,300)
order by pic_comp_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s12')
    
    _testmgr.testcase_end(desc)

def test005(desc="""a05"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0009 : A05
    #  Description:        This test verifies the SQL SELECT
    #                      statement with WHERE clause
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    #
    
    #         select normal test case with where clause - this tests
    #         the use of a LIKE predicate in the where clause.
    #
    
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.btsel01 
where char_10 like 'steven' or
pic_x_7 like 'bob%' or
var_char like 'jim_y'
order by binary_signed;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s0')
    
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.btsel01 
where char_10 like 'steven    '
order by binary_signed;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s1')
    
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 like '_'
order by syskey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s2')
    
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.btsel03 
where pic_x4_a not like 'joe '
order by syskey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s3')
    
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.btsel03 
where not (pic_x4_a like 'joe ')
order by syskey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s4')
    
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.btsel04 
where var_char like 'b%'
order by syskey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s5')
    
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.btsel05 
where col_9 not like '__e'
order by syskey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s6')
    
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.btsel06 
where pic_x_a like '%'
order by pic_x_a, pic_x_b, pic_x_c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s7')
    
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.btsel06 
where pic_x_a like '%%'
order by pic_x_a, pic_x_b, pic_x_c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s8')
    
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.btsel07 
where pic_x_a like '%_'
order by pic_x_c, pic_x_b, pic_x_a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s9')
    
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.btsel07 
where pic_x_a like '_%_'
order by pic_x_c, pic_x_b, pic_x_a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s10')
    
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.btsel07 
where pic_x_a like 'al'
order by pic_x_c, pic_x_b, pic_x_a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.btsel07 
where pic_x_a like '_al'
order by pic_x_c, pic_x_b, pic_x_a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s11')
    
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.btsel07 
where pic_x_a like 'al_'
order by pic_x_c, pic_x_b, pic_x_a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s12')
    
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.btsel07 
where pic_x_a like 'al '
order by pic_x_c, pic_x_b, pic_x_a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s13')
    
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.btsel08 
where pic_252 like '__r%s%'
order by large_int;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s14')
    
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.btsel09 
where pic_x_4 like '___  '
order by pic_x_a desc, pic_x_6 desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s15')
    
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.btsel10 
where char_10 like '_b_d_f%h%'
order by pic_9_7 asc, pic_x_7 desc, pic_x_a asc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s16')
    
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.btsel11 
where char_10 not like '_b_d_f%h%'
order by decimal_10 desc, pic_x_a asc, pic_9_7 desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s17')
    
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.pvsel01 
where pic_x_7 like 'walter '
order by pic_decimal_3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s18')
    
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.svsel11 
where col_6 like 'walter '
order by col_4, col_8;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s19')
    
    _testmgr.testcase_end(desc)

def test006(desc="""a06"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0009 : A06
    #  Description:        This test verifies the SQL SELECT
    #                      statement with WHERE clause
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    #
    
    #         select normal test case with where clause - this tests
    #         the use of an ESCAPE character in a LIKE predicate of
    #         a where clause.
    #
    
    stmt = """select *
from """ + gvars.g_schema_arkcasedb + """.btsel09 
where pic_x_2 like 't\_go' escape '\\\'
order by pic_x_a desc, pic_x_6 desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s0')

    stmt = """select *
from """ + gvars.g_schema_arkcasedb + """.btsel09 
where pic_x_4 like 'to\%go' escape '\\\'
order by pic_x_a desc, pic_x_6 desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s1')

    # TRAFODION This may need some more work.  The orignal table inserts use '\t', 
    # which may also be problematic using python.  You should see one row
    # returned if you are able to get the escape for \t right.
    stmt = """select *
from """ + gvars.g_schema_arkcasedb + """.btsel09 
where pic_x_a like '\ts' escape '\\\'
order by pic_x_a desc, pic_x_6 desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)

    stmt = """select *
from """ + gvars.g_schema_arkcasedb + """.btsel09 
where pic_x_2 like 't\__o' escape '\\\'
order by pic_x_a desc, pic_x_6 desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s3')
    
    stmt = """select *
from """ + gvars.g_schema_arkcasedb + """.btsel09 
where pic_x_4 like 'to\%%' escape '\\\'
order by pic_x_a desc, pic_x_6 desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s4')
 
    # TRAFODION This may need some more work.  The orignal table inserts use '\t',
    # which may also be problematic using python.  You should see one row
    # returned if you are able to get the escape for \t right.
    stmt = """select *
from """ + gvars.g_schema_arkcasedb + """.btsel09 
where pic_x_a like '\t\_' escape '\\\'
order by pic_x_a desc, pic_x_6 desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
   
    stmt = """select *
from """ + gvars.g_schema_arkcasedb + """.btsel09 
where pic_x_4 like '\\\%   ' escape '\\\'
order by pic_x_a desc, pic_x_6 desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s6')
    
    stmt = """select *
from """ + gvars.g_schema_arkcasedb + """.btsel07 
where pic_x_a like 'al' escape ' '
order by pic_x_c, pic_x_b, pic_x_a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """select *
from """ + gvars.g_schema_arkcasedb + """.btsel07 
where pic_x_a like '  al' escape ' '
order by pic_x_c, pic_x_b, pic_x_a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s7')
    
    stmt = """select *
from """ + gvars.g_schema_arkcasedb + """.btsel09 
where pic_x_2 like 't__go' escape '_'
order by pic_x_a desc, pic_x_6 desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s8')
    
    stmt = """select *
from """ + gvars.g_schema_arkcasedb + """.btsel09 
where pic_x_4 like 'to_%go' escape '_'
order by pic_x_a desc, pic_x_6 desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s9')
    
    stmt = """select *
from """ + gvars.g_schema_arkcasedb + """.btsel09 
where pic_x_4 like 'to_%%' escape '_'
order by pic_x_a desc, pic_x_6 desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s10')
    
    stmt = """select *
from """ + gvars.g_schema_arkcasedb + """.btsel09 
where pic_x_a like '__t_%' escape '_'
order by pic_x_a desc, pic_x_6 desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s11')
    
    stmt = """select *
from """ + gvars.g_schema_arkcasedb + """.btsel09 
where pic_x_4 like '___%   ' escape '_'
order by pic_x_a desc, pic_x_6 desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s12')
    
    stmt = """select *
from """ + gvars.g_schema_arkcasedb + """.btsel09 
where pic_x_2 like 't%_go' escape '%'
order by pic_x_a desc, pic_x_6 desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s13')
    
    stmt = """select *
from """ + gvars.g_schema_arkcasedb + """.btsel09 
where pic_x_4 like 'to%%go' escape '%'
order by pic_x_a desc, pic_x_6 desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s14')
    
    stmt = """select *
from """ + gvars.g_schema_arkcasedb + """.btsel09 
where pic_x_2 like 't%__o' escape '%'
order by pic_x_a desc, pic_x_6 desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s15')
    
    stmt = """select *
from """ + gvars.g_schema_arkcasedb + """.btsel09 
where pic_x_a like '%%t%_' escape '%'
order by pic_x_a desc, pic_x_6 desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s16')
    
    stmt = """select *
from """ + gvars.g_schema_arkcasedb + """.btsel09 
where pic_x_4 like '%%%_   ' escape '%'
order by pic_x_a desc, pic_x_6 desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s17')
    
    _testmgr.testcase_end(desc)

def test007(desc="""a07"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0009 : A07
    #  Description:        This test verifies the SQL SELECT
    #                      statement with WHERE clause
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    #
    
    #          select normal test case with where clause - this tests the use
    #          of the FOR read uncommitted access, FOR read committed access, and FOR repeatable
    #          access clauses. Only syntax is checked here.
    #
    
    #   **** check for locking on audited tables ****
    
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.btsel06 
where col_7 = 100
for read committed access
order by pic_x_a, pic_x_b, pic_x_c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s0')
    
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.btsel04 
where medium_int <= 1000
for read uncommitted access
order by syskey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s1')
    
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.btsel07 
where pic_x_b < 'Q'
for serializable access
order by pic_x_c, pic_x_b, pic_x_a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s2')
    
    #  **** check for locking on non-audited tables ****
    
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.btsel05 
where pic_x_a > 'abe'
for read uncommitted access
order by syskey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s3')
    
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.btsel05 
where pic_x_a > 'abe'
for read committed access
order by syskey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s4')
    
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.btsel05 
where pic_x_a > 'abe'
for serializable access
order by syskey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s5')
    
    #  **** check for locking on views ****
    
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.pvsel04 
where pic_comp_1 in (200,300)
for read uncommitted access
order by pic_comp_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s6')
    
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.pvsel01 
where binary_signed > 50
for read committed access
order by pic_decimal_3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s7')
    
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.svsel11 
where col_1 > 50
for read committed access
order by col_4, col_8;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s8')
    
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.pvsel02 
where pic_x_1 = 'B'
for serializable access
order by pic_x_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s9')
    
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.svsel13 
where medium_int = 1000
for serializable access
order by new_name_4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 2)
    
    _testmgr.testcase_end(desc)

def test008(desc="""a08"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0009 : A08
    #  Description:        This test verifies the SQL SELECT
    #                      statement with WHERE clause
    #                      Order by clause with aggregates is non
    #                      ANSI. Testware correction made on Oct 22
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    
    #         select normal where clause test case - this tests the selection
    #         of aggregate functions (COUNT, AVG, MAX, MIN, SUM). The
    #         following attributes of aggregates are tested:
    #             SELECT all set function (function argument a value expression,
    #                                      optionally preceded by ALL, value
    #                                      expression a simple column spec)
    #             SELECT distinct set function (function argument a column spec,
    #                                           preceded by DISTINCT)
    #             SELECT the average, max, min, sum of expressions
    #             SELECT an aggregate expression involving SYSKEY
    #             SELECT an expression with aggregates in it
    #             SELECT more than one aggregate
    #
    
    #  select ALL
    
    stmt = """select count(*)
from """ + gvars.g_schema_arkcasedb + """.btsel01 
where var_char = 'thomas';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s0')
    #       order by binary_signed;
    
    stmt = """select avg(medium_int)
from """ + gvars.g_schema_arkcasedb + """.pvsel01 
where medium_int <> 8000;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s1')
    #       order by pic_decimal_3;
    
    stmt = """select max(ALL new_name_3)
from """ + gvars.g_schema_arkcasedb + """.pvsel03 
where new_name_1 = 80;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s2')
    #       order by new_name_4;
    
    #  select aggregates on 0 records
    
    stmt = """select count(*)
from """ + gvars.g_schema_arkcasedb + """.btsel03 
where binary_32_u < 0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s3')
    #       order by syskey;
    
    stmt = """select avg(binary_64_s)
from """ + gvars.g_schema_arkcasedb + """.btsel03 
where binary_32_u < 0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s4')
    #       order by syskey;
    
    stmt = """select count(*), avg(binary_64_s)
from """ + gvars.g_schema_arkcasedb + """.btsel03 
where binary_32_u < 0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s5')
    #       order by syskey;
    
    stmt = """select count(*), avg(binary_64_s), avg(binary_32_u)
from """ + gvars.g_schema_arkcasedb + """.btsel03 
where binary_32_u < 0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s6')
    #       order by syskey;
    
    #  select DISTINCT
    
    stmt = """select SUM(distinct binary_64_s)
from """ + gvars.g_schema_arkcasedb + """.btsel01 
where binary_32_u > 50;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s7')
    #       order by binary_signed;
    
    stmt = """select count(distinct medium_int)
from """ + gvars.g_schema_arkcasedb + """.pvsel01 
where medium_int not in (1000,10000);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s8')
    #       order by pic_decimal_3;
    
    stmt = """select count(distinct var_char)
from """ + gvars.g_schema_arkcasedb + """.svsel13 
where (new_name_1 = 80) or (new_name_2 = 5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s9')
    #       order by new_name_4;
    
    #  select an expression inside an aggregate
    
    stmt = """select avg(ALL binary_32_u + pic_comp_1)
from """ + gvars.g_schema_arkcasedb + """.btsel01 
where (pic_comp_1 <> 60);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s10')
    #       order by binary_signed;
    
    stmt = """select max(ALL new_name_1 / new_name_2)
from """ + gvars.g_schema_arkcasedb + """.svsel13 
where ((new_name_1 = 80) or (new_name_1 = 90)) and
((new_name_2 = 5) or (new_name_2 = 6));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s11')
    #       order by new_name_4;
    
    stmt = """select sum ((col_1 + col_4) + 1000)
from """ + gvars.g_schema_arkcasedb + """.svsel11 
where col_6 like '*';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s12')
    #       order by col_4, col_8;
    
    #  select an expression with SYSKEY in an aggregate
    
    stmt = """select avg(SYSKEY + binary_64_s)
from """ + gvars.g_schema_arkcasedb + """.btsel03 
where SYSKEY <> 0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8411')
    #       order by syskey;
    
    #  select expression of aggregates
    
    stmt = """select (sum(pic_decimal_1) / count(*))
from """ + gvars.g_schema_arkcasedb + """.btsel01 
where pic_comp_3 > 100.6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s14')
    #       order by binary_signed;
    
    stmt = """select avg(pic_comp_1 ) + sum(pic_comp_1)
from """ + gvars.g_schema_arkcasedb + """.svsel13 
where pic_comp_1 > 100;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s15')
    #       order by new_name_4;
    
    stmt = """select sum(decimal_1) + sum(decimal_1)
from """ + gvars.g_schema_arkcasedb + """.btsel01 
where decimal_3_unsigned <> 110;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s16')
    #       order by binary_signed;
    
    #  select multiple aggregates
    
    stmt = """select sum(pic_decimal_3),avg(pic_decimal_3),max(pic_decimal_3),
min(pic_decimal_3),count(distinct pic_decimal_3),count(*)
from """ + gvars.g_schema_arkcasedb + """.pvsel01 
where pic_decimal_3 < 8;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s17')
    #       order by pic_decimal_3;
    
    stmt = """select sum(new_name_1), avg(new_name_2), max(new_name_3)
from """ + gvars.g_schema_arkcasedb + """.svsel13 
where pic_comp_1 > 100;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s18')
    
    _testmgr.testcase_end(desc)

def test009(desc="""a09"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    #  Test case name:	pretsta09
    #  Description:		This test creates the table btre207, and its
    # 			indes, and inserts the values into the table.
    #  Expected Results:
    #
    stmt = """create table btre207 (
empnum              PIC 9(4)     not null
, empname             PIC X(18)    default null
, regnum              PIC 99       default null
, branchnum           PIC 99       default null
, job                 VARCHAR (12)
)
clustering key ( empnum , job )
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create index btre207i on
 btre207 ( empname );"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create index btre207j on
 btre207 ( regnum, branchnum );"""
    output = _dci.cmdexec(stmt)
    
    #   Insert values needed for T139 (NULLs and DML);
    #   a SUBSET of records:
    #    insert into btre207
    #      values (   1,'ROGER GREEN',   99, null, 'UNKNOWN' ) ;
    #    insert into btre207
    #      values (  23,'JERRY HOWARD',   2, 1, 'MANAGER' ) ;
    #    insert into btre207
    #      values (  29,'JACK RAYMOND',   1, 1, 'MANAGER' ) ;
    #    insert into btre207
    #      values (  43,'PAUL WINTER',    5, 1, 'MANAGER' ) ;
    #    insert into btre207
    #      values (  78,'SPOT TO FILL',  77, 7, 'PROGRAMMER' ) ;
    #    insert into btre207
    #      values (  79,'SPOT TO FILL',  77, 8, 'SECRETARY' ) ;
    #    insert into btre207
    #      values (1001,       null , null , null , 'UNKNOWN' ) ;
    
    stmt = """update statistics for table btre207 ;"""
    output = _dci.cmdexec(stmt)
    stmt = """select * from btre207 
order by empnum;"""
    output = _dci.cmdexec(stmt)
    
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0009 : 9
    #  Description:        This test verifies the SQL/K SELECT
    #                      statement with WHERE clause
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    #
    
    stmt = """create table taba8a (a char(10)) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table taba8b (a varchar(10)) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into taba8a values ('one_');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into taba8a values ('ONE%');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into taba8b values ('one_');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into taba8b values ('ONE%');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select a.empnum, a.empname, ''
from """ + gvars.g_schema_arkcasedb + """.btre207 a
where a.branchnum in (1,7)
order by 1,2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s0')
    
    stmt = """set param ?P1 '%n%';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """set param ?P2 '%N%';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """set param ?P3 '%n%@12';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """set param ?P4 '%N%@12';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """set param ?P5 '%\_%';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """set param ?P6 '%\%%';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """set param ?tc '@';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """set param ?esc '\';"""
    output = _dci.cmdexec(stmt)
    
    #  Check the CH table
    
    stmt = """select * from taba8a 
where a like '%n%';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s1')
    
    stmt = """select * from taba8a 
where a like ?P1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s2')
    
    stmt = """select * from taba8a 
where upshift(a) like '%N%';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s3')
    
    stmt = """select * from taba8a 
where upshift(a) like ?P2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s4')
    
    stmt = """select * from taba8a 
where a like upshift('%n%');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s5')
    
    stmt = """select * from taba8a 
where a like upshift(?P1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s6')
    
    stmt = """select * from taba8a 
where upshift(a) like upshift('%n%');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s7')
    
    stmt = """select * from taba8a 
where upshift(a) like upshift(?P1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s8')
    
    stmt = """select * from taba8a 
where a like '%\_%' escape '\\\';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s9')
    
    stmt = """select * from taba8a 
where a like ?P5 escape '\\\';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s10')
    
    stmt = """select * from taba8a 
where upshift(a) like '%\%%' escape '\\\';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s11')
    
    stmt = """select * from taba8a 
where upshift(a) like ?P6 escape '\\\';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s12')
    
    stmt = """select * from taba8a 
where a like upshift('%\_%') escape '\\\';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s13')
    
    stmt = """select * from taba8a 
where a like upshift(?P5) escape '\\\';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s14')
    
    stmt = """select * from taba8a 
where upshift(a) like upshift('%\_%') escape '\\\';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s15')
    
    stmt = """select * from taba8a 
where upshift(a) like upshift(?P5) escape '\\\';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s16')
    
    stmt = """select * from taba8a 
where a like '%\_%' escape ?esc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """select * from taba8a 
where a like ?P5 escape ?esc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """select * from taba8a 
where upshift(a) like '%\%%' escape ?esc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """select * from taba8a 
where upshift(a) like ?P6 escape ?esc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """select * from taba8a 
where a like upshift('%\_%') escape ?esc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """select * from taba8a 
where a like upshift(?P5) escape ?esc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """select * from taba8a 
where upshift(a) like upshift('%\_%') escape ?esc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """select * from taba8a 
where upshift(a) like upshift(?P5) escape '\\\';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s24')
    
    #   select * from taba8a
    #     where a like '%n%@12' terminate '@';
    
    #   select * from taba8a
    #     where a like ?P3 terminate '@';
    
    #   select * from taba8a
    #     where upshift(a) like '%N%@12' terminate '@';
    
    #   select * from taba8a
    #     where upshift(a) like ?P4 terminate '@';
    
    #   select * from taba8a
    #     where a like upshift('%n%@12') terminate '@';
    
    #   select * from taba8a
    #     where a like upshift(?P3) terminate '@';
    
    #   select * from taba8a
    #     where upshift(a) like upshift('%n%@12') terminate '@';
    
    #   select * from taba8a
    #     where upshift(a) like upshift(?P3) terminate '@';
    
    #   select * from taba8a
    #     where a like '%n%@12' terminate ?tc;
    
    #   select * from taba8a
    #     where a like ?P3 terminate ?tc;
    
    #   select * from taba8a
    #     where upshift(a) like '%N%@12' terminate ?tc;
    
    #   select * from taba8a
    #     where upshift(a) like ?P4 terminate ?tc;
    
    #   select * from taba8a
    #     where a like upshift('%n%@12') terminate ?tc;
    
    #   select * from taba8a
    #     where a like upshift(?P3) terminate ?tc;
    
    #   select * from taba8a
    #     where upshift(a) like upshift('%n%@12') terminate ?tc;
    
    #   select * from taba8a
    #     where upshift(a) like upshift(?P3) terminate '@';
    
    #   select * from taba8a
    #     where a like '%\_%@12' escape '\' terminate '@';
    
    #   select * from taba8a
    #     where a like ?P3 escape '\' terminate '@';
    
    #   select * from taba8a
    #     where upshift(a) like '%\%%@12' escape '\' terminate '@';
    
    #   select * from taba8a
    #     where upshift(a) like ?P4 escape '\' terminate '@';
    
    #   select * from taba8a
    #     where a like upshift('%\_%@12') escape '\' terminate '@';
    
    #   select * from taba8a
    #     where a like upshift(?P3) escape '\' terminate '@';
    
    #   select * from taba8a
    #     where upshift(a) like upshift('%\_%@12')
    #                                     escape '\' terminate '@';
    
    #   select * from taba8a
    #     where upshift(a) like upshift(?P3) escape '\' terminate '@';
    
    #   select * from taba8a
    #     where a like '%\_%@12' escape ?esc terminate ?tc;
    
    #   select * from taba8a
    #     where a like ?P3 escape ?esc terminate ?tc;
    
    #   select * from taba8a
    #     where upshift(a) like '%\%%@12' escape ?esc terminate ?tc;
    
    #   select * from taba8a
    #     where upshift(a) like ?P4 escape ?esc terminate ?tc;
    
    #   select * from taba8a
    #     where a like upshift('%\_%@12') escape ?esc terminate ?tc;
    
    #   select * from taba8a
    #     where a like upshift(?P3) escape ?esc terminate ?tc;
    
    #   select * from taba8a
    #     where upshift(a) like upshift('%\_%@12')
    #                                      escape ?esc terminate ?tc;
    
    #   select * from taba8a
    #     where upshift(a) like upshift(?P3) escape ?esc terminate '@';
    
    #  Check the VCH table
    
    stmt = """select * from taba8b 
where a like '%n%';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s25')
    
    stmt = """select * from taba8b 
where a like ?P1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s26')
    
    stmt = """select * from taba8b 
where upshift(a) like '%N%';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s27')
    
    stmt = """select * from taba8b 
where upshift(a) like ?P2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s28')
    
    stmt = """select * from taba8b 
where a like upshift('%n%');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s29')
    
    stmt = """select * from taba8b 
where a like upshift(?P1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s30')
    
    stmt = """select * from taba8b 
where upshift(a) like upshift('%n%');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s31')
    
    stmt = """select * from taba8b 
where upshift(a) like upshift(?P1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s32')
    
    stmt = """select * from taba8b 
where a like '%\_%' escape '\\\';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s33')
    
    stmt = """select * from taba8b 
where a like ?P5 escape '\\\';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s34')
    
    stmt = """select * from taba8b 
where upshift(a) like '%\%%' escape '\\\';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s35')
    
    stmt = """select * from taba8b 
where upshift(a) like ?P6 escape '\\\';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s36')
    
    stmt = """select * from taba8b 
where a like upshift('%\_%') escape '\\\';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s37')
    
    stmt = """select * from taba8b 
where a like upshift(?P5) escape '\\\';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s38')
    
    stmt = """select * from taba8b 
where upshift(a) like upshift('%\_%') escape '\\\';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s39')
    
    stmt = """select * from taba8b 
where upshift(a) like upshift(?P5) escape '\\\';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s40')
    
    stmt = """select * from taba8b 
where a like '%\_%' escape ?esc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """select * from taba8b 
where a like ?P5 escape ?esc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """select * from taba8b 
where upshift(a) like '%\%%' escape ?esc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """select * from taba8b 
where upshift(a) like ?P6 escape ?esc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """select * from taba8b 
where a like upshift('%\_%') escape ?esc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """select * from taba8b 
where a like upshift(?P5) escape ?esc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """select * from taba8b 
where upshift(a) like upshift('%\_%') escape ?esc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """select * from taba8b 
where upshift(a) like upshift(?P5) escape '\\\';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s48')
    
    #  select * from taba8b
    #    where a like '%n%@12' terminate '@';
    
    #  select * from taba8b
    #    where a like ?P3 terminate '@';
    
    #  select * from taba8b
    #    where upshift(a) like '%N%@12' terminate '@';
    
    #  select * from taba8b
    #    where upshift(a) like ?P4 terminate '@';
    
    #  select * from taba8b
    #    where a like upshift('%n%@12') terminate '@';
    
    #  select * from taba8b
    #    where a like upshift(?P3) terminate '@';
    
    #  select * from taba8b
    #    where upshift(a) like upshift('%n%@12') terminate '@';
    
    #  select * from taba8b
    #    where upshift(a) like upshift(?P3) terminate '@';
    
    #  select * from taba8b
    #    where a like '%n%@12' terminate ?tc;
    
    #  select * from taba8b
    #    where a like ?P3 terminate ?tc;
    
    #  select * from taba8b
    #    where upshift(a) like '%N%@12' terminate ?tc;
    
    #  select * from taba8b
    #    where upshift(a) like ?P4 terminate ?tc;
    
    #  select * from taba8b
    #    where a like upshift('%n%@12') terminate ?tc;
    
    #  select * from taba8b
    #    where a like upshift(?P3) terminate ?tc;
    
    #  select * from taba8b
    #    where upshift(a) like upshift('%n%@12') terminate ?tc;
    
    #  select * from taba8b
    #    where upshift(a) like upshift(?P3) terminate '@';
    
    #  select * from taba8b
    #    where a like '%\_%@12' escape '\' terminate '@';
    
    #  select * from taba8b
    #    where a like ?P3 escape '\' terminate '@';
    
    #  select * from taba8b
    #    where upshift(a) like '%\%%@12' escape '\' terminate '@';
    
    #  select * from taba8b
    #    where upshift(a) like ?P4 escape '\' terminate '@';
    
    #  select * from taba8b
    #    where a like upshift('%\_%@12') escape '\' terminate '@';
    
    #  select * from taba8b
    #    where a like upshift(?P3) escape '\' terminate '@';
    
    #  select * from taba8b
    #    where upshift(a) like upshift('%\_%@12')
    #                                    escape '\' terminate '@';
    
    #  select * from taba8b
    #    where upshift(a) like upshift(?P3) escape '\' terminate '@';
    
    #  select * from taba8b
    #    where a like '%\_%@12' escape ?esc terminate ?tc;
    
    #  select * from taba8b
    #    where a like ?P3 escape ?esc terminate ?tc;
    
    #  select * from taba8b
    #    where upshift(a) like '%\%%@12' escape ?esc terminate ?tc;
    
    #  select * from taba8b
    #    where upshift(a) like ?P4 escape ?esc terminate ?tc;
    
    #  select * from taba8b
    #    where a like upshift('%\_%@12') escape ?esc terminate ?tc;
    
    #  select * from taba8b
    #    where a like upshift(?P3) escape ?esc terminate ?tc;
    
    #  select * from taba8b
    #    where upshift(a) like upshift('%\_%@12')
    #                                     escape ?esc terminate ?tc;
    
    #  select * from taba8b
    #    where upshift(a) like upshift(?P3) escape ?esc terminate '@';
    
    stmt = """reset param;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """drop table taba8a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table taba8b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #  Test case name:	psttsta09
    #  Description:		This test drops the table btre207, and its index.
    #  Expected Results:
    #
    stmt = """drop index btre207i;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index btre207j;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """drop table btre207;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test010(desc="""a10"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0009 : A10
    #  Description:        This test verifies the SQL SELECT
    #                      statement with WHERE clause
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    
    #   -- TESTCASE SUMMARY
    #   LIKE predicates with null-padded columns
    
    stmt = """drop index i1;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index i2;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index i3;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """drop table t1;"""
    output = _dci.cmdexec(stmt)
    #    drop catalog
    
    #create catalog
    
    stmt = """create table t1 
(pa       char(4)      no default   not null,
pb       char(4)      no default   not null,
i1a      char(4)      no default   not null,
i1b      char(3)      no default   not null,
i2       char(4)      no default   not null,
i3       varchar(4)   no default   not null,
cn       char(3)      no default   not null,
vn       varchar(4)   no default   not null,
cs       char(4)      no default   not null,
primary key (pa ascending, pb descending));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #  NOTE : Iam SURPRISED that this does not have INSERT statements.
    
    stmt = """create index i1
on t1 (i1a descending, i1b ascending);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index i2
on t1 (i2 ascending) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index i3
on t1 (i3 ascending) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into t1 
values ('A', 'A', 'A', 'A', 'A', 'A','A', 'A', 'A');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into t1 
values ('B', 'B', 'B', 'B', 'B', 'B','B', 'B', 'B');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    #  Like with a null-padded column that is the left part of a
    #  two-column primary key.
    #  Prior to C30.S06 the following query returned zero rows.
    stmt = """select cs from t1 where pa like 'A%';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s4')
    
    #  Like with a null-padded column that is the right part of a
    #  two-column primary key.
    #  Prior to C30.S06 the following query returned zero rows.
    stmt = """select cs from t1 where pa = 'B' and pb like 'B%';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s5')
    
    #  Like with a null-padded column that is the left part of a
    #  two-column index.
    #  Prior to C30.S06 the following query returned zero rows.
    stmt = """select cs from t1 where i1a like 'A%';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s6')
    
    #  Like with a null-padded column that is the right part of a
    #  two-column index.
    #  Prior to C30.S06 the following query returned zero rows.
    stmt = """select cs from t1 where i1a = 'B' and i1b like 'B%';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s7')
    
    #  Like with a null-padded column that is a one-column index.
    #  Prior to C30.S06 the following query returned zero rows.
    stmt = """select cs from t1 where i2 like 'A%';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s8')
    
    #  Like with a null-padded varchar column that is a one-column index.
    #  Prior to C30.S06 the following query returned zero rows.
    stmt = """select cs from t1 where i3 like 'A%';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s9')
    
    #  Like with a null-padded column that is not an index.
    stmt = """select cs from t1 where cn like 'A%';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s10')
    
    #  Like with a null-padded varchar column that is not an index.
    stmt = """select cs from t1 where vn like 'A%';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s11')
    
    stmt = """drop index i1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop index i2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop index i3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop table t1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test011(desc="""a11"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0009 : A11
    #  Description:        This test verifies the SQL SELECT
    #                      statement with WHERE clause
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    #
    
    stmt = """drop table t1;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table  t2;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table t1 
(c1 char(4) no default not null,
c2 char(4) no default not null,
primary key (c1));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into t1 values ('AA01', 'AA01');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 values ('AA02', 'AA02');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 values ('BB01', 'BB01');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 values ('BB02', 'BB02');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 values ('CC01', 'CC01');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 values ('CC02', 'CC02');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 values ('    ', '    ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """create table  t2 
(c1 char(4) no default not null,
c2 char(4) no default not null,
primary key (c1));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into t2 values ('AA01', 'AA01');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t2 values ('AA02', 'AA02');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t2 values ('BB01', 'BB01');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t2 values ('BB02', 'BB02');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t2 values ('CC01', 'CC01');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t2 values ('CC02', 'CC02');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t2 values ('    ', '    ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    #  Later on , when using DML , use the following statement
    #  instead  of the above insert statements.
    #  insert into t2 (select * from  t1);
    
    #   -- TESTCASE SUMMARY
    #   LIKE transformation and evaluation
    #
    #  Tests to demonstrate that LIKE need not be retained for
    #  patterns of the form 'AB%'.
    
    #  LIKEs using a column that is a key.
    
    stmt = """select c1 from t1 where c1 like '%';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s2')
    
    stmt = """select c1 from t1 where c1 like '_';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """select c1 from t1 where c1 like '';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """select c1 from t1 where c1 like 'A%0%';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s3')
    
    stmt = """select c1 from t1 where c1 like 'BB01%';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s4')
    
    stmt = """select c1 from t1 where c1 like 'CC0%';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s5')
    
    stmt = """select c1 from t1 where c1 like '_A0%';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s6')
    
    stmt = """select c1 from t1 where c1 like 'A%%';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s7')
    
    stmt = """select c1 from t1 where c1 like '%A0%';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s8')
    
    stmt = """select c1 from t1 where c1 like 'A% ';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    #  LIKEs using a column that is not a key.
    
    stmt = """select c2 from t1 where c2 like '%';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s9')
    
    stmt = """select c2 from t1 where c2 like '_';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """select c2 from t1 where c2 like '';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """select c2 from t1 where c2 like 'A%0%';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s10')
    
    stmt = """select c2 from t1 where c2 like 'BB01%';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s11')
    
    stmt = """select c2 from t1 where c2 like 'CC0%';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s12')
    
    stmt = """select c2 from t1 where c2 like '_A0%';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s13')
    
    stmt = """select c2 from t1 where c2 like 'A%%';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s14')
    
    stmt = """select c2 from t1 where c2 like '%A0%';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s15')
    
    stmt = """select c2 from t1 where c2 like 'A% ';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """select c1 from t1 where c1 like 'BB02 %';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s16')
    
    stmt = """select c2 from t1 where c2 like 'BB02 %';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s17')
    
    #  Tests of LIKEs with multiple tables.
    
    #  Inner join with a like predicate on a column in the outer table.
    stmt = """select t1.c1
from t1, t2 
where t1.c1 = t2.c1
and t1.c1 like '_B%'
and t1.c1 > '    '
and t1.c1 < 'ZZZZ'
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s18')
    
    #  Inner join with a like predicate on a column in the inner table.
    stmt = """select t1.c1
from t1, t2 
where t1.c1 = t2.c1
and t2.c1 like '_B%'
and t1.c1 > '    '
and t1.c1 < 'ZZZZ'
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s19')
    
    #  Outer join with a like predicate on a column in the outer table.
    stmt = """select t1.c1
from t1 left join t2 on t1.c1 = t2.c1
where t1.c1 like '_B%'
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s20')
    
    #  Outer join with a like predicate on a column in the inner table.
    stmt = """select t1.c1
from t1 left join t2 on t1.c1 = t2.c1
where t2.c1 like '_B%'
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s21')
    
    #  Correlated subquery with a like predicate on a column in the outer query.
    stmt = """select t1.c1
from t1 
where
 t1.c1 in
(select t2.c1
from t2 
where t1.c1 = t2.c1)
and t1.c1 like '_B%'
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s22')
    
    #  Correlated subquery with a like predicate on a column in the outer query.
    stmt = """select t1.c1
from t1 
where
 t1.c1 in
(select t2.c1
from t2 
where t1.c1 = t2.c1
and t1.c1 like '_B%')
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s23')
    
    #  Correlated subquery with a like predicate on a column in the subquery.
    stmt = """select t1.c1
from t1 
where
 t1.c1 in
(select t2.c1
from t2 
where t1.c1 = t2.c1
and t2.c1 like '_B%')
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s24')
    
    # Cleanup.
    stmt = """drop table t1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table t2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test012(desc="""a12"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0009 : 2
    #  Description:        This test verifies the SQL SELECT
    #                      statement with WHERE clause
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description
    # =================== End Test Case Header  ===================
    
    stmt = """drop table b2t1;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table b2t2;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table b2t3;"""
    output = _dci.cmdexec(stmt)
    
    #CREATE catalog
    
    stmt = """CREATE table b2t1 
(int_col      PIC S9(6)V9(3) COMP NOT NULL
,largeint_col NUMERIC (18,3) SIGNED
,real_col     REAL
,double_col   DOUBLE PRECISION
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """CREATE table b2t2 
(int_col      PIC S9(6)V9(3) COMP
,  largeint_col NUMERIC (18,3) SIGNED
,  real_col     REAL
,  double_col   DOUBLE PRECISION
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """CREATE table b2t3 
(int_col      PIC S9(6)V9(3) COMP NOT NULL
,  largeint_col NUMERIC (18,3) SIGNED
,  real_col     REAL
,  double_col   DOUBLE PRECISION
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # Insert values into table b2t1
    stmt = """INSERT INTO b2t1 
VALUES ( -123456.789
, -123456.789
, -123456.789
, -123456.789
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO b2t1 
VALUES (  -1 ,    -1 ,    -1 ,    -1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO b2t1 
VALUES (   0 ,      0 ,      0 ,   0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO b2t1 
VALUES (   1 ,       1,       1,   1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO b2t1 
VALUES (  2.1 ,   2.1 ,   2.1 ,   2.1000000);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO b2t1 
VALUES (3210   ,   3210 ,  4321,   4321);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # Insert values into table b2t2
    # Different code is excercised for 10 or more rows. So b2t2 is
    # loaded with the following.  Skewed toward the positive.
    #
    stmt = """INSERT INTO b2t2 
VALUES ( -214748.364 ,  -214748.364 ,  -2.14748364E5 ,  -2.14748364E5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO b2t2 
VALUES (-1 ,     -1 ,  -1 ,  -1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO b2t2 
VALUES (         -0.086
,             -0.086
,             -8.6e-2
,             -8.6000000e-2
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO b2t2 
VALUES (          0
,               0
,               0
,               0
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO b2t2 
VALUES (        0.086
,             0.086
,             8.6e-2
,             8.60000000e-2
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO b2t2 
VALUES (          1
,               1
,               1
,               1
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO b2t2 
VALUES (  214748.364
,       214748.364
,       214748.364
,       214748.364
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO b2t2 
VALUES (        256
,            256
,            256
,            256
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO b2t2 
VALUES (        512
,             512
,             512
,             512
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO b2t2 
VALUES (       1024
,            1024
,            1024
,            1024
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO b2t2 (int_col
,  largeint_col
,  real_col
,  double_col
)
VALUES (       2048
,           2048
,           2048
,           2048
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # For grins, put in a null in each column. (When this is working.)
    #
    stmt = """INSERT INTO b2t2 (
largeint_col
,  real_col
,        double_col
)
VALUES (
4096
,  4096
,  4096
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO b2t2 (int_col ,  real_col ,  double_col)
VALUES (       8092 ,            8092 ,            8092);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO b2t2 (int_col , largeint_col , double_col)
VALUES (      16348 ,           16384 ,           16384);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO b2t2 (int_col , largeint_col ,  real_col)
VALUES (      32768 ,           32768   ,           32768);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # Two rows with same value.
    #
    stmt = """INSERT INTO b2t2 (int_col
, largeint_col , real_col , double_col)
VALUES (655.35 ,  655.35 ,    6.5535e2 ,    6.55350000e2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO b2t2 (int_col ,largeint_col ,
real_col ,  double_col)
VALUES (655.35 ,  655.35 ,  6.5535e2 ,     6.5535e2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO b2t2 (int_col, largeint_col,
real_col ,  double_col)
VALUES (65536 , 65536 ,  6.5536e4 , 6.55360000e4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # Insert values into table b2t3
    # Put in small values so  doesn't overflow.
    #
    stmt = """INSERT INTO b2t3 
VALUES (       1
,            1
,            1
,            1
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO b2t3 
VALUES (       2
,            2
,            2
,            2
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO b2t3 
VALUES (       2
,            2
,            2
,            2
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO b2t3 
VALUES (       3
,            3
,            3
,            3
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO b2t3 
VALUES (       3
,            3
,            3
,            3
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO b2t3 
VALUES (       3
,            3
,            3
,            3
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO b2t3 
VALUES (       4
,            4
,            4
,            4
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO b2t3 
VALUES (       5
,            5
,            5
,            5
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    #   -- TESTCASE SUMMARY
    #     Test undocumented Surveyor aggregate
    #     fuctions.
    #
    #     The aggregates , , , , and  are used to
    #     support Surveyor.
    #
    #     The answers from  and  are actually closer to the results
    #     from spreadsheet program's S and S functions.  The
    #     result is also different from standard spreadsheet programs probably
    #     because S style function is used instead of .
    #
    
    #
    #   Try all undocumented aggregates for table with less then 10 rows.
    #
    
    stmt = """SELECT  (int_col)
,  (largeint_col)
,  (real_col)
,  (double_col)
FROM b2t1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s3')
    
    #
    #  Need to test  for < 50 % and >= 50%.
    #
    #
    #   Use PREPARE and EXECUTE after internal error fixed (Release 3?)
    #
    #     PREPARE Ptile_1 FROM
    #     SELECT  (int_col,  ?param_1)
    #     ,  (largeint_col, ?param_2)
    #     ,  (real_col,     ?param_3)
    #     ,  (double_col,   ?param_4)
    #    FROM b2t1;
    #    --
    #    -- Need to use separate params to avoid problem of parameter
    #    -- taking on the attrabutes of first column it is used with
    #    -- (although in this case it probably doesn't matter).
    #    --
    #     EXECUTE Ptile_1 USING ?param_1 = 33
    #     , ?param_2 = 33
    #     , ?param_3 = 33
    #     , ?param_4 = 33
    #      ;
    #     EXECUTE Ptile_1 USING ?param_1 = 66
    #   , ?param_2 = 66
    #   , ?param_3 = 66
    #   , ?param_4 = 66
    #     ;
    #
    stmt = """SELECT  (int_col),   (largeint_col),   (real_col),   (double_col)
FROM b2t1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s4')
    
    #
    #  Try a few of the documented aggregates.
    #
    stmt = """SELECT SUM (int_col)
FROM b2t1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s5')
    #
    #   Try all undocumented aggregates for table with 10 or more rows.
    #
    
    stmt = """SELECT  (int_col)
,   (largeint_col)
,   (real_col)
,   (double_col)
FROM b2t2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s6')
    
    #
    #  Need to test  for < 50 % and >= 50%.
    #
    #
    #  Use PREPARE and EXECUTE when internal error fixed. (Release 3?)
    #
    #     PREPARE Ptile_2 FROM
    #     SELECT  (int_col,  ?param_5)
    #    ,   (largeint_col, ?param_6)
    #    ,   (real_col,     ?param_7)
    #    ,   (double_col,   ?param_8)
    #         FROM b2t2;
    #    --
    #    -- Need to use separate params to avoid problem of parameter
    #    -- taking on the attrabutes of first column it is used with
    #    -- (although in this case it probably doesn't matter).
    #    --
    #     EXECUTE Ptile_2 USING ?param_5 = 33
    #    ,  ?param_6 = 33
    #    ,  ?param_7 = 33
    #    ,  ?param_8 = 33
    #     ;
    #
    #     EXECUTE Ptile_2 USING ?param_5 = 66
    #    ,  ?param_6 = 66
    #    ,  ?param_7 = 66
    #    ,  ?param_8 = 66
    #     ;
    
    stmt = """SELECT  (int_col)
,   (largeint_col)
,   (real_col)
,   (double_col)
FROM b2t2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s7')
    
    #
    #  Try a few of the documented aggregates.
    stmt = """SELECT SUM (int_col)
FROM b2t2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s8')
    
    #
    #   Try all undocumented aggregates for table with less then 10 rows
    #   and small number range.
    #
    
    stmt = """SELECT  (int_col)
,  (largeint_col)
,  (real_col)
,  (double_col)
FROM b2t3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s9')
    
    stmt = """SELECT  (int_col)
,   (largeint_col)
,   (real_col)
,   (double_col)
FROM b2t3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s10')
    
    stmt = """drop table b2t1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table b2t2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table b2t3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

