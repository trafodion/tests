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
    #  Test case name:     arkt1374 : A01
    #  Original Test case: arkt0010 : A01
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
    
    stmt = """select [any 2] char_1,decimal_1 from """ + gvars.g_schema_arkcasedb + """.btsel01 
group by char_1,decimal_1
order by char_1,decimal_1;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    _dci.expect_selected_msg(output, 2)
    
    stmt = """select [any 2] pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
group by pic_x_1
order by pic_x_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 2)
    
    stmt = """select [any 2] pic_x_7,pic_9_7 from """ + gvars.g_schema_arkcasedb + """.btsel03 
group by pic_9_7,pic_x_7
order by pic_9_7,pic_x_7 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 2)
    
    stmt = """select [any 2] medium_int from """ + gvars.g_schema_arkcasedb + """.btsel04 
group by medium_int
order by medium_int;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 2)
    
    stmt = """select [any 2] pic_x_b from """ + gvars.g_schema_arkcasedb + """.btsel05 
group by pic_x_b
order by pic_x_b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 2)
    
    stmt = """select [any 2] pic_x_a,col_1,col_3 from """ + gvars.g_schema_arkcasedb + """.btsel06 
group by pic_x_a,col_1,col_3
order by pic_x_a,col_1,col_3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 2)
    
    stmt = """select [any 2] pic_x_a,col_1,col_3 from """ + gvars.g_schema_arkcasedb + """.btsel06 
group by pic_x_a, col_1,col_1, col_3
order by pic_x_a, col_1, col_3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 2)
    
    stmt = """select [any 2] pic_x_a,col_1,col_3 from """ + gvars.g_schema_arkcasedb + """.btsel06 
group by pic_x_a,col_1,col_3, col_1
order by pic_x_a,col_1,col_3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 2)
    
    stmt = """select [any 2] pic_x_a from """ + gvars.g_schema_arkcasedb + """.btsel07 
group by pic_x_a
order by pic_x_a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 2)
    
    stmt = """select [any 2] pic_1,large_int from """ + gvars.g_schema_arkcasedb + """.btsel08 
group by pic_1,large_int
order by pic_1,large_int;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 2)
    
    #  Order by should have all the col names in the select [any 2] list
    stmt = """select [any 2] large_int from """ + gvars.g_schema_arkcasedb + """.btsel08 
group by pic_1,large_int
order by large_int;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 2)
    #       order by pic_1,arge_int;
    
    stmt = """select [any 2] pic_x_5 from """ + gvars.g_schema_arkcasedb + """.btsel09 
group by pic_x_5
order by pic_x_5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 2)
    
    stmt = """select [any 2] binary_32_signed from """ + gvars.g_schema_arkcasedb + """.btsel10 
group by binary_32_signed
order by binary_32_signed;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 2)
    
    stmt = """select [any 2] decimal_10 from """ + gvars.g_schema_arkcasedb + """.btsel11 
group by decimal_10
order by decimal_10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 2)
    
    stmt = """select [any 2] new_name_1 from """ + gvars.g_schema_arkcasedb + """.pvsel03 
group by new_name_1
order by new_name_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 2)
    
    stmt = """select [any 2] new_name_1 from """ + gvars.g_schema_arkcasedb + """.svsel13 
group by new_name_1
order by new_name_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 2)
    
    stmt = """select [any 2] SYSKEY
from """ + gvars.g_schema_arkcasedb + """.btsel04 
group by SYSKEY
order by SYSKEY;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 2)
    
    # Order by should have all the col names in the select [any 2] list
    stmt = """select [any 2] medium_int, binary_64_s, medium_int * binary_64_s
from """ + gvars.g_schema_arkcasedb + """.btsel01 
group by medium_int,binary_64_s
order by medium_int,binary_64_s;"""
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
    #  Test case name:     arkt1374 : A02
    #  Original Test case: arkt0010 : A02
    #  Description:        This test verifies the SQL simple
    #                      SELECT [any <N>] statements with JOIN
    #                      select joins simple testcase - this tests
    #                      the use of SELECT DISTINCT and SELECT ALL
    #                      statements on multiple tables.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    
    stmt = """select [any 4] distinct pic_x_1,pic_x_7
from  """ + gvars.g_schema_arkcasedb + """.btsel02, """ + gvars.g_schema_arkcasedb + """.btsel03 
order by pic_x_1,pic_x_7;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    _dci.expect_selected_msg(output, 4)
    
    stmt = """select [any 4] all pic_x_1,pic_x_7
from  """ + gvars.g_schema_arkcasedb + """.btsel02, """ + gvars.g_schema_arkcasedb + """.btsel03 
order by  """ + gvars.g_schema_arkcasedb + """.btsel02.syskey,  """ + gvars.g_schema_arkcasedb + """.btsel03.syskey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 4)
    
    stmt = """select [any 4] distinct   """ + gvars.g_schema_arkcasedb + """.btsel02.*,pic_x_7,binary_32_u
from  """ + gvars.g_schema_arkcasedb + """.btsel02, """ + gvars.g_schema_arkcasedb + """.btsel03 
order by  """ + gvars.g_schema_arkcasedb + """.btsel02.pic_x_1,pic_x_7,binary_32_u;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 4)
    
    stmt = """select [any 4] all   """ + gvars.g_schema_arkcasedb + """.btsel02.*,pic_x_7,binary_32_u
from  """ + gvars.g_schema_arkcasedb + """.btsel02, """ + gvars.g_schema_arkcasedb + """.btsel03 
order by  """ + gvars.g_schema_arkcasedb + """.btsel02.syskey,  """ + gvars.g_schema_arkcasedb + """.btsel03.syskey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 4)
    
    stmt = """select [any 4] distinct *
