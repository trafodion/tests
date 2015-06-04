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
    #  Test case name:     T1112:A01
    #  Description:        SQL non-transaction negative tests.
    #                      This test verifies the SQL Derived Table
    #                      features for error handling.
    #
    # =================== End Test Case Header  ===================
    #
    # ---------------------------
    # Negative Basic tests for Derived Tables.
    # ---------------------------
    #
    # ---------------------------------------
    # Set up defines globally.
    # ---------------------------------------
    # Catalog for 'global database #11'.
    #
    # Schema for 'global database #11'.
    #
    #  ---------------------------
    #       Id: DTN.01      Correlation name is required.
    #  ---------------------------
    #
    
    stmt = """select * from (select c2, c3 from VNA1P005) ;"""
    output = _dci.cmdexec(stmt)
    if hpdci.tgtSQ():
        _dci.expect_error_msg(output, '15001')
    elif hpdci.tgtTR():
        _dci.expect_selected_msg(output)

    #
    #  ---------------------------
    #       Id: DTN.02      Correlation name cannot be keyword.
    #  ---------------------------
    #
    #  Expect appropriate error message.
    stmt = """select * from (select c2, c3 from VNA1P005) select ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """select * from (select c2, c3 from VNA1P005) table  ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """select * from (select c2, c3 from VNA1P005) on     ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    #
    #  ---------------------------
    #       Id: DTN.03      ANSI SQL93, section 6.3, SR7: Number of explicit
    #                            derived column names cannot be more than
    #                            number of columns in DT.
    #  ---------------------------
    #
    #  Expect appropriate error message.
    stmt = """select * from
(select c2, c3 from VNA1P005 
) dt (c01, c02, c03, c04) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4016')
    #
    stmt = """select * from
(select c3     from VNA1P005 
) dt (c3, c4) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4016')
    #
    stmt = """select distinct
( select N1 from
( select N1
from VNA1P005 
) t1
right join
( select min(N1)
from VNA1P005 
) t2(a,b) --
on 1=1
)
from VNA1P005 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4016')
    #
    #  ---------------------------
    #       Id: DTN.04      ANSI SQL93, section 6.3, SR7: Number of explicit
    #                            derived column names cannot be less than
    #                            number of columns in DT.
    #  ---------------------------
    #
    #  Expect appropriate error message.
    stmt = """select * from
(select c2, c3 from VNA1P005 
) dt (c2)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4016')
    #
    stmt = """select * from
(select * from VNA1P005 
) dt (c2)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4016')
    #
    stmt = """select distinct
( select a from
( select N1, C2, C3, C4
from VNA1P005 
) t1(a)
right join
( select min(VARCHAR15_UNIQ)
from BTA1P001 
) t2
on 1=1
)
from VNA1P005 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4016')
    #
    #  ---------------------------
    #       Id: DTN.05      DT cannot include Order By
    #  ---------------------------
    #
    #  Expect appropriate error message.
    stmt = """select * from ( select c2, c3 from VNA1P005 order by 1 ) dt ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """select * from ( select c2, c3 from VNA1P005 order by c3) dt ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    #
    #  ---------------------------
    #       Id: DTN.06      Attempt to access column missing from DT column list.
    #  ---------------------------
    #
    #  Expect appropriate error message.
    stmt = """select noCol from (select * from VNA1P005 ) dt ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    stmt = """select stillNoCol from (
select c2, c3 from VNA1P005 
) dt( x, y )
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    #
    #  Error found by processing ON clause.
    stmt = """select *
from (select c2, c3 from VNA1P005) dta
right join (select char3_4 from BTA1P005) dtc
on dta.alsoNoCol = dtc.char3_4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4003')
    #
    #  Error found by processing WHERE clause.
    stmt = """select *
from (select c2, c3 from VNA1P005) dta
, (select char3_4 from BTA1P005) dtc
where dta.c3 = dtc.noCol
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4003')
    #
    #  ---------------------------
    #       Id: DTN.07      Empty list of derived columns.
    #  ---------------------------
    #
    #  Expect appropriate error message.
    stmt = """select * from (select c2, c3 from VNA1P005) dt () ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    #
    #  ---------------------------
    #       Id: DTN.08      Illegal name for derived table.
    #  ---------------------------
    #
    #  Expect appropriate error message.
    stmt = """select * from ( select c2, c3 from VNA1P005 ) *punc ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """select * from ( select c2, c3 from VNA1P005 ) punc^ ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """select * from ( select c2, c3 from VNA1P005 ) pun%c ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """select * from ( select c2, c3 from VNA1P005 ) pu#nc ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """select * from ( select c2, c3 from VNA1P005 ) p@unc ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    #
    #  ---------------------------
    #       Id: DTN.09      Illegal name for derived columns.
    #  ---------------------------
    #
    #  Expect appropriate error message.
    stmt = """select * from ( select c2, c3 from VNA1P005 ) dt (bad*col*name,c);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """select * from ( select c2, c3 from VNA1P005 ) dt (a,bad*col*name);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    #
    #  ---------------------------
    #  Scope Negative tests for DT's.
    #  ---------------------------
    #
    #  ---------------------------
    #       Id: DTN.11      ANSI SQL93, section 6.3, SR3: Don't expose the
    #                            same table name more than once in the same
    #                            scope.
    #  ---------------------------
    #
    #  Expect appropriate error message.
    stmt = """select * from (select c4 from VNA1P005) dt (c2a),
(select c2 from VNA1P005) dt (c2b) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4056')
    #
    #  ---------------------------
    #       Id: DTN.12      ANSI SQL93, section 6.3, SR6: Don't repeat column
    #                            name in explicit derived column list.
    #  ---------------------------
    #
    #  Expect appropriate error message.
    stmt = """select * from (select c2, c3 from VNA1P005) dt (c, c) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4017')
    #
    stmt = """select * from (
select c2, c3, c4 from VNA1P005 
) dt (c3, c, c3)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4017')
    #
    #  ---------------------------
    #       Id: DTN.13      ANSI SQL93, section 6.3, SR6: Don't repeat column
    #                            name in implicit derived column list.
    #  ---------------------------
    #
    #  Expect appropriate error message.
    stmt = """select * from (select c2, c2 from VNA1P005) dt ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4011')
    stmt = """select c2 from (select c2, c2 from VNA1P005) dt ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4004')
    #
    stmt = """select dt.c3 from (
select c3, c2, t.c3, c4 from VNA1P005 t
) dt
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s29')
    #
    #  See positive tests for the following -- legal if no explicit
    #  mention of duplicate column name,
    #    select dt.c2 from (
    #       select c3, c2, c3, c4 from VNA1P005
    #       ) dt
    #    ;
    #
    #  ---------------------------
    #       Id: DTN.14      Scope rule error: Attempt to use table name used
    #                            in construction of DT but not exposed.
    #  ---------------------------
    #
    #  Expect appropriate error message.
    stmt = """select VNA1P005.* from (
select * from VNA1P005 
) dt
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4010')
    #
    #  ---------------------------
    #       Id: DTN.15      Scope rule error: Attempt to use column name used
    #                            in construction of DT but not exposed.
    #  ---------------------------
    #
    #  Expect appropriate error message.
    stmt = """select c3 from (select c2, c3, c4 from VNA1P005)
