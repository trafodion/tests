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

import a14setup
import a17setup
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
    # =============== --- Begin Test Case Header  ==================
    #
    # Test case name:      T1103:A01
    # Description:         This test verifies SQL JOIN via SELECT.
    #                      Also some tests for Row Value Constructor.
    #
    # ================= ---End Test Case Header  ===================
    
    stmt = """insert into TJOIN values
-- Use literal blank until DEFAULT is supported (see note above).
--                     ('a',      1,'c' ,0.9,   DEFAULT ,NULL  ,NULL,0)
('a',      1,'c' ,0.9,       ''  ,NULL  ,NULL,0)
, ('cc'     ,2,'cc',2.00,      'cc',2.0   ,'cc',2)
, ('abcdefg',3,'cc',0.09,    'alph',2     ,'cc',1)
, ('b',      4,'c' ,1234567.89,'e' ,1234.5,'c' ,12345)
, ('abcdefg',5,'cc',0.09,      'cc',2     ,'cc',2)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 5)
    #  Expect 5 rows as inserted.
    stmt = """select * from TJOIN 
order by 1, 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s0')
    #
    # Expect 2 rows inserted.
    stmt = """insert into TJOIN2 
select * from TJOIN where nint < 3 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 2)
    stmt = """select * from TJOIN2 
order by 1, 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s1')
    #
    # Expect 6 rows inserted.
    stmt = """insert into TJOIN4 
select VARCHAR5_10 ,SDEC5_100 ,UDEC6_500 ,CHAR6_20 ,UBIN6_2 ,SBIN7_2
from BTA1P001 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 6)
    
    stmt = """select * from TJOIN4 
order by 1, 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s2')
    #
    # Expect 2 rows inserted -- until can insert all NULL.
    stmt = """insert into TJOINNUL values
--                     ( NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL)
--                   ,
('cc'     ,2,'cc',2.00,   'cc',2.0   ,'cc',NULL)
, (NULL     ,3,'cc',0.09, 'alph',2     ,'cc',1)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 2)
    stmt = """select * from TJOINNUL 
order by 1, 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s3')
    #
    # ----------------------------
    #  Basic NATURAL [INNER] JOIN ( [USING] is illegal -- see negative tests)
    #  NATURAL JOIN (natural equi-join) selects rows that have equal values;
    #  all exposed columns should have the same name.
    #  "USING" (illegal with NATURAL JOIN) is used in other joins to
    #  compare a subset of columns.
    # ----------------------------
    #       Id: JT.006      NATURAL JOIN
    #       Id: JT.007      NATURAL INNER JOIN
    #       Id: JT.030      All column names the same.
    #       Id: JT.032c     All row values are the same in matching columns.
    #       Id: JT.032e     Columns disallow NULLs (BTA1P001)
    #             or allow but don't have NULLs (BTA1P002)
    #
    #  Should show 6 rows as in base table.
    
    stmt = """select VARCHAR0_4 , CHAR1_4 , UDEC1_10 , SDEC5_100 , UBIN6_2
from BTA1P001 
natural join BTA1P001 t 
order by 2, 4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s4')
    #
    #  Should show 7 rows as in base table.
    stmt = """select VARCHAR0_4 , CHAR0_20 , SBIN1_100 , CHAR1_4 , UBIN1_4 ,
CHAR2_2 , SBIN3_1000 , SBIN4_2 , CHAR4_10
from BTA1P002 
natural inner join BTA1P002 t 
order by 1, 2, 3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s5')
    #
    #  Should show 4 rows as in base table.
    stmt = """select count(*) from BTA1P003 
natural join BTA1P003 t;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s6')
    #
    #  Should show 13 rows as in base table.
    stmt = """select count(*) from BTA1P004 
natural join BTA1P004 t;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s7')
    #
    # ----------------------------
    #       Id: JT.032f     Some of the data values are NULL (NULLs are in
    #                       BTA1P005,6,7,8,9)
    # ----------------------------
    #
    #  Expect 4 rows.
    stmt = """select * from TJOIN 
natural join TJOIN t 
order by 1, 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s8')
    #
    # Expect 0 rows.
    stmt = """select * from TJOINNUL 
natural join TJOINNUL t 
order by 1, 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    #
    #  Because all rows in BTA1P005 and
    #  BTA1P006 have at least one null column,
    #  0 rows should be returned from Natural Joins.
    #  Outer Join (elsewhere) should return number of rows in
    #  appropriate base table.
    stmt = """select count(*) from BTA1P005 
natural inner join BTA1P005 t 
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s9')
    #
    # Expect 0 rows.
    stmt = """select char0_n10 from BTA1P005 
natural join BTA1P005 t 
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    #
    # ----------------------------
    #       Id: JT.004      Correlated subquery contains RIGHT [OUTER] JOIN.
    #       Id: RV.022      RVC is (subquery)
    #       Id: RV.031      RVC returns values based on inner column(s)
    #       Id: RV.032      RVC returns values based on outer correlated column(s)
    #       Id: RV.051      RVC returns 1 row
    # ----------------------------
    #
    #  Correlated subquery: Expect 2 rows {(1,a),(2,cc)}.
    stmt = """select n2,
( select t3.v1 from TJOIN t1 right join TJOIN t2
on 1=1
where t1.nint=2 and t2.nint=2)
from TJOIN2 t3
order by 1, 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s10')
    #
    #  Expect 1 row.
    stmt = """select t1.VCH7, t2.NINT, t1.CH3, t1.NNUM9, t2.CH4, t2.NNUM5, t1.VCH5, t2.NSINT
from TJOIN t1 right join TJOIN t2
on 1=1
where t1.nint=2 and t2.nint=2
order by 1, 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s11')
    #
    #  Correlated subquery: Expect 2 row(s) {(1,a),(2,cc)}.
    stmt = """select n2,
( select t3.v1 from TJOIN t1 right outer join TJOIN t2
on t2.nint = t1.nint
where t2.nint=2)
from TJOIN2 t3
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s12')
    #
    #  Correlated subquery: Get 2 row(s) {(1,?),(2,cc)}.
    stmt = """select n2,
( select t3.v1 from TJOIN t1 right outer join TJOIN t2
on t2.nint = t1.nint
where t3.n2 = 2 and t1.nint=2 and t2.nint=2)
from TJOIN2 t3
order by 1, 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s13')
    #
    # ----------------------------
    #       Id: JT.005      Un-correlated subquery contains RIGHT [OUTER] JOIN.
    #       Id: RV.041      RVC returns numeric data type
    # ----------------------------
    #  Un-correlated subquery: Expect 2 row(s) {(1,2),(2,2)}.
    # 04/28/09 all following queries are commented out for WM mode testing
    stmt = """select n2,
( select nint  from TJOIN t1
right outer join TJOIN2 t2
on nint = n2
where n2 = 2
)
from TJOIN2 t3
order by 1, 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s14')
    
    stmt = """select nint  from TJOIN t1
right outer join TJOIN2 t2
on nint = n2
where n2 = 2
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s15')
    
    # ----------------------------
    #       Id: JT.009      Correlated subquery contains NATURAL JOIN.
    # ----------------------------
    #  Expect 2 row(s) {(1,cc),(2,cc)}.
    stmt = """select n2,
( select vch7 from TJOIN t1
natural join TJOIN t2
where nint=2
)
from TJOIN2 t3
order by 1, 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s16')
    
    #  Correlated subquery: Expect 2 row(s) {(cc),(?)}.
    stmt = """select
( select vch7 from TJOIN t1
natural join TJOIN t2
where nint=t3.n2
)
from TJOIN2 t3
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s17')
    
    # ----------------------------
    #       Id: JT.185a     Derived table contains NATURAL join
    #       Id: JT.185b     Derived table contains NATURAL join with GROUP BY.
    # ----------------------------
    #  Expect 1 row { b }.
    stmt = """select * from
( select vch7 from TJOIN t1
natural join TJOIN t2
where nint=4
) dt
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s18')
    #  Expect 1 row { b }.
    stmt = """select * from
( select vch7 from TJOIN t1
natural join TJOIN t2
where nint>3 and (nint<5)
group by vch7
) dt
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s19')
    #  Expect 2 rows { ( b ) (cc) }.
    stmt = """select * from
( select vch7 from TJOIN t1
natural join TJOIN t2
where nint<5 and vch7>'ac'
group by vch7, nint
) dt
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s20')
    
    # Expect 0 rows.
    stmt = """select * from
( select sbinneg15_nuniq ,char2_2 , char3_4
from BTA1P005 t1
natural join BTA1P005 t2
natural join BTA1P005 t3
) dt
natural join
( select char2_2
from BTA1P005 t1
natural join BTA1P005 t2
natural join BTA1P005 t3
) dt2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    # Expect 0 rows.
    stmt = """select * from
( select char2_2
from BTA1P005 t1
natural join BTA1P005 t2
natural join BTA1P005 t3
) dt
natural join
( select char2_2
from BTA1P005 t1
natural join BTA1P005 t2
natural join BTA1P005 t3
) dt2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    # ----------------------------
    #       Id: JT.010      NATURAL JOIN Table contains correlated subquery
    #       Id: JT.181      JOIN on derived table
    # ----------------------------
    #  Expect all 5 rows from TJOIN.
    stmt = """select vch7 from TJOIN t1 natural join
( select ( select t2.vch7 from TJOIN2 t3
where t2.vch7 = t3.v1 and 'cc'=t3.v1)
from TJOIN t2 where t2.nint = 2
) dt
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s21')
    
    #  Expect 1 row ( ('cc') ) from TJOIN.
    stmt = """select
( select t2.vch7 from TJOIN2 t3
where t2.vch7 = t3.v1 and 'cc'=t3.v1)
from TJOIN t2 where t2.nint = 2
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s22')
    
    _testmgr.testcase_end(desc)

def test002(desc="""a02"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =============== --- Begin Test Case Header  ==================
    #
    #  Test case name:     T1103:A02
    #  Description:        SQL JOIN on grouped views, Row Value
    #                      constructors, and derived tables.
    #
    # ================= ---End Test Case Header  ===================
    
    stmt = """select *
from VNA1P005 t1
order by n1, c3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s0')

    stmt = """select n1, c2 from VNA1P005 
natural join VNA1P005 t 
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s1')
    #  Expect ((1 'AA') (2 'BA'))
    stmt = """select count(n1), c2 from VNA1P005 
natural join VNA1P005 t 
group by c2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s2')
    #
    #  With natural outer join, expect all 6 rows, including those
    #  containing nulls.
    #  Expect (( -4344 'AA') ( -3552 'BA') (-2789 'DA') (-2389 'BA')
    #          ( NULL  NULL) ( NULL NULL ))
    stmt = """select n1, c2 from VNA1P005 
natural right outer join VNA1P005 t 
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s3')
    #
    #  Note that for count(column), null values count as zero.
    #  Expect ((0  NULL ) (1 'AA') (1 'DA') (2 'BA'))
    stmt = """select count(n1), c2 from VNA1P005 
natural right outer join VNA1P005 t 
group by c2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s4')
    #
    #  Note that for count(*), null values count as non-zero.
    #  Expect ((1 'AA') (1 'DA') (2 'BA') (2  NULL ))
    stmt = """select count(*), c2 from VNA1P005 
natural right outer join VNA1P005 t 
group by c2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s5')
    #
    # ----------------------------
    #       Id: JT.011      NATURAL  LEFT  JOIN
    # ----------------------------
    #
    stmt = """select count(*) from BTA1P006;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s6')
    #  Should show 4 rows as in view.
    stmt = """select count(*) from BTA1P006 
natural left join BTA1P006 t;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s7')
    #
    # ----------------------------
    #       Id: JT.012      NATURAL  LEFT  OUTER  JOIN
    # ----------------------------
    #
    #  Should show 6 rows as in base table.
    stmt = """select count(*) from BTA1P007 
natural left outer join BTA1P007 t;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s8')
    #
    # ---------------------------
    #      Id: JT.031      No columns match.
    # ---------------------------
    # No Columns match.
    # Expect 0 rows.
    
    stmt = """select * from BTA1P001 
natural join BTA1P004 t;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    #
    # ----------------------------
    #       Id: JT.200b     JOIN upon a grouped view containing a GROUP BY clause (e.g., NA1P002, NA1P004)
    # ----------------------------
    #
    #  Should show 7 rows as in view.
    stmt = """select CAST(char17_100 as char(20)) as char17_100
,udec17_100
from VNA1P002 
natural join VNA1P002 v
order by 1,2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s9')
    #
    #  Should count 3 rows as in view.
    stmt = """select count(*)
from VUA1P003 
natural join VUA1P003 v
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s10')
    #
    #  Should show 12 rows as in view.
    stmt = """select VARCHAR0_4, SBIN7_2, VARCHAR5_10, CHAR6_20, UBIN15_UNIQ
from VNA1P004 
natural join VNA1P004 v
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s11')
    #
    # ----------------------------
    #       Id: JT.301      JOIN upon a view containing natural join (VNA1P006)
    #       Id: OR.085      Orthogonality: one or more UNION view columns in Left and Right side of NATURAL JOIN.
    # ----------------------------
    #  Should show 4 rows as in view.
    stmt = """select sbin0_4 , sdec5_10 , sdec6_4 , varchar0_uniq
from VNA1P006 
natural join VNA1P006 v
order by 1,2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s12')
    #
    #  Should show 6 rows as in view.
    stmt = """select *
from ( select CCONCATVARCHAR from VNA1P007) v
natural join ( select CCONCATVARCHAR from VNA1P007) v2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s13')
    #
    # Should show 0 rows; 5 rows in view, all contain NULL.
    stmt = """select SDEC4_N20,SBIN4_N1000,CHAR4_N10,CHAR5_N20,SDEC5_10,UBIN5_N500
from VNA1P008 
natural join VNA1P008 v
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    #
    #  Expect ((0)).
    stmt = """select count(*)
from VNA1P008 
natural join VNA1P008 v
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s14')
    
    _testmgr.testcase_end(desc)

def test003(desc="""a03"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =============== --- Begin Test Case Header  ==================
    #
    #  Test case name:     T1103:A03
    #  Description:        SQL JOIN on grouped views, Row Value
    #                      constructors, and derived tables.
    #
    # ================= ---End Test Case Header  ===================
    #
    # ----------------------------
    #  Check contents of interesting view.
    # ----------------------------
    #  Expect 6 rows of our global view.
    
    stmt = """select N1, C2, C3, C4
from VNA1P005 j1
order by N1, C3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s0')
    #
    # ---------------------------
    #      Id: DA.001      PREPARE/EXECUTE/DEALLOCATE cycle for single statement name.
    # ---------------------------
    #
    # 1st PREPARE
    #
    # Look at JOINED VIEW!! Use different column order from
    # that of the subsequently prepared query.
    
    stmt = """prepare s1 from
select C4, C3, C2, N1 from VNA1P005 
natural join VNA1P005 t 
order by c4, n1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    #  Expect 3 rows (without null values):
    #                (('AA' 'AA' 'BA' -3552)
    #                 ('AA' 'AA' 'BA' -2389)
    #                 ('BA' 'BA' 'AA' -4344))
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s1')
    #
    # 2nd PREPARE
    #
    # ---------------------------
    #      Id: DT.101b     Within Derived Table use NATURAL JOIN: SELECT * from (SELECT * from NJ)
    # ---------------------------
    # Prepare another query with same statement name, but
    # different column order, and add DT.
    stmt = """prepare s1 from
select n1 , c2 , c3 , c4 from
( select * from VNA1P005 
natural join VNA1P005 t 
) dt
order by n1, c4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    #  Expect 3 rows without nulls from original view.
    #  ( (-4344 ... BA) (-3552 ... AA) (-2389 ... AA) )
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s2')
    #
    # 3rd PREPARE
    #
    # ---------------------------
    #      Id: DT.101c     Within Derived Table use NATURAL JOIN: SELECT col from (SELECT * from NJ)
    # ---------------------------
    # Prepare another query with same statement name, but select one
    # specific column.
    stmt = """prepare s1 from
select C3 from
( select * from VNA1P005 
natural join VNA1P005 t 
) dt
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    #  Expect ( (AA) (AA) (BA) )
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s3')
    #
    # 4th PREPARE
    #
    # ---------------------------
    #      Id: DT.101d     Within DT use NATURAL JOIN: SELECT columns with and without dt correlation name
    # ---------------------------
    # Prepare another query with same statement name, but select
    # specific columns.
    stmt = """prepare s1 from
select C2, dt.C3 from
( select * from VNA1P005 
natural join VNA1P005 t 
) dt
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    #  Expect ( (AA BA) (BA AA) (BA AA) )
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s4')
    #
    # ----------------------------
    #  Combinations of RIGHT JOINs
    # ----------------------------
    #       Id: JT.211      RIGHT JOIN/LEFT JOIN combinations.
    # ----------------------------
    #
    #  RJ with no column from Left-hand side.
    #  Expect 8 rows (4 for 'BA' in join columns):
    #     ( (AA -3552) (AA -2389) (BA  -4344) (BA  -4344)
    #       (BA  ? )   (BA   ? )  (DA  ? )    (EA  -2789) )
    stmt = """select j2.C3 , j2.N1
from VNA1P005 j1
right join VNA1P005 j2
on j1.C2 = j2.C3
order by 1,2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s5')
    #  RJ with no column from Right-hand side.
    #  Expect 8 rows (4 for 'BA' in join columns) and
    #     ( 2 for 'AA') and ('DA' -2789) ( NULL  NULL))
    stmt = """select j1.C2 , j1.N1
from VNA1P005 j1
right join VNA1P005 j2
on j1.C2 = j2.C4
order by 1,2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s6')
    #
    #  LJ with columns from both sides.
    #  Expect 9 rows (2* 'AA'; 2*2* 'BA'; 1* 'DA'; 2* null).
    stmt = """select j1.C2, j2.C3 as j2C3
, j1.N1, j1.C3, j1.C4
, j2.N1 as j2N1, j2.C2 as j2C2, j2.C4 as j2C4
from VNA1P005 j1
left join VNA1P005 j2
on j1.C2 = j2.C3
order by j1.C2, j2.N1, j1.N1, j1.C3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s7')
    #
    stmt = """prepare s1 from
select b, g from
( select * from VNA1P005 j1
right join VNA1P005 j2
on j1.C2 = j2.C4
) dt1 (a,b,c,d,e,f,g,h)
right join
( select * from VNA1P005 j1
left join VNA1P005 j2
on j1.C2 = j2.C3
) dt2 (i,j,k,l,m,n,o,p)
on 1=1
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    #
    #  Expect 8*9 rows.
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s8')
    #
    # (1997-11-14)  jz  Commented out RELEASE and DEALLOCATE
    #      DEALLOCATE PREPARE s1;
    #
    # ---------------------------
    #      Id: JT.212      LEFT JOIN/RIGHT JOIN combinations.
    #      Id: DI.006      DISTINCT expression: SELECT list without <set quantifier>
    # ---------------------------
    stmt = """prepare s1 from