from  """ + gvars.g_schema_arkcasedb + """.btsel02, """ + gvars.g_schema_arkcasedb + """.btsel10 
order by pic_x_1, pic_9_7 asc, pic_x_7 desc, pic_x_a asc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 4)
    
    stmt = """select [any 4] all *
from  """ + gvars.g_schema_arkcasedb + """.btsel02, """ + gvars.g_schema_arkcasedb + """.btsel10 
order by syskey, pic_9_7 asc, pic_x_7 desc, pic_x_a asc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 4)
    
    stmt = """select [any 4] distinct   """ + gvars.g_schema_arkcasedb + """.btsel02.*,  """ + gvars.g_schema_arkcasedb + """.btsel10.*
from  """ + gvars.g_schema_arkcasedb + """.btsel02, """ + gvars.g_schema_arkcasedb + """.btsel10 
order by pic_x_1, pic_9_7 asc, pic_x_7 desc, pic_x_a asc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 4)
    
    stmt = """select [any 4] all   """ + gvars.g_schema_arkcasedb + """.btsel02.*,  """ + gvars.g_schema_arkcasedb + """.btsel10.*
from  """ + gvars.g_schema_arkcasedb + """.btsel02, """ + gvars.g_schema_arkcasedb + """.btsel10 
order by syskey, pic_9_7 asc, pic_x_7 desc, pic_x_a asc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 4)
    
    stmt = """select [any 4] distinct new_name_3,pic_x_7
from  """ + gvars.g_schema_arkcasedb + """.pvsel03, """ + gvars.g_schema_arkcasedb + """.pvsel04 
order by new_name_3,pic_x_7;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 4)
    
    stmt = """select [any 4] all new_name_3,pic_x_7
from  """ + gvars.g_schema_arkcasedb + """.pvsel03, """ + gvars.g_schema_arkcasedb + """.pvsel04 
order by new_name_4, pic_comp_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 4)
    
    stmt = """select [any 4] distinct pic_x_b,pic_x_7
from  """ + gvars.g_schema_arkcasedb + """.btsel07, """ + gvars.g_schema_arkcasedb + """.pvsel04 
order by pic_x_b,pic_x_7;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 4)
    
    stmt = """select [any 4] all pic_x_b,pic_x_7
from  """ + gvars.g_schema_arkcasedb + """.btsel07, """ + gvars.g_schema_arkcasedb + """.pvsel04 
order by pic_x_c, pic_x_b, pic_x_a, pic_comp_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 4)
    
    stmt = """select [any 4] distinct   """ + gvars.g_schema_arkcasedb + """.pvsel03.new_name_3,  """ + gvars.g_schema_arkcasedb + """.svsel13.new_name_3
from  """ + gvars.g_schema_arkcasedb + """.pvsel03, """ + gvars.g_schema_arkcasedb + """.svsel13 
order by  """ + gvars.g_schema_arkcasedb + """.pvsel03.new_name_3,  """ + gvars.g_schema_arkcasedb + """.svsel13.new_name_3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 4)
    
    stmt = """select [any 4] all   """ + gvars.g_schema_arkcasedb + """.pvsel03.new_name_3,  """ + gvars.g_schema_arkcasedb + """.svsel13.new_name_3
from  """ + gvars.g_schema_arkcasedb + """.pvsel03, """ + gvars.g_schema_arkcasedb + """.svsel13 
order by  """ + gvars.g_schema_arkcasedb + """.pvsel03.new_name_4,  """ + gvars.g_schema_arkcasedb + """.svsel13.new_name_4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 4)
    
    stmt = """select [any 4] distinct col_3
from  """ + gvars.g_schema_arkcasedb + """.svsel13, """ + gvars.g_schema_arkcasedb + """.svsel11 
order by col_3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 4)
    
    stmt = """select [any 4] all col_3
from  """ + gvars.g_schema_arkcasedb + """.svsel13, """ + gvars.g_schema_arkcasedb + """.svsel11 
order by new_name_4, col_4, col_8;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 4)
    
    stmt = """select [any 4] distinct firs.pic_x_1,secon.pic_x_1
from  """ + gvars.g_schema_arkcasedb + """.btsel02 firs, """ + gvars.g_schema_arkcasedb + """.btsel02 secon
order by firs.pic_x_1,secon.pic_x_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 4)
    
    stmt = """select [any 4] all firs.pic_x_1,secon.pic_x_1
from  """ + gvars.g_schema_arkcasedb + """.btsel02 firs, """ + gvars.g_schema_arkcasedb + """.btsel02 secon
order by firs.syskey, secon.syskey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 4)
    
    stmt = """select [any 4] distinct firs.new_name_3,secon.new_name_3
from  """ + gvars.g_schema_arkcasedb + """.pvsel03 firs, """ + gvars.g_schema_arkcasedb + """.pvsel03 secon
order by firs.new_name_3,secon.new_name_3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 4)
    
    stmt = """select [any 4] all firs.new_name_3,secon.new_name_3
from  """ + gvars.g_schema_arkcasedb + """.pvsel03 firs, """ + gvars.g_schema_arkcasedb + """.pvsel03 secon
order by firs.new_name_4, secon.new_name_4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 4)
    
    stmt = """select [any 4] distinct firs.new_name_3,secon.new_name_3
from  """ + gvars.g_schema_arkcasedb + """.svsel13 firs, """ + gvars.g_schema_arkcasedb + """.svsel13 secon
order by firs.new_name_3,secon.new_name_3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 4)
    
    stmt = """select [any 4] all firs.new_name_3,secon.new_name_3
from  """ + gvars.g_schema_arkcasedb + """.svsel13 firs, """ + gvars.g_schema_arkcasedb + """.svsel13 secon
order by firs.new_name_4, secon.new_name_4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 4)
    
    stmt = """select [any 4] distinct pic_x_1,binary_64_s,medium_int
