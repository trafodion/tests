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
    #  Test case name:     arkt0148 : A01
    #  Description:        This test verifies the SQL UNION
    #                      statement
    #                      Simple UNION SELECT from base tables.
    #  Includes:           All major data types.
    #                      Column names the same.
    #                      Columns of same-length either side of UNION.
    #                      Numbers of columns vary.
    #                      Some nonunique data values.
    #                      No NULL values.
    #                      ALL (to avoid intermediate values).
    #
    #                      Use order-entry database
    #
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    #
    
    #   UNION of same-length CHAR - 1-column operands:
    stmt = """select char_1 from """ + gvars.g_schema_arkcasedb + """.btsel01 
union all
select char_1 from """ + gvars.g_schema_arkcasedb + """.btre204 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s0')
    
    #   UNION of same-length VARCHAR - 1-column operands:
    stmt = """select var_char_3 from """ + gvars.g_schema_arkcasedb + """.btre204 
union all
select var_char_3 from """ + gvars.g_schema_arkcasedb + """.btre208 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s1')
    
    #   UNION of two pairs of same-length VARCHARs - 2-column operands:
    stmt = """select var_char_2, var_char_3 from """ + gvars.g_schema_arkcasedb + """.btre204 
union all
select var_char_2, var_char_3 from """ + gvars.g_schema_arkcasedb + """.btre208 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s2')
    
    #   UNION of two pairs of exact numerics with same precision and scale:
    stmt = """select pic_comp_3, pic_decimal_2 from """ + gvars.g_schema_arkcasedb + """.btre201 
union all
select pic_comp_3, pic_decimal_2 from """ + gvars.g_schema_arkcasedb + """.btre204 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s3')
    
    #   UNION of two pairs of approximate numeric (FLOAT) with same
    #   precision and scale - 2-column operands:
    stmt = """select float_basic, float_double_p from """ + gvars.g_schema_arkcasedb + """.btre204 
union all
select float_basic, float_double_p from """ + gvars.g_schema_arkcasedb + """.btre201 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s4')
    
    #   UNION of DATETIME with same startdate and same enddate - 1-column
    #   operands:
    stmt = """select y_to_d from """ + gvars.g_schema_arkcasedb + """.btre204 
union all
select y_to_d from """ + gvars.g_schema_arkcasedb + """.btre208 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s5')
    
    #   UNION of INTERVAL with same startdate and same enddate - 1-column
    #   operands:
    stmt = """select ih_to_s from """ + gvars.g_schema_arkcasedb + """.btre204 
union all
select ih_to_s from """ + gvars.g_schema_arkcasedb + """.btre208 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s6')
    
    # 04/08/09 added order by
    #   UNION of a table with itself:
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.btsel01 
union all
select * from """ + gvars.g_schema_arkcasedb + """.btsel01 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s7')
    
    _testmgr.testcase_end(desc)

def test002(desc="""a02"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0148 : A02
    #  Description:        This test verifies the SQL UNION
    #                      statement
    #                      UNION SELECT with columns of differing
    #                      lengths; ORDER BY.
    #  Includes:           Column names differ.
    #                      Columns of differing lengths either side of UNION.
    #                      HEADING (Release 2 extension) on columns.
    #                      NULLs on left-side, right-side,both sides of UNION
    #                      Other keywords -
    #                         GROUP BY (which causes intermediate results);
    #                         ORDER BY;
    #                         lock consistency;
    #                         lock mode.
    #                      Mostly without ALL (to force intermediate
    #                         results).
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    #
    #  Query 1
    #   UNION of CHARs with left-side of UNION longer than right-side -
    #   column names differ - ORDER BY ordinal column 1:
    stmt = """select pic_x_8 from """ + gvars.g_schema_arkcasedb + """.btre204 
union
select char_1  from """ + gvars.g_schema_arkcasedb + """.btsel01 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s0')
    
    #  Query 2
    #   UNION of CHARs with left-side of UNION shorter than right-side -
    #   ALL - column names differ - ORDER BY column name from left-side:
    stmt = """select char_1  from """ + gvars.g_schema_arkcasedb + """.btsel01 
union all
select pic_x_8 from """ + gvars.g_schema_arkcasedb + """.btre204 
order by char_1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s1')
    
    #  Query 3
    #   UNION of VARCHARs with left-side of UNION longer than right-side -
    #   - column names differ - ORDER BY column names from left-side:
    stmt = """select var_char_3 from """ + gvars.g_schema_arkcasedb + """.btre204 
union all
select var_char_2 from """ + gvars.g_schema_arkcasedb + """.btre204 
order by var_char_3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s2')
    
    #  Query 4
    #   UNION of VARCHARs with left-side of UNION shorter than right-side
    #   column names differ - ORDER BY column names from left-side:
    stmt = """select var_char_2, var_char_3 from """ + gvars.g_schema_arkcasedb + """.btre204 
union all
select var_char_2, var_char_3 from """ + gvars.g_schema_arkcasedb + """.btre204 
order by var_char_2, var_char_3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s3')
    
    #  Query 5
    #   UNION of SMALLINT and INTEGER:
    stmt = """select small_int from """ + gvars.g_schema_arkcasedb + """.btsel01 
union all
select medium_int from """ + gvars.g_schema_arkcasedb + """.btre204 
order by small_int
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s4')
    
    #  Query 6
    #   UNION of SMALLINT and LARGEINT - NULLs on both sides of UNION.
    stmt = """select small_int from """ + gvars.g_schema_arkcasedb + """.btre201 
union
select large_int from """ + gvars.g_schema_arkcasedb + """.btre202 
order by small_int
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s5')
    
    #  Query 7
    #   UNION of INTEGER and SMALLINT:
    stmt = """select medium_int from """ + gvars.g_schema_arkcasedb + """.btre204 
union
select small_int  from """ + gvars.g_schema_arkcasedb + """.btsel01 
order by medium_int
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s6')
    
    #  Query 8
    #   UNION of INTEGER and LARGEINT - NULLs on left side of UNION:
    stmt = """select medium_int from """ + gvars.g_schema_arkcasedb + """.btre202 
union
select large_int from """ + gvars.g_schema_arkcasedb + """.btsel01 
order by medium_int
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s7')
    
    #  Query 9
    #   UNION of LARGEINT and SMALLINT:
    stmt = """select large_int from """ + gvars.g_schema_arkcasedb + """.btsel01 
union
select medium_int from """ + gvars.g_schema_arkcasedb + """.btre204 
order by large_int
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s8')
    
    #  Query 10
    #   UNION of LARGEINT and INTEGER - NULLs on right side of UNION:
    stmt = """select large_int from """ + gvars.g_schema_arkcasedb + """.btre204 
union
select medium_int from """ + gvars.g_schema_arkcasedb + """.btre202 
order by large_int
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s9')
    
    #  Query 11
    #   UNION of exact numerics - left-side precision & scale greater than
    #   those on the right:
    stmt = """select binary_64_s from """ + gvars.g_schema_arkcasedb + """.btsel01 
union
select binary_32_u from """ + gvars.g_schema_arkcasedb + """.btre201 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s10')
    
    #  Query 12
    #   UNION of exact numerics - left-side precision & scale less than
    #   those on the right:
    stmt = """select binary_32_u from """ + gvars.g_schema_arkcasedb + """.btre201 
union all
select binary_64_s from """ + gvars.g_schema_arkcasedb + """.btsel01 
order by binary_32_u desc
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s11')
    
    #  Query 13
    #   UNION of approx numerics - left-side precision greater
    #   than those on the right:
    stmt = """select float_double_p from """ + gvars.g_schema_arkcasedb + """.btre201 
union
select float_basic    from """ + gvars.g_schema_arkcasedb + """.btre202 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s12')
    
    #  Query 14
    #   UNION of approx numerics - left-side precision less
    #   than those on the right:
    stmt = """select float_basic    from """ + gvars.g_schema_arkcasedb + """.btre202 
union
select float_double_p from """ + gvars.g_schema_arkcasedb + """.btre201 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s13')
    
    #  Query 15
    #   UNION of approx numeric and binary, of approx numeric and
    #   exact numeric:
    stmt = """select float_basic, float_double_p from
 """ + gvars.g_schema_arkcasedb + """.btre201 
union
select binary_signed, small_int from
 """ + gvars.g_schema_arkcasedb + """.btsel01 
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s14')
    
    #   See DATETIME test unit T151 for:
    #   UNION of DATETIME  - left-side startdate & enddate greater
    #      than those on the right.
    #   UNION of DATETIME  - left-side startdate & enddate less
    #      than those on the right.
    #   UNION of INTERVAL  - left-side startdate & enddate greater
    #      than those on the right.
    #   UNION of INTERVAL  - left-side startdate & enddate less
    #      than those on the right.
    
    #  Query 16
    #   UNION with empty tables on left-side:
    stmt = """select some_data      from """ + gvars.g_schema_arkcasedb + """.btemprel 
union
select col_9          from """ + gvars.g_schema_arkcasedb + """.btsel06 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s15')
    
    #  Query 17
    #   UNION with empty tables on right-side:
    stmt = """select col_9          from """ + gvars.g_schema_arkcasedb + """.btsel06 
union
select some_data      from """ + gvars.g_schema_arkcasedb + """.btempkey 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s16')
    
    # Query 18
    #  UNION of empty tables on both sides:
    stmt = """select some_data      from """ + gvars.g_schema_arkcasedb + """.btempkey 
union
select some_data      from """ + gvars.g_schema_arkcasedb + """.btempent 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    # Query 19
    #  UNION of nonempty tables, with MATCH => empty result:
    stmt = """select decimal_1      from """ + gvars.g_schema_arkcasedb + """.btsel01 
where decimal_1 = 3
union
select medium_int    from """ + gvars.g_schema_arkcasedb + """.btsel04 
where medium_int = 3
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    #  Query 20
    #   UNION of CHAR on left-side of UNION with longer VARCHAR on right:
    stmt = """select char_1     from """ + gvars.g_schema_arkcasedb + """.btsel01 
union all
select var_char_2 from """ + gvars.g_schema_arkcasedb + """.btre204 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s17')
    
    #  Query 21
    #   UNION of CHAR on left-side of UNION with shorter VARCHAR on
    #   right:
    stmt = """select pic_x_8    from """ + gvars.g_schema_arkcasedb + """.btre204 
union
select var_char_3 from """ + gvars.g_schema_arkcasedb + """.btre204 
order by pic_x_8
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s18')
    
    #  Query 22
    #   Should allow ORDER BY after parenthesized UNION:
    stmt = """select pic_x_8    from """ + gvars.g_schema_arkcasedb + """.btre204 
union
select var_char_3 from """ + gvars.g_schema_arkcasedb + """.btre204     

order by pic_x_8
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s19')
    
    #  Query 23
    stmt = """select pic_x_8    from """ + gvars.g_schema_arkcasedb + """.btre204 
union
select var_char_3 from """ + gvars.g_schema_arkcasedb + """.btre204     

order by pic_x_8
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s20')
    
    #  Query 24
    #   Should allow ORDER BY inside last parenthesized SELECT:
    stmt = """select pic_x_8    from """ + gvars.g_schema_arkcasedb + """.btre204 
union
select var_char_3 from """ + gvars.g_schema_arkcasedb + """.btre204 
order by pic_x_8
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s21')
    
    #  Query 25
    stmt = """select pic_x_8    from """ + gvars.g_schema_arkcasedb + """.btre204 
union
select var_char_3 from """ + gvars.g_schema_arkcasedb + """.btre204 
order by pic_x_8
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s22')
    
    _testmgr.testcase_end(desc)

def test003(desc="""a03"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0148 : 3
    #  Description:        This test verifies the SQL/K UNION
    #                      statement
    #                      UNION in subquery (for INSERT and other
    #                      SQLCI contexts).
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    #
    # Create tables to be used.
    stmt = """create table a3table1 
(
SUPPNUM                        PIC 9(3)   NOT NULL
, SUPPNAME                       PIC X(18)   NOT NULL
, ADDRESS                        PIC X(22)   NOT NULL
, CITY                           PIC X(14)   NOT NULL
, STATE                          PIC X(12)   NOT NULL
, primary key (suppnum)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table a3table2 
(
SUPPNUM                        PIC 9(3)   NOT NULL
, SUPPNAME                       PIC X(18)   NOT NULL
, ADDRESS                        PIC X(22)   NOT NULL
, CITY                           PIC X(14)   NOT NULL
, STATE                          PIC X(12)   NOT NULL
, primary key (suppnum)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table a3table3 
(
SUPPNUM                        PIC 9(3)   NOT NULL
, SUPPNAME                       PIC X(18)   NOT NULL
, ADDRESS                        PIC X(22)   NOT NULL
, CITY                           PIC X(14)   NOT NULL
, STATE                          PIC X(12)   NOT NULL
, primary key (suppnum)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table a3table4 
(
SUPPNUM                        PIC 9(3)   NOT NULL
, SUPPNAME                       PIC X(18)   NOT NULL
, ADDRESS                        PIC X(22)   NOT NULL
, CITY                           PIC X(14)   NOT NULL
, STATE                          PIC X(12)   NOT NULL
, primary key (suppnum)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table a3table5 
(
SUPPNUM                        PIC 9(3)   NOT NULL
, SUPPNAME                       PIC X(18)   NOT NULL
, ADDRESS                        PIC X(22)   NOT NULL
, CITY                           PIC X(14)   NOT NULL
, STATE                          PIC X(12)   NOT NULL
, primary key (suppnum)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #  Populate tables to be used:
    stmt = """insert into a3table1 
select * from """ + gvars.g_schema_arkcasedb + """.supplier 
where suppnum < 10
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 5)
    stmt = """insert into a3table2 
select * from """ + gvars.g_schema_arkcasedb + """.supplier 
where suppnum >= 10
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 2)
    stmt = """insert into a3table4 
select * from """ + gvars.g_schema_arkcasedb + """.supplier 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 7)
    stmt = """insert into a3table5 
select * from """ + gvars.g_schema_arkcasedb + """.supplier 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 7)
    
    #  Insert using UNION in a select:
    stmt = """insert into a3table3 
select * from a3table1 
union
select * from a3table2 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 7)
    
    #   UNION in uncorrelated subquery in WHERE clause.
    stmt = """select city from a3table1 union select city from a3table2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s0')
    
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.supplier 
where city = ANY (
select city from a3table1 union select city from a3table2 
)
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s1')
    
    #   UNION in uncorrelated subquery in HAVING clause.
    #   (Should get same result as above).
    stmt = """select city from a3table1 union select city from a3table2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s2')
    
    stmt = """select city from """ + gvars.g_schema_arkcasedb + """.supplier 
group by city
having city = ANY (
select city from a3table1 union select city from a3table2 
)
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s3')
    
    #   UNION in an IN predicate.
    stmt = """select city from a3table1 union select city from a3table2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s4')
    
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.supplier 
where city IN (
select city from a3table1 union select city from a3table2 
)
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s5')
    
    #   UNION in a quantified predicate -
    #      a subquery 'quantified' by ALL => use in DELETE.
    stmt = """select * from a3table4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s6')
    stmt = """delete from a3table4 where suppnum = ALL
( select suppnum from a3table1 
union
select suppnum from a3table1 
where suppnum = 8
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 0)
    
    stmt = """select * from a3table4 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s7')
    
    #   UNION in a quantified predicate -
    #      a subquery 'quantified' by ANY => use in UPDATE.
    stmt = """select * from a3table5 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s8')
    stmt = """update a3table4 set address = 'New dress' where suppnum = ANY
( select suppnum from a3table1 
union
select suppnum from a3table2 
where suppnum = 8
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 5)
    stmt = """select * from a3table5 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s9')
    
    #   UNION in a quantified predicate -
    #      a subquery 'quantified' by SOME.
    stmt = """select * from a3table1 where suppnum = SOME
( select suppnum from a3table1 
union
select suppnum from a3table2 
where suppnum = 8
)
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s10')
    
    #   UNION in a subquery with the existential quantifier EXISTS.
    stmt = """select * from a3table1 where EXISTS
( select suppnum from a3table1 
union
select suppnum from a3table2 
where suppnum = 8
)
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s11')
    
    #  Drop tables to be used:
    stmt = """drop table a3table1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop table a3table2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop table a3table3 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop table a3table4 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop table a3table5 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test004(desc="""a05"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0148 : A05
    #  Description:        This test verifies the SQL UNION
    #                      statement
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    
    #   -- TESTCASE SUMMARY
    #   UNION - multiple, combining
    #   UNION (distinct) & UNION ALL.
    #
    #
    #   *                                                     *
    #   *  Test Case Name:  a5                                *
    #   *                                                     *
    #   *  (Used to be host tests in initial plan;            *
    #   *     all host tests moved to T169.)                  *
    #   *                                                     *
    #
    
    #   Test unit SQLT148, case a5.
    #   volume $local_1_A ;
    
    stmt = """select binary_signed  from """ + gvars.g_schema_arkcasedb + """.btre201 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s0')
    stmt = """select small_int      from """ + gvars.g_schema_arkcasedb + """.btre202 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s1')
    
    stmt = """select col_float      from """ + gvars.g_schema_arkcasedb + """.btre203 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """select binary_64_s    from """ + gvars.g_schema_arkcasedb + """.btre204 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s2')
    stmt = """select col_1          from """ + gvars.g_schema_arkcasedb + """.btre205 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s3')
    stmt = """select headed_numeric from """ + gvars.g_schema_arkcasedb + """.btre208 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s4')
    
    stmt = """select binary_signed  from """ + gvars.g_schema_arkcasedb + """.btre201 
union all
select small_int      from """ + gvars.g_schema_arkcasedb + """.btre202 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s5')
    
    stmt = """select col_float      from """ + gvars.g_schema_arkcasedb + """.btre203 
union all
select binary_64_s    from """ + gvars.g_schema_arkcasedb + """.btre204 
union all
select col_1          from """ + gvars.g_schema_arkcasedb + """.btre205 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s6')
    
    stmt = """select col_float      from """ + gvars.g_schema_arkcasedb + """.btre203 
union all
select binary_64_s    from """ + gvars.g_schema_arkcasedb + """.btre204 
union all
select col_1          from """ + gvars.g_schema_arkcasedb + """.btre205 
union all
select headed_numeric from """ + gvars.g_schema_arkcasedb + """.btre208 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s7')
    
    stmt = """select binary_signed  from """ + gvars.g_schema_arkcasedb + """.btre201 
union all
select small_int      from """ + gvars.g_schema_arkcasedb + """.btre202 
union all
select col_float      from """ + gvars.g_schema_arkcasedb + """.btre203 
union all
select binary_64_s    from """ + gvars.g_schema_arkcasedb + """.btre204 
union all
select col_1          from """ + gvars.g_schema_arkcasedb + """.btre205 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s8')
    
    stmt = """select binary_signed  from """ + gvars.g_schema_arkcasedb + """.btre201 
union all
select small_int      from """ + gvars.g_schema_arkcasedb + """.btre202 
union all
select col_float      from """ + gvars.g_schema_arkcasedb + """.btre203 
union all
select binary_64_s    from """ + gvars.g_schema_arkcasedb + """.btre204 
union all
select col_1          from """ + gvars.g_schema_arkcasedb + """.btre205 
union all
select headed_numeric from """ + gvars.g_schema_arkcasedb + """.btre208 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s9')
    
    stmt = """select binary_signed  from """ + gvars.g_schema_arkcasedb + """.btre201 
