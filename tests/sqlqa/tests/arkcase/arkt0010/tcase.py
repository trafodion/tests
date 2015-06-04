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
    #  Test case name:     arkt0010 : A01
    #  Description:        This test verifies the SQL SELECT
    #                      statement. Tests only normal (non-join &
    #                      non-subquery) select statements, with
    #                      GROUP BY, HAVING & ORDER BY clauses &
    #                      some complex queries with all together
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    
    stmt = """select char_1,decimal_1 from """ + gvars.g_schema_arkcasedb + """.btsel01 
group by char_1,decimal_1
order by char_1,decimal_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s0')
    
    stmt = """select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
group by pic_x_1
order by pic_x_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s1')
    
    stmt = """select pic_x_7,pic_9_7 from """ + gvars.g_schema_arkcasedb + """.btsel03 
group by pic_9_7,pic_x_7
order by pic_9_7,pic_x_7 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s2')
    
    stmt = """select medium_int from """ + gvars.g_schema_arkcasedb + """.btsel04 
group by medium_int
order by medium_int;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s3')
    
    stmt = """select pic_x_b from """ + gvars.g_schema_arkcasedb + """.btsel05 
group by pic_x_b
order by pic_x_b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s4')
    
    stmt = """select pic_x_a,col_1,col_3 from """ + gvars.g_schema_arkcasedb + """.btsel06 
group by pic_x_a,col_1,col_3
order by pic_x_a,col_1,col_3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s5')
    
    stmt = """select pic_x_a,col_1,col_3 from """ + gvars.g_schema_arkcasedb + """.btsel06 
group by pic_x_a, col_1,col_1, col_3
order by pic_x_a, col_1, col_3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s6')
    
    stmt = """select pic_x_a,col_1,col_3 from """ + gvars.g_schema_arkcasedb + """.btsel06 
group by pic_x_a,col_1,col_3, col_1
order by pic_x_a,col_1,col_3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s7')
    
    stmt = """select pic_x_a from """ + gvars.g_schema_arkcasedb + """.btsel07 
group by pic_x_a
order by pic_x_a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s8')
    
    stmt = """select pic_1,large_int from """ + gvars.g_schema_arkcasedb + """.btsel08 
group by pic_1,large_int
order by pic_1,large_int;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s9')
    
    #  Order by should have all the col names in the select list
    #  Testware correction made on oct22
    stmt = """select large_int from """ + gvars.g_schema_arkcasedb + """.btsel08 
group by pic_1,large_int
order by large_int;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s10')
    #       order by pic_1,arge_int;
    
    stmt = """select pic_x_5 from """ + gvars.g_schema_arkcasedb + """.btsel09 
group by pic_x_5
order by pic_x_5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s11')
    
    stmt = """select binary_32_signed from """ + gvars.g_schema_arkcasedb + """.btsel10 
group by binary_32_signed
order by binary_32_signed;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s12')
    
    stmt = """select decimal_10 from """ + gvars.g_schema_arkcasedb + """.btsel11 
group by decimal_10
order by decimal_10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s13')
    
    stmt = """select new_name_1 from """ + gvars.g_schema_arkcasedb + """.pvsel03 
group by new_name_1
order by new_name_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s14')
    
    stmt = """select new_name_1 from """ + gvars.g_schema_arkcasedb + """.svsel13 
group by new_name_1
order by new_name_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s15')
    
    stmt = """select SYSKEY
from """ + gvars.g_schema_arkcasedb + """.btsel04 
group by SYSKEY
order by SYSKEY;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 8)
    
    # Order by should have all the col names in the select list
    # Testware correction made on oct 22
    stmt = """select medium_int, binary_64_s, medium_int * binary_64_s
from """ + gvars.g_schema_arkcasedb + """.btsel01 
group by medium_int,binary_64_s
order by medium_int,binary_64_s;"""
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
    #  Test case name:     arkt0011 : A02
    #  Description:        This test verifies the SQL simple
    #                      SELECT statements with JOIN
    #                      select joins simple testcase - this tests
    #                      the use of SELECT DISTINCT and SELECT ALL
    #                      statements on multiple tables.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    
    stmt = """select distinct pic_x_1,pic_x_7
from  """ + gvars.g_schema_arkcasedb + """.btsel02, """ + gvars.g_schema_arkcasedb + """.btsel03 
order by pic_x_1,pic_x_7;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s0')
    
    stmt = """select all pic_x_1,pic_x_7
from  """ + gvars.g_schema_arkcasedb + """.btsel02, """ + gvars.g_schema_arkcasedb + """.btsel03 
order by  """ + gvars.g_schema_arkcasedb + """.btsel02.syskey,  """ + gvars.g_schema_arkcasedb + """.btsel03.syskey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s1')
    
    stmt = """select distinct   """ + gvars.g_schema_arkcasedb + """.btsel02.*,pic_x_7,binary_32_u
from  """ + gvars.g_schema_arkcasedb + """.btsel02, """ + gvars.g_schema_arkcasedb + """.btsel03 
order by  """ + gvars.g_schema_arkcasedb + """.btsel02.pic_x_1,pic_x_7,binary_32_u;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s2')
    
    stmt = """select all   """ + gvars.g_schema_arkcasedb + """.btsel02.*,pic_x_7,binary_32_u
from  """ + gvars.g_schema_arkcasedb + """.btsel02, """ + gvars.g_schema_arkcasedb + """.btsel03 
order by  """ + gvars.g_schema_arkcasedb + """.btsel02.syskey,  """ + gvars.g_schema_arkcasedb + """.btsel03.syskey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s3')
    
    stmt = """select distinct *
