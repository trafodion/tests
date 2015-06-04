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
    
def test001(desc="""a05"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     A05
    #  Description:        UNION
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    #  Notes:
    #  This test case incorporates features detailed in the "Title"
    #  by Ima Programmer (Version 1.1, <date>).
    #
    # =================== End Test Case Header  ===================
    
    # create and populate tables
    
    stmt = """create table tprtab1 (A INT      NO DEFAULT NOT NULL,
PIC_X_8  PIC  X(8)      NO DEFAULT NOT NULL,
VAR_CHAR_3 VARCHAR( 3 ) NO DEFAULT NOT NULL,
SMALL_INT  SMALLINT     NO DEFAULT NOT NULL,
primary key (a));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    # organization k
    # catalog
    
    stmt = """insert into tprtab1 values (0, 'bbb', 'ccc', 1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select pic_x_8, sum(small_int) from tprtab1 
group by pic_x_8
union
select var_char_3, sum(small_int) from tprtab1 
group by var_char_3
order by pic_x_8;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s0')
    
    #  Now, remove the aggregate and we get a little bit further.
    #     Prior to S03 fix, error is detected at Runtime (fixup) time.
    #     Perhaps due to failure at compile time, the FILENAME for
    #     the temporary table at runtime is an empty string!  Thus,
    #     the OPEN fails.
    
    stmt = """select pic_x_8 from tprtab1 
group by pic_x_8
union
select var_char_3 from tprtab1 
group by var_char_3
order by pic_x_8;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s1')
    
    #  Replace the column name by column number, and : no problem!
    stmt = """select pic_x_8 from tprtab1 
group by pic_x_8
union
select var_char_3 from tprtab1 
group by var_char_3
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s2')
    
    #  Now, add a compiler define to force the use of FASTSORT.
    #    Try a UNION select where the first SELECT returns 0 rows
    #    (specify order by column number so we get beyond the compiler
    #    errors).  We get SORT error (prior to S03 executor fix).
    
    stmt = """select pic_x_8 from tprtab1 
where pic_x_8 = 'xxx'
group by pic_x_8
union
select var_char_3 from tprtab1 
group by var_char_3
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s3')
    
    #  Now try a UNION query where the second SELECT returns 0 rows.
    #  Prior to S03 executor fix, entire query returns 0 rows.
    
    stmt = """select var_char_3 from tprtab1 
group by var_char_3
union
select pic_x_8 from tprtab1 
where pic_x_8 = 'xxx'
group by pic_x_8
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s4')
    
    
    stmt = """drop table tprtab1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test002(desc="""a06"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     A06
    #  Description:
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    #  Notes:
    #  This test case incorporates features detailed in the "Title"
    #  by Ima Programmer (Version 1.1, <date>).
    #
    # =================== End Test Case Header  ===================
    # File: SQLS0306
    # Component  : NonStop SQL Regression Test Suite
    # Description: Tests to validate bug fixes
    # NOTE:
    #   These tests should be run using C30S03 or its successor.
    # ---------------------------------
    # Open a Log file
    # ---------------------------------
    #   LOG logA06 CLEAR;
    # ---------------------------------
    
    # Internal error when the subquery contained a Distinct and
    #   a correlated column in its select list
    
    stmt = """create table mr271659 
(x int , y int) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #catalog
    
    stmt = """insert into mr271659 values(1, 10);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mr271659 values(2, 20);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mr271659 values(3, 30);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select x, max(A.y)
from mr271659 A
group by x
having max(A.y) = (select distinct min(A.y)
from mr271659 B
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s0')
    
    stmt = """drop table mr271659;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # The multi-valued predicates get truncated when the select is on
    #   a view which is defined using an union.
    
    stmt = """create table se241411(a smallint,
b int, c largeint, d char(2) UPSHIFT) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #catalog
    
    stmt = """insert into se241411 values (1,1,1, 'ab');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """create table se241412(e largeint,
f int,
g smallint,
h char(4)) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #                         catalog
    
    stmt = """insert into se241412 values (2,2,1, 'XYZW');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """create view vu241411 (x, y, z, w) as
select a, b, c, d from se241411 
union all
select e, f, g, h from se241412;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #catalog
    
    # prepare s1 from
    #  'select * '
    # &'  from vu241411 '
    # &' where z,x,y between 1,1,1 and 2,2,2 '
    # ;
    
    stmt = """prepare s1 from
select *
from vu241411 
where z,x,y between 1,1,1 and 2,2,2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain(NULL,'S1'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s2')
    # should see two rows
    
    # The access mode options of a select on a view which contains an
    #   union are lost.
    
    stmt = """prepare s2 from select * from vu241411;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """select seq_num, operator, total_cost
from table (explain(NULL, 'S2'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s3 from select * from vu241411 for read uncommitted access;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """select seq_num, operator, total_cost
from table (explain(null, 'S3'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s4 from
select * from vu241411 for serializable access;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """select seq_num, operator, total_cost
from table (explain(null, 'S4'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s5 from select * from vu241411;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """select seq_num, operator, total_cost
from table (explain(null, 'S5'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """drop view vu241411;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table se241411;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table se241412;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # Sort key was getting truncated when corresponding columns
    # were of different data types and type propagation introduced
    # convert nodes.
    
    stmt = """create table oc160904 
( a     largeint
, b     char(3)
, c     smallint
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #catalog
    
    stmt = """insert into oc160904 values (100,'abc',100);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into oc160904 values (100,'abd',100);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into oc160904 values (200,'abc',200);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into oc160904 values (200,'abd',200);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select distinct c, b, a from oc160904;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s7')
    
    #  display_explain
    #   'select distinct  c, b, a, 'from the 1st SELECT' '
    #  &'  from oc160904                          '
    #  &'union all                            '
    #  &'select distinct  a, b, c, 'from the 2nd SELECT' '
    #  &'  from oc160904                          '
    #  ;
    
    stmt = """select distinct  c, b, a, 'from the 1st SELECT'
from oc160904 
union all
select distinct  a, b, c, 'from the 2nd SELECT'
from oc160904;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s8')
    
    stmt = """prepare s6 from
select distinct  c, b, a, 'from the 1st SELECT'
from oc160904 
union all
select distinct  a, b, c, 'from the 2nd SELECT'
from oc160904;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select seq_num, operator, total_cost
from table (explain(null, 'S6'));"""
    output = _dci.cmdexec(stmt)
    
    #  display_explain
    #   'select distinct  a, b, c, 'from the 1st SELECT'  '
    #  &'  from oc160904                          '
    #  &'union all                            '
    #  &'select distinct  c, b, a, 'from the 2nd SELECT'  '
    #  &'  from oc160904                          '
    #  ;
    
    stmt = """select distinct  a, b, c, 'from the 1st SELECT'
from oc160904 
union all
select distinct  c, b, a, 'from the 2nd SELECT'
from oc160904;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s10')
    
    stmt = """prepare s7 from
select distinct  a, b, c, 'from the 1st SELECT'
from oc160904 
union all
select distinct  c, b, a, 'from the 2nd SELECT'
from oc160904;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select seq_num, operator, total_cost
from table (explain(null, 'S7'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select distinct  a, b, c, 'from the 1st SELECT'
from oc160904 
union all
select distinct  c, b, a, 'from the 2nd SELECT'
from oc160904;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s12')
    
    stmt = """prepare s8 from
select distinct  a, b, c, 'from the 1st SELECT'
from oc160904 
union all
select distinct  c, b, a, 'from the 2nd SELECT'
from oc160904;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select seq_num, operator, total_cost
from table (explain(null, 'S8'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """drop table oc160904;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # SQL Compiler error if the temp table contained more than 63 columns
    #   when actually  the FASTSORT limit applies to the key columns only
    
    stmt = """create table oc301427 (
c10 int not null
, c11 int not null
, c12 int not null
, c13 int
, c14 int
, c15 int
, c16 int
, c17 int
, c18 int
, c19 int
, c20 int
, c21 int
, c22 int
, c23 int
, c24 int
, c25 int
, c26 int
, c27 int
, c28 int
, c29 int
, c30 int
, c31 int
, c32 int
, c33 int
, c34 int
, c35 int
, c36 int
, c37 int
, c38 int
, c39 int
, c40 int
, c41 int
, c42 int
, c43 int
, c44 int
, c45 int
, c46 int
, c47 int
, c48 int
, c49 int
, c50 int
, c51 int
, c52 int
, c53 int
, c54 int
, c55 int
, c56 int
, c57 int
, c58 int
, c59 int
, c60 int
, c61 int
, c62 int
, c63 int
, c64 int
, c65 int
, c66 int
, c67 int
, c68 int
, c69 int
, c70 int
, c71 int
, c72 int
, c73 int
, c74 int
, c75 int
, c76 int
, c77 int
, c78 int
, c79 int
, primary key (c10,c11,c12)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #catalog
    
    stmt = """select *
from oc301427 h left join oc301427 c
on h.c10 = c.c10
and h.c11 = c.c11
and h.c12 = c.c12
and h.c13 = h.c13
where h.c10 = 17207
and h.c11,h.c12 between 0,0 and 99,9999
and h.c20 = 51
order by h.c60
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """drop table oc301427;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # A Distinct sort was combined with a sort for a Group By
    #   when there was an aggregate in the select list. The
    #   query therefore returned wrong results.
    
    stmt = """create table no270942(a int) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #catalog
    
    stmt = """insert into no270942 values(1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into no270942 values(1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into no270942 values(2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    #  There are 2 groups             a  count (*)
    #                              ----  ---------
    #                                 1          2   <=== count(*) > 1
    #                                 2          1
    #  Result should contain 1 row
    
    stmt = """select a
from no270942 
group by a
having count(*) > 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s14')
    
    #  Introducing a DISTINCT should not change the result because
    #    the grouping should be performed before projections.
    #  Result should still contain 1 row.
    
    stmt = """select distinct a
from no270942 
group by a
having count(*) > 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s15')
    
    stmt = """drop table no270942;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table de061541(a int, b int, c int) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #catalog
    
    stmt = """insert into de061541 values (1,1,1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into de061541 values (1,1,2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into de061541 values (1,1,3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into de061541 values (1,2,1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into de061541 values (1,2,2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into de061541 values (1,2,3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # prepare s1 from
    #  'select distinct  a, b, sum(c)   '
    # &'  from de061541                 '
    # &' where a,b between 1,1 and 2,2  '
    # &' group by 1, 2                  '
    # &' order by 2 desc, 1 asc         '
    # ;
    #
    stmt = """prepare s1 from
select distinct  a, b, sum(c)
from de061541 
where a,b between 1,1 and 2,2
-- group by 1, 2
group by a, b
order by 2 desc, 1 asc
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain(NULL,'S1'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s17')
    
    stmt = """drop table de061541;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #  Group by of fucntion on non-nullable and nullable timestamp columns
    #    was returning run-time errors because of bugs in OPTS
    
    stmt = """drop table testdate;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table testdatN;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table testdate 
( text pic x(20) , startdate largeint not null) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #catalog ;
    
    stmt = """create table testdatN 
( text pic x(20) , startdate largeint) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #catalog ;
    
    # control table testdate sequential insert on;
    stmt = """insert into testdate values ('october date',  211526683200000000);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into testdate values ('november date', 211524091200000000);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into testdate values ('december date', 211529361600000000);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into testdate values ('january date' , 211532040000000000);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into testdate values ('october date 1',  211526683200000000);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into testdate values ('november date 1', 211524091200000000);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into testdate values ('december date 1', 211529361600000000);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into testdate values ('january date  1', 211532040000000000);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select * from testdate;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s20')
    
    stmt = """insert into testdatN select * from testdate;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 8)
    
    stmt = """select * from testdatN;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s21')
    
    stmt = """select startdate, count (*) from testdate group by startdate;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s22')
    
    stmt = """select startdate, count (*) from testdatN group by startdate;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s23')
    
    stmt = """select converttimestamp(startdate) from testdate;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s24')
    
    stmt = """select converttimestamp(startdate) from testdatN;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s25')
    
    stmt = """select converttimestamp(startdate) from testdatN group by startdate;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s26')
    
    stmt = """select converttimestamp(startdate), count (*)
from testdate group by startdate;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s27')
    
    stmt = """select converttimestamp(startdate), count (*)
from testdatN group by startdate;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s28')
    
    stmt = """drop table testdate;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table testdatN;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table  ja231257(x int ,
y int,
z char(4)) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #                           catalog
    
    stmt = """insert into  ja231257 values(10, 10, 'Row1');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into  ja231257 values(30, 10, 'Row2');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into  ja231257 values(20, 20, 'Row3');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into  ja231257 values(40, 20, 'Row4');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select A.x, B.y, A.z
from  ja231257 A,  ja231257 B
where A.x = B.x
and A.x = (select distinct B.y
from  ja231257 C
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s29')
    # -- should see Row1 and Row3
    
    stmt = """drop table  ja231257;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # The sort key for a Distinct sot was truncated because of
    #   a dattime column in the select list
    
    stmt = """create table ja231410(x int , y timestamp, z char(4)) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #                           catalog
    
    stmt = """insert into ja231410 values
(10, timestamp '1990-01-01:00:00:00', 'Row1');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into ja231410 values
(20, timestamp '1990-01-01:00:00:00', 'Row2');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into ja231410 values
(30, timestamp '1999-12-31:00:00:00', 'Row3');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into ja231410 values
(40, timestamp '1990-12-31:00:00:00', 'Row4');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    #  select distinct x, y year to day, z
    stmt = """prepare s1 from
select distinct x, y, z
from ja231410 
order by 3 desc, 2 asc, 1 desc
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain(NULL,'S1'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s31')
    
    stmt = """drop table ja231410;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    
    #  the sort key length is set to 8 for any function so this test
    #  checks what happens when a sort is done on the result of UPSHIFT
    
    stmt = """create table bigcol (a char(2000), b char(2000)) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #                           catalog
    
    stmt = """select upshift(a),upshift(b) from bigcol order by 1,2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """drop table bigcol;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # Incorrect results on unions with order by and repeated column
    # column names in the first select.
    #
    # UNION distinct also gives incorrect result but that will be fixed
    # with S03 (T9095AAW)
    #
    stmt = """create table mkey27(a int, b int, c int) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create table empty(a int, b int, c int) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into mkey27 values (1,2,1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey27 values (2,1,1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey27 values (1,1,1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # Q1
    stmt = """prepare s1 from
select a,a,a from empty  union all
select a,b,c from mkey27 order by 1,2,3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s32')
    
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain(NULL,'S1'));"""
    output = _dci.cmdexec(stmt)
    
    # Q2
    stmt = """prepare s2 from
select a,a,a from empty  union  select a,b,c from mkey27;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """execute s2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s34')
    
    #  rows that are not duplicates were eliminated
    
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain(NULL,'S2'));"""
    output = _dci.cmdexec(stmt)
    
    # sort distinct done on only one column.
    
    stmt = """drop table mkey27;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop table empty;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # Union of two selects when the sort key lengths > 255,
    #   insertion sort used to be chosen giving run-time error
    
    stmt = """create table mr061035 
(
A                              VARCHAR( 15 ) DEFAULT NULL
, B                              VARCHAR( 5 ) DEFAULT 'abc'
, C                              VARCHAR( 255 ) DEFAULT 'a'
, D                              VARCHAR( 280 ) DEFAULT 'a'
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #catalog
    
    stmt = """insert into mr061035 values('abc' , 'abc' , 'a', 'a');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mr061035 values('abcd', 'abcd', 'a', 'a');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mr061035 values('b'   , 'b'   , 'b', 'b');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mr061035 values('b'   , 'b'   , 'b', 'bab');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select distinct 'bab' from mr061035 
union select d from mr061035;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s36')
    
    stmt = """select distinct 'bab' from mr061035 
union all select d from mr061035 order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s37')
    
    stmt = """select distinct 'bab' from mr061035 
union select d from mr061035 order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s38')
    
    stmt = """select  'bab' from mr061035 union
all select d from mr061035 order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s39')
    
    stmt = """select a from mr061035 union all select
d from mr061035 order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s40')
    
    stmt = """select a from mr061035  union select
d from mr061035;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s41')
    
    stmt = """drop table mr061035;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # Tom O'shea contributed this test case.
    # Was causing a loop in the C30 through S02 compiler
    
    stmt = """create table s02loop 
( a char
, b int
, c real
, d date
, e interval year
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    # catalog
    
    stmt = """set param ?p1 'a';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p2 2e1;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p3 3;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p4 '1966-02-06';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p5 '1';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into s02loop values (?p1, null, ?p3, null, ?p5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select ?p1, cast(?p2 as float)+0, ?p3+0, cast(?p4 as date), cast(?p5 as interval year)
from s02loop 
union
select a, b, c, d, e from s02loop;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s42')
    
    # select ?p1, ?p2+0, ?p3+0,cast( ?p4 as date), ?p5  year
    stmt = """select ?p1, cast(?p2 as float)+0, ?p3+0,cast( ?p4 as date), cast(?p5 as interval year)
from s02loop 
union
select a, b, c, d, e from s02loop;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s43')
    
    stmt = """drop table s02loop;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # To test the use of unique indices to avoid sorts
    
    stmt = """create table bug3tab (a int not null,
b int not null,
c int not null,
d int not null) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """insert into bug3tab values (1,1,2,2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into bug3tab values (2,2,1,1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #
    stmt = """prepare s from
select distinct a,b,c,d from bug3tab order by 1,2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """select seq_num, operator, total_cost
from table (explain(null, 'S'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s45')
    stmt = """prepare s from
create unique index bug3i1 on bug3tab(c,d);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """select seq_num, operator, total_cost
from table (explain(null, 'S'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop index bug3i1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """prepare s from
create unique index bug3i1 on bug3tab(c,d);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """select seq_num, operator, total_cost
from table (explain(null, 'S'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table bug3tab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table BR0125o (i int, n varchar(10)) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table BR0125p (i int, c varchar(64)) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into BR0125p(i,c) values
(1,'abcdefghij'),(1,'longer>six'),(1,'alsoLonger'),
(2,'ABCDEF'),(2,'four'),(2,'five!'),(2,'ok'),
(3,'n/a'),(4,''),(5,''),(6,'');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 11)
    
    stmt = """insert into BR0125o values(1,''),(2,'o.n'),(3,''),(4,''),(5,''),(6,'');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 6)
    
    stmt = """select cast(c as char(6)) ccast_, char_length(c) from BR0125p;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s48')
    
    stmt = """select c, char_length(c) from BR0125p p, BR0125o o
where p.i = o.i and o.n='o.n';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s49')
    
    stmt = """select cast(c as char(6)) ccast_, char_length(c) from BR0125p p, BR0125o o
where p.i = o.i and o.n='o.n';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s50')
    
    _testmgr.testcase_end(desc)

def test003(desc="""a07"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:         A07
    #  Description:
    #  Test case inputs:       This test relies on the existence of
    #                          the files OPTTST, SORTTST
    #  Test case outputs:
    #  Expected Results:        (provide a high-level description)
    #
    #  Notes:
    #
    # =================== End Test Case Header  ===================
    # File: SQLS0307
    # Component  : NonStop SQL Regression Test Suite
    # Description: Tests elimination of redundant sorts
    # NOTE:
    # 1) This test relies on the existence of the files OPTTST,
    #    keytest (DEFINEs in SQLDEFS in test library subvolume).
    # 2) It tests the changes made to SCMPOPTO, SCMPOPTS as
    #    part of the 'QUality Improvement Programme' instituted
    #    by a government sanction in 1990 for uplifting the
    #    quality of the downtrodden SQL Compiler.
    # ---------------------------------
    # Open a Log file
    # ---------------------------------
    # LOG logA07 CLEAR;
    # ---------------------------------
    #  start with a clean slate
    
    stmt = """drop table OPTABLE;"""
    output = _dci.cmdexec(stmt)
    
    # delete define =T;
    
    # Create the test database
    # add define =T, class map, file t;
    
    stmt = """create table OPTABLE 
( p1  largeint not null
, u1  smallint unsigned
, zi1 smallint not null
, f1  double precision
, n1  numeric (4,2) unsigned
, d1  decimal (4,2)
, t1  date
, c1  char
, p2  integer not null
, u2  integer unsigned
, zi2 integer not null
, f2  real
, n2  numeric (6,3) unsigned
, d2  decimal (6,3)
, t2  time
, c2  char(2)
, p3  smallint not null
, u3  largeint
, zi3 largeint not null
, f3  float
, n3  numeric (12,4)
, d3  decimal (12,4)
, t3  interval hour to second
, c3  char(3)
, z   char (3800)
, primary key (p1, p2, p3) )
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into OPTABLE values (
10,  10,  10,  10,  10,  10, date '1959-12-31',  'a' ,
9,   9,   9,   9,   9,   9, time '23:59:59', 'aa',
9,null,  -1,null,null,null, null, null, null
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into OPTABLE values (
10,  10,  10,  10,  10,  10, date '1960-01-01', 'a'  ,
10,  10,  10,  10,  10,  10, time '00:00:00', 'aa' ,
10,  10,  10,  10,  10,  10, interval '00:00:00' hour to second, 'aaa', 'Row01'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
10,  10,  10,  10,  10, 10, date '1960-01-01',  'a'  ,
10,  10,  10,  10,  10, 10, time '00:00:15', 'aa' ,
20,  20,  20,  20,  20, 20, interval '00:00:15' hour to second, 'aab', 'Row02'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
10,  10,  10,  10,  10,  10, date '1960-01-01',  'a'  ,
10,  10,  10,  10,  10,  10, time '00:00:30', 'aa' ,
30,  30,  30,  30,  30,  30, interval '00:00:30' hour to second, 'aac', 'Row03'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into OPTABLE values (
10,  10,  10,  10,  10,  10, date '1960-01-01',  'a'  ,
20,  20,  20,  20,  20,  20, time '00:00:45', 'ab' ,
10,  10,  10,  10,  10,  10, interval '00:00:45' hour to second, 'aba', 'Row04'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
10,  10,  10,  10,  10,  10, date '1960-01-01',  'a'  ,
20,  20,  20,  20,  20,  20, time '00:01:00', 'ab' ,
20,  20,  20,  20,  20,  20, interval '00:01:00' hour to second, 'abb', 'Row05'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
10,  10,  10,  10,  10,  10, date '1960-01-01',  'a'  ,
20,  20,  20,  20,  20,  20, time '00:01:15', 'ab' ,
30,  30,  30,  30,  30,  30, interval '00:01:15' hour to second, 'abc', 'Row06'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into OPTABLE values (
10,  10,  10,  10,  10,  10, date '1960-01-01',  'a'  ,
30,  30,  30,  30,  30,  30, time '00:01:30', 'ac' ,
10,  10,  10,  10,  10,  10, interval '00:01:30' hour to second, 'aca', 'Row07'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
10,  10,  10,  10,  10,  10, date '1960-01-01',  'a'  ,
30,  30,  30,  30,  30,  30, time '00:01:45', 'ac' ,
20,  20,  20,  20,  20,  20, interval '00:01:45' hour to second, 'acb', 'Row08'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
10,  10,  10,  10,  10,  10, date '1960-01-01',  'a'  ,
30,  30,  30,  30,  30,  30, time '00:02:00', 'ac' ,
30,  30,  30,  30,  30,  30, null, 'acc', 'Row09'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into OPTABLE values (
20,  20,  20,  20,  20,  20, date '1960-01-01',  'b'  ,
10,  10,  10,  10,  10,  10, null,                               'ba' ,
10,  10,  10,  10,  10,  10, interval '00:02:00' hour to second, 'baa', 'Row10'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
20,  20,  20,  20,  20,  20, date '1960-01-01',  'b'  ,
10,  10,  10,  10,  10,  10, time '00:59:00', 'ba' ,
20,  20,  20,  20,  20,  20, interval '00:59:00' hour to second, 'bab', 'Row11'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
20,  20,  20,  20,  20,  20, date '1960-01-01',  'b'  ,
10,  10,  10,  10,  10,  10, time '00:59:15', 'ba' ,
30,  30,  30,  30,  30,  30, interval '00:59:15' hour to second, 'bac', 'Row12'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
20,  20,  20,  20,  20,  20, date '1960-01-01',  'b'  ,
20,  20,  20,  20,  20,  20, time '00:59:30', 'bb' ,
10,  10,  10,  10,  10,  10, interval '00:59:30' hour to second, 'bba', 'Row13'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
20,  20,  20,  20,  20,  20, date '1960-01-01',  'b'  ,
20,  20,  20,  20,  20,  20, time '00:59:45', 'bb' ,
20,  20,  20,  20,  20,  20, interval '00:59:45' hour to second, 'bbb', 'Row14'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
20,  20,  20,  20,  20,  20, date '1960-01-01',  'b'  ,
20,  20,  20,  20,  20,  20, time '01:00:00', 'bb' ,
30,  30,  30,  30,  30,  30, interval '01:00:00' hour to second, 'bbc', 'Row15'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
20,  20,  20,  20,  20,  20, date '1960-01-01',  'b'  ,
30,  30,  30,  30,  30,  30, time '01:00:00', 'bc' ,
10,  10,  10,  10,  10,  10, null,                               'bca', 'Row16'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
20,  20,  20,  20,  20,  20, date '1960-01-01',  'b'  ,
30,  30,  30,  30,  30,  30, time '01:00:15', 'bc' ,
20,  20,  20,  20,  20,  20, interval '01:00:15' hour to second, 'bcb', 'Row17'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
20,  20,  20,  20,  20,  20, date '1960-01-01',  'b'  ,
30,  30,  30,  30,  30,  30, time '01:00:30', 'bc' ,
30,  30,  30,  30,  30,  30, interval '01:00:30' hour to second, 'bcc', 'Row18'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
30,  30,  30,  30,  30,  30, date '1960-01-01',  'c'  ,
10,  10,  10,  10,  10,  10, time '01:00:45', 'ca' ,
10,  10,  10,  10,  10,  10, interval '01:00:45' hour to second, 'caa', 'Row19'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
30,  30,  30,  30,  30,  30, date '1960-01-01',  'c'  ,
10,  10,  10,  10,  10,  10, null,                               'ca' ,
20,  20,  20,  20,  20,  20, interval '01:01:00' hour to second, 'cab', 'Row20'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
30,  30,  30,  30,  30,  30, date '1960-01-01',  'c'  ,
10,  10,  10,  10,  10,  10, time '01:59:00', 'ca' ,
30,  30,  30,  30,  30,  30, interval '01:59:00' hour to second, 'cac', 'Row21'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
30,  30,  30,  30,  30,  30, date '1960-01-01',  'c'  ,
20,  20,  20,  20,  20,  20, time '01:59:15', 'cb' ,
10,  10,  10,  10,  10,  10, interval '01:59:15' hour to second, 'cba', 'Row22'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
30,  30,  30,  30,  30,  30, date '1960-01-01',  'c'  ,
20,  20,  20,  20,  20,  20, time '01:59:30', 'cb' ,
20,  20,  20,  20,  20,  20, interval '01:59:30' hour to second, 'cbb', 'Row23'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
30,  30,  30,  30,  30,  30, date '1960-01-01',  'c'  ,
20,  20,  20,  20,  20,  20, time '01:59:45', 'cb' ,
30,  30,  30,  30,  30,  30, interval '01:59:45' hour to second, 'cbc', 'Row24'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
30,  30,  30,  30,  30,  30, date '1960-01-01',  'c'  ,
30,  30,  30,  30,  30,  30, time '02:00:00', 'cc' ,
10,  10,  10,  10,  10,  10, interval '02:00:00' hour to second, 'cca', 'Row25'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
30,  30,  30,  30,  30,  30, date '1960-01-01',  'c'  ,
30,  30,  30,  30,  30,  30, time '11:59:00', 'cc' ,
20,  20,  20,  20,  20,  20, interval '11:59:00' hour to second, 'ccb', 'Row26'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
30,  30,  30,  30,  30,  30, date '1960-01-01',  'c'  ,
30,  30,  30,  30,  30,  30, time '11:59:15', 'cc' ,
30,  30,  30,  30,  30,  30, interval '11:59:15' hour to second, 'ccc', 'Row27'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
30,  10,  10,  10,  10,  10, date '1960-01-01',  'a'  ,
30,  10,  10,  10,  10,  10, time '11:59:30', 'ac' ,
40,null,  -1,null,null,null, interval '11:59:30' hour to second, 'aca', 'Row28'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
30,  10,  10,  10,  10,  10, date '1960-01-01',  'a'  ,
40,null,  -1,null,null,null, time '11:59:45', 'aa' ,
30,  10,  10,  10,  10,  10, interval '11:59:45' hour to second, null,  'Row29'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
30,  10,  10,  10,  10,  10, date '1960-01-01',  'a'  ,
40,null,  -1,null,null,null, time '12:00:00', null ,
40,null,  -1,null,null,null, interval '12:00:00' hour to second, 'aaa', 'Row30'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
40,null,  -1,null,null,null, date '1960-01-01',  null ,
30,  10,  10,  10,  10,  10, time '12:00:00', 'aa' ,
30,  10,  10,  10,  10,  10, interval '12:00:00' hour to second, 'aaa', 'Row31'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
40,null,  -2,null,null,null, date '1960-01-01',  'b'  ,
30,  10,  10,  10,  10,  10, time '23:59:15', 'bb' ,
40,  10,  10,  10,  10,  10, interval '23:59:15' hour to second, null , 'Row32'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
40,null,  -1,null,null,null, date '1960-01-01',  'b'  ,
40,  10,  10,  10,  10,  10, time '23:59:30', null ,
30,null,  -1,null,null,null, interval '23:59:30' hour to second, 'bbb', 'Row33'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
40,null,  -1,null,null,null, date '1960-01-01',  null ,
40,null,  -1,null,null,null, time '23:59:45', 'bb' ,
40,  10,  10,  10,  10,  10, interval '23:59:45' hour to second, 'bbb', 'Row34'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
40,null,  -1,null,null,null, date '1960-01-02',  'c'  ,
40,null,  -1,null,null,null, time '00:00:00', 'cc' ,
50,null,  -1,null,null,null, interval '24:00:00' hour to second, null , 'Row35'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """update statistics for table OPTABLE on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #  SET 12: Duplicate sort key columns in union queries.
    #  Ambiguous ordering column references are now flagged
    
    stmt = """select u1,u1
from OPTABLE 
where u1 = 30
union all
select f1,f2
from OPTABLE 
where u1 = 30
order by u1, u1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4004')
    #  reference to u1 is ambiguous
    
    # explain
    stmt = """select u1,u2,u3,p1,u1
from OPTABLE 
where u1 = 30
union all
select f1,f2,f3,p1,n1
from OPTABLE 
where u1 = 30
order by u1,u2,u3,u1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4004')
    #  reference to u1 is ambiguous
    
    # explain
    stmt = """select u1,u2,u1,u3,p1
from OPTABLE 
where u1 = 30
union all
select f1,f2,f3,p1,n1
from OPTABLE 
where u1 = 30
order by u1,u2,u1,u3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4004')
    #  reference to u1 is ambiguous
    
    #  Duplicate indexed references to the select list are
    #    eliminated. All EXPLAIN reports should show only
    #    one instance of column U1 in the Order By clause.
    
    # explain
    stmt = """select u1,u1
from OPTABLE 
where u1 = 30
union all
select f1,f2
from OPTABLE 
where u1 = 30
order by 1,1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s4')
    
    # explain
    stmt = """select u1,u2,u3,p1,u1
from OPTABLE 
where u1 = 30
union all
select f1,f2,f3,p1,n1
from OPTABLE 
where u1 = 30
order by 5,2,3,4,5
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s5')
    
    # explain
    stmt = """select u1,u2,u1,u3,p1
from OPTABLE 
where u1 = 30
union all
select f1,f2,f3,p1,n1
from OPTABLE 
where u1 = 30
order by 3,2,4,3,5
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s6')
    
    #  The normalizer (PROC noch^col^list) was eliminating duplicate
    #    references to the same item in the select list. This wasn't
    #    the right thing to do for unions, e.g.,
    
    # explain
    stmt = """select u1,u1
from OPTABLE 
where u1 = 30
union all
select f1,f2
from OPTABLE 
where u1 = 30
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s7')
    
    stmt = """select u1,u1
from OPTABLE 
where u1 = 30
union all
select f1,f2
from OPTABLE 
where u1 = 30
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s8')
    
    # explain
    stmt = """select u1,u2,u3,p1,u1
from OPTABLE 
where u1 = 30
union all
select f1,f2,f3,p1,n1
from OPTABLE 
where u1 = 30
order by  1,u2,u3,5
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s9')
    
    # explain
    stmt = """select u1,u2,u1,u3,p1
from OPTABLE 
where u1 = 30
union all
select f1,f2,f3,p1,n1
from OPTABLE 
where u1 = 30
order by  1,u2,3,u3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s10')
    
    # explain
    stmt = """select 'a',u1,1,u1,'A',u1
from OPTABLE 
where u1 = 30
union all
select 'b',f3,2,f2,'B',f1
from OPTABLE 
where u1 = 30
order by 2,4,6
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s11')
    
    stmt = """select 'a',u1,1,u1,'A',u1
from OPTABLE 
where u1 = 30
union all
select 'b',f3,2,f2,'B',f1
from OPTABLE 
where u1 = 30
order by 2,4,6
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s12')
    
    # explain
    stmt = """select 'a',u1,1,u1,'A',u1
from OPTABLE 
where u1 = 30
union all
select 'b',f3,2,f2,'B',f1
from OPTABLE 
where u1 = 30
order by 2,4 desc,6
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s13')
    
    stmt = """select 'a',u1,1,u1,'A',u1
from OPTABLE 
where u1 = 30
union all
select 'b',f3,2,f2,'B',f1
from OPTABLE 
where u1 = 30
order by 2,4 desc, 6
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s14')
    
    # explain
    stmt = """select 'a',u1,1,u1,'A',u1
from OPTABLE 
where u1 = 30
union all
select 'b',f3,2,f2,'B',f1
from OPTABLE 
where u1 = 30
order by 4,2 desc,6
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s15')
    
    stmt = """select 'a',u1,1,u1,'A',u1
from OPTABLE 
where u1 = 30
union all
select 'b',f3,2,f2,'B',f1
from OPTABLE 
where u1 = 30
order by 4,2 desc, 6
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s16')
    
    # Tests without any indices
    
    # If a column name was repeated in the select list of a SELECT DISTINCT
    #   query, then the SQL COmpiler gave an internal error
    
    stmt = """prepare s1 from
select distinct u2, u2, u1
from OPTABLE 
where p1 = 30
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'S1'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s18')
    
    #  SET 1 : Queries containing Aggregate Distinct Functions.
    
    #  MIN/MAX DISTINCT are converted to ordinary MIN/MAX
    #  Should see no SORT
    # explain
    stmt = """select max(distinct u1)
from OPTABLE 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s19')
    
    #  A MIN/MAX DISTINCT together with a COUNT/SUM/AVG DISTINCT
    #  on different columns should be allowed
    # explain
    stmt = """select min(distinct u1), count(distinct u2)
from OPTABLE 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s20')
    
    #  Permuting positions should not cause a different behaviour from above
    # explain
    stmt = """select avg(distinct u1), max(distinct u2)
from OPTABLE 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s21')
    
    #  Aggregate DISTINCT functions on different columns should get an error.
    #  However, they should be allowed on the same columns
    stmt = """prepare s1 from
select avg(distinct u1), avg(distinct u2)
from OPTABLE 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s22')
    
    stmt = """prepare s1 from
select sum(distinct u1), count(distinct u1), avg(distinct u1)
from OPTABLE 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s23')
    
    # The presence of a MIN/MAX DISTINCT in the select list should not
    # prevent a COUNT/SUM/AVG DISTINCT from being specified in the HAVING.
    stmt = """prepare s1 from
select max(distinct u2)
from OPTABLE T1
having count(distinct p1) < 10
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s24')
    
    #  A COUNT/SUM/AVG DISTINCT in the select list and in the HAVING
    #  must operate on the same column
    
    stmt = """prepare s1 from                   -- ERROR CASE
select sum(distinct u1), count(distinct u1), avg(distinct u1)
from OPTABLE 
having count(distinct p1) < 10
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s25')
    
    stmt = """prepare s1 from
select sum(distinct u1), count(distinct u1), avg(distinct u1)
from OPTABLE 
having count(distinct u1) > 0
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s26')
    
    # COUNT/SUM/AVG DISTINCT operands of a functions should behave no
    # differently than when referenced in their native state.
    
    # A MAX DISTINCT is degraded to a MAX. So, no conflict.
    stmt = """prepare s1 from
select upshift(max(distinct c1)), count(distinct c2)
from OPTABLE 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s27')
    
    stmt = """prepare s1 from
select count(distinct c1), upshift(max(distinct c2))
from OPTABLE 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s28')
    
    #  Error case.
    stmt = """prepare s1 from
select cast(count(distinct c1) as int), count(distinct c2)
from OPTABLE 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s29')
    
    # SET 2 : Select Distincts and Aggregate Distinct Functions.
    # *****
    # A Select Distinct and an aggregate distinct are allowed
    #   in the same query
    
    stmt = """prepare s1 from
select distinct u1, count(distinct u2)
from OPTABLE 
group by u1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s30')
    
    stmt = """prepare s1 from
select distinct u1,u2
from OPTABLE 
--group by 1,2
group by u1, u2
having count(distinct u2) > 0
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s31')
    
    # SET 3 : Select Distinct with Group By.
    # *****
    # A sort for a Group By and a Distinct can be combined into a
    #   a sort for a Group By when all the grouping columns also
    #   appear in the select list
    
    # GB contains an extraneous column, should see two sorts
    stmt = """prepare s1 from
select distinct u1, u2
from OPTABLE 
group by u1, u2, u3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'S1'));"""
    output = _dci.cmdexec(stmt)
    #  should see two sorts
    
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s33')
    
    # GB is identical to the select list, need only 1 sort
    stmt = """prepare s1 from
select distinct u1, u2
from OPTABLE 
group by u1, u2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'S1'));"""
    output = _dci.cmdexec(stmt)
    #  should see only one sort
    
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s35')
    
    # GB form a unique leading prefix of select list, need only 1 sort
    stmt = """prepare s1 from
select distinct u1, sum(u2)
from OPTABLE 
group by u1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'S1'));"""
    output = _dci.cmdexec(stmt)
    #  should see only one sort
    
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s37')
    
    # The select list contains expressions, should still see only 1 sort
    stmt = """prepare s1 from
select distinct u1, (u1+u2+u3)/10 AS column2
from OPTABLE 
group by u1, u2, u3
-- group by column2, u1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'S1'));"""
    output = _dci.cmdexec(stmt)
    #  should see only one sort
    
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s39')
    
    # GB form a unique leading prefix of select list, need only 1 sort
    stmt = """prepare s1 from
select distinct sum(u1), (u1+u2+u3)/10 AS column2
from OPTABLE 
group by u1, u2, u3
--group by column2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'S1'));"""
    output = _dci.cmdexec(stmt)
    #  should see only one sort
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s41')
    
    #  SET 4 : Select Distinct with Order By.
    #  *****
    #  A sort for an Order By and a Distinct is always merged because
    #    all the ordering columns appear in the select list
    
    #  ERROR CASE: OB list contains a column not in the select list
    stmt = """prepare s1 from
select distinct u1, u2
from OPTABLE 
order by u1 desc, u3 asc
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4121')
    
    # OB list is identical to the select list, need only 1 sort
    stmt = """prepare s1 from
select distinct u1, u2
from OPTABLE 
order by u1 desc, u2 asc
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'S1'));"""
    output = _dci.cmdexec(stmt)
    #  should see only one sort
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s44')
    
    # OB is identical to the select list, need only 1 sort
    stmt = """prepare s1 from
select distinct u1, u2
from OPTABLE 
order by u2 desc
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'S1'));"""
    output = _dci.cmdexec(stmt)
    #  should see only one sort
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s46')
    
    # The select list contains expressions, should still see only 1 sort
    stmt = """prepare s1 from
select distinct u1, (u1+u2+u3)/10
from OPTABLE 
order by 2 asc, 1 desc
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'S1'));"""
    output = _dci.cmdexec(stmt)
    #  should see only one sort
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s48')
    
    # OB form a unique leading prefix of select list, need only 1 sort
    stmt = """prepare s1 from
select distinct u1, (u1+u2+u3)/10
from OPTABLE 
order by 2 desc
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'S1'));"""
    output = _dci.cmdexec(stmt)
    #  should see only one sort
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s50')
    
    # SET 5 : Plain Select with Group By and Order By.
    # *****
    # Only one sort is needed to satisfy both a GB and an OB request
    #    1) if OB is contained within GB
    # or 2) if GB forms left prefix of OB
    
    # OB list is identical to the GB list, need only 1 sort
    stmt = """prepare s1 from
select u1, 2 * u2/10 AS column2 , count(*)
from OPTABLE 
group by u1, u2
-- group by u1, column2
order by 2 asc , 1 desc
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'S1'));"""
    output = _dci.cmdexec(stmt)
    #  should see 1 sort
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s52')
    
    # GB forms left prefix
    stmt = """prepare s1 from
select u1, 2 * u2/10 AS column2, count(*)
from OPTABLE 
group by u1, u2
--group by column2, u1
order by 1 desc , 2 desc , 3 asc
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'S1'));"""
    output = _dci.cmdexec(stmt)
    #  should see 1 sort
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s54')
    
    # GB list does not form left prefix of OB
    stmt = """prepare s1 from
select u1, 2 * u2/10 AS column2, count(*)
from OPTABLE 
group by u1, u2
--group by u1, AS column2
order by 3,2 desc
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'S1'));"""
    output = _dci.cmdexec(stmt)
    #  should see 2 sorts
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s56')
    
    # GB list contains an extraneous columns
    stmt = """prepare s1 from
select u1, count(*)
from OPTABLE 
group by u1, u2
order by 1 , 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'S1'));"""
    output = _dci.cmdexec(stmt)
    #  should see 2 sorts
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s58')
    
    # SET 6 : Select Distinct with Group By and Order By.
    # *****
    # A sort for an Order By and a Distinct cannot always be merged
    #   if there is a Group By present
    
    # GB forms unique prefix of D list so the two are combined.
    # But GB does not form left prefix of OB. So need OB sort.
    stmt = """prepare s1 from
select distinct u1, count(*)
from OPTABLE 
group by u1
order by 2, 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'S1'));"""
    output = _dci.cmdexec(stmt)
    #  should see 2 sorts, 1 GB, 1 OB
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s60')
    
    # GB and D cannot be combined because u2 is an extraneous column.
    # OB and D can be combined because OB is contained within D
    stmt = """prepare s1 from
select distinct u1, count(*)
from OPTABLE 
group by u1, u2
order by 2, 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'S1'));"""
    output = _dci.cmdexec(stmt)
    #  should see 2 sorts, 1GB, 1 D
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s62')
    
    # SET 7 : Plain Select with Group By and and aggregate distinct
    # *****
    # A sort for a an aggregate distinct is always combined with
    #   a sort for a GB
    
    # GB list is a cover for select list, need only 1 sort
    stmt = """prepare s1 from
