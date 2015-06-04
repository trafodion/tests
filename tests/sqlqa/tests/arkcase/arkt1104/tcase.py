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
    #  Test case name:     T1104:A01
    #
    #  See file arkt1104/testa01.b4q for version of this test before
    #  testscript separated into a file to leverage for partitioned
    #  as well as non-partitioned data.
    #
    # =================== End Test Case Header  ===================
    #
    # Force autocommit:
    stmt = """SET transaction Autocommit on;"""
    output = _dci.cmdexec(stmt)
    #
    # ---------------------------
    # Parameter(s).
    # ---------------------------
    stmt = """set param ?paramA A;"""
    output = _dci.cmdexec(stmt)
    #
    #  ---------------------------
    #  DML on Grouped View containing GROUP BY (Select from
    #  View VNA1P002 in various contexts)
    #  ---------------------------
    #
    #  ---------------------------
    #       Id: GV.004      'GROUP BY' view and Aggregates (some of AVG,
    #                          COUNT, MAX, MIN, SUM, included as
    #                          multiple aggregates used on different
    #                          columns).
    #  ---------------------------
    #
    #  Should show 7 rows as in base table.
    stmt = """select cast(CHAR17_100 as char(20)) ,UDEC17_100
from """ + gvars.g_schema_arkcasedb + """.VNA1P002 
order by 1,2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s0')
    #
    #  Includes duplicate at 'CCAAAAAAAAAAAAAA', so expect :
    #     ( ( 7 AWAAAAAAAAAAAAAA DMAAAAAAAAAAAAAA 6 ) )
    stmt = """select cast(count(CHAR17_100) as smallint) as count1
, cast(min(CHAR17_100) as char(20)) as min1
, cast(max(CHAR17_100) as char(20)) as max1
, cast(count(distinct CHAR17_100) as smallint)
as count_distinct
from """ + gvars.g_schema_arkcasedb + """.VNA1P002 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s1')
    #
    #  Expect 6 rows (omitting one duplicate value of
    #  'CCAAAAAAAAAAAAAA'.)
    stmt = """select cast(CHAR17_100 as char(20))
from """ + gvars.g_schema_arkcasedb + """.VNA1P002 group by CHAR17_100
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s2')
    stmt = """select count(CHAR17_100) as char_count
, cast(min(CHAR17_100) as char(20)) as char_min
, cast(max(CHAR17_100) as char(20)) as char_max
, count(distinct CHAR17_100) as char_count_D
from """ + gvars.g_schema_arkcasedb + """.VNA1P002 
group by CHAR17_100
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s3')
    #
    #  Expect: ( ( 16  85  7 ) )
    stmt = """select min(UDEC17_100)
, max(UDEC17_100)
, count(distinct UDEC17_100)
from """ + gvars.g_schema_arkcasedb + """.VNA1P002 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s4')
    #  Expect: ( ( 7  333  1 ) )
    stmt = """select cast(count(UDEC17_100) as smallint)
, cast(sum(UDEC17_100) as int)
, (sum(UDEC17_100)/count(UDEC17_100))/(avg(UDEC17_100)) as IsItOne
from """ + gvars.g_schema_arkcasedb + """.VNA1P002 
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s5')
    #
    #  Expect: ( ( 7  333  333 ) )
    #  ----------------
    #  Bug in division? (a) rounding (b) width
    #  ----------------
    stmt = """select cast(count(UDEC17_100) as smallint)
, sum(UDEC17_100)
, cast((sum(UDEC17_100)/count(UDEC17_100))/(avg(UDEC17_100))
as int) as IsIt333
from """ + gvars.g_schema_arkcasedb + """.VNA1P002 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s6')
    stmt = """select cast(count(UDEC17_100) as smallint)
, sum(UDEC17_100)
, cast((sum(UDEC17_100)/count(UDEC17_100))/(avg(UDEC17_100))
as numeric(9,1) ) as IsIt333
from """ + gvars.g_schema_arkcasedb + """.VNA1P002 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s7')
    #
    #  Expect: ( ( 7  333  1) )
    stmt = """select cast(count(UDEC17_100) as smallint)
, cast(sum(UDEC17_100) as int)
, cast( 7 * avg(UDEC17_100) as int) as IsIt333
from """ + gvars.g_schema_arkcasedb + """.VNA1P002 
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s8')
    
    # debug:
    stmt = """explain options 'f'
select cast(CHAR17_100 as CHARACTER)
from """ + gvars.g_schema_arkcasedb + """.VNA1P002 
group by CHAR17_100
order by 1
;"""
    output = _dci.cmdexec(stmt)
    stmt = """select cast(CHAR17_100 as CHARACTER)
from """ + gvars.g_schema_arkcasedb + """.VNA1P002 
group by CHAR17_100
order by 1
;"""
    output = _dci.cmdexec(stmt)
    #
    #  ---------------------------
    #       Id: GV.005      GROUP BY upon 'GROUP BY' view
    #       Id: GV.008      UNION upon 'GROUP BY' view
    #  ---------------------------
    #
    #  6 rows (same for cast as CHARACTER(1) because can only GROUP BY
    #  column, not expression (e.g. cannot have 'Group By cast(...)' )
    #  Expect initial characters omitting duplicate full value:
    #  ( (A) (B) (C) (C) (D) (D) )
    stmt = """select cast(CHAR17_100 as CHARACTER)
from """ + gvars.g_schema_arkcasedb + """.VNA1P002 
group by CHAR17_100
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '8402')
    
    #
    #  Expect all 7 rows.
    stmt = """select cast(CHAR17_100 as CHARACTER(16) )
, UDEC17_100
from """ + gvars.g_schema_arkcasedb + """.VNA1P002 
group by CHAR17_100, UDEC17_100
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s10')
    #
    #  Expect ( (1 1) * 5, (4 4) )
    stmt = """select count(v1.CHAR17_100)
, count(v2.CHAR17_100)
from """ + gvars.g_schema_arkcasedb + """.VNA1P002 v1
left join """ + gvars.g_schema_arkcasedb + """.VNA1P002 v2
on v1.CHAR17_100 = v2.CHAR17_100
group by v1.CHAR17_100, v2.CHAR17_100
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s11')
    #
    #  Expect 7 rows (max 'DM...' appears twice, duplicate 'CC...' only once)
    stmt = """select cast(CHAR17_100 as CHARACTER(16) )
from """ + gvars.g_schema_arkcasedb + """.VNA1P002 v1
group by CHAR17_100
union all
select max( cast(CHAR17_100 as CHARACTER(16) ))
from """ + gvars.g_schema_arkcasedb + """.VNA1P002 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s12')
    #
    #  Expect 6 rows (no duplicate)
    stmt = """select cast(CHAR17_100 as CHARACTER(16) )
from """ + gvars.g_schema_arkcasedb + """.VNA1P002 v1
group by CHAR17_100
union
select cast(max(CHAR17_100) as CHARACTER(16))
from """ + gvars.g_schema_arkcasedb + """.VNA1P002 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s13')
    #
    #  Expect 4 rows ( 'CBA..', 'CCA..', 'DDA..', 'DMA..', no duplicate )
    stmt = """select  cast(CHAR17_100 as CHARACTER(16) )
from """ + gvars.g_schema_arkcasedb + """.VNA1P002 v1
group by CHAR17_100
having CHAR17_100 > 'BZZ'
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s14')
    #
    #  Expect 4 rows ( ( 1 1 ) * 3 ( 4 4 ) )
    stmt = """select count(v1.CHAR17_100) , count(v2.CHAR17_100) from """ + gvars.g_schema_arkcasedb + """.VNA1P002 v1
left join """ + gvars.g_schema_arkcasedb + """.VNA1P002 v2
on v1.CHAR17_100 = v2.CHAR17_100
group by v2.CHAR17_100
having v2.CHAR17_100 > 'BZZ'
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s15')
    #
    #  Note that it's an error to attempt to use having on aggregated
    #  column; aggregation does not make a query "grouped". Therefore,
    #  the following is executed in negative tests:
    #     select max(CHAR17_100) from VNA1P002
    #        having CHAR17_100 > 'BZZ'
    #     ;
    #  Expect 4 rows ( 'CBA..', 'CCA..', 'DDA..', 'DMA..', no duplicate )
    stmt = """select cast(CHAR17_100 as CHARACTER(16) )
from """ + gvars.g_schema_arkcasedb + """.VNA1P002 v1
group by CHAR17_100
having CHAR17_100 > 'BZZ'
union
select cast(max(CHAR17_100) as CHARACTER(16) )
from """ + gvars.g_schema_arkcasedb + """.VNA1P002 
group by CHAR17_100
having CHAR17_100 > 'BZZ'
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s16')
    #
    #  Expect 8 rows ( 'CBA..', 'CCA..', 'DDA..', 'DMA..', all duplicated ).
    stmt = """select cast(CHAR17_100 as CHARACTER(16) )
from """ + gvars.g_schema_arkcasedb + """.VNA1P002 v1
group by CHAR17_100
having CHAR17_100 > 'BZZ'
union all
select cast(max(CHAR17_100) as CHARACTER(16) )
from """ + gvars.g_schema_arkcasedb + """.VNA1P002 
group by CHAR17_100
having CHAR17_100 > 'BZZ'
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s17')
    #
    #  ---------------------------
    #       Id: GV.007      'GROUP BY' view and WHERE clause
    #  ---------------------------
    #
    #  Expect :
    #     ( ( 16  78  6 ) )
    stmt = """select min(UDEC17_100) , max(UDEC17_100)
, count(distinct UDEC17_100)
from """ + gvars.g_schema_arkcasedb + """.VNA1P002 
where UDEC17_100 <> 85
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s18')
    #
    #  Expect 2 rows ( 'CBA..', 'CCA..', no duplicates )
    stmt = """select cast(CHAR17_100 as CHARACTER(16) )
from """ + gvars.g_schema_arkcasedb + """.VNA1P002 v1
where  CHAR17_100 < 'CAZ'
group by CHAR17_100
having CHAR17_100 > 'BZZ'
union all
select cast( max(CHAR17_100) as CHARACTER(16) )
from """ + gvars.g_schema_arkcasedb + """.VNA1P002 
where  CHAR17_100 < 'DAZ'
group by CHAR17_100
having CHAR17_100 > 'BZZ'
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s19')
    
    _testmgr.testcase_end(desc)

