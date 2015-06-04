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
    #  Description:        SELECTs on a single table using multivalued
    #                      predicates.
    #                      This is a positive multivalued predicate
    #                      test using SELECTs on a single table.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    #  Notes:
    #
    # =================== End Test Case Header  ===================
    
    #  Query 1
    #      SELECTs with WHERE clauses using COMPARISON
    #      predicates (one using a subquery).
    #      -- add parentheses to where clause 3/29/90
    
    stmt = """SELECT *  FROM """ + gvars.g_schema_arkcasedb + """.btsel18 
WHERE (binary_signed, small_int, data_93)
>  (-1000, 6000, 400)
ORDER BY binary_signed;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s0')
    
    #  Query 2
    #      This should use index BTSEL18a
    stmt = """SELECT small_int, syskey FROM """ + gvars.g_schema_arkcasedb + """.btsel18 
WHERE (small_int, syskey)
>  (6001, 2)
ORDER BY syskey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 6)
    
    #  Query 3
    #      SELECTs with WHERE clauses using BETWEEN
    #      predicates (one using a subquery).
    stmt = """SELECT *  FROM """ + gvars.g_schema_arkcasedb + """.btsel07 
WHERE (pic_x_b, pic_x_c)
BETWEEN ('D', 'en')
AND  ('Z', 'jn')
ORDER BY pic_x_b, pic_x_a, pic_x_c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s2')
    
    #  Query 4
    stmt = """SELECT *  FROM """ + gvars.g_schema_arkcasedb + """.btsel09 
WHERE (pic_x_a, pic_x_2, pic_x_3, pic_x_4, pic_x_5,
pic_x_6, pic_x_7)
NOT BETWEEN ('box', 'here', 'R', 'debby', 5, 11, 50)
AND  ('why', 'gone', 'R', 'billy', 7, 15, 30)
ORDER BY pic_x_a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s3')
    
    #  Query 5
    #      SELECTs with HAVING clauses using COMPARISON
    #      and BETWEEN predicates.
    stmt = """SELECT data_x3, AVG(data_93)
FROM """ + gvars.g_schema_arkcasedb + """.btsel12 
GROUP BY data_x3
HAVING data_x3
BETWEEN 'g' AND 's'
ORDER BY data_x3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s4')
    
    #  Query 6
    stmt = """SELECT pic_x_a, SUM(pic_x_5 - pic_x_6 + pic_x_7)
FROM """ + gvars.g_schema_arkcasedb + """.btsel09 
GROUP BY pic_x_a, pic_x_2, pic_x_3, pic_x_4,
pic_x_5, pic_x_6, pic_x_7
HAVING (pic_x_a, pic_x_2, pic_x_3, pic_x_4, pic_x_5,
pic_x_6, pic_x_7)
BETWEEN ('box', 'bill', 'A', 'BILL', 0, 0, 0)
AND  ('why', 'over', 'Y', 'tommy', 7, 90, 100)
ORDER BY pic_x_a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s5')
    
    stmt = """SELECT *
FROM """ + gvars.g_schema_arkcasedb + """.btsel09 
WHERE (pic_x_a, pic_x_2, pic_x_3, pic_x_4, pic_x_5,
pic_x_6, pic_x_7)
BETWEEN ('box', 'bill', 'A', 'BILL', 0, 0, 0)
AND  ('why', 'over', 'Y', 'tommy', 7, 90, 100)
ORDER BY pic_x_a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s6')
    
    stmt = """SELECT pic_x_a, SUM(pic_x_5 - pic_x_6 + pic_x_7)
FROM """ + gvars.g_schema_arkcasedb + """.btsel09 
GROUP BY pic_x_a
HAVING pic_x_a
BETWEEN 'box'
AND  'why'
ORDER BY pic_x_a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s7')
    
    #  Query 7
    stmt = """SELECT pic_x_a, SUM(pic_x_5 - pic_x_6 + pic_x_7)
FROM """ + gvars.g_schema_arkcasedb + """.btsel09 
GROUP BY pic_x_a
HAVING pic_x_a
BETWEEN 'box' AND  'why';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s8')
    
    #  Query 8
    stmt = """SELECT pic_x_a, SUM(pic_x_5 - pic_x_6 + pic_x_7)
FROM """ + gvars.g_schema_arkcasedb + """.btsel09 
GROUP BY pic_x_a
HAVING pic_x_a
BETWEEN 'box' AND  'why'
ORDER BY pic_x_a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s9')
    
    #  Query 9
    #      SELECT with HAVING and WHERE clauses
    stmt = """SELECT data_x3, MIN(data_93) FROM """ + gvars.g_schema_arkcasedb + """.btsel12 
WHERE (data_93, data_x3)
>=   (400, 'sun')
GROUP BY data_x3, data_93
HAVING (data_x3, data_93)
BETWEEN ('nun', 700)
AND  ('ton', 900)
ORDER BY data_x3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s10')
    
    stmt = """SELECT data_x3, MIN(data_93)