dt (ca, cb, cc) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    _testmgr.testcase_end(desc)

def test002(desc="""a02"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     T1112:A02
    #  Description:        SQL non-transaction negative tests.
    #                      This test verifies SQL subquery and
    #                      equality transformations
    #                      via SELECT -- Error handling.
    #
    # =================== End Test Case Header  ===================
    #
    # ---------------------------
    # Choose local schema:
    # ---------------------------
    #
    # Personal schema for this testunit.
    #
    #  End of file cidefs.
    #
    
    #  Check initial values.
    stmt = """select vchar1, nint from TTFONE order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s0')
    #
    #  ---------------------------
    #       Id: TFN.01        Subquery attempts to return > 1 column in SELECT list.
    #  ---------------------------
    #
    #  Expect error.
    stmt = """select ( select vchar1, nint from TTFONE ) from TTFONE t1 ;"""
    output = _dci.cmdexec(stmt)
    if hpdci.tgtSQ():
        _dci.expect_error_msg(output, '4019')
    elif hpdci.tgtTR():
        _dci.expect_selected_msg(output)

    #
    #  Expect error.
    stmt = """select ( select 1,2 from TTFONE ) from TTFONE t1 ;"""
    output = _dci.cmdexec(stmt)
    if hpdci.tgtSQ():
        _dci.expect_error_msg(output, '4019')
    elif hpdci.tgtTR():
        _dci.expect_selected_msg(output)
    #
    #  This should be ok.
    stmt = """select ( select 1 from TTFONE )
from TTFONE t1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s3')
    #
    #  ---------------------------
    #       Id: TFN.02a       Subquery attempts to return > 1 row in select list.
    #  ---------------------------
    #
    #  Expect error.
    stmt = """select  ( select ch4 from TTF )
from TTF t1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8401')
    #
    #  Expect error.
    stmt = """select  ( select 2   from TTF )
from TTF t1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8401')
    #
    #  ---------------------------
    #       Id: TFN.02b       Subquery with predicate in select list attempts to return > 1 row.
    #  ---------------------------
    #
    stmt = """select ch4 from TTF where ch4 > 'b' ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s6')
    #
    #  Expect error.
    stmt = """select  ( select ch4 from TTF where ch4 > 'b' )
from TTF t1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8401')
    #
    #  ---------------------------
    #       Id: TFN.02c       Subquery in WHERE clause attempts to return > 1 row.
    #  ---------------------------
    #
    #  Expect error.
    stmt = """select * from TTF t1
where ( select ch4 from TTF ) > 'b' ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8401')
    #
    #  ---------------------------
    #       Id: TFN.02d       Subquery with predicate in WHERE clause attempts to return > 1 row.
    #  ---------------------------
    #
    #  Expect error.
    stmt = """select * from TTF t1
where ( select ch4 from TTF where ch4 > 'b' ) < 'd' ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8401')
    #
    #  ---------------------------
    #       Id: TFN.02e       Subquery in ON clause attempts to return > 1 row.
    #  ---------------------------
    #
    #  Expect error.
    stmt = """select  t1.vch7, t2.vch7
from TTF t1 left join TTF t2
on  ( select t3.vch7 from TTF t3 ) = t2.vch7
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8401')
    #
    #  ---------------------------
    #       Id: TFN.02f       Subquery in select list of searched CASE attempts to return > 1 row.
    #  ---------------------------
    #
    #  Expect error.
    stmt = """select
CASE (select t.nsint from TTF t)
WHEN 1 THEN ''
WHEN 2 THEN 'c'
ELSE NULL
END
from TTF 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8401')
    #
    #  ---------------------------
    #       Id: TFN.03        Subquery in Derived Table attempts to return > 1 column.
    #  ---------------------------
    #
    #  Expect ('cc', 2).
    stmt = """select max(t.vch7), min(t.nnum5) from TTF t ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s12')
    #  Expect error.
    stmt = """select (select max(t.vch7), min(t.nnum5) from TTF t) from TTF;"""
    output = _dci.cmdexec(stmt)
    if hpdci.tgtSQ():
        _dci.expect_error_msg(output, '4019')
    elif hpdci.tgtTR():
        _dci.expect_selected_msg(output)
    #
    #  Expect ('cc', 2).
    stmt = """select * from (
select max(t.vch7), min(t.nnum5)
from TTF t
) dt (colname1, nint)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s14')
    #
    #  Expect error.
    stmt = """select * from (
select (
select max(t.vch7), min(t.nnum5)
from TTF t
) from TTF 
) dt (colname1, nint)
;"""
    output = _dci.cmdexec(stmt)
    if hpdci.tgtSQ():
        _dci.expect_error_msg(output, '4019')
    elif hpdci.tgtTR():
        _dci.expect_selected_msg(output)
    #
    #  Expect (1, 2).
    stmt = """select * from (
select distinct 1,2 from TTF 
) dt (colname1, nint)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s16')
    #
    #  Expect (1, 2) for derived table.
    stmt = """select * from (
select * from (
select distinct 1,2 from TTF 
) dt (colname1, nint)
) dt1 (colname1, nint)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s17')
    #
    #  Expect ERROR 4019 for subquery.
    stmt = """select * from (
select (
select distinct 1,2 from TTF t
) from TTF 
) dt (colname1, nint)
;"""
    output = _dci.cmdexec(stmt)
    if hpdci.tgtSQ():
        _dci.expect_error_msg(output, '4019')
    elif hpdci.tgtTR():
        _dci.expect_selected_msg(output)
    #  Use numeric constants instead of column names -- still expect error.
    stmt = """select * from (
select (
select distinct 1,2 from TTF t
) from TTF 
) dt
;"""
    output = _dci.cmdexec(stmt)
    if hpdci.tgtSQ():
        _dci.expect_error_msg(output, '4019')
    elif hpdci.tgtTR():
        _dci.expect_selected_msg(output)
    #  One numeric constant only.
    stmt = """select * from (
select (
select distinct 2 from TTF t
) from TTF 
) dt (nint)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s20')
    #  Expect error.
    stmt = """select (
select distinct 1,2 from TTF t
) from TTF 
;"""
    output = _dci.cmdexec(stmt)
    if hpdci.tgtSQ():
        _dci.expect_error_msg(output, '4019')
    elif hpdci.tgtTR():
        _dci.expect_selected_msg(output)
    #  Expect ok with one literal in subquery.
    stmt = """select (
select distinct 1 from TTF t
) from TTF 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s22')
    #
    #  Expect error.
    stmt = """select * from (
select (
select vchar1, nint from TTFONE 
) from TTFONE 
) dt (colname1, nint)
;"""
    output = _dci.cmdexec(stmt)
    if hpdci.tgtSQ():
        _dci.expect_error_msg(output, '4019')
    elif hpdci.tgtTR():
        _dci.expect_selected_msg(output)
    #
    #  ---------------------------
    #       Id: TFN.04        No column by that name known to subquery.
    #  ---------------------------
    #
    #  Expect error.
    stmt = """select noSuchCol from TTF ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    #
    #  Expect error.
    stmt = """select ( select noSuchCol from TTF )
from TTFONE ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    #
    #  Expect error.
    stmt = """select ( select t.noSuchCol from TTF t )
from TTFONE ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4003')
    #
    #  Expect error.
    stmt = """select ( select max(noSuchCol) from TTF )
from TTFONE ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    #
    #  Expect error.
    stmt = """select ( select max(t.noSuchCol) from TTF t )
from TTFONE ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4003')
    #
    #  ---------------------------
    #  Final reckoning; remove rows.
    #  ---------------------------
    #
    stmt = """select * from TTF order by 1, 2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s29')
    
    stmt = """delete from TTF;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 5)
    #
    #  Check initial values.
    stmt = """select vchar1, nint from TTFONE order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s30')
    stmt = """delete from TTFONE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    _testmgr.testcase_end(desc)

