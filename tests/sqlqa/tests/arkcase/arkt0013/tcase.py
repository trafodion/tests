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
    #  Test case name:     arkt0013 : A01
    #  Description:        This test verifies the SQL SELECT
    #                      statement. Tests JOIN-form select
    #                      statements with WHERE, GROUP BY,
    #                      HAVING & ORDER BY clauses and tests
    #                      some complex queries with all together
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    #
    #  obey set_env;
    # obey set_path;
    
    # Query 1
    stmt = """select pic_9_7
from  """ + gvars.g_schema_arkcasedb + """.btsel03, """ + gvars.g_schema_arkcasedb + """.btsel04 
group by pic_9_7
order by pic_9_7;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s0')
    
    # Query 2
    stmt = """select medium_int
from  """ + gvars.g_schema_arkcasedb + """.btsel03, """ + gvars.g_schema_arkcasedb + """.btsel04 
group by medium_int
order by medium_int;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s1')
    
    #  similar to above, without reference to btsel03
    #  (compare output - should be the same)
    
    # Query 3
    stmt = """select medium_int
from  """ + gvars.g_schema_arkcasedb + """.btsel04 
group by medium_int
order by medium_int;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s2')
    
    # Query 4
    stmt = """select pic_9_7, """ + gvars.g_schema_arkcasedb + """.btsel03.pic_x_7
from  """ + gvars.g_schema_arkcasedb + """.btsel03, """ + gvars.g_schema_arkcasedb + """.btsel04 
group by pic_9_7, """ + gvars.g_schema_arkcasedb + """.btsel03.pic_x_7
order by pic_9_7, """ + gvars.g_schema_arkcasedb + """.btsel03.pic_x_7;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s3')
    
    # Query 5
    stmt = """select pic_9_7,medium_int
from  """ + gvars.g_schema_arkcasedb + """.btsel03, """ + gvars.g_schema_arkcasedb + """.btsel04 
group by pic_9_7,medium_int
order by pic_9_7,medium_int;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s4')
    
    # Query 6
    stmt = """select pic_x_1,pic_9_7,medium_int
from  """ + gvars.g_schema_arkcasedb + """.btsel02,
 """ + gvars.g_schema_arkcasedb + """.btsel03,
 """ + gvars.g_schema_arkcasedb + """.btsel04 
group by pic_x_1,pic_9_7,medium_int
order by pic_x_1,pic_9_7,medium_int;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s5')
    
    # Query 7
    stmt = """select decimal_1,new_name_1
from  """ + gvars.g_schema_arkcasedb + """.btsel01, """ + gvars.g_schema_arkcasedb + """.pvsel03 
group by decimal_1,new_name_1
order by decimal_1,new_name_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s6')
    
    # Query 8
    stmt = """select decimal_1,new_name_1
from  """ + gvars.g_schema_arkcasedb + """.btsel01, """ + gvars.g_schema_arkcasedb + """.svsel13 
group by decimal_1,new_name_1
order by decimal_1,new_name_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s7')
    
    # Query 9
    stmt = """select  """ + gvars.g_schema_arkcasedb + """.pvsel01.medium_int, """ + gvars.g_schema_arkcasedb + """.pvsel04.medium_int
from  """ + gvars.g_schema_arkcasedb + """.pvsel01, """ + gvars.g_schema_arkcasedb + """.pvsel04 
group by  """ + gvars.g_schema_arkcasedb + """.pvsel01.medium_int, """ + gvars.g_schema_arkcasedb + """.pvsel04.medium_int
order by  """ + gvars.g_schema_arkcasedb + """.pvsel01.medium_int, """ + gvars.g_schema_arkcasedb + """.pvsel04.medium_int;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s8')
    
    # Query 10
    stmt = """select  """ + gvars.g_schema_arkcasedb + """.pvsel01.medium_int
from  """ + gvars.g_schema_arkcasedb + """.pvsel01, """ + gvars.g_schema_arkcasedb + """.svsel13 
group by  """ + gvars.g_schema_arkcasedb + """.pvsel01.medium_int
order by  """ + gvars.g_schema_arkcasedb + """.pvsel01.medium_int;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s9')
    
    # Query 11
    stmt = """select new_name_3,col_3
from  """ + gvars.g_schema_arkcasedb + """.svsel13, """ + gvars.g_schema_arkcasedb + """.svsel11 
group by new_name_3,col_3
order by new_name_3,col_3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s10')
    
    # Query 12
    stmt = """select secon.char_1, f.medium_int
from   """ + gvars.g_schema_arkcasedb + """.btsel01 f,   """ + gvars.g_schema_arkcasedb + """.btsel01 secon
group by secon.char_1,f.medium_int
order by secon.char_1,f.medium_int;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s11')
    
    # Query 13
    stmt = """select secon.medium_int
from  """ + gvars.g_schema_arkcasedb + """.pvsel01 f,  """ + gvars.g_schema_arkcasedb + """.pvsel01 secon
group by secon.medium_int
order by secon.medium_int;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s12')
    
    _testmgr.testcase_end(desc)

def test002(desc="""a02"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0013 : A02
    #  Description:        This test verifies the SQL SELECT
    #                      statement. Tests JOIN-form select
    #                      statements with WHERE, GROUP BY,
    #                      HAVING & ORDER BY clauses and tests
    #                      some complex queries with all together
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    #
    # obey set_env;
    # obey set_path;
    
    stmt = """select pic_9_7
from  """ + gvars.g_schema_arkcasedb + """.btsel03, """ + gvars.g_schema_arkcasedb + """.btsel04 
group by pic_9_7
having pic_9_7 < 100
order by pic_9_7;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s0')
    
    stmt = """select medium_int