FROM """ + gvars.g_schema_arkcasedb + """.btsel12 
WHERE (data_93, data_x3) >=   (400, 'sun')
GROUP BY  data_x3
HAVING data_x3 BETWEEN 'nun' and 'ton'
ORDER BY data_x3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s11')
    
    #  Query 10
    #      Specify many (41) expressions for a row-
    #      value specification.
    stmt = """SELECT pic_x_a FROM """ + gvars.g_schema_arkcasedb + """.btsel06 
WHERE (pic_x_a,
pic_x_b,
pic_x_c,
col_1,
col_2,
col_3,
col_4,
col_5,
col_6,
col_7,
col_8,
col_9,
col_10,
col_21,
col_22,
col_23,
col_24,
col_25,
col_26,
col_27,
col_28,
col_29,
col_30,
col_41,
col_42,
col_43,
col_44,
col_45,
col_46,
col_47,
col_48,
col_61,
col_62,
col_63,
col_64,
col_65,
col_66,
col_67,
col_68,
col_69,
col_70)
<=
('joe',
'A',
'jo',
100,
1000,
200,
1000,
1000,
50,
1000,
1000,
1000,
1000,
1000,
1000,
1000,
1000,
1000,
1000,
1000,
1000,
1000,
1000,
1000.00,
1000.00,
1000.00,
1000.00,
1000.00,
1000.00,
1000.00,
1000.00,
1000,
1000,
1000,
1000,
1000,
1000,
1000,
1000,
1000,
1000)
ORDER BY pic_x_a;"""
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
    #  Test case name:     A02
    #  Description:        SELECTs on a views using multivalued
    #                      predicates.
    #                      This is a positive multivalued predicate
    #                      test using SELECTs on a view.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    #  Notes:
    #  This test case incorporates features detailed in the "Title"
    #  by Ima Programmer (Version 1.1, <date>).
    #
    # =================== End Test Case Header  ===================
    
    #    **  SELECTs with WHERE clauses using COMPARISON  **
    #    **  and BETWEEN predicates.                      **
    stmt = """SELECT decimal_10, char_10, pic_9_7, pic_x_7, pic_x_a
FROM """ + gvars.g_schema_arkcasedb + """.svsel01 
WHERE (decimal_10, char_10, pic_9_7, pic_x_7, pic_x_a)
<=  (10000, 'outside', 50, 'who', 'd')
ORDER BY decimal_10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s0')
    
    stmt = """SELECT * FROM """ + gvars.g_schema_arkcasedb + """.svsel11 
WHERE (col_1, col_2, col_3, col_4, col_5, col_6, col_7, col_8)
BETWEEN (1000,  999,  9000,  4, 'C', '7', 80, 'michael')
AND  (8000, 1000, 10000, 3, 'B', '9',  90, '7')
ORDER BY col_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s1')
    
    stmt = """SELECT * FROM """ + gvars.g_schema_arkcasedb + """.svsel19 
WHERE (data_x3, data_93, small_int)
BETWEEN ('bob', 200, 2000)
AND  ('tom', 100, 1000)
ORDER BY data_x3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s2')
    
    #    **  SELECTs with HAVING clauses using COMPARISON  **
    #    **  and BETWEEN predicates.                       **
    stmt = """SELECT data_x3, MAX(data_93 + small_int)  FROM """ + gvars.g_schema_arkcasedb + """.svsel16 
GROUP BY data_x3, small_int, data_x3
HAVING (data_93, small_int, data_x3)
>   (200, 2000, 'boa')
ORDER BY data_x3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4005')
    
    stmt = """SELECT data_x3, MAX(data_93 + small_int)  FROM """ + gvars.g_schema_arkcasedb + """.svsel16 
GROUP BY data_x3
HAVING data_x3
>  'boa'
ORDER BY data_x3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s4')
    
    stmt = """SELECT data_x3, COUNT(DISTINCT data_93)  FROM """ + gvars.g_schema_arkcasedb + """.svsel19 
GROUP BY data_x3, data_93, small_int,
binary_signed, pic_comp_2
HAVING (data_x3, data_93, small_int, binary_signed, pic_comp_2)
NOT BETWEEN ('bob', 200, 2000,  8000, -.25)
AND  ('tom', 100, 1000, -5001,  .12)
ORDER BY data_x3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s5')
    
    stmt = """SELECT data_x3, COUNT(DISTINCT data_93)  FROM """ + gvars.g_schema_arkcasedb + """.svsel19 
GROUP BY data_x3
HAVING data_x3
NOT BETWEEN 'bob' AND  'tom'
ORDER BY data_x3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    _testmgr.testcase_end(desc)

def test003(desc="""a03"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     A03
    #  Description:        SELECTs on a multiple tables using
    #                      multivalued predicates.
    #                      This is a positive multivalued predicate
    #                      test using SELECTs on multiple tables.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    #  Notes:
    #  This test case incorporates features detailed in the "Title"
    #  by Ima Programmer (Version 1.1, <date>).
    #
    # =================== End Test Case Header  ===================
    
    #    **  SELECTs with WHERE clauses using COMPARISON  **
    #    **  predicates (one using a subquery).           **
    
    stmt = """SELECT * FROM """ + gvars.g_schema_arkcasedb + """.btsel12, """ + gvars.g_schema_arkcasedb + """.btsel16 
WHERE (""" + gvars.g_schema_arkcasedb + """.btsel12.data_x3, """ + gvars.g_schema_arkcasedb + """.btsel12.data_93)
> ('nun', 600)
AND (""" + gvars.g_schema_arkcasedb + """.btsel16.small_int, """ + gvars.g_schema_arkcasedb + """.btsel16.data_93)
BETWEEN (500,  166)
AND  (1500, 168)
ORDER BY """ + gvars.g_schema_arkcasedb + """.btsel12.data_x3, """ + gvars.g_schema_arkcasedb + """.btsel12.data_93, """ + gvars.g_schema_arkcasedb + """.btsel16.small_int;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s0')
    
    stmt = """SELECT * FROM """ + gvars.g_schema_arkcasedb + """.btsel12, """ + gvars.g_schema_arkcasedb + """.btsel13 
WHERE (""" + gvars.g_schema_arkcasedb + """.btsel12.data_x3, """ + gvars.g_schema_arkcasedb + """.btsel12.data_93, """ + gvars.g_schema_arkcasedb + """.btsel13.data_93)
=  ('tom', """ + gvars.g_schema_arkcasedb + """.btsel13.data_93, 100)
ORDER BY """ + gvars.g_schema_arkcasedb + """.btsel12.data_x3, """ + gvars.g_schema_arkcasedb + """.btsel12.data_93;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s1')
    
    stmt = """SELECT * FROM """ + gvars.g_schema_arkcasedb + """.btsel13, """ + gvars.g_schema_arkcasedb + """.btsel14 
WHERE (""" + gvars.g_schema_arkcasedb + """.btsel13.data_93, """ + gvars.g_schema_arkcasedb + """.btsel14.data_93)
=  (SELECT 100, data_93 FROM """ + gvars.g_schema_arkcasedb + """.btsel12)
ORDER BY """ + gvars.g_schema_arkcasedb + """.btsel13.data_93, """ + gvars.g_schema_arkcasedb + """.btsel14.data_93;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8401')
    
    stmt = """SELECT * FROM """ + gvars.g_schema_arkcasedb + """.btsel13, """ + gvars.g_schema_arkcasedb + """.btsel14 
