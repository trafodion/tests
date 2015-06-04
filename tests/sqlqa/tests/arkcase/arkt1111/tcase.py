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
    # Test case name:      T1111:A01
    # Description:         Parallel execution in SQL with
    #                      2-way joins.
    #                      Testware leveraged from arkt1102.
    #
    # =================== End Test Case Header  ===================
    
    # Get parallelism defaults for this test unit's execution.
    # Includes choice of global schema.
    #
    # Defaults and defines for this testunit.
    #
    # Get the parameter to use the partitioned global db.
    # Catalog for 'global database #11'.
    #
    # Schema for 'PARTITIONED global database #11'.
    #
    # Turn Parallel ON.
    
    stmt = """Control query default ATTEMPT_ESP_PARALLELISM 'ON';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #================ Fix a07s15 SQlci Abend Error provide by Wong,Steven======
    stmt = """control query default TARGET_CPU_FREQUENCY '200';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #
    # And let's look at SHOWSHAPE
    #   Set Showshape On ;
    # Nov 98 for setting up ref files.
    # TEMPORARILY debugging run with non-partitioned global db.
    #   obey ../tools11/ci11defs;
    
    stmt = """Control query default ATTEMPT_ESP_PARALLELISM 'ON';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """control query default PARALLEL_NUM_ESPS '1';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    # Try with 2 ESPs.
    stmt = """control query default PARALLEL_NUM_ESPS '2';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """control query default PARALLEL_NUM_ESPS '4';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from VNA1P006 order by 1,2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s0')
    #
    # ---------------------------
    # Subquery transformations: Subqueries beneath OR using params.
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
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s1')
    #
    stmt = """select distinct cast(?p as pic x(5))
from VNA1P006 
where ( (select min(sbin0_4) from VNA1P006),?pn)
= ( (select min(sdec6_4) from VNA1P006),?pn)
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s2')
    #
    stmt = """select distinct cast(?p as pic x(5)) from VNA1P006 
where ( (select -sum(sbin0_4)/?pn from VNA1P006),?pn)
= ( (select -?pn2/min(sdec6_4) from VNA1P006),?pn)
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s3')
    #
    stmt = """select distinct cast(?p as pic x(5)) from VNA1P006 
where (select -sum(sbin0_4)/cast(?pn as int) from VNA1P006)
= (select -cast(?pn2 as int)/min(sdec6_4) from VNA1P006)
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s4')
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
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s5')
    #
    stmt = """select distinct cast(?p as pic x(5)) from VNA1P006 
where ( (select -sum(sbin0_4)/cast(?pn as int) from VNA1P006)
,cast(?p as char(6)) )
= ( (select -cast(?pn2 as int)/min(sdec6_4) from VNA1P006)
,cast(?p as char(6)) )
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s6')
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
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s7')
    #
    #  Expect 10 matching rows.
    stmt = """select t.varchar0_uniq,u.varchar0_uniq
from BTA1P006 t, BTA1P006 u
where t.char2_2=u.char2_2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s8')
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
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s9')
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
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s10')
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
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s11')
    
    _testmgr.testcase_end(desc)

def test002(desc="""a02"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    # Test case name:      T1111:A02
    # Description:         Parallel execution in SQL with
    #                      2-way joins.
    #                      Testware leveraged from arkt1102, etc.
    #
    # =================== End Test Case Header  ===================
    
    # Get parallelism defaults for this test unit's execution.
    # Includes choice of global schema.
    #
    # Defaults and defines for this testunit.
    #
    # Get the parameter to use the partitioned global db.
    # Catalog for 'global database #11'.
    #
    #
    # Turn Parallel ON.
    
    stmt = """control query default ATTEMPT_ESP_PARALLELISM 'ON';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #   control query default PARALLEL_EXECUTION 'ON';
    #
    # And let's look at SHOWSHAPE
    
    stmt = """control query default ATTEMPT_ESP_PARALLELISM 'ON';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """control query default PARALLEL_NUM_ESPS '1';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # Jan 9, 1999 -- Try with 2 ESPs.
    stmt = """control query default PARALLEL_NUM_ESPS '2';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """control query default PARALLEL_NUM_ESPS '4';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #  ---------------------------
    #  Check the values of views that are combinations of JOIN, GROUP BY.
    #  Tables include unique and non-unique values:
    #  ---------------------------
    #
    #  View containing CASE:
    stmt = """select * from VNA1P009 
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s0')
    #
    #  View containing string functions:
    stmt = """select CLOWER, CUPPER from VNA1P007 
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s1')
    #
    #  ---------------------------
    #       Id: JT.161      NATURAL JOIN on view containing simple and searched CASE.
    #       Id: JT.154      NATURAL JOIN on view containing ANSI String functions.
    #  ---------------------------
    #
    #  Expect 14 rows (8 as in view plus 6).
    stmt = """select * from VNA1P009 v91
natural join VNA1P009 v92
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s2')
    #
    # Expect 0 row.
    stmt = """select * from
( select * from VNA1P009 
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
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s3')
    #
    #  ---------------------------
    #       Id: JT.162      RIGHT OUTER JOIN on view containing simple and searched CASE.
    #       Id: JT.155      RIGHT OUTER JOIN on view containing ANSI String functions.
    #  ---------------------------
    #
    #  Expect 8 rows as in view, no match.
    stmt = """select v91.csimple as v91_csimple, v92.csimple as v92_csimple
from VNA1P009 v91
right outer join VNA1P009 v92
--  on (v91.csimple, v92.csimple) like ('Value%','Value B%')
on v91.csimple like 'Value %' and
v92.csimple like 'Value B%'
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s4')
    #
    #  Expect 48 (6*8) rows.
    stmt = """select * from
( select * from VNA1P009 
) v9(a,b)
right outer join
( select CLOWER, CUPPER from VNA1P007 
) v7(a,b)
on (1=1)
order by 1, 2, 3    

;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s5')
    #
    #  Repeat with LEFT JOIN, without derived tables.
    stmt = """select v9.*, CLOWER, CUPPER
from VNA1P007 v7
left outer join VNA1P009 v9
on csimple like 'Value %'
--       and CLOWER like 'aaaa%'
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s6')
    #
    #  Repeat with specific columns in select list and without
    #  derived tables; different predicate.
    stmt = """select CLOWER, CUPPER
from VNA1P009 v9
right outer join VNA1P007 v7
on csimple like 'Value %'
--       and CLOWER like 'aaaa%'
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s7')
    #  Empty right side:
    stmt = """select CLOWER, CUPPER
from VNA1P009 v9
right outer join VNA1P007 v7
on (1=0)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s8')
    #
    stmt = """select CLOWER, CUPPER
from VNA1P009 v9
right outer join VNA1P007 v7
on CLOWER between 'London' and 'Paris'
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s9')
    #
    #  Empty left side:
    stmt = """select CLOWER, CUPPER
from VNA1P009 v9
right outer join VNA1P007 v7
on csimple between 'London' and 'Paris'
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s10')
    #
    #  Expect 36 rows (6*6) as in view.
    stmt = """select v71.CUPPER, v72.CLOWER from VNA1P007 v71
right outer join VNA1P007 v72
on (1=1)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s11')
    #
    #  ---------------------------
    #       Id: JT.163      INNER JOIN on view containing simple and searched CASE.
    #       Id: JT.156      INNER JOIN on view containing ANSI String functions.
    #  ---------------------------
    #
    #  Expect 64 rows (8*8 as in view), no match.
    stmt = """select v91.csimple, v92.csearched
from VNA1P009 v91
inner join VNA1P009 v92
on (1=1)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s12')
    #
    #  Expect ?? rows as in view.
    stmt = """select v91.csimple, v92.csearched
from VNA1P009 v91
inner join VNA1P009 v92
on ( v91.csimple LIKE '%3')
and (v92.csearched between 'rabid' and 'silly' )
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s13')
    #
    #  Expect 8 rows.
    stmt = """select * from
( select * from VNA1P009 
) v9(a,b)
inner join
( select CLOWER, CUPPER from VNA1P007 
) v7(a,b)
on (v7.a LIKE 'b%' )
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s14')
    #
    #  Expect 30 rows (6*5).
    stmt = """select v71.CUPPER, v72.CLOWER from VNA1P007 v71
inner join VNA1P007 v72
on (lower(v71.cupper) <> v72.clower)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s15')
    #
    #  ---------------------------
    #       Id: JT.164      Simple CASE contains NATURAL JOIN.
    #  ---------------------------
    #
    #  Expect 3 rows.
    stmt = """select distinct csimple, char_length(csimple) as length_csimple
FROM VNA1P009 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s16')
    #
    stmt = """select distinct CASE char_length(csimple)
WHEN 1
THEN 'Text: csimple length is one'
ELSE 'Text: Not WHEN 1 THEN'
END
as case_result
FROM VNA1P009 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s17')
    #
    #  Natural Join in RVC for truth value in WHEN.
    stmt = """select distinct CASE
WHEN -- 1
--  Expect 14 rows (8 as in view plus 6).
( 14 = ( select count(*)
from VNA1P009 v91
natural join VNA1P009 v92
)
)
THEN 'Text: the total is 14'
ELSE 'Text: the total is NOT 14'
END
FROM VNA1P009 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s18')
    #
    stmt = """select distinct CASE
WHEN -- 1
--  Expect 14 rows (8 as in view plus 6).
( 14 = 14
)
THEN 'Text: the total is 14'
ELSE 'Text: the total is NOT 14'
END
FROM VNA1P009 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s19')
    #
    stmt = """select CASE char_length(csimple)
WHEN 1
THEN
'Max = ' ||
( select max(csimple) from VNA1P009 v91
natural join VNA1P009 v92
)
ELSE
'Min = ' ||
( select min(csimple)
from VNA1P009 v91
natural join VNA1P009 v92
)
END
FROM VNA1P009 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s20')
    #
    stmt = """select CASE char_length(csimple)
WHEN 1
THEN
'Max = ' ||
( select max(csimple) from VNA1P009 v91
natural join VNA1P009 v92
)
ELSE
'Min = ' ||
( select min(v91.csimple) from VNA1P009 v91
right join VNA1P009 v92
on (1=1)
)
END
FROM VNA1P009 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s21')
    #
    stmt = """select CASE char_length(csimple)
WHEN 1
THEN
'Max = ' ||
( select max(csimple) from VNA1P009 v91
natural join VNA1P009 v92
)
ELSE
'Min = ' ||
( select min(csimple) from VNA1P009 v91
natural join VNA1P009 v92
)
END
FROM VNA1P009 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s22')
    #
    #  ---------------------------
    #       Id: JT.157      JOIN view columns defined as ANSI numeric-value functions (CHAR_LENGTH, POSITION).
    #  ---------------------------
    #
    stmt = """select v1.cChar_length, v1.cPosition
from VNA1P007 v1
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s23')
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
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s24')
    #
    #  ---------------------------
    #       Id: JT.158      JOIN view columns defined as ANSI string-value functions (SUBSTRING, TRIM).
    #  ---------------------------
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
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s25')
    #
    #  ---------------------------
    #       Id: JT.159      JOIN view columns defined as ANSI string operator: || (concatenate on character strings).
    #       Id: JT.160      JOIN view columns defined as ANSI numeric-value functions (LOWER, UPPER).
    #  ---------------------------
    #
    #  Expect 6 rows
    stmt = """select v1.cUpper, v2.cLower
from VNA1P007 v1
right outer join VNA1P007 v2
on v1.cUpper = upper(v2.cLower)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s26')
    
    _testmgr.testcase_end(desc)