def test003(desc="""a03"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     T1112:A03
    #  Description:        SQL non-transaction negative tests.
    #                      This test verifies SQL JOIN
    #                      via SELECT: negative tests.
    #
    # =================== End Test Case Header  ===================
    #
    # ---------------------------
    # Basic Negative tests for JOIN.
    # ---------------------------
    #
    # ---------------------------
    # ANSI syntax requirements and other errors.
    # ---------------------------
    #
    # ---------------------------------------
    # Set up defines globally.
    # ---------------------------------------
    # Catalog for 'global database #11'.
    #
    # Schema for 'global database #11'.
    #
    #  ---------------------------
    #       Id: JTN.11      NATURAL JOIN cannot reference column names qualified
    #                        by name of a joined table (not accessible explicitly).
    #  ---------------------------
    #
    
    stmt = """select BTA1P001.VARCHAR0_4
from BTA1P001    natural join BTA1P001 t1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4002')
    stmt = """select VARCHAR0_4 , BTA1P001.CHAR1_4
from BTA1P001 t1 natural join BTA1P001 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4002')
    #
    stmt = """select VARCHAR0_4 , CHAR1_4 , UDEC1_10 , t1.SDEC5_100 , UBIN6_2
from BTA1P001    natural join BTA1P001 t1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4002')
    stmt = """select VARCHAR0_4 , t.CHAR1_4
from BTA1P001    natural join BTA1P001 t
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4002')
    #
    #  ---------------------------
    #       Id: JTN.12      ON is illegal on NATURAL JOIN
    #  ---------------------------
    #
    stmt = """select VARCHAR0_4 , CHAR1_4 from BTA1P001 s
natural join BTA1P001 t
ON s.VARCHAR0_4 = t.CHAR1_4 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    #
    stmt = """select VARCHAR0_4 , CHAR1_4 from BTA1P001 
natural join BTA1P001 t
ON VARCHAR0_4 = CHAR1_4 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    #
    stmt = """select VARCHAR0_4 , CHAR1_4 from BTA1P001 s natural join BTA1P001 t
ON s.VARCHAR0_4 = 'a' ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    #
    #  ---------------------------
    #       Id: JTN.13      USING is illegal on NATURAL JOIN
    #  Syntactically, USING not supported till after MS3.
    #  ---------------------------
    #
    stmt = """select VARCHAR0_4 , CHAR1_4 from BTA1P001 natural join BTA1P001 t
USING CHAR1_4 , VARCHAR0_4 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    #
    stmt = """select VARCHAR0_4 from BTA1P001 natural join BTA1P001 t
USING VARCHAR0_4 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    #
    #  ---------------------------
    #       Id: JTN.14      UNION is illegal with NATURAL JOIN.
    #  ---------------------------
    #
    stmt = """select VARCHAR0_4 from BTA1P001 
natural UNION join BTA1P001 t ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    #
    #  ---------------------------
    #       Id: JTN.15      UNION is illegal with join condition (ON ...).
    #  ---------------------------
    #
    stmt = """select s.VARCHAR0_4 from BTA1P001 s
UNION join BTA1P001 t ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3137')
    #
    stmt = """select t.VARCHAR0_4 from BTA1P001 s
UNION join BTA1P001 t ON s.VARCHAR0_4 = t.CHAR1_4 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3137')
    #
    stmt = """select VARCHAR0_4 from BTA1P001 
UNION join BTA1P001 t ON VARCHAR0_4 = CHAR1_4 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3137')
    #
    #  ---------------------------
    #       Id: JTN.16      UNION is illegal with named-columns join (USING (<col-list>)).
    #  ---------------------------
    #
    stmt = """select VARCHAR0_4 from BTA1P001 UNION join BTA1P001 t
USING VARCHAR0_4 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3137')
    #
    stmt = """select VARCHAR0_4 from BTA1P001 UNION BTA1P001 t
USING VARCHAR0_4 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    #
    #  ---------------------------
    #       Id: JTN.21      Attempt to join row-value constructor in a LEFT join on right-hand side.
    #                       The error is that row-value constructor is illegal;
    #                       A Derived Table is legal here.
    #                       Expect syntax error, which may include attempt to
    #                       use keywords as derived table names.
    #                       Same for JTN.21 to JTN.24.
    #  ---------------------------
    #
    stmt = """select * from ( select t1.sbinneg15_nuniq from BTA1P005 t1 ) dt
left join ( select t1.sbinneg15_nuniq     from BTA1P005 t1 )
on 1=1
;"""
    output = _dci.cmdexec(stmt)
    if hpdci.tgtSQ():
        _dci.expect_error_msg(output, '15001')
    elif hpdci.tgtTR():
        _dci.expect_selected_msg(output)

    #
    #  ---------------------------
    #       Id: JTN.22      Attempt to join row-value constructor in a LEFT join on left-hand side.
    #  ---------------------------
    #
    stmt = """select * from ( select sbinneg15_nuniq from BTA1P005 )
left join ( select sbinneg15_nuniq from BTA1P005) dt on 1=1 ;"""
    output = _dci.cmdexec(stmt)
    if hpdci.tgtSQ():
        _dci.expect_error_msg(output, '15001')
    elif hpdci.tgtTR():
        _dci.expect_selected_msg(output)

    #
    #  ---------------------------
    #       Id: JTN.23      Attempt to join row-value constructor in a NATURAL join on left-hand side.
    #  ---------------------------
    #
    stmt = """select * from ( select sbinneg15_nuniq from BTA1P005 )
natural join (  select sbinneg15_nuniq from BTA1P005 ) dt ;"""
    output = _dci.cmdexec(stmt)
    if hpdci.tgtSQ():
        _dci.expect_error_msg(output, '15001')
    elif hpdci.tgtTR():
        _dci.expect_selected_msg(output)

    #
    #  ---------------------------
    #       Id: JTN.24      Attempt to join row-value constructor in a NATURAL join on right-hand side.
    #  ---------------------------
    #
    stmt = """select * from ( select t1.sbinneg15_nuniq from BTA1P005 t1 ) dt
natural join  ( select t1.sbinneg15_nuniq from BTA1P005 t1 ) ;"""
    output = _dci.cmdexec(stmt)
    if hpdci.tgtSQ():
        _dci.expect_error_msg(output, '15001')
    elif hpdci.tgtTR():
        _dci.expect_selected_msg(output)
 
    _testmgr.testcase_end(desc)

def test004(desc="""a04"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     T1112:A04
    #  Description:        SQL non-transaction negative tests.
    #                      This test checks negative DEALLOCATE and RELEASE
    #                      while also exercising outer JOIN a little more.
    #
    # =================== End Test Case Header  ===================
    #
    # ---------------------------
    # Basic Negative tests for RELEASE and DEALLOCATE.
    # ---------------------------
    #
    # ---------------------------------------
    # Set up defines globally.
    # ---------------------------------------
    # Catalog for 'global database #11'.
    #
    # Schema for 'global database #11'.
    #
    #  ---------------------------
    #  Reality check: Attempt to EXECUTE a statement that has not been prepared.
    #  ---------------------------
    
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '29431')
    #
    # ---------------------------
    #      Id: DAN.01      Attempt to EXECUTE a statement that has been prepared but then RELEASE'd.
    # ---------------------------
    #
    
    stmt = """prepare s1 from
select n1
from VNA1P005 
natural join VNA1P005 t
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    #  Expected results: ((-4344) (-3552) (-2389))
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s1')
    #  Expect error: RELEASE is supported in host not SQLCI.
    stmt = """RELEASE s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    #  Expected results as above because RELEASE not supported in SQLCI.
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s3')
    #
    # ---------------------------
    #      Id: DAN.02      Attempt to EXECUTE a statement that has been prepared but then DEALLOCATE PREPARE'd.
    # ---------------------------
    #
    # Prepare another query with same statement name, but add DT.
    stmt = """prepare s1 from
select * from (
select *
from VNA1P005 
natural join VNA1P005 t
) dt
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    #  Expect 3 rows without nulls from original view.
    #     ((-4344 ...) (-3552 ...) (-2389 ...))
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s4')
    #
    #  Expect error: DEALLOCATE is supported in host not SQLCI.
    #  05/10/09 Following statement is not supported in NCI
    stmt = """DEALLOCATE PREPARE s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    #  Expected results as above because DEALLOCATE not supported in SQLCI.
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s6')
    #
    # ---------------------------
    #      Id: DAN.03      Prepare 4 statement; DEALLOCATE one, RELEASE another; attempt to each statement.
    # ---------------------------
    # Expect 3 rows without nulls from original view.
    stmt = """prepare s1 from select max(n1) from VNA1P005;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """prepare s2 from select max(c2) from VNA1P005;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """prepare s3 from select max(c3) from VNA1P005;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """prepare s4 from select max(c4) from VNA1P005;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s7')
    #
    #  Expect error: DEALLOCATE is supported in host not SQLCI.
    stmt = """DEALLOCATE PREPARE s2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    #  Expect error: RELEASE is supported in host not SQLCI.
    stmt = """RELEASE s3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    #  If the above commands were supported in SQLCI, we would
    #  no longer have statements s2, s3; in either case we expect
    #  results for s1 and s4.
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s10')
    stmt = """execute s2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s11')
    stmt = """execute s3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s12')
    stmt = """execute s4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s13')
    
    _testmgr.testcase_end(desc)

def test005(desc="""a05"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     T1112:A05
    #  Description:        SQL non-transaction negative tests.
    #                      This test verifies SQL Grouping and
    #                      Having, Grouped Views via SELECT.
    #                      Also some tests for Joins.
    #
    # =================== End Test Case Header  ===================
    #
    # ---------------------------
    # Basic Negative tests for DML on Grouped Views.
    # ---------------------------
    #
    # ---------------------------------------
    # Set up defines globally.
    # ---------------------------------------
    # Catalog for 'global database #11'.
    #
    # Schema for 'global database #11'.
    #
    #  ---------------------------
    #  Note error when attempt to use having on aggregated column;
    #  aggregation does not make a query "grouped".
    #  ---------------------------
    #
    
    #  Expect Error 4005 (The column reference CHAR17_2 must be
    #  ... or be specified within an aggregate).
    stmt = """select max (char17_2) from BTA1P005 
having char17_2 > 'A'
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4005')
    #  The above error goes away if the column in HAVING clause
    #  is made into an aggregate:
    stmt = """select max (char17_2) from BTA1P005 
having max(char17_2) > 'A'
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s1')
    #
    #  ---------------------------
    #  Attempt to Order By column outside of select and grouping list.
    #  ---------------------------
    #
    #  The first three should be ok, the fourth should give error.
    #  Order by cols.
    stmt = """select t.char17_2, sdec17_nuniq
from BTA1P005 t
order by char17_2, sdec17_nuniq
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s2')
    #
    #  Group by cols.
    stmt = """select char17_2, sdec17_nuniq
from BTA1P005 t
group by char17_2, sdec17_nuniq
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s3')
    #
    #   (97-01-31) Bogus 4001 on Group By Order By
    #  **** ERROR[ 4001]: Column SDEC17_NUNIQ not found.  Tables in scope:  T.
    #  Group by and order by cols.
    stmt = """select t.char17_2 from BTA1P005 t
group by char17_2, sdec17_nuniq
order by char17_2, sdec17_nuniq
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4121')
    #
    #  This should give error.
    #  Group by and order by different cols.
    stmt = """select t.char17_2 from BTA1P005 t
group by char17_2
order by sdec17_nuniq
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4121')
    #
    #  These should be ok.
    stmt = """select t.C2, t.C4 from VNA1P005 t
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s6')
    stmt = """select t.C4       from VNA1P005 t
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s7')
    #
    #  These should complain about Order By column not being in Select List.
    #   (97-01-31) Bogus 4001 on Group By Order By
    #  **** ERROR[ 4001]: Column T.C2 not a column of table T.
    #
    stmt = """select t.C4
from VNA1P005 t
group by t.C2, t.C4
order by t.C2, t.C4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4121')
    stmt = """select t.C4
from VNA1P005 t
group by t.C4
order by t.C2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4121')
    #
    #  Should get error because a column in select list
    #  is a non-grouping column.
    stmt = """select t.C4
from VNA1P005 t
group by t.C2
order by t.C4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4005')
    
    _testmgr.testcase_end(desc)

def test006(desc="""a06"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     T1112:A06
    #  Description:        SQL non-transaction negative tests.
    #                      This test verifies SQL INSERT
    #                      -- Error handling.
    #
    # =================== End Test Case Header  ===================
    #
    # ---------------------------
    # Choose local schema.
    # This test case will make explicit reference to global data.
    # ---------------------------
    #
    # Personal schema for this testunit.
    #
    # End of file cidefs.
    #
    stmt = """SET TRANSACTION AUTOCOMMIT ON;"""
    output = _dci.cmdexec(stmt)
    #
    # ---------------------------
    # Basic Negative tests for Row Value Constructors.
    # Before we begin, remove rows from tables that we insert into.
    # Do not remove rows from the table we are reading.
    # ---------------------------
    #
    
    stmt = """delete from TAB1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 0)
    stmt = """delete from TAB4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 0)
    stmt = """delete from TNODEF1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 0)
    stmt = """delete from TNODEF5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 0)
    #
    # ---------------------------
    #      Id: RVN.01        RVC attempts to return more than one row.
    # ---------------------------
    #
    stmt = """delete from TAB4 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 0)
    #  Expect {(5)}
    stmt = """select count(c2) from TTREAD  ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s0')
    #
    #  Expect appropriate error message.
    stmt = """select count(c2) from TTREAD 
where c2 = ( select c3 from TTREAD  )
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8401')
    #
    # Expect ok.
    stmt = """insert into TAB4  (vc9, vc5) select c2,c4
from TTREAD 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 5)
    #
    #  Expect {(5)}
    stmt = """select count(vc9) from TAB4 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s2')
    #
    # Throughout, include DELETE before moving on to next subsection,
    # to remove rows whether inserted correctly or erroneously.
    stmt = """delete from TAB4 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 5)
    #
    #  ---------------------------
    #       Id: RVN.02        RVC of lower degree than the degree of what
    #                         it is compared with; RVC is literal or
    #                         <table subquery>.
    #  ---------------------------
    #
    #  Expect appropriate error message.
    stmt = """insert into TAB4 (vc9, vc5) VALUES ('a')  ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4023')
    #
    #  Expect appropriate error message.
    stmt = """select * from TAB4 where (vc9, vc5) = ('a')  ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    #
    #  Expect appropriate error message.
    stmt = """insert into TAB4 (vc9, vc5) select max(c4)
from TTREAD 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4023')
    #
    #   (97-01-31) ??? Insert with different degrees reveals implementation
    # 		(UNION) used -- tacky.
    #   **** ERROR[ 4066]: The operands of a union must be of equal degree.
    stmt = """insert into TAB4 
VALUES ('a1','b1','c1','d1'), ('a2','b2','c2')
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4126')
    #
    #  Expect {(0)}
    stmt = """select count(vc9) from TAB4 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s7')
    stmt = """delete from TAB4 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 0)
    #
    #  ---------------------------
    #       Id: RVN.03        RVC of higher degree than the degree of what
    #                         it is compared with; RVC is literal or
    #                         <table subquery>.
    #  ---------------------------
    #
    #  Expect appropriate error message.
    stmt = """insert into TAB4 (vc9) VALUES ('a', 'b') ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4023')
    #
    #  Expect appropriate error message.
    stmt = """insert into TAB4 (vc9, vc5) select max(c2), 'z', max(c4)
from TTREAD 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4023')
    #
    #  Expect {(0)}
    stmt = """select count(vc9) from TAB4 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s10')
    stmt = """delete from TAB4 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 0)
    #
    #  ---------------------------
    #       Id: RVN.04        RVC includes data of different type from the
    #                         result it is compared with for <table subquery>
    #  ---------------------------
    #
    #  Expect appropriate error message.
    stmt = """insert into TAB4 (vc9) values (42) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4039')
    #
    #  Expect appropriate error message.
    stmt = """insert into TAB4 (vc9) select max(n1)
from TTREAD 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4039')
    #
    #  Expect {(0)}
    stmt = """select count(vc9) from TAB4 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s13')
    # 04/23/09 the return results for regular mode and mode_special_1 are different
    # adding expectfile to reflect this difference
    stmt = """delete from TAB4 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 0)
    #
    #  ---------------------------
    #       Id: RVN.05        RVC list is empty "()".
    #  ---------------------------
    #
    #  Expect appropriate error message.
    stmt = """insert into TAB4  (vc9) VALUES () ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """delete from TAB4 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 0)
    #
    #  ---------------------------
    #       Id: INN.11        INSERT result of RVC containing <subquery> of degree 1 when need more than 1.
    #                         Here the target table has 4 columns.
    #  ---------------------------
    #
    #  Expect appropriate error message.
    stmt = """INSERT INTO TAB4 VALUES (
( select min(c4) from TTREAD  )
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4023')
    #  Should work?? -- delete after sanity test!
    stmt = """INSERT INTO TAB4 VALUES (
( select min(c4), min(c4), max(c4), max(c4) from TTREAD  )
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #
    #  The following 1-row value should work on insert.
    stmt = """select min(c4) from TTREAD  ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s17')
    #
    # Expect appropriate error message.
    # (97-01-31) Bad error on attempt to execute subquery within values clause.
    # **** WARNING[ 7000]: Internal error in the code generator: valuesToBeBound.isEmpty().
    stmt = """insert into TAB1 values (
( select min(c4) from TTREAD )
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #
    #  Expect 5 rows.
    stmt = """select min('1') from TTREAD  ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s18')
    #
    # Expect appropriate error message.
    stmt = """insert into TAB1 values (
( select min('1') from TTREAD )
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #
    stmt = """delete from TAB1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 2)
    stmt = """delete from TAB4 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    #
    #  ---------------------------
    #       Id: INN.12        INSERT result of RVC containing <subquery> of degree 1 when need more than 1.
    #                         Here 2 columns are specified in the target table.
    #  ---------------------------
    #
    #  Expect appropriate error message.
    stmt = """INSERT INTO TAB4 (vc7, vc9) VALUES
( ( select min(c4) from TTREAD ) )
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4023')
    #
    #  ---------------------------
    #       Id: INN.13        INSERT result of RVC containing <subquery> of degree more than 1 when need 1.
    #  ---------------------------
    #
    #  Definition of TTREAD columns are:
    #  ( n1 integer , c2 varchar(7)
    #  , c3 char(5) , c4 varchar(4) )
    #
    #  Expect appropriate error message.
    stmt = """INSERT INTO TAB4 (vc7) VALUES (
( select min(c4), max(c4) from TTREAD  )
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4023')
    #
    #  ---------------------------
    #       Id: INN.14        INSERT result of RVC containing <subquery> of degree more than 1 (illegal whether that degree is expected or not).
    #  ---------------------------
    #
    #  Expect appropriate error message.
    stmt = """INSERT INTO TAB4 (vc7, vc9) VALUES (
( select min(c4), max(c4) from TTREAD  )
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """delete from TAB4 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    #
    # ---------------------------
    #      Id: INN.21        INSERT illegal with literals and <column name list> together.
    # ---------------------------
    #
    stmt = """set param ?paramp 'paramv' ;"""
    output = _dci.cmdexec(stmt)
    #
    #  Expect appropriate error message.
    stmt = """insert into TAB4 values (
'literal',
( select min(c4), max(c4) from TTREAD  ),
?paramp
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    stmt = """insert into TAB4 values (
'literal',
( select min(c4), max(c4) from TTREAD  ),
( select max(c4) from TTREAD  ),
?paramp
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    #
    #  Should work -- Just checking that can insert!
    # 05/10/09 following INSERT will fail in NCI since the value for the param
    # length is longer than target column length
    stmt = """insert into TAB4 values (
'literal',
( select min(c4) from TTREAD  ),
( select max(c4) from TTREAD  ),
?paramp
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    stmt = """insert into TAB4 values ( 'literal', ?paramp, 'abc', 'x' ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #
    #  Expect {(2)}
    #  5/10/09 should expect 1 since the first INSERT failed from NCI due to param
    # length
    stmt = """select count(vc9) from TAB4 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s25')
    stmt = """delete from TAB4 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    #
    #  ---------------------------
    #       Id: INN.22        Illegal to use both DEFAULT VALUES and <column name list> (<one-named-col>) in insert.
    #                         Also see 1112:A02 for
    #                         "Subquery returns > 1 row in select list."
    #  ---------------------------
    #
    #  Expect appropriate error message.
    stmt = """INSERT INTO TAB4 (vc5) DEFAULT VALUES ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """delete from TAB4 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 0)
    #
    #  ---------------------------
    #       Id: INN.23        Illegal to use both DEFAULT VALUES and <column name list> (<four-named-col>) in insert.
    #  ---------------------------
    #
    #  Expect appropriate error message.
    stmt = """INSERT INTO TAB4 (vc9 ,vc7 ,vc5 ,vc3 ) DEFAULT VALUES ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """delete from TAB4 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 0)
    #
    #  ---------------------------
    #       Id: INN.24        Illegal to INSERT DEFAULT VALUES where 1 column disallow defaults
    #  ---------------------------
    #
    #  (97-01-31) Bug in UNIX simulator, cannot make table with NO DEFAULT.
    #             Therefore get 'no such table' error falsely below.
    #
    #  Expect appropriate error message.
    stmt = """INSERT INTO TNODEF1 DEFAULT VALUES;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4024')
    stmt = """delete from TAB4 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 0)
    #
    #  ---------------------------
    #       Id: INN.25        Illegal to INSERT DEFAULT VALUES where some columns disallow defaults
    #  ---------------------------
    #
    #  (97-01-31) Bug in UNIX simulator, cannot make table with NO DEFAULT.
    #  Should see table in NT; in Sun simulator get 'no such table' error falsely below.
    #
    #  Expect appropriate error message.
    stmt = """INSERT INTO TNODEF5 DEFAULT VALUES;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4024')
    #
    #  Expect {(0)}
    stmt = """select count(vc9) from TAB4 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s30')
    stmt = """delete from TAB4 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 0)
    #
    # ---------------------------
    #      Id: UPN.01        UPDATE with <row value constructor> of too high a degree.
    # ---------------------------
    #
    # Previous system-initiated transactions are immediately committed.
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    # Insert 2 rows, to give SQL some rows to update!
    stmt = """insert into TAB4 values
('a',      'a'  ,'cc'  ,'cc' )
, ('abcdefg','cc' ,'alph','cc')
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 2)
    #
    # Expect OK.
    stmt = """UPDATE TAB4 SET vc7 = 'should', vc9 = 'work' ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 2)
    #  Expect appropriate error message.
    stmt = """UPDATE TAB4 SET vc7, vc9  = ( 'bad', 'news') ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """UPDATE TAB4 SET (vc7,vc9) = ( 'not', 'this') ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 2)
    stmt = """SELECT * from TAB4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s33')
    #
    #  Expect appropriate error message.
    stmt = """UPDATE TAB4 SET (vc7,vc9) = ( 'needs 2 values') ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4023')
    #
    #  Expect appropriate error message.
    stmt = """UPDATE TAB4 SET vc7 = ( 'literalx', 'literaly') ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """UPDATE TAB4 SET vc7 = 'literalx', 'literaly' ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """SELECT * from TAB4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s37')
    
    stmt = """rollback work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    # ---------------------------
    #      Id: UPN.11        Negative UPDATE: wrong degree of subquery in <row value constructor>.
    # ---------------------------
    #
    # Attempt to UPDATE value from a subquery of more than one element
    # (i.e. of DEGREE greater than 1):  UPDATE  <sometable>  SET c = (
    # (<select-of-degree-2>) )
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    # Insert 2 rows, to give SQL some rows to update!
    stmt = """insert into TAB4 values
('a',      'a'  ,'cc'  ,'cc' )
, ('abcdefg','cc' ,'alph','cc')
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 2)
    #
    # Should be ok.
    stmt = """UPDATE TAB4 SET vc7 = (
select ch3 from TTF 
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 2)
    #
    #  Expect appropriate error message.
    stmt = """UPDATE TAB4 SET vc7 = (
select * from TTF 
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4039')
    #
    #  Expect appropriate error message.
    stmt = """UPDATE TAB4 SET vc7 = (
select vch5, ch3 from TTF 
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4039')
    #
    #  Expect appropriate error message.
    stmt = """UPDATE TAB4 SET vc7 = (
select max(vch5), min(ch3) from TTF 
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4039')
    stmt = """rollback work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table tt (a int, b int) no partition;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into tt values (9, 0);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """values (1, 2), ((select a, b from tt));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s41')
    
    #
    # ---------------------------
    # Final reckoning; should be empty but remove rows anyway.
    # ---------------------------
    #
    stmt = """delete from TAB1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 0)
    stmt = """delete from TAB4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 0)
    stmt = """delete from TNODEF1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 0)
    stmt = """delete from TNODEF5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 0)
    
    _testmgr.testcase_end(desc)

def test007(desc="""a07"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     T1112:A07
    #  Description:        Verifies SQL Negative ANSI Transactions.
    #                      (See A09 for Update statistics).
    #
    #  Expected Results:   Correct error handling
    #
    # =================== End Test Case Header  ===================
    #
    # ---------------------------
    # Choose local schema.
    # ---------------------------
    #
    # Personal schema for this testunit.
    #
    #  End of file cidefs.
    #
    #  ---------------------------
    #  Basic COMMIT WORK *** Start no transaction before this.
    #  ---------------------------
    #    Id: TXN.03   Attempt to COMMIT WORK when no transaction has been started.
    #  ---------------------------
    #
    #  Should give error -- no transaction in progress.
    #  *** Start no transaction before this test. ***
    #
    
    stmt = """COMMIT WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8605')
    #
    #  ---------------------------
    #  Basic ROLLBACK WORK *** Start no transaction before this.
    #  ---------------------------
    #    Id: TXN.06   Attempt to ROLLBACK WORK when no transaction has been started.
    #  ---------------------------
    #
    #  Should give error -- no transaction in progress.
    #  *** Start no transaction before this test. ***
    #
    stmt = """ROLLBACK WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8609')
    #
    # ---------------------------
    # Check that needed table exists and and is empty.
    # ---------------------------
    #
    
    stmt = """delete from BTAUD ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 3)
    stmt = """select count(*) from BTAUD;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s2')
    #
    # ---------------------------
    # Basic BEGIN, COMMIT, and ROLLBACK WORK negative tests.
    # ---------------------------
    #   Id: TXN.01   Attempt to BEGIN WORK when a system transaction is already
    #                in progress through a system initiated transaction
    #                due to previous DML on an audited table.
    # ---------------------------
    #
    stmt = """SET TRANSACTION AUTOCOMMIT OFF;"""
    output = _dci.cmdexec(stmt)
    #
    # The next statement starts a transaction that remains active for
    # subsequent statements.
    stmt = """insert into BTAUD values ('abc',1), ('abd',2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 2)
    #
    #  Should give error -- transaction in progress.
    stmt = """BEGIN WORK ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8603')
    #
    #  Check contents, remove through rollback.
    #  Should be 2 rows.
    stmt = """select count(*) from BTAUD;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s4')
    #
    stmt = """ROLLBACK WORK ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    #  ---------------------------
    #       *** Start no transaction after above ROLLBACK.
    #    Id: TXN.05   Attempt to COMMIT WORK after ROLLBACK WORK.
    #  ---------------------------
    #
    #  Should give error -- no transaction in progress.
    stmt = """COMMIT WORK ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8605')
    #
    #  Should be 0 rows.
    stmt = """select count(*) from BTAUD;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s6')
    #
    # Complete transaction started by system for SELECT.
    stmt = """COMMIT WORK ;"""
    output = _dci.cmdexec(stmt)
    # _dci.expect_complete_msg(output)

    #
    #  ---------------------------
    #       *** Start no transaction after above COMMIT.
    #    Id: TXN.07   Attempt to ROLLBACK WORK immediately after a COMMIT WORK.
    #  ---------------------------
    #
    #  Should give error -- no transaction in progress.
    stmt = """ROLLBACK WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8609')
    #
    # ---------------------------
    #   Id: TXN.02   Attempt to BEGIN WORK when user transaction is in progress.
    # ---------------------------
    #
    # Start a user transaction.
    stmt = """BEGIN WORK ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    #  Attempt to start another user transaction.
    #  Should give error.
    stmt = """BEGIN WORK ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8603')
    #
    # Complete transaction started by user.
    stmt = """COMMIT WORK ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    #  ---------------------------
    #       *** Start no transaction after above COMMIT.
    #    Id: TXN.04   Attempt to COMMIT WORK after COMMIT WORK.
    #  ---------------------------
    #
    #  Should give error -- no transaction in progress.
    stmt = """COMMIT WORK ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8605')
    #
    # ---------------------------
    #   Id: TXN.08   Attempt to ROLLBACK WORK immediately after another ROLLBACK WORK.
    # ---------------------------
    #
    # Delete any rows, then insert.
    stmt = """delete from BTAUD ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 0)
    stmt = """insert into BTAUD values ('abe',3) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #
    #  Check contents, remove through rollback.
    #  Should be 2 rows.
    stmt = """select count(*) from BTAUD;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s10')
    stmt = """ROLLBACK WORK ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    #  Rollback after rollback should give error -- no transaction in progress.
    stmt = """ROLLBACK WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8609')
    #
    # ---------------------------
    # Should not get system transaction started for these DCL statements:
    # ---------------------------
    #
    # ---------------------------
    #   Id: TXN.09a  FREE RESOURCES removed from test;
    #                not supported in 1998 release.
    # ---------------------------
    #
    # ---------------------------
    #   Id: TXN.09b  LOCK TABLE starts system transaction (as of 980301).
    # ---------------------------
    #
    stmt = """LOCK TABLE BTAUD IN SHARE MODE;"""
    output = _dci.cmdexec(stmt)
    # TRAF TODO _dci.expect_complete_msg(output)
    #
    # Should succeed -- transaction in progress.
    stmt = """COMMIT WORK ;"""
    output = _dci.cmdexec(stmt)
    # TRAF TODO _dci.expect_complete_msg(output)
    #
    # ---------------------------
    #   Id: TXN.09c  UNLOCK TABLE starts system transaction (as of 980301).
    # ---------------------------
    #
    stmt = """UNLOCK TABLE BTAUD;"""
    output = _dci.cmdexec(stmt)
    # TRAF TODO _dci.expect_complete_msg(output)
    #
    # Should succeed -- transaction in progress.
    stmt = """COMMIT WORK ;"""
    output = _dci.cmdexec(stmt)
    # TRAF TODO _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test008(desc="""a08"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     T1112:A08
    #  Description:        Verifies SQL Negative ANSI Transactions.
    #
    #  Expected Results:   Correct error handling
    #
    # =================== End Test Case Header  ===================
    #
    # ---------------------------
    # Choose local schema.
    # ---------------------------
    #
    # Personal schema for this testunit.
    #
    # End of file cidefs.
    #
    # ---------------------------
    # Remove any data in needed tables, which should exist and
    # be empty.
    # ---------------------------
    #
    
    stmt = """delete from BTAUD ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 0)
    stmt = """select count(*) from BTAUD;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s0')
    #
    # ---------------------------
    # SET TRANSACTION Negative tests
    # ---------------------------
    #   Id: TXN.11   SET TRANSACTION is illegal within an active transaction
    # ---------------------------
    #
    # BEGIN user transaction.
    stmt = """BEGIN WORK ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8603')
    #
    # Should give error -- transaction in progress.
    # 06/01/09 it is allowed to set transaction from JDBC/ODBC within transaction
    stmt = """SET TRANSACTION READ ONLY;"""
    output = _dci.cmdexec(stmt)
    # Should give error -- transaction in progress.
    stmt = """SET TRANSACTION READ WRITE;"""
    output = _dci.cmdexec(stmt)
    #
    # End user transaction then begin system transaction through DML.
    stmt = """COMMIT WORK ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    # Should be able to read and write (i.e. not limited to Read only).
    # Delete any rows (shouldn't be any), then insert.
    stmt = """delete from BTAUD ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 0)
    stmt = """insert into BTAUD values ('abf',4), ('abf',5), ('ab',6) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 3)
    stmt = """select count(*) from BTAUD;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    #
    # ---------------------------
    # Cleanup.
    # ---------------------------
    # Note -- don't remove table until TU cleanup.
    stmt = """delete from BTAUD ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 3)
    
    _testmgr.testcase_end(desc)

