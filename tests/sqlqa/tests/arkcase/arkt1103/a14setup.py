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

#== setup for tescase a14 ========================

# Remove relevant tables and views.
# Include dropping of views that would otherwise prevent
# tables from dropping.
def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci
    
    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()
    
    stmt = """drop view view1 ;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop view view2 ;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop view view3 ;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop view view4 ;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop view view5 ;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop view view6 ;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop view view7 ;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop view view8 ;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table tab1 ;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table tab2 ;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table tab3 ;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table tab4 ;"""
    output = _dci.cmdexec(stmt)
    #
    
    # Create the tables.
    stmt = """create table tab1 (
vch7 varchar(7) , chu3 char(3) ) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table tab2 (
vch7 varchar(7) , chu3 char(3) ) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table tab3 (
vch7 varchar(7) , chu3 char(3) ) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table tab4 (
vch7 varchar(7) , chu3 char(3) ) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    # Insert data into those tables; column chu3 has unique values,
    # column vch7 has values that map to those in 1 or more other tables;
    # include NULL value.
    
    stmt = """insert into tab1 values
(NULL, '1xu' )
, ('ab', '1xv' )
, ('ac', '1xw' )
, ('ad', '1xy' )
, ('abcd', '1xz' )
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 5)
    
    stmt = """select * from tab1 order by 1, 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a14sexp""", 'a14ss1')
    #
    
    # Include duplicate value.
    
    stmt = """insert into tab2 values
('ab', '2xu' )
, ('ab', '2xv' )
, ('bc', '2xw' )
, ('bd', '2xy' )
, ('abcd', '1xz' )
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 5)
    
    stmt = """select * from tab2 order by 1, 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a14sexp""", 'a14ss2')
    #
    
    # Include NULL value.
    
    stmt = """insert into tab3 values
(NULL, '3xu' )
, ('ac', '3xv' )
, ('bc', '3xw' )
, ('cd', '3xy' )
, ('abcd', '1xz' )
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 5)
    
    stmt = """select * from tab3 order by 1, 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a14sexp""", 'a14ss3')
    #
    # Include duplicate value.
    
    stmt = """insert into tab4 values
('cd', '4xu' )
, ('ad', '4xv' )
, ('bd', '4xw' )
, ('cd', '4xy' )
, ('abcd', '1xz' )
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 5)
    
    stmt = """select * from tab4 order by 1, 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a14sexp""", 'a14ss4')
    #
    # Create the views.
    #
    # ======================================
    # (1) Join on columns in ajacent tables.
    #     <view1> is <table1>
    #		INNER JOIN <table2>
    #		LEFT JOIN <table3>
    #		LEFT JOIN <table4>
    # joining on column values in ajacent tables.
    # ======================================
    #
    # Scaffolding selects:
    stmt = """select t1.vch7, t1.chu3, t2.vch7, t2.chu3
from tab1 t1
inner join tab2 t2 on t1.vch7 = t2.vch7
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a14sexp""", 'a14ss5')
    
    stmt = """select t1.vch7, t1.chu3, t2.vch7, t2.chu3, t3.vch7, t3.chu3
from tab1 t1
inner join tab2 t2 on t1.vch7 = t2.vch7
left join tab3 t3 on t2.vch7 = t3.vch7
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a14sexp""", 'a14ss6')
    #
    stmt = """create view view1 
( c1, c2, c3, c4, c5, c6, c7, c8 ) as
select t1.vch7, t1.chu3, t2.vch7, t2.chu3
, t3.vch7, t3.chu3, t4.vch7, t4.chu3
from tab1 t1
inner join tab2 t2 on t1.vch7 = t2.vch7
left join tab3 t3 on t2.vch7 = t3.vch7
left join tab4 t4 on t3.vch7 = t4.vch7
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from view1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a14sexp""", 'a14ss7')
    #
    # ======================================
    # (2) Join on columns (including non=ajacent tables).
    #     <view2> is <table1>
    #		LEFT JOIN <table2>
    #		INNER JOIN <table3>
    #		LEFT JOIN <table4>
    # ======================================
    
    stmt = """select t1.vch7, t1.chu3, t2.vch7, t2.chu3
