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
    #  Test case name:     arkt1376 : A01
    #  Original Test case: arkt0013 : A01
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
    
    # Query 1
    stmt = """select [any 2] pic_9_7
from  """ + gvars.g_schema_arkcasedb + """.btsel03, """ + gvars.g_schema_arkcasedb + """.btsel04 
group by pic_9_7
order by pic_9_7;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    _dci.expect_selected_msg(output, 2)
    
    # Query 2
    stmt = """select [any 2] medium_int
from  """ + gvars.g_schema_arkcasedb + """.btsel03, """ + gvars.g_schema_arkcasedb + """.btsel04 
group by medium_int
order by medium_int;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 2)
    
    #  similar to above, without reference to btsel03
    #  (compare output - should be the same)
    
    # Query 3
    stmt = """select [any 2] medium_int
from  """ + gvars.g_schema_arkcasedb + """.btsel04 
group by medium_int
order by medium_int;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 2)
    
    # Query 4
    stmt = """select [any 2] pic_9_7, """ + gvars.g_schema_arkcasedb + """.btsel03.pic_x_7
from  """ + gvars.g_schema_arkcasedb + """.btsel03, """ + gvars.g_schema_arkcasedb + """.btsel04 
group by pic_9_7, """ + gvars.g_schema_arkcasedb + """.btsel03.pic_x_7
order by pic_9_7, """ + gvars.g_schema_arkcasedb + """.btsel03.pic_x_7;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 2)
    
    # Query 5
    stmt = """select [any 2] pic_9_7,medium_int
from  """ + gvars.g_schema_arkcasedb + """.btsel03, """ + gvars.g_schema_arkcasedb + """.btsel04 
group by pic_9_7,medium_int
order by pic_9_7,medium_int;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 2)
    
    # Query 6
    stmt = """select [any 2] pic_x_1,pic_9_7,medium_int
from  """ + gvars.g_schema_arkcasedb + """.btsel02,
 """ + gvars.g_schema_arkcasedb + """.btsel03,
 """ + gvars.g_schema_arkcasedb + """.btsel04 
group by pic_x_1,pic_9_7,medium_int
order by pic_x_1,pic_9_7,medium_int;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 2)
    
    # Query 7
    stmt = """select [any 2] decimal_1,new_name_1
from  """ + gvars.g_schema_arkcasedb + """.btsel01, """ + gvars.g_schema_arkcasedb + """.pvsel03 
group by decimal_1,new_name_1
order by decimal_1,new_name_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 2)
    
    # Query 8
    stmt = """select [any 2] decimal_1,new_name_1
from  """ + gvars.g_schema_arkcasedb + """.btsel01, """ + gvars.g_schema_arkcasedb + """.svsel13 
group by decimal_1,new_name_1
order by decimal_1,new_name_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 2)
    
    # Query 9
    stmt = """select [any 2]  """ + gvars.g_schema_arkcasedb + """.pvsel01.medium_int, """ + gvars.g_schema_arkcasedb + """.pvsel04.medium_int
from  """ + gvars.g_schema_arkcasedb + """.pvsel01, """ + gvars.g_schema_arkcasedb + """.pvsel04 
group by  """ + gvars.g_schema_arkcasedb + """.pvsel01.medium_int, """ + gvars.g_schema_arkcasedb + """.pvsel04.medium_int
order by  """ + gvars.g_schema_arkcasedb + """.pvsel01.medium_int, """ + gvars.g_schema_arkcasedb + """.pvsel04.medium_int;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 2)
    
    # Query 10
    stmt = """select [any 2]  """ + gvars.g_schema_arkcasedb + """.pvsel01.medium_int
from  """ + gvars.g_schema_arkcasedb + """.pvsel01, """ + gvars.g_schema_arkcasedb + """.svsel13 
group by  """ + gvars.g_schema_arkcasedb + """.pvsel01.medium_int
order by  """ + gvars.g_schema_arkcasedb + """.pvsel01.medium_int;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 2)
    
    # Query 11
    stmt = """select [any 2] new_name_3,col_3
from  """ + gvars.g_schema_arkcasedb + """.svsel13, """ + gvars.g_schema_arkcasedb + """.svsel11 
group by new_name_3,col_3
order by new_name_3,col_3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 2)
    
    # Query 12
    stmt = """select [any 2] secon.char_1, f.medium_int
from   """ + gvars.g_schema_arkcasedb + """.btsel01 f,   """ + gvars.g_schema_arkcasedb + """.btsel01 secon
group by secon.char_1,f.medium_int
order by secon.char_1,f.medium_int;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 2)
    
    # Query 13
    stmt = """select [any 2] secon.medium_int
from  """ + gvars.g_schema_arkcasedb + """.pvsel01 f,  """ + gvars.g_schema_arkcasedb + """.pvsel01 secon
group by secon.medium_int
order by secon.medium_int;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 2)
    
    # Query 14
    stmt = """select [any 2] f.new_name_1,f.new_name_3
from  """ + gvars.g_schema_arkcasedb + """.svsel13 f, """ + gvars.g_schema_arkcasedb + """.svsel13 secon
group by f.new_name_1,f.new_name_3
order by f.new_name_1,f.new_name_3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 2)
    
    _testmgr.testcase_end(desc)