from  """ + gvars.g_schema_arkcasedb + """.btsel03, """ + gvars.g_schema_arkcasedb + """.btsel04 
group by medium_int
having medium_int between 500 and 3000
order by medium_int;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s1')
    
    stmt = """select pic_9_7, """ + gvars.g_schema_arkcasedb + """.btsel03.pic_x_7
from  """ + gvars.g_schema_arkcasedb + """.btsel03, """ + gvars.g_schema_arkcasedb + """.btsel04 
group by pic_9_7, """ + gvars.g_schema_arkcasedb + """.btsel03.pic_x_7
having pic_9_7 in (50,80,100)
order by pic_9_7, """ + gvars.g_schema_arkcasedb + """.btsel03.pic_x_7;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s2')
    
    stmt = """select pic_9_7,medium_int
from  """ + gvars.g_schema_arkcasedb + """.btsel03, """ + gvars.g_schema_arkcasedb + """.btsel04 
group by pic_9_7,medium_int
having (pic_9_7 * 2) <> medium_int
order by pic_9_7,medium_int;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s3')
    
    stmt = """select pic_x_1,pic_9_7,medium_int
from  """ + gvars.g_schema_arkcasedb + """.btsel02,
 """ + gvars.g_schema_arkcasedb + """.btsel03,
 """ + gvars.g_schema_arkcasedb + """.btsel04 
group by pic_x_1,pic_9_7,medium_int
having pic_x_1 like 'Q'
order by pic_x_1,pic_9_7,medium_int;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s4')
    
    stmt = """select decimal_1,new_name_1
from  """ + gvars.g_schema_arkcasedb + """.btsel01, """ + gvars.g_schema_arkcasedb + """.pvsel03 
group by decimal_1,new_name_1
having new_name_1 in (80,100)
order by decimal_1,new_name_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s5')
    
    # test select from 0 groups
    
    stmt = """select decimal_1,new_name_1
from  """ + gvars.g_schema_arkcasedb + """.btsel01, """ + gvars.g_schema_arkcasedb + """.pvsel03 
group by decimal_1,new_name_1
having new_name_1 in (872,100)
order by decimal_1,new_name_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """select decimal_1,new_name_1
from  """ + gvars.g_schema_arkcasedb + """.btsel01, """ + gvars.g_schema_arkcasedb + """.svsel13 
group by decimal_1,new_name_1
having new_name_1 <> 80
order by decimal_1,new_name_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s6')
    
    stmt = """select  """ + gvars.g_schema_arkcasedb + """.pvsel01.medium_int, """ + gvars.g_schema_arkcasedb + """.pvsel04.medium_int
from  """ + gvars.g_schema_arkcasedb + """.pvsel01, """ + gvars.g_schema_arkcasedb + """.pvsel04 
group by  """ + gvars.g_schema_arkcasedb + """.pvsel01.medium_int, """ + gvars.g_schema_arkcasedb + """.pvsel04.medium_int
having  """ + gvars.g_schema_arkcasedb + """.pvsel01.medium_int =  """ + gvars.g_schema_arkcasedb + """.pvsel04.medium_int
order by  """ + gvars.g_schema_arkcasedb + """.pvsel01.medium_int, """ + gvars.g_schema_arkcasedb + """.pvsel04.medium_int;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s7')
    
    stmt = """select  """ + gvars.g_schema_arkcasedb + """.pvsel01.medium_int
from  """ + gvars.g_schema_arkcasedb + """.pvsel01, """ + gvars.g_schema_arkcasedb + """.svsel13 
group by  """ + gvars.g_schema_arkcasedb + """.pvsel01.medium_int
having  """ + gvars.g_schema_arkcasedb + """.pvsel01.medium_int between 2000 and 10000
order by  """ + gvars.g_schema_arkcasedb + """.pvsel01.medium_int;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s8')
    
    #   08/19/98  EL  Took out the comments for testing
    stmt = """select new_name_3,col_3
from  """ + gvars.g_schema_arkcasedb + """.svsel13, """ + gvars.g_schema_arkcasedb + """.svsel11 
group by new_name_3,col_3
having (new_name_3 like 'A      ') or
(new_name_3 like '7      ')
order by new_name_3,col_3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s9')
    
    stmt = """select secon.char_1, f.medium_int
from  """ + gvars.g_schema_arkcasedb + """.btsel01 f,  """ + gvars.g_schema_arkcasedb + """.btsel01 secon
group by secon.char_1,f.medium_int
having f.medium_int <> 5000
order by secon.char_1,f.medium_int;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s10')
    
    stmt = """select secon.medium_int
from  """ + gvars.g_schema_arkcasedb + """.pvsel01 f,  """ + gvars.g_schema_arkcasedb + """.pvsel01 secon
group by secon.medium_int
having secon.medium_int <> 5000
order by secon.medium_int;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s11')
    
    #   08/19/98  EL  Took out the comments for testing
    stmt = """select f.new_name_1,f.new_name_3
from  """ + gvars.g_schema_arkcasedb + """.svsel13 f, """ + gvars.g_schema_arkcasedb + """.svsel13 secon
group by f.new_name_1,f.new_name_3
having f.new_name_1 <> 90
order by f.new_name_1,f.new_name_3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s12')
    
    _testmgr.testcase_end(desc)