from  """ + gvars.g_schema_arkcasedb + """.btsel02, """ + gvars.g_schema_arkcasedb + """.btsel10 
order by pic_x_1, pic_9_7 asc, pic_x_7 desc, pic_x_a asc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s4')
    
    stmt = """select all *
from  """ + gvars.g_schema_arkcasedb + """.btsel02, """ + gvars.g_schema_arkcasedb + """.btsel10 
order by syskey, pic_9_7 asc, pic_x_7 desc, pic_x_a asc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s5')
    
    stmt = """select distinct   """ + gvars.g_schema_arkcasedb + """.btsel02.*,  """ + gvars.g_schema_arkcasedb + """.btsel10.*
from  """ + gvars.g_schema_arkcasedb + """.btsel02, """ + gvars.g_schema_arkcasedb + """.btsel10 
order by pic_x_1, pic_9_7 asc, pic_x_7 desc, pic_x_a asc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s6')
    
    stmt = """select all   """ + gvars.g_schema_arkcasedb + """.btsel02.*,  """ + gvars.g_schema_arkcasedb + """.btsel10.*
from  """ + gvars.g_schema_arkcasedb + """.btsel02, """ + gvars.g_schema_arkcasedb + """.btsel10 
order by syskey, pic_9_7 asc, pic_x_7 desc, pic_x_a asc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s7')
    
    stmt = """select distinct new_name_3,pic_x_7
from  """ + gvars.g_schema_arkcasedb + """.pvsel03, """ + gvars.g_schema_arkcasedb + """.pvsel04 
order by new_name_3,pic_x_7;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s8')
    
    stmt = """select all new_name_3,pic_x_7
from  """ + gvars.g_schema_arkcasedb + """.pvsel03, """ + gvars.g_schema_arkcasedb + """.pvsel04 
order by new_name_4, pic_comp_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s9')
    
    stmt = """select distinct pic_x_b,pic_x_7
from  """ + gvars.g_schema_arkcasedb + """.btsel07, """ + gvars.g_schema_arkcasedb + """.pvsel04 
order by pic_x_b,pic_x_7;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s10')
    
    stmt = """select all pic_x_b,pic_x_7
from  """ + gvars.g_schema_arkcasedb + """.btsel07, """ + gvars.g_schema_arkcasedb + """.pvsel04 
order by pic_x_c, pic_x_b, pic_x_a, pic_comp_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s11')
    
    stmt = """select distinct   """ + gvars.g_schema_arkcasedb + """.pvsel03.new_name_3,  """ + gvars.g_schema_arkcasedb + """.svsel13.new_name_3
from  """ + gvars.g_schema_arkcasedb + """.pvsel03, """ + gvars.g_schema_arkcasedb + """.svsel13 
order by  """ + gvars.g_schema_arkcasedb + """.pvsel03.new_name_3,  """ + gvars.g_schema_arkcasedb + """.svsel13.new_name_3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s12')
    
    stmt = """select all   """ + gvars.g_schema_arkcasedb + """.pvsel03.new_name_3,  """ + gvars.g_schema_arkcasedb + """.svsel13.new_name_3
from  """ + gvars.g_schema_arkcasedb + """.pvsel03, """ + gvars.g_schema_arkcasedb + """.svsel13 
order by  """ + gvars.g_schema_arkcasedb + """.pvsel03.new_name_4,  """ + gvars.g_schema_arkcasedb + """.svsel13.new_name_4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s13')
    
    stmt = """select distinct col_3
from  """ + gvars.g_schema_arkcasedb + """.svsel13, """ + gvars.g_schema_arkcasedb + """.svsel11 
order by col_3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s14')
    
    stmt = """select all col_3
from  """ + gvars.g_schema_arkcasedb + """.svsel13, """ + gvars.g_schema_arkcasedb + """.svsel11 
order by new_name_4, col_4, col_8;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s15')
    
    stmt = """select distinct firs.pic_x_1,secon.pic_x_1
from  """ + gvars.g_schema_arkcasedb + """.btsel02 firs, """ + gvars.g_schema_arkcasedb + """.btsel02 secon
order by firs.pic_x_1,secon.pic_x_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s16')
    
    stmt = """select all firs.pic_x_1,secon.pic_x_1
from  """ + gvars.g_schema_arkcasedb + """.btsel02 firs, """ + gvars.g_schema_arkcasedb + """.btsel02 secon
order by firs.syskey, secon.syskey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s17')
    
    stmt = """select distinct firs.new_name_3,secon.new_name_3
from  """ + gvars.g_schema_arkcasedb + """.pvsel03 firs, """ + gvars.g_schema_arkcasedb + """.pvsel03 secon
order by firs.new_name_3,secon.new_name_3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s18')
    
    stmt = """select all firs.new_name_3,secon.new_name_3
from  """ + gvars.g_schema_arkcasedb + """.pvsel03 firs, """ + gvars.g_schema_arkcasedb + """.pvsel03 secon
order by firs.new_name_4, secon.new_name_4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s19')
    
    stmt = """select distinct firs.new_name_3,secon.new_name_3
from  """ + gvars.g_schema_arkcasedb + """.svsel13 firs, """ + gvars.g_schema_arkcasedb + """.svsel13 secon
order by firs.new_name_3,secon.new_name_3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s20')
    
    stmt = """select all firs.new_name_3,secon.new_name_3
from  """ + gvars.g_schema_arkcasedb + """.svsel13 firs, """ + gvars.g_schema_arkcasedb + """.svsel13 secon
order by firs.new_name_4, secon.new_name_4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s21')
    
    stmt = """select distinct pic_x_1,binary_64_s,medium_int
from  """ + gvars.g_schema_arkcasedb + """.btsel02,
 """ + gvars.g_schema_arkcasedb + """.btsel03,
 """ + gvars.g_schema_arkcasedb + """.btsel04 