def test002(desc="""a02"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt1376 : A02
    #  Original Test case: arkt0013 : A02
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
    
    stmt = """select [any 3] pic_9_7
from  """ + gvars.g_schema_arkcasedb + """.btsel03, """ + gvars.g_schema_arkcasedb + """.btsel04 
group by pic_9_7
having pic_9_7 < 100
order by pic_9_7;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    _dci.expect_selected_msg(output, 3)
    
    stmt = """select [any 3] medium_int
from  """ + gvars.g_schema_arkcasedb + """.btsel03, """ + gvars.g_schema_arkcasedb + """.btsel04 
group by medium_int
having medium_int between 500 and 3000
order by medium_int;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 3)
    
    stmt = """select [any 3] pic_9_7, """ + gvars.g_schema_arkcasedb + """.btsel03.pic_x_7
from  """ + gvars.g_schema_arkcasedb + """.btsel03, """ + gvars.g_schema_arkcasedb + """.btsel04 
group by pic_9_7, """ + gvars.g_schema_arkcasedb + """.btsel03.pic_x_7
having pic_9_7 in (50,80,100)
order by pic_9_7, """ + gvars.g_schema_arkcasedb + """.btsel03.pic_x_7;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 3)
    
    stmt = """select [any 3] pic_9_7,medium_int
from  """ + gvars.g_schema_arkcasedb + """.btsel03, """ + gvars.g_schema_arkcasedb + """.btsel04 
group by pic_9_7,medium_int
having (pic_9_7 * 2) <> medium_int
order by pic_9_7,medium_int;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 3)
    
    stmt = """select [any 3] pic_x_1,pic_9_7,medium_int
from  """ + gvars.g_schema_arkcasedb + """.btsel02,
 """ + gvars.g_schema_arkcasedb + """.btsel03,
 """ + gvars.g_schema_arkcasedb + """.btsel04 
group by pic_x_1,pic_9_7,medium_int
having pic_x_1 like 'Q'
order by pic_x_1,pic_9_7,medium_int;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 3)
    
    stmt = """select [any 3] decimal_1,new_name_1
from  """ + gvars.g_schema_arkcasedb + """.btsel01, """ + gvars.g_schema_arkcasedb + """.pvsel03 
group by decimal_1,new_name_1
having new_name_1 in (80,100)
order by decimal_1,new_name_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 3)
    
    # test select [any 3] from 0 groups
    
    stmt = """select [any 3] decimal_1,new_name_1
from  """ + gvars.g_schema_arkcasedb + """.btsel01, """ + gvars.g_schema_arkcasedb + """.pvsel03 
group by decimal_1,new_name_1
having new_name_1 in (872,100)
order by decimal_1,new_name_1;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """select [any 3] decimal_1,new_name_1
from  """ + gvars.g_schema_arkcasedb + """.btsel01, """ + gvars.g_schema_arkcasedb + """.svsel13 
group by decimal_1,new_name_1
having new_name_1 <> 80
order by decimal_1,new_name_1;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    _dci.expect_selected_msg(output, 3)
    
    stmt = """select [any 3]  """ + gvars.g_schema_arkcasedb + """.pvsel01.medium_int, """ + gvars.g_schema_arkcasedb + """.pvsel04.medium_int
from  """ + gvars.g_schema_arkcasedb + """.pvsel01, """ + gvars.g_schema_arkcasedb + """.pvsel04 
group by  """ + gvars.g_schema_arkcasedb + """.pvsel01.medium_int, """ + gvars.g_schema_arkcasedb + """.pvsel04.medium_int
having  """ + gvars.g_schema_arkcasedb + """.pvsel01.medium_int =  """ + gvars.g_schema_arkcasedb + """.pvsel04.medium_int
order by  """ + gvars.g_schema_arkcasedb + """.pvsel01.medium_int, """ + gvars.g_schema_arkcasedb + """.pvsel04.medium_int;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    _dci.expect_selected_msg(output, 1)
    
    stmt = """select [any 3]  """ + gvars.g_schema_arkcasedb + """.pvsel01.medium_int
from  """ + gvars.g_schema_arkcasedb + """.pvsel01, """ + gvars.g_schema_arkcasedb + """.svsel13 
group by  """ + gvars.g_schema_arkcasedb + """.pvsel01.medium_int
having  """ + gvars.g_schema_arkcasedb + """.pvsel01.medium_int between 2000 and 10000
order by  """ + gvars.g_schema_arkcasedb + """.pvsel01.medium_int;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    _dci.expect_selected_msg(output, 3)
    
    stmt = """select [any 3] new_name_3,col_3
from  """ + gvars.g_schema_arkcasedb + """.svsel13, """ + gvars.g_schema_arkcasedb + """.svsel11 
group by new_name_3,col_3
having (new_name_3 like 'A      ') or
(new_name_3 like '7      ')
order by new_name_3,col_3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 3)
    
    stmt = """select [any 3] secon.char_1, f.medium_int
from  """ + gvars.g_schema_arkcasedb + """.btsel01 f,  """ + gvars.g_schema_arkcasedb + """.btsel01 secon
group by secon.char_1,f.medium_int
having f.medium_int <> 5000
order by secon.char_1,f.medium_int;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 3)
    
    stmt = """select [any 3] secon.medium_int