select distinct (b || ' ' || h || ' ' || j || ' ' || o )
as concatenated_fields from
( select * from VNA1P005 j1
right join VNA1P005 j2
on j1.C2 = j2.C4
) dt1 (a,b,c,d,e,f,g,h)
right join
( select * from VNA1P005 j1
left join VNA1P005 j2
on j1.C2 = j2.C3
) dt2 (i,j,k,l,m,n,o,p)
on 1=1
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    #  Expect 10 rows (3*3 plus NULL)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s9')
    #
    # (1997-11-14)  jz  Commented out RELEASE and DEALLOCATE
    #      DEALLOCATE PREPARE s1;
    #
    # ---------------------------
    #      Id: JT.213      RIGHT JOIN/NATURAL JOIN combinations.
    #      Id: DI.002      DISTINCT expression: COUNT(DISTINCT <expression>).
    #      Id: DI.007      DISTINCT expression: SELECT list with <set quantifier>
    # ---------------------------
    # (Scaffold query)
    stmt = """prepare s1 from
select (j || ' ' || o ) from
( select * from VNA1P005 j1
right join VNA1P005 j2
on j1.C2 = j2.C2
) dt2 (i,j,k,l,m,n,o,p)
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    #
    #  Expect 8 rows ((AA BA) 4*(BA AA) (DA EA) 2*NULL)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s10')
    #
    # (Scaffold query)
    stmt = """prepare s1 from
select count(distinct(b || ' ' || c)) from
( select * from VNA1P005 
natural join VNA1P005 t 
) dt1 (a,b,c,d)
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    #  Expect ((2))
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s11')
    #
    stmt = """prepare s1 from
select (b || ' ' || c) from
( select * from VNA1P005 
natural join VNA1P005 t 
) dt1 (a,b,c,d)
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    #  Expect (('AA BA') ('BA AA') ('BA AA'))
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s12')
    #
    stmt = """prepare s1 from
select distinct (b || ' ' || c || ' ' || j || ' ' || o ) from
( select * from VNA1P005 j1
right join VNA1P005 j2
on j1.C2 = j2.C2
) dt2 (i,j,k,l,m,n,o,p)
right join
( select * from VNA1P005 
natural join VNA1P005 t 
) dt1 (a,b,c,d)
on 1=1
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s13')
    #
    # ---------------------------
    #      Id: JT.214      NATURAL JOIN/RIGHT JOIN combinations.
    # ---------------------------
    stmt = """prepare s1 from
select distinct (b || ' ' || c || ' ' || j || ' ' || o ) from
( select * from VNA1P005 
natural join VNA1P005 t 
) dt1  (a,b,c,d)
right join
( select * from VNA1P005 j1
right join VNA1P005 j2
on j1.C2 = j2.C2
) dt2 (i,j,k,l,m,n,o,p)
on (n <> k) or (p <> k) or (o <> k)
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s14')
    
    _testmgr.testcase_end(desc)

def test004(desc="""a04"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =============== --- Begin Test Case Header  ==================
    #
    #  Test case name:     T1103:A04
    #  Description:        SQL JOIN on grouped views, Row Value
    #                      constructors, and derived tables.
    #
    # ================= ---End Test Case Header  ===================
    # ----------------------------
    #  Check contents of interesting views.
    # ----------------------------
    #  UNION view.
    #  Expect 5 rows.
    
    stmt = """select  v1.varchar0_500
, v1.ubin1_20
, v1.char2_2
, v1.sdec2_500
, v1.char3_4
, v1.char5_n20
from VNA1P008 v1
order by 1,2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s0')
    #
    #  JOIN view.
    #  Expect 6 rows.
    stmt = """select * from VNA1P005 
order by 1,3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s1')
    #
    # ----------------------------
    #       Id: OR.081      Orthogonality: implicit join (cross product) of UNION view.
    # ----------------------------
    #
    #  Expect 25 rows.
    stmt = """select count(*)
from VNA1P008 v1
, VNA1P008 v2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s2')
    #
    #  Expect 25 rows.
    stmt = """select v1.varchar0_500
, v1.ubin1_20
, v1.char2_2
, v2.sdec2_500
, v2.char5_n20
from VNA1P008 v1
, ( select * from VNA1P008) v2
order by 1,2, SDEC2_500
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s3')
    #
    # ----------------------------
    #       Id: OR.082      Orthogonality: UNION view column(s) in INNER join of UNION view.
    # ----------------------------
    #
    #  Expect 8 rows (2 joined on 'AA' and 6(=2*3) joined on 'BA')
    stmt = """select v1.varchar0_500
, v1.ubin1_20
, v1.char2_2
, v2.sdec2_500
, v2.char3_4
, v2.char5_n20
from VNA1P008 v1
inner join VNA1P008 v2
on v1.char2_2 || 'AAAAAA' = v2.char3_4
order by varchar0_500, sdec2_500
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s4')
    #
    #  Expect 8 rows (2 joined on 'AA' and 6(=2*3) joined on 'BA')
    stmt = """select v1.varchar0_500
, v1.ubin1_20
, v1.char2_2
, v2.c2
, v2.c3
, v2.c4
from VNA1P008 v1
inner join VNA1P005 v2
on v1.char2_2 = v2.c2
where v1.char2_2 = v2.c2
order by varchar0_500, sdec2_500
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s5')
    #
    # ----------------------------
    #       Id: OR.083      Orthogonality: UNION view column(s) in Left and Right side of RIGHT OUTER JOIN.
    # ----------------------------
    #
    #  Expect 10 rows (2*1 'AA' and 3*2 'BA' and 2 null-extended rows
    #  for 'CA...' and 'DA...').
    stmt = """select v1.varchar0_500
, v1.ubin1_20
, v1.char2_2
, v2.sdec2_500
, v2.char3_4
, v2.char5_n20
from VNA1P008 v1
right outer join VNA1P008 v2
on v1.char2_2 || 'AAAAAA' = v2.char3_4
order by varchar0_500, sdec2_500
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s6')
    #
    #  Expect 8 rows because WHERE clasue removes non-nulls.
    stmt = """select v1.varchar0_500
, v1.ubin1_20
, v1.char2_2
, v2.c2
, v2.c3
, v2.c4
from VNA1P008 v1
right outer join VNA1P005 v2
on v1.char2_2 = v2.c2
where v1.char2_2 = v2.c2
order by varchar0_500, c2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s7')
    #
    # Expect 0 rows.
    
    stmt = """select v1.varchar0_500
, v1.ubin1_20
, v1.char2_2
, v2.c2
, v2.c3
, v2.c4
from VNA1P008 v1
right outer join VNA1P005 v2
on v1.char3_4 = v2.c2
where v1.char3_4 = v2.c2
order by varchar0_500, c2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    #
    # ----------------------------
    #       Id: OR.084      Orthogonality: UNION view column(s) in Right side of LEFT JOIN.
    # ----------------------------
    #
    #  Expect 8 rows.
    stmt = """select v1.varchar0_500
, v1.ubin1_20
, v1.char2_2
, v2.sdec2_500
, v2.char3_4
, v2.char5_n20
from VNA1P008 v1
left outer join VNA1P008 v2
on v1.char2_2 || 'AAAAAA' = v2.char3_4
order by varchar0_500, v2.sdec2_500
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s8')
    #
    #  Scaffolding.
    stmt = """select v1.c2
, v1.c3
, v1.c4
from VNA1P005 v1
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s9')
    stmt = """select v2.char2_2
, v2.sdec2_500
, v2.char3_4
, v2.char5_n20
from VNA1P008 v2
order by v2.sdec2_500, v2.sdec2_500
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s10')
    #
    #  Expect 12 rows.
    stmt = """select v1.c2
, v1.c3
, v1.c4
, v2.char2_2
, v2.sdec2_500
, v2.char3_4
, v2.char5_n20
from VNA1P005 v1
left outer join VNA1P008 v2
on v1.c3 =v2.char2_2
order by 1, v2.char2_2, v2.sdec2_500
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s11')
    #
    # ----------------------------
    #       Id: OR.086      Orthogonality: GROUP BY on UNION view column(s).
    # ----------------------------
    #
    #  Scaffold: Expect 10?rows.
    stmt = """select v1.varchar0_500
, v2.char3_4
from VNA1P008 v1
right outer join VNA1P008 v2
on v1.char2_2 || 'AAAAAA' = v2.char3_4
order by 1,2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s12')
    #
    #  Expect ?? rows. <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    stmt = """select v1.varchar0_500
, v2.char3_4
from VNA1P008 v1
right outer join VNA1P008 v2
on v1.char2_2 || 'AAAAAA' = v2.char3_4
group by v1.varchar0_500
, v2.char3_4
order by 1,2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s13')
    #
    #  Omit if above is good.
    #  Expect 10 rows.
    stmt = """select v1.varchar0_500
, v1.ubin1_20
, v1.char2_2
, v2.sdec2_500
, v2.char3_4
, v2.char5_n20
from VNA1P008 v1
right outer join VNA1P008 v2
on v1.char2_2 || 'AAAAAA' = v2.char3_4
group by v1.char2_2 , v2.char5_n20
, v1.varchar0_500
, v1.ubin1_20
, v2.sdec2_500
, v2.char3_4
order by varchar0_500, v2.sdec2_500
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s14')
    #
    # ----------------------------
    #       Id: OR.087      Orthogonality: HAVING on UNION view column(s).
    # ----------------------------
    #
    #  Expect 10 rows.
    stmt = """select v1.char2_2
, v2.char3_4
, v2.char5_n20
from VNA1P008 v1
right outer join VNA1P008 v2
on v1.char2_2 || 'AAAAAA' = v2.char3_4
order by 1,2,3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s15')
    #
    #  Expect 1 row.
    stmt = """select v1.char2_2
, v2.char3_4
, v2.char5_n20
from VNA1P008 v1
right outer join VNA1P008 v2
on v1.char2_2 || 'AAAAAA' = v2.char3_4
group by v1.char2_2 , v2.char5_n20 , v2.char3_4
having v1.char2_2 || 'AAAAAA' > v2.char5_n20
order by 1,2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s16')
    #
    # ----------------------------
    #       Id: OR.088      Orthogonality: An aggregate function on a UNION view column.
    # ----------------------------
    #
    #  Expect 1 row.
    stmt = """select max(v1.varchar0_500)
, min(v1.ubin1_20)
, count(v2.varchar0_500)
, sum(v2.sdec2_500)
, min(v2.char3_4)
from VNA1P008 v1
right outer join VNA1P008 v2
on v1.char2_2 || 'AAAAAA' = v2.char3_4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s17')
    #
    #  Expect 4 rows.
    stmt = """select max(v1.varchar0_500)
, min(v1.ubin1_20)
, count(v2.varchar0_500)
, sum(v2.sdec2_500)
, min(v2.char3_4)
from VNA1P008 v1
right outer join VNA1P008 v2
on v1.char2_2 || 'AAAAAA' = v2.char3_4
group by v1.char2_2 , v2.char3_4
order by 1,2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s18')
    
    _testmgr.testcase_end(desc)

def test005(desc="""a05"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =============== --- Begin Test Case Header  ==================
    #
    # Test case name:      T1103:A05
    # Description:         This test verifies SQL JOIN via SELECT.
    #                      Also some tests for RVC (Row Value Constructor).
    #
    # ================= ---End Test Case Header  ===================
    # ----------------------------
    #  Check contents of interesting view.
    # ----------------------------
    #  Expect 5 rows of our global view.
    
    stmt = """select VCH7, NINT, CH3, NNUM9, CH4, NNUM5
from TJOIN t1
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s0')
    #
    # ----------------------------
    #       Id: JT.019      Correlated subquery contains NATURAL RIGHT JOIN.
    # ----------------------------
    #  Expect 2 row(s) {(1,cc),(2,cc)}.
    stmt = """select n2,
( select vch7 from TJOIN t1
natural right join TJOIN t2
where nint=2 )
from TJOIN2 t3
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s1')
    #
    #  Correlated subquery.
    #  Expect 2 row(s) {(1,a),(2,cc)}.
    stmt = """select n2,
( select vch7 from TJOIN t1
natural right join TJOIN t2
where nint=t3.n2 )
from TJOIN2 t3
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s2')
    #
    # ----------------------------
    #       Id: JT.020      NATURAL RIGHT JOIN Table contains correlated subquery
    # ----------------------------
    #  Expect (('cc'))
    stmt = """select
( select t2.vch7 from TJOIN2 t3
where t2.vch7 = t3.v1 and 'cc'=t3.v1)
from TJOIN t2
where t2.nint = 2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s3')
    #
    #  Expect 5 rows from TJOIN, each with 'cc' from subquery.
    stmt = """select t2_vch7, vch7, nint from
( select
( select t2.vch7 from TJOIN2 t3
where t2.vch7 = t3.v1 and 'cc'=t3.v1
)
from TJOIN t2 where t2.nint = 2
) dt (t2_vch7)
natural right join TJOIN t1
order by 1, nint
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s4')
    #
    #  Expect 2 rows from TJOIN2, each with 'cc' from subquery.
    stmt = """select TJOIN_vch7, V1, N2, C3, N4, C5, N6 from
( select
( select t2.vch7 from TJOIN2 t3
where t2.vch7 = t3.v1 and 'cc'=t3.v1
) as TJOIN_vch7
from TJOIN t2 where t2.nint = 2
) dt
natural right join TJOIN2 t1
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s5')
    #
    # ----------------------------
    #       Id: JT.032a     Only one (of several) rows has same values in matching columns.
    # ----------------------------
    #
    stmt = """select * from TJOIN a
natural join
( select * from TJOIN 
where nint = 3
) dt (VCH7,NINT,CH3,NNUM9,CH4,NNUM5,VCH5,NSINT)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s6')
    #
    # Inner join on 2 tables:
    
    stmt = """select * from
( select v1, n2 from TJOIN2 
where n2 = 3
) dt
inner join
( select VCH7, NINT from TJOIN 
) dt2
on (1=1)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    # Natural join on 2 tables:
    stmt = """select * from
( select v1, n2 from TJOIN2 
where n2 = 3
) dt
natural join
( select VCH7, NINT from TJOIN 
) dt2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    # Natural left join on 2 tables:
    stmt = """select * from
( select v1, n2 from TJOIN2 
where n2 = 3
) dt
natural left join
( select VCH7, NINT from TJOIN 
) dt2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    #  Natural right join on 2 tables:
    stmt = """select * from
( select v1, n2 from TJOIN2 
where n2 = 3
) dt
natural right join
( select VCH7, NINT from TJOIN 
) dt2
order by vch7, nint
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s7')
    #
    # ----------------------------
    #  NATURAL [INNER] JOIN ( [USING] is illegal); JOIN Table to different table.
    # ----------------------------
    #       Id: JT.028      Only one (of several) column names the same.
    #       Id: JT.029      A few (of several) column names the same.
    # ----------------------------
    #
    #  Basic data for NATURAL JOIN on global view:
    #  Should show 6 rows as in view.
    stmt = """select UBIN2_4, CHAR2_2, UDEC2_100
from VUA1P001 
natural join VUA1P001 v
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s8')
    #
    #  Expect 36 (=6*6) rows with value ('CA').
    stmt = """select CHAR11_4 from BTA1P001 
natural join
(select CHAR11_4 from BTA1P001) dt
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s9')
    #
    #  Expect 6 rows with value ('CA').
    stmt = """select CHAR11_4 from BTA1P001 
natural join TJOIN4 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s10')
    #
    stmt = """select VARCHAR5_10
from BTA1P001 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s11')
    stmt = """select VARCHAR5_10
from TJOIN4 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s12')
    stmt = """select VARCHAR5_10
from BTA1P001 
natural join TJOIN4 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s13')
    stmt = """select VARCHAR5_10 ,SDEC5_100 ,UDEC6_500 ,CHAR6_20 ,UBIN6_2 ,SBIN7_2
from BTA1P001 
natural join TJOIN4 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s14')
    #
    #  Basics.
    stmt = """select CHAR11_4 from BTA1P001 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s15')
    stmt = """select CHAR11_4 from BTA1P002 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s16')
    stmt = """select CHAR11_4 from BTA1P003 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s17')
    stmt = """select CHAR11_4 from BTA1P004 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s18')
    #
    #  Expect 1 row matching (('CA')).
    stmt = """select *
from (select CHAR11_4 from BTA1P003) d3
natural join
(select CHAR11_4 from BTA1P004) d4
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s19')
    #
    #  Expect 3 rows matching (('CA')).
    stmt = """select *
from (select CHAR11_4 from BTA1P003) d3
natural join
(select CHAR11_4 from BTA1P002) d2
natural join
(select CHAR11_4 from BTA1P004) d4
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s20')
    #
    #  Expect 18 (=6*3*1*1) rows matching (('CA')).
    stmt = """select *
from (select CHAR11_4 from BTA1P003) d3
natural join
(select CHAR11_4 from BTA1P001) d1
natural join
(select CHAR11_4 from BTA1P002) d2
natural join
(select CHAR11_4 from BTA1P004) d4
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s21')
    #
    # ----------------------------
    #  Basic NATURAL JOIN-- View to different view.
    # ----------------------------
    #
    stmt = """select UDEC9_10 from VUA1P001 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s22')
    stmt = """select UDEC9_10 from VUA1P003 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s23')
    #
    #  Should show 1 row ((9)).
    stmt = """select *
from (select UDEC9_10 from VUA1P001) d1
natural join
(select UDEC9_10 from VUA1P003) d3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s24')
    #
    # ----------------------------
    #  Basic NATURAL JOIN of Table to View.
    # ----------------------------
    #  Expect 6 rows.
    stmt = """select VARCHAR0_4 from BTA1P001 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s25')
    #  Expect 7 rows.
    stmt = """select VARCHAR0_4 from BTA1P002 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s26')
    #  Expect 13 rows.
    stmt = """select VARCHAR0_4 from BTA1P004 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s27')
    #  Expect 6 rows.
    stmt = """select VARCHAR0_4 from VUA1P001 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s28')
    #
    # Should show 0 rows (none of full rows match completely).
    stmt = """select VARCHAR0_4 from
(select t.varchar0_4 from BTA1P001 t) t1
natural join
(select t.varchar0_4 from BTA1P002 t) t2
natural join
(select t.varchar0_4 from BTA1P004 t) t3
natural join
(select t.varchar0_4 from VUA1P001 t) t4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    #  Expect ((108)) (=3*6*6).
    stmt = """select count(VARCHAR0_4) from