order by pic_x_1,binary_64_s,medium_int;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s22')
    
    stmt = """select all pic_x_1,binary_64_s,medium_int
from  """ + gvars.g_schema_arkcasedb + """.btsel02,
 """ + gvars.g_schema_arkcasedb + """.btsel03,
 """ + gvars.g_schema_arkcasedb + """.btsel04 
order by  """ + gvars.g_schema_arkcasedb + """.btsel02.syskey,  """ + gvars.g_schema_arkcasedb + """.btsel03.syskey,  """ + gvars.g_schema_arkcasedb + """.btsel04.syskey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s23')
    
    _testmgr.testcase_end(desc)

def test003(desc="""a03"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0010 : A03
    #  Description:        This test verifies the SQL SELECT
    #                      statement. Tests only normal (non-join &
    #                      non-subquery) select statements, with
    #                      GROUP BY, HAVING & ORDER BY clauses &
    #                      some complex queries with all together
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.btsel01 
order by char_1,decimal_1, binary_signed;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s0')
    
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.btsel02 
order by pic_x_1 ASC, syskey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s1')
    
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.btsel03 
order by 4,1 DESC, syskey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s2')
    
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.btsel04 
order by 2, syskey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s3')
    
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.btsel05 
order by pic_x_b DESC, syskey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s4')
    
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.btsel06 
order by pic_x_a DESC,col_1,col_3 ASC, pic_x_b, pic_x_c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s5')
    
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.btsel06 
order by pic_x_a , col_1,col_1, col_3, pic_x_b, pic_x_c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s6')
    
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.btsel06 
order by pic_x_a , col_1, col_3, col_1, pic_x_b, pic_x_c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s7')
    
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.btsel06 
order by pic_x_a , col_1 ASC, col_1 DESC, col_3, pic_x_b, pic_x_c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s8')
    
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.btsel07 
order by pic_x_a, pic_x_c, pic_x_b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s9')
    
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.btsel08 
order by 3  DESC, large_int ASC;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s10')
    
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.btsel09 
order by pic_x_5, pic_x_a, pic_x_6 desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s11')
    
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.btsel10 
order by binary_32_signed, pic_x_a, pic_9_7 asc, pic_x_7 desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s12')
    
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.btsel11 
order by decimal_10, pic_x_a, pic_9_7 desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s13')
    
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.pvsel03 
order by new_name_1, new_name_4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 4)
    
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.svsel13 
order by new_name_1, new_name_4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 4)
    
    #  order by SYSKEY
    
    stmt = """select SYSKEY,*
from """ + gvars.g_schema_arkcasedb + """.btsel03 
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 8)
    
    stmt = """select *,SYSKEY
from """ + gvars.g_schema_arkcasedb + """.btsel03 
order by 6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 8)
    
    stmt = """select *,SYSKEY
from """ + gvars.g_schema_arkcasedb + """.btsel03 
order by 4,6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 8)
    
    stmt = """select small_int
from """ + gvars.g_schema_arkcasedb + """.btsel01 
order by medium_int, binary_signed;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s19')
    
    _testmgr.testcase_end(desc)

def test004(desc="""a04"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0010 : A04
    #  Description:        This test verifies the SQL SELECT
    #                      statement. Tests only normal (non-join &
    #                      non-subquery) select statements, with
    #                      GROUP BY, HAVING & ORDER BY clauses &
    #                      some complex queries with all together
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    
    #  Query 1
    stmt = """select char_1, decimal_1
from """ + gvars.g_schema_arkcasedb + """.btsel01 
where (char_1 like '%') and
(var_char in ('B','jimmy','thomas','marilyn','christopher'))
and (binary_32_u between 50 and 100) and
(decimal_1 < (decimal_2_signed*100))
group by char_1,decimal_1
having decimal_1 between 2 and 8
order by decimal_1   DESC, char_1
for serializable access;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s0')
    
    #  Query 2
    stmt = """select distinct var_char,binary_64_s, pic_comp_1
from """ + gvars.g_schema_arkcasedb + """.btsel01 
where (char_1 like '%') and
(var_char in ('B','jimmy','thomas','marilyn','christopher'))
and (binary_32_u between 50 and 100) and
(decimal_1 < (decimal_2_signed*100))
group by binary_64_s,pic_comp_1, var_char
having binary_64_s > pic_comp_1
order by binary_64_s, 2 DESC, pic_comp_1, var_char
for serializable access;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s1')
    
    #  Order by should have all the cols in the select list
    #  Testware correction made on oct 22
    #  Query 3
    stmt = """select (new_name_1 * new_name_1), new_name_1, new_name_3
from """ + gvars.g_schema_arkcasedb + """.pvsel03 
where (new_name_1 between new_name_2 and 100) and
(new_name_3 in ('A','B','7')) and
(new_name_3 like '_      ') and
(new_name_1 > (new_name_2 + 20))
group by new_name_1,new_name_3
having new_name_1 = 80
order by new_name_3 ASC, new_name_1
for read committed access;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s2')
    
    #  Query 4
    stmt = """select new_name_1,new_name_4
from """ + gvars.g_schema_arkcasedb + """.svsel13 
where ((var_char like 'b%') or (var_char like 'tom')) and
(pic_comp_1 in (200,300,400,500)) and
(new_name_1 between 80 and 90)
group by new_name_1,new_name_4
having new_name_1 = 80
order by new_name_1, new_name_4
for read uncommitted access;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 3)
    
    #  Query 5
    stmt = """select medium_int,SYSKEY
from """ + gvars.g_schema_arkcasedb + """.btsel04 
where (medium_int > 200)
group by medium_int,SYSKEY
having medium_int in (999,1000,2000)
order by medium_int,SYSKEY;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 6)
    
    #  Query 6
    stmt = """select pic_x_b from """ + gvars.g_schema_arkcasedb + """.btsel05 
where col_1 = 'lowry'
group by pic_x_b
order by pic_x_b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s5')
    
    #  Query 7
    stmt = """select col_6, pic_x_a,col_1, pic_x_b, pic_x_c