select u1, u2, count(distinct f1)
from OPTABLE 
group by u1, u2, u3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'S1'));"""
    output = _dci.cmdexec(stmt)
    #  should see only one sort
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s64')
    
    # GB is identical to the select list, need only 1 sort
    stmt = """prepare s1 from
select u1, u2, count(distinct f1)
from OPTABLE 
group by u1, u2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'S1'));"""
    output = _dci.cmdexec(stmt)
    #  should see only one sort
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s66')
    
    # GB form a unique leading prefix of select list, need only 1 sort
    stmt = """prepare s1 from
select u1, sum(u2), count(distinct f1)
from OPTABLE 
group by u1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'S1'));"""
    output = _dci.cmdexec(stmt)
    #  should see only one sort
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s68')
    
    # The select list contains expressions, should still see only 1 sort
    stmt = """prepare s1 from
select u1, (u1+u2+u3)/10 AS column2, count(distinct f1)
from OPTABLE 
group by u1, u2, u3
-- group by column2, u1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'S1'));"""
    output = _dci.cmdexec(stmt)
    #  should see only one sort
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s70')
    
    # GB form a unique leading prefix of select list, need only 1 sort
    stmt = """prepare s1 from
select sum(u1), (u1+u2+u3)/10 AS column2, count(distinct f1)
from OPTABLE 
group by u1, u2, u3
--group by  AS column2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'S1'));"""
    output = _dci.cmdexec(stmt)
    #  should see only one sort
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s72')
    
    # SET 8 : Select Distinct with Group By and aggregate Distinct
    
    # Query contains D and GB. GB contains extraneous column, need only 2 sorts
    stmt = """prepare s1 from