from  """ + gvars.g_schema_arkcasedb + """.btsel02,
 """ + gvars.g_schema_arkcasedb + """.btsel03,
 """ + gvars.g_schema_arkcasedb + """.btsel04 
order by pic_x_1,binary_64_s,medium_int;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 4)
    
    stmt = """select [any 4] all pic_x_1,binary_64_s,medium_int
from  """ + gvars.g_schema_arkcasedb + """.btsel02,
 """ + gvars.g_schema_arkcasedb + """.btsel03,
 """ + gvars.g_schema_arkcasedb + """.btsel04 
order by  """ + gvars.g_schema_arkcasedb + """.btsel02.syskey,  """ + gvars.g_schema_arkcasedb + """.btsel03.syskey,  """ + gvars.g_schema_arkcasedb + """.btsel04.syskey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 4)
    
    _testmgr.testcase_end(desc)

def test003(desc="""a03"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt1374 : A03
    #  Original Test case: arkt0010 : A03
    #  Description:        This test verifies the SQL SELECT
    #                      statement. Tests only normal (non-join &
    #                      non-subquery) select [any 1] statements, with
    #                      GROUP BY, HAVING & ORDER BY clauses &
    #                      some complex queries with all together
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    
    stmt = """select [any 1] * from """ + gvars.g_schema_arkcasedb + """.btsel01 
order by char_1,decimal_1, binary_signed;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    _dci.expect_selected_msg(output, 1)
    
    stmt = """select [any 1] * from """ + gvars.g_schema_arkcasedb + """.btsel02 
order by pic_x_1 ASC, syskey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    
    stmt = """select [any 1] * from """ + gvars.g_schema_arkcasedb + """.btsel03 
order by 4,1 DESC, syskey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    
    stmt = """select [any 1] * from """ + gvars.g_schema_arkcasedb + """.btsel04 
order by 2, syskey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    
    stmt = """select [any 1] * from """ + gvars.g_schema_arkcasedb + """.btsel05 
order by pic_x_b DESC, syskey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    
    stmt = """select [any 1] * from """ + gvars.g_schema_arkcasedb + """.btsel06 
order by pic_x_a DESC,col_1,col_3 ASC, pic_x_b, pic_x_c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    
    stmt = """select [any 1] * from """ + gvars.g_schema_arkcasedb + """.btsel06 
order by pic_x_a , col_1,col_1, col_3, pic_x_b, pic_x_c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    
    stmt = """select [any 1] * from """ + gvars.g_schema_arkcasedb + """.btsel06 
order by pic_x_a , col_1, col_3, col_1, pic_x_b, pic_x_c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    
    stmt = """select [any 1] * from """ + gvars.g_schema_arkcasedb + """.btsel06 
order by pic_x_a , col_1 ASC, col_1 DESC, col_3, pic_x_b, pic_x_c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    
    stmt = """select [any 1] * from """ + gvars.g_schema_arkcasedb + """.btsel07 
order by pic_x_a, pic_x_c, pic_x_b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    
    stmt = """select [any 1] * from """ + gvars.g_schema_arkcasedb + """.btsel08 
order by 3  DESC, large_int ASC;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    
    stmt = """select [any 1] * from """ + gvars.g_schema_arkcasedb + """.btsel09 
order by pic_x_5, pic_x_a, pic_x_6 desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    
    stmt = """select [any 1] * from """ + gvars.g_schema_arkcasedb + """.btsel10 
order by binary_32_signed, pic_x_a, pic_9_7 asc, pic_x_7 desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    
    stmt = """select [any 1] * from """ + gvars.g_schema_arkcasedb + """.btsel11 
order by decimal_10, pic_x_a, pic_9_7 desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    
    stmt = """select [any 1] * from """ + gvars.g_schema_arkcasedb + """.pvsel03 
order by new_name_1, new_name_4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    
    stmt = """select [any 1] * from """ + gvars.g_schema_arkcasedb + """.svsel13 
order by new_name_1, new_name_4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    
    #  order by SYSKEY
    
    stmt = """select [any 1] SYSKEY,*
from """ + gvars.g_schema_arkcasedb + """.btsel03 
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    
    stmt = """select [any 1] *,SYSKEY
from """ + gvars.g_schema_arkcasedb + """.btsel03 
order by 6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    
    stmt = """select [any 1] *,SYSKEY
from """ + gvars.g_schema_arkcasedb + """.btsel03 
order by 4,6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    
    stmt = """select [any 1] small_int
from """ + gvars.g_schema_arkcasedb + """.btsel01 
order by medium_int, binary_signed;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    
    _testmgr.testcase_end(desc)

def test004(desc="""a04"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt1374 : A04
    #  Original Test case: arkt0010 : A04
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
    stmt = """select [any 3] char_1, decimal_1
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
    _dci.unexpect_error_msg(output)
    _dci.expect_selected_msg(output, 3)
    
    #  Query 2
    stmt = """select [any 3] distinct var_char,binary_64_s, pic_comp_1
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
    _dci.expect_selected_msg(output, 3)
    
    #  Order by should have all the cols in the select [any 3] list
    #  Testware correction made on oct 22
    #  Query 3
    stmt = """select [any 3] (new_name_1 * new_name_1), new_name_1, new_name_3
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
    _dci.unexpect_error_msg(output)
    _dci.expect_selected_msg(output, 2)
    
    #  Query 4
    stmt = """select [any 3] new_name_1,new_name_4
from """ + gvars.g_schema_arkcasedb + """.svsel13 
where ((var_char like 'b%') or (var_char like 'tom')) and
(pic_comp_1 in (200,300,400,500)) and
(new_name_1 between 80 and 90)
group by new_name_1,new_name_4
having new_name_1 = 80
order by new_name_1, new_name_4
for read uncommitted access;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    _dci.expect_selected_msg(output, 3)
    
    #  Query 5
    stmt = """select [any 3] medium_int,SYSKEY
from """ + gvars.g_schema_arkcasedb + """.btsel04 
where (medium_int > 200)
group by medium_int,SYSKEY
having medium_int in (999,1000,2000)
order by medium_int,SYSKEY;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 3)
    
    #  Query 6
    stmt = """select [any 3] pic_x_b from """ + gvars.g_schema_arkcasedb + """.btsel05 
where col_1 = 'lowry'
group by pic_x_b
order by pic_x_b;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    _dci.expect_selected_msg(output, 2)
    
    #  Query 7
    stmt = """select [any 3] col_6, pic_x_a,col_1, pic_x_b, pic_x_c