from  """ + gvars.g_schema_arkcasedb + """.pvsel01 f,  """ + gvars.g_schema_arkcasedb + """.pvsel01 secon
group by secon.medium_int
having secon.medium_int <> 5000
order by secon.medium_int;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 3)
    
    stmt = """select [any 3] f.new_name_1,f.new_name_3
from  """ + gvars.g_schema_arkcasedb + """.svsel13 f, """ + gvars.g_schema_arkcasedb + """.svsel13 secon
group by f.new_name_1,f.new_name_3
having f.new_name_1 <> 90
order by f.new_name_1,f.new_name_3;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    _dci.expect_selected_msg(output, 2)
    
    _testmgr.testcase_end(desc)

def test003(desc="""a03"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt1376 : A03
    #  Original Test case: arkt0013 : A03
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
    
    # 	*************** Test A03.1
    
    stmt = """select [any 16] pic_9_7
from  """ + gvars.g_schema_arkcasedb + """.btsel03, """ + gvars.g_schema_arkcasedb + """.btsel04 
order by pic_9_7 ASC;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    _dci.expect_selected_msg(output, 16)
    
    stmt = """select [any 16] *
from  """ + gvars.g_schema_arkcasedb + """.btsel03, """ + gvars.g_schema_arkcasedb + """.btsel04 
order by 6 DESC, """ + gvars.g_schema_arkcasedb + """.btsel03.syskey, """ + gvars.g_schema_arkcasedb + """.btsel04.syskey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 16)
    
    stmt = """select [any 16] *
from  """ + gvars.g_schema_arkcasedb + """.btsel03, """ + gvars.g_schema_arkcasedb + """.btsel04 
order by 4,6, """ + gvars.g_schema_arkcasedb + """.btsel03.syskey, """ + gvars.g_schema_arkcasedb + """.btsel04.syskey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 16)
    
    stmt = """select [any 16] pic_x_1,pic_9_7,medium_int
from  """ + gvars.g_schema_arkcasedb + """.btsel02,
 """ + gvars.g_schema_arkcasedb + """.btsel03,
 """ + gvars.g_schema_arkcasedb + """.btsel04 
order by pic_x_1,pic_9_7,medium_int ASC;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 16)
    
    stmt = """select [any 16] decimal_1,new_name_1
from  """ + gvars.g_schema_arkcasedb + """.btsel01, """ + gvars.g_schema_arkcasedb + """.pvsel03 
order by decimal_1,new_name_1 DESC;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 16)
    
    stmt = """select [any 16] decimal_1,new_name_1
from  """ + gvars.g_schema_arkcasedb + """.btsel01, """ + gvars.g_schema_arkcasedb + """.svsel13 
order by decimal_1,new_name_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 16)
    
    stmt = """select [any 16] """ + gvars.g_schema_arkcasedb + """.pvsel01.medium_int, """ + gvars.g_schema_arkcasedb + """.pvsel04.medium_int
from  """ + gvars.g_schema_arkcasedb + """.pvsel01, """ + gvars.g_schema_arkcasedb + """.pvsel04 
order by  """ + gvars.g_schema_arkcasedb + """.pvsel01.medium_int DESC,
 """ + gvars.g_schema_arkcasedb + """.pvsel04.medium_int DESC;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 16)
    
    stmt = """select [any 16] """ + gvars.g_schema_arkcasedb + """.pvsel01.medium_int
from  """ + gvars.g_schema_arkcasedb + """.pvsel01, """ + gvars.g_schema_arkcasedb + """.svsel13 
order by  """ + gvars.g_schema_arkcasedb + """.pvsel01.medium_int;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 16)
    
    stmt = """select [any 16] new_name_3, col_3
from  """ + gvars.g_schema_arkcasedb + """.svsel13, """ + gvars.g_schema_arkcasedb + """.svsel11 
order by new_name_3,col_3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 16)
    
    stmt = """select [any 16] firs.medium_int, secon.char_1
from  """ + gvars.g_schema_arkcasedb + """.btsel01 firs, """ + gvars.g_schema_arkcasedb + """.btsel01 secon
order by secon.char_1 DESC, firs.medium_int ASC;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 16)
    
    stmt = """select [any 16] secon.medium_int
from  """ + gvars.g_schema_arkcasedb + """.pvsel01 firs, """ + gvars.g_schema_arkcasedb + """.pvsel01 secon
order by secon.medium_int;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 16)
    
    # 	*************** Test A03.12
    stmt = """select [any 16] firs.new_name_3, firs.new_name_1
from  """ + gvars.g_schema_arkcasedb + """.svsel13 firs, """ + gvars.g_schema_arkcasedb + """.svsel13 secon
order by firs.new_name_1,firs.new_name_3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 16)
    
    _testmgr.testcase_end(desc)

def test004(desc="""a04"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt1376 : A04
    #  Original Test case: arkt0013 : A04
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
    
    stmt = """select [any 4] pic_9_7,medium_int
from  """ + gvars.g_schema_arkcasedb + """.btsel03, """ + gvars.g_schema_arkcasedb + """.btsel04 
where (pic_9_7 <= pic_comp_1) and
(binary_32_u between 0 and medium_int) and
(pic_comp_1 in (medium_int,binary_64_s,100,300,500))
group by pic_9_7,medium_int
having (pic_9_7 * 2) <> medium_int
order by pic_9_7,2 DESC
for read uncommitted access;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    _dci.expect_selected_msg(output, 4)
    
    stmt = """select [any 4] pic_x_1,pic_9_7,medium_int
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
    _dci.expect_selected_msg(output, 4)
    
    stmt = """select [any 4] decimal_1,new_name_1
from  """ + gvars.g_schema_arkcasedb + """.btsel01, """ + gvars.g_schema_arkcasedb + """.pvsel03 
where (var_char like '_%') and
(new_name_1 < binary_64_s)
group by decimal_1,new_name_1
having new_name_1 in (80,100)
order by decimal_1,new_name_1 DESC
for serializable access;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 4)
    
    stmt = """select [any 4] decimal_1,new_name_1
from  """ + gvars.g_schema_arkcasedb + """.btsel01, """ + gvars.g_schema_arkcasedb + """.svsel13 
where (""" + gvars.g_schema_arkcasedb + """.btsel01.var_char like '_%') and
(new_name_1 < binary_64_s)
group by decimal_1,new_name_1
having new_name_1 <> 80
order by decimal_1,new_name_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 4)
    
    stmt = """select [any 4]  """ + gvars.g_schema_arkcasedb + """.pvsel01.medium_int, """ + gvars.g_schema_arkcasedb + """.pvsel04.medium_int