select distinct u1, u2, count(distinct f1)
from OPTABLE 
group by u1, u2, u3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'S1'));"""
    output = _dci.cmdexec(stmt)
    #  should see two sorts
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s74')
    
    # Query contains D and GB is identical to the select list, need only 1 sort
    stmt = """prepare s1 from
select distinct u1, u2, count(distinct f1)
from OPTABLE 
group by u1, u2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'S1'));"""
    output = _dci.cmdexec(stmt)
    #  should see only one sort
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s76')
    
    # Query contains a D and GB form a unique leading prefix of select list
    stmt = """prepare s1 from
select distinct u1, sum(u2), count(distinct f1)
from OPTABLE 
group by u1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'S1'));"""
    output = _dci.cmdexec(stmt)
    #  should see only one sort
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s78')
    
    # The select list contains a D and expressions, should still see only 1 sort
    stmt = """prepare s1 from
select distinct u1, (u1+u2+u3)/10 AS column2, count(distinct f1)
from OPTABLE 
group by u1, u2, u3
--group by  AS column2, u1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'S1'));"""
    output = _dci.cmdexec(stmt)
    #  should see only one sort
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s80')
    
    # GB form a unique leading prefix of select list, need only 1 sort
    stmt = """prepare s1 from
select distinct sum(u1), (u1+u2+u3)/10 AS column2, count(distinct f1)
from OPTABLE 
group by u1, u2, u3
--group by  column2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'S1'));"""
    output = _dci.cmdexec(stmt)
    #  should see only one sort
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s82')
    
    # SET 9 : Select with Group By and aggregate Distinct
    #         and Order By
    
    # OB list is identical to the GB list, need only 1 sort
    stmt = """prepare s1 from
select u1, 2 * u2/10 AS column2 , count(*), count(distinct f1)
from OPTABLE 
group by u1, u2
--group by u1, column2
order by 2 asc , 1 desc
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'S1'));"""
    output = _dci.cmdexec(stmt)
    #  should see 1 sort
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s84')
    
    # GB list is contained in the OB list, need only 1 sort
    stmt = """prepare s1 from
select u1, 2 * u2/10 AS column2, count(*), count(distinct f1)
from OPTABLE 
group by u1, u2
--group by column2, u1
order by 1 desc , 2 desc , 3 asc
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'S1'));"""
    output = _dci.cmdexec(stmt)
    #  should see 1 sort
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s86')
    
    # OB list contained in the GB list, need 1 sort
    stmt = """prepare s1 from
select u1, 2 * u2/10 AS column2 , count(*), count(distinct f1)
from OPTABLE 
group by u1, u2
--group by u1,  column2
order by 2 desc
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'S1'));"""
    output = _dci.cmdexec(stmt)
    #  should see 1 sort
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s88')
    
    # GB list contains an extraneous columns
    stmt = """prepare s1 from