def test003(desc="""a03"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0013 : A03
    #  Description:        This test verifies the SQL SELECT
    #                      statement. Tests JOIN-form select
    #                      statements with WHERE, GROUP BY,
    #                      HAVING & ORDER BY clauses and tests
    #                      some complex queries with all together
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    #
    
    # 	*************** Test A03.1
    stmt = """select pic_9_7
from  """ + gvars.g_schema_arkcasedb + """.btsel03, """ + gvars.g_schema_arkcasedb + """.btsel04 
order by pic_9_7 ASC;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s0')
    
    stmt = """select *
from  """ + gvars.g_schema_arkcasedb + """.btsel03, """ + gvars.g_schema_arkcasedb + """.btsel04 
order by 6 DESC, """ + gvars.g_schema_arkcasedb + """.btsel03.syskey, """ + gvars.g_schema_arkcasedb + """.btsel04.syskey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s1')
    
    # 	*************** Test A03.3
    # 	Commented out because pic_9_7 is ambiguous here
    #       select pic_9_7, btsel03.pic_9_7
    #       from  btsel03, btsel04
    #       order by pic_9_7, btsel03.pic_9_7;
    
    stmt = """select *
from  """ + gvars.g_schema_arkcasedb + """.btsel03, """ + gvars.g_schema_arkcasedb + """.btsel04 
order by 4,6, """ + gvars.g_schema_arkcasedb + """.btsel03.syskey, """ + gvars.g_schema_arkcasedb + """.btsel04.syskey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s2')
    
    stmt = """select pic_x_1,pic_9_7,medium_int
from  """ + gvars.g_schema_arkcasedb + """.btsel02,
 """ + gvars.g_schema_arkcasedb + """.btsel03,
 """ + gvars.g_schema_arkcasedb + """.btsel04 
order by pic_x_1,pic_9_7,medium_int ASC;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s3')
    
    stmt = """select decimal_1,new_name_1
from  """ + gvars.g_schema_arkcasedb + """.btsel01, """ + gvars.g_schema_arkcasedb + """.pvsel03 
order by decimal_1,new_name_1 DESC;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s4')
    
    stmt = """select decimal_1,new_name_1
from  """ + gvars.g_schema_arkcasedb + """.btsel01, """ + gvars.g_schema_arkcasedb + """.svsel13 
order by decimal_1,new_name_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s5')
    
    stmt = """select """ + gvars.g_schema_arkcasedb + """.pvsel01.medium_int, """ + gvars.g_schema_arkcasedb + """.pvsel04.medium_int
from  """ + gvars.g_schema_arkcasedb + """.pvsel01, """ + gvars.g_schema_arkcasedb + """.pvsel04 
order by  """ + gvars.g_schema_arkcasedb + """.pvsel01.medium_int DESC,
 """ + gvars.g_schema_arkcasedb + """.pvsel04.medium_int DESC;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s6')
    
    stmt = """select """ + gvars.g_schema_arkcasedb + """.pvsel01.medium_int
from  """ + gvars.g_schema_arkcasedb + """.pvsel01, """ + gvars.g_schema_arkcasedb + """.svsel13 
order by  """ + gvars.g_schema_arkcasedb + """.pvsel01.medium_int;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s7')
    
    stmt = """select new_name_3, col_3
from  """ + gvars.g_schema_arkcasedb + """.svsel13, """ + gvars.g_schema_arkcasedb + """.svsel11 
order by new_name_3,col_3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s8')
    
    stmt = """select firs.medium_int, secon.char_1
from  """ + gvars.g_schema_arkcasedb + """.btsel01 firs, """ + gvars.g_schema_arkcasedb + """.btsel01 secon
order by secon.char_1 DESC, firs.medium_int ASC;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s9')
    
    stmt = """select secon.medium_int
from  """ + gvars.g_schema_arkcasedb + """.pvsel01 firs, """ + gvars.g_schema_arkcasedb + """.pvsel01 secon
order by secon.medium_int;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s10')
    
    # 	*************** Test A03.12
    stmt = """select firs.new_name_3, firs.new_name_1
from  """ + gvars.g_schema_arkcasedb + """.svsel13 firs, """ + gvars.g_schema_arkcasedb + """.svsel13 secon
order by firs.new_name_1,firs.new_name_3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s11')
    
    _testmgr.testcase_end(desc)

def test004(desc="""a04"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0013 : A04
    #  Description:        This test verifies the SQL SELECT
    #                      statement. Tests JOIN-form select
    #                      statements with WHERE, GROUP BY,
    #                      HAVING & ORDER BY clauses and tests
    #                      some complex queries with all together
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    #
    
    # obey set_env;
    # obey set_path;
    
    stmt = """select pic_9_7,medium_int
from  """ + gvars.g_schema_arkcasedb + """.btsel03, """ + gvars.g_schema_arkcasedb + """.btsel04 
where (pic_9_7 <= pic_comp_1) and
(binary_32_u between 0 and medium_int) and
(pic_comp_1 in (medium_int,binary_64_s,100,300,500))
group by pic_9_7,medium_int
having (pic_9_7 * 2) <> medium_int
order by pic_9_7,2 DESC
for read uncommitted access;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s0')
    
    stmt = """select pic_x_1,pic_9_7,medium_int
from  """ + gvars.g_schema_arkcasedb + """.btsel02,
 """ + gvars.g_schema_arkcasedb + """.btsel03,
 """ + gvars.g_schema_arkcasedb + """.btsel04 
where (pic_x_1 <>  """ + gvars.g_schema_arkcasedb + """.btsel04.pic_x_7) and
(pic_x_1 not in ( """ + gvars.g_schema_arkcasedb + """.btsel03.pic_x_7,
 """ + gvars.g_schema_arkcasedb + """.btsel04.pic_x_7)) and
(binary_32_u between 0 and medium_int)
group by pic_x_1,pic_9_7,medium_int
having pic_x_1 like 'Q'
order by pic_x_1,pic_9_7,medium_int ASC
for read committed access;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s1')
    
    stmt = """select decimal_1,new_name_1
from  """ + gvars.g_schema_arkcasedb + """.btsel01, """ + gvars.g_schema_arkcasedb + """.pvsel03 
where (var_char like '_%') and
(new_name_1 < binary_64_s)
group by decimal_1,new_name_1
having new_name_1 in (80,100)
order by decimal_1,new_name_1 DESC
for serializable access;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s2')
    
    stmt = """select decimal_1,new_name_1
from  """ + gvars.g_schema_arkcasedb + """.btsel01, """ + gvars.g_schema_arkcasedb + """.svsel13 
where (""" + gvars.g_schema_arkcasedb + """.btsel01.var_char like '_%') and
(new_name_1 < binary_64_s)
group by decimal_1,new_name_1
having new_name_1 <> 80
order by decimal_1,new_name_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s3')
    
    stmt = """select  """ + gvars.g_schema_arkcasedb + """.pvsel01.medium_int, """ + gvars.g_schema_arkcasedb + """.pvsel04.medium_int
from   """ + gvars.g_schema_arkcasedb + """.pvsel01, """ + gvars.g_schema_arkcasedb + """.pvsel04 
where  """ + gvars.g_schema_arkcasedb + """.pvsel01.medium_int >=  """ + gvars.g_schema_arkcasedb + """.pvsel04.medium_int
group by  """ + gvars.g_schema_arkcasedb + """.pvsel01.medium_int, """ + gvars.g_schema_arkcasedb + """.pvsel04.medium_int
having  """ + gvars.g_schema_arkcasedb + """.pvsel01.medium_int =  """ + gvars.g_schema_arkcasedb + """.pvsel04.medium_int
order by  """ + gvars.g_schema_arkcasedb + """.pvsel01.medium_int, """ + gvars.g_schema_arkcasedb + """.pvsel04.medium_int;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s4')
    
    stmt = """select  """ + gvars.g_schema_arkcasedb + """.pvsel01.medium_int
from  """ + gvars.g_schema_arkcasedb + """.pvsel01, """ + gvars.g_schema_arkcasedb + """.svsel13 
where small_int <> new_name_1
group by  """ + gvars.g_schema_arkcasedb + """.pvsel01.medium_int
having  """ + gvars.g_schema_arkcasedb + """.pvsel01.medium_int between 2000 and 10000
order by  """ + gvars.g_schema_arkcasedb + """.pvsel01.medium_int;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s5')
    
    #   08/19/98  EL  Took out the comments for testing
    stmt = """select new_name_3,col_3
from  """ + gvars.g_schema_arkcasedb + """.svsel13, """ + gvars.g_schema_arkcasedb + """.svsel11 
where  """ + gvars.g_schema_arkcasedb + """.svsel13.medium_int in (999,1000,2000)
group by new_name_3,col_3
having (new_name_3 like 'A      ') or (new_name_3 like '7      ')
order by new_name_3,col_3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s6')
    
    stmt = """select secon.char_1,f.medium_int
from  """ + gvars.g_schema_arkcasedb + """.btsel01 f, """ + gvars.g_schema_arkcasedb + """.btsel01 secon
where f.small_int = secon.small_int
group by secon.char_1,f.medium_int
having f.medium_int <> 5000
order by secon.char_1,f.medium_int;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s7')
    
    _testmgr.testcase_end(desc)

def test005(desc="""a05"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0013 : A05
    #  Description:        This test verifies the SQL SELECT
    #                      statement. Tests JOIN-form select
    #                      statements with WHERE, GROUP BY,
    #                      HAVING & ORDER BY clauses and tests
    #                      some complex queries with all together
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    #
    
    stmt = """select pic_9_7
from  """ + gvars.g_schema_arkcasedb + """.btsel03, """ + gvars.g_schema_arkcasedb + """.btsel04 
group by pic_9_7
for read uncommitted access
order by pic_9_7;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s0')
    
    stmt = """select decimal_1,new_name_1
from  """ + gvars.g_schema_arkcasedb + """.btsel01, """ + gvars.g_schema_arkcasedb + """.pvsel03 
group by decimal_1,new_name_1
having new_name_1 in (80,100)
for read committed access
order by decimal_1,new_name_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s1')
    
    stmt = """select *
from  """ + gvars.g_schema_arkcasedb + """.btsel01, """ + gvars.g_schema_arkcasedb + """.svsel13 
order by decimal_1,new_name_1, binary_signed, new_name_4
for serializable access;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 32)
    
    stmt = """select pic_x_1,pic_9_7,medium_int
from  """ + gvars.g_schema_arkcasedb + """.btsel02,
 """ + gvars.g_schema_arkcasedb + """.btsel03,
 """ + gvars.g_schema_arkcasedb + """.btsel04 
group by pic_x_1,pic_9_7,medium_int
for serializable access
order by pic_x_1,pic_9_7,medium_int;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s3')
    
    stmt = """select  """ + gvars.g_schema_arkcasedb + """.pvsel01.medium_int
from  """ + gvars.g_schema_arkcasedb + """.pvsel01, """ + gvars.g_schema_arkcasedb + """.svsel13 
group by  """ + gvars.g_schema_arkcasedb + """.pvsel01.medium_int
having  """ + gvars.g_schema_arkcasedb + """.pvsel01.medium_int between 2000 and 10000
for read uncommitted access
order by  """ + gvars.g_schema_arkcasedb + """.pvsel01.medium_int;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s4')
    
    stmt = """select *
from  """ + gvars.g_schema_arkcasedb + """.svsel13, """ + gvars.g_schema_arkcasedb + """.svsel11 
order by new_name_3,col_3, new_name_4, col_4, col_8
for read committed access;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 40)
    
    stmt = """select  """ + gvars.g_schema_arkcasedb + """.pvsel01.medium_int, """ + gvars.g_schema_arkcasedb + """.pvsel04.medium_int
from  """ + gvars.g_schema_arkcasedb + """.pvsel01, """ + gvars.g_schema_arkcasedb + """.pvsel04 
group by  """ + gvars.g_schema_arkcasedb + """.pvsel01.medium_int, """ + gvars.g_schema_arkcasedb + """.pvsel04.medium_int
for read committed access
order by  """ + gvars.g_schema_arkcasedb + """.pvsel01.medium_int, """ + gvars.g_schema_arkcasedb + """.pvsel04.medium_int;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s6')
    
    stmt = """select secon.medium_int
from  """ + gvars.g_schema_arkcasedb + """.pvsel01 f, """ + gvars.g_schema_arkcasedb + """.pvsel01 secon
group by secon.medium_int
having secon.medium_int <> 5000
for serializable access
order by secon.medium_int;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s7')
    
    stmt = """select *
from  """ + gvars.g_schema_arkcasedb + """.svsel13 f, """ + gvars.g_schema_arkcasedb + """.svsel13 secon
order by f.new_name_1,f.new_name_3,
f.new_name_4,secon.new_name_4
for read uncommitted access;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 16)
    
    stmt = """select secon.char_1,f.medium_int
from  """ + gvars.g_schema_arkcasedb + """.btsel01 f,  """ + gvars.g_schema_arkcasedb + """.btsel01 secon
group by secon.char_1,f.medium_int
for serializable access
order by secon.char_1,f.medium_int;"""
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
    #  Test case name:     arkt0013 : A06
    #  Description:        This test verifies the SQL SELECT
    #                      statement. Tests JOIN-form select
    #                      statements with WHERE, GROUP BY,
    #                      HAVING & ORDER BY clauses and tests
    #                      some complex queries with all together
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    #
    
    #  this query is similar to the s query in testcase A0 -
    #  only 'count(*)' is also selected to determine if the join
    #  is executing properly
    
    stmt = """select medium_int, count(*)
from  """ + gvars.g_schema_arkcasedb + """.btsel03, """ + gvars.g_schema_arkcasedb + """.btsel04 
group by medium_int
order by medium_int;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s0')
    
    #  similar to query above, without reference to btsel04 -
    #  compare value returned for count(*) here to value
    #  returned for count(*), above
    
    stmt = """select medium_int, count(*)
