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
    
def test001(desc="""Uncorrelated subquery in having clause test"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     A01
    #  Description:        SELECT ... HAVING ... IN ... SUBQUERY
    #                      Uncorrelated subquery in having clause test
    #                      tests the use of the IN operator connecting
    #                      the outer query with the subquery.
    #                      Vary attributes as described in testunit
    #                      comments above.  Test the use of NOT IN.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    #  Notes:
    #  This test case incorporates features detailed in the "Title"
    #  by Ima Programmer (Version 1.1, <date>).
    #
    # =================== End Test Case Header  ===================
    
    # Get supplier numbers for suppliers who supply part 4102.
    
    # set param ?p 4102;
    
    stmt = """set param ?p  4100;"""
    output = _dci.cmdexec(stmt)
    stmt = """select suppnum
from """ + gvars.g_schema_arkcasedb + """.supplier 
group by suppnum
having suppnum in
(select suppnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where partnum = ( ?p + 2 )
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s0')
    
    # Get supplier numbers for suppliers who DON'T supply part 4102.
    stmt = """set param ?p   4102;"""
    output = _dci.cmdexec(stmt)
    stmt = """select suppnum
from """ + gvars.g_schema_arkcasedb + """.supplier 
group by suppnum
having suppnum NOT in
(select suppnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where partnum = ?p
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s1')
    
    #  Get employee numbers who are regional managers (notice no >
    #  where clause in subquery)
    stmt = """select empnum
from """ + gvars.g_schema_arkcasedb + """.employee 
group by empnum
having empnum in
(select manager
from """ + gvars.g_schema_arkcasedb + """.region)
order by empnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s2')
    
    #  get part numbers, for parts supplied by supplier 15
    #  and supplied by at least one other supplier.
    stmt = """set param  ?p 15;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param  ?p1 30;"""
    output = _dci.cmdexec(stmt)
    stmt = """select partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where suppnum <> ?p
group by partnum
having partnum in
(select partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where suppnum = ( ?p1 / 2) );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s3')
    
    #  get part numbers, for parts supplied by supplier 15
    #  and supplied by at least one other supplier, eliminate
    #  duplicate part numbers
    stmt = """set param  ?p 15;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p1 5;"""
    output = _dci.cmdexec(stmt)
    stmt = """select distinct partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where suppnum <> ?p
group by partnum
having partnum in
(select partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where suppnum = (?p1 * 3 ) )
order by partnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s4')
    
    #   same as above, only use aliases.
    stmt = """select distinct partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup X
where X.suppnum <> ?p
group by partnum
having X.partnum in
(select Y.partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup Y
where suppnum = ?p)
order by partnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s5')
    
    #  get salesman numbers and order numbers for salesman
    #  who have orders for parts costing > 50000
    stmt = """set param ?p 50000;"""
    output = _dci.cmdexec(stmt)
    stmt = """select salesman,ordernum
from """ + gvars.g_schema_arkcasedb + """.orders 
group by ordernum, salesman
having  """ + gvars.g_schema_arkcasedb + """.orders.ordernum in
(select  """ + gvars.g_schema_arkcasedb + """.odetail.ordernum
from """ + gvars.g_schema_arkcasedb + """.odetail,""" + gvars.g_schema_arkcasedb + """.parts 
where  """ + gvars.g_schema_arkcasedb + """.odetail.partnum =  """ + gvars.g_schema_arkcasedb + """.parts.partnum
and price > ?p);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s6')
    
    #   get salesman numbers who have orders for parts prices > 50000
    #   (eliminate duplicate salesman numbers and order numbers)
    stmt = """select distinct salesman
from """ + gvars.g_schema_arkcasedb + """.orders 
group by salesman,ordernum
having ordernum in
(select distinct ordernum
from """ + gvars.g_schema_arkcasedb + """.odetail,""" + gvars.g_schema_arkcasedb + """.parts 
where  """ + gvars.g_schema_arkcasedb + """.odetail.partnum =  """ + gvars.g_schema_arkcasedb + """.parts.partnum
and price > ?p );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s7')
    
    #   get parts numbers with a cost > 10000
    stmt = """select partnum
from """ + gvars.g_schema_arkcasedb + """.parts 
group by partnum
having partnum in
(select partnum
from """ + gvars.g_schema_arkcasedb + """.expfroms);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s8')
    
    #  get supplier numbers for suppliers who are in the same
    #  state as supplier 1. (This tests the use of IN with a
    #  subquery that returns only one record).
    stmt = """set param ?p 2;"""
    output = _dci.cmdexec(stmt)
    stmt = """select suppnum
from """ + gvars.g_schema_arkcasedb + """.supplier 
group by state, suppnum
having state IN
(select state
from """ + gvars.g_schema_arkcasedb + """.supplier 
where suppnum = (?p - 1 ));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s9')
    
    _testmgr.testcase_end(desc)

def test002(desc="""SELECT, HAVING (<,<=,=,<>,>,>=) SUBQUERY"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     A02
    #  Description:        Simple comparison operators:
    #                      SELECT ... HAVING ...
    #                      (<,<=,=,<>,>,>=) ... SUBQUERY
    #                      Uncorrelated subquery in having clause test
    #                      - this tests the use of simple comparison
    #                      operators (<,<=,=,<>,.,>=) connecting the outer
    #                      query with the subquery. Note that the subquery
    #                      can return at most one record.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    #  Notes:
    #  This test case incorporates features detailed in the "Title"
    #  by Ima Programmer (Version 1.1, <date>).
    #
    # =================== End Test Case Header  ===================
    
    # get supplier numbers for suppliers who are in the same state
    # as supplier 1.
    
    stmt = """set param ?p 1;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select suppnum
from """ + gvars.g_schema_arkcasedb + """.supplier 
group by suppnum, state
having state =
(select state
from """ + gvars.g_schema_arkcasedb + """.supplier 
where suppnum = (2 - ?p) )
order by suppnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s0')
    
    # get supplier numbers for suppliers who are in the same state
    # as supplier 1 (use aliases).
    stmt = """set param ?p 1;"""
    output = _dci.cmdexec(stmt)
    stmt = """select suppnum
from """ + gvars.g_schema_arkcasedb + """.supplier X
group by suppnum, X.state
having X.state =
(select Y.state
from """ + gvars.g_schema_arkcasedb + """.supplier Y
where suppnum = ?p)
order by suppnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s1')
    
    # get partnumbers for parts whose cost is 6000, and are not
    # supplied by supplier #10.
    stmt = """set param ?p 6000;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p1 5;"""
    output = _dci.cmdexec(stmt)
    stmt = """select partnum
from """ + gvars.g_schema_arkcasedb + """.parts 
group by partnum
having partnum =
(select distinct partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where partcost = ?p
and suppnum <> (?p1 * 2) )
order by partnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s2')
    
    # get customer numbers for customers who have not ordered parts
    # stored at location 'V67'
    stmt = """set param ?p 'V67';"""
    output = _dci.cmdexec(stmt)
    stmt = """select custnum
from """ + gvars.g_schema_arkcasedb + """.customer 
group by custnum
having custnum <>
(select col_12
from """ + gvars.g_schema_arkcasedb + """.partsfor 
where col_2 = ?p )
order by custnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s3')
    
    #  get customer numbers for customers who have not ordered parts
    #  stored at location 'V67', order by customer number
    stmt = """select custnum
from """ + gvars.g_schema_arkcasedb + """.customer 
group by custnum
having custnum <>
(select col_12
from """ + gvars.g_schema_arkcasedb + """.partsfor 
where col_2 = ?p )
order by custnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s4')
    
    #  same as first, only use a join instead of the view partsfor
    stmt = """select custnum
from """ + gvars.g_schema_arkcasedb + """.customer 
group by custnum
having custnum <>
(select custnum
from """ + gvars.g_schema_arkcasedb + """.orders, """ + gvars.g_schema_arkcasedb + """.odetail, """ + gvars.g_schema_arkcasedb + """.parts 
where
( """ + gvars.g_schema_arkcasedb + """.orders.ordernum =  """ + gvars.g_schema_arkcasedb + """.odetail.ordernum) and
( """ + gvars.g_schema_arkcasedb + """.odetail.partnum =  """ + gvars.g_schema_arkcasedb + """.parts.partnum) and
(location = ?p ))
order by custnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s5')
    
    # same as first, but eliminate customers in Texas
    stmt = """set param ?p1 'Texas';"""
    output = _dci.cmdexec(stmt)
    stmt = """select custnum
from """ + gvars.g_schema_arkcasedb + """.customer 
where state <> ?p1
group by custnum
having custnum <>
(select col_12
from """ + gvars.g_schema_arkcasedb + """.partsfor 
where col_2 = ?p )
order by custnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s6')
    
    # get supplier numbers whose price for part #4102 is less
    # than or equal to supplier number 8
    stmt = """set param ?p  4102;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p1 8;"""
    output = _dci.cmdexec(stmt)
    stmt = """select suppnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
group by suppnum,partnum,partcost
having partcost <=
(select partcost
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where partnum = ?p
and suppnum = ?p1 )
AND partnum = ?p
order by suppnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s7')
    
    #  same as above, but AND condition before the subquery
    stmt = """select suppnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
group by suppnum,partnum,partcost
having partnum = ?p
and partcost <=
(select partcost
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where partnum = ?p
and suppnum = ?p1)
order by suppnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s8')
    
    _testmgr.testcase_end(desc)

def test003(desc="""Quantified comparison operators: >=ANY,=ALL,etc."""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     A03
    #  Description:        Quantified comparison operators: >=ANY,=ALL,etc.
    #                      Uncorrelated subquery in having clause test case
    #                      - this tests the use of the quantified comparison
    #                      operators (=ANY,>=ALL,etc.). These operators can
    #                      be used with subqueries that return sets, not just
    #                      single records.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    #  Notes:
    #  This test case incorporates features detailed in the "Title"
    #  by Ima Programmer (Version 1.1, <date>).
    #
    # =================== End Test Case Header  ===================
    
    #  get supplier numbers for suppliers who supply part 4102
    stmt = """set param ?p 4102;"""
    output = _dci.cmdexec(stmt)
    stmt = """select suppnum
from """ + gvars.g_schema_arkcasedb + """.supplier 
group by suppnum
having suppnum =ANY
(select suppnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where partnum = ?p )
order by suppnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s0')
    
    #   same as above , with SOME instead of ANY
    #  ?p is set to 4102
    stmt = """select suppnum
from """ + gvars.g_schema_arkcasedb + """.supplier 
group by suppnum
having suppnum =SOME
(select suppnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where partnum = ?p )
order by suppnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s1')
    
    #   Get supplier numbers for suppliers who DON'T supply part 4102.
    #  ?p is set to 4102
    stmt = """select suppnum
from """ + gvars.g_schema_arkcasedb + """.supplier 
group by suppnum
having suppnum =ANY
(select suppnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where partnum = ?p
)
order by suppnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s2')
    
    #   Get supplier names for suppliers who DON'T supply part 4102.
    #  ?p is set to 4102
    stmt = """select suppnum
from """ + gvars.g_schema_arkcasedb + """.supplier 
group by suppnum
having suppnum =ANY
(select suppnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where partnum = ?p
)
order by suppnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s3')
    
    #   Get supplier names for suppliers who DON'T supply part 4102.
    #  ?p is set to 4102
    stmt = """select suppnum
from """ + gvars.g_schema_arkcasedb + """.supplier 
group by suppnum
having suppnum <>SOME
(select suppnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where partnum = ?p
)
order by suppnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s4')
    
    #   Get employee numbers who are regional managers (notice no
    #   where clause in subquery)
    stmt = """select empnum
from """ + gvars.g_schema_arkcasedb + """.employee 
group by empnum
having empnum =ANY
(select manager
from """ + gvars.g_schema_arkcasedb + """.region)
order by empnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s5')
    
    #  get part numbers, for parts supplied by supplier 15
    #  and supplied by at least one other supplier
    # param ?p2 is set to 15.
    stmt = """set param ?p2 15;"""
    output = _dci.cmdexec(stmt)
    stmt = """select partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where suppnum <> ?p2
group by partnum
having partnum in
(select partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where suppnum = ?p2 )
order by partnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s6')
    
    #   get part numbers, for parts supplied by supplier 15
    #   and supplied by at least one other supplier, eliminate
    #   duplicate part numbers
    #  param ?p2 is set to 15.
    stmt = """select distinct partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where suppnum <> ?p2
group by partnum
having partnum in
(select partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where suppnum = ?p2)
order by partnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s7')
    
    #   same as above, only use aliases.
    #  param ?p2 is set to 15.
    stmt = """select distinct partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup X
where X.suppnum <> ?p2
group by partnum
having X.partnum in
(select Y.partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup Y
where suppnum = ?p2 )
order by partnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s8')
    
    #  get salesman numbers and order numbers for salesman
    #  who have orders for parts costing > 50000
    # param ?p is set to 50000;
    stmt = """set param ?p 50000;"""
    output = _dci.cmdexec(stmt)
    stmt = """select salesman,ordernum
from """ + gvars.g_schema_arkcasedb + """.orders 
group by ordernum,salesman
having  """ + gvars.g_schema_arkcasedb + """.orders.ordernum =SOME
(select  """ + gvars.g_schema_arkcasedb + """.odetail.ordernum
from """ + gvars.g_schema_arkcasedb + """.odetail, """ + gvars.g_schema_arkcasedb + """.parts 
where  """ + gvars.g_schema_arkcasedb + """.odetail.partnum =  """ + gvars.g_schema_arkcasedb + """.parts.partnum
and price > ?p )
order by ordernum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s9')
    
    #   get salesman numbers who have orders for parts prices > 50000
    #   (eliminate duplicate salesman numbers and order numbers)
    #  param ?p is set to 5000;
    stmt = """select distinct salesman
from """ + gvars.g_schema_arkcasedb + """.orders 
group by ordernum,salesman
having ordernum =ANY
(select distinct ordernum
from """ + gvars.g_schema_arkcasedb + """.odetail, """ + gvars.g_schema_arkcasedb + """.parts 
where  """ + gvars.g_schema_arkcasedb + """.odetail.partnum =  """ + gvars.g_schema_arkcasedb + """.parts.partnum
and price > ?p )
order by salesman;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s10')
    
    #   get part numbers with a cost > 10000
    stmt = """select partnum
from """ + gvars.g_schema_arkcasedb + """.parts 
group by partnum
having partnum =SOME
(select partnum
from """ + gvars.g_schema_arkcasedb + """.expfroms)
order by partnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s11')
    
    #  get supplier numbers for suppliers who are in the same
    #  state as supplier 1. (This tests the use of =ANY with a
    #  subquery that returns only one record).
    # param ?p is set to 1;
    stmt = """set param ?p 1;"""
    output = _dci.cmdexec(stmt)
    stmt = """select suppnum
from """ + gvars.g_schema_arkcasedb + """.supplier 
group by state, suppnum
having state =ANY
(select state
from """ + gvars.g_schema_arkcasedb + """.supplier 
where suppnum = ?p)
order by suppnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s12')
    
    #  get supplier numbers whose price for part 4102 is less
    #  than some other supplier who supplies part 4102
    # param ?p is set to 4102;
    stmt = """set param ?p 4102;"""
    output = _dci.cmdexec(stmt)
    stmt = """select suppnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
group by suppnum, partnum, partcost
having partcost <SOME
(select partcost
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where partnum = ?p)
and partnum = ?p
order by suppnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s13')
    
    #   same as above, with ANY instead of SOME
    #  param ?p is set to 4102;
    stmt = """select suppnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
group by suppnum, partnum, partcost
having partcost <ANY
(select partcost
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where partnum = ?p )
and partnum = ?p
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s14')
    
    #   get supplier numbers whose price for part 4102 is less
    #   than or equal to ALL suppliers who supply part 4102
    #  param ?p is set to 4102;
    stmt = """select suppnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
group by suppnum,partnum,partcost
having partcost <=ALL
(select partcost
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where partnum = ?p )
and partnum = ?p
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s15')
    
    #  get supplier numbers who are in the same state as supplier
    #  1 (this tests the use of =ALL with a subquery that only
    #  returns one record).
    # param ?p is set to 1.
    stmt = """set param ?p 1;"""
    output = _dci.cmdexec(stmt)
    stmt = """select suppnum
from """ + gvars.g_schema_arkcasedb + """.supplier 
group by state, suppnum
having state =ALL
(select state
from """ + gvars.g_schema_arkcasedb + """.supplier 
where suppnum = ?p)
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s16')
    
    #  get the salesmans' empnum (if any) who has the only order
    #  where at least one part has been ordered in quanities > 25
    # set param ?p to 25;
    stmt = """set param ?p 25;"""
    output = _dci.cmdexec(stmt)
    stmt = """select salesman
from """ + gvars.g_schema_arkcasedb + """.orders 
group by salesman, ordernum
having ordernum =ALL
(select ordernum
from """ + gvars.g_schema_arkcasedb + """.odetail 
where quantity > ?p )
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s17')
    
    #  same as previous, with where ordernum > 100
    # set param ?p1 to 100;
    # param ?p is set to 25;
    stmt = """set param ?p1 100;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p 25;"""
    output = _dci.cmdexec(stmt)
    stmt = """select salesman
from """ + gvars.g_schema_arkcasedb + """.orders 
where ordernum > ?p1
group by salesman, ordernum
having ordernum =ALL
(select ordernum
from """ + gvars.g_schema_arkcasedb + """.odetail 
where quantity > ?p)
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s18')
    
    #  same as first, but with 'select DISTINCT ordernum'
    # param ?p is set to 25;
    stmt = """set param ?p 25;"""
    output = _dci.cmdexec(stmt)
    stmt = """select salesman
from """ + gvars.g_schema_arkcasedb + """.orders 
group by salesman, ordernum
having ordernum =ALL
(select distinct ordernum
from """ + gvars.g_schema_arkcasedb + """.odetail 
where quantity > ?p)
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s19')
    
    #   get supplier names whose state is not equal to some
    #   customer state
    stmt = """select S.suppname
from """ + gvars.g_schema_arkcasedb + """.supplier S
group by state, suppname
having state <>ANY
(select C.state
from """ + gvars.g_schema_arkcasedb + """.customer C)
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s20')
    
    #   get supplier names whose state is not equal to ALL
    #   customer states
    stmt = """select suppname
from """ + gvars.g_schema_arkcasedb + """.supplier 
group by state, suppname
having state <>ALL
(select state
from """ + gvars.g_schema_arkcasedb + """.customer)
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s21')
    
    #  same as above, add group by,having clauses
    # param ?p is set to 'Texas'
    stmt = """set param ?p 'Texas';"""
    output = _dci.cmdexec(stmt)
    stmt = """select suppname
from """ + gvars.g_schema_arkcasedb + """.supplier 
group by state, suppname
having state <>ALL
(select state
from """ + gvars.g_schema_arkcasedb + """.customer 
group by state
having state <> ?p )
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s22')
    
    #   get the salesmens' names who sold the part whose price
    #   is greater than or equal to all parts
    stmt = """select col_11
from """ + gvars.g_schema_arkcasedb + """.partsfor 
group by col_11, col_3
having col_3 >=ALL
(select col_3
from """ + gvars.g_schema_arkcasedb + """.partsfor)
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s23')
    
    _testmgr.testcase_end(desc)

def test004(desc="""Multiple nested subqueries, multiple subqueries"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     A04
    #  Description:        Multiple nested subqueries, multiple subqueries
    #                      connected with AND,OR, and SELECTs with subqueries
    #                      (uncorrelated) in both the WHERE clause and HAVING
    #                      clause
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    #  Notes:
    #  This test case incorporates features detailed in the "Title"
    #  by Ima Programmer (Version 1.1, <date>).
    #
    # =================== End Test Case Header  ===================
    #
    
    #
    # -------------------------------
    # Open a Log file
    # -------------------------------
    # -------------------------------
    #  get supplier numbers for suppliers who supply part 4102 (?p)
    #  and part 5504 (?p2)
    stmt = """set param ?p 4102;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p2 5504;"""
    output = _dci.cmdexec(stmt)
    stmt = """select suppnum
from """ + gvars.g_schema_arkcasedb + """.supplier 
group by suppnum
having (suppnum in
(select suppnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where partnum = ?p))
and (suppnum =ANY
(select suppnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where partnum = ?p2))
order by suppnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s0')
    
    #   get supplier numbers for suppliers who supply part 4102 (?p)
    #   and part 5504 (?p2) - replace AND condition in having clause
    #   with a where clause
    stmt = """select suppnum
from """ + gvars.g_schema_arkcasedb + """.supplier 
where suppnum =ANY
(select suppnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where partnum = ?p2
)
group by suppnum
having suppnum in
(select suppnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where partnum = ?p
)
order by suppnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s1')
    
    #   get supplier numbers for suppliers who supply part 4102 (?p)
    #   OR 5504 (?p2)  -- same as above, replace 'and' with 'or'
    stmt = """select suppnum
from """ + gvars.g_schema_arkcasedb + """.supplier 
group by suppnum
having (suppnum in
(select suppnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where partnum = ?p))
or (suppnum =ANY
(select suppnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where partnum = ?p2))
order by suppnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s2')
    
    #   get supplier numbers for suppliers who DON'T supply parts
    #   4102 (?p) or 5504 (?p2)-- same as previous, add NOT before entire
    #   predicate.
    stmt = """select suppnum
from """ + gvars.g_schema_arkcasedb + """.supplier 
group by suppnum
having NOT ((suppnum in
(select suppnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where partnum = ?p ))
or (suppnum =ANY
(select suppnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where partnum = ?p2 )))
order by suppnum ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s3')
    
    #   get supplier numbers for suppliers who DON'T supply parts
    #   4102(?p) or 5504(?p2) -- same as previous, but use both a subquery
    #   in a where clause and in a having clause.
    stmt = """select suppnum
from """ + gvars.g_schema_arkcasedb + """.supplier 
where suppnum <>ANY
(select suppnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where partnum = ?p2
)
group by suppnum
having suppnum NOT in
(select suppnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where partnum = ?p
)
order by suppnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s4')
    
    #  get supplier numbers for suppliers who supply parts 4102(?p),
    #  5504(?p2), and 5505(?p1).
    stmt = """set param ?p1 5505;"""
    output = _dci.cmdexec(stmt)
    stmt = """select suppnum
from """ + gvars.g_schema_arkcasedb + """.supplier 
group by suppnum
having (suppnum in
(select suppnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where partnum = ?p))
and (suppnum =ANY
(select suppnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where partnum = ?p2 ))
and (suppnum =SOME
(select suppnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where partnum = ?p1 ))
order by suppnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s5')
    
    #  get employee numbers who have salary >= 30000 and age < 30
    #  ?p = 30000 and ?p1 = 30;
    #EL 12/15/97
    stmt = """set param ?p  30000;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p1 30;"""
    output = _dci.cmdexec(stmt)
    stmt = """select empnum
from """ + gvars.g_schema_arkcasedb + """.emppub 
group by empnum
having empnum in
(select empnum
from """ + gvars.g_schema_arkcasedb + """.employee 
where salary >= ?p )
and empnum in
(select empnum
from """ + gvars.g_schema_arkcasedb + """.employee 
-- EL 12/15/97
--         where age < ?p)
where age < ?p1)
order by empnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s6')
    
    #  get job titles for employees who work in the Chicago branch
    #  of the Central region, excluding programmers, order by job title  b
    # ?p = 'PROGRAMMER'
    # ?p1 = 'CENTRAL'
    # ?p2 = 'CHICAGO'
    stmt = """set param ?p 'PROGRAMMER';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p1 'CENTRAL';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p2 'CHICAGO';"""
    output = _dci.cmdexec(stmt)
    stmt = """select job
from """ + gvars.g_schema_arkcasedb + """.employee 
where job <> ?p
group by job, regnum, branchnum
having (regnum  in
(select regnum
from """ + gvars.g_schema_arkcasedb + """.region 
where regname = ?p1))
and (branchnum in
(select branchnum
from """ + gvars.g_schema_arkcasedb + """.branch 
where branchname = ?p2
group by branchnum))
order by job;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s7')
    
    #  get supplier numbers for suppliers who supply at least
    #  one part whose inventory is negative (less than 0)
    stmt = """set param ?p 0;"""
    output = _dci.cmdexec(stmt)
    stmt = """select suppnum
from """ + gvars.g_schema_arkcasedb + """.supplier 
group by suppnum
having suppnum in
(select suppnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
group by suppnum,partnum
having partnum in
(select partnum
from """ + gvars.g_schema_arkcasedb + """.parts 
where inventory < ?p )
)
order by suppnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s8')
    
    #  get supplier numbers for suppliers who supply at least
    #  one part whose inventory is negative (less than 0) - use
    #  subquery in having clause , subquery in where clause (mixed)
    stmt = """set param ?p 0;"""
    output = _dci.cmdexec(stmt)
    stmt = """select suppnum
from """ + gvars.g_schema_arkcasedb + """.supplier 
group by suppnum
having suppnum in
(select suppnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where partnum in
(select partnum
from """ + gvars.g_schema_arkcasedb + """.parts 
where inventory < ?p)
)
order by suppnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s9')
    
    #  get supplier names for suppliers who supply at least
    #  one part whose inventory is negative (less than 0) - use
    #  subquery in having clause, subquery in where clause (mixed)
    stmt = """set param ?p 0;"""
    output = _dci.cmdexec(stmt)
    stmt = """select suppname
from """ + gvars.g_schema_arkcasedb + """.supplier 
where suppnum in
(select suppnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
group by suppnum,partnum
having partnum in
(select partnum
from """ + gvars.g_schema_arkcasedb + """.parts 
where inventory < ?p )
)
order by suppname;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s10')
    
    #  same as first, except use =SOME instead of IN
    stmt = """set param ?p 0;"""
    output = _dci.cmdexec(stmt)
    stmt = """select suppnum
from """ + gvars.g_schema_arkcasedb + """.supplier 
group by suppnum
having suppnum =SOME
(select suppnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
group by suppnum,partnum
having partnum =ANY
(select partnum
from """ + gvars.g_schema_arkcasedb + """.parts 
where inventory < ?p )
)
order by suppnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s11')
    
    #  get supplier numbers for suppliers who supply part 'LP__900_LPM'
    # ?p = 'LP__900_LPM'
    stmt = """set param ?p 'LP  900 LPM';"""
    output = _dci.cmdexec(stmt)
    stmt = """select suppnum
from """ + gvars.g_schema_arkcasedb + """.supplier 
group by suppnum
having suppnum IN
(select suppnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
group by suppnum, partnum
having partnum =
(select partnum
from """ + gvars.g_schema_arkcasedb + """.parts 
where partname = ?p))
order by suppnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s12')
    
    #   get supplier numbers for suppliers who supply part 'LP__900_LPM'
    #  ?p = 'LP__900_LPM'
    stmt = """select suppnum
from """ + gvars.g_schema_arkcasedb + """.supplier 
group by suppnum
having suppnum IN
(select suppnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where partnum =
(select partnum
from """ + gvars.g_schema_arkcasedb + """.parts 
where partname = ?p ))
order by suppnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s13')
    
    #   get supplier names for suppliers who supply part 'LP__900_LPM'
    #  ?p = 'LP__900_LPM'
    stmt = """select suppname
from """ + gvars.g_schema_arkcasedb + """.supplier 
where suppnum IN
(select suppnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
group by suppnum, partnum
having partnum =
(select partnum
from """ + gvars.g_schema_arkcasedb + """.parts 
where partname = ?p ))
order by suppname;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s14')
    
    #   get age of those employees whose salary is less than or
    #   equal to the salary of the youngest employee
    stmt = """select age
from """ + gvars.g_schema_arkcasedb + """.employee 
group by age, salary
having salary <=
(select salary
from """ + gvars.g_schema_arkcasedb + """.employee 
group by age, salary
having age <= ALL
(select age
from """ + gvars.g_schema_arkcasedb + """.employee 
)
)
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s15')
    
    #   get age of those employees whose salary is less than or
    #   equal to the salary of the youngest employee
    stmt = """select age
from """ + gvars.g_schema_arkcasedb + """.employee 
group by age, salary
having salary <=
(select salary
from """ + gvars.g_schema_arkcasedb + """.employee 
where age <= ALL
(select age
from """ + gvars.g_schema_arkcasedb + """.employee 
)
)
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s16')
    
    #   get age of those employees whose salary is less than or
    #   equal to the salary of the youngest employee
    stmt = """select age
from """ + gvars.g_schema_arkcasedb + """.employee 
where salary <=
(select salary
from """ + gvars.g_schema_arkcasedb + """.employee 
group by age, salary
having age <= ALL
(select age
from """ + gvars.g_schema_arkcasedb + """.employee 
)
)
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s17')
    
    #   get age of those employees whose salary is less than or
    #   equal to the salary of the youngest employee
    stmt = """select X.age
from """ + gvars.g_schema_arkcasedb + """.employee X
group by age, salary
having X.salary <=
(select salary
from """ + gvars.g_schema_arkcasedb + """.employee Y
group by age, salary
having Y.age <= ALL
(select Z.age
from """ + gvars.g_schema_arkcasedb + """.employee Z
)
)
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s18')
    
    #  get salesman names who have  for parts priced < 8000
    #  (eliminate duplicate salesman names,order numbers, and
    #  records where the price = 8000)
    # ?p = 8000;
    stmt = """set param ?p 8000;"""
    output = _dci.cmdexec(stmt)
    stmt = """select distinct salesman
from """ + gvars.g_schema_arkcasedb + """.orders 
group by salesman, ordernum
having ordernum in
(select distinct ordernum
from """ + gvars.g_schema_arkcasedb + """.odetail, """ + gvars.g_schema_arkcasedb + """.parts 
group by """ + gvars.g_schema_arkcasedb + """.odetail.ordernum,  """ + gvars.g_schema_arkcasedb + """.odetail.partnum,
 """ + gvars.g_schema_arkcasedb + """.parts.partnum, """ + gvars.g_schema_arkcasedb + """.parts.price
having  """ + gvars.g_schema_arkcasedb + """.odetail.partnum =  """ + gvars.g_schema_arkcasedb + """.parts.partnum
and price <
(select distinct price
from """ + gvars.g_schema_arkcasedb + """.parts 
where price = ?p ))
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s19')
    
    #  get salesman names who have orders for parts priced < 8000
    #  (eliminate duplicate salesman names,order numbers, and
    #  records where the price = 8000)
    # ?p = 8000
    stmt = """set param ?p 8000;"""
    output = _dci.cmdexec(stmt)
    stmt = """select distinct salesman
from """ + gvars.g_schema_arkcasedb + """.orders 
group by salesman, ordernum
having ordernum in
(select distinct ordernum
from """ + gvars.g_schema_arkcasedb + """.odetail, """ + gvars.g_schema_arkcasedb + """.parts 
where  """ + gvars.g_schema_arkcasedb + """.odetail.partnum =  """ + gvars.g_schema_arkcasedb + """.parts.partnum
group by ordernum, price
having price <
(select distinct price
from """ + gvars.g_schema_arkcasedb + """.parts 
where price = ?p ))
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s20')
    
    #  get customer numbers who have  for parts supplied by
    #  suppliers in MASS.
    # ?p = 'MASS'
    stmt = """set param ?p 'MASS';"""
    output = _dci.cmdexec(stmt)
    stmt = """select custnum
from """ + gvars.g_schema_arkcasedb + """.customer 
group by custnum
having custnum in
(select custnum
from """ + gvars.g_schema_arkcasedb + """.orders 
group by ordernum, custnum
having ordernum in
(select distinct ordernum
from """ + gvars.g_schema_arkcasedb + """.odetail 
group by ordernum, partnum
having partnum in
(select distinct partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
group by partnum, suppnum
having suppnum in
(select suppnum
from """ + gvars.g_schema_arkcasedb + """.supplier 
where state = ?p
)
)
)
)
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s21')
    
    #   get customer numbers who have  for parts supplied by
    #   suppliers in Mass.
    #  ?p = 'MASS'
    stmt = """select custnum
from """ + gvars.g_schema_arkcasedb + """.customer 
group by custnum
having custnum in
(select custnum
from """ + gvars.g_schema_arkcasedb + """.orders 
where ordernum in
(select distinct ordernum
from """ + gvars.g_schema_arkcasedb + """.odetail 
group by ordernum, partnum
having partnum in
(select distinct partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where suppnum in
(select suppnum
from """ + gvars.g_schema_arkcasedb + """.supplier 
where state = ?p
)
)
)
)
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s22')
    
    #   get customer names who have  for parts supplied by
    #   suppliers in Mass.
    #  ?p = 'MASS'
    stmt = """select custname
from """ + gvars.g_schema_arkcasedb + """.customer 
where custnum in
(select custnum
from """ + gvars.g_schema_arkcasedb + """.orders 
group by ordernum, custnum
having ordernum in
(select distinct ordernum
from """ + gvars.g_schema_arkcasedb + """.odetail 
group by ordernum, partnum
having partnum in
(select distinct partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
group by partnum, suppnum
having suppnum in
(select suppnum
from """ + gvars.g_schema_arkcasedb + """.supplier 
where state = ?p
)
)
)
)
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s23')
    
    #  get customer numbers who have  for parts supplied by
    #  suppliers in Mass, where the order month is less than 4
    # ?p = 'MASS'
    # ?p1 = 4;
    stmt = """set param ?p1 4;"""
    output = _dci.cmdexec(stmt)
    stmt = """select custnum
from """ + gvars.g_schema_arkcasedb + """.customer 
group by custnum
having custnum in
(select custnum
from """ + gvars.g_schema_arkcasedb + """.orders 
where ordernum in
(select distinct ordernum
from """ + gvars.g_schema_arkcasedb + """.odetail 
group by ordernum, partnum
having partnum in
(select distinct partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
group by partnum, suppnum
having suppnum in
(select suppnum
from """ + gvars.g_schema_arkcasedb + """.supplier 
where state = ?p
)
)
)
and omonth < ?p1
)
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s24')
    
    #  get salesman names for salesman who work in the Central region
    # ?p = 'CENTRAL'
    stmt = """set param ?p  'CENTRAL';"""
    output = _dci.cmdexec(stmt)
    stmt = """select empname
from """ + gvars.g_schema_arkcasedb + """.salecust 
group by empname
having empname in
(select empname
from """ + gvars.g_schema_arkcasedb + """.emppub 
group by empname, regnum
having regnum in
(select regnum
from """ + gvars.g_schema_arkcasedb + """.region 
where regname = ?p
)
)
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s25')
    
    #  get supplier numbers for suppliers who supply at least
    #  one part whose inventory is negative, eliminate duplicates
    #  with group by
    # ?p1 = 0
    stmt = """set param ?p1 0;"""
    output = _dci.cmdexec(stmt)
    stmt = """select suppnum
from """ + gvars.g_schema_arkcasedb + """.supplier 
group by suppnum
having suppnum in
(select suppnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where partnum in
(select partnum
from """ + gvars.g_schema_arkcasedb + """.parts 
where inventory < ?p1)
group by suppnum
)
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s26')
    
    #  same as above, but eliminate supplier #2
    # ?p2 = 2
    # ?p1 = 0
    stmt = """set param ?p2 2;"""
    output = _dci.cmdexec(stmt)
    stmt = """select suppnum
from """ + gvars.g_schema_arkcasedb + """.supplier 
group by suppnum
having suppnum in
(select suppnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where partnum in
(select partnum
from """ + gvars.g_schema_arkcasedb + """.parts 
where inventory < ?p1)
group by suppnum
having suppnum <> ?p2
)
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s27')
    
    #  get age of those employees who are not 22 and whose salary
    #  is less than or equal to the salary of the youngest employee
    #  under 40.
    # ?p = 22;
    # ?p1 = 40
    stmt = """set param ?p 22;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p1 40;"""
    output = _dci.cmdexec(stmt)
    stmt = """select age
from """ + gvars.g_schema_arkcasedb + """.employee 
where age <> ?p
group by age, salary
having salary <=
(select salary
from """ + gvars.g_schema_arkcasedb + """.employee 
group by salary, age
having age <=ALL
(select age
from """ + gvars.g_schema_arkcasedb + """.employee 
group by age
having age < ?p1
)
)
order by age;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s28')
    
    # 04/27/00 EL  Added following queries to test parameters.
    
    stmt = """prepare s from
select age from """ + gvars.g_schema_arkcasedb + """.employee where age <> ?;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute s using 39;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s29')
    
    stmt = """prepare n from
select age from """ + gvars.g_schema_arkcasedb + """.employee;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute n using ?p;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s30')
    
    stmt = """prepare n1 from
select age from """ + gvars.g_schema_arkcasedb + """.employee where age <> ?;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute n1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '29464')
    
    stmt = """prepare n2 from
select age from """ + gvars.g_schema_arkcasedb + """.employee where age <> ? and salary = ?;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute n2 using 40;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '29464')
    
    _testmgr.testcase_end(desc)

def test005(desc="""Subqueries with for read uncommitted"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     A05
    #  Description:        Subqueries with for read uncommitted
    #                      access, read committed access and
    #                      serializable access.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    #  Notes:
    #  This test case incorporates features detailed in the "Title"
    #  by Ima Programmer (Version 1.1, <date>).
    #
    # =================== End Test Case Header  ===================
    
    #  get part numbers, for parts supplied by supplier 15
    #  and supplied by at least one other supplier.
    # ?p = 15;
    stmt = """set param ?p 15;"""
    output = _dci.cmdexec(stmt)
    stmt = """select partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where suppnum <> ?p
group by partnum
having partnum in
(select partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where suppnum = ?p
for read uncommitted access
)
for serializable access
order by partnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s0')
    
    #   get part numbers, for parts supplied by supplier 15
    #   and supplied by at least one other supplier.
    #  ?p = 15
    stmt = """select partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where suppnum <> ?p
group by partnum
having partnum in
(select partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where suppnum = ?p
for read committed access
)
for read uncommitted access
order by partnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s1')
    
    #   get part numbers, for parts supplied by supplier 15
    #   and supplied by at least one other supplier.
    #  ?p = 15
    stmt = """select partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where suppnum <> ?p
group by partnum
having partnum in
(select partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where suppnum = ?p
for serializable access
)
for read committed access
order by partnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s2')
    
    #  get salesman numbers and order numbers for salesman
    #  who have orders for parts costing > 50000
    # ?p = 50000;
    stmt = """set param ?p 50000;"""
    output = _dci.cmdexec(stmt)
    stmt = """select salesman,ordernum
from """ + gvars.g_schema_arkcasedb + """.orders 
group by ordernum, salesman
having """ + gvars.g_schema_arkcasedb + """.orders.ordernum in
(select  """ + gvars.g_schema_arkcasedb + """.odetail.ordernum
from """ + gvars.g_schema_arkcasedb + """.odetail, """ + gvars.g_schema_arkcasedb + """.parts 
where  """ + gvars.g_schema_arkcasedb + """.odetail.partnum =  """ + gvars.g_schema_arkcasedb + """.parts.partnum
and price > ?p
for serializable access
)
order by salesman, ordernum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s3')
    
    #  get supplier numbers for suppliers who are in the same state
    #  as supplier 1 (use aliases).
    # ?p = 1
    stmt = """set param ?p 1;"""
    output = _dci.cmdexec(stmt)
    stmt = """select suppnum
from """ + gvars.g_schema_arkcasedb + """.supplier X
group by suppnum, X.state
having X.state =
(select Y.state
from """ + gvars.g_schema_arkcasedb + """.supplier Y
where suppnum = ?p
for read uncommitted access
)
for serializable access
order by suppnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s4')
    
    #   get supplier numbers for suppliers who are in the same state
    #   as supplier 1 (use aliases).
    #  ?p = 1
    stmt = """select suppnum
from """ + gvars.g_schema_arkcasedb + """.supplier X
group by suppnum, X.state
having X.state =
(select Y.state
from """ + gvars.g_schema_arkcasedb + """.supplier Y
where suppnum = ?p
for read committed access
)
for read uncommitted access
order by suppnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s5')
    
    #   get supplier numbers for suppliers who are in the same state
    #   as supplier 1 (use aliases).
    #  ?p = 1
    stmt = """select suppnum
from """ + gvars.g_schema_arkcasedb + """.supplier X
group by suppnum, X.state
having X.state =
(select Y.state
from """ + gvars.g_schema_arkcasedb + """.supplier Y
where suppnum = ?p
for serializable access
)
for read committed access
order by suppnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s6')
    
    #  get customer numbers for customers who have not ordered parts
    #  stored at location 'V67'
    # ?p = 'V67'
    stmt = """set param ?p 'V67';"""
    output = _dci.cmdexec(stmt)
    stmt = """select custnum
from """ + gvars.g_schema_arkcasedb + """.customer 
group by custnum
having custnum <>
(select col_12
from """ + gvars.g_schema_arkcasedb + """.partsfor 
where col_2 = ?p
for read uncommitted access
)
order by custnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s7')
    
    #   get customer numbers for customers who have not ordered parts
    #   stored at location 'V67'
    #  ?p = 'V67'
    stmt = """select custnum
from """ + gvars.g_schema_arkcasedb + """.customer 
group by custnum
having custnum <>
(select col_12
from """ + gvars.g_schema_arkcasedb + """.partsfor 
where col_2 = ?p
for read committed access
)
order by custnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s8')
    
    #   get customer numbers for customers who have not ordered parts
    #   stored at location 'V67'
    #  ?p = 'V67'
    stmt = """select custnum
from """ + gvars.g_schema_arkcasedb + """.customer 
group by custnum
having custnum <>
(select col_12
from """ + gvars.g_schema_arkcasedb + """.partsfor 
where col_2 = ?p
for serializable access
)
order by custnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s9')
    
    #   same as above, only use a join instead of the view partsfor
    #  ?p = 'V67'
    stmt = """select custnum
from """ + gvars.g_schema_arkcasedb + """.customer 
group by custnum
having custnum <>
(select custnum
from """ + gvars.g_schema_arkcasedb + """.orders, """ + gvars.g_schema_arkcasedb + """.odetail, """ + gvars.g_schema_arkcasedb + """.parts 
where ( """ + gvars.g_schema_arkcasedb + """.orders.ordernum =  """ + gvars.g_schema_arkcasedb + """.odetail.ordernum) and
( """ + gvars.g_schema_arkcasedb + """.odetail.partnum =  """ + gvars.g_schema_arkcasedb + """.parts.partnum) and
(location = ?p )
for serializable access
)
order by custnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s10')
    
    #  get supplier numbers for suppliers who supply part 4102
    #  and part 5504
    # ?p = 4102
    # ?p1 = 5504
    stmt = """set param ?p 4102;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p1 5504;"""
    output = _dci.cmdexec(stmt)
    stmt = """select suppnum
from """ + gvars.g_schema_arkcasedb + """.supplier 
group by suppnum
having (suppnum in
(select suppnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where partnum = ?p
for read uncommitted access
)
)
and (suppnum =ANY
(select suppnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where partnum = ?p1
for read committed access
)
)
order by suppnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s11')
    
    #   get supplier numbers for suppliers who supply part 4102
    #   and part 5504
    #  ?p = 4102
    #  ?p1 = 5504
    stmt = """select suppnum
from """ + gvars.g_schema_arkcasedb + """.supplier 
group by suppnum
having (suppnum in
(select suppnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where partnum = ?p
for serializable access
)
)
and (suppnum =ANY
(select suppnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where partnum = ?p1
for read committed access
)
)
order by suppnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s12')
    
    #   get supplier numbers for suppliers who supply part 4102
    #   and part 5504
    #  ?p = 4102
    #  ?p1 = 5504
    stmt = """select suppnum
from """ + gvars.g_schema_arkcasedb + """.supplier 
group by suppnum
having (suppnum in
(select suppnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where partnum = ?p
for read uncommitted access
)
)
and (suppnum =ANY
(select suppnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where partnum = ?p1
for serializable access
)
)
order by suppnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s13')
    
    #  get supplier numbers for suppliers who supply at least
    #  one part whose inventory is negative (less than 0)
    # ?p = 0
    stmt = """set param ?p 0;"""
    output = _dci.cmdexec(stmt)
    stmt = """select suppnum
from """ + gvars.g_schema_arkcasedb + """.supplier 
group by suppnum
having suppnum in
(select suppnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
group by suppnum,partnum
having partnum in
(select partnum
from """ + gvars.g_schema_arkcasedb + """.parts 
where inventory < ?p
for read uncommitted access
)
for serializable access
)
for read committed access
order by suppnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s14')
    
    #   get age of those employees whose salary is less than or
    #   equal to the salary of the youngest employee
    stmt = """select X.age
from """ + gvars.g_schema_arkcasedb + """.employee X
group by age, salary
having X.salary <=
(select salary
from """ + gvars.g_schema_arkcasedb + """.employee Y
group by age, salary
having Y.age <= ALL
(select Z.age
from """ + gvars.g_schema_arkcasedb + """.employee Z
for serializable access
)
for read committed access
)
for read uncommitted access
order by 1  ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s15')
    
    #  get salesman names who have orders for parts priced < 8000
    #  (eliminate duplicate salesman names,order numbers, and
    #  records where the price = 8000)
    # ?p = 8000
    stmt = """set param ?p 8000;"""
    output = _dci.cmdexec(stmt)
    stmt = """select distinct salesman
from """ + gvars.g_schema_arkcasedb + """.orders 
group by salesman, ordernum
having ordernum in
(select distinct ordernum
from """ + gvars.g_schema_arkcasedb + """.odetail, """ + gvars.g_schema_arkcasedb + """.parts 
group by ordernum,  """ + gvars.g_schema_arkcasedb + """.odetail.partnum,
 """ + gvars.g_schema_arkcasedb + """.parts.partnum, price
having  """ + gvars.g_schema_arkcasedb + """.odetail.partnum =  """ + gvars.g_schema_arkcasedb + """.parts.partnum
and price <
(select distinct price
from """ + gvars.g_schema_arkcasedb + """.parts 
where price = ?p
for read uncommitted access
)
for serializable access
)
for read committed access
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s16')
    
    #  get salesman names for salesman who work in the Central region
    # ?p = 'CENTRAL'
    stmt = """set param ?p 'CENTRAL';"""
    output = _dci.cmdexec(stmt)
    stmt = """select empname
from """ + gvars.g_schema_arkcasedb + """.salecust 
group by empname
having empname in
(select empname
from """ + gvars.g_schema_arkcasedb + """.emppub 
group by empname, regnum
having regnum in
(select regnum
from """ + gvars.g_schema_arkcasedb + """.region 
where regname = ?p
for read committed access
)
for serializable access
)
for read uncommitted access
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s17')
    
    _testmgr.testcase_end(desc)

def test006(desc="""SELECT aggregate functions with aggregates in subquery"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     A06
    #  Description:        SELECT aggregate functions with aggregates in
    #                      subquery
    #                      Select uncorrelated subquery in HAVING clause
    #                      test - this tests the selection of aggregate
    #                      functions (COUNT, AVG, MAX, MIN, SUM).
    #                      Aggregates are tested in the SELECT clause and
    #                      in the HAVING clause.
    #  Test case inputs:   Uses Glabl database.
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    #  Notes:
    #  This test case incorporates features detailed in the "Title"
    #  by Ima Programmer (Version 1.1, <date>).
    #
    # =================== End Test Case Header  ===================
    
    #   get region #, branch #  and the average payroll for the
    #   branch(es) with the highest average payroll
    
    stmt = """select regnum,branchnum, avg(salary)
from """ + gvars.g_schema_arkcasedb + """.employee 
group by regnum, branchnum
having avg(salary) >=ALL
(select avg(salary)
from """ + gvars.g_schema_arkcasedb + """.employee 
group by regnum, branchnum
)
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s0')
    
    #   get region #, branch #  and the average payroll for the
    #   branch(es) with the highest TOTAL payroll
    stmt = """select regnum,branchnum, avg(salary)
from """ + gvars.g_schema_arkcasedb + """.employee 
group by regnum, branchnum
having sum(salary) >=ALL
(select sum(salary)
from """ + gvars.g_schema_arkcasedb + """.employee 
group by regnum, branchnum
)
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s1')
    
    stmt = """select job, avg(age)
from """ + gvars.g_schema_arkcasedb + """.employee 
group by job;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s2')
    
    stmt = """select job, avg(salary)
from """ + gvars.g_schema_arkcasedb + """.employee 
group by job;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s3')
    
    #   get job, average salary, and average age for jobs whose average
    #   salary is greater than the average salary of the job with the
    #   lowest average employee age.
    stmt = """select job, avg(salary), avg(age)
from """ + gvars.g_schema_arkcasedb + """.employee 
group by job
having avg(salary) >=ALL
(select avg(salary)
from """ + gvars.g_schema_arkcasedb + """.employee 
group by job
having avg(age) <=ALL
(select avg(age)
from """ + gvars.g_schema_arkcasedb + """.employee 
group by job
)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s4')
    # ++++++ may take a long (an hour) time to run
    
    #   get job, average salary, and average distinct age for jobs
    #   whose average salary is greater than the average salary of the
    #   job with the lowest average distinct employee age.
    stmt = """select job, avg(salary), avg(distinct age)
from """ + gvars.g_schema_arkcasedb + """.employee 
group by job
having avg(salary) >=ALL
(select avg(salary)
from """ + gvars.g_schema_arkcasedb + """.employee 
group by job
having avg(distinct age) <=ALL
(select avg(distinct age)
from """ + gvars.g_schema_arkcasedb + """.employee 
group by job
)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s5')
    # +++++ may take a long (an hour) time to run
    
    #   get the salaries and minimum age of employees with that salary
    #   where the salary is greater than the average salary for all
    #   employees.
    stmt = """select salary, min(age)
from """ + gvars.g_schema_arkcasedb + """.employee 
group by salary
having salary >
(select avg(salary)
from """ + gvars.g_schema_arkcasedb + """.employee 
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s6')
    
    #  get the salaries and minimum age of employees with that salary
    #  where the salary is greater than the 'median' salary for all
    #  employees.
    # ?p = 2;
    stmt = """set param ?p 2;"""
    output = _dci.cmdexec(stmt)
    stmt = """select salary, min(age)
from """ + gvars.g_schema_arkcasedb + """.employee 
group by salary
having salary >
(select min(salary) + ((max(salary) - min(salary)) / ?p )
from """ + gvars.g_schema_arkcasedb + """.employee 
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s7')
    
    #   get the salaries and minimum age of employees with that
    #   salary where the minimum age is greater than the average age
    #   of all employees
    stmt = """select salary, min(age)
from """ + gvars.g_schema_arkcasedb + """.employee 
group by salary
having min(age) >
(select avg(age)
from """ + gvars.g_schema_arkcasedb + """.employee 
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s8')
    
    #   get the salaries and the number of employees who make that
    #   salary, such that more employees make that salary than any
    #   other
    stmt = """select salary, count(*)
from """ + gvars.g_schema_arkcasedb + """.employee 
group by salary
having count(*) >=ALL
(select count(*)
from """ + gvars.g_schema_arkcasedb + """.employee 
group by salary
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s9')
    
    _testmgr.testcase_end(desc)