select u1, count(*), count(distinct f1)
from OPTABLE 
group by u1, u2
order by 1 , 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'S1'));"""
    output = _dci.cmdexec(stmt)
    #  should see 2 sorts
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s90')
    
    stmt = """prepare s1 from
select distinct u1, u2, count(distinct f1)
from OPTABLE 
group by u1, u2
order by 1 desc, 2 desc
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'S1'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s92')
    
    stmt = """prepare s1 from
select distinct u1, u2, count(*), sum(u1), avg(u1)
from OPTABLE 
group by u1, u2
having count(distinct u1) > 0
order by 1 desc, 2 desc
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'S1'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s94')
    
    # SET 10: Conversion of a Distinct to a Group By.
    
    stmt = """prepare s1 from
select distinct u1, u2 ,u3
from OPTABLE 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'S1'));"""
    output = _dci.cmdexec(stmt)
    # should see a sort for a Group By
    
    stmt = """prepare s1 from
select distinct u1, u2-u1,u3
from OPTABLE 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'S1'));"""
    output = _dci.cmdexec(stmt)
    #  should see a sort for a DISTINCT (no conversion to a Group By).
    
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'S1'));"""
    output = _dci.cmdexec(stmt)
    #  should see a sort for a Group By
    
    #  SET 11: Elimination of sorts due to presence of indices.
    
    stmt = """select u1, u2, u3, c3
from OPTABLE 
order by 2, 1, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s98')
    #  Sort key is not a subset of the search key
    #  Should see a sort being performed
    
    stmt = """select u1, u2, u3, c3
from OPTABLE 
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s99')
    #  ORDER BY in a different sequence than the index.
    #  Should see a sort being performed
    
    stmt = """select u1, u2, u3, c3
from OPTABLE 
order by 1, 2 desc, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s100')
    #  ORDER BY in the same sequence as the index.
    #  Should not see a sort being performed
    
    stmt = """select u1, u2, u3, c3
from OPTABLE 
order by 1 desc, 2 asc, 3 desc
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s101')
    #  ORDER BY in the reverse sequence as the index.
    #  Should not see a sort being performed
    
    stmt = """select u1, u2, u3, c3
from OPTABLE 
order by 1, 2 desc
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s102')
    #  ORDER BY in the same sequence as the index, partial sort key
    #  Should not see a sort being performed
    
    stmt = """select u1, u2, u3, c3
from OPTABLE 
order by 1 desc, 2 asc
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s103')
    #  ORDER BY in the reverse sequence as the index, partial sort key
    #  Should not see a sort being performed
    
    stmt = """select u1, u2, u3, c3
from OPTABLE 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s104')
    #  ORDER BY in the same sequence as the index, partial sort key
    #  Should not see a sort being performed
    
    stmt = """select u1, u2, u3, c3
from OPTABLE 
order by 1 desc
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s105')
    #  ORDER BY in the reverse sequence as the index, partial sort key
    #  Should not see a sort being performed
    
    stmt = """select u1, u2, u3, max(c3)
from OPTABLE 
-- group by 2, 1, 3
group by u2, u1, u3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s106')
    #  GROUP BY sort key is not a subset of the search key
    #  Should see a sort being performed
    
    stmt = """select u1, u2, u3, max(c3)
from OPTABLE 
-- group by 1, 2, 3
group by u1, u2, u3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s107')
    #  GROUP BY in a different sequence than the index.
    #  Should not see a sort being performed
    
    stmt = """select u1, u2, u3, max(c3)
from OPTABLE 
group by u1, u2, u3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s108')
    #  GROUP BY in the same sequence than the index.
    #  Should not see a sort being performed
    
    stmt = """select u1, u2, max(u3), max(c3)
from OPTABLE 
group by u1, u2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s109')
    #  GROUP BY in a different sequence than the index, partial sort key.
    #  Should not see a sort being performed
    
    stmt = """select u1, max(u2), max(u3), max(c3)
from OPTABLE 
group by u1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s110')
    #  GROUP BY in a different sequence than the index, partial sort key.
    #  Should not see a sort being performed
    
    stmt = """select distinct u1, u2, u3
from OPTABLE 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s111')
    #  DISTINCT in the same column order as the keys of a non-unique index
    #  Should see a sort being performed
    
    stmt = """select distinct u1, u2, u3, u2+u3
from OPTABLE 
group by u1, u2, u3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s112')
    #  A non-unique index on (u1, u2,u3) should be used.
    
    stmt = """select distinct p2, p1, p3
from OPTABLE 
--  DISTINCT in a different column order from OPTABLEhe unique index.
--  Should not see a sort being performed
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s113')
    
    stmt = """select distinct p1, p2, p3
from OPTABLE 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s114')
    #  DISTINCT in the same column order as the index.
    #  Should not see a sort being performed
    
    stmt = """select distinct T1.zi1, T1.zi2
from OPTABLE T1, OPTABLE  T2
where T1.zi1 = T2.zi2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s115')
    # Even if the unique index is used, a sort is required
    
    # SET 13: Use of an unique index when index key > sort key
    
    # DISTINCT
    # Sort key spans over an index key (constant in the sel list)
    stmt = """prepare s1 from
select distinct zi1,zi2,zi3,5
from OPTABLE 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'S1'));"""
    output = _dci.cmdexec(stmt)
    #  Should see no sort
    
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s117')
    
    # Expression in the select list
    stmt = """prepare s1 from
select distinct zi1,zi2,zi3,UPSHIFT(c1)
from OPTABLE 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'S1'));"""
    output = _dci.cmdexec(stmt)
    #  Should see no sort
    
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s119')
    
    # Non index key columns in the select list
    stmt = """prepare s1 from
select distinct u1,u2,u3,zi1,zi2,zi3
from OPTABLE 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'S1'));"""
    output = _dci.cmdexec(stmt)
    #  should see no sort
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s121')
    
    # ORDER BY
    stmt = """prepare s1 from
select u1,u2,u3,zi1,zi2,zi3
from OPTABLE 
order by 4,5,6,2,1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'S1'));"""
    output = _dci.cmdexec(stmt)
    #  should see no sort
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s123')
    
    stmt = """prepare s1 from
select u1,u2,u3,zi1,zi2,zi3
from OPTABLE order by 4 desc,5 asc,6
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'S1'));"""
    output = _dci.cmdexec(stmt)
    # ASC/DESC does not match that of the index, should see a sort
    
    stmt = """prepare s1 from
select distinct u1,u2,u3,zi1,zi2,zi3
from OPTABLE order by 4 desc,5 desc,6 desc
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'S1'));"""
    output = _dci.cmdexec(stmt)
    #  sort in the exact reverse sequence of the index, no sort necessary
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s126')
    
    stmt = """prepare s1 from
select zi1,zi2,zi3,u1,count(*)
from OPTABLE 
-- group by 1,2,3,4
group by zi1, zi2, zi3, u1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'S1'));"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s128')
    
    # Create a whole bunch of indices
    
    stmt = """create unique index zi123 on
 OPTABLE(zi1, zi2, zi3) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create unique index zi132 on
 OPTABLE(zi1, zi3, zi2) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create unique index zi231 on
 OPTABLE(zi2, zi3, zi1) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create unique index zi213 on
 OPTABLE(zi2, zi1, zi3) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create unique index zi312 on
 OPTABLE(zi3, zi1, zi2) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create unique index zi321 on
 OPTABLE(zi3, zi2, zi1) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index u123 on
 OPTABLE(u1, u2, u3) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index u132 on
 OPTABLE(u1, u3, u2) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index u231 on
 OPTABLE(u2, u3, u1) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index u213 on
 OPTABLE(u2, u1, u3) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index u312 on
 OPTABLE(u3, u1, u2) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index u321 on
 OPTABLE(u3, u2, u1) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index iuaaa on
 OPTABLE(U1 asc, u2 asc, u3 asc) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index iuaad on
 OPTABLE(U1 asc, u2 asc, u3 desc) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index iuada on
 OPTABLE(U1 asc, u2 desc, u3 asc) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index iuadd on
 OPTABLE(U1 asc, u2 desc, u3 desc) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index iudaa on
 OPTABLE(U1 desc, u2 asc, u3 asc) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index iudad on
 OPTABLE(U1 desc, u2 asc, u3 desc) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index iudda on
 OPTABLE(U1 desc, u2 desc, u3 asc) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index iuddd on
 OPTABLE(U1 desc, u2 desc, u3 desc) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # If a column name was repeated in the select list of a SELECT DISTINCT
    #   query, then the SQL COmpiler gave an internal error
    
    stmt = """prepare s1 from
select distinct u2, u2, u1
from OPTABLE 
where p1 = 30
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'S1'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s130')
    
    #  SET 1 : Queries containing Aggregate Distinct Functions.
    
    #  MIN/MAX DISTINCT are converted to ordinary MIN/MAX
    #  Should see no SORT
    # explain
    stmt = """select max(distinct u1)
from OPTABLE 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s131')
    
    #  A MIN/MAX DISTINCT together with a COUNT/SUM/AVG DISTINCT
    #  on different columns should be allowed
    # explain
    stmt = """select min(distinct u1), count(distinct u2)
from OPTABLE 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s132')
    
    #  Permuting positions should not cause a different behaviour from above
    # explain
    stmt = """select avg(distinct u1), max(distinct u2)
from OPTABLE 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s133')
    
    #  Aggregate DISTINCT functions on different columns should get an error.
    #  However, they should be allowed on the same columns
    stmt = """prepare s1 from
select avg(distinct u1), avg(distinct u2)
from OPTABLE 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s134')
    
    stmt = """prepare s1 from
select sum(distinct u1), count(distinct u1), avg(distinct u1)
from OPTABLE 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s135')
    
    # The presence of a MIN/MAX DISTINCT in the select list should not
    # prevent a COUNT/SUM/AVG DISTINCT from being specified in the HAVING.
    stmt = """prepare s1 from
select max(distinct u2)
from OPTABLE T1
having count(distinct p1) < 10
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s136')
    
    #  A COUNT/SUM/AVG DISTINCT in the select list and in the HAVING
    #  must operate on the same column
    
    stmt = """prepare s1 from                   -- ERROR CASE
select sum(distinct u1), count(distinct u1), avg(distinct u1)
from OPTABLE 
having count(distinct p1) < 10
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s137')
    
    stmt = """prepare s1 from
select sum(distinct u1), count(distinct u1), avg(distinct u1)
from OPTABLE 
having count(distinct u1) > 0
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s138')
    
    # COUNT/SUM/AVG DISTINCT operands of a functions should behave no
    # differently than when referenced in their native state.
    
    # A MAX DISTINCT is degraded to a MAX. So, no conflict.
    stmt = """prepare s1 from
select upshift(max(distinct c1)), count(distinct c2)
from OPTABLE 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s139')
    
    stmt = """prepare s1 from
select count(distinct c1), upshift(max(distinct c2))
from OPTABLE 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s140')
    
    #  Error case.
    stmt = """prepare s1 from
select cast(count(distinct c1) as int), count(distinct c2)
from OPTABLE 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s141')
    
    # SET 2 : Select Distincts and Aggregate Distinct Functions.
    # *****
    # A Select Distinct and an aggregate distinct are allowed
    #   in the same query
    
    stmt = """prepare s1 from
select distinct u1, count(distinct u2)
from OPTABLE 
group by u1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s142')
    
    stmt = """prepare s1 from
select distinct u1,u2
from OPTABLE 
--group by 1,2
group by u1, u2
having count(distinct u2) > 0
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s143')
    
    # SET 3 : Select Distinct with Group By.
    # *****
    # A sort for a Group By and a Distinct can be combined into a
    #   a sort for a Group By when all the grouping columns also
    #   appear in the select list
    
    # GB contains an extraneous column, should see two sorts
    stmt = """prepare s1 from
select distinct u1, u2
from OPTABLE 
group by u1, u2, u3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'S1'));"""
    output = _dci.cmdexec(stmt)
    #  should see two sorts
    
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s145')
    
    # GB is identical to the select list, need only 1 sort
    stmt = """prepare s1 from
select distinct u1, u2
from OPTABLE 
group by u1, u2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'S1'));"""
    output = _dci.cmdexec(stmt)
    #  should see only one sort
    
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s147')
    
    # GB form a unique leading prefix of select list, need only 1 sort
    stmt = """prepare s1 from
select distinct u1, sum(u2)
from OPTABLE 
group by u1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'S1'));"""
    output = _dci.cmdexec(stmt)
    #  should see only one sort
    
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s149')
    
    # The select list contains expressions, should still see only 1 sort
    stmt = """prepare s1 from
select distinct u1, (u1+u2+u3)/10 AS column2
from OPTABLE 
group by u1, u2, u3
-- group by column2, u1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'S1'));"""
    output = _dci.cmdexec(stmt)
    #  should see only one sort
    
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s151')
    
    # GB form a unique leading prefix of select list, need only 1 sort
    stmt = """prepare s1 from
select distinct sum(u1), (u1+u2+u3)/10 AS column2
from OPTABLE 
group by u1, u2, u3
--group by column2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'S1'));"""
    output = _dci.cmdexec(stmt)
    #  should see only one sort
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s153')
    
    #  SET 4 : Select Distinct with Order By.
    #  *****
    #  A sort for an Order By and a Distinct is always merged because
    #    all the ordering columns appear in the select list
    
    #  ERROR CASE: OB list contains a column not in the select list
    stmt = """prepare s1 from
select distinct u1, u2
from OPTABLE 
order by u1 desc, u3 asc
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4121')
    
    # OB list is identical to the select list, need only 1 sort
    stmt = """prepare s1 from
select distinct u1, u2
from OPTABLE 
order by u1 desc, u2 asc
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'S1'));"""
    output = _dci.cmdexec(stmt)
    #  should see only one sort
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s156')
    
    # OB is identical to the select list, need only 1 sort
    stmt = """prepare s1 from
select distinct u1, u2
from OPTABLE 
order by u2 desc
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'S1'));"""
    output = _dci.cmdexec(stmt)
    #  should see only one sort
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s158')
    
    # The select list contains expressions, should still see only 1 sort
    stmt = """prepare s1 from
select distinct u1, (u1+u2+u3)/10
from OPTABLE 
order by 2 asc, 1 desc
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'S1'));"""
    output = _dci.cmdexec(stmt)
    #  should see only one sort
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s160')
    
    # OB form a unique leading prefix of select list, need only 1 sort
    stmt = """prepare s1 from
select distinct u1, (u1+u2+u3)/10
from OPTABLE 
order by 2 desc
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'S1'));"""
    output = _dci.cmdexec(stmt)
    #  should see only one sort
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s162')
    
    # SET 5 : Plain Select with Group By and Order By.
    # *****
    # Only one sort is needed to satisfy both a GB and an OB request
    #    1) if OB is contained within GB
    # or 2) if GB forms left prefix of OB
    
    # OB list is identical to the GB list, need only 1 sort
    stmt = """prepare s1 from
select u1, 2 * u2/10 AS column2 , count(*)
from OPTABLE 
group by u1, u2
-- group by u1, column2
order by 2 asc , 1 desc
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'S1'));"""
    output = _dci.cmdexec(stmt)
    #  should see 1 sort
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s164')
    
    # GB forms left prefix
    stmt = """prepare s1 from
select u1, 2 * u2/10 AS column2, count(*)
from OPTABLE 
group by u1, u2
--group by column2, u1
order by 1 desc , 2 desc , 3 asc
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'S1'));"""
    output = _dci.cmdexec(stmt)
    #  should see 1 sort
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s166')
    
    # GB list does not form left prefix of OB
    stmt = """prepare s1 from
select u1, 2 * u2/10 AS column2, count(*)
from OPTABLE 
group by u1, u2
--group by u1, AS column2
order by 3,2 desc
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'S1'));"""
    output = _dci.cmdexec(stmt)
    #  should see 2 sorts
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s168')
    
    # GB list contains an extraneous columns
    stmt = """prepare s1 from
