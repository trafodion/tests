# @@@ START COPYRIGHT @@@
#
# (C) Copyright 2014-2015 Hewlett-Packard Development Company, L.P.
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
    #  Test case name:     arkt0149 : A01
    #  Description:        This test verifies the SQL OUTER JOIN
    #                      statements
    #                      Simple JOIN of base tables.
    #                      Includes:
    #                      All major data types.
    #                      Column names the same.
    #                      Columns of same-length either side of JOIN.
    #                      Numbers of columns vary.
    #                      Some nonunique data values.
    #                      No NULL values.
    #                      Correlation names.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    # ---------------------------------
    # Set up default catalog and schema
    # ---------------------------------
    
    #   INNER JOIN of same-length CHAR:
    
    stmt = """select char_1 from """ + gvars.g_schema_arkcasedb + """.btsel01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s0')
    
    stmt = """select char_1 from """ + gvars.g_schema_arkcasedb + """.btre204;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s1')
    
    stmt = """select """ + gvars.g_schema_arkcasedb + """.btsel01.char_1, """ + gvars.g_schema_arkcasedb + """.btre204.char_1
from       """ + gvars.g_schema_arkcasedb + """.btsel01 
inner join """ + gvars.g_schema_arkcasedb + """.btre204 
on """ + gvars.g_schema_arkcasedb + """.btsel01.char_1 = """ + gvars.g_schema_arkcasedb + """.btre204.char_1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s2')
    
    stmt = """select """ + gvars.g_schema_arkcasedb + """.btsel01.char_1, """ + gvars.g_schema_arkcasedb + """.btre204.char_1
from       """ + gvars.g_schema_arkcasedb + """.btre204 
inner join """ + gvars.g_schema_arkcasedb + """.btsel01 
on """ + gvars.g_schema_arkcasedb + """.btsel01.char_1 = """ + gvars.g_schema_arkcasedb + """.btre204.char_1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s3')
    
    #   INNER JOIN of same-length CHAR, with correlation names:
    # 04/10/09 added order by
    stmt = """select a.char_1 from """ + gvars.g_schema_arkcasedb + """.btsel01 a ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s4')
    
    stmt = """select b.char_1 from """ + gvars.g_schema_arkcasedb + """.btre204 b ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s5')
    
    stmt = """select a.char_1, b.char_1
from       """ + gvars.g_schema_arkcasedb + """.btsel01 a
inner join """ + gvars.g_schema_arkcasedb + """.btre204 b
on a.char_1 = b.char_1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s6')
    
    stmt = """select a.char_1, b.char_1
from       """ + gvars.g_schema_arkcasedb + """.btre204 a
inner join """ + gvars.g_schema_arkcasedb + """.btsel01 b
on a.char_1 = b.char_1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s7')
    
    #   LEFT JOIN of same-length CHAR, with correlation names:
    stmt = """select a.char_1 from """ + gvars.g_schema_arkcasedb + """.btsel01 a ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s8')
    
    stmt = """select b.char_1 from """ + gvars.g_schema_arkcasedb + """.btre204 b ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s9')
    
    stmt = """select a.char_1, b.char_1
from      """ + gvars.g_schema_arkcasedb + """.btsel01 a
left join """ + gvars.g_schema_arkcasedb + """.btre204 b
on a.char_1 = b.char_1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s10')
    
    #   LEFT, RIGHT JOIN of same-length CHAR, with correlation names:
    stmt = """select a.char_1 from """ + gvars.g_schema_arkcasedb + """.btsel01 a ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s11')
    
    stmt = """select b.char_1 from """ + gvars.g_schema_arkcasedb + """.btre204 b ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s12')
    
    stmt = """select a.char_1, b.char_1
from       """ + gvars.g_schema_arkcasedb + """.btsel01 a
left  join """ + gvars.g_schema_arkcasedb + """.btre204 b
on a.char_1 = b.char_1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s13')
    
    stmt = """select a.char_1, b.char_1
from       """ + gvars.g_schema_arkcasedb + """.btre204 b
left join  """ + gvars.g_schema_arkcasedb + """.btsel01 a
on a.char_1 = b.char_1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s14')
    
    #   LEFT JOIN of same-length VARCHAR:
    stmt = """select """ + gvars.g_schema_arkcasedb + """.btre204.var_char_3 from """ + gvars.g_schema_arkcasedb + """.btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s15')
    
    stmt = """select """ + gvars.g_schema_arkcasedb + """.btre201.var_char_3 from """ + gvars.g_schema_arkcasedb + """.btre201 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s16')
    
    stmt = """select """ + gvars.g_schema_arkcasedb + """.btre204.var_char_3, """ + gvars.g_schema_arkcasedb + """.btre201.var_char_3
from """ + gvars.g_schema_arkcasedb + """.btre204 left  join """ + gvars.g_schema_arkcasedb + """.btre201 
on """ + gvars.g_schema_arkcasedb + """.btre204.var_char_3 = """ + gvars.g_schema_arkcasedb + """.btre201.var_char_3 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s17')
    
    #   LEFT  JOIN of same-length integer:
    # 04/10/09 added order by
    stmt = """select """ + gvars.g_schema_arkcasedb + """.btsel01.small_int from """ + gvars.g_schema_arkcasedb + """.btsel01 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s18')
    
    stmt = """select """ + gvars.g_schema_arkcasedb + """.btre202.small_int from """ + gvars.g_schema_arkcasedb + """.btre202 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s19')
    
    stmt = """select """ + gvars.g_schema_arkcasedb + """.btsel01.small_int, """ + gvars.g_schema_arkcasedb + """.btre202.small_int
from       """ + gvars.g_schema_arkcasedb + """.btsel01 
left  join """ + gvars.g_schema_arkcasedb + """.btre202 
on """ + gvars.g_schema_arkcasedb + """.btsel01.small_int = """ + gvars.g_schema_arkcasedb + """.btre202.small_int ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s20')
    
    #   LEFT JOIN of exact numerics with same precision and scale:
    stmt = """select """ + gvars.g_schema_arkcasedb + """.btre204.pic_decimal_2
from """ + gvars.g_schema_arkcasedb + """.btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s21')
    
    stmt = """select """ + gvars.g_schema_arkcasedb + """.btre208.pic_decimal_2
from """ + gvars.g_schema_arkcasedb + """.btre208 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s22')
    
    stmt = """select """ + gvars.g_schema_arkcasedb + """.btre204.pic_decimal_2,
 """ + gvars.g_schema_arkcasedb + """.btre208.pic_decimal_2
from       """ + gvars.g_schema_arkcasedb + """.btre204 
left  join """ + gvars.g_schema_arkcasedb + """.btre208 
on """ + gvars.g_schema_arkcasedb + """.btre204.pic_decimal_2 =
 """ + gvars.g_schema_arkcasedb + """.btre208.pic_decimal_2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s23')
    
    #   LEFT JOIN of DATETIME with same startdate and same enddate:
    stmt = """select """ + gvars.g_schema_arkcasedb + """.btre204.y_to_d
from      """ + gvars.g_schema_arkcasedb + """.btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s24')
    
    stmt = """select """ + gvars.g_schema_arkcasedb + """.btre208.y_to_d
from """ + gvars.g_schema_arkcasedb + """.btre208 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s25')
    
    stmt = """select """ + gvars.g_schema_arkcasedb + """.btre204.y_to_d, """ + gvars.g_schema_arkcasedb + """.btre208.y_to_d
from      """ + gvars.g_schema_arkcasedb + """.btre204 
left join """ + gvars.g_schema_arkcasedb + """.btre208 
on """ + gvars.g_schema_arkcasedb + """.btre204.y_to_d = """ + gvars.g_schema_arkcasedb + """.btre208.y_to_d ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s26')
    
    #   LEFT  JOIN of INTERVAL with same startdate and same enddate:
    stmt = """select """ + gvars.g_schema_arkcasedb + """.btre204.ih_to_s
from       """ + gvars.g_schema_arkcasedb + """.btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s27')
    
    stmt = """select  """ + gvars.g_schema_arkcasedb + """.btre208.ih_to_s
from       """ + gvars.g_schema_arkcasedb + """.btre208 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s28')
    
    stmt = """select """ + gvars.g_schema_arkcasedb + """.btre204.ih_to_s, """ + gvars.g_schema_arkcasedb + """.btre208.ih_to_s
from       """ + gvars.g_schema_arkcasedb + """.btre204 
left  join """ + gvars.g_schema_arkcasedb + """.btre208 
on """ + gvars.g_schema_arkcasedb + """.btre204.ih_to_s = """ + gvars.g_schema_arkcasedb + """.btre208.ih_to_s ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s29')
    
    #   LEFT  JOIN of two pairs of approximate numeric (FLOAT) with
    #   same precision and scale:
    stmt = """select """ + gvars.g_schema_arkcasedb + """.btre204.float_basic
from """ + gvars.g_schema_arkcasedb + """.btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s30')
    
    stmt = """select """ + gvars.g_schema_arkcasedb + """.btre208.float_double_p
from """ + gvars.g_schema_arkcasedb + """.btre208 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s31')
    
    stmt = """select a.float_basic, b.float_basic
from       """ + gvars.g_schema_arkcasedb + """.btre204 a
left  join """ + gvars.g_schema_arkcasedb + """.btre204 b
on a.float_basic = b.float_basic ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s32')
    
    stmt = """select a.float_double_p, b.float_double_p
from       """ + gvars.g_schema_arkcasedb + """.btre208 a
, """ + gvars.g_schema_arkcasedb + """.btre208 b
where a.float_double_p = b.float_double_p ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s33')
    
    #   RIGHT JOIN support dropped for R2.
    #   RIGHT, LEFT, INNER JOINs of a table with itself; also cross
    #   product:
    
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.btsel27 a ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s34')
    
    stmt = """select * from  """ + gvars.g_schema_arkcasedb + """.btsel27 b ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s35')
    
    stmt = """select * from  """ + gvars.g_schema_arkcasedb + """.btsel27 a
left  join """ + gvars.g_schema_arkcasedb + """.btsel27 b
on a.selector = b.selector
order by 1, 4 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s36')
    
    stmt = """select * from  """ + gvars.g_schema_arkcasedb + """.btsel27 a
inner join """ + gvars.g_schema_arkcasedb + """.btsel27 b
on a.selector = b.selector
order by 1, 4 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s37')
    
    stmt = """select * from  """ + gvars.g_schema_arkcasedb + """.btsel27 b
inner join """ + gvars.g_schema_arkcasedb + """.btsel27 a
on a.selector = b.selector
order by 1, 4 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s38')
    
    #   For R2, right join fails - will work for R3
    stmt = """select * from  """ + gvars.g_schema_arkcasedb + """.btsel27 a
right join """ + gvars.g_schema_arkcasedb + """.btsel27 b
on a.selector = b.selector
order by 1, 4 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s39')
    
    #   Cross product.
    stmt = """select * from  """ + gvars.g_schema_arkcasedb + """.btsel27 a ,
 """ + gvars.g_schema_arkcasedb + """.btsel27 b
order by 1, 4 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s40')
    
    _testmgr.testcase_end(desc)

def test002(desc="""a02"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0149 : A02
    #  Description:        This test verifies the SQL OUTER JOIN
    #                      statements
    #                      JOIN columns of differing lengths, with NULLs.
    #                      Includes:
    #                           Column names differ.
    #                           Columns of differing lengths either side of JOIN.
    #                           HEADING (Release 2 extension) on columns.
    #                           NULLs on left-side, right-side,
    #                              both sides of JOIN.
    #
    #                      Also includes other SELECT keywords -
    #                              GROUP BY (which causes intermediate results);
    #                              ORDER BY;
    #                              lock consistency;
    #                              lock mode.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    
    #   LEFT JOIN of CHARs; NULLs in left-side table;
    #   left-side of JOIN longer than right-side; column names differ:
    stmt = """select """ + gvars.g_schema_arkcasedb + """.btre204.pic_x_8 from """ + gvars.g_schema_arkcasedb + """.btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s0')
    
    stmt = """select  """ + gvars.g_schema_arkcasedb + """.btsel01.char_1 from """ + gvars.g_schema_arkcasedb + """.btsel01 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s1')
    
    stmt = """select """ + gvars.g_schema_arkcasedb + """.btre204.pic_x_8, """ + gvars.g_schema_arkcasedb + """.btsel01.char_1
from       """ + gvars.g_schema_arkcasedb + """.btre204 
left  join """ + gvars.g_schema_arkcasedb + """.btsel01 
on """ + gvars.g_schema_arkcasedb + """.btre204.pic_x_8 <> """ + gvars.g_schema_arkcasedb + """.btsel01.char_1
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s2')
    
    stmt = """select """ + gvars.g_schema_arkcasedb + """.btre204.pic_x_8, """ + gvars.g_schema_arkcasedb + """.btsel01.char_1
from       """ + gvars.g_schema_arkcasedb + """.btre204 
left  join """ + gvars.g_schema_arkcasedb + """.btsel01 
on """ + gvars.g_schema_arkcasedb + """.btre204.pic_x_8 is null
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s3')
    
    stmt = """select """ + gvars.g_schema_arkcasedb + """.btre204.pic_x_8, """ + gvars.g_schema_arkcasedb + """.btsel01.char_1
from       """ + gvars.g_schema_arkcasedb + """.btre204 
left  join """ + gvars.g_schema_arkcasedb + """.btsel01 
on """ + gvars.g_schema_arkcasedb + """.btsel01.char_1 is null
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s4')
    
    stmt = """select """ + gvars.g_schema_arkcasedb + """.btre204.pic_x_8, """ + gvars.g_schema_arkcasedb + """.btsel01.char_1
from       """ + gvars.g_schema_arkcasedb + """.btre204 
left  join """ + gvars.g_schema_arkcasedb + """.btsel01 
on """ + gvars.g_schema_arkcasedb + """.btre204.pic_x_8 <> """ + gvars.g_schema_arkcasedb + """.btsel01.char_1
and """ + gvars.g_schema_arkcasedb + """.btre204.pic_x_8 is null
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s5')
    
    stmt = """select """ + gvars.g_schema_arkcasedb + """.btre204.pic_x_8, """ + gvars.g_schema_arkcasedb + """.btsel01.char_1
from       """ + gvars.g_schema_arkcasedb + """.btre204 
left  join """ + gvars.g_schema_arkcasedb + """.btsel01 
on """ + gvars.g_schema_arkcasedb + """.btre204.pic_x_8 <> """ + gvars.g_schema_arkcasedb + """.btsel01.char_1
and """ + gvars.g_schema_arkcasedb + """.btsel01.char_1 is null
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s6')
    
    #   LEFT JOIN of different-length VARCHAR:
    stmt = """select a.var_char_2
from       """ + gvars.g_schema_arkcasedb + """.btre201 a ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s7')
    
    stmt = """select               b.var_char_3
from       """ + gvars.g_schema_arkcasedb + """.btre208 b ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s8')
    
    stmt = """select a.var_char_2, b.var_char_3
from       """ + gvars.g_schema_arkcasedb + """.btre201 a
left  join """ + gvars.g_schema_arkcasedb + """.btre208 b
on a.var_char_2 = b.var_char_3
order by a.var_char_2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s9')
    
    stmt = """select a.var_char_2, b.var_char_3
from       """ + gvars.g_schema_arkcasedb + """.btre201 a
left  join """ + gvars.g_schema_arkcasedb + """.btre208 b
on a.var_char_2 = b.var_char_3
and a.var_char_2 is null
order by a.var_char_2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s10')
    
    stmt = """select a.var_char_2, b.var_char_3
from       """ + gvars.g_schema_arkcasedb + """.btre201 a
left  join """ + gvars.g_schema_arkcasedb + """.btre208 b
on a.var_char_2 = b.var_char_3
and b.var_char_3 is null
order by a.var_char_2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s11')
    
    #   LEFT JOIN of different-length CHAR and VARCHAR:
    stmt = """select """ + gvars.g_schema_arkcasedb + """.btre204.var_char_2, """ + gvars.g_schema_arkcasedb + """.btre208.var_char_3
from       """ + gvars.g_schema_arkcasedb + """.btre204 
left  join """ + gvars.g_schema_arkcasedb + """.btre208 
on """ + gvars.g_schema_arkcasedb + """.btre204.var_char_2 = """ + gvars.g_schema_arkcasedb + """.btre208.var_char_3
order by """ + gvars.g_schema_arkcasedb + """.btre204.var_char_2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s12')
    
    #   LEFT  JOIN of two pairs of approximate numeric (FLOAT) with
    #   different precision and scale:
    stmt = """select """ + gvars.g_schema_arkcasedb + """.btre204.float_basic
from """ + gvars.g_schema_arkcasedb + """.btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s13')
    
    stmt = """select """ + gvars.g_schema_arkcasedb + """.btre208.float_double_p
from """ + gvars.g_schema_arkcasedb + """.btre208 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s14')
    
    stmt = """select """ + gvars.g_schema_arkcasedb + """.btre204.float_basic, """ + gvars.g_schema_arkcasedb + """.btre208.float_double_p
from       """ + gvars.g_schema_arkcasedb + """.btre204 
left  join """ + gvars.g_schema_arkcasedb + """.btre208 
on """ + gvars.g_schema_arkcasedb + """.btre204.float_basic = """ + gvars.g_schema_arkcasedb + """.btre208.float_double_p ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s15')
    
    stmt = """select """ + gvars.g_schema_arkcasedb + """.btre204.float_basic, """ + gvars.g_schema_arkcasedb + """.btre208.float_double_p
from       """ + gvars.g_schema_arkcasedb + """.btre204 
, """ + gvars.g_schema_arkcasedb + """.btre208 
where """ + gvars.g_schema_arkcasedb + """.btre204.float_basic = """ + gvars.g_schema_arkcasedb + """.btre208.float_double_p ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s16')
    
    #   LEFT  JOIN of CHARs; NULLs in right-side table;
    #   left-side of JOIN shorter than right-side; column names differ:
    stmt = """select """ + gvars.g_schema_arkcasedb + """.btsel01.char_1 from """ + gvars.g_schema_arkcasedb + """.btsel01 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s17')
    
    stmt = """select """ + gvars.g_schema_arkcasedb + """.btre204.pic_x_8 from """ + gvars.g_schema_arkcasedb + """.btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s18')
    
    stmt = """select """ + gvars.g_schema_arkcasedb + """.btsel01.char_1, """ + gvars.g_schema_arkcasedb + """.btre204.pic_x_8
from       """ + gvars.g_schema_arkcasedb + """.btsel01 
left  join """ + gvars.g_schema_arkcasedb + """.btre204 
on """ + gvars.g_schema_arkcasedb + """.btsel01.char_1 = """ + gvars.g_schema_arkcasedb + """.btre204.pic_x_8
order by 2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s19')
    
    #   LEFT JOIN of CHARs with no match:
    stmt = """select """ + gvars.g_schema_arkcasedb + """.btsel04.var_char from  """ + gvars.g_schema_arkcasedb + """.btsel04 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s20')
    
    stmt = """select """ + gvars.g_schema_arkcasedb + """.btre201.char_1 from  """ + gvars.g_schema_arkcasedb + """.btre201 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s21')
    
    stmt = """select """ + gvars.g_schema_arkcasedb + """.btsel04.var_char, """ + gvars.g_schema_arkcasedb + """.btre201.char_1
from       """ + gvars.g_schema_arkcasedb + """.btsel04 
left  join """ + gvars.g_schema_arkcasedb + """.btre201 
on """ + gvars.g_schema_arkcasedb + """.btsel04.var_char = """ + gvars.g_schema_arkcasedb + """.btre201.char_1
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s22')
    
    #   JOIN of CHARs with no match:
    #   (Correlation names used for RIGHT join to avoid error -4060 for
    #   R2.)
    
    stmt = """select a.var_char from  """ + gvars.g_schema_arkcasedb + """.btsel01 a ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s23')
    
    stmt = """select b.char_1 from  """ + gvars.g_schema_arkcasedb + """.btre201 b ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s24')
    
    stmt = """select a.var_char, b.char_1
from       """ + gvars.g_schema_arkcasedb + """.btre201 b
left join  """ + gvars.g_schema_arkcasedb + """.btsel01   a
on a.var_char = b.char_1
order by 1, 2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s25')
    
    stmt = """select a.var_char, b.char_1
from       """ + gvars.g_schema_arkcasedb + """.btre201 b
right join  """ + gvars.g_schema_arkcasedb + """.btsel01   a
on a.var_char = b.char_1
order by 1, 2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s26')
    
    #   NULLs on both sides; LEFT & RIGHT JOIN of SMALLINT and INTEGER:
    # 04/10/09 added order by for following queries
    stmt = """select """ + gvars.g_schema_arkcasedb + """.btre201.small_int from """ + gvars.g_schema_arkcasedb + """.btre201 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s27')
    
    stmt = """select """ + gvars.g_schema_arkcasedb + """.btre202.medium_int from """ + gvars.g_schema_arkcasedb + """.btre202 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s28')
    
    stmt = """select """ + gvars.g_schema_arkcasedb + """.btre201.small_int, """ + gvars.g_schema_arkcasedb + """.btre202.medium_int
from       """ + gvars.g_schema_arkcasedb + """.btre201 
left  join """ + gvars.g_schema_arkcasedb + """.btre202 
on """ + gvars.g_schema_arkcasedb + """.btre201.small_int = """ + gvars.g_schema_arkcasedb + """.btre202.medium_int
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s29')
    
    #   (Correlation names used here to avoid error -4060 for R2.)
    stmt = """select       a.small_int,       b.medium_int
from       """ + gvars.g_schema_arkcasedb + """.btre202 b
left join  """ + gvars.g_schema_arkcasedb + """.btre201 a
on a.small_int = b.medium_int order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s30')
    
    stmt = """select       a.small_int,       b.medium_int
from       """ + gvars.g_schema_arkcasedb + """.btre202 b
left join  """ + gvars.g_schema_arkcasedb + """.btre201 a
on a.small_int = b.medium_int
and a.small_int is null
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s31')
    
    stmt = """select       a.small_int,       b.medium_int
from       """ + gvars.g_schema_arkcasedb + """.btre202 b
left join  """ + gvars.g_schema_arkcasedb + """.btre201 a
on a.small_int = b.medium_int
and ( b.medium_int is null )
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s32')
    
    #   UNION of LEFT & RIGHT JOIN gives in effect the OUTER JOIN:
    #   For R2, test with Left joins:
    stmt = """select """ + gvars.g_schema_arkcasedb + """.btre201.small_int, """ + gvars.g_schema_arkcasedb + """.btre202.medium_int
from       """ + gvars.g_schema_arkcasedb + """.btre201 
left  join """ + gvars.g_schema_arkcasedb + """.btre202 
on """ + gvars.g_schema_arkcasedb + """.btre201.small_int = """ + gvars.g_schema_arkcasedb + """.btre202.medium_int ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s33')
    
    stmt = """select """ + gvars.g_schema_arkcasedb + """.btre201.small_int, """ + gvars.g_schema_arkcasedb + """.btre202.medium_int
from       """ + gvars.g_schema_arkcasedb + """.btre201 
left join  """ + gvars.g_schema_arkcasedb + """.btre202 
on """ + gvars.g_schema_arkcasedb + """.btre201.small_int = """ + gvars.g_schema_arkcasedb + """.btre202.medium_int
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s34')
    
    stmt = """select """ + gvars.g_schema_arkcasedb + """.btre201.small_int, """ + gvars.g_schema_arkcasedb + """.btre202.medium_int
from       """ + gvars.g_schema_arkcasedb + """.btre201 
left  join """ + gvars.g_schema_arkcasedb + """.btre202 
on """ + gvars.g_schema_arkcasedb + """.btre201.small_int = """ + gvars.g_schema_arkcasedb + """.btre202.medium_int
union
select """ + gvars.g_schema_arkcasedb + """.btre201.small_int, """ + gvars.g_schema_arkcasedb + """.btre202.medium_int
from       """ + gvars.g_schema_arkcasedb + """.btre201 
left join  """ + gvars.g_schema_arkcasedb + """.btre202 
on """ + gvars.g_schema_arkcasedb + """.btre201.small_int = """ + gvars.g_schema_arkcasedb + """.btre202.medium_int
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s35')
    
    stmt = """select """ + gvars.g_schema_arkcasedb + """.btre201.small_int, """ + gvars.g_schema_arkcasedb + """.btre202.medium_int
from       """ + gvars.g_schema_arkcasedb + """.btre201 
left  join """ + gvars.g_schema_arkcasedb + """.btre202 
on """ + gvars.g_schema_arkcasedb + """.btre201.small_int = """ + gvars.g_schema_arkcasedb + """.btre202.medium_int
union
select       a.small_int,       b.medium_int
from       """ + gvars.g_schema_arkcasedb + """.btre202 b
right join """ + gvars.g_schema_arkcasedb + """.btre201 a
on        a.small_int =      b.medium_int
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s36')
    
    #  LEFT and RIGHT JOIN of left-side empty table with right-side
    #  nonempty table:
    stmt = """select """ + gvars.g_schema_arkcasedb + """.btemprel.some_data, """ + gvars.g_schema_arkcasedb + """.btsel20.data_93
from       """ + gvars.g_schema_arkcasedb + """.btemprel 
left  join """ + gvars.g_schema_arkcasedb + """.btsel20 
on """ + gvars.g_schema_arkcasedb + """.btemprel.some_data = """ + gvars.g_schema_arkcasedb + """.btsel20.data_93
order by 2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    #   (Correlation names used here to avoid error -4060 for R2.)
    stmt = """select        a.data_93,         b.some_data
from       """ + gvars.g_schema_arkcasedb + """.btempkey b
right join  """ + gvars.g_schema_arkcasedb + """.btsel20  a
on         a.data_93  =       b.some_data
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s37')
    
    stmt = """select        a.data_93,         b.some_data
from       """ + gvars.g_schema_arkcasedb + """.btempkey b
right join  """ + gvars.g_schema_arkcasedb + """.btsel20  a
on         a.data_93  =       b.some_data
and (   a.data_93  is null )
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s38')
    
    stmt = """select        a.data_93,         b.some_data
from       """ + gvars.g_schema_arkcasedb + """.btempkey b
right join  """ + gvars.g_schema_arkcasedb + """.btsel20  a
on         a.data_93  =       b.some_data
and (   b.some_data is null )
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s39')
    
    #  LEFT and RIGHT JOIN of left-side nonempty table with right-side
    #  empty table:
    #  (Correlation names used here to avoid error -4060 for R2.)
    stmt = """select        a.some_data,       b.data_93
from       """ + gvars.g_schema_arkcasedb + """.btsel20  b
right join """ + gvars.g_schema_arkcasedb + """.btemprel a
on         a.some_data =      b.data_93
order by 2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """select """ + gvars.g_schema_arkcasedb + """.btsel20.data_93 , """ + gvars.g_schema_arkcasedb + """.btempkey.some_data
from       """ + gvars.g_schema_arkcasedb + """.btsel20 
left  join """ + gvars.g_schema_arkcasedb + """.btempkey 
on """ + gvars.g_schema_arkcasedb + """.btsel20.data_93 = """ + gvars.g_schema_arkcasedb + """.btempkey.some_data
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s40')
    
    #  LEFT & RIGHT JOIN of empty tables on both sides:
    stmt = """select """ + gvars.g_schema_arkcasedb + """.btempkey.some_data, """ + gvars.g_schema_arkcasedb + """.btempent.some_data
from       """ + gvars.g_schema_arkcasedb + """.btempent 
left  join """ + gvars.g_schema_arkcasedb + """.btempkey 
on """ + gvars.g_schema_arkcasedb + """.btempkey.some_data = """ + gvars.g_schema_arkcasedb + """.btempent.some_data ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    #  (Correlation names used here to avoid error -4060 for R2.)
    stmt = """select        b.some_data,        a.some_data
from       """ + gvars.g_schema_arkcasedb + """.btempkey b
right join """ + gvars.g_schema_arkcasedb + """.btempent a
on        a.some_data =        b.some_data ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """select """ + gvars.g_schema_arkcasedb + """.btempkey.some_data, """ + gvars.g_schema_arkcasedb + """.btempent.some_data
from       """ + gvars.g_schema_arkcasedb + """.btempent 
left  join """ + gvars.g_schema_arkcasedb + """.btempkey 
on """ + gvars.g_schema_arkcasedb + """.btempkey.some_data = """ + gvars.g_schema_arkcasedb + """.btempent.some_data
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    _testmgr.testcase_end(desc)

def test003(desc="""a03"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """create table  a3table1 
(
SUPPNUM                        PIC 9(3)   NOT NULL
, SUPPNAME                       PIC X(18)   NOT NULL
, ADDRESS                        PIC X(22)   NOT NULL
, CITY                           PIC X(14)   NOT NULL
, STATE                          PIC X(12)   NOT NULL
, primary key (suppnum)
)
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table  a3table2 
(
SUPPNUM                        PIC 9(3)   NOT NULL
, SUPPNAME                       PIC X(18)   NOT NULL
, ADDRESS                        PIC X(22)   NOT NULL
, CITY                           PIC X(14)   NOT NULL
, STATE                          PIC X(12)   NOT NULL
, primary key (suppnum)
)
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table  a3table3 (
suppnum  pic 999
, suppname pic x(18)
, address  pic x(22)
, city     pic x(14)
, state    pic x(12)
)  no partition
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table  a3table4 
(
suppnum  pic 999
, suppname pic x(18)
, address  pic x(22)
, city     pic x(14)
, state    pic x(12)
) no partition
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table  a3table5 
(   suppnum  pic 999
, suppname pic x(18)
, address  pic x(22)
, city     pic x(14)
, state    pic x(12)
) no partition
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table  a3table6 
( suppnum  pic 999
, suppname pic x(18)
, address  pic x(22)
, city     pic x(14)
, state    pic x(12)
) no partition
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table  a3table7 
( suppnum  pic 999
, suppname pic x(18)
, address  pic x(22)
, city     pic x(14)
, state    pic x(12)
) no partition
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table  a3table8 
( suppnum  pic 999
, suppname pic x(18)
, address  pic x(22)
, city     pic x(14)
, state    pic x(12)
) no partition
;"""
    output = _dci.cmdexec(stmt)
    
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0149 : A03
    #  Description:        This test verifies the SQL OUTER JOIN
    #                      statements
    #                      JOIN in subquery, INSERT, other SQLCI contexts.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    #
    
    #  Populate tables to be used:
    
    #  Query 1
    stmt = """insert into a3table1 
select * from """ + gvars.g_schema_arkcasedb + """.supplier 
where suppnum <= 10 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 6)
    
    #   Query 2
    stmt = """select * from a3table1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s0')
    
    #  Query 3
    stmt = """insert into a3table2 