WHERE (""" + gvars.g_schema_arkcasedb + """.btsel13.data_93, """ + gvars.g_schema_arkcasedb + """.btsel14.data_93)
=  (SELECT DISTINCT 100, data_93 FROM """ + gvars.g_schema_arkcasedb + """.btsel12)
ORDER BY """ + gvars.g_schema_arkcasedb + """.btsel13.data_93, """ + gvars.g_schema_arkcasedb + """.btsel14.data_93;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8401')
    
    #    **  SELECTs with WHERE clauses using BETWEEN  **
    #    **  predicates.
    stmt = """SELECT * FROM """ + gvars.g_schema_arkcasedb + """.btsel19, """ + gvars.g_schema_arkcasedb + """.btsel20 
WHERE (""" + gvars.g_schema_arkcasedb + """.btsel19.data_93, """ + gvars.g_schema_arkcasedb + """.btsel20.data_93)
BETWEEN (412, 422)
AND  (413, 423)
ORDER BY """ + gvars.g_schema_arkcasedb + """.btsel19.binary_signed, """ + gvars.g_schema_arkcasedb + """.btsel19.data_93, """ + gvars.g_schema_arkcasedb + """.btsel20.data_93;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s4')
    
    stmt = """SELECT * FROM """ + gvars.g_schema_arkcasedb + """.btsel18, """ + gvars.g_schema_arkcasedb + """.btsel13 
WHERE (""" + gvars.g_schema_arkcasedb + """.btsel13.data_93, """ + gvars.g_schema_arkcasedb + """.btsel18.small_int, """ + gvars.g_schema_arkcasedb + """.btsel18.binary_signed)
NOT BETWEEN (401, 6000+1, 1001*2)
AND	    (408, 6006-1, 4012/2)
ORDER BY """ + gvars.g_schema_arkcasedb + """.btsel18.small_int, """ + gvars.g_schema_arkcasedb + """.btsel18.data_93, """ + gvars.g_schema_arkcasedb + """.btsel13.data_93;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s5')
    
    #    **  SELECTs with HAVING clauses using COMPARISON  **
    #    **  and BETWEEN predicates.                       **
    
    stmt = """SELECT """ + gvars.g_schema_arkcasedb + """.btsel09.pic_x_4, """ + gvars.g_schema_arkcasedb + """.btsel09.pic_x_a, """ + gvars.g_schema_arkcasedb + """.btsel09.pic_x_5, """ + gvars.g_schema_arkcasedb + """.btsel25.pic_x_3,
AVG(""" + gvars.g_schema_arkcasedb + """.btsel09.pic_x_7), COUNT(*)
FROM """ + gvars.g_schema_arkcasedb + """.btsel09, """ + gvars.g_schema_arkcasedb + """.btsel25 
GROUP BY """ + gvars.g_schema_arkcasedb + """.btsel09.pic_x_4, """ + gvars.g_schema_arkcasedb + """.btsel09.pic_x_5,
 """ + gvars.g_schema_arkcasedb + """.btsel09.pic_x_a, """ + gvars.g_schema_arkcasedb + """.btsel25.pic_x_3
HAVING (""" + gvars.g_schema_arkcasedb + """.btsel09.pic_x_5, """ + gvars.g_schema_arkcasedb + """.btsel25.pic_x_3)
=   (7,""" + gvars.g_schema_arkcasedb + """.btsel09.pic_x_a)
ORDER BY """ + gvars.g_schema_arkcasedb + """.btsel09.pic_x_4, """ + gvars.g_schema_arkcasedb + """.btsel09.pic_x_5,
 """ + gvars.g_schema_arkcasedb + """.btsel09.pic_x_a, """ + gvars.g_schema_arkcasedb + """.btsel25.pic_x_3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s6')
    
    stmt = """SELECT """ + gvars.g_schema_arkcasedb + """.btsel22.data_93, """ + gvars.g_schema_arkcasedb + """.btsel23.data_93, SUM(""" + gvars.g_schema_arkcasedb + """.btsel22.pic_comp_2),
SUM(""" + gvars.g_schema_arkcasedb + """.btsel23.pic_comp_2)  FROM """ + gvars.g_schema_arkcasedb + """.btsel22, """ + gvars.g_schema_arkcasedb + """.btsel23 
GROUP BY """ + gvars.g_schema_arkcasedb + """.btsel22.data_93, """ + gvars.g_schema_arkcasedb + """.btsel23.data_93
HAVING (""" + gvars.g_schema_arkcasedb + """.btsel22.data_93, """ + gvars.g_schema_arkcasedb + """.btsel23.data_93)
BETWEEN (438, 446)
AND  (440, 447)
ORDER BY """ + gvars.g_schema_arkcasedb + """.btsel22.data_93, """ + gvars.g_schema_arkcasedb + """.btsel23.data_93;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s7')
    
    #    **  SELECT with HAVING and WHERE clauses  **
    stmt = """SELECT """ + gvars.g_schema_arkcasedb + """.btsel24.data_x3, """ + gvars.g_schema_arkcasedb + """.btsel25.pic_x_3, SUM(""" + gvars.g_schema_arkcasedb + """.btsel24.pic_comp_2)
FROM """ + gvars.g_schema_arkcasedb + """.btsel24, """ + gvars.g_schema_arkcasedb + """.btsel25 
WHERE (""" + gvars.g_schema_arkcasedb + """.btsel24.data_x3, """ + gvars.g_schema_arkcasedb + """.btsel25.pic_x_1)
>  ( 'tom', 'M')
GROUP BY """ + gvars.g_schema_arkcasedb + """.btsel24.data_x3, """ + gvars.g_schema_arkcasedb + """.btsel25.pic_x_3
HAVING (""" + gvars.g_schema_arkcasedb + """.btsel24.data_x3, """ + gvars.g_schema_arkcasedb + """.btsel25.pic_x_3)
BETWEEN ('bob', 'a')
AND  ('ton', 'z')
ORDER BY """ + gvars.g_schema_arkcasedb + """.btsel24.data_x3, """ + gvars.g_schema_arkcasedb + """.btsel25.pic_x_3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s8')
    
    _testmgr.testcase_end(desc)

def test004(desc="""a04"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     A04
    #  Description:        S04 testing SELECTs on a single table
    #                      using multivalued predicates with negative
    #                      key values.
    #                      This is a positive multivalued predicate test
    #                      using SELECTs on a single table with negative
    #                      key values.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    #  Notes:
    #  This test case incorporates features detailed in the "Title"
    #  by Ima Programmer (Version 1.1, <date>).
    #
    # =================== End Test Case Header  ===================
    
    #   A negative value that is truncated to compare with
    #   a key may cause qualifying rows to be eliminated
    #   from a select.  This was fixed as part of S04.
    #   end.
    
    stmt = """drop   table a4table;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table a4table 
(int_1       smallint default 0 not null
,int_2       smallint default 0 not null
,int_3       smallint default 0 not null
,primary key (int_1, int_2, int_3)
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into a4table values (1, 1, 3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a4table values (1, 1, 2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a4table values (1, 1, 1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a4table values (1, 1, 0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a4table values (1, 1, -1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a4table values (1, 1, -2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a4table values (1, 1, -3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a4table values (1, 1, -4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select int_1, int_2, int_3 from a4table order by 1,2,3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s1')
    
    stmt = """select int_1, int_2, int_3 from a4table 