select u1, count(*)
from OPTABLE 
group by u1, u2
order by 1 , 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'S1'));"""
    output = _dci.cmdexec(stmt)
    #  should see 2 sorts
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s170')
    
    # SET 6 : Select Distinct with Group By and Order By.
    # *****
    # A sort for an Order By and a Distinct cannot always be merged
    #   if there is a Group By present
    
    # GB forms unique prefix of D list so the two are combined.
    # But GB does not form left prefix of OB. So need OB sort.
    stmt = """prepare s1 from
select distinct u1, count(*)
from OPTABLE 
group by u1
order by 2, 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'S1'));"""
    output = _dci.cmdexec(stmt)
    #  should see 2 sorts, 1 GB, 1 OB
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s172')
    
    # GB and D cannot be combined because u2 is an extraneous column.
    # OB and D can be combined because OB is contained within D
    stmt = """prepare s1 from
select distinct u1, count(*)
from OPTABLE 
group by u1, u2
order by 2, 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'S1'));"""
    output = _dci.cmdexec(stmt)
    #  should see 2 sorts, 1GB, 1 D
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s174')
    
    # SET 7 : Plain Select with Group By and and aggregate distinct
    # *****
    # A sort for a an aggregate distinct is always combined with
    #   a sort for a GB
    
    # GB list is a cover for select list, need only 1 sort
    stmt = """prepare s1 from
select u1, u2, count(distinct f1)
from OPTABLE 
group by u1, u2, u3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'S1'));"""
    output = _dci.cmdexec(stmt)
    #  should see only one sort
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s176')
    
    # GB is identical to the select list, need only 1 sort
    stmt = """prepare s1 from
select u1, u2, count(distinct f1)
from OPTABLE 
group by u1, u2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'S1'));"""
    output = _dci.cmdexec(stmt)
    #  should see only one sort
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s178')
    
    # GB form a unique leading prefix of select list, need only 1 sort
    stmt = """prepare s1 from
select u1, sum(u2), count(distinct f1)
from OPTABLE 
group by u1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'S1'));"""
    output = _dci.cmdexec(stmt)
    #  should see only one sort
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s180')
    
    # The select list contains expressions, should still see only 1 sort
    stmt = """prepare s1 from
select u1, (u1+u2+u3)/10 AS column2, count(distinct f1)
from OPTABLE 
group by u1, u2, u3
-- group by column2, u1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'S1'));"""
    output = _dci.cmdexec(stmt)
    #  should see only one sort
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s182')
    
    # GB form a unique leading prefix of select list, need only 1 sort
    stmt = """prepare s1 from
select sum(u1), (u1+u2+u3)/10 AS column2, count(distinct f1)
from OPTABLE 
group by u1, u2, u3
--group by  AS column2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'S1'));"""
    output = _dci.cmdexec(stmt)
    #  should see only one sort
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s184')
    
    # SET 8 : Select Distinct with Group By and aggregate Distinct
    
    # Query contains D and GB. GB contains extraneous column, need only 2 sorts
    stmt = """prepare s1 from
select distinct u1, u2, count(distinct f1)
from OPTABLE 
group by u1, u2, u3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'S1'));"""
    output = _dci.cmdexec(stmt)
    #  should see two sorts
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s186')
    
    # Query contains D and GB is identical to the select list, need only 1 sort
    stmt = """prepare s1 from
select distinct u1, u2, count(distinct f1)
from OPTABLE 
group by u1, u2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'S1'));"""
    output = _dci.cmdexec(stmt)
    #  should see only one sort
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s188')
    
    # Query contains a D and GB form a unique leading prefix of select list
    stmt = """prepare s1 from
select distinct u1, sum(u2), count(distinct f1)
from OPTABLE 
group by u1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'S1'));"""
    output = _dci.cmdexec(stmt)
    #  should see only one sort
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s190')
    
    # The select list contains a D and expressions, should still see only 1 sort
    stmt = """prepare s1 from
select distinct u1, (u1+u2+u3)/10 AS column2, count(distinct f1)
from OPTABLE 
group by u1, u2, u3
--group by  AS column2, u1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'S1'));"""
    output = _dci.cmdexec(stmt)
    #  should see only one sort
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s192')
    
    # GB form a unique leading prefix of select list, need only 1 sort
    stmt = """prepare s1 from
select distinct sum(u1), (u1+u2+u3)/10 AS column2, count(distinct f1)
from OPTABLE 
group by u1, u2, u3
--group by  column2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'S1'));"""
    output = _dci.cmdexec(stmt)
    #  should see only one sort
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s194')
    
    # SET 9 : Select with Group By and aggregate Distinct
    #         and Order By
    
    # OB list is identical to the GB list, need only 1 sort
    stmt = """prepare s1 from
select u1, 2 * u2/10 AS column2 , count(*), count(distinct f1)
from OPTABLE 
group by u1, u2
--group by u1, column2
order by 2 asc , 1 desc
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'S1'));"""
    output = _dci.cmdexec(stmt)
    #  should see 1 sort
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s196')
    
    # GB list is contained in the OB list, need only 1 sort
    stmt = """prepare s1 from
select u1, 2 * u2/10 AS column2, count(*), count(distinct f1)
from OPTABLE 
group by u1, u2
--group by column2, u1
order by 1 desc , 2 desc , 3 asc
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'S1'));"""
    output = _dci.cmdexec(stmt)
    #  should see 1 sort
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s198')
    
    # OB list contained in the GB list, need 1 sort
    stmt = """prepare s1 from
select u1, 2 * u2/10 AS column2 , count(*), count(distinct f1)
from OPTABLE 
group by u1, u2
--group by u1,  column2
order by 2 desc
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'S1'));"""
    output = _dci.cmdexec(stmt)
    #  should see 1 sort
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s200')
    
    # GB list contains an extraneous columns
    stmt = """prepare s1 from
select u1, count(*), count(distinct f1)
from OPTABLE 
group by u1, u2
order by 1 , 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'S1'));"""
    output = _dci.cmdexec(stmt)
    #  should see 2 sorts
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s202')
    
    stmt = """prepare s1 from
select distinct u1, u2, count(distinct f1)
from OPTABLE 
group by u1, u2
order by 1 desc, 2 desc
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'S1'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s204')
    
    stmt = """prepare s1 from
select distinct u1, u2, count(*), sum(u1), avg(u1)
from OPTABLE 
group by u1, u2
having count(distinct u1) > 0
order by 1 desc, 2 desc
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'S1'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s206')
    
    # SET 10: Conversion of a Distinct to a Group By.
    
    stmt = """prepare s1 from
select distinct u1, u2 ,u3
from OPTABLE 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'S1'));"""
    output = _dci.cmdexec(stmt)
    # should see a sort for a Group By
    
    stmt = """prepare s1 from
select distinct u1, u2-u1,u3
from OPTABLE 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'S1'));"""
    output = _dci.cmdexec(stmt)
    #  should see a sort for a DISTINCT (no conversion to a Group By).
    
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'S1'));"""
    output = _dci.cmdexec(stmt)
    #  should see a sort for a Group By
    
    #  SET 11: Elimination of sorts due to presence of indices.
    stmt = """select u1, u2, u3, c3
from OPTABLE 
order by 2, 1, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s210')
    #  Sort key is not a subset of the search key
    #  Should see a sort being performed
    
    stmt = """select u1, u2, u3, c3
from OPTABLE 
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s211')
    #  ORDER BY in a different sequence than the index.
    #  Should see a sort being performed
    
    stmt = """select u1, u2, u3, c3
from OPTABLE 
order by 1, 2 desc, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s212')
    #  ORDER BY in the same sequence as the index.
    #  Should not see a sort being performed
    
    stmt = """select u1, u2, u3, c3
from OPTABLE 
order by 1 desc, 2 asc, 3 desc
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s213')
    #  ORDER BY in the reverse sequence as the index.
    #  Should not see a sort being performed
    
    stmt = """select u1, u2, u3, c3
from OPTABLE 
order by 1, 2 desc
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s214')
    #  ORDER BY in the same sequence as the index, partial sort key
    #  Should not see a sort being performed
    
    stmt = """select u1, u2, u3, c3
from OPTABLE 
order by 1 desc, 2 asc
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s215')
    #  ORDER BY in the reverse sequence as the index, partial sort key
    #  Should not see a sort being performed
    
    stmt = """select u1, u2, u3, c3
from OPTABLE 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s216')
    #  ORDER BY in the same sequence as the index, partial sort key
    #  Should not see a sort being performed
    
    stmt = """select u1, u2, u3, c3
from OPTABLE 
order by 1 desc
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s217')
    #  ORDER BY in the reverse sequence as the index, partial sort key
    #  Should not see a sort being performed
    stmt = """select u1, u2, u3, max(c3)
from OPTABLE 
-- group by 2, 1, 3
group by u2, u1, u3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s218')
    #  GROUP BY sort key is not a subset of the search key
    #  Should see a sort being performed
    
    stmt = """select u1, u2, u3, max(c3)
from OPTABLE 
-- group by 1, 2, 3
group by u1, u2, u3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s219')
    #  GROUP BY in a different sequence than the index.
    #  Should not see a sort being performed
    
    stmt = """select u1, u2, u3, max(c3)
from OPTABLE 
group by u1, u2, u3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s220')
    #  GROUP BY in the same sequence than the index.
    #  Should not see a sort being performed
    
    stmt = """select u1, u2, max(u3), max(c3)
from OPTABLE 
group by u1, u2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s221')
    #  GROUP BY in a different sequence than the index, partial sort key.
    #  Should not see a sort being performed
    
    stmt = """select u1, max(u2), max(u3), max(c3)
from OPTABLE 
group by u1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s222')
    #  GROUP BY in a different sequence than the index, partial sort key.
    #  Should not see a sort being performed
    
    stmt = """select distinct u1, u2, u3
from OPTABLE 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s223')
    #  DISTINCT in the same column order as the keys of a non-unique index
    #  Should see a sort being performed
    
    stmt = """select distinct u1, u2, u3, u2+u3
from OPTABLE 
group by u1, u2, u3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s224')
    #  A non-unique index on (u1, u2,u3) should be used.
    
    stmt = """select distinct p2, p1, p3
from OPTABLE 
--  DISTINCT in a different column order from OPTABLEhe unique index.
--  Should not see a sort being performed
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s225')
    
    stmt = """select distinct p1, p2, p3
from OPTABLE 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s226')
    #  DISTINCT in the same column order as the index.
    #  Should not see a sort being performed
    
    stmt = """select distinct T1.zi1, T1.zi2
from OPTABLE T1, OPTABLE  T2
where T1.zi1 = T2.zi2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s227')
    # Even if the unique index is used, a sort is required
    
    # SET 13: Use of an unique index when index key > sort key
    
    # DISTINCT
    # Sort key spans over an index key (constant in the sel list)
    stmt = """prepare s1 from
select distinct zi1,zi2,zi3,5
from OPTABLE 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'S1'));"""
    output = _dci.cmdexec(stmt)
    #  Should see no sort
    
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s229')
    
    # Expression in the select list
    stmt = """prepare s1 from
select distinct zi1,zi2,zi3,UPSHIFT(c1)
from OPTABLE 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'S1'));"""
    output = _dci.cmdexec(stmt)
    #  Should see no sort
    
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s231')
    
    # Non index key columns in the select list
    stmt = """prepare s1 from
select distinct u1,u2,u3,zi1,zi2,zi3
from OPTABLE 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'S1'));"""
    output = _dci.cmdexec(stmt)
    #  should see no sort
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s233')
    
    # ORDER BY
    stmt = """prepare s1 from
select u1,u2,u3,zi1,zi2,zi3
from OPTABLE 
order by 4,5,6,2,1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'S1'));"""
    output = _dci.cmdexec(stmt)
    #  should see no sort
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s235')
    
    stmt = """prepare s1 from
select u1,u2,u3,zi1,zi2,zi3
from OPTABLE order by 4 desc,5 asc,6
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'S1'));"""
    output = _dci.cmdexec(stmt)
    # ASC/DESC does not match that of the index, should see a sort
    
    stmt = """prepare s1 from
select distinct u1,u2,u3,zi1,zi2,zi3
from OPTABLE order by 4 desc,5 desc,6 desc
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'S1'));"""
    output = _dci.cmdexec(stmt)
    #  sort in the exact reverse sequence of the index, no sort necessary
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s238')
    
    stmt = """prepare s1 from
select zi1,zi2,zi3,u1,count(*)
from OPTABLE 
-- group by 1,2,3,4
group by zi1, zi2, zi3, u1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'S1'));"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s240')
    
    stmt = """drop index iuaaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop index iuaad;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop index iuada;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop index iuadd;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop index iudaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop index iudad;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop index iudda;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop index iuddd;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop index u123;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop index u132;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop index u231;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop index u213;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop index u312;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop index u321;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop index zi123;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop index zi132;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop index zi231;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop index zi213;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop index zi312;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop index zi321;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test004(desc="""a08"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     A08
    #  Description:        Merge Joins and Sorts includes Outer/Inner Joins
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    #  Notes:
    #  02/12/97            Explain has been commented out for Regress runs.
    #  This test case incorporates features detailed in the "Title"
    #  by Ima Programmer (Version 1.1, <date>).
    #
    # =================== End Test Case Header  ===================
    # File       :  SQLS0308                Formerly .dtest.mjtest2
    # Description:  Merge Joins and Sorts
    #               Includes Outer/Inner Joins
    #
    # ---------------------------------
    # Open a Log file
    # ---------------------------------
    # LOG logA08 CLEAR;
    # ---------------------------------
    
    stmt = """create table omerg1 (a int default null,
b int default null,
c int default null) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table omerg2 (a int default null,
b int default null,
c int default null) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table omerg3 (a int default null,
b int default null,
c int default null) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """insert into omerg1 values (0,0,0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into omerg2 values (0,0,0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into omerg3 values (0,0,0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """update statistics for table omerg1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """update statistics for table omerg2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """update statistics for table omerg3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """delete from omerg1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    stmt = """delete from omerg2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    stmt = """delete from omerg3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    stmt = """set param ?a1 10;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?a2 10;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?a3 10;"""
    output = _dci.cmdexec(stmt)
    stmt = """prepare s from insert into omerg1 values(?a1, ?a2, ?a3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """set param ?b1 10;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?b2 1;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?b3 1;"""
    output = _dci.cmdexec(stmt)
    stmt = """prepare s from insert into omerg2 values(?b1, ?b2, ?b3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """set param ?b1 10;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?b2 5;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?b3 1;"""
    output = _dci.cmdexec(stmt)
    stmt = """prepare s from insert into omerg2 values(?b1, ?b2, ?b3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """set param ?b1 10;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?b2 10;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?b3 1;"""
    output = _dci.cmdexec(stmt)
    stmt = """prepare s from insert into omerg2 values(?b1, ?b2, ?b3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """prepare s1 from
select t1.b from omerg2 t1 left join
 omerg2 t2
on (t1.b=t2.b)
order by t1.b desc
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain(NULL,'S1'));"""
    output = _dci.cmdexec(stmt)
    #  If a merge join is done then there is no need to sort for the
    #  order by.
    #  Neither S02 nor S03 generate a sort for the order. The S02 -- explain
    #  will show that the sort for the merge join will be done in ASC
    #  order when in reality it will be done in DESC order. S03 -- explain
    #  shows that it is in DESC order.
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s1')
    
    stmt = """prepare s2 from select t1.b from omerg2 t1
join omerg2 t2 on (t1.b=t2.b) order by t1.b desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain(NULL,'S2'));"""
    output = _dci.cmdexec(stmt)
    #  If a merge join is done then there is no need for a sort for the
    #  OB regardless of which table is the outer table.
    #
    stmt = """execute s2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s3')
    
    stmt = """prepare s3 from
select t1.b from omerg2 t1 join omerg2 t2
on (t1.b=t2.b) order by t2.b desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain(NULL,'S3'));"""
    output = _dci.cmdexec(stmt)
    #  This query is the same as s2 except OB t2.b instead of t1.b
    #  The optimizer should the same plan as in query S2 since there
    #  is no difference in the queries (except that it is a toss up).
    #  S02 picks the same plan S03 picks different plans.
    
    stmt = """execute s3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s5')
    
    stmt = """prepare s4 from
select t2.b from omerg1 t1 left join omerg2 t2
on (t1.a=t2.b)
left join omerg2 t3
on (t2.b=t3.c)
order by t2.b desc
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain(NULL,'S4'));"""
    output = _dci.cmdexec(stmt)
    #  If a merge join is done to join the composite (T1,T2) table with
    #  T3 then there is no need to sort again for the order by.
    #  S02 does not realize this.
    stmt = """execute s4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s7')
    
    stmt = """prepare s5 from
select t2.b from omerg1 t1      join omerg2 t2
on (t1.a=t2.b)
join omerg2 t3
on (t2.b=t3.c)
order by t2.b desc
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain(NULL,'S5'));"""
    output = _dci.cmdexec(stmt)
    # Each table is sorted once and there is no need for an additional
    # sort for the order by regardless of which table is the outer table.
    # Again the S02 -- explain shows the sorts in ASC
    # order but will actually be done in descending order.
    stmt = """execute s5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """prepare s6 from