from   """ + gvars.g_schema_arkcasedb + """.pvsel01, """ + gvars.g_schema_arkcasedb + """.pvsel04 
where  """ + gvars.g_schema_arkcasedb + """.pvsel01.medium_int >=  """ + gvars.g_schema_arkcasedb + """.pvsel04.medium_int
group by  """ + gvars.g_schema_arkcasedb + """.pvsel01.medium_int, """ + gvars.g_schema_arkcasedb + """.pvsel04.medium_int
having  """ + gvars.g_schema_arkcasedb + """.pvsel01.medium_int =  """ + gvars.g_schema_arkcasedb + """.pvsel04.medium_int
order by  """ + gvars.g_schema_arkcasedb + """.pvsel01.medium_int, """ + gvars.g_schema_arkcasedb + """.pvsel04.medium_int;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    _dci.expect_selected_msg(output, 1)
    
    stmt = """select [any 4]  """ + gvars.g_schema_arkcasedb + """.pvsel01.medium_int
from  """ + gvars.g_schema_arkcasedb + """.pvsel01, """ + gvars.g_schema_arkcasedb + """.svsel13 
where small_int <> new_name_1
group by  """ + gvars.g_schema_arkcasedb + """.pvsel01.medium_int
having  """ + gvars.g_schema_arkcasedb + """.pvsel01.medium_int between 2000 and 10000
order by  """ + gvars.g_schema_arkcasedb + """.pvsel01.medium_int;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select [any 4] new_name_3,col_3
from  """ + gvars.g_schema_arkcasedb + """.svsel13, """ + gvars.g_schema_arkcasedb + """.svsel11 
where  """ + gvars.g_schema_arkcasedb + """.svsel13.medium_int in (999,1000,2000)
group by new_name_3,col_3
having (new_name_3 like 'A      ') or (new_name_3 like '7      ')
order by new_name_3,col_3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 4)
    
    stmt = """select [any 4] secon.char_1,f.medium_int
from  """ + gvars.g_schema_arkcasedb + """.btsel01 f, """ + gvars.g_schema_arkcasedb + """.btsel01 secon
where f.small_int = secon.small_int
group by secon.char_1,f.medium_int
having f.medium_int <> 5000
order by secon.char_1,f.medium_int;"""
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
    #  Test case name:     arkt1376 : A05
    #  Original Test case: arkt0013 : A05
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
    
    stmt = """select [any 16] pic_9_7
from  """ + gvars.g_schema_arkcasedb + """.btsel03, """ + gvars.g_schema_arkcasedb + """.btsel04 
group by pic_9_7
for read uncommitted access
order by pic_9_7;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    _dci.expect_selected_msg(output, 4)
    
    stmt = """select [any 16] decimal_1,new_name_1
from  """ + gvars.g_schema_arkcasedb + """.btsel01, """ + gvars.g_schema_arkcasedb + """.pvsel03 
group by decimal_1,new_name_1
having new_name_1 in (80,100)
for read committed access
order by decimal_1,new_name_1;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    _dci.expect_selected_msg(output, 6)
    
    stmt = """select [any 16] *
from  """ + gvars.g_schema_arkcasedb + """.btsel01, """ + gvars.g_schema_arkcasedb + """.svsel13 
order by decimal_1,new_name_1, binary_signed, new_name_4
for serializable access;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    _dci.expect_selected_msg(output, 16)
    
    stmt = """select [any 16] pic_x_1,pic_9_7,medium_int
from  """ + gvars.g_schema_arkcasedb + """.btsel02,
 """ + gvars.g_schema_arkcasedb + """.btsel03,
 """ + gvars.g_schema_arkcasedb + """.btsel04 
group by pic_x_1,pic_9_7,medium_int
for serializable access
order by pic_x_1,pic_9_7,medium_int;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 16)
    
    stmt = """select [any 16]  """ + gvars.g_schema_arkcasedb + """.pvsel01.medium_int
from  """ + gvars.g_schema_arkcasedb + """.pvsel01, """ + gvars.g_schema_arkcasedb + """.svsel13 
group by  """ + gvars.g_schema_arkcasedb + """.pvsel01.medium_int
having  """ + gvars.g_schema_arkcasedb + """.pvsel01.medium_int between 2000 and 10000
for read uncommitted access
order by  """ + gvars.g_schema_arkcasedb + """.pvsel01.medium_int;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    _dci.expect_selected_msg(output, 4)
    
    stmt = """select [any 16] *
from  """ + gvars.g_schema_arkcasedb + """.svsel13, """ + gvars.g_schema_arkcasedb + """.svsel11 
order by new_name_3,col_3, new_name_4, col_4, col_8
for read committed access;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    _dci.expect_selected_msg(output, 16)
    
    stmt = """select [any 16]  """ + gvars.g_schema_arkcasedb + """.pvsel01.medium_int, """ + gvars.g_schema_arkcasedb + """.pvsel04.medium_int