(select t.varchar0_4 from BTA1P001 t) t1
natural join
(select t.varchar0_4 from BTA1P002 t) t2
natural join
(select t.varchar0_4 from VUA1P001 t) t3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s29')
    #  Expect 18 (=3*6) rows.
    stmt = """select VARCHAR0_4 from
(select t.varchar0_4 from BTA1P001 t) t1
natural join
(select t.varchar0_4 from BTA1P002 t) t2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s30')
    stmt = """select VARCHAR0_4 from
(select t.varchar0_4 from BTA1P001 t) t1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s31')
    #
    # ----------------------------
    #  Id: JT.032b   A few (of several) rows have same values in matching columns.
    # ----------------------------
    #
    #  Preliminary check.
    stmt = """select * from TJOIN t1
natural join TJOIN t2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s32')
    #
    #  Expect 3 rows.
    stmt = """select *
from (select * from TJOIN where nint < 5) dt
natural join
(select * from TJOIN where nint > 1) dt2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s33')
    #
    # ---------------------------
    #      Id: JT.032d     No row values match.
    # ---------------------------
    stmt = """select *
from (select * from TJOIN where nint > 3) dt
natural join
(select * from TJOIN where nint < 3) dt2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    #
    stmt = """select *
from TJOIN 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s34')
    stmt = """select *
from TJOINNUL 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s35')
    stmt = """select *
from TJOIN 
natural join TJOINNUL 
order by vch7, nint, v1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s36')
    
    _testmgr.testcase_end(desc)