from """ + gvars.g_schema_arkcasedb + """.btsel06 
where col_6 < 90
order by pic_x_a,col_1, pic_x_b, pic_x_c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s6')
    
    #  Query 8
    stmt = """select pic_1,large_int from """ + gvars.g_schema_arkcasedb + """.btsel08 
where large_int >= 100
group by pic_1,large_int
having large_int in (100,200,1000,2000)
order by pic_1,large_int;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s7')
    
    #  Query 9
    stmt = """select pic_x_5 from """ + gvars.g_schema_arkcasedb + """.btsel09 
where pic_x_6 <> 11
group by pic_x_5
order by pic_x_5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s8')
    
    #  Query 10
    stmt = """select decimal_10 from """ + gvars.g_schema_arkcasedb + """.btsel10 
group by decimal_10
having decimal_10 in (90,100,110,10000,50000)
order by decimal_10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s9')
    
    _testmgr.testcase_end(desc)

def test005(desc="""a05"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0010 : A05
    #  Description:        This test verifies the SQL SELECT
    #                      statement. Tests only normal (non-join &
    #                      non-subquery) select statements, with
    #                      GROUP BY, HAVING & ORDER BY clauses &
    #                      some complex queries with all together
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    
    stmt = """select large_int from """ + gvars.g_schema_arkcasedb + """.btsel08 
group by large_int
for read uncommitted access
order by large_int;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s0')
    
    stmt = """select pic_x_5 from """ + gvars.g_schema_arkcasedb + """.btsel09 
group by pic_x_5
having pic_x_5 > 4
for read committed access
order by pic_x_5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s1')
    
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.btsel10 
order by pic_9_7, pic_x_7 desc, pic_x_a asc
for serializable access;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s2')
    
    #   *****  non-audited tables *****
    
    stmt = """select pic_x_b from """ + gvars.g_schema_arkcasedb + """.btsel05 
group by pic_x_b
for read committed access
order by pic_x_b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s3')
    
    stmt = """select pic_x_b from """ + gvars.g_schema_arkcasedb + """.btsel05 
group by pic_x_b
having (pic_x_b = 'D') or (pic_x_b = 'B')
for serializable access
order by pic_x_b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s4')
    
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.btsel05 
order by pic_x_b, syskey
for read uncommitted access;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s5')
    
    #     **** views *****
    
    stmt = """select new_name_1 from """ + gvars.g_schema_arkcasedb + """.pvsel03 
group by new_name_1
for serializable access
order by new_name_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s6')
    
    stmt = """select new_name_1 from """ + gvars.g_schema_arkcasedb + """.svsel13 
group by new_name_1
for serializable access
order by new_name_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s7')
    
    stmt = """select new_name_1 from """ + gvars.g_schema_arkcasedb + """.pvsel03 
group by new_name_1
having new_name_1 = 80
for read uncommitted access
order by new_name_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s8')
    
    stmt = """select new_name_1 from """ + gvars.g_schema_arkcasedb + """.svsel13 
group by new_name_1
having new_name_1 = 80
for read uncommitted access
order by new_name_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s9')
    
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.pvsel03 
order by new_name_1, new_name_4
for read committed access;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 4)
    
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.svsel13 
order by new_name_1, new_name_4
for read committed access;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 4)
    
    _testmgr.testcase_end(desc)

def test006(desc="""a06"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0010 : A06
    #  Description:        This test verifies the SQL SELECT
    #                      statement. Tests only normal (non-join &
    #                      non-subquery) select statements, with
    #                      GROUP BY, HAVING & ORDER BY clauses &
    #                      some complex queries with all together.
    #                      Where clause should always precede the
    #                      other three clauses viz. order by,
    #                      having or group by (ansi).
    #                      group by , having and order by is
    #                      the order among the three clauses
    #                      Testware correction made on oct 22
    #
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    
    stmt = """select char_1, decimal_1
from """ + gvars.g_schema_arkcasedb + """.btsel01 
where (char_1 like '%') and
(var_char in ('B','jimmy','thomas','marilyn','christopher'))
and (binary_32_u between 50 and 100) and
(decimal_1 > decimal_2_signed)
group by char_1,decimal_1
having decimal_1 between 2 and 8
order by decimal_1   DESC, char_1
for serializable access;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s0')
    
    #  Query 2
    stmt = """select char_1, decimal_1
from """ + gvars.g_schema_arkcasedb + """.btsel01 
where (char_1 like '%') and
(var_char in ('B','jimmy','thomas','marilyn','christopher'))
and (binary_32_u between 50 and 100) and
(decimal_1 > decimal_2_signed)
group by char_1,decimal_1
having decimal_1 between 2 and 8
order by decimal_1   DESC, char_1
for read committed access;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s1')
    
    #  Query 3
    stmt = """select char_1, decimal_1
from """ + gvars.g_schema_arkcasedb + """.btsel01 
where (char_1 like '%') and
(var_char in ('B','jimmy','thomas','marilyn','christopher'))
and (binary_32_u between 50 and 100) and
(decimal_1 > decimal_2_signed)
group by char_1,decimal_1
having decimal_1 between 2 and 8
order by decimal_1   DESC, char_1
for read uncommitted access;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s2')
    
    #  Query 4
    stmt = """select distinct var_char,binary_64_s, pic_comp_1
from """ + gvars.g_schema_arkcasedb + """.btsel01 
where (char_1 like '%') and
(var_char in ('B','jimmy','thomas','marilyn','christopher'))
and (binary_32_u between 50 and 100) and
(decimal_1 > decimal_2_signed)
group by binary_64_s,pic_comp_1, var_char
having binary_64_s > pic_comp_1
order by binary_64_s, 2 DESC, pic_comp_1, var_char
for read committed access;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s3')
    
    #  Query 5
    stmt = """select distinct var_char,binary_64_s, pic_comp_1
from """ + gvars.g_schema_arkcasedb + """.btsel01 
where (char_1 like '%') and
(var_char in ('B','jimmy','thomas','marilyn','christopher'))
and (binary_32_u between 50 and 100) and
(decimal_1 > decimal_2_signed)
group by binary_64_s,pic_comp_1, var_char
having binary_64_s > pic_comp_1
order by binary_64_s, 2 DESC, pic_comp_1, var_char
for read uncommitted access;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s4')
    
    #  Query 6
    stmt = """select distinct var_char,binary_64_s, pic_comp_1
from """ + gvars.g_schema_arkcasedb + """.btsel01 
where (char_1 like '%') and
(var_char in ('B','jimmy','thomas','marilyn','christopher'))
and (binary_32_u between 50 and 100) and
(decimal_1 > decimal_2_signed)
group by binary_64_s,pic_comp_1, var_char
having binary_64_s > pic_comp_1
order by binary_64_s, 2 DESC, pic_comp_1, var_char
for serializable access;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s5')
    
    #  Query 7
    stmt = """select new_name_1,new_name_4
from """ + gvars.g_schema_arkcasedb + """.svsel13 
where ((var_char like 'b%') or (var_char like 'tom')) and
(pic_comp_1 in (200,300,400,500)) and
(new_name_1 between 80 and 90)
group by new_name_1,new_name_4
having new_name_1 = 80
order by new_name_1, new_name_4
for read uncommitted access;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 3)
    
    #  Query 8
    stmt = """select medium_int,SYSKEY
from """ + gvars.g_schema_arkcasedb + """.btsel04 
where (medium_int > 200)
group by medium_int,SYSKEY
having medium_int in (999,1000,2000)
order by medium_int, syskey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 6)
    
    #  Query 9
    stmt = """select pic_x_b