from  """ + gvars.g_schema_arkcasedb + """.btsel04 
group by medium_int
order by medium_int;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s1')
    
    stmt = """select f.binary_64_s, count(*)
from  """ + gvars.g_schema_arkcasedb + """.btsel01 f,  """ + gvars.g_schema_arkcasedb + """.btsel01 s
group by f.binary_64_s
order by f.binary_64_s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s2')
    
    #  02/13/98 EL
    #      select avg(f.large_int)
    #      from  pvsel01 f,  pvsel01 s
    #      group by f.medium_int
    #      order by f.medium_int;
    
    #      select avg(s.large_int)
    #      from  pvsel01 f,  pvsel01 s
    #      group by f.medium_int
    #      order by f.medium_int;
    
    stmt = """select binary_64_s, """ + gvars.g_schema_arkcasedb + """.pvsel04.pic_comp_1,min(ALL decimal_2_signed)
from  """ + gvars.g_schema_arkcasedb + """.btsel01,  """ + gvars.g_schema_arkcasedb + """.pvsel04 
group by binary_64_s,  """ + gvars.g_schema_arkcasedb + """.pvsel04.pic_comp_1
order by binary_64_s,  """ + gvars.g_schema_arkcasedb + """.pvsel04.pic_comp_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s3')
    
    stmt = """select  """ + gvars.g_schema_arkcasedb + """.pvsel03.new_name_2, sum( """ + gvars.g_schema_arkcasedb + """.pvsel03.new_name_2)
from  """ + gvars.g_schema_arkcasedb + """.pvsel03,  """ + gvars.g_schema_arkcasedb + """.svsel13 
group by  """ + gvars.g_schema_arkcasedb + """.pvsel03.new_name_2
order by  """ + gvars.g_schema_arkcasedb + """.pvsel03.new_name_2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s4')
    
    stmt = """select  """ + gvars.g_schema_arkcasedb + """.pvsel03.new_name_2, sum( """ + gvars.g_schema_arkcasedb + """.svsel13.new_name_2)