def test006(desc="""a06"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =============== --- Begin Test Case Header  ==================
    #
    #  Test case name:     T1103:A06
    #  Description:        SQL JOIN on grouped views, Row Value
    #                      constructors, and derived tables.
    #
    # ================= ---End Test Case Header  ===================
    # ----------------------------
    #  Tables created in preparation for test unit.
    # ----------------------------
    #
    #  Preliminary review of contents of views.
    
    stmt = """select * from VNA1P005 t1
order by n1, c3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s0')
    #
    # ----------------------------
    #       Id: JT.273      Within ON clause of JOIN, RVC contains Columns.
    #       Id: JT.274      Within ON clause of JOIN, RVC is a list containing literals.
    # ----------------------------
    #  Expect 8 rows (4 like inner join plus 4 null-augmented).
    stmt = """select t1.n1 as LHSn1, t1.c2 as LHSc2, t1.c3 as LHSc3
, t2.* from VNA1P005 t1
right join VNA1P005 t2
ON (t1.c2, t2.c2, 'AA', t2.c3 ) = ('BA','BA', t1.c3, 'AA')
order by t2.c3, t2.n1, t1.n1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s1')
    #  Expect 4 rows.
    stmt = """select t1.n1 as LHSn1, t1.c2 as LHSc2, t1.c3 as LHSc3
, t2.* from VNA1P005 t1
inner join VNA1P005 t2
ON (t1.c2, t2.c2, 'AA', t2.c3 ) = ('BA','BA', t1.c3, 'AA')
order by t2.c3, t2.n1, t1.n1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s2')
    #
    # ---------------------------
    #      Id: JT.092b     RIGHT JOIN of Grouped Views and Derived
    #                      Tables: Add parameters in ON clause.
    #      Id: JT.275      Within ON clause of JOIN, RVC contains parameters
    #                      e.g. ON (t1.col1, ?p1) = (? codep1,t2.col2);
    # ---------------------------
    stmt = """set param ?pba 'BA' ;"""
    output = _dci.cmdexec(stmt)
    
    #  value of interest for column c2.
    stmt = """set param ?paa 'AA' ;"""
    output = _dci.cmdexec(stmt)
    #  value of interest for column c3.
    stmt = """select t1.n1 as LHSn1, t1.c2 as LHSc2, t1.c3 as LHSc3
, t2.* from VNA1P005 t1
right join VNA1P005 t2
ON (t1.c2, t2.c2, 'AA', t2.c3 ) = ('BA','BA', t1.c3, ?paa)
order by t2.c3, t2.n1, t1.n1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s3')
    #  Reuse parameter, and use second parameter.
    stmt = """select t1.n1 as LHSn1, t1.c2 as LHSc2, t1.c3 as LHSc3
, t2.* from VNA1P005 t1
right join VNA1P005 t2
ON (t1.c2, t2.c2, ?paa, t2.c3 ) = ( ?pba,'BA', t1.c3, ?paa)
order by t2.c3, t2.n1, t1.n1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s4')
    #
    # ----------------------------
    #       Id: JT.276      Within ON clause of JOIN, RVC containing single-valued subquery,
    #                       e.g., SELECT COUNT (*) FROM t2 LEFT JOIN t3
    #                                 ON (t2.a) = (subquery of 1 column) ;
    #  Expect 36 (6*6) rows:
    stmt = """select t1.c2 as t1c2, t2.c2 as t2c2
from VNA1P005 t1
right join VNA1P005 t2
ON (1 = 1)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s5')
    #
    #  Expect 16 rows: 12 (2*6) with t2.c2='BA' plus 4 null-extended rows
    #  without 'BA' in t2.c2.
    stmt = """select t1.n1 as LHSn1, t1.c2 as LHSc2, t1.c3 as LHSc3
, t2.* from VNA1P005 t1
right join VNA1P005 t2
ON (t2.c2 ) = ( select max ('BA') from VNA1P005 )
order by t2.c3, t2.n1, t1.c3, t1.n1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s6')
    
    _testmgr.testcase_end(desc)

def test007(desc="""a07"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =============== --- Begin Test Case Header  ==================
    #
    #  Test case name:     T1103:A07
    #  Description:        SQL JOIN on grouped views, Row Value
    #                      constructors, and derived tables.
    #
    # ================= ---End Test Case Header  ===================
    #
    # ----------------------------
    #  Tables created in preparation for test unit.
    # ----------------------------
    #
    # ----------------------------
    #  Check contents of interesting view.
    # ----------------------------
    #
    
    stmt = """select min(VARCHAR15_UNIQ), max(CHAR13_100)
from BTA1P001 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s0')
    #
    stmt = """select UDEC17_100, CHAR17_100
from VNA1P002 
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s1')
    #
    stmt = """select UBIN15_UNIQ , SDEC15_10 , SBIN16_20
, UBIN16_1000 , SBIN17_UNIQ , SDEC17_20
from VUA1P003 
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s2')
    #
    #  Expect 6 rows of our global view.
    stmt = """select *
from VNA1P005 t1
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s3')
    #
    # ----------------------------
    #       Id: JT.182      JOIN contained in DTs within Subquery within Select list
    #                       Should get -2789, repeated for the number of rows ( )
    #                       in the table in the main query -- for which
    #                       we use the view again.
    # ----------------------------
    stmt = """select N1 from VNA1P005 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s4')
    stmt = """select min(VARCHAR15_UNIQ), max(CHAR13_100)
from BTA1P001 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s5')
    #  Expect (-2389).
    stmt = """select distinct
( select max(N1) from
( select N1, C2, C3, C4
from VNA1P005 
) t2
) from VNA1P005 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s6')
    #  Expect (-2389).
    stmt = """select max(N1) from
( select N1, C2, C3, C4
from VNA1P005 
) t2
right join
( select min(VARCHAR15_UNIQ), max(CHAR13_100)
from BTA1P001 
) t1(a,b)
on 1=1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s7')
    #  Expect (-2389).
    stmt = """select distinct
( select max(N1) from
( select N1, C2, C3, C4
from VNA1P005 
) t2
right join
( select min(VARCHAR15_UNIQ), max(CHAR13_100)
from BTA1P001 
) t1(a,b)
on 1=1
)
from VNA1P005 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s8')
    #
    #  Query of interest.
    #  Expect (-2389).
    stmt = """select distinct
( select N1 from
( select N1, C2, C3, C4
from VNA1P005 
) t2
right join
( select min(VARCHAR15_UNIQ), max(CHAR13_100)
from BTA1P001 
) t1(a,b)
on 1=1
where lower(t2.C2) <> upper(t1.a) and C4 is NULL
)
from VNA1P005 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s9')
    #
    # ----------------------------
    #       Id: JT.183      JOIN contained in DTs within Subquery within WHERE clause
    #       Id: GV.041      Join of one Grouped view to another, in the right tree of a LEFT JOIN.
    # ----------------------------
    #  TG:  GROUP BY (VNA1P002)
    #  TAGH:aggregates, GROUP BY, HAVING (e.g., VNA1P005).
    # ----------------------------
    #
    #  Subquery.
    stmt = """select N1 from
( select N1, C2, C3, C4, UDEC17_100, CHAR17_100
from VNA1P005 
right join VNA1P002 
on ( UDEC17_100 > 70 )
where udec17_100 < 80
) t1
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s10')
    stmt = """select * from
( select * from
( select N1, C2, C3, C4, UDEC17_100, CHAR17_100
from VNA1P005 
right join VNA1P002 
on ( UDEC17_100 > 70 )
where udec17_100 < 80
) t1
) dt
order by 1, 3, 5
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s11')
    #
    stmt = """select * from VNA1P005 touter
where touter.N1 <
( select max(N1) from
( select N1, C2, C3, C4, UDEC17_100, CHAR17_100
from VNA1P005 
right join VNA1P002 
on ( UDEC17_100 > 70 )
where udec17_100 < 80
) t1
)
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s12')
    #
    # ----------------------------
    #       Id: JT.184      JOIN contained in DTs within Subquery within ON clause
    #       Id: GV.042      Join of one Grouped view (in the right tree of a LEFT JOIN) to a non-Grouped view.
    # ----------------------------
    #  TG:  GROUP BY (VNA1P002)
    #   (VUA1P003)
    # ----------------------------
    stmt = """select count(*) from VNA1P002;"""
    output = _dci.cmdexec(stmt)
    stmt = """select count(*) from BTA1P003;"""
    output = _dci.cmdexec(stmt)
    stmt = """select cast(t3.UBIN15_UNIQ/t2.UDEC17_100 as pic 9999V99) as a
, cast(t3.SDEC15_10/t2.UDEC17_100      as pic 9V9999 ) as b
, cast(t3.SBIN16_20/t2.UDEC17_100      as pic 9V9999 ) as c
, cast(t3.UBIN16_1000/t2.UDEC17_100    as pic 9V9999 ) as d
, cast(t3.SBIN17_UNIQ/t2.UDEC17_100    as pic 9999V99) as e
, cast(t3.SDEC17_20/t2.UDEC17_100      as pic 9999V99) as f
from VNA1P002 t2
, BTA1P003 t3
order by 1, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s13')
    #
    stmt = """select t2.UDEC17_100, t3.UBIN16_1000
from VNA1P002 t2
left join BTA1P003 t3
on (1=1)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s14')
    #
    # ----------------------------
    #       Id: GV.043      Join of one Grouped view (in the right tree of a LEFT JOIN) to base table.
    # ----------------------------
    #  TG:  GROUP BY (VNA1P002)
    #   (BTA1P003)
    # ----------------------------
    stmt = """select UBIN15_UNIQ , SDEC15_10 , SBIN16_20
from BTA1P003 
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s15')
    #
    stmt = """select UBIN16_1000 , SBIN17_UNIQ , SDEC17_20
from BTA1P003 
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s16')
    #
    stmt = """select t2.UDEC17_100
, t3.UBIN15_UNIQ , t3.SDEC15_10 , t3.SBIN16_20
, t3.UBIN16_1000 , t3.SBIN17_UNIQ , t3.SDEC17_20    

from VNA1P002 t2
left join BTA1P003 t3
on (1=1)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s17')
    #
    # ----------------------------
    #       Id: JT.???      NATURAL JOIN on joined table without aggregates.
    #       Id: JT.186a     Derived Table contains RIGHT JOIN
    #       Id: JT.186b     Derived Table contains RIGHT JOIN with GROUP BY.
    # ----------------------------
    #
    stmt = """select distinct
( select N1 from
( select N1, C2, C3, C4
from VNA1P005 
) t2
right join
( select min(VARCHAR15_UNIQ), max(CHAR13_100)
from BTA1P001 
) t1(a,b)
on 1=1
where lower(t2.C2) <> upper(t1.a) and C4 is NULL
)
from VNA1P005 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s18')
    #
    #  Values ... ???
    stmt = """select * from
( select t1.sbinneg15_nuniq , t1.char2_2 , t3.char3_4
from BTA1P005 t1
right join BTA1P005 t2 on t1.char2_2 = t2.char3_4
left  join BTA1P005 t3 on t2.char2_2 = t3.char3_4
) dt
natural join
( select t1.char2_2
from BTA1P005 t1
right join BTA1P005 t2 on t1.char2_2 = t2.char3_4
left  join BTA1P005 t3 on t2.char2_2 = t3.char3_4
group by t1.char2_2, t2.char3_4
) dt2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s19')
    #
    #  Values ... ???
    stmt = """select * from
( select t1.sbinneg15_nuniq , t1.char2_2 -- , t3.char3_4
from BTA1P005 t1
right join BTA1P005 t2 on t1.char2_2 = t2.char3_4
) dt
natural join
( select t1.char2_2
from BTA1P005 t1
right join BTA1P005 t2 on t1.char2_2 = t2.char3_4
left  join BTA1P005 t3 on t2.char2_2 = t3.char3_4
) dt2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s20')
    #
    #  Omitting BOTH left joins => 49 rows (ok?)
    stmt = """select * from
( select t1.sbinneg15_nuniq , t1.char2_2 -- , t3.char3_4
from BTA1P005 t1
right join BTA1P005 t2 on t1.char2_2 = t2.char3_4
) dt
natural join
( select t1.char2_2
from BTA1P005 t1
right join BTA1P005 t2 on t1.char2_2 = t2.char3_4
) dt2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s21')
    #
    #  Omitting BOTH joins from RHS of LJ => 72 rows (ok?)
    stmt = """select * from
( select t1.sbinneg15_nuniq -- , t1.char2_2 , t3.char3_4
from BTA1P005 t1
) dt
natural join
( select t1.char2_2
from BTA1P005 t1
right join BTA1P005 t2 on t1.char2_2 = t2.char3_4
left  join BTA1P005 t3 on t2.char2_2 = t3.char3_4
) dt2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s22')
    
    _testmgr.testcase_end(desc)

def test008(desc="""a08"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =============== --- Begin Test Case Header  ==================
    #
    #  Test case name:     T1103:A08
    #  Description:        SQL JOIN on grouped views, Row Value
    #                      constructors, and derived tables.
    #
    # ================= ---End Test Case Header  ===================
    #
    # ----------------------------
    #  Tables created in preparation for test unit.
    # ----------------------------
    #
    
    stmt = """select t1.sbin16_20, t1.varchar5_10
from BTA1P001 t1
order by 1,2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s0')
    #
    #  Access UNION view, VNA1P008.
    stmt = """select varchar0_500, CHAR4_N10, CHAR5_N20, char6_n100
from BTA1P008 
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s1')
    stmt = """select varchar0_500, CHAR4_N10, CHAR5_N20, char6_n100
from VNA1P008 
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s2')
    #
    stmt = """select * from VNA1P005 
order by 1,3 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s3')
    #
    stmt = """select * from VNA1P006 
order by 1,2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s4')
    #
    # ----------------------------
    #       Id: JT.061      Joins with UNION as left or right child of a RIGHT join.
    # ----------------------------
    #
    #  VNA1P008 is Union view; VNA1P005 is Grouped view.
    #
    #  SELECT * FROM (union view)
    #  RIGHT JOIN Table2
    #  ON <expression> ;
    #
    stmt = """SELECT count(*) FROM VNA1P008 t8
RIGHT JOIN BTA1P005 t5
ON t8.varchar0_500 = t5.char17_2
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s5')
    #
    #  SELECT * FROM Table1
    #  RIGHT JOIN (union view)
    #  ON <expression> ;
    #
    stmt = """SELECT count(*) FROM BTA1P005 t5
RIGHT JOIN VNA1P008 t8
ON t8.varchar0_500 = t5.char17_2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s6')
    #
    #  SELECT * FROM (union view or derived table that is a UNION)
    #  RIGHT JOIN (union view or derived table that is another UNION)
    #  ON <expression> ;
    stmt = """SELECT count(*) FROM VNA1P008 t1
RIGHT JOIN VNA1P008 t2
ON t1.varchar0_500 = t2.varchar0_500
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s7')
    stmt = """SELECT count(*) FROM VNA1P008 t1
RIGHT JOIN VNA1P008 t2
ON t1.CHAR4_N10 = t2.CHAR5_N20
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s8')
    #
    stmt = """select c2 FROM VNA1P005 t2
UNION ALL
select C3 FROM VNA1P005 t3
UNION ALL
select C4 FROM VNA1P005 t4
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s9')
    #
    stmt = """select c2 FROM VNA1P005 t2
UNION
select C3 FROM VNA1P005 t3
UNION
select C4 FROM VNA1P005 t4
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s10')
    #
    stmt = """SELECT count(*) FROM
(
select c2 FROM VNA1P005 t2
UNION ALL
select C3 FROM VNA1P005 t3
UNION ALL
select C4 FROM VNA1P005 t4
) tleft
RIGHT JOIN
(
select c2 FROM VNA1P005 t2
UNION
select C3 FROM VNA1P005 t3
UNION
select C4 FROM VNA1P005 t4
) tright
ON tleft.C2 = tright.C2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s11')
    #
    # ----------------------------
    #       Id: JT.062      Joins with Group By as left or right child of a RIGHT join.
    #  See ../arkt1100/testA02 for Grouped View test #021
    #  (Outer Join on Grouped View (GROUP BY and aggregates) )
    #
    #  Also see ../arkt1103/testA07 for Grouped View test #041
    #  (Join of one Grouped view to another, in the right tree of a LEFT JOIN.)
    # ----------------------------
    #
    #  SELECT * FROM (Grouped View)
    #  RIGHT JOIN Table2
    #  ON <expression> ;
    #
    stmt = """SELECT count(*) FROM VNA1P005 t1
RIGHT JOIN BTA1P005 t2
ON t1.C2 = t2.CHAR5_N20
OR t1.C3 = t2.CHAR5_N20
OR t1.C4 = t2.CHAR5_N20
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s12')
    #
    #  SELECT * FROM Table1
    #  RIGHT JOIN (Grouped View)
    #  ON <expression> ;
    #
    stmt = """SELECT count(*) FROM BTA1P005 t1
RIGHT JOIN VNA1P005 t2
ON t2.C2 = t1.CHAR5_N20
OR t2.C3 = t1.CHAR5_N20
OR t2.C4 = t1.CHAR5_N20
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s13')
    #
    #  SELECT * FROM (Grouped View)
    #  RIGHT JOIN (Grouped View)
    #  ON <expression> ;
    #
    stmt = """SELECT count(*) FROM VNA1P005 t1
RIGHT JOIN VNA1P005 t2
ON t1.C2 = t2.C3
OR t1.C3 = t2.C3
OR t1.C4 = t2.C3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s14')
    #
    stmt = """SELECT count(*) FROM VNA1P005 t1
RIGHT JOIN VNA1P005 t2
ON t1.C3 = t2.C2
OR t1.C3 = t2.C3
OR t1.C3 = t2.C4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s15')
    #
    # ----------------------------
    #       Id: JT.063      Joins with UNION as left or right child of a NATURAL join.
    # ----------------------------
    #
    #  BTA1P008 is Union view; VNA1P005 is Grouped view.
    #
    #  SELECT * FROM (union view)
    #  NATURAL JOIN Table2 ;
    #
    stmt = """SELECT count(*) FROM VNA1P008 t8
NATURAL JOIN BTA1P005 t5
Order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s16')
    #
    #  SELECT * FROM Table1
    #  NATURAL JOIN (union view) ;
    #
    stmt = """SELECT count(*) FROM
( select char17_2 from BTA1P005) t5(xyz)
NATURAL JOIN
( select varchar0_500 from BTA1P008) t8(xyz)
Order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s17')
    #
    #  SELECT * FROM (union view or derived table that is a UNION)
    #  NATURAL JOIN (union view or derived table that is another UNION) ;
    stmt = """SELECT count(*) FROM VNA1P008 t1
NATURAL JOIN VNA1P008 t2
Order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s18')
    #
    stmt = """select c2 FROM VNA1P005 t2
UNION ALL
select C3 FROM VNA1P005 t3
UNION ALL
select C4 FROM VNA1P005 t4
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s19')
    #
    stmt = """select c2 FROM VNA1P005 t2
UNION
select C3 FROM VNA1P005 t3
UNION
select C4 FROM VNA1P005 t4
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s20')
    #
    stmt = """SELECT count(*) FROM
( select c2 FROM VNA1P005 t2
UNION ALL
select C3 FROM VNA1P005 t3
) tleft
NATURAL JOIN
( select c2 FROM VNA1P005 t2
UNION
select C4 FROM VNA1P005 t4
) tright
Order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s21')
    #
    stmt = """SELECT count(*) FROM
( select c2 FROM VNA1P005 t2
UNION ALL
select C3 FROM VNA1P005 t3
UNION ALL
select C4 FROM VNA1P005 t4
) tleft
NATURAL JOIN
( select c2 FROM VNA1P005 t2
UNION
select C3 FROM VNA1P005 t3
UNION
select C4 FROM VNA1P005 t4
) tright
Order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s22')
    #
    # ----------------------------
    #       Id: JT.064      Joins with Group By as left or right child of a NATURAL join.
    #  See ../arkt1103/testA01/testA02 for Join test #185b
    #  (Derived table contains NATURAL join with GROUP BY.)
    # ----------------------------
    #
    #  SELECT * FROM (Grouped View)
    #  NATURAL JOIN Table2 ;
    #
    stmt = """SELECT count(*) FROM VNA1P005 t1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s23')
    stmt = """SELECT count(*) FROM BTA1P005 t1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s24')
    
    stmt = """SELECT count(*) FROM VNA1P005 t1
NATURAL JOIN BTA1P005 t2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s25')
    stmt = """SELECT count(*) FROM VNA1P005 t1
NATURAL JOIN BTA1P005 t2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s26')
    #
    #  SELECT * FROM Table1
    #  NATURAL JOIN (Grouped View) ;
    #
    stmt = """SELECT count(*) FROM BTA1P005 t1
NATURAL JOIN VNA1P005 t2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s27')
    #
    #  SELECT * FROM (Grouped View)
    #  NATURAL JOIN (Grouped View) ;
    #
    stmt = """SELECT c2 , c3 , c4 FROM VNA1P005 t1
NATURAL JOIN VNA1P005 t2
Order by c2 , c3 , c4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s28')
    #
    stmt = """SELECT c3 FROM VNA1P005 t1
NATURAL JOIN VNA1P005 t2
GROUP BY c3
Order by c3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s29')
    #
    stmt = """SELECT c4 FROM VNA1P005 t1
NATURAL JOIN VNA1P005 t2
GROUP BY c4
Order by c4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s30')
    
    _testmgr.testcase_end(desc)

def test009(desc="""a09"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =============== --- Begin Test Case Header  ==================
    #
    # Test case name:      T1103:A09
    # Description:         This test verifies SQL JOIN via SELECT.
    #                      It focuses on NATURAL RIGHT JOIN and N.R. OUTER JOIN.
    #
    # ================= ---End Test Case Header  ===================
    #
    # ---------------------------------------
    # Specify catalog and schema globally.
    # ---------------------------------------
    #  In global database:
    #     char0_n10, sbin0_uniq is in table 5, not table 6.
    #     sbin0_4, varchar0_uniq is in table 6, not table 5.
    #     char2_2 , char3_4 , sbin4_n1000 , sbin7_n20 occur in both tables.
    #  Expect 6 rows ( ('AA' ...) ('AA' ...) ('BA' ...) ('BA' ...) ('DA' ...) ('EA' ...) )
    
    stmt = """select char2_2 , char3_4 , sbin4_n1000 , sbin7_n20, char0_n10, sbin0_uniq
from BTA1P005 
order by 1, 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s0')
    #
    #  Expect 4 rows ( ('AA' ...) ('AA' ...) ('AA' ...) ('BA' ...) )
    stmt = """select char2_2 , char3_4 , sbin4_n1000 , sbin7_n20, sbin0_4, varchar0_uniq
from BTA1P006 
order by 1, 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s1')
    #
    # ----------------------------
    #       Id: JT.016      NATURAL  RIGHT  JOIN
    # ----------------------------
    #  Expect 4 rows from BTA1P006.
    stmt = """select CHAR2_2 from BTA1P005 
natural right join BTA1P006 t 
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s2')
    #
    stmt = """select CHAR2_2 from BTA1P005 
natural right outer join BTA1P006 t 
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s3')
    #
    # Expect 0 rows, because of NULLs.
    
    stmt = """select char2_2 , char3_4
from BTA1P005 t1
natural join BTA1P005 t2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    #
    #  Expect 6 rows, as in BTA1P005.
    stmt = """select char2_2 , char3_4
from BTA1P005 t1
natural right outer join BTA1P005 t2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s4')
    #
    # ----------------------------
    #  Note: Global database grouped view (VNA1P005) contains 6 rows,
    #        including 3 with nulls.
    #       Id: JT.017      NATURAL  RIGHT  OUTER  JOIN
    #       Id: JT.200a     JOIN upon grouped view containing aggregate (VNA1P005)
    #       Id: JT.200c     JOIN upon grouped view containing HAVING (VNA1P005)
    # ----------------------------
    #
    #  Expect 6 rows (includes null values)
    stmt = """select n1, c2 from VNA1P005 
natural right outer join VNA1P005 t 
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s5')
    #
    #  Expect 6 rows (includes null values)
    stmt = """select * from VNA1P005 
natural right outer join VNA1P005 t 
order by 1, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s6')
    #
    #  Expect 3 rows (omit those with null)
    stmt = """select n1, c2 from VNA1P005 
natural join VNA1P005 t 
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s7')
    
    _testmgr.testcase_end(desc)

def test010(desc="""a10"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =============== --- Begin Test Case Header  ==================
    #
    #  Test case name:     T1103:A10
    #  Description:        SQL JOIN on grouped views, Row Value
    #                      constructors, and derived tables.
    #
    # ================= ---End Test Case Header  ===================
    #
    # ----------------------------
    #  Tables created in preparation for test unit.
    # ----------------------------
    #
    # ----------------------------
    #  Check potential aggregates, etc for derived tables.
    # ----------------------------
    
    stmt = """select  SBIN4_2, CHAR13_100, VARCHAR15_UNIQ
,SBIN16_20,UBIN16_1000,SDEC19_1000
from BTA1P001 
order by 1, 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s0')
    #
    stmt = """select  UBIN4_4, SDEC4_10, UDEC4_2, SDEC11_20
from BTA1P002 
order by 1, 2, 4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s1')
    #
    stmt = """select  CHAR15_100, CHAR17_2
from BTA1P006 
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s2')
    #
    #  aggregates (only)
    #  BTA1P001: Not null:
    stmt = """select min(SBIN4_2),     max(SBIN4_2)
, min(CHAR13_100),  max(CHAR13_100)
, min(VARCHAR15_UNIQ), max(VARCHAR15_UNIQ)
, min(SBIN16_20),   max(SBIN16_20)
, min(UBIN16_1000), max(UBIN16_1000)
, min(SDEC19_1000), max(SDEC19_1000)
from BTA1P001 
order by 1, 3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s3')
    #
    #  BTA1P002: Non-integer numerics:
    stmt = """select min( UBIN4_4), max( UBIN4_4)
, min(SDEC4_10)  , max(SDEC4_10)
, min(UDEC4_2)  , max(UDEC4_2)
, min(SDEC11_20)  , max(SDEC11_20)
from BTA1P002 
order by 1, 3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s4')
    #
    #   aggregates and GROUP BY
    stmt = """select min(SBIN4_2),     max(SBIN4_2)
, min(CHAR13_100),  max(CHAR13_100)
, min(VARCHAR15_UNIQ), max(VARCHAR15_UNIQ)
, min(SBIN16_20),   max(SBIN16_20)
, min(UBIN16_1000), max(UBIN16_1000)
, min(SDEC19_1000), max(SDEC19_1000)
from BTA1P001 
group by SBIN4_2, CHAR13_100, VARCHAR15_UNIQ
,SBIN16_20,UBIN16_1000,SDEC19_1000
order by 1, 3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s5')
    #
    #  BTA1P002: Non-integer numerics:
    stmt = """select min(UBIN4_4),  max(UBIN4_4)
, min(SDEC4_10), max(SDEC4_10)
, min(UDEC4_2),  max(UDEC4_2)
, min(SDEC11_20),max(SDEC11_20)
from BTA1P002 
group by UBIN4_4, SDEC4_10, UDEC4_2, SDEC11_20
order by 1, 3, 7;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s6')
    #
    # ----------------------------
    #  TA:  aggregates (derived tables) joined to the other grouped views
    #       in turn.
    # ----------------------------
    #  TA:  aggregates (derived tables)
    #  TG:  GROUP BY (VNA1P002)
    #  TAG: aggregates, GROUP BY (derived tables)
    #  TGH: GROUP BY and HAVING (VNA1P004)
    #  TAGH:aggregates, GROUP BY, HAVING (e.g., VNA1P005).
    #    (TA) RJ (TA2) ; (TA) RJ (TG); etc., making 25 (5*5 combinations)
    # ----------------------------
    #       Id: JT.091a     RIGHT JOIN (TA) RJ (TA2)
    # ----------------------------
    stmt = """select t1.SDEC19_1000
from BTA1P001 t1
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s7')
    stmt = """select min(t1.SDEC19_1000)
from BTA1P001 t1
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s8')
    stmt = """select t2.UBIN4_4
from BTA1P002 t2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s9')
    stmt = """select max(t2.UBIN4_4)
from BTA1P002 t2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s10')
    #
    #  (TA) RJ (TA)
    #  Expect 7 {(.3,.3) (.3,.3) 5*(Null,<value>)}
    stmt = """select t1.SDEC19_1000, t2.UBIN4_4
from BTA1P001 t1 right join BTA1P002 t2
on t1.SDEC19_1000=t2.UBIN4_4
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s11')
    #
    #  (TA) RJ (TA)
    #  Expect 42 (=6*7) rows
    stmt = """select t1.SDEC19_1000, t2.UBIN4_4
from (select t1.SDEC19_1000 from BTA1P001 t1) t1
right join
(select t2.UBIN4_4 from BTA1P002 t2 ) t2
on 1=1
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s12')
    #
    #  (TA) RJ (TA)
    #  Expect {.3,.3}
    stmt = """select *
from (select min(t1.SDEC19_1000) from BTA1P001 t1) t1
right join
(select max(t2.UBIN4_4) from BTA1P002 t2 ) t2
on 1=1
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s13')
    #
    #  (TA) RJ (TA)
    #  Expect 7 (NULL for t1 values)
    stmt = """select *
from (select t1.SDEC19_1000 from BTA1P001 t1) t1 (a)
right join
(select t2.UBIN4_4 from BTA1P002 t2 ) t2 (b)
on 1=0
order by 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s14')
    #
    #  (TA) RJ (TA)
    #  Expect {?, .3}
    stmt = """select *
from (select min(t1.SDEC19_1000) from BTA1P001 t1) t1
right join
(select max(t2.UBIN4_4) from BTA1P002 t2 ) t2
on 1=0
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s15')
    #
    # ----------------------------
    #       Id: JT.094a     INNER JOIN (TA) IJ (TA2)
    # ----------------------------
    #
    #  (TA) IJ (TA)
    #  Expect {.3,.3}
    stmt = """select *
from (select min(t1.SDEC19_1000) from BTA1P001 t1) t1
inner join
(select max(t2.UBIN4_4) from BTA1P002 t2 ) t2
on 1=1
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s16')
    #
    # (TA) IJ (TA)
    # Expect 0 rows (false ON clause means no match).
    
    stmt = """select *
from (select min(t1.SDEC19_1000) from BTA1P001 t1) t1
inner join
(select max(t2.UBIN4_4) from BTA1P002 t2 ) t2
on 1=0
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    #
    # ----------------------------
    #       Id: JT.091b     RIGHT JOIN (TA) RJ (TG)
    #       Id: JT.091f     RIGHT JOIN (TG) RJ (TA)
    #  TA:  aggregates (derived tables)
    #  TG:  GROUP BY (VNA1P002)
    # ----------------------------
    #
    #  (TA) RJ (TG)
    stmt = """select *
from (select max(UDEC4_2),max(SDEC11_20) from BTA1P001 t1 ) t1
right join
(select UDEC17_100 from BTA1P002 t2) t2
on 1=0
order by 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s17')
    #
    #  (TA) RJ (TG)
    stmt = """select *
from (select max(UDEC4_2),max(SDEC11_20) from BTA1P001 t1 ) t1
right join
(select UDEC17_100 from VNA1P002 t2) t2
on 1=0
order by 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s18')
    #
    #  (TG) RJ (TA)  Expect { ? ? 16 }
    stmt = """select *
from (select SDEC4_10,  SDEC11_20 from BTA1P001 t1) t1
right join
(select min(UDEC17_100) from VNA1P002 t2 ) t2
on 1=0
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s19')
    #
    stmt = """select min(UDEC17_100) from VNA1P002 t2 order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s20')
    stmt = """select SDEC4_10, SDEC11_20 from BTA1P001 t1 order by 1, 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s21')
    #
    #  (TG) RJ (TA)  Expect { .8 .00012 16}
    stmt = """select *
from (select SDEC4_10, SDEC11_20 from BTA1P001 t1) t1(SDEC4_10, SDEC11_20)
right join
(select min(UDEC17_100) from VNA1P002 t2 ) t2(UDEC17_100)
on t2.UDEC17_100 = t1.SDEC4_10 * 20
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s22')
    #
    # ---------------------------
    #      Id: JT.094b     INNER JOIN (TA) IJ (TG)
    #      Id: JT.094f     INNER JOIN (TG) IJ (TA)
    # ---------------------------
    #
    # (TG) IJ (TA)  Expect 0 rows (false ON clause means no match).
    stmt = """select *
from (select SDEC4_10,  SDEC11_20 from BTA1P001 t1) t1
inner join
(select min(UDEC17_100) from VNA1P002 t2 ) t2
on 1=0
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    #
    #  (TG) IJ (TA)  Expect { .8 .00012 16}
    stmt = """select *
from (select SDEC4_10, SDEC11_20 from BTA1P001 t1) t1(SDEC4_10, SDEC11_20)
inner join
(select min(UDEC17_100) from VNA1P002 t2 ) t2(UDEC17_100)
on t2.UDEC17_100 = t1.SDEC4_10 * 20
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s23')
    #
    # ----------------------------
    #       Id: JT.091c     RIGHT JOIN (TA) RJ (TAG)
    #       Id: JT.091k     RIGHT JOIN (TAG) RJ (TA)
    #  TA:  aggregates (derived tables)
    #  TAG: aggregates, GROUP BY (derived tables)
    # ----------------------------
    #
    #  Expect {AAAA AX}
    stmt = """select min(VARCHAR15_UNIQ), max(CHAR13_100)
from BTA1P001 t1
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s24')
    #
    #  Expect 6 rows as in table.
    stmt = """select min(VARCHAR15_UNIQ), max(CHAR13_100)
from BTA1P001 t2
group by CHAR13_100
order by 1, 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s25')
    #
    #  (TA) RJ (TAG)  Expect { AAAA AX *6 rows from t2 }
    stmt = """select *
from (select min(VARCHAR15_UNIQ), max(CHAR13_100) from BTA1P001 t1) t1(a,b)
right join
(select min(VARCHAR15_UNIQ), CHAR13_100 from BTA1P001 t2
group by CHAR13_100
) t2(c,d)
on 1=1
order by 1, 3, 4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s26')
    #
    #  (TA) RJ (TAG)  Expect { ? ? *6 rows from t2 }
    stmt = """select *
from (select min(VARCHAR15_UNIQ), max(CHAR13_100) from BTA1P001 t1) t1(a,b)
right join
(select min(VARCHAR15_UNIQ), CHAR13_100 from BTA1P001 t2
group by CHAR13_100
) t2(c,d)
on 1=0
order by 1, 3, 4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s27')
    #
    #  (TA) RJ (TAG)  Expect { (AAAA AX AAAA AX) , (? ? *5 rows from t2) }
    stmt = """select *
from (select min(VARCHAR15_UNIQ), max(CHAR13_100) from BTA1P001 t1) t1(a,b)
right join
(select min(VARCHAR15_UNIQ), CHAR13_100 from BTA1P001 t2
group by CHAR13_100
) t2(c,d)
on t1.a=t2.c
order by 1, 3, 4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s28')
    #
    #  (TAG) RJ (TA)  Expect { AAAA AX preceeded by *6 rows from t2 }
    stmt = """select *
from (select min(VARCHAR15_UNIQ), CHAR13_100 from BTA1P001 t2
group by CHAR13_100
) t2(c,d)
right join
(select min(VARCHAR15_UNIQ), max(CHAR13_100) from BTA1P001 t1) t1(a,b)
on 1=1
order by 1, 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s29')
    #
    #  (TAG) RJ (TA)  Expect { ? ? AAAA AX }
    stmt = """select *
from (select min(VARCHAR15_UNIQ), CHAR13_100 from BTA1P001 t2
group by CHAR13_100
) t2(c,d)
right join
(select min(VARCHAR15_UNIQ), max(CHAR13_100) from BTA1P001 t1) t1(a,b)
on 1=0
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s30')
    #
    #  (TAG) RJ (TA)  Expect { AAAA AX AAAA AX }
    stmt = """select *
from (select min(VARCHAR15_UNIQ), CHAR13_100 from BTA1P001 t2
group by CHAR13_100
) t2(c,d)
right join
(select min(VARCHAR15_UNIQ), max(CHAR13_100) from BTA1P001 t1) t1(a,b)
on t1.a=t2.c
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s31')
    #
    # ----------------------------
    #       Id: JT.094c     INNER JOIN (TA) IJ (TAG)
    #       Id: JT.094k     INNER JOIN (TAG) IJ (TA)
    # ----------------------------
    #
    #  (TA) IJ (TAG)  Expect 1 row { (AAAA AX AAAA AX) }
    stmt = """select *
from (select min(VARCHAR15_UNIQ), max(CHAR13_100) from BTA1P001 t1) t1(a,b)
inner join
(select min(VARCHAR15_UNIQ), CHAR13_100 from BTA1P001 t2
group by CHAR13_100
) t2(c,d)
on t1.a=t2.c
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s32')
    #
    #  (TAG) IJ (TA)  Expect 1 row { AAAA AX AAAA AX }
    stmt = """select *
from (select min(VARCHAR15_UNIQ), CHAR13_100 from BTA1P001 t2
group by CHAR13_100
) t2(c,d)
inner join
(select min(VARCHAR15_UNIQ), max(CHAR13_100) from BTA1P001 t1) t1(a,b)
on t1.a=t2.c
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s33')
    #
    # ----------------------------
    #       Id: JT.091d     RIGHT JOIN (TA) RJ (TGH)
    #       Id: JT.091p     RIGHT JOIN (TGH) RJ (TA)
    #       Id: JT.153      HAVING clause for JOIN contains ANSI String function
    # ----------------------------
    #  TA:  aggregates (derived tables)
    #  TGH: GROUP BY and HAVING (VNA1P004)
    # ----------------------------
    #
    #  >>>>>>>>>>>>> Omit table BTA1P004 if test on view VNA1P004 below! >>>>>>>>>>
    #  >>>>>>>>>>>>> Change table BTA1P004 to view VNA1P004 >>>>>>>>>>
    #  View has 12 instead of 13 rows; columns are:
    #     varchar0_4     , char0_1000 , sbin7_2
    #         , varchar5_10    , char6_20   , ubin15_uniq
    #         , varchar15_uniq , char16_uniq
    #
    #  >>>>>>>>>>>>> Expected results ????????? >>>>>>>>>>
    #
    #  Expect 6 rows as in table.
    stmt = """select min(VARCHAR15_UNIQ), max(CHAR13_100)
from BTA1P001 t2 group by CHAR13_100
order by 1, 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s34')
    #
    #  Check out base table if can't get view columns (are these same as view
    #  will be??)
    stmt = """select VARCHAR0_4 ,CHAR0_1000
from BTA1P004 
order by 1, 2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s35')
    stmt = """select SBIN7_2
,VARCHAR5_10     ,CHAR6_20      ,UBIN15_UNIQ
,VARCHAR15_UNIQ  ,CHAR16_UNIQ
from BTA1P004 
order by 1, 2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s36')
    #
    #  >>>??? Expect 3 rows { (A ...), (A ...), (CAA ...) }
    stmt = """select  VARCHAR0_4 ,VARCHAR5_10 ,VARCHAR15_UNIQ
from BTA1P004 
group by VARCHAR0_4 ,VARCHAR5_10 ,VARCHAR15_UNIQ
having lower(VARCHAR0_4||'x') > 'ab'
order by 1,2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s37')
    #
    stmt = """select VARCHAR5_10 ,substring( VARCHAR5_10 from 4 for 3)
from BTA1P004 
order by 1, 2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s38')
    #  >>>??? Expect 2 rows { (A ...), (AAA ...) } with 'AAA' at 4th to 6th of VARCHAR5_10
    stmt = """select  VARCHAR0_4 ,VARCHAR5_10 ,VARCHAR15_UNIQ
from BTA1P004 
group by VARCHAR0_4 ,VARCHAR5_10 ,VARCHAR15_UNIQ
having substring( VARCHAR5_10 from 4 for 3) = 'AAA'
order by 1,2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s39')
    #
    #  >>>>>>>>>>>>> view VNA1P004  Expected results ????????? >>>>>>>>>>
    #
    stmt = """select VARCHAR0_4 ,CHAR0_1000
from VNA1P004 
order by 1, 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s40')
    stmt = """select SBIN7_2
,VARCHAR5_10     ,CHAR6_20      ,UBIN15_UNIQ
,VARCHAR15_UNIQ  ,CHAR16_UNIQ
from VNA1P004 
order by 1, 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s41')
    #
    #  Expect 6 values as in view.
    stmt = """select min(VARCHAR15_UNIQ), max(VARCHAR15_UNIQ)
from VNA1P004 t2 group by VARCHAR15_UNIQ
order by 1, 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s42')
    stmt = """select min(VARCHAR15_UNIQ), VARCHAR15_UNIQ
from VNA1P004 t2
group by VARCHAR15_UNIQ
order by 1, 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s43')
    #
    #  Expect?
    stmt = """select VARCHAR0_4 ,CHAR0_1000
from VNA1P004 
order by 1, 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s44')
    stmt = """select SBIN7_2
,VARCHAR5_10     ,CHAR6_20      ,UBIN15_UNIQ
,VARCHAR15_UNIQ  ,CHAR16_UNIQ
from VNA1P004 
order by 1, 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s45')
    #
    stmt = """select VARCHAR0_4 ,CHAR0_1000
from VNA1P004 
order by 1, 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s46')
    stmt = """select SBIN7_2
,VARCHAR5_10     ,CHAR6_20      ,UBIN15_UNIQ
,VARCHAR15_UNIQ  ,CHAR16_UNIQ
from VNA1P004 
order by 1, 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s47')
    #
    #  >>>??? Expect 3 rows { (A ...), (A ...), (CAA ...) }
    stmt = """select  VARCHAR0_4 ,VARCHAR5_10 ,VARCHAR15_UNIQ
from VNA1P004 
group by VARCHAR0_4 ,VARCHAR5_10 ,VARCHAR15_UNIQ
having lower(VARCHAR0_4||'x') > 'ab'
order by 1,2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s48')
    #
    stmt = """select VARCHAR5_10 ,substring( VARCHAR5_10 from 4 for 3)
from VNA1P004 
order by 1,2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s49')
    
    #  >>>??? Expect 2 rows { (A ...), (AAA ...) } with 'AAA' at 4th to 6th of VARCHAR5_10
    stmt = """select  VARCHAR0_4 ,VARCHAR5_10 ,VARCHAR15_UNIQ
from VNA1P004 
group by VARCHAR0_4 ,VARCHAR5_10 ,VARCHAR15_UNIQ
having substring( VARCHAR5_10 from 4 for 3) = 'AAA'
order by 1,2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s50')
    #
    #  >>>>>>>>>>>>> Expected results ????????? >>>>>>>>>>
    #  (TA) RJ (TGH)  Expect { AAAA AXconcat *2 rows from view }
    stmt = """select *
from (select min(VARCHAR15_UNIQ), max(CHAR13_100||'concat')
from BTA1P001 t1
) t1(a,b)
right join
(select  VARCHAR0_4 ,VARCHAR5_10 ,VARCHAR15_UNIQ
from VNA1P004 
group by VARCHAR0_4 ,VARCHAR5_10 ,VARCHAR15_UNIQ
having lower(VARCHAR0_4||'x') > 'ab'
) t2(c,d,e)
on 1=1
order by a, d, e
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s51')
    #
    #  >>>>>>>>>>>>> Expected results ????????? >>>>>>>>>>
    #  (TA) RJ (TGH)  Expect { AAAA AXconcat *2 rows from view }
    stmt = """select *
from (select min(VARCHAR15_UNIQ), max(CHAR13_100||'concat')
from BTA1P001 t1
) t1(a,b)
right join
(select  VARCHAR0_4 ,VARCHAR5_10 ,VARCHAR15_UNIQ
from BTA1P004 
group by VARCHAR0_4 ,VARCHAR5_10 ,VARCHAR15_UNIQ
having substring( VARCHAR5_10 from 4 for 3) = 'AAA'
) t2(c,d,e)
on 1=1
order by a,c
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s52')
    #
    #  >>>>>>>>>>>>> Expected results ????????? >>>>>>>>>>
    #  (TGH) RJ (TA)  Expect 1 row { ? ? ? 'AAAA' 'AX   concat' }
    stmt = """select *
from (select  VARCHAR0_4 ,VARCHAR5_10 ,VARCHAR15_UNIQ
from BTA1P004 
group by VARCHAR0_4 ,VARCHAR5_10 ,VARCHAR15_UNIQ
having lower(VARCHAR0_4||'x') > 'ab'
) t2(c,d,e)
right join
(select min(VARCHAR15_UNIQ), max(CHAR13_100||'concat')
from BTA1P001 t1
) t1(a,b)
on 1=0
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s53')
    #
    # ----------------------------
    #       Id: JT.094d     INNER JOIN (TA) IJ (TGH)
    #       Id: JT.094p     INNER JOIN (TGH) IJ (TA)
    # ----------------------------
    #
    #  (TA) IJ (TGH)  Expect 2 rows { AAAA AXconcat *2 rows from view }
    stmt = """select *
from (select min(VARCHAR15_UNIQ), max(CHAR13_100||'concat')
from BTA1P001 t1
) t1(a,b)
inner join
(select  VARCHAR0_4 ,VARCHAR5_10 ,VARCHAR15_UNIQ
from BTA1P004 
group by VARCHAR0_4 ,VARCHAR5_10 ,VARCHAR15_UNIQ
having substring( VARCHAR5_10 from 4 for 3) = 'AAA'
) t2(c,d,e)
on 1=1
order by 1,3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s54')
    #
    # (TGH) IJ (TA)  Expect 0 rows.
    stmt = """select *
from (select  VARCHAR0_4 ,VARCHAR5_10 ,VARCHAR15_UNIQ
from BTA1P004 
group by VARCHAR0_4 ,VARCHAR5_10 ,VARCHAR15_UNIQ
having lower(VARCHAR0_4||'x') > 'ab'
) t2(c,d,e)
inner join
(select min(VARCHAR15_UNIQ), max(CHAR13_100||'concat')
from BTA1P001 t1
) t1(a,b)
on 1=0
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    #
    # ----------------------------
    #       Id: JT.091e     RIGHT JOIN (TA) RJ (TAGH)
    #       Id: JT.091u     RIGHT JOIN (TAGH) RJ (TA)
    #       Id: JT.151      ON clause contains ANSI String functions
    #       Id: JT.152      WHERE clause for JOIN contains ANSI String functions
    # ----------------------------
    #  TA:  aggregates (derived tables)
    #  TAGH:aggregates, GROUP BY, HAVING (e.g., VNA1P005).
    # ----------------------------
    #
    #  Expect {AAAA AX}
    stmt = """select min(VARCHAR15_UNIQ), max(CHAR13_100)
from BTA1P001 t1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s55')
    #
    #  Expect 6 rows as in table.
    stmt = """select min(VARCHAR15_UNIQ), max(CHAR13_100)
from BTA1P001 t2
group by CHAR13_100
order by 1, 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s56')
    #
    #  (TA) RJ (TAGH)  Expect {        }
    stmt = """select *
from (select min(VARCHAR15_UNIQ), max(CHAR13_100)
from BTA1P001 
) t1(a,b)
right join
(select N1, C2, C3, C4 from VNA1P005 ) t2
on 1=1
order by 1,3,5
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s57')
    #
    #  (TA) RJ (TAGH)  Expect {        }
    stmt = """select *
from (select min(VARCHAR15_UNIQ), max(CHAR13_100)
from BTA1P001 
) t1(a,b)
right join
(select N1, C2, C3, C4 from VNA1P005 ) t2
on lower(t2.C2) <> upper(t1.a)
order by 1,3,5
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s58')
    #
    #  (TAGH) RJ (TA)  Expect {        }
    stmt = """select *
from (select N1, C2, C3, C4 from VNA1P005 ) t2
right join
(select min(VARCHAR15_UNIQ), max(CHAR13_100)
from BTA1P001 
) t1(a,b)
on 1=1
order by 1,3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s59')
    #
    #  (TAGH) RJ (TA)  Expect {        }
    stmt = """select *
from (select N1, C2, C3, C4 from VNA1P005 ) t2
right join
(select min(VARCHAR15_UNIQ), max(CHAR13_100)
from BTA1P001 
) t1(a,b)
on 1=1
where lower(t2.C2) <> upper(t1.a)
order by 1,2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s60')
    #
    # ----------------------------
    #       Id: JT.094e     INNER JOIN (TA) IJ (TAGH)
    #       Id: JT.094u     INNER JOIN (TAGH) IJ (TA)
    # ----------------------------
    #
    #  (TA) IJ (TAGH)  Expect 4 rows (no null extension)
    stmt = """select *
from (select min(VARCHAR15_UNIQ), max(CHAR13_100)
from BTA1P001 
) t1(a,b)
inner join
(select N1, C2, C3, C4 from VNA1P005 ) t2
on lower(t2.C2) <> upper(t1.a)
order by 1,3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s61')
    #
    #  (TAGH) IJ (TA)  Expect  4 rows (no null extension)
    stmt = """select *
from (select N1, C2, C3, C4 from VNA1P005 ) t2
inner join
(select min(VARCHAR15_UNIQ), max(CHAR13_100)
from BTA1P001 
) t1(a,b)
on 1=1
where lower(t2.C2) <> upper(t1.a)
order by 1,2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s62')
    #
    # ----------------------------
    #  TG:  GROUP BY (VNA1P002) joined to the other grouped views
    #       in turn.
    # ----------------------------
    #  TG:  GROUP BY (VNA1P002)
    #  TAG: aggregates, GROUP BY (derived tables)
    #  TGH: GROUP BY and HAVING (VNA1P004)
    #  TAGH:aggregates, GROUP BY, HAVING (e.g., VNA1P005).
    #    (TA) RJ (TA2) ; (TA) RJ (TG); etc., making 25 (5*5 combinations)
    # ----------------------------
    #       Id: JT.091g     RIGHT JOIN (TG) RJ (TG)
    # ----------------------------
    #  TG:  GROUP BY (VNA1P002)
    #
    #  (TG) RJ (TG)  Expect 7 rows as in base table {(16,16) (24,24) ..}
    stmt = """select *
from (select UDEC17_100 from VNA1P002 t1) t1
right join
(select UDEC17_100 from VNA1P002 t2) t2
on t1.UDEC17_100=t2.UDEC17_100
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s63')
    #
    # ----------------------------
    #       Id: JT.094g     INNER JOIN (TG) IJ (TG)
    # ----------------------------
    #
    #  (TG) IJ (TG)  Expect 7 rows as in base table {(16,16) (24,24) ..}
    stmt = """select *
from (select UDEC17_100 from VNA1P002 t1) t1
inner join
(select UDEC17_100 from VNA1P002 t2) t2
on t1.UDEC17_100=t2.UDEC17_100
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s64')
    #
    # ----------------------------
    #       Id: JT.091h     RIGHT JOIN (TG) RJ (TAG)
    #       Id: JT.091l     RIGHT JOIN (TAG) RJ (TG)
    # ----------------------------
    #  TG:  GROUP BY (VNA1P002)
    #  TAG: aggregates, GROUP BY (derived tables)
    #
    #  Check results -- rows with 16 and 24 in the last column are used in
    #  joins in this set.
    stmt = """select SBIN1_100 , UDEC3_2000
, SBIN1_100 + 2 * UDEC3_2000 from BTA1P001 
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s65')
    #
    #  (TG) RJ (TAG)  Expect 6 rows from base table displayed on left of RJ,
    #                 and column A shown for rows where it is 16 or 24.
    stmt = """select *
from (select UDEC17_100 from VNA1P002 
) t1 (a)
right join
(select SBIN1_100 , UDEC3_2000
, SBIN1_100 + 2 * UDEC3_2000 from BTA1P001 
group by SBIN1_100, UDEC3_2000
) t2(c,d,e )
on t2.e = t1.a or ( t2.e + 1 = t1.a )
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s66')
    #
    #  (TAG) RJ (TG)  Expect 7 rows, with non-null values from joined table
    #                 when column A is 16 or 24.
    stmt = """select *
from (select SBIN1_100 , UDEC3_2000
, SBIN1_100 + 2 * UDEC3_2000 from BTA1P001 
group by SBIN1_100, UDEC3_2000
) t2(c,d,e )
right join
(select UDEC17_100 from VNA1P002 
) t1 (a)
on t2.e = t1.a or ( t2.e + 1 = t1.a )
order by c,a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s67')
    #
    # ----------------------------
    #       Id: JT.094h     INNER JOIN (TG) IJ (TAG)
    #       Id: JT.094l     INNER JOIN (TAG) IJ (TG)
    # ----------------------------
    #
    #  (TG) IJ (TAG)  Expect 2 rows from base table where column a
    #                 is 16 or 24 and row is not null-extended.
    stmt = """select *
from (select UDEC17_100 from VNA1P002 
) t1 (a)
inner join
(select SBIN1_100 , UDEC3_2000
, SBIN1_100 + 2 * UDEC3_2000 from BTA1P001 
group by SBIN1_100, UDEC3_2000
) t2(c,d,e )
on t2.e = t1.a or ( t2.e + 1 = t1.a )
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s68')
    #
    #  (TAG) IJ (TG)  Expect 2 rows from base table where column a
    #                 is 16 or 24 and row is not null-extended.
    stmt = """select *
from (select SBIN1_100 , UDEC3_2000
, SBIN1_100 + 2 * UDEC3_2000 from BTA1P001 
group by SBIN1_100, UDEC3_2000
) t2(c,d,e )
inner join
(select UDEC17_100 from VNA1P002 
) t1 (a)
on t2.e = t1.a or ( t2.e + 1 = t1.a )
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s69')
    
    _testmgr.testcase_end(desc)

def test011(desc="""a11"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =============== --- Begin Test Case Header  ==================
    #
    #  Test case name:     T1103:A11
    #  Description:        SQL JOIN on grouped views, Row Value
    #                      constructors, and derived tables.
    #
    # ================= ---End Test Case Header  ===================
    #
    # ----------------------------
    #  Tables created in preparation for test unit.
    # ----------------------------
    #
    # ----------------------------
    #  Check potential aggregates, etc for derived tables.
    # ----------------------------
    
    stmt = """select  SBIN4_2, CHAR13_100, VARCHAR15_UNIQ
,SBIN16_20,UBIN16_1000,SDEC19_1000
from BTA1P001 
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s0')
    stmt = """select  UBIN4_4, SDEC4_10, UDEC4_2, SDEC11_20
from BTA1P002 
order by 1, 2, 4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s1')
    stmt = """select  CHAR15_100, CHAR17_2
from BTA1P006 
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s2')
    #
    #  aggregates (only)
    #  BTA1P001: Not null:
    stmt = """select min(SBIN4_2),     max(SBIN4_2)
, min(CHAR13_100),  max(CHAR13_100)
, min(VARCHAR15_UNIQ), max(VARCHAR15_UNIQ)
, min(SBIN16_20),   max(SBIN16_20)
, min(UBIN16_1000), max(UBIN16_1000)
, min(SDEC19_1000), max(SDEC19_1000)
from BTA1P001 
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s3')
    #
    #  BTA1P002: Non-integer numerics:
    stmt = """select min( UBIN4_4), max( UBIN4_4)
, min(SDEC4_10)  , max(SDEC4_10)
, min(UDEC4_2)  , max(UDEC4_2)
, min(SDEC11_20)  , max(SDEC11_20)
from BTA1P002 
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s4')
    #
    #   aggregates and GROUP BY
    stmt = """select min(SBIN4_2),     max(SBIN4_2)
, min(CHAR13_100),  max(CHAR13_100)
, min(VARCHAR15_UNIQ), max(VARCHAR15_UNIQ)
, min(SBIN16_20),   max(SBIN16_20)
, min(UBIN16_1000), max(UBIN16_1000)
, min(SDEC19_1000), max(SDEC19_1000)
from BTA1P001 
group by SBIN4_2, CHAR13_100, VARCHAR15_UNIQ
,SBIN16_20,UBIN16_1000,SDEC19_1000
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s5')
    #  BTA1P002: Non-integer numerics:
    stmt = """select min(UBIN4_4),  max(UBIN4_4)
, min(SDEC4_10), max(SDEC4_10)
, min(UDEC4_2),  max(UDEC4_2)
, min(SDEC11_20),max(SDEC11_20)
from BTA1P002 
group by UBIN4_4, SDEC4_10, UDEC4_2, SDEC11_20
order by 1, 3, 7
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s6')
    #
    # ----------------------------
    #       Id: JT.091i     RIGHT JOIN (TG) RJ (TGH)
    #       Id: JT.091q     RIGHT JOIN (TGH) RJ (TG)
    #  TG:  GROUP BY (VNA1P002)
    #  TGH: GROUP BY and HAVING (VNA1P004)
    # ----------------------------
    #
    #  (98-10-13) Changed table BTA1P004 to view VNA1P004,
    #             as originally planned.
    #
    stmt = """select CHAR6_20 from VNA1P004 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s7')
    #
    stmt = """select CHAR17_100, UDEC17_100 from VNA1P002 
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s8')
    #
    #  (TG) RJ (TGH)  Expect 5 rows (2 matched rows on CCAA...A and 3 with NULLs
    #                 in A and B.
    stmt = """select *
from (select cast(CHAR17_100 as varchar(20))
, UDEC17_100 from VNA1P002 
) t1 (a, b)
right join
--       (select CHAR6_20 || 'AAAAAAAA' from BTA1P004
(select CHAR6_20 || 'AAAAAAAA' from VNA1P004 
group by CHAR6_20
) t2(c)
on t2.c=t1.a
order by 1, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s9')
    #
    #  (TGH) RJ (TG)  Expect 7 rows (2 matched rows on CCAA...A and 5
    #                 with NULLs in C.
    stmt = """select *
--  from (select CHAR6_20 || 'AAAAAAAA' from BTA1P004
from (select CHAR6_20 || 'AAAAAAAA' from VNA1P004 
group by CHAR6_20
) t2(c)
right join
(select cast(CHAR17_100 as varchar(20))
, UDEC17_100 from VNA1P002 
) t1 (a, b)
on t2.c=t1.a
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s10')
    #
    # ----------------------------
    #       Id: JT.094i     INNER JOIN (TG) IJ (TGH)
    #       Id: JT.094q     INNER JOIN (TGH) IJ (TG)
    # ----------------------------
    #
    #  (TG) IJ (TGH)  Expect 2 matched rows on CCAA...A.
    stmt = """select *
from (select cast(CHAR17_100 as varchar(20)), UDEC17_100 from VNA1P002 
) t1 (a, b)
inner join
(select CHAR6_20 || 'AAAAAAAA' from BTA1P004 
group by CHAR6_20
) t2(c)
on t2.c=t1.a
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s11')
    #
    #  (TGH) IJ (TG)  Expect 2 matched rows on CCAA...A.
    stmt = """select *
from (select CHAR6_20 || 'AAAAAAAA' from BTA1P004 
group by CHAR6_20
) t2(c)
inner join
(select cast(CHAR17_100 as varchar(20))
, UDEC17_100 from VNA1P002 
) t1 (a, b)
on t2.c=t1.a
order by 1, b
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s12')
    #
    # ----------------------------
    #       Id: JT.091j     RIGHT JOIN (TG) RJ (TAGH)
    #       Id: JT.091v     RIGHT JOIN (TAGH) RJ (TG)
    #  TG:  GROUP BY (VNA1P002)
    #  TAGH:aggregates, GROUP BY, HAVING (e.g., VNA1P005).
    # ----------------------------
    #
    #  (TG) RJ (TAGH)  Expect { 24 6*VNA1P005 rows  }
    stmt = """select *
from (select UDEC17_100 from VNA1P002 t1 ) t1(a)
right join
(select N1, C2, C3, C4 from VNA1P005 ) t2
on 1=1
where a=24
order by 1, 2, 4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s13')
    #  Expect 3 nulls, 3 24's.
    stmt = """select  char_length(C2||C3||C4)
from VNA1P005 order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s14')
    #
    #  (TG) RJ (TAGH)  Expect {          }
    #  Expect 3 nulls, 3 24's.
    stmt = """select *
from (select UDEC17_100 from VNA1P002 t1 ) t1(a)
right join
(select N1, C2, C3, C4
from VNA1P005 
) t2 (b,c,d,e)
on 2 * char_length(c||d||e) = t1.a
order by 1, 2, 4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s15')
    #
    #  (TAGH) RJ (TG)
    stmt = """select *
from (select N1, C2, C3, C4
from VNA1P005 
) t2 (b,c,d,e)
right join
(select UDEC17_100 from VNA1P002 t1 ) t1(a)
on 1=1
where a=24
order by 1, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s16')
    #
    #  (TAGH) RJ (TG)
    stmt = """select  2 * char_length(c||d||e) , t1.a
from (select N1, C2, C3, C4
from VNA1P005 
) t2 (b,c,d,e)
, (select UDEC17_100 from VNA1P002 t1 ) t1(a)
order by 1,2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s17')
    #
    #  (TAGH) RJ (TG)
    stmt = """select *
from (select N1, C2, C3, C4
from VNA1P005 
) t2 (b,c,d,e)
right join
(select UDEC17_100 from VNA1P002 t1 ) t1(a)
on 2 * char_length(c||d||e) = t1.a
where a=24
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s18')
    #
    # ----------------------------
    #       Id: JT.094j     INNER JOIN (TG) IJ (TAGH)
    #       Id: JT.094v     INNER JOIN (TAGH) IJ (TG)
    # ----------------------------
    #
    #  (TG) IJ (TAGH)  Expect {          }
    #  Expect 3 rows (24 * matching rows from VNA1P005).
    stmt = """select *
from (select UDEC17_100 from VNA1P002 t1 ) t1(a)
inner join
(select N1, C2, C3, C4
from VNA1P005 
) t2 (b,c,d,e)
on 2 * char_length(c||d||e) = t1.a
order by 1,2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s19')
    #
    #  (TAGH) IJ (TG)  Expect {          }
    stmt = """select *
from (select N1, C2, C3, C4
from VNA1P005 
) t2 (b,c,d,e)
inner join
(select UDEC17_100 from VNA1P002 t1 ) t1(a)
on 2 * char_length(c||d||e) = t1.a
where a=24
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s20')
    #
    # ----------------------------
    #  TAG: aggregates, GROUP BY (derived tables) joined to the other grouped views
    #       in turn.
    # ----------------------------
    #  TAG: aggregates, GROUP BY (derived tables)
    #  TGH: GROUP BY and HAVING (VNA1P004)
    #  TAGH:aggregates, GROUP BY, HAVING (e.g., VNA1P005).
    #    (TA) RJ (TA2) ; (TA) RJ (TG); etc., making 25 (5*5 combinations)
    # ----------------------------
    #       Id: JT.091m     RIGHT JOIN (TAG) RJ (TAG)
    # ----------------------------
    #  TAG: aggregates, GROUP BY (derived tables)
    #
    #  Expect {AAAA AX}
    #  Expect 6 rows as in table.
    stmt = """select VARCHAR15_UNIQ, CHAR13_100
from BTA1P001 t1
group by VARCHAR15_UNIQ, CHAR13_100
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s21')
    #
    stmt = """select min(VARCHAR15_UNIQ), max(CHAR13_100)
from BTA1P001 t2
group by CHAR13_100
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s22')
    #
    stmt = """select VARCHAR15_UNIQ, max(CHAR13_100) from BTA1P001 t1
group by VARCHAR15_UNIQ
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s23')
    #
    stmt = """select min(VARCHAR15_UNIQ), CHAR13_100 from BTA1P001 t2
group by CHAR13_100
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s24')
    #
    #  (TAG) RJ (TAG)  Expect 30 rows (cross product of 5*6 rows)
    stmt = """select *
from (select VARCHAR15_UNIQ, max(CHAR13_100) from BTA1P001 t1
group by VARCHAR15_UNIQ
) t1(a,b)
right join
(select min(VARCHAR15_UNIQ), CHAR13_100 from BTA1P001 t2
group by CHAR13_100
) t2(c,d)
on 1=1
order by 1, 2, 3, 4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s25')
    #
    # ----------------------------
    #       Id: JT.094m     INNER JOIN (TAG) IJ (TAG)
    # ----------------------------
    #
    #  (TAG) IJ (TAG)  Expect 30 rows (cross product of 5*6 rows).
    stmt = """select *
from (select VARCHAR15_UNIQ, max(CHAR13_100) from BTA1P001 t1
group by VARCHAR15_UNIQ
) t1(a,b)
inner join
(select min(VARCHAR15_UNIQ), CHAR13_100 from BTA1P001 t2
group by CHAR13_100
) t2(c,d)
on 1=1
order by 1, 2, 3, 4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s26')
    #
    # ----------------------------
    #       Id: JT.091n     RIGHT JOIN (TAG) RJ (TGH)
    #       Id: JT.091r     RIGHT JOIN (TGH) RJ (TAG)
    #  TAG: aggregates, GROUP BY (derived tables)
    #  TGH: GROUP BY and HAVING (VNA1P004)
    # ----------------------------
    #
    #  >>>>>>>>>>>>> Expected results ????????? >>>>>>>>>>
    #  (98-10-13) Changed table BTA1P004 to view VNA1P004,
    #             as originally planned.
    #
    #  select CHAR6_20 from BTA1P004
    stmt = """select CHAR6_20 from VNA1P004 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s27')
    #
    stmt = """select CHAR17_100, UDEC17_100 from VNA1P002 
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s28')
    #
    #  (TAG) RJ (TGH)  Expect 9 rows (1 matched rows on ABAA...ABAA;
    #                  4 on {AX 8.30} for each row of VNA1P004;
    #                  4 on {GIAAEAAA 8.90} for each row of VNA1P004;
    stmt = """select *
from ( select min(VARCHAR15_UNIQ),UBIN16_1000 from BTA1P001 
group by UBIN16_1000
) t1(a, b)
right join
(select substring(CHAR6_20 from 1 for 4 ) from BTA1P004 
) t2(c)
on t2.c=t1.a or ( b > 8.1 )
order by 1, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s29')
    stmt = """select *
from ( select min(VARCHAR15_UNIQ),UBIN16_1000 from BTA1P001 
group by UBIN16_1000
) t1(a, b)
right join
(select substring(CHAR6_20 from 1 for 4 ) from VNA1P004 
) t2(c)
on t2.c=t1.a or ( b > 8.1 )
order by 1, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s30')
    #
    #  (TGH) RJ (TAG)  Expect 9 rows as above, plus 3 rows with values
    #                  for a and b, with NULL column c, where match fails.
    stmt = """select a,b,c
from (select substring(CHAR6_20 from 1 for 4 ) from BTA1P004 
) t2(c)
right join
( select min(VARCHAR15_UNIQ),UBIN16_1000 from BTA1P001 
group by UBIN16_1000
) t1(a, b)
on t2.c=t1.a or ( b > 8.1 )
order by 1, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s31')
    stmt = """select a,b,c
from (select substring(CHAR6_20 from 1 for 4 ) from VNA1P004 
) t2(c)
right join
( select min(VARCHAR15_UNIQ),UBIN16_1000 from BTA1P001 
group by UBIN16_1000
) t1(a, b)
on t2.c=t1.a or ( b > 8.1 )
order by 1, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s32')
    #
    # ----------------------------
    #       Id: JT.094n     INNER JOIN (TAG) IJ (TGH)
    #       Id: JT.094r     INNER JOIN (TGH) IJ (TAG)
    # ----------------------------
    #
    #  (TAG) IJ (TGH)  Expect 9 rows (1 matched rows on ABAA...ABAA;
    #                  4 on {AX 8.30} for each row of VNA1P004;
    #                  4 on {GIAAEAAA 8.90} for each row of VNA1P004;
    stmt = """select *
from ( select min(VARCHAR15_UNIQ),UBIN16_1000 from BTA1P001 
group by UBIN16_1000
) t1(a, b)
inner join
(select substring(CHAR6_20 from 1 for 4 ) from BTA1P004 
) t2(c)
on t2.c=t1.a or ( b > 8.1 )
order by 1, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s33')
    stmt = """select *
from ( select min(VARCHAR15_UNIQ),UBIN16_1000 from BTA1P001 
group by UBIN16_1000
) t1(a, b)
inner join
(select substring(CHAR6_20 from 1 for 4 ) from VNA1P004 
) t2(c)
on t2.c=t1.a or ( b > 8.1 )
order by 1, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s34')
    #
    #  (TGH) IJ (TAG)  Expect 9 rows as above.
    stmt = """select a,b,c
from (select substring(CHAR6_20 from 1 for 4 ) from BTA1P004 
) t2(c)
inner join
( select min(VARCHAR15_UNIQ),UBIN16_1000 from BTA1P001 
group by UBIN16_1000
) t1(a, b)
on t2.c=t1.a or ( b > 8.1 )
order by 1, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s35')
    stmt = """select a,b,c
from (select substring(CHAR6_20 from 1 for 4 ) from VNA1P004 
) t2(c)
inner join
( select min(VARCHAR15_UNIQ),UBIN16_1000 from BTA1P001 
group by UBIN16_1000
) t1(a, b)
on t2.c=t1.a or ( b > 8.1 )
order by 1, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s36')
    #
    # ----------------------------
    #       Id: JT.091o     RIGHT JOIN (TAG) RJ (TAGH)
    #       Id: JT.091w     RIGHT JOIN (TAGH) RJ (TAG)
    #  TAG: aggregates, GROUP BY (derived tables)
    #  TAGH:aggregates, GROUP BY, HAVING (e.g., VNA1P005).
    # ----------------------------
    #
    stmt = """select min(VARCHAR15_UNIQ), CHAR13_100 from BTA1P001 t2
group by CHAR13_100
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s37')
    #
    #  (TAG) RJ (TAGH)
    #  Expect 6 rows: { 'AAAA' , 1.98 , -4344 , 'AA' , 'BA' }
    #                 plus five rows of VNA1P005 with left 2 columns NULL.
    stmt = """select *
from ( select min(VARCHAR15_UNIQ),UBIN16_1000 from BTA1P001 t2
group by UBIN16_1000
) t1(a, b)
right join
(select N1, C2, C4 from VNA1P005 ) t2
on c2||c2 = a
order by 1, 3, 5
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s38')
    #
    #  (TAGH) RJ (TG)  Expect { -4344 , 'AA' , 'BA' , 'AAAA' , 1.98 }
    stmt = """select *
from (select N1, C2, C4 from VNA1P005 ) t2
right join
(select min(VARCHAR15_UNIQ),UBIN16_1000 from BTA1P001 t2
group by UBIN16_1000
) t1(a, b)
on c2||c2 = a and n1 <> b
order by 1, 4, 5
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s39')
    #
    # ----------------------------
    #       Id: JT.094o     INNER JOIN (TAG) IJ (TAGH)
    #       Id: JT.094w     INNER JOIN (TAGH) IJ (TAG)
    # ----------------------------
    #
    #  (TAG) IJ (TAGH)
    #  Expect 1 row: { 'AAAA' , 1.98 , -4344 , 'AA' , 'BA' }
    #  ?????????????????????????
    stmt = """select *
from ( select min(VARCHAR15_UNIQ),UBIN16_1000 from BTA1P001 t2
group by UBIN16_1000
) t1(a, b)
inner join
(select N1, C2, C4 from VNA1P005 ) t2
on c2||c2 = a
order by 1, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s40')
    #
    #  (TAGH) IJ (TG)  Expect { -4344 , 'AA' , 'BA' , 'AAAA' , 1.98 }
    stmt = """select *
from (select N1, C2, C4 from VNA1P005 ) t2
inner join
(select min(VARCHAR15_UNIQ),UBIN16_1000 from BTA1P001 t2
group by UBIN16_1000
) t1(a, b)
on c2||c2 = a and n1 <> b
order by 1, 4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s41')
    #
    # ----------------------------
    #  TGH: GROUP BY and HAVING (VNA1P004) joined to the other grouped views
    #       in turn.
    # ----------------------------
    #  TGH: GROUP BY and HAVING (VNA1P004)
    #  TAGH:aggregates, GROUP BY, HAVING (e.g., VNA1P005).
    #    (TA) RJ (TA2) ; (TA) RJ (TG); etc., making 25 (5*5 combinations)
    # ----------------------------
    #       Id: JT.091s    RIGHT JOIN (TGH) RJ (TGH)
    #  TGH: GROUP BY and HAVING (VNA1P004)
    # ----------------------------
    #
    #  (98-10-13) Changed table BTA1P004 to view VNA1P004,
    #             as originally planned. May keep table tests
    #             with View tests.
    #
    #  >>>>>>>>>>>>> Expected results ????????? >>>>>>>>>>
    #
    #  (TGH) RJ (TGH)  Expect 7 rows (2 matched rows on CCAA...A and 5 with NULLs
    #                  in C) <<< ?
    stmt = """select CHAR6_20 || 'AAAAAAAA' from BTA1P004 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s42')
    stmt = """select *
from (select CHAR6_20 || 'AAAAAAAA' from BTA1P004 
group by CHAR6_20
) t2(ca)
right join
(select CHAR6_20 || 'AAAAAAAA' from BTA1P004 
group by CHAR6_20
) t1 (cb)
on t2.ca=t1.cb
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s43')
    #
    stmt = """select *
from (select CHAR6_20 || 'AAAAAAAA' from BTA1P004 
where CHAR6_20 < 'AK'
group by CHAR6_20
) t2(ca)
right join
(select CHAR6_20 || 'AAAAAAAA' from BTA1P004 
where CHAR6_20 > 'AI'
group by CHAR6_20
) t1 (cb)
on (select max(CHAR6_20) from BTA1P004) > 'CC' --<<<<<< subq in ON clause
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s44')
    #
    #  >>>>>>>>>>>>> view VNA1P004 >>>>>>>>>>
    #
    stmt = """select CHAR6_20 || 'AAAAAAAA' from VNA1P004 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s45')
    stmt = """select *
from (select CHAR6_20 || 'AAAAAAAA' from VNA1P004 
group by CHAR6_20
) t2(ca)
right join
(select CHAR6_20 || 'AAAAAAAA' from VNA1P004 
group by CHAR6_20
) t1 (cb)
on t2.ca=t1.cb
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s46')
    #
    stmt = """select *
from (select CHAR6_20 || 'AAAAAAAA' from VNA1P004 
where CHAR6_20 < 'AK'
group by CHAR6_20
) t2(ca)
right join
(select CHAR6_20 || 'AAAAAAAA' from VNA1P004 
where CHAR6_20 > 'AI'
group by CHAR6_20
) t1 (cb)
on (select max(CHAR6_20) from VNA1P004) > 'CC' --<<<<<< subq in ON clause
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s47')
    #
    # ----------------------------
    #       Id: JT.094s    INNER JOIN (TGH) IJ (TGH)
    # ----------------------------
    #
    stmt = """select *
from (select CHAR6_20 || 'AAAAAAAA' from BTA1P004 
group by CHAR6_20
) t2(ca)
inner join
(select CHAR6_20 || 'AAAAAAAA' from BTA1P004 
group by CHAR6_20
) t1 (cb)
on t2.ca=t1.cb
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s48')
    #
    stmt = """select *
from (select CHAR6_20 || 'AAAAAAAA' from BTA1P004 
where CHAR6_20 < 'AK'
group by CHAR6_20
) t2(ca)
inner join
(select CHAR6_20 || 'AAAAAAAA' from BTA1P004 
where CHAR6_20 > 'AI'
group by CHAR6_20
) t1 (cb)
on (select max(CHAR6_20) from BTA1P004) > 'CC' --<<<<<< subq in ON clause
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s49')
    #
    #  >>>>>>>>>>>>> view VNA1P004 >>>>>>>>>>
    #
    stmt = """select *
from (select CHAR6_20 || 'AAAAAAAA' from VNA1P004 
group by CHAR6_20
) t2(ca)
inner join
(select CHAR6_20 || 'AAAAAAAA' from VNA1P004 
group by CHAR6_20
) t1 (cb)
on t2.ca=t1.cb
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s50')
    #
    
    stmt = """select *
from (select CHAR6_20 || 'AAAAAAAA' from VNA1P004 
where CHAR6_20 < 'AK'
group by CHAR6_20
) t2(ca)
inner join
(select CHAR6_20 || 'AAAAAAAA' from VNA1P004 
where CHAR6_20 > 'AI'
group by CHAR6_20
) t1 (cb)
on (select max(CHAR6_20) from VNA1P004) > 'CC' --<<<<<< subq in ON clause
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    #
    # ----------------------------
    #       Id: JT.091t     RIGHT JOIN (TGH) RJ (TAGH)
    #       Id: JT.091x     RIGHT JOIN (TAGH) RJ (TGH)
    #  TGH: GROUP BY and HAVING (VNA1P004)
    #  TAGH:aggregates, GROUP BY, HAVING (e.g., VNA1P005).
    # ----------------------------
    #
    #  >>>>>>>>>>>>> Expected results ????????? >>>>>>>>>>
    #
    stmt = """select VARCHAR5_10, CHAR6_20 from BTA1P004 
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s51')
    #
    #  Expect 6 rows {(BA, ABAAAAAA, AA, BA) (BA, ABAAAAAA, ?, BA)
    #                 plus (? ? xx yy) for remainder}
    #  (TGH) RJ (TAGH)
    stmt = """select *
from ( select substring(VARCHAR5_10 from 2 for 2), CHAR6_20
from BTA1P004 
) t1(a,b)
right join
(select C2, C4 from VNA1P005 ) t2
on a=c4
order by 1, 3, 4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s52')
    stmt = """select *
from ( select substring(VARCHAR5_10 from 2 for 2), CHAR6_20
from VNA1P004 
) t1(a,b)
right join
(select C2, C4 from VNA1P005 ) t2
on a=c4
order by 1, 3, 4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s53')
    #  (TAGH) RJ (TGH)
    #  Expect 5 rows (4 rows in VNA1P004, with 2 corresponding rows in VNA1P005),
    #   {(AA, BA, BA, ABAAAAAA) (?, BA, BA, ABAAAAAA)
    #                 plus (? ? xx yy) for remainder}
    stmt = """select *
from (select C2, C4 from VNA1P005 ) t2
right join
(select substring(VARCHAR5_10 from 2 for 2), CHAR6_20
from BTA1P004 
) t1(a,b)
on a=c4
order by 1, 2, 3, 4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s54')
    stmt = """select *
from (select C2, C4 from VNA1P005 ) t2
right join
(select substring(VARCHAR5_10 from 2 for 2), CHAR6_20
from VNA1P004 
) t1(a,b)
on a=c4
order by 1, 2, 3, 4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s55')
    #
    # ----------------------------
    #       Id: JT.094t     INNER JOIN (TGH) IJ (TAGH)
    #       Id: JT.094x     INNER JOIN (TAGH) IJ (TGH)
    # ----------------------------
    #
    #  (TGH) IJ (TAGH)
    #  Expect 2 rows {(BA, ABAAAAAA, AA, BA) (BA, ABAAAAAA, ?, BA)}
    stmt = """select *
from ( select substring(VARCHAR5_10 from 2 for 2), CHAR6_20
from BTA1P004 
) t1(a,b)
inner join
(select C2, C4 from VNA1P005 ) t2
on a=c4
order by 1, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s56')
    stmt = """select *
from ( select substring(VARCHAR5_10 from 2 for 2), CHAR6_20
from VNA1P004 
) t1(a,b)
inner join
(select C2, C4 from VNA1P005 ) t2
on a=c4
order by 1, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s57')
    #
    #  (TAGH) IJ (TGH)
    #  Expect 2 rows {(AA, BA, BA, ABAAAAAA) (?, BA, BA, ABAAAAAA)}
    stmt = """select *
from (select C2, C4 from VNA1P005 ) t2
inner join
(select substring(VARCHAR5_10 from 2 for 2), CHAR6_20
from BTA1P004 
) t1(a,b)
on a=c4
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s58')
    stmt = """select *
from (select C2, C4 from VNA1P005 ) t2
inner join
(select substring(VARCHAR5_10 from 2 for 2), CHAR6_20
from VNA1P004 
) t1(a,b)
on a=c4
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s59')
    #
    # ----------------------------
    #  TAGH:aggregates, GROUP BY, HAVING (e.g., VNA1P005) joined to itself.
    # ----------------------------
    #  TAGH:aggregates, GROUP BY, HAVING (e.g., VNA1P005).
    #    (TA) RJ (TA2) ; (TA) RJ (TG); etc., making 25 (5*5 combinations)
    # ----------------------------
    #       Id: JT.091y     RIGHT JOIN (TAGH) RJ (TAGH)
    #  TAGH:aggregates, GROUP BY, HAVING (e.g., VNA1P005).
    # ----------------------------
    #
    stmt = """select C2, C4 from VNA1P005 
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s60')
    #
    #  (TAGH) RJ (TAGH)
    stmt = """select *
from (select C2, C4 from VNA1P005 ) t1
right join
(select C2, C4 from VNA1P005 ) t2
on t1.c2 > t2.c2
order by 1, 3, 4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s61')
    #
    # ----------------------------
    #       Id: JT.094y     INNER JOIN (TAGH) IJ (TAGH)
    # ----------------------------
    #
    #  (TAGH) RJ (TAGH)
    stmt = """select *
from (select C2, C4 from VNA1P005 ) t1
inner join
(select C2, C4 from VNA1P005 ) t2
on t1.c2 > t2.c2
order by 1, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s62')
    
    _testmgr.testcase_end(desc)

def test012(desc="""a12"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =============== --- Begin Test Case Header  ==================
    #
    #  Test case name:     T1103:A12
    #  Description:        SQL JOIN on grouped views, Row Value
    #                      constructors, and derived tables.
    #
    # ================= ---End Test Case Header  ===================
    
    #  Expect 13 rows of base table.
    stmt = """select VARCHAR5_10, CHAR6_20
from BTA1P004 
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s0')
    #
    #  Expect 12 rows of view.
    stmt = """select VARCHAR5_10, CHAR6_20
from VNA1P004 
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s1')
    #
    #  Expect 12 rows of maximum ('AM').
    stmt = """select
( select max(VARCHAR5_10) from VNA1P004 
)
from
( select CHAR6_20
from VNA1P004 
) t1(b);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s2')
    #
    #  Expect 1 row { BA, ABAAAAAA, DA, DA }
    stmt = """select max(a)
, (select max(VARCHAR5_10) from BTA1P004)
, max(C2)
from
( select substring(VARCHAR5_10 from 2 for 2), CHAR6_20
from BTA1P004 
) t1(a,b)
right join
( select C2, C4 from VNA1P005 
) t2
on a=c4
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s3')
    #
    #  Expect 1 row { BA, ABAAAAAA, DA, DA }
    stmt = """select max(a)
, (select max(VARCHAR5_10) from BTA1P004)
, max(C2)
from
( select substring(VARCHAR5_10 from 2 for 2)
, CHAR6_20
from BTA1P004 
) t1(a,b)
inner join
( select C2, C4 from VNA1P005 
) t2
on a=c4
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s4')
    #
    # ----------------------------
    #  Same queries as given above with tables are now given with views.
    # ----------------------------
    #
    #  Expect ?
    stmt = """select max(a)
, (select max(VARCHAR5_10) from VNA1P004)
, max(C2)
from
( select substring(VARCHAR5_10 from 2 for 2), CHAR6_20
from VNA1P004 
) t1(a,b)
right join
( select C2, C4 from VNA1P005 
) t2
on a=c4
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s5')
    #
    #  Expect 1 row { BA, ABAAAAAA, DA, DA }
    stmt = """select max(a)
, (select max(VARCHAR5_10) from VNA1P004)
, max(C2)
from
( select substring(VARCHAR5_10 from 2 for 2)
, CHAR6_20
from VNA1P004 
) t1(a,b)
inner join
( select C2, C4 from VNA1P005 
) t2
on a=c4
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s6')
    #
    # ----------------------------
    #       Id: JT.272      RVC within Joined columns via Derived Tables.
    #                       See also:
    #  TGH: GROUP BY and HAVING (VNA1P004)
    #  TAGH:aggregates, GROUP BY, HAVING (e.g., VNA1P005).
    # ----------------------------
    #
    #  (TGH) IJ (TAGH)
    #
    #  Expect 'BA':
    stmt = """select min(substring(VARCHAR5_10 from 2 for 2))
from VNA1P004 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s7')
    #
    #  Expect 6 rows from view:
    stmt = """select C2, C4 from VNA1P005 
order by C2, C4 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s8')
    #
    #  Expect 12 rows: 8 rows are (BA .... BA) plus 4 are (? ? <VNA1P005 value>)
    stmt = """select * from
( select
( select min(substring(VARCHAR5_10 from 2 for 2) )
from BTA1P004 
)
, CHAR6_20
from BTA1P004 
) t1(a,b)
right join
( select C2, C4 from VNA1P005 
) t2
on a=c4
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s9')
    #
    #  Expect 8 rows (BA .... BA)
    stmt = """select * from
( select
( select min(substring(VARCHAR5_10 from 2 for 2) )
from BTA1P004 
)
, CHAR6_20
from BTA1P004 
) t1(a,b)
right join
( select C2, C4 from VNA1P005 
) t2
on a=c4
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s10')
    
    _testmgr.testcase_end(desc)

def test013(desc="""a13"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =============== --- Begin Test Case Header  ==================
    #
    # Test case name:      T1103:A13
    # Description:         This test verifies SQL JOIN in preparation
    #                      on grouped views.
    #
    # ================= ---End Test Case Header  ===================
    
    stmt = """create table t(i int) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """insert into t values (39);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #
    #  Join 2 tables; include all tables in at least one ON clause.
    #  Expect 1 row.
    stmt = """select * from
(select t1.i, t2.i
from t t1
left join t t2 on t2.i = t1.i
) dt(a,b) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s0')
    
    #  Join 2 tables; omit one of tables from all ON clauses.
    #  Expect 1 row.
    stmt = """select * from
(select t1.i, t2.i
from t t1
left join t t2 on t2.i = 39
) dt(a,b) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s1')
    #  Expect 1 row.
    stmt = """select * from
(select t1.i, t2.i
from t t1
left join t t2 on 39 = t1.i
) dt(a,b) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s2')
    
    #  Join 3 tables; include all tables in at least one ON clause.
    #  Expect 1 row.
    stmt = """select * from
(select t1.i, t2.i, t3.i
from t t1
left join t t2 on t2.i = t1.i
inner join t t3 on t3.i = t1.i
) dt(a,b,c) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s3')
    
    #  Join 3 tables; omit one of tables from all ON clauses.
    #  Expect 1 row.
    stmt = """select * from
(select t1.i, t2.i , t3.i
from t t1
left join t t2 on t2.i = t1.i
left join t t3 on t2.i = t1.i
) dt(a,b,c) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s4')
    #  Expect 1 row.
    stmt = """select * from
(select t1.i, t2.i , t3.i
from t t1
left join t t2 on t2.i = t1.i
left join t t3 on (1=1)
) dt(a,b,c) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s5')
    #  Expect 1 row.
    stmt = """select * from
(select t1.i, t2.i , t3.i
from t t1
left join t t2 on t2.i = t1.i
left join t t3 on (1=0)
) dt(a,b,c) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s6')
    
    #  Join 4 tables; include all tables in at least one ON clause.
    #  Expect 1 row.
    stmt = """select * from
(select t1.i, t2.i , t3.i, t4.i
from t t1
left join t t2 on t2.i = t1.i
left join t t3 on t2.i = t3.i
inner join t t4 on t1.i = t4.i
) dt(a,b,c,d) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s7')
    
    #  Join 3 tables; omit one of tables from all ON clauses.
    #  Expect 1 row.
    stmt = """select * from
(select t1.i, t3.i, t4.i
from t t1
left join t t3 on t1.i = t3.i
inner join t t4 on t1.i = t3.i
--   Note: ON omits t4
) dt(a,c,d) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s8')
    
    #  Join 4 tables; omit one of tables from all ON clauses.
    #  Expect 1 row.
    stmt = """select * from
(select t1.i, t2.i , t3.i, t4.i
from t t1
left join t t2 on t2.i = t1.i
left join t t3 on t2.i = t3.i
inner join t t4 on t1.i = t3.i
--    Note: ON omits t4
) dt(a,b,c,d) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s9')
    
    _testmgr.testcase_end(desc)

def test014(desc="""a14"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =============== --- Begin Test Case Header  ==================
    #
    #  Test case name:     T1103:A14
    #  Description:        SQL JOIN on grouped views, Row Value
    #                      constructors, and derived tables.
    #
    # ================= ---End Test Case Header  ===================
    
    # ----------------------------
    #  Check the values of views that are combinations of JOIN, GROUP BY.
    #  Tables include unique and non-unique values:
    # ----------------------------
    
    a14setup._init(_testmgr)
    
    stmt = """select * from view1 order by c1, c2, c4 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a14exp""", 'a14s0')
    stmt = """select * from view2 order by 1, 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a14exp""", 'a14s1')
    stmt = """select * from view3 order by c1, c7, c8 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a14exp""", 'a14s2')
    stmt = """select * from view4 order by c1, c2, c4 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a14exp""", 'a14s3')
    stmt = """select c1, c2, c3, c4, c5 from view5 order by 1, 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a14exp""", 'a14s4')
    stmt = """select c1, c2, c6, c7, c8 from view5 order by 1, 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a14exp""", 'a14s5')
    
    # ----------------------------
    #  OUTER Join the views.
    # ----------------------------
    #
    #  Expect 2 rows (('abcd' '1xz' 'abcd' 'abcd' '1xz' abcd')
    #                 (NULL  NULL  NULL  'ac' '1xw'  NULL))
    stmt = """select v1.c1, v1.c2, v1.c3, v2.c1, v2.c2, v2.c3 from view1 v1
right join view2 v2
on v1.c1=v2.c1
order by 1, 5
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a14exp""", 'a14s6')
    #
    #  Expect 2 rows ((NULL  NULL  NULL  'ac' '1xw'  NULL)
    #                 (NULL  NULL  NULL  'abcd' '1xz' abcd'))
    stmt = """select v1.c1, v1.c2, v1.c3, v2.c1, v2.c2, v2.c3 from view1 v1
right join view2 v2
on v1.c1=v2.c2 -- Change JOIN condition from the above.
order by 1, 5
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a14exp""", 'a14s7')
    #
    #  Vary the combinations of joined views.
    #  Expect 5 rows with all columns 'abcd'.
    stmt = """select v2.c1, v2.c3, v2.c5, v3.c1, v3.c3, v3.c5 from view2 v2
right join view3 v3
on v2.c1=v3.c1
order by 1, 5
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a14exp""", 'a14s8')
    #
    #  Expect 10 rows: 5 rows with all columns 'abcd';
    #  the other 5 rows of view4 are NULL-extended.
    stmt = """select v3.c1, v3.c3, v3.c5, v4.c1, v4.c3, v4.c5 from view3 v3
right join view4 v4
on v3.c1=v4.c1
order by 1, 4, 5
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a14exp""", 'a14s9')
    #
    #  Expect 1 row with all columns 'abcd'.
    stmt = """select v4.c1, v4.c3, v4.c5, v5.c1, v5.c3, v5.c5 from view4 v4
right join view5 v5
on v4.c1=v5.c1
order by 1, 5
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a14exp""", 'a14s10')
    #
    # ----------------------------
    #  NATURAL Join the views.
    # ----------------------------
    #
    #  Expect 1 matching row.
    stmt = """select * from view1 v1
NATURAL join view2 v2
order by 1, 5
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a14exp""", 'a14s11')
    #
    #  Expect 1 matching row.
    stmt = """select * from view2 v2
NATURAL join view3 v3
order by 1, 5
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a14exp""", 'a14s12')
    #
    #  Expect 1 matching row.
    stmt = """select * from view3 v3
NATURAL join view4 v4
order by 1, 5
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a14exp""", 'a14s13')
    #
    #  Cannot made NATURAL join of view4 with view5 because
    #  column data types differ. Likewise for view5 and view1.
    #
    # ----------------------------
    #  INNER Join the views.
    # ----------------------------
    #
    #  Expect 1 row (('abcd' '1xz' 'abcd' 'abcd' '1xz' abcd')}
    stmt = """select v1.c1, v1.c2, v1.c3, v2.c1, v2.c2, v2.c3 from view1 v1
INNER join view2 v2
on v1.c1=v2.c1
order by 1, 5
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a14exp""", 'a14s14')
    #
    #  Expect 5 rows with all columns 'abcd'.
    stmt = """select v2.c1, v2.c3, v2.c5, v3.c1, v3.c3, v3.c5 from view2 v2
INNER join view3 v3
on v2.c1=v3.c1
order by 1, 5
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a14exp""", 'a14s15')
    #
    #  Expect 5 rows with all columns 'abcd'.
    stmt = """select v3.c1, v3.c3, v3.c5, v4.c1, v4.c3, v4.c5 from view3 v3
INNER join view4 v4
on v3.c1=v4.c1
order by 1, 5
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a14exp""", 'a14s16')
    #
    #  Expect 1 row with all columns 'abcd'.
    stmt = """select v4.c1, v4.c3, v4.c5, v5.c1, v5.c3, v5.c5 from view4 v4
INNER join view5 v5
on v4.c1=v5.c1
order by 1, 5
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a14exp""", 'a14s17')
    
    _testmgr.testcase_end(desc)

def test015(desc="""a15"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =============== --- Begin Test Case Header  ==================
    #
    #  Test case name:     T1103:A15
    #  Description:        SQL JOIN on grouped views, Row Value
    #                      constructors, and derived tables.
    #
    # ================= ---End Test Case Header  ===================
 
    # ----------------------------
    #  Check the values of views that are combinations of JOIN, GROUP BY.
    #  Tables include unique and non-unique values:
    # ----------------------------
    #
    #  View containing CASE:
    
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.VNA1P009 
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s0')
    #
    #  View containing string functions:
    stmt = """select CLOWER, CUPPER from VNA1P007 
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s1')
    #
    # ----------------------------
    #       Id: JT.161      NATURAL JOIN on view containing simple and searched CASE.
    #       Id: JT.154      NATURAL JOIN on view containing ANSI String functions.
    # ----------------------------
    #
    #  Expect 14 rows (8 as in view plus 6).
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.VNA1P009 v91
natural join """ + gvars.g_schema_arkcasedb + """.VNA1P009 v92
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s2')
    #
    # Expect 0 row.
    
    stmt = """select * from
( select * from """ + gvars.g_schema_arkcasedb + """.VNA1P009 
) v9(a,b)
natural join
( select CLOWER, CUPPER from VNA1P007 
) v7(a,b)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    #
    #  Expect 6 rows as in view (where each stored row is unique,
    #  although this subset of columns shows duplicates).
    stmt = """select cchar_length, cposition from VNA1P007 v71
natural join VNA1P007 v72
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s3')
    #
    # ----------------------------
    #       Id: JT.162      RIGHT OUTER JOIN on view containing simple and searched CASE.
    #       Id: JT.155      RIGHT OUTER JOIN on view containing ANSI String functions.
    # ----------------------------
    #
    #  Expect 8 rows as in view, no match.
    stmt = """select v91.csimple as v91_csimple, v92.csimple as v92_csimple
from """ + gvars.g_schema_arkcasedb + """.VNA1P009 v91
right outer join """ + gvars.g_schema_arkcasedb + """.VNA1P009 v92
--  on (v91.csimple, v92.csimple) like ('Value%','Value B%')
on v91.csimple like 'Value %' and
v92.csimple like 'Value B%'
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s4')
    #
    #  Expect 48 (6*8) rows.
    stmt = """select * from
( select * from """ + gvars.g_schema_arkcasedb + """.VNA1P009 
) v9(a,b)
right outer join
( select CLOWER, CUPPER from VNA1P007 
) v7(a,b)
on (1=1)
order by 1, 2, 3    

;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s5')
    #
    #  Repeat with LEFT JOIN, without derived tables.
    stmt = """select v9.*, CLOWER, CUPPER
from VNA1P007 v7
left outer join """ + gvars.g_schema_arkcasedb + """.VNA1P009 v9
on csimple like 'Value %'
--       and CLOWER like 'aaaa%'
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s6')
    #
    #  Repeat with specific columns in select list and without
    #  derived tables; different predicate.
    stmt = """select CLOWER, CUPPER
from """ + gvars.g_schema_arkcasedb + """.VNA1P009 v9
right outer join VNA1P007 v7
on csimple like 'Value %'
--       and CLOWER like 'aaaa%'
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s7')
    #  Empty right side:
    stmt = """select CLOWER, CUPPER
from """ + gvars.g_schema_arkcasedb + """.VNA1P009 v9
right outer join VNA1P007 v7
on (1=0)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s8')
    #
    stmt = """select CLOWER, CUPPER
from """ + gvars.g_schema_arkcasedb + """.VNA1P009 v9
right outer join VNA1P007 v7
on CLOWER between 'London' and 'Paris'
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s9')
    #
    #  Empty left side:
    stmt = """select CLOWER, CUPPER
from """ + gvars.g_schema_arkcasedb + """.VNA1P009 v9
right outer join VNA1P007 v7
on csimple between 'London' and 'Paris'
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s10')
    #
    #  Expect 36 rows (6*6) as in view.
    stmt = """select v71.CUPPER, v72.CLOWER from VNA1P007 v71
right outer join VNA1P007 v72
on (1=1)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s11')
    #
    # ----------------------------
    #       Id: JT.163      INNER JOIN on view containing simple and searched CASE.
    #       Id: JT.156      INNER JOIN on view containing ANSI String functions.
    # ----------------------------
    #
    #  Expect 64 rows (8*8 as in view), no match.
    stmt = """select v91.csimple, v92.csearched
from """ + gvars.g_schema_arkcasedb + """.VNA1P009 v91
inner join """ + gvars.g_schema_arkcasedb + """.VNA1P009 v92
on (1=1)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s12')
    #
    #  Expect ?? rows as in view.
    stmt = """select v91.csimple, v92.csearched
from """ + gvars.g_schema_arkcasedb + """.VNA1P009 v91
inner join """ + gvars.g_schema_arkcasedb + """.VNA1P009 v92
on ( v91.csimple LIKE '%3')
and (v92.csearched between 'rabid' and 'silly' )
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s13')
    #
    #  Expect 8 rows.
    stmt = """select * from
( select * from """ + gvars.g_schema_arkcasedb + """.VNA1P009 
) v9(a,b)
inner join
( select CLOWER, CUPPER from VNA1P007 
) v7(a,b)
on (v7.a LIKE 'b%' )
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s14')
    #
    #  Expect 30 rows (6*5).
    stmt = """select v71.CUPPER, v72.CLOWER from VNA1P007 v71
inner join VNA1P007 v72
on (lower(v71.cupper) <> v72.clower)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s15')
    #
    # ----------------------------
    #       Id: JT.164      Simple CASE contains NATURAL JOIN.
    # ----------------------------
    #
    #  Expect 3 rows.
    stmt = """select distinct csimple, char_length(csimple) as length_csimple
FROM """ + gvars.g_schema_arkcasedb + """.VNA1P009 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s16')
    #
    stmt = """select distinct CASE char_length(csimple)
WHEN 1
THEN 'Text: csimple length is one'
ELSE 'Text: Not WHEN 1 THEN'
END
as case_result
FROM """ + gvars.g_schema_arkcasedb + """.VNA1P009 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s17')
    #
    #  Natural Join in RVC for truth value in WHEN.
    stmt = """select distinct CASE
WHEN -- 1
--  Expect 14 rows (8 as in view plus 6).
( 14 = ( select count(*)
from """ + gvars.g_schema_arkcasedb + """.VNA1P009 v91
natural join """ + gvars.g_schema_arkcasedb + """.VNA1P009 v92
)
)
THEN 'Text: the total is 14'
ELSE 'Text: the total is NOT 14'
END
FROM """ + gvars.g_schema_arkcasedb + """.VNA1P009 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s18')
    #
    stmt = """select distinct CASE
WHEN -- 1
--  Expect 14 rows (8 as in view plus 6).
( 14 = 14
)
THEN 'Text: the total is 14'
ELSE 'Text: the total is NOT 14'
END
FROM """ + gvars.g_schema_arkcasedb + """.VNA1P009 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s19')
    #
    stmt = """select CASE char_length(csimple)
WHEN 1
THEN
'Max = ' ||
( select max(csimple) from """ + gvars.g_schema_arkcasedb + """.VNA1P009 v91
natural join """ + gvars.g_schema_arkcasedb + """.VNA1P009 v92
)
ELSE
'Min = ' ||
( select min(csimple)
from """ + gvars.g_schema_arkcasedb + """.VNA1P009 v91
natural join """ + gvars.g_schema_arkcasedb + """.VNA1P009 v92
)
END
FROM """ + gvars.g_schema_arkcasedb + """.VNA1P009 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s20')
    #
    stmt = """select CASE char_length(csimple)
WHEN 1
THEN
'Max = ' ||
( select max(csimple) from """ + gvars.g_schema_arkcasedb + """.VNA1P009 v91
natural join """ + gvars.g_schema_arkcasedb + """.VNA1P009 v92
)
ELSE
'Min = ' ||
( select min(v91.csimple) from """ + gvars.g_schema_arkcasedb + """.VNA1P009 v91
right join """ + gvars.g_schema_arkcasedb + """.VNA1P009 v92
on (1=1)
)
END
FROM """ + gvars.g_schema_arkcasedb + """.VNA1P009 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s21')
    #
    stmt = """select CASE char_length(csimple)
WHEN 1
THEN
'Max = ' ||
( select max(csimple) from """ + gvars.g_schema_arkcasedb + """.VNA1P009 v91
natural join """ + gvars.g_schema_arkcasedb + """.VNA1P009 v92
)
ELSE
'Min = ' ||
( select min(csimple) from """ + gvars.g_schema_arkcasedb + """.VNA1P009 v91
natural join """ + gvars.g_schema_arkcasedb + """.VNA1P009 v92
)
END
FROM """ + gvars.g_schema_arkcasedb + """.VNA1P009 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s22')
    #
    # ----------------------------
    #       Id: JT.157      JOIN view columns defined as ANSI numeric-value functions (CHAR_LENGTH, POSITION).
    # ----------------------------
    #
    stmt = """select v1.cChar_length, v1.cPosition
from VNA1P007 v1
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s23')
    #  Expect 6 rows
    #  { (? 0) (? 0) (? 0) (8 9) (8 9) (8 9) }
    #  ( 7 7 8 16 16 16) joined to (0 0 0 9 9 9) -1.
    stmt = """select v1.cChar_length, v2.cPosition
from VNA1P007 v1
right outer join VNA1P007 v2
on v1.cChar_length = (v2.cPosition - 1)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s24')
    #
    # ----------------------------
    #       Id: JT.158      JOIN view columns defined as ANSI string-value functions (SUBSTRING, TRIM).
    # ----------------------------
    #
    #  Expect 11 rows
    stmt = """select v1.cSubstring, v2.cTrim
from VNA1P007 v1
right outer join VNA1P007 v2
on v1.cSubstring = v2.cTrim -- which gives 0 rows.
or (v1.cSubstring = 'BA') -- which gives all 6 'BA' rows.
or (v2.cTrim = 'trim leading spaces BA') -- which gives 5 rows plus 1 dup.
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s25')
    #
    # ----------------------------
    #       Id: JT.159      JOIN view columns defined as ANSI string operator: || (concatenate on character strings).
    #       Id: JT.160      JOIN view columns defined as ANSI numeric-value functions (LOWER, UPPER).
    # ----------------------------
    #
    #  Expect 6 rows
    stmt = """select v1.cUpper, v2.cLower
from VNA1P007 v1
right outer join VNA1P007 v2
on v1.cUpper = upper(v2.cLower)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s26')
    
    _testmgr.testcase_end(desc)

def test016(desc="""a16"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =============== --- Begin Test Case Header  ==================
    #
    # Test case name:      T1103:A16 -- Natural Join of wide tables and views
    #                      isolated here; otherwise they stopped testA05 by gobbling
    #                      virtual memory).
    # Description:         This test verifies SQL NATURAL JOIN via SELECT
    #                      on wide tables.
    #
    # ================= ---End Test Case Header  ===================
    # ----------------------------
    #  NATURAL [INNER] JOIN; JOIN wide Tables.
    # ----------------------------
    
    stmt = """select CHAR11_4 from BTA1P001 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s0')
    stmt = """select CHAR11_4 from BTA1P002 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s1')
    stmt = """select CHAR11_4 from BTA1P003 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s2')
    stmt = """select CHAR11_4 from BTA1P004 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s3')
    #
    # Should show 0 rows.
    
    stmt = """select CHAR11_4 from BTA1P001 
natural join BTA1P002 
natural join BTA1P003 
natural join BTA1P004 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    #
    # Should show 0 rows.
    stmt = """select * from BTA1P001 
natural join BTA1P002 
natural join BTA1P003 
natural join BTA1P004 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    #
    # ---------------------------
    # Basic NATURAL JOIN-- View to different view.
    # ---------------------------
    #
    # Should show 0 rows, due to non-matching columns.
    stmt = """select UDEC9_10 from VUA1P001 
natural join VUA1P003 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    #
    # ----------------------------
    #  Basic NATURAL JOIN of Table to View.
    # ----------------------------
    #
    #  Should show 0 rows (none of full rows match completely).
    stmt = """select VARCHAR0_4 from BTA1P001 t1
natural join BTA1P004 t2
natural join BTA1P002 t3
natural join VUA1P001 t4
natural join BTA1P001 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    #
    # Should show 0 rows (none match completely).
    stmt = """select VARCHAR0_4 from
 BTA1P001 natural join
 BTA1P002 natural join
 BTA1P004 natural join
 VUA1P001 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    #
    # ----------------------------
    #       ********** Also see above!!!!!!!!!
    #                       NATURAL RIGHT JOIN
    #                       NOTE: NO TABLE NAME exposed in NATURAL JOIN.
    #
    #  Base table, using columns of type numeric, char, varchar:
    stmt = """select sbinneg15_nuniq, char3_4 from BTA1P005 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s5')
    stmt = """select sbinneg15_nuniq, char3_4 from BTA1P005 
natural right join BTA1P005 t 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s6')
    stmt = """select varchar0_4, varchar5_10 from BTA1P002 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s7')
    #  MS3+ (3/20/96 build) loops after 2 rows; Assertion failed: file opt.C, line 295
    #  On DISPLAY, after normalization.
    stmt = """select varchar0_4, varchar5_10 from BTA1P002 
natural right join BTA1P002 t 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s8')
    #
    #  View containing outer join.
    stmt = """select * from VNA1P005 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s9')
    #  BUG 3/1/96. Assertion failed: file GenPreCode.C, line 535
    #  BUG9606: MS3 returns 0 rows.
    stmt = """select * from VNA1P005 
natural join VNA1P005 v
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s10')
    
    _testmgr.testcase_end(desc)

def test017(desc="""a17"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =============== --- Begin Test Case Header  ==================
    #
    # Test case name:      T1103:A17
    # Description:         This test verifies SQL NATURAL outer
    #                      JOIN on grouped views.
    #
    # ================= ---End Test Case Header  ===================
    #
    # ----------------------------
    #  Check the values of views that are combinations of JOIN, GROUP BY.
    #  Tables include unique and non-unique values:
    # ----------------------------
    
    a17setup._init(_testmgr)
    
    stmt = """select * from view1 order by 1, 2, c4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s0')
    stmt = """select * from view2 order by 1, 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s1')
    stmt = """select * from view3 order by 1, 2, c7, c8;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s2')
    stmt = """select * from view4 order by 1, 2, c4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s3')
    stmt = """select * from view6 order by 1, 2, c4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s4')
    stmt = """select * from view7 order by 1, 2, c4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s5')
    #
    # ----------------------------
    #  NATURAL RIGHT Join the views.
    # ----------------------------
    #
    #  Expect 2 rows.
    stmt = """select * from view1 v1
NATURAL  right join  view2 v2
order by 1, 5
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s6')
    #
    #  Expect 5 rows.
    stmt = """select * from view2 v2
NATURAL  right join  view3 v3
order by C1, C7, C8
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s7')
    #
    #  Expect 6 rows.
    stmt = """select * from view3 v3
NATURAL  right join  view4 v4
order by C1, C4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s8')
    #
    #  Expect 1 row.
    stmt = """select * from view4 v4
NATURAL  right join  view6 v6
order by 1, 5
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s9')
    #
    #  Expect 3 rows.
    stmt = """select * from view6 v6
NATURAL  right join  view1 v1
order by C1, C4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s10')
    #
    #  Expect 1 row.
    stmt = """select * from view4 v4
NATURAL  right join  view7 v7
order by 1, 5
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s11')
    #
    #  Expect 3 rows.
    stmt = """select * from view7 v7
NATURAL  right join  view1 v1
order by C1, C4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s12')
    
    _testmgr.testcase_end(desc)