def test009(desc="""a09"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     T1112:A09
    #  Description:        Verifies SQL Negative ANSI Transactions.
    #
    #  Expected Results:   Correct error handling
    #
    # =================== End Test Case Header  ===================
    #
    # ---------------------------
    # Choose local schema.
    # ---------------------------
    #
    # Personal schema for this testunit.
    #
    # End of file cidefs.
    # ---------------------------
    # Remove any data in needed tables, which should exist and
    # be empty.
    # ---------------------------
    #
    
    stmt = """set transaction autocommit off;"""
    output = _dci.cmdexec(stmt)
    stmt = """set transaction autocommit on;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """delete from BTAUD ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 0)
    
    stmt = """select count(*) from BTAUD;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s0')
    
    #
    # ---------------------------
    # SET TRANSACTION Negative tests
    # ---------------------------
    #   Id: TXN.12   SET TRANSACTION <conflicting isolation levels>
    # ---------------------------
    #
    # Should give error -- conflicting isolation levels.
    stmt = """SET TRANSACTION ISOLATION LEVEL READ COMMITTED, REPEATABLE READ ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED, SERIALIZABLE  ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #
    # ---------------------------
    #   Id: TXN.13   SET TRANSACTION <list of conflicting transaction access mode>
    # ---------------------------
    #
    # Should give error -- conflicting transaction access mode.
    stmt = """SET TRANSACTION ISOLATION LEVEL READ ONLY, READ WRITE ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #
    # ---------------------------
    #   Id: TXN.14   SET TRANSACTION <list of transaction-access-modes-without-comma-delimiter >
    # ---------------------------
    #
    # Should give syntax error.
    stmt = """SET TRANSACTION READ WRITE  REPEATABLE READ ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    #
    # ---------------------------
    #   Id: TXN.15   SET TRANSACTION does not start a transaction
    # ---------------------------
    #
    # 06/01/09 set transaction is allowed within transaction from JDBC/ODBC
    stmt = """SET TRANSACTION READ WRITE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    #  Should give error -- no transaction in progress.
    stmt = """COMMIT WORK ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    # ---------------------------
    #   Id: TXN.16   SET TRANSACTION DIAGNOSTICS SIZE # -- illegal in SQLCI
    # ---------------------------
    #
    # Should give syntax error.
    stmt = """SET TRANSACTION DIAGNOSTICS SIZE ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """SET TRANSACTION DIAGNOSTICS SIZE 100;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    # ---------------------------
    # Cleanup.
    # ---------------------------
    # Note -- don't remove table until TU cleanup.
    stmt = """delete from BTAUD ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 0)
    
    _testmgr.testcase_end(desc)