select t2.b from omerg1 t1      join omerg2 t2
on (t1.a=t2.b)
left join omerg2 t3
on (t2.b=t3.c)
order by t2.b desc
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain(NULL,'S6'));"""
    output = _dci.cmdexec(stmt)
    #  Again, no sort for order by is needed.
    stmt = """execute s6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s10')
    
    stmt = """prepare s7 from
select t2.b from omerg1 t1 left join omerg2 t2
on (t1.a=t2.b)
join omerg2 t3
on (t2.b=t3.c)
order by t2.b desc
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain(NULL,'S7'));"""
    output = _dci.cmdexec(stmt)
    # S02 does not perform a merge join between the composite (T1,T2)
    # and T3. If it did then it could
    # also detect that there is no need for an additional sort for the
    # order by.
    stmt = """execute s7;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """prepare s8 from
select t2.b from omerg1 t1 left join omerg2 t2
on (t1.a=t2.b)
left join omerg2 t3
on (t2.b=t3.c)
left join omerg3 t4
on (t2.b=t4.a)
order by t2.b desc
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain(NULL,'S8'));"""
    output = _dci.cmdexec(stmt)
    #  The last merge join does not need a sort for a previous composite
    #  since there was a sort for a previous composite already done for
    #  column t2.b. S02 does the sort for the previous composite in this
    #  case. S03 wont.
    #  Also there is no need for a sort for the order by for the same reasons
    #  but S02 does not detect that.
    
    stmt = """execute s8;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s13')
    
    stmt = """prepare s9 from
select t2.b from omerg1 t1 left join omerg2 t2
on (t1.a=t2.b)
left join omerg2 t3
on (t2.b=t3.c)
left join omerg3 t4
on (t3.c=t4.a)
order by t2.b desc
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain(NULL,'S9'));"""
    output = _dci.cmdexec(stmt)
    #  The opposite of the previous query. The last merge join needs to
    #  do a sort previous composite on T3.c and the sort for the order
    #  order by becomes necessary.
    #  S02 and S03 should generate the same plan here.
    
    stmt = """execute s9;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s15')
    
    stmt = """prepare s10 from
select t1.b,t2.b from omerg2 t1 left join omerg3 t2
on (t1.b=t2.b)
left join omerg2 t3
on (t2.b=t3.c)
order by t1.b desc
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain(NULL,'S10'));"""
    output = _dci.cmdexec(stmt)
    #  If a merge join is done to join the composite (T1,T2) table with
    #  T3 then there we need to sort again for the order by.
    #  S02 does not realize this. 
    stmt = """execute s10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s17')
    # Should be sorted by the first column desc, not the second column
    
    stmt = """drop table omerg1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table omerg2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table omerg3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test005(desc="""a09"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:         A09
    #  Description:
    #  Test case inputs:       This test relies on the existence of
    #                          the files OPTTST,AGGTST
    #  Test case outputs:
    #  Expected Results:        (provide a high-level description)
    #
    #  Notes:
    #  This test case incorporates features detailed in the "Title"
    #  by Ima Programmer (Version 1.1, <date>).
    #
    # =================== End Test Case Header  ===================
    # File: SQLS0309
    # Component  : NonStop SQL Regression Test Suite
    # Description: Test MIN/MAX optimization.
    # NOTE:
    #   This test relies on the existence of the files OPTTST,
    #   =aggtest (DEFINEs in SQLDEFS in test library subvolume).
    #   These tests should be run using C30S02 or its successor.
    #
    # ---------------------------------
    # Open a Log file
    # ---------------------------------
    # ---------------------------------
    # start with a clean slate
    
    stmt = """drop table OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # delete define =T;
    
    # Create the test database
    # add define =T, class map, file t;
    
    stmt = """create table OPTABLE 