def test002(desc="""a02"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     T1104:A02
    #  Description:        This test verifies SQL Grouped Views
    #                      via SELECT. Insert and Update tables using
    #                      values from Grouped Views; use of set
    #                      functions on Grouped Views 
    #
    # =================== End Test Case Header  ===================
    #
    # Force autocommit:
    stmt = """SET transaction Autocommit on;"""
    output = _dci.cmdexec(stmt)
    # ---------------------------
    # DML on View containing Grouped View; check results.
    # ---------------------------
    # Create view on columns such that their values omit duplicate rows.
    
    stmt = """create view V1A as select vch7 , ch3 , nnum5 , vch5
from T1A 
group by ch3 , nnum5 , vch5, vch7
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #  Expect 5 rows.
    stmt = """select * from V1A 
order by 1,2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s0')
    #
    # Create view on view.
    stmt = """create view V1B as select ch3 , vch5
from V1A 
group by ch3 , vch5
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #  Expect 4 rows.
    stmt = """select CH3 as C, VCH5 as V
from V1B 
order by 1,2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s1')
    #
    #  ---------------------------
    #       Id: GV.031      Inner Join on nested grouped views.
    #       Id: GV.033      Order By   on nested grouped views.
    #  ---------------------------
    #
    #  Expect 4 rows: (('c' 'c') ('c' 'c') ('cc' 'cc') ('cc' 'cc'))
    stmt = """select v1.ch3, v2.vch5 from V1B v1 join V1B v2
on v1.ch3 = v2.vch5
order by 1,2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s2')
    #
    #  Expect 8 rows: ((4*('c' 'cc') ('cC' 'c') 2*('cC' 'cc') ('cc' 'c'))
    stmt = """select v1.ch3, v2.vch5 from V1B v1 inner join V1B v2
on v1.ch3 <> v2.vch5
order by 1,2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s3')
    #
    #  ---------------------------
    #       Id: GV.034      Aggregates on nested grouped views.
    #       Id: GV.051      Concatenate string literals with char and varchar data from a grouped view.
    #       Id: GV.052      Concatenate string literals with char and varchar data within grouped view
    #  ---------------------------
    #
    #  Should get spaces to pad out fixed-length character variable with
    #  spaces; should get no extra padding spaces after varchar.
    #
    #  Expect 1 row ( 'cc ----c'  'cc----c'  'cc----cc'  'c----c'  4   3)
    
    stmt = """select max(ch3) || '----' || min(vch5) as xch_nvch
, max(vch5)|| '----' || min(ch3)    as xvch_nch
, max(vch5 || '----' || ch3)        as x_vch_ch
, min(vch5 || '----' || ch3)        as n_vch_ch
, cast(count(ch3) as smallint)      as countC
, cast(count(vch5) as smallint)     as countV
from V1B 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s4')
    
    #  Expect 4 rows (('c  ----c' 'c----c' 'c.' 1)
    #     ('cC ----cc' 'cc----cC' 'cc.' 2)
    #     ('cc ----cc' 'cc----cc' 'cc.' 2)
    #     (nulls))
    
    stmt = """select ch3 || '----' || vch5 as ch_vch
, vch5 || '----' || ch3   as vch_ch
, vch5||'.' as vDot
, cast(char_length(vch5) as smallint) as L_vch
from V1B 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s5')
    #
    #  Expect 4 rows.
    stmt = """select vch5 || '----' || ch3 as vch_ch
, ch3 || '----' || vch5   as ch_vch
, cast(char_length(vch5) as smallint) as lenV
, cast(char_length(ch3)  as smallint) as lenC
, cast(char_length(vch5||ch3) as smallint) as lenVC
from V1B 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s6')
    #
    
    stmt = """create view V1C (xch_nvch, xvch_nch, x_vch_ch, n_vch_ch, Cch, Cvch) as
select max(ch3)  || '----' || min(vch5)
, max(vch5) || '----' || min(ch3)
, max(vch5 || '----' || ch3)
, min(vch5 || '----' || ch3)
, cast(count(ch3) as smallint)
, cast(count(vch5) as smallint)
from V1B 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #  Expect 1 row ( 'cc ----c'  'cc----c'  'cc----cc'  'c----c'  4   3 )
    stmt = """select xch_nvch, xvch_nch, x_vch_ch, n_vch_ch, cast(Cch as smallint),
cast(Cvch as smallint)
from V1C 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s7')
    #
    stmt = """create view V1D (a,b,c,d) as
select max(ch3)  || '----' || min(vch5)
, max(vch5) || '----' || min(ch3)
, max(vch5 || '----' || ch3)
, min(vch5 || '----' || ch3)
from V1B 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    #  Expect 1 row ( 'cc ----c'  'cc----c'  'cc----cc'  'c----c' )
    stmt = """select * from V1D order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s8')
    #
    #  ---------------------------
    #       Id: GV.032      Outer join on nested grouped views.
    #       Id: GV.035      'GROUP BY' on nested grouped views.
    #  ---------------------------
    #
    #  Expect 3 rows (('c') ('cC') ('cc'))
    stmt = """select ch3 from V1B group by ch3
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s9')
    #  Expect 3 rows (('c') ('cc') (NULL))
    stmt = """select vch5 from V1B group by vch5
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s10')
    #
    #  Add outer join.
    #  Expect 5 rows ( ('c' 'c') ('c' 'c') ('cc' 'cc') ('cc' 'cc') (? ?) )
    stmt = """select t.vch5, u.ch3
from V1B t
left join V1B u
on t.vch5 = u.ch3
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s11')
    #
    #  Another outer join.
    #  Scaffold.
    #  Expect (('c' 'c' 'c' 'c')
    #          ('c' NULL 'c' 'c')
    #          ('cC' 'cc' NULL NULL)
    #          ('cc' 'cc' 'cC' 'cc')
    #          ('cc' 'cc' 'cc' 'cc'))
    stmt = """select t.ch3, t.vch5, u.ch3, u.vch5
from V1B t
left join V1B u
on t.ch3 = u.vch5
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s12')
    #
    #  Expect (('c' 'c')
    #          ('cc' 'cC')
    #          ('cc' 'cc')
    #          ('cc' NULL)
    #          (NULL 'c' ))
    stmt = """select t.vch5, u.ch3
from V1B t
left join V1B u
on t.ch3 = u.vch5
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s13')
    stmt = """insert into TEMPT select ch3, vch5 from V1B;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 4)
    #
    #  Expect 4 rows.
    stmt = """select * from TEMPT 
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s14')
    stmt = """delete from TEMPT ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 4)
    #
    #  ---------------------------
    #       Id: GV.036      'HAVING' on nested grouped views.
    #  ---------------------------
    #
    #  Expect (('c' 'c') ('cc' 'cc'))
    stmt = """select t.vch5, u.ch3
from V1B t, V1B u
group by t.vch5, u.ch3
having t.vch5 = u.ch3
order by 1,2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s15')
    #
    #  ---------------------------
    #       Id: GV.037      'WHERE' on nested grouped views.
    #  ---------------------------
    #
    #  Expect (('c' 'c' 'c' 'c')
    #          ('c' 'c' 'c' NULL)
    #          ('cC' 'cc' 'cc' 'cc')
    #          ('cc' 'cc' 'cc' 'cc'))
    stmt = """select t.ch3 as t_ch3, t.vch5 as t_vch5
, u.ch3 as u_ch3, u.vch5 as u_vch5
from V1B t, V1B u
where t.vch5 = u.ch3
order by 1,2,3,4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s16')
    #
    #  ---------------------------
    #       Id: GV.038      'UNION' on nested grouped views.
    #  ---------------------------
    #
    #  Expect 4 rows.
    #  Expect (('c') ('cC') ('cc') (NULL))
    stmt = """select ch3 from V1B 
union
select vch5 from V1B 
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s17')
    #
    #  Expect 8 rows.
    #  Expect (3*('c') ('cC') 3*('cc') (NULL))
    stmt = """select vch5 from V1B 
union all
select ch3 from V1B 
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s18')
    #
    # ---------------------------
    # Drop View created in this script.
    # Done in postTxxx.
    # ---------------------------
    # ---------------------------
    # Drop Views created in this test case.
    # Note the order -- views that depend upon others must be
    # removed first as the "drop" does not cascade from a view
    # (nor a table) to its dependents.
    # ---------------------------
    # Remove this later!
    stmt = """drop view V1D ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view V1C ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view V1B ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view V1A ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test003(desc="""a03"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     T1104:A03
    #
    #  See file arkt1104/testa03.b4q for version of this test before
    #  testscript separated into a file to leverage for partitioned
    #  as well as non-partitioned data.
    #
    # =================== End Test Case Header  ===================
    #
    # Force autocommit:
    stmt = """SET transaction Autocommit on;"""
    output = _dci.cmdexec(stmt)
    #
    #  ---------------------------
    #  ANSI string functions on data from Grouped Views
    #  VNA1P002, VNA1P004, VNA1P005
    #  ---------------------------
    #
    #  Check view values.
    #  Expect 12 rows.
    
    stmt = """select varchar0_4
, varchar5_10
, char6_20
, varchar15_uniq
, char16_uniq
from VNA1P004 
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s0')
    #
    #  Expect 6 rows:
    #  N1      C2  C3  C4
    #  ------  --  --  --------
    #
    #   -4344  AA  BA  BA
    #   -3552  BA  AA  AA
    #   -2789  DA  EA         ?
    #   -2389  BA  AA  AA
    #       ?   ?  BA  BA
    #       ?   ?  DA  DA
    stmt = """select * from VNA1P005 order by N1, C3 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s1')
    #
    #  ---------------------------
    #       Id: GV.061a     Upon grouped view, UPPER and LOWER string functions on varchar columns.
    #  ---------------------------
    #
    #  Expect (('A' 'acaaa' 'BEAAGAAC')
    #          ('A' 'aeaaaaa' 'FJAAGAA')
    #          ('AAA' 'abaaaaaa' 'FGAAAAAB'))
    stmt = """select upper(lower(varchar0_4)) as u_l_v
, lower(varchar5_10)         as l_v
, upper(varchar15_uniq)      as u_v
from VNA1P004 
where lower(varchar0_4) < 'b'
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s2')
    #
    #  ---------------------------
    #       Id: GV.061b     Upon grouped view, Arithmetic upon CHAR_LENGTH of Concatenated char and varchar columns.
    #  ---------------------------
    #
    #  Expect 12 rows, with fixed-length chars and variable-length varchars.
    #  ABEAAGAACBEAAGAAC     A           BEAAGAAC     BEAAGAAC
    #  to
    #  AFJAAGAAEFJAAGAA      A           FJAAGAAE     FJAAGAA
    stmt = """select varchar0_4||char16_uniq||varchar15_uniq
, varchar0_4, char16_uniq, varchar15_uniq
from VNA1P004 
order by char16_uniq,varchar0_4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s3')
    #
    #  Expect 12 rows, with fixed-length chars and variable-length varchars.
    stmt = """select char_length(varchar0_4||char16_uniq||varchar15_uniq) as Len_concat
, char_length(varchar0_4) as Len_varchar0
, char_length(char16_uniq) as Len_char16
, char_length(varchar15_uniq) as Len_varchar15
, char_length(varchar0_4) + char_length(char16_uniq)
+ char_length(varchar15_uniq) as Sum_Len
from VNA1P004 
order by char16_uniq
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s4')
    #
    #  ---------------------------
    #       Id: GV.061c     Upon grouped view, Arithmetic upon OCTET_LENGTH of Concatenated char and varchar columns.
    #  ---------------------------
    #
    #  Expect 12 rows, with fixed-length chars and variable-length varchars.
    #  ABAAAAAAFGAAAAABABAAAAAA   ABAAAAAA  FGAAAAAB        ABAAAAAA
    #  or
    #  AM      BEAAGAACAM         AM        BEAAGAAC        AM
    stmt = """select char6_20||varchar15_uniq||varchar5_10