from  """ + gvars.g_schema_arkcasedb + """.pvsel01, """ + gvars.g_schema_arkcasedb + """.pvsel04 
group by  """ + gvars.g_schema_arkcasedb + """.pvsel01.medium_int, """ + gvars.g_schema_arkcasedb + """.pvsel04.medium_int
for read committed access
order by  """ + gvars.g_schema_arkcasedb + """.pvsel01.medium_int, """ + gvars.g_schema_arkcasedb + """.pvsel04.medium_int;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    _dci.expect_selected_msg(output, 15)
    
    stmt = """select [any 16] secon.medium_int
from  """ + gvars.g_schema_arkcasedb + """.pvsel01 f, """ + gvars.g_schema_arkcasedb + """.pvsel01 secon
group by secon.medium_int
having secon.medium_int <> 5000
for serializable access
order by secon.medium_int;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    _dci.expect_selected_msg(output, 4)
    
    stmt = """select [any 16] *
from  """ + gvars.g_schema_arkcasedb + """.svsel13 f, """ + gvars.g_schema_arkcasedb + """.svsel13 secon
order by f.new_name_1,f.new_name_3,
f.new_name_4,secon.new_name_4
for read uncommitted access;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 16)
    
    stmt = """select [any 16] secon.char_1,f.medium_int
from  """ + gvars.g_schema_arkcasedb + """.btsel01 f,  """ + gvars.g_schema_arkcasedb + """.btsel01 secon
group by secon.char_1,f.medium_int
for serializable access
order by secon.char_1,f.medium_int;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 16)
    
    _testmgr.testcase_end(desc)

def test006(desc="""a06"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt1376 : A05
    #  Original Test case: arkt0013 : A05
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
    
    #  this query is similar to the s query in testcase A0 -
    #  only 'count(*)' is also selected to determine if the join
    #  is executing properly
    
    stmt = """select [any 2] medium_int, count(*)
from  """ + gvars.g_schema_arkcasedb + """.btsel03, """ + gvars.g_schema_arkcasedb + """.btsel04 
group by medium_int
order by medium_int;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    _dci.expect_selected_msg(output, 2)
    
    #  similar to query above, without reference to btsel04 -
    #  compare value returned for count(*) here to value
    #  returned for count(*), above
    
    stmt = """select [any 2] medium_int, count(*)
from  """ + gvars.g_schema_arkcasedb + """.btsel04 
group by medium_int
order by medium_int;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 2)
    
    stmt = """select [any 2] binary_64_s, """ + gvars.g_schema_arkcasedb + """.pvsel04.pic_comp_1,min(ALL decimal_2_signed)
from  """ + gvars.g_schema_arkcasedb + """.btsel01,  """ + gvars.g_schema_arkcasedb + """.pvsel04 
group by binary_64_s,  """ + gvars.g_schema_arkcasedb + """.pvsel04.pic_comp_1
order by binary_64_s,  """ + gvars.g_schema_arkcasedb + """.pvsel04.pic_comp_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 2)
    
    stmt = """select [any 2]  """ + gvars.g_schema_arkcasedb + """.pvsel03.new_name_2, sum( """ + gvars.g_schema_arkcasedb + """.pvsel03.new_name_2)
from  """ + gvars.g_schema_arkcasedb + """.pvsel03,  """ + gvars.g_schema_arkcasedb + """.svsel13 
group by  """ + gvars.g_schema_arkcasedb + """.pvsel03.new_name_2
order by  """ + gvars.g_schema_arkcasedb + """.pvsel03.new_name_2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 2)
    
    stmt = """select [any 2]  """ + gvars.g_schema_arkcasedb + """.pvsel03.new_name_2, sum( """ + gvars.g_schema_arkcasedb + """.svsel13.new_name_2)
from  """ + gvars.g_schema_arkcasedb + """.pvsel03,  """ + gvars.g_schema_arkcasedb + """.svsel13 
group by  """ + gvars.g_schema_arkcasedb + """.pvsel03.new_name_2
order by  """ + gvars.g_schema_arkcasedb + """.pvsel03.new_name_2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 2)
    
    stmt = """select [any 2] """ + gvars.g_schema_arkcasedb + """.svsel13.pic_comp_1, count(distinct  """ + gvars.g_schema_arkcasedb + """.svsel13.var_char)
from  """ + gvars.g_schema_arkcasedb + """.svsel13,  """ + gvars.g_schema_arkcasedb + """.btsel01 
group by  """ + gvars.g_schema_arkcasedb + """.svsel13.pic_comp_1
order by  """ + gvars.g_schema_arkcasedb + """.svsel13.pic_comp_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 2)
    
    stmt = """select [any 2] """ + gvars.g_schema_arkcasedb + """.svsel13.pic_comp_1, count(distinct  """ + gvars.g_schema_arkcasedb + """.btsel01.var_char)
from  """ + gvars.g_schema_arkcasedb + """.svsel13,  """ + gvars.g_schema_arkcasedb + """.btsel01 
group by  """ + gvars.g_schema_arkcasedb + """.svsel13.pic_comp_1
order by  """ + gvars.g_schema_arkcasedb + """.svsel13.pic_comp_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 2)
    
    stmt = """select [any 2]  """ + gvars.g_schema_arkcasedb + """.btsel01.medium_int,