def test010(desc="""a10"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     T1112:A10
    #  Description:        Verifies SQL Negative ANSI Transactions.
    #                      for Update statistics.
    #
    #  Expected Results:   Correct error handling.
    #
    # =================== End Test Case Header  ===================
    #
    # ---------------------------
    # Choose local schema.
    # ---------------------------
    #
    # Personal schema for this testunit.
    #
    # End of file cidefs.
    #
    # ---------------------------
    # Check that needed table exists and is empty.
    # ---------------------------
    #
    
    # Ensure that transactions get committed.
    stmt = """SET TRANSACTION AUTOCOMMIT ON;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """delete from BTAUD ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 0)
    stmt = """select count(*) from BTAUD;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s0')

    stmt = """SET TRANSACTION AUTOCOMMIT OFF;"""
    output = _dci.cmdexec(stmt)
    #
    # ---------------------------
    # Should not get system transaction started for DSL statements:
    # ---------------------------
    #
    # ---------------------------
    #   Id: TXN.10   UPDATE STATISTICS should not start system transaction.
    #                Replaces original "UPDATE HISTOGRAM STATISTICS".
    # ---------------------------
    #
    stmt = """UPDATE STATISTICS FOR TABLE BTAUD ;"""
    output = _dci.cmdexec(stmt)
    # TRAF TODO _dci.expect_complete_msg(output)
    #
    #  Should give error -- no transaction in progress.
    stmt = """COMMIT WORK ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8605')
    #
    # UPDATE HISTOGRAM STATISTICS FOR TABLE BTAUD ;
    stmt = """UPDATE STATISTICS FOR TABLE BTAUD ;"""
    output = _dci.cmdexec(stmt)
    # TRAF TODO _dci.expect_complete_msg(output)
    #
    #  Should give error -- no transaction in progress.
    stmt = """COMMIT WORK ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8605')
    #
    # Put some rows into the table and UPDATE statistics again.
    stmt = """insert into BTAUD values ('abe',3)
, ('abf',4)
, ('abg',5)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 3)
    stmt = """COMMIT WORK ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    stmt = """UPDATE STATISTICS FOR TABLE BTAUD ;"""
    output = _dci.cmdexec(stmt)
    # TRAF TODO _dci.expect_complete_msg(output)
    #
    #  Should give error -- no transaction in progress.
    stmt = """COMMIT WORK ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8605')
  
    # reset auto-commit 
    stmt = """SET TRANSACTION AUTOCOMMIT ON;"""
    output = _dci.cmdexec(stmt)
 
    _testmgr.testcase_end(desc)

def test011(desc="""a11"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt1112:A11
    #  Description:        This verifies the SQL CASE feature
    #                      negative tests for attempts to use multi-column
    #                      subquery to provide Row Value Constructor where
    #                      should have scalar value.
    #
    #  Expected Results:   Correct error handling
    #
    # =================== End Test Case Header  ===================
    #
    # ---------------------------
    # Choose local schema.
    # ---------------------------
    #
    # Personal schema for this testunit.
    #
    #  End of file cidefs.
    #
    
    stmt = """select * from tbl1 order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s0')
    stmt = """select * from tbl3 order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s1')
    #
    #  Expect error [4019] The select list of a subquery in a select
    #  list must be scalar (degree of one).
    stmt = """select (
select distinct max(t.l_name)
, case t.mar_status
when 1 then 'single'
else 'unknown'
end
from tbl3 t
where t.l_name = 'crinar'
group by t.l_name, t.mar_status
)
from tbl1 
;"""
    output = _dci.cmdexec(stmt)
    if hpdci.tgtSQ():
        _dci.expect_error_msg(output, '4019')
    elif hpdci.tgtTR():
        _dci.expect_selected_msg(output)
    #  This also should give the error [4019].
    stmt = """select (
select distinct 1,2 from tbl3 t
) from tbl3 
;"""
    output = _dci.cmdexec(stmt)
    if hpdci.tgtSQ():
        _dci.expect_error_msg(output, '4019')
    elif hpdci.tgtTR():
        _dci.expect_selected_msg(output)
    #
    #  ---------------------------------
    #  Separated out from testcase 1101.A01 (test area CA.101b)
    #  because of a bug that cause an Error popup window.
    #  ---------------------------------
    #
    #  Components of query below.
    #  (1) Expect ( ( 37000 ) ( 175500 ) )
    stmt = """select salary from tbl1 
where dept_num = 9000
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s4')
    
    #  (2) Expect ( ( 2 ) ( 2 ) )
    stmt = """select case marital_status
when 2 then marital_status
else  marital_status - 1
end
from tbl1 where dept_num = 9000 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s5')
    #
    #  Expect error [8401] A row subquery or SELECT...INTO statement
    #  cannot return more than one row.
    stmt = """select last_name from tbl1 
where (case when salary > 60000
then salary
else salary * 1.5
end
, 2)
<= ( (select salary from tbl1 
where dept_num = 9000)
,(select case marital_status
when 2 then marital_status
else  marital_status - 1
end
from tbl1 where dept_num = 9000)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8401')
    #
    #  Query below with constant instead of last case.
    #  Expect error [8401] A row subquery or SELECT...INTO statement
    #  cannot return more than one row.
    stmt = """select last_name from tbl1 
where (case when salary > 60000
then salary
else salary * 1.5
end
, 2)
<= ( (select salary from tbl1 
where dept_num = 9000)
,(2)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8401')
    #
    #  Query below with constant everywhere.
    #  Expect 4 names as in base table.
    stmt = """select last_name from tbl1 
where (1
, 2)
<= ( 1
,(2)
)
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s8')
    
    _testmgr.testcase_end(desc)