,char6_20
,varchar15_uniq
,varchar5_10
from VNA1P004 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s5')
    #
    #  Expect 12 rows, with fixed-length chars and variable-length varchars.
    #         18       8       8       2       18
    #  to
    #         24       8       8       8       24
    stmt = """select octet_length(char6_20||varchar15_uniq||varchar5_10)
as len_concat
,cast(octet_length(char6_20) as smallint)       as L1
,cast(octet_length(varchar15_uniq) as smallint) as L2
,cast(octet_length(varchar5_10) as smallint)    as L3
,cast(octet_length(char6_20)
+ octet_length(varchar15_uniq)
+ octet_length(varchar5_10)
as smallint) as sum_len
from VNA1P004 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s6')
    #
    #  ---------------------------
    #       Id: GV.061d     Upon grouped view, POSITION of literal in varchar
    #  ---------------------------
    #
    #  Condition on column on Right of Left Join.
    #  Expect 24 rows, cross-product of 2 VNA1P005 rows where c3 starts
    #  with B, and all 12 of VNA1P004.
    #  AA  BA  BEAAGAAC                 0                    1
    #  to
    #   ?  BA  FJAAGAA                  ?                    0
    stmt = """select c2, c3
, varchar15_uniq
, position ( 'B' in c2 )             as B_in_C2
, position ( 'B' in varchar15_uniq ) as B_in_varchar15_uniq
from VNA1P004 t4 left join VNA1P005 t5
on position ( 'B' in c3 ) = 1
order by c2, varchar15_uniq
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s7')
    #
    #  Condition on column on Left of Left Join.
    #  Expect 17: all 6 rows from Right table of Left join, for 1 row in Left
    #  table that satisfies ON condition; plus the other 11 rows for Left table.
    #  AA  BA  BA        FGAAAAAB                 0                    8
    #  to
    #   ?   ?         ?  FJAAGAA                  ?                    0
    stmt = """select c2, c3, c4
, varchar15_uniq
, position ( 'B' in c2 )             as B_in_C2
, position ( 'B' in varchar15_uniq ) as B_in_varchar15_uniq
from VNA1P004 t4 left join VNA1P005 t5
on position ( 'B' in varchar15_uniq ) = 8
order by c2, c3, varchar15_uniq
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s8')
    #
    #  Condition on column on each side of Left Join.
    #  Expect 25: 4 rows (from Right Table) match on position=0 ;
    #   20 (2*10) rows match on position=1;
    #   and 1 non-match (null extension) for position=8.
    #  BA  AA  AA        FJAAGAA                  0                    0
    #  to
    #   ?   ?         ?  FGAAAAAB                 ?                    8
    stmt = """select c2, c3, c4
, varchar15_uniq
, position ( 'B' in c3 )             as B_in_C3
, position ( 'B' in varchar15_uniq ) as B_in_varchar15_uniq
from VNA1P004 t4 left join VNA1P005 t5
on position ( 'B' in c3 )
= position ( 'B' in varchar15_uniq )
order by 6, c2, c3, varchar15_uniq
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s9')
    #
    #  ---------------------------
    #       Id: GV.061e     Upon grouped view, SUBSTRING on varchar
    #  ---------------------------
    #
    #  Expect 12 rows.
    stmt = """select substring(varchar15_uniq from 7 for 2) as S1
, substring(char6_20 for 2) as S2
from VNA1P004 
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s10')
    #
    #  Expect 2 rows matching on substrings 'AC', 'AB'
    #  (('BEAAGAAC' 'ACAAAAAA' 'AC')
    #   ('FGAAAAAB' 'ABAAAAAA' 'AB'))
    stmt = """select varchar15_uniq, char6_20
, substring(varchar15_uniq from 7 for 2) as S1
from VNA1P004 
where substring(varchar15_uniq from 7 for 2)
= substring(char6_20 from 1 for 2)
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s11')
    #
    #  ---------------------------
    #       Id: GV.061f     1997-11-20 (971107Beta): Moved to T1104:A09 to
    #                       separate it because it killed DP2.
    #                       Upon grouped view, TRIM of Concatenated string
    #                       literal and varchar.
    #  ---------------------------
    #
    #  ---------------------------
    #  CASE on data from Grouped Views VNA1P002, VNA1P004, VNA1P005
    #  ---------------------------
    #       Id: GV.071      Simple CASE in select list uses columns from Grouped Views
    #  ---------------------------
    #
    #  Expect 6 rows:
    #  c2 is BA            -3552  BA  AA  AA
    #  to
    #  the great unknown       ?   ?  DA  DA
    stmt = """select
CASE c2
when 'BA' then 'c2 is BA'
else 'the great unknown'
END
, *
from VNA1P005 
order by 1, n1, c3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s12')
    #
    #  ---------------------------
    #       Id: GV.072      Searched CASE in select list uses columns from Grouped Views
    #                       Searched CASE ('CASE with searched conditions') allows
    #                       multiple conditions to be evaluated in a single query.
    #  ---------------------------
    #
    #  Expect 6 rows:
    #  c2 is NULL              ?   ?  BA  BA
    #  to:
    #  the great unknown   -2789  DA  EA         ?
    stmt = """select
CASE when c2 is NULL then 'c2 is NULL'
when c2 < 'C'   then 'c2 is below C'
else 'the great unknown'
END
, *
from VNA1P005 
order by 1, n1, c3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s13')
    #
    #  ---------------------------
    #       Id: GV.073      Simple CASE in predicate uses columns from Grouped Views.
    #  ---------------------------
    #
    #  Expect 4 rows (without c2 as 'BA').
    stmt = """select *
from VNA1P005 
where '0' = CASE c2
when 'BA' then 'c2 is BA'
else '0'
END
order by 1, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s14')
    #
    #  ---------------------------
    #       Id: GV.074      Searched CASE in predicate uses columns from Grouped Views.
    #  ---------------------------
    #
    #  Expect 3 rows (those with c2 less than 'C').
    stmt = """select *
from VNA1P005 
where 'c2 is below C' = CASE
when c2 is NULL then 'c2 is NULL'
when c2 < 'C'   then 'c2 is below C'
else 'the great unknown'
END
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s15')
    
    _testmgr.testcase_end(desc)