min(ALL  """ + gvars.g_schema_arkcasedb + """.pvsel01.large_int *  """ + gvars.g_schema_arkcasedb + """.btsel01.medium_int)
from  """ + gvars.g_schema_arkcasedb + """.pvsel01,  """ + gvars.g_schema_arkcasedb + """.btsel01 
group by  """ + gvars.g_schema_arkcasedb + """.btsel01.medium_int
order by  """ + gvars.g_schema_arkcasedb + """.btsel01.medium_int;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 2)
    
    stmt = """select [any 2] f.pic_comp_1, avg(f.pic_comp_1) + sum(s.pic_comp_1)
from  """ + gvars.g_schema_arkcasedb + """.svsel13 f,  """ + gvars.g_schema_arkcasedb + """.svsel13 s
group by f.pic_comp_1
order by f.pic_comp_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 2)
    
    #  queries with predicates
    
    stmt = """select [any 2] f.binary_64_s, count(*)
from  """ + gvars.g_schema_arkcasedb + """.btsel01 f,  """ + gvars.g_schema_arkcasedb + """.btsel01 s
where f.var_char = 'thomas'
group by f.binary_64_s
order by f.binary_64_s;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    _dci.expect_selected_msg(output, 1)
    
    stmt = """select [any 2] large_int, count(*)
from  """ + gvars.g_schema_arkcasedb + """.btsel01,  """ + gvars.g_schema_arkcasedb + """.pvsel04 
where  """ + gvars.g_schema_arkcasedb + """.btsel01.large_int =  """ + gvars.g_schema_arkcasedb + """.pvsel04.medium_int
group by large_int
order by large_int;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    _dci.expect_selected_msg(output, 2)
    
    stmt = """select [any 2]  """ + gvars.g_schema_arkcasedb + """.svsel13.pic_comp_1, avg(decimal_1)
from  """ + gvars.g_schema_arkcasedb + """.svsel13,  """ + gvars.g_schema_arkcasedb + """.btsel01 
where decimal_3_unsigned = new_name_1
group by  """ + gvars.g_schema_arkcasedb + """.svsel13.pic_comp_1
order by  """ + gvars.g_schema_arkcasedb + """.svsel13.pic_comp_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 2)
    
    stmt = """select [any 2]  """ + gvars.g_schema_arkcasedb + """.pvsel01.medium_int,
avg(distinct  """ + gvars.g_schema_arkcasedb + """.pvsel04.medium_int)
from  """ + gvars.g_schema_arkcasedb + """.pvsel01,  """ + gvars.g_schema_arkcasedb + """.pvsel04 
where  """ + gvars.g_schema_arkcasedb + """.pvsel01.medium_int >  """ + gvars.g_schema_arkcasedb + """.pvsel04.medium_int
group by  """ + gvars.g_schema_arkcasedb + """.pvsel01.medium_int
order by  """ + gvars.g_schema_arkcasedb + """.pvsel01.medium_int;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 2)
    
    stmt = """select [any 2] pic_9_7, sum(binary_32_u + pic_comp_1)
from  """ + gvars.g_schema_arkcasedb + """.btsel03,  """ + gvars.g_schema_arkcasedb + """.btsel04 
where pic_comp_1 in (medium_int, binary_64_s)
group by pic_9_7
order by pic_9_7;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 2)
    
    stmt = """select [any 2] pic_comp_1, avg(col_7) * sum(pic_comp_1)
from  """ + gvars.g_schema_arkcasedb + """.svsel13,  """ + gvars.g_schema_arkcasedb + """.svsel11 
where new_name_3 = col_8
group by pic_comp_1
order by pic_comp_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 2)
    
    _testmgr.testcase_end(desc)

def test007(desc="""a07"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt1376 : A07
    #  Original Test case: arkt0013 : A07
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
    
    #  test use of HAVING clause with no GROUP BY clause
    
    stmt = """select [any 1] sum(pic_decimal_2), max( """ + gvars.g_schema_arkcasedb + """.pvsel04.var_char)
from  """ + gvars.g_schema_arkcasedb + """.btsel01, """ + gvars.g_schema_arkcasedb + """.pvsel04 
having avg( """ + gvars.g_schema_arkcasedb + """.btsel01.pic_comp_1) > 500 and
avg( """ + gvars.g_schema_arkcasedb + """.pvsel04.pic_comp_1) > 1000;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    _dci.expect_selected_msg(output, 1)
    
    stmt = """select [any 1] f.binary_64_s, count(*)
from  """ + gvars.g_schema_arkcasedb + """.btsel01 f,  """ + gvars.g_schema_arkcasedb + """.btsel01 s
group by f.binary_64_s
having sum(distinct f.pic_comp_1) < 1000
order by f.binary_64_s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    
    stmt = """select [any 1] avg(f.large_int)
from  """ + gvars.g_schema_arkcasedb + """.pvsel01 f,  """ + gvars.g_schema_arkcasedb + """.pvsel01 s
group by f.medium_int
having sum(f.large_int) > 0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    #       order by f.medium_int;
    
    stmt = """select [any 1] avg(s.large_int)
