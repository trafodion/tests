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
    #  Test case name:     T1102:A01
    #  Description:        This test verifies SQL subquery and
    #                      equality transformations
    #                      via SELECT.
    #
    # =================== End Test Case Header  ===================
    #
    #  ---------------------------
    #  Check tables.
    #  ---------------------------
    stmt = """select * from TTF ORDER BY 1, 2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s0')
    stmt = """select * from TTFONE ORDER BY 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s1')
    #
    #  ---------------------------
    #  Subquery transformations: SELECT list.
    #  ---------------------------
    #
    #  ---------------------------
    #  Note: a <select list> element is a <derived column>.  Therefore,
    #        a subquery in a select list must be a scalar subquery
    #        not a row subquery, e.g. expect error on (see negative tests):
    #
    #  ---------------------------
    #       Id: TF.001       Simple select with subqueries in select list.
    #  ---------------------------
    #  Expect {(2.0, 'c', 1), 3*(2.0, 'cc', 1), (2.0, ?, 1)}
    stmt = """select ( select nnum5 from TTF where nint = 3 )
, vch5
, ( select nsint from TTF where nint = 3 )
from TTF t1
ORDER BY 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s2')
    #
    #  Expect {5* ('abcdefg')}
    stmt = """select (select ( select  vch7 from TTF where nint = 3 )
from TTF where nint = 3 )
from TTF t1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s3')
    #
    #  Note that one row is returned from the subquery.
    #  Expect {('abcdefg')}
    stmt = """select ( select  vch7 from TTF where nint = 3 )
from TTF where nint = 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s4')
    #
    #  Expect {(1)}
    stmt = """select distinct ( select distinct (select nint from TTF where vch5 is null )
from TTF )
from TTF t1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s5')
    #
    #  Expect 4 rows, first column varies: ((a) (abcdefg) (b) (cc));
    #  other columns are constants:
    #        (abcdefg , 1 , cc , 0.09 , alph , 2.0 , cc , 1)
    #
    stmt = """select distinct vch7
, ( select  vch7 from TTF where nint = 3 ) As c3vch7
, ( select distinct
(select nint from TTF where vch5 is null )
from TTF ) as Nnint
, ( select ch3   from TTF where nint = 3 ) as c3ch3
, ( select cast(nnum9 as pic 9V99)
from TTF where nint = 3 ) as c3nnum9
, ( select ch4   from TTF where nint = 3 ) as c3ch4
, ( select nnum5 from TTF where nint = 3 ) as c3nnum5
, ( select vch5  from TTF where nint = 3 ) as c3vch5
, ( select nsint from TTF where nint = 3 ) as c3nsint
from TTF t1
ORDER BY 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s6')
    #
    #  Single level of subquery works.
    #  Expect 1 row: {(2)}.
    stmt = """select (select nint from TTFONE) from TTFONE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s7')
    #
    #  Expect 1 row: {(2)}.
    stmt = """select (select (select nint from TTFONE) from TTFONE )
from TTFONE ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s8')
    #
    #  Expect 1 row: { (1) }.
    stmt = """select distinct (select nint from TTF where vch5 is null )
from TTF;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s9')
    #
    #  Expect 1 row: { (1) }.
    stmt = """select distinct
(select distinct
(select nint from TTF where vch5 is null )
from TTF )
from TTF;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s10')
    #
    #  ---------------------------
    #       Id: TF.002       Simple select: subqueries in WHERE pred and select list
    #       Id: TF.011       Subqueries use correlated column in simple select list
    #  ---------------------------
    #  Expect 5 rows ((2.0) , (2.0) , (2.0) , (1234.5) , (?))
    stmt = """select t2.nnum5 from TTF t2
ORDER BY 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s11')
    #  Expect 1 row ((1234.5) (4)) -- count(x) excludes NULL values.
    stmt = """select max(t2.nnum5), count(t2.nnum5) from TTF t2
ORDER BY 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s12')
    #  Expect 5 rows ((1) , (2) , (3) , (4) , (5))
    stmt = """select  t1.nint
from TTF t1
where ( select max(t2.nnum5) from TTF t2) > 1
ORDER BY 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s13')
    #
    #  Expect 1 row.
    stmt = """select * from TTFONE t2 where t2.nint = 2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s14')
    #  Expect 4 rows {(2) , (3) , (4) , (5))
    stmt = """select  t1.nint
from TTF t1
where ( select t1.nnum5 from TTFONE t2 where t2.nint = 2 ) > 1
ORDER BY 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s15')
    #  Expect 1 row {(2))
    stmt = """select  t1.nint
from TTF t1
where ( select t1.nnum5 from TTFONE t2 where t1.nint = 2 ) > 1
ORDER BY 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s16')
    #
    #  ---------------------------
    #  ANSI 7.6 SR 3:
    #  ---------------------------
    #   The colref (t1.nnum5) contained in the subquery in the where clause
    #   references a column of "T" (= TTF t1), yet it is specified in
    #   an aggregate function (max()), violating SR3.
    #
    #   Not very intuitive!  But it's the law!  So the following would
    #   give SQL: Aggregate functions placed incorrectly:
    #     select  t1.nint
    #       from TTF t1
    #       where ( select count(t1.nnum5) from TTF t2 where t2.nint = 2 ) > 1
    #      ;
    #  ---------------------------
    #
    #  Expect 5 rows (true predicate)
    #     { (1.09) (1.09) (1.90) (3.00) (1234568.89) }
    #
    stmt = """select  (select min(t1.nint) from TTF t1) + nnum9
from TTF t2
where 2 * ( select max(t3.nnum5) from TTF t3 )
< ( ( select max(t4.nsint) from TTF t4 ) )
ORDER BY 1
;"""
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
    #  Test case name:     T1102:A02
    #  Description:        This test verifies the SQL transformations
    #                      for deeply nested subqueries, via SELECT.
    #
    # =================== End Test Case Header  ===================
    #
    
    #
    # Make sure that each transaction commits.
    stmt = """set transaction autocommit on;"""
    output = _dci.cmdexec(stmt)
    #
    #  ---------------------------
    #  Check tables.
    #  ---------------------------
    stmt = """select * from TTF  ORDER BY 1,2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s0')
    stmt = """select * from TTF1 ORDER BY 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s1')
    #
    #  ---------------------------
    #  Subqueries nested deeply:
    #  ---------------------------
    #
    #  ---------------------------
    #       Id: TF.021       5 deep in select list of Derived Table; uncorrelated columns.
    #       Id: TF.041       Subqueries in <select list> within Derived Table.
    #  ---------------------------
    #
    #  5 deep.
    #  Must have ONE value in subquery -- use table with one row.
    #  Expect (('cc'))
    stmt = """select a from (select (select (select (select (select
( select  vch5
from TTF1 t5) from TTF1 t4) from TTF1 t3) from TTF1 t2)
from TTF1 t1) from TTF1 t0
) dt ( a )
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s2')
    #
    #  ---------------------------
    #       Id: TF.023       10 deep in select list of Derived Table; uncorrelated columns.
    #  ---------------------------
    #
    #  10 deep.
    #  Expect ({5})
    stmt = """select a from ( select
( select
( select (select (select  ( select
( select (select (select (select
( select  max(nint) from TTF t10)
from TTF1 t9) from TTF1 t8) from TTF1 t7) from TTF1 t6)
from TTF1 t5) from TTF1 t4) from TTF1 t3) from TTF1 t2)
from TTF1 t1) from TTF1 t0
) dt ( a )
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s3')
    #
    #  20 deep.
    #  Expect ({3})
    stmt = """select * from (select (select (select (select
(select
(select (select (select
(select (select (select
(select (select (select
(select (select (select
(select (select (select
( select cast(avg(t20.nint) as numeric (9,2))
from TTF t20)
from TTF1 t19) from TTF1 t18) from TTF1 t17)
from TTF1 t16) from TTF1 t15) from TTF1 t14)
from TTF1 t13) from TTF1 t12) from TTF1 t11)
from TTF1 t10) from TTF1 t9) from TTF1 t8)
from TTF1 t7) from TTF1 t6) from TTF1 t5)
from TTF1 t4) from TTF1 t3) from TTF1 t2)
from TTF1 t1) from TTF1 t0
) dt ( a )
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s4')
    #
    #  ---------------------------
    #       Id: TF.024       10 deep in select list of Derived Table; correlated columns.
    #       Id: TF.012       Subqueries use correlated column in select list of DT.
    #  ---------------------------
    #  10 deep.
    #  Small query to look for correlation name
    #  Expect {(3}).
    stmt = """select * from ( select
( select  t4.nint from TTF1 t10)  from TTF1 t4
) dt
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s5')
    #
    #  Expect {(1), (2), (3), (4), (5})
    stmt = """select * from ( select
( select
( select (select (select (select
--  nint is unknown to other tables.
( select  t4.nint from TTF1 t10)
from TTF1 t9) from TTF1 t8) from TTF1 t7)
from TTF1 t6) from TTF1 t5)
from TTF  t4
) dt
ORDER BY 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s6')
    #
    #  ---------------------------
    #       Id: TF.025       20 deep in WHERE predicate of Derived Table; uncorrelated columns
    #       Id: TF.026       20 deep in WHERE predicate of Derived Table; correlated columns
    #       Id: TF.013       Subqueries use correlated column in WHERE clause.
    #       Id: TF.042       Subqueries in <where pred> within Derived Table.
    #  ---------------------------
    #
    #  2 deep.
    #  Expect {('abcdefg'}).
    stmt = """select vch7 from TTF1 
where ( select (select count(nint)from TTF1) from TTF1)
>= ( select count(nint) from TTF1) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s7')
    #  Expect {(1}).
    stmt = """select (select count(t1.nint)
from TTF1 t1)
from TTF1 t
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s8')
    #  Expect {(1}).
    stmt = """select (select count(t.nint)
from TTF1 t1)
from TTF1 t
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s9')
    #
    #  Expect the one row from TTF1.
    stmt = """select * from ( select vch7, vch5, nint from TTF1 
where
( select ( select ( select ( select ( select
( select ( select ( select ( select ( select
( select ( select ( select ( select ( select
( select ( select ( select ( select ( select
( select  count(t2.nint) from TTF1 t20 )
from TTF1 t19) from TTF1 t18)
from TTF1 t17) from TTF1 t16)
from TTF1 t15) from TTF1 t14)
from TTF1 t13) from TTF1 t12)
from TTF1 t11) from TTF1 t10)
from TTF1 t9) from TTF1 t8)
from TTF1 t7) from TTF1 t6)
from TTF1 t5) from TTF1 t4)
from TTF1 t3) from TTF1 t2)
from TTF1 t1) from TTF1 t0)
>= 1
) dt ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s10')
    #
    #  Expect {(1}).
    stmt = """select ( select ( select ( select
( select  count(t2.nint) from TTF1 t20 ) -- file NormRelExpr.C, line 2018
from TTF1 t3) from TTF1 t2)
from TTF1 t1) from TTF1 t0
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s11')
    #
    #  Expect the one row from TTF1.
    stmt = """select * from ( select vch7, vch5, nint from TTF1 
where
( select ( select ( select ( select
( select  count(t2.nint) from TTF1 t20 ) -- file NormRelExpr.C, line 2018
from TTF1 t3) from TTF1 t2)
from TTF1 t1) from TTF1 t0)
>= 1
) dt ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s12')
    #
    #  Expect {('abcdefg' , 'cc' , 3}).
    stmt = """select * from ( select vch7, vch5, nint from TTF1 
where
9999
>=
( select ( select ( select ( select ( select
( select ( select ( select ( select ( select
( select ( select ( select ( select ( select
( select ( select ( select ( select ( select
( select  count(nint) from TTF t20 )
from TTF1 t19) from TTF1 t18)
from TTF1 t17) from TTF1 t16) -1
from TTF1 t15) from TTF1 t14)
from TTF1 t13) from TTF1 t12)
from TTF1 t11) from TTF1 t10)
from TTF1 t9) from TTF1 t8)
from TTF1 t7) from TTF1 t6)
from TTF1 t5) from TTF1 t4)
from TTF1 t3) from TTF1 t2)
from TTF1 t1) from TTF1 t0)
) dt ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s13')
    #
    #  Expect {('abcdefg' , 'cc' , 3}).
    stmt = """select * from ( select vch7, vch5, nint from TTF1 
where
( select ( select ( select ( select
( select ( select ( select ( select max(nnum5) +
( select ( select ( select ( select
( select ( select ( select ( select
( select ( select ( select ( select
( select  count(nint) from TTF1 t20 )
from TTF1 t19) from TTF1 t18)
from TTF1 t17) from TTF1 t16)
from TTF1 t15) from TTF1 t14)
from TTF1 t13) from TTF1 t12)
from TTF1 t11) from TTF1 t10)
from TTF1 t9 ) from TTF1 t8 )
from TTF1 t7 ) from TTF1 t6 )
from TTF1 t5 ) from TTF1 t4 )
from TTF1 t3 ) from TTF1 t2 )
from TTF1 t1 ) from TTF1 t0 )
>=
( select ( select ( select ( select ( select
( select ( select ( select ( select ( select
( select ( select ( select ( select ( select
( select ( select ( select ( select ( select
( select  count(nint) from TTF1 )
from TTF1 t19) from TTF1 t18)
from TTF1 t17) from TTF1 t16) -1
from TTF1 t15) from TTF1 t14)
from TTF1 t13) from TTF1 t12)
from TTF1 t11) from TTF1 t10)
from TTF1 t9) from TTF1 t8)
from TTF1 t7) from TTF1 t6)
from TTF1 t5) from TTF1 t4)
from TTF1 t3) from TTF1 t2)
from TTF1 t1) from TTF1 t0)
) dt ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s14')
    
    _testmgr.testcase_end(desc)