select * from """ + gvars.g_schema_arkcasedb + """.supplier 
where suppnum >= 10 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 2)
    
    #   Query 4
    # 04/10/09 added order by
    stmt = """select * from a3table2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s1')
    
    #   Query 5
    #   Insert using LEFT JOIN in a select:
    stmt = """select a3table1.suppnum, a3table1.suppname
, a3table2.address
, a3table2.city   , a3table2.state
from       a3table1 
left  join a3table2 
on a3table1.suppnum = a3table2.suppnum
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s2')
    
    #  Query 6
    stmt = """insert into a3table3 
select a3table1.suppnum, a3table1.suppname
, a3table2.address
, a3table2.city   , a3table2.state
from       a3table1 
left  join a3table2 
on a3table1.suppnum = a3table2.suppnum
--       order by 1 ;
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 6)
    
    #   Query 7
    stmt = """select * from a3table3 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s3')
    
    #   Query 8
    #   Insert using RIGHT JOIN in a select:
    #   (For R2, changed to LEFT JOIN, as RIGHT JOIN is not supported;
    #   (use of correlation names avoids error -4060 for R2.)
    stmt = """select        a.suppnum,        a.suppname
,        b.address
,        b.city   ,        b.state
from       a3table2 b
left join  a3table1 a
on        a.suppnum =        b.suppnum
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s4')
    
    #  Query 9
    stmt = """insert into a3table4 
select        a.suppnum,        a.suppname
,        b.address
,        b.city   ,        b.state
from       a3table2 b
left join  a3table1 a
on        a.suppnum =        b.suppnum
--       order by 1 ;
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 2)
    
    #   Query 10
    stmt = """select * from a3table4 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s5')
    
    #   Query 11
    #   Insert using INNER JOIN in a select:
    stmt = """select        a.suppnum,        a.suppname
,        b.address
,        b.city   ,        b.state
from        a3table2 b
inner join  a3table1 a
on        a.suppnum =        b.suppnum
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s6')
    
    #  Query 12
    stmt = """insert into a3table5 
select        a.suppnum,        a.suppname
,        b.address
,        b.city   ,        b.state
from        a3table2 b
inner join  a3table1 a
on        a.suppnum =        b.suppnum
--       order by 1 ;
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    #   Query 13
    stmt = """select * from a3table5 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s7')
    
    #   Insert using UNION of LEFT JOINs (see far below!).
    
    #   Query 14
    #   The two simple selects:
    stmt = """select a3table1.suppnum, a3table1.suppname
from       a3table1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s8')
    
    stmt = """select a3table2.address , a3table2.city , a3table2.state
from       a3table2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s9')
    
    #   Query 15
    #   The two JOINs:
    stmt = """select a3table1.suppnum, a3table1.suppname
, a3table2.address
, a3table2.city   , a3table2.state
from       a3table2 
left  join a3table1 
on a3table1.suppnum = a3table2.suppnum
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s10')
    
    #   Query 16
    stmt = """select a3table1.suppnum, a3table1.suppname
, a3table2.address
, a3table2.city   , a3table2.state
from       a3table1 
left  join a3table2 
on a3table1.suppnum = a3table2.suppnum
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s11')
    
    #   Query 17
    #   The UNION:
    stmt = """select a3table1.suppnum, a3table1.suppname
, a3table2.address
, a3table2.city   , a3table2.state
from       a3table2 
left  join a3table1 
on a3table1.suppnum = a3table2.suppnum
union
select a3table1.suppnum, a3table1.suppname
, a3table2.address
, a3table2.city   , a3table2.state
from       a3table1 
left  join a3table2 
on a3table1.suppnum = a3table2.suppnum
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s12')
    
    #  Query 18
    #  The insert using UNION of LEFT JOINs:
    stmt = """insert into a3table6     

select a3table1.suppnum, a3table1.suppname
, a3table2.address
, a3table2.city   , a3table2.state
from       a3table2 
left  join a3table1 
on a3table1.suppnum = a3table2.suppnum
union
select a3table1.suppnum, a3table1.suppname
, a3table2.address
, a3table2.city   , a3table2.state
from       a3table1 
left  join a3table2 
on a3table1.suppnum = a3table2.suppnum
--       order by 1 ;
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 7)
    
    #   Query 19
    stmt = """select * from a3table6 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s13')
    
    #   Insert using UNION of LEFT and INNER JOIN (see far below!):
    
    #   Query 20
    #   The two simple selects:
    # 04/10/09 added order by
    stmt = """select a3table1.suppnum, a3table1.suppname
from       a3table1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s14')
    
    stmt = """select a3table2.address , a3table2.city , a3table2.state
from       a3table2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s15')
    
    #   Query 21
    #   The two JOINs:
    
    stmt = """select        a.suppnum,        a.suppname
,        b.address
,        b.city   ,        b.state
from       a3table1 a
left  join a3table2 b
on        a.suppnum =        b.suppnum
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s16')
    
    #   Query 22
    stmt = """select a3table1.suppnum, a3table1.suppname
, a3table2.address
, a3table2.city   , a3table2.state
from        a3table2 
inner join  a3table1 
on a3table1.suppnum = a3table2.suppnum
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s17')
    
    #   Query 23
    #   The UNION:
    
    stmt = """select        a.suppnum,        a.suppname
,        b.address
,        b.city   ,        b.state
from       a3table1 a
left  join a3table2 b
on        a.suppnum =        b.suppnum    

union    

select a3table1.suppnum, a3table1.suppname
, a3table2.address
, a3table2.city   , a3table2.state
from        a3table2 
inner join  a3table1 
on a3table1.suppnum = a3table2.suppnum    

order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s18')
    
    #  Query 24
    #  Insert using UNION of LEFT and INNER JOIN:
    
    stmt = """insert into a3table7 
select        a.suppnum,        a.suppname
,        b.address
,        b.city   ,        b.state
from       a3table1 a
left  join a3table2 b
on        a.suppnum =        b.suppnum    

union    

select a3table1.suppnum, a3table1.suppname
, a3table2.address
, a3table2.city   , a3table2.state
from        a3table2 
inner join  a3table1 
on a3table1.suppnum = a3table2.suppnum    

--       order by 1 ;
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 6)
    stmt = """select * from a3table7 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s19')
    
    #   Insert using UNION of LEFT and RIGHT JOIN - FAILS for R2:
    
    #   Query 25
    #   The two simple selects:
    # 04/10/09 added order by
    stmt = """select a3table1.suppnum, a3table1.suppname
from       a3table1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s20')
    
    stmt = """select a3table2.address , a3table2.city , a3table2.state
from       a3table2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s21')
    
    #   Query 26
    #   The two JOINs:
    stmt = """select        a.suppnum,        a.suppname
,        b.address
,        b.city   ,        b.state
from       a3table1 a
right join a3table2 b
on        a.suppnum =        b.suppnum
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s22')
    
    #   Query 27
    stmt = """select a3table1.suppnum, a3table1.suppname
, a3table2.address
, a3table2.city   , a3table2.state
from        a3table2 
left  join  a3table1 
on a3table1.suppnum = a3table2.suppnum
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s23')
    
    #   Query 28
    #   The UNION:
    #   (Correlation names used here to avoid error -4060 for R2.)
    stmt = """select        a.suppnum,        a.suppname
,        b.address
,        b.city   ,        b.state
from       a3table1 a
right join a3table2 b
on        a.suppnum =        b.suppnum    

union    

select a3table1.suppnum, a3table1.suppname
, a3table2.address
, a3table2.city   , a3table2.state
from        a3table2 
left  join  a3table1 
on a3table1.suppnum = a3table2.suppnum    

order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s24')
    
    #  Query 29
    #  Insert using UNION of LEFT and RIGHT JOIN:
    stmt = """insert into a3table8     

select        a.suppnum,        a.suppname
,        b.address
,        b.city   ,        b.state
from       a3table1 a
right join a3table2 b
on        a.suppnum =        b.suppnum    

union    

select a3table1.suppnum, a3table1.suppname
, a3table2.address
, a3table2.city   , a3table2.state
from        a3table2 
left  join  a3table1 
on a3table1.suppnum = a3table2.suppnum
--       order by 1 ;
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 2)
    
    #   Query 30
    stmt = """select * from a3table8 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s25')
    stmt = """drop table  a3table1;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """drop table  a3table2;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """drop table  a3table3;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """drop table  a3table4;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """drop table  a3table5;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """drop table  a3table6 ;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """drop table  a3table7;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """drop table  a3table8 ;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test004(desc="""a05"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    #  drop tables first in case left over from previous run.
    stmt = """drop table  a5table1 ;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table  a5table2 ;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table  a5table3 ;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table  a5table4;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table  a5table5;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table  a5table6;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table  a5table7;"""
    output = _dci.cmdexec(stmt)
    
    #  Create tables to be used:
    stmt = """create table  a5table1 
(
SUPPNUM                        PIC 9(3)   NOT NULL
, SUPPNAME                       PIC X(18)   NOT NULL
, ADDRESS                        PIC X(22)   NOT NULL
, CITY                           PIC X(14)   NOT NULL
, STATE                          PIC X(12)   NOT NULL
, primary key (suppnum)
)
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table  a5table2 
(
SUPPNUM                        PIC 9(3)   NOT NULL
, SUPPNAME                       PIC X(18)   NOT NULL
, ADDRESS                        PIC X(22)   NOT NULL
, CITY                           PIC X(14)   NOT NULL
, STATE                          PIC X(12)   NOT NULL
, primary key (suppnum)
)
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table  a5table3 (
suppnum  pic 999
, suppname pic x(18)
, address  pic x(22)
, city     pic x(14)
, state    pic x(12)
)  no partition
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table  a5table4 
(   suppnum  pic 999
, suppname pic x(18)
, address  pic x(22)
, city     pic x(14)
, state    pic x(12)
)  no partition
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table  a5table5 
(   suppnum  pic 999
, suppname pic x(18)
, address  pic x(22)
, city     pic x(14)
, state    pic x(12)
)  no partition
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table  a5table6 
(   suppnum  pic 999
, suppname pic x(18)
, address  pic x(22)
, city     pic x(14)
, state    pic x(12)
)  no partition
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table  a5table7 
(   suppnum  pic 999
, suppname pic x(18)
, address  pic x(22)
, city     pic x(14)
, state    pic x(12)
)  no partition
;"""
    output = _dci.cmdexec(stmt)
    
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0149 : A05
    #  Description:        This test verifies the SQL OUTER JOIN
    #                      statements
    #                      JOIN in subquery.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    #
    
    #  Populate tables to be used:
    stmt = """insert into a5table1 
select * from """ + gvars.g_schema_arkcasedb + """.supplier 
where suppnum < 10 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 5)
    
    stmt = """select * from a5table1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s0')
    stmt = """insert into a5table2 
select * from """ + gvars.g_schema_arkcasedb + """.supplier 
where suppnum >= 8 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 3)
    
    stmt = """select * from a5table2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s1')
    stmt = """insert into a5table3 
select * from """ + gvars.g_schema_arkcasedb + """.supplier ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 7)
    
    stmt = """select * from a5table3 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s2')
    stmt = """insert into a5table4 
select * from """ + gvars.g_schema_arkcasedb + """.supplier ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 7)
    
    stmt = """select * from a5table4 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s3')
    stmt = """insert into a5table5 
select * from """ + gvars.g_schema_arkcasedb + """.supplier ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 7)
    
    stmt = """select * from a5table5 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s4')
    
    #   JOIN in uncorrelated subquery in WHERE clause.
    #   List supplier info for which the left join of supplier has
    #   same city (only DALLAS):
    stmt = """select a5table1.city
from a5table1 
left join a5table2 
on a5table1.city = a5table2.city ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s5')
    
    stmt = """select city from """ + gvars.g_schema_arkcasedb + """.supplier 