from  """ + gvars.g_schema_arkcasedb + """.pvsel01 f,  """ + gvars.g_schema_arkcasedb + """.pvsel01 s
group by f.medium_int
having sum(ALL f.large_int) > 0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    #       order by f.medium_int;
    
    stmt = """select [any 1] binary_64_s, """ + gvars.g_schema_arkcasedb + """.pvsel04.pic_comp_1,min(ALL decimal_2_signed)
from  """ + gvars.g_schema_arkcasedb + """.btsel01,  """ + gvars.g_schema_arkcasedb + """.pvsel04 
group by binary_64_s,  """ + gvars.g_schema_arkcasedb + """.pvsel04.pic_comp_1
having max(binary_32_u) >= 50
order by binary_64_s,  """ + gvars.g_schema_arkcasedb + """.pvsel04.pic_comp_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    
    stmt = """select [any 1]  """ + gvars.g_schema_arkcasedb + """.pvsel03.new_name_2, sum( """ + gvars.g_schema_arkcasedb + """.pvsel03.new_name_2)
from  """ + gvars.g_schema_arkcasedb + """.pvsel03,  """ + gvars.g_schema_arkcasedb + """.svsel13 
group by  """ + gvars.g_schema_arkcasedb + """.pvsel03.new_name_2
having sum( """ + gvars.g_schema_arkcasedb + """.svsel13.new_name_1) > 500
order by  """ + gvars.g_schema_arkcasedb + """.pvsel03.new_name_2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    
    stmt = """select [any 1]  """ + gvars.g_schema_arkcasedb + """.pvsel03.new_name_2, sum( """ + gvars.g_schema_arkcasedb + """.svsel13.new_name_2)
from  """ + gvars.g_schema_arkcasedb + """.pvsel03,  """ + gvars.g_schema_arkcasedb + """.svsel13 
group by  """ + gvars.g_schema_arkcasedb + """.pvsel03.new_name_2
having sum(distinct  """ + gvars.g_schema_arkcasedb + """.svsel13.new_name_1) > 100
order by  """ + gvars.g_schema_arkcasedb + """.pvsel03.new_name_2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    
    stmt = """select [any 1] """ + gvars.g_schema_arkcasedb + """.svsel13.pic_comp_1, count(distinct  """ + gvars.g_schema_arkcasedb + """.svsel13.var_char)
from  """ + gvars.g_schema_arkcasedb + """.svsel13,  """ + gvars.g_schema_arkcasedb + """.btsel01 
group by  """ + gvars.g_schema_arkcasedb + """.svsel13.pic_comp_1
having avg((new_name_1 * new_name_2) / 2) <> 240
order by  """ + gvars.g_schema_arkcasedb + """.svsel13.pic_comp_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    
    stmt = """select [any 1] """ + gvars.g_schema_arkcasedb + """.svsel13.pic_comp_1, count(distinct """ + gvars.g_schema_arkcasedb + """.btsel01.var_char)
from  """ + gvars.g_schema_arkcasedb + """.svsel13,  """ + gvars.g_schema_arkcasedb + """.btsel01 
group by """ + gvars.g_schema_arkcasedb + """.svsel13.pic_comp_1
having min( """ + gvars.g_schema_arkcasedb + """.svsel13.medium_int +  """ + gvars.g_schema_arkcasedb + """.btsel01.medium_int)
< 2000
order by """ + gvars.g_schema_arkcasedb + """.svsel13.pic_comp_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    
    stmt = """select [any 1] """ + gvars.g_schema_arkcasedb + """.btsel01.binary_64_s, avg(ALL binary_32_u +  """ + gvars.g_schema_arkcasedb + """.btsel04.pic_comp_1)
from  """ + gvars.g_schema_arkcasedb + """.btsel01,  """ + gvars.g_schema_arkcasedb + """.btsel04 
group by  """ + gvars.g_schema_arkcasedb + """.btsel01.binary_64_s
having sum( """ + gvars.g_schema_arkcasedb + """.btsel04.medium_int) +
sum( """ + gvars.g_schema_arkcasedb + """.btsel04.pic_comp_1) > 20000
order by  """ + gvars.g_schema_arkcasedb + """.btsel01.binary_64_s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    
    stmt = """select [any 1]  """ + gvars.g_schema_arkcasedb + """.btsel01.medium_int,
min(ALL  """ + gvars.g_schema_arkcasedb + """.pvsel01.large_int *  """ + gvars.g_schema_arkcasedb + """.btsel01.medium_int)
from  """ + gvars.g_schema_arkcasedb + """.pvsel01,  """ + gvars.g_schema_arkcasedb + """.btsel01 
group by  """ + gvars.g_schema_arkcasedb + """.btsel01.medium_int
having avg( """ + gvars.g_schema_arkcasedb + """.btsel01.medium_int) >
avg( """ + gvars.g_schema_arkcasedb + """.pvsel01.medium_int)
order by  """ + gvars.g_schema_arkcasedb + """.btsel01.medium_int;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    
    stmt = """select [any 1]  """ + gvars.g_schema_arkcasedb + """.btsel01.medium_int,