where int_1 = 1 and int_2 = 1 and int_3 < -2.5  order by 1,2,3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s2')
    
    stmt = """select int_1, int_2, int_3 from a4table 
where int_1 = 1 and int_2 = 1 and int_3 > -2.5  order by 1,2,3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s3')
    
    stmt = """select int_1, int_2, int_3 from a4table 
where int_1 = 1 and int_2 = 1 and int_3 >= -2.5 order by 1,2,3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s4')
    
    stmt = """select int_1, int_2, int_3 from a4table 
where int_1 = 1 and int_2 = 1 and int_3 <= -2.5 order by 1,2,3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s5')
    
    stmt = """select int_1, int_2, int_3 from a4table 
where int_1 = 1 and int_2 = 1 and int_3 > -0.5 order by 1,2,3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s6')
    
    stmt = """select int_1, int_2, int_3 from a4table 
where int_1 = 1 and int_2 = 1 and int_3 <  2.5 order by 1,2,3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s7')
    
    stmt = """select int_1, int_2, int_3 from a4table 
where int_1 = 1 and int_2 = 1 and int_3 >  2.5 order by 1,2,3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s8')
    
    stmt = """drop table a4table;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test005(desc="""a05"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     A05
    #  Description:        SELECT with multiple instances of same
    #                      parameter in multivalued predicates.
    #                      This is a positive multivalued predicate
    #                      test.
    #
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    #  Notes:
    #  This test case incorporates features detailed in the "Title"
    #  by Ima Programmer (Version 1.1, <date>).
    #
    # =================== End Test Case Header  ===================
    
    
    stmt = """drop table a5table1;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table a5table1 
( ref_num     largeint
, z_text      char(3)
, emp_num     smallint
) no partition
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into a5table1 values (100,'abc',99);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a5table1 values (100,'abd',99);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a5table1 values (100,'abe',99);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a5table1 values (100,'abc',100);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a5table1 values (100,'abd',100);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a5table1 values (100,'abe',100);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a5table1 values (100,'abc',101);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a5table1 values (100,'abd',101);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a5table1 values (100,'abe',101);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a5table1 values (100,'abb',null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a5table1 values (100,'abc',null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a5table1 values (100,'abd',null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a5table1 values (100,'abe',null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a5table1 values (100,null,99);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a5table1 values (100,null,100);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a5table1 values (100,null,101);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a5table1 values (200,'abc',200);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a5table1 values (200,'abd',200);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a5table1 values (200,'abe',200);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    #  Without parameters:
    stmt = """select * from a5table1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s0')
    
    stmt = """select * from a5table1 
where (ref_num, z_text, emp_num =
100,'abd',100) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s1')
    
    # With parameters:
    stmt = """set param ?p0 100;"""
    output = _dci.cmdexec(stmt)
    stmt = """prepare q1 from
select * from a5table1 
where (ref_num, z_text, emp_num =
?p0,'abd',?p0)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """execute q1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s2')
    #- 1 row should have been selected
    
    stmt = """set param ?p0 100;"""
    output = _dci.cmdexec(stmt)
    stmt = """prepare q2 from
select * from a5table1 
where (ref_num, z_text, emp_num >
?p0,'abd',?p0)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """execute q2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s3')
    #- 8 rows should have been selected
    
    stmt = """set param ?p0 100;"""
    output = _dci.cmdexec(stmt)
    stmt = """prepare q3 from
select * from a5table1 
where (ref_num, z_text, emp_num >=
?p0,'abd',?p0)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """execute q3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s4')
    #- 9 rows should have been selected
    
    stmt = """set param ?p0 100;"""
    output = _dci.cmdexec(stmt)
    stmt = """prepare q4 from
select * from a5table1 
where (ref_num, z_text, emp_num <
?p0,'abd',?p0)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """execute q4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s5')
    #- 6 rows should have been selected
    
    stmt = """set param ?p0 100;"""
    output = _dci.cmdexec(stmt)
    stmt = """prepare q5 from