def test003(desc="""a03"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    # Test case name:      T1111:A03
    # Description:         Parallel execution in SQL with
    #                      2-way joins.
    #                      Additional Testware.
    #
    # =================== End Test Case Header  ===================
    
    # Get parallelism defaults for this test unit's execution.
    # Includes choice of global schema.
    #
    # Defaults and defines for this testunit.
    #
    # Get the parameter to use the partitioned global db.
    # Catalog for 'global database #11'.
    #
    # Turn Parallel ON.
    
    stmt = """control query default ATTEMPT_ESP_PARALLELISM 'ON';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #   control query default PARALLEL_EXECUTION 'ON';
    #
    # And let's look at SHOWSHAPE
    #   Set Showshape On ;
    # Nov 98 for setting up ref files.
    # TEMPORARILY debugging run with non-partitioned global db.
    #   obey ../tools11/ci11defs;
    
    stmt = """control query default ATTEMPT_ESP_PARALLELISM 'ON';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """control query default PARALLEL_NUM_ESPS '1';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    # Jan 9, 1999 -- Try with 2 ESPs.
    stmt = """control query default PARALLEL_NUM_ESPS '2';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """control query default PARALLEL_NUM_ESPS '4';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # Force autocommit:
    stmt = """Set Transaction Autocommit On;"""
    output = _dci.cmdexec(stmt)
    #
    #  ---------------------------
    #  Join key to key for table 1.
    #       primary key ( varchar5_10, ubin15_uniq , char0_10 )
    #  ---------------------------
    #  prepare s from
    stmt = """Select Count( t1.varchar5_10 ), Count( t2.ubin15_uniq )
From BTA1P001 t1
Join BTA1P001 t2
On ( t1.varchar5_10, t1.ubin15_uniq , t1.char0_10 )
= ( t2.varchar5_10, t2.ubin15_uniq , t2.char0_10 )
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s0')
    stmt = """Select Count( t1.varchar5_10 ), Count( t2.ubin15_uniq )
From BTA1P001 t1
Join BTA1P001 t2
On ( t1.varchar5_10, t1.ubin15_uniq )
= ( t2.varchar5_10, t2.ubin15_uniq )
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s1')
    stmt = """Select Count( t1.varchar5_10 ), Count( t2.ubin15_uniq )
From BTA1P001 t1
Join BTA1P001 t2
On ( t1.varchar5_10 )
= ( t2.varchar5_10 )
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s2')
    #
    #  ---------------------------
    #  Join key to key for all other tables.
    #  Include index and non-index columns.
    #  (2) primary key ( ubin3_uniq DESC )
    #  (3) Etc.
    #  ---------------------------
    stmt = """Select Count( t1.ubin3_uniq ), Count( t2.ubin15_uniq )
From BTA1P001 t1
Join BTA1P001 t2
On ( t1.ubin3_uniq )
= ( t2.ubin3_uniq )
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s3')
    #  ---------------------------
    #  Join index to index for table 2.
    #       INDEX IXA1P002a ON BTA1P002 ( varchar0_4 )
    #       INDEX IXA1P002b ON BTA1P002 ( sdec13_uniq )
    #  ---------------------------
    stmt = """Select Count( t1.varchar0_4 ), Count( t2.varchar0_4 )
From BTA1P002 t1
Join BTA1P002 t2
On ( t1.varchar0_4 )
= ( t2.varchar0_4 )
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s4')
    stmt = """Select Count( t1.sdec13_uniq ), Count( t2.sdec13_uniq )
From BTA1P002 t1
Left Join BTA1P002 t2
On ( t1.sdec13_uniq )
= ( t2.sdec13_uniq )
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s5')
    #
    #  ---------------------------
    #  Join primary key of table 1 to index for table 2.
    #       primary key ( varchar5_10, ... )
    #       INDEX IXA1P002a ON BTA1P002 ( varchar0_4 )
    #  ---------------------------
    stmt = """Select Count( t1.varchar5_10 ), Count( t2.varchar0_4 )
From BTA1P001 t1
Join BTA1P002 t2
On ( t1.varchar5_10 )
> ( t2.varchar0_4 )
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s6')
    
    _testmgr.testcase_end(desc)

def test004(desc="""a04"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    # Test case name:      T1111:A04
    # Description:         Parallel execution in SQL with
    #                      3-way joins.
    #                      Testware leveraged from arkt1102.
    #
    # =================== End Test Case Header  ===================
    
    # Get parallelism defaults for this test unit's execution.
    # Includes choice of global schema.
    #
    # Defaults and defines for this testunit.
    #
    # Get the parameter to use the partitioned global db.
    # Catalog for 'global database #11'.
    #
    # Turn Parallel ON.
    
    stmt = """control query default ATTEMPT_ESP_PARALLELISM 'ON';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """control query default ATTEMPT_ESP_PARALLELISM 'ON';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """control query default PARALLEL_NUM_ESPS '1';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    # Jan 9, 1999 -- Try with 2 ESPs.
    stmt = """control query default PARALLEL_NUM_ESPS '2';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """control query default PARALLEL_NUM_ESPS '4';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #  ---------------------------
    #  Subquery transformations: in DTs and views.
    #  Some of these tests are done in context of other queries.
    #  ---------------------------
    #
    #  ---------------------------
    #  Part of Id: TF.043: Subqueries in <select list> upon Derived Table
    #  ---------------------------
    #
    stmt = """select * from VNA1P005 v0
order by 1,3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s0')
    #
    #  Non-grouped query.
    #  Expect 6 rows of ( ( -4344 'DA' 'AA' ) ).
    stmt = """select (select V.n1 from VNA1P005 V
where V.n1 < -4300
) as c1
, (select v1.c2 from VNA1P005 v1 where v1.n1 = -2789 ) as c2
, (select v0.c2 from VNA1P005 v0 where v0.c2 < 'B' ) as c3
from (select * from VNA1P005 ) dt
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s1')
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
from (select * from VNA1P005 ) dt
where -4344
= (select distinct dt.n1 from VNA1P005 V where dt.n1 < -4300 )
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s2')
    #
    #  2 OR-ed subqueries in <where pred> upon Derived Table.
    #  Again expect 1 row: ( -4344 'AA' 'BA' 'BA' )
    stmt = """select *
from (select * from VNA1P005 ) dt
where -4344
= (select distinct dt.n1 from VNA1P005 V where dt.n1 < -4300 )
-- 	or ('a')
--          > (select distinct dt.c2 from VNA1P005 v1 where dt.n1 = -2789 )
or (select distinct dt.c3 from VNA1P005 v1 where dt.n1 = -4344 )
> ('a')
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s3')
    #
    #  2 OR-ed subqueries in <where pred> upon Derived Table.
    #  Expect 2 rows: ( ( -4344 'AA' 'BA' 'BA' ) ( -2789 'DA' 'EA' NULL) )
    stmt = """select *
from (select * from VNA1P005 ) dt
where -4344
= (select distinct dt.n1 from VNA1P005 V where dt.n1 < -4300 )
or ('a')
> (select distinct dt.c2 from VNA1P005 v1 where dt.n1 = -2789 )
-- 	or (select distinct dt.c3 from VNA1P005 v1 where dt.n1 = -4344 )
--          > ('a')
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s4')
    #
    #  3 OR-ed subqueries (2 ORs) in <where pred> upon Derived Table.
    #  Expect 2 rows: ( ( -4344 'AA' 'BA' 'BA' ) ( -2789 'DA' 'EA' NULL) )
    stmt = """select *
from (select * from VNA1P005 ) dt
where -4344
= (select distinct dt.n1 from VNA1P005 V where dt.n1 < -4300 )
or ('a')
> (select distinct dt.c2 from VNA1P005 v1 where dt.n1 = -2789 )
or (select distinct dt.c3 from VNA1P005 v1 where dt.n1 = -4344 )
> ('a')
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s5')
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
from (select * from VNA1P005 ) dt
where ?pn
= (select distinct dt.n1 from VNA1P005 V where dt.n1 < (?pn+1) )
or ?p
> (select distinct dt.c2 from VNA1P005 v1 where dt.n1 = -2789 )
or (select distinct dt.c3 from VNA1P005 v1 where dt.n1 = ?pn )
> ?p
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s6')
    #
    #  Add GROUP BYs to get the query we want.
    stmt = """select * from VNA1P005 dt
where ?pn
= ( select distinct dt.n1 from VNA1P005 V where dt.n1 < (?pn+1)
group by dt.n1
)
or ?p
> ( select distinct dt.c2 from VNA1P005 v1
where dt.n1 = -2789
group by dt.c2
)
or ( select distinct dt.c3 from VNA1P005 v1
where dt.n1 = ?pn
group by dt.c3
)
> ?p
group by n1, c2, c3, c4
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s7')
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
from (select * from VNA1P005 ) dt
where -4344
= (select distinct dt.n1 from VNA1P005 V where dt.n1 < -4300 )
or ('a')
> (select distinct dt.c2 from VNA1P005 v1 where dt.n1 = -2789 )
or (select distinct dt.c3 from VNA1P005 v1 where dt.n1 = -4344 )
> ('a')
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s8')
    # Same with params appearing in more than one place.
    stmt = """set param ?pn -4344 ;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?px a ;"""
    output = _dci.cmdexec(stmt)
    stmt = """select *
from (select * from VNA1P005 ) dt
where ?pn
= (select distinct dt.n1 from VNA1P005 V where dt.n1 < (?pn+1) )
or ?p
> (select distinct dt.c2 from VNA1P005 v1 where dt.n1 = -2789 )
or (select distinct dt.c3 from VNA1P005 v1 where dt.n1 = ?pn )
> ?p
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s9')
    #
    #  ---------------------------
    #       Id: TF.045       Subqueries in <select list> on Grouped view.
    #                        VNA1P005 is a grouped view with an outer join.
    #  ---------------------------
    #
    stmt = """select * from VNA1P005 v0
order by 1,3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s10')
    stmt = """select distinct v0.c3,(select n1 from VNA1P005 V where n1 < -4300)
, (select v1.c2 from VNA1P005 v1 where v1.n1 = -2789 )
, (select count(c2) from VNA1P005 )
from VNA1P005 v0
order by 1,3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s11')
    #
    #  ---------------------------
    #       Id: TF.046       Subqueries in <where pred> on Grouped view.
    #                        VNA1P005 is a grouped view (also has outer join)
    #  ---------------------------
    #
    #  6 rows.
    stmt = """select * from VNA1P005 v0
where ( select max(v1.c3) from VNA1P005 v1 ) > 'AAAAA'
order by 1,3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s12')
    #  6 rows.
    stmt = """select * from VNA1P005 v0
where ( select count(v1.c2) from VNA1P005 v1 where v1.c2 IS NOT NULL )
= 4
order by 1,3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s13')
    #  1 row.
    stmt = """select * from VNA1P005 v0
where ( select distinct v0.c2 from VNA1P005 v1 where v0.c2 = 'DA' )
= 'DA'
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s14')
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
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s15')
    stmt = """select (select max(VARCHAR0_500) from BTA1P008)
, (select min(v1.CHAR3_4) from BTA1P008 v1)
, (select count(v2.SDEC4_N20) from BTA1P008 v2)
from VNA1P008 v0
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s16')
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
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s17')
    #  Same with correlation name from outer table.
    #  Note, however, ANSI 7.6 SR 3: "No <column reference> contained
    #        in a <subquery> in the <search condition> that references
    #        a column of 'T' (the result of the preceding <from clause>
    #        shall be specified in a <set [aggregate] function
    #        specification>."
    #  Therefore, "where ( select max(v0.CHAR3_4) from BTA1P008 v1)  > 'B'"
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
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s18')
    #
    stmt = """select CHAR10_20, CHAR13_100, VARCHAR15_UNIQ
from BTA1P001 
order by 1,2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s19')
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
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s20')
    #
    stmt = """select CHAR10_20, CHAR13_100, VARCHAR15_UNIQ
from BTA1P001 
where CHAR10_20 = CHAR13_100
and CHAR10_20 = VARCHAR15_UNIQ
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s21')
    #
    #  check with 3 preds, a=b and b=c and c=a
    stmt = """select CHAR10_20, CHAR13_100, VARCHAR15_UNIQ
from BTA1P001 
where CHAR10_20 = CHAR13_100
and CHAR13_100 = VARCHAR15_UNIQ
and VARCHAR15_UNIQ = CHAR10_20
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s22')
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
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s23')
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
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s24')
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
From VNA1P004 v
Order by 1,2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s25')
    #  Expect 14 rows.
    stmt = """Select Cast( v.varchar0_4 As Char(3) ) As cv
, v.char0_1000
, Cast( v.sbin7_2 As smallint ) As csi
From VNA1P004 v, VNA1P004 v2
Where ( v.varchar0_4 )
= (v2.varchar0_4 )
Order by 1,2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s26')
    #  Expect 12 rows.
    stmt = """Select Cast( v.varchar0_4 As Char(3) ) As cv
, v.char0_1000
, Cast( v.sbin7_2 As smallint ) As csi
From VNA1P004 v, VNA1P004 v2
Where ( v.varchar0_4,  v.char0_1000,  v.sbin7_2 )
= (v2.varchar0_4, v2.char0_1000, v2.sbin7_2 )
Order by 1,2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s27')
    #
    #  Expect cols N1, C2, C3, C4.
    #  Expect 6 rows in View.
    stmt = """Select *
From VNA1P005 
Order by 1, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s28')
    #  Expect 6 rows matching on non-null C2.
    stmt = """Select v.N1,  v.C2,  v.C3,  v.C4, v2.N1, v2.C2, v2.C3, v2.C4
From VNA1P005 v, VNA1P005 v2
Where ( v.C2 )
= (v2.C2 )
Order by 1, 5
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s29')
    #  Expect 3 rows matching on non-null columns.
    stmt = """Select v.N1,  v.C2,  v.C3,  v.C4, v2.N1, v2.C2, v2.C3, v2.C4
From VNA1P005 v, VNA1P005 v2
Where ( v.N1,  v.C2,  v.C3,  v.C4 )
= (v2.N1, v2.C2, v2.C3, v2.C4 )
Order by 1, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s30')
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
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s31')
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
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s32')
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
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s33')
    #
    #  Expect 7 rows.
    stmt = """Select v.sdec6_4, v2.sdec6_4
From VNA1P008 v, VNA1P008 v2
Where ( v.sdec6_4 )
= (v2.sdec6_4 )
Order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s34')
    
    _testmgr.testcase_end(desc)

def test005(desc="""a05"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    # Test case name:      T1111:A05
    # Description:         Parallel execution in SQL with
    #                      over 3-way joins.
    #                      Testware leveraged from arkt1103.
    #
    # =================== End Test Case Header  ===================
    
    # Get parallelism defaults for this test unit's execution.
    # Includes choice of global schema.
    #
    # Defaults and defines for this testunit.
    #
    # Get the parameter to use the partitioned global db.
    # Catalog for 'global database #11'.
    #
    # Turn Parallel ON.
    stmt = """control query default ATTEMPT_ESP_PARALLELISM 'ON';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """control query default ATTEMPT_ESP_PARALLELISM 'ON';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """control query default PARALLEL_NUM_ESPS '1';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    # Try with 2 ESPs.
    stmt = """control query default PARALLEL_NUM_ESPS '2';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """control query default PARALLEL_NUM_ESPS '4';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #  ---------------------------
    #  Tables created in preparation for test unit.
    #  ---------------------------
    #
    #  ---------------------------
    #  Within Derived Table use NATURAL JOIN
    #  ---------------------------
    #
    #  ---------------------------
    #  Check contents of interesting view.
    #  ---------------------------
    #  Expect 6 rows of our global view.
    stmt = """select N1, C2, C3, C4
from VNA1P005 j1
order by N1, C3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s0')
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
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s1')
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
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s2')
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
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s3')
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
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s4')
    #
    #  ---------------------------
    #  Combinations of RIGHT JOINs
    #  ---------------------------
    #       Id: JT.211      RIGHT JOIN/LEFT JOIN combinations.
    #  ---------------------------
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
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s5')
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
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s6')
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
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s7')
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
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s8')
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
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s9')
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
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s10')
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
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s11')
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
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s12')
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
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s13')
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
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s14')
    
    _testmgr.testcase_end(desc)

def test006(desc="""a06"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    # Test case name:      T1111:A06
    # Description:         Parallel execution in SQL with
    #                      over 3-way joins.
    #                      Testware leveraged from arkt1103.
    #
    # =================== End Test Case Header  ===================
    
    # Get parallelism defaults for this test unit's execution.
    # Includes choice of global schema.
    #
    # Defaults and defines for this testunit.
    #
    # Get the parameter to use the partitioned global db.
    # Catalog for 'global database #11'.
    #
    # Turn Parallel ON.
    stmt = """control query default ATTEMPT_ESP_PARALLELISM 'ON';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """control query default ATTEMPT_ESP_PARALLELISM 'ON';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """control query default PARALLEL_NUM_ESPS '1';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    # Jan 9, 1999 -- Try with 2 ESPs.
    stmt = """control query default PARALLEL_NUM_ESPS '2';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """control query default PARALLEL_NUM_ESPS '4';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #  ---------------------------
    #  Tables created in preparation for test unit.
    #  ---------------------------
    #
    #  Preliminary review of contents of views.
    stmt = """select * from VNA1P005 t1
order by n1, c3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s0')
    #
    #  ---------------------------
    #       Id: JT.273      Within ON clause of JOIN, RVC contains Columns.
    #       Id: JT.274      Within ON clause of JOIN, RVC is a list containing literals.
    #  ---------------------------
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
    # value of interest for column c2.
    stmt = """set param ?paa 'AA' ;"""
    output = _dci.cmdexec(stmt)
    # value of interest for column c3.
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
    #  ---------------------------
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
    # =================  Begin Test Case Header  ==================
    #
    # Test case name:      T1111:A07
    # Description:         Parallel execution in SQL with
    #                      4-way join views.
    #                      Testware leveraged from arkt1103.
    #
    # =================== End Test Case Header  ===================
    
    # Get parallelism defaults for this test unit's execution.
    # Includes choice of global schema.
    #
    # Defaults and defines for this testunit.
    #
    # Get the parameter to use the partitioned global db.
    # Catalog for 'global database #11'.
    #
    # Turn Parallel ON.
    stmt = """control query default ATTEMPT_ESP_PARALLELISM 'ON';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """control query default ATTEMPT_ESP_PARALLELISM 'ON';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """control query default PARALLEL_NUM_ESPS '1';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    # Jan 9, 1999 -- Try with 2 ESPs.
    stmt = """control query default PARALLEL_NUM_ESPS '2';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """control query default PARALLEL_NUM_ESPS '4';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # ---------------------------
    # Objects created in preparation for test unit.
    # ---------------------------
    #
    #  ---------------------------
    #       Id: VM.011a     <view1> is <table1> INNER JOIN <table2> LEFT JOIN <table3> LEFT JOIN <table4>, joining on ajacent tables
    #       Id: VM.011b     <view2> is <table1> LEFT JOIN <table2> INNER JOIN <table3> LEFT JOIN <table4>, some join on non-ajacent tables (e.g. ON <table1.colx>=<table3.coly>
    #       Id: VM.011c     <view3> is <table1> LEFT JOIN <table2> LEFT JOIN <table3> INNER JOIN <table4> GROUP BY <columns>;
    #       Id: VM.011d     <view4> is <table1> LEFT JOIN <table2> LEFT JOIN <table3> LEFT JOIN <table4>; DISTINCT rows.
    #       Id: VM.011e     <view5> is <table1> LEFT JOIN <table2> LEFT JOIN <table3> LEFT JOIN <table4>; aggregates on results.
    #  ---------------------------
    #
    #  ---------------------------
    #  Check the values of views that are combinations of JOIN, GROUP BY.
    #  Tables include unique and non-unique values:
    #  ---------------------------
    stmt = """select * from view1 order by c1, c2, c4 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s0')
    stmt = """select * from view2 order by 1, 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s1')
    stmt = """select * from view3 order by c1, c7, c8 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s2')
    stmt = """select * from view4 order by c1, c2, c4 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s3')
    stmt = """select c1, c2, c3, c4, c5 from view5 order by 1, 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s4')
    stmt = """select c1, c2, c6, c7, c8 from view5 order by 1, 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s5')
    #  ---------------------------
    #
    #  ---------------------------
    #  OUTER Join the views.
    #  ---------------------------
    #
    #  Expect 2 rows (('abcd' '1xz' 'abcd' 'abcd' '1xz' abcd')
    #                 (NULL  NULL  NULL  'ac' '1xw'  NULL))
    stmt = """select v1.c1, v1.c2, v1.c3, v2.c1, v2.c2, v2.c3 from view1 v1
right join view2 v2
on v1.c1=v2.c1
order by 1, 5
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s6')
    #
    #  Expect 2 rows ((NULL  NULL  NULL  'ac' '1xw'  NULL)
    #                 (NULL  NULL  NULL  'abcd' '1xz' abcd'))
    stmt = """select v1.c1, v1.c2, v1.c3, v2.c1, v2.c2, v2.c3 from view1 v1
right join view2 v2
on v1.c1=v2.c2 -- Change JOIN condition from the above.
order by 1, 5
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s7')
    #
    #  Vary the combinations of joined views.
    #  Expect 5 rows with all columns 'abcd'.
    stmt = """select v2.c1, v2.c3, v2.c5, v3.c1, v3.c3, v3.c5 from view2 v2
right join view3 v3
on v2.c1=v3.c1
order by 1, 5
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s8')
    #
    #  Expect 10 rows: 5 rows with all columns 'abcd';
    #  the other 5 rows of view4 are NULL-extended.
    stmt = """select v3.c1, v3.c3, v3.c5, v4.c1, v4.c3, v4.c5 from view3 v3
right join view4 v4
on v3.c1=v4.c1
order by 1, 4, 5
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s9')
    #
    #  Expect 1 row with all columns 'abcd'.
    stmt = """select v4.c1, v4.c3, v4.c5, v5.c1, v5.c3, v5.c5 from view4 v4
right join view5 v5
on v4.c1=v5.c1
order by 1, 5
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s10')
    #
    #  ---------------------------
    #  NATURAL Join the views.
    #  ---------------------------
    #
    #  Expect 1 matching row.
    stmt = """select * from view1 v1
NATURAL join view2 v2
order by 1, 5
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s11')
    #
    #  Expect 1 matching row.
    stmt = """select * from view2 v2
NATURAL join view3 v3
order by 1, 5
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s12')
    #
    #  Expect 1 matching row.
    stmt = """select * from view3 v3
NATURAL join view4 v4
order by 1, 5
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s13')
    #
    #  Cannot made NATURAL join of view4 with view5 because
    #  column data types differ. Likewise for view5 and view1.
    #
    #  ---------------------------
    #  INNER Join the views.
    #  ---------------------------
    #
    #  Expect 1 row (('abcd' '1xz' 'abcd' 'abcd' '1xz' abcd')}
    stmt = """select v1.c1, v1.c2, v1.c3, v2.c1, v2.c2, v2.c3 from view1 v1
INNER join view2 v2
on v1.c1=v2.c1
order by 1, 5
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s14')
    #
    #  Expect 5 rows with all columns 'abcd'.
    stmt = """select v2.c1, v2.c3, v2.c5, v3.c1, v3.c3, v3.c5 from view2 v2
INNER join view3 v3
on v2.c1=v3.c1
order by 1, 5
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s15')
    #
    #  Expect 5 rows with all columns 'abcd'.
    stmt = """select v3.c1, v3.c3, v3.c5, v4.c1, v4.c3, v4.c5 from view3 v3
INNER join view4 v4
on v3.c1=v4.c1
order by 1, 5
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s16')
    #
    #  Expect 1 row with all columns 'abcd'.
    stmt = """select v4.c1, v4.c3, v4.c5, v5.c1, v5.c3, v5.c5 from view4 v4
INNER join view5 v5
on v4.c1=v5.c1
order by 1, 5
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s17')
    
    _testmgr.testcase_end(desc)

def test008(desc="""a08"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    # Test case name:      T1111:A08
    # Description:         Parallel execution in SQL with
    #                      Grouped views used in Joins.
    #                      Testware leveraged from arkt1103.
    #
    # =================== End Test Case Header  ===================
    
    # Get parallelism defaults for this test unit's execution.
    # Includes choice of global schema.
    #
    # Defaults and defines for this testunit.
    #
    # Get the parameter to use the partitioned global db.
    # Catalog for 'global database #11'.
    #
    # Turn Parallel ON.
    stmt = """control query default ATTEMPT_ESP_PARALLELISM 'ON';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """control query default ATTEMPT_ESP_PARALLELISM 'ON';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """control query default PARALLEL_NUM_ESPS '1';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    # Jan 9, 1999 -- Try with 2 ESPs.
    stmt = """control query default PARALLEL_NUM_ESPS '2';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """control query default PARALLEL_NUM_ESPS '4';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #  ---------------------------
    #  Tables created in preparation for test unit.
    #  ---------------------------
    #
    #  ---------------------------
    #  Check contents of interesting view.
    #  ---------------------------
    #
    stmt = """select min(VARCHAR15_UNIQ), max(CHAR13_100)
from BTA1P001 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s0')
    #
    stmt = """select UDEC17_100, CHAR17_100
from VNA1P002 
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s1')
    #
    stmt = """select UBIN15_UNIQ , SDEC15_10 , SBIN16_20
, UBIN16_1000 , SBIN17_UNIQ , SDEC17_20
from VUA1P003 
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s2')
    #
    #  Expect 6 rows of our global view.
    stmt = """select *
from VNA1P005 t1
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s3')
    #
    #  ---------------------------
    #       Id: JT.182      JOIN contained in DTs within Subquery within Select list
    #                       Should get -2789, repeated for the number of rows ( )
    #                       in the table in the main query -- for which
    #                       we use the view again.
    #  ---------------------------
    stmt = """select N1 from VNA1P005 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s4')
    stmt = """select min(VARCHAR15_UNIQ), max(CHAR13_100)
from BTA1P001 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s5')
    #  Expect (-2389).
    stmt = """select distinct
( select max(N1) from
( select N1, C2, C3, C4
from VNA1P005 
) t2
) from VNA1P005 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s6')
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
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s7')
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
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s8')
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
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s9')
    #
    #  ---------------------------
    #       Id: JT.183      JOIN contained in DTs within Subquery within WHERE clause
    #       Id: GV.041      Join of one Grouped view to another, in the right tree of a LEFT JOIN.
    #  ---------------------------
    #  TG:  GROUP BY (.VNA1P002)
    #  TAGH:aggregates, GROUP BY, HAVING (e.g., VNA1P005).
    #  ---------------------------
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
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s10')
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
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s11')
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
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s12')
    #
    #  ---------------------------
    #       Id: JT.184      JOIN contained in DTs within Subquery within ON clause
    #       Id: GV.042      Join of one Grouped view (in the right tree of a LEFT JOIN) to a non-Grouped view.
    #  ---------------------------
    #  TG:  GROUP BY (VNA1P002)
    #   (VUA1P003)
    #  ---------------------------
    stmt = """select cast(t3.UBIN15_UNIQ/t2.UDEC17_100 as pic 9999V99) as a
, cast(t3.SDEC15_10/t2.UDEC17_100      as pic 9V9999 ) as b
, cast(t3.SBIN16_20/t2.UDEC17_100      as pic 9V9999 ) as c
, cast(t3.UBIN16_1000/t2.UDEC17_100    as pic 9V9999 ) as d
, cast(t3.SBIN17_UNIQ/t2.UDEC17_100    as pic 9999V99) as e
, cast(t3.SDEC17_20/t2.UDEC17_100      as pic 9999V99) as f
from VNA1P002 t2
, BTA1P003 t3
order by 1, 3, 4, 5
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s13')
    #
    stmt = """select t2.UDEC17_100, t3.UBIN16_1000
from VNA1P002 t2
left join BTA1P003 t3
on (1=1)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s14')
    #
    #  ---------------------------
    #       Id: GV.043      Join of one Grouped view (in the right tree of a LEFT JOIN) to base table.
    #  ---------------------------
    #  TG:  GROUP BY (VNA1P002)
    #   (BTA1P003)
    #  ---------------------------
    stmt = """select UBIN15_UNIQ , SDEC15_10 , SBIN16_20
from BTA1P003 
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s15')
    #
    stmt = """select UBIN16_1000 , SBIN17_UNIQ , SDEC17_20
from BTA1P003 
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s16')
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
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s17')
    #
    #  ---------------------------
    #       Id: JT.???      NATURAL JOIN on joined table without aggregates.
    #       Id: JT.186a     Derived Table contains RIGHT JOIN
    #       Id: JT.186b     Derived Table contains RIGHT JOIN with GROUP BY.
    #  ---------------------------
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
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s18')
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
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s19')
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
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s20')
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
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s21')
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
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s22')
    
    _testmgr.testcase_end(desc)

def test009(desc="""a09"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    # Test case name:      T1111:A09
    # Description:         Parallel execution in SQL with
    #                      Grouped views used in Joins.
    #                      Testware leveraged from arkt1103.
    #
    # =================== End Test Case Header  ===================
    
    # Get parallelism defaults for this test unit's execution.
    # Includes choice of global schema.
    #
    # Defaults and defines for this testunit.
    #
    # Get the parameter to use the partitioned global db.
    # Catalog for 'global database #11'.
    #
    # Turn Parallel ON.
    stmt = """control query default ATTEMPT_ESP_PARALLELISM 'ON';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """control query default ATTEMPT_ESP_PARALLELISM 'ON';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """control query default PARALLEL_NUM_ESPS '1';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    # Try with 2 ESPs.
    stmt = """control query default PARALLEL_NUM_ESPS '2';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """control query default PARALLEL_NUM_ESPS '4';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #  ---------------------------
    #  Tables created in preparation for test unit.
    #  ---------------------------
    #
    #  ---------------------------
    #  Check potential aggregates, etc for derived tables.
    #  ---------------------------
    stmt = """select  SBIN4_2, CHAR13_100, VARCHAR15_UNIQ
,SBIN16_20,UBIN16_1000,SDEC19_1000
from BTA1P001 
order by 1, 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s0')
    #
    stmt = """select  UBIN4_4, SDEC4_10, UDEC4_2, SDEC11_20
from BTA1P002 
order by 1, 2, 4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s1')
    #
    stmt = """select  CHAR15_100, CHAR17_2
from BTA1P006 
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s2')
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
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s3')
    #
    #  BTA1P002: Non-integer numerics:
    stmt = """select min( UBIN4_4), max( UBIN4_4)
, min(SDEC4_10)  , max(SDEC4_10)
, min(UDEC4_2)  , max(UDEC4_2)
, min(SDEC11_20)  , max(SDEC11_20)
from BTA1P002 
order by 1, 3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s4')
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
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s5')
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
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s6')
    #
    #  ---------------------------
    #  TA:  aggregates (derived tables) joined to the other grouped views
    #       in turn.
    #  ---------------------------
    #  TA:  aggregates (derived tables)
    #  TG:  GROUP BY (VNA1P002)
    #  TAG: aggregates, GROUP BY (derived tables)
    #  TGH: GROUP BY and HAVING (VNA1P004)
    #  TAGH:aggregates, GROUP BY, HAVING (e.g., VNA1P005).
    #    (TA) RJ (TA2) ; (TA) RJ (TG); etc., making 25 (5*5 combinations)
    #  ---------------------------
    #       Id: JT.091a     RIGHT JOIN (TA) RJ (TA2)
    #  ---------------------------
    stmt = """select t1.SDEC19_1000
from BTA1P001 t1
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s7')
    stmt = """select min(t1.SDEC19_1000)
from BTA1P001 t1
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s8')
    stmt = """select t2.UBIN4_4
from BTA1P002 t2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s9')
    stmt = """select max(t2.UBIN4_4)
from BTA1P002 t2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s10')
    #
    #  (TA) RJ (TA)
    #  Expect 7 {(.3,.3) (.3,.3) 5*(Null,<value>)}
    stmt = """select t1.SDEC19_1000, t2.UBIN4_4
from BTA1P001 t1 right join BTA1P002 t2
on t1.SDEC19_1000=t2.UBIN4_4
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s11')
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
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s12')
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
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s13')
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
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s14')
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
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s15')
    #
    #  ---------------------------
    #       Id: JT.094a     INNER JOIN (TA) IJ (TA2)
    #  ---------------------------
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
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s16')
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
    #  ---------------------------
    #       Id: JT.091b     RIGHT JOIN (TA) RJ (TG)
    #       Id: JT.091f     RIGHT JOIN (TG) RJ (TA)
    #  TA:  aggregates (derived tables)
    #  TG:  GROUP BY (VNA1P002)
    #  ---------------------------
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
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s17')
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
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s18')
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
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s19')
    #
    stmt = """select min(UDEC17_100) from VNA1P002 t2 order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s20')
    stmt = """select SDEC4_10, SDEC11_20 from BTA1P001 t1 order by 1, 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s21')
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
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s22')
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
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s23')
    #
    #  ---------------------------
    #       Id: JT.091c     RIGHT JOIN (TA) RJ (TAG)
    #       Id: JT.091k     RIGHT JOIN (TAG) RJ (TA)
    #  TA:  aggregates (derived tables)
    #  TAG: aggregates, GROUP BY (derived tables)
    #  ---------------------------
    #
    #  Expect {AAAA AX}
    stmt = """select min(VARCHAR15_UNIQ), max(CHAR13_100)
from BTA1P001 t1
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s24')
    #
    #  Expect 6 rows as in table.
    stmt = """select min(VARCHAR15_UNIQ), max(CHAR13_100)
from BTA1P001 t2
group by CHAR13_100
order by 1, 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s25')
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
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s26')
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
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s27')
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
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s28')
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
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s29')
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
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s30')
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
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s31')
    #
    #  ---------------------------
    #       Id: JT.094c     INNER JOIN (TA) IJ (TAG)
    #       Id: JT.094k     INNER JOIN (TAG) IJ (TA)
    #  ---------------------------
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
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s32')
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
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s33')
    #
    #  ---------------------------
    #       Id: JT.091d     RIGHT JOIN (TA) RJ (TGH)
    #       Id: JT.091p     RIGHT JOIN (TGH) RJ (TA)
    #       Id: JT.153      HAVING clause for JOIN contains ANSI String function
    #  ---------------------------
    #  TA:  aggregates (derived tables)
    #  TGH: GROUP BY and HAVING (VNA1P004)
    #  ---------------------------
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
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s34')
    #
    #  Check out base table if can't get view columns (are these same as view
    #  will be??)
    stmt = """select VARCHAR0_4 ,CHAR0_1000
from BTA1P004 
order by 1, 2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s35')
    stmt = """select SBIN7_2
,VARCHAR5_10     ,CHAR6_20      ,UBIN15_UNIQ
,VARCHAR15_UNIQ  ,CHAR16_UNIQ
from BTA1P004 
order by 1, 2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s36')
    #
    #  >>>??? Expect 3 rows { (A ...), (A ...), (CAA ...) }
    stmt = """select  VARCHAR0_4 ,VARCHAR5_10 ,VARCHAR15_UNIQ
from BTA1P004 
group by VARCHAR0_4 ,VARCHAR5_10 ,VARCHAR15_UNIQ
having lower(VARCHAR0_4||'x') > 'ab'
order by 1,2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s37')
    #
    stmt = """select VARCHAR5_10 ,substring( VARCHAR5_10 from 4 for 3)
from BTA1P004 
order by 1, 2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s38')
    #  >>>??? Expect 2 rows { (A ...), (AAA ...) } with 'AAA' at 4th to 6th of VARCHAR5_10
    stmt = """select  VARCHAR0_4 ,VARCHAR5_10 ,VARCHAR15_UNIQ
from BTA1P004 
group by VARCHAR0_4 ,VARCHAR5_10 ,VARCHAR15_UNIQ
having substring( VARCHAR5_10 from 4 for 3) = 'AAA'
order by 1,2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s39')
    #
    #  >>>>>>>>>>>>> view VNA1P004  Expected results ????????? >>>>>>>>>>
    #
    stmt = """select VARCHAR0_4 ,CHAR0_1000
from VNA1P004 
order by 1, 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s40')
    stmt = """select SBIN7_2
,VARCHAR5_10     ,CHAR6_20      ,UBIN15_UNIQ
,VARCHAR15_UNIQ  ,CHAR16_UNIQ
from VNA1P004 
order by 1, 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s41')
    #
    #  Expect 6 values as in view.
    stmt = """select min(VARCHAR15_UNIQ), max(VARCHAR15_UNIQ)
from VNA1P004 t2 group by VARCHAR15_UNIQ
order by 1, 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s42')
    stmt = """select min(VARCHAR15_UNIQ), VARCHAR15_UNIQ
from VNA1P004 t2
group by VARCHAR15_UNIQ
order by 1, 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s43')
    #
    #  Expect?
    stmt = """select VARCHAR0_4 ,CHAR0_1000
from VNA1P004 
order by 1, 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s44')
    stmt = """select SBIN7_2
,VARCHAR5_10     ,CHAR6_20      ,UBIN15_UNIQ
,VARCHAR15_UNIQ  ,CHAR16_UNIQ
from VNA1P004 
order by 1, 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s45')
    #
    stmt = """select VARCHAR0_4 ,CHAR0_1000
from VNA1P004 
order by 1, 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s46')
    stmt = """select SBIN7_2
,VARCHAR5_10     ,CHAR6_20      ,UBIN15_UNIQ
,VARCHAR15_UNIQ  ,CHAR16_UNIQ
from VNA1P004 
order by 1, 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s47')
    #
    #  >>>??? Expect 3 rows { (A ...), (A ...), (CAA ...) }
    stmt = """select  VARCHAR0_4 ,VARCHAR5_10 ,VARCHAR15_UNIQ
from VNA1P004 
group by VARCHAR0_4 ,VARCHAR5_10 ,VARCHAR15_UNIQ
having lower(VARCHAR0_4||'x') > 'ab'
order by 1,2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s48')
    #
    stmt = """select VARCHAR5_10 ,substring( VARCHAR5_10 from 4 for 3)
from VNA1P004 
order by 1,2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s49')
    
    #  >>>??? Expect 2 rows { (A ...), (AAA ...) } with 'AAA' at 4th to 6th of VARCHAR5_10
    stmt = """select  VARCHAR0_4 ,VARCHAR5_10 ,VARCHAR15_UNIQ
from VNA1P004 
group by VARCHAR0_4 ,VARCHAR5_10 ,VARCHAR15_UNIQ
having substring( VARCHAR5_10 from 4 for 3) = 'AAA'
order by 1,2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s50')
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
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s51')
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
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s52')
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
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s53')
    #
    #  ---------------------------
    #       Id: JT.094d     INNER JOIN (TA) IJ (TGH)
    #       Id: JT.094p     INNER JOIN (TGH) IJ (TA)
    #  ---------------------------
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
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s54')
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
    #  ---------------------------
    #       Id: JT.091e     RIGHT JOIN (TA) RJ (TAGH)
    #       Id: JT.091u     RIGHT JOIN (TAGH) RJ (TA)
    #       Id: JT.151      ON clause contains ANSI String functions
    #       Id: JT.152      WHERE clause for JOIN contains ANSI String functions
    #  ---------------------------
    #  TA:  aggregates (derived tables)
    #  TAGH:aggregates, GROUP BY, HAVING (e.g., VNA1P005).
    #  ---------------------------
    #
    #  Expect {AAAA AX}
    stmt = """select min(VARCHAR15_UNIQ), max(CHAR13_100)
from BTA1P001 t1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s55')
    #
    #  Expect 6 rows as in table.
    stmt = """select min(VARCHAR15_UNIQ), max(CHAR13_100)
from BTA1P001 t2
group by CHAR13_100
order by 1, 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s56')
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
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s57')
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
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s58')
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
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s59')
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
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s60')
    #
    #  ---------------------------
    #       Id: JT.094e     INNER JOIN (TA) IJ (TAGH)
    #       Id: JT.094u     INNER JOIN (TAGH) IJ (TA)
    #  ---------------------------
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
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s61')
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
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s62')
    #
    #  ---------------------------
    #  TG:  GROUP BY (VNA1P002) joined to the other grouped views
    #       in turn.
    #  ---------------------------
    #  TG:  GROUP BY (VNA1P002)
    #  TAG: aggregates, GROUP BY (derived tables)
    #  TGH: GROUP BY and HAVING (VNA1P004)
    #  TAGH:aggregates, GROUP BY, HAVING (e.g., VNA1P005).
    #    (TA) RJ (TA2) ; (TA) RJ (TG); etc., making 25 (5*5 combinations)
    #  ---------------------------
    #       Id: JT.091g     RIGHT JOIN (TG) RJ (TG)
    #  ---------------------------
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
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s63')
    #
    #  ---------------------------
    #       Id: JT.094g     INNER JOIN (TG) IJ (TG)
    #  ---------------------------
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
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s64')
    #
    #  ---------------------------
    #       Id: JT.091h     RIGHT JOIN (TG) RJ (TAG)
    #       Id: JT.091l     RIGHT JOIN (TAG) RJ (TG)
    #  ---------------------------
    #  TG:  GROUP BY (VNA1P002)
    #  TAG: aggregates, GROUP BY (derived tables)
    #
    #  Check results -- rows with 16 and 24 in the last column are used in
    #  joins in this set.
    stmt = """select SBIN1_100 , UDEC3_2000
, SBIN1_100 + 2 * UDEC3_2000 from BTA1P001 
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s65')
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
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s66')
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
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s67')
    #
    #  ---------------------------
    #       Id: JT.094h     INNER JOIN (TG) IJ (TAG)
    #       Id: JT.094l     INNER JOIN (TAG) IJ (TG)
    #  ---------------------------
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
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s68')
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
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s69')
    
    _testmgr.testcase_end(desc)

def test010(desc="""a10"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    # Test case name:      T1111:A10
    # Description:         Parallel execution in SQL with
    #                      Grouped views used in Joins.
    #                      Testware leveraged from arkt1103.
    #
    # =================== End Test Case Header  ===================
    
    # Get parallelism defaults for this test unit's execution.
    # Includes choice of global schema.
    #
    # Defaults and defines for this testunit.
    #
    # Get the parameter to use the partitioned global db.
    # Catalog for 'global database #11'.
    #
    # Turn Parallel ON.
    stmt = """control query default ATTEMPT_ESP_PARALLELISM 'ON';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """control query default ATTEMPT_ESP_PARALLELISM 'ON';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """control query default PARALLEL_NUM_ESPS '1';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    # Try with 2 ESPs.
    stmt = """control query default PARALLEL_NUM_ESPS '2';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """control query default PARALLEL_NUM_ESPS '4';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #  ---------------------------
    #  Tables created in preparation for test unit.
    #  ---------------------------
    #
    #  ---------------------------
    #  Check potential aggregates, etc for derived tables.
    #  ---------------------------
    stmt = """select  SBIN4_2, CHAR13_100, VARCHAR15_UNIQ
,SBIN16_20,UBIN16_1000,SDEC19_1000
from BTA1P001 
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s0')
    stmt = """select  UBIN4_4, SDEC4_10, UDEC4_2, SDEC11_20
from BTA1P002 
order by 1, 2, 4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s1')
    stmt = """select  CHAR15_100, CHAR17_2
from BTA1P006 
order by 1, 2
;"""
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
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s3')
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
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s5')
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
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s6')
    #
    #  ---------------------------
    #       Id: JT.091i     RIGHT JOIN (TG) RJ (TGH)
    #       Id: JT.091q     RIGHT JOIN (TGH) RJ (TG)
    #  TG:  GROUP BY (VNA1P002)
    #  TGH: GROUP BY and HAVING (VNA1P004)
    #  ---------------------------
    #
    #  (98-10-13) Changed table BTA1P004 to view VNA1P004,
    #             as originally planned.
    #
    stmt = """select CHAR6_20 from VNA1P004 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s7')
    #
    stmt = """select CHAR17_100, UDEC17_100 from VNA1P002 
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s8')
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
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s9')
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
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s10')
    #
    #  ---------------------------
    #       Id: JT.094i     INNER JOIN (TG) IJ (TGH)
    #       Id: JT.094q     INNER JOIN (TGH) IJ (TG)
    #  ---------------------------
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
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s11')
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
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s12')
    #
    #  ---------------------------
    #       Id: JT.091j     RIGHT JOIN (TG) RJ (TAGH)
    #       Id: JT.091v     RIGHT JOIN (TAGH) RJ (TG)
    #  TG:  GROUP BY (VNA1P002)
    #  TAGH:aggregates, GROUP BY, HAVING (e.g., VNA1P005).
    #  ---------------------------
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
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s13')
    #  Expect 3 nulls, 3 24's.
    stmt = """select  char_length(C2||C3||C4)
from VNA1P005 order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s14')
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
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s15')
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
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s16')
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
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s17')
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
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s18')
    #
    #  ---------------------------
    #       Id: JT.094j     INNER JOIN (TG) IJ (TAGH)
    #       Id: JT.094v     INNER JOIN (TAGH) IJ (TG)
    #  ---------------------------
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
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s19')
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
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s20')
    #
    #  ---------------------------
    #  TAG: aggregates, GROUP BY (derived tables) joined to the other grouped views
    #       in turn.
    #  ---------------------------
    #  TAG: aggregates, GROUP BY (derived tables)
    #  TGH: GROUP BY and HAVING (VNA1P004)
    #  TAGH:aggregates, GROUP BY, HAVING (e.g., VNA1P005).
    #    (TA) RJ (TA2) ; (TA) RJ (TG); etc., making 25 (5*5 combinations)
    #  ---------------------------
    #       Id: JT.091m     RIGHT JOIN (TAG) RJ (TAG)
    #  ---------------------------
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
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s21')
    #
    stmt = """select min(VARCHAR15_UNIQ), max(CHAR13_100)
from BTA1P001 t2
group by CHAR13_100
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s22')
    #
    stmt = """select VARCHAR15_UNIQ, max(CHAR13_100) from BTA1P001 t1
group by VARCHAR15_UNIQ
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s23')
    #
    stmt = """select min(VARCHAR15_UNIQ), CHAR13_100 from BTA1P001 t2
group by CHAR13_100
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s24')
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
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s25')
    #
    #  ---------------------------
    #       Id: JT.094m     INNER JOIN (TAG) IJ (TAG)
    #  ---------------------------
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
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s26')
    #
    #  ---------------------------
    #       Id: JT.091n     RIGHT JOIN (TAG) RJ (TGH)
    #       Id: JT.091r     RIGHT JOIN (TGH) RJ (TAG)
    #  TAG: aggregates, GROUP BY (derived tables)
    #  TGH: GROUP BY and HAVING (VNA1P004)
    #  ---------------------------
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
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s27')
    #
    stmt = """select CHAR17_100, UDEC17_100 from VNA1P002 
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s28')
    #
    #  (TAG) RJ (TGH)  Expect 9 rows (1 matched rows on ABAA...ABAA;
    #                  4 on {AX 8.30} for each row of VNA1P004;
    #                  4 on {GIAAEAAA 8.90} for each row of VNA1P004;
    stmt = """select *
from ( select min(VARCHAR15_UNIQ),UBIN16_1000 from BTA1P001 
group by UBIN16_1000
) t1(a, b)
right join
(select substring(CHAR6_20 for 4 ) from BTA1P004 
) t2(c)
on t2.c=t1.a or ( b > 8.1 )
order by 1, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s29')
    stmt = """select *
from ( select min(VARCHAR15_UNIQ),UBIN16_1000 from BTA1P001 
group by UBIN16_1000
) t1(a, b)
right join
(select substring(CHAR6_20 for 4 ) from VNA1P004 
) t2(c)
on t2.c=t1.a or ( b > 8.1 )
order by 1, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s30')
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
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s31')
    stmt = """select a,b,c
from (select substring(CHAR6_20 for 4 ) from VNA1P004 
) t2(c)
right join
( select min(VARCHAR15_UNIQ),UBIN16_1000 from BTA1P001 
group by UBIN16_1000
) t1(a, b)
on t2.c=t1.a or ( b > 8.1 )
order by 1, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s32')
    #
    #  ---------------------------
    #       Id: JT.094n     INNER JOIN (TAG) IJ (TGH)
    #       Id: JT.094r     INNER JOIN (TGH) IJ (TAG)
    #  ---------------------------
    #
    #  (TAG) IJ (TGH)  Expect 9 rows (1 matched rows on ABAA...ABAA;
    #                  4 on {AX 8.30} for each row of VNA1P004;
    #                  4 on {GIAAEAAA 8.90} for each row of VNA1P004;
    stmt = """select *
from ( select min(VARCHAR15_UNIQ),UBIN16_1000 from BTA1P001 
group by UBIN16_1000
) t1(a, b)
inner join
(select substring(CHAR6_20 for 4 ) from BTA1P004 
) t2(c)
on t2.c=t1.a or ( b > 8.1 )
order by 1, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s33')
    stmt = """select *
from ( select min(VARCHAR15_UNIQ),UBIN16_1000 from BTA1P001 
group by UBIN16_1000
) t1(a, b)
inner join
(select substring(CHAR6_20 for 4 ) from VNA1P004 
) t2(c)
on t2.c=t1.a or ( b > 8.1 )
order by 1, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s34')
    #
    #  (TGH) IJ (TAG)  Expect 9 rows as above.
    stmt = """select a,b,c
from (select substring(CHAR6_20 for 4 ) from BTA1P004 
) t2(c)
inner join
( select min(VARCHAR15_UNIQ),UBIN16_1000 from BTA1P001 
group by UBIN16_1000
) t1(a, b)
on t2.c=t1.a or ( b > 8.1 )
order by 1, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s35')
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
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s36')
    #
    #  ---------------------------
    #       Id: JT.091o     RIGHT JOIN (TAG) RJ (TAGH)
    #       Id: JT.091w     RIGHT JOIN (TAGH) RJ (TAG)
    #  TAG: aggregates, GROUP BY (derived tables)
    #  TAGH:aggregates, GROUP BY, HAVING (e.g., VNA1P005).
    #  ---------------------------
    #
    stmt = """select min(VARCHAR15_UNIQ), CHAR13_100 from BTA1P001 t2
group by CHAR13_100
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s37')
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
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s38')
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
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s39')
    #
    #  ---------------------------
    #       Id: JT.094o     INNER JOIN (TAG) IJ (TAGH)
    #       Id: JT.094w     INNER JOIN (TAGH) IJ (TAG)
    #  ---------------------------
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
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s40')
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
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s41')
    #
    #  ---------------------------
    #  TGH: GROUP BY and HAVING (VNA1P004) joined to the other grouped views
    #       in turn.
    #  ---------------------------
    #  TGH: GROUP BY and HAVING (VNA1P004)
    #  TAGH:aggregates, GROUP BY, HAVING (e.g., VNA1P005).
    #    (TA) RJ (TA2) ; (TA) RJ (TG); etc., making 25 (5*5 combinations)
    #  ---------------------------
    #       Id: JT.091s    RIGHT JOIN (TGH) RJ (TGH)
    #  TGH: GROUP BY and HAVING (VNA1P004)
    #  ---------------------------
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
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s42')
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
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s43')
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
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s44')
    #
    #  >>>>>>>>>>>>> view VNA1P004 >>>>>>>>>>
    #
    stmt = """select CHAR6_20 || 'AAAAAAAA' from VNA1P004 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s45')
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
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s46')
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
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s47')
    #
    #  ---------------------------
    #       Id: JT.094s    INNER JOIN (TGH) IJ (TGH)
    #  ---------------------------
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
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s48')
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
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s49')
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
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s50')
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
    #  ---------------------------
    #       Id: JT.091t     RIGHT JOIN (TGH) RJ (TAGH)
    #       Id: JT.091x     RIGHT JOIN (TAGH) RJ (TGH)
    #  TGH: GROUP BY and HAVING (VNA1P004)
    #  TAGH:aggregates, GROUP BY, HAVING (e.g., VNA1P005).
    #  ---------------------------
    #
    #  >>>>>>>>>>>>> Expected results ????????? >>>>>>>>>>
    #
    stmt = """select VARCHAR5_10, CHAR6_20 from BTA1P004 
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s51')
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
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s52')
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
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s53')
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
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s54')
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
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s55')
    #
    #  ---------------------------
    #       Id: JT.094t     INNER JOIN (TGH) IJ (TAGH)
    #       Id: JT.094x     INNER JOIN (TAGH) IJ (TGH)
    #  ---------------------------
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
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s56')
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
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s57')
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
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s58')
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
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s59')
    #
    #  ---------------------------
    #  TAGH:aggregates, GROUP BY, HAVING (e.g., VNA1P005) joined to itself.
    #  ---------------------------
    #  TAGH:aggregates, GROUP BY, HAVING (e.g., VNA1P005).
    #    (TA) RJ (TA2) ; (TA) RJ (TG); etc., making 25 (5*5 combinations)
    #  ---------------------------
    #       Id: JT.091y     RIGHT JOIN (TAGH) RJ (TAGH)
    #  TAGH:aggregates, GROUP BY, HAVING (e.g., VNA1P005).
    #  ---------------------------
    #
    stmt = """select C2, C4 from VNA1P005 
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s60')
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
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s61')
    #
    #  ---------------------------
    #       Id: JT.094y     INNER JOIN (TAGH) IJ (TAGH)
    #  ---------------------------
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
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s62')
    
    _testmgr.testcase_end(desc)

def test011(desc="""a11"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    # Test case name:      T1111:A11
    # Description:         Parallel execution in SQL with
    #                      Grouped views used in Joins.
    #                      Testware leveraged from arkt1103.
    #
    # =================== End Test Case Header  ===================
    
    # Get parallelism defaults for this test unit's execution.
    # Includes choice of global schema.
    #
    # Defaults and defines for this testunit.
    #
    # Get the parameter to use the partitioned global db.
    # Catalog for 'global database #11'.
    #
    # Turn Parallel ON.
    stmt = """control query default ATTEMPT_ESP_PARALLELISM 'ON';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """control query default ATTEMPT_ESP_PARALLELISM 'ON';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """control query default PARALLEL_NUM_ESPS '1';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    # Try with 2 ESPs.
    stmt = """control query default PARALLEL_NUM_ESPS '2';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """control query default PARALLEL_NUM_ESPS '4';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #  Expect 13 rows of base table.
    stmt = """select VARCHAR5_10, CHAR6_20
from BTA1P004 
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s0')
    #
    #  Expect 12 rows of view.
    stmt = """select VARCHAR5_10, CHAR6_20
from VNA1P004 
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s1')
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
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s2')
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
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s3')
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
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s4')
    #
    #  ---------------------------
    #  Same queries as given above with tables are now given with views.
    #  ---------------------------
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
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s5')
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
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s6')
    #
    #  ---------------------------
    #       Id: JT.272      RVC within Joined columns via Derived Tables.
    #                       See also:
    #  TGH: GROUP BY and HAVING (VNA1P004)
    #  TAGH:aggregates, GROUP BY, HAVING (e.g., VNA1P005).
    #  ---------------------------
    #
    #  (TGH) IJ (TAGH)
    #
    #  Expect 'BA':
    stmt = """select min(substring(VARCHAR5_10 from 2 for 2))
from VNA1P004 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s7')
    #
    #  Expect 6 rows from view:
    stmt = """select C2, C4 from VNA1P005 
order by C2, C4 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s8')
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
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s9')
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
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s10')
    
    _testmgr.testcase_end(desc)

def test012(desc="""a12"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    # Test case name:      T1111:A12
    # Description:         Parallel execution in SQL with
    #                      Grouped views used in Joins.
    #                      Testware leveraged from arkt1104.
    #
    # =================== End Test Case Header  ===================
    
    # Get parallelism defaults for this test unit's execution.
    # Includes choice of global schema.
    #
    # Defaults and defines for this testunit.
    #
    # Get the parameter to use the partitioned global db.
    # Catalog for 'global database #11'.
    #
    # Turn Parallel ON.
    stmt = """control query default ATTEMPT_ESP_PARALLELISM 'ON';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """control query default ATTEMPT_ESP_PARALLELISM 'ON';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """control query default PARALLEL_NUM_ESPS '1';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    # Try with 2 ESPs.
    stmt = """control query default PARALLEL_NUM_ESPS '2';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """control query default PARALLEL_NUM_ESPS '4';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
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
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s0')
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
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s1')
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
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s2')
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
order by char16_uniq
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s3')
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
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s4')
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
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s5')
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
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s6')
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
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s7')
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
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s8')
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
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s9')
    #
    #  ---------------------------
    #       Id: GV.061e     Upon grouped view, SUBSTRING on varchar
    #  ---------------------------
    #
    #  Expect 12 rows.
    stmt = """select substring(varchar15_uniq from 7 for 2) as S1
, substring(char6_20 from 1 for 2) as S2
from VNA1P004 
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s10')
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
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s11')
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
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s12')
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
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s13')
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
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s14')
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
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s15')
    
    _testmgr.testcase_end(desc)

def test013(desc="""a13"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    # Test case name:      T1111:A13
    # Description:         Parallel execution in SQL with
    #                      Grouped views used in Joins.
    #                      Testware leveraged from arkt1104.
    #
    # =================== End Test Case Header  ===================
    
    # Get parallelism defaults for this test unit's execution.
    # Includes choice of global schema.
    #
    # Defaults and defines for this testunit.
    #
    # Get the parameter to use the partitioned global db.
    # Catalog for 'global database #11'.
    #
    # Turn Parallel ON.
    
    stmt = """control query default PARALLEL_EXECUTION 'ON';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '2050')
    
    stmt = """control query default PARALLEL_NUM_ESPS '1';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    # Jan 9, 1999 -- Try with 2 ESPs.
    stmt = """control query default PARALLEL_NUM_ESPS '2';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """control query default PARALLEL_NUM_ESPS '4';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # ---------------------------------------
    # Specify catalog and schema BEFORE you obey this script.
    # ---------------------------------------
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
from VNA1P002 
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s0')
    #
    stmt = """select varchar15_uniq
, varchar5_10 , varchar0_4 , sbin7_2
from VNA1P004 
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s1')
    #
    stmt = """select varchar15_uniq
, char6_20   , ubin15_uniq
, char16_uniq
from VNA1P004 
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s2')
    #
    stmt = """select n1, c2, c3, c4
from VNA1P005 
order by n1, c3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s3')
    #
    #  ---------------------------
    #  Note, in SQL it is legal to reference a grouped view in a subquery
    #  participating in a comparison predicate; 
    #
    #       Id: GV.081a     Grouped view referenced in subquery in RHS of a comparison predicate.
    #       Id: GV.081b     Grouped view referenced in subquery in LHS of a comparison predicate.
    #  ---------------------------
    #
    #  Check needed value for subsequent tests.
    #  Expect ( ( 0 ) )
    stmt = """select min(t2.sbin7_2) as min_sbin7_2
from VNA1P004 t2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s4')
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
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s5')
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
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s6')
    #
    #  Expect ( ( 1188  FGAAAAAB ) ).
    stmt = """select t1.ubin15_uniq, varchar15_uniq
from VNA1P004 t1
where t1.ubin15_uniq = 1188
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s7')
    #
    #  Expect ( ( FGAAAAAB ) ).
    stmt = """select varchar15_uniq
from VNA1P004 t1
where
( ( select distinct t1.ubin15_uniq from VNA1P002 t2
where t1.ubin15_uniq < 2000
) > 1000
)
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s8')
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
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s9')
    #
    #  Expect 7 rows.
    stmt = """select cast(char17_100 as char(20)), udec17_100
from VNA1P002 t2
where
( select count(*)
from VNA1P004 t4
left join VNA1P005 t5
on position ( 'B' in c3 ) = 1
) = 24
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s10')
    #
    #  Expect 7 rows.
    stmt = """select cast(char17_100 as char(20)), udec17_100
from VNA1P002 t2
where 6 <>
( select count(*)
from VNA1P004 t4
left join VNA1P005 t5
on position ( 'B' in c3 ) = 1
)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s11')
    #
    #  ---------------------------
    #       Id: GV.081d     Grouped view referenced in subquery and compared with multi-value predicate.
    #  ---------------------------
    #
    #  Includes duplicate at 'CCAAAAAAAAAAAAAA', so expect :
    #     ( ( 7 'AWAAAAAAAAAAAAAA' ) )
    stmt = """select cast( count( CHAR17_100 ) As Smallint ) As count17
, cast( min( CHAR17_100 ) as char(20) ) As min17
from VNA1P002 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s12')
    #
    #  Expect ( ( 'DMAAAAAAAAAAAAAA' 6 ) )
    stmt = """select cast( max( CHAR17_100 ) as char(20) )
, cast( count( distinct CHAR17_100 ) As Smallint ) As DISTINCT_count17
from VNA1P002 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s13')
    #
    #  Expect ( ('yes'  7) )
    stmt = """select 'yes', cast( count( CHAR17_100 ) As Smallint ) As count17
from VNA1P002 
where (
( 'AWAAAAAAAAAAAAAA' )
=
( select cast( min(CHAR17_100) as char(20) )
from VNA1P002 )
)
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s14')
    #
    #  Is this fixed now in FCS ...
    #
    stmt = """select 'yes', cast( count( CHAR17_100 ) As Smallint ) As count17
from VNA1P002 
where (
( 7, 'AWAAAAAAAAAAAAAA' )
=
( ( select cast( count( CHAR17_100 ) As Smallint )
, cast( min( CHAR17_100 ) as char(20))
from VNA1P002 ) )
)
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s15')
    stmt = """select 'yes', cast( count( CHAR17_100 ) As Smallint ) As count17
from VNA1P002 
where (
( 7, 'AWAAAAAAAAAAAAAA' )
=
( ( select count( CHAR17_100 )
, min( CHAR17_100 )
from VNA1P002 ) )
)
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s16')
    #
    stmt = """select 'yes', cast( count( CHAR17_100 ) As Smallint ) As count17
from VNA1P002 
where (
( 7, 'AWAAAAAAAAAAAAAA' )
=
( ( select cast( count( CHAR17_100 ) As Smallint )
from VNA1P002 )
, ( select cast( min( CHAR17_100 ) as char(20) )
from VNA1P002 )
)
)
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s17')
    
    _testmgr.testcase_end(desc)

def test014(desc="""a14"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    # Test case name:      T1111:A14
    # Description:         Parallel execution in SQL with
    #                      Grouped views used in Joins.
    #                      Testware leveraged from arkt1104.
    #
    # =================== End Test Case Header  ===================
    
    # Get parallelism defaults for this test unit's execution.
    # Includes choice of global schema.
    #
    # Defaults and defines for this testunit.
    #
    # Get the parameter to use the partitioned global db.
    # Catalog for 'global database #11'.
    #
    # Turn Parallel ON.
    stmt = """control query default ATTEMPT_ESP_PARALLELISM 'ON';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """control query default ATTEMPT_ESP_PARALLELISM 'ON';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """set define ATTEMPT_ESP_PARALLELISM 1;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """control query default PARALLEL_NUM_ESPS '1';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    # Jan 9, 1999 -- Try with 2 ESPs.
    stmt = """control query default PARALLEL_NUM_ESPS '2';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """control query default PARALLEL_NUM_ESPS '4';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # ---------------------------------------
    # Specify catalog and schema BEFORE you obey this script.
    # ---------------------------------------
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
    _dci.expect_file(output, defs.test_dir + """/a14exp""", 'a14s0')
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
    _dci.expect_file(output, defs.test_dir + """/a14exp""", 'a14s1')
    #
    #  One select-list item has TWO TRIM functions.
    #  Expect 13 rows.
    stmt = """select trim (both 'B' from trim (both 'A' from varchar15_uniq) )
, trim (both 'A' from char6_20)
from BTA1P004 t4
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a14exp""", 'a14s2')
    #
    #  Two select-list items have TWO TRIM functions.
    #  Expect 13 rows.
    stmt = """select trim (both 'B' from trim (both 'A' from varchar15_uniq) )
, trim (both 'B' from trim (both 'A' from char6_20) )
from BTA1P004 t4
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a14exp""", 'a14s3')
    
    _testmgr.testcase_end(desc)

def test015(desc="""a15"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    # Test case name:      T1111:A15
    # Description:         Parallel execution in SQL with
    #                      Nested Joins in Query.
    #                      Testware leveraged from arkt1102.
    #
    # =================== End Test Case Header  ===================
    
    # Get parallelism defaults for this test unit's execution.
    # Includes choice of global schema.
    #
    # Defaults and defines for this testunit.
    #
    # Get the parameter to use the partitioned global db.
    # Catalog for 'global database #11'.
    #
    # Turn Parallel ON.
    stmt = """control query default ATTEMPT_ESP_PARALLELISM 'ON';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """control query default ATTEMPT_ESP_PARALLELISM 'ON';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """set define ATTEMPT_ESP_PARALLELISM 1;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """control query default PARALLEL_NUM_ESPS '1';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    # Jan 9, 1999 -- Try with 2 ESPs.
    stmt = """control query default PARALLEL_NUM_ESPS '2';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """control query default PARALLEL_NUM_ESPS '4';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #  ---------------------------
    #  Check tables.
    #  ---------------------------
    stmt = """select * from TTF order by 1,2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s0')
    stmt = """select * from TTF2 order by 1,2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s1')
    #
    #  ---------------------------
    #  Subquery transformations: SELECT list.
    #  ---------------------------
    #
    #  ---------------------------
    #       Id: TF.004       Simple select: NATURAL JOIN; subqueries in select list and WHERE pred.
    #                        NOTE: NO TABLE NAME exposed in NATURAL JOIN.
    #  ---------------------------
    #
    #  Expect {('abcdefg') ('abcdefg') ('d') ('cc')}
    stmt = """select vch7
from TTF t1 natural join TTF t2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s2')
    #
    #  Expect {4 * ('cc')}
    stmt = """select  ( select max(t0.vch7) from TTF t0 )
from TTF t1 natural join TTF t2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s3')
    #
    #  Expect {('cc')}
    stmt = """select max(vch7)
from TTF t1 natural join TTF t2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s4')
    #
    #  Expect 4 rows, null excluded.
    stmt = """select  ( select max(t0.vch7) from TTF t0 ) as max_vch7
, vch7
from TTF t1 natural join TTF t2
where 'A' < ( select vch7 from TTF where vch5 is null )
order by 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s5')
    #
    #  Expect 4 rows, null excluded.
    stmt = """select  ( select min(t0.vch7) from TTF t0 ), vch7
from TTF t1 natural join TTF t2
where ( select t3.vch7 from TTF t3 where vch5 is null )
= ( select t4.vch7 from TTF t4 where vch5 is null )
order by 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s6')
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
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s7')
    #  Expect {('abcdefg')}
    stmt = """select vch7 from TTF where nint = 3 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s8')
    #
    #  Expect 5 rows.
    stmt = """select ( select vch7 from TTF where nint = 3 ) from TTF t
union
select c5 from TTF2 tt2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s9')
    #
    #  Expect 1 row {(3)}.
    stmt = """select ( select t1.nint from TTF t1 where nint = 3 ) from TTF t
union
select (select n2 from TTF2 tt1 where n2 = 3 ) from TTF2 tt2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s10')
    #
    #  Expect 5 * ('abcdefg' 3)
    stmt = """select ( select t1.vch7 from TTF t1 where nint = 3 ) as vch7
, ( select t3.nint from TTF t3 where nint = 3 ) as nint_is_3
from TTF t2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s11')
    #
    #  Expect (('alph' 3) ('cc' 3) ('cc' 3) ('e' 3) (Null 3))
    stmt = """select c5, (select n2 from TTF2 tt1 where n2 = 3 ) from TTF2 tt2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s12')
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
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s13')
    #
    #  ---------------------------
    #       Id: TF.006       Simple select: UNION CORRESPONDING; subqueries in WHERE pred and select list.
    #  ---------------------------
    #  Omit CORRESPONDING (from UNION CORRESPONDING) till supported.
    #  Kept test that gave bug for UNION without CORRESPONDING.
    #
    stmt = """select t.vch7 from TTF t where nint=5 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s14')
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
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s15')
    #
    #  Use derived table to control column name.
    #  Expect 5 * ('abcdefg' 2)
    stmt = """select * from (
select ( select vch7 from TTF where nint=5)
,( select nsint from TTF where nint=5)
from TTF ) dt (unmatchedcolname2, nnum5)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s16')
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
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s17')
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
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s18')
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
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s19')
    #
    #  Expect ((12345)).
    stmt = """select max(t.n8) from TTF2 t ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s20')
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
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s21')
    #
    #  -----------------------------
    #       Id: TF.032       Subquery within Simple CASE in WHERE clause.
    #  ---------------------------
    #
    stmt = """select v7 from TTF2 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s22')
    #
    #  Expect ((0))
    stmt = """select min(t.n8) from TTF2 t;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s23')
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
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s24')
    #  Expect row with N2 = 4 and V7 ='c':
    stmt = """select * from TTF2 
WHERE v7 = CASE (select t.n2 from TTF2 t where t.n8=12345)
WHEN 1 THEN ''
WHEN 4 THEN 'c'
ELSE NULL
END
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s25')
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
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s26')
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
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s27')
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
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s28')
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
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s29')
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
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s30')
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
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s31')
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
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s32')
    
    _testmgr.testcase_end(desc)

def test016(desc="""a16"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    # Test case name:      T1111:A16
    # Description:         Parallel execution in SQL with
    #                      Inner and Outer 3-way joins.
    #                      Joins with Union.
    #                      Testware leveraged from arkt1103.
    #
    # =================== End Test Case Header  ===================
    
    # Get parallelism defaults for this test unit's execution.
    # Includes choice of global schema.
    #
    # Defaults and defines for this testunit.
    #
    # Get the parameter to use the partitioned global db.
    # Catalog for 'global database #11'.
    #
    # Turn Parallel ON.
    stmt = """control query default ATTEMPT_ESP_PARALLELISM 'ON';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """control query default ATTEMPT_ESP_PARALLELISM 'ON';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """set define ATTEMPT_ESP_PARALLELISM 1;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """control query default PARALLEL_NUM_ESPS '1';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    # Try with 2 ESPs.
    stmt = """control query default PARALLEL_NUM_ESPS '2';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """control query default PARALLEL_NUM_ESPS '4';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #  ---------------------------
    #  Tables created in preparation for test unit.
    #  ---------------------------
    #
    #  Preliminary review of contents of views.
    stmt = """select * from VNA1P005 t1
order by n1, c3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s0')
    #
    #  ---------------------------
    #       Id: JT.273      Within ON clause of JOIN, RVC contains Columns.
    #       Id: JT.274      Within ON clause of JOIN, RVC is a list containing literals.
    #  ---------------------------
    #  Expect 8 rows (4 like inner join plus 4 null-augmented).
    stmt = """select t1.n1 as LHSn1, t1.c2 as LHSc2, t1.c3 as LHSc3
, t2.* from VNA1P005 t1
right join VNA1P005 t2
ON (t1.c2, t2.c2, 'AA', t2.c3 ) = ('BA','BA', t1.c3, 'AA')
order by t2.c3, t2.n1, t1.n1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s1')
    #  Expect 4 rows.
    stmt = """select t1.n1 as LHSn1, t1.c2 as LHSc2, t1.c3 as LHSc3
, t2.* from VNA1P005 t1
inner join VNA1P005 t2
ON (t1.c2, t2.c2, 'AA', t2.c3 ) = ('BA','BA', t1.c3, 'AA')
order by t2.c3, t2.n1, t1.n1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s2')
    #
    # ---------------------------
    #      Id: JT.092b     RIGHT JOIN of Grouped Views and Derived
    #                      Tables: Add parameters in ON clause.
    #      Id: JT.275      Within ON clause of JOIN, RVC contains parameters
    #                      e.g. ON (t1.col1, ?p1) = (? codep1,t2.col2);
    # ---------------------------
    stmt = """set param ?pba 'BA' ;"""
    output = _dci.cmdexec(stmt)
    # value of interest for column c2.
    stmt = """set param ?paa 'AA' ;"""
    output = _dci.cmdexec(stmt)
    # value of interest for column c3.
    stmt = """select t1.n1 as LHSn1, t1.c2 as LHSc2, t1.c3 as LHSc3
, t2.* from VNA1P005 t1
right join VNA1P005 t2
ON (t1.c2, t2.c2, 'AA', t2.c3 ) = ('BA','BA', t1.c3, ?paa)
order by t2.c3, t2.n1, t1.n1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s3')
    #  Reuse parameter, and use second parameter.
    stmt = """select t1.n1 as LHSn1, t1.c2 as LHSc2, t1.c3 as LHSc3
, t2.* from VNA1P005 t1
right join VNA1P005 t2
ON (t1.c2, t2.c2, ?paa, t2.c3 ) = ( ?pba,'BA', t1.c3, ?paa)
order by t2.c3, t2.n1, t1.n1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s4')
    #
    #  ---------------------------
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
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s5')
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
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s6')
    
    _testmgr.testcase_end(desc)

def test017(desc="""a17"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    # Test case name:      T1111:A17
    # Description:         Parallel execution in SQL with
    #                      Union as child of a Join, and Joins
    #                      with Group By as child of a Join.
    #                      Testware leveraged from arkt1103.
    #
    # =================== End Test Case Header  ===================
    
    # Get parallelism defaults for this test unit's execution.
    # Includes choice of global schema.
    #
    # Defaults and defines for this testunit.
    #
    # Get the parameter to use the partitioned global db.
    # Catalog for 'global database #11'.
    #
    # Turn Parallel ON.
    stmt = """control query default ATTEMPT_ESP_PARALLELISM 'ON';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """control query default ATTEMPT_ESP_PARALLELISM 'ON';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """set define ATTEMPT_ESP_PARALLELISM 1;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """control query default PARALLEL_NUM_ESPS '1';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    # Jan 9, 1999 -- Try with 2 ESPs.
    stmt = """control query default PARALLEL_NUM_ESPS '2';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """control query default PARALLEL_NUM_ESPS '4';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #  Turn on SHOWSHAPE for temporary debugging! Yippee!
    #    Set Showshape ON ;
    
    #  ---------------------------
    #  Tables created in preparation for test unit.
    #  ---------------------------
    #
    stmt = """select t1.sbin16_20, t1.varchar5_10
from BTA1P001 t1
order by 1,2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s0')
    #
    #  Access UNION view, VNA1P008.
    stmt = """select varchar0_500, CHAR4_N10, CHAR5_N20, char6_n100
from BTA1P008 
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s1')
    stmt = """select varchar0_500, CHAR4_N10, CHAR5_N20, char6_n100
from VNA1P008 
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s2')
    #
    stmt = """select * from VNA1P005 
order by 1,3 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s3')
    #
    stmt = """select * from VNA1P006 
order by 1,2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s4')
    #
    #  ---------------------------
    #       Id: JT.061      Joins with UNION as left or right child of a RIGHT join.
    #  ---------------------------
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
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s5')
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
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s6')
    #
    #  SELECT * FROM (union view or derived table that is a UNION)
    #  RIGHT JOIN (union view or derived table that is another UNION)
    #  ON <expression> ;
    stmt = """SELECT count(*) FROM VNA1P008 t1
RIGHT JOIN VNA1P008 t2
ON t1.varchar0_500 = t2.varchar0_500
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s7')
    stmt = """SELECT count(*) FROM VNA1P008 t1
RIGHT JOIN VNA1P008 t2
ON t1.CHAR4_N10 = t2.CHAR5_N20
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s8')
    #
    stmt = """select c2 FROM VNA1P005 t2
UNION ALL
select C3 FROM VNA1P005 t3
UNION ALL
select C4 FROM VNA1P005 t4
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s9')
    #
    stmt = """select c2 FROM VNA1P005 t2
UNION
select C3 FROM VNA1P005 t3
UNION
select C4 FROM VNA1P005 t4
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s10')
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
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s11')
    #
    #  ---------------------------
    #       Id: JT.062      Joins with Group By as left or right child of a RIGHT join.
    #  See ../arkt1100/testA02 for Grouped View test #021
    #  (Outer Join on Grouped View (GROUP BY and aggregates) )
    #
    #  Also see ../arkt1103/testA07 for Grouped View test #041
    #  (Join of one Grouped view to another, in the right tree of a LEFT JOIN.)
    #  ---------------------------
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
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s12')
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
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s13')
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
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s14')
    #
    stmt = """SELECT count(*) FROM VNA1P005 t1
RIGHT JOIN VNA1P005 t2
ON t1.C3 = t2.C2
OR t1.C3 = t2.C3
OR t1.C3 = t2.C4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s15')
    #
    #  ---------------------------
    #       Id: JT.063      Joins with UNION as left or right child of a NATURAL join.
    #  ---------------------------
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
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s16')
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
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s17')
    #
    #  SELECT * FROM (union view or derived table that is a UNION)
    #  NATURAL JOIN (union view or derived table that is another UNION) ;
    stmt = """SELECT count(*) FROM VNA1P008 t1
NATURAL JOIN VNA1P008 t2
Order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s18')
    #
    stmt = """select c2 FROM VNA1P005 t2
UNION ALL
select C3 FROM VNA1P005 t3
UNION ALL
select C4 FROM VNA1P005 t4
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s19')
    #
    stmt = """select c2 FROM VNA1P005 t2
UNION
select C3 FROM VNA1P005 t3
UNION
select C4 FROM VNA1P005 t4
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s20')
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
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s21')
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
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s22')
    #
    #  ---------------------------
    #       Id: JT.064      Joins with Group By as left or right child of a NATURAL join.
    #  See ../arkt1103/testA01/testA02 for Join test #185b
    #  (Derived table contains NATURAL join with GROUP BY.)
    #  ---------------------------
    #
    #  SELECT * FROM (Grouped View)
    #  NATURAL JOIN Table2 ;
    #
    stmt = """SELECT count(*) FROM VNA1P005 t1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s23')
    stmt = """SELECT count(*) FROM BTA1P005 t1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s24')
    
    stmt = """SELECT count(*) FROM VNA1P005 t1
NATURAL JOIN BTA1P005 t2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s25')
    stmt = """SELECT count(*) FROM VNA1P005 t1
NATURAL JOIN BTA1P005 t2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s26')
    #
    #  SELECT * FROM Table1
    #  NATURAL JOIN (Grouped View) ;
    #
    stmt = """SELECT count(*) FROM BTA1P005 t1
NATURAL JOIN VNA1P005 t2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s27')
    #
    #  SELECT * FROM (Grouped View)
    #  NATURAL JOIN (Grouped View) ;
    #
    stmt = """SELECT c2 , c3 , c4 FROM VNA1P005 t1
NATURAL JOIN VNA1P005 t2
Order by c2 , c3 , c4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s28')
    #
    stmt = """SELECT c3 FROM VNA1P005 t1
NATURAL JOIN VNA1P005 t2
GROUP BY c3
Order by c3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s29')
    #
    stmt = """SELECT c4 FROM VNA1P005 t1
NATURAL JOIN VNA1P005 t2
GROUP BY c4
Order by c4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s30')
    
    _testmgr.testcase_end(desc)

def test018(desc="""a18"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    # Test case name:      T1111:A18
    # Description:         Parallel execution in SQL with
    #                      Union All on Grouped Views; also
    #                      Union, aggregates, predicates.
    #                      Testware leveraged from arkt1104.
    #
    # =================== End Test Case Header  ===================
    
    # Get parallelism defaults for this test unit's execution.
    # Includes choice of global schema.
    #
    # Defaults and defines for this testunit.
    #
    # Get the parameter to use the partitioned global db.
    # Catalog for 'global database #11'.
    #
    # Turn Parallel ON.
    stmt = """control query default ATTEMPT_ESP_PARALLELISM 'ON';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """control query default ATTEMPT_ESP_PARALLELISM 'ON';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """set define ATTEMPT_ESP_PARALLELISM 1;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """control query default PARALLEL_NUM_ESPS '1';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    # Jan 9, 1999 -- Try with 2 ESPs.
    stmt = """control query default PARALLEL_NUM_ESPS '2';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """control query default PARALLEL_NUM_ESPS '4';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
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
from VNA1P002 
order by 1,2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a18exp""", 'a18s0')
    #
    #  Includes duplicate at 'CCAAAAAAAAAAAAAA', so expect :
    #     ( ( 7 AWAAAAAAAAAAAAAA DMAAAAAAAAAAAAAA 6 ) )
    stmt = """select cast(count(CHAR17_100) as smallint) as count1
, cast(min(CHAR17_100) as char(20)) as min1
, cast(max(CHAR17_100) as char(20)) as max1
, cast(count(distinct CHAR17_100) as smallint)
as count_distinct
from VNA1P002 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a18exp""", 'a18s1')
    #
    #  Expect 6 rows (omitting one duplicate value of
    #  'CCAAAAAAAAAAAAAA'.)
    stmt = """select cast(CHAR17_100 as char(20))
from VNA1P002 group by CHAR17_100
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a18exp""", 'a18s2')
    stmt = """select count(CHAR17_100) as char_count
, cast(min(CHAR17_100) as char(20)) as char_min
, cast(max(CHAR17_100) as char(20)) as char_max
, count(distinct CHAR17_100) as char_count_D
from VNA1P002 
group by CHAR17_100
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a18exp""", 'a18s3')
    #
    #  Expect: ( ( 16  85  7 ) )
    stmt = """select min(UDEC17_100)
, max(UDEC17_100)
, count(distinct UDEC17_100)
from VNA1P002 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a18exp""", 'a18s4')
    #  Expect: ( ( 7  333  1 ) )
    stmt = """select cast(count(UDEC17_100) as smallint)
, cast(sum(UDEC17_100) as int)
, (sum(UDEC17_100)/count(UDEC17_100))/(avg(UDEC17_100)) as IsItOne
from VNA1P002 
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a18exp""", 'a18s5')
    #
    #  Expect: ( ( 7  333  333 ) )
    #  ----------------
    #  Bug in division? (a) rounding (b) width
    #  ----------------
    stmt = """select cast(count(UDEC17_100) as smallint)
, sum(UDEC17_100)
, cast((sum(UDEC17_100)/count(UDEC17_100))/(avg(UDEC17_100))
as int) as IsIt333
from VNA1P002 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a18exp""", 'a18s6')
    stmt = """select cast(count(UDEC17_100) as smallint)
, sum(UDEC17_100)
, cast((sum(UDEC17_100)/count(UDEC17_100))/(avg(UDEC17_100))
as numeric(9,1) ) as IsIt333
from VNA1P002 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a18exp""", 'a18s7')
    #
    #  Expect: ( ( 7  333  1) )
    stmt = """select cast(count(UDEC17_100) as smallint)
, cast(sum(UDEC17_100) as int)
, cast( 7 * avg(UDEC17_100) as int) as IsIt333
from VNA1P002 
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a18exp""", 'a18s8')
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
from VNA1P002 
group by CHAR17_100
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '8402')
    _dci.expect_str_token(output, 'A')
    _dci.expect_str_token(output, 'B')
    _dci.expect_str_token(output, 'C')
    _dci.expect_str_token(output, 'D')
    _dci.expect_selected_msg(output, 6)
    #
    #  Expect all 7 rows.
    stmt = """select cast(CHAR17_100 as CHARACTER(16) )
, UDEC17_100
from VNA1P002 
group by CHAR17_100, UDEC17_100
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a18exp""", 'a18s10')
    #
    #  Expect ( (1 1) * 5, (4 4) )
    stmt = """select count(v1.CHAR17_100)
, count(v2.CHAR17_100)
from VNA1P002 v1
left join VNA1P002 v2
on v1.CHAR17_100 = v2.CHAR17_100
group by v1.CHAR17_100, v2.CHAR17_100
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a18exp""", 'a18s11')
    #
    #  Expect 7 rows (max 'DM...' appears twice, duplicate 'CC...' only once)
    stmt = """select cast(CHAR17_100 as CHARACTER(16) )
from VNA1P002 v1
group by CHAR17_100
union all
select max( cast(CHAR17_100 as CHARACTER(16) ))
from VNA1P002 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a18exp""", 'a18s12')
    #
    #  Expect 6 rows (no duplicate)
    stmt = """select cast(CHAR17_100 as CHARACTER(16) )
from VNA1P002 v1
group by CHAR17_100
union
select cast(max(CHAR17_100) as CHARACTER(16))
from VNA1P002 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a18exp""", 'a18s13')
    #
    #  ---------------------------
    #       Id: GV.006      'GROUP BY' view and HAVING
    #  ---------------------------
    #
    #  Expect 4 rows ( 'CBA..', 'CCA..', 'DDA..', 'DMA..', no duplicate )
    stmt = """select  cast(CHAR17_100 as CHARACTER(16) )
from VNA1P002 v1
group by CHAR17_100
having CHAR17_100 > 'BZZ'
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a18exp""", 'a18s14')
    #
    #  Expect 4 rows ( ( 1 1 ) * 3 ( 4 4 ) )
    stmt = """select count(v1.CHAR17_100) , count(v2.CHAR17_100) from VNA1P002 v1
left join VNA1P002 v2
on v1.CHAR17_100 = v2.CHAR17_100
group by v2.CHAR17_100
having v2.CHAR17_100 > 'BZZ'
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a18exp""", 'a18s15')
    #
    #  Note that it's an error to attempt to use having on aggregated
    #  column; aggregation does not make a query "grouped". Therefore,
    #  the following is executed in negative tests:
    #     select max(CHAR17_100) from VNA1P002
    #        having CHAR17_100 > 'BZZ'
    #     ;
    #  Expect 4 rows ( 'CBA..', 'CCA..', 'DDA..', 'DMA..', no duplicate )
    stmt = """select cast(CHAR17_100 as CHARACTER(16) )
from VNA1P002 v1
group by CHAR17_100
having CHAR17_100 > 'BZZ'
union
select cast(max(CHAR17_100) as CHARACTER(16) )
from VNA1P002 
group by CHAR17_100
having CHAR17_100 > 'BZZ'
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a18exp""", 'a18s16')
    #
    #  Expect 8 rows ( 'CBA..', 'CCA..', 'DDA..', 'DMA..', all duplicated ).
    stmt = """select cast(CHAR17_100 as CHARACTER(16) )
from VNA1P002 v1
group by CHAR17_100
having CHAR17_100 > 'BZZ'
union all
select cast(max(CHAR17_100) as CHARACTER(16) )
from VNA1P002 
group by CHAR17_100
having CHAR17_100 > 'BZZ'
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a18exp""", 'a18s17')
    #
    #  ---------------------------
    #       Id: GV.007      'GROUP BY' view and WHERE clause
    #  ---------------------------
    #
    #  Expect :
    #     ( ( 16  78  6 ) )
    stmt = """select min(UDEC17_100) , max(UDEC17_100)
, count(distinct UDEC17_100)
from VNA1P002 
where UDEC17_100 <> 85
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a18exp""", 'a18s18')
    #
    #  Expect 2 rows ( 'CBA..', 'CCA..', no duplicates )
    stmt = """select cast(CHAR17_100 as CHARACTER(16) )
from VNA1P002 v1
where  CHAR17_100 < 'CAZ'
group by CHAR17_100
having CHAR17_100 > 'BZZ'
union all
select cast( max(CHAR17_100) as CHARACTER(16) )
from VNA1P002 
where  CHAR17_100 < 'DAZ'
group by CHAR17_100
having CHAR17_100 > 'BZZ'
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a18exp""", 'a18s19')
    
    _testmgr.testcase_end(desc)