from tab1 t1
left join tab2 t2 on t1.vch7 = t2.vch7
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a14sexp""", 'a14ss8')
    
    stmt = """select t1.vch7, t1.chu3, t2.vch7, t2.chu3
, t3.vch7, t3.chu3
from tab1 t1
left join tab2 t2 on t1.vch7 = t2.vch7
inner join tab3 t3 on t1.vch7 = t3.vch7
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a14sexp""", 'a14ss9')
    
    stmt = """create view view2 
( c1, c2, c3, c4, c5, c6, c7, c8 ) as
select t1.vch7, t1.chu3, t2.vch7, t2.chu3
, t3.vch7, t3.chu3, t4.vch7, t4.chu3
from tab1 t1
left join tab2 t2 on t1.vch7 = t2.vch7
inner join tab3 t3 on t1.vch7 = t3.vch7
left join tab4 t4 on t1.vch7 = t4.vch7
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from view2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a14sexp""", 'a14ss10')
    #
    # ======================================
    # (3) Join on column values (including non=ajacent tables);
    #     GROUP BY.
    #     <view3> is <table1>
    #		LEFT JOIN <table2>
    #		LEFT JOIN <table3>
    #		INNER JOIN <table4>
    # ======================================
    
    stmt = """select t1.vch7, t1.chu3, t2.vch7, t2.chu3
from tab1 t1
left join tab2 t2 on t2.vch7 = t1.vch7
group by t1.vch7, t1.chu3, t2.vch7, t2.chu3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a14sexp""", 'a14ss11')
    
    stmt = """select t1.vch7, t1.chu3, t2.vch7, t2.chu3
, t3.vch7, t3.chu3
from tab1 t1
left join tab2 t2 on t2.vch7 = t1.vch7
left join tab3 t3 on t2.vch7 = t3.vch7
group by t1.vch7, t1.chu3, t2.vch7, t2.chu3, t3.vch7, t3.chu3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a14sexp""", 'a14ss12')
    
    stmt = """create view view3 
( c1, c2, c3, c4, c5, c6, c7, c8 ) as
select t1.vch7, t1.chu3, t2.vch7, t2.chu3
, t3.vch7, t3.chu3, t4.vch7, t4.chu3
from tab1 t1
left join tab2 t2 on t2.vch7 = t1.vch7
left join tab3 t3 on t2.vch7 = t3.vch7
inner join tab4 t4 on t1.vch7 = t3.vch7
group by t1.vch7, t1.chu3, t2.vch7, t2.chu3
, t3.vch7, t3.chu3, t4.vch7, t4.chu3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from view3 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a14sexp""", 'a14ss13')
    #
    # ======================================
    # (4) Join on column values (including non=ajacent tables);
    #     DISTINCT.
    #     <view4> is <table1>
    #		LEFT JOIN <table2>
    #		LEFT JOIN <table3>
    #		LEFT JOIN <table4>
    # Include joining on column values in non=ajacent tables.
    # ======================================
    
    stmt = """select DISTINCT
t1.vch7, t1.chu3, t2.vch7, t2.chu3
, t3.vch7, t3.chu3, t4.vch7, t4.chu3
from tab1 t1
left join tab2 t2 on t1.vch7 = t2.vch7
left join tab3 t3 on t2.vch7 = t3.vch7
left join tab4 t4 on t3.vch7 = t4.vch7
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a14sexp""", 'a14ss14')
    
    stmt = """create view view4 ( c1, c2, c3, c4, c5, c6, c7, c8 ) as