from  """ + gvars.g_schema_arkcasedb + """.pvsel03,  """ + gvars.g_schema_arkcasedb + """.svsel13 
group by  """ + gvars.g_schema_arkcasedb + """.pvsel03.new_name_2
order by  """ + gvars.g_schema_arkcasedb + """.pvsel03.new_name_2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s5')
    
    stmt = """select """ + gvars.g_schema_arkcasedb + """.svsel13.pic_comp_1, count(distinct  """ + gvars.g_schema_arkcasedb + """.svsel13.var_char)
from  """ + gvars.g_schema_arkcasedb + """.svsel13,  """ + gvars.g_schema_arkcasedb + """.btsel01 
group by  """ + gvars.g_schema_arkcasedb + """.svsel13.pic_comp_1
order by  """ + gvars.g_schema_arkcasedb + """.svsel13.pic_comp_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s6')
    
    stmt = """select """ + gvars.g_schema_arkcasedb + """.svsel13.pic_comp_1, count(distinct  """ + gvars.g_schema_arkcasedb + """.btsel01.var_char)
from  """ + gvars.g_schema_arkcasedb + """.svsel13,  """ + gvars.g_schema_arkcasedb + """.btsel01 
group by  """ + gvars.g_schema_arkcasedb + """.svsel13.pic_comp_1
order by  """ + gvars.g_schema_arkcasedb + """.svsel13.pic_comp_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s7')
    
    #  02/13/98 EL
    #       select binary_64_s, avg(ALL binary_32_u +  btsel04.pic_comp_1)
    #      from  btsel01,  btsel04
    #      group by  btsel01.binary_64_s
    #      order by  btsel01.binary_64_s;
    
    stmt = """select  """ + gvars.g_schema_arkcasedb + """.btsel01.medium_int,
min(ALL  """ + gvars.g_schema_arkcasedb + """.pvsel01.large_int *  """ + gvars.g_schema_arkcasedb + """.btsel01.medium_int)
from  """ + gvars.g_schema_arkcasedb + """.pvsel01,  """ + gvars.g_schema_arkcasedb + """.btsel01 
group by  """ + gvars.g_schema_arkcasedb + """.btsel01.medium_int
order by  """ + gvars.g_schema_arkcasedb + """.btsel01.medium_int;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s8')
    
    stmt = """select f.pic_comp_1, avg(f.pic_comp_1) + sum(s.pic_comp_1)