from """ + gvars.g_schema_arkcasedb + """.btsel05 
where col_1 = 'lowry'
group by pic_x_b
order by pic_x_b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s8')
    
    #  Query 10
    stmt = """select  col_6, pic_x_a,col_1, pic_x_b, pic_x_c
from """ + gvars.g_schema_arkcasedb + """.btsel06 
where col_6 < 90
order by pic_x_a,col_1, pic_x_b, pic_x_c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s9')
    
    #  Query 11
    stmt = """select pic_1,large_int
from """ + gvars.g_schema_arkcasedb + """.btsel08 
where large_int >= 100
group by pic_1,large_int
having large_int in (100,200,1000,2000)
order by pic_1,large_int;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s10')
    
    #  Query 12
    stmt = """select pic_x_5
from """ + gvars.g_schema_arkcasedb + """.btsel09 
where pic_x_6 <> 11
group by pic_x_5
order by pic_x_5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s11')
    
    #  Query 13
    stmt = """select decimal_10
from """ + gvars.g_schema_arkcasedb + """.btsel10 
group by decimal_10
having decimal_10 in (90,100,110,10000,50000)
order by decimal_10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s12')
    
    _testmgr.testcase_end(desc)

def test007(desc="""a07"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0010 : A07
    #  Description:        This test verifies the SQL SELECT
    #                      statement. Tests only normal (non-join &
    #                      non-subquery) select statements, with
    #                      GROUP BY, HAVING & ORDER BY clauses &
    #                      some complex queries with all together
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    
    stmt = """select char_1 , decimal_1
from """ + gvars.g_schema_arkcasedb + """.btsel01 
where
( char_1 like '%')
and
( var_char in
( 'B' ,
'jimmy'
,
'thomas'
,
'marilyn'
,
'christopher'
)
)
and
(
binary_32_u between 50 and 100
)
and ( decimal_1 < (decimal_2_signed * 100))
group by char_1 , decimal_1
having decimal_1 between 2 and 8
order by decimal_1 DESC,  char_1
for serializable access ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s0')
    
    # Moved the following query to testA30
    
    #       select distinct var_char,binary_64_s, pic_comp_1
    #       from btsel01
    #       where (char_1 like '%') and
    #             (var_char in ('B','jimmy','thomas','marilyn','christopher'))
    #         and (binary_32_u between 50 and 100) and
    #             (decimal_1 > decimal_2_signed)
    #       group by binary_64_s,pic_comp_1, var_char
    #       having binary_64_s > pic_comp_1
    #       order by binary_64_s, 2 DESC, pic_comp_1, var_char
    #       for serializable access ;
    
    stmt = """select                   (new_name_1*new_name_1), new_name_1, new_name_3
from                     """ + gvars.g_schema_arkcasedb + """.pvsel03 
where                    (new_name_1 between new_name_2 and 100) and
(new_name_3 in ('A','B','7')) and
(new_name_3 like '_') and
(new_name_1 > (new_name_2 + 20))
group by new_name_1,new_name_3
having new_name_1=80
order by new_name_3 ASC, new_name_1
for read committed access;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """SELECT new_name_1,new_name_4
FROM """ + gvars.g_schema_arkcasedb + """.svsel13 
WHERE ((var_char like 'b%') OR (var_char LIKE 'tom')) and
(pic_comp_1 IN (200,300,400,500)) AND
(new_name_1 BETWEEN 80 and 90)
group BY new_name_1,new_name_4
having new_name_1 = 80
ORDER by new_name_1, new_name_4
for read uncommitted access;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 3)
    
    stmt = """select medium_int,SYSKEY
from """ + gvars.g_schema_arkcasedb + """.btsel04 
where (medium_int > 200)
GROUP BY medium_int,SYSKEY
HAVING medium_int in (999,1000,2000)
order by medium_int, syskey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 6)
    
    stmt = """select PIC_X_B from """ + gvars.g_schema_arkcasedb + """.btsel05 