union
select small_int      from """ + gvars.g_schema_arkcasedb + """.btre202 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s10')
    
    stmt = """select binary_signed  from """ + gvars.g_schema_arkcasedb + """.btre201 
union all
select small_int      from """ + gvars.g_schema_arkcasedb + """.btre202 
union all
select col_float      from """ + gvars.g_schema_arkcasedb + """.btre203 
union all
select binary_64_s    from """ + gvars.g_schema_arkcasedb + """.btre204 
union all
select col_1          from """ + gvars.g_schema_arkcasedb + """.btre205 
union all
select headed_numeric from """ + gvars.g_schema_arkcasedb + """.btre208 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s11')
    
    stmt = """select binary_signed  from """ + gvars.g_schema_arkcasedb + """.btre201 
union
select small_int      from """ + gvars.g_schema_arkcasedb + """.btre202 
union all
select col_float      from """ + gvars.g_schema_arkcasedb + """.btre203 
union
select binary_64_s    from """ + gvars.g_schema_arkcasedb + """.btre204 
union all
select col_1          from """ + gvars.g_schema_arkcasedb + """.btre205 
union
select headed_numeric from """ + gvars.g_schema_arkcasedb + """.btre208 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s12')
    
    stmt = """select binary_signed  from """ + gvars.g_schema_arkcasedb + """.btre201 
union all
select small_int      from """ + gvars.g_schema_arkcasedb + """.btre202 
union
select col_float      from """ + gvars.g_schema_arkcasedb + """.btre203 
union all
select binary_64_s    from """ + gvars.g_schema_arkcasedb + """.btre204 
union
select col_1          from """ + gvars.g_schema_arkcasedb + """.btre205 
union all
select headed_numeric from """ + gvars.g_schema_arkcasedb + """.btre208 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s13')
    
    stmt = """select binary_signed  from """ + gvars.g_schema_arkcasedb + """.btre201 
union
select small_int      from """ + gvars.g_schema_arkcasedb + """.btre202 
union
select col_float      from """ + gvars.g_schema_arkcasedb + """.btre203 
union all
select binary_64_s    from """ + gvars.g_schema_arkcasedb + """.btre204 
union all
select col_1          from """ + gvars.g_schema_arkcasedb + """.btre205 
union
select headed_numeric from """ + gvars.g_schema_arkcasedb + """.btre208 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s14')
    
    stmt = """select binary_signed  from """ + gvars.g_schema_arkcasedb + """.btre201 
union
( select small_int      from """ + gvars.g_schema_arkcasedb + """.btre202 
union
select binary_64_s    from """ + gvars.g_schema_arkcasedb + """.btre204 
)
union
select col_1          from """ + gvars.g_schema_arkcasedb + """.btre205 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s15')
    
    stmt = """select binary_signed  from """ + gvars.g_schema_arkcasedb + """.btre201 