def test004(desc="""a04"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     T1104:A04
    #
    #  See file arkt1104/testa04.b4q for version of this test before
    #  testscript separated into a file to leverage for partitioned
    #  as well as non-partitioned data.
    #
    # =================== End Test Case Header  ===================
    #
    # Force autocommit:
    stmt = """SET transaction Autocommit on;"""
    output = _dci.cmdexec(stmt)
    #
    #  ---------------------------
    #  Check grouped views of interest.
    #  ---------------------------
    
    #  Expect 7 rows.
    stmt = """select cast(char17_100 as char(20)), udec17_100
from """ + gvars.g_schema_arkcasedb + """.VNA1P002 
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s0')
    #
    stmt = """select varchar15_uniq
, varchar5_10 , varchar0_4 , sbin7_2
from VNA1P004 
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s1')
    #
    stmt = """select varchar15_uniq
, char6_20   , ubin15_uniq
, char16_uniq
from VNA1P004 
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s2')
    #
    stmt = """select n1, c2, c3, c4
from VNA1P005 
order by n1, c3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s3')
    
    #  Check needed value for subsequent tests.
    #  Expect ( ( 0 ) )
    stmt = """select min(t2.sbin7_2) as min_sbin7_2
from VNA1P004 t2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s4')
    #
    # Expect 0 rows.
    
    stmt = """select VARCHAR0_4 , SBIN7_2 , VARCHAR5_10 , CHAR6_20
from VNA1P004 
where
( ( select min(t2.sbin7_2) from VNA1P004 t2
) < -9
)
OR
( 9 <
( ( select min(t3.sbin7_2) from VNA1P004 t3
)
)
)
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    #
    #  Expect all 12 rows.
    stmt = """select VARCHAR0_4 , SBIN7_2 , VARCHAR5_10 , CHAR6_20
from VNA1P004 
where
( ( select min(t2.sbin7_2) from VNA1P004 t2
) < -9
)
OR
( 9 >
( ( select min(t3.sbin7_2) from VNA1P004 t3
)
)
)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s5')
    #
    #  ---------------------------
    #       Id: GV.081      Grouped view referenced in correlated subquery comparison.
    #  ---------------------------
    #
    #  Scaffolding for below.
    #  Expect ( ( 1188 ) ).
    stmt = """select distinct t1.ubin15_uniq
from VNA1P004 t1
where t1.ubin15_uniq < 2000
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s6')
    #
    #  Expect ( ( 1188  FGAAAAAB ) ).
    stmt = """select t1.ubin15_uniq, varchar15_uniq
from VNA1P004 t1
where t1.ubin15_uniq = 1188
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s7')
    #
    #  Expect ( ( FGAAAAAB ) ).
    stmt = """select varchar15_uniq
from VNA1P004 t1
where
( ( select distinct t1.ubin15_uniq from """ + gvars.g_schema_arkcasedb + """.VNA1P002 t2
where t1.ubin15_uniq < 2000
) > 1000
)
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s8')
    #
    #  ---------------------------
    #       Id: GV.081c     Grouped view referenced in subquery containing outer join.
    #  ---------------------------
    #
    #  Expect ( ( 24) ) rows.
    stmt = """select count(*)
from VNA1P004 t4
left join VNA1P005 t5
on position ( 'B' in c3 ) = 1
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s9')
    #
    #  Expect 7 rows.
    stmt = """select cast(char17_100 as char(20)), udec17_100
from """ + gvars.g_schema_arkcasedb + """.VNA1P002 t2
where
( select count(*)
from VNA1P004 t4
left join VNA1P005 t5
on position ( 'B' in c3 ) = 1
) = 24
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s10')
    #
    #  Expect 7 rows.
    stmt = """select cast(char17_100 as char(20)), udec17_100
from """ + gvars.g_schema_arkcasedb + """.VNA1P002 t2
where 6 <>
( select count(*)
from VNA1P004 t4
left join VNA1P005 t5
on position ( 'B' in c3 ) = 1
)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s11')
    #
    #  ---------------------------
    #       Id: GV.081d     Grouped view referenced in subquery and compared with multi-value predicate.
    #  ---------------------------
    #
    #  Includes duplicate at 'CCAAAAAAAAAAAAAA', so expect :
    #     ( ( 7 'AWAAAAAAAAAAAAAA' ) )
    stmt = """select cast( count( CHAR17_100 ) As Smallint ) As count17
, cast( min( CHAR17_100 ) as char(20) ) As min17
from """ + gvars.g_schema_arkcasedb + """.VNA1P002 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s12')
    #
    #  Expect ( ( 'DMAAAAAAAAAAAAAA' 6 ) )
    stmt = """select cast( max( CHAR17_100 ) as char(20) )
, cast( count( distinct CHAR17_100 ) As Smallint ) As DISTINCT_count17
from """ + gvars.g_schema_arkcasedb + """.VNA1P002 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s13')
    #
    #  Expect ( ('yes'  7) )
    stmt = """select 'yes', cast( count( CHAR17_100 ) As Smallint ) As count17
from """ + gvars.g_schema_arkcasedb + """.VNA1P002 
where (
( 'AWAAAAAAAAAAAAAA' )
=
( select cast( min(CHAR17_100) as char(20) )
from """ + gvars.g_schema_arkcasedb + """.VNA1P002 )
)
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s14')
    #
    #  Matt's bug ...
    #
    stmt = """select 'yes', cast( count( CHAR17_100 ) As Smallint ) As count17
from """ + gvars.g_schema_arkcasedb + """.VNA1P002 
where (
( 7, 'AWAAAAAAAAAAAAAA' )
=
( ( select cast( count( CHAR17_100 ) As Smallint )
, cast( min( CHAR17_100 ) as char(20))
from """ + gvars.g_schema_arkcasedb + """.VNA1P002 ) )
)
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s15')
    stmt = """select 'yes', cast( count( CHAR17_100 ) As Smallint ) As count17
from """ + gvars.g_schema_arkcasedb + """.VNA1P002 
where (
( 7, 'AWAAAAAAAAAAAAAA' )
=
( ( select count( CHAR17_100 )
, min( CHAR17_100 )
from """ + gvars.g_schema_arkcasedb + """.VNA1P002 ) )
)
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s16')
    #
    stmt = """select 'yes', cast( count( CHAR17_100 ) As Smallint ) As count17
from """ + gvars.g_schema_arkcasedb + """.VNA1P002 
where (
( 7, 'AWAAAAAAAAAAAAAA' )
=
( ( select cast( count( CHAR17_100 ) As Smallint )
from """ + gvars.g_schema_arkcasedb + """.VNA1P002 )
, ( select cast( min( CHAR17_100 ) as char(20) )
from """ + gvars.g_schema_arkcasedb + """.VNA1P002 )
)
)
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s17')
    
    _testmgr.testcase_end(desc)

def test005(desc="""a05"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     T1104:A05
    #  Description:        This test verifies SQL Grouped Views
    #                      in correlated subqueries, via SELECT.
    #
    # =================== End Test Case Header  ===================
    #
    # Force autocommit:
    stmt = """SET transaction Autocommit on;"""
    output = _dci.cmdexec(stmt)
    #
    
    #  ---------------------------
    #  Check values in tables.
    #  ---------------------------
    #  Expect 7 rows.
    stmt = """select suppnum, suppname
from GSUPPLY gvsup
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s0')
    #
    #  Expect 39 rows.
    stmt = """select suppnum, partnum, partcost
from GFROMSUP GFROMSUP 
order by partnum, suppnum
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s1')
    #
    #  ---------------------------
    #       Id: GV.082      Grouped views in correlated subqueries.
    #  ---------------------------
    #  Expect 3 rows:
    #     (('DATADRIVE') ('INFORMATION STORAG') ('MAGNETICS CORP'))
    #
    stmt = """select suppname
from GSUPPLY gvsup
where 4102 in
(select partnum
from GFROMSUP GFROMSUP 
where  gvsup.suppnum =  GFROMSUP.suppnum)
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s2')
    #
    #  get gsupply names for gsupplys who DON'T supply part 4102
    #  Expect 4 rows:
    #     (('DATA TERMINAL CO') ('DISPLAY INC') ('STEELWORK INC') ('TANDEM COMPUTERS'))
    #
    stmt = """select suppname
from GSUPPLY gvsup
where 4102 NOT in
(select partnum
from GFROMSUP GFROMSUP 
where  gvsup.suppnum = GFROMSUP.suppnum)
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s3')
    #
    #  get part numbers for all gparts supplied by more than one supplier
    #  Expect 8 rows:
    #     ((4101) (4102) (4103) (5101) (5103) (5504) (6401) (6402))
    #
    stmt = """select distinct X.partnum
from GFROMSUP X
where X.partnum in
(select Y.partnum
from GFROMSUP Y
where Y.suppnum <> X.suppnum
)
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s4')
    #
    #  same as above, with 'distinct Y.partnum' in subquery.
    #  Expect same 8 rows as above.
    #
    stmt = """select distinct X.partnum
from GFROMSUP X
where X.partnum in
(select distinct Y.partnum
from GFROMSUP Y
where Y.suppnum <> X.suppnum
)
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s5')
    #
    #  same as first, with 'group by Y.partnum'
    #  Expect same 8 rows as above.
    #
    stmt = """select distinct X.partnum
from GFROMSUP X
where X.partnum in
(select Y.partnum
from GFROMSUP Y
where Y.suppnum <> X.suppnum
group by Y.partnum
)
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s6')
    #
    #  same as first, with 'group by X.partnum' instead of
    #  'distinct X.partnum'
    #  Expect same 8 rows as above.
    #
    stmt = """select X.partnum
from GFROMSUP X
where X.partnum in
(select Y.partnum
from GFROMSUP Y
where Y.suppnum <> X.suppnum
)
group by X.partnum
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s7')
    #
    #  same as first, but with two group by clauses
    #  Expect same 8 rows as above.
    #
    stmt = """select X.partnum
from GFROMSUP X
where X.partnum in
(select Y.partnum
from GFROMSUP Y
where Y.suppnum <> X.suppnum
group by Y.partnum
)
group by X.partnum
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s8')
    #
    #  correlated subquery in where clause test - this tests the use
    #  of simple comparison operators (<,<=,=,<>,>,>=) and quantified
    #  comparison operators (=ANY,>ALL,etc.) as the relational operator
    #  between the outer and subqueries. Note that some of the
    #  subqueries in this testcase return 0 records (empty sets).
    #
    #  get gvsup.numbers and part number for gsupplys whose
    #  cost for that part is less than or equal to some other
    #  gsupplys cost for that part
    #
    stmt = """select suppnum, partnum, partcost
from GFROMSUP X
where partcost <=SOME
(select partcost
from GFROMSUP Y
where X.suppnum <> Y.suppnum
and X.partnum = Y.partnum
)
order by 1 , 2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s9')
    #
    #  same as above, use <=ANY instead of SOME
    #
    stmt = """select suppnum, partnum, partcost
from GFROMSUP X
where partcost <=ANY
(select partcost
from GFROMSUP Y
where X.suppnum <> Y.suppnum
and X.partnum = Y.partnum
)
order by 1 , 2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s10')
    #
    #  same as above, use <ALL instead
    #
    stmt = """select suppnum, partnum, partcost
from GFROMSUP X
where partcost <ALL
(select partcost
from GFROMSUP Y
where X.suppnum <> Y.suppnum
and X.partnum = Y.partnum
)
order by 1 , 2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s11')
    #
    #  get gvsup.numbers for other gsupply. who supply
    #  at least one part supplied by gsupply 15.
    #
    stmt = """select distinct suppnum
from GFROMSUP X
where X.partnum =SOME
(select Y.partnum
from GFROMSUP Y
where (X.suppnum <> Y.suppnum)
and (Y.suppnum = 15)
)
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s12')
    #
    #  get gvsup.numbers who are in the same state as gsupply 1
    #
    stmt = """select suppnum
from GSUPPLY X
where 1 =ANY
(select suppnum
from GSUPPLY Y
where X.state = Y.state
)
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s13')
    #
    #  get gvsup.names for gsupplys who supply part 4102
    #
    stmt = """select suppname
from GSUPPLY gvsup
where 4102 =SOME
(select partnum
from GFROMSUP  Y
where  gvsup.suppnum =  Y.suppnum)
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s14')
    #
    #  same as above, add gfromsup as qualifier for suppnum
    #
    stmt = """select suppname
from GSUPPLY gvsup
where 4102 =ANY
(select partnum
from GFROMSUP GFROMSUP 
where  gvsup.suppnum =  GFROMSUP.suppnum)
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s15')
    #
    #  get gvsup.names for gsupplys who DON'T supply part 4102
    #
    stmt = """select suppname
from GSUPPLY gvsup
where 4102 <>SOME
(select partnum
from GFROMSUP GFROMSUP 
where  gvsup.suppnum = GFROMSUP.suppnum)
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s16')
    #
    #  correlated subquery in where clause test - this tests the use of
    #  a correlated subquery with translated IN form of
    #  EXISTS/NOT EXISTS quantifiers.
    #
    #  get gvsup.names for gsupplys who supply part 4102
    #
    stmt = """select suppname
from GSUPPLY gvsup
where exists
(select *
from GFROMSUP GFROMSUP 
where  gvsup.suppnum = GFROMSUP.suppnum
and partnum = 4102
)
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s17')
    #
    #  same as above, change 'select *' to 'select partnum'
    #
    stmt = """select suppname
from GSUPPLY gvsup
where exists
(select partnum
from GFROMSUP GFROMSUP 
where  gvsup.suppnum = GFROMSUP.suppnum
and partnum = 4102
)
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s18')
    #
    #  get gvsup.names for gsupplys who DON'T supply part 4102
    #
    stmt = """select suppname
from GSUPPLY gvsup
where not exists
(select *
from GFROMSUP GFROMSUP 
where  gvsup.suppnum = GFROMSUP.suppnum
and partnum = 4102
)
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s19')
    #
    #  correlated subquery in where clause test - this tests the use
    #  of EXIST/NOT EXISTS to simulate the use of FOR ALL.
    #
    #  get gvsup.numbers for gsupplys who supply at least
    #  all those gparts.supplied by gsupply 6.
    #
    stmt = """select distinct suppnum
from GFROMSUP X
where not exists
(select partnum
from GFROMSUP Y
where suppnum = 6
and not exists
(select *
from GFROMSUP Z
where X.suppnum = Z.suppnum
and Z.partnum = Y.partnum
)
)
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s20')
    #
    #  same as above, except use 'group by suppnum' instead of
    #  select distinct suppnum to eliminate duplicates
    #
    stmt = """select suppnum
from GFROMSUP X
where not exists
(select *
from GFROMSUP Y
where suppnum = 6
and not exists
(select *
from GFROMSUP Z
where X.suppnum = Z.suppnum
and Z.partnum = Y.partnum
)
)
group by suppnum
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s21')
    #
    #  correlated subquery in where clause test - this tests multiply
    #  nested subqueries and multiple subqueries connected with
    #  and/or.
    #
    #  get gvsup.names for gsupplys who supply part 4102
    #
    stmt = """select suppname
from GSUPPLY gvsup
where 4102 in
(select partnum
from GFROMSUP GFROMSUP 
where  gvsup.suppnum = GFROMSUP.suppnum)
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s22')
    
    #  same as above, add gfromsup as qualifier for suppnum
    #
    stmt = """select suppname
from GSUPPLY gvsup
where 4102 in
(select partnum
from GFROMSUP GFROMSUP 
where  gvsup.suppnum =  GFROMSUP.suppnum)
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s23')
    
    #  get gsupply names for gsupplys who DON'T supply part 4102
    #
    stmt = """select suppname
from GSUPPLY gvsup
where 4102 NOT in
(select partnum
from GFROMSUP GFROMSUP 
where  gvsup.suppnum = GFROMSUP.suppnum)
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s24')
    #
    #  correlated subquery in where clause test - this tests the use of
    #  for browse access, for stable access,
    #  and for repeatable access inside of subqueries.
    #
    #  get part numbers for all gparts.supplied by more than one supplier
    #
    stmt = """select distinct X.partnum
from GFROMSUP X
where X.partnum in
(select distinct Y.partnum
from GFROMSUP Y
where Y.suppnum <> X.suppnum
for browse access
)
for stable access
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s25')
    #
    #  get part numbers for all gparts supplied by more than one supplier
    #
    stmt = """select distinct X.partnum
from GFROMSUP X
where X.partnum in
(select distinct Y.partnum
from GFROMSUP Y
where Y.suppnum <> X.suppnum
for stable access
)
for repeatable access
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s26')
    #
    #  get part numbers for all gparts supplied by more than one supplier
    #
    stmt = """select distinct X.partnum
from GFROMSUP X
where X.partnum in
(select distinct Y.partnum
from GFROMSUP Y
where Y.suppnum <> X.suppnum
for repeatable access
)
for repeatable access
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s27')
    
    _testmgr.testcase_end(desc)

def test006(desc="""a06"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     T1104:A06
    #  Description:        This test verifies SQL Grouped Views
    #                      via SELECT. Insert and Update tables using
    #                      values from Grouped Views; use of set
    #                      functions on Grouped Views
    #
    # =================== End Test Case Header  ===================
    #
    # Force autocommit:
    stmt = """SET transaction Autocommit on;"""
    output = _dci.cmdexec(stmt)
    #
    # To avoid unwanted warnings about string truncation on Insert:
    stmt = """SET WARNINGS OFF;"""
    output = _dci.cmdexec(stmt)
    #
    #  ---------------------------
    #  DML using Select from grouped View containing GROUP BY
    #  (View VNA1P002) in various contexts.
    #  ---------------------------
    #
    #  ---------------------------
    #  INSERT data SELECTed from 'GROUP BY' view.
    #  ---------------------------
    #
    #  ---------------------------
    #       Id: GV.091a     'GROUP BY' view in INSERT statement of 1 row from VNA1P002.
    #       Id: GV.091b     'GROUP BY' view in INSERT statement of several rows from VNA1P002.
    #  ---------------------------
    #
    
    #  Check the contents of the view.
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.VNA1P002 
order by 1, 2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s0')
    #
    # Expect ( 16 85 7 )
    
    stmt = """insert into T4INSERT ( n2, n4, n6) (
select min(UDEC17_100) , max(UDEC17_100)
, count(distinct UDEC17_100)
from """ + gvars.g_schema_arkcasedb + """.VNA1P002 
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """select n2, n4, n6 from T4INSERT order by 1,2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s1')
    #
    #  Expect to add 4 rows ( (1 1) * 3 (4 4) )
    stmt = """select count(v1.CHAR17_100) , count(v2.CHAR17_100)
from """ + gvars.g_schema_arkcasedb + """.VNA1P002 v1
left join """ + gvars.g_schema_arkcasedb + """.VNA1P002 v2
on v1.CHAR17_100 = v2.CHAR17_100
group by v2.CHAR17_100
having v2.CHAR17_100 > 'BZZ'
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s2')
    stmt = """insert into T4INSERT ( n2, n4) (
select count(v1.CHAR17_100) , count(v2.CHAR17_100) from """ + gvars.g_schema_arkcasedb + """.VNA1P002 v1
left join """ + gvars.g_schema_arkcasedb + """.VNA1P002 v2
on v1.CHAR17_100 = v2.CHAR17_100
group by v2.CHAR17_100
having v2.CHAR17_100 > 'BZZ'
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 4)
    stmt = """select n2, n4 from T4INSERT order by 1,2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s3')
    stmt = """select * from T4INSERT order by 1,2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s4')
    stmt = """delete from T4INSERT ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 5)
    #
    # ---------------------------
    # UPDATE data with value SELECTed from 'GROUP BY' view.
    # ---------------------------
    #
    # ---------------------------
    #      Id: GV.094      'GROUP BY' view in UPDATE statement of 1 row.
    # ---------------------------
    #
    # Make temporary data for cols (v1,v7,n2,n4,n6,n8,c3,c5):
    stmt = """insert into V4INSERT (v1,v7,n2,n4,n6,n8,c3,c5)
(select vch7,vch5,nint,nnum9,nnum5,nsint,ch3,ch4
from T1A 
where nnum9 < 4
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 4)
    stmt = """select * from T4INSERT 
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s5')
    #
    # Expect modification: ( ( 2 , 78 ) )
    stmt = """update V4INSERT set n4 =
( select max(UDEC17_100) from """ + gvars.g_schema_arkcasedb + """.VNA1P002 
where UDEC17_100 <> 85
)
where n2=2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select n2, n4 from T4INSERT 
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s6')
    #
    # Expect modification: ( ( 3 , 16 , 6 ) )
    stmt = """update T4INSERT set n4 =
( select min(UDEC17_100) from """ + gvars.g_schema_arkcasedb + """.VNA1P002 
where UDEC17_100 <> 85
)
, n6 =
( select count(distinct UDEC17_100)
from """ + gvars.g_schema_arkcasedb + """.VNA1P002 
where UDEC17_100 <> 85
)
where n2=3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select n2, n4, n6 from T4INSERT 
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s7')
    #
    #  Defensive check: The other values should not change.
    stmt = """select * from T4INSERT 
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s8')
    #
    stmt = """delete from T4INSERT ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 4)
    #
    #  ---------------------------
    #  DML using Select from grouped View containing GROUP BY, HAVING
    #  (View VNA1P004 in various contexts)
    #  ---------------------------
    #
    #  ---------------------------
    #  INSERT data SELECTed from 'GROUP BY, HAVING' view.
    #  ---------------------------
    #
    #  ---------------------------
    #       Id: GV.092a     'GROUP BY, HAVING' view in INSERT statement of 1 row.
    #       Id: GV.092b     'GROUP BY, HAVING' view in INSERT statement of several rows.
    #  ---------------------------
    #
    #  Check the contents of the view.
    stmt = """select VARCHAR0_4, VARCHAR15_UNIQ, CHAR16_UNIQ
from VNA1P004 
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s9')
    stmt = """select CHAR0_1000 from VNA1P004 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s10')
    stmt = """select SBIN7_2, VARCHAR5_10, CHAR6_20, UBIN15_UNIQ
from VNA1P004 
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s11')
    #
    # Expect ( ( M , BEAAGAAC , 11 ) )
    stmt = """insert into V4INSERT ( c5, v1, n2)
( select max(VARCHAR0_4), min(VARCHAR15_UNIQ)
, count(distinct CHAR16_UNIQ)
from VNA1P004 
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """select c5, v1, n2 from T4INSERT order by 1,2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s12')
    #
    #  Note that one of target cols v7 is only 5-characters long, so cast.
    #  Expect to add 3 rows ( ( A , 'BEAAGAAC' , 'BEAAGAAC' )
    #  ( A , 'FJAAGAA' , 'FJAAGAAE' )
    #  ( AAA , 'FGAAAAAB' , 'FGAAAAAB' ))
    stmt = """select VARCHAR0_4, VARCHAR15_UNIQ
, cast(CHAR16_UNIQ as char(5))
from VNA1P004 
group by VARCHAR0_4, VARCHAR15_UNIQ, CHAR16_UNIQ
order by 1,2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s13')
    #
    #  Be aware of column length now that we are killed in executor
    #  (ANSI standard) if overflow occurs on Insert or Update.
    stmt = """select cast(VARCHAR0_4 as char(3)), cast(VARCHAR15_UNIQ as char(8))
, cast(CHAR16_UNIQ as char(5))||'...'
from VNA1P004 
group by VARCHAR0_4, VARCHAR15_UNIQ, CHAR16_UNIQ
order by 1,2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s14')
    
    stmt = """insert into V4INSERT ( c5, v1, v7)
( select cast(VARCHAR0_4 as char(3)), cast(VARCHAR15_UNIQ as char(8))
, cast(CHAR16_UNIQ as char(5))
from VNA1P004 
group by VARCHAR0_4, VARCHAR15_UNIQ, CHAR16_UNIQ
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 12)
    stmt = """select c5, v1, v7 from T4INSERT 
order by 1,2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s15')
    stmt = """delete from T4INSERT ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 13)
    #
    # ---------------------------
    # UPDATE data with value SELECTed from 'GROUP BY, HAVING' view.
    # ---------------------------
    #
    # ---------------------------
    #      Id: GV.095      'GROUP BY, HAVING' view in UPDATE statement of 1 row.
    # ---------------------------
    #
    # Make temporary data for cols (v1,v7,n2,n4,n6,n8,c3,c5):
    stmt = """insert into V4INSERT (v1,v7,n2,n4,n6,n8,c3,c5)
( select vch7,vch5,nint,nnum9,nnum5,nsint,ch3,ch4
from T1A 
where nnum9 < 4
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 4)
    stmt = """select * from T4INSERT 
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s16')
    #
    #  Expect n4 modified to 13000 in all rows.
    stmt = """select max(UBIN15_UNIQ) from VNA1P004 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s17')
    stmt = """update V4INSERT set n4 =
( select max(UBIN15_UNIQ) from VNA1P004 )
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 4)
    stmt = """select * from T4INSERT 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s18')
    stmt = """delete from T4INSERT ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 4)
    
    _testmgr.testcase_end(desc)

def test007(desc="""a07"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     T1104:A07
    #  Description:        This test verifies SQL Grouped Views
    #                      via SELECT. Insert and Update tables using
    #                      values from Grouped Views; use of set
    #                      functions on Grouped Views
    #
    # =================== End Test Case Header  ===================
    #
    # Force autocommit:
    stmt = """SET transaction Autocommit on;"""
    output = _dci.cmdexec(stmt)
    
    #
    #  ---------------------------
    #  DML using Select from grouped View containing GROUP BY and
    #  aggregates (View VNA1P005) in various contexts.
    #  ---------------------------
    #
    #  Check the contents of the view.
    #  Expect 6 rows:
    #
    #  N1                    C2  C3  C4
    #  --------------------  --  --  --------
    #                 -4344  AA  BA  BA
    #                 -3552  BA  AA  AA
    #                 -2789  DA  EA         ?
    #                 -2389  BA  AA  AA
    #                     ?   ?  BA  BA
    #                     ?   ?  DA  DA
    #
    stmt = """select * from VNA1P005 t1
order by N1 , C3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s0')
    #
    # ---------------------------
    #      Id: GV.093a     'GROUP BY, aggregates' view in INSERT statement of 1 row.
    #      Id: GV.093b     'GROUP BY, aggregates' view in INSERT statement of several rows.
    # ---------------------------
    #
    # Expect 1 row { (-2389 , 'AA' , 6  'DA' ) }
    
    stmt = """insert into T4INSERT ( n6, v1, n2, c3) (
select  max(n1), min(c2), count(c3), max(c4)
from VNA1P005 t1
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """select n6, v1, n2, c3 from T4INSERT order by 1,2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s1')
    #
    # Expect to add 4 rows {
    # ( -4344.0 , 'AA' , 2 , 'BA' )
    # ( -2789.0 , 'DA' , 1 , NULL  )
    # ( -2389.0 , 'BA' , 2 , 'AA' )
    # ( NULL    , NULL , 1 , 'DA' )
    #  }
    #
    stmt = """insert into T4INSERT ( n6, v1, n2, c3) (
select  max(n1), min(c2), count(c3), c4
from VNA1P005 t1
group by c4
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 4)
    stmt = """select n6, v1, n2, c3 from T4INSERT 
order by 1,2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s2')
    stmt = """select * from T4INSERT 
order by 1,2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s3')
    #
    # Expect to add 1 row { ( 'EA' , NULL ) }
    stmt = """insert into T4INSERT ( c3, v1) (
select  c3, c4 from VNA1P005 t1
group by c3, c4 HAVING c4 is null
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """select  c3, v1 from T4INSERT 
order by 1,2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s4')
    stmt = """select * from T4INSERT 
order by 1,2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s5')
    stmt = """delete from T4INSERT ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 6)
    #
    # ---------------------------
    # UPDATE data with value SELECTed from 'GROUP BY, HAVING' view.
    # ---------------------------
    #
    # ---------------------------
    #      Id: GV.096      'GROUP BY, aggregates' view in UPDATE statement of 1 row.
    # ---------------------------
    #
    # Make temporary data for cols (v1,v7,n2,n4,n6,n8,c3,c5):
    stmt = """insert into T4INSERT (v1,v7,n2,n4,n6,n8,c3,c5)
( select vch7,vch5,nint,nnum9,nnum5,nsint,ch3,ch4 from T1A 
where nnum9 < 4
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 4)
    stmt = """insert into V4INSERT (v1,v7,n2,n4,n6,n8,c3,c5)
( select vch7,vch5,nint,nnum9,nnum5,nsint,ch3,ch4 from T1A 
where nnum9 < 4
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 4)
    #  Expect 8 rows (4 sets of twins).
    stmt = """select * from T4INSERT 
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s6')
    #
    # Expect n4 becomes { -2389.00 } in all columns.
    stmt = """update T4INSERT set n4 =
( select max(n1) from VNA1P005 
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 8)
    #  Expect 8 rows (4 sets of twins).
    stmt = """select * from T4INSERT 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s7')
    #
    stmt = """select * from V4INSERT 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s8')
    #
    stmt = """delete from T4INSERT ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 8)
    
    _testmgr.testcase_end(desc)

def test008(desc="""a08"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     T1104:A08
    #  Description:        This test verifies SQL Grouped Views using
    #                      string functions.
    #
    # =================== End Test Case Header  ===================
    #
    # Force autocommit:
    stmt = """SET transaction Autocommit on;"""
    output = _dci.cmdexec(stmt)
    #
    
    #  ---------------------------
    #  NOTE -- VIEWS ARE CREATED ON THE FLY AS NEEDED.
    #  First check columns of interest in base table.
    #  ---------------------------
    #
    #  Expect 5 rows as in base table.
    stmt = """select vch7, vch5, ch4 from T1A 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s0')
    #
    # ---------------------------
    # ANSI string functions within Grouped Views.
    # ---------------------------
    #      Id: GV.072a     Within grouped view, UPPER and LOWER string functions on varchar columns.
    #      Id: GV.072b     Within grouped view, Arithmetic upon CHAR_LENGTH of Concatenated char and varchar columns.
    #      Id: GV.072c     Within grouped view, Arithmetic upon OCTET_LENGTH of Concatenated char and varchar columns.
    # ---------------------------
    #
    
    stmt = """create view V1A ( cLower, cUpper, clenV, clenF) as
select lower(vch7)
, upper(vch5)
, char_length (vch5)
, char_length (ch4)
from T1A 
group by vch7, vch5, ch4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    #  Note: length of varchar (clenv); CLENV should be 1 when CUPPER is 'C'.
    stmt = """select * from V1A 
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s1')
    #
    #  ---------------------------
    #       Id: GV.072d     Within grouped view, POSITION of literal in varchar
    #       Id: GV.072e     Within grouped view, SUBSTRING in varchar
    #       Id: GV.072f     Within grouped view, TRIM of Concatenated string literal and varchar
    #  ---------------------------
    #
    #  9/22/98 Added concatenation on vch7 to avoid error 8403: The length
    #          argument of function SUBSTRING cannot be less than zero or
    #          greater than source string length.
    stmt = """select vch7, substring ( vch7||'xyz' from 3 for 2 )
from T1A 
group by vch7
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s2')
    stmt = """create view V1B (cOctet_length,  cPosition, cSubstring, cTrim) as
select
-- Expect 4
octet_length (ch4)
, position  ( 'c' in vch7 )
, substring ( vch7||'xyz' from 3 for 2 )
, trim (leading 'a' from vch7)
from T1A 
group by vch7, vch5, ch4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    #  Expect ((4 0 '' '') (4 0 'Cd' 'AbCdEfG')
    #          (4 0 'b' '') (4 1 '' 'cc')
    #          (4 3 'cd' 'bcdefg'))
    stmt = """select * from V1B 
order by 2, 3, 4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s3')
    #
    #  Join the grouped views:
    #  Expect 5 rows.
    # (('abcdefg' 'CC' 'Cd' 'AbCdEfG'))
    #  ('abcdefg' 'CC' 'Cd' 'AbCdEfG')
    #  ('b' 'C' '' 'b')
    #  ('cc' 'CC' '' 'cc')
    #  ('a' NULL NULL NULL))
    stmt = """select clower, cupper, csubstring, ctrim
from V1A 
left join V1B 
on upper(ctrim) = upper(clower)
order by ctrim, clower
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s4')
    #
    #  Expect 5 rows.
    stmt = """select upper(ctrim) as up_trim , upper(clower) as up_clower
, ctrim , clower
from V1A 
left join V1B 
on upper(ctrim) = upper(clower)
order by ctrim, clower
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s5')
    #
    #  Expect 6 rows, with 2 rows in V1B being null extended,
    #  and one row with 'abcdefg'-type value matching 2 rows in V1A.
    stmt = """select upper(ctrim) as up_trim , upper(clower) as up_clower
, ctrim , clower
from V1A 
right join V1B 
on upper(ctrim) = upper(clower)
order by ctrim, clower
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s6')
    #
    #  Expect 5 rows.
    stmt = """select upper(ctrim) as up_ctrim , upper(cupper) as up_cupper
, ctrim , cupper , clower
from V1A 
left join V1B 
on upper(ctrim) = upper(cupper)
order by ctrim, cupper, clower
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s7')
    #
    #  Expect 7 rows, with 4 rows in V1B being null extended,
    #  and one row with 'CC' value matching 3 rows in V1A.
    stmt = """select upper(ctrim) as up_ctrim , upper(cupper) as up_cupper
, ctrim , cupper , clower
from V1A 
right join V1B 
on upper(ctrim) = upper(cupper)
order by ctrim, cupper, clower
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s8')
    
    _testmgr.testcase_end(desc)

def test009(desc="""a09"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     T1104:A09
    #
    #  See file arkt1104/testa09.b4q for version of this test before
    #  testscript separated into a file to leverage for partitioned
    #  as well as non-partitioned data.
    #
    # =================== End Test Case Header  ===================
    #
    # Force autocommit:
    stmt = """SET transaction Autocommit on;"""
    output = _dci.cmdexec(stmt)
    #
    #  ---------------------------
    #  ANSI string functions on data from Grouped Views
    #  VNA1P002, VNA1P004, VNA1P005
    #  ---------------------------
    #
    #  ---------------------------
    #       Id: GV.061f     Upon grouped view, TRIM of Concatenated string literal and varchar
    #  ---------------------------
    #
    #  Expect 12 rows.
    #  Note removal of multiple values where applicable.
    stmt = """select varchar15_uniq
, trim (both 'B' from trim (both 'A' from varchar15_uniq) )
, char6_20
, trim (both 'B' from trim (both 'A' from char6_20) )
from VNA1P004 t4
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s0')
    #
    #  Also for the underlying table.
    #  Expect 13 rows.
    #  Only one TRIM function per select-list item.
    stmt = """select varchar15_uniq
, trim (both 'A' from varchar15_uniq)
, char6_20
, trim (both 'A' from char6_20)
from BTA1P004 t4
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s1')
    #
    #  One select-list item has TWO TRIM functions.
    #  Expect 13 rows.
    stmt = """select trim (both 'B' from trim (both 'A' from varchar15_uniq) )
, trim (both 'A' from char6_20)
from BTA1P004 t4
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s2')
    #
    #  Two select-list items have TWO TRIM functions.
    #  Expect 13 rows.
    stmt = """select trim (both 'B' from trim (both 'A' from varchar15_uniq) )
, trim (both 'B' from trim (both 'A' from char6_20) )
from BTA1P004 t4
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s3')
    
    _testmgr.testcase_end(desc)

def test010(desc="""a10"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     T1104:A10
    #  Description:        This test verifies SQL Grouped Views
    #                      via SELECT. Also some tests for Joins.
    #
    # =================== End Test Case Header  ===================
    #
    #
    # Force autocommit:
    stmt = """SET transaction Autocommit on;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table t036t1(a int) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """insert into t036t1 values(1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t036t1 values(2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t036t1 values(3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """select * from t036t1 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s0')
    #
    
    stmt = """create view t036v24 as
select a,sum(b) as r
from (select * from (values (1), (2)) x
natural join
(select a from t036t1)z
) y(a,b)
group by a
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #  Expect 6 rows.
    stmt = """select * from (values (1), (2)) x
natural join
(select a from t036t1)z
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s1')
    #  Expect 2 rows: ( (1, 6) (2, 6) )
    stmt = """select * from t036v24 
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s2')
    stmt = """drop view t036v24 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #  ---------------------------
    #  Additional test for Natural Join which should select
    #  rows that have equal values in the relevant columns.
    #  The difference from the above is in the column names.
    #  ---------------------------
    #  Note: 1 column.
    #  Expect ((1) (2))
    
    stmt = """select * from ( values ('1'), ('2') ) x(a)
natural join
(select cast(a as char(6)) as a from t036t1)z
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s3')
    #
    
    stmt = """create view t036v24 as
select *
from (select * from ( values ('1'), ('2') ) x(a)
natural join
(select cast(a as varchar(6)) as a from t036t1)z
) y
group by a
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #  Expect ((1) (2))
    stmt = """select * from t036v24 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s4')
    stmt = """drop view t036v24 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #
    #  ---------------------------
    #  Add test for inner join which should return all rows.
    #  Contrast with Natural Join which should select rows that have
    #  equal values in the relevant columns.
    #  ---------------------------
    #
    #  Expect 6 rows ((1 1) (1 2) (1 3) (2 1) (2 2) (2 3))
    stmt = """select * from (values (1), (2)) x
inner join
(select a from t036t1)z
on 1=1
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s5')
    
    stmt = """create view t036v24 as
select a, sum(b) as r
from (select * from (values (1), (2)) x
inner join
(select a from t036t1)z
on 1=1
) y(a,b)
group by a
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #  Expect 2 rows ((1 6) (2 6))
    stmt = """select * from t036v24 
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s6')
    stmt = """drop view t036v24 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #
    #  ---------------------------
    #  Add test for cross product which should return all rows.
    #  Contrast with Natural Join which should select rows that have
    #  equal values in the relevant columns.
    #  ---------------------------
    #
    #  Expect 6 rows ((1 1) (1 2) (1 3) (2 1) (2 2) (2 3))
    stmt = """select * from (values (1), (2)) x
,
(select a from t036t1)z
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s7')
    
    stmt = """create view t036v24 as
select a, sum(b) as r
from (select * from (values (1), (2)) x
,
(select a from t036t1)z
) y(a,b)
group by a
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #  Expect 2 rows ((1 6) (2 6))
    stmt = """select * from t036v24 
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s8')
    stmt = """drop view t036v24 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    stmt = """drop table t036t1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #
    # ---------------------------
    # Another table and a view with a different aggregate.
    # ---------------------------
    stmt = """create table t036t1(a varchar (9)) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """insert into t036t1 values('joanzim');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t036t1 values('kirkstone');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t036t1 values('swansea');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """select * from t036t1 order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s9')
    stmt = """select * from ( values ('1'), ('2') ) x
natural join
(select a from t036t1)z
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s10')
    
    stmt = """create view t036v24 as
select a as r
from (select * from ( values ('1'), ('2') ) x(a)
natural join
(select a from t036t1)z
) y(a)
group by a
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #  Expect 6 rows.
    stmt = """select * from ( values ('1'), ('2') ) x
natural join
(select a from t036t1)z
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s11')
    stmt = """select *
from (select * from ( values ('1',2), ('2',2) ) x(a, b)
natural join
(select a, 2 from t036t1)z
) y(a,b,c)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """select a
from (select * from ( values ('1'), ('2') ) x(a)
natural join
(select a from t036t1)z
) y(a)
group by a
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    # Expect 2 rows ((1 3) (2 3)) <<< expect 0??
    stmt = """select * from t036v24 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """drop view t036v24 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create view t036v24 as
select a
from (select * from ( values ('1'), ('2') ) x(a)
natural join
(select a from t036t1)z
) y(a)
group by a
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # Expect 6 rows.
    stmt = """select * from ( values ('1'), ('2') ) x(a)
natural join
(select a, '2' from t036t1)z
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    #  Expect 0 rows
    stmt = """select count(*) from t036v24 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s12')
    stmt = """drop view t036v24 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table t036t1 ;"""
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
    #  Test case name:     T1104:A11
    #  Description:        This test verifies SQL Grouped Views
    #                      via SELECT. Also some tests for Joins.
    #
    # =================== End Test Case Header  ===================
    # ---------------------------
    # Create local table in pre-test code.
    # ---------------------------
    
    stmt = """create table TA11 
( varcol  varchar(7)
, charcol char(7)
)  no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into TA11 values ('v1' , 'c1' )
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """select varcol||'.' , char_length(varcol)
, charcol||'.' , char_length(charcol)
from TA11 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s0')
    #
    stmt = """insert into TA11 values ('v2' , 'c2' )
, ('v3' , 'c3' )
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 2)
    stmt = """insert into TA11 values ('v777777' , 'c777777' ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into TA11 values ('v66666' , 'c4' ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into TA11 values ('v4' , 'c444' ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """select varcol||'.' , char_length(varcol)
, charcol||'.' , char_length(charcol)
from TA11 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s1')
    #
    stmt = """delete from TA11;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 6)
    stmt = """insert into TA11 values ('v4' , 'c4' )
, ('v777777' , 'c777777' )
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 2)
    stmt = """select varcol||'.' , char_length(varcol)
, charcol||'.' , char_length(charcol)
from TA11 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s2')
    #
    stmt = """delete from TA11;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 2)
    stmt = """insert into TA11 values ('v1' , 'c1' )
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """select varcol||'.' , char_length(varcol)
, charcol||'.' , char_length(charcol)
from TA11 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s3')
    #
    stmt = """delete from TA11;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    stmt = """insert into TA11 values ('v2' , 'c2' )