min(ALL  """ + gvars.g_schema_arkcasedb + """.pvsel01.large_int *  """ + gvars.g_schema_arkcasedb + """.btsel01.medium_int)
from  """ + gvars.g_schema_arkcasedb + """.pvsel01,  """ + gvars.g_schema_arkcasedb + """.btsel01 
group by  """ + gvars.g_schema_arkcasedb + """.btsel01.medium_int
having count(*) <> 16
order by  """ + gvars.g_schema_arkcasedb + """.btsel01.medium_int;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    
    #  queries with predicates
    
    stmt = """select [any 1] large_int, count(*)
from  """ + gvars.g_schema_arkcasedb + """.btsel01,  """ + gvars.g_schema_arkcasedb + """.pvsel04 
where  """ + gvars.g_schema_arkcasedb + """.btsel01.large_int =  """ + gvars.g_schema_arkcasedb + """.pvsel04.medium_int
group by large_int
having sum( """ + gvars.g_schema_arkcasedb + """.btsel01.small_int) >
sum(decimal_2_signed * 100)
order by large_int;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    
    stmt = """select [any 1]  """ + gvars.g_schema_arkcasedb + """.svsel13.pic_comp_1, avg(decimal_1)
from  """ + gvars.g_schema_arkcasedb + """.svsel13,  """ + gvars.g_schema_arkcasedb + """.btsel01 
where decimal_3_unsigned = new_name_1
group by  """ + gvars.g_schema_arkcasedb + """.svsel13.pic_comp_1
having min(ALL pic_decimal_3) < 5
order by  """ + gvars.g_schema_arkcasedb + """.svsel13.pic_comp_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    
    stmt = """select [any 1]  """ + gvars.g_schema_arkcasedb + """.pvsel01.medium_int,
avg(distinct  """ + gvars.g_schema_arkcasedb + """.pvsel04.medium_int)
from  """ + gvars.g_schema_arkcasedb + """.pvsel01,  """ + gvars.g_schema_arkcasedb + """.pvsel04 
where  """ + gvars.g_schema_arkcasedb + """.pvsel01.medium_int >  """ + gvars.g_schema_arkcasedb + """.pvsel04.medium_int
group by  """ + gvars.g_schema_arkcasedb + """.pvsel01.medium_int
having avg(pic_decimal_3 *  """ + gvars.g_schema_arkcasedb + """.pvsel04.medium_int) < 7500
order by  """ + gvars.g_schema_arkcasedb + """.pvsel01.medium_int;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    
    stmt = """select [any 1] pic_9_7, sum(binary_32_u + pic_comp_1)
from  """ + gvars.g_schema_arkcasedb + """.btsel03,  """ + gvars.g_schema_arkcasedb + """.btsel04 
where pic_comp_1 in (medium_int, binary_64_s)
group by pic_9_7
having sum(distinct binary_32_u) <> 5
order by pic_9_7;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    
    stmt = """select [any 1] pic_comp_1, avg(col_7) * sum(pic_comp_1)
from  """ + gvars.g_schema_arkcasedb + """.svsel13,  """ + gvars.g_schema_arkcasedb + """.svsel11 
where new_name_3 = col_8
group by pic_comp_1
having sum(col_4 * col_7) < 5000
order by pic_comp_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    
    #  complex queries
    
    stmt = """select [any 1] large_int, count(*)
from  """ + gvars.g_schema_arkcasedb + """.btsel01,  """ + gvars.g_schema_arkcasedb + """.pvsel04 
where  """ + gvars.g_schema_arkcasedb + """.btsel01.large_int =  """ + gvars.g_schema_arkcasedb + """.pvsel04.medium_int
group by large_int
having sum( """ + gvars.g_schema_arkcasedb + """.btsel01.small_int) >
sum(decimal_2_signed * 100)
order by large_int
for serializable access;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    
    stmt = """select [any 1]  """ + gvars.g_schema_arkcasedb + """.svsel13.pic_comp_1, avg(decimal_1)
from   """ + gvars.g_schema_arkcasedb + """.svsel13,  """ + gvars.g_schema_arkcasedb + """.btsel01 
where decimal_3_unsigned = new_name_1
group by  """ + gvars.g_schema_arkcasedb + """.svsel13.pic_comp_1
having min(ALL pic_decimal_3) < 5
order by 1 DESC  ,2 DESC
for read committed access;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    
    stmt = """select [any 1]  """ + gvars.g_schema_arkcasedb + """.pvsel01.medium_int,
avg(distinct  """ + gvars.g_schema_arkcasedb + """.pvsel04.medium_int)
from   """ + gvars.g_schema_arkcasedb + """.pvsel01,  """ + gvars.g_schema_arkcasedb + """.pvsel04 
where  """ + gvars.g_schema_arkcasedb + """.pvsel01.medium_int >  """ + gvars.g_schema_arkcasedb + """.pvsel04.medium_int
group by  """ + gvars.g_schema_arkcasedb + """.pvsel01.medium_int
having avg(pic_decimal_3 *  """ + gvars.g_schema_arkcasedb + """.pvsel04.medium_int) < 7500
order by 2, """ + gvars.g_schema_arkcasedb + """.pvsel01.medium_int
for read uncommitted access;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    
    stmt = """select [any 1] pic_9_7, sum(binary_32_u + pic_comp_1)
from  """ + gvars.g_schema_arkcasedb + """.btsel03,  """ + gvars.g_schema_arkcasedb + """.btsel04 
where pic_comp_1 in (medium_int, binary_64_s)
group by pic_9_7
having sum(distinct binary_32_u) <> 5
order by pic_9_7 ASC
for serializable access;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    
    stmt = """select [any 1] pic_comp_1, avg(col_7) * sum(pic_comp_1)
from  """ + gvars.g_schema_arkcasedb + """.svsel13,  """ + gvars.g_schema_arkcasedb + """.svsel11 
where new_name_3 = col_8
group by pic_comp_1
having sum(col_4 * col_7) < 5000
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    
    _testmgr.testcase_end(desc)