where city = ANY (
select a5table1.city
from a5table1 left join a5table2 
on a5table1.city = a5table2.city
)
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s6')
    
    #   List supplier info for which the inner join of supplier has
    #   same city (only DALLAS):
    stmt = """select a5table1.city from a5table1 inner join a5table2 
on a5table1.city = a5table2.city ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s7')
    
    stmt = """select city from """ + gvars.g_schema_arkcasedb + """.supplier 
where city = ANY (
select a5table1.city
from a5table1 inner join a5table2 
on a5table1.city = a5table2.city
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s8')
    
    #   JOIN in uncorrelated subquery in HAVING clause.
    #   (Should get same result as above).
    stmt = """select city from """ + gvars.g_schema_arkcasedb + """.supplier 
group by city
having city = ANY (
select a5table1.city
from a5table1 left join a5table2 
on a5table1.city = a5table2.city
)
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s9')
    
    #   JOIN in an IN predicate.
    # 04/10/09 added order by
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.supplier 
where city IN (
select a5table1.city
from a5table1 left join a5table2 
on a5table1.city = a5table2.city
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s10')
    
    #   JOIN in a quantified predicate -
    #      a subquery 'quantified' by ALL => use in DELETE.
    stmt = """select * from a5table1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s11')
    stmt = """select * from a5table4 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s12')
    stmt = """select *
from a5table1 left join a5table4 
on a5table1.suppnum = a5table4.suppnum
where a5table1.suppnum = 3 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s13')
    
    stmt = """delete from a5table3 
where suppnum = ALL (
select a5table1.suppnum
from a5table1 left join a5table4 
on a5table1.suppnum = a5table4.suppnum
where a5table1.suppnum = 3
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    stmt = """select * from a5table3 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s14')
    
    #   JOIN in a quantified predicate -
    #      a subquery 'quantified' by ANY => use in UPDATE.
    # 04/10/09 added order by for following queries
    stmt = """select * from a5table1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s15')
    stmt = """select * from a5table4 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s16')
    stmt = """select * from a5table5 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s17')
    
    stmt = """select a5table1.suppnum
from a5table1 left join a5table4 
on a5table1.suppnum = a5table4.suppnum ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s18')
    
    stmt = """update a5table5 set address = 'New Address'
where suppnum = ANY (
select a5table1.suppnum
from a5table1 left join a5table4 
on a5table1.suppnum = a5table4.suppnum
where a5table1.suppnum = 6
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select * from a5table5 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s19')
    
    #   JOIN in a quantified predicate -
    #      a subquery 'quantified' by SOME.
    stmt = """select * from a5table1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s20')
    stmt = """select * from a5table2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s21')
    stmt = """select * from a5table2 
where suppnum = SOME (
select a5table1.suppnum
from a5table1 left join a5table2 
on a5table1.city    = a5table2.city
where a5table2.suppnum = 8
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s22')
    
    #   JOIN in a subquery with the existential quantifier EXISTS.
    stmt = """select * from a5table1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s23')
    stmt = """select * from a5table4 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s24')
    stmt = """select a5table1.suppnum, a5table4.suppnum
from a5table1 left join a5table4 
on a5table1.suppnum = a5table4.suppnum
where a5table1.suppnum = 8 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s25')
    
    stmt = """select * from a5table1 
where EXISTS (
select a5table1.suppnum
from a5table1 left join a5table4 
on a5table1.suppnum = a5table4.suppnum
where a5table1.suppnum = 8
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s26')
    
    stmt = """select * from a5table4 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s27')
    
    stmt = """select a5table1.suppnum, a5table4.suppnum
from a5table1, a5table4 
where a5table1.suppnum = a5table4.suppnum
and   a5table1.suppnum = 8 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s28')
    
    stmt = """select * from a5table1 
where EXISTS (
select a5table1.suppnum
from a5table1, a5table4 
where a5table1.suppnum = a5table4.suppnum
and   a5table1.suppnum = 8
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s29')
    
    #  Create tables to be used:
    stmt = """drop table  a5table1 ;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table  a5table2 ;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table  a5table3 ;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table  a5table4;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table  a5table5;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table  a5table6;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table  a5table7;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test005(desc="""a06"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0149 : A06
    #  Description:        This test verifies the SQL OUTER JOIN
    #                      statements
    #                      JOIN with constants and expressions.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    #
    
    #   JOIN with literals - expect 3 full records; the rest with nulls:
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.parts 
left join """ + gvars.g_schema_arkcasedb + """.odetail 
on """ + gvars.g_schema_arkcasedb + """.parts.partnum = """ + gvars.g_schema_arkcasedb + """.odetail.partnum and quantity > 20 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s0')
    
    stmt = """select 'a', quantity
from """ + gvars.g_schema_arkcasedb + """.parts 
left join """ + gvars.g_schema_arkcasedb + """.odetail 
on """ + gvars.g_schema_arkcasedb + """.parts.partnum = """ + gvars.g_schema_arkcasedb + """.odetail.partnum and quantity > 20
order by 2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s1')
    
    stmt = """select 'a' from """ + gvars.g_schema_arkcasedb + """.parts 
left join """ + gvars.g_schema_arkcasedb + """.odetail 
on """ + gvars.g_schema_arkcasedb + """.parts.partnum = """ + gvars.g_schema_arkcasedb + """.odetail.partnum and quantity > 20 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s2')
    
    #   JOIN with literals:
    stmt = """select """ + gvars.g_schema_arkcasedb + """.btsel04.var_char from """ + gvars.g_schema_arkcasedb + """.btsel04 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s3')
    
    stmt = """select """ + gvars.g_schema_arkcasedb + """.btre201.char_1 from """ + gvars.g_schema_arkcasedb + """.btre201 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s4')
    
    stmt = """select """ + gvars.g_schema_arkcasedb + """.btsel04.var_char, 'first literal'
, """ + gvars.g_schema_arkcasedb + """.btre201.char_1, 'second literal'
from       """ + gvars.g_schema_arkcasedb + """.btsel04 
left  join """ + gvars.g_schema_arkcasedb + """.btre201 
on """ + gvars.g_schema_arkcasedb + """.btsel04.var_char = """ + gvars.g_schema_arkcasedb + """.btre201.char_1
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s5')
    
    #   JOIN with inequality expressions in ON clause:
    #   >=, etc
    # 04/10/09 added order by for following queries
    stmt = """select """ + gvars.g_schema_arkcasedb + """.btsel13.data_93 from """ + gvars.g_schema_arkcasedb + """.btsel13 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s6')
    
    stmt = """select """ + gvars.g_schema_arkcasedb + """.btsel14.data_93 from """ + gvars.g_schema_arkcasedb + """.btsel14 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s7')
    
    stmt = """select """ + gvars.g_schema_arkcasedb + """.btsel13.data_93 , """ + gvars.g_schema_arkcasedb + """.btsel14.data_93
, """ + gvars.g_schema_arkcasedb + """.btsel13.data_93 + """ + gvars.g_schema_arkcasedb + """.btsel14.data_93
from """ + gvars.g_schema_arkcasedb + """.btsel13 
left join """ + gvars.g_schema_arkcasedb + """.btsel14 
on """ + gvars.g_schema_arkcasedb + """.btsel13.data_93 >= """ + gvars.g_schema_arkcasedb + """.btsel14.data_93
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s8')
    
    stmt = """select """ + gvars.g_schema_arkcasedb + """.btsel13.data_93 , """ + gvars.g_schema_arkcasedb + """.btsel14.data_93
, """ + gvars.g_schema_arkcasedb + """.btsel13.data_93 + """ + gvars.g_schema_arkcasedb + """.btsel14.data_93
from """ + gvars.g_schema_arkcasedb + """.btsel13 
left join """ + gvars.g_schema_arkcasedb + """.btsel14 
on """ + gvars.g_schema_arkcasedb + """.btsel13.data_93 <  """ + gvars.g_schema_arkcasedb + """.btsel14.data_93
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s9')
    
    _testmgr.testcase_end(desc)

def test006(desc="""a07"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0149 : A07
    #  Description:        This test verifies the SQL OUTER JOIN
    #                      statements
    #                      JOINs of MANY columns or tables.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    
    #   Show base tables:
    
    #  Query 1
    stmt = """select a.binary_signed , a.char_1 , a.char_10
, a.pic_comp_1    , a.small_int
from      """ + gvars.g_schema_arkcasedb + """.btsel01 a ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s0')
    
    #  Query 2
    stmt = """select b.ordering
, b.char_1 ,     b.pic_x_8 ,  b.binary_signed
, b.pic_comp_1 , b.small_int
from      """ + gvars.g_schema_arkcasedb + """.btre201 b ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s1')
    
    #  Query 3
    stmt = """select a.binary_signed , a.char_1 , a.char_10
, b.ordering      , b.char_1 , b.pic_x_8
from      """ + gvars.g_schema_arkcasedb + """.btsel01 a
,         """ + gvars.g_schema_arkcasedb + """.btre201 b
where a.char_1        = b.char_1
or a.char_10       = b.pic_x_8
or a.binary_signed = b.binary_signed
or a.pic_comp_1    = b.pic_comp_1
or a.small_int     = b.small_int ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s2')
    
    #  Query 4
    #   JOIN with some columns from global database:
    stmt = """select a.binary_signed , a.char_1 , a.char_10
, b.ordering      , b.char_1 , b.pic_x_8
from      """ + gvars.g_schema_arkcasedb + """.btsel01 a
left join """ + gvars.g_schema_arkcasedb + """.btre201 b
on  a.char_1        = b.char_1
and a.char_10       = b.pic_x_8
and a.binary_signed = b.binary_signed
and a.pic_comp_1    = b.pic_comp_1
and a.small_int     = b.small_int ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s3')
    
    #  Query 5
    #   JOIN with more columns from global database:
    stmt = """select a.pic_x_1 , a.binary_signed , a.binary_32_u
, a.binary_64_s
from      """ + gvars.g_schema_arkcasedb + """.btsel01 a ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s4')
    
    #  Query 6
    stmt = """select b.ordering , b.var_char_2 , b.binary_signed , b.binary_32_u
, b.binary_64_s
from      """ + gvars.g_schema_arkcasedb + """.btre201 b ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s5')
    
    #  Query 7
    stmt = """select a.binary_signed , b.ordering
from      """ + gvars.g_schema_arkcasedb + """.btsel01 a
,         """ + gvars.g_schema_arkcasedb + """.btre201 b
where a.binary_signed = b.binary_signed
or a.binary_32_u   = b.binary_32_u
or a.binary_64_s   = b.binary_64_s ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s6')
    
    #  Query 8
    stmt = """select a.binary_signed , b.ordering
from      """ + gvars.g_schema_arkcasedb + """.btsel01 a
left join """ + gvars.g_schema_arkcasedb + """.btre201 b
on  a.binary_signed = b.binary_signed
and a.binary_32_u   = b.binary_32_u
and a.binary_64_s   = b.binary_64_s ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s7')
    
    #  Query 9
    stmt = """select a.binary_signed , a.pic_comp_1 , a.pic_comp_2 , a.pic_comp_3
from      """ + gvars.g_schema_arkcasedb + """.btsel01 a ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s8')
    
    #  Query 10
    stmt = """select b.ordering , b.pic_comp_1 , b.pic_comp_2 , b.pic_comp_3
from      """ + gvars.g_schema_arkcasedb + """.btre201 b ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s9')
    
    #  Query 11
    stmt = """select a.binary_signed , b.ordering
from      """ + gvars.g_schema_arkcasedb + """.btsel01 a
,         """ + gvars.g_schema_arkcasedb + """.btre201 b
where a.pic_comp_1    = b.pic_comp_1
or a.pic_comp_2    = b.pic_comp_2
or a.pic_comp_3    = b.pic_comp_3 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s10')
    
    #  Query 12
    stmt = """select a.binary_signed , b.ordering
from      """ + gvars.g_schema_arkcasedb + """.btsel01 a
left join """ + gvars.g_schema_arkcasedb + """.btre201 b
on  a.pic_comp_1    = b.pic_comp_1
and a.pic_comp_2    = b.pic_comp_2
and a.pic_comp_3    = b.pic_comp_3 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s11')
    
    #  Query 13
    stmt = """select a.binary_signed , a.small_int , a.medium_int , a.large_int
from      """ + gvars.g_schema_arkcasedb + """.btsel01 a ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s12')
    
    #  Query 14
    stmt = """select b.ordering , b.small_int , b.medium_int , b.large_int
from      """ + gvars.g_schema_arkcasedb + """.btre201 b ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s13')
    
    #  Query 15
    stmt = """select a.binary_signed , b.ordering
from      """ + gvars.g_schema_arkcasedb + """.btsel01 a
left join """ + gvars.g_schema_arkcasedb + """.btre201 b
on  a.small_int     = b.small_int
and a.medium_int    = b.medium_int
and a.large_int     = b.large_int ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s14')
    
    #  Query 16
    stmt = """select a.binary_signed , b.ordering
from      """ + gvars.g_schema_arkcasedb + """.btsel01 a
,         """ + gvars.g_schema_arkcasedb + """.btre201 b
where a.small_int     = b.small_int
or a.medium_int    = b.medium_int
or a.large_int     = b.large_int ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s15')
    
    #  Query 17
    stmt = """select a.binary_signed
, a.decimal_1 , a.decimal_2_signed
, a.decimal_3_unsigned , a.pic_decimal_1
, a.pic_decimal_2 , a.pic_decimal_3
from      """ + gvars.g_schema_arkcasedb + """.btsel01 a ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s16')
    
    #  Query 18
    stmt = """select b.ordering
, b.decimal_1 , b.decimal_2_signed
, b.decimal_3_unsigned , b.pic_decimal_1
, b.pic_decimal_2 , b.pic_decimal_3
from      """ + gvars.g_schema_arkcasedb + """.btre201 b ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s17')
    
    #  Query 19
    stmt = """select a.binary_signed , b.ordering
from      """ + gvars.g_schema_arkcasedb + """.btsel01 a
,         """ + gvars.g_schema_arkcasedb + """.btre201 b
where a.decimal_1     = b.decimal_1
or a.decimal_2_signed   = b.decimal_2_signed
or a.decimal_3_unsigned = b.decimal_3_unsigned
or a.pic_decimal_1 = b.pic_decimal_1
or a.pic_decimal_2 = b.pic_decimal_2
or a.pic_decimal_3 = b.pic_decimal_3 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s18')
    
    #  Query 20
    stmt = """select a.binary_signed , b.ordering
from      """ + gvars.g_schema_arkcasedb + """.btsel01 a
left join """ + gvars.g_schema_arkcasedb + """.btre201 b
on  a.decimal_1     = b.decimal_1
and a.decimal_2_signed   = b.decimal_2_signed
and a.decimal_3_unsigned = b.decimal_3_unsigned
and a.pic_decimal_1 = b.pic_decimal_1
and a.pic_decimal_2 = b.pic_decimal_2
and a.pic_decimal_3 = b.pic_decimal_3 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s19')
    
    #  Query 21
    stmt = """select a.binary_signed , b.ordering
from      """ + gvars.g_schema_arkcasedb + """.btsel01 a
left join """ + gvars.g_schema_arkcasedb + """.btre201 b
on  a.char_1        = b.char_1
and a.char_10       = b.pic_x_8
and a.pic_x_1       = b.var_char_2
and a.binary_signed = b.binary_signed
and a.binary_32_u   = b.binary_32_u
and a.binary_64_s   = b.binary_64_s
and a.pic_comp_1    = b.pic_comp_1
and a.pic_comp_2    = b.pic_comp_2
and a.pic_comp_3    = b.pic_comp_3
and a.small_int     = b.small_int
and a.medium_int    = b.medium_int
and a.large_int     = b.large_int
and a.decimal_1     = b.decimal_1
and a.decimal_2_signed   = b.decimal_2_signed
and a.decimal_3_unsigned = b.decimal_3_unsigned
and a.pic_decimal_1 = b.pic_decimal_1
and a.pic_decimal_2 = b.pic_decimal_2
and a.pic_decimal_3 = b.pic_decimal_3 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s20')
    
    #  -- Query 22
    stmt = """select a.binary_signed , b.ordering
from      """ + gvars.g_schema_arkcasedb + """.btsel01 a
left join """ + gvars.g_schema_arkcasedb + """.btre201 b
on a.char_1        = b.char_1
or a.char_10       = b.pic_x_8
or a.pic_x_1       = b.var_char_2
or a.binary_signed = b.binary_signed
or a.binary_32_u   = b.binary_32_u
or a.binary_64_s   = b.binary_64_s
or a.pic_comp_1    = b.pic_comp_1
or a.pic_comp_2    = b.pic_comp_2
or a.pic_comp_3    = b.pic_comp_3
or a.small_int     = b.small_int
or a.medium_int    = b.medium_int
or a.large_int     = b.large_int
or a.decimal_1     = b.decimal_1
or a.decimal_2_signed   = b.decimal_2_signed
or a.decimal_3_unsigned = b.decimal_3_unsigned
or a.pic_decimal_1 = b.pic_decimal_1
or a.pic_decimal_2 = b.pic_decimal_2
or a.pic_decimal_3 = b.pic_decimal_3 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s21')
    
    # -- Query 23
    # --  Attempt to JOIN 16 table (see n1 for
    # --  17 (i.e., one over the limit) tables):
    
    # XXXXX  THIS IS TEMPORARY until the OPTIMIZER is fixed
    stmt = """control query default OPTIMIZATION_LEVEL '0';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select """ + gvars.g_schema_arkcasedb + """.btsel12.data_x3
, """ + gvars.g_schema_arkcasedb + """.btsel12.data_93
, """ + gvars.g_schema_arkcasedb + """.btsel15.small_int
, """ + gvars.g_schema_arkcasedb + """.btsel18.binary_signed
, """ + gvars.g_schema_arkcasedb + """.btsel23.pic_comp_2
from """ + gvars.g_schema_arkcasedb + """.btsel12 
join """ + gvars.g_schema_arkcasedb + """.btsel13 
on """ + gvars.g_schema_arkcasedb + """.btsel12.data_93       <> """ + gvars.g_schema_arkcasedb + """.btsel13.data_93
join """ + gvars.g_schema_arkcasedb + """.btsel14 
on  """ + gvars.g_schema_arkcasedb + """.btsel12.data_93       = """ + gvars.g_schema_arkcasedb + """.btsel14.data_93
join """ + gvars.g_schema_arkcasedb + """.btsel15 
on  """ + gvars.g_schema_arkcasedb + """.btsel12.data_93       = """ + gvars.g_schema_arkcasedb + """.btsel15.data_93
join """ + gvars.g_schema_arkcasedb + """.btsel16 
on  """ + gvars.g_schema_arkcasedb + """.btsel15.small_int     = """ + gvars.g_schema_arkcasedb + """.btsel16.small_int
join """ + gvars.g_schema_arkcasedb + """.btsel17 
on  """ + gvars.g_schema_arkcasedb + """.btsel15.small_int     = """ + gvars.g_schema_arkcasedb + """.btsel17.small_int
join """ + gvars.g_schema_arkcasedb + """.btsel18 
on  """ + gvars.g_schema_arkcasedb + """.btsel15.small_int     = """ + gvars.g_schema_arkcasedb + """.btsel18.small_int
join """ + gvars.g_schema_arkcasedb + """.btsel19 
on  """ + gvars.g_schema_arkcasedb + """.btsel18.binary_signed = """ + gvars.g_schema_arkcasedb + """.btsel19.binary_signed
join """ + gvars.g_schema_arkcasedb + """.btsel20 
on  """ + gvars.g_schema_arkcasedb + """.btsel18.binary_signed = """ + gvars.g_schema_arkcasedb + """.btsel20.binary_signed
join """ + gvars.g_schema_arkcasedb + """.btsel21 
on  """ + gvars.g_schema_arkcasedb + """.btsel18.binary_signed = """ + gvars.g_schema_arkcasedb + """.btsel21.binary_signed
join """ + gvars.g_schema_arkcasedb + """.btsel22 
on  """ + gvars.g_schema_arkcasedb + """.btsel21.pic_comp_2    = """ + gvars.g_schema_arkcasedb + """.btsel22.pic_comp_2
join """ + gvars.g_schema_arkcasedb + """.btsel23 
on  """ + gvars.g_schema_arkcasedb + """.btsel21.pic_comp_2    = """ + gvars.g_schema_arkcasedb + """.btsel23.pic_comp_2
join """ + gvars.g_schema_arkcasedb + """.btsel24 
on  """ + gvars.g_schema_arkcasedb + """.btsel21.pic_comp_2    = """ + gvars.g_schema_arkcasedb + """.btsel24.pic_comp_2
join """ + gvars.g_schema_arkcasedb + """.btsel16 a
on  """ + gvars.g_schema_arkcasedb + """.btsel15.small_int     =       a.small_int
join """ + gvars.g_schema_arkcasedb + """.btsel19 b
on  """ + gvars.g_schema_arkcasedb + """.btsel18.binary_signed =       b.binary_signed ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """control query default OPTIMIZATION_LEVEL reset;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #  Query 24
    stmt = """select data_x3 , data_93       from """ + gvars.g_schema_arkcasedb + """.btsel12 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s22')
    #  Query 25
    stmt = """select data_93       from """ + gvars.g_schema_arkcasedb + """.btsel13 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s23')
    #  Query 26
    stmt = """select data_93       from """ + gvars.g_schema_arkcasedb + """.btsel14 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s24')
    #  Query 27
    stmt = """select data_93       from """ + gvars.g_schema_arkcasedb + """.btsel15 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s25')
    #  Query 28
    stmt = """select small_int     from """ + gvars.g_schema_arkcasedb + """.btsel15 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s26')
    #  Query 29
    stmt = """select small_int     from """ + gvars.g_schema_arkcasedb + """.btsel16 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s27')
    #  Query 30
    stmt = """select small_int     from """ + gvars.g_schema_arkcasedb + """.btsel17 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s28')
    #  Query 31
    stmt = """select small_int     from """ + gvars.g_schema_arkcasedb + """.btsel18 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s29')
    #  Query 33
    stmt = """select binary_signed from """ + gvars.g_schema_arkcasedb + """.btsel18 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s30')
    #  Query 34
    stmt = """select binary_signed from """ + gvars.g_schema_arkcasedb + """.btsel19 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s31')
    #  Query 35
    stmt = """select binary_signed from """ + gvars.g_schema_arkcasedb + """.btsel20 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s32')
    #  Query 36
    stmt = """select binary_signed from """ + gvars.g_schema_arkcasedb + """.btsel21 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s33')
    #  Query 37
    stmt = """select pic_comp_2    from """ + gvars.g_schema_arkcasedb + """.btsel21 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s34')
    stmt = """select pic_comp_2    from """ + gvars.g_schema_arkcasedb + """.btsel22 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s35')
    #  Query 38
    stmt = """select pic_comp_2    from """ + gvars.g_schema_arkcasedb + """.btsel23 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s36')
    #  Query 39
    stmt = """select pic_comp_2    from """ + gvars.g_schema_arkcasedb + """.btsel24 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s37')
    
    # Query 40
    # XXXXX  THIS IS TEMPORARY until the OPTIMIZER is fixed
    stmt = """control query default OPTIMIZATION_LEVEL '0';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select """ + gvars.g_schema_arkcasedb + """.btsel12.data_x3
, """ + gvars.g_schema_arkcasedb + """.btsel12.data_93
, """ + gvars.g_schema_arkcasedb + """.btsel15.small_int
, """ + gvars.g_schema_arkcasedb + """.btsel18.binary_signed
, """ + gvars.g_schema_arkcasedb + """.btsel23.pic_comp_2
from      """ + gvars.g_schema_arkcasedb + """.btsel12 
left join """ + gvars.g_schema_arkcasedb + """.btsel13 
on """ + gvars.g_schema_arkcasedb + """.btsel12.data_93       <> """ + gvars.g_schema_arkcasedb + """.btsel13.data_93
left join """ + gvars.g_schema_arkcasedb + """.btsel14 
on  """ + gvars.g_schema_arkcasedb + """.btsel12.data_93       = """ + gvars.g_schema_arkcasedb + """.btsel14.data_93
left join """ + gvars.g_schema_arkcasedb + """.btsel15 
on  """ + gvars.g_schema_arkcasedb + """.btsel12.data_93       = """ + gvars.g_schema_arkcasedb + """.btsel15.data_93
left join """ + gvars.g_schema_arkcasedb + """.btsel16 
on  """ + gvars.g_schema_arkcasedb + """.btsel15.small_int     = """ + gvars.g_schema_arkcasedb + """.btsel16.small_int
left join """ + gvars.g_schema_arkcasedb + """.btsel17 
on  """ + gvars.g_schema_arkcasedb + """.btsel15.small_int     = """ + gvars.g_schema_arkcasedb + """.btsel17.small_int
left join """ + gvars.g_schema_arkcasedb + """.btsel18 
on  """ + gvars.g_schema_arkcasedb + """.btsel15.small_int     = """ + gvars.g_schema_arkcasedb + """.btsel18.small_int
left join """ + gvars.g_schema_arkcasedb + """.btsel19 
on  """ + gvars.g_schema_arkcasedb + """.btsel18.binary_signed = """ + gvars.g_schema_arkcasedb + """.btsel19.binary_signed
left join """ + gvars.g_schema_arkcasedb + """.btsel20 
on  """ + gvars.g_schema_arkcasedb + """.btsel18.binary_signed = """ + gvars.g_schema_arkcasedb + """.btsel20.binary_signed
left join """ + gvars.g_schema_arkcasedb + """.btsel21 
on  """ + gvars.g_schema_arkcasedb + """.btsel18.binary_signed = """ + gvars.g_schema_arkcasedb + """.btsel21.binary_signed
left join """ + gvars.g_schema_arkcasedb + """.btsel22 
on  """ + gvars.g_schema_arkcasedb + """.btsel21.pic_comp_2    = """ + gvars.g_schema_arkcasedb + """.btsel22.pic_comp_2
left join """ + gvars.g_schema_arkcasedb + """.btsel23 
on  """ + gvars.g_schema_arkcasedb + """.btsel21.pic_comp_2    = """ + gvars.g_schema_arkcasedb + """.btsel23.pic_comp_2
left join """ + gvars.g_schema_arkcasedb + """.btsel24 
on  """ + gvars.g_schema_arkcasedb + """.btsel21.pic_comp_2    = """ + gvars.g_schema_arkcasedb + """.btsel24.pic_comp_2
left join """ + gvars.g_schema_arkcasedb + """.btsel16 a
on  """ + gvars.g_schema_arkcasedb + """.btsel15.small_int     =       a.small_int
left join """ + gvars.g_schema_arkcasedb + """.btsel19 b
on  """ + gvars.g_schema_arkcasedb + """.btsel18.binary_signed =       b.binary_signed ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s38')
    
    stmt = """control query default OPTIMIZATION_LEVEL reset;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #  Query 41
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.btsel13 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s39')
    #  Query 42
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.btsel14 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s40')
    
    #  Query 43
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.btsel13 t1
left join """ + gvars.g_schema_arkcasedb + """.btsel14 t2
on t1.data_93 = t2.data_93
left join """ + gvars.g_schema_arkcasedb + """.btsel14 t3
on t2.data_93 = t3.data_93
left join """ + gvars.g_schema_arkcasedb + """.btsel14 t4
on t3.data_93 = t4.data_93
left join """ + gvars.g_schema_arkcasedb + """.btsel14 t5
on t4.data_93 = t5.data_93 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s41')
    
    #  Query 44
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.btsel13 t1
left join """ + gvars.g_schema_arkcasedb + """.btsel14 t2
on t1.data_93 = t2.data_93
left join """ + gvars.g_schema_arkcasedb + """.btsel14 t3
on t2.data_93 = t3.data_93
left join """ + gvars.g_schema_arkcasedb + """.btsel14 t4
on t3.data_93 = t4.data_93
left join """ + gvars.g_schema_arkcasedb + """.btsel14 t5
on t4.data_93 = t5.data_93
left join """ + gvars.g_schema_arkcasedb + """.btsel14 t6
on t5.data_93 = t6.data_93
left join """ + gvars.g_schema_arkcasedb + """.btsel14 t7
on t6.data_93 = t7.data_93
left join """ + gvars.g_schema_arkcasedb + """.btsel14 t8
on t7.data_93 = t8.data_93
left join """ + gvars.g_schema_arkcasedb + """.btsel14 t9
on t8.data_93 = t9.data_93 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s42')
    
    # Query 45
    # XXXXX  THIS IS TEMPORARY until the OPTIMIZER is fixed
    stmt = """control query default OPTIMIZATION_LEVEL '0';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.btsel13 t1
left join """ + gvars.g_schema_arkcasedb + """.btsel14 t2
on t1.data_93 = t2.data_93
left join """ + gvars.g_schema_arkcasedb + """.btsel14 t3
on t2.data_93 = t3.data_93
left join """ + gvars.g_schema_arkcasedb + """.btsel14 t4
on t3.data_93 = t4.data_93
left join """ + gvars.g_schema_arkcasedb + """.btsel14 t5
on t4.data_93 = t5.data_93
left join """ + gvars.g_schema_arkcasedb + """.btsel14 t6
on t5.data_93 = t6.data_93
left join """ + gvars.g_schema_arkcasedb + """.btsel14 t7
on t6.data_93 = t7.data_93
left join """ + gvars.g_schema_arkcasedb + """.btsel14 t8
on t7.data_93 = t8.data_93
left join """ + gvars.g_schema_arkcasedb + """.btsel14 t9
on t8.data_93 = t9.data_93
left join """ + gvars.g_schema_arkcasedb + """.btsel14 t10
on  t9.data_93 = t10.data_93
left join """ + gvars.g_schema_arkcasedb + """.btsel14 t11
on t10.data_93 = t11.data_93
left join """ + gvars.g_schema_arkcasedb + """.btsel14 t12
on t11.data_93 = t12.data_93
left join """ + gvars.g_schema_arkcasedb + """.btsel14 t13
on t12.data_93 = t13.data_93
left join """ + gvars.g_schema_arkcasedb + """.btsel14 t14
on t13.data_93 = t14.data_93
left join """ + gvars.g_schema_arkcasedb + """.btsel14 t15
on t14.data_93 = t15.data_93
left join """ + gvars.g_schema_arkcasedb + """.btsel14 t16
on t15.data_93 = t16.data_93 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s43')
    
    stmt = """control query default OPTIMIZATION_LEVEL reset;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test007(desc="""a08"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0149 : A08
    #  Description:        This test verifies the SQL OUTER JOIN
    #                      statements
    #                      Cartesian products.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    
    #   Select with value = constant
    
    stmt = """select """ + gvars.g_schema_arkcasedb + """.customer.city, """ + gvars.g_schema_arkcasedb + """.customer.state
from      """ + gvars.g_schema_arkcasedb + """.customer 
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s0')
    
    stmt = """select """ + gvars.g_schema_arkcasedb + """.supplier.city, """ + gvars.g_schema_arkcasedb + """.supplier.state
from      """ + gvars.g_schema_arkcasedb + """.supplier 
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s1')
    
    stmt = """select """ + gvars.g_schema_arkcasedb + """.customer.city, """ + gvars.g_schema_arkcasedb + """.customer.state
, """ + gvars.g_schema_arkcasedb + """.supplier.city, """ + gvars.g_schema_arkcasedb + """.supplier.state
from      """ + gvars.g_schema_arkcasedb + """.customer 
left join """ + gvars.g_schema_arkcasedb + """.supplier 
on """ + gvars.g_schema_arkcasedb + """.customer.city = 'SAN FRANCISCO'
order by 1, 3 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s2')
    
    stmt = """select """ + gvars.g_schema_arkcasedb + """.customer.city, """ + gvars.g_schema_arkcasedb + """.customer.state
, """ + gvars.g_schema_arkcasedb + """.supplier.city, """ + gvars.g_schema_arkcasedb + """.supplier.state
from      """ + gvars.g_schema_arkcasedb + """.customer 
left join """ + gvars.g_schema_arkcasedb + """.supplier 
on """ + gvars.g_schema_arkcasedb + """.customer.city = 'san francisco'
order by 1, 3 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s3')
    
    stmt = """select """ + gvars.g_schema_arkcasedb + """.customer.city, """ + gvars.g_schema_arkcasedb + """.customer.state
, """ + gvars.g_schema_arkcasedb + """.supplier.city, """ + gvars.g_schema_arkcasedb + """.supplier.state
from      """ + gvars.g_schema_arkcasedb + """.customer 
left join """ + gvars.g_schema_arkcasedb + """.supplier 
on """ + gvars.g_schema_arkcasedb + """.customer.city <> 'X'
order by 1, 3 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s4')
    
    stmt = """select """ + gvars.g_schema_arkcasedb + """.customer.city, """ + gvars.g_schema_arkcasedb + """.customer.state
, """ + gvars.g_schema_arkcasedb + """.supplier.city, """ + gvars.g_schema_arkcasedb + """.supplier.state
from      """ + gvars.g_schema_arkcasedb + """.customer 
left join """ + gvars.g_schema_arkcasedb + """.supplier 
on """ + gvars.g_schema_arkcasedb + """.customer.city <> 'SAN FRANCISCO'
order by 1, 3 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s5')
    
    #   Select with value = constant
    stmt = """select """ + gvars.g_schema_arkcasedb + """.customer.city, """ + gvars.g_schema_arkcasedb + """.customer.state
, """ + gvars.g_schema_arkcasedb + """.supplier.city, """ + gvars.g_schema_arkcasedb + """.supplier.state
from      """ + gvars.g_schema_arkcasedb + """.customer 
left join """ + gvars.g_schema_arkcasedb + """.supplier 
on """ + gvars.g_schema_arkcasedb + """.customer.city = 'SAN FRANCISCO'
or """ + gvars.g_schema_arkcasedb + """.customer.city <> 'SAN FRANCISCO'
order by 1, 3 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s6')
    
    #   Cartesian product (components first):
    stmt = """select """ + gvars.g_schema_arkcasedb + """.customer.city, """ + gvars.g_schema_arkcasedb + """.customer.state
, """ + gvars.g_schema_arkcasedb + """.supplier.city, """ + gvars.g_schema_arkcasedb + """.supplier.state
from           """ + gvars.g_schema_arkcasedb + """.customer 
left join """ + gvars.g_schema_arkcasedb + """.supplier 
on """ + gvars.g_schema_arkcasedb + """.customer.city = """ + gvars.g_schema_arkcasedb + """.supplier.city
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s7')
    
    stmt = """select """ + gvars.g_schema_arkcasedb + """.fromsup.suppnum, """ + gvars.g_schema_arkcasedb + """.fromsup.partnum , """ + gvars.g_schema_arkcasedb + """.parts.partname
from           """ + gvars.g_schema_arkcasedb + """.fromsup 
left join """ + gvars.g_schema_arkcasedb + """.parts 
on """ + gvars.g_schema_arkcasedb + """.fromsup.partnum = """ + gvars.g_schema_arkcasedb + """.parts.partnum
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s8')
    
    _testmgr.testcase_end(desc)

def test008(desc="""a09"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    #  drop used tables in case left over from previous run.:
    stmt = """drop table a9table1;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table a9table2;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table a9table3 ;"""
    output = _dci.cmdexec(stmt)
    
    #  Create tables to be used:
    stmt = """create table a9table1 
(
SUPPNUM                        PIC 9(3)  NOT NULL
, SUPPNAME                       PIC X(18)  NOT NULL
, ADDRESS                        PIC X(22)  NOT NULL
, CITY                           PIC X(14)  NOT NULL
, STATE                          PIC X(12)  NOT NULL
, primary key (suppnum)
);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table a9table2 
(
SUPPNUM                        PIC 9(3)  NOT NULL
, SUPPNAME                       PIC X(18)  NOT NULL
, ADDRESS                        PIC X(22)  NOT NULL
, CITY                           PIC X(14)  NOT NULL
, STATE                          PIC X(12)  NOT NULL
, primary key (suppnum)
);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table a9table3 
(
SUPPNUM                        PIC 9(3)  NOT NULL
, SUPPNAME                       PIC X(18)  NOT NULL
, ADDRESS                        PIC X(22)  NOT NULL
, CITY                           PIC X(14)  NOT NULL
, STATE                          PIC X(12)  NOT NULL
, primary key (suppnum)
) ;"""
    output = _dci.cmdexec(stmt)
    
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0149 : A09
    #  Description:        This test verifies the SQL OUTER JOIN
    #                      statements
    #                      JOIN of table on different local volumes.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    #
    
    #  Populate tables to be used:
    stmt = """insert into a9table1 
select * from """ + gvars.g_schema_arkcasedb + """.supplier 
where suppnum <= 3 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 3)
    
    stmt = """insert into a9table2 
select * from """ + gvars.g_schema_arkcasedb + """.supplier 
where suppnum >= 3 and suppnum <= 10 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 4)
    
    stmt = """insert into a9table3 
select * from """ + gvars.g_schema_arkcasedb + """.supplier 
where suppnum >= 10 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 2)
    
    #   Check what's there:
    # 04/10/09 added order by
    stmt = """select * from a9table1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s0')
    stmt = """select * from a9table2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s1')
    stmt = """select * from a9table3 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s2')
    
    #   Join between two volumes:
    stmt = """select a9table1.suppnum, a9table2.suppnum
from       a9table1 
left join  a9table2 
on a9table1.suppnum = a9table2.suppnum ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s3')
    
    stmt = """select a9table2.suppnum, a9table3.suppnum
from       a9table2 
left join  a9table3 
on a9table2.suppnum <> a9table3.suppnum ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s4')
    
    stmt = """select a9table2.suppnum, a9table3.suppnum
from       a9table2 
,  a9table3 
where a9table2.suppnum <> a9table3.suppnum ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s5')
    
    #   Join between three volumes, changing sequence:
    
    stmt = """select a9table1.suppnum, a9table2.suppnum, a9table3.suppnum
from            a9table1 
left join  a9table2 
on  a9table1.suppnum < a9table2.suppnum
left join  a9table3 
on a9table3.suppnum > a9table2.suppnum
order by 1, 2, 3 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s6')
    
    stmt = """select a9table1.suppnum, a9table2.suppnum, a9table3.suppnum
from a9table2 
left join  a9table3 
on a9table3.suppnum > a9table2.suppnum
left join  a9table1 
on a9table1.suppnum < a9table2.suppnum
order by 1, 2, 3 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s7')
    
    stmt = """select a9table1.suppnum, a9table2.suppnum, a9table3.suppnum
from            a9table3 
left join  a9table1 
on a9table3.suppnum > a9table1.suppnum
left join  a9table2 
on a9table1.suppnum < a9table2.suppnum
order by 1, 2, 3 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s8')
    
    #  drop used tables:
    stmt = """drop table a9table1;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table a9table2;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table a9table3 ;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test009(desc="""a10"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0149 : A10
    #  Description:        This test verifies the SQL OUTER JOIN
    #                      statements
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    #
    
    #   -- TESTCASE SUMMARY
    #   JOIN with LIKE predicate
    #
    #
    #   *                                                     *
    #   *  Test Case Name:  b0                                *
    #   *                                                     *
    #
    
    #   Test unit SQLT149, case b0
    #   volume $local_1_A ;
    
    # 04/10/09 added order by
    
    stmt = """select a.city, a.state
from      """ + gvars.g_schema_arkcasedb + """.customer a
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s0')
    stmt = """select                  b.city, b.state
from      """ + gvars.g_schema_arkcasedb + """.supplier b
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s1')
    
    #   Join with LIKE - supported in ANSI spec
    stmt = """select a.city, a.state, b.city, b.state
from      """ + gvars.g_schema_arkcasedb + """.customer a
left join """ + gvars.g_schema_arkcasedb + """.supplier b
on a.state = b.state
where a.city like 'S%'
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s2')
    
    stmt = """select a.city, a.state, b.city, b.state
from      """ + gvars.g_schema_arkcasedb + """.customer a
left join """ + gvars.g_schema_arkcasedb + """.supplier b
on a.city like 'S%'
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s3')
    
    stmt = """select a.city, a.state, b.city, b.state
from      """ + gvars.g_schema_arkcasedb + """.customer a
left join """ + gvars.g_schema_arkcasedb + """.supplier b
on  ( a.state = b.state )
and ( a.city like 'S%' )
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s4')
    
    _testmgr.testcase_end(desc)

def test010(desc="""a11"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0149 : A11
    #  Description:        This test verifies the SQL OUTER JOIN
    #                      statements
    #                      JOIN with multi-values predicate;
    #                      also multiple joins.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    
    #   Create tables to be used:
    
    stmt = """drop table b1table1;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table b1table1 
(a int,
b int,
c int )  no partition
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create view b1v1 (x,y) as
select t1.a, t2.a
from b1table1 t1
left join b1table1 t2
on ( t1.c <> t2.c )
where ( t1.a <> t2.a
or t2.b is not null )
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #  Populate tables to be used:
    stmt = """insert into b1table1 values (1, 2, 3) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    #   Check what's there:
    stmt = """select * from b1table1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s1')
    
    # during view composition *
    # the normalizer was attaching (erroneously)
    # the where clause of the SELECT stmt used
    # to define the view, to the ON clause of
    # the SELECT stmt used to query the view.
    
    stmt = """select * from b1table1   ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s2')
    
    stmt = """select * from b1v1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """select * from b1v1 
left join b1table1 t3 on (a=x)
where y=a or y is null ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """select * from b1v1 
left join b1table1 t3 on (x=a)
where y=a or y is null ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """select * from b1table1 t3
left join b1v1 on (x=a)
where y=a or y is null ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s3')
    
    #  Index can alter from executor evaluation to Disc Process
    #  evaluation:
    
    stmt = """create index b1ia 
on  b1table1 (a)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index b1ib 
on b1table1 (b)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index b1ic 
on b1table1 (c)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from b1v1 
left join b1table1 t3 on (a=x)
where y=a or y is null ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """select * from b1v1 
left join b1table1 t3 on (x=a)
where y=a or y is null ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """select * from b1table1 t3
left join b1v1 on (x=a)
where y=a or y is null ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s4')
    
    stmt = """drop view b1v1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop index b1ia ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop index b1ib ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop index b1ic ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #   Test for:
    #      (ON clauses for two LEFT *
    #       JOINS are identical)                *
    
    stmt = """select * from b1table1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s5')
    
    stmt = """select * from b1table1 t1
left join b1table1 t2 on t1.a <> t2.a ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s6')
    
    #   Second on clause refers only to t1 and t2:
    
    stmt = """select * from b1table1 t1
left join b1table1 t2 on t1.a <> t2.a
left join b1table1 t3 on t1.a <> t2.a ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s7')
    
    #       ON clauses for two LEFT
    #       JOINS use identical cols, but first operator is <>
    #       and second is =.
    stmt = """select * from b1table1 t1
left join b1table1 t2 on t1.a <> t2.a
left join b1table1 t3 on t1.a =  t2.a ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s8')
    
    stmt = """select * from b1table1 t1
left join b1table1 t2 on t1.a =  t2.a
left join b1table1 t3 on t1.a <> t2.a ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s9')
    
    stmt = """select * from b1table1 t1
left join b1table1 t2 on t1.a =  t2.a
left join b1table1 t3 on t1.a =  t2.a ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s10')
    
    #   Second on clause refers only to t1 and t3:
    stmt = """select * from b1table1 t1
left join b1table1 t2 on t1.a <> t2.a
left join b1table1 t3 on t1.a <> t3.a ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s11')
    
    stmt = """select * from b1table1 t1
left join b1table1 t2 on t1.a <> t2.a
left join b1table1 t3 on t1.a =  t3.a ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s12')
    
    stmt = """select * from b1table1 t1
left join b1table1 t2 on t1.a =  t2.a
left join b1table1 t3 on t1.a <> t3.a ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s13')
    
    stmt = """select * from b1table1 t1
left join b1table1 t2 on t1.a =  t2.a
left join b1table1 t3 on t1.a =  t3.a ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s14')
    
    #   Second on clause refers only to t2 and t3:
    stmt = """select * from b1table1 t1
left join b1table1 t2 on t1.a <> t2.a
left join b1table1 t3 on t2.a <> t3.a ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s15')
    
    stmt = """select * from b1table1 t1
left join b1table1 t2 on t1.a <> t2.a
left join b1table1 t3 on t2.a =  t3.a ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s16')
    
    stmt = """select * from b1table1 t1
left join b1table1 t2 on t1.a =  t2.a
left join b1table1 t3 on t2.a <> t3.a ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s17')
    
    stmt = """select * from b1table1 t1
left join b1table1 t2 on t1.a =  t2.a
left join b1table1 t3 on t2.a =  t3.a ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s18')
    
    #   NULLS:
    stmt = """select * from b1table1 t1
left join b1table1 t2 on t1.a is null
left join b1table1 t3 on t1.a is null ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s19')
    
    stmt = """select * from b1table1 t1
left join b1table1 t2 on t1.a is null
left join b1table1 t3 on t1.a is not null ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s20')
    
    stmt = """select * from b1table1 t1
left join b1table1 t2 on t1.a is not null
left join b1table1 t3 on t1.a is null ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s21')
    
    stmt = """select * from b1table1 t1
left join b1table1 t2 on t1.a is not null
left join b1table1 t3 on t1.a is not null ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s22')
    
    #  Index can alter from executor evaluation to Disc Process
    #  evaluation:
    
    stmt = """create index b1ia on b1table1 (a)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from b1table1 t1
left join b1table1 t2 on t1.a <> t2.a
left join b1table1 t3 on t1.a <> t2.a ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s23')
    
    stmt = """select * from b1table1 t1
left join b1table1 t2 on t1.a <> t2.a
left join b1table1 t3 on t1.a =  t2.a ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s24')
    
    stmt = """select * from b1table1 t1
left join b1table1 t2 on t1.a <> t2.a
left join b1table1 t3 on t1.a <> t3.a ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s25')
    
    stmt = """select * from b1table1 t1
left join b1table1 t2 on t1.a <> t2.a
left join b1table1 t3 on t2.a =  t3.a ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s26')
    
    stmt = """select * from b1table1 t1
left join b1table1 t2 on t1.a is not null
left join b1table1 t3 on t1.a is null ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s27')
    
    stmt = """drop index b1ia ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #   A different table:
    stmt = """select t1.char_1 from """ + gvars.g_schema_arkcasedb + """.btsel01 t1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s28')
    
    stmt = """select t1.char_1, t2.char_1
from      """ + gvars.g_schema_arkcasedb + """.btsel01 t1
left join """ + gvars.g_schema_arkcasedb + """.btsel01 t2
on t1.char_1 <> t2.char_1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s29')
    
    stmt = """select t1.char_1, t2.char_1
from      """ + gvars.g_schema_arkcasedb + """.btsel01 t1
left join """ + gvars.g_schema_arkcasedb + """.btsel01 t2
on t1.char_1 <> t2.char_1
left join """ + gvars.g_schema_arkcasedb + """.btsel01 t3
on t1.char_1 <> t2.char_1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s30')
    
    #  Test for:
    #      parentheses in a
    #      multivalued predicate in the
    #      ON clause for view containing a LEFT JOIN
    #      were being ignored when stored into a
    #      VIEW.
    stmt = """create view b1v2 (x,y) as
select t1.a, t2.a from b1table1 t1
left join b1table1 t2
on (t1.b , t1.c) = (t2.b , t2.c)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from b1v2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s31')
    
    #  drop tables to be used:
    
    stmt = """drop view b1v2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table b1table1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test011(desc="""a12"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0149 : A12
    #  Description:        This test verifies the SQL OUTER JOIN
    #                      statements
    #                      LEFT JOIN, ORDER BY, with WHERE clause
    #                      containing OR statement referencing
    #                      second table.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    
    #  Create tables to be used:
    stmt = """create table b2table1 (
key1 char(4)    not null
, a1   char(4)    not null
, b1   char(4)    not null
) no partition
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table b2table2 (
key2 char(4)    not null
, a2   char(4)    not null
, b2   char(4)    not null
)  no partition
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into b2table1 values ('01','A','B');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into b2table1 values ('02','B','C');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into b2table1 values ('03','C','D');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into b2table1 values ('04','D','E');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into b2table1 values ('05','E','F');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into b2table1 values ('06','F','G');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into b2table1 values ('07','G','H');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into b2table1 values ('08','H','I');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into b2table1 values ('09','I','J');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into b2table1 values ('10','J','K');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """select * from b2table1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s0')
    
    stmt = """insert into b2table2 values ('01','a','b');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into b2table2 values ('02','b','c');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into b2table2 values ('03','c','d');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into b2table2 values ('04','d','e');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into b2table2 values ('05','e','f');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into b2table2 values ('06','f','g');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into b2table2 values ('07','g','h');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into b2table2 values ('08','h','i');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into b2table2 values ('09','i','j');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into b2table2 values ('10','J','k');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """select * from b2table2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s1')
    
    #   initial problem with a join, but it is not
    #   essential to the problem, to use their view vwleftj with cols:
    #                 (key1, key2, a1, b1, a2, b2)
    #
    #   Query 1
    stmt = """select a.key1, b.key2, a.a1, a.b1, b.a2, b.b2
from b2table1 a left join b2table2 b
on a.key1   = b.key2
where a.key1   > '0'
and   b.key2 in ( '02' , '03' )
order by a.key1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s2')
    
    #   Inner join instead of left join:
    #   Query 2
    stmt = """select a.key1, b.key2, a.a1, a.b1, b.a2, b.b2
from b2table1 a      join b2table2 b
on a.key1   = b.key2
where a.key1   > '0'
and   b.key2 in ( '02' , '03' )
order by a.key1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s3')
    
    #   Removed ORDER BY from LJ:
    #   Query 3
    stmt = """select a.key1, b.key2, a.a1, a.b1, b.a2, b.b2
from b2table1 a left join b2table2 b
on a.key1   = b.key2
where a.key1   > '0'
and   b.key2 in ( '02' , '03' ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s4')
    
    #   Order by column from other table:
    #   Query 4
    stmt = """select a.key1, b.key2, a.a1, a.b1, b.a2, b.b2
from b2table1 a left join b2table2 b
on a.key1   = b.key2
where a.key1   > '0'
and   b.key2 in ( '02' , '03' )
order by b.key2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s5')
    
    #   Order by column from table not in where clause:
    #   Query 5
    stmt = """select a.key1, b.key2, a.a1, a.b1, b.a2, b.b2
from b2table1 a left join b2table2 b
on a.key1   = b.key2
where a.key1   > '0'
and   a.key1 in ( '02' , '03' )
order by b.key2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s6')
    
    #   Query 6
    stmt = """select a.key1, b.key2, a.a1, a.b1, b.a2, b.b2
from b2table1 a left join b2table2 b
on a.key1   = b.key2
where b.key2   > '0'
and   b.key2 in ( '02' , '03' )
order by a.key1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s7')
    
    #   Order by and where columns all in same table:
    #   Query 7
    stmt = """select a.key1, b.key2, a.a1, a.b1, b.a2, b.b2
from b2table1 a left join b2table2 b
on a.key1   = b.key2
where a.key1   > '0'
and   a.key1 in ( '02' , '03' )
order by a.key1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s8')
    
    #   Group by and order by columns in different tables gives error:
    #   Query 8
    stmt = """select a.key1, b.key2
from b2table1 a
left join b2table2 b
on a.key1   = b.key2
group by a.key1, b.key2
having a.key1   > '0' and a.key1 in ( '02' , '03' )
order by b.key2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s9')
    
    #   Query 9
    stmt = """select a.key1, b.key2
from b2table1 a left join b2table2 b
on a.key1   = b.key2
--        group by         b.key2
having a.key1   > '0' and a.key1 in ( '02' , '03' )
order by a.key1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4005')
    
    #   01/10/94 - Added Order By 1 to avoid spurious order changes.
    #   Query 10
    stmt = """select a.key1, b.key2
from b2table1 a left join b2table2 b
on a.key1   = b.key2
group by a.key1, b.key2
having a.key1   > '0' and a.key1 in ( '02' , '03' )
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s11')
    
    #   01/10/94 - Added Order By 2 to avoid spurious order changes.
    
    #   Query 11
    stmt = """select a.key1, b.key2
from b2table1 a left join b2table2 b
on a.key1   = b.key2
where  a.key1   > '0'
and a.key1 in ( '02' , '03' )
group by a.key1, b.key2
having a.key1   > '0'
and a.key1 in ( '02' , '03' )
order by 2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s12')
    
    #   Query 12
    #   Similarly on global database (problem seen only on non-key columns):
    stmt = """select a.var_char_3
from """ + gvars.g_schema_arkcasedb + """.btre201 a ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s13')
    
    #   Query 13
    stmt = """select a.var_char_3, b.var_char_3
from """ + gvars.g_schema_arkcasedb + """.btre201 a
left join """ + gvars.g_schema_arkcasedb + """.btre201 b
on a.var_char_3 = b.var_char_3
where a.var_char_3  > 'b'
and b.var_char_3  in ( 'AbC', 'rum' )
order by a.var_char_3 , b.var_char_3 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s14')
    
    #   Query 14
    stmt = """select a.var_char_3 , b.var_char_3
from """ + gvars.g_schema_arkcasedb + """.btre201 a
left join """ + gvars.g_schema_arkcasedb + """.btre201 b
on a.var_char_3 = b.var_char_3
where a.var_char_3  > 'b'
and b.var_char_3  in ( 'AbC', 'rum' ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s15')
    
    stmt = """drop table b2table1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table b2table2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test012(desc="""a13"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0149 : A13
    #  Description:        This test verifies the SQL OUTER JOIN
    #                      statements
    #                      LEFT JOIN, nested loop, ON clause
    #                      contains predicate that must be
    #                      evaluated by executor.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    
    stmt = """drop table  b3tab;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table  b3tab 
(a int,
b int,
c int) no partition
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """set param ?a 10;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?b 20;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?c 30;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s from insert into b3tab values (?a,?b,?c);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """execute s ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    #using 10,20,30;
    
    stmt = """set param ?a 10;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?b 30;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?c 20;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s from insert into b3tab values (?a,?b,?c);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    # using 10,30,20;
    
    # Update statistics
    # update statistics for table b3tab;
    
    stmt = """prepare s from
select * from b3tab t1 left join b3tab t2
on (t1.a = t2.a and t2.c <=all
(select t3.b from b3tab t3))
where t1.b = 20;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select * from b3tab t1 where t1.b = 20;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s1')
    
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s2')
    
    stmt = """drop table  b3tab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test013(desc="""a14"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    #  LEFT JOIN between a table and a view does not return
    #  correct result.  Predicate of the view is treated as the
    #  predicate of the LEFT JOIN statement, so some rows that
    #  should be returned are eliminated.
    
    stmt = """create table b4table1 
(a int not null, b int not null,
c varchar(100) not null,
primary key (a) );"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table b4table2 
(a int not null, b int not null, c varchar(100) not null,
primary key (a));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create index b4tab1x 
on b4table1 (b);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create index b4tab2x 
on b4table2 (b);"""
    output = _dci.cmdexec(stmt)
    
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0149 : A14
    #  Description:        This test verifies the SQL OUTER JOIN
    #                      statements
    #                      Left join between table and view - predicate of
    #                      view should not be treated as predicate of join.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    
    #using 1,1,'a';
    stmt = """set param ?p 1;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?q 1;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?r 'a';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s from
insert into b4table1 values (?p,?q,?r);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """execute s ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """set param ?p 2;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?q 2;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?r 'b';"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    # using 2,2,'b';
    
    stmt = """set param ?p 101;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?q 101;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?r 'c';"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    # using 101,101,'c';
    
    stmt = """set param ?p 102;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?q 102;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?r 'c';"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    # using 102,102,'c';
    
    stmt = """set param ?p 201;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?q 201;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?r 'd';"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    # using 201,201,'d';
    
    stmt = """set param ?p 205;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?q 205;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?r 'd';"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    # using 205,205,'d';
    
    stmt = """set param ?p 307;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?q 307;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?r 'e';"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #using 307,307,'e';
    
    stmt = """set param ?p 400;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?q 400;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?r 'e';"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    # using 400,400,'e';
    
    stmt = """prepare t from
insert into b4table2 values (?p,?q,?r);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """set param ?p 1;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?q 1;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?r 'a';"""
    output = _dci.cmdexec(stmt)
    stmt = """execute t ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """set param ?p 2;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?q 2;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?r 'b';"""
    output = _dci.cmdexec(stmt)
    stmt = """execute t;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """set param ?p 101;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?q 101;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?r 'c';"""
    output = _dci.cmdexec(stmt)
    stmt = """execute t;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """set param ?p 102;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?q 102;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?r 'c';"""
    output = _dci.cmdexec(stmt)
    stmt = """execute t;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """set param ?p 201;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?q 201;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?r 'd';"""
    output = _dci.cmdexec(stmt)
    stmt = """execute t;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """set param ?p 205;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?q 205;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?r 'd';"""
    output = _dci.cmdexec(stmt)
    stmt = """execute t;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """set param ?p 307;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?q 307;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?r 'e';"""
    output = _dci.cmdexec(stmt)
    stmt = """execute t ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """set param ?p 400;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?q 400;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?r 'e';"""
    output = _dci.cmdexec(stmt)
    stmt = """execute t;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select * from b4table1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a14exp""", 'a14s0')
    stmt = """select * from b4table2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a14exp""", 'a14s1')
    
    stmt = """create view b4tab2v (x,y) as select a*2, upshift(c)
from b4table2 where b=2*1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from b4tab2v;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a14exp""", 'a14s2')
    
    stmt = """select t1.*,b4table1.* from b4tab2v t1
left join b4table1 
on b4table1.a=t1.x**2
order by 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a14exp""", 'a14s3')
    
    stmt = """select t1.*,b4table1.* from b4table1 
left join b4tab2v t1
on t1.x=b4table1.a**2
order by 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a14exp""", 'a14s4')
    
    stmt = """select t1.*,b4table1.* from b4tab2v t1
left join b4table1 
on b4table1.a=t1.x**2
UNION
select t1.*,b4table1.* from b4table1 
left join b4tab2v t1
on t1.x=b4table1.a**2
order by 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a14exp""", 'a14s5')
    
    stmt = """select t1.*,b4table1.* from b4table1 
left join b4tab2v t1
on t1.x=b4table1.a**2
UNION
select t1.*,b4table1.* from b4tab2v t1
left join b4table1 
on b4table1.a=t1.x**2
order by 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a14exp""", 'a14s6')
    
    stmt = """drop view b4tab2v;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table b4table1 ;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table b4table2 ;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test014(desc="""a15"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #  Test case name:     arkt0149 : A15
    #  Description:        This test verifies the SQL OUTER JOIN
    #                      statements
    #                      Left join followed by inner join:
    #                      Avoid suboptimal plan with projection done late.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    #
    stmt = """drop table mkey2  ;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table mkey2 
(a int,
b int,
c int) no partition
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """invoke mkey2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # Create an index to use in the query.
    
    stmt = """create index mkey2i1 on
 mkey2 (a,b,c)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop table omerg1 ;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table omerg1 
(a int,
b int,
c int)  no partition
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """invoke omerg1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into mkey2 values ( 1, 1, 1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 1, 1, 2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 1, 1, 3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 1, 1, 4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 1, 1, 5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 1, 1, null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 1, 2, 1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 1, 2, 2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 1, 2, 3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 1, 2, 4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 1, 2, 5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 1, 2, null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 1, 3, 1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 1, 3, 2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 1, 3, 3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 1, 3, 4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 1, 3, 5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 1, 3, null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 1, 4, 1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 1, 4, 2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 1, 4, 3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 1, 4, 4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 1, 4, 5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 1, 4, null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 1, 5, 1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 1, 5, 2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 1, 5, 3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 1, 5, 4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 1, 5, 5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 1, 5, null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 1, null, 1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 1, null, 2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 1, null, 3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 1, null, 4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 1, null, 5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 1, null, null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into mkey2 values ( 2, 1, 1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 2, 1, 2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 2, 1, 3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 2, 1, 4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 2, 1, 5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 2, 1, null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 2, 2, 1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 2, 2, 2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 2, 2, 3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 2, 2, 4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 2, 2, 5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 2, 2, null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 2, 3, 1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 2, 3, 2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 2, 3, 3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 2, 3, 4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 2, 3, 5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 2, 3, null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 2, 4, 1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 2, 4, 2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 2, 4, 3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 2, 4, 4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 2, 4, 5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 2, 4, null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 2, 5, 1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 2, 5, 2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 2, 5, 3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 2, 5, 4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 2, 5, 5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 2, 5, null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 2, null, 1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 2, null, 2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 2, null, 3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 2, null, 4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 2, null, 5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 2, null, null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into mkey2 values ( 3, 1, 1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 3, 1, 2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 3, 1, 3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 3, 1, 4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 3, 1, 5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 3, 1, null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 3, 2, 1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 3, 2, 2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 3, 2, 3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 3, 2, 4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 3, 2, 5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 3, 2, null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 3, 3, 1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 3, 3, 2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 3, 3, 3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 3, 3, 4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 3, 3, 5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 3, 3, null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 3, 4, 1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 3, 4, 2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 3, 4, 3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 3, 4, 4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 3, 4, 5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 3, 4, null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 3, 5, 1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 3, 5, 2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 3, 5, 3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 3, 5, 4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 3, 5, 5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 3, 5, null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 3, null, 1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 3, null, 2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 3, null, 3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 3, null, 4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 3, null, 5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 3, null, null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into mkey2 values ( 4, 1, 1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 4, 1, 2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 4, 1, 3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 4, 1, 4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 4, 1, 5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 4, 1, null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 4, 2, 1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 4, 2, 2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 4, 2, 3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 4, 2, 4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 4, 2, 5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 4, 2, null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 4, 3, 1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 4, 3, 2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 4, 3, 3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 4, 3, 4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 4, 3, 5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 4, 3, null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 4, 4, 1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 4, 4, 2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 4, 4, 3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 4, 4, 4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 4, 4, 5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 4, 4, null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 4, 5, 1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 4, 5, 2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 4, 5, 3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 4, 5, 4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 4, 5, 5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 4, 5, null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 4, null, 1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 4, null, 2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 4, null, 3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 4, null, 4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 4, null, 5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 4, null, null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into mkey2 values ( 5, 1, 1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 5, 1, 2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 5, 1, 3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 5, 1, 4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 5, 1, 5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 5, 1, null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 5, 2, 1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 5, 2, 2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 5, 2, 3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 5, 2, 4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 5, 2, 5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 5, 2, null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 5, 3, 1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 5, 3, 2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 5, 3, 3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 5, 3, 4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 5, 3, 5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 5, 3, null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 5, 4, 1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 5, 4, 2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 5, 4, 3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 5, 4, 4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 5, 4, 5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 5, 4, null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 5, 5, 1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 5, 5, 2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 5, 5, 3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 5, 5, 4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 5, 5, 5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 5, 5, null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 5, null, 1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 5, null, 2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 5, null, 3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 5, null, 4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 5, null, 5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 5, null, null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into mkey2 values ( null, 1, 1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( null, 1, 2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( null, 1, 3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( null, 1, 4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( null, 1, 5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( null, 1, null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( null, 2, 1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( null, 2, 2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( null, 2, 3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( null, 2, 4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( null, 2, 5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( null, 2, null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( null, 3, 1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( null, 3, 2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( null, 3, 3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( null, 3, 4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( null, 3, 5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( null, 3, null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( null, 4, 1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( null, 4, 2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( null, 4, 3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( null, 4, 4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( null, 4, 5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( null, 4, null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( null, 5, 1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( null, 5, 2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( null, 5, 3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( null, 5, 4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( null, 5, 5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( null, 5, null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( null, null, 1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( null, null, 2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( null, null, 3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( null, null, 4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( null, null, 5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( null, null, null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select * from mkey2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s4')
    
    stmt = """update statistics for table mkey2;"""
    output = _dci.cmdexec(stmt)
    
    # Suboptimal plan when left join followed by inner join
    # projection done late.
    
    stmt = """insert into  omerg1 values (10,10,10);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """prepare s from
select * from omerg1 t1
left join omerg1 t2
on t1.a=t2.a
inner join mkey2 t3
on t2.a=t3.a and t2.b=t3.b and t2.c=t3.c ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    #
    # The join into the table T3 fails to use the excellent key
    # predicates that are provided. The plan basically performs the
    # cross product between the result of the left join and table T3 and
    # then applies the predicates between T2 and T3. This predicates
    # should have been applied on the join between the result of the
    # outer join and T3.
    #
    
    stmt = """prepare s from select * from omerg1 t1 left join
 omerg1 t2
on t1.a=t2.a
inner join mkey2 t3
on 1=1
where t2.a=t3.a and t2.b=t3.b and
t2.c=t3.c ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """prepare s from select * from omerg1 t1 left join
 omerg1 t2
on t1.a=t2.a
left  join mkey2 t3
on t2.a=t3.a and t2.b=t3.b and
t2.c=t3.c ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s5')
    #  In this case we should apply the predicates on the
    #  scan of T3.
    
    # ----------------------------
    #   Many LEFT and INNER JOINs:
    # ----------------------------
    
    #  This gives memory fault right now. So commented out.
    
    #  prepare t from
    stmt = """select t1.binary_signed , t2.char_1 , t3.pic_x_8
from """ + gvars.g_schema_arkcasedb + """.btsel01 t1
left join """ + gvars.g_schema_arkcasedb + """.btsel01 t2
on t1.char_1        = t2.char_1
inner join """ + gvars.g_schema_arkcasedb + """.btre201 t3
on t1.char_10       = t3.pic_x_8 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s6')
    
    # execute t;
    
    stmt = """drop table mkey2  ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table omerg1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test015(desc="""a16"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0149 : A16
    #  Description:        This test verifies the SQL OUTER JOIN
    #                      statements
    #                       LEFT JOIN with Having clause
    #                       Having predicate involves an aggregate
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    #
    # AR 1/15/07 added order by for consistent result
    stmt = """select T1.binary_signed,
T1.binary_32_u,
count(distinct T2.binary_64_s) ,
count(*)
from """ + gvars.g_schema_arkcasedb + """.btsel01 T1
left join
 """ + gvars.g_schema_arkcasedb + """.btsel01 T2
on T1.binary_signed = T2.medium_int
group by T1.binary_signed, T1.binary_32_u
having count(distinct T2.binary_64_s) > 0
order by T1.binary_signed;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s0')
    
    stmt = """select T1.binary_signed,
T1.binary_32_u,
count(T2.binary_64_s) ,
count(*)
from """ + gvars.g_schema_arkcasedb + """.btsel01 T1
left join
 """ + gvars.g_schema_arkcasedb + """.btsel01 T2
on T1.binary_signed = T2.medium_int
group by T1.binary_signed, T1.binary_32_u
having count(T2.binary_64_s) > 0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s1')
    
    _testmgr.testcase_end(desc)

def test016(desc="""a17"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    #--------------------------------
    #-- Create & populate database:
    #--------------------------------
    # Purge tables, which should not exist at this time:
    
    stmt = """drop   table expr;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop   table require;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop   table sets1;"""
    output = _dci.cmdexec(stmt)
    
    # Create tables:
    stmt = """create table expr 
(can_num pic 9(6)  not null
,set_id  int unsigned no default not null
,skill_id int unsigned no default not null
,expr smallint unsigned no default not null
) no partition;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table require 
(
job_id pic x(8)  not null
,set_id int unsigned no default not null
,skill_id int unsigned no default not null
,expr smallint unsigned no default not null
,pri pic 9  not null
) no partition;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table sets1 
(
set_id int unsigned no default not null
,skill_id int unsigned no default not null
,s_level int unsigned no default not null
) no partition;"""
    output = _dci.cmdexec(stmt)
    
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0149 : A17
    #  Description:        This test verifies the SQL OUTER JOIN
    #                      statements
    #                      Left join in subquery used with WHERE NOT EXISTS.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    
    # Populate tables:
    # Table expr:
    stmt = """insert into expr values (100081,1010001, 1010000, 1)  ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into expr values (100081,1040002, 1040002, 1)  ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into expr values (100081,1040007, 1040007, 1)  ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into expr values (100081,1060001, 1060000, 1)  ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into expr values (100081,1080003, 1080003, 1)  ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into expr values (100081,1010001, 1010001, 5)  ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into expr values (100700,1020001, 1020001, 1)  ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into expr values (100677,1010001, 1010001, 2)  ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into expr values (100677,1010005, 1010005, 2)  ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into expr values (100677,1010009, 1010009, 2)  ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into expr values (100677,1010016, 1010016, 2)  ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into expr values (100677,1020004, 1020004, 2)  ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into expr values (100677,1040007, 1040007, 2)  ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into expr values (100677,1040008, 1040007, 2)  ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into expr values (100677,1040011, 1040011, 2)  ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into expr values (100677,1040012, 1040012, 2)  ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into expr values (100677,1050003, 1050003, 2)  ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into expr values (100677,1080001, 1080001, 2)  ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into expr values (100677,1080002, 1080002, 2)  ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into expr values (100677,1080003, 1080003, 2)  ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into expr values (100669,1010001, 1010001, 4)  ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into expr values (100669,1020004, 1020004, 3)  ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into expr values (100669,1020006, 1020006, 1)  ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into expr values (100669,1040007, 1040007, 4)  ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into expr values (100669,1040008, 1040008, 4)  ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into expr values (100669,1040012, 1040012, 4)  ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into expr values (100669,1050003, 1050003, 3)  ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into expr values (100669,1080001, 1080001, 3)  ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # Table require:
    stmt = """insert into require values ('TEST', 1010001, 1010001, 4, 0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into require values ('TEST', 1020001, 1020000, 2, 1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # Table sets1:
    stmt = """insert into sets1 values (1010001,1000000,3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sets1 values (1010001,1010000,2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sets1 values (1010001,1010001,0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sets1 values (1010005,1000000,3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sets1 values (1010005,1010000,2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sets1 values (1010005,1050000,0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sets1 values (1010009,1000000,3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sets1 values (1010009,1010009,2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sets1 values (1010009,1010000,0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sets1 values (1010016,1000000,3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sets1 values (1010016,1010000,2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sets1 values (1010016,1010016,0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sets1 values (1020001,1000000,3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sets1 values (1020001,1020000,2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sets1 values (1020001,1020001,0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sets1 values (1020004,1000000,3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sets1 values (1020004,1020000,2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sets1 values (1020004,1020004,0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    #------------------------------
    # Simplified queries to check stored values:
    #------------------------------
    
    stmt = """SET PARAM ?JOB TEST;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select * from require;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s0')
    stmt = """select * from expr;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s1')
    stmt = """select * from expr 
where expr.CAN_NUM IN (100669,100677,100700,100081);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s2')
    stmt = """select * from sets1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s3')
    
    stmt = """prepare s  from
SELECT EE.CAN_NUM, EE.SET_ID, EE.EXPR, SS.*
FROM expr EE
LEFT JOIN sets1 SS
ON (EE.EXPR >= 2)
ORDER BY 1, 2, 4, 5 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #   Expect 385 rows.
    stmt = """execute s  ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s4')
    
    #  Expect 385 rows in following view.
    stmt = """create view v (e1, e2, e3, s1, s2, s3) as
SELECT EE.CAN_NUM, EE.SET_ID, EE.EXPR, SS.*
FROM expr EE
LEFT JOIN sets1 SS
ON (EE.EXPR >= 2)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from v ORDER BY 1, 2, 4, 5 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s5')
    
    stmt = """drop   view v ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #------------------------------
    # 3 simplified versions of the customer query; fail pre-c30.s06.
    #------------------------------
    
    stmt = """prepare s3 from
SELECT EE.CAN_NUM, EE.SET_ID, EE.EXPR, SS.*
FROM require RR
JOIN expr EE
ON RR.JOB_ID = ?JOB
LEFT JOIN sets1 SS
ON (RR.PRI = 0 OR (RR.PRI > 0
AND EE.EXPR >= RR.EXPR))
ORDER BY 1, 2, 4, 5 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #   Expect 889 rows (504 + 385) rows.
    stmt = """execute s3 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s6')
    
    stmt = """prepare s2 from
SELECT EE.CAN_NUM, EE.SET_ID, EE.EXPR,
RR.EXPR, RR.SKILL_ID, SS.SET_ID, SS.SKILL_ID
FROM require RR
JOIN expr EE
ON RR.JOB_ID = ?JOB
AND EE.CAN_NUM IN (100669,100677,100700, 100081)
LEFT JOIN sets1 SS
ON (EE.SET_ID, RR.SKILL_ID) = (SS.SET_ID, SS.SKILL_ID)
AND (RR.PRI = 0 OR
(RR.PRI > 0 AND EE.EXPR >= RR.EXPR))
ORDER BY 1, 2, 3, 5, 6 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #   Expect these 56 rows.
    stmt = """execute s2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s7')
    
    stmt = """prepare s1 from
SELECT EE.CAN_NUM, EE.SET_ID, EE.EXPR,
RR.EXPR, RR.SKILL_ID, SS.SET_ID, SS.SKILL_ID,
S1.SET_ID, S1.SKILL_ID, SS.S_LEVEL , S1.S_LEVEL
FROM require RR
JOIN expr EE
ON RR.JOB_ID = ?JOB
AND EE.CAN_NUM IN (100669,100677,100700, 100081)
LEFT JOIN sets1 SS
ON (EE.SET_ID, RR.SKILL_ID) = (SS.SET_ID, SS.SKILL_ID)
AND (RR.PRI = 0
OR (RR.PRI > 0 AND EE.EXPR >= RR.EXPR))
LEFT JOIN sets1 S1
ON SS.S_LEVEL = S1.S_LEVEL
AND (RR.SET_ID, RR.SKILL_ID)
= (S1.SET_ID, S1.SKILL_ID)
ORDER BY 1, 2, 6, 7 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #   Expect these 56 rows.
    stmt = """execute s1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 56)
    
    stmt = """create view v (e1, e2, e3, r1, r2, s1, s2, s3, s4, s5, s6 ) as
SELECT EE.CAN_NUM, EE.SET_ID, EE.EXPR,
RR.EXPR, RR.SKILL_ID, SS.SET_ID, SS.SKILL_ID,
S1.SET_ID, S1.SKILL_ID, SS.S_LEVEL , S1.S_LEVEL
FROM require RR
JOIN expr EE
--             ON RR.JOB_ID = ?JOB
ON RR.JOB_ID = 'TEST'
AND EE.CAN_NUM IN (100669,100677,100700, 100081)
LEFT JOIN sets1 SS
ON (EE.SET_ID, RR.SKILL_ID) = (SS.SET_ID, SS.SKILL_ID)
AND (RR.PRI = 0
OR (RR.PRI > 0 AND EE.EXPR >= RR.EXPR))
LEFT JOIN sets1 S1
ON SS.S_LEVEL = S1.S_LEVEL
AND (RR.SET_ID, RR.SKILL_ID)
= (S1.SET_ID, S1.SKILL_ID)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #   Expect these 56 rows.
    stmt = """select * from v ORDER BY 1, 2, 6, 7 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 56)
    
    stmt = """drop   view v ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #------------------------------
    # Other simplified portions of the customer query:
    #------------------------------
    
    stmt = """prepare s1 from
SELECT EE.CAN_NUM FROM require RR
JOIN expr EE ON RR.JOB_ID = ?JOB
ORDER BY 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #   Expect 56 rows.
    stmt = """execute s1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s10')
    
    stmt = """prepare s1 from
SELECT EE.CAN_NUM
FROM require RR
JOIN expr EE ON RR.JOB_ID = ?JOB
AND EE.CAN_NUM IN (100669,100677,100700, 100081)
ORDER BY 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #   Expect 56 rows.
    stmt = """execute s1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s11')
    
    stmt = """prepare s1 from
SELECT EE.CAN_NUM
FROM require RR
JOIN expr EE ON RR.JOB_ID = ?JOB
AND EE.CAN_NUM IN (100669,100677,100700, 100081)
LEFT JOIN sets1 SS
ON (EE.SET_ID, RR.SKILL_ID) = (SS.SET_ID, SS.SKILL_ID)
ORDER BY 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #   Expect 56 rows.
    stmt = """execute s1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s12')
    
    stmt = """SELECT count(*) from expr EE ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s13')
    stmt = """SELECT count(*) from require RR ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s14')
    stmt = """SELECT count(*), (28 * 2 * 18) from sets1 SS ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s15')
    
    stmt = """prepare s1 from
SELECT count(*)
from expr EE , require RR , sets1 SS ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    #   Expect 1008 rows.
    stmt = """execute s1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s16')
    
    
    #   Expect 4 rows.
    stmt = """SELECT DISTINCT E.CAN_NUM FROM expr E ORDER BY 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s17')
    
    #   Expect 4 rows.
    stmt = """SELECT DISTINCT EE.CAN_NUM FROM require RR
JOIN expr EE
ON RR.JOB_ID = ?JOB
AND EE.CAN_NUM IN (100669,100677,100700, 100081)
LEFT JOIN sets1 SS
ON (EE.SET_ID, RR.SKILL_ID) = (SS.SET_ID, SS.SKILL_ID)
AND (RR.PRI = 0
OR (RR.PRI > 0 AND EE.EXPR >= RR.EXPR))
LEFT JOIN sets1 S1
ON SS.S_LEVEL = S1.S_LEVEL
AND (RR.SET_ID, RR.SKILL_ID)
= (S1.SET_ID, S1.SKILL_ID)
ORDER BY 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s18')
    
    #  Expect 0 rows.
    stmt = """SELECT E.CAN_NUM
-- EE.CAN_NUM, etc are not known to the outer query.
FROM expr E
--next line returns 0 rows
--returns data if next line is WHERE EXISTS
--Bug => fails with 8424 if nextline is WHERE E.CAN_NUM NOT IN
--  WHERE NOT EXISTS
WHERE E.CAN_NUM NOT IN
(
SELECT EE.CAN_NUM
FROM require RR
JOIN expr EE
ON RR.JOB_ID = ?JOB
AND EE.CAN_NUM IN (100669,100677,100700, 100081)
LEFT JOIN sets1 SS
ON (EE.SET_ID, RR.SKILL_ID) = (SS.SET_ID, SS.SKILL_ID)
AND (RR.PRI = 0
OR (RR.PRI > 0 AND EE.EXPR >= RR.EXPR))
LEFT JOIN sets1 S1
ON SS.S_LEVEL = S1.S_LEVEL
AND (RR.SET_ID, RR.SKILL_ID)
= (S1.SET_ID, S1.SKILL_ID)         )
ORDER BY 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """create view v as
SELECT E.CAN_NUM
FROM expr E
WHERE NOT EXISTS
(
SELECT EE.CAN_NUM
FROM require RR
JOIN expr EE
--             ON RR.JOB_ID = ?JOB
ON RR.JOB_ID = 'TEST'
AND EE.CAN_NUM IN (100669,100677,100700, 100081)
LEFT JOIN sets1 SS
ON (EE.SET_ID, RR.SKILL_ID) = (SS.SET_ID, SS.SKILL_ID)
AND (RR.PRI = 0
OR (RR.PRI > 0 AND EE.EXPR >= RR.EXPR))
LEFT JOIN sets1 S1
ON SS.S_LEVEL = S1.S_LEVEL
AND (RR.SET_ID, RR.SKILL_ID)
= (S1.SET_ID, S1.SKILL_ID)         )
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #  Expect 0 rows.
    stmt = """select * from v ORDER BY 1  ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """drop   view v ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """SELECT E.CAN_NUM
FROM expr E
--BUG => next line fails with 8424
--returns data if next line is WHERE EXISTS
--returns 0 rows if next line is WHERE NOT EXISTS
WHERE NOT EXISTS
--  WHERE E.CAN_NUM NOT IN
(
SELECT EE.CAN_NUM
FROM require RR
JOIN expr EE
ON RR.JOB_ID = ?JOB
AND EE.CAN_NUM IN (100669,100677,100700, 100081)
LEFT JOIN sets1 SS
ON (EE.SET_ID, RR.SKILL_ID) = (SS.SET_ID, SS.SKILL_ID)
AND (RR.PRI = 0
OR (RR.PRI > 0 AND EE.EXPR >= RR.EXPR))
LEFT JOIN sets1 S1
ON SS.S_LEVEL = S1.S_LEVEL
AND (RR.SET_ID, RR.SKILL_ID)
= (S1.SET_ID, S1.SKILL_ID)         )
ORDER BY 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    #  Expect 0 rows.
    
    stmt = """create view v as
SELECT E.CAN_NUM
FROM expr E
WHERE E.CAN_NUM NOT IN
(
SELECT EE.CAN_NUM
FROM require RR
JOIN expr EE
--             ON RR.JOB_ID = ?JOB
ON RR.JOB_ID = 'TEST'
AND EE.CAN_NUM IN (100669,100677,100700, 100081)
LEFT JOIN sets1 SS
ON (EE.SET_ID, RR.SKILL_ID) = (SS.SET_ID, SS.SKILL_ID)
AND (RR.PRI = 0
OR (RR.PRI > 0 AND EE.EXPR >= RR.EXPR))
LEFT JOIN sets1 S1
ON SS.S_LEVEL = S1.S_LEVEL
AND (RR.SET_ID, RR.SKILL_ID)
= (S1.SET_ID, S1.SKILL_ID)         )
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from v ORDER BY 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """drop   view v ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #   Query to show subset needed below:
    #   Expect 56 rows.
    stmt = """SELECT EE.CAN_NUM, EE.SET_ID, EE.EXPR,
RR.EXPR, RR.SKILL_ID, RR.SET_ID,
SS.S_LEVEL, SS.SET_ID, SS.SKILL_ID,
S1.SET_ID, S1.SKILL_ID
FROM require RR
JOIN expr EE
ON RR.JOB_ID = ?JOB
AND EE.CAN_NUM IN (100669,100677,100700, 100081)
LEFT JOIN sets1 SS
ON (EE.SET_ID, RR.SKILL_ID) = (SS.SET_ID, SS.SKILL_ID)
AND (RR.PRI = 0
OR (RR.PRI > 0 AND EE.EXPR >= RR.EXPR))
LEFT JOIN sets1 S1
ON SS.S_LEVEL = S1.S_LEVEL
AND (RR.SET_ID, RR.SKILL_ID)
= (S1.SET_ID, S1.SKILL_ID)
--       WHERE  SUM(SS.S_LEVEL) IS NULL
--       HAVING SUM(SS.S_LEVEL) IS NULL
--       GROUP BY EE.CAN_NUM,RR.SET_ID
ORDER BY 1, 2, 3, 5, 6, 8 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s19')
    
    stmt = """create view v (e1, e2, e3, r1, r2, r3, s1, s2, s3, s4, s5 ) as
SELECT EE.CAN_NUM, EE.SET_ID, EE.EXPR,
RR.EXPR, RR.SKILL_ID, RR.SET_ID,
SS.S_LEVEL, SS.SET_ID, SS.SKILL_ID,
S1.SET_ID, S1.SKILL_ID
FROM require RR
JOIN expr EE
--             ON RR.JOB_ID = ?JOB
ON RR.JOB_ID = 'TEST'
AND EE.CAN_NUM IN (100669,100677,100700, 100081)
LEFT JOIN sets1 SS
ON (EE.SET_ID, RR.SKILL_ID) = (SS.SET_ID, SS.SKILL_ID)
AND (RR.PRI = 0
OR (RR.PRI > 0 AND EE.EXPR >= RR.EXPR))
LEFT JOIN sets1 S1
ON SS.S_LEVEL = S1.S_LEVEL
AND (RR.SET_ID, RR.SKILL_ID)
= (S1.SET_ID, S1.SKILL_ID)
--      WHERE  SUM(SS.S_LEVEL) IS NULL
--      HAVING SUM(SS.S_LEVEL) IS NULL
--      GROUP BY EE.CAN_NUM,RR.SET_ID
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #   Expect 56 rows.
    stmt = """select * from v ORDER BY 1, 2, 3, 5, 6, 8 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s20')
    stmt = """drop   view v ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #   Expect 3 rows   --- no 100669's or 100677's
    stmt = """SELECT EE.CAN_NUM, RR.SET_ID
FROM require RR
JOIN expr EE
ON RR.JOB_ID = ?JOB
AND EE.CAN_NUM IN (100669,100677,100700, 100081)
LEFT JOIN sets1 SS
ON (EE.SET_ID, RR.SKILL_ID) = (SS.SET_ID, SS.SKILL_ID)
AND (RR.PRI = 0
OR (RR.PRI > 0 AND EE.EXPR >= RR.EXPR))
LEFT JOIN sets1 S1
ON SS.S_LEVEL = S1.S_LEVEL
AND (RR.SET_ID, RR.SKILL_ID)
= (S1.SET_ID, S1.SKILL_ID)
--         WHERE  SUM(SS.S_LEVEL) IS NULL
--         HAVING SUM(SS.S_LEVEL) IS NULL
--         GROUP BY EE.CAN_NUM,RR.SET_ID
ORDER BY 1, 2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s21')
    
    stmt = """create view v as
SELECT EE.CAN_NUM, RR.SET_ID
FROM require RR
JOIN expr EE
--             ON RR.JOB_ID = ?JOB
ON RR.JOB_ID = 'TEST'
AND EE.CAN_NUM IN (100669,100677,100700, 100081)
LEFT JOIN sets1 SS
ON (EE.SET_ID, RR.SKILL_ID) = (SS.SET_ID, SS.SKILL_ID)
AND (RR.PRI = 0
OR (RR.PRI > 0 AND EE.EXPR >= RR.EXPR))
LEFT JOIN sets1 S1
ON SS.S_LEVEL = S1.S_LEVEL
AND (RR.SET_ID, RR.SKILL_ID)
= (S1.SET_ID, S1.SKILL_ID)
--        WHERE  SUM(SS.S_LEVEL) IS NULL
--        HAVING SUM(SS.S_LEVEL) IS NULL
--        GROUP BY EE.CAN_NUM,RR.SET_ID
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #   Expect 3 rows.
    stmt = """select * from v ORDER BY 1, 2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s22')
    
    stmt = """drop   view v ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # ------------------------------
    #  Q0, the customers original query, which returned error 8424.
    # ------------------------------
    
    #  Expect 21 rows, with can_num values remaining after removal of
    #  those in subquery.
    stmt = """SELECT E.CAN_NUM
--  EE.CAN_NUM, etc are not known to the outer query.
FROM expr E
WHERE E.CAN_NUM IN (100669,100677,100700,100081)
AND E.CAN_NUM NOT IN
(
SELECT EE.CAN_NUM
FROM require RR
JOIN expr EE
ON RR.JOB_ID = ?JOB
AND EE.CAN_NUM IN (100669,100677,100700, 100081)
LEFT JOIN sets1 SS
ON (EE.SET_ID, RR.SKILL_ID) = (SS.SET_ID, SS.SKILL_ID)
AND (RR.PRI = 0
OR (RR.PRI > 0 AND EE.EXPR >= RR.EXPR))
LEFT JOIN sets1 S1
ON SS.S_LEVEL = S1.S_LEVEL
AND (RR.SET_ID, RR.SKILL_ID)
= (S1.SET_ID, S1.SKILL_ID)
GROUP BY EE.CAN_NUM,RR.SET_ID
HAVING SUM(SS.S_LEVEL) IS NULL
)
ORDER BY 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s23')
    
    stmt = """create view v as
SELECT E.CAN_NUM
FROM expr E
WHERE E.CAN_NUM IN (100669,100677,100700,100081)
AND E.CAN_NUM NOT IN
(
SELECT EE.CAN_NUM
FROM require RR
JOIN expr EE
--             ON RR.JOB_ID = ?JOB
ON RR.JOB_ID = 'TEST'
AND EE.CAN_NUM IN (100669,100677,100700, 100081)
LEFT JOIN sets1 SS
ON (EE.SET_ID, RR.SKILL_ID) = (SS.SET_ID, SS.SKILL_ID)
AND (RR.PRI = 0
OR (RR.PRI > 0 AND EE.EXPR >= RR.EXPR))
LEFT JOIN sets1 S1
ON SS.S_LEVEL = S1.S_LEVEL
AND (RR.SET_ID, RR.SKILL_ID)
= (S1.SET_ID, S1.SKILL_ID)
GROUP BY EE.CAN_NUM,RR.SET_ID
HAVING SUM(SS.S_LEVEL) IS NULL
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #   Expect 21 rows.
    stmt = """select * from v ORDER BY 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s24')
    
    stmt = """drop   view v ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # ------------------------------
    #  Q01, customer's original query demonstrating it works if the final
    #  left join is removed.
    # ------------------------------
    
    #   Expect 21 rows.
    stmt = """SELECT E.CAN_NUM
--  EE.CAN_NUM, etc are not known to the outer query.
FROM expr E
WHERE E.CAN_NUM IN (100669,100677,100700,100081)
AND E.CAN_NUM NOT IN
(
SELECT EE.CAN_NUM
FROM require RR
JOIN expr EE
ON RR.JOB_ID = ?JOB
AND EE.CAN_NUM IN (100669,100677,100700, 100081)
LEFT JOIN sets1 SS
ON (EE.SET_ID, RR.SKILL_ID) = (SS.SET_ID, SS.SKILL_ID)
AND (RR.PRI = 0
OR (RR.PRI > 0 AND EE.EXPR >= RR.EXPR))
--         LEFT JOIN SETS1 S1
--              ON SS.S_LEVEL = S1.S_LEVEL
--              AND (RR.SET_ID, RR.SKILL_ID)
--                = (S1.SET_ID, S1.SKILL_ID)
GROUP BY EE.CAN_NUM,RR.SET_ID
HAVING SUM(SS.S_LEVEL) IS NULL
)
ORDER BY 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s25')
    
    stmt = """create view v as
SELECT E.CAN_NUM
-- EE.CAN_NUM, etc are not known to the outer query.
FROM expr E
WHERE E.CAN_NUM IN (100669,100677,100700,100081)
AND E.CAN_NUM NOT IN
(
SELECT EE.CAN_NUM
FROM require RR
JOIN expr EE
--             ON RR.JOB_ID = ?JOB
ON RR.JOB_ID = 'TEST'
AND EE.CAN_NUM IN (100669,100677,100700, 100081)
LEFT JOIN sets1 SS
ON (EE.SET_ID, RR.SKILL_ID) = (SS.SET_ID, SS.SKILL_ID)
AND (RR.PRI = 0
OR (RR.PRI > 0 AND EE.EXPR >= RR.EXPR))
GROUP BY EE.CAN_NUM,RR.SET_ID
HAVING SUM(SS.S_LEVEL) IS NULL
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #   Expect 21 rows.
    stmt = """select * from v ORDER BY 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s26')
    
    stmt = """drop   view v ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop   table expr;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop   table require;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop   table sets1;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test017(desc="""a18"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """drop table b8tab1;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table b8tab2;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table b8tab3;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table b8tab4;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table b8tab1 (col1 pic 9 not null) no partition;"""
    output = _dci.cmdexec(stmt)
    stmt = """create table b8tab2 
(col1 pic 9 not null
,col2 date not null) no partition;"""
    output = _dci.cmdexec(stmt)
    stmt = """CREATE TABLE b8tab3 (C1 PIC 9 NOT NULL,PRIMARY KEY (C1));"""
    output = _dci.cmdexec(stmt)
    stmt = """CREATE TABLE b8tab4 (C2 PIC 9 NOT NULL,
C3 DATE NOT NULL,
C4 DATE DEFAULT NULL,
PRIMARY KEY (C2));"""
    output = _dci.cmdexec(stmt)
    
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0149 : A18
    #  Description:        This test verifies the SQL OUTER JOIN
    #                      statements . Not converted completely because
    #                      of the use of DEFINES in this test.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    
    stmt = """insert into b8tab1 values (1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into b8tab1 values (2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into b8tab2 values (1, date '0001-01-01');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    #--BEGIN_DDL
    # we make views & select from them.
    stmt = """create view b8pv1 as select * from b8tab1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create view b8pv2 as select * from b8tab2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create view b8view1 (c1, c2) as
select b8pv1.col1, b8pv2.col2 from b8pv1 
left join b8pv2 on (b8pv1.col1 = b8pv2.col1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    # --END_DDL
    
    #   Expect 2 rows.
    stmt = """select * from b8view1 ORDER BY 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a18exp""", 'a18s0')
    
    #--BEGIN_DDL
    stmt = """drop   view b8view1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create view b8view2 (c1, c2) as
select b8pv1.col1, dateformat(b8pv2.col2, default) from b8pv1 
left join b8pv2 on (b8pv1.col1 = b8pv2.col1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    # --END_DDL
    
    #   Expect 2 rows.
    stmt = """select * from b8view2 ORDER BY 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a18exp""", 'a18s1')
    
    #--BEGIN_DDL
    stmt = """drop   view b8view2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #--END_DDL
    
    stmt = """INSERT INTO b8tab3 VALUES (1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO b8tab3 VALUES (2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO b8tab4 VALUES (1
,DATE '1910-10-10'
,NULL);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #  Expect 2 rows.
    stmt = """SELECT C1, C2, C3, C4
FROM b8tab3 LEFT JOIN b8tab4 ON C1 = C2
order by 1,2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a18exp""", 'a18s2')
    #
    #  DATETIME FUNCTIONS USED ON COLUMN C3 DEFINED NOT NULL
    #  NEXT 3 SELECTS
    #
    #  Expect 2 rows.
    stmt = """SELECT C1, C2,
DATEFORMAT (C3,DEFAULT),
C4
FROM b8tab3 LEFT JOIN b8tab4 ON C1 = C2
order by 1,2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a18exp""", 'a18s3')
    
    stmt = """SELECT C1, C2,
JULIANTIMESTAMP (C3),
C4
FROM b8tab3 LEFT JOIN b8tab4 ON C1 = C2
order by 1,2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a18exp""", 'a18s4')
    
    #  Expect 2 rows.
    stmt = """SELECT C1, C2,
DAYOFWEEK (C3),
C4
FROM b8tab3 LEFT JOIN b8tab4 ON C1 = C2
order by 1,2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a18exp""", 'a18s5')
    
    #  Expect 2 rows.
    stmt = """SELECT C1,C2,
EXTEND (C3),
C4
FROM b8tab3 LEFT JOIN b8tab4 ON C1 = C2
order by 1,2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a18exp""", 'a18s6')
    
    #
    #  DATETIME FUNCTIONS USED ON COLUMN C4 DEFINED WITH NULL
    #
    #  Expect 2 rows.
    stmt = """SELECT C1,C2,
C3,
DATEFORMAT (C4,DEFAULT),
JULIANTIMESTAMP (C4)   ,
DAYOFWEEK (C4),
EXTEND (C4)
FROM b8tab3 LEFT JOIN b8tab4 ON C1 = C2
order by 1,2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a18exp""", 'a18s7')
    
    #
    #  WORKAROUND: MAKE C3 PART OF AN EXPRESSION
    #
    #  Expect 2 rows.
    stmt = """SELECT C1,C2,
DATEFORMAT ((C3 + INTERVAL '0' YEAR),DEFAULT),
JULIANTIMESTAMP (C3 + INTERVAL '0' YEAR),
DAYOFWEEK (C3 + INTERVAL '0' YEAR),
C4
FROM b8tab3 LEFT JOIN b8tab4 ON C1 =C2
order by 1,2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a18exp""", 'a18s8')
    
    #
    # -----------------------------------------------
    #  Left join with not null on right of left join.
    #  All data types.  Include expressions in left side.
    # -----------------------------------------------
    
    #  delete define ** ;
    #  add define =t1, class map, file $global_A.btsel01 ;
    #  add define =t2, class map, file $global_A.btre201 ;
    #  add define =t3, class map, file $global_A.btre203 ;
    #  add define =t4, class map, file $global_A.btre204 ;
    
    stmt = """select t2.ALWAYSNULL , t2.CHAR_1     , t2.VAR_CHAR_3 ,
t2.PIC_COMP_3 , t2.binary_32_u , t2.ordering
from """ + gvars.g_schema_arkcasedb + """.btre201 t2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a18exp""", 'a18s9')
    stmt = """select t1.small_int , t1.var_char , t1.char_10
, t1.binary_32_u , t1.DECIMAL_2_SIGNED , t1.DECIMAL_3_UNSIGNED
from """ + gvars.g_schema_arkcasedb + """.btsel01 t1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a18exp""", 'a18s10')
    
    stmt = """select t2.ALWAYSNULL , t1.small_int from """ + gvars.g_schema_arkcasedb + """.btre201 t2 LEFT JOIN """ + gvars.g_schema_arkcasedb + """.btsel01 t1 on
t2.ALWAYSNULL = t1.small_int
order by 1,2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a18exp""", 'a18s11')
    stmt = """select t2.CHAR_1     , t1.var_char  from """ + gvars.g_schema_arkcasedb + """.btre201 t2 LEFT JOIN """ + gvars.g_schema_arkcasedb + """.btsel01 t1 on
t2.CHAR_1     = t1.var_char
order by 1,2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a18exp""", 'a18s12')
    stmt = """select t2.CHAR_1     , t1.var_char  from """ + gvars.g_schema_arkcasedb + """.btre201 t2 LEFT JOIN """ + gvars.g_schema_arkcasedb + """.btsel01 t1 on
t2.CHAR_1     = cast(t1.small_int as varchar(20))
order by 1,2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a18exp""", 'a18s13')
    stmt = """select t2.VAR_CHAR_3 , t1.char_10 from """ + gvars.g_schema_arkcasedb + """.btre201 t2 LEFT JOIN """ + gvars.g_schema_arkcasedb + """.btsel01 t1 on
t2.VAR_CHAR_3 = t1.char_10
order by 1,2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a18exp""", 'a18s14')
    stmt = """select t2.PIC_COMP_3 , t1.binary_32_u from """ + gvars.g_schema_arkcasedb + """.btre201 t2 LEFT JOIN """ + gvars.g_schema_arkcasedb + """.btsel01 t1 on
t2.PIC_COMP_3 = t1.binary_32_u
order by 1,2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a18exp""", 'a18s15')
    stmt = """select t2.binary_32_u , t1.DECIMAL_3_UNSIGNED from """ + gvars.g_schema_arkcasedb + """.btre201 t2 LEFT JOIN """ + gvars.g_schema_arkcasedb + """.btsel01 t1 on
t2.binary_32_u = t1.DECIMAL_3_UNSIGNED
order by 1,2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a18exp""", 'a18s16')
    stmt = """select t2.ordering , t1.DECIMAL_2_SIGNED from """ + gvars.g_schema_arkcasedb + """.btre201 t2 LEFT JOIN """ + gvars.g_schema_arkcasedb + """.btsel01 t1 on
t2.ordering = t1.DECIMAL_2_SIGNED
order by 1,2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a18exp""", 'a18s17')
    
    #  Use Table BTRE203 - a table with fewer columns than btre201,
    #                      and some NOT NULL columns;
    
    #  Float, not null on right:
    #  Table BTRE203
    #     , col_float2         float (5)                not null
    stmt = """select t2.ordering from """ + gvars.g_schema_arkcasedb + """.btre201 t2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a18exp""", 'a18s18')
    stmt = """select t3.col_varchar from """ + gvars.g_schema_arkcasedb + """.btre203 t3 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """select t2.ordering , t3.col_varchar from """ + gvars.g_schema_arkcasedb + """.btre201 t2 LEFT JOIN """ + gvars.g_schema_arkcasedb + """.btre203 t3 on
t2.float_basic = t3.col_float2
order by 1,2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a18exp""", 'a18s19')
    
    #  Date, not null on right:
    #  Table BTRE204
    #     , y_to_d              datetime year to day    not null
    stmt = """select t2.y_to_d from """ + gvars.g_schema_arkcasedb + """.btre201 t2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a18exp""", 'a18s20')
    stmt = """select t4.y_to_d from """ + gvars.g_schema_arkcasedb + """.btre204 t4 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a18exp""", 'a18s21')
    stmt = """select t2.y_to_d , t4.y_to_d     from """ + gvars.g_schema_arkcasedb + """.btre201 t2 LEFT JOIN """ + gvars.g_schema_arkcasedb + """.btre204 t4 on
t2.y_to_d = t4.y_to_d
order by 1,2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a18exp""", 'a18s22')
    stmt = """select t2.y_to_d , t4.y_to_d
, dateformat (t2.y_to_d,default)
, dateformat( t4.y_to_d , default)
from """ + gvars.g_schema_arkcasedb + """.btre201 t2 LEFT JOIN """ + gvars.g_schema_arkcasedb + """.btre204 t4 on
dateformat (t2.y_to_d,default)
= dateformat( t4.y_to_d , default)
order by 1,2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a18exp""", 'a18s23')
    stmt = """select t2.y_to_d , t4.y_to_d
, DayOfWeek ( t2.y_to_d ) , DayOfWeek ( t4.y_to_d )
from """ + gvars.g_schema_arkcasedb + """.btre201 t2 LEFT JOIN """ + gvars.g_schema_arkcasedb + """.btre204 t4 on
DayOfWeek (t2.y_to_d) = DayOfWeek( t4.y_to_d)
order by 1,2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a18exp""", 'a18s24')
    stmt = """select t2.y_to_d , t4.y_to_d
, JulianTimestamp ( t2.y_to_d ) , JulianTimestamp ( t4.y_to_d )
from """ + gvars.g_schema_arkcasedb + """.btre201 t2 LEFT JOIN """ + gvars.g_schema_arkcasedb + """.btre204 t4 on
JulianTimestamp (t2.y_to_d) = JulianTimestamp( t4.y_to_d)
order by 1,2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a18exp""", 'a18s25')
    
    #  Time, not null on right:
    #  Table BTRE204
    #     , h_to_f              datetime hour to fraction(3) not null
    stmt = """select t2.h_to_f from """ + gvars.g_schema_arkcasedb + """.btre201 t2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a18exp""", 'a18s26')
    stmt = """select t4.h_to_f from """ + gvars.g_schema_arkcasedb + """.btre204 t4 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a18exp""", 'a18s27')
    stmt = """select t2.h_to_f , t4.h_to_f , tx.h_to_f
from """ + gvars.g_schema_arkcasedb + """.btre201 t2 LEFT JOIN """ + gvars.g_schema_arkcasedb + """.btre204 t4 on
t2.h_to_f    = t4.h_to_f
--                LEFT JOIN btre204 t4 tx on
LEFT JOIN """ + gvars.g_schema_arkcasedb + """.btre204 tx on
t2.h_to_f   <> tx.h_to_f
order by 1,2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a18exp""", 'a18s28')
    
    #  Interval, not null on right:
    #  Table BTRE204
    #     , iy_to_mo            interval year(4) to month  not null
    #     , ih_to_s             interval hour to second not null
    stmt = """select t2.iy_to_mo from """ + gvars.g_schema_arkcasedb + """.btre201 t2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a18exp""", 'a18s29')
    stmt = """select t2.ih_to_s  from """ + gvars.g_schema_arkcasedb + """.btre201 t2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a18exp""", 'a18s30')
    stmt = """select t2.iy_to_mo from """ + gvars.g_schema_arkcasedb + """.btre201 t2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a18exp""", 'a18s31')
    stmt = """select t4.iy_to_mo from """ + gvars.g_schema_arkcasedb + """.btre204 t4 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a18exp""", 'a18s32')
    stmt = """select t2.iy_to_mo , t2.ih_to_s
, t4.iy_to_mo , t4.ih_to_s      from """ + gvars.g_schema_arkcasedb + """.btre201 t2 LEFT JOIN """ + gvars.g_schema_arkcasedb + """.btre204 t4 on
( t2.iy_to_mo , t2.ih_to_s )
= ( t4.iy_to_mo , t4.ih_to_s )
order by 1,2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a18exp""", 'a18s33')
    
    stmt = """drop view b8pv1;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop view b8pv2;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop view b8view1;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop view b8view2;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """drop table b8tab4;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table b8tab3;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table b8tab2;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table b8tab1;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test018(desc="""a20"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #  Test unit SQLT149, case n2.
    
    stmt = """drop table n2table1;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table n2table2;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table n2table3;"""
    output = _dci.cmdexec(stmt)
    
    #  Extension of tests on 29 March 1990 to test for bug reported in
    stmt = """CREATE TABLE  n2table1 ( x int, y int) no partition;"""
    output = _dci.cmdexec(stmt)
    stmt = """CREATE TABLE  n2table2 ( y int, z int) no partition;"""
    output = _dci.cmdexec(stmt)
    stmt = """CREATE TABLE  n2table3 ( z int, w int) no partition;"""
    output = _dci.cmdexec(stmt)
    #  VIEW between two tables:
    stmt = """CREATE VIEW n2view1 ( y, z, w ) AS
SELECT n2table2.y, n2table2.z, n2table3.w
FROM   n2table2  , n2table3 
WHERE  n2table2.z = n2table3.z
;"""
    output = _dci.cmdexec(stmt)
    
    #  ----3
    stmt = """INSERT INTO   n2table3 VALUES ( 200,3 ) ;"""
    output = _dci.cmdexec(stmt)
    stmt = """SELECT * FROM n2table3 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a20exp""", 'a20s0')
    stmt = """SELECT * FROM n2view1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """SELECT * FROM n2table1 left join n2view1 on
( n2table1.y = n2view1.y) ;"""
    output = _dci.cmdexec(stmt)
    #  --2-3
    stmt = """INSERT INTO   n2table2 VALUES ( 10,100) ;"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO   n2table2 VALUES ( 20,200) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """SELECT * FROM n2table2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a20exp""", 'a20s1')
    stmt = """SELECT * FROM n2view1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a20exp""", 'a20s2')
    stmt = """SELECT * FROM n2table1 left join n2view1 on
( n2table1.y = n2view1.y) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    #  1-2-3
    stmt = """INSERT INTO   n2table1 VALUES ( 1,10) ;"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO   n2table1 VALUES ( 1,20) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """SELECT * FROM n2table1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a20exp""", 'a20s3')
    stmt = """SELECT * FROM n2view1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a20exp""", 'a20s4')
    stmt = """SELECT * FROM n2table1 left join n2view1 on
( n2table1.y = n2view1.y) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 2)
    #  1---3
    
    stmt = """DROP VIEW n2view1;"""
    output = _dci.cmdexec(stmt)
    stmt = """DROP TABLE    n2table2 ;"""
    output = _dci.cmdexec(stmt)
    stmt = """CREATE TABLE  n2table2 ( y int, z int) no partition;"""
    output = _dci.cmdexec(stmt)
    stmt = """CREATE VIEW n2view1 ( y, z, w ) AS
SELECT n2table2.y, n2table2.z, n2table3.w
FROM   n2table2  , n2table3 
WHERE  n2table2.z = n2table3.z
;"""
    output = _dci.cmdexec(stmt)
    stmt = """SELECT * FROM n2view1;"""
    output = _dci.cmdexec(stmt)
    stmt = """SELECT * FROM n2table1 left join n2view1 on
( n2table1.y = n2view1.y) ;"""
    output = _dci.cmdexec(stmt)
    #  1----
    stmt = """DROP VIEW n2view1;"""
    output = _dci.cmdexec(stmt)
    stmt = """DROP TABLE    n2table3 ;"""
    output = _dci.cmdexec(stmt)
    stmt = """CREATE TABLE  n2table3 ( z int, w int) no partition;"""
    output = _dci.cmdexec(stmt)
    stmt = """CREATE VIEW n2view1 ( y, z, w ) AS
SELECT n2table2.y, n2table2.z, n2table3.w
FROM   n2table2  , n2table3 
WHERE  n2table2.z = n2table3.z
;"""
    output = _dci.cmdexec(stmt)
    stmt = """SELECT * FROM n2view1;"""
    output = _dci.cmdexec(stmt)
    stmt = """SELECT * FROM n2table1 left join n2view1 on
( n2table1.y = n2view1.y) ;"""
    output = _dci.cmdexec(stmt)
    #  1-2--
    stmt = """INSERT INTO   n2table2 VALUES ( 10,100) ;"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO   n2table2 VALUES ( 20,200) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """SELECT * FROM n2table2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a20exp""", 'a20s5')
    stmt = """SELECT * FROM n2view1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """SELECT * FROM n2table1 left join n2view1 on
( n2table1.y = n2view1.y) ;"""
    output = _dci.cmdexec(stmt)
    #   --2--
    stmt = """DROP TABLE    n2table1 ;"""
    output = _dci.cmdexec(stmt)
    stmt = """CREATE TABLE  n2table1 ( x int, y int) no partition;"""
    output = _dci.cmdexec(stmt)
    stmt = """SELECT * FROM n2table1 ;"""
    output = _dci.cmdexec(stmt)
    stmt = """SELECT * FROM n2view1;"""
    output = _dci.cmdexec(stmt)
    stmt = """SELECT * FROM n2table1 left join n2view1 on
( n2table1.y = n2view1.y) ;"""
    output = _dci.cmdexec(stmt)
    
    #    PURGE ! n2view* ;
    #    PURGE ! n2table* ;
    
    _testmgr.testcase_end(desc)

def test019(desc="""n01"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    #  Create & populate additional tables; then attempt to JOIN 17
    #  tables (i.e., one over the limit):
    stmt = """create table n1table1 
( pic_comp_2   pic sv9(2) comp   not null
, data_x3     pic x(3)          not null
, primary key (pic_comp_2)
)
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table n1table2 
( pic_comp_2   pic sv9(2) comp   not null
, data_x3     pic x(3)          not null
, primary key (pic_comp_2)
)
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table n1table3 
( pic_comp_2   pic sv9(2) comp   not null
, data_x3     pic x(3)          not null
, primary key (pic_comp_2)
)
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table n1table4 
( pic_comp_2   pic sv9(2) comp   not null
, data_x3     pic x(3)          not null
, primary key (pic_comp_2)
)
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table n1tablea (col_n smallint) no partition ;"""
    output = _dci.cmdexec(stmt)
    stmt = """create constraint JOIN on n1tablea.col_1 check col_n > 99 ;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create constraint INNER on n1tablea.col_1 check col_n > 99 ;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table n1tableb ( INNER smallint) ;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table n1tablec ( LEFT  smallint) ;"""
    output = _dci.cmdexec(stmt)
    
    #  OUTER JOIN is not legal for a protection view:
    stmt = """create view n1view1 (c1, s1, c2, s2) as
select """ + gvars.g_schema_arkcasedb + """.customer.city ,
 """ + gvars.g_schema_arkcasedb + """.customer.state
, """ + gvars.g_schema_arkcasedb + """.supplier.city , """ + gvars.g_schema_arkcasedb + """.supplier.state
from """ + gvars.g_schema_arkcasedb + """.customer 
left join """ + gvars.g_schema_arkcasedb + """.supplier 
on """ + gvars.g_schema_arkcasedb + """.customer.state = """ + gvars.g_schema_arkcasedb + """.supplier.state
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create view n1view2 (c1, s1, c , s ) as
select """ + gvars.g_schema_arkcasedb + """.customer.city ,
 """ + gvars.g_schema_arkcasedb + """.customer.state
, """ + gvars.g_schema_arkcasedb + """.supplier.city , """ + gvars.g_schema_arkcasedb + """.supplier.state
from """ + gvars.g_schema_arkcasedb + """.customer 
left join """ + gvars.g_schema_arkcasedb + """.supplier 
on """ + gvars.g_schema_arkcasedb + """.customer.state = """ + gvars.g_schema_arkcasedb + """.supplier.state
;"""
    output = _dci.cmdexec(stmt)
    
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0149 : N01
    #  Description:        This test verifies the SQL JOIN
    #                      statements. Negative test.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    #
    
    #   RIGHT JOIN not supported Release 2 (C30L).
    stmt = """select        a.city,        a.state
,        b.city,        b.state
from       """ + gvars.g_schema_arkcasedb + """.customer a
right join """ + gvars.g_schema_arkcasedb + """.supplier b
on """ + gvars.g_schema_arkcasedb + """.customer.city = """ + gvars.g_schema_arkcasedb + """.supplier.city
order by 1, 2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4002')
    
    #   Syntax-related errors.
    
    #   LEFT JOIN with missing right-hand reference:
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.parts 
left join ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #   RIGHT JOIN with missing left-hand reference:
    stmt = """right join """ + gvars.g_schema_arkcasedb + """.parts ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #   LEFT & RIGHT JOIN with bad syntax in ON clause:
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.parts 
left join  """ + gvars.g_schema_arkcasedb + """.odetail 
on """ + gvars.g_schema_arkcasedb + """.parts.partnum ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #   (Correlation names used here to avoid error -4060 for R2.)
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.parts   a
right join """ + gvars.g_schema_arkcasedb + """.odetail b
on """ + gvars.g_schema_arkcasedb + """.odetail.partnum ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #   LEFT JOIN with omitted ON clause:
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.parts 
left join  """ + gvars.g_schema_arkcasedb + """.odetail 
--      on NOTHING !!!!!!
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #   Attempt to JOIN nonexistent tables:
    stmt = """select """ + gvars.g_schema_arkcasedb + """.btsel12.data_x3
from """ + gvars.g_schema_arkcasedb + """.btsel12 
join notable
on   """ + gvars.g_schema_arkcasedb + """.btsel12.data_93       = notable.data_93
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4082')
    stmt = """select """ + gvars.g_schema_arkcasedb + """.btsel12.data_x3
from notable
left join """ + gvars.g_schema_arkcasedb + """.btsel12 
on   """ + gvars.g_schema_arkcasedb + """.btsel12.data_93       = notable.data_93
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4082')
    stmt = """select """ + gvars.g_schema_arkcasedb + """.btsel12.data_x3
from notable1
join notable2
on   notable1.data_93       = notable2.data_93
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4082')
    
    stmt = """insert into n1tablea values ( 1 ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into n1tablea values ( 123 ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """select * from n1tablea ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n01exp""", 'n01s9')
    
    #   Reserved word rejected for column name:
    stmt = """insert into n1tableb values ( 1 ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4082')
    stmt = """insert into n1tablec values ( 123 ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4082')
    stmt = """select INNER from n1tableb ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """select LEFT from n1tablec ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #   Reserved word rejected for correlation name:
    
    stmt = """select LEFT.partnum from """ + gvars.g_schema_arkcasedb + """.parts LEFT ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """select RIGHT.partnum from """ + gvars.g_schema_arkcasedb + """.parts RIGHT ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #   Reserved word LEFT and JOIN are NOT rejected for statement name.
    #   While LEFT and JOIN should be rejected when parsed by the
    #   SQL parser (such as when issued from SQLCOBOL), they are
    #   are accepted here because only SQLCI Reserved words are
    #   restricted.
    #
    stmt = """prepare LEFT from
select partnum from """ + gvars.g_schema_arkcasedb + """.parts ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n01exp""", 'n01s16')
    stmt = """execute LEFT ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n01exp""", 'n01s17')
    stmt = """prepare JOIN from
select partnum from """ + gvars.g_schema_arkcasedb + """.parts ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n01exp""", 'n01s18')
    stmt = """execute JOIN ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n01exp""", 'n01s19')
    stmt = """show prepared LEFT ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n01exp""", 'n01s20')
    stmt = """show prepared JOIN ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n01exp""", 'n01s21')
    
    stmt = """show prepared;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n01exp""", 'n01s21a')
    
    stmt = """insert into n1table1 values ( 0.22,'pin' ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into n1table2 values ( 0.22,'pin' ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into n1table3 values ( 0.22,'pin' ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into n1table4 values ( 0.22,'pin' ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    #  Attempt to JOIN 17 tables (i.e., one over the limit):
    
    stmt = """select """ + gvars.g_schema_arkcasedb + """.btsel12.data_x3
, """ + gvars.g_schema_arkcasedb + """.btsel12.data_93
, """ + gvars.g_schema_arkcasedb + """.btsel15.small_int
, """ + gvars.g_schema_arkcasedb + """.btsel18.binary_signed
, """ + gvars.g_schema_arkcasedb + """.btsel23.pic_comp_2
, n1table4.data_x3
from """ + gvars.g_schema_arkcasedb + """.btsel12 
join """ + gvars.g_schema_arkcasedb + """.btsel13 
on   """ + gvars.g_schema_arkcasedb + """.btsel12.data_93       = """ + gvars.g_schema_arkcasedb + """.btsel13.data_93
join """ + gvars.g_schema_arkcasedb + """.btsel14 
on   """ + gvars.g_schema_arkcasedb + """.btsel13.data_93       = """ + gvars.g_schema_arkcasedb + """.btsel14.data_93
join """ + gvars.g_schema_arkcasedb + """.btsel15 
on   """ + gvars.g_schema_arkcasedb + """.btsel14.data_93       = """ + gvars.g_schema_arkcasedb + """.btsel15.data_93
join """ + gvars.g_schema_arkcasedb + """.btsel16 
on   """ + gvars.g_schema_arkcasedb + """.btsel15.small_int     = """ + gvars.g_schema_arkcasedb + """.btsel16.small_int
join """ + gvars.g_schema_arkcasedb + """.btsel17 
on   """ + gvars.g_schema_arkcasedb + """.btsel16.small_int     = """ + gvars.g_schema_arkcasedb + """.btsel17.small_int
join """ + gvars.g_schema_arkcasedb + """.btsel18 
on   """ + gvars.g_schema_arkcasedb + """.btsel17.small_int     = """ + gvars.g_schema_arkcasedb + """.btsel18.small_int
join """ + gvars.g_schema_arkcasedb + """.btsel19 
on   """ + gvars.g_schema_arkcasedb + """.btsel18.binary_signed = """ + gvars.g_schema_arkcasedb + """.btsel19.binary_signed
join """ + gvars.g_schema_arkcasedb + """.btsel20 
on   """ + gvars.g_schema_arkcasedb + """.btsel19.binary_signed = """ + gvars.g_schema_arkcasedb + """.btsel20.binary_signed
join """ + gvars.g_schema_arkcasedb + """.btsel21 
on   """ + gvars.g_schema_arkcasedb + """.btsel20.binary_signed = """ + gvars.g_schema_arkcasedb + """.btsel21.binary_signed
join """ + gvars.g_schema_arkcasedb + """.btsel22 
on   """ + gvars.g_schema_arkcasedb + """.btsel21.pic_comp_2    = """ + gvars.g_schema_arkcasedb + """.btsel22.pic_comp_2
join """ + gvars.g_schema_arkcasedb + """.btsel23 
on   """ + gvars.g_schema_arkcasedb + """.btsel22.pic_comp_2    = """ + gvars.g_schema_arkcasedb + """.btsel23.pic_comp_2
join """ + gvars.g_schema_arkcasedb + """.btsel24 
on   """ + gvars.g_schema_arkcasedb + """.btsel22.pic_comp_2    = """ + gvars.g_schema_arkcasedb + """.btsel24.pic_comp_2
join n1table1 
on   """ + gvars.g_schema_arkcasedb + """.btsel24.pic_comp_2    = n1table1.pic_comp_2
join n1table2 
on   """ + gvars.g_schema_arkcasedb + """.btsel24.pic_comp_2    = n1table2.pic_comp_2
join n1table3 
on   """ + gvars.g_schema_arkcasedb + """.btsel24.pic_comp_2    = n1table3.pic_comp_2
join n1table4 
on   """ + gvars.g_schema_arkcasedb + """.btsel24.pic_comp_2    = n1table4.pic_comp_2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    #   Errors related to semantics of ON clause.
    
    #   Ambiguous column reference:
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.parts 
left join  """ + gvars.g_schema_arkcasedb + """.odetail 
on partnum = partnum
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4004')
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.parts 
left join  """ + gvars.g_schema_arkcasedb + """.odetail 
on """ + gvars.g_schema_arkcasedb + """.parts.partnum = partnum
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4004')
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.parts 
left join  """ + gvars.g_schema_arkcasedb + """.odetail 
on partnum = """ + gvars.g_schema_arkcasedb + """.odetail.partnum
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4004')
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.parts 
left join  """ + gvars.g_schema_arkcasedb + """.odetail 
on partnum = """ + gvars.g_schema_arkcasedb + """.parts.partnum
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4004')
    
    #   Column referenced does not exist:
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.parts 
left join  """ + gvars.g_schema_arkcasedb + """.odetail 
on """ + gvars.g_schema_arkcasedb + """.parts.partnum = """ + gvars.g_schema_arkcasedb + """.odetail.nocolumn
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4003')
    
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.parts 
left join  """ + gvars.g_schema_arkcasedb + """.odetail 
on """ + gvars.g_schema_arkcasedb + """.parts.nocolumn = """ + gvars.g_schema_arkcasedb + """.odetail.partnum
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4003')
    
    #   Reference nonlocal column:
    
    #   ?????????
    #   ??? See p6 of ES - nested query?
    #   ?????????
    
    stmt = """select """ + gvars.g_schema_arkcasedb + """.customer.city , """ + gvars.g_schema_arkcasedb + """.customer.state
, """ + gvars.g_schema_arkcasedb + """.supplier.city , """ + gvars.g_schema_arkcasedb + """.supplier.state
from """ + gvars.g_schema_arkcasedb + """.customer 
left join """ + gvars.g_schema_arkcasedb + """.supplier 
on """ + gvars.g_schema_arkcasedb + """.customer.state = """ + gvars.g_schema_arkcasedb + """.supplier.state
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n01exp""", 'n01s28')
    
    stmt = """select * from n1view1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n01exp""", 'n01s29')
    
    #   Cannot have a grouping imposed on any column involved in the
    #   left join:
    stmt = """select * from n1view2 group by s ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4012')
    
    #   Cannot apply aggregate function to any column involved in the
    #   left join:
    stmt = """select min (c1) from n1view2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n01exp""", 'n01s31')
    stmt = """select min (s1) from n1view2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n01exp""", 'n01s32')
    stmt = """select min (c ) from n1view2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n01exp""", 'n01s33')
    stmt = """select min (s ) from n1view2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n01exp""", 'n01s34')
    
    #  OUTER JOIN is not legal for a protection view:
    stmt = """drop view n1view1;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """drop view n1view2;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """drop table n1table1 ;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table n1table2 ;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table n1table3 ;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table n1table4 ;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table n1tablea ;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop constraint JOIN on n1tablea.col_1 check col_n > 99 ;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """drop constraint INNER on n1tablea.col_1 check col_n > 99 ;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """drop table n1tableb  ;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """drop table n1tablec ;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test020(desc="""n02"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    # Extension of tests on 29 March 1990 to test for bug reported in
    stmt = """drop view n2view1;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """drop table n2table1;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table n2table2;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table n2table3;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE  n2table1 ( x int, y int) no partition;"""
    output = _dci.cmdexec(stmt)
    stmt = """CREATE TABLE  n2table2 ( y int, z int) no partition;"""
    output = _dci.cmdexec(stmt)
    stmt = """CREATE TABLE  n2table3 ( z int, w int) no partition;"""
    output = _dci.cmdexec(stmt)
    
    #  VIEW between two tables:
    stmt = """CREATE VIEW n2view1 ( y, z, w ) AS
SELECT n2table2.y, n2table2.z, n2table3.w
FROM   n2table2  , n2table3 
WHERE  n2table2.z = n2table3.z
;"""
    output = _dci.cmdexec(stmt)
    
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0149 : N02
    #  Description:        This test verifies the SQL OUTER JOIN
    #                      statements
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    #
    
    stmt = """INSERT INTO   n2table3 VALUES ( 200,3 ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """SELECT * FROM n2table3 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n02exp""", 'n02s0')
    stmt = """SELECT * FROM n2view1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """SELECT * FROM n2table1 left join n2view1 on
( n2table1.y = n2view1.y) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    #  --2-3
    stmt = """INSERT INTO   n2table2 VALUES ( 10,100) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO   n2table2 VALUES ( 20,200) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """SELECT * FROM n2table2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n02exp""", 'n02s1')
    stmt = """SELECT * FROM n2view1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n02exp""", 'n02s2')
    stmt = """SELECT * FROM n2table1 left join n2view1 on
( n2table1.y = n2view1.y) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    #  1-2-3
    stmt = """INSERT INTO   n2table1 VALUES ( 1,10) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO   n2table1 VALUES ( 1,20) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """SELECT * FROM n2table1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n02exp""", 'n02s3')
    stmt = """SELECT * FROM n2view1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n02exp""", 'n02s4')
    stmt = """SELECT * FROM n2table1 left join n2view1 on
( n2table1.y = n2view1.y) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n02exp""", 'n02s5')
    
    # --BEGIN_DDL
    
    #   1---3
    stmt = """drop view n2view1;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """DROP TABLE    n2table2 ;"""
    output = _dci.cmdexec(stmt)
    stmt = """DROP VIEW     n2view1;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE  n2table2 ( y int, z int) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """CREATE VIEW n2view1 ( y, z, w ) AS
SELECT n2table2.y, n2table2.z, n2table3.w
FROM   n2table2  , n2table3 
WHERE  n2table2.z = n2table3.z
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    # --END_DDL
    
    stmt = """SELECT * FROM n2view1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """SELECT * FROM n2table1 left join n2view1 on
( n2table1.y = n2view1.y) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n02exp""", 'n02s10')
    
    # --BEGIN_DDL
    
    #   1----
    stmt = """drop view n2view1;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """DROP TABLE    n2table3 ;"""
    output = _dci.cmdexec(stmt)
    stmt = """CREATE TABLE  n2table3 ( z int, w int) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """CREATE VIEW n2view1 ( y, z, w ) AS
SELECT n2table2.y, n2table2.z, n2table3.w
FROM   n2table2  , n2table3 
WHERE  n2table2.z = n2table3.z
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    # --END_DDL
    
    stmt = """SELECT * FROM n2view1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """SELECT * FROM n2table1 left join n2view1 on
( n2table1.y = n2view1.y) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n02exp""", 'n02s15')
    
    #  1-2--
    stmt = """INSERT INTO   n2table2 VALUES ( 10,100) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO   n2table2 VALUES ( 20,200) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """SELECT * FROM n2table2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n02exp""", 'n02s16')
    stmt = """SELECT * FROM n2view1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """SELECT * FROM n2table1 left join n2view1 on
( n2table1.y = n2view1.y) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n02exp""", 'n02s18')
    
    #--BEGIN_DDL
    
    #  --2--
    stmt = """DROP TABLE    n2table1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """CREATE TABLE  n2table1 ( x int, y int) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #--END_DDL
    
    stmt = """SELECT * FROM n2table1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """SELECT * FROM n2view1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """SELECT * FROM n2table1 left join n2view1 on
( n2table1.y = n2view1.y) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    # Extension of tests on 29 March 1990 to test for bug reported in
    stmt = """drop VIEW n2view1;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop TABLE  n2table1  ;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop TABLE  n2table2  ;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop TABLE  n2table3  ;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