, ('v3' , 'c3' )
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 2)
    stmt = """select varcol||'.' , char_length(varcol)
, charcol||'.' , char_length(charcol)
from TA11 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s4')
    #
    stmt = """delete from TA11;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 2)
    stmt = """insert into TA11 values ('v66666' , 'c4' )
, ('v4' , 'c444' )
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 2)
    stmt = """select varcol||'.' , char_length(varcol)
, charcol||'.' , char_length(charcol)
from TA11 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s5')
    #
    stmt = """delete from TA11;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 2)
    stmt = """insert into TA11 values ('v1' , 'c1' )
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """select varcol||'.' , char_length(varcol)
, charcol||'.' , char_length(charcol)
from TA11 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s6')
    #
    stmt = """insert into TA11 values ('v1  ' , 'c2' )
, ('v1' , 'c3' )
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 2)
    stmt = """select varcol||'.' , char_length(varcol)
, charcol||'.' , char_length(charcol)
from TA11 
order by 1, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s7')
    #
    stmt = """insert into TA11 values ('v66666' , 'c4' )
, ('v1' , 'c444' )
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 2)
    stmt = """select varcol||'.' , char_length(varcol)
, charcol||'.' , char_length(charcol)
from TA11 
order by 1, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s8')
    #
    stmt = """select distinct varcol