from """ + gvars.g_schema_arkcasedb + """.btsel06 
where col_6 < 90
order by pic_x_a,col_1, pic_x_b, pic_x_c;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    _dci.expect_selected_msg(output, 3)
    
    #  Query 8
    stmt = """select [any 3] pic_1,large_int from """ + gvars.g_schema_arkcasedb + """.btsel08 
where large_int >= 100
group by pic_1,large_int
having large_int in (100,200,1000,2000)
order by pic_1,large_int;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 3)
    
    #  Query 9
    stmt = """select [any 3] pic_x_5 from """ + gvars.g_schema_arkcasedb + """.btsel09 
where pic_x_6 <> 11
group by pic_x_5
order by pic_x_5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 3)
    
    #  Query 10
    stmt = """select [any 3] decimal_10 from """ + gvars.g_schema_arkcasedb + """.btsel10 
group by decimal_10
having decimal_10 in (90,100,110,10000,50000)
order by decimal_10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 3)
    
    _testmgr.testcase_end(desc)

def test005(desc="""a05"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt1374 : A05
    #  Original Test case: arkt0010 : A05
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
    
    #   *****    audited tables  *****
    
    stmt = """select [any 4] large_int from """ + gvars.g_schema_arkcasedb + """.btsel08 
group by large_int
for read uncommitted access
order by large_int;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    _dci.expect_selected_msg(output, 4)
    
    stmt = """select [any 4] pic_x_5 from """ + gvars.g_schema_arkcasedb + """.btsel09 
group by pic_x_5
having pic_x_5 > 4
for read committed access
order by pic_x_5;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    _dci.expect_selected_msg(output, 2)
    
    stmt = """select [any 4] * from """ + gvars.g_schema_arkcasedb + """.btsel10 
order by pic_9_7, pic_x_7 desc, pic_x_a asc
for serializable access;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    _dci.expect_selected_msg(output, 4)
    
    #   *****  non-audited tables *****
    
    stmt = """select [any 4] pic_x_b from """ + gvars.g_schema_arkcasedb + """.btsel05 
group by pic_x_b
for read committed access
order by pic_x_b;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    _dci.expect_selected_msg(output, 4)
    
    stmt = """select [any 4] pic_x_b from """ + gvars.g_schema_arkcasedb + """.btsel05 
group by pic_x_b
having (pic_x_b = 'D') or (pic_x_b = 'B')
for serializable access
order by pic_x_b;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    _dci.expect_selected_msg(output, 2)
    
    stmt = """select [any 4] * from """ + gvars.g_schema_arkcasedb + """.btsel05 
order by pic_x_b, syskey
for read uncommitted access;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    _dci.expect_selected_msg(output, 4)
    
    #     **** views *****
    
    stmt = """select [any 4] new_name_1 from """ + gvars.g_schema_arkcasedb + """.pvsel03 
group by new_name_1
for serializable access
order by new_name_1;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    _dci.expect_selected_msg(output, 2)
    
    stmt = """select [any 4] new_name_1 from """ + gvars.g_schema_arkcasedb + """.svsel13 
group by new_name_1
for serializable access
order by new_name_1;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    _dci.expect_selected_msg(output, 2)
    
    stmt = """select [any 4] new_name_1 from """ + gvars.g_schema_arkcasedb + """.pvsel03 
group by new_name_1
having new_name_1 = 80
for read uncommitted access
order by new_name_1;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    _dci.expect_selected_msg(output, 1)
    
    stmt = """select [any 4] new_name_1 from """ + gvars.g_schema_arkcasedb + """.svsel13 
group by new_name_1
having new_name_1 = 80
for read uncommitted access
order by new_name_1;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    _dci.expect_selected_msg(output, 1)
    
    stmt = """select [any 4] * from """ + gvars.g_schema_arkcasedb + """.pvsel03 
order by new_name_1, new_name_4
for read committed access;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    _dci.expect_selected_msg(output, 4)
    
    stmt = """select [any 4] * from """ + gvars.g_schema_arkcasedb + """.svsel13 
order by new_name_1, new_name_4
for read committed access;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    _dci.expect_selected_msg(output, 4)
    
    _testmgr.testcase_end(desc)