from  """ + gvars.g_schema_arkcasedb + """.svsel13 f,  """ + gvars.g_schema_arkcasedb + """.svsel13 s
group by f.pic_comp_1
order by f.pic_comp_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s9')
    
    #  queries with predicates
    
    stmt = """select f.binary_64_s, count(*)
from  """ + gvars.g_schema_arkcasedb + """.btsel01 f,  """ + gvars.g_schema_arkcasedb + """.btsel01 s
where f.var_char = 'thomas'
group by f.binary_64_s
order by f.binary_64_s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s10')
    
    stmt = """select large_int, count(*)
from  """ + gvars.g_schema_arkcasedb + """.btsel01,  """ + gvars.g_schema_arkcasedb + """.pvsel04 
where  """ + gvars.g_schema_arkcasedb + """.btsel01.large_int =  """ + gvars.g_schema_arkcasedb + """.pvsel04.medium_int
group by large_int
order by large_int;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s11')
    
    stmt = """select  """ + gvars.g_schema_arkcasedb + """.svsel13.pic_comp_1, avg(decimal_1)
from  """ + gvars.g_schema_arkcasedb + """.svsel13,  """ + gvars.g_schema_arkcasedb + """.btsel01 
where decimal_3_unsigned = new_name_1
group by  """ + gvars.g_schema_arkcasedb + """.svsel13.pic_comp_1
order by  """ + gvars.g_schema_arkcasedb + """.svsel13.pic_comp_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s12')
    
    stmt = """select  """ + gvars.g_schema_arkcasedb + """.pvsel01.medium_int,
avg(distinct  """ + gvars.g_schema_arkcasedb + """.pvsel04.medium_int)
from  """ + gvars.g_schema_arkcasedb + """.pvsel01,  """ + gvars.g_schema_arkcasedb + """.pvsel04 
where  """ + gvars.g_schema_arkcasedb + """.pvsel01.medium_int >  """ + gvars.g_schema_arkcasedb + """.pvsel04.medium_int
group by  """ + gvars.g_schema_arkcasedb + """.pvsel01.medium_int
order by  """ + gvars.g_schema_arkcasedb + """.pvsel01.medium_int;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s13')
    
    stmt = """select pic_9_7, sum(binary_32_u + pic_comp_1)
from  """ + gvars.g_schema_arkcasedb + """.btsel03,  """ + gvars.g_schema_arkcasedb + """.btsel04 
where pic_comp_1 in (medium_int, binary_64_s)
group by pic_9_7
order by pic_9_7;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s14')
    
    stmt = """select pic_comp_1, avg(col_7) * sum(pic_comp_1)
from  """ + gvars.g_schema_arkcasedb + """.svsel13,  """ + gvars.g_schema_arkcasedb + """.svsel11 
where new_name_3 = col_8
group by pic_comp_1
order by pic_comp_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s15')
    
    _testmgr.testcase_end(desc)