from TA11 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s9')
    
    stmt = """drop table TA11;"""
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
    #  Test case name:     T1104:A12
    #  Description:        This test verifies SQL Grouped Views
    #                      via SELECT. Also some tests for Joins.
    #
    # =================== End Test Case Header  ===================
    stmt = """set param ?paramA A;"""
    output = _dci.cmdexec(stmt)
    #  ---------------------------
    #  DML on Grouped View containing GROUP BY, HAVING (Select from
    #  View VNA1P004 in various contexts)
    #
    
    stmt = """select varchar0_4
, varchar5_10    , char6_20   , ubin15_uniq
, varchar15_uniq , char16_uniq
from BTA1P004 
order by 1, 2, char16_uniq
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s0')
    
    #  Expect 12 rows, as in view, (omitting 'CAA' ... 'ACAAA' ... ).
    stmt = """select varchar0_4     , sbin7_2
, varchar5_10    , char6_20   , ubin15_uniq
, varchar15_uniq , char16_uniq
from BTA1P004 
where
ubin15_uniq > 1000
and (
(  varchar0_4 <> 'CAA' )
or ( varchar5_10 <> 'ACAAA')
or ( varchar15_uniq <> 'EJAAJAA' )
)
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s1')
    #
    stmt = """select varchar0_4 , cast( char0_1000 as varchar(65))
from BTA1P004 
where
ubin15_uniq > 1000
and (
(  varchar0_4 <> 'CAA' )
or ( varchar5_10 <> 'ACAAA')
or ( varchar15_uniq <> 'EJAAJAA' )
)
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s2')
    #
    stmt = """select varchar0_4     , char0_1000 , sbin7_2