def test006(desc="""a06"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt1374 : A06
    #  Original Test case: arkt0010 : A06
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
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    
    #  Query 1
    stmt = """select [any 1] char_1, decimal_1
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
    _dci.unexpect_error_msg(output)
    _dci.expect_selected_msg(output, 1)
    
    #  Query 2
    stmt = """select [any 1] char_1, decimal_1
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
    _dci.expect_selected_msg(output, 1)
    
    #  Query 3
    stmt = """select [any 1] char_1, decimal_1
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
    _dci.expect_selected_msg(output, 1)
    
    #  Query 4
    stmt = """select [any 1] distinct var_char,binary_64_s, pic_comp_1
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
    _dci.expect_selected_msg(output, 1)
    
    #  Query 5
    stmt = """select [any 1] distinct var_char,binary_64_s, pic_comp_1
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
    _dci.expect_selected_msg(output, 1)
    
    #  Query 6
    stmt = """select [any 1] distinct var_char,binary_64_s, pic_comp_1
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
    _dci.expect_selected_msg(output, 1)
    
    #  Query 7
    stmt = """select [any 1] new_name_1,new_name_4
from """ + gvars.g_schema_arkcasedb + """.svsel13 
where ((var_char like 'b%') or (var_char like 'tom')) and
(pic_comp_1 in (200,300,400,500)) and
(new_name_1 between 80 and 90)
group by new_name_1,new_name_4
having new_name_1 = 80
order by new_name_1, new_name_4
for read uncommitted access;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    
    #  Query 8
    stmt = """select [any 1] medium_int,SYSKEY
from """ + gvars.g_schema_arkcasedb + """.btsel04 
where (medium_int > 200)
group by medium_int,SYSKEY
having medium_int in (999,1000,2000)
order by medium_int, syskey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    
    #  Query 9
    stmt = """select [any 1] pic_x_b
from """ + gvars.g_schema_arkcasedb + """.btsel05 
where col_1 = 'lowry'
group by pic_x_b
order by pic_x_b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    
    #  Query 10
    stmt = """select [any 1]  col_6, pic_x_a,col_1, pic_x_b, pic_x_c
from """ + gvars.g_schema_arkcasedb + """.btsel06 
where col_6 < 90
order by pic_x_a,col_1, pic_x_b, pic_x_c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    
    #  Query 11
    stmt = """select [any 1] pic_1,large_int
from """ + gvars.g_schema_arkcasedb + """.btsel08 
where large_int >= 100
group by pic_1,large_int
having large_int in (100,200,1000,2000)
order by pic_1,large_int;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    
    #  Query 12
    stmt = """select [any 1] pic_x_5
from """ + gvars.g_schema_arkcasedb + """.btsel09 
where pic_x_6 <> 11
group by pic_x_5
order by pic_x_5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    
    #  Query 13
    stmt = """select [any 1] decimal_10
from """ + gvars.g_schema_arkcasedb + """.btsel10 
group by decimal_10
having decimal_10 in (90,100,110,10000,50000)
order by decimal_10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    
    _testmgr.testcase_end(desc)

def test007(desc="""a07"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt1374 : A01
    #  Original Test case: arkt0010 : A01
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
    
    stmt = """select [any 2] char_1 , decimal_1
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
    _dci.unexpect_error_msg(output)
    _dci.expect_selected_msg(output, 2)
    
    # Moved the following query to testA30
    
    #       select [any 2] distinct var_char,binary_64_s, pic_comp_1
    #       from btsel01
    #       where (char_1 like '%') and
    #             (var_char in ('B','jimmy','thomas','marilyn','christopher'))
    #         and (binary_32_u between 50 and 100) and
    #             (decimal_1 > decimal_2_signed)
    #       group by binary_64_s,pic_comp_1, var_char
    #       having binary_64_s > pic_comp_1
    #       order by binary_64_s, 2 DESC, pic_comp_1, var_char
    #       for serializable access ;
    
    stmt = """select [any 2]                   (new_name_1*new_name_1), new_name_1, new_name_3
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
    _dci.unexpect_error_msg(output)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """select [any 2] new_name_1,new_name_4
FROM """ + gvars.g_schema_arkcasedb + """.svsel13 
WHERE ((var_char like 'b%') OR (var_char LIKE 'tom')) and
(pic_comp_1 IN (200,300,400,500)) AND
(new_name_1 BETWEEN 80 and 90)
group BY new_name_1,new_name_4
having new_name_1 = 80
ORDER by new_name_1, new_name_4
for read uncommitted access;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    _dci.expect_selected_msg(output, 2)
    
    stmt = """select [any 2] medium_int,SYSKEY
from """ + gvars.g_schema_arkcasedb + """.btsel04 
where (medium_int > 200)
GROUP BY medium_int,SYSKEY
HAVING medium_int in (999,1000,2000)
order by medium_int, syskey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 2)
    
    stmt = """select [any 2] PIC_X_B from """ + gvars.g_schema_arkcasedb + """.btsel05 
where COL_1 = 'lowry'
group by PIC_X_B
order by PIC_X_B;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 2)
    
    stmt = """select [any 2] * from """ + gvars.g_schema_arkcasedb + """.btsel06 
where Col_6 < 90
order by pIc_X_a,cOL_1, pic_x_b, pic_x_c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 2)
    
    #  test use of space between > and = in the >= sign
    
    stmt = """select [any 2] pic_1,large_int
from """ + gvars.g_schema_arkcasedb + """.btsel08 
where large_int >= 100
group by pic_1,large_int
having large_int in (100,200,1000,2000)
order by pic_1, large_int;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 2)
    
    stmt = """select [any 2] pic_x_5 from """ + gvars.g_schema_arkcasedb + """.btsel09 where pic_x_6 <> 11
group by pic_x_5 order by pic_x_5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 2)
    
    stmt = """select [any 2] decimal_10 from """ + gvars.g_schema_arkcasedb + """.btsel10 
group by decimal_10
having decimal_10 in
( 90,100,110,10000,50000)
order by decimal_10;"""
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
    #  Test case name:     arkt1374 : A08
    #  Original Test case: arkt0010 : A08
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
    
    stmt = """select [any 1] binary_64_s,count(*)