select DISTINCT
t1.vch7, t1.chu3, t2.vch7, t2.chu3
, t3.vch7, t3.chu3, t4.vch7, t4.chu3
from tab1 t1
left join tab2 t2 on t1.vch7 = t2.vch7
left join tab3 t3 on t2.vch7 = t3.vch7
left join tab4 t4 on t3.vch7 = t4.vch7
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    ##endtt
    
    ##tabtype mptab
    
    ##expect any *--- SQL operation complete.*
    stmt = """create table tempvw4 (c1 varchar(7), c2 char(3), c3 varchar(7), c4 char(3),
c5 varchar(7), c6 char(3), c7 varchar(7), c8 char(3))
no partition;"""
    output = _dci.cmdexec(stmt)
    
    ##expect any *--- SQL operation complete.*
    stmt = """create view view4 as select * from tempvw4 for protection;"""
    output = _dci.cmdexec(stmt)
    
    ##expect any *--- 6 row(s) inserted.*
    #  insert into view4
    #      select DISTINCT
    #         t1.vch7, t1.chu3, t2.vch7, t2.chu3
    #         , t3.vch7, t3.chu3, t4.vch7, t4.chu3
    #      from tab1 t1
    #      left join tab2 t2 on t1.vch7 = t2.vch7
    #      left join tab3 t3 on t2.vch7 = t3.vch7
    #      left join tab4 t4 on t3.vch7 = t4.vch7
    #   ;
    #
    ##endtt
    
    stmt = """select * from view4 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a14sexp""", 'a14ss15')
    
    #
    # ======================================
    # (5) Join on column values (including non=ajacent tables);
    #     aggregated results.
    #     <view5> is <table1>
    #		LEFT JOIN <table2>
    #		LEFT JOIN <table3>
    #		LEFT JOIN <table4>
    # ======================================
    
    stmt = """select max(t1.vch7), count(t1.chu3)
, max(t2.vch7), count(t2.chu3)
, max(t3.vch7), count(t3.chu3)
, max(t4.vch7), count(t4.chu3)
from tab1 t1
join tab2 t2 on t1.vch7 = t2.vch7
left join tab3 t3 on t2.vch7 = t3.vch7
left join tab4 t4 on t3.vch7 = t4.vch7
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a14sexp""", 'a14ss16')
    
    stmt = """create view view5 
( c1, c2, c3, c4, c5, c6, c7, c8 ) as
select max(t1.vch7), count(t1.chu3)
, max(t2.vch7), count(t2.chu3)
, max(t3.vch7), count(t3.chu3)
, max(t4.vch7), count(t4.chu3)
from tab1 t1
join tab2 t2 on t1.vch7 = t2.vch7
left join tab3 t3 on t2.vch7 = t3.vch7
left join tab4 t4 on t3.vch7 = t4.vch7
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    ##endtt
    
    ##tabtype mptab
    
    ##expect any *--- SQL operation complete.*
    #   create table tempvw5 (c1 varchar(7), c2 integer, c3 varchar(7), c4 integer,
    #                         c5 varchar(7), c6 integer, c7 varchar(7), c8 integer)
    #   no partition;
    
    ##expect any *--- SQL operation complete.*
    #   create view view5 as select * from tempvw5 for protection;
    #
    ##expect any *--- 1 row(s) inserted.*
    #  insert into view5
    #      select max(t1.vch7), count(t1.chu3)
    #           , max(t2.vch7), count(t2.chu3)
    #           , max(t3.vch7), count(t3.chu3)
    #           , max(t4.vch7), count(t4.chu3)
    #      from tab1 t1
    #      join tab2 t2 on t1.vch7 = t2.vch7
    #      left join tab3 t3 on t2.vch7 = t3.vch7
    #      left join tab4 t4 on t3.vch7 = t4.vch7
    #   ;
    
    ##expectfile ${test_dir}/a14sexp a14ss17
    #   select * from view5 ;
    
    ##endtt
    