select * from a5table1 
where (ref_num, z_text, emp_num <=
?p0,'abd',?p0)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """execute q5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s6')
    #- 7 rows should have been selected
    
    # Introduce some indexes:
    
    stmt = """create index a5iraea on
 a5table1 (ref_num asc,
z_text,
emp_num asc)
-- catalog
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index a5iraed on
 a5table1 (ref_num asc,
z_text,
emp_num desc)
-- catalog
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index a5irdea on
 a5table1 (ref_num desc,
z_text,
emp_num asc)
-- catalog
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index a5irded on
 a5table1 (ref_num desc,
z_text,
emp_num desc)
-- catalog
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """set param ?p0 100;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p1 200;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare q6 from
select * from a5table1 
where (ref_num, z_text, emp_num) between (?p0,'abd',?p0)
and (?p1,'abd',?p1) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """execute q6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s7')
    #- 8 rows should have been selected
    
    stmt = """set param ?p0 100;"""
    output = _dci.cmdexec(stmt)
    stmt = """prepare q7 from
select * from a5table1 
where ref_num = ?p0
and z_text  = 'abd'
and emp_num <= ?p0
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """execute q7;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s8')
    #- 2 rows should have been selected
    
    #  Cleanup objects:
    stmt = """drop table a5table1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test006(desc="""a06"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     A06
    #  Description:        SELECT with BETWEEN and '>' in multivalued
    #                      predicates.
    #                      This is a positive multivalued predicate
    #                      test.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    #  Notes:
    #  This test case incorporates features detailed in the "Title"
    #  by Ima Programmer (Version 1.1, <date>).
    #
    # =================== End Test Case Header  ===================
    
    #   Cleanup objects that may be laying around
    
    stmt = """drop   table a6table1;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop   table a6table2;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table a6table1 
(char_10     char (10)  default ' ' not null
,pic_x_7     pic x(07)  default ' ' not null
,int_1       smallint   default 0   not null
,primary key (char_10, pic_x_7, int_1)
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into a6table1 
values ('charlene' , 'brown',   1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a6table1 
values ('claire'   , 'green',   0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a6table1 
values ('samuel'   , 'red',     1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a6table1 
values ('johnny'   , 'orange',  2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a6table1 
values ('jennifer' , 'purple', -3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a6table1 
values ('elizabeth', 'black',   1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select * from a6table1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s2')
    
    stmt = """prepare s from
select char_10, pic_x_7, int_1 from a6table1 
where (char_10, pic_x_7, int_1)
BETWEEN ('c',     'b',     0)
AND     ('r',     'q',     3)
AND   (char_10, pic_x_7, int_1)
>       ('c',     'b',     0)
order by
char_10, pic_x_7, int_1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s3')
    
    # 5 rows should have been selected
    
    stmt = """create table a6table2 
(author      char (10)  default ' ' not null
,title       pic x(30)  default ' ' not null
,int_1       smallint   default 0   not null
)
store by (title,author)
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into a6table2 
values ('Kozol' , 'Illiterate America',   1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a6table2 
values ('Dr. Seuss' , 'Green Eggs and Ham', 100);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a6table2 
values ('Steinbeck' , 'Of Mice and Men', 100);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a6table2 
values ('Hemmingway' , 'The Old Man and the Sea', 77);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a6table2 
values ('Kafka' , 'Metamorphisis', 26217);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select * from a6table2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s4')
    
    stmt = """set param  ?p0 0;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param  ?p1 Kozol;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param  ?p2 0;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param  ?p3 Kozol;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param  ?p4 'Illiterate America';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param  ?p5 Kozol;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param  ?p6 2115025792699988973;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s from
select syskey,* from a6table2 
where (int_1 = ?p0 and author = ?p1
and int_1,author <= ?p2,?p3
and title,author,syskey > ?p4,?p5,?p6)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    # 0  rows should have been selected
    
    #  Cleanup objects:
    stmt = """drop   table a6table1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop   table a6table2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test007(desc="""a07"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     A07
    #  Description:        SELECT with table with index using multivalued
    #                      predicates.
    #                      This is a positive multivalued predicate test.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    #  Notes:
    #  This test case incorporates features detailed in the "Title"
    #  by Ima Programmer (Version 1.1, <date>).
    #
    # =================== End Test Case Header  ===================
    
    stmt = """DROP VIEW  a7view1;"""
    output = _dci.cmdexec(stmt)
    stmt = """DROP TABLE a7table1;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table a7table1 
(char_09   char (09) not null
,char_07   char (07) not null
,char_06   char (06) not null
,primary key (char_09, char_07)
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """CREATE INDEX a7indx1 
ON a7table1 (char_07)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """CREATE VIEW a7view1 AS
SELECT *
from a7table1 
WHERE (char_06, char_09, char_07) > ('11111', ' ', ' ')
AND char_06 <= '~~~~~'
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into a7table1 values ('         ' , '       ', '      ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a7table1 values ('111111111' , '1111111', '111111');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a7table1 values ('BBBBBBBBB' , 'BBBBBBB', 'BBBBBB');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a7table1 values ('ccccccccc' , 'ccccccc', 'cccccc');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a7table1 values ('~~~~~~~~'  , '~~~~~~~', '~~~~~~');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a7table1 values ('         ' , '>>>>>>>', '^^^^^^');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a7table1 values ('/////////' , '       ', 'pppppp');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """prepare s1 from
select *
from a7table1 
WHERE (char_06, char_09, char_07) > ('11111', ' ', ' ')
AND char_06 <= '~~~~~';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #  The incorrect behavior returned only 4 rows.
    
    stmt = """EXECUTE s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s2')
    
    #  The incorrect behavior returned only 4 rows.
    
    stmt = """SELECT * from a7view1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s3')
    
    stmt = """DROP INDEX a7indx1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """prepare s1 from