( p1  largeint not null
, u1  smallint unsigned
, zi1 smallint not null
, f1  double precision
, n1  numeric (4,2) unsigned
, d1  decimal (4,2)
, t1  date
, c1  char
, p2  integer not null
, u2  integer unsigned
, zi2 integer not null
, f2  real
, n2  numeric (6,3) unsigned
, d2  decimal (6,3)
, t2  time
, c2  char(2)
, p3  smallint not null
, u3  largeint
, zi3 largeint not null
, f3  float
, n3  numeric (12,4)
, d3  decimal (12,4)
, t3  interval hour to second
, c3  char(3)
, z   char (3800)
, primary key (p1, p2, p3) )
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into OPTABLE values (
10,  10,  10,  10,  10,  10, date '1959-12-31',  'a' ,
9,   9,   9,   9,   9,   9, time '23:59:59', 'aa',
9,null,  -1,null,null,null, null, null, null
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into OPTABLE values (
10,  10,  10,  10,  10,  10, date '1960-01-01', 'a'  ,
10,  10,  10,  10,  10,  10, time '00:00:00', 'aa' ,
10,  10,  10,  10,  10,  10, interval '00:00:00' hour to second, 'aaa', 'Row01'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
10,  10,  10,  10,  10, 10, date '1960-01-01',  'a'  ,
10,  10,  10,  10,  10, 10, time '00:00:15', 'aa' ,
20,  20,  20,  20,  20, 20, interval '00:00:15' hour to second, 'aab', 'Row02'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
10,  10,  10,  10,  10,  10, date '1960-01-01',  'a'  ,
10,  10,  10,  10,  10,  10, time '00:00:30', 'aa' ,
30,  30,  30,  30,  30,  30, interval '00:00:30' hour to second, 'aac', 'Row03'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into OPTABLE values (
10,  10,  10,  10,  10,  10, date '1960-01-01',  'a'  ,
20,  20,  20,  20,  20,  20, time '00:00:45', 'ab' ,
10,  10,  10,  10,  10,  10, interval '00:00:45' hour to second, 'aba', 'Row04'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
10,  10,  10,  10,  10,  10, date '1960-01-01',  'a'  ,
20,  20,  20,  20,  20,  20, time '00:01:00', 'ab' ,
20,  20,  20,  20,  20,  20, interval '00:01:00' hour to second, 'abb', 'Row05'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
10,  10,  10,  10,  10,  10, date '1960-01-01',  'a'  ,
20,  20,  20,  20,  20,  20, time '00:01:15', 'ab' ,
30,  30,  30,  30,  30,  30, interval '00:01:15' hour to second, 'abc', 'Row06'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into OPTABLE values (
10,  10,  10,  10,  10,  10, date '1960-01-01',  'a'  ,
30,  30,  30,  30,  30,  30, time '00:01:30', 'ac' ,
10,  10,  10,  10,  10,  10, interval '00:01:30' hour to second, 'aca', 'Row07'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
10,  10,  10,  10,  10,  10, date '1960-01-01',  'a'  ,
30,  30,  30,  30,  30,  30, time '00:01:45', 'ac' ,
20,  20,  20,  20,  20,  20, interval '00:01:45' hour to second, 'acb', 'Row08'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
10,  10,  10,  10,  10,  10, date '1960-01-01',  'a'  ,
30,  30,  30,  30,  30,  30, time '00:02:00', 'ac' ,
30,  30,  30,  30,  30,  30, null, 'acc', 'Row09'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into OPTABLE values (
20,  20,  20,  20,  20,  20, date '1960-01-01',  'b'  ,
10,  10,  10,  10,  10,  10, null,                               'ba' ,
10,  10,  10,  10,  10,  10, interval '00:02:00' hour to second, 'baa', 'Row10'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
20,  20,  20,  20,  20,  20, date '1960-01-01',  'b'  ,
10,  10,  10,  10,  10,  10, time '00:59:00', 'ba' ,
20,  20,  20,  20,  20,  20, interval '00:59:00' hour to second, 'bab', 'Row11'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
20,  20,  20,  20,  20,  20, date '1960-01-01',  'b'  ,
10,  10,  10,  10,  10,  10, time '00:59:15', 'ba' ,
30,  30,  30,  30,  30,  30, interval '00:59:15' hour to second, 'bac', 'Row12'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
20,  20,  20,  20,  20,  20, date '1960-01-01',  'b'  ,
20,  20,  20,  20,  20,  20, time '00:59:30', 'bb' ,
10,  10,  10,  10,  10,  10, interval '00:59:30' hour to second, 'bba', 'Row13'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
20,  20,  20,  20,  20,  20, date '1960-01-01',  'b'  ,
20,  20,  20,  20,  20,  20, time '00:59:45', 'bb' ,
20,  20,  20,  20,  20,  20, interval '00:59:45' hour to second, 'bbb', 'Row14'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
20,  20,  20,  20,  20,  20, date '1960-01-01',  'b'  ,
20,  20,  20,  20,  20,  20, time '01:00:00', 'bb' ,
30,  30,  30,  30,  30,  30, interval '01:00:00' hour to second, 'bbc', 'Row15'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
20,  20,  20,  20,  20,  20, date '1960-01-01',  'b'  ,
30,  30,  30,  30,  30,  30, time '01:00:00', 'bc' ,
10,  10,  10,  10,  10,  10, null,                               'bca', 'Row16'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
20,  20,  20,  20,  20,  20, date '1960-01-01',  'b'  ,
30,  30,  30,  30,  30,  30, time '01:00:15', 'bc' ,
20,  20,  20,  20,  20,  20, interval '01:00:15' hour to second, 'bcb', 'Row17'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
20,  20,  20,  20,  20,  20, date '1960-01-01',  'b'  ,
30,  30,  30,  30,  30,  30, time '01:00:30', 'bc' ,
30,  30,  30,  30,  30,  30, interval '01:00:30' hour to second, 'bcc', 'Row18'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
30,  30,  30,  30,  30,  30, date '1960-01-01',  'c'  ,
10,  10,  10,  10,  10,  10, time '01:00:45', 'ca' ,
10,  10,  10,  10,  10,  10, interval '01:00:45' hour to second, 'caa', 'Row19'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
30,  30,  30,  30,  30,  30, date '1960-01-01',  'c'  ,
10,  10,  10,  10,  10,  10, null,                               'ca' ,
20,  20,  20,  20,  20,  20, interval '01:01:00' hour to second, 'cab', 'Row20'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
30,  30,  30,  30,  30,  30, date '1960-01-01',  'c'  ,
10,  10,  10,  10,  10,  10, time '01:59:00', 'ca' ,
30,  30,  30,  30,  30,  30, interval '01:59:00' hour to second, 'cac', 'Row21'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
30,  30,  30,  30,  30,  30, date '1960-01-01',  'c'  ,
20,  20,  20,  20,  20,  20, time '01:59:15', 'cb' ,
10,  10,  10,  10,  10,  10, interval '01:59:15' hour to second, 'cba', 'Row22'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
30,  30,  30,  30,  30,  30, date '1960-01-01',  'c'  ,
20,  20,  20,  20,  20,  20, time '01:59:30', 'cb' ,
20,  20,  20,  20,  20,  20, interval '01:59:30' hour to second, 'cbb', 'Row23'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
30,  30,  30,  30,  30,  30, date '1960-01-01',  'c'  ,
20,  20,  20,  20,  20,  20, time '01:59:45', 'cb' ,
30,  30,  30,  30,  30,  30, interval '01:59:45' hour to second, 'cbc', 'Row24'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
30,  30,  30,  30,  30,  30, date '1960-01-01',  'c'  ,
30,  30,  30,  30,  30,  30, time '02:00:00', 'cc' ,
10,  10,  10,  10,  10,  10, interval '02:00:00' hour to second, 'cca', 'Row25'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
30,  30,  30,  30,  30,  30, date '1960-01-01',  'c'  ,
30,  30,  30,  30,  30,  30, time '11:59:00', 'cc' ,
20,  20,  20,  20,  20,  20, interval '11:59:00' hour to second, 'ccb', 'Row26'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
30,  30,  30,  30,  30,  30, date '1960-01-01',  'c'  ,
30,  30,  30,  30,  30,  30, time '11:59:15', 'cc' ,
30,  30,  30,  30,  30,  30, interval '11:59:15' hour to second, 'ccc', 'Row27'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
30,  10,  10,  10,  10,  10, date '1960-01-01',  'a'  ,
30,  10,  10,  10,  10,  10, time '11:59:30', 'ac' ,
40,null,  -1,null,null,null, interval '11:59:30' hour to second, 'aca', 'Row28'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
30,  10,  10,  10,  10,  10, date '1960-01-01',  'a'  ,
40,null,  -1,null,null,null, time '11:59:45', 'aa' ,
30,  10,  10,  10,  10,  10, interval '11:59:45' hour to second, null,  'Row29'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
30,  10,  10,  10,  10,  10, date '1960-01-01',  'a'  ,
40,null,  -1,null,null,null, time '12:00:00', null ,
40,null,  -1,null,null,null, interval '12:00:00' hour to second, 'aaa', 'Row30'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
40,null,  -1,null,null,null, date '1960-01-01',  null ,
30,  10,  10,  10,  10,  10, time '12:00:00', 'aa' ,
30,  10,  10,  10,  10,  10, interval '12:00:00' hour to second, 'aaa', 'Row31'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
40,null,  -2,null,null,null, date '1960-01-01',  'b'  ,
30,  10,  10,  10,  10,  10, time '23:59:15', 'bb' ,
40,  10,  10,  10,  10,  10, interval '23:59:15' hour to second, null , 'Row32'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
40,null,  -1,null,null,null, date '1960-01-01',  'b'  ,
40,  10,  10,  10,  10,  10, time '23:59:30', null ,
30,null,  -1,null,null,null, interval '23:59:30' hour to second, 'bbb', 'Row33'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
40,null,  -1,null,null,null, date '1960-01-01',  null ,
40,null,  -1,null,null,null, time '23:59:45', 'bb' ,
40,  10,  10,  10,  10,  10, interval '23:59:45' hour to second, 'bbb', 'Row34'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
40,null,  -1,null,null,null, date '1960-01-02',  'c'  ,
40,null,  -1,null,null,null, time '00:00:00', 'cc' ,
50,null,  -1,null,null,null, interval '24:00:00' hour to second, null , 'Row35'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """update statistics for table OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index u123 on
 OPTABLE(u1, u2, u3) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index u132 on
 OPTABLE(u1, u3, u2) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index u231 on
 OPTABLE(u2, u3, u1) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index u213 on
 OPTABLE(u2, u1, u3) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index u312 on
 OPTABLE(u3, u1, u2) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index u321 on
 OPTABLE(u3, u2, u1) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """update statistics for table OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """prepare s1 from select min(u1) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain(NULL,'S1'));"""
    output = _dci.cmdexec(stmt)
    #  should use u123 or u132
    
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s1')
    
    stmt = """prepare s1 from select min(u2) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain(NULL,'S1'));"""
    output = _dci.cmdexec(stmt)
    #  should use u231 or u213
    
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s3')
    
    stmt = """prepare s1 from select min(u3) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain(NULL,'S1'));"""
    output = _dci.cmdexec(stmt)
    #  should use u321 or u312
    
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s5')
    
    stmt = """prepare s1 from
select min(u2)
from OPTABLE 
where u1 = 10
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain(NULL,'S1'));"""
    output = _dci.cmdexec(stmt)
    #  should use u123
    
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s7')
    
    stmt = """prepare s1 from
select min(u3)
from OPTABLE 
where u1 = 10
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain(NULL,'S1'));"""
    output = _dci.cmdexec(stmt)
    #  should use u132
    
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s9')
    
    stmt = """prepare s1 from
select min(u3)
from OPTABLE 
where u2 = 10
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain(NULL,'S1'));"""
    output = _dci.cmdexec(stmt)
    #  should use u231
    
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s11')
    
    stmt = """prepare s1 from
select min(u1)
from OPTABLE 
where u2 = 10
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain(NULL,'S1'));"""
    output = _dci.cmdexec(stmt)
    #  should use u213
    
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s13')
    
    stmt = """prepare s1 from
select min(u2)
from OPTABLE 
where u3 = 10
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain(NULL,'S1'));"""
    output = _dci.cmdexec(stmt)
    #  should use u321
    
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s15')
    
    stmt = """prepare s1 from
select min(u1)
from OPTABLE 
where u3 = 10
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain(NULL,'S1'));"""
    output = _dci.cmdexec(stmt)
    #  should use u312
    
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s17')
    
    stmt = """prepare s1 from
select min(p1)
from OPTABLE 
where u1 = 10
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain(NULL,'S1'));"""
    output = _dci.cmdexec(stmt)
    #  should use u123 or u231
    
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s19')
    
    stmt = """prepare s1 from
select min(u3)
from OPTABLE 
where u2 = 10
and c1 is not null
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain(NULL,'S1'));"""
    output = _dci.cmdexec(stmt)
    #  should use u231 or u213
    
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s21')
    # should see 10
    
    stmt = """prepare s1 from
select max(u3)
from OPTABLE 
where u2 = 10
and c1 is not null
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain(NULL,'S1'));"""
    output = _dci.cmdexec(stmt)
    #  should use u231 or u213
    
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s23')
    # should see 30
    
    stmt = """prepare s1 from
select min(u3)
from OPTABLE 
where u2 = 10
and u1 = 10
and c1 is not null
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain(NULL,'S1'));"""
    output = _dci.cmdexec(stmt)
    #  should use u213 or u123
    
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s25')
    # should see 10
    
    stmt = """prepare s1 from
select max(u3)
from OPTABLE 
where u2 = 10
and u1 = 10
and c1 is not null
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain(NULL,'S1'));"""
    output = _dci.cmdexec(stmt)
    #  should use u213 or u123
    
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s27')
    # should see 30
    
    # be clean
    
    stmt = """drop table OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test006(desc="""a10"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:         A10
    #  Description:
    #  Test case inputs:       This test relies on the existence of
    #                          the files OPTTST, =keytest
    #  Test case outputs:
    #  Expected Results:        (provide a high-level description)
    #
    #  Notes:
    #  This test case incorporates features detailed in the "Title"
    #  by Ima Programmer (Version 1.1, <date>).
    #
    # ---------------------------------
    # Open a Log file
    # ---------------------------------
    # ---------------------------------
    #  start with a clean slate
    
    stmt = """drop table OPTABLE;"""
    output = _dci.cmdexec(stmt)
    
    # delete define =T;
    
    # add define =T, class map, file t;
    
    stmt = """create table OPTABLE 
( p1  largeint not null
, u1  smallint unsigned
, zi1 smallint not null
, f1  double precision
, n1  numeric (4,2) unsigned
, d1  decimal (4,2)
, t1  date
, c1  char
, p2  integer not null
, u2  integer unsigned
, zi2 integer not null
, f2  real
, n2  numeric (6,3) unsigned
, d2  decimal (6,3)
, t2  time
, c2  char(2)
, p3  smallint not null
, u3  largeint
, zi3 largeint not null
, f3  float
, n3  numeric (12,4)
, d3  decimal (12,4)
, t3  interval hour to second
, c3  char(3)
, z   char (3800)
, primary key (p1, p2, p3) )
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into OPTABLE values (
10,  10,  10,  10,  10,  10, date '1959-12-31',  'a' ,
9,   9,   9,   9,   9,   9, time '23:59:59', 'aa',
9,null,  -1,null,null,null, null, null, null
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into OPTABLE values (
10,  10,  10,  10,  10,  10, date '1960-01-01', 'a'  ,
10,  10,  10,  10,  10,  10, time '00:00:00', 'aa' ,
10,  10,  10,  10,  10,  10, interval '00:00:00' hour to second, 'aaa', 'Row01'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
10,  10,  10,  10,  10, 10, date '1960-01-01',  'a'  ,
10,  10,  10,  10,  10, 10, time '00:00:15', 'aa' ,
20,  20,  20,  20,  20, 20, interval '00:00:15' hour to second, 'aab', 'Row02'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
10,  10,  10,  10,  10,  10, date '1960-01-01',  'a'  ,
10,  10,  10,  10,  10,  10, time '00:00:30', 'aa' ,
30,  30,  30,  30,  30,  30, interval '00:00:30' hour to second, 'aac', 'Row03'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into OPTABLE values (
10,  10,  10,  10,  10,  10, date '1960-01-01',  'a'  ,
20,  20,  20,  20,  20,  20, time '00:00:45', 'ab' ,
10,  10,  10,  10,  10,  10, interval '00:00:45' hour to second, 'aba', 'Row04'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
10,  10,  10,  10,  10,  10, date '1960-01-01',  'a'  ,
20,  20,  20,  20,  20,  20, time '00:01:00', 'ab' ,
20,  20,  20,  20,  20,  20, interval '00:01:00' hour to second, 'abb', 'Row05'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
10,  10,  10,  10,  10,  10, date '1960-01-01',  'a'  ,
20,  20,  20,  20,  20,  20, time '00:01:15', 'ab' ,
30,  30,  30,  30,  30,  30, interval '00:01:15' hour to second, 'abc', 'Row06'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into OPTABLE values (
10,  10,  10,  10,  10,  10, date '1960-01-01',  'a'  ,
30,  30,  30,  30,  30,  30, time '00:01:30', 'ac' ,
10,  10,  10,  10,  10,  10, interval '00:01:30' hour to second, 'aca', 'Row07'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
10,  10,  10,  10,  10,  10, date '1960-01-01',  'a'  ,
30,  30,  30,  30,  30,  30, time '00:01:45', 'ac' ,
20,  20,  20,  20,  20,  20, interval '00:01:45' hour to second, 'acb', 'Row08'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
10,  10,  10,  10,  10,  10, date '1960-01-01',  'a'  ,
30,  30,  30,  30,  30,  30, time '00:02:00', 'ac' ,
30,  30,  30,  30,  30,  30, null, 'acc', 'Row09'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into OPTABLE values (
20,  20,  20,  20,  20,  20, date '1960-01-01',  'b'  ,
10,  10,  10,  10,  10,  10, null,                               'ba' ,
10,  10,  10,  10,  10,  10, interval '00:02:00' hour to second, 'baa', 'Row10'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
20,  20,  20,  20,  20,  20, date '1960-01-01',  'b'  ,
10,  10,  10,  10,  10,  10, time '00:59:00', 'ba' ,
20,  20,  20,  20,  20,  20, interval '00:59:00' hour to second, 'bab', 'Row11'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
20,  20,  20,  20,  20,  20, date '1960-01-01',  'b'  ,
10,  10,  10,  10,  10,  10, time '00:59:15', 'ba' ,
30,  30,  30,  30,  30,  30, interval '00:59:15' hour to second, 'bac', 'Row12'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
20,  20,  20,  20,  20,  20, date '1960-01-01',  'b'  ,
20,  20,  20,  20,  20,  20, time '00:59:30', 'bb' ,
10,  10,  10,  10,  10,  10, interval '00:59:30' hour to second, 'bba', 'Row13'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
20,  20,  20,  20,  20,  20, date '1960-01-01',  'b'  ,
20,  20,  20,  20,  20,  20, time '00:59:45', 'bb' ,
20,  20,  20,  20,  20,  20, interval '00:59:45' hour to second, 'bbb', 'Row14'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
20,  20,  20,  20,  20,  20, date '1960-01-01',  'b'  ,
20,  20,  20,  20,  20,  20, time '01:00:00', 'bb' ,
30,  30,  30,  30,  30,  30, interval '01:00:00' hour to second, 'bbc', 'Row15'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
20,  20,  20,  20,  20,  20, date '1960-01-01',  'b'  ,
30,  30,  30,  30,  30,  30, time '01:00:00', 'bc' ,
10,  10,  10,  10,  10,  10, null,                               'bca', 'Row16'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
20,  20,  20,  20,  20,  20, date '1960-01-01',  'b'  ,
30,  30,  30,  30,  30,  30, time '01:00:15', 'bc' ,
20,  20,  20,  20,  20,  20, interval '01:00:15' hour to second, 'bcb', 'Row17'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
20,  20,  20,  20,  20,  20, date '1960-01-01',  'b'  ,
30,  30,  30,  30,  30,  30, time '01:00:30', 'bc' ,
30,  30,  30,  30,  30,  30, interval '01:00:30' hour to second, 'bcc', 'Row18'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
30,  30,  30,  30,  30,  30, date '1960-01-01',  'c'  ,
10,  10,  10,  10,  10,  10, time '01:00:45', 'ca' ,
10,  10,  10,  10,  10,  10, interval '01:00:45' hour to second, 'caa', 'Row19'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
30,  30,  30,  30,  30,  30, date '1960-01-01',  'c'  ,
10,  10,  10,  10,  10,  10, null,                               'ca' ,
20,  20,  20,  20,  20,  20, interval '01:01:00' hour to second, 'cab', 'Row20'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
30,  30,  30,  30,  30,  30, date '1960-01-01',  'c'  ,
10,  10,  10,  10,  10,  10, time '01:59:00', 'ca' ,
30,  30,  30,  30,  30,  30, interval '01:59:00' hour to second, 'cac', 'Row21'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
30,  30,  30,  30,  30,  30, date '1960-01-01',  'c'  ,
20,  20,  20,  20,  20,  20, time '01:59:15', 'cb' ,
10,  10,  10,  10,  10,  10, interval '01:59:15' hour to second, 'cba', 'Row22'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
30,  30,  30,  30,  30,  30, date '1960-01-01',  'c'  ,
20,  20,  20,  20,  20,  20, time '01:59:30', 'cb' ,
20,  20,  20,  20,  20,  20, interval '01:59:30' hour to second, 'cbb', 'Row23'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
30,  30,  30,  30,  30,  30, date '1960-01-01',  'c'  ,
20,  20,  20,  20,  20,  20, time '01:59:45', 'cb' ,
30,  30,  30,  30,  30,  30, interval '01:59:45' hour to second, 'cbc', 'Row24'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
30,  30,  30,  30,  30,  30, date '1960-01-01',  'c'  ,
30,  30,  30,  30,  30,  30, time '02:00:00', 'cc' ,
10,  10,  10,  10,  10,  10, interval '02:00:00' hour to second, 'cca', 'Row25'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
30,  30,  30,  30,  30,  30, date '1960-01-01',  'c'  ,
30,  30,  30,  30,  30,  30, time '11:59:00', 'cc' ,
20,  20,  20,  20,  20,  20, interval '11:59:00' hour to second, 'ccb', 'Row26'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
30,  30,  30,  30,  30,  30, date '1960-01-01',  'c'  ,
30,  30,  30,  30,  30,  30, time '11:59:15', 'cc' ,
30,  30,  30,  30,  30,  30, interval '11:59:15' hour to second, 'ccc', 'Row27'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
30,  10,  10,  10,  10,  10, date '1960-01-01',  'a'  ,
30,  10,  10,  10,  10,  10, time '11:59:30', 'ac' ,
40,null,  -1,null,null,null, interval '11:59:30' hour to second, 'aca', 'Row28'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
30,  10,  10,  10,  10,  10, date '1960-01-01',  'a'  ,
40,null,  -1,null,null,null, time '11:59:45', 'aa' ,
30,  10,  10,  10,  10,  10, interval '11:59:45' hour to second, null,  'Row29'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
30,  10,  10,  10,  10,  10, date '1960-01-01',  'a'  ,
40,null,  -1,null,null,null, time '12:00:00', null ,
40,null,  -1,null,null,null, interval '12:00:00' hour to second, 'aaa', 'Row30'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
40,null,  -1,null,null,null, date '1960-01-01',  null ,
30,  10,  10,  10,  10,  10, time '12:00:00', 'aa' ,
30,  10,  10,  10,  10,  10, interval '12:00:00' hour to second, 'aaa', 'Row31'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
40,null,  -2,null,null,null, date '1960-01-01',  'b'  ,
30,  10,  10,  10,  10,  10, time '23:59:15', 'bb' ,
40,  10,  10,  10,  10,  10, interval '23:59:15' hour to second, null , 'Row32'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
40,null,  -1,null,null,null, date '1960-01-01',  'b'  ,
40,  10,  10,  10,  10,  10, time '23:59:30', null ,
30,null,  -1,null,null,null, interval '23:59:30' hour to second, 'bbb', 'Row33'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
40,null,  -1,null,null,null, date '1960-01-01',  null ,
40,null,  -1,null,null,null, time '23:59:45', 'bb' ,
40,  10,  10,  10,  10,  10, interval '23:59:45' hour to second, 'bbb', 'Row34'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
40,null,  -1,null,null,null, date '1960-01-02',  'c'  ,
40,null,  -1,null,null,null, time '00:00:00', 'cc' ,
50,null,  -1,null,null,null, interval '24:00:00' hour to second, null , 'Row35'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """update statistics for table OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # Overlapping range, partial equality key, 1st key only
    stmt = """prepare x from
select p1, p2, p3
from OPTABLE 
where p1 = 20
or p1 = 20                 -- overlaps with previous interval
or p1 = 30
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s2')
    # should get 21 rows
    
    # Overlapping range, identical intervals
    stmt = """prepare x from
select p1, p2, p3
from OPTABLE 
where p1,p2 = 10,10
or p1,p2 = 20,20
or p1,p2 = 10,10           -- overlaps with 1st interval
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s4')
    # should get 6 rows
    
    # Overlapping range    [  (  ]  )
    stmt = """prepare x from
select p1, p2, p3
from OPTABLE 
where p1,p2 between 20,10 and 20,25    -- 10 rows
or p1,p2 between 20,20 and 20,30    -- 10 rows
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s6')
    # should get 9 rows
    
    # Overlapping range    [  ( )  ]
    stmt = """prepare x from
select p1, p2, p3
from OPTABLE 
where p1 between 20 and 30    -- 21 rows
or p1,p2 = 20,20           --  3 rows
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s8')
    # should get 21 rows
    
    stmt = """create index iuaaa on
 OPTABLE(U1 asc, u2 asc, u3 asc) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index inaaa on
 OPTABLE(n1 asc, n2 asc, n3 asc) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create unique index iziaaa 
on OPTABLE (zi1, zi2, zi3) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # update statistics for table t;
    
    # Overlapping range, primary + alternate
    stmt = """prepare x from
select p1,p2,p3
from OPTABLE 
where u1,u2,u3 is null
or zi1 < 0
or p1,p2 > 40,10
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s10')
    # should get 5 rows
    
    # Overlapping range, primary + alternate
    stmt = """prepare x from
select p1,p2,p3
from OPTABLE 
where u1,u2,u3 is null
or n1,n2,n3 is null
or u1,u2    is null and u3 = 10
or n1,n2    is null and n3 = 10
or u1       is null and u2 = 10  and u3 is null
or n1       is null and n2 = 10  and n3 is null
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s12')
    # should get 3 rows
    
    # Overlapping range, primary + alternate
    stmt = """prepare x from
select p1,p2,p3
from OPTABLE 
where u1 = 10 and u2 is null
or n1 = 10 and n2 is null
or u1       is null and u2 between 10 and 20
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s14')
    # should get 5 rows
    
    stmt = """prepare x from
select p1, p2, p3
from OPTABLE 
where n1,n2,n3    > 30,20,20
or u1,u2       > 30,10 and u1,u2 < 30,30
or zi1,zi2,zi3 < 10,10,10
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s16')
    # should get 15 rows
    
    stmt = """drop table OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test007(desc="""a11"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:         A11
    #  Description:
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:        (provide a high-level description)
    #
    #  Notes:
    #  This test case incorporates features detailed in the "Title"
    #  by Ima Programmer (Version 1.1, <date>).
    #
    # =================== End Test Case Header  ===================
    stmt = """create table otab1 (a int,
b int,
c int,
d int) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #                 catalog
    
    # insert 14 rows ( 7 distinct rows)
    stmt = """insert into otab1 values (0,0,0,0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into otab1 values (0,0,0,0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into otab1 values (0,0,0,1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into otab1 values (0,0,0,1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into otab1 values (0,0,1,1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into otab1 values (0,0,1,1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into otab1 values (0,1,1,1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into otab1 values (0,1,1,1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into otab1 values (1,1,1,1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into otab1 values (1,1,1,1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into otab1 values (1,null,1,null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into otab1 values (1,null,1,null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into otab1 values (null,null,null,null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into otab1 values (null,null,null,null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # setup tables for merge join tests (dml5)
    
    stmt = """create table mjtab1 (a int) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #       catalog
    
    stmt = """create table mjtab2 (b int) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #       catalog
    
    stmt = """create table mjtab3 (c int) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #       catalog
    
    stmt = """insert into mjtab1 values (1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mjtab1 values (3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mjtab2 values (1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mjtab3 values (0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mjtab3 values (1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """update statistics for table mjtab1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """update statistics for table mjtab2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """update statistics for table mjtab3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #update basetabs set rowcount = 1000 where tablename like '%MJTAB1%';
    #update basetabs set rowcount = 1000 where tablename like '%MJTAB2%';
    #update basetabs set rowcount = 1000 where tablename like '%MJTAB3%';
    
    # control query shape sort(merge_join(cut,cut));
    
    # Testing Optimizer Enhancement #1:
    #   Order By list should be merged into Group By List if it is completely
    #   contained in the Group By List.
    
    stmt = """prepare s1 from select a,b,c,d from otab1 group by a,b,c,d
order by 1,2,3,4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain(NULL,'S1'));"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s1')
    # should return 7 rows order by a,b,c,d
    
    # specify column names instead of numbers (order should be according
    # to ORDER BY list
    stmt = """prepare s1a from select a,b,c,d from otab1 group by a,b,c,d
order by a,b,d,c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain(NULL,'S1A'));"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s3')
    # should return 7 rows order by a,b,d,c
    
    stmt = """prepare s2 from select a,b,c,d from otab1 group by a,b,c,d
order by 4 desc, 2, 3 desc, 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain(NULL,'S2'));"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s5')
    # should return 7 rows order by d desc, b, c desc, a
    
    stmt = """prepare s2a from select a,b,c,d from otab1 group by a,b,c,d
order by d desc, b, c desc, a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain(NULL,'S2A'));"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s2a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s7')
    # should return 7 rows in same order
    
    stmt = """prepare s3 from select a,b,c,d from otab1 group by a,b,c,d
order by 2, 3 desc, 4 desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain(NULL,'S3'));"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s9')
    # should return 7 rows ordered by b, c desc, d desc
    
    stmt = """prepare s3a from select a,b,c,d from otab1 group by a,b,c,d
order by b, c desc, d desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain(NULL,'S3A'));"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s3a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s11')
    # should return 7 rows in same order
    
    # The following order by list cannot be eliminated
    stmt = """prepare s4 from select a,b,c, count(*) from otab1 group by a,b,c
order by 3 desc, 4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain(NULL,'S4'));"""
    output = _dci.cmdexec(stmt)
    #  should get two sorts
    stmt = """execute s4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s13')
    # should get 6 rows, count = 2 for all rows but 1
    
    stmt = """prepare s4a from select a,b,c, count(*) from otab1 group by a,b,c
order by 3 desc, 4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain(NULL,'S4A'));"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s4a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s15')
    # should get 6 rows, count = 2 for all rows but 1
    
    # Testing Optimizer Enhancement #2:
    #   Order By List should be eliminated since Group By List
    #   occurs among the first N items of the Order By List.
    #   Group By list should be modified to preserve the position
    #   and asc/desc information in the order by list.
    
    stmt = """prepare s1 from select a,b,c, count(*), sum(a) from otab1 group by a,b,c
order by 1,2,3,4,5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain(NULL,'S1'));"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s17')
    
    stmt = """prepare s2 from select a,b,c, count(*), sum(a) from otab1 group by a,b,c
order by 1,3 desc, 2, 5,4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain(NULL,'S2'));"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s19')
    
    # Specifying DESC on aggregate column is unecessary and should be eliminated.
    stmt = """prepare s3 from select a,b,c, count(*), sum(a) from otab1 group by a,b,c
order by 1,2,3,4 desc,5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain(NULL,'S3'));"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s21')
    
    stmt = """prepare s4 from select a,b,c, count(*), sum(a) from otab1 group by a,b,c
order by 1,2 desc,3,4 desc,5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain(NULL,'S4'));"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s23')
    
    stmt = """prepare s5 from select a,b,count(*), a+b from otab1 group by a,b
order by 1,2 desc,3,4 desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain(NULL,'S5'));"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s25')
    
    # Can't merge the order by list in the following query.
    #   Group By list is not the first N items of the Order By list.
    stmt = """prepare s6 from select a,b,c, count(*), sum(a) from otab1 group by a,b,c
