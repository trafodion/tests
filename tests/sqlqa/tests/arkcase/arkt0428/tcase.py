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
    #  Test case name:         A03
    #  Description:            Bug fixes.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:        (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    
    stmt = """drop table t;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table tab_t (a char(2) NOT NULL,
PRIMARY key (a));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """insert into tab_t values ('ab');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    #  should return one row
    stmt = """select * from tab_t where
a <= (select 'ab ' from tab_t);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s1')
    
    stmt = """drop table tab_t;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create table tab_t (a int NOT NULL, b int,
PRIMARY key (a));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """insert into tab_t values (1,0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """prepare updt from
update tab_t 
set b = 0
where a = 0 or a = 1 or a = 0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain (null, 'UPDT'));"""
    output = _dci.cmdexec(stmt)
    
    # should show '1 row updated'
    stmt = """update tab_t set b = 0 where a = 0 or a = 1 or a = 0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    # should show '1 row deleted'
    stmt = """delete from tab_t where a = 0 or a = 1 or a = 0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    stmt = """insert into tab_t values (1,0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    # should show '1 row updated'
    stmt = """update tab_t set b = 0 where a = 1 or a = 0 or a = 0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    # should show '1 row deleted'
    stmt = """delete from tab_t where a = 1 or a = 0 or a = 0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    stmt = """insert into tab_t values (1,0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    # should show '1 row updated'
    stmt = """update tab_t set b = 0 where a = 0 or a = 0 or a = 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    # should show '1 row deleted'
    stmt = """delete from tab_t where a = 0 or a = 0 or a = 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    stmt = """drop table tab_t;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create table tab_t (a numeric (9,6), b numeric (9,6)) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """insert into tab_t values (3.111113, 3.311113);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select * from tab_t;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s3')
    
    stmt = """drop table tab_t;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create table tab_t (a int NOT NULL,
PRIMARY key (a));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """insert into tab_t values (1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tab_t values (2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # should not return any rows
    stmt = """select * from tab_t where a =
(select * from tab_t where a = 0 or a = 0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    # should not return any rows
    stmt = """select * from tab_t where a =
(select * from tab_t where a = 0 or a > 2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    # should not return any rows
    stmt = """select * from tab_t where a =
(select * from tab_t where a > 2 or a = 0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    # should not return any rows
    stmt = """select * from tab_t where a
= (select * from tab_t where a < 1 or a > 2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    #  should return 1 row
    stmt = """select * from tab_t where a =
(select * from tab_t where a = 1 or a = 0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s4')
    
    #  should return 1 row
    stmt = """select * from tab_t where a =
(select * from tab_t where a = 0 or a = 1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s5')
    
    #  should return 1 row
    stmt = """select * from tab_t where a =
(select * from tab_t where a = 0 or a <= 1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s6')
    
    #  should return 1 row
    stmt = """select * from tab_t where a =
(select * from tab_t where a  <= 1 or a = 0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s7')
    
    stmt = """select * from tab_t where a =
(select * from tab_t where a = 1 or a = 2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8401')
    
    stmt = """select * from tab_t where a =
(select * from tab_t where a = 1 or a >= 2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8401')
    
    stmt = """select * from tab_t where a =
(select * from tab_t where a <= 1 or a = 2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8401')
    
    stmt = """select * from tab_t where a =
(select * from tab_t where a <= 1 or a >= 2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8401')
    
    # should not return any rows
    stmt = """select * from tab_t where a =
(select * from tab_t where a = 0 or a = 0
union all
select * from tab_t where a = 0 or a = 0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    #  should return 1 row
    stmt = """select * from tab_t where a =
(select * from tab_t where a = 1 or a = 0
union all
select * from tab_t where a = 0 or a = 0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s12')
    
    #  should return 1 row
    stmt = """select * from tab_t where a =
(select * from tab_t where a = 0 or a = 0
union all
select * from tab_t where a <= 1 or a = 0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s13')
    
    stmt = """select * from tab_t where a =
(select * from tab_t where a = 0 or a = 1
union all
select * from tab_t where a <= 1 or a = 0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8401')
    
    stmt = """drop table tab_t;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create table tab_t (a pic 9(3)  NOT NULL,
b pic x(11) NOT NULL,
c pic x(2)  NOT NULL,
PRIMARY key (a,b,c));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """insert into tab_t values (0, 'a', '10');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    #  should return   'a  10'
    stmt = """select distinct b,c from tab_t;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s15')
    
    # error message should show 'format' instead of 'syntax'
    stmt = """drop table tab_t;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create table tab_t (a date) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """insert into tab_t values (DATE 'abc');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3045')
    
    stmt = """set param ?p 'abc';"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab_t values (?p);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    stmt = """drop table tab_t;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test002(desc="""a02"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:         A02
    #  Description:            Order by ASC
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:        (provide a high-level ascription)
    #
    # =================== End Test Case Header  ===================
    
    stmt = """create table tab_a 
(c1 int unsigned no default not null,
c2 char(8) no default not null,
c3 char(5) no default not null,
primary key (c1));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into tab_a values (1,'c2', 'c3');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tab_a values (2,'c2', 'c3');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tab_a values (3,'c2', 'c3');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tab_a values (4,'c2', 'c3');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tab_a values (5,'c2', 'c3');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """create table tab_b 
(d1 int unsigned no default not null,
d2 char(8) no default not null,
d3 char(5) no default not null,
primary key (d1,d2));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #		organization k;
    #                catalog
    
    stmt = """insert into tab_b values (1,'d2', 'd3');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tab_b values (2,'d2', 'd3');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tab_b values (3,'d2', 'd3');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tab_b values (4,'d2', 'd3');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """create table kmergx 
(a int no default not null,
b int no default not null,
c int no default not null,
primary key (a,b,c));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #			organization k;
    #                     catalog
    
    stmt = """insert into kmergx values (0,0,0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into kmergx values (1,1,1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into kmergx values (2,2,2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into kmergx values (3,3,3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into kmergx values (4,4,4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """update statistics for table tab_a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """update statistics for table tab_b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """update statistics for table kmergx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # update basetabs set rowcount = 1000000
    stmt = """prepare s1 from
select tab_a.c1, tab_b.d1
from tab_a,tab_b 
where tab_a.c1 = tab_b.d1
order by tab_a.c1 asc ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain (null, 'S1'));"""
    output = _dci.cmdexec(stmt)
    
    #  Should not do additional sort for the order by
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s1')
    # Should return 4 rows ascending
    
    stmt = """prepare s2 from
select tab_a.c1, tab_b.d1
from tab_a,tab_b 
where tab_a.c1 = tab_b.d1
order by tab_b.d1 asc ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain (null, 'S2'));"""
    output = _dci.cmdexec(stmt)
    
    #  Should not do additional sort for the order by
    stmt = """execute s2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s3')
    # Should return 4 rows ascending
    
    stmt = """prepare s3 from
select tab_a.c1, tab_b.d1
from tab_a,tab_b 
where tab_a.c1 = tab_b.d1
order by tab_a.c1 asc, tab_a.c2 asc ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain (null, 'S3'));"""
    output = _dci.cmdexec(stmt)
    
    #  Should not do additional sort for the order by
    stmt = """execute s3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s5')
    # Should return 4 rows ascending
    
    stmt = """prepare s4 from
select tab_a.c1, tab_b.d1
from tab_a,tab_b 
where tab_a.c1 = tab_b.d1
order by tab_b.d1 asc, tab_b.d2 asc ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain (null, 'S4'));"""
    output = _dci.cmdexec(stmt)
    #  Should do additional sort for the order by
    stmt = """execute s4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s7')
    
    # NOW, FOR OUTER JOINS
    stmt = """prepare s5 from
select tab_a.c1, tab_b.d1
from tab_a left join tab_b 
on tab_a.c1 = tab_b.d1
order by tab_a.c1 asc ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain (null, 'S5'));"""
    output = _dci.cmdexec(stmt)
    
    #  No sort necessary for ORDER BY
    stmt = """execute s5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s9')
    
    stmt = """prepare s6 from
select tab_a.c1, tab_b.d1
from tab_a left join tab_b 
on tab_a.c1 = tab_b.d1
order by tab_a.c1 asc ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain (null, 'S6'));"""
    output = _dci.cmdexec(stmt)
    
    #  No sort necessary for ORDER BY
    stmt = """execute s6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s11')
    
    stmt = """prepare s7 from
select tab_a.c1, tab_b.d1
from tab_a left join tab_b 
on tab_a.c1 = tab_b.d1
order by tab_b.d1 asc ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain (null, 'S7'));"""
    output = _dci.cmdexec(stmt)
    
    #  Sort needed for ORDER BY
    stmt = """execute s7;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s13')
    
    # Testing some merge join fixes
    stmt = """prepare s1 from select x.a, x.b from kmergx x
inner join kmergx y
on x.a = y.b order by 1 asc, 2 asc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain (null, 'S1'));"""
    output = _dci.cmdexec(stmt)
    
    #  Should not perform additional sort for the ORDER BY
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s15')
    
    stmt = """create index ikmerg on kmergx (b asc);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # Following query caused executor internal error in S03.
    # Problem due to the fact join orders (ASC) information was not relevant.
    # Therefore, two tables of a merge join might be in different orders.
    stmt = """prepare s2 from select x.a, x.b from kmergx x
inner join kmergx y
on x.b = y.a order by x.b asc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain (null, 'S2'));"""
    output = _dci.cmdexec(stmt)
    
    #  S03 version produced internal error here.
    stmt = """execute s2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s17')
    
    stmt = """drop table tab_t;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """Create table tab_t ( a int, b int not null, primary key (b));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into tab_t values (0,0),(1,1),(2,2),(3,3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 4)
    
    stmt = """select a from tab_t order by b desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s19')
    
    stmt = """drop table tab_a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table tab_b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table kmergx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table tab_t;"""
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
    #  Test case name:         A03
    #  Description:
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:        (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    
    stmt = """drop table tab_t;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table tab_t (a int) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """select converttimestamp(a) from tab_t;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """drop table tab_t;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # create table tab_t (y_to_m datetime year to minute);
    stmt = """create table tab_t (y_to_m timestamp) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from tab_t where y_to_m in
(select y_to_m from tab_t 
where y_to_m < timestamp '1991-05-27 00:00:00');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    #    where y_to_m < DATE '1991-05-27');
    
    # should return the column name without downshifting 'X'
    stmt = """drop table tab_t;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table tab_t(ABCDEFGHIJKLMNOPQRSTUVWXYZ DATE) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # insert into tab_t values (current);
    stmt = """insert into tab_t values (current_date);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """select * from tab_t;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s1')
    
    # should not return error 7003 from SQLCOMP
    
    stmt = """drop table tab_t;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create table tab_t (a int) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """prepare s1 from
select * from tab_t where ?,?,?,?,?,?,?,?,?,? = 0,0,0,0,0,0,0,0,0,0 and
?,?,?,?,?,?,?,?,?,? = 0,0,0,0,0,0,0,0,0,0 and
?,?,?,?,?,?,?,?,?,? = 0,0,0,0,0,0,0,0,0,0 and
?,?,?,?,?,?,?,?,?,? = 0,0,0,0,0,0,0,0,0,0 and
?,?,?,?,?,?,?,?,?,? = 0,0,0,0,0,0,0,0,0,0 and
?,?,?,?,?,?,?,?,?,? = 0,0,0,0,0,0,0,0,0,0 and
?,?,?,?,?,?,?,?,?,? = 0,0,0,0,0,0,0,0,0,0 and
?,?,?,?,?,?,?,?,?,? = 0,0,0,0,0,0,0,0,0,0 and
?,?,?,?,?,?,?,?,?,? = 0,0,0,0,0,0,0,0,0,0 and
?,?,?,?,?,?,?,?,?,? = 0,0,0,0,0,0,0,0,0,0 and
?,?,?,?,?,?,?,?,?,? = 0,0,0,0,0,0,0,0,0,0 and
?,?,?,?,?,?,?,?,?,? = 0,0,0,0,0,0,0,0,0,0 and
?,?,?,?,?,?,?,?,?,? = 0,0,0,0,0,0,0,0,0,0 and
?,?,?,?,?,?,?,?,?,? = 0,0,0,0,0,0,0,0,0,0 and
?,?,?,?,?,?,?,?,?,? = 0,0,0,0,0,0,0,0,0,0 and
?,?,?,?,?,?,?,?,?,? = 0,0,0,0,0,0,0,0,0,0 and
?,?,?,?,?,?,?,?,?,? = 0,0,0,0,0,0,0,0,0,0 and
?,?,?,?,?,?,?,?,?,? = 0,0,0,0,0,0,0,0,0,0 and
?,?,?,?,?,?,?,?,?,? = 0,0,0,0,0,0,0,0,0,0 and
?,?,?,?,?,?,?,?,?,? = 0,0,0,0,0,0,0,0,0,0 and
?,?,?,?,?,?,?,?,?,? = 0,0,0,0,0,0,0,0,0,0 and
?,?,?,?,?,?,?,?,?,? = 0,0,0,0,0,0,0,0,0,0 and
?,?,?,?,?,?,?,?,?,? = 0,0,0,0,0,0,0,0,0,0 and
?,?,?,?,?,?,?,?,?,? = 0,0,0,0,0,0,0,0,0,0 and
?,?,?,?,?,?,?,?,?,? = 0,0,0,0,0,0,0,0,0,0 and
?,?,?,?,? = 0,0,0,0,0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # should not return executor internal error.
    
    stmt = """drop table tab_t;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create table tab_t(a int NOT NULL,
b int NOT NULL,
c int NOT NULL,
primary key (a,b,c));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """insert into tab_t values (0,0,-2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """prepare s from select * from
 tab_t where a,b=0,0 and c<-2.5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    #  plan uses primary index
    
    stmt = """select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain (null, 'S'));"""
    output = _dci.cmdexec(stmt)
    
    # should not return row where c = -2
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """prepare s from select a,b,c from
 tab_t where a,b=0,0 and c>=-2.5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain (null, 'S'));"""
    output = _dci.cmdexec(stmt)
    
    #  should return row where c = -2
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s4')
    
    #should return a row
    
    stmt = """drop table tab_t;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create table tab_t (a pic 9(1)) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into tab_t values (0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select * from tab_t;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s5')
    
    stmt = """drop table tab_t;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create table tab_t (a pic S9(18)) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into tab_t values (0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select * from tab_t;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s6')
    
    #  DISPLAY STATISTICS should show '1 Records accessed and Used' for both
    #  tables T1 and T2.
    
    stmt = """drop table t1;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table t2;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table t1 (a int NOT NULL,
PRIMARY key (a));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create table t2 (a int NOT NULL,
PRIMARY key (a));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into t1 values (0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t2 values (0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """prepare s from
select * from t1 where t1.a
= (select * from t2 
where t2.a = t1.a);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain (null, 'S'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select * from t1 where t1.a
= (select * from t2 where
 t2.a = t1.a);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s10')
    
    stmt = """drop table tab_t;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create table tab_t (a char(2) NOT NULL,
PRIMARY key (a));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """insert into tab_t values ('ab');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    #  should return one row
    stmt = """select * from tab_t where
a <= (select 'ab ' from tab_t);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s11')
    
    stmt = """drop table tab_t;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create table tab_t (a int NOT NULL,
b int,
PRIMARY key (a));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """insert into tab_t values (1,0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """prepare s from
update tab_t 
set b = 0 where a = 0 or a = 1 or a = 0 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain (null, 'S'));"""
    output = _dci.cmdexec(stmt)
    
    # should show '1 row updated'
    stmt = """update tab_t set b = 0 where a = 0 or a = 1 or a = 0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    # should show '1 row deleted'
    stmt = """delete from tab_t where a = 0 or a = 1 or a = 0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    stmt = """insert into tab_t values (1,0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    # should show '1 row updated'
    stmt = """update tab_t set b = 0 where a = 1 or a = 0 or a = 0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    # should show '1 row deleted'
    stmt = """delete from tab_t where a = 1 or a = 0 or a = 0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    stmt = """insert into tab_t values (1,0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    # should show '1 row updated'
    stmt = """update tab_t set b = 0 where a = 0 or a = 0 or a = 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    # should show '1 row deleted'
    stmt = """delete from tab_t where a = 0 or a = 0 or a = 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    stmt = """drop table tab_t;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create table tab_t (a numeric (9,6), b numeric (9,6)) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """insert into tab_t values (3.111113, 3.311113);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    #  set list_count 0;
    stmt = """select * from tab_t;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s13')
    
    stmt = """drop table tab_t;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create table tab_t (a int NOT NULL,
PRIMARY key (a));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """insert into tab_t values (1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tab_t values (2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # should not return any rows
    stmt = """select * from tab_t where a =
(select * from tab_t where a = 0 or a = 0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    # should not return any rows
    stmt = """select * from tab_t where a =
(select * from tab_t where a = 0 or a > 2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    # should not return any rows
    stmt = """select * from tab_t where a =
(select * from tab_t where a > 2 or a = 0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    # should not return any rows
    stmt = """select * from tab_t where a
= (select * from tab_t where a < 1 or a > 2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    #  should return 1 row
    stmt = """select * from tab_t where a =
(select * from tab_t where a = 1 or a = 0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s14')
    
    #  should return 1 row
    stmt = """select * from tab_t where a =
(select * from tab_t where a = 0 or a = 1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s15')
    
    #  should return 1 row
    stmt = """select * from tab_t where a =
(select * from tab_t where a = 0 or a <= 1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s16')
    
    #  should return 1 row
    stmt = """select * from tab_t where a =
(select * from tab_t where a  <= 1 or a = 0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s17')
    
    stmt = """select * from tab_t where a =
(select * from tab_t where a = 1 or a = 2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8401')
    
    stmt = """select * from tab_t where a =
(select * from tab_t where a = 1 or a >= 2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8401')
    
    stmt = """select * from tab_t where a =
(select * from tab_t where a <= 1 or a = 2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8401')
    
    stmt = """select * from tab_t where a =
(select * from tab_t where a <= 1 or a >= 2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8401')
    
    # should not return any rows
    stmt = """select * from tab_t where a =
(select * from tab_t where a = 0 or a = 0
union all
select * from tab_t where a = 0 or a = 0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    #  should return 1 row
    stmt = """select * from tab_t where a =
(select * from tab_t where a = 1 or a = 0
union all
select * from tab_t where a = 0 or a = 0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s22')
    
    #  should return 1 row
    stmt = """select * from tab_t where a =
(select * from tab_t where a = 0 or a = 0
union all
select * from tab_t where a <= 1 or a = 0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s23')
    
    stmt = """select * from tab_t where a =
(select * from tab_t where a = 0 or a = 1
union all
select * from tab_t where a <= 1 or a = 0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8401')
    
    stmt = """drop table tab_t;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create table tab_t (a pic 9(3)  NOT NULL,
b pic x(11) NOT NULL,
c pic x(2)  NOT NULL,
PRIMARY key (a,b,c));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """insert into tab_t values (0, 'a', '10');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    #  should return   'a  10'
    stmt = """select distinct b,c from tab_t;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s25')
    
    # error message should show 'format' instead of 'syntax'
    
    stmt = """drop table tab_t;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create table tab_t (a date) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """insert into tab_t values (DATE 'abc');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3045')
    
    stmt = """set param ?p 'abc';"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab_t values (?p);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    stmt = """drop table tab_t;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table t1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table t2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test004(desc="""a04"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:         A04
    #  Description:            Order by DESC
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:        (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    
    stmt = """create table tab_a 
(c1 int unsigned no default not null,
c2 char(8) no default not null,
c3 char(5) no default not null,
primary key (c1));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into tab_a values (1,'c2', 'c3');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tab_a values (2,'c2', 'c3');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tab_a values (3,'c2', 'c3');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tab_a values (4,'c2', 'c3');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tab_a values (5,'c2', 'c3');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """create table tab_b 
(d1 int unsigned no default not null,
d2 char(8) no default not null,
d3 char(5) no default not null,
primary key (d1,d2));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #		 organization k;
    #                catalog
    
    stmt = """insert into tab_b values (1,'d2', 'd3');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tab_b values (2,'d2', 'd3');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tab_b values (3,'d2', 'd3');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tab_b values (4,'d2', 'd3');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """create table kmergx 
(a int no default not null,
b int no default not null,
c int no default not null,
primary key (a,b,c));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #			organization k;
    #                     catalog
    
    stmt = """insert into kmergx values (0,0,0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into kmergx values (1,1,1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into kmergx values (2,2,2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into kmergx values (3,3,3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into kmergx values (4,4,4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """update statistics for table tab_a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """update statistics for table tab_b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """update statistics for table kmergx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # update basetabs set rowcount = 1000000
    stmt = """prepare s1 from
select tab_a.c1, tab_b.d1
from tab_a,tab_b 
where tab_a.c1 = tab_b.d1
order by tab_a.c1 desc ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain (null, 'S1'));"""
    output = _dci.cmdexec(stmt)
    
    #  Should not do additional sort for the order by
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s1')
    # Should return 4 rows descending
    
    stmt = """prepare s2 from
select tab_a.c1, tab_b.d1
from tab_a,tab_b 
where tab_a.c1 = tab_b.d1
order by tab_b.d1 desc ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain (null, 'S2'));"""
    output = _dci.cmdexec(stmt)
    
    #  Should not do additional sort for the order by
    stmt = """execute s2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s3')
    # Should return 4 rows descending
    
    stmt = """prepare s3 from
select tab_a.c1, tab_b.d1
from tab_a,tab_b 
where tab_a.c1 = tab_b.d1
order by tab_a.c1 desc, tab_a.c2 desc ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain (null, 'S3'));"""
    output = _dci.cmdexec(stmt)
    
    #  Should not do additional sort for the order by
    stmt = """execute s3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s5')
    # Should return 4 rows descending
    
    stmt = """prepare s4 from
select tab_a.c1, tab_b.d1
from tab_a,tab_b 
where tab_a.c1 = tab_b.d1
order by tab_b.d1 desc, tab_b.d2 desc ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain (null, 'S4'));"""
    output = _dci.cmdexec(stmt)
    
    #  Should do additional sort for the order by
    stmt = """execute s4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s7')
    
    # NOW, FOR OUTER JOINS
    stmt = """prepare s5 from
select tab_a.c1, tab_b.d1
from tab_a left join tab_b 
on tab_a.c1 = tab_b.d1
order by tab_a.c1 desc ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain (null, 'S5'));"""
    output = _dci.cmdexec(stmt)
    
    #  No sort necessary for ORDER BY
    stmt = """execute s5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s9')
    
    stmt = """prepare s6 from
select tab_a.c1, tab_b.d1
from tab_a left join tab_b 
on tab_a.c1 = tab_b.d1
order by tab_a.c1 desc ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain (null, 'S6'));"""
    output = _dci.cmdexec(stmt)
    
    #  No sort necessary for ORDER BY
    stmt = """execute s6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s11')
    
    stmt = """prepare s7 from
select tab_a.c1, tab_b.d1
from tab_a left join tab_b 
on tab_a.c1 = tab_b.d1
order by tab_b.d1 desc ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain (null, 'S7'));"""
    output = _dci.cmdexec(stmt)
    
    #  Sort needed for ORDER BY
    stmt = """execute s7;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s13')
    
    # Testing some merge join fixes
    stmt = """prepare s1 from select x.a, x.b from kmergx x
inner join kmergx y
on x.a = y.b order by 1 desc, 2 desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain (null, 'S1'));"""
    output = _dci.cmdexec(stmt)
    
    #  Should not perform additional sort for the ORDER BY
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s15')
    
    stmt = """create index ikmerg on kmergx (b desc);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # Following query caused executor internal error in S03.
    # Problem due to the fact join orders (DESC) information was not relevant.
    # Therefore, two tables of a merge join might be in different orders.
    stmt = """prepare s2 from select x.a, x.b from kmergx x
inner join kmergx y
on x.b = y.a order by x.b asc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain (null, 'S2'));"""
    output = _dci.cmdexec(stmt)
    
    #  S03 version produced internal error here.
    stmt = """execute s2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s17')
    
    stmt = """drop table tab_a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table tab_b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table kmergx;"""
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
    #  Test case name:         A05
    #  Description:            1.Selecting from a shorthand view
    #                          2.Inserting into a protection view
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:        (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    
    stmt = """drop table tmp1;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table tmp1 
(a int      NOT NULL,
b char(11) NOT NULL,
c float    NOT NULL,
d timestamp,
primary key (a,b,c)) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create view vtmp1 as select b,c,d,a from tmp1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop table tmp2;"""
    output = _dci.cmdexec(stmt)
    
    # ignore error
    stmt = """create table tmp2 (a int       NOT NULL,
b char(11)  NOT NULL,
c float     NOT NULL,
d timestamp,
primary key (a,b,c)) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create view vtmp2 as select b,c,d,a from tmp2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # create a shorthand view with a union
    
    stmt = """create view vunion as
select * from tmp1 
union all
select a+1,b,c,d from vtmp1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """delete from vtmp1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 0)
    stmt = """delete from vtmp2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 0)
    
    # insert into vtmp1 values ('xxx', 3.5, current, 1);
    stmt = """insert into vtmp1 values ('xxx', 3.5, current, 1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # insert into pview
    
    stmt = """prepare s from
insert into vtmp2 (select * from vtmp1 
union all select b,c,d,a+1 from tmp1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain (null, 'S'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 2)
    
    stmt = """prepare s from
insert into vtmp2 (select
b,c,d,a+2 from vunion);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain (null, 'S'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 2)
    
    stmt = """prepare s from
insert into vtmp2 (select distinct b,c,d,a+4
from vunion);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain (null, 'S'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 2)
    
    stmt = """prepare s from
insert into vtmp2 (select b,c,d,a+10
from vunion)
order by 1,2,3,4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain (null, 'S'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 2)
    
    stmt = """prepare s from
insert into vtmp2 
(select b,c,d,a+12 from
 vtmp1)
order by 2,3,4,1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain (null, 'S'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """prepare s from
insert into vtmp2 
(select b,c,d,a+13 from
 tmp1)
order by 3,4,2,1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain (null, 'S'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """set param ?a 0;"""
    output = _dci.cmdexec(stmt)

    stmt = """prepare s from
insert into vtmp2 (select b,c,d,a+14 from
 vunion where a>?a);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain (null, 'S'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 2)
    
    stmt = """set param ?a 100;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s from
insert into vtmp2 (select b,c,d,a+14 from
 vunion where a>?a);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain (null, 'S'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 0)
    
    stmt = """set param ?b 0;"""
    output = _dci.cmdexec(stmt)
    stmt = """prepare s from
select b,c,d,a+14 from vunion where a>?b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain (null, 'S'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 2)
    
    stmt = """set param ?b 100;"""
    output = _dci.cmdexec(stmt)
    stmt = """prepare s from
select b,c,d,a+14 from vunion where a>?b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain (null, 'S'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """set param ?c 16;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s from
insert into vtmp2 (
select b,c,d,a+?c from vunion);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain (null, 'S'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 2)
    
    stmt = """prepare s from
select b,c,d,a+?c from vunion;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain (null, 'S'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 2)
    
    stmt = """select * from tmp2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 14)
    
    stmt = """create table ta021608(a largeint  NOT NULL,
b int       NOT NULL,
c smallint  NOT NULL,
d int,
primary key (a, b, c) );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #                                catalog
    
    stmt = """insert into ta021608 values (10,10,10,10);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into ta021608 values (10,20,20,20);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into ta021608 values (10,30,30,30);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into ta021608 values (10,40,40,40);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into ta021608 values (10,50,50,50);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # Create Shorthand views
    
    stmt = """create view vu021608 (x,y,z,w) as
select a,b,c,d from ta021608 where a = 10 and b = 10
union
select a,b,c,d from ta021608 where a = 10 and b = 20
union
select a,b,c,d from ta021608 where a = 10 and b = 30
union
select a,b,c,d from ta021608 where a = 10 and b = 40
union
select a,b,c,d from ta021608 where a = 10 and b = 50;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #catalog
    
    stmt = """set param ?p1 40;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p2 50;"""
    output = _dci.cmdexec(stmt)
    
    # ?section q1
    stmt = """select * from vu021608;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s17')
    
    #?section q2
    stmt = """prepare s1 from
select * from vu021608 where z in (?p1,?p2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain (null, 'S1'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s19')
    
    #?section q3
    
    stmt = """prepare s1 from
select * from vu021608 where z between ?p1 and ?p2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain (null, 'S1'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s21')
    
    #?section q4
    
    stmt = """prepare s1 from
select * from vu021608 where w in (?p1,?p2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain (null, 'S1'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s23')
    
    #?section q5
    
    stmt = """prepare s1 from
select * from vu021608 where w between ?p1 and ?p2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain (null, 'S1'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s25')
    
    stmt = """drop view vu021608;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view vunion;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view vtmp1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view vtmp2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table tmp1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table tmp2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table ta021608;"""
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
    #  Test case name:         A06
    #  Description:            1.Selecting from a shorthand view
    #                          2.Inserting into a protection view
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:
    #
    #  Notes:
    #  This testcase has been split from testcase TESTA05(i.e.
    #  sqltsql:SQLS0405).
    #
    # =================== End Test Case Header  ===================
    
    stmt = """create table ta021608(a largeint  NOT NULL,
b int       NOT NULL,
c smallint  NOT NULL,
d int,
primary key (a, b, c) );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #                                catalog
    
    stmt = """insert into ta021608 values (10,10,10,10);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into ta021608 values (10,20,20,20);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into ta021608 values (10,30,30,30);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into ta021608 values (10,40,40,40);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into ta021608 values (10,50,50,50);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # Create Shorthand views
    
    stmt = """create view vu021608 (x,y,z,w) as
select a,b,c,d from ta021608 where a = 10 and b = 10
union
select a,b,c,d from ta021608 where a = 10 and b = 20
union
select a,b,c,d from ta021608 where a = 10 and b = 30
union
select a,b,c,d from ta021608 where a = 10 and b = 40
union
select a,b,c,d from ta021608 where a = 10 and b = 50;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #catalog
    
    stmt = """set param ?p1 40;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p2 50;"""
    output = _dci.cmdexec(stmt)
    
    # ?section q1
    stmt = """select * from vu021608;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s0')
    
    #?section q2
    stmt = """prepare s1 from
select * from vu021608 where z in (?p1,?p2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain (null, 'S1'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s2')
    
    #?section q3
    
    stmt = """prepare s1 from
select * from vu021608 where z between ?p1 and ?p2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain (null, 'S1'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s4')
    
    #?section q4
    
    stmt = """prepare s1 from
select * from vu021608 where w in (?p1,?p2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain (null, 'S1'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s6')
    
    #?section q5
    
    stmt = """prepare s1 from
select * from vu021608 where w between ?p1 and ?p2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain (null, 'S1'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s8')
    
    stmt = """drop view vu021608;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table ta021608;"""
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
    #  Test case name:         A08
    #  Description:            GROUP BY on expressions.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:        (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    
    stmt = """drop table DT;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table DT 
(DT DATE, Y PIC 9999 ,M PIC 99,D PIC 99) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """INSERT INTO DT VALUES (DATE '1989-10-20',1989,10,20);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO DT VALUES (DATE '1989-10-20',1989,10,20);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO DT VALUES (DATE '1990-10-20',1990,10,20);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO DT VALUES (DATE '1990-11-21',1990,11,21);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO DT VALUES (DATE '1990-11-21',1990,11,21);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO DT VALUES (DATE '1991-11-21',1991,11,21);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO DT VALUES (DATE '1991-12-22',1991,12,22);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO DT VALUES (DATE '1991-12-22',1991,12,22);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO DT VALUES (DATE '1992-12-22',1992,12,22);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO DT VALUES (DATE '1980-12-23',1980,12,23);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select * from  DT;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s1')
    
    stmt = """create index IDT on DT (DT);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #catalog
    
    # prepare s1 from select DT month to month
    # from DT group by 1;
    stmt = """prepare s1 from select DT from DT group by DT;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain (null, 'S1'));"""
    output = _dci.cmdexec(stmt)
    
    #  Should see a sort for the GROUP BY
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s3')
    # Should see 3 rows
    
    # prepare s2 from select DT units month from DT group by 1;
    stmt = """prepare s2 from select DT from DT group by DT;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain (null, 'S2'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute s2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s5')
    # This query generates ERROR -8420 with S03 T9095ABE
    
    # prepare s3 from select DT month to month from  DT group by DT;
    stmt = """prepare s3 from select DT from DT group by DT;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain (null, 'S3'));"""
    output = _dci.cmdexec(stmt)
    #  Should see no sort for the GROUP BY
    stmt = """execute s3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s7')
    
    stmt = """prepare s4 from select -m, DT from DT group by m,DT;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain (null, 'S4'));"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s9')
    
    # prepare s5 from select DT month to month, m, d, count(*), sum(m) from
    # DT group by 1,2,3 order by 1,2 desc, 3 desc, 5,4;
    stmt = """prepare s5 from
select DT , m, d, count(*), sum(m)
from DT 
--   group by DT,Y, M
group by DT, M, D
order by 1,2 desc, 3 desc, 5,4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain (null, 'S5'));"""
    output = _dci.cmdexec(stmt)
    
    #  Should see one sort for the group by
    stmt = """execute s5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s11')
    
    # prepare s6 from select -m, sum(m) from DT group by DT;
    stmt = """prepare s6 from select -m, sum(m) from DT group by m;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain (null, 'S6'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute s6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s13')
    
    # prepare s7 from select m,d,m+d from DT group by 1,2,3;
    stmt = """prepare s7 from select dt1.a, dt1.b, dt1.c
from (select m,d,m+d from DT ) dt1 (a,b,c)group by a,b,c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain (null, 'S7'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute s7;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s15')
    
    # Same result expected as above statement.
    stmt = """prepare s8 from select m, d, m+d AS d1 from DT group by m, d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain (null, 'S8'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute s8;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s17')
    
    stmt = """drop table DT;"""
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
    #  Test case name:         A09
    #  Description:            LEFT JOIN of views
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:        (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    
    stmt = """create table oja(a int NOT NULL,
PRIMARY key (a));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create table ojb(b int NOT NULL,
PRIMARY key (b));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create table ojc(c int NOT NULL,
PRIMARY key (c));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create table ojd(d int NOT NULL,
PRIMARY key (d));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create table oje(e int NOT NULL,
PRIMARY key (e));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create table ojf(f int NOT NULL,
PRIMARY key (f));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create table ojg(g int NOT NULL,
PRIMARY key (g));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create table ojh(h int NOT NULL,
PRIMARY key (h));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into oja values(1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into oja values(2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into ojb values(2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into ojc values(1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into ojc values(2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into ojd values(2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into oje values(1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into oje values(2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into ojf values(2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into ojg values(1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into ojg values(2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into ojh values(2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """update statistics for table oja;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """update statistics for table ojb;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """update statistics for table ojc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """update statistics for table ojd;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """update statistics for table oje;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """update statistics for table ojf;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """update statistics for table ojg;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """update statistics for table ojh;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create view vao(p) as
select *
from oja 
where 0 = 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from vao;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    # should get 0 rows
    
    stmt = """create view vap(p) as
select *
from oja 
where a = 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from vap;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s0')
    # should get 1 row (1)
    
    stmt = """create view vb(q) as
select *
from ojb 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from vb;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s1')
    # should get 1 row (2)
    
    stmt = """create view vex(x) as
select *
from oje 
where e = 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from vex;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s2')
    # should get 1 row (1)
    
    # a, b
    
    stmt = """create view vab(p,q) as
select a,b
from oja,ojb 
where a = b
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from vab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s3')
    # should get 1 row (2,2)
    
    # c, d
    
    stmt = """create view vcd(r,s) as
select c,d
from ojc,ojd 
where c = d
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from vcd;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s4')
    # should get 1 row (2,2)
    
    # a ij b
    
    stmt = """create view vaib(p,q) as
select a,b
from oja inner join ojb on a = b ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from vaib;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s5')
    # should get 1 row (2,2)
    
    # c ij d
    
    stmt = """create view vcid(r,s) as
select c,d
from ojc inner join ojd on c = d ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from vcid;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s6')
    # should get 1 row (2,2)
    
    # a lj b
    
    stmt = """create view valb(p,q) as
select a,b
from oja left join ojb on a = b ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from valb;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s7')
    # should get 2 rows { (1,null), (2,2) }
    
    # c lj d
    
    stmt = """create view vcld(r,s) as
select c,d
from ojc left join ojd on c = d ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from vcld;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s8')
    # should get 2 rows { (1,null), (2,2) }
    
    # e lj f
    
    stmt = """create view velf(r,s) as
select e,f
from oje left join ojf on e = f ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from velf;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s9')
    # two rows { (1,null), (2,2) }
    
    # a, b ij c
    
    stmt = """create view vabic(p,q) as
select a,c
from oja, ojb inner join ojc on b = c
where a = c ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from vabic;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s10')
    # one row (2,2)
    
    # b ij c, a
    
    stmt = """create view vbica(p,q) as
select a,c
from ojb inner join ojc on b = c, oja 
where a = c ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from vbica;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s11')
    # one row (2,2)
    
    # e ij f, g
    
    stmt = """create view vefig(r,s) as
select e,g
from oje, ojf inner join ojg on f = g
where e = g ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from vefig;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s12')
    # one row (2,2)
    
    # f ij g, e
    
    stmt = """create view vfige(r,s) as
select e,g
from ojf inner join ojg on f = g, oje 
where e = g ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from vfige;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s13')
    # one row (2,2)
    
    # a lj b, c
    
    stmt = """create view valbc(p,q) as
select c,b
from oja left join ojb on a = b, ojc 
where c = a ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from valbc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s14')
    # two rows { (1,null), (2,2) }
    
    # c, a lj b
    
    stmt = """create view vcalb(p,q) as
select c,b
from ojc, oja left join ojb on a = b
where c = a ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from vcalb;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s15')
    # two rows { (1,null), (2,2) }
    
    # e lj f, g
    
    stmt = """create view velfg(r,s) as
select g,f
from oje left join ojf on e = f, ojg 
where g = e ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from velfg;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s16')
    # two rows { (1,null), (2,2) }
    
    # g, e lj f
    
    stmt = """create view vgelf(r,s) as
select g,f
from ojg, oje left join ojf on e = f
where g = e ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from vgelf;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s17')
    # two rows { (1,null), (2,2) }
    
    # (a lj b) ij c
    
    stmt = """create view valbic(p,q) as
select c,V.q
from valb V inner join ojc on c = V.p ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from valbic;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s18')
    # two rows { (1,null), (2,2) }
    
    # c ij (a lj b)
    
    stmt = """create view vcialb(p,q) as
select c,V.q
from ojc inner join valb V on V.p = c
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from vcialb;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s19')
    # two rows { (1,null), (2,2) }
    
    # (e lj f) ij g
    
    stmt = """create view velfig(r,s) as
select g,V.s
from velf V inner join ojg on g = V.r
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from velfig;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s20')
    # two rows { (1,null), (2,2) }
    
    # g ij (e lf j)
    
    stmt = """create view vgielf(r,s) as
select g,V.s
from ojg inner join velf V on g = V.r
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from vgielf;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s21')
    # two rows { (1,null), (2,2) }
    
    # ( a, (b ij c) ) ij ( e, (f ij g) )
    
    stmt = """create view viii1 (p, q) as
select X.p, Y.r
from vabic X inner join vefig Y on X.p = Y.r
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from viii1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s22')
    # should get (2,2)
    
    # ( a, (b ij c) ) ij ( (f ij g), e )
    
    stmt = """create view viii2 (p, q) as
select X.p, Y.r
from vabic X inner join vfige Y on X.p = Y.r
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from viii2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s23')
    # should get (2,2)
    
    # ( (b ij c), a ) ij ( e, (f ij g) )
    
    stmt = """create view viii3 (p, q) as
select X.p, Y.r
from vbica X inner join vefig Y on X.p = Y.r
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from viii3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s24')
    # should get (2,2)
    
    # ( (b ij c), a ) ij ( (f ij g), e )
    
    stmt = """create view viii4 (p, q) as
select X.p, Y.r
from vbica X inner join vfige Y on X.p = Y.r
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from viii4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s25')
    # should get (2,2)
    
    # ( a, (b ij c) ) lj ( e, (f ij g) )
    
    stmt = """create view vili1 (p, q) as
select X.p, Y.r
from vabic X left  join vefig Y on X.p = Y.r
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from vili1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s26')
    # should get (2,2)
    
    # ( a, (b ij c) ) lj ( (f ij g), e )
    
    stmt = """create view vili2 (p, q) as
select X.p, Y.r
from vabic X left join vfige Y on X.p = Y.r
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from vili2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s27')
    # should get (2,2)
    
    # ( (b ij c), a ) lj ( e, (f ij g) )
    
    stmt = """create view vili3 (p, q) as
select X.p, Y.r
from vbica X left join vefig Y on X.p = Y.r
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from vili3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s28')
    # should get (2,2)
    
    # ( (b ij c), a ) lj ( (f ij g), e )
    
    stmt = """create view vili4 (p, q) as
select X.p, Y.r
from vbica X left join vfige Y on X.p = Y.r
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from vili4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s29')
    # should get (2,2)
    
    # ( (a lj b), c) ij ( (e lj f), g )
    
    stmt = """create view vlil1 (r, s) as
select X.p, Y.s
from valbc X inner join velfg Y on X.p = Y.r
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from vlil1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s30')
    # should get { (1,null), (2,2) }
    
    # ( (a lj b), c) ij ( g, (e lj f) )
    
    stmt = """create view vlil2 (r, s) as
select X.p, Y.s
from valbc X inner join vgelf Y on X.p = Y.r
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from vlil2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s31')
    # should get { (1,null), (2,2) }
    
    # ( c, (a lj b) ) ij ( (e lj f), g )
    
    stmt = """create view vlil3 (r, s) as
select X.p, Y.s
from vcalb X inner join velfg Y on X.p = Y.r
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from vlil3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s32')
    # should get { (1,null), (2,2) }
    
    # ( c, (a lj b)) ij ( g, (e lj f) )
    
    stmt = """create view vlil4 (r, s) as
select X.p, Y.s
from vcalb X inner join vgelf Y on X.p = Y.r
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from vlil4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s33')
    # should get { (1,null), (2,2) }
    
    # *  QUERIES ON THE VIEWS CREATED ABOVE.                  *
    
    # Each view is a single table
    # View Vao returns no rows
    stmt = """prepare s1 from
select *
from vao inner join vb on p = q
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain (null, 'S1'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    # should see 0 rows
    
    # View Vao returns no rows
    stmt = """prepare s1 from
select *
from vao left  join vb  on p = q
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain (null, 'S1'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    # should see 0 rows
    
    # View Vao returns no rows
    stmt = """prepare s1 from
select *
from vb left  join vao  on p = q
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain (null, 'S1'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s37')
    # should see 1 row (2, null)
    
    # The predicate (0 = 1) in the WHERE clause of Vao
    #   should get ANDed to the ON clause of the query.
    stmt = """prepare s1 from
select *
from oje X left  join vao Y on X.e = Y.p
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain (null, 'S1'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s39')
    # should see two rows { (1,null), (2,null) }
    
    # The predicate (a = 1) in the WHERE clause of Vap
    #   should get ANDed to the WHERE clause of the query.
    stmt = """prepare s1 from
select *
from vex X left  join oja Y on a = 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain (null, 'S1'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s41')
    # should see 1 row (1, 2)
    
    # SECTION A) : Trees on both sides
    # (a ij b) ij (c ij d)
    stmt = """prepare s1 from
select *
from vaib X inner join vcid Y  on X.p = Y.r
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain (null, 'S1'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s43')
    # should get 1 row (2,2,2,2)
    
    # (a ij b) ij (c lj d)
    stmt = """prepare s1 from
select *
from vaib X inner join vcld Y on X.p = Y.r
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain (null, 'S1'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s45')
    # should get 1 row (2,2,2,2)
    
    # (c lj d) ij (a ij b)
    stmt = """prepare s1 from
select *
from vcld X inner join vaib Y on X.r = Y.p
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain (null, 'S1'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s47')
    # should get 1 row (2,2,2,2)
    
    # (c lj d) ij (a lj b)
    stmt = """prepare s1 from
select *
from vcld X inner join valb Y on X.r = Y.p
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain (null, 'S1'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s49')
    #  should get 2 rows { (1,null,1null), (2,2,2,2) }
    
    #  (a ij b) lj (c ij d)
    stmt = """select *
from vaib X left  join vcid Y on X.p = Y.r
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s50')
    #  should give normalizer error
    
    #  (a ij b) lj (c lj d)
    stmt = """select *
from vaib X left  join vcld Y on X.p = Y.r
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s51')
    #  should give normalizer error
    
    #  (c lj d) lj (a ij b)
    stmt = """select *
from vcld X left  join vaib Y on X.r = Y.p
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s52')
    # should give normalizer error
    
    # (c lj d) lj (a lj b)
    stmt = """prepare s1 from
select *
from vcld X left  join valb Y on X.r = Y.p
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    # should give normalizer error
    
    # SECTION B) List on at least one side
    # (a, b) ij (c, d)
    stmt = """prepare s1 from
select *
from vab X inner join vcd Y on X.p = Y.r
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain (null, 'S1'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s54')
    # should get 1 row (2,2,2,2)
    
    # (a, b) ij (c lj d)
    stmt = """prepare s1 from
select *
from vab X inner join vcld Y on X.p = Y.r
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain (null, 'S1'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s56')
    # should get 1 row (2,2,2,2)
    
    # (c lj d) ij (a, b)
    stmt = """prepare s1 from
select *
from vcld X inner join vab Y on X.r = Y.p
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain (null, 'S1'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s58')
    #  should get 1 row ( 2,2,2,2 )
    
    #  (a, b) lj (c, d)
    stmt = """select *
from vab X left  join vcd Y on X.p = Y.r
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s59')
    #  should give normalizer error
    
    #  (a, b) lj (c lj d)
    stmt = """select *
from vab X left  join vcld Y on X.p = Y.r
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s60')
    #  should give normalizer error
    
    #  (c lj d) lj (a, b)
    stmt = """select *
from vcld X left  join vab Y on X.r = Y.p
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s61')
    # should give normalizer error
    
    # SECTION c) :  Combination of a list and tree on one side
    # (a, b ij c) ij (e, f ij g)
    stmt = """prepare s1 from
select *
from vabic X inner join vefig Y on X.p = Y.r
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain (null, 'S1'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s63')
    # should get 1 row (2,2,2,2)
    
    # (a, b ij c) ij (f ij g, e)
    stmt = """prepare s1 from
select *
from vabic X inner join vfige Y on X.p = Y.r
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain (null, 'S1'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s65')
    # should get 1 row (2,2,2,2)
    
    # (b ij c, a) ij (e, f ij g)
    stmt = """prepare s1 from
select *
from vbica X inner join vefig Y on X.p = Y.r
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain (null, 'S1'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s67')
    # should get 1 row (2,2,2,2)
    
    # (b ij c, a) ij (f ij g, e)
    stmt = """prepare s1 from
select *
from vbica X inner join vfige Y on X.p = Y.r
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain (null, 'S1'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s69')
    # should get 1 row (2,2,2,2)
    
    # (a lj b, c) ij (e lj f, g)
    stmt = """prepare s1 from
select *
from valbc X inner join velfg Y on X.p = Y.r
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain (null, 'S1'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s71')
    # should get 1 row { (1,null,1,null), (2,2,2,2) }
    
    # (a lj b, c) ij (g, e lj f)
    stmt = """prepare s1 from
select *
from valbc X inner join vgelf Y on X.p = Y.r
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain (null, 'S1'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s73')
    # should get 1 row { (1,null,1,null), (2,2,2,2) }
    
    # (c, a lj b) ij (e lj f, g)
    stmt = """prepare s1 from
select *
from vcalb X inner join velfg Y on X.p = Y.r
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain (null, 'S1'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s75')
    # should get 1 row { (1,null,1,null), (2,2,2,2) }
    
    # (c, a lj b) ij (g, e lj f)
    stmt = """prepare s1 from
select *
from vcalb X inner join vgelf Y on X.p = Y.r
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain (null, 'S1'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s77')
    # should get 1 row { (1,null,1,null), (2,2,2,2) }
    
    # (a, b ij c) ij (e lj f, g)
    stmt = """prepare s1 from
select *
from vabic X inner join velfg Y on X.p = Y.r
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain (null, 'S1'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s79')
    # should get 1 row (2,2,2,2)
    
    # (a lj b, c) ij (e, f ij g)
    stmt = """prepare s1 from
select *
from valbc X inner join vefig Y on X.p = Y.r
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain (null, 'S1'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s81')
    # should get 1 row (2,2,2,2)
    
    # (a, b ij c) lj (e, f ij g)
    stmt = """prepare s1 from
select *
from vabic X left  join vefig Y on X.p = Y.r
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    # should get normalizer error
    
    # (a, b ij c) lj (f ij g, e)
    stmt = """prepare s1 from
select *
from vabic X left  join vfige Y on X.p = Y.r
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    # should get normalizer error
    
    # (a, b ij c) lj (g, e lj f)
    stmt = """prepare s1 from
select *
from vabic X left  join vgelf Y on X.p = Y.r
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    # should get normalizer error
    
    # (a, b ij c) lj (f lj g, e)
    stmt = """prepare s1 from
select *
from vabic X left  join velfg Y on X.p = Y.r
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    # should get normalizer error
    
    # SECTION D) Left join is not the root node
    # ( (a lj b) ij c ) ij ( (e lj f) ij g )
    stmt = """prepare s1 from
select *
from valbic X inner join velfig Y on X.p = Y.r
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain (null, 'S1'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s83')
    # should get two rows { (1,null,1,null), (2,2,2,2) }
    
    # ( (a lj b) ij c ) ij ( g ij (e lj f) )
    stmt = """prepare s1 from
select *
from valbic X inner join vgielf Y on X.p = Y.r
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain (null, 'S1'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s85')
    # should get two rows { (1,null,1,null), (2,2,2,2) }
    
    # ( c ij (a lj b) ) ij ( (e lj f) ij g )
    stmt = """prepare s1 from
select *
from vcialb X inner join velfig Y on X.p = Y.r
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain (null, 'S1'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s87')
    # should get two rows { (1,null,1,null), (2,2,2,2) }
    
    # ( c ij (a lj b) ) ij ( g ij (e lj f) )
    stmt = """prepare s1 from
select *
from vcialb X inner join vgielf Y on X.p = Y.r
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain (null, 'S1'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s89')
    # should get two rows { (1,null,1,null), (2,2,2,2) }
    
    # ( (a lj b) ij c ) lj ( (e lj f) ij g )
    stmt = """prepare s1 from
select *
from valbic X left join velfig Y on X.p = Y.r
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    # should get normalizer error
    
    # ( (a lj b) ij c ) lj ( g ij (e lj f) )
    stmt = """prepare s1 from
select *
from valbic X left join vgielf Y on X.p = Y.r
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    # should get normalizer error
    
    # ( c ij (a lj b) ) lj ( (e lj f) ij g )
    stmt = """prepare s1 from
select *
from vcialb X left join velfig Y on X.p = Y.r
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    # should get normalizer error
    
    # ( c ij (a lj b) ) lj ( g ij (e lj f) )
    stmt = """prepare s1 from
select *
from vcialb X left join vgielf Y on X.p = Y.r
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    # should get normalizer error
    
    # a ij ( (e lj f) ij g )
    stmt = """prepare s1 from
select *
from oja X inner join velfig Y on X.a = Y.r
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain (null, 'S1'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s91')
    # should get two rows { (1,1,null), (2,2,2) }
    
    # a ij ( g ij (e lj f) )
    stmt = """prepare s1 from
select *
from oja X inner join vgielf Y on X.a = Y.r
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain (null, 'S1'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s93')
    # should get two rows { (1,1,null), (2,2,2) }
    
    # a ij ( (e lj f) ij g )
    stmt = """prepare s1 from
select *
from oja X inner join velfig Y on X.a = Y.r
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain (null, 'S1'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s95')
    # should get two rows { (1,1,null), (2,2,2) }
    
    # a ij ( g ij (e lj f) )
    stmt = """prepare s1 from
select *
from oja X inner join vgielf Y on X.a = Y.r
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain (null, 'S1'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s97')
    # should get two rows { (1,1,null), (2,2,2) }
    
    # ( (a lj b) ij c ) ij oje
    stmt = """prepare s1 from
select *
from valbic X inner join oje Y on X.p = Y.e
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain (null, 'S1'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s99')
    # should get two rows { (1,null,1), (2,2,2) }
    
    # ( (a lj b) ij c ) ij oje
    stmt = """prepare s1 from
select *
from valbic X inner join oje Y on X.p = Y.e
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain (null, 'S1'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s101')
    # should get two rows { (1,null,1), (2,2,2) }
    
    # ( c ij (a lj b) ) ij e
    stmt = """prepare s1 from
select *
from vcialb X inner join oje Y on X.p = Y.e
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain (null, 'S1'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s103')
    # should get two rows { (1,null,1), (2,2,2) }
    
    # ( c ij (a lj b) ) ij e
    stmt = """prepare s1 from
select *
from vcialb X inner join oje Y on X.p = Y.e
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain (null, 'S1'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s105')
    # should get two rows { (1,null,1), (2,2,2) }
    
    # ( (a lj b) ij c ) lj f
    stmt = """prepare s1 from
select *
from valbic X left join ojf Y on X.p = Y.f
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain (null, 'S1'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s107')
    # should get two rows { (1,null,null), (2,2,2) }
    
    # ( (a lj b) ij c ) lj f
    stmt = """prepare s1 from
select *
from valbic X left join ojf Y on X.p = Y.f
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain (null, 'S1'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s109')
    # should get two rows { (1,null,null), (2,2,2) }
    
    # ( c ij (a lj b) ) lj f
    stmt = """prepare s1 from
select *
from vcialb X left join ojf Y on X.p = Y.f
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain (null, 'S1'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s111')
    # should get two rows { (1,null,null), (2,2,2) }
    
    # ( c ij (a lj b) ) lj f
    stmt = """prepare s1 from
select *
from vcialb X left join ojf Y on X.p = Y.f
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain (null, 'S1'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s113')
    # should get two rows { (1,null,null), (2,2,2) }
    
    # ( (a lj b) ij c ) ij e
    stmt = """prepare s1 from
select *
from valbic X inner join vex Y on X.p = Y.x
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain (null, 'S1'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s115')
    # should get one row (1,null,1)
    
    # ( (a lj b) ij c ) ij e
    stmt = """prepare s1 from
select *
from valbic X inner join vex Y on X.p = Y.x
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain (null, 'S1'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s117')
    # should get one row (1,null,1)
    
    # ( c ij (a lj b) ) ij e
    stmt = """prepare s1 from
select *
from vcialb X inner join vex Y on X.p = Y.x
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain (null, 'S1'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s119')
    # should get one row (1,null,1)
    
    # ( c ij (a lj b) ) ij e
    stmt = """prepare s1 from
select *
from vcialb X inner join vex Y on X.p = Y.x
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain (null, 'S1'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s121')
    # should get one rows (1,null,1)
    
    # ( (a lj b) ij c ) lj e
    stmt = """prepare s1 from
select *
from valbic X left join vex Y on X.p = Y.x
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain (null, 'S1'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s123')
    # should get two rows { (1,null,1), (2,2,null) }
    
    # ( (a lj b) ij c ) lj e
    stmt = """prepare s1 from
select *
from valbic X left join vex Y on X.p = Y.x
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain (null, 'S1'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s125')
    # should get two rows { (1,null,1), (2,2,null) }
    
    # ( c ij (a lj b) ) lj e
    stmt = """prepare s1 from
select *
from vcialb X left join vex Y on X.p = Y.x
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain (null, 'S1'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s127')
    # should get two rows { (1,null,1), (2,2,null) }
    
    # ( c ij (a lj b) ) lj e
    stmt = """prepare s1 from
select *
from vcialb X left join vex Y on X.p = Y.x
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain (null, 'S1'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s129')
    # should get two rows { (1,null,1), (2,2,null) }
    
    stmt = """drop view vao;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view vap;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view vb;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view vex;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view vab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view vcd;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view vaib;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view vcid;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view valbic;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view vcialb;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view valb;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view vcld;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view velfig;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view vgielf;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view velf;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view viii1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view viii2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view vili1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view vili2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view vabic;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view viii3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view viii4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view vili3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view vili4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view vbica;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view vefig;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view vfige;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view vlil1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view vlil2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view valbc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view vlil3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view velfg;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view vlil4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view vgelf;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view vcalb;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop table oja;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table ojb;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table ojc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table ojd;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table oje;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table ojf;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table ojg;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table ojh;"""
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
    #  Test case name:         A10
    #  Description:            Test cases involving GROUP BY/
    #                          AGGREGATE-DISTINCT/ HAVING clauses
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:        (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    
    stmt = """create table k1 (a int not null,
b int not null,
c int not null) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create unique index ki1 on k1 (a);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into k1 values (0,0,0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into k1 values (1,1,0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into k1 values (2,2,0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into k1 values (3,3,1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into k1 values (4,4,1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into k1 values (5,5,1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # create tables for merge join tests
    
    stmt = """create table oj1 (a int) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #                catalog
    
    stmt = """insert into oj1 values (1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into oj1 values (1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into oj1 values (2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into oj1 values (3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into oj1 values (null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """create table oj2 (b int) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #                catalog
    
    stmt = """insert into oj2 values (2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into oj2 values (3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into oj2 values (3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """update statistics for table oj1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """update statistics for table oj2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """prepare s1 from
select t1.a, t1.b, count(distinct t2.c)
from k1 t1 inner join k1 t2 on t1.a = t2.a
group by t1.a, t1.b
having count(distinct t2.c) > 0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain (null, 'S1'));"""
    output = _dci.cmdexec(stmt)
    
    #  Should perform one sort for the GROUP BY for the DISTINCT (Phil Bug #1)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s1')
    
    # Same query, LEFT JOIN
    stmt = """prepare s1a from
select t1.a, t1.b, count(distinct t2.c)
from k1 t1 left join k1 t2 on t1.a = t2.a
group by t1.a, t1.b
having count(distinct t2.c) > 0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain (null, 'S1A'));"""
    output = _dci.cmdexec(stmt)
    
    #  Should perform one sort for the GROUP BY for the DISTINCT (Phil Bug #1)
    stmt = """execute s1a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s3')
    
    # Now, remove the aggregate-distinct from the SELECT list
    stmt = """prepare s2 from
select t1.a from k1 t1 inner join k1 t2 on t1.a = t2.a
group by t1.a
having count(distinct t2.c) > 0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain (null, 'S2'));"""
    output = _dci.cmdexec(stmt)
    
    #  Should perform SORT for the GROUP BY (for the DISTINCT)
    stmt = """execute s2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s5')
    
    # Unique Index T1.A, aggregate distinct on column from same table
    stmt = """prepare s3 from
select t1.a,count(distinct t1.c) from k1 t1 
inner join k1 t2 
on t1.a = t2.a
group by t1.a
having count(distinct t1.c) > 0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain (null, 'S3'));"""
    output = _dci.cmdexec(stmt)
    
    #  No sort necessary
    stmt = """execute s3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s7')
    
    # Now, remove the aggregate-distinct from SELECT list
    stmt = """prepare s4 from
select t1.a from k1 t1 inner join k1 t2 on t1.a = t2.a
group by t1.a
having count(distinct t1.c) > 0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain (null, 'S4'));"""
    output = _dci.cmdexec(stmt)
    
    #  No sort necessary
    stmt = """execute s4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s9')
    
    stmt = """drop index ki1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # Create a non-unique index on k1;
    
    stmt = """create index kni1 on k1(a);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # Non-unique index on T1.A, aggregate-distinct on T1.C
    stmt = """prepare s5 from
select t1.a from k1 t1 inner join k1 t2 on t1.a = t2.a
group by t1.a
having count(distinct t1.c) > 0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain (null, 'S5'));"""
    output = _dci.cmdexec(stmt)
    
    #  Sort necessary.  Should sort on T1.A, T1.C  (Phils Bug #2)
    stmt = """execute s5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s11')
    
    # Now, include aggregate-distinct in SELECT list
    stmt = """prepare s6 from
select t1.a, count(distinct t1.b) from k1 t1 
inner join k1 t2 
on t1.a = t2.a
group by t1.a
having count(distinct t1.b) > 0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain (null, 'S6'));"""
    output = _dci.cmdexec(stmt)
    
    #  Sort necessary.  Should sort on T1.A, T1.C
    stmt = """execute s6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s13')
    
    # MERGE JOIN TESTS
    
    stmt = """prepare s1 from
select a from oj1 left join oj2 on a=b
group by a
having count(distinct a) > 0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    stmt = """select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain (null, 'S1'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s15')
    
    # Now, add aggregate distinct to the SELECT list
    stmt = """prepare s2 from
select a, count(distinct a)
from oj1 left join oj2 on a=b
group by a
having count(distinct a) > 0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain (null, 'S2'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute s2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s17')
    
    stmt = """prepare s3 from
select a, count(distinct b)
from oj1 left join oj2 on a=b
group by a
having count(distinct b) > 0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain (null, 'S3'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute s3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s19')
    
    stmt = """prepare s4 from
select a
from oj1 left join oj2 on a=b
group by a
having count(distinct b) > 0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain (null, 'S4'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute s4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s21')
    
    stmt = """drop table k1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table oj1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table oj2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