select *
from a7table1 
WHERE char_06, char_09, char_07 > '11111', ' ', ' '
AND char_06 <= '~~~~~';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #  Without the index, the correct number of rows are returned.
    stmt = """EXECUTE s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s4')
    
    #  Without the index, the correct number of rows are returned.
    stmt = """SELECT * from a7view1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s5')
    
    #  Cleanup objects:
    
    stmt = """DROP VIEW  a7view1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """DROP TABLE a7table1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test008(desc="""a08"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     A08
    #  Description:        INSERTs into tables using comparison
    #                      and between predicates.
    #                      This is a positive multivalued predicate test
    #                      executing INSERTs into tables.
    #
    #                      This test unit has its own table, B1TABLE
    #                      instead of reusing TABLE - not all inserts are
    #                      removed!
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    #  Notes:
    #  This test case incorporates features detailed in the "Title"
    #  by Ima Programmer (Version 1.1, <date>).
    #
    # =================== End Test Case Header  ===================
    
    stmt = """drop table b1table;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE b1table 
(data_x3 pic x(3) default ' ' not null,
data_93 pic 9(3) default  0  not null) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #    INSERTs with WHERE clauses using COMPARISON
    #    predicates (one using a subquery).
    
    stmt = """SELECT pic_x_a, pic_x_7
FROM """ + gvars.g_schema_arkcasedb + """.btsel09 
WHERE (pic_x_a, pic_x_2, pic_x_7)
=  ('box',   'here',  50) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s0')
    
    stmt = """INSERT INTO b1table 
(SELECT pic_x_a, pic_x_7
FROM """ + gvars.g_schema_arkcasedb + """.btsel09 
WHERE (pic_x_a, pic_x_2, pic_x_7)
=  ('box',   'here',  50));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """SELECT data_x3, data_93
FROM """ + gvars.g_schema_arkcasedb + """.btsel23,
 """ + gvars.g_schema_arkcasedb + """.btsel24 
WHERE (data_x3, data_93)
BETWEEN ('kim', 440)
AND  ('kin', 442)
ORDER BY data_x3, data_93;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s1')
    
    
    stmt = """INSERT INTO b1table 
(SELECT data_x3, data_93
FROM """ + gvars.g_schema_arkcasedb + """.btsel23,
 """ + gvars.g_schema_arkcasedb + """.btsel24 
WHERE (data_x3, data_93)
BETWEEN ('kim', 440)
AND  ('kin', 442));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 2)
    
    
    stmt = """INSERT INTO b1table 
(SELECT pic_x_a, 100
FROM """ + gvars.g_schema_arkcasedb + """.btsel10 
WHERE (pic_x_a, binary_unsigned)
>  (SELECT 'rob', MAX(pic_x_6)
FROM """ + gvars.g_schema_arkcasedb + """.btsel09));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 5)
    #      Display the results of the inserts
    stmt = """SELECT * FROM b1table 
ORDER BY data_x3, data_93;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s2')
    
    stmt = """DROP TABLE b1table ;"""
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
    #  Description:        DELETE from tables using comparison
    #                      and between predicates.
    #                      This is a positive multivalued predicate
    #                      test which DELETE rows from tables.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    #  Notes:
    #  This test case incorporates features detailed in the "Title"
    #  by Ima Programmer (Version 1.1, <date>).
    #
    # =================== End Test Case Header  ===================
    
    stmt = """drop table tableA09;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table tableA09 (
data_x3                pic x(3) default ' ' not null
, data_93                pic 9(3) default 0   not null
, primary key ( data_x3 )
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index tablA09a 
on tableA09 ( data_93 )
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    # stmt = """BEGIN WORK;"""
    # output = _dci.cmdexec(stmt)
    # _dci.expect_complete_msg(output)
 
    stmt = """insert into tableA09 values ('tom',100);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tableA09 values ('bob',200);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tableA09 values ('run',300);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tableA09 values ('sun',400);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tableA09 values ('fun',500);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tableA09 values ('gun',600);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tableA09 values ('nun',700);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tableA09 values ('pun',800);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    #  update statistics for table tableA09;
    stmt = """select * from tableA09;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s1')
    
    #   **  INSERTs with WHERE clauses using COMPARISON  **
    #   **  predicates (one using a subquery).           **
    stmt = """DELETE FROM tableA09 
WHERE (data_x3, data_93)
=  ('nun',   700);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    stmt = """DELETE FROM tableA09 
WHERE (data_x3, data_93)
BETWEEN ('art', 400)
AND  ('fun', 500);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 2)
    
    stmt = """DELETE FROM tableA09 