union all
select small_int      from """ + gvars.g_schema_arkcasedb + """.btre202 
union all
( select binary_64_s    from """ + gvars.g_schema_arkcasedb + """.btre204 
union all
select col_1          from """ + gvars.g_schema_arkcasedb + """.btre205 
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s16')
    
    stmt = """( select binary_signed  from """ + gvars.g_schema_arkcasedb + """.btre201 
union all
select small_int      from """ + gvars.g_schema_arkcasedb + """.btre202 
)
union all
select binary_64_s    from """ + gvars.g_schema_arkcasedb + """.btre204 
union all
select col_1          from """ + gvars.g_schema_arkcasedb + """.btre205 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s17')
    
    _testmgr.testcase_end(desc)

def test005(desc="""a06"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0148 : A06
    #  Description:        This test verifies the SQL UNION
    #                      statement
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    
    #  -- TESTCASE SUMMARY
    #  UNION with constants and expressions.
    #
    #
    #  *                                                     *
    #  *  Test Case Name:  a6                                *
    #  *                                                     *
    #  *  Known bug:                                         *
    #  *     select small_int , binary_signed , ( small_int +
    #  *      binary_signed )
    #  *     from $SQL_A.SQLDD01W.btsel01
    #  *        union
    #  *     select (col_1*100) , (col_2/1000) , (col_2/col_1)
    #  *     from $SQL_A.SQLDD01W.btsel06
    #  *     order by 1 , 2 , 3
    #  *     ;
    #  *   *** ERROR from SQL [-6010]: Internal error: The SQL compiler
    #  *            detected an
    #  *   ***      inconsistent internal data structure.
    #  *
    #
    
    #  Test unit SQLT148, case a6.
    #  volume $local_1_A ;
    
    #  UNION with constants:
    stmt = """select 'a' from """ + gvars.g_schema_arkcasedb + """.btempkey 
union all
select 'j' from """ + gvars.g_schema_arkcasedb + """.btemprel 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """select 'a' from """ + gvars.g_schema_arkcasedb + """.btsel27 
union all
select 'j' from """ + gvars.g_schema_arkcasedb + """.btsel27 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s0')
    
    #   UNION with constants:
    stmt = """select var_char_2, 'april', var_char_3, 'may' from
 """ + gvars.g_schema_arkcasedb + """.btre204 
union all
select 'june',     'july',  var_char_2, var_char_3 from
 """ + gvars.g_schema_arkcasedb + """.btre208 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s1')
    
    #   UNION with expressions:
    stmt = """select small_int , binary_signed , ( small_int + binary_signed )
from """ + gvars.g_schema_arkcasedb + """.btsel01 
union
select col_1 , col_2 , (col_2 - col_1)
from """ + gvars.g_schema_arkcasedb + """.btsel06 
order by 1 , 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s2')
    
    #   UNION with expressions, ordering by the expression also:
    stmt = """select small_int , binary_signed , ( small_int + binary_signed )
from """ + gvars.g_schema_arkcasedb + """.btsel01 
union
select col_1 , col_2 , (col_2 - col_1)
from """ + gvars.g_schema_arkcasedb + """.btsel06 
order by 1 , 2 , 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s3')
    stmt = """select small_int , binary_signed , ( small_int + binary_signed )
from """ + gvars.g_schema_arkcasedb + """.btsel01 
union
select (col_1*100) , (col_2/1000) , (col_2/col_1)
from """ + gvars.g_schema_arkcasedb + """.btsel06 
order by 1 , 2 , 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s4')
    
    _testmgr.testcase_end(desc)

def test006(desc="""a07"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0148 : A07
    #  Description:        This test verifies the SQL UNION
    #                      statement
    #                      Table btuwl02 is a relative optimizer table.
    #                      Will not run this test until the optimizer
    #                      database is modified and the relative table
    #                      is converted to key sequenced table.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    #   -- TESTCASE SUMMARY
    #   Multi-column UNIONs & extended
    #   multi-UNION SELECTs.
    #
    #
    #   *                                                     *
    #   *  Test Case Name:  a7                                *
    #   *                                                     *
    #   *  21 Dec 1990, using ref file with spurious char to avoid
    #   *         appearance of failure due to SQL - Phil will correct
    #   *         optimizer database problem - spurious trailing characters.
    #
    
    #   Test unit SQLT148, case a7.
    #   volume $local_1_A ;
    
    #   UNION on 10 columns from global database.
    stmt = """select char_1 , pic_x_1 , binary_signed , binary_32_u
, pic_comp_1 , pic_comp_2 , small_int , decimal_1
, pic_decimal_1 , pic_decimal_3
from """ + gvars.g_schema_arkcasedb + """.btsel01 
union
select char_1 , pic_x_8 , binary_signed , binary_32_u
, pic_comp_1 , pic_comp_2 , small_int , decimal_1
, pic_decimal_1 , pic_decimal_3
from """ + gvars.g_schema_arkcasedb + """.btre201 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s0')
    
    #  To avoid spurious Warning 6008 from SQL when
    #  Statistics for a table
    #       not available,
    #  Warnings are set OFF:
    stmt = """SET SESSION WARNINGS OFF ;"""
    output = _dci.cmdexec(stmt)
    #   UNION on 98 of 100 columns from optimizer database:
    #   The SELECT on the first table only:
    #     select sbin0_500 , char0_10 , ubin0_1000 , sdec0_uniq
    #        , sbin1_100 , char1_4 , udec1_10 , ubin1_4 , sdec1_2
    #        , sbin2_2 , ubin2_4 , sdec2_10 , char2_2 , udec2_100
    #        , sbin3_1000 , udec3_2000 , char3_1000 , sdec3_500 , ubin3_uniq
    #        , sbin4_2 , ubin4_4 , char4_10 , sdec4_10 , udec4_2
    #        , sbin5_4 , ubin5_20 , udec5_20 , varchar5_10 , sdec5_100
    #        , sbin6_uniq , sdec6_2000 , udec6_500 , char6_20 , ubin6_2
    #        , sbin7_2 , sdec7_10 , char7_uniq , udec7_20 , ubin7_100
    #        , sbin8_1000 , char8_500 , sdec8_2000 , udec8_500 , ubin8_2
    #        , sbin9_4 , char9_uniq , udec9_10 , sdec9_20 , ubin9_100
    #        , sbin10_uniq , ubin10_1000 , char10_20 , udec10_2000
    #        , sdec10_500
    #        , sbin11_2000 , sdec11_20 , udec11_20 , ubin11_2 , char11_4
    #        , sbin12_1000 , sdec12_100 , char12_10 , ubin12_10
    #        , udec12_1000
    #        , sbin13_uniq , char13_100 , sdec13_uniq , ubin13_10
    #        , udec13_500
    #        , sbin14_100 , ubin14_2 , sdec14_20 , udec14_10 , char14_20
    #        , sbin15_2 , udec15_4 , varchar15_uniq , ubin15_uniq
    #        , sdec15_10
    #        , sbin16_20 , sdec16_100 , ubin16_1000 , udec16_1000
    #        , char16_uniq
    #        , sbin17_uniq , sdec17_20 , ubin17_2000 , char17_100
    #        , udec17_100
    #        , sbin18_uniq , char18_20 , ubin18_20 , sdec18_4 , udec18_4
    #        , sbin19_4 , char19_2 , ubin19_10 , udec19_100 , sdec19_1000
    #        , sbin20_2000 , udec20_uniq , ubin20_1000 , char20_10
    #           from $optim_2_A.btuwl02
    #     where ubin0_1000 = 10
    #     order by 1
    #     ;
    #   The UNION:
    #     select sbin0_500 , char0_10 , ubin0_1000 , sdec0_uniq
    #        , sbin1_100 , char1_4 , udec1_10 , ubin1_4 , sdec1_2
    #        , sbin2_2 , ubin2_4 , sdec2_10 , char2_2 , udec2_100
    #        , sbin3_1000 , udec3_2000 , char3_1000 , sdec3_500 , ubin3_uniq
    #        , sbin4_2 , ubin4_4 , char4_10 , sdec4_10 , udec4_2
    #        , sbin5_4 , ubin5_20 , udec5_20 , varchar5_10 , sdec5_100
    #        , sbin6_uniq , sdec6_2000 , udec6_500 , char6_20 , ubin6_2
    #        , sbin7_2 , sdec7_10 , char7_uniq , udec7_20 , ubin7_100
    #        , sbin8_1000 , char8_500 , sdec8_2000 , udec8_500 , ubin8_2
    #        , sbin9_4 , char9_uniq , udec9_10 , sdec9_20 , ubin9_100
    #        , sbin10_uniq , ubin10_1000 , char10_20 , udec10_2000
    #        , sdec10_500
    #        , sbin11_2000 , sdec11_20 , udec11_20 , ubin11_2 , char11_4
    #        , sbin12_1000 , sdec12_100 , char12_10 , ubin12_10
    #        , udec12_1000
    #        , sbin13_uniq , char13_100 , sdec13_uniq , ubin13_10
    #        , udec13_500
    #        , sbin14_100 , ubin14_2 , sdec14_20 , udec14_10 , char14_20
    #        , sbin15_2 , udec15_4 , varchar15_uniq , ubin15_uniq
    #        , sdec15_10
    #       , sbin16_20 , sdec16_100 , ubin16_1000 , udec16_1000
    #        , char16_uniq
    #        , sbin17_uniq , sdec17_20 , ubin17_2000 , char17_100
    #        , udec17_100
    #        , sbin18_uniq , char18_20 , ubin18_20 , sdec18_4 , udec18_4
    #        , sbin19_4 , char19_2 , ubin19_10 , udec19_100 , sdec19_1000
    #        , sbin20_2000 , udec20_uniq , ubin20_1000 , char20_10
    #           from $optim_2_A.btuwl02
    #        union
    #     select sdec0_uniq , varchar0_4 , sbin0_500 , udec0_2000
    #        , sbin1_100 , char1_4 , udec1_10 , ubin1_4 , sdec1_2
    #        , sbin2_2 , ubin2_4 , sdec2_10 , char2_2 , udec2_100
    #        , sbin3_1000 , udec3_2000 , char3_1000 , sdec3_500 , ubin3_uniq
    #        , sbin4_2 , ubin4_4 , char4_10 , sdec4_10 , udec4_2
    #        , sbin5_4 , ubin5_20 , udec5_20 , varchar5_10 , sdec5_100
    #        , sbin6_uniq , sdec6_2000 , udec6_500 , char6_20 , ubin6_2
    #        , sbin7_2 , sdec7_10 , char7_uniq , udec7_20 , ubin7_100
    #        , sbin8_1000 , char8_500 , sdec8_2000 , udec8_500 , ubin8_2
    #        , sbin9_4 , char9_uniq , udec9_10 , sdec9_20 , ubin9_100
    #       , sbin10_uniq , ubin10_1000 , char10_20 , udec10_2000
    #        , sdec10_500
    #        , sbin11_2000 , sdec11_20 , udec11_20 , ubin11_2 , char11_4
    #        , sbin12_1000 , sdec12_100 , char12_10 , ubin12_10
    #        , udec12_1000
    #        , sbin13_uniq , char13_100 , sdec13_uniq , ubin13_10
    #        , udec13_500
    #        , sbin14_100 , ubin14_2 , sdec14_20 , udec14_10 , char14_20
    #        , sbin15_2 , udec15_4 , varchar15_uniq , ubin15_uniq
    #        , sdec15_10
    #       , sbin16_20 , sdec16_100 , ubin16_1000 , udec16_1000
    #       , char16_uniq
    #       , sbin17_uniq , sdec17_20 , ubin17_2000 , char17_100
    #       , udec17_100
    #       , sbin18_uniq , char18_20 , ubin18_20 , sdec18_4 , udec18_4
    #        , sbin19_4 , char19_2 , ubin19_10 , udec19_100 , sdec19_1000
    #        , sbin20_2000 , udec20_uniq , ubin20_1000 , char20_10
    #           from $optim_1_A.btuwl04
    #    where ubin0_1000 = 10
    #     order by 1
    #    ;
    
    #   UNION of SELECTs that contain UNION.
    stmt = """select city, state from """ + gvars.g_schema_arkcasedb + """.customer 
union
select city, state from """ + gvars.g_schema_arkcasedb + """.supplier 
union
select state, city from """ + gvars.g_schema_arkcasedb + """.customer 
union
select state, city from """ + gvars.g_schema_arkcasedb + """.supplier 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s1')
    
    #   UNION of SELECTs with UNION in WHERE clause:
    stmt = """select city, state from """ + gvars.g_schema_arkcasedb + """.customer 
union
select city, state from """ + gvars.g_schema_arkcasedb + """.supplier 
where city = ANY
(select city from """ + gvars.g_schema_arkcasedb + """.customer 
union
select city from """ + gvars.g_schema_arkcasedb + """.supplier 
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s2')
    
    stmt = """select city, state from """ + gvars.g_schema_arkcasedb + """.customer 
union
select city, state from """ + gvars.g_schema_arkcasedb + """.supplier 
where city = ANY
(select city from """ + gvars.g_schema_arkcasedb + """.customer 
union
select city from """ + gvars.g_schema_arkcasedb + """.supplier 
where city = ANY
(select city from """ + gvars.g_schema_arkcasedb + """.customer 
union
select city from """ + gvars.g_schema_arkcasedb + """.supplier 
)
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s3')
    
    stmt = """select city, state from """ + gvars.g_schema_arkcasedb + """.customer 
union
select city, state from """ + gvars.g_schema_arkcasedb + """.supplier 
where city = ANY
(select city from """ + gvars.g_schema_arkcasedb + """.customer 
union
select city from """ + gvars.g_schema_arkcasedb + """.supplier 
where city = ANY
(select city from """ + gvars.g_schema_arkcasedb + """.customer 
union
select city from """ + gvars.g_schema_arkcasedb + """.supplier 
where city = ANY
(select city from """ + gvars.g_schema_arkcasedb + """.customer 
union
select city from """ + gvars.g_schema_arkcasedb + """.supplier 
)
)
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s4')
    
    _testmgr.testcase_end(desc)

def test007(desc="""a08"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0148 : A08
    #  Description:        This test verifies the SQL UNION
    #                      statement
    #                      UNION of table on different local volumes.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    #  Create tables to be used:
    
    stmt = """create table a8table1 
(
SUPPNUM                        PIC 9(3)  NOT NULL
, SUPPNAME                       PIC X(18)  NOT NULL
, ADDRESS                        PIC X(22)  NOT NULL
, CITY                           PIC X(14)  NOT NULL
, STATE                          PIC X(12)  NOT NULL
, primary key (suppnum)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table a8table2 
(
SUPPNUM                        PIC 9(3)  NOT NULL
, SUPPNAME                       PIC X(18)  NOT NULL
, ADDRESS                        PIC X(22)  NOT NULL
, CITY                           PIC X(14)  NOT NULL
, STATE                          PIC X(12)  NOT NULL
, primary key (suppnum)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table a8table3 
(
SUPPNUM                        PIC 9(3)  NOT NULL
, SUPPNAME                       PIC X(18)  NOT NULL
, ADDRESS                        PIC X(22)  NOT NULL
, CITY                           PIC X(14)  NOT NULL
, STATE                          PIC X(12)  NOT NULL
, primary key (suppnum)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #  Populate tables to be used:
    stmt = """insert into a8table1 
select * from """ + gvars.g_schema_arkcasedb + """.supplier 
where suppnum < 5 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 3)
    
    stmt = """insert into a8table2 
select * from """ + gvars.g_schema_arkcasedb + """.supplier 
where suppnum >= 5 and suppnum < 10 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 2)
    
    stmt = """insert into a8table3 
select * from """ + gvars.g_schema_arkcasedb + """.supplier 
where suppnum >= 10 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 2)
    
    stmt = """select city from a8table1 
union
select city from a8table2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s0')
    
    stmt = """select city from a8table1 
union
select city from a8table2 
union
select city from a8table3 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s1')
    
    stmt = """select city from a8table1 
union
( select city from a8table2 
union
select city from a8table3 
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s2')
    
    stmt = """drop table a8table1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table a8table2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table a8table3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test008(desc="""a09"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0148 : A09
    #  Description:        This test verifies the SQL UNION
    #                      statement
    #                      UNION ALL and ORDER BY and EXPRESSION.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    # create tables:
    stmt = """create table a9table1 
(
UNIT              CHAR( 5 )      NO DEFAULT NOT NULL
, DATE1              NUMERIC( 6, 0) NO DEFAULT NOT NULL
, AMOUNT            NUMERIC( 5, 0) NO DEFAULT NOT NULL
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table a9table2 
(
UNIT              CHAR( 5 )      NO DEFAULT NOT NULL
, DATE1              NUMERIC( 6, 0) NO DEFAULT NOT NULL
, AMOUNT            NUMERIC( 5, 0) NO DEFAULT NOT NULL
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #   Create two views (must be s/h) with same & different column names
    
    #   expressions in views, unioned
    
    stmt = """select 'View1', city, state from """ + gvars.g_schema_arkcasedb + """.customer;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s0')
    
    stmt = """create view a9view1 (l, c, s) as
select 'View1', city, state from """ + gvars.g_schema_arkcasedb + """.customer;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from a9view1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s1')
    
    stmt = """create view a9view2 (l, c, a) as
select 'View2', city, address from """ + gvars.g_schema_arkcasedb + """.supplier;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from a9view2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s2')
    
    #  Create two s/h views that contain unions:
    
    stmt = """create view a9view5 (l, c, s) as
select 'ABCDE', city, state from """ + gvars.g_schema_arkcasedb + """.customer 
union
select 'XYZ'  , city, state from """ + gvars.g_schema_arkcasedb + """.supplier;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from a9view5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s3')
    
    #  Note the reversal of fields:
    stmt = """create view a9view6 (l, s, c) as
select 'A9'   , state, city from """ + gvars.g_schema_arkcasedb + """.customer 
union
select 'A'    , state, city from """ + gvars.g_schema_arkcasedb + """.supplier;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from a9view6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s4')
    
    stmt = """insert into  a9table1 values ('UN1', 900610, 100);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into  a9table1 values ('UN1', 900611, 200);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into  a9table1 values ('UN1', 900612, 300);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into  a9table1 values ('UN2', 900610,  50);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into  a9table1 values ('UN2', 900611, 150);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into  a9table1 values ('UN2', 900612, 250);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """select 'A9Table1', unit, date1, amount from  a9table1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s5')
    
    stmt = """insert into  a9table2 values ('UN1', 900610, 1000);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into  a9table2 values ('UN1', 900611, 2000);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into  a9table2 values ('UN1', 900612, 3000);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into  a9table2 values ('UN2', 900610, 1500);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into  a9table2 values ('UN2', 900611, 2500);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into  a9table2 values ('UN2', 900612, 3500);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """select 'A9Table2', unit, date1, amount from  a9table2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s6')
    
    #   UNIONs:
    
    #   Col 1 ordering ignored in C30G; worked in C30L:
    stmt = """select 'A9Table1', unit, date1, amount from  a9table1 
union
select 'A9Table2', unit, date1, amount from  a9table2 
order by 2,1,3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s7')
    
    #   Col 1 ordering ignored in C30G and in C30L:
    stmt = """select 'A9Table1', unit, date1, amount from  a9table1 
union all
select 'A9Table2', unit, date1, amount from  a9table2 
order by 2,1,3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s8')
    
    #   Test other orderings, other columns:
    stmt = """select 'A9Table1', unit, date1, amount from  a9table1 
union all
select 'A9Table2', unit, date1, amount from  a9table2 
order by 1,2,4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s9')
    
    stmt = """select 'A9Table1', unit, date1, amount from  a9table1 
union
select 'A9Table2', unit, date1, amount from  a9table2 
order by 4,1,2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s10')
    
    stmt = """select 'A9Table1', unit, date1, amount from  a9table1 
union all
select 'A9Table2', unit, date1, amount from  a9table2 
order by 1,3,2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s11')
    
    stmt = """select 'A9Table1', unit, date1, amount from  a9table1 
union
select 'A9Table2', unit, date1, amount from  a9table2 
order by 2,3,1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s12')
    
    stmt = """select 'A9Table1', unit, date1, amount from  a9table1 
union all
select 'A9Table2', unit, date1, amount from  a9table2 
order by 3,2,1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s13')
    
    #  Order of literals
    
    stmt = """select unit, 'A9Table1', date1, amount from a9table1 
union
select unit, 'A9Table2', date1, amount from a9table2 
order by 3,2,1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s14')
    
    stmt = """select date1, unit, 'A9Table1', amount from a9table1 
union all
select date1, unit, 'A9Table2', amount from a9table2 
order by 3,2,1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s15')
    
    stmt = """select amount, date1, unit, 'A9Table1' from a9table1 
union
select amount, date1, unit, 'A9Table2' from a9table2 
order by 4,3,2,1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s16')
    
    stmt = """select amount, date1, unit, 'A9Table1' from a9table1 
union
select amount, date1, unit, 'A9Table2' from a9table2 
order by 3,2,4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s17')
    
    stmt = """select * from  a9view1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s18')
    stmt = """select * from  a9view2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s19')
    
    stmt = """select * from  a9view1 
union
select * from  a9view2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s20')
    
    stmt = """select * from  a9view1 
union
select * from  a9view2 
order by 1,2,3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s21')
    
    stmt = """select * from  a9view1 
union
select * from  a9view2 
order by 2,3,1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s22')
    
    stmt = """select * from  a9view1 
union
select * from  a9view2 
order by 3,1,2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s23')
    
    stmt = """select * from  a9view5 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s24')
    stmt = """select * from  a9view6 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s25')
    
    stmt = """select * from  a9view5 
union
select * from  a9view6 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s26')
    
    #  And finally (Jay found internal error when literals were
    #  of different lengths):
    stmt = """select 'A9Table1' from  a9table1 
union
select 'A9Table2' from a9table2 
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s27')
    
    stmt = """select 'A9Table1' from a9table1 
union all
select 'A9Table2' from a9table2 
order by 1 desc ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s28')
    
    stmt = """select 'B'        from a9table1 
union
select 'A'        from a9table2 
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s29')
    
    stmt = """select 'B'        from a9table1 
union all
select 'A'        from a9table2 
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s30')
    
    stmt = """select 'B2345678' from a9table1 
union
select 'A2'       from a9table2 
order by 1 desc ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s31')
    
    stmt = """select 'B2345678' from a9table1 
union all
select 'A2'       from a9table2 
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s32')
    
    stmt = """select 'A2'       from a9table2 
union
select 'B2345678' from a9table1 
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s33')
    
    stmt = """select 'A2'       from a9table2 
union all
select 'B2345678' from a9table1 
order by 1 desc ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s34')
    
    # drop views and tables
    stmt = """drop view a9view1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view a9view1;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop view a9view2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view a9view5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view a9view6 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop table a9table1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table a9table2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test009(desc="""a10"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0148 : A10
    #  Description:        This test verifies the SQL UNION
    #                      statement
    #                      Insert into view created using UNION.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    
    #------------------------
    # For view with union:
    #------------------------
    # create tables:
    stmt = """create table aatable0 
(
c1      CHAR( 10 ) DEFAULT NULL
, c2      NUMERIC( 3, 0) DEFAULT NULL
, c3      CHAR( 5 ) DEFAULT NULL
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table aatable1 
(
c1      CHAR( 10 ) DEFAULT NULL
, c2      NUMERIC( 3, 0) DEFAULT NULL
, c3      CHAR( 5 ) DEFAULT NULL
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table aatable2 
(
c1      CHAR( 10 ) DEFAULT NULL
, c2      NUMERIC( 3, 0) DEFAULT NULL
, c3      CHAR( 5 ) DEFAULT NULL
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # create view:
    stmt = """create view aaview1 (c1,c2,c3) as
select * from aatable1 
union
select * from aatable2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table aatable3 
(
c1      CHAR( 10 ) DEFAULT NULL
, c2      NUMERIC( 3, 0) DEFAULT NULL
, c3      CHAR( 5 ) DEFAULT NULL
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #------------------------
    # For 1-col view with union:
    #------------------------
    # create view:
    stmt = """create view aaview2 (c2) as
select c2 from aatable1 
union all
select c2 from aatable2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # create table:
    stmt = """create table aatable4 ( c2 numeric( 3, 0) default null ) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #------------------------
    # For view without union:
    #------------------------
    # create tables:
    stmt = """create table aatable5 
(
c1      CHAR( 10 ) DEFAULT NULL
, c2      NUMERIC( 3, 0) DEFAULT NULL
, c3      CHAR( 5 ) DEFAULT NULL
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # create views:
    stmt = """create view aaview3 (v1, v2, v3) as
select c1, c2, c3 from aatable1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from aaview1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """insert into aatable3 
(select * from aaview1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 0)
    
    stmt = """select * from aaview1  ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """select * from aatable1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """select * from aatable2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """select * from aatable3 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    # Clean out records from target table:
    stmt = """delete from aatable3 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 0)
    
    stmt = """select * from aatable3 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """insert into aatable1 values ('aatable1',10,'aaa');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into aatable1 values ('aatable1',11,'aaa');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into aatable1 values ('aatable1',12,'aaa');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into aatable3 
(select c1,c2,c3 from aaview1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 3)
    
    stmt = """select * from aaview1  ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s0')
    stmt = """select * from aatable1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s1')
    stmt = """select * from aatable2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """select * from aatable3 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s2')
    
    # Clean out records from target table:
    stmt = """delete from aatable3 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 3)
    
    stmt = """select * from aatable3 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """insert into aatable2 values ('aatable2',20,'aaa');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into aatable2 values ('aatable2',21,'aaa');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into aatable2 values ('aatable2',22,'aaa');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into aatable3 
(select * from aaview1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 6)
    
    stmt = """select * from aaview1  ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s3')
    stmt = """select * from aatable1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s4')
    stmt = """select * from aatable2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s5')
    stmt = """select * from aatable3 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s6')
    
    # Clean out records from target table:
    stmt = """delete from aatable3 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 6)
    
    stmt = """select * from aatable3 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """insert into aatable1 values ('aatable1',13,'aaa');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into aatable1 values ('aatasame',04,'aaa');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into aatable2 values ('aatasame',04,'aaa');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into aatable3 
(select c1,c2,c3 from aaview1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 8)
    
    stmt = """select * from aaview1  ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s7')
    stmt = """select * from aatable1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s8')
    stmt = """select * from aatable2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s9')
    stmt = """select * from aatable3 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s10')
    
    stmt = """select * from aaview1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s11')
    stmt = """select * from aaview2  ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s12')
    
    stmt = """insert into aatable4 
(select * from aaview2 );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 9)
    
    stmt = """select * from aatable4 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s13')
    
    stmt = """insert into aatable4 
(select c2 from aaview2 );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 9)
    
    stmt = """select * from aatable4 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s14')
    
    stmt = """insert into aatable5 
(select * from aaview3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 5)
    
    stmt = """select * from aaview3  ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s15')
    stmt = """select * from aatable5 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s16')
    
    #------------------------
    # For view with union:
    #------------------------
    # drop view:
    stmt = """drop view aaview1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view aaview2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view aaview3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # drop tables:
    stmt = """drop table aatable0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table aatable1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table aatable2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table aatable3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table aatable4 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #------------------------
    # For view without union:
    #------------------------
    # drop views:
    
    # drop tables:
    stmt = """drop table aatable5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test010(desc="""a11"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0148 : A11
    #  Description:        This test verifies the SQL UNION
    #                      statement
    #                      Parameters in UNION ALL.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    
    #------------------------
    # Params:
    #------------------------
    stmt = """set param ?n1 8000  ;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?a1 'B'   ;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?a2 'mad' ;"""
    output = _dci.cmdexec(stmt)
    
    # ------------------------
    #  Basic data:
    # ------------------------
    stmt = """select char_1, var_char, medium_int, small_int
from """ + gvars.g_schema_arkcasedb + """.btsel01 
order by small_int ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s0')
    stmt = """select char_1, var_char, medium_int, small_int
from """ + gvars.g_schema_arkcasedb + """.btsel01 
where medium_int > ?n1
order by small_int ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s1')
    stmt = """select char_1, var_char, medium_int, small_int
from """ + gvars.g_schema_arkcasedb + """.btsel01 
where char_1 > ?a1
order by small_int ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s2')
    stmt = """select char_1, var_char, medium_int, small_int
from """ + gvars.g_schema_arkcasedb + """.btsel01 
where var_char > ?a2
order by small_int ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s3')
    
    # ------------------------
    #  Union with param for numeric:
    # ------------------------
    stmt = """select char_1, small_int
from """ + gvars.g_schema_arkcasedb + """.btsel01 
where medium_int > ?n1
union all
select char_1, small_int
from """ + gvars.g_schema_arkcasedb + """.btsel01 
order by char_1    ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s4')
    
    stmt = """select char_1, small_int
from """ + gvars.g_schema_arkcasedb + """.btsel01 
union all
select char_1, small_int
from """ + gvars.g_schema_arkcasedb + """.btsel01 
where medium_int > ?n1
order by char_1    ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s5')
    
    stmt = """select char_1, small_int
from """ + gvars.g_schema_arkcasedb + """.btsel01 
where medium_int > ?n1
union
select char_1, small_int
from """ + gvars.g_schema_arkcasedb + """.btsel01 
where medium_int > ?n1
order by char_1    ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s6')
    
    # ------------------------
    #   Ok:
    stmt = """select small_int
from """ + gvars.g_schema_arkcasedb + """.btsel01 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s7')
    
    stmt = """set param ?p 100;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s from
select small_int from """ + gvars.g_schema_arkcasedb + """.btsel01 
where small_int = ?p  ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """set param ?p 100;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s from
select small_int from """ + gvars.g_schema_arkcasedb + """.btsel01 
where small_int = ?p
union all
select small_int from """ + gvars.g_schema_arkcasedb + """.btsel01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s8')
    
    stmt = """set param ?p  80;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?q  90;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s from
select small_int from """ + gvars.g_schema_arkcasedb + """.btsel01 
where small_int = ?p
union all
select small_int from """ + gvars.g_schema_arkcasedb + """.btsel01 
where small_int = ?q  ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s9')
    
    #  UNION instead of UNION ALL:
    
    stmt = """set param ?p  90;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?q  80;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s from
select small_int from """ + gvars.g_schema_arkcasedb + """.btsel01 
where small_int = ?p
union
select small_int from """ + gvars.g_schema_arkcasedb + """.btsel01 
where small_int = ?q ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s10')
    
    #  Param typed by inclusion in SELECT list with addition of 0:
    
    stmt = """set param ?p  80;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?q  90;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s from
select (?p+0), small_int from """ + gvars.g_schema_arkcasedb + """.btsel01 
where small_int = ?p
union all
select (?q+0), small_int from """ + gvars.g_schema_arkcasedb + """.btsel01 
where small_int = ?q  ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s11')
    
    # ------------------------
    #  Union with param for char, varchar:
    # ------------------------
    stmt = """select char_1, var_char
from """ + gvars.g_schema_arkcasedb + """.btsel01 
where char_1 > ?a1
union
select char_1, var_char
from """ + gvars.g_schema_arkcasedb + """.btsel01 
order by char_1    ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s12')
    
    stmt = """select char_1, var_char
from """ + gvars.g_schema_arkcasedb + """.btsel01 
union
select char_1, var_char
from """ + gvars.g_schema_arkcasedb + """.btsel01 
where var_char  > ?a2
order by char_1    ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s13')
    
    stmt = """select char_1, var_char
from """ + gvars.g_schema_arkcasedb + """.btsel01 
where var_char  > ?a2
union all
select char_1, var_char
from """ + gvars.g_schema_arkcasedb + """.btsel01 
where char_1  > ?a1
order by char_1    ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s14')
    
    #------------------------
    # Params:
    #------------------------
    stmt = """set param ?y1 1900-01-01;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?i1 '01:02:03';"""
    output = _dci.cmdexec(stmt)
    
    #------------------------
    # Basic data:
    #------------------------
    # This test has to be modified from here to the end.
    # The Column Y has to be substitued with appropriate
    # Colun name. Since I can't insert using ARK
    # datatypes into MP tables, this portion has not been
    # Converted.
    #
    
    stmt = """CREATE TABLE aBTRE211 
(
Y_to_D      DATE,
Y_to_S      TIMESTAMP,
Y_to_F      TIMESTAMP(3),
H_to_S      TIME,
H_to_F      TIME(3)
) no partition ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """INSERT INTO aBTRE211 VALUES (
date '1988-01-01',
timestamp '1988-01-01:12:35:30',
timestamp '1988-01-01:12:35:30.333',
time '10:15:30'
,time '10:15:30.555'
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO aBTRE211 VALUES (
date '1977-03-02' ,
timestamp '1979-06-05:14:40:45' ,
timestamp '1980-07-06:15:45:50.678' ,
time '03:53:56',
time '04:54:57.345'
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO aBTRE211 VALUES (
date '1802-09-07' ,
timestamp '1805-12-10:07:59:03' ,
timestamp '1806-01-11:08:01:04.789' ,
time '18:08:09',
time '19:09:10.234'
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO aBTRE211 VALUES (
date '1901-01-01' ,
timestamp '1901-01-01:00:00:00' ,
timestamp '1901-01-01:00:00:00.00' ,
time '00:00:00' ,
time '00:00:00.00'
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select Y_to_D from aBTRE211 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s15')
    
    stmt = """select Y_to_D from aBTRE211 
where Y_to_D > ?y1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s16')
    
    stmt = """select Y_to_D from aBTRE211 
where Y_to_D < ?y1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s17')
    
    stmt = """select Y_to_D from aBTRE211 
where ( Y_to_D < ?y1 ) and ( Y_to_D > ?y1 ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    #------------------------
    # Union with param for date, time:
    #------------------------
    stmt = """select Y_to_D from aBTRE211 
where Y_to_D = ?y1
union all
select Y_to_D from aBTRE211 
order by Y_to_D ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s18')
    
    stmt = """select Y_to_D from aBTRE211 
union
select Y_to_D from aBTRE211 
where Y_to_D = ?y1
order by Y_to_D ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s19')
    
    #  UNION of INTERVAL:
    stmt = """select ih_to_s from """ + gvars.g_schema_arkcasedb + """.btre204 
union all
select ih_to_s from """ + gvars.g_schema_arkcasedb + """.btre204 
where ih_to_s > cast(?i1 as interval hour to second)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s20')
    stmt = """select ih_to_s from """ + gvars.g_schema_arkcasedb + """.btre204 
where ih_to_s < cast(?i1 as interval hour to second)
union all
select ih_to_s from """ + gvars.g_schema_arkcasedb + """.btre208 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s21')
    
    stmt = """drop table aBTRE211;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test011(desc="""a12"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0148 : A12
    #  Description:        This test verifies the SQL UNION
    #                      statement
    #                      UNION ALL, FOR xxx access when referencing
    #                      a VIEW.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    
    #  Create tables
    stmt = """Create table  ACaward 
(
CARD_NUM        CHAR( 19 ) NO DEFAULT NOT NULL
, WIN_DAT_TIM     DATE NOT NULL
, STORE_NUM       CHAR( 4 ) NOT NULL
, KIOSK_LOC_NUM   CHAR( 3 ) NOT NULL
, KIOSK_SEQ_NUM   CHAR( 4 ) NOT NULL
, GAME_NUM        CHAR( 4 ) NOT NULL
, PRIZE_LVL       CHAR( 2 ) NOT NULL
, PRIZE_TYP       CHAR( 1 ) NOT NULL
, WIN_PNT         NUMERIC( 6, 0) NOT NULL
, AWARD_STATUS    CHAR( 1 ) NO DEFAULT NOT NULL
, CLAIM_DAT       DATE NOT NULL
, AWARD_DAT       DATE NOT NULL
, WIN_NUM         NUMERIC( 8, 0) NOT NULL
, primary key (card_num));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table  ACpur 
(
CARD_NUM        CHAR( 19 ) NO DEFAULT NOT NULL
, DAT             DATE NOT NULL
, STORE_NUM       CHAR( 4 ) NO DEFAULT NOT NULL
, TERM_LOC        CHAR( 3 ) NO DEFAULT NOT NULL
, TERM_SEQ_NUM    CHAR( 4 ) NO DEFAULT NOT NULL
, PURCH_PNT       NUMERIC( 6, 0) NOT NULL
, ITEM_LVL_PNT    NUMERIC( 6, 0) NOT NULL
, REDEEMED_PNT    NUMERIC( 6, 0) NOT NULL
, AMT_DUE         NUMERIC( 7, 2) NOT NULL
, primary key (card_num));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """Create table  ACpadj 
(
CARD_NUM          CHAR( 19 ) NO DEFAULT NOT NULL
, TRAN_DAT          DATE NO DEFAULT NOT NULL
, STORE_NUM         CHAR( 4 ) NO DEFAULT NOT NULL
, LOC_NUM           CHAR( 3 ) NO DEFAULT NOT NULL
, SEQ_NUM           CHAR( 4 ) NO DEFAULT NOT NULL
, ADJ_CDE           CHAR( 2 ) NOT NULL
, PNT_ADJ           NUMERIC( 10, 0) NOT NULL
, BEFORE_PNT_BAL    NUMERIC( 10, 0) NOT NULL
, AFTER_PNT_BAL     NUMERIC( 10, 0) NOT NULL
, USER_ID           CHAR( 10 ) NOT NULL
, ADJ_DAT DATE NOT NULL
, primary key (card_num));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """CREATE VIEW  ACview01(    

------------------- ----------------
-- COLUMN NAME      SOURCE TABLE
------------------- ----------------    

card_num          , -- AWARD,PURCH,PADJ
DAT               , -- AWARD,PURCH,PADJ
STORE_NUM         , -- PURCH,AWARD,PADJ
LOC_NUM           , -- PURCH,AWARD,PADJ
SEQ_NUM             -- PURCH,AWARD,PADJ
)
AS
(
select
padj.card_num,
padj.tran_dat,
PADJ.STORE_NUM,PADJ.LOC_NUM,PADJ.SEQ_NUM    

from   ACpadj padj    

union all
select
pur.card_num,
pur.dat,
PUR.STORE_NUM, PUR.TERM_LOC, PUR.TERM_SEQ_NUM    

from   ACpur pur    

union all    

select
a.card_num,
a.win_dat_tim,
A.STORE_NUM, A.KIOSK_LOC_NUM, A.KIOSK_SEQ_NUM    

from   ACaward a    

) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # Store data:
    
    stmt = """insert into  ACaward values
('6006060000000000001',date '1990-05-01'
,'0001','l12', 's12','g123','p2','t',123456,'o',date
'1990-07-01' , date'1990-08-01' , 12345678
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into  ACaward values
('6006060000000000002',
date '1990-05-02' ,'0002','l22',
's22','g223','p2','t', 343456 ,'o',date '1990-07-02'
, date '1990-08-02' , 21345678 );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into  ACaward values
('6006060000000000003',
date '1990-05-03' ,'0003','l32',
's32','g323','p3','t', 767656 ,'o',date '1990-07-03'
, date '1990-08-03' , 32345678 );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into  ACaward values
('6006060000000000004',
date '1990-05-04' ,'0001','l42',
's42','g423','p4','t',567832,'o',date '1990-07-04'
, date '1990-08-04' , 42345678 );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into  ACaward values
('6006060000000000005',
date '1990-05-05' ,'0002','l12',
's52','g523','p5','t',452357,'o',date '1990-07-05'
, date '1990-08-05' , 52345678 );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    #----------------------
    stmt = """insert into  ACpur values
('6006060000000000001',
date '1990-05-01'  ,'0123','t12', 's123',123456,
654321,234567,200);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into  ACpur values
('6006060000000000002',
date '1990-05-02' , '0001','t12', 's123',567896,
454321,254567,340);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into  ACpur values
('6006060000000000003',
date '1990-05-03'    ,'0002','t22', 's323',156546,
676521,234767,600);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into  ACpur values
('6006060000000000004',date '1990-05-04' ,'0003','t12',
's133',124556, 644321,212567,900);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into  ACpur values
('6006060000000000005',date '1990-05-05' ,
'0003','t12', 's134',143456, 612321,289567,500);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    #-----------------------
    stmt = """insert into  ACpadj values
('6006060000000000001',date '1990-05-01'
,'0001','l12','s12', 'ad', 1234567890, 2345678901,
3456789012,'user000001', date '1990-07-01'  );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into  ACpadj values
('6006060000000000002',date '1990-05-02'
,'0003','l12','s12', 'ad', 1233467890, 2342348901,
3452349012,'user000002', date '1990-07-02'    );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into  ACpadj values
('6006060000000000003',date '1990-05-03'
,'0005','l12','s12', 'ad', 1567677890, 2334558901,
3456457012,'user000003', date '1990-07-03'   );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into  ACpadj values
('6006060000000000004',date '1990-05-04'
,'0002','l12','s12', 'ad', 1243534890, 2456464561,
3477787612,'user000004', date '1990-07-04'   );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into  ACpadj values
('6006060000000000005',date '1990-05-05'
,'0005','l12','s12', 'ad', 1234343890, 2367567601,
3455677012,'user000005', date '1990-07-05'   );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    #  Use view with read uncommitted access:
    stmt = """prepare s1 from
select * from  ACview01 for read uncommitted access ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s0')
    
    #  Use view with read committed access:
    stmt = """prepare s2 from
select * from  ACview01 for read committed access ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """execute s2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s1')
    
    #  Use view with serializable access:
    stmt = """prepare s3 from
select * from  ACview01 for serializable access ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """execute s3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s2')
    
    #   Do not start a transaction automatically:
    #  set autowork off;
    
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s3')
    stmt = """execute s2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s4')
    stmt = """execute s3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s5')
    
    stmt = """drop view  ACview01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table  ACaward;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table  ACpur;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table  ACpadj;"""
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
    #  Test case name:     arkt0148 : A13
    #  Description:        This test verifies the SQL UNION
    #                      statement
    #                      UNION of SELECTS, one of which returns 0
    #                      rows and forces SORT.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    # ------------------------------------------------
    #   Basic info:
    # ------------------------------------------------
    stmt = """select var_char_3,small_int from """ + gvars.g_schema_arkcasedb + """.btre204 
order by var_char_3 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s0')
    
    stmt = """select pic_x_8,small_int from """ + gvars.g_schema_arkcasedb + """.btre204 
order by pic_x_8;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s1')
    
    stmt = """select pic_x_8, sum(small_int) from """ + gvars.g_schema_arkcasedb + """.btre204 
group by pic_x_8
union
select var_char_3, sum(small_int)
from """ + gvars.g_schema_arkcasedb + """.btre204 
group by var_char_3
order by pic_x_8;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s2')
    stmt = """select pic_x_8, sum(small_int) from """ + gvars.g_schema_arkcasedb + """.btre204 
group by pic_x_8
union all
select var_char_3, sum(small_int)
from """ + gvars.g_schema_arkcasedb + """.btre204 
group by var_char_3
order by pic_x_8;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s3')
    
    stmt = """select pic_x_8 from """ + gvars.g_schema_arkcasedb + """.btre204 
group by pic_x_8
union
select var_char_3 from """ + gvars.g_schema_arkcasedb + """.btre204 
group by var_char_3
order by pic_x_8;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s4')
    stmt = """select pic_x_8 from """ + gvars.g_schema_arkcasedb + """.btre204 
group by pic_x_8
union all
select var_char_3 from """ + gvars.g_schema_arkcasedb + """.btre204 
group by var_char_3
order by pic_x_8;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s5')
    
    stmt = """select var_char_3 from """ + gvars.g_schema_arkcasedb + """.btre204 
group by var_char_3
union
select pic_x_8 from """ + gvars.g_schema_arkcasedb + """.btre204 
group by pic_x_8
order by var_char_3 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s6')
    stmt = """select var_char_3 from """ + gvars.g_schema_arkcasedb + """.btre204 
group by var_char_3
union all
select pic_x_8 from """ + gvars.g_schema_arkcasedb + """.btre204 
group by pic_x_8
order by var_char_3 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s7')
    
    #  Replace the column name by column number, and : no problem!
    
    stmt = """select pic_x_8 from """ + gvars.g_schema_arkcasedb + """.btre204 
group by pic_x_8
union
select var_char_3 from """ + gvars.g_schema_arkcasedb + """.btre204 
group by var_char_3
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s8')
    stmt = """select pic_x_8 from """ + gvars.g_schema_arkcasedb + """.btre204 
group by pic_x_8
union all
select var_char_3 from """ + gvars.g_schema_arkcasedb + """.btre204 
group by var_char_3
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s9')
    
    # ------------------------------------------------
    #   These tests from test A2, with GROUP BY added.
    # ------------------------------------------------
    
    #   UNION of CHARs with left-side of UNION longer than right-side -
    #   column names differ - ORDER BY ordinal column 1:
    stmt = """select pic_x_8 from """ + gvars.g_schema_arkcasedb + """.btre204 
group by pic_x_8
union
select char_1  from """ + gvars.g_schema_arkcasedb + """.btsel01 
group by char_1
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s10')
    
    #   UNION of CHARs with left-side of UNION shorter than right-side -
    #   ALL - column names differ - ORDER BY column name from left-side:
    stmt = """select char_1  from """ + gvars.g_schema_arkcasedb + """.btsel01 
group by char_1
union all
select pic_x_8 from """ + gvars.g_schema_arkcasedb + """.btre204 
group by pic_x_8
order by char_1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s11')
    
    #   UNION of VARCHARs with left-side of UNION longer than right-side -
    #   - column names differ - ORDER BY column names from left-side:
    stmt = """select var_char_3 from """ + gvars.g_schema_arkcasedb + """.btre204 
group by var_char_3
union all
select var_char_2 from """ + gvars.g_schema_arkcasedb + """.btre204 
group by var_char_2
order by var_char_3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s12')
    
    #   UNION of VARCHARs with left-side of UNION shorter than right-side
    #   column names differ - ORDER BY column names from left-side:
    stmt = """select var_char_2, var_char_3 from
 """ + gvars.g_schema_arkcasedb + """.btre204 
group by var_char_2,var_char_3
union all
select var_char_2, var_char_3 from
 """ + gvars.g_schema_arkcasedb + """.btre204 
group by var_char_2,var_char_3
order by var_char_2, var_char_3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s13')
    
    #   UNION of SMALLINT and INTEGER:
    stmt = """select small_int from """ + gvars.g_schema_arkcasedb + """.btsel01 
group by small_int
union all
select medium_int from """ + gvars.g_schema_arkcasedb + """.btre204 
group by medium_int
order by small_int
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s14')
    
    #   UNION of SMALLINT and LARGEINT - NULLs on both sides of UNION.
    stmt = """select small_int from """ + gvars.g_schema_arkcasedb + """.btre201 
group by small_int
union
select large_int from """ + gvars.g_schema_arkcasedb + """.btre202 
group by large_int
order by small_int
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s15')
    
    #   UNION of INTEGER and SMALLINT:
    stmt = """select medium_int from """ + gvars.g_schema_arkcasedb + """.btre204 
group by medium_int
union
select small_int  from """ + gvars.g_schema_arkcasedb + """.btsel01 
group by small_int
order by medium_int
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s16')
    
    #   UNION of INTEGER and LARGEINT - NULLs on left side of UNION:
    stmt = """select medium_int from """ + gvars.g_schema_arkcasedb + """.btre202 
group by medium_int
union
select large_int from """ + gvars.g_schema_arkcasedb + """.btsel01 
group by large_int
order by medium_int
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s17')
    
    #   UNION of LARGEINT and SMALLINT:
    stmt = """select large_int from """ + gvars.g_schema_arkcasedb + """.btsel01 
group by large_int
union
select medium_int from """ + gvars.g_schema_arkcasedb + """.btre204 
group by medium_int
order by large_int
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s18')
    
    #   UNION of LARGEINT and INTEGER - NULLs on right side of UNION:
    stmt = """select large_int from """ + gvars.g_schema_arkcasedb + """.btre204 
group by large_int
union
select medium_int from """ + gvars.g_schema_arkcasedb + """.btre202 
group by medium_int
order by large_int
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s19')
    
    #   UNION of exact numerics - left-side precision & scale greater than
    #   those on the right:
    stmt = """select binary_64_s from """ + gvars.g_schema_arkcasedb + """.btsel01 
group by binary_64_s
union
select binary_32_u from """ + gvars.g_schema_arkcasedb + """.btre201 
group by binary_32_u
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s20')
    
    #   UNION of exact numerics - left-side precision & scale less than
    #   those on the right:
    stmt = """select binary_32_u from """ + gvars.g_schema_arkcasedb + """.btre201 
group by binary_32_u
union all
select binary_64_s from """ + gvars.g_schema_arkcasedb + """.btsel01 
group by binary_64_s
order by binary_32_u desc
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s21')
    
    #   UNION of approx numerics - left-side precision greater
    #   than those on the right:
    stmt = """select float_double_p from """ + gvars.g_schema_arkcasedb + """.btre201 
group by float_double_p
union
select float_basic    from """ + gvars.g_schema_arkcasedb + """.btre202 
group by float_basic
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s22')
    
    #   UNION of approx numerics - left-side precision less
    #   than those on the right:
    stmt = """select float_basic    from """ + gvars.g_schema_arkcasedb + """.btre202 
group by float_basic
union
select float_double_p from """ + gvars.g_schema_arkcasedb + """.btre201 
group by float_double_p
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s23')
    
    #   UNION of approx numeric and binary, of approx numeric and
    #   exact numeric:
    stmt = """select float_basic, float_double_p from
 """ + gvars.g_schema_arkcasedb + """.btre201 
group by float_basic, float_double_p
union
select binary_signed, small_int from
 """ + gvars.g_schema_arkcasedb + """.btsel01 
group by binary_signed, small_int
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s24')
    
    #   See DATETIME test unit T151 for:
    #   UNION of DATETIME  - left-side startdate & enddate greater
    #      than those on the right.
    #   UNION of DATETIME  - left-side startdate & enddate less
    #      than those on the right.
    #   UNION of INTERVAL  - left-side startdate & enddate greater
    #      than those on the right.
    #   UNION of INTERVAL  - left-side startdate & enddate less
    #      than those on the right.
    
    #   UNION with empty tables on left-side:
    stmt = """select some_data      from """ + gvars.g_schema_arkcasedb + """.btemprel 
group by some_data
union
select col_9          from """ + gvars.g_schema_arkcasedb + """.btsel06 
group by col_9
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s25')
    
    #   UNION with empty tables on right-side:
    stmt = """select col_9          from """ + gvars.g_schema_arkcasedb + """.btsel06 
group by col_9
union
select some_data      from """ + gvars.g_schema_arkcasedb + """.btempkey 
group by some_data
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s26')
    
    #  UNION of empty tables on both sides:
    stmt = """select some_data      from """ + gvars.g_schema_arkcasedb + """.btempkey 
group by some_data
union
select some_data      from """ + gvars.g_schema_arkcasedb + """.btempent 
group by some_data
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    #  UNION of nonempty tables, with MATCH => empty result:
    stmt = """select decimal_1      from """ + gvars.g_schema_arkcasedb + """.btsel01 
where decimal_1 = 3
group by decimal_1
union
select medium_int    from """ + gvars.g_schema_arkcasedb + """.btsel04 
where medium_int = 3
group by medium_int
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    #   UNION of CHAR on left-side of UNION with longer VARCHAR on right:
    stmt = """select char_1     from """ + gvars.g_schema_arkcasedb + """.btsel01 
group by char_1
union all
select var_char_2 from """ + gvars.g_schema_arkcasedb + """.btre204 
group by var_char_2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s27')
    
    #   UNION of CHAR on left-side of UNION with shorter VARCHAR on
    #   right:
    stmt = """select pic_x_8    from """ + gvars.g_schema_arkcasedb + """.btre204 
group by pic_x_8
union
select var_char_3 from """ + gvars.g_schema_arkcasedb + """.btre204 
group by var_char_3
order by pic_x_8
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s28')
    
    #   Should allow ORDER BY after parenthesized UNION:
    stmt = """( select pic_x_8    from """ + gvars.g_schema_arkcasedb + """.btre204 
group by pic_x_8
union
select var_char_3 from """ + gvars.g_schema_arkcasedb + """.btre204 
group by var_char_3
)
order by pic_x_8
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s29')
    
    # ------------------------------------------------
    #   These tests are same as above, with GROUP BY;
    #   BUT each union becomes union ALL,
    #   and each union ALL becomes union.
    # ------------------------------------------------
    
    #   UNION ALL of CHARs with left-side of UNION longer than right-side -
    #   column names differ - ORDER BY ordinal column 1:
    stmt = """select pic_x_8 from """ + gvars.g_schema_arkcasedb + """.btre204 
group by pic_x_8
union ALL
select char_1  from """ + gvars.g_schema_arkcasedb + """.btsel01 
group by char_1
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s30')
    
    #   UNION of CHARs with left-side of UNION shorter than right-side -
    #   ALL - column names differ - ORDER BY column name from left-side:
    stmt = """select char_1  from """ + gvars.g_schema_arkcasedb + """.btsel01 
group by char_1
union
select pic_x_8 from """ + gvars.g_schema_arkcasedb + """.btre204 
group by pic_x_8
order by char_1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s31')
    
    #   UNION of VARCHARs with left-side of UNION longer than right-side -
    #   - column names differ - ORDER BY column names from left-side:
    stmt = """select var_char_3 from """ + gvars.g_schema_arkcasedb + """.btre204 
group by var_char_3
union
select var_char_2 from """ + gvars.g_schema_arkcasedb + """.btre204 
group by var_char_2
order by var_char_3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s32')
    
    #   UNION of VARCHARs with left-side of UNION shorter than right-side
    #   column names differ - ORDER BY column names from left-side:
    stmt = """select var_char_2, var_char_3 from
 """ + gvars.g_schema_arkcasedb + """.btre204 
group by var_char_2,var_char_3
union
select var_char_2, var_char_3 from
 """ + gvars.g_schema_arkcasedb + """.btre204 
group by var_char_2,var_char_3
order by var_char_2, var_char_3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s33')
    
    #   UNION of SMALLINT and INTEGER:
    stmt = """select small_int from """ + gvars.g_schema_arkcasedb + """.btsel01 
group by small_int
union
select medium_int from """ + gvars.g_schema_arkcasedb + """.btre204 
group by medium_int
order by small_int
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s34')
    
    #   UNION of SMALLINT and LARGEINT - NULLs on both sides of UNION.
    stmt = """select small_int from """ + gvars.g_schema_arkcasedb + """.btre201 
group by small_int
union ALL
select large_int from """ + gvars.g_schema_arkcasedb + """.btre202 
group by large_int
order by small_int
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s35')
    
    #   UNION of INTEGER and SMALLINT:
    stmt = """select medium_int from """ + gvars.g_schema_arkcasedb + """.btre204 
group by medium_int
union ALL
select small_int  from """ + gvars.g_schema_arkcasedb + """.btsel01 
group by small_int
order by medium_int
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s36')
    
    #   UNION of INTEGER and LARGEINT - NULLs on left side of UNION:
    stmt = """select medium_int from """ + gvars.g_schema_arkcasedb + """.btre202 
group by medium_int
union ALL
select large_int from """ + gvars.g_schema_arkcasedb + """.btsel01 
group by large_int
order by medium_int
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s37')
    
    #   UNION of LARGEINT and SMALLINT:
    stmt = """select large_int from """ + gvars.g_schema_arkcasedb + """.btsel01 
group by large_int
union ALL
select medium_int from """ + gvars.g_schema_arkcasedb + """.btre204 
group by medium_int
order by large_int
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s38')
    
    #   UNION of LARGEINT and INTEGER - NULLs on right side of UNION:
    stmt = """select large_int from """ + gvars.g_schema_arkcasedb + """.btre204 
group by large_int
union ALL
select medium_int from """ + gvars.g_schema_arkcasedb + """.btre202 
group by medium_int
order by large_int
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s39')
    
    #   UNION of exact numerics - left-side precision & scale greater than
    #   those on the right:
    stmt = """select binary_64_s from """ + gvars.g_schema_arkcasedb + """.btsel01 
group by binary_64_s
union ALL
select binary_32_u from """ + gvars.g_schema_arkcasedb + """.btre201 
group by binary_32_u
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s40')
    
    #   UNION of exact numerics - left-side precision & scale less than
    #   those on the right:
    stmt = """select binary_32_u from """ + gvars.g_schema_arkcasedb + """.btre201 
group by binary_32_u
union
select binary_64_s from """ + gvars.g_schema_arkcasedb + """.btsel01 
group by binary_64_s
order by binary_32_u desc
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s41')
    
    #   UNION of approx numerics - left-side precision greater
    #   than those on the right:
    stmt = """select float_double_p from """ + gvars.g_schema_arkcasedb + """.btre201 
group by float_double_p
union ALL
select float_basic    from """ + gvars.g_schema_arkcasedb + """.btre202 
group by float_basic
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s42')
    
    #   UNION of approx numerics - left-side precision less
    #   than those on the right:
    stmt = """select float_basic    from """ + gvars.g_schema_arkcasedb + """.btre202 
group by float_basic
union ALL
select float_double_p from """ + gvars.g_schema_arkcasedb + """.btre201 
group by float_double_p
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s43')
    
    #   UNION of approx numeric and binary, of approx numeric and
    #   exact numeric:
    stmt = """select float_basic, float_double_p from
 """ + gvars.g_schema_arkcasedb + """.btre201 
group by float_basic, float_double_p
union ALL
select binary_signed, small_int from
 """ + gvars.g_schema_arkcasedb + """.btsel01 
group by binary_signed, small_int
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s44')
    
    #   See DATETIME test unit T151 for:
    #   UNION of DATETIME  - left-side startdate & enddate greater
    #      than those on the right.
    #   UNION of DATETIME  - left-side startdate & enddate less
    #      than those on the right.
    #   UNION of INTERVAL  - left-side startdate & enddate greater
    #      than those on the right.
    #   UNION of INTERVAL  - left-side startdate & enddate less
    #      than those on the right.
    
    #   UNION with empty tables on left-side:
    stmt = """select some_data      from """ + gvars.g_schema_arkcasedb + """.btemprel 
group by some_data
union ALL
select col_9          from """ + gvars.g_schema_arkcasedb + """.btsel06 
group by col_9
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s45')
    
    #   UNION with empty tables on right-side:
    stmt = """select col_9          from """ + gvars.g_schema_arkcasedb + """.btsel06 
group by col_9
union ALL
select some_data      from """ + gvars.g_schema_arkcasedb + """.btempkey 
group by some_data
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s46')
    
    #  UNION of empty tables on both sides:
    stmt = """select some_data      from """ + gvars.g_schema_arkcasedb + """.btempkey 
group by some_data
union ALL
select some_data      from """ + gvars.g_schema_arkcasedb + """.btempent 
group by some_data
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    #  UNION of nonempty tables, with MATCH => empty result:
    stmt = """select decimal_1      from """ + gvars.g_schema_arkcasedb + """.btsel01 
where decimal_1 = 3
group by decimal_1
union ALL
select medium_int    from """ + gvars.g_schema_arkcasedb + """.btsel04 
where medium_int = 3
group by medium_int
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """select char_1     from """ + gvars.g_schema_arkcasedb + """.btsel01 
group by char_1
union
select var_char_2 from """ + gvars.g_schema_arkcasedb + """.btre204 
group by var_char_2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s47')
    
    #   UNION of CHAR on left-side of UNION with shorter VARCHAR on
    #   right:
    stmt = """select pic_x_8    from """ + gvars.g_schema_arkcasedb + """.btre204 
group by pic_x_8
union ALL
select var_char_3 from """ + gvars.g_schema_arkcasedb + """.btre204 
group by var_char_3
order by pic_x_8
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s48')
    
    #   Should allow ORDER BY after parenthesized UNION:
    stmt = """( select pic_x_8    from """ + gvars.g_schema_arkcasedb + """.btre204 
group by pic_x_8
union ALL
select var_char_3 from """ + gvars.g_schema_arkcasedb + """.btre204 
group by var_char_3
)
order by pic_x_8
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s49')
    
    _testmgr.testcase_end(desc)

def test013(desc="""a14"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0148 : A14
    #  Description:        This test verifies the SQL UNION
    #                      statement
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    stmt = """drop view custsupp;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create view custsupp 
(state, cname)
as
( select s.state, s.suppname
from """ + gvars.g_schema_arkcasedb + """.supplier s
union all
select c.state, c.custname
from """ + gvars.g_schema_arkcasedb + """.customer c
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from custsupp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a14exp""", 'a14s1')
    
    stmt = """select *
from custsupp 
--   where state, cname >= 'CALIFORNIA', 'M'
where state >= 'CALIFORNIA'
--    order by 1 ;
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a14exp""", 'a14s2')
    
    stmt = """prepare S1 from
select *
from custsupp 
--    where state, cname >= 'CALIFORNIA', 'M'  ;
where state >= 'CALIFORNIA';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select SEQ_NUM,  OPERATOR, LEFT_CHILD_SEQ_NUM, RIGHT_CHILD_SEQ_NUM,
TNAME
from TABLE( EXPLAIN (NULL, 'S1'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """drop view custsupp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # #testcase a15 a15
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0148 : A15
    #  Description:        This test verifies the SQL UNION
    #                      statement
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    _testmgr.testcase_end(desc)

def test014(desc="""a16"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0148 : A16
    #  Description:        This test verifies the SQL UNION
    #                      statement
    #                      SELECT with param in WHERE clause
    #                      on view that is a UNION.
    #  *  Problem reported in host, but behavior appears
    #  *  in SQLCI with params, and that's what's tested.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    #------------------------------------------------
    #  UNION in view; use of param:
    #------------------------------------------------
    stmt = """create table  agtab3 ( e char(4), p char(6) ) no partition ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table  agtab4 ( e char(4), p char(6) ) no partition ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create view agvy2 (e, p) as
( select * from agtab3 
union
select * from agtab4 
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #  20 unions:
    stmt = """create view agvy3 (e, p) as
( select * from agtab3 
union
select * from agtab4 
union
select * from agtab3 
union
select * from agtab4 
union
select * from agtab3 
union
select * from agtab4 
union
select * from agtab3 
union
select * from agtab4 
union
select * from agtab3 
union
select * from agtab4 
union
select * from agtab3 
union
select * from agtab4 
union
select * from agtab3 
union
select * from agtab4 
union
select * from agtab3 
union
select * from agtab4 
union
select * from agtab3 
union
select * from agtab4 
union
select * from agtab3 
union
select * from agtab4 
union
select * from agtab3 
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #  60 unions:
    stmt = """create view agvy4 (e, p) as
( select * from agtab3 
union all
select * from agtab4 
union
select * from agtab3 
union all
select * from agtab4 
union
select * from agtab3 
union
select * from agtab4 
union
select * from agtab3 
union
select * from agtab4 
union
select * from agtab3 
union
select * from agtab4 
union
select * from agtab3 
union
select * from agtab4 
union
select * from agtab3 
union
select * from agtab4 
union
select * from agtab3 
union
select * from agtab4 
union
select * from agtab3 
union
select * from agtab4 
union
select * from agtab3 
union
select * from agtab4 
union
select * from agtab3 
union
select * from agtab4 
union
select * from agtab3 
union
select * from agtab4 
union
select * from agtab3 
union
select * from agtab4 
union
select * from agtab3 
union
select * from agtab4 
union
select * from agtab3 
union
select * from agtab4 
union
select * from agtab3 
union
select * from agtab4 
union
select * from agtab3 
union
select * from agtab4 
union
select * from agtab3 
union
select * from agtab4 
union
select * from agtab3 
union
select * from agtab4 
union
select * from agtab3 
union
select * from agtab4 
union
select * from agtab3 
union
select * from agtab4 
union
select * from agtab3 
union
select * from agtab4 
union
select * from agtab3 
union
select * from agtab4 
union
select * from agtab3 
union
select * from agtab4 
union
select * from agtab3 
union
select * from agtab4 
union
select * from agtab3 
union
select * from agtab4 
union
select * from agtab3 
union
select * from agtab4 
union
select * from agtab3 
union
select * from agtab4 
union
select * from agtab3 
union
select * from agtab4 
union
select * from agtab3 
union
select * from agtab4 
union
select * from agtab3 
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #  Create views, report contents:
    stmt = """create view agview1 (c, s) as
( select city, state from """ + gvars.g_schema_arkcasedb + """.customer 
union
select city, state from """ + gvars.g_schema_arkcasedb + """.customer 
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """CREATE TABLE  agtable1 ( col_string   PIC X NOT NULL ) no partition ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """CREATE TABLE  agtableN ( col_string   PIC X DEFAULT NULL ) no partition ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create view agview2 (c) as
( SELECT col_string FROM agtable1 
UNION
SELECT col_string FROM agtableN 
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create view agview3 (c) as
( SELECT col_string FROM agtableN 
UNION ALL
SELECT col_string FROM agtable1 
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #  Added local dup to avoid massive db_copy.  But must use
    #  local copy of table to create view, so do not interfer with
    #  global database.
    #    dup btsel01, * , views explicit ;
    #    dup btsel06, * , views explicit ;
    #    dup btre202, * , views explicit ;
    #    dup btre204, * , views explicit ;
    #    dup btre208, * , views explicit ;
    #    dup btre211, * , views explicit ;
    #    dup btemprel,* , views explicit ;
    #    dup btempkey,* , views explicit ;
    
    stmt = """DROP TABLE BTRE211;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE   BTRE211 (
Y_to_D      DATE,
Y_to_S      TIMESTAMP(0),
Y_to_F      TIMESTAMP(6),
H_to_S      TIME,
H_to_F      TIME(6)
) no partition
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO BTRE211 VALUES (
date '1988-01-01' ,
timestamp '1988-01-01 12:35:30' ,
timestamp '1988-01-01 12:35:30.333' ,
time '10:15:30' ,
time '10:15:30.555'
) ;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO BTRE211 VALUES (
date '1977-03-02' ,
timestamp '1979-06-05 14:40:45' ,
timestamp '1980-07-06 15:45:50.678' ,
time '03:53:56' ,
time '04:54:57.345'
) ;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO BTRE211 VALUES (
date '0802-09-07' ,
timestamp '0805-12-10 07:59:03' ,
timestamp '0806-01-11 08:01:04.789' ,
time '18:08:09' ,
time '19:09:10.234'
) ;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO BTRE211 VALUES (
date '0100-01-01' ,
timestamp '0100-01-01 00:00:00' ,
timestamp '0100-01-01 00:00:00.00' ,
time '00:00:00' ,
time '00:00:00.0'
) ;"""
    output = _dci.cmdexec(stmt)
    
    #  UNION of same-length CHAR - 1-column operands:
    #  Dup ALL!! tables to local!
    stmt = """create view agview4 (char_1) as
( select char_1 from """ + gvars.g_schema_arkcasedb + """.btsel01 
union all
select char_1 from """ + gvars.g_schema_arkcasedb + """.btre204 
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #  UNION of two pairs of same-length VARCHARs - 2-column operands:
    #  Dup ALL!! tables to local!
    stmt = """create view agview5 (vc2, vc3) as
( select var_char_2, var_char_3 from """ + gvars.g_schema_arkcasedb + """.btre204 
union all
select var_char_2, var_char_3 from """ + gvars.g_schema_arkcasedb + """.btre208 
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #  UNION of DATETIME with same startdate and same enddate - 1-column
    #  operands:
    #  Dup ALL!! tables to local!
    stmt = """select y_to_d from """ + gvars.g_schema_arkcasedb + """.btre204;"""
    output = _dci.cmdexec(stmt)
    stmt = """select y_to_d from BTRE211;"""
    output = _dci.cmdexec(stmt)
    stmt = """create view agview6 (ytod) as
( select y_to_d from """ + gvars.g_schema_arkcasedb + """.btre204 
union all
select y_to_d from BTRE211 
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from agview6;"""
    output = _dci.cmdexec(stmt)
    #  UNION of CHARs with left-side of UNION longer than right-side -
    #  column names differ - ORDER BY ordinal column 1:
    #  Dup ALL!! tables to local!
    stmt = """create view agview7 (picx8) as
( select pic_x_8 from """ + gvars.g_schema_arkcasedb + """.btre204 
union
select char_1  from """ + gvars.g_schema_arkcasedb + """.btsel01 
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #  UNION of CHARs with left-side of UNION shorter than right-side -
    #  ALL - column names differ - ORDER BY column name from left-side:
    stmt = """create view agview8 (char1) as
( select char_1  from """ + gvars.g_schema_arkcasedb + """.btsel01 
union
select pic_x_8 from """ + gvars.g_schema_arkcasedb + """.btre204 
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #  UNION of LARGEINT and INTEGER - NULLs on right side of UNION:
    stmt = """create view agview9 (lint) as
( select large_int from """ + gvars.g_schema_arkcasedb + """.btre204 
union
select medium_int from """ + gvars.g_schema_arkcasedb + """.btre202 
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """set param ?n 100   ;"""
    output = _dci.cmdexec(stmt)
    
    #  UNION with empty tables on left-side:
    stmt = """create view agviewa (x) as
( select some_data      from """ + gvars.g_schema_arkcasedb + """.btemprel 
union
select col_9          from """ + gvars.g_schema_arkcasedb + """.btsel06 
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #  UNION with empty tables on right-side:
    stmt = """create view agviewb (x) as
( select col_9          from """ + gvars.g_schema_arkcasedb + """.btsel06 
union
select some_data      from """ + gvars.g_schema_arkcasedb + """.btemprel 
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #  UNION of empty tables on both sides:
    stmt = """create view agviewc (x) as
( select some_data      from """ + gvars.g_schema_arkcasedb + """.btempkey 
union
select some_data      from """ + gvars.g_schema_arkcasedb + """.btemprel 
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into    agtab3 values ( 'BBBB', 'BBBBBB' ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into    agtab3 values ( 'AAAA', 'BBBBBB' ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """select * from  agtab3 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s0')
    
    stmt = """insert into    agtab4 values ( 'ABBB', 'BBBBBB' ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into    agtab4 values ( 'ABCC', 'BBBBBB' ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into    agtab4 values ( 'BBCC', 'BBBBBB' ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into    agtab4 values ( 'BBCD', 'BBBBBB' ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select * from  agtab4 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s1')
    stmt = """select * from  agvy2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s2')
    
    stmt = """set param ?eparam 'ABCD'   ;"""
    output = _dci.cmdexec(stmt)
    stmt = """select * from  agvy2 where e > ?eparam ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s3')
    stmt = """select * from  agvy2 where e = ?eparam ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """select * from  agvy2 where e < ?eparam ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s4')
    
    stmt = """select * from  agvy2 where e > 'ABCD' ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s5')
    stmt = """select * from  agvy2 where e = 'ABCD'   ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """select * from  agvy2 where e < 'ABCD' ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s6')
    
    stmt = """select * from  agvy3 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s7')
    stmt = """select * from  agvy3 where e > ?eparam ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s8')
    stmt = """select * from  agvy3 where e = ?eparam ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """select * from  agvy3 where e < ?eparam ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s9')
    
    stmt = """select * from  agvy3 where e > 'ABCD' ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s10')
    stmt = """select * from  agvy3 where e = 'ABCD'   ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """select * from  agview1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s12')
    stmt = """select * from  agview1 where c >  'M' ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s13')
    stmt = """select * from  agview1 where c <= 'M' ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s14')
    
    #------------------------
    #  Params:
    #------------------------
    stmt = """set param ?a1 'M'   ;"""
    output = _dci.cmdexec(stmt)
    stmt = """select * from  agview1 where c >  ?a1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s15')
    stmt = """select * from  agview1 where c <= ?a1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s16')
    
    #  UNION between old and new objects - SELECT:
    stmt = """INSERT INTO    agtable1 VALUES ( 'A' ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO    agtable1 VALUES ( 'B' ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO    agtable1 VALUES ( 'C' ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """SELECT * FROM  agtable1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s17')
    
    stmt = """INSERT INTO    agtableN VALUES ( 'A' ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO    agtableN VALUES ( 'C' ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """SELECT * FROM  agtableN ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s18')
    
    stmt = """set param ?p 'B'   ;"""
    output = _dci.cmdexec(stmt)
    stmt = """select * from  agview2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s19')
    stmt = """select * from  agview2 where c >= 'B' ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s20')
    stmt = """select * from  agview2 where c >= ?p ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s21')
    stmt = """select * from  agview3 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s22')
    stmt = """select * from  agview3 where c >= 'B' ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s23')
    stmt = """select * from  agview3 where c >= ?p ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s24')
    
    stmt = """select col_string from  agtable1 union
select col_string from  agtableN  ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s25')
    
    stmt = """select col_string from  agtable1 union
select col_string from  agtableN where col_string > 'B' ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s26')
    
    stmt = """select col_string from  agtable1 union all
select col_string from  agtable1 where col_string > ?p ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s27')
    
    #   Bug: ERROR from SQL [-8030]: SQL statement has an invalid
    #                                object.
    stmt = """select col_string from  agtable1 union all
select col_string from  agtableN where col_string > 'B' ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s28')
    
    #   Bug: ERROR from SQL [-8999]: Internal error:  SQL executor.
    stmt = """select col_string from  agtable1 union
select col_string from  agtable1 where col_string > ?p ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s29')
    
    #   Bug: ERROR from SQL [-8999]: Internal error:  SQL executor.
    stmt = """select col_string from  agtable1 union all
select col_string from  agtable1 where col_string >= 'B';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s30')
    
    stmt = """set param ?p 'B'   ;"""
    output = _dci.cmdexec(stmt)
    stmt = """select * from  agview4 order by char_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s31')
    stmt = """select * from  agview4 where char_1 >= 'B' ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s32')
    stmt = """select * from  agview4 where char_1 >= ?p ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s33')
    
    stmt = """set param ?p 'E'   ;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?q 'rum' ;"""
    output = _dci.cmdexec(stmt)
    stmt = """select * from  agview5 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s34')
    stmt = """select * from  agview5 where vc2 = 'E' and vc3 = 'rum' ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s35')
    stmt = """select * from  agview5 where vc2 = ?p  and vc3 = ?q ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s36')
    
    stmt = """set param ?p '1977-03-02'   ;"""
    output = _dci.cmdexec(stmt)
    stmt = """select * from  agview6 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s37')
    stmt = """select * from  agview6 where ytod = date '0802-09-07';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s38')
    stmt = """select * from  agview6 where ytod = date '1977-03-02' ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s39')
    stmt = """select * from  agview6 where ytod = ?p ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s40')
    
    stmt = """set param ?p 'B'   ;"""
    output = _dci.cmdexec(stmt)
    stmt = """select * from  agview7 order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s41')
    stmt = """select * from  agview7 where picx8 > 'B' order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s42')
    stmt = """select * from  agview7 where picx8 > ?p  order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s43')
    
    stmt = """set param ?p 'C'   ;"""
    output = _dci.cmdexec(stmt)
    stmt = """select * from  agview8 order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s44')
    stmt = """select * from  agview8 where char1 > 'C' order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s45')
    stmt = """select * from  agview8 where char1 > ?p  order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s46')
    
    stmt = """set param ?n 100   ;"""
    output = _dci.cmdexec(stmt)
    stmt = """select * from  agview9 order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s47')
    stmt = """select * from  agview9 where lint > 100 order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s48')
    stmt = """select * from  agview9 where lint > ?n  order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s49')
    
    stmt = """set param ?n 99    ;"""
    output = _dci.cmdexec(stmt)
    stmt = """select * from  agviewa order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s50')
    stmt = """select * from  agviewa where x > 99  order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s51')
    stmt = """select * from  agviewa where x > ?n  order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s52')
    
    stmt = """set param ?n 99    ;"""
    output = _dci.cmdexec(stmt)
    stmt = """select * from  agviewb order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s53')
    stmt = """select * from  agviewb where x > 99  order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s54')
    stmt = """select * from  agviewb where x > ?n  order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s55')
    
    stmt = """set param ?n 99    ;"""
    output = _dci.cmdexec(stmt)
    stmt = """select * from  agviewc order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """select * from  agviewc where x > 99  order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """select * from  agviewc where x > ?n  order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """drop view agvy2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view agvy3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view agvy4;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """drop view agview1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop view agview2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view agview3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view agview4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view agview5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view agview6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view agview7 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view agview8;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view agview9;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop view agviewa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view agviewb;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view agviewc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop table  agtab3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table  agtab4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop TABLE  agtable1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop TABLE  agtableN;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test015(desc="""a17"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0148 : A17
    #  Description:        This test verifies the SQL UNION
    #                      statement
    #                      UNIONs with various numeric types.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    #   *  This test case creates its own base tables and
    #   *  shorthand views.  Columns were choosen representing
    #   *  all numeric types.  The base tables contain
    #   *  limits values for each data type.
    #   *  SELECTs with UNIONs combine unlike numeric data
    #   *  types.
    #   *  Shorthand views are created to examine resultant
    #   *  column characteristics from the COLUMNS tables.
    
    #  Create LOG file
    
    #  The SELECTs that follow involve UNIONs that combine smallint,
    #  integer and largeint data type in different ways.
    #  This is the subject area of the TRP for which this testcase
    #  was constructed.
    #  These 25 tests use UNION without the ALL option.
    #  With C30.07, 10 of these 25 tests fail producing error -8402.
    
    stmt = """create table ahtab1 
(row_key            char (4)        no default  not null
,smallint_signed    smallint        signed
,smallint_unsigned  smallint        unsigned
,integer_signed     integer         signed
,integer_unsigned   integer         unsigned
,largeint_signed    largeint        signed
,numeric_s_4_0      numeric (4,0)   signed
,numeric_s_4_2      numeric (4,2)   signed
,numeric_s_9_2      numeric (9,2)   signed
,numeric_u_9_9      numeric (9,9)   unsigned
,numeric_s_18_9     numeric (18,9)  signed
,numeric_s_18_18    numeric (18,18) signed
,real_              real
,double_precision   double precision
,decimal_s_3_1      decimal (3,1)   signed
,decimal_u_1_0      decimal (1,0)   unsigned
,decimal_s_18_2     decimal (18,2)  signed
,primary key (row_key)
)
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table ahtab2 
(row_key            char (4)        no default  not null
,smallint_signed    smallint        signed
,smallint_unsigned  smallint        unsigned
,integer_signed     integer         signed
,integer_unsigned   integer         unsigned
,largeint_signed    largeint        signed
,numeric_s_4_0      numeric (4,0)   signed
,numeric_s_4_2      numeric (4,2)   signed
,numeric_s_9_2      numeric (9,2)   signed
,numeric_u_9_9      numeric (9,9)   unsigned
,numeric_s_18_9     numeric (18,9)  signed
,numeric_s_18_18    numeric (18,18) signed
,real_              real
,double_precision   double precision
,decimal_s_3_1      decimal (3,1)   signed
,decimal_u_1_0      decimal (1,0)   unsigned
,decimal_s_18_2     decimal (18,2)  signed
,primary key (row_key)
)
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create view ahv1 
(smallint_signed
,smallint_unsigned
,integer_signed
,integer_unsigned
,largeint_signed
,numeric_s_4_0
,numeric_s_4_2
,numeric_s_9_2
,numeric_u_9_9
,numeric_s_18_9
,numeric_s_18_18
,real_
,double_precision
,decimal_s_3_1
,decimal_u_1_0
,decimal_s_18_2)
as (
select
smallint_signed
,smallint_unsigned
,integer_signed
,integer_unsigned
,largeint_signed
,numeric_s_4_0
,numeric_s_4_2
,numeric_s_9_2
,numeric_u_9_9
,numeric_s_18_9
,numeric_s_18_18
,real_
,double_precision
,decimal_s_3_1
,decimal_u_1_0
,decimal_s_18_2
from ahtab1 
union
select
smallint_signed
,smallint_unsigned
,integer_signed
,integer_unsigned
,largeint_signed
,numeric_s_4_0
,numeric_s_4_2
,numeric_s_9_2
,numeric_u_9_9
,numeric_s_18_9
,numeric_s_18_18
,real_
,double_precision
,decimal_s_3_1
,decimal_u_1_0
,decimal_s_18_2
from ahtab2 
)
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create view ahv2 
(smallint_signed
,smallint_unsigned
,integer_signed
,integer_unsigned
,largeint_signed
,numeric_s_4_0
,numeric_s_4_2
,numeric_s_9_2
,numeric_u_9_9
,numeric_s_18_9
,numeric_s_18_18
,real_
,double_precision
,decimal_s_3_1
,decimal_u_1_0
,decimal_s_18_2)
as (
select
smallint_signed
,smallint_unsigned
,integer_signed
,integer_unsigned
,largeint_signed
,numeric_s_4_0
,numeric_s_4_2
,numeric_s_9_2
,numeric_u_9_9
,numeric_s_18_9
,numeric_s_18_18
,real_
,double_precision
,decimal_s_3_1
,decimal_u_1_0
,decimal_s_18_2
from ahtab1 
union
select
smallint_unsigned
,integer_signed
,integer_unsigned
,largeint_signed
,numeric_s_4_0
,numeric_s_4_2
,numeric_s_9_2
,numeric_u_9_9
,numeric_s_18_9
,numeric_s_18_18
,real_
,double_precision
,decimal_s_3_1
,decimal_u_1_0
,decimal_s_18_2
,smallint_signed
from ahtab2 
)
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create view ahv3 
(smallint_signed
,smallint_unsigned
,integer_signed
,integer_unsigned
,largeint_signed
,numeric_s_4_0
,numeric_s_4_2
,numeric_s_9_2
,numeric_u_9_9
,numeric_s_18_9
,numeric_s_18_18
,real_
,double_precision
,decimal_s_3_1
,decimal_u_1_0
,decimal_s_18_2)
as (
select
smallint_signed
,smallint_unsigned
,integer_signed
,integer_unsigned
,largeint_signed
,numeric_s_4_0
,numeric_s_4_2
,numeric_s_9_2
,numeric_u_9_9
,numeric_s_18_9
,numeric_s_18_18
,real_
,double_precision
,decimal_s_3_1
,decimal_u_1_0
,decimal_s_18_2
from ahtab1 
union
select
integer_signed
,integer_unsigned
,largeint_signed
,numeric_s_4_0
,numeric_s_4_2
,numeric_s_9_2
,numeric_u_9_9
,numeric_s_18_9
,numeric_s_18_18
,real_
,double_precision
,decimal_s_3_1
,decimal_u_1_0
,decimal_s_18_2
,smallint_signed
,smallint_unsigned
from ahtab2 
)
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create view ahv4 
(smallint_signed
,smallint_unsigned
,integer_signed
,integer_unsigned
,largeint_signed
,numeric_s_4_0
,numeric_s_4_2
,numeric_s_9_2
,numeric_u_9_9
,numeric_s_18_9
,numeric_s_18_18
,real_
,double_precision
,decimal_s_3_1
,decimal_u_1_0
,decimal_s_18_2)
as (
select
smallint_signed
,smallint_unsigned
,integer_signed
,integer_unsigned
,largeint_signed
,numeric_s_4_0
,numeric_s_4_2
,numeric_s_9_2
,numeric_u_9_9
,numeric_s_18_9
,numeric_s_18_18
,real_
,double_precision
,decimal_s_3_1
,decimal_u_1_0
,decimal_s_18_2
from ahtab1 
union
select
integer_unsigned
,largeint_signed
,numeric_s_4_0
,numeric_s_4_2
,numeric_s_9_2
,numeric_u_9_9
,numeric_s_18_9
,numeric_s_18_18
,real_
,double_precision
,decimal_s_3_1
,decimal_u_1_0
,decimal_s_18_2
,smallint_signed
,smallint_unsigned
,integer_signed
from ahtab2 
)
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create view ahv5 
(smallint_signed
,smallint_unsigned
,integer_signed
,integer_unsigned
,largeint_signed
,numeric_s_4_0
,numeric_s_4_2
,numeric_s_9_2
,numeric_u_9_9
,numeric_s_18_9
,numeric_s_18_18
,real_
,double_precision
,decimal_s_3_1
,decimal_u_1_0
,decimal_s_18_2)
as (
select
smallint_signed
,smallint_unsigned
,integer_signed
,integer_unsigned
,largeint_signed
,numeric_s_4_0
,numeric_s_4_2
,numeric_s_9_2
,numeric_u_9_9
,numeric_s_18_9
,numeric_s_18_18
,real_
,double_precision
,decimal_s_3_1
,decimal_u_1_0
,decimal_s_18_2
from ahtab1 
union
select
largeint_signed
,numeric_s_4_0
,numeric_s_4_2
,numeric_s_9_2
,numeric_u_9_9
,numeric_s_18_9
,numeric_s_18_18
,real_
,double_precision
,decimal_s_3_1
,decimal_u_1_0
,decimal_s_18_2
,smallint_signed
,smallint_unsigned
,integer_signed
,integer_unsigned
from ahtab2 
)
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create view ahv6 
(smallint_signed
,smallint_unsigned
,integer_signed
,integer_unsigned
,largeint_signed
,numeric_s_4_0
,numeric_s_4_2
,numeric_s_9_2
,numeric_u_9_9
,numeric_s_18_9
,numeric_s_18_18
,real_
,double_precision
,decimal_s_3_1
,decimal_u_1_0
,decimal_s_18_2)
as (
select
smallint_signed
,smallint_unsigned
,integer_signed
,integer_unsigned
,largeint_signed
,numeric_s_4_0
,numeric_s_4_2
,numeric_s_9_2
,numeric_u_9_9
,numeric_s_18_9
,numeric_s_18_18
,real_
,double_precision
,decimal_s_3_1
,decimal_u_1_0
,decimal_s_18_2
from ahtab1 
union
select
numeric_s_4_0
,numeric_s_4_2
,numeric_s_9_2
,numeric_u_9_9
,numeric_s_18_9
,numeric_s_18_18
,real_
,double_precision
,decimal_s_3_1
,decimal_u_1_0
,decimal_s_18_2
,smallint_signed
,smallint_unsigned
,integer_signed
,integer_unsigned
,largeint_signed
from ahtab2 
)
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create view ahv7 
(smallint_signed
,smallint_unsigned
,integer_signed
,integer_unsigned
,largeint_signed
,numeric_s_4_0
,numeric_s_4_2
,numeric_s_9_2
,numeric_u_9_9
,numeric_s_18_9
,numeric_s_18_18
,real_
,double_precision
,decimal_s_3_1
,decimal_u_1_0
,decimal_s_18_2)
as (
select
smallint_signed
,smallint_unsigned
,integer_signed
,integer_unsigned
,largeint_signed
,numeric_s_4_0
,numeric_s_4_2
,numeric_s_9_2
,numeric_u_9_9
,numeric_s_18_9
,numeric_s_18_18
,real_
,double_precision
,decimal_s_3_1
,decimal_u_1_0
,decimal_s_18_2
from ahtab1 
union
select
numeric_s_4_2
,numeric_s_9_2
,numeric_u_9_9
,numeric_s_18_9
,numeric_s_18_18
,real_
,double_precision
,decimal_s_3_1
,decimal_u_1_0
,decimal_s_18_2
,smallint_signed
,smallint_unsigned
,integer_signed
,integer_unsigned
,largeint_signed
,numeric_s_4_0
from ahtab2 
)
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create view ahv8 
(smallint_signed
,smallint_unsigned
,integer_signed
,integer_unsigned
,largeint_signed
,numeric_s_4_0
,numeric_s_4_2
,numeric_s_9_2
,numeric_u_9_9
,numeric_s_18_9
,numeric_s_18_18
,real_
,double_precision
,decimal_s_3_1
,decimal_u_1_0
,decimal_s_18_2)
as (
select
smallint_signed
,smallint_unsigned
,integer_signed
,integer_unsigned
,largeint_signed
,numeric_s_4_0
,numeric_s_4_2
,numeric_s_9_2
,numeric_u_9_9
,numeric_s_18_9
,numeric_s_18_18
,real_
,double_precision
,decimal_s_3_1
,decimal_u_1_0
,decimal_s_18_2
from ahtab1 
union
select
numeric_s_9_2
,numeric_u_9_9
,numeric_s_18_9
,numeric_s_18_18
,real_
,double_precision
,decimal_s_3_1
,decimal_u_1_0
,decimal_s_18_2
,smallint_signed
,smallint_unsigned
,integer_signed
,integer_unsigned
,largeint_signed
,numeric_s_4_0
,numeric_s_4_2
from ahtab2 
)
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create view ahv9 
(smallint_signed
,smallint_unsigned
,integer_signed
,integer_unsigned
,largeint_signed
,numeric_s_4_0
,numeric_s_4_2
,numeric_s_9_2
,numeric_u_9_9
,numeric_s_18_9
,numeric_s_18_18
,real_
,double_precision
,decimal_s_3_1
,decimal_u_1_0
,decimal_s_18_2)
as (
select
smallint_signed
,smallint_unsigned
,integer_signed
,integer_unsigned
,largeint_signed
,numeric_s_4_0
,numeric_s_4_2
,numeric_s_9_2
,numeric_u_9_9
,numeric_s_18_9
,numeric_s_18_18
,real_
,double_precision
,decimal_s_3_1
,decimal_u_1_0
,decimal_s_18_2
from ahtab1 
union
select
numeric_u_9_9
,numeric_s_18_9
,numeric_s_18_18
,real_
,double_precision
,decimal_s_3_1
,decimal_u_1_0
,decimal_s_18_2
,smallint_signed
,smallint_unsigned
,integer_signed
,integer_unsigned
,largeint_signed
,numeric_s_4_0
,numeric_s_4_2
,numeric_s_9_2
from ahtab2 
)
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create view ahv10 
(smallint_signed
,smallint_unsigned
,integer_signed
,integer_unsigned
,largeint_signed
,numeric_s_4_0
,numeric_s_4_2
,numeric_s_9_2
,numeric_u_9_9
,numeric_s_18_9
,numeric_s_18_18
,real_
,double_precision
,decimal_s_3_1
,decimal_u_1_0
,decimal_s_18_2)
as (
select
smallint_signed
,smallint_unsigned
,integer_signed
,integer_unsigned
,largeint_signed
,numeric_s_4_0
,numeric_s_4_2
,numeric_s_9_2
,numeric_u_9_9
,numeric_s_18_9
,numeric_s_18_18
,real_
,double_precision
,decimal_s_3_1
,decimal_u_1_0
,decimal_s_18_2
from ahtab1 
union
select
numeric_s_18_9
,numeric_s_18_18
,real_
,double_precision
,decimal_s_3_1
,decimal_u_1_0
,decimal_s_18_2
,smallint_signed
,smallint_unsigned
,integer_signed
,integer_unsigned
,largeint_signed
,numeric_s_4_0
,numeric_s_4_2
,numeric_s_9_2
,numeric_u_9_9
from ahtab2 
)
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create view ahv11 
(smallint_signed
,smallint_unsigned
,integer_signed
,integer_unsigned
,largeint_signed
,numeric_s_4_0
,numeric_s_4_2
,numeric_s_9_2
,numeric_u_9_9
,numeric_s_18_9
,numeric_s_18_18
,real_
,double_precision
,decimal_s_3_1
,decimal_u_1_0
,decimal_s_18_2)
as (
select
smallint_signed
,smallint_unsigned
,integer_signed
,integer_unsigned
,largeint_signed
,numeric_s_4_0
,numeric_s_4_2
,numeric_s_9_2
,numeric_u_9_9
,numeric_s_18_9
,numeric_s_18_18
,real_
,double_precision
,decimal_s_3_1
,decimal_u_1_0
,decimal_s_18_2
from ahtab1 
union
select
numeric_s_18_18
,real_
,double_precision
,decimal_s_3_1
,decimal_u_1_0
,decimal_s_18_2
,smallint_signed
,smallint_unsigned
,integer_signed
,integer_unsigned
,largeint_signed
,numeric_s_4_0
,numeric_s_4_2
,numeric_s_9_2
,numeric_u_9_9
,numeric_s_18_9
from ahtab2 
)
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create view ahv12 
(smallint_signed
,smallint_unsigned
,integer_signed
,integer_unsigned
,largeint_signed
,numeric_s_4_0
,numeric_s_4_2
,numeric_s_9_2
,numeric_u_9_9
,numeric_s_18_9
,numeric_s_18_18
,real_
,double_precision
,decimal_s_3_1
,decimal_u_1_0
,decimal_s_18_2)
as (
select
smallint_signed
,smallint_unsigned
,integer_signed
,integer_unsigned
,largeint_signed
,numeric_s_4_0
,numeric_s_4_2
,numeric_s_9_2
,numeric_u_9_9
,numeric_s_18_9
,numeric_s_18_18
,real_
,double_precision
,decimal_s_3_1
,decimal_u_1_0
,decimal_s_18_2
from ahtab1 
union
select
real_
,double_precision
,decimal_s_3_1
,decimal_u_1_0
,decimal_s_18_2
,smallint_signed
,smallint_unsigned
,integer_signed
,integer_unsigned
,largeint_signed
,numeric_s_4_0
,numeric_s_4_2
,numeric_s_9_2
,numeric_u_9_9
,numeric_s_18_9
,numeric_s_18_18
from ahtab2 
)
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create view ahv13 
(smallint_signed
,smallint_unsigned
,integer_signed
,integer_unsigned
,largeint_signed
,numeric_s_4_0
,numeric_s_4_2
,numeric_s_9_2
,numeric_u_9_9
,numeric_s_18_9
,numeric_s_18_18
,real_
,double_precision
,decimal_s_3_1
,decimal_u_1_0
,decimal_s_18_2)
as (
select
smallint_signed
,smallint_unsigned
,integer_signed
,integer_unsigned
,largeint_signed
,numeric_s_4_0
,numeric_s_4_2
,numeric_s_9_2
,numeric_u_9_9
,numeric_s_18_9
,numeric_s_18_18
,real_
,double_precision
,decimal_s_3_1
,decimal_u_1_0
,decimal_s_18_2
from ahtab1 
union
select
double_precision
,decimal_s_3_1
,decimal_u_1_0
,decimal_s_18_2
,smallint_signed
,smallint_unsigned
,integer_signed
,integer_unsigned
,largeint_signed
,numeric_s_4_0
,numeric_s_4_2
,numeric_s_9_2
,numeric_u_9_9
,numeric_s_18_9
,numeric_s_18_18
,real_
from ahtab2 
)
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create view ahv14 
(smallint_signed
,smallint_unsigned
,integer_signed
,integer_unsigned
,largeint_signed
,numeric_s_4_0
,numeric_s_4_2
,numeric_s_9_2
,numeric_u_9_9
,numeric_s_18_9
,numeric_s_18_18
,real_
,double_precision
,decimal_s_3_1
,decimal_u_1_0
,decimal_s_18_2)
as (
select
smallint_signed
,smallint_unsigned
,integer_signed
,integer_unsigned
,largeint_signed
,numeric_s_4_0
,numeric_s_4_2
,numeric_s_9_2
,numeric_u_9_9
,numeric_s_18_9
,numeric_s_18_18
,real_
,double_precision
,decimal_s_3_1
,decimal_u_1_0
,decimal_s_18_2
from ahtab1 
union
select
decimal_s_3_1
,decimal_u_1_0
,decimal_s_18_2
,smallint_signed
,smallint_unsigned
,integer_signed
,integer_unsigned
,largeint_signed
,numeric_s_4_0
,numeric_s_4_2
,numeric_s_9_2
,numeric_u_9_9
,numeric_s_18_9
,numeric_s_18_18
,real_
,double_precision
from ahtab2 
)
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create view ahv15 
(smallint_signed
,smallint_unsigned
,integer_signed
,integer_unsigned
,largeint_signed
,numeric_s_4_0
,numeric_s_4_2
,numeric_s_9_2
,numeric_u_9_9
,numeric_s_18_9
,numeric_s_18_18
,real_
,double_precision
,decimal_s_3_1
,decimal_u_1_0
,decimal_s_18_2)
as (
select
smallint_signed
,smallint_unsigned
,integer_signed
,integer_unsigned
,largeint_signed
,numeric_s_4_0
,numeric_s_4_2
,numeric_s_9_2
,numeric_u_9_9
,numeric_s_18_9
,numeric_s_18_18
,real_
,double_precision
,decimal_s_3_1
,decimal_u_1_0
,decimal_s_18_2
from ahtab1 
union
select
decimal_u_1_0
,decimal_s_18_2
,smallint_signed
,smallint_unsigned
,integer_signed
,integer_unsigned
,largeint_signed
,numeric_s_4_0
,numeric_s_4_2
,numeric_s_9_2
,numeric_u_9_9
,numeric_s_18_9
,numeric_s_18_18
,real_
,double_precision
,decimal_s_3_1
from ahtab2 
)
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create view ahv16 
(smallint_signed
,smallint_unsigned
,integer_signed
,integer_unsigned
,largeint_signed
,numeric_s_4_0
,numeric_s_4_2
,numeric_s_9_2
,numeric_u_9_9
,numeric_s_18_9
,numeric_s_18_18
,real_
,double_precision
,decimal_s_3_1
,decimal_u_1_0
,decimal_s_18_2)
as (
select
smallint_signed
,smallint_unsigned
,integer_signed
,integer_unsigned
,largeint_signed
,numeric_s_4_0
,numeric_s_4_2
,numeric_s_9_2
,numeric_u_9_9
,numeric_s_18_9
,numeric_s_18_18
,real_
,double_precision
,decimal_s_3_1
,decimal_u_1_0
,decimal_s_18_2
from ahtab1 
union
select
decimal_s_18_2
,smallint_signed
,smallint_unsigned
,integer_signed
,integer_unsigned
,largeint_signed
,numeric_s_4_0
,numeric_s_4_2
,numeric_s_9_2
,numeric_u_9_9
,numeric_s_18_9
,numeric_s_18_18
,real_
,double_precision
,decimal_s_3_1
,decimal_u_1_0
from ahtab2 
);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into ahtab1 
values ('AAAA'                -- column 0   char (4)
, -32768                -- column 1   smallint signed
, 0                     -- column 2   smallint unsigned
, -2147483648           -- column 3   integer signed
, 0                     -- column 4   integer unsigned
, -9223372036000000000  -- column 5   largeint signed
, -9999                 -- column 6   numeric (4,0) signed
, -99.99                -- column 7   numeric (4,2) signed
, -9999999.99           -- column 8   numeric (9,2) signed
, 0                     -- column 9   numeric (9,9) unsigned
, -999999999.999999999  -- column 10  numeric (18,9) signed
, -.999999999999999999  -- column 11  numeric (18,18) signed
--      , -1.15792e+77          -- column 12  real
, -3.40282346e+38       -- column 12  real
, -1.15792e+77          -- column 13  double precision
, -99.9                 -- column 14  decimal (3,1) signed
, 0                     -- column 15  decimal (1,0) unsigned
, -9999999999999999.99  -- column 16  decimal (18,2) signed
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into ahtab1 
values ('BBBB'                -- column 0   char (4)
, -1                    -- column 1   smallint signed
, +1                    -- column 2   smallint unsigned
, -1                    -- column 3   integer signed
, +1                    -- column 4   integer unsigned
, -1                    -- column 5   largeint signed
, -1                    -- column 6   numeric (4,0) signed
, -1.23                 -- column 7   numeric (4,2) signed
, -1.23                 -- column 8   numeric (9,2) signed
, .123456789            -- column 9   numeric (9,9) unsigned
, -1.234567898          -- column 10  numeric (18,9) signed
, -.123456789876543212  -- column 11  numeric (18,18) signed
--      , -1e-76                -- column 12  real
, -2e-38                -- column 12  real
--      , -1e-76                -- column 13  double precision
, -3e-308               -- column 13  double precision
, -1.2                  -- column 14  decimal (3,1) signed
, +1                    -- column 15  decimal (1,0) unsigned
, -1.23                 -- column 16  decimal (18,2) signed
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into ahtab1 
values ('CCCC'                -- column 0   char (4)
, 0                     -- column 1   smallint signed
, +32767                -- column 2   smallint unsigned
, -0                    -- column 3   integer signed
, +2147483647           -- column 4   integer unsigned
, 0                     -- column 5   largeint signed
, 0                     -- column 6   numeric (4,0) signed
, 0                     -- column 7   numeric (4,2) signed
, 0                     -- column 8   numeric (9,2) signed
, .555555555            -- column 9   numeric (9,9) unsigned
, 0                     -- column 10  numeric (18,9) signed
, 0                     -- column 11  numeric (18,18) signed
, 0                     -- column 12  real
, 0                     -- column 13  double precision
, 0                     -- column 14  decimal (3,1) signed
, 5                     -- column 15  decimal (1,0) unsigned
, 0                     -- column 16  decimal (18,2) signed
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into ahtab1 
values ('DDDD'                -- column 0   char (4)
, +1                    -- column 1   smallint signed
, +32768                -- column 2   smallint unsigned
, +1                    -- column 3   integer signed
, +2147483648           -- column 4   integer unsigned
, +1                    -- column 5   largeint signed
, +1                    -- column 6   numeric (4,0) signed
, +1.23                 -- column 7   numeric (4,2) signed
, +1.23                 -- column 8   numeric (9,2) signed
, .888888888            -- column 9   numeric (9,9) unsigned
, +1.234567898          -- column 10  numeric (18,9) signed
, +.123456789876543212  -- column 11  numeric (18,18) signed
--      , +1e-76                -- column 12  real
, +2e-38                -- column 12  real
--      , +1e-76                -- column 13  double precision
, +3e-308               -- column 13  double precision
, +1.2                  -- column 14  decimal (3,1) signed
, +8                    -- column 15  decimal (1,0) unsigned
, +1.23                 -- column 16  decimal (18,2) signed
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    #  this row contains the highest value for each data type.
    stmt = """insert into ahtab1 
values ('EEEE'                -- column 0   char (4)
, +32767                -- column 1   smallint signed
, +65535                -- column 2   smallint unsigned
, +2147483647           -- column 3   integer signed
, +4294967295           -- column 4   integer unsigned
, +9223372036000000000  -- column 5   largeint signed
, +9999                 -- column 6   numeric (4,0) signed
, +99.99                -- column 7   numeric (4,2) signed
, +9999999.99           -- column 8   numeric (9,2) signed
, +.999999999           -- column 9   numeric (9,9) unsigned
, +999999999.999999999  -- column 10  numeric (18,9) signed
, +.999999999999999999  -- column 11  numeric (18,18) signed
--      , +1.15792e+77          -- column 12  real
, +3.40282346e+38       -- column 12  real
--      , +1.15792e+77          -- column 13  double precision
, +1.7976931348623157e+308            -- column 13  double precision
, +99.9                 -- column 14  decimal (3,1) signed
, 9                     -- column 15  decimal (1,0) unsigned
, +9999999999999999.99  -- column 16  decimal (18,2) signed
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # this row contains null values.
    stmt = """insert into ahtab1 
values ('FFFF'                -- column 0   char (4)
, null                  -- column 1   smallint signed
, null                  -- column 2   smallint unsigned
, null                  -- column 3   integer signed
, null                  -- column 4   integer unsigned
, null                  -- column 5   largeint signed
, null                  -- column 6   numeric (4,0) signed
, null                  -- column 7   numeric (4,2) signed
, null                  -- column 8   numeric (9,2) signed
, null                  -- column 9   numeric (9,9) unsigned
, null                  -- column 10  numeric (18,9) signed
, null                  -- column 11  numeric (18,18) signed
, null                  -- column 12  real
, null                  -- column 13  double precision
, null                  -- column 14  decimal (3,1) signed
, null                  -- column 15  decimal (1,0) unsigned
, null                  -- column 16  decimal (18,2) signed
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    #  This shows some wrong values.
    #   Hence putting this statement in testA30.
    stmt = """select * from ahtab1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s2')
    
    stmt = """select smallint_signed from ahtab1 
union
select smallint_signed from ahtab2 
order by smallint_signed
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s3')
    
    stmt = """select smallint_signed from ahtab1 
union
select smallint_unsigned from ahtab2 
order by smallint_signed
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s4')
    
    stmt = """select smallint_signed from ahtab1 
union
select integer_signed from ahtab2 
order by smallint_signed
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s5')
    
    stmt = """select smallint_signed from ahtab1 
union
select integer_unsigned from ahtab2 
order by smallint_signed
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s6')
    
    stmt = """select smallint_signed from ahtab1 
union
select largeint_signed from ahtab2 
order by smallint_signed
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s7')
    
    stmt = """select smallint_unsigned from ahtab1 
union
select smallint_signed from ahtab2 
order by smallint_unsigned
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s8')
    
    stmt = """select smallint_unsigned from ahtab1 
union
select smallint_unsigned from ahtab2 
order by smallint_unsigned
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s9')
    
    stmt = """select smallint_unsigned from ahtab1 
union
select integer_signed from ahtab2 
order by smallint_unsigned
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s10')
    
    stmt = """select smallint_unsigned from ahtab1 
union
select integer_unsigned from ahtab2 
order by smallint_unsigned
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s11')
    
    stmt = """select smallint_unsigned from ahtab1 
union
select largeint_signed from ahtab2 
order by smallint_unsigned
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s12')
    
    stmt = """select integer_signed from ahtab1 
union
select smallint_signed from ahtab2 
order by integer_signed
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s13')
    
    stmt = """select integer_signed from ahtab1 
union
select smallint_unsigned from ahtab2 
order by integer_signed
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s14')
    
    stmt = """select integer_signed from ahtab1 
union
select integer_signed from ahtab2 
order by integer_signed
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s15')
    
    stmt = """select integer_signed from ahtab1 
union
select integer_unsigned from ahtab2 
order by integer_signed
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s16')
    
    stmt = """select integer_signed from ahtab1 
union
select largeint_signed from ahtab2 
order by integer_signed
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s17')
    
    stmt = """select integer_unsigned from ahtab1 
union
select smallint_signed from ahtab2 
order by integer_unsigned
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s18')
    
    stmt = """select integer_unsigned from ahtab1 
union
select smallint_unsigned from ahtab2 
order by integer_unsigned
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s19')
    
    stmt = """select integer_unsigned from ahtab1 
union
select integer_signed from ahtab2 
order by integer_unsigned
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s20')
    
    stmt = """select integer_unsigned from ahtab1 
union
select integer_unsigned from ahtab2 
order by integer_unsigned
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s21')
    
    stmt = """select integer_unsigned from ahtab1 
union
select largeint_signed from ahtab2 
order by integer_unsigned
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s22')
    
    stmt = """select largeint_signed from ahtab1 
union
select smallint_signed from ahtab2 
order by largeint_signed
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s23')
    
    stmt = """select largeint_signed from ahtab1 
union
select smallint_unsigned from ahtab2 
order by largeint_signed
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s24')
    
    stmt = """select largeint_signed from ahtab1 
union
select integer_signed from ahtab2 
order by largeint_signed
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s25')
    
    stmt = """select largeint_signed from ahtab1 
union
select integer_unsigned from ahtab2 
order by largeint_signed
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s26')
    
    stmt = """select largeint_signed from ahtab1 
union
select largeint_signed from ahtab2 
order by largeint_signed
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s27')
    
    #  The test that follows is a two-way UNION from ahtab1 and ahtab2.
    
    stmt = """select
smallint_signed
,smallint_unsigned
,integer_signed
,integer_unsigned
,largeint_signed
,numeric_s_4_0
,numeric_s_4_2
,numeric_s_9_2
,numeric_u_9_9
,numeric_s_18_9
,numeric_s_18_18
,real_
,double_precision
,decimal_s_3_1
,decimal_u_1_0
,decimal_s_18_2
from ahtab1 
union
select
smallint_signed
,smallint_unsigned
,integer_signed
,integer_unsigned
,largeint_signed
,numeric_s_4_0
,numeric_s_4_2
,numeric_s_9_2
,numeric_u_9_9
,numeric_s_18_9
,numeric_s_18_18
,real_
,double_precision
,decimal_s_3_1
,decimal_u_1_0
,decimal_s_18_2
from ahtab2 
order by
1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s28')
    
    _testmgr.testcase_end(desc)

def test016(desc="""a18"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0148 : A18
    #  Description:        This test verifies the SQL UNION
    #                      statement
    #                      UNION ALL of SELECT DISTINCTs with different
    #                      sized columns
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    stmt = """select distinct small_int from """ + gvars.g_schema_arkcasedb + """.btsel01 
union all
select medium_int from """ + gvars.g_schema_arkcasedb + """.btsel01 
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a18exp""", 'a18s0')
    
    stmt = """select large_int from """ + gvars.g_schema_arkcasedb + """.btsel01 
union all
select distinct medium_int from """ + gvars.g_schema_arkcasedb + """.btsel01 
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a18exp""", 'a18s1')
    
    stmt = """select distinct pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel01 
union all
select pic_x_7 from """ + gvars.g_schema_arkcasedb + """.btsel01 
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a18exp""", 'a18s2')
    
    stmt = """select distinct decimal_1 from """ + gvars.g_schema_arkcasedb + """.btsel01 
union all
select pic_decimal_3 from """ + gvars.g_schema_arkcasedb + """.btsel01 
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a18exp""", 'a18s3')
    
    _testmgr.testcase_end(desc)

def test017(desc="""a19"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0148 : A19
    #  Description:        This test verifies the SQL UNION
    #                      statement
    #                      SELECT WITH UNION
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    stmt = """create table a1 
(col1 pic 999 NOT NULL,
primary key (col1));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table a2 
(col1 pic 999 NOT NULL,
primary key (col1));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table a3 
(col1 pic 999 NOT NULL,
primary key (col1));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into a1 (*) values (1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a2 (*) values (1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a3 (*) values (1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a1 (*) values (2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select col1 from  a1 where col1 not in
( select col1 from  a2 union
select col1 from  a3 
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a19exp""", 'a19s0')
    
    #     update histogram statistics for table  a1;
    #     update histogram statistics for table  a2;
    #     update histogram statistics for table  a3;
    
    stmt = """select col1 from  a1 where col1 not in
( select col1 from  a2 union
select col1 from  a3 
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a19exp""", 'a19s1')
    
    stmt = """drop table a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table a2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table a3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test018(desc="""a20"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0148 : A20
    #  Description:        This test verifies the SQL UNION
    #                      statement
    #                      Simple UNION SELECT from base tables.
    #  Includes:           Column names the same.
    #                      Columns of same-length either side of UNION.
    #                      Some nonunique data values.
    #                      No NULL values.
    #                      ALL
    #
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    stmt = """create table table1 
( col1 integer not null) no partition ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into table1 values(1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into table1 values(1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into table1 values(1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into table1 values(2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into table1 values(3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into table1 values(4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into table1 values(5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into table1 values(5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select col1 from table1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a20exp""", 'a20s0')
    
    stmt = """create table table2 
( col1 integer not null) no partition ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into table2 values(1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into table2 values(1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into table2 values(2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into table2 values(2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into table2 values(3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into table2 values(3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into table2 values(3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select col1 from table2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a20exp""", 'a20s1')
    
    stmt = """create table table3 
( col1 integer not null) no partition ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into table3 values(10);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into table3 values(11);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into table3 values(12);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into table3 values(13);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into table3 values(14);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into table3 values(15);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into table3 values(16);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into table3 values(17);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into table3 values(18);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into table3 values(19);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into table3 values(20);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into table3 values(21);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into table3 values(22);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into table3 values(23);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into table3 values(24);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into table3 values(25);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into table3 values(26);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into table3 values(27);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into table3 values(28);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into table3 values(29);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """update statistics for table table1 on every column;"""
    output = _dci.cmdexec(stmt)
    stmt = """update statistics for table table2 on every column;"""
    output = _dci.cmdexec(stmt)
    stmt = """update statistics for table table3 on every column;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select col1 from table3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a20exp""", 'a20s2')
    
    #  Using both Union and Union All
    
    stmt = """select col1 from table1 
union
select col1 from table2 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a20exp""", 'a20s3')
    
    stmt = """select col1 from table1 
union all
select col1 from table2 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a20exp""", 'a20s4')
    
    #  Using both Union and Union All with order by
    
    stmt = """select col1 from table1 
union
select col1 from table2 
order by col1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a20exp""", 'a20s5')
    
    stmt = """select col1 from table1 
union all
select col1 from table2 
order by col1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a20exp""", 'a20s6')
    #  A Union of table to itself.
    #  Result of following two queries should be same.
    
    stmt = """select col1 from table1 
union
select col1 from table1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a20exp""", 'a20s7')
    
    stmt = """select col1 from table1 
union
select col1 from table1 
order by col1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a20exp""", 'a20s8')
    
    stmt = """select distinct * from table1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a20exp""", 'a20s9')
    
    # Order of execution test
    # Order of execution is left to right.
    
    stmt = """prepare S1 from
select col1 from table1 
union
select col1 from table3 
union
select col1 from table2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """SELECT SEQ_NUM, OPERATOR, LEFT_CHILD_SEQ_NUM,
RIGHT_CHILD_SEQ_NUM, TNAME
FROM TABLE( EXPLAIN ( NULL, 'S1'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute S1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a20exp""", 'a20s11')
    
    stmt = """prepare S1 from
select col1 from table1 
union
select col1 from table2 
union
select col1 from table3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """SELECT SEQ_NUM, OPERATOR, LEFT_CHILD_SEQ_NUM,
RIGHT_CHILD_SEQ_NUM, TNAME
FROM TABLE( EXPLAIN ( NULL, 'S1'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute S1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a20exp""", 'a20s13')
    stmt = """prepare S1 from
select col1 from table1 
union all
select col1 from table2 
union
select col1 from table3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """SELECT SEQ_NUM, OPERATOR, LEFT_CHILD_SEQ_NUM,
RIGHT_CHILD_SEQ_NUM, TNAME
FROM TABLE( EXPLAIN ( NULL, 'S1'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute S1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a20exp""", 'a20s15')
    
    stmt = """prepare S1 from
select col1 from table1 
union all
select col1 from table2 
union all
select col1 from table3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """SELECT SEQ_NUM, OPERATOR, LEFT_CHILD_SEQ_NUM,
RIGHT_CHILD_SEQ_NUM, TNAME
FROM TABLE( EXPLAIN ( NULL, 'S1'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute S1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a20exp""", 'a20s17')
    # Order of execution test with order by
    # Order of execution is left to right.
    
    stmt = """prepare S1 from
select col1 from table1 
union
select col1 from table3 
union
select col1 from table2 
order by col1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """SELECT SEQ_NUM, OPERATOR, LEFT_CHILD_SEQ_NUM,
RIGHT_CHILD_SEQ_NUM, TNAME
FROM TABLE( EXPLAIN ( NULL, 'S1'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute S1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a20exp""", 'a20s19')
    
    stmt = """prepare S1 from
select col1 from table1 
union
select col1 from table2 
union
select col1 from table3 
order by col1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """SELECT SEQ_NUM, OPERATOR, LEFT_CHILD_SEQ_NUM,
RIGHT_CHILD_SEQ_NUM, TNAME
FROM TABLE( EXPLAIN ( NULL, 'S1'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute S1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a20exp""", 'a20s21')
    stmt = """prepare S1 from
select col1 from table1 
union all
select col1 from table2 
union
select col1 from table3 
order by col1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """SELECT SEQ_NUM, OPERATOR, LEFT_CHILD_SEQ_NUM,
RIGHT_CHILD_SEQ_NUM, TNAME
FROM TABLE( EXPLAIN ( NULL, 'S1'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute S1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a20exp""", 'a20s23')
    
    stmt = """prepare S1 from
select col1 from table1 
union all
select col1 from table2 
union all
select col1 from table3 
order by col1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """SELECT SEQ_NUM, OPERATOR, LEFT_CHILD_SEQ_NUM,
RIGHT_CHILD_SEQ_NUM, TNAME
FROM TABLE( EXPLAIN ( NULL, 'S1'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute S1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a20exp""", 'a20s25')
    
    stmt = """drop table table1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table table2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table table3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test019(desc="""a21.sav"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #   Test unit SQLT148, case n1.
    
    #    volume $FIRE.SQLT148d ;
    
    #   Syntax-related errors.
    
    #   UNION alone!
    stmt = """union ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #   UNION with missing right-hand query expression:
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.parts 
union
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #   UNION with missing left-hand query term:
    stmt = """union
select * from """ + gvars.g_schema_arkcasedb + """.parts 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #   Errors due to differences in number of columns.
    
    #   1 column in left-hand query term and 2 columns in right-hand query
    #   expression.
    stmt = """select partnum           from """ + gvars.g_schema_arkcasedb + """.parts 
union
select partnum, partname from """ + gvars.g_schema_arkcasedb + """.parts 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4066')
    
    #   1 column in left-hand query term and >=3 columns on right of
    #   UNION.
    stmt = """select partnum           from """ + gvars.g_schema_arkcasedb + """.parts 
union
select *                 from """ + gvars.g_schema_arkcasedb + """.parts 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4066')
    
    #   2 columns in left-hand query term and 1 column in right-hand query
    #   expression.
    stmt = """select partnum, partname from """ + gvars.g_schema_arkcasedb + """.parts 
union
select partnum           from """ + gvars.g_schema_arkcasedb + """.parts 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4066')
    
    #   >=3 columns in left-hand query term and 1 column on right of
    #   UNION.
    stmt = """select *                 from """ + gvars.g_schema_arkcasedb + """.parts 
union
select partnum           from """ + gvars.g_schema_arkcasedb + """.parts 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4066')
    
    #   Errors due to differences in column data types (which Jay calls
    #   different domains).
    
    #   Numeric (INTEGER) column UNION CHAR column:
    stmt = """select partnum           from """ + gvars.g_schema_arkcasedb + """.parts 
union
select partname          from """ + gvars.g_schema_arkcasedb + """.parts 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4055')
    
    #   VARCHAR column UNION DATETIME column:
    stmt = """select var_char_3        from """ + gvars.g_schema_arkcasedb + """.btre201 
union
select y_to_d            from """ + gvars.g_schema_arkcasedb + """.btre201 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4055')
    
    #   INTERVAL column UNION FLOAT column:
    stmt = """select iy_to_mo          from """ + gvars.g_schema_arkcasedb + """.btre201 
union
select float_basic       from """ + gvars.g_schema_arkcasedb + """.btre201 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4055')
    
    #   Errors due to naming or identifying columns.
    
    #   UNION with the same 2 columns (with different data type) on each
    #   side on UNION, and the column names are in different orders:
    stmt = """select partnum, partname from """ + gvars.g_schema_arkcasedb + """.parts 
union
select partname, partnum from """ + gvars.g_schema_arkcasedb + """.parts 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4055')
    
    #   ORDER BY on UNION names a column that does not exist:
    stmt = """select partnum, partname from """ + gvars.g_schema_arkcasedb + """.parts 
union
select partnum, partname from """ + gvars.g_schema_arkcasedb + """.parts 
order by absentcolumn
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4120')
    
    #   ORDER BY on UNION names a column from the right-hand query
    #   expression:
    stmt = """select partnum, partname from """ + gvars.g_schema_arkcasedb + """.parts 
union
select suppnum, suppname from """ + gvars.g_schema_arkcasedb + """.supplier 
order by suppnum
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4120')
    
    stmt = """select partnum, partname from """ + gvars.g_schema_arkcasedb + """.parts 
union
select suppnum, suppname from """ + gvars.g_schema_arkcasedb + """.supplier 
order by suppname
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4120')
    
    #   ORDER BY on UNION references a ordinal column too big (e.g. 3 or
    #   100 for a two-column UNION):
    stmt = """select partnum, partname from """ + gvars.g_schema_arkcasedb + """.parts 
union
select suppnum, suppname from """ + gvars.g_schema_arkcasedb + """.supplier 
order by 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4007')
    
    stmt = """select partnum, partname from """ + gvars.g_schema_arkcasedb + """.parts 
union
select suppnum, suppname from """ + gvars.g_schema_arkcasedb + """.supplier 
order by 100
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4007')
    
    #   ORDER BY on UNION references ordinal column 0:
    stmt = """select partnum, partname from """ + gvars.g_schema_arkcasedb + """.parts 
union
select suppnum, suppname from """ + gvars.g_schema_arkcasedb + """.supplier 
order by 0
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4007')
    
    #   ORDER BY on UNION references negative ordinal column -1:
    stmt = """select partnum, partname from """ + gvars.g_schema_arkcasedb + """.parts 
union
select suppnum, suppname from """ + gvars.g_schema_arkcasedb + """.supplier 
order by -1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #   ORDER BY in wrong position.
    
    #   ORDER BY, applied to 1st (left-hand) SELECT:
    stmt = """select partnum, partname from """ + gvars.g_schema_arkcasedb + """.parts 
order by 1
union
select suppnum, suppname from """ + gvars.g_schema_arkcasedb + """.supplier 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #   ORDER BY, applied to 1st (left-hand) SELECT with parentheses
    #   around that combination:
    stmt = """(select partnum, partname from """ + gvars.g_schema_arkcasedb + """.parts 
order by 1)
union
select suppnum, suppname from """ + gvars.g_schema_arkcasedb + """.supplier 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #   ORDER BY between UNION and 2nd (right-hand) SELECT:
    stmt = """select partnum, partname from """ + gvars.g_schema_arkcasedb + """.parts 
union
order by 1
select suppnum, suppname from """ + gvars.g_schema_arkcasedb + """.supplier 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    #   ORDER BY within parenthesized UNION:
    stmt = """( select b.partnum from """ + gvars.g_schema_arkcasedb + """.parts b
union
select c.partnum from """ + gvars.g_schema_arkcasedb + """.parts c
order by b.partnum
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """( select b.partnum from """ + gvars.g_schema_arkcasedb + """.parts b
order by b.partnum
union
select c.partnum from """ + gvars.g_schema_arkcasedb + """.parts c
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    #   ORDER BY within parenthesized UNION, followed by last ORDER BY:
    stmt = """select a.partnum from """ + gvars.g_schema_arkcasedb + """.parts a
union
( select b.partnum from """ + gvars.g_schema_arkcasedb + """.parts b
union
select c.partnum from """ + gvars.g_schema_arkcasedb + """.parts c
order by b.partnum
)
order by a.partnum
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    #   ORDER BY after parenthesized UNION, before last UNION:
    stmt = """( select a.partnum from """ + gvars.g_schema_arkcasedb + """.parts a
union
select b.partnum from """ + gvars.g_schema_arkcasedb + """.parts b
)
order by b.partnum
union
select c.partnum from """ + gvars.g_schema_arkcasedb + """.parts c
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    #   ORDER BY before parenthesized UNION:
    stmt = """select a.partnum from """ + gvars.g_schema_arkcasedb + """.parts a
order by a.partnum
union
( select b.partnum from """ + gvars.g_schema_arkcasedb + """.parts b
union
select c.partnum from """ + gvars.g_schema_arkcasedb + """.parts c
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #   ORDER BY before LOCKing option associated with 2nd (right-hand)
    #   SELECT:
    stmt = """select partnum, partname from """ + gvars.g_schema_arkcasedb + """.parts 
union
select suppnum, suppname from """ + gvars.g_schema_arkcasedb + """.supplier 
order by 1
read uncommitted access
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a21.savexp""", 'a21.savs3d')
    
    #   ORDER BY before other clauses associated with 2nd (right-hand)
    #   SELECT:
    stmt = """select partnum, partname from """ + gvars.g_schema_arkcasedb + """.parts 
union
select suppnum, suppname from """ + gvars.g_schema_arkcasedb + """.supplier 
where suppnum > 100
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a21.savexp""", 'a21.savs4')
    
    #   Some things cannot be done by a view containing a UNION.
    
    #   Create a view that has all cities and all states & countries where
    #   customers and suppliers are located (view & tables on first
    #   temporary subvolume):
    stmt = """create view n1view1 (c, s) as
select city, state from """ + gvars.g_schema_arkcasedb + """.customer 
union
select city, state from """ + gvars.g_schema_arkcasedb + """.supplier 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #   A view containing a UNION:
    stmt = """select c   , s     from n1view1 
union
select city, state from """ + gvars.g_schema_arkcasedb + """.supplier 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a21.savexp""", 'a21.savs5a')
    
    stmt = """select * from n1view1 
union
select city, state from """ + gvars.g_schema_arkcasedb + """.supplier 
order by 1,2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a21.savexp""", 'a21.savs6')
    
    #   A view containing a UNION
    #   Cannot have a grouping imposed on any column involved in the
    #   Union:
    stmt = """select * from n1view1 group by s ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4012')
    
    stmt = """select * from n1view1 order by c ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a21.savexp""", 'a21.savs8')
    
    #   A view containing a UNION
    #   Cannot apply aggregate function to any column involved in the
    #   Union:
    stmt = """select min (s) from n1view1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a21.savexp""", 'a21.savs9')
    
    #   Cleanup:
    stmt = """drop view n1view1 ;"""
    output = _dci.cmdexec(stmt)
    
    #   View with UNION and order by:
    stmt = """create view n1view2 (c, s) as
select city, state       from """ + gvars.g_schema_arkcasedb + """.customer 
union
select city, state       from """ + gvars.g_schema_arkcasedb + """.supplier 
order by city
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #   View should not be created:
    stmt = """select * from n1view2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a21.savexp""", 'a21.savs9b')
    #   Cleanup:
    stmt = """drop view n1view2 ;"""
    output = _dci.cmdexec(stmt)
    
    #   Protection view - 'FOR PROTECTION' clause rejected with UNION:
    stmt = """create view n1view3 (c, s) as
select city, state       from """ + gvars.g_schema_arkcasedb + """.customer 
union
select city, state       from """ + gvars.g_schema_arkcasedb + """.supplier 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #   View should not be created:
    stmt = """select * from n1view3 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a21.savexp""", 'a21.savs10a')
    #   Cleanup:
    stmt = """drop view n1view3 ;"""
    output = _dci.cmdexec(stmt)
    
    #   Protection view - 'FOR PROTECTION' clause rejected with UNION:
    stmt = """create view n1view3 (c, s) as
select city, state       from """ + gvars.g_schema_arkcasedb + """.customer 
union
select city, state       from """ + gvars.g_schema_arkcasedb + """.supplier 
order by city
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #   View should not be created:
    stmt = """select * from n1view3 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a21.savexp""", 'a21.savs11a')
    
    #   Cleanup:
    stmt = """drop view n1view3 ;"""
    output = _dci.cmdexec(stmt)
    
    #   MATCH - supported in ANSI spec.
    stmt = """select city, state       from """ + gvars.g_schema_arkcasedb + """.customer 
union
select city, state       from """ + gvars.g_schema_arkcasedb + """.supplier 
where city like 'S%'
;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test020(desc="""a22"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #  Test unit SQLT148, case n2.
    
    #    volume $SRC.SQLT148d ;
    
    # Create table n2tab1 and load with data.
    stmt = """create table n2tab1 
(dt_year_to_second   datetime year to second
,dt_year_to_day      datetime year to day
,dt_hour_to_second   datetime hour to second
,dt_fraction_4       datetime fraction (4)
,dt_fraction_6       datetime fraction
,interval_year_to_month interval year (4) to month
,interval_year_2     interval year (2)
,interval_year_4     interval year (4)
,interval_hour_3     interval hour (3)
) no partition
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into n2tab1 values
(datetime '1952-01-02:12:00:00' year to second  -- dt_year_to_second
,datetime '1992-02-29'          year to day     -- dt_year_to_day
,datetime '17:59:59'            hour to second  -- dt_hour_to_second
,datetime '1234'                fraction (4)    -- dt_fraction_4
,datetime '654321'              fraction (6)    -- dt_fraction_6
,interval '2-7'                 year to month   -- interval_year_to_month
,interval '65'                  year            -- interval_year_2
,interval '12'                  year            -- interval_year_4
,interval '99'                  hour            -- interval_hour_3
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4082')
    
    stmt = """insert into n2tab1 values
(datetime '2000-01-31:00:00:00' year to second  -- dt_year_to_second
,datetime '2000-01-31'          year to day     -- dt_year_to_day
,datetime '17:59:59'            hour to second  -- dt_hour_to_second
,datetime '1234'                fraction (4)    -- dt_fraction_4
,datetime '654321'              fraction (6)    -- dt_fraction_6
,interval '2-7'                 year to month   -- interval_year_to_month
,interval '02'                  year            -- interval_year_2
,interval '2000'                year (4)        -- interval_year_4
,interval '999'                 hour (3)        -- interval_hour_3
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4082')
    
    # Create shorthand views n2v1 and n2v2.
    stmt = """create view n2v1 as
select dt_year_to_second from n2tab1 
where dt_year_to_second = date '1991-10-04'
union
select dt_year_to_second from n2tab1 
where dt_year_to_second = datetime '1991-10-04:00:00:00' year to second
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create view n2v2 as
select dt_year_to_second from n2tab1 
where dt_year_to_second = date '1991-10-04'
union all
select dt_year_to_second from n2tab1 
where dt_year_to_second = datetime '1991-10-04:00:00:00' year to second
;"""
    output = _dci.cmdexec(stmt)
    
    # Datetime test using UNION without the ALL option.
    # A column (year to second) is compared to a literal (year to day).
    # In C30.07, this test fails producing error -8041.
    # After the fix this test correctly produces error -7011.
    stmt = """select dt_year_to_second from n2tab1 
where dt_year_to_second = date '1991-10-04'
union
select dt_year_to_second from n2tab1 
where dt_year_to_second = datetime '1991-10-04:00:00:00' year to second
;"""
    output = _dci.cmdexec(stmt)
    
    # Datetime test using UNION without the ALL option.
    # Same as the previous test except that 'datetime' is used instead
    # of 'date' in the literal.
    # In C30.07, this test fails producing error -8041.
    # After the fix this test correctly produces error -7011.
    stmt = """select dt_year_to_second from n2tab1 
where dt_year_to_second = datetime '1991-10-04' year to day
union
select dt_year_to_second from n2tab1 
where dt_year_to_second = datetime '1991-10-04:00:00:00' year to second
;"""
    output = _dci.cmdexec(stmt)
    
    # Datetime test using UNION with the ALL option.
    # A column (year to second) is compared to a literal (year to day).
    # In C30.07, this test correctly produces error -7011.
    stmt = """select dt_year_to_second from n2tab1 
where dt_year_to_second = date '1991-10-04'
union all
select dt_year_to_second from n2tab1 
where dt_year_to_second = datetime '1991-10-04:00:00:00' year to second
;"""
    output = _dci.cmdexec(stmt)
    
    # Datetime test using UNION without the ALL option.
    # A column (year to second) is compared to another column (year to day).
    # In C30.07, this test fails producing error -8041.
    # After the fix this test correctly produces error -7011.
    stmt = """select dt_year_to_second from n2tab1 
where dt_year_to_second = dt_year_to_day
union
select dt_year_to_second from n2tab1 
where dt_year_to_second = datetime '1991-10-04:00:00:00' year to second
;"""
    output = _dci.cmdexec(stmt)
    
    # Interval test using UNION without the ALL option.
    # Column (year to month) is compared to another column (year).
    # This is a positive test.
    stmt = """select dt_year_to_second from n2tab1 
where interval_year_to_month = interval_year_4
union
select dt_year_to_second from n2tab1 
where dt_year_to_second = datetime '1991-10-04:00:00:00' year to second
;"""
    output = _dci.cmdexec(stmt)
    
    # Datetime test using UNION without the ALL option.
    # The result of an arithmetic operation (year to second) is compared
    # to a column (year to day)
    # In C30.07, this test fails producing error -8041.
    # After the fix this test correctly produces error -7011.
    stmt = """select dt_year_to_second from n2tab1 
where dt_year_to_second + interval_year_2 = dt_year_to_day
union
select dt_year_to_second from n2tab1 
where dt_year_to_second = datetime '1991-10-04:00:00:00' year to second
;"""
    output = _dci.cmdexec(stmt)
    
    # Datetime test using UNION without the ALL option in a shorthand view.
    # A column (year to second) is compared to a literal (year to day).
    # In C30.07, this test fails producing error -8041.
    # After the fix this test correctly produces error -7011.
    stmt = """select * from n2v1;"""
    output = _dci.cmdexec(stmt)
    
    # Datetime test using UNION with the ALL option in a shorthand view.
    # A column (year to second) is compared to a literal (year to day).
    # In C30.07, this test correctly produces error -7011.
    stmt = """select * from n2v2;"""
    output = _dci.cmdexec(stmt)
    
    # Datetime test using UNION without the ALL option.
    # A column (year to second) is compared to a parameter (year to day).
    # In C30.07, this test fails producing error -8041.
    # After the fix this test correctly produces error -7011.
    stmt = """set param ?param1 '1992-02-10';"""
    output = _dci.cmdexec(stmt)
    stmt = """select dt_year_to_second from n2tab1 
where dt_year_to_second = date '1991-10-04'
union
select dt_year_to_second from n2tab1 
where dt_year_to_second = datetime '1991-10-04:00:00:00' year to second
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4082')
    
    #  Datetime test using UNION without the ALL option.
    #  A column (year to second) is compared to the result of the EXTEND
    #  function (year to hour).
    #  In C30.07, this test fails producing error -8041.
    #  After the fix this test correctly produces error -7011.
    stmt = """select dt_year_to_second from n2tab1 
where dt_year_to_second = extend (dt_year_to_day, year to hour)
union
select dt_year_to_second from n2tab1 
where dt_year_to_second = datetime '1991-10-04:00:00:00' year to second
;"""
    output = _dci.cmdexec(stmt)
    
    #  Datetime test using UNION without the ALL option.
    #  A column (year to second) is compared to the result of the EXTEND
    #  function (year to second).
    #  This is a positive test.
    stmt = """select dt_year_to_second from n2tab1 
where dt_year_to_second = extend (dt_year_to_day, year to second)
union
select dt_year_to_second from n2tab1 
where dt_year_to_second = datetime '1991-10-04:00:00:00' year to second
;"""
    output = _dci.cmdexec(stmt)
    
    # Datetime test using UNION without the ALL option in a subquery.
    # A column (year to second) is compared to another column (year to day).
    # In C30.07, this test fails producing error -8041.
    # After the fix this test correctly produces error -7011.
    stmt = """select dt_year_to_second from n2tab1 
where dt_year_to_second =
(select dt_year_to_second from n2tab1 
where dt_year_to_second = dt_year_to_day
union
select dt_year_to_second from n2tab1 
where dt_year_to_second = datetime '1991-10-04:00:00:00' year to second)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    #  Cleanup:
    stmt = """drop table n2tab1;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