def test007(desc="""a07"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0013 : A07
    #  Description:        This test verifies the SQL SELECT
    #                      statement. Tests JOIN-form select
    #                      statements with WHERE, GROUP BY,
    #                      HAVING & ORDER BY clauses and tests
    #                      some complex queries with all together
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    #
    
    #  test use of HAVING clause with no GROUP BY clause
    
    stmt = """select sum(pic_decimal_2), max( """ + gvars.g_schema_arkcasedb + """.pvsel04.var_char)
from  """ + gvars.g_schema_arkcasedb + """.btsel01, """ + gvars.g_schema_arkcasedb + """.pvsel04 
having avg( """ + gvars.g_schema_arkcasedb + """.btsel01.pic_comp_1) > 500 and
avg( """ + gvars.g_schema_arkcasedb + """.pvsel04.pic_comp_1) > 1000;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s0')
    
    stmt = """select f.binary_64_s, count(*)
from  """ + gvars.g_schema_arkcasedb + """.btsel01 f,  """ + gvars.g_schema_arkcasedb + """.btsel01 s
group by f.binary_64_s
having sum(distinct f.pic_comp_1) < 1000
order by f.binary_64_s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s1')
    
    stmt = """select avg(f.large_int)
from  """ + gvars.g_schema_arkcasedb + """.pvsel01 f,  """ + gvars.g_schema_arkcasedb + """.pvsel01 s
group by f.medium_int
having sum(f.large_int) > 0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s2')
    #       order by f.medium_int;
    
    stmt = """select avg(s.large_int)
from  """ + gvars.g_schema_arkcasedb + """.pvsel01 f,  """ + gvars.g_schema_arkcasedb + """.pvsel01 s
group by f.medium_int
having sum(ALL f.large_int) > 0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s3')
    #       order by f.medium_int;
    
    stmt = """select binary_64_s, """ + gvars.g_schema_arkcasedb + """.pvsel04.pic_comp_1,min(ALL decimal_2_signed)
from  """ + gvars.g_schema_arkcasedb + """.btsel01,  """ + gvars.g_schema_arkcasedb + """.pvsel04 
group by binary_64_s,  """ + gvars.g_schema_arkcasedb + """.pvsel04.pic_comp_1
having max(binary_32_u) >= 50
order by binary_64_s,  """ + gvars.g_schema_arkcasedb + """.pvsel04.pic_comp_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s4')
    
    stmt = """select  """ + gvars.g_schema_arkcasedb + """.pvsel03.new_name_2, sum( """ + gvars.g_schema_arkcasedb + """.pvsel03.new_name_2)
from  """ + gvars.g_schema_arkcasedb + """.pvsel03,  """ + gvars.g_schema_arkcasedb + """.svsel13 
group by  """ + gvars.g_schema_arkcasedb + """.pvsel03.new_name_2
having sum( """ + gvars.g_schema_arkcasedb + """.svsel13.new_name_1) > 500
order by  """ + gvars.g_schema_arkcasedb + """.pvsel03.new_name_2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s5')
    
    stmt = """select  """ + gvars.g_schema_arkcasedb + """.pvsel03.new_name_2, sum( """ + gvars.g_schema_arkcasedb + """.svsel13.new_name_2)
from  """ + gvars.g_schema_arkcasedb + """.pvsel03,  """ + gvars.g_schema_arkcasedb + """.svsel13 
group by  """ + gvars.g_schema_arkcasedb + """.pvsel03.new_name_2
having sum(distinct  """ + gvars.g_schema_arkcasedb + """.svsel13.new_name_1) > 100
order by  """ + gvars.g_schema_arkcasedb + """.pvsel03.new_name_2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s6')
    
    stmt = """select """ + gvars.g_schema_arkcasedb + """.svsel13.pic_comp_1, count(distinct  """ + gvars.g_schema_arkcasedb + """.svsel13.var_char)
from  """ + gvars.g_schema_arkcasedb + """.svsel13,  """ + gvars.g_schema_arkcasedb + """.btsel01 
group by  """ + gvars.g_schema_arkcasedb + """.svsel13.pic_comp_1
having avg((new_name_1 * new_name_2) / 2) <> 240
order by  """ + gvars.g_schema_arkcasedb + """.svsel13.pic_comp_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s7')
    
    stmt = """select """ + gvars.g_schema_arkcasedb + """.svsel13.pic_comp_1, count(distinct """ + gvars.g_schema_arkcasedb + """.btsel01.var_char)
from  """ + gvars.g_schema_arkcasedb + """.svsel13,  """ + gvars.g_schema_arkcasedb + """.btsel01 
group by """ + gvars.g_schema_arkcasedb + """.svsel13.pic_comp_1
having min( """ + gvars.g_schema_arkcasedb + """.svsel13.medium_int +  """ + gvars.g_schema_arkcasedb + """.btsel01.medium_int)
< 2000
order by """ + gvars.g_schema_arkcasedb + """.svsel13.pic_comp_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s8')
    
    stmt = """select """ + gvars.g_schema_arkcasedb + """.btsel01.binary_64_s, avg(ALL binary_32_u +  """ + gvars.g_schema_arkcasedb + """.btsel04.pic_comp_1)
from  """ + gvars.g_schema_arkcasedb + """.btsel01,  """ + gvars.g_schema_arkcasedb + """.btsel04 
group by  """ + gvars.g_schema_arkcasedb + """.btsel01.binary_64_s
having sum( """ + gvars.g_schema_arkcasedb + """.btsel04.medium_int) +
sum( """ + gvars.g_schema_arkcasedb + """.btsel04.pic_comp_1) > 20000
order by  """ + gvars.g_schema_arkcasedb + """.btsel01.binary_64_s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s9')
    
    stmt = """select  """ + gvars.g_schema_arkcasedb + """.btsel01.medium_int,
min(ALL  """ + gvars.g_schema_arkcasedb + """.pvsel01.large_int *  """ + gvars.g_schema_arkcasedb + """.btsel01.medium_int)
from  """ + gvars.g_schema_arkcasedb + """.pvsel01,  """ + gvars.g_schema_arkcasedb + """.btsel01 
group by  """ + gvars.g_schema_arkcasedb + """.btsel01.medium_int
having avg( """ + gvars.g_schema_arkcasedb + """.btsel01.medium_int) >
avg( """ + gvars.g_schema_arkcasedb + """.pvsel01.medium_int)
order by  """ + gvars.g_schema_arkcasedb + """.btsel01.medium_int;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s10')
    
    stmt = """select  """ + gvars.g_schema_arkcasedb + """.btsel01.medium_int,
min(ALL  """ + gvars.g_schema_arkcasedb + """.pvsel01.large_int *  """ + gvars.g_schema_arkcasedb + """.btsel01.medium_int)
from  """ + gvars.g_schema_arkcasedb + """.pvsel01,  """ + gvars.g_schema_arkcasedb + """.btsel01 
group by  """ + gvars.g_schema_arkcasedb + """.btsel01.medium_int
having count(*) <> 16
order by  """ + gvars.g_schema_arkcasedb + """.btsel01.medium_int;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s11')
    
    #  queries with predicates
    
    stmt = """select large_int, count(*)
from  """ + gvars.g_schema_arkcasedb + """.btsel01,  """ + gvars.g_schema_arkcasedb + """.pvsel04 
where  """ + gvars.g_schema_arkcasedb + """.btsel01.large_int =  """ + gvars.g_schema_arkcasedb + """.pvsel04.medium_int
group by large_int
having sum( """ + gvars.g_schema_arkcasedb + """.btsel01.small_int) >
sum(decimal_2_signed * 100)
order by large_int;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s12')
    
    stmt = """select  """ + gvars.g_schema_arkcasedb + """.svsel13.pic_comp_1, avg(decimal_1)
from  """ + gvars.g_schema_arkcasedb + """.svsel13,  """ + gvars.g_schema_arkcasedb + """.btsel01 
where decimal_3_unsigned = new_name_1
group by  """ + gvars.g_schema_arkcasedb + """.svsel13.pic_comp_1
having min(ALL pic_decimal_3) < 5
order by  """ + gvars.g_schema_arkcasedb + """.svsel13.pic_comp_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s13')
    
    stmt = """select  """ + gvars.g_schema_arkcasedb + """.pvsel01.medium_int,
avg(distinct  """ + gvars.g_schema_arkcasedb + """.pvsel04.medium_int)
from  """ + gvars.g_schema_arkcasedb + """.pvsel01,  """ + gvars.g_schema_arkcasedb + """.pvsel04 
where  """ + gvars.g_schema_arkcasedb + """.pvsel01.medium_int >  """ + gvars.g_schema_arkcasedb + """.pvsel04.medium_int
group by  """ + gvars.g_schema_arkcasedb + """.pvsel01.medium_int
having avg(pic_decimal_3 *  """ + gvars.g_schema_arkcasedb + """.pvsel04.medium_int) < 7500
order by  """ + gvars.g_schema_arkcasedb + """.pvsel01.medium_int;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s14')
    
    stmt = """select pic_9_7, sum(binary_32_u + pic_comp_1)
from  """ + gvars.g_schema_arkcasedb + """.btsel03,  """ + gvars.g_schema_arkcasedb + """.btsel04 
where pic_comp_1 in (medium_int, binary_64_s)
group by pic_9_7
having sum(distinct binary_32_u) <> 5
order by pic_9_7;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s15')
    
    stmt = """select pic_comp_1, avg(col_7) * sum(pic_comp_1)
from  """ + gvars.g_schema_arkcasedb + """.svsel13,  """ + gvars.g_schema_arkcasedb + """.svsel11 
where new_name_3 = col_8
group by pic_comp_1
having sum(col_4 * col_7) < 5000
order by pic_comp_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s16')
    
    #  complex queries
    
    stmt = """select large_int, count(*)
from  """ + gvars.g_schema_arkcasedb + """.btsel01,  """ + gvars.g_schema_arkcasedb + """.pvsel04 
where  """ + gvars.g_schema_arkcasedb + """.btsel01.large_int =  """ + gvars.g_schema_arkcasedb + """.pvsel04.medium_int
group by large_int
having sum( """ + gvars.g_schema_arkcasedb + """.btsel01.small_int) >
sum(decimal_2_signed * 100)
order by large_int
for serializable access;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s17')
    
    stmt = """select  """ + gvars.g_schema_arkcasedb + """.svsel13.pic_comp_1, avg(decimal_1)
from   """ + gvars.g_schema_arkcasedb + """.svsel13,  """ + gvars.g_schema_arkcasedb + """.btsel01 
where decimal_3_unsigned = new_name_1
group by  """ + gvars.g_schema_arkcasedb + """.svsel13.pic_comp_1
having min(ALL pic_decimal_3) < 5
order by 1 DESC  ,2 DESC
for read committed access;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s18')
    
    stmt = """select  """ + gvars.g_schema_arkcasedb + """.pvsel01.medium_int,
avg(distinct  """ + gvars.g_schema_arkcasedb + """.pvsel04.medium_int)
from   """ + gvars.g_schema_arkcasedb + """.pvsel01,  """ + gvars.g_schema_arkcasedb + """.pvsel04 
where  """ + gvars.g_schema_arkcasedb + """.pvsel01.medium_int >  """ + gvars.g_schema_arkcasedb + """.pvsel04.medium_int
group by  """ + gvars.g_schema_arkcasedb + """.pvsel01.medium_int
having avg(pic_decimal_3 *  """ + gvars.g_schema_arkcasedb + """.pvsel04.medium_int) < 7500
order by 2, """ + gvars.g_schema_arkcasedb + """.pvsel01.medium_int
for read uncommitted access;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s19')
    
    stmt = """select pic_9_7, sum(binary_32_u + pic_comp_1)
from  """ + gvars.g_schema_arkcasedb + """.btsel03,  """ + gvars.g_schema_arkcasedb + """.btsel04 
where pic_comp_1 in (medium_int, binary_64_s)
group by pic_9_7
having sum(distinct binary_32_u) <> 5
order by pic_9_7 ASC
for serializable access;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s20')
    
    stmt = """select pic_comp_1, avg(col_7) * sum(pic_comp_1)
from  """ + gvars.g_schema_arkcasedb + """.svsel13,  """ + gvars.g_schema_arkcasedb + """.svsel11 
where new_name_3 = col_8
group by pic_comp_1
having sum(col_4 * col_7) < 5000
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s21')
    
    _testmgr.testcase_end(desc)