WHERE (data_x3, data_93)
= (SELECT DISTINCT pic_x_a, data_93
FROM """ + gvars.g_schema_arkcasedb + """.btsel11,
 """ + gvars.g_schema_arkcasedb + """.btsel13 
WHERE (pic_x_a, data_93)
=  ('bob',   200));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 0)
    
    #  12/31/98 HC  Added DISTINCT, one of the earlier test cases
    #               sometimes adds (or deletes) a bob/200 entry
    #  NOTE: bob/200 got deleted in the delete just before this delete
    
    #    **  Display the results of the deletes  **
    stmt = """SELECT * FROM tableA09 
ORDER BY data_x3, data_93;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s2')
    
    stmt = """drop table tableA09;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test010(desc="""a10"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     A10
    #  Description:        UPDATE from tableA10s using comparison
    #                      and between predicates.
    #                      This is a positive multivalued predicate
    #                      test which UPDATE rows from tableA10s.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    #  Notes:
    #  This test case incorporates features detailed in the "Title"
    #  by Ima Programmer (Version 1.1, <date>).
    #
    # =================== End Test Case Header  ===================
    
    stmt = """drop table tableA10;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table tableA10 (
data_x3                pic x(3) default ' ' not null
, data_93                pic 9(3) default 0   not null
, primary key ( data_x3 )
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index tablA10a 
on tableA10 ( data_93 )
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into tableA10 values ('tom',100);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tableA10 values ('bob',200);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tableA10 values ('run',300);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tableA10 values ('sun',400);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tableA10 values ('fun',500);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tableA10 values ('gun',600);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tableA10 values ('nun',700);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tableA10 values ('pun',800);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    #  update statistics for table tableA10;
    stmt = """select * from tableA10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s1')
    
    stmt = """BEGIN WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #   **  INSERTs with WHERE clauses using COMPARISON  **
    #   **  predicates (one using a subquery).           **
    stmt = """UPDATE tableA10 
SET data_93 = 777
WHERE (data_x3, data_93)
=  ('nun',   700);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """UPDATE tableA10 
SET data_93 = 999
WHERE (data_x3, data_93)
BETWEEN ('art', 400)
AND  ('fun', 500);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 2)
    
    stmt = """UPDATE tableA10 
SET data_x3 = 'ho', data_93 = 222
WHERE (data_x3, data_93)
= (SELECT pic_x_a, data_93
FROM """ + gvars.g_schema_arkcasedb + """.btsel11,
 """ + gvars.g_schema_arkcasedb + """.btsel13 
WHERE (pic_x_a, data_93)
=  ('bob',   200));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4033')
    
    #    **  Display the results of the updates  **
    stmt = """SELECT * FROM tableA10 
ORDER BY data_x3, data_93;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s3')
    
    #   **  Undo all updates  **
    stmt = """ROLLBACK WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop table tableA10;"""
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
    #  Test case name:     A11
    #  Description:        CREATE VIEWS on tables using comparison
    #                      and between predicates.
    #                      This is a positive multivalued predicate test
    #                      which CREATEs VIEWS on tables.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    #  Notes:
    #  This test case incorporates features detailed in the "Title"
    #  by Ima Programmer (Version 1.1, <date>).
    #
    # =================== End Test Case Header  ===================
    
    stmt = """drop table tableA11;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table tableA11 (
data_x3			pic x(3) default ' ' not null
,data_93			pic 9(3) default  0  not null
, primary key ( data_x3 )
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index idxA11 
on tableA11 ( data_93 )
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into tableA11 values ('tom',100);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tableA11 values ('bob',200);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tableA11 values ('run',300);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tableA11 values ('sun',400);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tableA11 values ('fun',500);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tableA11 values ('gun',600);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tableA11 values ('nun',700);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tableA11 values ('pun',800);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    #  update statistics for table tableA11;
    stmt = """select * from tableA11;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s1')
    
    #   **  INSERTs with WHERE clauses using COMPARISON  **
    #   **  predicates (one using a subquery).           **
    stmt = """CREATE VIEW view1 
AS SELECT * FROM tableA11 
WHERE (data_x3, data_93)
=  ('nun',   700);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """CREATE VIEW view2 
AS SELECT * FROM tableA11 
WHERE (data_x3, data_93)
BETWEEN ('art', 400)
AND  ('fun', 500);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """CREATE VIEW view3 
AS SELECT * FROM tableA11 
WHERE (data_x3, data_93)
= (SELECT DISTINCT  pic_x_a, data_93
FROM """ + gvars.g_schema_arkcasedb + """.btsel11,
 """ + gvars.g_schema_arkcasedb + """.btsel13 
WHERE (pic_x_a, data_93)
=  ('bob',   200));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #    catalog
    
    #    **  Display the resulting views  **
    stmt = """SELECT * FROM view1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s2')
    
    stmt = """SELECT * FROM view2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s3')
    #  NOTE: Between is a <= and >=, so correct to have fun,500
    
    stmt = """SELECT * FROM view3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s4')
    
    stmt = """create table tab1 
(flda    pic x(5) not null ,
fldb    pic x(5),
fldc    pic x(5),
fldd    pic x(5),
primary key (flda) );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table tab2 
(fldw    pic x(5) not null ,
fldx    pic x(5),
fldy    pic x(5),
fldz    pic x(5),
primary key (fldw) );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #  catalog
    #  organization key sequenced;
    
    # 12/31/98 HC  Added the following insert statements:
    
    stmt = """insert into tab1 values ('tom','rat', 'aaa', 'bob');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tab1 values ('ton','bat', 'bbb', 'hat');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tab1 values ('tim','fat', 'xyz', 'zzz');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into tab2 values ('sue','rat',  'aaa', 'bob');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tab2 values ('tom','cat',  'ety', 'bill');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tab2 values ('ton','bat',  'bbb', 'sat');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tab2 values ('zan','heat', 'dgh', 'bbb');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tab2 values ('abe','zat',  'xyz', 'zzz');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """create view view11 (fld1,fld2,fld3,fld4)
as select a.flda,a.fldb,b.fldy,b.fldz
from tab1 a, tab2 b
where (a.flda,a.fldb,a.fldc) = (b.fldw,b.fldx,b.fldy);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create view view12 (fld1,fld2,fld3,fld4)
as select a.flda,a.fldb,b.fldy,b.fldz
from tab1 a, tab2 b
where (a.flda,a.fldb,a.fldc <> b.fldw,b.fldx,b.fldy);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create view view13 (fld1,fld2,fld3,fld4)
as select a.flda,a.fldb,b.fldy,b.fldz
from tab1 a, tab2 b
where (a.flda,a.fldb,a.fldc) <= (b.fldw,b.fldx,b.fldy);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create view view14 (fld1,fld2,fld3,fld4)
as select a.flda,a.fldb,b.fldy,b.fldz
from tab1 a, tab2 b
where (a.flda,a.fldb,a.fldc >= b.fldw,b.fldx,b.fldy);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create view view15 (fld1,fld2,fld3,fld4)
as select a.flda,a.fldb,b.fldy,b.fldz
from tab1 a, tab2 b
where (a.flda,a.fldb,a.fldc) < (b.fldw,b.fldx,b.fldy);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create view view16 (fld1,fld2,fld3,fld4)
as select a.flda,a.fldb,b.fldy,b.fldz
from tab1 a, tab2 b
where (a.flda,a.fldb,a.fldc) > (b.fldw,b.fldx,b.fldy);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #    catalog
    
    stmt = """create view view22 (fld1,fld2,fld3,fld4)
as select a.flda,a.fldb,b.fldy,b.fldz
from tab1 a, tab2 b
where a.flda = b.fldw and
a.fldb = b.fldx and
a.fldc = b.fldy;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create view view23 (fld1,fld2,fld3,fld4)
as select a.flda,a.fldb,b.fldy,b.fldz
from tab1 a, tab2 b
where (a.flda,a.fldb) between
(a.fldc, b.fldw) AND (b.fldx, b.fldy);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create view view33 (fld1,fld2,fld3,fld4)
as select a.flda,a.fldb,b.fldy,b.fldz
from tab1 a, tab2 b
where a.flda,a.fldb,a.fldc is null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from view11 order by fld1, fld2, fld3, fld4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s5')
    stmt = """select * from view12 order by fld1, fld2, fld3, fld4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s6')
    stmt = """select * from view13 order by fld1, fld2, fld3, fld4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s7')
    stmt = """select * from view14 order by fld1, fld2, fld3, fld4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s8')
    stmt = """select * from view15 order by fld1, fld2, fld3, fld4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s9')
    stmt = """select * from view16 order by fld1, fld2, fld3, fld4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s10')
    stmt = """select * from view22 order by fld1, fld2, fld3, fld4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s11')
    stmt = """select * from view23 order by fld1, fld2, fld3, fld4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s12')
    stmt = """select * from view33 order by fld1, fld2, fld3, fld4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    # Clean up
    
    stmt = """drop view view1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view view2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view view3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view view11;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view view12;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view view13;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view view14;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view view15;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view view16;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view view22;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view view23;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view view33;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # NOTE: Because flda is defined as NOT NULL
    #       this should always be zero rows
    
    stmt = """drop index idxA11;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop table tableA11;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table tab1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table tab2;"""
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
    #  Test case name:     A12
    #  Description:        CREATE CONSTRAINTS on tables using
    #                      comparison and between predicates.
    #                      This is a positive multivalued predicate
    #                      test which CREATEs CONSTRAINTS on tables.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    #  Notes:
    #  This test case incorporates features detailed in the "Title"
    #  by Ima Programmer (Version 1.1, <date>).
    #
    # =================== End Test Case Header  ===================
    
    stmt = """drop table tableA12;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table tableA12 (
data_x3		pic x(3) default ' ' not null
, data_93		pic 9(3) default  0  not null
, primary key ( data_x3 )
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index tablA12a 
on tableA12 ( data_93 )
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into tableA12 values ('tom',100);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tableA12 values ('bob',200);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tableA12 values ('run',300);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tableA12 values ('sun',400);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tableA12 values ('fun',500);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tableA12 values ('gun',600);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tableA12 values ('nun',700);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tableA12 values ('pun',800);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    #  update statistics for table tableA12;
    stmt = """select * from tableA12;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s1')
    
    #   **  INSERTs with WHERE clauses using COMPARISON  **
    #   **  predicates (one using a subquery).           **
    
    stmt = """ALTER TABLE tableA12 ADD CONSTRAINT constr1
CHECK (data_x3, data_93 < 'y', 940);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """ALTER TABLE tableA12  ADD CONSTRAINT constr2
CHECK (data_x3, data_93 BETWEEN 'a', 50
AND 'z', 990);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #     CREATE CONSTRAINT constr3 ON tableA12
    #        CHECK data_x3, data_93
    #           >= (SELECT pic_x_a, data_93
    #                 FROM btsel11, btsel13
    #                 WHERE pic_x_a, data_93 = 'bar', 100);
    
    stmt = """INSERT INTO tableA12(data_x3, data_93)
VALUES ('zaz', 999);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8101')
    
    stmt = """INSERT INTO tableA12 (data_x3, data_93)
VALUES ('z', 910);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8101')
    
    stmt = """INSERT INTO tableA12 (data_x3, data_93)
VALUES ('a', 10);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8101')
    
    #    **  Display the resulting views  **
    #    SET STYLE VARCHAR_WIDTH 48;
    
    stmt = """select * from tableA12;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s5')
    
    stmt = """drop table tableA12;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test013(desc="""a13"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     A13
    #  Description:        NEGATIVE multivalued predicate test.
    #                      This is a negative multivalued predicate test.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    #  Notes:
    #  This test case incorporates features detailed in the "Title"
    #  by Ima Programmer (Version 1.1, <date>).
    #
    # =================== End Test Case Header  ===================
    
    #    **  Type mismatch between expessions in a row-  **
    #    **  value specification.                        **
    
    stmt = """SELECT * FROM """ + gvars.g_schema_arkcasedb + """.btsel07 
GROUP BY pic_x_a, pic_x_b, pic_x_c
HAVING (pic_x_a, pic_x_b, pic_x_c)
<   ('wig',   'G',     'P');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s0')
    
    #    **  Specify a subquery which returns more than  **
    #    **  one row.                                    **
    stmt = """SELECT * FROM """ + gvars.g_schema_arkcasedb + """.btsel02 
WHERE pic_x_1 = (
SELECT * FROM """ + gvars.g_schema_arkcasedb + """.btsel02 
WHERE pic_x_1 = 'B');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8401')
    
    #    **  Use a subquery as one of the row-value     **
    #    **  specifications in a BETWEEN predicate.     **
    
    stmt = """SELECT * FROM """ + gvars.g_schema_arkcasedb + """.btsel16 
WHERE (small_int, data_93)
BETWEEN (1500, 168)
AND  (8510, (SELECT MAX(data_93) FROM """ + gvars.g_schema_arkcasedb + """.btsel16));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s2')
    
    _testmgr.testcase_end(desc)

def test014(desc="""n13"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     N13
    #  Description:        NEGATIVE multivalued predicate test.
    #                      This is a negative multivalued predicate test.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    #  Notes:
    #  This test case incorporates features detailed in the "Title"
    #  by Ima Programmer (Version 1.1, <date>).
    #
    # =================== End Test Case Header  ===================
    
    stmt = """SELECT * FROM """ + gvars.g_schema_arkcasedb + """.btsel07 
HAVING (pic_x_a, pic_x_b, pic_x_c)
<   ('wig',   'G',     34);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4005')
    
    #    **  Specify a subquery which returns more than  **
    #    **  one row.                                    **
    stmt = """SELECT * FROM """ + gvars.g_schema_arkcasedb + """.btsel02 
WHERE pic_x_1 =
SELECT * FROM """ + gvars.g_schema_arkcasedb + """.btsel02 
WHERE pic_x_1 = 'B';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #    **  Use a subquery as one of the row-value     **
    #    **  specifications in a BETWEEN predicate.     **
    stmt = """SELECT * FROM """ + gvars.g_schema_arkcasedb + """.btsel16 
WHERE (small_int, data_93)
BETWEEN (1500, 168)
AND  (8510, SELECT MAX(data_93)) FROM """ + gvars.g_schema_arkcasedb + """.btsel16;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    _testmgr.testcase_end(desc)