where COL_1 = 'lowry'
group by PIC_X_B
order by PIC_X_B;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s3')
    
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.btsel06 
where Col_6 < 90
order by pIc_X_a,cOL_1, pic_x_b, pic_x_c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s4')
    
    #  test use of space between > and = in the >= sign
    
    stmt = """select pic_1,large_int
from """ + gvars.g_schema_arkcasedb + """.btsel08 
where large_int >= 100
group by pic_1,large_int
having large_int in (100,200,1000,2000)
order by pic_1, large_int;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s5')
    
    stmt = """select pic_x_5 from """ + gvars.g_schema_arkcasedb + """.btsel09 where pic_x_6 <> 11
group by pic_x_5 order by pic_x_5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s6')
    
    stmt = """select decimal_10 from """ + gvars.g_schema_arkcasedb + """.btsel10 
group by decimal_10
having decimal_10 in
( 90,100,110,10000,50000)
order by decimal_10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s7')
    
    _testmgr.testcase_end(desc)

def test008(desc="""a08"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0010 : A08
    #  Description:        This test verifies the SQL SELECT
    #                      statement. Tests only normal (non-join &
    #                      non-subquery) select statements, with
    #                      GROUP BY, HAVING & ORDER BY clauses &
    #                      some complex queries with all together
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    
    #  select ALL
    
    stmt = """select binary_64_s,count(*)
from """ + gvars.g_schema_arkcasedb + """.btsel01 
group by binary_64_s
order by binary_64_s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s0')
    
    stmt = """select avg(large_int)
from """ + gvars.g_schema_arkcasedb + """.pvsel01 
group by medium_int;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s1')
    #       order by medium_int;
    
    stmt = """select binary_64_s, pic_comp_1, min(ALL decimal_2_signed)
from """ + gvars.g_schema_arkcasedb + """.btsel01 
group by binary_64_s,pic_comp_1
order by binary_64_s,pic_comp_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s2')
    
    stmt = """select new_name_2, sum(new_name_2)
from """ + gvars.g_schema_arkcasedb + """.pvsel03 
group by new_name_2
order by new_name_2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s3')
    
    stmt = """select pic_comp_1,min(var_char)
from """ + gvars.g_schema_arkcasedb + """.svsel13 
group by pic_comp_1
order by pic_comp_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s4')
    
    #  select DISTINCT
    
    stmt = """select pic_comp_1,AVG(distinct binary_32_u)
from """ + gvars.g_schema_arkcasedb + """.btsel01 
group by pic_comp_1
order by pic_comp_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s5')
    
    stmt = """select new_name_1,count(distinct var_char)
from """ + gvars.g_schema_arkcasedb + """.svsel13 
group by new_name_1
order by new_name_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s6')
    
    stmt = """select binary_64_s, min(distinct var_char)
from """ + gvars.g_schema_arkcasedb + """.btsel01 
group by binary_64_s
order by binary_64_s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s7')
    
    #  select an expression inside an aggregate
    
    stmt = """select binary_64_s, avg(ALL binary_32_u + pic_comp_1)
from """ + gvars.g_schema_arkcasedb + """.btsel01 
group by binary_64_s
order by binary_64_s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s8')
    
    stmt = """select medium_int, min(ALL large_int * small_int)
from """ + gvars.g_schema_arkcasedb + """.pvsel01 
group by medium_int
order by medium_int;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s9')
    
    stmt = """select medium_int, min(ALL large_int * medium_int)
from """ + gvars.g_schema_arkcasedb + """.pvsel01 
group by medium_int
order by medium_int;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s10')
    
    #  select an expression with SYSKEY in an aggregate
    
    stmt = """select pic_x_7, max(SYSKEY / 3 + medium_int)
from """ + gvars.g_schema_arkcasedb + """.btsel04 
group by pic_x_7
order by pic_x_7;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 7)
    
    #  select expression of aggregates
    
    stmt = """select medium_int,(sum(pic_decimal_3) + sum(small_int)) / 100
from """ + gvars.g_schema_arkcasedb + """.pvsel01 
group by medium_int
order by medium_int;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s12')
    
    stmt = """select medium_int,(sum(pic_decimal_3) + sum(medium_int)) / 100
from """ + gvars.g_schema_arkcasedb + """.pvsel01 
group by medium_int
order by medium_int;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s13')
    
    stmt = """select pic_comp_1,avg(pic_comp_1 ) + sum(pic_comp_1)
from """ + gvars.g_schema_arkcasedb + """.svsel13 
group by pic_comp_1
order by pic_comp_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s14')
    
    stmt = """select medium_int,sum(decimal_1) + sum(decimal_1)
from """ + gvars.g_schema_arkcasedb + """.btsel01 
group by medium_int
order by medium_int;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s15')
    
    stmt = """select medium_int,
sum(pic_decimal_3),avg(pic_decimal_3),max(pic_decimal_3),
min(pic_decimal_3),count(distinct pic_decimal_3),count(*)
from """ + gvars.g_schema_arkcasedb + """.pvsel01 
group by medium_int
order by medium_int;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s16')
    
    #  queries with where predicates
    
    stmt = """select binary_64_s, count(*)
from """ + gvars.g_schema_arkcasedb + """.btsel01 
where var_char = 'thomas'
group by binary_64_s
order by binary_64_s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s17')
    
    stmt = """select pic_comp_1, SUM(distinct binary_64_s)
from """ + gvars.g_schema_arkcasedb + """.btsel01 
where binary_32_u > 50
group by pic_comp_1
order by pic_comp_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s18')
    
    stmt = """select new_name_1, count(distinct var_char)
from """ + gvars.g_schema_arkcasedb + """.svsel13 
where (new_name_1 = 80) or (new_name_2 = 5)
group by new_name_1
order by new_name_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s19')
    
    stmt = """select pic_comp_1, avg(ALL binary_32_u + pic_comp_1)
from """ + gvars.g_schema_arkcasedb + """.btsel01 
where (pic_comp_1 <> 60)
group by pic_comp_1
order by pic_comp_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s20')
    
    stmt = """select binary_64_s, sum(decimal_1) + sum(decimal_1)