def test003(desc="""a03"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     T1102:A03
    #  Description:        This tests SQL subquery transformations
    #                      for subqueries beneath OR's.
    #
    # =================== End Test Case Header  ===================
    #
    
    #
    stmt = """select * from TTF  order by 1, 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s0')
    stmt = """select * from TTF2 order by 1, 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s1')
    #
    #  ---------------------------
    #  Subquery transformations: Subqueries beneath OR.
    #  ---------------------------
    #
    #  Expect ((2.0))
    stmt = """select min(t2.nnum5) from TTF t2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s2')
    #  Expect ((1))
    stmt = """select min(t3.nint) from TTF t3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s3')
    #
    #  ---------------------------
    #       Id: TF.101       Below OR, subquery has arithmetic expression.
    #       Id: TF.105       Below OR, subquery has Literals
    #       Id: TF.106a      Logical comparison within predicates of subqueries;
    #                           compare with negative and positive values.
    #       Id: TF.106b      Logical comparison of subquery result with value;
    #                           compare with negative and positive values.
    #       Id: TF.131       Aggregate on uncorrelated columns
    #  ---------------------------
    #
    #  Negative constants, positive aggregates.
    #  Expect all 5 rows as in base table TTF.
    stmt = """select vch7, nint, ch3, nnum5
from TTF t1
where
( ( select min(t2.nnum5) from TTF t2 ) < -99 )
OR
( 1 > ( (select min(t3.nint) from TTF t3) - 7) )
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s4')
    #
    #  Expect all 5 rows as in base table TTF.
    stmt = """select vch7, nint, ch3, nnum5
from TTF t1
where
(select -min(t2.nnum5) from TTF t2 where -t2.nnum5 < -7
) = -1234.5
OR
(select min(-t3.nint) from TTF t3 where -3 > -t3.nint
) = -5
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s5')
    #
    #  Negative aggregates and constants.
    #  Expect all 5 rows as in base table TTF.
    stmt = """select vch7, nint, ch3, nnum5
from TTF t1
where ((select min(-t2.nnum5) from TTF t2) < -99 )
OR ( 1 > ( (select min(-t3.nint) from TTF t3) - 7) )
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s6')
    #
    #  Expect all 5 rows as in base table TTF.
    stmt = """select vch7, nint, ch3, nnum5
from TTF t1
where ((select -min(t2.nnum5) from TTF t2) < -99 )
OR ( 1 > ( (select -min(t3.nint) from TTF t3) - 7) )
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s7')
    #
    #  Positive numbers in aggregates and constants.
    #  Expect all 5 rows as in base table TTF.
    stmt = """select vch7, nint, ch3, nnum5
from TTF t1
where ((select min(t2.nnum5) from TTF t2) < 99)
OR ( 1 > ( (select min(t3.nint) from TTF t3) + 7) )
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s8')
    #
    #  Positive constants, negative aggregates.
    #  Expect all 5 rows as in base table TTF.
    stmt = """select vch7, nint, ch3, nnum5
from TTF t1
where
( ( select -min(t2.nnum5) from TTF t2 ) < 99
)
OR
( 1 >
( (select -min(-t3.nint) from TTF t3 ) + 7 )
)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s9')
    #
    #  Equal.
    #  Expect all 5 rows as in base table TTF.
    stmt = """select vch7, nint, ch3, nnum5
from TTF t1
where
( (select -min(t2.nnum5) from TTF t2) = -3 )
OR
( -2 =
( (select -min(t3.nint) from TTF t3) - 1 )
)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s10')
    #
    # ---------------------------
    #      Id: TF.102       Below OR, subquery has BETWEEN predicates
    #      Id: TF.103       Below OR, subquery has IN predicates
    #      Id: TF.108       Below OR, subquery has Negation (NOT)
    #      Id: TF.110       Below OR, subquery has Parameters
    # ---------------------------
    #
    stmt = """set param ?p 4;"""
    output = _dci.cmdexec(stmt)
    #
    #  Expect 5 rows ((4) (4) (4) (4) (4)).
    stmt = """select cast(?p as smallint) from TTF t1
where
( ( select max(t2.nnum5) from TTF t2 ) BETWEEN 5 and 19 )
OR
( (select max(t3.nint) from TTF t3 ) NOT IN (2,?p,6,8) )
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s11')
    #
    #  Expect 5 rows as in base table.
    #    select vch7, nint, ch3, nnum5, ?p
    stmt = """select *, ?p
from TTF t1
where
((select max(t2.nnum5) from TTF t2) BETWEEN 1 and 9)
OR
((select max(t3.nint)  from TTF t3) NOT IN (2,?p,6,8))
OR
((select max(t3.nint)  from TTF t3) NOT IN (2,4,6,8))
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s12')
    #
    #  ---------------------------
    #       Id: TF.104       Below OR, subquery has LIKE predicates
    #       Id: TF.109       Below OR, subquery has NULL-value predicate
    #  ---------------------------
    #
    stmt = """select distinct
vch7, ch3
from TTF t2
where t2.vch7 = 'b'
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s13')
    #
    #  Expect (('b' , 4 , 'c' , 1234.5 , 'e'))
    stmt = """select vch7, nint, ch3, nnum5, ch4
from TTF t1
where
( select distinct -- Must include DISTINCT to get unique row.
t1.ch3
from TTF t2
where t1.vch7 = 'b'
) LIKE '%c%'
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s14')
    stmt = """select vch7, nint, ch3, nnum5, ch4
from TTF t1
where
( select distinct -- Must include DISTINCT to get unique row.
t1.ch3
from TTF t2
where t1.vch7 = 'b'
) = 'c'
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s15')
    #
    #  Watch out in the following. The query with "IS NULL" subquery
    #  should return 5 rows and not 1 row.
    #  (1) The first value from t1 (ch4 = NULL), will
    #      return a NULL value from the subquery since the subquery
    #      is returning t1.ch4. So, "where <SubQ> is NULL" will be TRUE.
    #  (2) For the remaining 4 rows, the predicate "t1.ch4 is NULL" will
    #      be FALSE so the subquery will not return any rows and the
    #      result will be a NULL value. Which will make the where
    #      predicate "<SubQ> is NULL" TRUE and return those rows.
    #
    stmt = """select ch4  from TTF t3 where ch4 IS NULL ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s16')
    #
    #  For "is NULL" subquery, expect all 5 rows as in table TTF.
    stmt = """select vch7, nint, ch3, nnum9, ch4
from TTF t1
where
( select distinct t1.ch4 from TTF t3
where t1.ch4 IS NULL
) IS NULL
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s17')
    #
    #  For "is NULL" subquery, expect all 5 rows as in table TTF.
    stmt = """select vch7, nint, ch3, nnum5
from TTF t1
where
( ( select distinct -- Must include DISTINCT to get unique row.
t1.vch7
from TTF t2
where t1.vch7 = 'b'
) LIKE 'c'
)
OR
( ( select distinct t1.ch4 from TTF t3
where t1.ch4 IS NULL
) IS NULL
)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s18')
    #
    #  ---------------------------
    #       Id: TF.107       Below OR, subquery has Multi-valued predicates
    #  ---------------------------
    #
    #  Expect all 5 rows.
    stmt = """select vch7, nint, ch3, nnum5
from TTF t1
where ( (select max(t1.nnum5) from TTF t1)
, (select max(t1.vch7)  from TTF t1)
)
= ( 1234.5 , 'cc')
OR ( 0.09, 'c' )
= ( (select min(t2.nnum9) from TTF t2)
, (select min(t2.vch5) from TTF t2)
)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s19')
    #
    #  Expect all 5 rows.
    stmt = """select vch7, nint, ch3, nnum5
from TTF t1
where ( (1234.5 , 'cc') = ( 1234.5 , 'cc') )
OR ( ( 0.09, 'c' ) = ( 0.09, 'c' ) )
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s20')
    #
    #  ---------------------------
    #  Subquery transformations: SELECT attributes in Subqueries beneath OR.
    #  ---------------------------
    #       Id: TF.132       Subquery below OR has DISTINCT on uncorrelated column.
    #                        Both single and multiple DISTINCT.
    #       Id: TF.133       Subquery below OR has DISTINCT on correlated column.
    #  ---------------------------
    #
    #  Expect all 5 rows as in table TTF.
    stmt = """select vch7, nint, ch3, nnum5
from TTF t1
where ( (select distinct t1.nnum9 from TTF t2 where t1.nnum9 = 0.09 ) > 0)
OR ( 1 > ( (select min(t3.nint) from TTF t3) - 7) )
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s21')
    #
    #  Expect all 5 rows as in table TTF.
    stmt = """select vch7, nint, ch3, nnum5
from TTF t1
where ( 1 > ( (select min(t3.nint) from TTF t3) - 7) )
OR ((select distinct t1.nnum9 from TTF t2 where t1.nnum9 = 0.09 ) > 0)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s22')
    #
    #  Multiple DISTINCT; subset of rows (2 with nnum9 = 0.09) is selected.
    stmt = """select vch7, nint, ch3, nnum5
from TTF t1
where
( (select distinct t1.nnum9 from TTF t2
where t1.nnum9 = 0.09
) < t1.nsint
)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s23')
    #
    #  Expect 1 row ( ('abcdefg'  5  'cc'  2.0  .09  2) ).
    stmt = """select vch7, cast(nint as smallint), ch3, nnum5, nnum9 , nsint
from TTF t1
where
( (select distinct t1.nnum9 from TTF t2
where t1.nnum9 > 1000
) < 2000
)
OR
( (select distinct t1.nnum9 from TTF t2
where t1.nnum9 = 0.09
) < (t1.nsint/20)
)
OR
( (select distinct t2.n8 from TTF2 t2
where t2.n8 = 2
) < -3
)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s24')
    #
    #  Multiple DISTINCT; last clause is correct.
    #  Expect all 5 rows.
    stmt = """select vch7, nint, ch3, nnum5
from TTF t1
where
( (select distinct t2.n8 from TTF2 t2 where t2.n8 > 2 ) < 0)
OR
( (select distinct t2.n8 from TTF2 t2 where t2.n8 = 2 ) = 0)
OR
( (select distinct t2.n8 from TTF2 t2 where t2.n8 < 1 ) = 0)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s25')
    #
    #  ---------------------------
    #       Id: TF.134       Subquery below OR has GROUP BY on correlated column.
    #       Id: TF.135       Subquery below OR has GROUP BY on uncorrelated column.
    #  ---------------------------
    #
    stmt = """select vch7, nint, ch3, nnum5
from TTF t1
where ( (select t1.nnum9 from TTF t2
where t1.nnum9 = 0.09
group by t1.nnum9
) > 0 )
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s26')
    
    stmt = """select vch7, nint, ch3, nnum5
from TTF t1
where ( (select t1.nnum9 from TTF t2
where t1.nnum9 = 0.09
group by t1.nnum9 ) > 0
and
(t1.nint = 4) )
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """select vch7, nint, ch3, nnum5
from TTF t1
where ( 1 > ( (select min(t3.nint) from TTF t3 ) - 7 )
)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s27')
    #
    #  Expect 1 rows (nint 5):
    stmt = """select vch7, nint, ch3, nnum5
from TTF t1
where ((select t1.nnum9 from TTF t2
where t1.nnum9 = 0.09
group by t1.nnum9
) > 0 and (t1.nint = 4) )
OR ( 1 > ( (select min(t3.nint) from TTF t3) - 7
) and (t1.nint = 5) )
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s28')
    #
    #  Expect 1 row (nint 3):
    stmt = """select vch7, nint, ch3, nnum5
from TTF t1
where ( ( (select min(t3.nint) from TTF t3) - 7 = t1.nsint
) and (t1.nint = 4) )
OR (((select t1.nnum9 from TTF t2
where t1.nnum9 = 0.09
group by t1.nnum9
) > 0 ) and (t1.nint = 3) )
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s29')
    #
    #  Multiple Group By; subset of 3 rows (1 with nint=2 and
    #  2 with nnum9 = 0.09) is selected.
    stmt = """select vch7, nint, ch3, nnum5
from TTF t1
where ((select distinct t1.nnum9 from TTF t2
where t1.nnum9 > 1000
group by t2.nint
) < 2000)
OR ((select t1.nnum9 from TTF t2
where t1.nnum9 = 0.09
group by t1.nnum9
) < t1.nsint)
OR ((select t2.n8 from TTF2 t2
where t2.n8 = 2
group by t2.n8
) = t1.nint )
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s30')
    #
    #  Multiple Group By; last clause returns TRUE value,
    #  so should get 1 row with nint=3.
    stmt = """select vch7, nint, ch3, nnum5
from TTF t1
where ((select t2.n8 from TTF2 t2 where t2.n8 > 2
group by t2.n8
) < 0 and (t1.nint = 1) )
OR ((select t2.n8 from TTF2 t2 where t2.n8 = 2
group by t2.n8
) = 0 and (t1.nint = 2))
OR ((select t2.n8 from TTF2 t2 where t2.n8 < 1
group by t2.n8
) = 0 and (t1.nint = 3))
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s31')
    #
    #  ---------------------------
    #       Id: TF.136       Subquery below OR has HAVING on correlated column.
    #       Id: TF.137       Subquery below OR has HAVING on uncorrelated column.
    #  ---------------------------
    #
    #  Returns 1 row:
    stmt = """select t1.nnum9 from TTF t1
where t1.nnum9 > 10
group by t1.nnum9
having t1.nnum9  > 10
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s32')
    #
    #  Expect all 5 rows from TTF:
    stmt = """select vch7, nint, ch3, nnum5
from TTF 
where ( select t1.nnum9 from TTF t1
where t1.nnum9 > 10
group by t1.nnum9
having t1.nnum9  > 10
) > 0
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s33')
    #
    # The column reference T3.NINT must be a grouping column or
    # be specified within an aggregate -- that column is specified
    # within an aggregate.
    # Expect 0 rows.
    stmt = """select min(t3.nint) from TTF t3
having min(t3.nint) = 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    #  Expect ((1)).
    stmt = """select min(t3.nint) from TTF t3
having min(t3.nint) = 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s34')
    #  Expect ((3)).
    stmt = """select min(t3.nint) from TTF t3
where t3.nint = 3
having min(t3.nint) = 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s35')
    #
    #  Expect 2 rows (nint 4 and 5):
    stmt = """select vch7, nint, ch3, nnum5
from TTF t1
Where ( ( select t1.nnum9 from TTF t2
Group by t1.nnum9
Having t1.nnum9  > 10
) > 0 and
( t1.nint = 4) )
Or ( 1 > ( ( Select min(t3.nint) from TTF t3
Group by  t3.nint
Having t3.nint = 3
) - 7
) and (t1.nint = 5)
)
Order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s36')
    #
    #  Expect 1 row (nint 3):
    stmt = """select vch7, nint, ch3, nnum5
from TTF t1
Where ( ( (select min(t3.nint) from TTF t3) - 7 = t1.nsint
) and (t1.nint = 4) )
Or (( (select t1.nnum9 from TTF t2
Group by t1.nnum9
Having t1.nnum9 = 0.09
) > 0 )
And (t1.nint = 3) )
Order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s37')
    #
    #  Multiple Group By; subset of 3 rows (1 with nint=2 and
    #  2 with nnum9 = 0.09) is selected.
    stmt = """select vch7, nint, ch3, nnum5
from TTF t1
where ((select distinct t1.nnum9 from TTF t2
group by t2.nint
having t1.nnum9 > 1000
) < 2000)
OR ((select t1.nnum9 from TTF t2
Group by t1.nnum9
Having t1.nnum9 = 0.09
) < t1.nsint)
OR ((select t2.n8 from TTF2 t2
Group by t2.n8
Having t2.n8 = 2
) = t1.nint )
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s38')
    #
    #  Multiple Group By; last clause returns TRUE value,
    #  so should get 1 row with nint=3.
    stmt = """select vch7, nint, ch3, nnum5
from TTF t1
where ((select t2.n8 from TTF2 t2
Group by t2.n8
Having t2.n8 > 2
) < 0 and
(t1.nint = 1) )
Or ((select t2.n8 from TTF2 t2
Group by t2.n8
Having t2.n8 = 2
) = 0 and (t1.nint = 2))
Or ((select t2.n8 from TTF2 t2
Group by t2.n8
Having t2.n8 < 1
) = 0 and (t1.nint = 3))
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s39')
    
    _testmgr.testcase_end(desc)

def test004(desc="""a04"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     T1102:A04 (was part of A01 until memory
    #                      management faults occurred).
    #  Description:        This test verifies SQL subquery and
    #                      equality transformations via SELECT.
    #
    # =================== End Test Case Header  ===================
    #
    
    #
    stmt = """select * from TTF order by 1, 2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s0')
    #
    #  ---------------------------
    #  Subquery transformations: SELECT list.
    #  ---------------------------
    #
    #  ---------------------------
    #  Id: TF.003  Simple select: LEFT JOIN; subqueries in ON pred and select list.
    #  ---------------------------
    #
    #  Expect 10 rows.
    stmt = """select  ( select count(t0.vch7) from TTF t0 ) as count_ttf_vch7
, t1.vch7, t2.vch7
from TTF t1 left join TTF t2
on t1.vch7 < t2.vch7
order by 2,3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s1')
    #
    #  Expect 5 rows, ((5, xxx, 'cc')) where xxx is each value of
    #  vch7 in base table.
    stmt = """select ( select count(t0.vch7) from TTF t0 ) as count_ttf_vch7
, t1.vch7, t2.vch7
from TTF t1 left join TTF t2
on ( select distinct 'cc' from TTF t3 ) = t2.vch7
order by 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s2')
    #
    #  Expect (('cc'))
    stmt = """select max(t3.vch7) from TTF t3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s3')
    #
    #  Expect 5 rows, ((5, xxx, 'cc')) where xxx is each value of
    #  vch7 in base table.
    stmt = """select ( select count(t0.vch7) from TTF t0 ) as count_ttf_vch7
, t1.vch7, t2.vch7
from TTF t1 left join TTF t2
on ( select max(t3.vch7) from TTF t3 ) = t2.vch7
order by 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s4')
    #
    #  Expect 5 rows, ((5, xxx, 'cc')) where xxx is each value of
    #  vch7 in base table.
    stmt = """select ( select count(t0.vch7) from TTF t0 ) as count_ttf_vch7
, t1.vch7, t2.vch7
from TTF t1 left join TTF t2
on ( select max('cc') from TTF t3 ) = t2.vch7
order by 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s5')
    #
    #  Expect 5 rows, ((5, xxx, 'cc')) where xxx is each value of
    #  vch7 in base table.
    stmt = """select  ( select count(t0.vch7) from TTF t0 ) as count_ttf_vch7
, t1.vch7, t2.vch7
from TTF t1 left join TTF t2
on 'cc' = t2.vch7
order by 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s6')
    #
    #  Expect (('cc'))
    stmt = """select max(t4.vch7) from TTF t4 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s7')
    #
    #  Expect 21 rows: ( (20* (5, yyy, xxx) where 'yyy, xxx' combines each value
    #  of vch7 in base table except yyy is never 'cc') (5, 'cc', NULL)).
    stmt = """select ( select count(t0.vch7) from TTF t0 ) as count_ttf_vch7
, t1.vch7 as t1_vch7
, t2.vch7 as t2_vch7
from TTF t1 left join TTF t2
on t1.vch7 < ( select max(t4.vch7) from TTF t4 )
order by 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s8')
    #
    #  Expect 21 rows: ( (20* (5, yyy, xxx) where 'yyy, xxx' combines each value
    #  of vch7 in base table except yyy is never 'cc') (5, 'cc', NULL)).
    stmt = """select ( select count(t0.vch7) from TTF t0 ) as count_ttf_vch7
, t1.vch7 as t1_vch7
, t2.vch7 as t2_vch7
from TTF t1 left join TTF t2
on t1.vch7 < 'cc'
order by 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s9')
    #
    #  Expect 5 rows, ((5, xxx, 'cc')) where xxx is each value of
    #  vch7 in base table.
    stmt = """select ( select count(t0.vch7) from TTF t0 ) as count_ttf_vch7
, t1.vch7 as t1_vch7
, t2.vch7 as t2_vch7
from TTF t1 left join TTF t2
on ( select count(t3.vch7) from TTF t3 )
< ( select count(t4.vch7) from TTF t4 )
order by 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s10')
    
    _testmgr.testcase_end(desc)

def test005(desc="""a05"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     T1102:A05 (was part of A01 until memory
    #                      management faults occurred
    #                      during debugging).
    #  Description:        This test verifies SQL subquery and
    #                      equality transformations via SELECT.
    #
    # =================== End Test Case Header  ===================
    
    #
    #  ---------------------------
    #  Check tables.
    #  ---------------------------
    stmt = """select * from TTF order by 1,2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s0')
    stmt = """select * from TTF2 order by 1,2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s1')
    #
    #  ---------------------------
    #  Subquery transformations: SELECT list.
    #  ---------------------------
    #
    #  ---------------------------
    #  Id: TF.004 Simple select: NATURAL JOIN; subqueries in select
    #  list and WHERE pred.
    #                        NOTE: NO TABLE NAME exposed in NATURAL JOIN.
    #  ---------------------------
    #
    #  Expect {('abcdefg') ('abcdefg') ('d') ('cc')}
    stmt = """select vch7
from TTF t1 natural join TTF t2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s2')
    #
    #  Expect {4 * ('cc')}
    stmt = """select  ( select max(t0.vch7) from TTF t0 )
from TTF t1 natural join TTF t2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s3')
    #
    #  Expect {('cc')}
    stmt = """select max(vch7)
from TTF t1 natural join TTF t2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s4')
    #
    #  Expect 4 rows, null excluded.
    stmt = """select  ( select max(t0.vch7) from TTF t0 ) as max_vch7
, vch7
from TTF t1 natural join TTF t2
where 'A' < ( select vch7 from TTF where vch5 is null )
order by 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s5')
    #
    #  Expect 4 rows, null excluded.
    stmt = """select  ( select min(t0.vch7) from TTF t0 ), vch7
from TTF t1 natural join TTF t2
where ( select t3.vch7 from TTF t3 where vch5 is null )
= ( select t4.vch7 from TTF t4 where vch5 is null )
order by 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s6')
    #
    #  ---------------------------
    #       Id: TF.005       Simple select: UNION; subqueries in WHERE predicate and select list.
    #  ---------------------------
    #
    #  Expect 9 rows (10 if used UNION ALL; UNION removes one duplicate).
    stmt = """select vch7, nint from TTF 
union
select c5, n2 from TTF2 
order by 2,1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s7')
    #  Expect {('abcdefg')}
    stmt = """select vch7 from TTF where nint = 3 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s8')
    #
    #  Expect 5 rows.
    stmt = """select ( select vch7 from TTF where nint = 3 ) from TTF t
union
select c5 from TTF2 tt2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s9')
    #
    #  Expect 1 row {(3)}.
    stmt = """select ( select t1.nint from TTF t1 where nint = 3 ) from TTF t
union
select (select n2 from TTF2 tt1 where n2 = 3 ) from TTF2 tt2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s10')
    #
    #  Expect 5 * ('abcdefg' 3)
    stmt = """select ( select t1.vch7 from TTF t1 where nint = 3 ) as vch7
, ( select t3.nint from TTF t3 where nint = 3 ) as nint_is_3
from TTF t2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s11')
    #
    #  Expect (('alph' 3) ('cc' 3) ('cc' 3) ('e' 3) (Null 3))
    stmt = """select c5, (select n2 from TTF2 tt1 where n2 = 3 ) from TTF2 tt2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s12')
    #
    #  Expect ( ('abcdefg' 3) ('alph' 3) ('cc' 3) ('e' 3) (Null 3))
    stmt = """select ( select t1.vch7 from TTF t1 where nint = 3 )
, ( select t2.nint from TTF t2 where nint = 3 )
from TTF t3
union
select c5, (select n2 from TTF2 t4 where n2 = 3 ) from TTF2 t5
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s13')
    #
    #  ---------------------------
    #       Id: TF.006       Simple select: UNION CORRESPONDING; subqueries in WHERE pred and select list.
    #  ---------------------------
    #  Omit CORRESPONDING (from UNION CORRESPONDING) till supported.
    #  Kept test that gave bug for UNION without CORRESPONDING.
    #
    stmt = """select t.vch7 from TTF t where nint=5 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s14')
    #
    #  Expect ( ('abcdefg' 5) ('cc' 5) )
    stmt = """select ( select t.vch7 from TTF t where nint=5)
, ( select t.nint from TTF t where nint=5)
from TTF 
union -- corresponding
select ( select t1.ch4 from TTF t1 where nint=5)
,( select t.nint from TTF t where nint=5)
from TTF 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s15')
    #
    #  Use derived table to control column name.
    #  Expect 5 * ('abcdefg' 2)
    stmt = """select * from (
select ( select vch7 from TTF where nint=5)
,( select nsint from TTF where nint=5)
from TTF ) dt (unmatchedcolname2, nnum5)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s16')
    #
    #  Omit CORRESPONDING till supported.
    #  Expect (('abcdefg' 2))
    stmt = """select * from (
select ( select t.vch7 from TTF t where nint=5)
, ( select t.nnum5 from TTF t where nint=5)
from TTF ) dt (unmatchedcolname1, nint)
union -- corresponding
select * from (
select ( select vch7 from TTF where nint=5)
,( select t4.nsint from TTF t4 where nint=5)
from TTF ) dt (unmatchedcolname2, nsint)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s17')
    #
    #  ---------------------------
    #  Subquery transformations: in CASE statements.
    #  ---------------------------
    #
    #  ---------------------------
    #       Id: TF.031       Subquery within Simple CASE in <select list>.
    #  ---------------------------
    #  Expect ((12345)).
    stmt = """select t.n8 from TTF2 t where t.n8=12345 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s18')
    #
    #  Expect ((0 'jackpot') (1 'jackpot') (2 'jackpot')
    #          (2 'jackpot') (12345 'jackpot'))
    stmt = """select n8
, CASE (select t.n8 from TTF2 t where t.n8=12345)
WHEN 1 THEN ''
WHEN 2 THEN 'c'
WHEN 12345 THEN 'jackpot'
ELSE NULL
END
from TTF2 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s19')
    #
    #  Expect ((12345)).
    stmt = """select max(t.n8) from TTF2 t ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s20')
    #
    #  Expect ((0 'superduper') (1 'superduper') (2 'superduper')
    #          (2 'superduper' ) (12345 'superduper'))
    stmt = """select n8
, CASE (select max(t.n8) from TTF2 t)
WHEN 1 THEN 'aa'
WHEN 2 THEN 'bb'
WHEN 12345 THEN 'superduper'
ELSE 'e'
END
from TTF2 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s21')
    #
    #  -----------------------------
    #       Id: TF.032       Subquery within Simple CASE in WHERE clause.
    #  ---------------------------
    #
    stmt = """select v7 from TTF2 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s22')
    #
    #  Expect ((0))
    stmt = """select min(t.n8) from TTF2 t;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s23')
    #  Expect one row with v7='c', i.e. n8=12345.
    stmt = """select n8 from TTF2 
WHERE v7 = CASE (select min(t.n8) from TTF2 t)
WHEN 0 THEN 'c'
WHEN 1 THEN 'min(t.n8) is one'
ELSE NULL
END
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s24')
    #  Expect row with N2 = 4 and V7 ='c':
    stmt = """select * from TTF2 
WHERE v7 = CASE (select t.n2 from TTF2 t where t.n8=12345)
WHEN 1 THEN ''
WHEN 4 THEN 'c'
ELSE NULL
END
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s25')
    #
    #  ---------------------------
    #       Id: TF.033       Simple CASE within subquery.
    #                        Note TTF2 is used twice without correlation name
    #                        and no ambiguous column is referenced.
    #  ---------------------------
    #
    stmt = """select t.n8 from TTF2 t
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s26')
    #
    #  Expect 4 rows ((0, 'zero') (1, 'zero') (2, 'zero') (12345, 'zero'))
    stmt = """select n8, ( select distinct
CASE (select min(t.n8) from TTF2 t)
WHEN 1 THEN ''
WHEN 2 THEN 'c'
WHEN 0 THEN 'zero'
ELSE 'x'
END
from TTF2 ) as case_expr
from TTF2 
group by n8
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s27')
    #
    #  Expect 5 rows ((0, 'zero') (1, 'zero')
    #     (2, 'zero') (2, 'zero') (12345, 'zero'))
    stmt = """select n8, ( select distinct
CASE (select t.n8 from TTF2 t where t.n8=0)
WHEN 1 THEN ''
WHEN 2 THEN 'c'
WHEN 0 THEN 'zero'
ELSE NULL
END
from TTF2 ) as case_expr
from TTF2 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s28')
    #
    #  Expect 4 rows {(0 'x'), (1 'x'), (2 'x'), (12345 'x')}
    stmt = """select n8, ( select distinct
CASE (select t.n8 from TTF2 t where t.n8=12345)
WHEN 1 THEN ''
WHEN 2 THEN 'c'
ELSE  'x'
END
from TTF2 )
from TTF2 
group by n8
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s29')
    #
    #  ---------------------------
    #       Id: TF.034       Subquery in <select list> contains Searched CASE.
    #  ---------------------------
    #
    #  Expect 5 rows ((0, ..) (1, ..) (2, ..) (2, ..) (12345, ..))
    stmt = """select n8, n2, ( select distinct
CASE WHEN max(t2.n2) = 3 THEN 't2.n2 is 3'
WHEN max(t2.n2) = 4 THEN 't2.n2 is 4'
else 't2.n2 is not 3 or 4'
END
from TTF t
)
from TTF2 t2
group by n8, n2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s30')
    #
    #  Expect 4 rows ((0, ..) (1, ..) (2, ..) (12345, ..))
    stmt = """select n8, ( select distinct
CASE WHEN max(t2.n2) = 3 THEN 't2.n2 is 3'
WHEN max(t2.n2) = 4 THEN 't2.n2 is 4'
else 't2.n2 is not 3 or 4'
END
from TTF t
)
from TTF2 t2
group by n8
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s31')
    #
    #  ---------------------------
    #       Id: TF.035       Subquery in WHERE clause contains Searched CASE.
    #  ---------------------------
    #
    #  Expect 3 rows with n8 = 1 (1 row) or 2 (2 rows).
    stmt = """select *
from TTF2 t2
where
'e' > CASE (select min(t.n8) from TTF2 t where t2.n8=t.n8)
WHEN 1 THEN 'aa'
WHEN 2 THEN 'bb'
ELSE 'e'
END
order by 1,2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s32')
    
    _testmgr.testcase_end(desc)

def test006(desc="""a06"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     T1102:A06 (was part of A01 until memory
    #                      management faults occurred during
    #                      debugging; see also A04 and A05).
    #  Description:        This test verifies SQL subquery and
    #                      equality transformations via SELECT.
    #
    # =================== End Test Case Header  ===================
    #
    
    #
    stmt = """select * from TTF order by 1,2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s0')
    #
    #  ---------------------------
    #  Similar but different predicates in query and subquery
    #  ---------------------------
    #
    #  ---------------------------
    #       Id: TF.241       Query has: WHERE (w=x) and (x=y) and (y=z)
    #                          while one subquery has WHERE (w=x) and (y=z) ;
    #  ---------------------------
    #
    #  Expect 2 rows with vch3 'a' and 'cc'.
    stmt = """select * from TTF where   vch7 = ch3 order by 1,2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s1')
    stmt = """select * from TTF where   ch3 = vch7 order by 1,2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s2')
    #
    #  Expect 2 rows with ch3 'cc'.
    stmt = """select * from TTF where   ch4 = vch5 order by 1,2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s3')
    stmt = """select * from TTF where   ch3 = ch4  order by 1,2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s4')
    #
    #  Expect 1 row with ch3 = vch7 = ch4 = 'cc'.
    stmt = """select *
from TTF 
where   vch7 = ch3
and   ch3 = ch4
and   ch4 = vch5
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s5')
    #
    stmt = """select t1.vch7 from TTF t1
where vch7= ch3
and   ch3 = ch4
and   ch4 = vch5
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s6')
    #
    stmt = """select t1.vch5 from TTF t1
where vch7 = ch3
and   ch4 = vch5
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s7')
    #
    #  Expect 1 row with value 2.
    stmt = """select nint
from TTF t1
where vch7=
(select t1.vch7 from TTF t1
where vch7= ch3
and   ch3 = ch4
and   ch4 = vch5
)
and vch7 =
(select t1.vch5 from TTF t1
where vch7 = ch3
and   ch4 = vch5
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s8')
    #
    #  Expect 1 row with ch3 = vch7 = ch4 = 'cc'.
    stmt = """select *
from TTF t1
where vch7 =
(select t1.vch7 from TTF t1
where vch7= ch3
and   ch3 = ch4
and   ch4 = vch5
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s9')
    #
    #  ---------------------------
    #       Id: TF.242       Query has: WHERE (w=x) and (x=y) and (y=z)
    #                          while another subquery has WHERE (w=x) and (z=y).
    #  ---------------------------
    #  Expect 1 row with value 2.
    stmt = """select nint
from TTF t1
where vch7=
(select t1.vch7 from TTF t1
where vch7= ch3
and   ch3 = ch4
and   ch4 = vch5
)
and vch7 =
(select t1.vch5 from TTF t1
where vch7= ch3
and   vch5= ch4
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s10')
    #
    #  ---------------------------
    #       Id: TF.251       Query has: WHERE (w='a') and (x='b') and (y='c')
    #                        while its subquery has:
    #                            WHERE (w='a') and (x='b') and (y='c')
    #  ---------------------------
    #
    #  Expect 1 row with value 3.
    stmt = """SELECT * FROM
(select nint
from TTF t1
where vch7 = 'abcdefg'
and   ch3 = 'cc'
and   ch4 = 'alph'
and exists
(select   vch7
from  TTF t2
where   vch7 = 'abcdefg'
and   ch3 = 'cc'
-- Value of ch4 different from c3.
and   ch4 = 'alph'
group by vch7
)
) dt ORDER BY 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s11')
    
    #  ---------------------------
    #       Id: TF.252       Query has: WHERE (w='a') and (x='b') and (y='c')
    #                        while its subquery has:
    #                           WHERE (w='a') and (x='b') and (y='b').
    #  ---------------------------
    #
    #  Expect (( 3 )).
    stmt = """SELECT * FROM
(select nint
from TTF t1
where vch7 = 'abcdefg'
and   ch3 = 'cc'
and   ch4 = 'alph'
and exists
(select   vch7
from TTF t1
where   vch7 = 'abcdefg'
and   ch3 = 'cc'
-- Value of ch4 same as c3.
and   ch4 = 'cc'
)
) dt ORDER BY 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s12')
    #
    #  ---------------------------
    #       Id: TF.253       Query/subquery preds -- query has: WHERE (w=x) and (x=y) and (y='a')
    #                        while its subquery has WHERE (w=x) and (x='a').
    #  ---------------------------
    #
    #  Expect ((2) (5)).
    stmt = """SELECT * FROM
(select nint
from TTF t1
where ch4 = vch5
and vch5= ch3
and ch3 = 'cc'
and exists
(select   vch7
from TTF t1
where   ch4 = vch5
and  vch5 = 'cc'
group by vch7
)
) dt ORDER BY 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s13')
    #
    #  Expect (( 3 )).
    stmt = """SELECT * FROM
(select nint
from TTF t1
where vch7 = 'abcdefg'
and   ch3 = 'cc'
-- Value of ch4 different from c3.
and   ch4 = 'alph'
and exists
(select   vch7
from  TTF t2
where   vch7 = 'abcdefg'
and   ch3 = 'cc'
-- Value of ch4 same as c3.
and   ch4 = 'cc'
group by vch7
)
) dt ORDER BY 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s14')
    #
    #  ---------------------------
    #       Id: TF.261       Query/subquery preds with params -- query has WHERE (w=?p1) and (x=w) and (y=w)
    #                        while its subquery has WHERE (w=x) and (x=y)
    #  ---------------------------
    #  Expect (( 3 )).
    stmt = """SELECT * FROM
(select nint
from TTF t1
where vch7 = 'abcdefg'
and   ch3 = 'cc'
and   ch4 = 'alph'
and exists
(select   vch7
from  TTF t2
where   vch7 = 'abcdefg'
and   ch3 = 'cc'
-- Value of ch4 different from c3.
and   ch4 = 'alph'
group by vch7
)
) dt ORDER BY 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s15')
    #
    # Same query with param.
    stmt = """set param ?p1 'abcdefg';"""
    output = _dci.cmdexec(stmt)
    stmt = """SELECT * FROM
(select nint
from TTF t1
where vch7 = ?p1
and   ch3 = 'cc'
and   ch4 = 'alph'
and exists
(select   vch7
from  TTF t2
where   vch7 = ?p1
and   ch3 = 'cc'
-- Value of ch4 different from c3.
and   ch4 = 'alph'
group by vch7
)
) dt ORDER BY 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s16')
    #
    #  ---------------------------
    #       Id: TF.262       Query/subquery preds with params -- query has WHERE (w='a') and (x='b') and (y='c')
    #                        while its subquery has WHERE (w='a') and (x='b') and (y='b').
    #  ---------------------------
    #  Expect (( 3 )).
    stmt = """SELECT * FROM
(select nint
from TTF t1
where vch7 = 'abcdefg'
and   ch3 = 'cc'
and   ch4 = 'alph'
and exists
(select   vch7
from TTF t1
where   vch7 = 'abcdefg'
and   ch3 = 'cc'
-- Value of ch4 same as c3.
and   ch4 = 'cc'
)
) dt ORDER BY 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s17')
    #
    #  ---------------------------
    #       Id: TF.263       Query/subquery preds with params -- subquery reuses param used in query
    #                        giving WHERE (w=?p) and (x=y).
    #  ---------------------------
    #
    #  Expect ((2) (5)).
    stmt = """SELECT * FROM
(select nint
from TTF t1
where ch4 = vch5
and vch5= ch3
and ch3 = 'cc'
and exists
(select   vch7
from TTF t1
where   ch4 = vch5
and  vch5 = 'cc'
group by vch7
)
) dt ORDER BY 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s18')
    #
    stmt = """set param ?p1 'cc';"""
    output = _dci.cmdexec(stmt)
    #  Expect ((2) (5)). Same query as above but with params.
    stmt = """SELECT * FROM
(select nint
from TTF t1
where ch4 = vch5
and vch5= ch3
and ch3 = ?p1
and exists
(select   vch7
from TTF t1
where   ch4 = vch5
and  vch5 = ?p1
group by vch7
)
) dt ORDER BY 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s19')
    #
    #  Expect (( 3 )).
    stmt = """SELECT * FROM
(select nint
from TTF t1
where vch7 = 'abcdefg'
and   ch3 = 'cc'
-- Value of ch4 different from c3.
and   ch4 = 'alph'
and exists
(select   vch7
from  TTF t2
where   vch7 = 'abcdefg'
and   ch3 = 'cc'
-- Value of ch4 same as c3.
and   ch4 = 'cc'
group by vch7
)
) dt ORDER BY 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s20')
    
    _testmgr.testcase_end(desc)

def test007(desc="""a07"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     T1102:A07 (Isolates some tests using shared
    #                      global database).
    #  Description:        This test verifies SQL subquery and
    #                      equality transformations via SELECT.
    #
    #  ---------------------------
    #  Subquery transformations: in DTs and views.
    #  Some of these tests are done in context of other queries.
    #  ---------------------------
    #
    #  ---------------------------
    #  Part of Id: TF.043: Subqueries in <select list> upon Derived Table
    #  ---------------------------
    #
    
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.VNA1P005 v0
order by 1,3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s0')
    #
    #  Non-grouped query.
    #  Expect 6 rows of ( ( -4344 'DA' 'AA' ) ).
    stmt = """select (select V.n1 from """ + gvars.g_schema_arkcasedb + """.VNA1P005 V
where V.n1 < -4300
) as c1
, (select v1.c2 from """ + gvars.g_schema_arkcasedb + """.VNA1P005 v1 where v1.n1 = -2789 ) as c2
, (select v0.c2 from """ + gvars.g_schema_arkcasedb + """.VNA1P005 v0 where v0.c2 < 'B' ) as c3
from (select * from """ + gvars.g_schema_arkcasedb + """.VNA1P005 ) dt
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s1')
    #
    #  Grouped query -- NOTE, cannot GROUP BY associated derived column name.
    #  1999-03-24: Moved queries to file Qxx.
    #
    #  ---------------------------
    #       Id: TF.044       Subqueries in <where pred> upon Derived Table
    #       Id: TF.111       WHERE clause contains subqueries with one or more OR
    #                        Other tests with OR and subqueries are T1102:A03.
    #  ---------------------------
    #
    #  Single WHERE clause; subquery in <where pred> upon Derived Table.
    #  Expect ( -4344 'AA' 'BA' 'BA' )
    stmt = """select *
from (select * from """ + gvars.g_schema_arkcasedb + """.VNA1P005 ) dt
where -4344
= (select distinct dt.n1 from """ + gvars.g_schema_arkcasedb + """.VNA1P005 V where dt.n1 < -4300 )
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s2')
    #
    #  2 OR-ed subqueries in <where pred> upon Derived Table.
    #  Again expect 1 row: ( -4344 'AA' 'BA' 'BA' )
    stmt = """select *
from (select * from """ + gvars.g_schema_arkcasedb + """.VNA1P005 ) dt
where -4344
= (select distinct dt.n1 from """ + gvars.g_schema_arkcasedb + """.VNA1P005 V where dt.n1 < -4300 )
-- 	or ('a')
--          > (select distinct dt.c2 from VNA1P005 v1 where dt.n1 = -2789 )
or (select distinct dt.c3 from """ + gvars.g_schema_arkcasedb + """.VNA1P005 v1 where dt.n1 = -4344 )
> ('a')
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s3')
    #
    #  2 OR-ed subqueries in <where pred> upon Derived Table.
    #  Expect 2 rows: ( ( -4344 'AA' 'BA' 'BA' ) ( -2789 'DA' 'EA' NULL) )
    stmt = """select *
from (select * from """ + gvars.g_schema_arkcasedb + """.VNA1P005 ) dt
where -4344
= (select distinct dt.n1 from """ + gvars.g_schema_arkcasedb + """.VNA1P005 V where dt.n1 < -4300 )
or ('a')
> (select distinct dt.c2 from """ + gvars.g_schema_arkcasedb + """.VNA1P005 v1 where dt.n1 = -2789 )
-- 	or (select distinct dt.c3 from VNA1P005 v1 where dt.n1 = -4344 )
--          > ('a')
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s4')
    #
    #  3 OR-ed subqueries (2 ORs) in <where pred> upon Derived Table.
    #  Expect 2 rows: ( ( -4344 'AA' 'BA' 'BA' ) ( -2789 'DA' 'EA' NULL) )
    stmt = """select *
from (select * from """ + gvars.g_schema_arkcasedb + """.VNA1P005 ) dt
where -4344
= (select distinct dt.n1 from """ + gvars.g_schema_arkcasedb + """.VNA1P005 V where dt.n1 < -4300 )
or ('a')
> (select distinct dt.c2 from """ + gvars.g_schema_arkcasedb + """.VNA1P005 v1 where dt.n1 = -2789 )
or (select distinct dt.c3 from """ + gvars.g_schema_arkcasedb + """.VNA1P005 v1 where dt.n1 = -4344 )
> ('a')
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s5')
    #
    # NOTE: An expression in a comparison predicate may be a subquery
    # ONLY if the subquery is scalar (returns a single row consisting of a
    # single column). For example, this would be illegal:
    #    or ('a','a')
    #           > (select distinct dt.c2, dt.c3 from VNA1P005 v1
    #              where v1.n1 = -2789
    #             )
    #
    # Same as previous query, with params appearing in more than one place.
    # Params with 3 OR-ed subqueries (2 ORs) in <where pred> upon Derived
    # Table.
    # Expect 2 rows: ( ( -4344 'AA' 'BA' 'BA' ) ( -2789 'DA' 'EA' NULL) )
    stmt = """set param ?pn -4344 ;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p  a ;"""
    output = _dci.cmdexec(stmt)
    stmt = """select *
from (select * from """ + gvars.g_schema_arkcasedb + """.VNA1P005 ) dt
where ?pn
= (select distinct dt.n1 from """ + gvars.g_schema_arkcasedb + """.VNA1P005 V where dt.n1 < (?pn+1) )
or ?p
> (select distinct dt.c2 from """ + gvars.g_schema_arkcasedb + """.VNA1P005 v1 where dt.n1 = -2789 )
or (select distinct dt.c3 from """ + gvars.g_schema_arkcasedb + """.VNA1P005 v1 where dt.n1 = ?pn )
> ?p
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s6')
    #
    #  Add GROUP BYs to get the query we want.
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.VNA1P005 dt
where ?pn
= ( select distinct dt.n1 from """ + gvars.g_schema_arkcasedb + """.VNA1P005 V where dt.n1 < (?pn+1)
group by dt.n1
)
or ?p
> ( select distinct dt.c2 from """ + gvars.g_schema_arkcasedb + """.VNA1P005 v1
where dt.n1 = -2789
group by dt.c2
)
or ( select distinct dt.c3 from """ + gvars.g_schema_arkcasedb + """.VNA1P005 v1
where dt.n1 = ?pn
group by dt.c3
)
> ?p
group by n1, c2, c3, c4
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s7')
    #
    #  ---------------------------
    #       Id: TF.112       ON clause contains subqueries with one or more OR
    #                        Other tests with OR and subqueries are T1102:A03.
    #                        Other tests with OR in ON clause are in JOIN tests
    #                        (e.g. T1103:A02)
    #  ---------------------------
    #
    #  Non-grouped query.
    stmt = """select *
from (select * from """ + gvars.g_schema_arkcasedb + """.VNA1P005 ) dt
where -4344
= (select distinct dt.n1 from """ + gvars.g_schema_arkcasedb + """.VNA1P005 V where dt.n1 < -4300 )
or ('a')
> (select distinct dt.c2 from """ + gvars.g_schema_arkcasedb + """.VNA1P005 v1 where dt.n1 = -2789 )
or (select distinct dt.c3 from """ + gvars.g_schema_arkcasedb + """.VNA1P005 v1 where dt.n1 = -4344 )
> ('a')
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s8')
    # Same with params appearing in more than one place.
    stmt = """set param ?pn -4344 ;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?px a ;"""
    output = _dci.cmdexec(stmt)
    stmt = """select *
from (select * from """ + gvars.g_schema_arkcasedb + """.VNA1P005 ) dt
where ?pn
= (select distinct dt.n1 from """ + gvars.g_schema_arkcasedb + """.VNA1P005 V where dt.n1 < (?pn+1) )
or ?p
> (select distinct dt.c2 from """ + gvars.g_schema_arkcasedb + """.VNA1P005 v1 where dt.n1 = -2789 )
or (select distinct dt.c3 from """ + gvars.g_schema_arkcasedb + """.VNA1P005 v1 where dt.n1 = ?pn )
> ?p
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s9')
    #
    #  ---------------------------
    #       Id: TF.045       Subqueries in <select list> on Grouped view.
    #                        VNA1P005 is a grouped view with an outer join.
    #  ---------------------------
    #
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.VNA1P005 v0
order by 1,3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s10')
    stmt = """select distinct v0.c3,(select n1 from """ + gvars.g_schema_arkcasedb + """.VNA1P005 V where n1 < -4300)
, (select v1.c2 from """ + gvars.g_schema_arkcasedb + """.VNA1P005 v1 where v1.n1 = -2789 )
, (select count(c2) from """ + gvars.g_schema_arkcasedb + """.VNA1P005 )
from """ + gvars.g_schema_arkcasedb + """.VNA1P005 v0
order by 1,3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s11')
    #
    #  ---------------------------
    #       Id: TF.046       Subqueries in <where pred> on Grouped view.
    #                        VNA1P005 is a grouped view (also has outer join)
    #  ---------------------------
    #
    #  6 rows.
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.VNA1P005 v0
where ( select max(v1.c3) from """ + gvars.g_schema_arkcasedb + """.VNA1P005 v1 ) > 'AAAAA'
order by 1,3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s12')
    #  6 rows.
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.VNA1P005 v0
where ( select count(v1.c2) from """ + gvars.g_schema_arkcasedb + """.VNA1P005 v1 where v1.c2 IS NOT NULL )
= 4
order by 1,3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s13')
    #  1 row.
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.VNA1P005 v0
where ( select distinct v0.c2 from """ + gvars.g_schema_arkcasedb + """.VNA1P005 v1 where v0.c2 = 'DA' )
= 'DA'
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s14')
    #
    #  ---------------------------
    #       Id: TF.047       Subqueries in <select list> on UNION view.
    #                        VNA1P008 has union view (CORRESPONDING not supported
    #                        in 1998 so omitted).
    #  ---------------------------
    #
    stmt = """select (select max(VARCHAR0_500) from VNA1P008)
, (select min(v1.CHAR3_4) from VNA1P008 v1)
, (select count(v2.SDEC4_N20) from VNA1P008 v2)
from VNA1P008 v0
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s15')
    stmt = """select (select max(VARCHAR0_500) from BTA1P008)
, (select min(v1.CHAR3_4) from BTA1P008 v1)
, (select count(v2.SDEC4_N20) from BTA1P008 v2)
from VNA1P008 v0
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s16')
    #
    #  ---------------------------
    #       Id: TF.048       Subqueries in <where pred> on UNION view.
    #                        VNA1P008 has union.
    #  ---------------------------
    #
    stmt = """select VARCHAR0_500, UBIN1_20, CHAR3_4, SDEC4_N20, CHAR8_N1000
from VNA1P008 v0
where ( select max(v1.CHAR3_4) from VNA1P008 v1) > 'B'
order by 1,2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s17')
    #  Same with correlation name from outer table.
    #  Note, however, ANSI 7.6 SR 3: "No <column reference> contained
    #        in a <subquery> in the <search condition> that references
    #        a column of 'T' (the result of the preceding <from clause>
    #        shall be specified in a <set [aggregate] function
    #        specification>."
    #  Therefore, "where ( select max(v0.CHAR3_4) from BTA1P008 v1) > 'B'"
    #  violates  ANSI 7.6 SR 3; a predicate (not a set function) must
    #  be used to get the unique subquery value.
    #
    #  DISTINCT gets the 1 row in the correlated subquery.
    #  Expect ( ( 'CAAAGAAA' 4 'DAAAAAAA' 11 'AEAAEAAA' ) )
    stmt = """select VARCHAR0_500, UBIN1_20, CHAR3_4, SDEC4_N20, CHAR8_N1000
from VNA1P008 v0
where ( select distinct v0.CHAR3_4 from VNA1P008 v1
where v0.CHAR3_4 like 'DAA%'
) > 'B'
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s18')
    #
    stmt = """select CHAR10_20, CHAR13_100, VARCHAR15_UNIQ
from BTA1P001 
order by 1,2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s19')
    #
    #  ---------------------------
    #  Equality comparison in predicates.
    #  ---------------------------
    #
    #  ---------------------------
    #       Id: TF.211       Equality comparison in predicate of derived table.
    #                        AND predicates, where  a = b  and  b = c
    #  ---------------------------
    #
    stmt = """select CHAR10_20, CHAR13_100, VARCHAR15_UNIQ
from BTA1P001 
where CHAR10_20 = CHAR13_100
and CHAR13_100 = VARCHAR15_UNIQ
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s20')
    #
    stmt = """select CHAR10_20, CHAR13_100, VARCHAR15_UNIQ
from BTA1P001 
where CHAR10_20 = CHAR13_100
and CHAR10_20 = VARCHAR15_UNIQ
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s21')
    #
    #  check with 3 preds, a=b and b=c and c=a
    stmt = """select CHAR10_20, CHAR13_100, VARCHAR15_UNIQ
from BTA1P001 
where CHAR10_20 = CHAR13_100
and CHAR13_100 = VARCHAR15_UNIQ
and VARCHAR15_UNIQ = CHAR10_20
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s22')
    #
    stmt = """select * from ( select
(select CHAR10_20 from BTA1P001 where CHAR10_20 = CHAR13_100)
, (select CHAR13_100 from BTA1P001 where CHAR13_100 = VARCHAR15_UNIQ)
, (select VARCHAR15_UNIQ from BTA1P001 where VARCHAR15_UNIQ = CHAR10_20)
from BTA1P001 
) dt(a, b, c)
where  a = b
and  b = c
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s23')
    #
    stmt = """select * from ( select
(select max(CHAR10_20) from BTA1P001)
, (select max(CHAR13_100) from BTA1P001)
, (select max(VARCHAR15_UNIQ) from BTA1P001)
from BTA1P001 
where   CHAR10_20 = CHAR13_100
and   CHAR13_100 = VARCHAR15_UNIQ
) dt
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s24')
    #
    #  ---------------------------
    #       Id: TF.212       Equality comparison in predicate on Grouped view.
    #  ---------------------------
    #  View has cols varchar0_4    , char0_1000 , sbin7_2
    #             , varchar5_10    , char6_20   , ubin15_uniq
    #             , varchar15_uniq , char16_uniq
    #  Expect 12 rows in View.
    stmt = """Select Cast( v.varchar0_4 As Char(3) ) As cv
, v.char0_1000
, Cast( v.sbin7_2 As smallint ) As csi
From """ + gvars.g_schema_arkcasedb + """.VNA1P004 v
Order by 1,2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s25')
    #  Expect 14 rows.
    stmt = """Select Cast( v.varchar0_4 As Char(3) ) As cv
, v.char0_1000
, Cast( v.sbin7_2 As smallint ) As csi
From """ + gvars.g_schema_arkcasedb + """.VNA1P004 v, """ + gvars.g_schema_arkcasedb + """.VNA1P004 v2
Where ( v.varchar0_4 )
= (v2.varchar0_4 )
Order by 1,2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s26')
    #  Expect 12 rows.
    stmt = """Select Cast( v.varchar0_4 As Char(3) ) As cv
, v.char0_1000
, Cast( v.sbin7_2 As smallint ) As csi
From """ + gvars.g_schema_arkcasedb + """.VNA1P004 v, """ + gvars.g_schema_arkcasedb + """.VNA1P004 v2
Where ( v.varchar0_4,  v.char0_1000,  v.sbin7_2 )
= (v2.varchar0_4, v2.char0_1000, v2.sbin7_2 )
Order by 1,2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s27')
    #
    #  Expect cols N1, C2, C3, C4.
    #  Expect 6 rows in View.
    stmt = """Select *
From """ + gvars.g_schema_arkcasedb + """.VNA1P005 
Order by 1, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s28')
    #  Expect 6 rows matching on non-null C2.
    stmt = """Select v.N1,  v.C2,  v.C3,  v.C4, v2.N1, v2.C2, v2.C3, v2.C4
From """ + gvars.g_schema_arkcasedb + """.VNA1P005 v, """ + gvars.g_schema_arkcasedb + """.VNA1P005 v2
Where ( v.C2 )
= (v2.C2 )
Order by 1, 5
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s29')
    #  Expect 3 rows matching on non-null columns.
    stmt = """Select v.N1,  v.C2,  v.C3,  v.C4, v2.N1, v2.C2, v2.C3, v2.C4
From """ + gvars.g_schema_arkcasedb + """.VNA1P005 v, """ + gvars.g_schema_arkcasedb + """.VNA1P005 v2
Where ( v.N1,  v.C2,  v.C3,  v.C4 )
= (v2.N1, v2.C2, v2.C3, v2.C4 )
Order by 1, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s30')
    #
    #  ---------------------------
    #       Id: TF.213       Equality comparison in predicate on UNION view.
    #  ---------------------------
    #  Expect key col sdec16_uniq, and many other columns, including
    #  sbin0_4 , varchar0_500 , ubin1_20 , udec1_nuniq.
    #  Non-unique values for sdec6_4, char17_2.
    #  Expect 5 rows in View.
    stmt = """Select Cast( v.sdec16_uniq As Smallint ) As cs16
, Cast( v.sbin0_4 As Smallint ) As cs0 , v.varchar0_500
, Cast( v.ubin1_20 As Smallint ) As cs1 , v.udec1_nuniq
, v.sdec6_4, v.char17_2
From VNA1P008 v
Order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s31')
    #
    #  Expect 5 rows as in View.
    stmt = """Select Cast( v.sdec16_uniq As Smallint ) As cs16, v.sbin0_4 , v.varchar0_500
, Cast(v2.sdec16_uniq As Smallint ) As cs162,v2.sbin0_4, v2.varchar0_500
From VNA1P008 v, VNA1P008 v2
Where ( v.sdec16_uniq )
= (v2.sdec16_uniq )
Order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s32')
    #
    #  Expect 5 rows as in View.
    stmt = """Select  v.varchar0_500 , v.ubin1_20 , v.udec1_nuniq
, v2.varchar0_500, v2.ubin1_20, v2.udec1_nuniq
From VNA1P008 v, VNA1P008 v2
Where ( v.varchar0_500 )
= (v2.varchar0_500 )
Order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s33')
    #
    #  Expect 7 rows.
    stmt = """Select v.sdec6_4, v2.sdec6_4
From VNA1P008 v, VNA1P008 v2
Where ( v.sdec6_4 )
= (v2.sdec6_4 )
Order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s34')
    
    _testmgr.testcase_end(desc)

def test008(desc="""a08"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     T1102:A08
    #  Description:        This tests SQL subquery transformations
    #                      for subqueries beneath OR's.
    #
    # =================== End Test Case Header  ===================
    
    stmt = """select * from VNA1P006 order by 1,2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s0')
    #
    # ---------------------------
    # Subquery transformations: Subqueries beneath OR using params.
    # Also,
    # ---------------------------
    #      Id: RV.061       Aggregates in RVC.
    #      Id: TF.151       Parameters in SELECT list within subquery.
    # ---------------------------
    #
    # 04/21/09 added sigle quote around parameter value
    #   set param ?p Found ;
    stmt = """set param ?p 'Found' ;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?pn 5 ;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?pn2 2 ;"""
    output = _dci.cmdexec(stmt)
    #  Need CAST on parameters.
    stmt = """select distinct cast(?p as pic x(5))
from VNA1P006 
where (select min(sbin0_4) from VNA1P006)
= (select min(sdec6_4) from VNA1P006)
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s1')
    #
    stmt = """select distinct cast(?p as pic x(5))
from VNA1P006 
where ( (select min(sbin0_4) from VNA1P006),?pn)
= ( (select min(sdec6_4) from VNA1P006),?pn)
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s2')
    #
    stmt = """select distinct cast(?p as pic x(5)) from VNA1P006 
where ( (select -sum(sbin0_4)/?pn from VNA1P006),?pn)
= ( (select -?pn2/min(sdec6_4) from VNA1P006),?pn)
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s3')
    #
    stmt = """select distinct cast(?p as pic x(5)) from VNA1P006 
where (select -sum(sbin0_4)/cast(?pn as int) from VNA1P006)
= (select -cast(?pn2 as int)/min(sdec6_4) from VNA1P006)
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s4')
    #
    #  Tests in new contexts of row-value expressions, like:
    #  (col1, col2, col3, col4) = (col5, ?param6, col7, "string8").
    #  See also tests for Row-value constructor.
    stmt = """select distinct cast(?p as pic x(5)) from VNA1P006 
where ( (select -sum(sbin0_4)/cast(?pn as int) from VNA1P006), cast(?p as pic x(5)) )
= ( (select -cast(?pn2 as int)/min(sdec6_4) from VNA1P006), cast(?p as pic x(5)) )
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s5')
    #
    stmt = """select distinct cast(?p as pic x(5)) from VNA1P006 
where ( (select -sum(sbin0_4)/cast(?pn as int) from VNA1P006)
,cast(?p as char(6)) )
= ( (select -cast(?pn2 as int)/min(sdec6_4) from VNA1P006)
,cast(?p as char(6)) )
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s6')
    #
    #  ---------------------------
    #  Subquery transformations: Subqueries within Row Value Expressions.
    #  ---------------------------
    #       Id: TF.231       Equality comparison (in predicates) of cols, params, constants.
    #  like (col1, col2, col3, col4) = (col5, ?param6, col7, "string8").
    #  ---------------------------
    #
    #  Expect 4 rows in base table.
    stmt = """select varchar0_uniq,char2_2,char3_4,char15_100 ,char17_2
from BTA1P006 
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s7')
    #
    #  Expect 10 matching rows.
    stmt = """select t.varchar0_uniq,u.varchar0_uniq
from BTA1P006 t, BTA1P006 u
where t.char2_2=u.char2_2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s8')
    #
    #  Expect 16 rows in this cross product.
    stmt = """select t.varchar0_uniq as t_varchar0_uniq
, t.char2_2       as t_char2_2
, t.char3_4       as t_char3_4
, u.varchar0_uniq as u_varchar0_uniq
, u.char2_2       as u_char2_2
from BTA1P006 t, BTA1P006 u
order by t.varchar0_uniq, t.char2_2, u.varchar0_uniq
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s9')
    #
    #  Expect 2 rows that meet WHERE predicate.
    stmt = """select t.varchar0_uniq as t_varchar0_uniq
, t.char2_2       as t_char2_2
, t.char3_4       as t_char3_4
, u.varchar0_uniq as u_varchar0_uniq
, u.char2_2       as u_char2_2
from BTA1P006 t, BTA1P006 u
where (t.char2_2,  'AA', t.char3_4  ,'CJAAAAAC')
=('AA' ,u.char2_2 , 'AAAAAAAA' , u.varchar0_uniq)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s10')
    #
    #  ---------------------------
    #       Id: TF.232       Equality comparison (in predicates) of cols, params, constants, subqueries.
    #  like (col1, (subq1), col3, (subq2)) = (col5, ?param6, (subq3), "string8").
    #  ---------------------------
    #  Expect as above.
    stmt = """select t.varchar0_uniq, t.char2_2, t.char3_4
, u.varchar0_uniq, u.char2_2
from BTA1P006 t, BTA1P006 u
where (t.char2_2,
(select min(s.char2_2) from BTA1P006 s)
, t.char3_4
,(select max(r.varchar0_uniq) from BTA1P006 r)
)
= ( (select min(q.char2_2) from BTA1P006 q)
, u.char2_2
,(select min(p.char3_4) from BTA1P006 p)
, u.varchar0_uniq
)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s11')
    
    _testmgr.testcase_end(desc)

def test009(desc="""a09"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     T1102:A09
    #  Description:        This tests SQL subquery transformations
    #                      for subqueries beneath OR's.
    #
    # =================== End Test Case Header  ===================
    #
    
    stmt = """set transaction autocommit on;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select * from TTF  order by 1,2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s0')
    #
    #  ---------------------------
    #  Subquery transformations: Subqueries beneath OR, for
    #                            Insert/update/delete.
    #  ---------------------------
    #
    #  ---------------------------
    #       Id: TF.161b      Within View, Subqueries below multiple OR.
    #  ---------------------------
    #
    #  Pre-test code drops view VTFW.
    #
    #  Expect all 5 rows.
    stmt = """select * from TTF t0
where
( select nint from TTF t1
where t1.nint > -100 and t1.nint < 2
) = 1
order by 1, 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s1')
    #  Expect 1 row (('a' ...).
    stmt = """select * from TTF t0
where
( select nint from TTF t1
where t1.nint > -100 and t1.nint < 2
and t0.nint > -100 and t0.nint < 2
) = 1
order by 1, 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s2')
    #
    #  Note, not legal to include aggregate in subquery in where clause.
    #  e.g. where ( select max(t0.nint) from TTF t1 ) = 1
    #
    #  Expect all 5 rows.
    stmt = """select * from TTF t0
where
( select nint from TTF t1
where t1.nint > -100 and t1.nint < 2
) = 1
OR
( select nint from TTF t1
where t1.nint > 1 and t1.nint < 3
) = 2
OR
( select nint from TTF t1
where t1.nint > 2 and t1.nint < 4
) = 3
order by 1, 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s3')
    #
    #  Expect all 5 rows.
    stmt = """select * from TTF t0
where
( select nint from TTF t1
where t1.nint > -100 and t1.nint < 2
) = 1
OR
( select nint from TTF t1
where t1.nint > 1 and t1.nint < 3
) = 2
OR
( select nint from TTF t1
where t1.nint > 2 and t1.nint < 4
) = 3
OR
( select nint from TTF t1
where t1.nint > 3 and t1.nint < 5
) between 3.9 and 4.1
OR
( select nint from TTF t1
where t1.nint > 4 and t1.nint < 1000
) = 5
order by 1, 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s4')
    #
    # Create view using same SELECT statement.
    
    stmt = """create view VTFW as select * from
( select * from TTF t0
where
( select nint from TTF t1
where t1.nint > -100 and t1.nint < 2
) = 1
OR
( select nint from TTF t1
where t1.nint > 1 and t1.nint < 3
) = 2
OR
( select nint from TTF t1
where t1.nint > 2 and t1.nint < 4
) = 3
OR
( select nint from TTF t1
where t1.nint > 3 and t1.nint < 5
) between 3.9 and 4.1
OR
( select nint from TTF t1
where t1.nint > 4 and t1.nint < 1000
) = 5
) dt;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #  Expect all 5 rows.
    stmt = """select * from VTFW 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s5')
    stmt = """drop view VTFW;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #
    # This table should be empty.
    stmt = """delete from TTFA09 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 0)
    stmt = """insert into TTFA09  values
('w',      7,'cc' ,2.00,      'cc',2.0   ,'cc',2)
, ('x',    101,'a'  ,0.9,       NULL,NULL  ,NULL,0)
, ('y',    452,'cc' ,2.00,      'cc',2.0   ,'cc',2)
, ('z',    501,'cc' ,2.00,      'cc',2.0   ,'cc',2)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 4)
    stmt = """select * from TTFA09 
order by 1 DESC ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s6')
    
    stmt = """create view VTFW as select * from
(select * from TTFA09 t0 where
(select nint from TTFA09 t1 where t1.nint > 500 and t1.nint < 601)
= 501
OR (select nint from TTFA09 t1 where t1.nint > 200 and t1.nint < 301)
= 201
OR (select nint from TTFA09 t1 where t1.nint > 300 and t1.nint < 401)
= 302
OR (select nint from TTFA09 t1 where t1.nint > 400 and t1.nint < 501)
between 420 and 489
OR (select nint from TTFA09 t1 where t1.nint > 100 and t1.nint < 201)
= 101
) dt;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #  Expect all 4 rows inserted above.
    stmt = """select * from VTFW 
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s7')
    stmt = """drop view VTFW;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    #  The above look good -- check the new queries +d above w/correlation
    #  name and check this query and view.
    #  Expect all 4 rows inserted above.
    stmt = """select * from TTFA09 t0
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s8')
    #  Expect ((452))
    stmt = """select nint from TTFA09 t1
where t1.nint between 420 and 489
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s9')
    #  Expect the 4 rows from the base table.
    stmt = """select * from TTFA09 t0 where exists
(select nint from TTFA09 t1 where
t1.nint between 420 and 489 )
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s10')
    
    stmt = """create view VTFW as select * from
(select * from TTFA09 t0 where exists
(select nint from TTFA09 t1 where
t1.nint between 420 and 489 )
) dt;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #  Expect all 4 rows inserted above.
    stmt = """select * from VTFW 
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s11')
    stmt = """drop view VTFW;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test010(desc="""a10"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     T1102:A10
    #  Description:        This tests SQL subquery transformations
    #                      for subqueries beneath OR's.
    #
    # =================== End Test Case Header  ===================
    #
    
    #
    stmt = """set transaction autocommit on;"""
    output = _dci.cmdexec(stmt)
    #
    stmt = """select * from TTF  order by 1,2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s0')
    stmt = """select * from TTF2 order by 1,2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s1')
    #
    # ---------------------------
    # Subquery transformations: Subqueries beneath OR, for
    #                           Insert/update/delete.
    # ---------------------------
    #
    # ---------------------------
    #      Id: TF.141       Insert using Subqueries below one OR.
    # ---------------------------
    #
    # In pretest file, make temporary table TTFX to receive data.
    
    stmt = """delete from TTFX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 0)
    #
    # Insert 5 rows:
    stmt = """insert into TTFX (
select * from TTF t1
where (
(select max(t1.nnum5) from TTF t1)
, (select max(t1.vch7)  from TTF t1)
)
= ( 1234.5 , 'cc')
OR  (    0.09, 'c' )
= (
(select min(t2.nnum9) from TTF t2)
, (select min(t2.vch5) from TTF t2)
)
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 5)
    #
    stmt = """select * from TTFX 
order by 1,2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s2')
    #
    # ---------------------------
    #      Id: TF.143       Update using Subqueries below one OR.
    # ---------------------------
    #
    # Expect 1 row with value of 3.
    stmt = """update TTFX set n6 = (
select nint from TTF t1
where ( ( (select min(t3.nint) from TTF t3) - 7 = t1.nsint
) and (t1.nint = 4) )
OR (((select t1.nnum9 from TTF t2
where t1.nnum9 = 0.09
group by t1.nnum9
) > 0 ) and (t1.nint = 3) )
) where n2=1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    #
    stmt = """select * from TTFX 
order by 1,2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s3')
    #
    # ---------------------------
    #      Id: TF.145       Delete using Subqueries below one OR.
    # ---------------------------
    #
    # Expect 2 rows deleted (for nint=4 and nint=5):
    stmt = """delete from TTFX where n2 = (
select nint from TTF t1
where ((select t1.nnum9 from TTF t2
group by t1.nnum9
having t1.nnum9  > 10
) > 0 and (t1.nint = 4) )
OR ( 1 > ( (select min(t3.nint) from TTF t3
group by  t3.nint
having t3.nint = 3
) - 7
) and (t1.nint = 4) )
)
or n2 = (
select nint from TTF t1
where ((select t1.nnum9 from TTF t2
group by t1.nnum9
having t1.nnum9  > 10
) > 0 and (t1.nint = 5) )
OR ( 1 > ( (select min(t3.nint) from TTF t3
group by  t3.nint
having t3.nint = 3
) - 7
) and (t1.nint = 5) )
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 2)
    #
    stmt = """select * from TTFX 
order by 1,2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s4')
    #
    # Remove all rows:
    stmt = """delete from TTFX ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 3)
    #
    # ---------------------------
    #      Id: TF.142       Insert using Subqueries below multiple OR.
    #      Id: TF.161a      Within Derived Table, Subqueries below multiple OR.
    # ---------------------------
    #
    # 0 rows inserted.
    stmt = """insert into TTFX select * from
(select * from TTF t1 where
(select sum(nint) from TTF t1 where t1.nint < 4) =
(select sum(nint) from TTF t1 where t1.nint > 4)
OR (select sum(nint)   from TTF t1 ) =
(select count(nint) from TTF t1 )
OR (select count(nint) from TTF t1 where t1.nint > 5) =
(select count(nint) from TTF t1 where t1.nint <= 5)
) dt;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 0)
    #
    stmt = """select * from TTFX 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    #
    #  Check that the two aggregates are the same value.
    stmt = """select count(nint) from TTF t1 where t1.nint > 3 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s5')
    stmt = """select count(nint) from TTF t1 where t1.nint < 3 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s6')
    #
    # Predicate is true (2 values of nint are over 3 and 2 are under 3),
    # so all 5 rows are inserted.
    stmt = """insert into TTFX select * from
(select * from TTF t1 where
(select sum(nint) from TTF t1 where t1.nint < 4) =
(select sum(nint) from TTF t1 where t1.nint > 4)
OR (select sum(nint)   from TTF t1 ) =
(select count(nint) from TTF t1 )
OR (select count(nint) from TTF t1 where t1.nint > 5) =
(select count(nint) from TTF t1 where t1.nint <= 5)
OR (select count(nint) from TTF t1 where t1.nint > 3) =
(select count(nint) from TTF t1 where t1.nint < 3)
) dt;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 5)
    #
    stmt = """select * from TTFX 
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s7')
    #
    #  ---------------------------
    #       Id: TF.144       Update using Subqueries below multiple OR.
    #  ---------------------------
    #
    #  Multiple DISTINCT; subset of rows (one with nnum9 = 1234567.89 ) is selected.
    #  Check results for single OR components:
    stmt = """select distinct nnum9 from TTF t1
where ((select distinct t1.nnum9 from TTF t2
where t1.nnum9 > 1000 ) > 2000)
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s8')
    #
    # Expect 0 rows.
    stmt = """select distinct nnum9 from TTF t1
where ((select distinct t2.n8 from TTF2 t2
where t2.n8 = 2 ) < -3 )
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    #
    # 2 rows with n2 = 4, 5 get n6 updated to 1234567.89.
    stmt = """update TTFX set n6 = (
select distinct nnum9 from TTF t1
where ((select distinct t1.nnum9 from TTF t2
where t1.nnum9 > 1000 ) > 2000)
OR ((select distinct t1.nnum9 from TTF t2
where t1.nnum9 > 1000 ) > 2000)
OR ((select distinct t2.n8 from TTF2 t2
where t2.n8 = 2 ) < -3 )
OR ((select distinct t2.n8 from TTF2 t2
where t2.n8 = 2 ) < -3 )
) where n2>3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 2)
    #
    stmt = """select * from TTFX 
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s9')
    #
    # ---------------------------
    #      Id: TF.146       Delete using Subqueries below multiple OR.
    # ---------------------------
    #
    # Expect 2 rows deleted (for n8=2 ((n8+1)=nint=3) ):
    # Multiple Group By; last clause returns TRUE value.
    stmt = """delete from TTFX where n8 +1 = (
select nint from TTF t1
where ((select t2.n8 from TTF2 t2
group by t2.n8
having t2.n8 > 2
) < 0 and (t1.nint = 1) )
OR ((select t2.n8 from TTF2 t2
group by t2.n8
having t2.n8 = 2
) = 0 and (t1.nint = 2))
OR ((select t2.n8 from TTF2 t2
group by t2.n8
having t2.n8 < 1
) = 0 and (t1.nint = 3))
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 2)
    #
    #  Expect n2=1,3,4.
    stmt = """select * from TTFX 
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s10')
    
    stmt = """delete from TTFX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 3)
    
    _testmgr.testcase_end(desc)