from """ + gvars.g_schema_arkcasedb + """.btsel01 
group by binary_64_s
order by binary_64_s;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    _dci.expect_selected_msg(output, 1)
    
    stmt = """select [any 1] avg(large_int)
from """ + gvars.g_schema_arkcasedb + """.pvsel01 
group by medium_int;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    
    stmt = """select [any 1] binary_64_s, pic_comp_1, min(ALL decimal_2_signed)
from """ + gvars.g_schema_arkcasedb + """.btsel01 
group by binary_64_s,pic_comp_1
order by binary_64_s,pic_comp_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    
    stmt = """select [any 1] new_name_2, sum(new_name_2)
from """ + gvars.g_schema_arkcasedb + """.pvsel03 
group by new_name_2
order by new_name_2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    
    stmt = """select [any 1] pic_comp_1,min(var_char)
from """ + gvars.g_schema_arkcasedb + """.svsel13 
group by pic_comp_1
order by pic_comp_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    
    #  select [any 1] DISTINCT
    
    stmt = """select [any 1] pic_comp_1,AVG(distinct binary_32_u)
from """ + gvars.g_schema_arkcasedb + """.btsel01 
group by pic_comp_1
order by pic_comp_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    
    stmt = """select [any 1] new_name_1,count(distinct var_char)
from """ + gvars.g_schema_arkcasedb + """.svsel13 
group by new_name_1
order by new_name_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    
    stmt = """select [any 1] binary_64_s, min(distinct var_char)
from """ + gvars.g_schema_arkcasedb + """.btsel01 
group by binary_64_s
order by binary_64_s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    
    #  select [any 1] an expression inside an aggregate
    
    stmt = """select [any 1] binary_64_s, avg(ALL binary_32_u + pic_comp_1)
from """ + gvars.g_schema_arkcasedb + """.btsel01 
group by binary_64_s
order by binary_64_s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    
    stmt = """select [any 1] medium_int, min(ALL large_int * small_int)
from """ + gvars.g_schema_arkcasedb + """.pvsel01 
group by medium_int
order by medium_int;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    
    stmt = """select [any 1] medium_int, min(ALL large_int * medium_int)
from """ + gvars.g_schema_arkcasedb + """.pvsel01 
group by medium_int
order by medium_int;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    
    #  select [any 1] an expression with SYSKEY in an aggregate
    
    stmt = """select [any 1] pic_x_7, max(SYSKEY / 3 + medium_int)
from """ + gvars.g_schema_arkcasedb + """.btsel04 
group by pic_x_7
order by pic_x_7;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    
    #  select [any 1] expression of aggregates
    
    stmt = """select [any 1] medium_int,(sum(pic_decimal_3) + sum(small_int)) / 100
from """ + gvars.g_schema_arkcasedb + """.pvsel01 
group by medium_int
order by medium_int;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    
    stmt = """select [any 1] medium_int,(sum(pic_decimal_3) + sum(medium_int)) / 100
from """ + gvars.g_schema_arkcasedb + """.pvsel01 
group by medium_int
order by medium_int;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    
    stmt = """select [any 1] pic_comp_1,avg(pic_comp_1 ) + sum(pic_comp_1)
from """ + gvars.g_schema_arkcasedb + """.svsel13 
group by pic_comp_1
order by pic_comp_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    
    stmt = """select [any 1] medium_int,sum(decimal_1) + sum(decimal_1)
from """ + gvars.g_schema_arkcasedb + """.btsel01 
group by medium_int
order by medium_int;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    
    stmt = """select [any 1] medium_int,
sum(pic_decimal_3),avg(pic_decimal_3),max(pic_decimal_3),
min(pic_decimal_3),count(distinct pic_decimal_3),count(*)
from """ + gvars.g_schema_arkcasedb + """.pvsel01 
group by medium_int
order by medium_int;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    
    #  queries with where predicates
    
    stmt = """select [any 1] binary_64_s, count(*)
from """ + gvars.g_schema_arkcasedb + """.btsel01 
where var_char = 'thomas'
group by binary_64_s
order by binary_64_s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    
    stmt = """select [any 1] pic_comp_1, SUM(distinct binary_64_s)
from """ + gvars.g_schema_arkcasedb + """.btsel01 
where binary_32_u > 50
group by pic_comp_1
order by pic_comp_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    
    stmt = """select [any 1] new_name_1, count(distinct var_char)
from """ + gvars.g_schema_arkcasedb + """.svsel13 
where (new_name_1 = 80) or (new_name_2 = 5)
group by new_name_1
order by new_name_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    
    stmt = """select [any 1] pic_comp_1, avg(ALL binary_32_u + pic_comp_1)
from """ + gvars.g_schema_arkcasedb + """.btsel01 
where (pic_comp_1 <> 60)
group by pic_comp_1
order by pic_comp_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    
    stmt = """select [any 1] binary_64_s, sum(decimal_1) + sum(decimal_1)
from """ + gvars.g_schema_arkcasedb + """.btsel01 
where decimal_3_unsigned <> 110
group by binary_64_s
order by binary_64_s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    
    stmt = """select [any 1] medium_int,avg(large_int)
from """ + gvars.g_schema_arkcasedb + """.pvsel01 
where small_int <> 8000
group by medium_int
order by medium_int;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    
    #  select [any 1] aggregate, group by SYSKEY
    
    stmt = """select [any 1] avg(pic_comp_1)
from """ + gvars.g_schema_arkcasedb + """.btsel04 
group by SYSKEY;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    
    _testmgr.testcase_end(desc)

def test009(desc="""a09"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt1374 : A09
    #  Original Test case: arkt0010 : A09
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
    
    stmt = """select [any 1] max(binary_32_u)
from """ + gvars.g_schema_arkcasedb + """.btsel01 
having sum(pic_decimal_3) > 30;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    _dci.expect_selected_msg(output, 1)
    
    stmt = """select [any 1] avg(pic_decimal_3)