order by 3 desc, 2, 4, 1, 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain(NULL,'S6'));"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s27')
    
    # Testing Optimizer Modification #3:
    #   DISTINCT can be eliminated if GROUP BY list is contained
    #   in the SELECT list.
    stmt = """prepare s1 from select distinct a,b,c,d from otab1 group by a,b,c,d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain(NULL,'S1'));"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s29')
    
    stmt = """prepare s2 from select distinct a,b,sum(a), a+b from otab1 group by a,b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain(NULL,'S2'));"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s31')
    
    # Try this with column numbers just to verify the same behaviour
    stmt = """prepare s3 from select distinct a,b,sum(a), a+b from otab1 group by a,b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain(NULL,'S3'));"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s33')
    
    stmt = """prepare s4 from select distinct a,b,c,d from otab1 group by b,a,d,c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """Select SEQ_NUM, OPERATOR,
TOTAL_COST from table (explain(NULL,'S4'));"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s35')
    
    # distinct should not be eliminated in this case
    stmt = """prepare s4 from select distinct a,b,sum(a) from otab1 group by a,b,c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain(NULL,'S4'));"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s37')
    
    # Should show 1 sort on a desc and b desc
    stmt = """prepare s5 from select distinct a,b,sum(a) from otab1 group by a,b
having sum(a) >= 0 order by a desc, b desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain(NULL,'S5'));"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s39')
    
    # Now, remove the distinct
    stmt = """prepare s6 from select a,b,sum(a) from otab1 group by a,b
having sum(a) >= 0
order by a desc, b desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    # explain s6;
    
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain(NULL,'S6'));"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s41')
    
    # Now, remove the having clause (again, no problem)
    stmt = """prepare s7 from select distinct a,b,sum(a) from otab1 group by a,b
order by a desc, b desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain(NULL,'S7'));"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s7;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s43')
    
    stmt = """prepare s8 from select distinct a,b,sum(a) from otab1 group by a,b
having sum(b) is null order by a desc, b desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain(NULL,'S8'));"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s8;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s45')
    
    stmt = """prepare s9 from select distinct t1.a, t1.b, t2.a, t2.b, count(*)
from otab1 t1 ,otab1 t2 where t1.a=t2.a group by t1.a, t1.b, t2.a, t2.b
having count(*) > 0  order by t1.a desc, t1.b desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain(NULL,'S9'));"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s9;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s47')
    
    # Testing Optimizer Modification #4:
    #   SELECT DISTINCT with no aggregate, group by, nor having clause
    #   should be converted into a select with group by
    
    stmt = """prepare s1 from select distinct a,b,c,d from otab1 where a >= 0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain(NULL,'S1'));"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s49')
    
    stmt = """prepare s2 from select distinct a,b,c from otab1 where (a,b) > (0,0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain(NULL,'S2'));"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s51')
    
    stmt = """prepare s3 from select distinct t1.a, t1.b, t2.a, t2.b
from otab1 t1, otab1 t2 where t1.a = t2.a order by t1.a, t1.b desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain(NULL,'S3'));"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s53')
    
    stmt = """prepare s4 from select distinct t1.a, t1.b, t2.a, t2.b from
 otab1 t1 left join otab1 t2 on t1.a = t2.b order by t1.a, t1.b desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain(NULL,'S4'));"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s55')
    
    stmt = """prepare s5 from select distinct t1.a, t2.a, count(*) from
 otab1 t1 left join otab1 t2 on t1.a = t2.b group by t1.a, t2.a
order by t1.a, t2.a desc, 3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain(NULL,'S5'));"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s57')
    
    # Testing Optimizer Modification #5:
    #   Test different merge join plans.
    #   Should eliminate unecessary SORTs.
    
    stmt = """prepare s1 from select * from mjtab1 t1 left join mjtab2 t2
on (t1.a = t2.b)
left join mjtab3 t3 on (t2.b = t3.c)
left join mjtab1 t4 on (t2.b = t4.a);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain(NULL,'S1'));"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s59')
    # Should return 2 rows: (1,1,1,1) and (3,?,?,?)
    
    # Try reversing predicates for sanity check
    #   Should still preserve the same order
    stmt = """prepare s2 from select * from mjtab1 t1 left join mjtab2 t2
on (t2.b = t1.a)
left join mjtab3 t3 on (t3.c = t2.b)
left join mjtab1 t4 on (t2.b = t4.a) order by t1.a desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain(NULL,'S2'));"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s61')
    
    # This last order by SORT should be eliminated
    stmt = """prepare s3 from select * from mjtab1 t1 left join mjtab2 t2
on (t2.b = t1.a)
left join mjtab3 t3 on (t3.c = t2.b)
left join mjtab1 t4 on (t2.b = t4.a) order by t2.b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain(NULL,'S3'));"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s63')
    
    # Now, try changing the outer join to inner join.
    # Optimizer now chooses nested join.  Note the alarming cost!
    stmt = """prepare s4 from select * from mjtab1 t1 left join mjtab2 t2 on (t1.a=t2.b)
inner join mjtab3 t3 on (t2.b = t3.c)
inner join mjtab1 t4 on (t2.b = t4.a) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain(NULL,'S4'));"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s65')
    
    # Let's try a simpler case.  Two table joins.
    # Same behaviour.
    stmt = """prepare s5 from select * from mjtab1 t1 left join mjtab2 t2
on (t1.a = t2.b) inner join mjtab3 t3 on (t2.b = t3.c) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain(NULL,'S5'));"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s67')
    # Should return 1 row : (1,1,1,1)
    
    # try outer join with cartesian product
    stmt = """prepare s6 from
select * from mjtab1 t1
left join
 mjtab2 t2 on (t1.a = t2.b),
 mjtab3 t3
order by t3.c, t2.b desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain(NULL,'S6'));"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s69')
    # Should return 4 rows:  (3,?,0) (1,1,0) (3,?,1) (1,1,1)
    
    # combination of outer join, cartesian products
    stmt = """prepare s7 from
select * from (mjtab1 t1
left join
 mjtab2 t2 on a=b),
(mjtab1 t3
left join mjtab2 t4 on b=a)
order by t1.a, t2.b, t3.a, t4.b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain(NULL,'S7'));"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s7;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s71')
    # Should return 4 rows: (1,1,1,1) (1,1,3,?) (3,?,1,1) (3,?,3,?)
    
    # OUTSTANDING PROBLEM. FOLLOWING QUERY CURRENTLY RETURNS WRONG PLAN.
    # Combination of outer join, cartesian product, and inner join.
    #
    stmt = """prepare s8 from
select * from mjtab1 t1 left join mjtab2 t2 on a=b,
 mjtab1 inner join mjtab2 on b=a
order by t1.a desc, t2.b desc ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain(NULL,'S8'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute s8;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s73')
    #  Should return 2 rows: (3,?,1,1) (1,1,1,1)
    
    stmt = """drop index otkey1;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """drop index otkey2;"""
    output = _dci.cmdexec(stmt)
    
    # testing with keys
    
    #create index otkey1 on otab1 (a, b, c) catalog SQLQA.SCH;
    stmt = """create index otkey1 on otab1 (a, b, c);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #create index otkey2 on otab1 (a, b desc, c) catalog SQLQA.SCH;
    stmt = """create index otkey2 on otab1 (a, b desc, c);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # should use index OTKEY1
    stmt = """prepare s1 from select a,b,c,count(*) from otab1 group by a,b,c
order by 1,2,3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain(NULL,'S1'));"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s77')
    
    # Now add the aggregate column to the ORDER BY list.
    # Should still use the same access plan as the last query.
    stmt = """prepare s2 from select a,b,c,count(*) from otab1 group by a,b,c
order by 1,2,3,4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain(NULL,'S2'));"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s79')
    
    # Should still use the same access plan.
    stmt = """prepare s3 from select a,b,c,count(*) from otab1 group by a,b,c
order by 1 desc,3 desc,2 desc,4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain(NULL,'S3'));"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s81')
    
    # testing with subqueries
    
    # The following queries use the in-memory B-tree sort.
    stmt = """prepare s1 from select * from mjtab1 where a in
(select sum(a) from mjtab1 group by a);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain(NULL,'S1'));"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s83')
    
    # Currently, we still choose in-memory B-Tree sort for subquery, even though
    # subquery returns exactly 1 value.
    stmt = """prepare s2 from select * from mjtab1 where a in
(select sum(a) from mjtab1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain(NULL,'S2'));"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """drop table otab1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table mjtab1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table mjtab2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table mjtab3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test008(desc="""a12"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:         A12
    #  Description:
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:        (provide a high-level description)
    #
    #  Notes:
    #  This test case incorporates features detailed in the "Title"
    #  by Ima Programmer (Version 1.1, <date>).
    #
    stmt = """drop table tree;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table tree (a int) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into tree values (10);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # update all statistics for table tree;
    stmt = """update statistics for table tree;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #  update basetabs set rowcount = 100000 where tablename like '%TREE%';
    
    #  control query shape sort(merge_join(cut,cut));
    
    stmt = """select * from tree where
a in (select * from tree) or
a in (select * from tree) or
a in (select * from tree);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s1')
    
    stmt = """drop table ptiletab;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table ptiletab (a largeint not null,
b pic s9(6)v9(3) comp default -999999.999 not null) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into ptiletab values (6,5.807);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select a, b from ptiletab group by a, b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s3')
    
    stmt = """create table tabor (a int not null,
b int not null,
primary key (a,b));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #catalog ;
    
    stmt = """insert into tabor values (3,4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    # EXPLAIN SELECT *
    #         FROM tabor
    #         WHERE a,b > 1,2+0 OR a,b > 1,2;
    stmt = """prepare s from
select * from tabor where a,b > 1,2+0 OR a,b > 1,2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select seq_num, operator, total_cost
from table (explain(null, 'S'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s5')
    
    stmt = """create table dformat (a timestamp) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into dformat values (null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """select dateformat (a, usa) from dformat;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s6')
    
    stmt = """create table \"unsigned\" (a int unsigned) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into \"unsigned\" values (3000000000);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """select * from \"unsigned\";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s7')
    stmt = """select * from \"unsigned\" where a < 0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """drop table tree;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table ptiletab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table tabor;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table \"unsigned\";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table dformat;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