, varchar5_10    , char6_20   , ubin15_uniq
, varchar15_uniq , char16_uniq
from BTA1P004 
where
ubin15_uniq > 1000
and (
(  varchar0_4 <> 'CAA' )
or ( varchar5_10 <> 'ACAAA')
or ( varchar15_uniq <> 'EJAAJAA' )
)
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s3')
    #  This row is omitted:
    #  CAA         EJAAJAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA        1  ACAAA        CCAAAAAA         3889  EJAAJAA         EJAAJAAC
    #
    #  View should show 12 rows.
    stmt = """select count(*) from VNA1P004;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s4')
    #
    stmt = """select VARCHAR0_4
, VARCHAR15_UNIQ
, CHAR16_UNIQ
from VNA1P004 
order by VARCHAR5_10
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s5')
    #
    #  Expect (( 'M'  'BEAAGAAC'  11 ))
    stmt = """select max(VARCHAR0_4) as mycol
, min(VARCHAR15_UNIQ)
, count(distinct CHAR16_UNIQ)
from VNA1P004 
order by mycol ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s6')
    #
    #  Expect (( 'M'  'BEAAGAAC'  12 )) without DISTINCT.
    stmt = """select max(VARCHAR0_4),min(VARCHAR15_UNIQ)
, count(CHAR16_UNIQ)
from VNA1P004 
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s7')
    #
    #  ---------------------------
    #       Id: GV.015      'GROUP BY' on Grouped view that contains HAVING
    #  ---------------------------
    #
    stmt = """select VARCHAR0_4
, VARCHAR15_UNIQ
, CHAR16_UNIQ
, VARCHAR5_10 as OrderByVarChar5_10
from VNA1P004 
order by VARCHAR5_10
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s8')
    #
    stmt = """select t.VARCHAR15_UNIQ
from VNA1P004 t
group by t.VARCHAR15_UNIQ
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s9')
    #
    stmt = """select t.VARCHAR15_UNIQ
, t.CHAR16_UNIQ
from VNA1P004 t
group by t.VARCHAR15_UNIQ
, t.CHAR16_UNIQ
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s10')
    #
    #  Expect 121 rows (11 * 11)
    stmt = """select t.VARCHAR0_4, u.VARCHAR0_4
from VNA1P004 t, VNA1P004 u
group by t.VARCHAR0_4, u.VARCHAR0_4
order by t.VARCHAR0_4, u.VARCHAR0_4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s11')
    #
    #  Add left join.
    #  Expect 14 rows.
    stmt = """select t.VARCHAR0_4, u.VARCHAR0_4
, t.VARCHAR15_UNIQ, u.CHAR16_UNIQ
from VNA1P004 t
left join VNA1P004 u
on t.VARCHAR0_4 = u.VARCHAR0_4
group by t.VARCHAR0_4, u.VARCHAR0_4
, t.VARCHAR15_UNIQ, u.CHAR16_UNIQ
order by t.VARCHAR0_4, 3, 4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s12')
    #  Expect 2 rows.
    stmt = """select t.VARCHAR0_4, u.VARCHAR0_4