from """ + gvars.g_schema_arkcasedb + """.btsel01 
having avg(pic_decimal_3) > 4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s1')
    
    stmt = """select [any 1] count(*)
from """ + gvars.g_schema_arkcasedb + """.pvsel01 
having min(small_int) <= 10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    
    stmt = """select [any 1] sum(col_4)
from """ + gvars.g_schema_arkcasedb + """.svsel11 
having count(*) = 8;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    _dci.expect_selected_msg(output, 0)
    
    # test select [any 1] from 0 groups
    
    stmt = """select [any 1] max(binary_64_s), min(binary_64_s)
from """ + gvars.g_schema_arkcasedb + """.btsel03 
group by pic_9_7
having pic_9_7 > 200;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """select [any 1] binary_64_s,count(*)
from """ + gvars.g_schema_arkcasedb + """.btsel01 
group by binary_64_s
having sum(distinct pic_comp_1) < 1000
order by binary_64_s;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    _dci.expect_selected_msg(output, 1)
    
    stmt = """select [any 1] binary_64_s,count(*)
from """ + gvars.g_schema_arkcasedb + """.btsel01 
group by binary_64_s
having binary_64_s <> 200
order by binary_64_s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    
    stmt = """select [any 1] binary_64_s,count(*)
from """ + gvars.g_schema_arkcasedb + """.btsel01 
group by binary_64_s
having sum(binary_64_s) > 2000
order by binary_64_s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    
    stmt = """select [any 1] binary_64_s
from """ + gvars.g_schema_arkcasedb + """.btsel01 
group by binary_64_s
having sum(binary_64_s) > 2000
order by binary_64_s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    
    stmt = """select [any 1] binary_64_s,count(*)
from """ + gvars.g_schema_arkcasedb + """.btsel01 
group by binary_64_s
having count(*) >= 2
order by binary_64_s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    
    stmt = """select [any 1] avg(large_int)
from """ + gvars.g_schema_arkcasedb + """.pvsel01 
group by medium_int
having sum(large_int) > 0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    #       order by medium_int;
    
    stmt = """select [any 1] binary_64_s, pic_comp_1, min(ALL decimal_2_signed)
from """ + gvars.g_schema_arkcasedb + """.btsel01 
group by binary_64_s, pic_comp_1
having max(binary_32_u) >= 50
order by binary_64_s, pic_comp_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    
    stmt = """select [any 1] new_name_2, sum(new_name_2)
from """ + gvars.g_schema_arkcasedb + """.pvsel03 
group by new_name_2
having (sum(new_name_1) + min(new_name_1)) * 2 > 400
order by new_name_2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    
    stmt = """select [any 1] pic_comp_1, min(var_char)
from """ + gvars.g_schema_arkcasedb + """.svsel13 
group by pic_comp_1
having min(new_name_1) + min(new_name_2) <> 86
order by pic_comp_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    
    stmt = """select [any 1] pic_comp_1, AVG(distinct binary_32_u)
from """ + gvars.g_schema_arkcasedb + """.btsel01 
group by pic_comp_1
having avg(pic_comp_2) < 0.5
order by pic_comp_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    
    stmt = """select [any 1] new_name_1
from """ + gvars.g_schema_arkcasedb + """.svsel13 
group by new_name_1
having sum(new_name_2) in (5,18)
order by new_name_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    
    stmt = """select [any 1] binary_64_s, avg(ALL binary_32_u + pic_comp_1)
from """ + gvars.g_schema_arkcasedb + """.btsel01 
group by binary_64_s
having avg(ALL binary_32_u + pic_comp_1) > 100
order by binary_64_s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    
    stmt = """select [any 1] binary_64_s
from """ + gvars.g_schema_arkcasedb + """.btsel01 
group by binary_64_s
having avg(ALL binary_32_u + pic_comp_1) > 100
order by binary_64_s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    
    #  queries with where predicates
    
    stmt = """select [any 1] pic_comp_1, SUM(distinct binary_64_s)
from """ + gvars.g_schema_arkcasedb + """.btsel01 
where binary_32_u > 50
group by pic_comp_1
having sum(binary_signed) > 5000
order by pic_comp_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    
    stmt = """select [any 1] new_name_1, count(distinct var_char)
from """ + gvars.g_schema_arkcasedb + """.svsel13 
where (new_name_1 = 80) or (new_name_2 = 5)
group by new_name_1
having avg(new_name_2) in (5,6)
order by new_name_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    
    stmt = """select [any 1] pic_comp_1, avg(ALL binary_32_u + pic_comp_1)
from """ + gvars.g_schema_arkcasedb + """.btsel01 
where (pic_comp_1 <> 60)
group by pic_comp_1
having min(binary_signed) < 1000
order by pic_comp_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    
    stmt = """select [any 1] binary_64_s, sum(decimal_1) + sum(decimal_1)
from """ + gvars.g_schema_arkcasedb + """.btsel01 
where decimal_3_unsigned <> 110
group by binary_64_s
having (max(pic_comp_2) between 0.2 and 0.99)
and (binary_64_s <> 1200)
order by binary_64_s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    
    stmt = """select [any 1] medium_int, avg(large_int)
from """ + gvars.g_schema_arkcasedb + """.pvsel01 
where small_int <> 8000
group by medium_int
having not max(pic_x_1) = 'E'
order by medium_int;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    
    #  complex queries
    
    stmt = """select [any 1] pic_comp_1, SUM(distinct binary_64_s)