from """ + gvars.g_schema_arkcasedb + """.btsel01 
where decimal_3_unsigned <> 110
group by binary_64_s
order by binary_64_s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s21')
    
    stmt = """select medium_int,avg(large_int)
from """ + gvars.g_schema_arkcasedb + """.pvsel01 
where small_int <> 8000
group by medium_int
order by medium_int;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s22')
    
    #  select aggregate, group by SYSKEY
    
    stmt = """select avg(pic_comp_1)
from """ + gvars.g_schema_arkcasedb + """.btsel04 
group by SYSKEY;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s23')
    
    _testmgr.testcase_end(desc)

def test009(desc="""a09"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0010 : A09
    #  Description:        This test verifies the SQL SELECT
    #                      statement. Tests only normal (non-join &
    #                      non-subquery) select statements, with
    #                      GROUP BY, HAVING & ORDER BY clauses &
    #                      some complex queries with all together
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    
    #  test use of a HAVING clause with no GROUP BY clause
    
    stmt = """select max(binary_32_u)
from """ + gvars.g_schema_arkcasedb + """.btsel01 
having sum(pic_decimal_3) > 30;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s0')
    
    stmt = """select avg(pic_decimal_3)
from """ + gvars.g_schema_arkcasedb + """.btsel01 
having avg(pic_decimal_3) > 4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s1')
    
    stmt = """select count(*)
from """ + gvars.g_schema_arkcasedb + """.pvsel01 
having min(small_int) <= 10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s2')
    
    stmt = """select sum(col_4)
from """ + gvars.g_schema_arkcasedb + """.svsel11 
having count(*) = 8;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    # test select from 0 groups
    
    stmt = """select max(binary_64_s), min(binary_64_s)
from """ + gvars.g_schema_arkcasedb + """.btsel03 
group by pic_9_7
having pic_9_7 > 200;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """select binary_64_s,count(*)
from """ + gvars.g_schema_arkcasedb + """.btsel01 
group by binary_64_s
having sum(distinct pic_comp_1) < 1000
order by binary_64_s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s3')
    
    stmt = """select binary_64_s,count(*)
from """ + gvars.g_schema_arkcasedb + """.btsel01 
group by binary_64_s
having binary_64_s <> 200
order by binary_64_s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s4')
    
    stmt = """select binary_64_s,count(*)
from """ + gvars.g_schema_arkcasedb + """.btsel01 
group by binary_64_s
having sum(binary_64_s) > 2000
order by binary_64_s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s5')
    
    stmt = """select binary_64_s
from """ + gvars.g_schema_arkcasedb + """.btsel01 
group by binary_64_s
having sum(binary_64_s) > 2000
order by binary_64_s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s6')
    
    stmt = """select binary_64_s,count(*)
from """ + gvars.g_schema_arkcasedb + """.btsel01 
group by binary_64_s
having count(*) >= 2
order by binary_64_s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s7')
    
    stmt = """select avg(large_int)
from """ + gvars.g_schema_arkcasedb + """.pvsel01 
group by medium_int
having sum(large_int) > 0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s8')
    #       order by medium_int;
    
    stmt = """select binary_64_s, pic_comp_1, min(ALL decimal_2_signed)
from """ + gvars.g_schema_arkcasedb + """.btsel01 
group by binary_64_s, pic_comp_1
having max(binary_32_u) >= 50
order by binary_64_s, pic_comp_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s9')
    
    stmt = """select new_name_2, sum(new_name_2)
from """ + gvars.g_schema_arkcasedb + """.pvsel03 
group by new_name_2
having (sum(new_name_1) + min(new_name_1)) * 2 > 400
order by new_name_2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s10')
    
    stmt = """select pic_comp_1, min(var_char)
from """ + gvars.g_schema_arkcasedb + """.svsel13 
group by pic_comp_1
having min(new_name_1) + min(new_name_2) <> 86
order by pic_comp_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s11')
    
    stmt = """select pic_comp_1, AVG(distinct binary_32_u)
from """ + gvars.g_schema_arkcasedb + """.btsel01 
group by pic_comp_1
having avg(pic_comp_2) < 0.5
order by pic_comp_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s12')
    
    stmt = """select new_name_1
from """ + gvars.g_schema_arkcasedb + """.svsel13 
group by new_name_1
having sum(new_name_2) in (5,18)
order by new_name_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s13')
    
    stmt = """select binary_64_s, avg(ALL binary_32_u + pic_comp_1)
from """ + gvars.g_schema_arkcasedb + """.btsel01 
group by binary_64_s
having avg(ALL binary_32_u + pic_comp_1) > 100
order by binary_64_s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s14')
    
    stmt = """select binary_64_s
from """ + gvars.g_schema_arkcasedb + """.btsel01 
group by binary_64_s
having avg(ALL binary_32_u + pic_comp_1) > 100
order by binary_64_s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s15')
    
    #  queries with where predicates
    
    stmt = """select pic_comp_1, SUM(distinct binary_64_s)
from """ + gvars.g_schema_arkcasedb + """.btsel01 
where binary_32_u > 50
group by pic_comp_1
having sum(binary_signed) > 5000
order by pic_comp_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s16')
    
    stmt = """select new_name_1, count(distinct var_char)
from """ + gvars.g_schema_arkcasedb + """.svsel13 
where (new_name_1 = 80) or (new_name_2 = 5)
group by new_name_1
having avg(new_name_2) in (5,6)
order by new_name_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s17')
    
    stmt = """select pic_comp_1, avg(ALL binary_32_u + pic_comp_1)
from """ + gvars.g_schema_arkcasedb + """.btsel01 
where (pic_comp_1 <> 60)
group by pic_comp_1
having min(binary_signed) < 1000
order by pic_comp_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s18')
    
    stmt = """select binary_64_s, sum(decimal_1) + sum(decimal_1)
from """ + gvars.g_schema_arkcasedb + """.btsel01 
where decimal_3_unsigned <> 110
group by binary_64_s
having (max(pic_comp_2) between 0.2 and 0.99)
and (binary_64_s <> 1200)
order by binary_64_s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s19')
    
    stmt = """select medium_int, avg(large_int)
from """ + gvars.g_schema_arkcasedb + """.pvsel01 
where small_int <> 8000
group by medium_int
having not max(pic_x_1) = 'E'
order by medium_int;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s20')
    
    #  complex queries
    
    stmt = """select pic_comp_1, SUM(distinct binary_64_s)
from """ + gvars.g_schema_arkcasedb + """.btsel01 
where binary_32_u > 50
group by pic_comp_1
having sum(binary_signed) > 5000
order by pic_comp_1, 2
for serializable access;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s21')
    
    stmt = """select new_name_1, count(distinct var_char)
from """ + gvars.g_schema_arkcasedb + """.svsel13 
where (new_name_1 = 80) or (new_name_2 = 5)
group by new_name_1
having avg(new_name_2) in (5,6)
order by 1, 2 ASC
for read committed access;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s22')
    
    stmt = """select pic_comp_1, avg(ALL binary_32_u + pic_comp_1)
from """ + gvars.g_schema_arkcasedb + """.btsel01 
where (pic_comp_1 <> 60)
group by pic_comp_1
having min(binary_signed) < 1000
order by pic_comp_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s23')
    
    stmt = """select binary_64_s, sum(decimal_1) + sum(decimal_1), pic_comp_2
from """ + gvars.g_schema_arkcasedb + """.btsel01 
where decimal_3_unsigned <> 110
group by binary_64_s, pic_comp_2
having pic_comp_2 between 0.2 and 0.99
order by 2, binary_64_s, pic_comp_2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s24')
    
    stmt = """select medium_int, avg(large_int)
from """ + gvars.g_schema_arkcasedb + """.pvsel01 
where small_int <> 8000
group by medium_int
having not max(pic_x_1) = 'E'
order by medium_int
for read uncommitted access;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s25')
    
    #  select having aggregate(SYSKEY)
    
    stmt = """select pic_comp_1
from """ + gvars.g_schema_arkcasedb + """.btsel04 
group by pic_comp_1
having avg(SYSKEY) > 0
order by pic_comp_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s26')
    
    _testmgr.testcase_end(desc)

def test010(desc="""a10"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0010 : A10
    #  Description:        This test verifies the SQL SELECT
    #                      statement. Tests only normal (non-join &
    #                      non-subquery) select statements, with
    #                      GROUP BY, HAVING & ORDER BY clauses &
    #                      some complex queries with all together
    #  NOTE:
    #                      This test had group by col numbers
    #                      Had to substitute the queries with
    #                      queries using derived tables, to
    #                      handle the situation where the colomn
    #                      is not just the colomn name but an
    #                      expression
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    
    stmt = """select char_1,decimal_1 from """ + gvars.g_schema_arkcasedb + """.btsel01 
group by  char_1,decimal_1
order by  1,2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s0')
    
    stmt = """select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
group by pic_x_1
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s1')
    
    stmt = """select pic_x_7,pic_9_7 from """ + gvars.g_schema_arkcasedb + """.btsel03 
group by pic_9_7, pic_x_7
order by 2,1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s2')
    
    stmt = """select pic_x_a,col_1,col_3 from """ + gvars.g_schema_arkcasedb + """.btsel06 
group by pic_x_a, col_1, col_1, col_3
order by 1, 2, 3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s3')
    
    stmt = """select pic_x_a,col_1,col_3 from """ + gvars.g_schema_arkcasedb + """.btsel06 
group by pic_x_a, col_1, col_3, col_1
order by 1, 2, 3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s4')
    
    stmt = """select a , b from
(select medium_int * 2, binary_64_s + 100
from """ + gvars.g_schema_arkcasedb + """.btsel01) dt(a,b)
group by a,b
order by 1,2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s5')
    
    stmt = """select dt.a, dt.b from
(select medium_int * 2, binary_64_s
from """ + gvars.g_schema_arkcasedb + """.btsel01) dt(a,b)
group by a, b
order by 1, 2   ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s6')
    
    stmt = """select a,b  from
(select sum(medium_int), sum(pic_comp_1)
from """ + gvars.g_schema_arkcasedb + """.btsel01) tab(a,b)
group by a,b
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s7')
    
    stmt = """select x, y from
(select medium_int , binary_64_s
from """ + gvars.g_schema_arkcasedb + """.btsel01) dt(x,y)
group by x,y
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s8')
    
    stmt = """select dt.x, dt.y from
(select avg(medium_int * binary_64_s), sum(medium_int * binary_64_s)
from """ + gvars.g_schema_arkcasedb + """.btsel01) dt (x , y)
group by x,y
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s9')
    
    stmt = """select x, y from
(select medium_int * binary_64_s, medium_int
from """ + gvars.g_schema_arkcasedb + """.btsel01) tab (x,y)
group by x,y
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s10')
    
    _testmgr.testcase_end(desc)

def test011(desc="""a11"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0010 : A11
    #  Description:        This test verifies the SQL SELECT
    #                      statement. Tests only normal (non-join &
    #                      non-subquery) select statements, with
    #                      GROUP BY, HAVING & ORDER BY clauses &
    #                      some complex queries with all together
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    
    stmt = """drop view svsel20;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create view svsel20 (medium_int,aggr_exp)
as select
X.medium_int, (X.binary_64_s / sum(Y.binary_32_u) * 100)
from """ + gvars.g_schema_arkcasedb + """.btsel01 X,
""" + gvars.g_schema_arkcasedb + """.btsel03 Y
where X.medium_int = (Y.pic_9_7 * 100)
group by X.medium_int, X.binary_64_s
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from svsel20 
order by medium_int, aggr_exp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s0')
    
    stmt = """drop view svsel20;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