, t.VARCHAR15_UNIQ, u.CHAR16_UNIQ
from VNA1P004 t
left join VNA1P004 u
on t.VARCHAR0_4 = u.VARCHAR0_4
where t.VARCHAR0_4 > 'E' and u.VARCHAR0_4 < 'H'
group by t.VARCHAR0_4, u.VARCHAR0_4
, t.VARCHAR15_UNIQ, u.CHAR16_UNIQ
order by t.VARCHAR0_4, u.VARCHAR0_4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s13')
    #
    #  Group by column that is missing from select list.
    #  Expect 34 rows.
    stmt = """select t.VARCHAR15_UNIQ, u.VARCHAR15_UNIQ
from VNA1P004 t
left join VNA1P004 u
on t.VARCHAR15_UNIQ = u.VARCHAR15_UNIQ
group by t.VARCHAR0_4, u.VARCHAR0_4
, t.VARCHAR15_UNIQ, u.VARCHAR15_UNIQ
order by u.VARCHAR15_UNIQ
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s14')
    #
    # -------------------------
    #       Id: GV.016      'HAVING' on Grouped view that contains HAVING
    #  ---------------------------
    #
    #  HAVING on an outer column of left join.
    #  Expect 10 rows all but ( 'A' ... )
    stmt = """select t.VARCHAR0_4, u.VARCHAR0_4
, t.VARCHAR15_UNIQ, u.CHAR16_UNIQ
from VNA1P004 t
left join VNA1P004 u
on t.VARCHAR0_4 = u.VARCHAR0_4
group by t.VARCHAR0_4, u.VARCHAR0_4
, t.VARCHAR15_UNIQ, u.CHAR16_UNIQ
HAVING t.VARCHAR0_4 > 'A'
order by t.VARCHAR0_4, u.VARCHAR0_4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s15')
    #
    #  HAVING on an inner column of left join; subquery in HAVING.
    #  Expect 5 rows ( ( 'A' ... ) * 4 and ( 'AAA' 'FGAAAAAB' ) )
    stmt = """select t.VARCHAR0_4, u.CHAR16_UNIQ
from VNA1P004 t
left join VNA1P004 u
on t.VARCHAR0_4 = u.VARCHAR0_4
group by t.VARCHAR0_4, u.VARCHAR0_4
, t.VARCHAR15_UNIQ, u.CHAR16_UNIQ
HAVING u.VARCHAR0_4
< (select min(VARCHAR15_UNIQ) from VNA1P004)
order by t.VARCHAR0_4, u.CHAR16_UNIQ
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s16')
    #
    #  HAVING on an outer column of left join; param in HAVING.
    #  Expect 10 rows ( 'AAA' 'AAA' 'FGAAAAAB' 'FGAAAAAB' )
    stmt = """select t.VARCHAR0_4, u.VARCHAR0_4
, t.VARCHAR15_UNIQ, u.CHAR16_UNIQ
from VNA1P004 t
left join VNA1P004 u
on t.VARCHAR0_4 = u.VARCHAR0_4
group by t.VARCHAR0_4, u.VARCHAR0_4
, t.VARCHAR15_UNIQ, u.CHAR16_UNIQ
HAVING t.VARCHAR0_4 > ?paramA
order by t.VARCHAR0_4, u.VARCHAR0_4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s17')
    #
    #  ---------------------------
    #       Id: GV.017      'WHERE' on Grouped view that contains HAVING
    #  ---------------------------
    #
    #  WHERE on an outer column of left join.
    #  Expect 10 row ( 'AAA' 'AAA' 'FGAAAAAB' 'FGAAAAAB' ), etc.
    stmt = """select t.VARCHAR0_4, u.VARCHAR0_4
, t.VARCHAR15_UNIQ, u.CHAR16_UNIQ
from VNA1P004 t
left join VNA1P004 u
on t.VARCHAR0_4 = u.VARCHAR0_4
WHERE t.VARCHAR0_4 <> 'A'
group by t.VARCHAR0_4, u.VARCHAR0_4
, t.VARCHAR15_UNIQ, u.CHAR16_UNIQ
order by t.VARCHAR0_4, u.VARCHAR0_4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s18')
    #
    #  WHERE on an inner column of left join; param in WHERE.
    #  Expect 10 row as above.
    stmt = """select t.VARCHAR0_4, u.VARCHAR0_4
, t.VARCHAR15_UNIQ, u.CHAR16_UNIQ
from VNA1P004 t
left join VNA1P004 u
on t.VARCHAR0_4 = u.VARCHAR0_4
WHERE u.VARCHAR0_4 <> ?paramA
group by t.VARCHAR0_4, u.VARCHAR0_4
, t.VARCHAR15_UNIQ, u.CHAR16_UNIQ
order by t.VARCHAR0_4, u.VARCHAR0_4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s19')
    #
    #  WHERE on an outer column of left join; subquery in WHERE.
    #  Expect 14 rows ( 12 + 2 ).
    stmt = """select t.VARCHAR0_4, u.CHAR16_UNIQ
from VNA1P004 t
left join VNA1P004 u
on t.VARCHAR0_4 = u.VARCHAR0_4
WHERE t.VARCHAR0_4
<> (select min(VARCHAR15_UNIQ) from VNA1P004)
group by t.VARCHAR0_4, u.VARCHAR0_4
, t.VARCHAR15_UNIQ, u.CHAR16_UNIQ
order by t.VARCHAR0_4, u.CHAR16_UNIQ
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s20')
    #
    #  ---------------------------
    #       Id: GV.018      'UNION' on Grouped view that contains HAVING
    #  ---------------------------
    #
    #  UNION of grouping columns varchar0_4, varchar5_10, varchar15_uniq
    stmt = """select VARCHAR0_4 from VNA1P004 
UNION
select VARCHAR5_10 from VNA1P004 
UNION
select VARCHAR15_UNIQ from VNA1P004 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s21')
    #
    stmt = """select CHAR0_1000 from VNA1P004 
UNION select CHAR6_20 from VNA1P004 
UNION
select CHAR16_UNIQ from VNA1P004 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s22')
    #
    #  ---------------------------
    #  DML on Grouped View containing GROUP BY and aggregates
    #  (Select from View VNA1P005 in various contexts)
    #  ---------------------------
    #
    #  ---------------------------
    #       Id: GV.023      'ORDER BY' on Grouped view (GROUP BY, aggregates).
    #  ---------------------------
    #
    #  Expect 6 rows:
    #  N1                    C2  C3  C4
    #  --------------------  --  --  --------
    #
    #                 -4344  AA  BA  BA
    #                 -3552  BA  AA  AA
    #                 -2789  DA  EA         ?
    #                 -2389  BA  AA  AA
    #                     ?   ?  BA  BA
    #                     ?   ?  DA  DA
    #
    stmt = """select * from VNA1P005 t1 order by 2, 4, 1, 3 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s23')
    #
    #  ---------------------------
    #       Id: GV.024      Aggregates on Grouped view (GROUP BY, aggregates).
    #  ---------------------------
    #
    stmt = """select * from VNA1P005 
order by 1, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s24')
    #
    stmt = """select t1.sbinneg15_nuniq , t1.char2_2
, t2.char2_2 , t3.char3_4
from BTA1P005 t1
right join BTA1P005 t2 on t1.char2_2 = t2.char3_4
left  join BTA1P005 t3 on t2.char2_2 = t3.char3_4
group by t1.sbinneg15_nuniq , t1.char2_2 , t2.char2_2 , t3.char3_4
order by 1, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s25')
    #
    stmt = """select t1.sbinneg15_nuniq , t1.char2_2 , t2.char2_2
from BTA1P005 t1
right join BTA1P005 t2 on t1.char2_2   = t2.char3_4
group by t1.sbinneg15_nuniq , t1.char2_2 , t2.char2_2
order by 1, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s26')
    #
    stmt = """select t1.sbinneg15_nuniq , t1.char2_2 , t2.char2_2
from BTA1P005 t1
right join BTA1P005 t2 on (1 = 1)
group by t1.sbinneg15_nuniq , t1.char2_2 , t2.char2_2
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s27')
    #
    #  Expect 1 row ( -2389  'AA'  6  'DA' )
    stmt = """select  max(n1), min(c2), count(c3), max(distinct c4)
from VNA1P005 t1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s28')
    #
    #  ---------------------------
    #       Id: GV.025      'GROUP BY' on Grouped view (GROUP BY, aggregates).
    #  ---------------------------
    #
    #  Expect 4 rows.
    stmt = """select max(n1) as max_n1
, min(c2) as min_c2
, count(c3) as count_c3
, c4
from VNA1P005 t1
group by c4
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s29')
    stmt = """select c3, c4 from VNA1P005 t1
group by c3, c4
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s30')
    stmt = """select c3, c4 from VNA1P005 t1
group by c4, c3
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s31')
    #
    #  -------------------------
    #       Id: GV.026      'HAVING' on Grouped view (GROUP BY, aggregates).
    #  ---------------------------
    #
    #  Expect (( 'EA'  NULL ))
    stmt = """select c3, c4 from VNA1P005 t1
group by c3, c4 HAVING c4 is null
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s32')
    #  Expect (( 'AA' 'AA' ),( 'EB' 'EB' ),( 'DA' 'DA' ))
    stmt = """select c3, c4 from VNA1P005 t1
group by c3, c4 HAVING c4 is NOT null
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s33')
    #  Expect (( 'AA' 'AA' ),( 'EB' 'EB' ),( 'DA' 'DA' ))
    stmt = """select c3, c4 from VNA1P005 t1
group by c3, c4 HAVING c4 = c3
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s34')
    
    stmt = """select c3, c4 from VNA1P005 t1
group by c3, c4 HAVING c3 <> c4
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    #
    #  ---------------------------
    #       Id: GV.027      'WHERE' on Grouped view (GROUP BY, aggregates).
    #  ---------------------------
    #
    #  Expect 2 rows:
    #                 -4344  AA   2  BA
    #                 -3552  BA   2  AA
    stmt = """select max(n1) as max_n1
, min(c2) as min_c2
, count(c3) as count_c3
, c4
from VNA1P005 t1
where c3 < 'DA'
group by c4
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s35')
    #
    #  Expect 2 rows:
    #                 -4344  AA   2  BA
    #                     ?   ?   1  DA
    stmt = """select max(n1) as max_n1
, min(c2) as min_c2
, count(c3) as count_c3
, c4
from VNA1P005 t1
where c4 > 'AA'
group by c4
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s36')
    #
    #  ---------------------------
    #       Id: GV.028      'UNION' on Grouped view (GROUP BY, aggregates).
    #  ---------------------------
    #  Expect 11 rows:
    #      ( AA, BA, DA, EA, ?) UNION ALL ( DA, BA, AA, BA, ?, ? )
    #
    stmt = """select c4 from VNA1P005 t1
union     select c3 from VNA1P005 t1
union all select c2 from VNA1P005 t1
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s37')
    
    _testmgr.testcase_end(desc)