from """ + gvars.g_schema_arkcasedb + """.btsel01 
where binary_32_u > 50
group by pic_comp_1
having sum(binary_signed) > 5000
order by pic_comp_1, 2
for serializable access;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    
    stmt = """select [any 1] new_name_1, count(distinct var_char)
from """ + gvars.g_schema_arkcasedb + """.svsel13 
where (new_name_1 = 80) or (new_name_2 = 5)
group by new_name_1
having avg(new_name_2) in (5,6)
order by 1, 2 ASC
for read committed access;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    
    stmt = """select [any 1] pic_comp_1, avg(ALL binary_32_u + pic_comp_1)
from """ + gvars.g_schema_arkcasedb + """.btsel01 
where (pic_comp_1 <> 60)
group by pic_comp_1
having min(binary_signed) < 1000
order by pic_comp_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    
    stmt = """select [any 1] binary_64_s, sum(decimal_1) + sum(decimal_1), pic_comp_2
from """ + gvars.g_schema_arkcasedb + """.btsel01 
where decimal_3_unsigned <> 110
group by binary_64_s, pic_comp_2
having pic_comp_2 between 0.2 and 0.99
order by 2, binary_64_s, pic_comp_2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    
    stmt = """select [any 1] medium_int, avg(large_int)
from """ + gvars.g_schema_arkcasedb + """.pvsel01 
where small_int <> 8000
group by medium_int
having not max(pic_x_1) = 'E'
order by medium_int
for read uncommitted access;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    
    #  select [any 1] having aggregate(SYSKEY)
    
    stmt = """select [any 1] pic_comp_1
from """ + gvars.g_schema_arkcasedb + """.btsel04 
group by pic_comp_1
having avg(SYSKEY) > 0
order by pic_comp_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    
    _testmgr.testcase_end(desc)

def test010(desc="""a10"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt1374 : A10
    #  Original Test case: arkt0010 : A10
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
    
    stmt = """select [any 1] char_1,decimal_1 from """ + gvars.g_schema_arkcasedb + """.btsel01 
group by  char_1,decimal_1
order by  1,2;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    _dci.expect_selected_msg(output, 1)
    
    stmt = """select [any 1] pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
group by pic_x_1
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    
    stmt = """select [any 1] pic_x_7,pic_9_7 from """ + gvars.g_schema_arkcasedb + """.btsel03 
group by pic_9_7, pic_x_7
order by 2,1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    
    stmt = """select [any 1] pic_x_a,col_1,col_3 from """ + gvars.g_schema_arkcasedb + """.btsel06 
group by pic_x_a, col_1, col_1, col_3
order by 1, 2, 3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    
    stmt = """select [any 1] pic_x_a,col_1,col_3 from """ + gvars.g_schema_arkcasedb + """.btsel06 
group by pic_x_a, col_1, col_3, col_1
order by 1, 2, 3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    
    stmt = """select [any 1] a , b from
(SELECT medium_int * 2, binary_64_s + 100
from """ + gvars.g_schema_arkcasedb + """.btsel01) dt(a,b)
group by a,b
order by 1,2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    
    stmt = """select [any 1] dt.a, dt.b from
(SELECT medium_int * 2, binary_64_s
from """ + gvars.g_schema_arkcasedb + """.btsel01) dt(a,b)
group by a, b
order by 1, 2   ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    
    stmt = """select [any 1] a,b  from
(SELECT sum(medium_int), sum(pic_comp_1)
from """ + gvars.g_schema_arkcasedb + """.btsel01) tab(a,b)
group by a,b
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    
    stmt = """select [any 1] x, y from
(SELECT medium_int , binary_64_s
from """ + gvars.g_schema_arkcasedb + """.btsel01) dt(x,y)
group by x,y
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    
    stmt = """select [any 1] dt.x, dt.y from
(SELECT avg(medium_int * binary_64_s), sum(medium_int * binary_64_s)
from """ + gvars.g_schema_arkcasedb + """.btsel01) dt (x , y)
group by x,y
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    
    stmt = """select [any 1] x, y from
(SELECT medium_int * binary_64_s, medium_int
from """ + gvars.g_schema_arkcasedb + """.btsel01) tab (x,y)
group by x,y
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    
    _testmgr.testcase_end(desc)

def test011(desc="""a11"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt1374 : A11
    #  Original Test case: arkt0010 : A11
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
    
    stmt = """select [any 3] * from svsel20 
order by medium_int, aggr_exp;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """drop view svsel20;"""
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
    #  Test case name:     arkt1374 : A12
    #  Original Test case: arkt0010 : A12
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
    
    stmt = """create table ptiletab (a largeint not null,
b pic s9(6)v9(3) default -999999.999 not null) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create view ptilevw as
select b from ptiletab ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into ptiletab values (6,5.806);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into ptiletab values (6,5.805);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into ptiletab values (6,4.807);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into ptiletab values (6,3.807);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into ptiletab values (5,37.681);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into ptiletab values (2,6.254);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # - Positive tests
    
    stmt = """select [any 6] b, ptile (b,50) from ptiletab group by b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    stmt = """select [any 6] b, ptile (b,90) from ptiletab group by b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    stmt = """select [any 6] a,b,ptile (b,10) from ptiletab group by a,b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    stmt = """select [any 6] b, ptile (b,50) from ptilevw group by b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    stmt = """select [any 6] b, ptile (b,90) from ptilevw group by b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    # - Negative tests
    stmt = """select [any 6] b, ptile (b,0) from ptiletab group by b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    stmt = """select [any 6] b, ptile (b,-10) from ptiletab group by b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    stmt = """select [any 6] a,b,ptile (b,100) from ptiletab group by a,b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    stmt = """select [any 6] b, ptile (b,0) from ptilevw group by b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    stmt = """select [any 6] b, ptile (b,-10) from ptilevw group by b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    stmt = """select [any 6] b, ptile (b,100) from ptilevw group by b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    stmt = """DROP view ptilevw;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """DROP table ptiletab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

