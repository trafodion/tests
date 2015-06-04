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
    #  Test case name:     arkt0014 : A01
    #  Description:        This test verifies the SQL SELECT
    #                      statements with UnCorrelated SubQueries
    #                      in their WHERE clauses.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    
    #  Get supplier names for suppliers who supply part 4102.
    
    stmt = """select suppname
from """ + gvars.g_schema_arkcasedb + """.supplier 
where suppnum in
(select suppnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where partnum = 4102
)
order by suppnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s0')
    
    #  Get supplier names for suppliers who DON'T supply part 4102.
    
    stmt = """select suppname
from """ + gvars.g_schema_arkcasedb + """.supplier 
where suppnum NOT in
(select suppnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where partnum = 4102
)
order by suppnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s1')
    
    #  Get employee names who are regional managers (notice no
    #  where clause in subquery)
    
    stmt = """select empname
from """ + gvars.g_schema_arkcasedb + """.employee 
where empnum in
(select manager
from """ + gvars.g_schema_arkcasedb + """.region)
order by empnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s2')
    
    #  Get employee names who do not work at first branches
    #  (eliminate duplicates)
    
    stmt = """select empname
from """ + gvars.g_schema_arkcasedb + """.employee 
where branchnum in
(select branchnum
from """ + gvars.g_schema_arkcasedb + """.branch 
where branchnum <> 1
group by branchnum)
order by empname;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s3')
    
    #  same as previous query, but use DISTINCT instead of
    #  GROUP BY to eliminate duplicates
    
    stmt = """select empname
from """ + gvars.g_schema_arkcasedb + """.employee 
where branchnum in
(select distinct branchnum
from """ + gvars.g_schema_arkcasedb + """.branch 
where branchnum <> 1
)
order by empnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s4')
    
    #  same as query before last, but use HAVING with GROUP BY
    #  instead of WHERE to eliminate branches with branchnum = 1
    
    stmt = """select empname
from """ + gvars.g_schema_arkcasedb + """.employee 
where branchnum in
(select branchnum
from """ + gvars.g_schema_arkcasedb + """.branch 
group by branchnum
having branchnum <> 1)
order by empnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s5')
    
    #  get region names where the manager's employee number is
    #  less than 100
    
    stmt = """select regname
from """ + gvars.g_schema_arkcasedb + """.region 
where manager in
(select *
from """ + gvars.g_schema_arkcasedb + """.empone 
where empnum < 100)
order by regnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s6')
    
    #  get supplier numbers, for suppliers who supply at least
    #  one part supplied by supplier 15.
    
    stmt = """select distinct suppnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where partnum in
(select partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where suppnum = 15)
order by suppnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s7')
    
    #  same as above, only use aliases.
    
    stmt = """select distinct suppnum
from """ + gvars.g_schema_arkcasedb + """.fromsup X
where X.partnum in
(select Y.partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup Y
where suppnum = 15)
order by suppnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s8')
    
    #  get salesman numbers and order numbers for salesman
    #  who have orders for parts costing > 50000
    
    stmt = """select salesman,ordernum
from """ + gvars.g_schema_arkcasedb + """.orders 
where  """ + gvars.g_schema_arkcasedb + """.orders.ordernum in
(select  """ + gvars.g_schema_arkcasedb + """.odetail.ordernum
from """ + gvars.g_schema_arkcasedb + """.odetail,""" + gvars.g_schema_arkcasedb + """.parts 
where  """ + gvars.g_schema_arkcasedb + """.odetail.partnum =  """ + gvars.g_schema_arkcasedb + """.parts.partnum
and price > 50000)
order by ordernum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s9')
    
    #  get salesman numbers who have orders for parts prices > 50000
    #  (eliminate duplicate salesman numbers and order numbers)
    
    stmt = """select distinct salesman
from """ + gvars.g_schema_arkcasedb + """.orders 
where ordernum in
(select distinct ordernum
from """ + gvars.g_schema_arkcasedb + """.odetail,""" + gvars.g_schema_arkcasedb + """.parts 
where  """ + gvars.g_schema_arkcasedb + """.odetail.partnum =  """ + gvars.g_schema_arkcasedb + """.parts.partnum
and price > 50000)
order by salesman;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s10')
    
    #  get parts records with a cost > 10000
    
    stmt = """select *
from """ + gvars.g_schema_arkcasedb + """.parts 
where partnum in
(select partnum
from """ + gvars.g_schema_arkcasedb + """.expfroms)
order by partnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s11')
    
    #  get supplier numbers for suppliers who are in the same
    #  state as supplier 1. (This tests the use of IN with a
    #  subquery that returns only one record).
    
    stmt = """select suppnum
from """ + gvars.g_schema_arkcasedb + """.supplier 
where state IN
(select state
from """ + gvars.g_schema_arkcasedb + """.supplier 
where suppnum = 1)
order by suppnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s12')
    
    _testmgr.testcase_end(desc)

def test002(desc="""a02"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0014 : A02
    #  Description:        This test verifies the SQL SELECT
    #                      statements with UnCorrelated SubQueries
    #                      in their WHERE clauses.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    
    #  get supplier numbers for suppliers who are in the same state
    #  as supplier 1.
    
    stmt = """select suppnum
from """ + gvars.g_schema_arkcasedb + """.supplier 
where state =
(select state
from """ + gvars.g_schema_arkcasedb + """.supplier 
where suppnum = 1)
order by suppnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s0')
    
    #  get supplier numbers for suppliers who are in the same state
    #  as supplier 1 (use aliases).
    
    stmt = """select suppnum
from """ + gvars.g_schema_arkcasedb + """.supplier X
where X.state =
(select X.state
from """ + gvars.g_schema_arkcasedb + """.supplier X
where suppnum = 1)
order by suppnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s1')
    
    #  get the region's name whose manager's employee number is
    #  greater than one.
    
    stmt = """select regname
from """ + gvars.g_schema_arkcasedb + """.region 
where manager >
(select *
from """ + gvars.g_schema_arkcasedb + """.empone 
where empnum = 1)
order by regnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s2')
    
    #  get partnames for parts whose cost is 6000, and are not
    #  supplied by supplier #10.
    
    stmt = """select partname
from """ + gvars.g_schema_arkcasedb + """.parts 
where partnum =
(select distinct partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where partcost = 6000
and suppnum <> 10)
order by partnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s3')
    
    #  get customer names for customers who have not ordered parts
    #  stored at location 'V67'
    
    stmt = """select custname
from """ + gvars.g_schema_arkcasedb + """.customer 
where custnum <>
(select col_12
from """ + gvars.g_schema_arkcasedb + """.partsfor 
where col_2 = 'V67')
order by custnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s4')
    
    #  same as above, only use a join instead of the view partsfor
    
    stmt = """select custname
from """ + gvars.g_schema_arkcasedb + """.customer 
where custnum <>
(select custnum
from """ + gvars.g_schema_arkcasedb + """.orders,
 """ + gvars.g_schema_arkcasedb + """.odetail,
 """ + gvars.g_schema_arkcasedb + """.parts 
where ( """ + gvars.g_schema_arkcasedb + """.orders.ordernum =  """ + gvars.g_schema_arkcasedb + """.odetail.ordernum) and
( """ + gvars.g_schema_arkcasedb + """.odetail.partnum =  """ + gvars.g_schema_arkcasedb + """.parts.partnum) and
(location = 'V67'))
order by custnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s5')
    
    #  get states for customers who have not ordered parts stored
    #  at location 'V67', group by state.
    
    stmt = """select state
from """ + gvars.g_schema_arkcasedb + """.customer 
where custnum <>
(select col_12
from """ + gvars.g_schema_arkcasedb + """.partsfor 
where col_2 = 'V67')
group by state
order by state;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s6')
    
    #  same as above, but eliminate customers in Texas
    
    stmt = """select state
from """ + gvars.g_schema_arkcasedb + """.customer 
where custnum <>
(select col_12
from """ + gvars.g_schema_arkcasedb + """.partsfor 
where col_2 = 'V67')
group by state
having state <> 'TEXAS'
order by state;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s7')
    
    #  same as above, but order by state
    
    stmt = """select state
from """ + gvars.g_schema_arkcasedb + """.customer 
where custnum <>
(select col_12
from """ + gvars.g_schema_arkcasedb + """.partsfor 
where col_2 = 'V67')
group by state
having state <> 'TEXAS'
order by state;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s8')
    
    #  get supplier numbers whose price for part #4102 is less
    #  than or equal to supplier number 8
    
    stmt = """select suppnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where partcost <=
(select partcost
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where partnum = 4102
and suppnum = 8)
AND partnum = 4102
order by partnum, suppnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s9')
    
    #  same as above, but AND condition before the subquery
    
    stmt = """select suppnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where partnum = 4102
and partcost <=
(select partcost
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where partnum = 4102
and suppnum = 8)
order by partnum, suppnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s10')
    
    _testmgr.testcase_end(desc)

def test003(desc="""a03"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0014 : A03
    #  Description:        This test verifies the SQL SELECT
    #                      statements with UnCorrelated SubQueries
    #                      in their WHERE clauses.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    
    #  get supplier names for suppliers who supply part 4102
    
    stmt = """select suppname
from """ + gvars.g_schema_arkcasedb + """.supplier 
where suppnum =ANY
(select suppnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where partnum = 4102)
order by suppnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s0')
    
    #  same as above , with SOME instead of ANY
    #  test use of white space between = and SOME
    
    stmt = """select suppname
from """ + gvars.g_schema_arkcasedb + """.supplier 
where suppnum =    SOME
(select suppnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where partnum = 4102)
order by suppnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s1')
    
    #  Get supplier names for suppliers who DON'T supply part 4102.
    
    stmt = """select suppname
from """ + gvars.g_schema_arkcasedb + """.supplier 
where NOT suppnum =ANY
(select suppnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where partnum = 4102
)
order by suppnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s2')
    
    #  Get supplier names for suppliers who DON'T supply part 4102.
    #  test use of white space between <> and ANY
    
    stmt = """select suppname
from """ + gvars.g_schema_arkcasedb + """.supplier 
where suppnum <>
ANY
(select suppnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where partnum = 4102
)
order by suppnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s3')
    
    #  Get supplier names for suppliers who DON'T supply part 4102.
    
    stmt = """select suppname
from """ + gvars.g_schema_arkcasedb + """.supplier 
where suppnum <>SOME
(select suppnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where partnum = 4102
)
order by suppnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s4')
    
    #  Get employee names who are regional managers (notice no
    #  where clause in subquery)
    
    stmt = """select empname
from """ + gvars.g_schema_arkcasedb + """.employee 
where empnum =ANY
(select manager
from """ + gvars.g_schema_arkcasedb + """.region)
order by empnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s5')
    
    #  Get employee names who do not work at first branches
    #  (eliminate duplicates)
    
    stmt = """select empname
from """ + gvars.g_schema_arkcasedb + """.employee 
where branchnum =SOME
(select branchnum
from """ + gvars.g_schema_arkcasedb + """.branch 
where branchnum <> 1
group by branchnum)
order by empnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s6')
    
    #  same as previous query, but use DISTINCT instead of
    #  GROUP BY to eliminate duplicates
    
    stmt = """select empname
from """ + gvars.g_schema_arkcasedb + """.employee 
where branchnum =ANY
(select distinct branchnum
from """ + gvars.g_schema_arkcasedb + """.branch 
where branchnum <> 1
)
order by empnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s7')
    
    #  same as query before last, but use HAVING with GROUP BY
    #  instead of WHERE to eliminate branches with branchnum = 1
    
    stmt = """select empname
from """ + gvars.g_schema_arkcasedb + """.employee 
where branchnum =SOME
(select branchnum
from """ + gvars.g_schema_arkcasedb + """.branch 
group by branchnum
having branchnum <> 1)
order by empnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s8')
    
    #  get region names where the manager's employee number is
    #  less than 100
    
    stmt = """select regname
from """ + gvars.g_schema_arkcasedb + """.region 
where manager =ANY
(select *
from """ + gvars.g_schema_arkcasedb + """.empone 
where empnum < 100)
order by regnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s9')
    
    #  get supplier numbers, for suppliers who supply at least
    #  one part supplied by supplier 15.
    
    stmt = """select distinct suppnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where partnum =SOME
(select partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where suppnum = 15)
order by suppnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s10')
    
    #  same as above, only use aliases.
    
    stmt = """select distinct suppnum
from """ + gvars.g_schema_arkcasedb + """.fromsup X
where X.partnum =ANY
(select Y.partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup Y
where suppnum = 15)
order by suppnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s11')
    
    #  get salesman numbers and order numbers for salesman
    #  who have orders for parts costing > 50000
    
    stmt = """select salesman,ordernum
from """ + gvars.g_schema_arkcasedb + """.orders 
where  """ + gvars.g_schema_arkcasedb + """.orders.ordernum =SOME
(select  """ + gvars.g_schema_arkcasedb + """.odetail.ordernum
from """ + gvars.g_schema_arkcasedb + """.odetail,""" + gvars.g_schema_arkcasedb + """.parts 
where  """ + gvars.g_schema_arkcasedb + """.odetail.partnum =  """ + gvars.g_schema_arkcasedb + """.parts.partnum
and price > 50000)
order by ordernum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s12')
    
    #  get salesman numbers who have orders for parts prices > 50000
    #  (eliminate duplicate salesman numbers and order numbers)
    
    stmt = """select distinct salesman
from """ + gvars.g_schema_arkcasedb + """.orders 
where ordernum =ANY
(select distinct ordernum
from """ + gvars.g_schema_arkcasedb + """.odetail,""" + gvars.g_schema_arkcasedb + """.parts 
where  """ + gvars.g_schema_arkcasedb + """.odetail.partnum =  """ + gvars.g_schema_arkcasedb + """.parts.partnum
and price > 5000)
order by salesman;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s13')
    
    #  get parts records with a cost > 10000
    
    stmt = """select *
from """ + gvars.g_schema_arkcasedb + """.parts 
where partnum =SOME
(select partnum
from """ + gvars.g_schema_arkcasedb + """.expfroms)
order by partnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s14')
    
    #  get supplier numbers for suppliers who are in the same
    #  state as supplier 1. (This tests the use of =ANY with a
    #  subquery that returns only one record).
    
    stmt = """select suppnum
from """ + gvars.g_schema_arkcasedb + """.supplier 
where state =ANY
(select state
from """ + gvars.g_schema_arkcasedb + """.supplier 
where suppnum = 1)
order by suppnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s15')
    
    #  get supplier numbers whose price for part 4102 is less
    #  than some other supplier who supplies part 4102
    
    stmt = """select suppnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where partcost <SOME
(select partcost
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where partnum = 4102)
and partnum = 4102
order by partnum, suppnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s16')
    
    #  same as above, with ANY instead of SOME
    
    stmt = """select suppnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where partcost <ANY
(select partcost
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where partnum = 4102)
and partnum = 4102
order by partnum, suppnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s17')
    
    #  get supplier numbers whose price for part 4102 is less
    #  than or equal to ALL suppliers who supply part 4102
    
    stmt = """select suppnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where partcost <=ALL
(select partcost
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where partnum = 4102)
and partnum = 4102
order by partnum, suppnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s18')
    
    #  get supplier numbers who are in the same state as supplier
    #  1 (this tests the use of =ALL with a subquery that only
    #  returns one record).
    
    stmt = """select suppnum
from """ + gvars.g_schema_arkcasedb + """.supplier 
where state =ALL
(select state
from """ + gvars.g_schema_arkcasedb + """.supplier 
where suppnum = 1)
order by suppnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s19')
    
    #  get the salesmans' empnum (if any) who has the only order
    #  where at least one part has been ordered in quanities > 25.
    
    stmt = """select salesman
from """ + gvars.g_schema_arkcasedb + """.orders 
where ordernum =ALL
(select ordernum
from """ + gvars.g_schema_arkcasedb + """.odetail 
where quantity > 25)
order by ordernum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s20')
    
    #  same as above, but with group by salesman
    
    stmt = """select salesman
from """ + gvars.g_schema_arkcasedb + """.orders 
where ordernum =ALL
(select ordernum
from """ + gvars.g_schema_arkcasedb + """.odetail 
where quantity > 25)
group by salesman
order by salesman;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s21')
    
    #  same as previous, with having salesman # >= 210
    
    stmt = """select salesman
from """ + gvars.g_schema_arkcasedb + """.orders 
where ordernum =ALL
(select ordernum
from """ + gvars.g_schema_arkcasedb + """.odetail 
where quantity > 25)
group by salesman
having salesman >= 210
order by salesman;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s22')
    
    #  same as first, but with 'select DISTINCT ordernum'
    
    stmt = """select salesman
from """ + gvars.g_schema_arkcasedb + """.orders 
where ordernum =ALL
(select distinct ordernum
from """ + gvars.g_schema_arkcasedb + """.odetail 
where quantity > 25)
order by ordernum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s23')
    
    #  get supplier names whose state is not equal to some
    #  customer state
    
    stmt = """select S.suppname
from """ + gvars.g_schema_arkcasedb + """.supplier S
where state <>ANY
(select C.state
from """ + gvars.g_schema_arkcasedb + """.customer C)
order by suppnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s24')
    
    #  get supplier names whose state is not equal to ALL
    #  customer states
    
    stmt = """select suppname
from """ + gvars.g_schema_arkcasedb + """.supplier 
where state <>ALL
(select state
from """ + gvars.g_schema_arkcasedb + """.customer)
order by suppnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s25')
    
    #  same as above, add group by,having clauses
    
    stmt = """select suppname
from """ + gvars.g_schema_arkcasedb + """.supplier 
where state <>ALL
(select state
from """ + gvars.g_schema_arkcasedb + """.customer 
group by state
having state <> 'TEXAS')
order by suppnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s26')
    
    _testmgr.testcase_end(desc)

def test004(desc="""a04"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0014 : A04
    #  Description:        This test verifies the SQL SELECT
    #                      statements with UnCorrelated SubQueries
    #                      in their WHERE clauses.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    
    #  get supplier names for suppliers who supply part 4102
    #  and part 5504
    
    stmt = """select suppname
from """ + gvars.g_schema_arkcasedb + """.supplier 
where (suppnum in
(select suppnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where partnum = 4102))
and (suppnum =ANY
(select suppnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where partnum = 5504))
order by suppnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s0')
    
    #  get supplier names for suppliers who supply part 4102
    #  OR 5504   -- same as above, replace 'and' with 'or'
    
    stmt = """select suppname
from """ + gvars.g_schema_arkcasedb + """.supplier 
where (suppnum in
(select suppnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where partnum = 4102))
or (suppnum =ANY
(select suppnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where partnum = 5504))
order by suppnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s1')
    
    #  get supplier names for suppliers who DON'T supply parts
    #  4102 or 5504 -- same as previous, add NOT before entire
    #  predicate.
    
    stmt = """select suppname
from """ + gvars.g_schema_arkcasedb + """.supplier 
where NOT ((suppnum in
(select suppnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where partnum = 4102))
or (suppnum =ANY
(select suppnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where partnum = 5504)))
order by suppnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s2')
    
    #  get supplier names for suppliers who supply parts 4102,
    #  5504, and 5505.
    
    stmt = """select suppname
from """ + gvars.g_schema_arkcasedb + """.supplier 
where (suppnum in
(select suppnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where partnum = 4102))
and (suppnum =ANY
(select suppnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where partnum = 5504))
and (suppnum =SOME
(select suppnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where partnum = 5505))
order by suppnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s3')
    
    #  get employee names who have salary >= 30000 and age < 30
    
    stmt = """select empname
from """ + gvars.g_schema_arkcasedb + """.emppub 
where empnum in
(select empnum
from """ + gvars.g_schema_arkcasedb + """.employee 
where salary >= 30000)
and empnum in
(select empnum
from """ + gvars.g_schema_arkcasedb + """.employee 
where age < 30)
order by empnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s4')
    
    #  get job titles for employees who work in the Chicago branch
    #  of the Central region, excluding programmers, order by job title
    
    stmt = """select job
from """ + gvars.g_schema_arkcasedb + """.employee 
where (regnum not in
(select regnum
from """ + gvars.g_schema_arkcasedb + """.region 
where regname <> 'CENTRAL'))
and (branchnum in
(select branchnum
from """ + gvars.g_schema_arkcasedb + """.branch 
where branchname = 'CHICAGO'
group by branchnum))
group by job
having job <> 'PROGRAMMER'
order by job;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s5')
    
    #  same as above, except eliminate 'group bys' and add 'distinct'
    
    stmt = """select distinct job
from """ + gvars.g_schema_arkcasedb + """.employee 
where (regnum not in
(select regnum
from """ + gvars.g_schema_arkcasedb + """.region 
where regname <> 'CENTRAL'))
and (branchnum in
(select distinct branchnum
from """ + gvars.g_schema_arkcasedb + """.branch 
where branchname = 'CHICAGO'))
and job <> 'PROGRAMMER'
order by job;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s6')
    
    #  get supplier names for suppliers who supply at least
    #  one part whose inventory is negative (less than 0)
    
    stmt = """select suppname
from """ + gvars.g_schema_arkcasedb + """.supplier 
where suppnum in
(select suppnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where partnum in
(select partnum
from """ + gvars.g_schema_arkcasedb + """.parts 
where inventory < 0)
)
order by suppnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s7')
    
    #  same as above, except use '=SOME' instead of IN
    
    stmt = """select suppname
from """ + gvars.g_schema_arkcasedb + """.supplier 
where suppnum in
(select suppnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where partnum =SOME
(select partnum
from """ + gvars.g_schema_arkcasedb + """.parts 
where inventory < 0)
)
order by suppnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s8')
    
    #  get supplier names for suppliers who supply part 'LP__900_LPM'
    
    stmt = """select suppname
from """ + gvars.g_schema_arkcasedb + """.supplier 
where suppnum IN
(select suppnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where partnum =
(select partnum
from """ + gvars.g_schema_arkcasedb + """.parts 
where partname = 'LP  900 LPM'))
order by suppnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s9')
    
    #  get age of those employees whose salary is less than or
    #  equal to the salary to the youngest employee
    
    stmt = """select age
from """ + gvars.g_schema_arkcasedb + """.employee 
where salary <=
(select salary
from """ + gvars.g_schema_arkcasedb + """.employee 
where age <= ALL
(select age
from """ + gvars.g_schema_arkcasedb + """.employee 
)
)
order by empnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s10')
    
    #  same as above, with aliases
    
    stmt = """select X.age
from """ + gvars.g_schema_arkcasedb + """.employee X
where X.salary <=
(select salary
from """ + gvars.g_schema_arkcasedb + """.employee Y
where Y.age <= ALL
(select Z.age
from """ + gvars.g_schema_arkcasedb + """.employee Z
)
)
order by empnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s11')
    
    #  get salesman names who have orders for parts priced < 8000
    #  (eliminate duplicate salesman names,order numbers, and
    #  records where the price = 8000)
    
    stmt = """select distinct salesman
from """ + gvars.g_schema_arkcasedb + """.orders 
where ordernum in
(select distinct ordernum
from """ + gvars.g_schema_arkcasedb + """.odetail,""" + gvars.g_schema_arkcasedb + """.parts 
where  """ + gvars.g_schema_arkcasedb + """.odetail.partnum =  """ + gvars.g_schema_arkcasedb + """.parts.partnum
and price <
(select distinct price
from """ + gvars.g_schema_arkcasedb + """.parts 
where price = 8000))
order by salesman;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s12')
    
    #  get customer names who have orders for parts supplied by
    #  suppliers in Mass.
    
    stmt = """select custname
from """ + gvars.g_schema_arkcasedb + """.customer 
where custnum in
(select custnum
from """ + gvars.g_schema_arkcasedb + """.orders 
where ordernum in
(select distinct ordernum
from """ + gvars.g_schema_arkcasedb + """.odetail 
where partnum in
(select distinct partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where suppnum in
(select suppnum
from """ + gvars.g_schema_arkcasedb + """.supplier 
where state = 'MASS'
)
)
)
)
order by custnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s13')
    
    #  same as above, eliminate 'distinct'
    
    stmt = """select custname
from """ + gvars.g_schema_arkcasedb + """.customer 
where custnum in
(select custnum
from """ + gvars.g_schema_arkcasedb + """.orders 
where ordernum in
(select ordernum
from """ + gvars.g_schema_arkcasedb + """.odetail 
where partnum in
(select partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where suppnum in
(select suppnum
from """ + gvars.g_schema_arkcasedb + """.supplier 
where state = 'MASS'
)
)
)
)
order by custnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s14')
    
    #  get customer names who have orders for parts supplied by
    #  suppliers in Mass, where the order month is less than 4
    
    stmt = """select custname
from """ + gvars.g_schema_arkcasedb + """.customer 
where custnum in
(select custnum
from """ + gvars.g_schema_arkcasedb + """.orders 
where ordernum in
(select distinct ordernum
from """ + gvars.g_schema_arkcasedb + """.odetail 
where partnum in
(select distinct partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where suppnum in
(select suppnum
from """ + gvars.g_schema_arkcasedb + """.supplier 
where state = 'MASS'
)
)
)
and omonth < 4
)
order by custnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s15')
    
    #  get salesman names and their customer names for salesman
    #  who work in the Central region
    
    stmt = """select empname,custname
from """ + gvars.g_schema_arkcasedb + """.salecust 
where empname in
(select empname
from """ + gvars.g_schema_arkcasedb + """.emppub 
where regnum in
(select regnum
from """ + gvars.g_schema_arkcasedb + """.region 
where regname = 'CENTRAL'
)
)
order by custname;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s16')
    
    #  get supplier names for suppliers who supply at least
    #  one part whose inventory is negative, eliminate duplicates
    #  with group by
    
    stmt = """select suppname
from """ + gvars.g_schema_arkcasedb + """.supplier 
where suppnum in
(select suppnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where partnum in
(select partnum
from """ + gvars.g_schema_arkcasedb + """.parts 
where inventory < 0)
group by suppnum
)
order by suppnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s17')
    
    #  same as above, but eliminate supplier #2
    
    stmt = """select suppname
from """ + gvars.g_schema_arkcasedb + """.supplier 
where suppnum in
(select suppnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where partnum in
(select partnum
from """ + gvars.g_schema_arkcasedb + """.parts 
where inventory < 0)
group by suppnum
having suppnum <> 2
)
order by suppnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s18')
    
    #  get age of those employees who are not 22 and whose salary
    #  is less than or equal to the salary of the youngest employee
    #  under 40.
    
    stmt = """select age
from """ + gvars.g_schema_arkcasedb + """.employee 
where salary <=
(select salary
from """ + gvars.g_schema_arkcasedb + """.employee 
where age <=ALL
(select age
from """ + gvars.g_schema_arkcasedb + """.employee 
group by age
having age <40
)
)
group by age
having age <> 22
order by age;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s19')
    
    _testmgr.testcase_end(desc)

def test005(desc="""a05"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0014 : A05
    #  Description:        This test verifies the SQL SELECT
    #                      statements with UnCorrelated SubQueries
    #                      in their WHERE clauses.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    
    #  get supplier numbers, for suppliers who supply at least
    #  one part supplied by supplier 15.
    
    stmt = """select distinct suppnum
from """ + gvars.g_schema_arkcasedb + """.fromsup X
where X.partnum in
(select Y.partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup Y
where suppnum = 15
for read uncommitted access
)
for serializable access
order by suppnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s0')
    
    #  get supplier numbers, for suppliers who supply at least
    #  one part supplied by supplier 15.
    
    stmt = """select distinct suppnum
from """ + gvars.g_schema_arkcasedb + """.fromsup X
where X.partnum in
(select Y.partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup Y
where suppnum = 15
for read committed access
)
for read uncommitted access
order by suppnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s1')
    
    #  get supplier numbers, for suppliers who supply at least
    #  one part supplied by supplier 15.
    
    stmt = """select distinct suppnum
from """ + gvars.g_schema_arkcasedb + """.fromsup X
where X.partnum in
(select Y.partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup Y
where suppnum = 15
for serializable access
)
for read committed access
order by suppnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s2')
    
    #  get salesman numbers and order numbers for salesman
    #  who have orders for parts costing > 50000
    
    stmt = """select salesman,ordernum
from """ + gvars.g_schema_arkcasedb + """.orders 
where  """ + gvars.g_schema_arkcasedb + """.orders.ordernum in
(select  """ + gvars.g_schema_arkcasedb + """.odetail.ordernum
from """ + gvars.g_schema_arkcasedb + """.odetail,""" + gvars.g_schema_arkcasedb + """.parts 
where  """ + gvars.g_schema_arkcasedb + """.odetail.partnum =  """ + gvars.g_schema_arkcasedb + """.parts.partnum
and price > 50000
for serializable access
)
order by ordernum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s3')
    
    #  get supplier numbers for suppliers who are in the same state
    #  as supplier 1 (use aliases).
    
    stmt = """select suppnum
from """ + gvars.g_schema_arkcasedb + """.supplier X
where X.state =
(select Y.state
from """ + gvars.g_schema_arkcasedb + """.supplier Y
where suppnum = 1
for read uncommitted access
)
for serializable access
order by suppnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s4')
    
    #  get supplier numbers for suppliers who are in the same state
    #  as supplier 1 (use aliases).
    
    stmt = """select suppnum
from """ + gvars.g_schema_arkcasedb + """.supplier X
where X.state =
(select Y.state
from """ + gvars.g_schema_arkcasedb + """.supplier Y
where suppnum = 1
for read committed access
)
for read uncommitted access
order by suppnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s5')
    
    #  get supplier numbers for suppliers who are in the same state
    #  as supplier 1 (use aliases).
    
    stmt = """select suppnum
from """ + gvars.g_schema_arkcasedb + """.supplier X
where X.state =
(select Y.state
from """ + gvars.g_schema_arkcasedb + """.supplier Y
where suppnum = 1
for serializable access
)
for read committed access
order by suppnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s6')
    
    #  get customer names for customers who have not ordered parts
    #  stored at location 'V67'
    
    stmt = """select custname
from """ + gvars.g_schema_arkcasedb + """.customer 
where custnum <>
(select col_12
from """ + gvars.g_schema_arkcasedb + """.partsfor 
where col_2 = 'V67'
for read uncommitted access
)
order by custnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s7')
    
    #  get customer names for customers who have not ordered parts
    #  stored at location 'V67'
    
    stmt = """select custname
from """ + gvars.g_schema_arkcasedb + """.customer 
where custnum <>
(select col_12
from """ + gvars.g_schema_arkcasedb + """.partsfor 
where col_2 = 'V67'
for read committed access
)
order by custnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s8')
    
    #  get customer names for customers who have not ordered parts
    #  stored at location 'V67'
    
    stmt = """select custname
from """ + gvars.g_schema_arkcasedb + """.customer 
where custnum <>
(select col_12
from """ + gvars.g_schema_arkcasedb + """.partsfor 
where col_2 = 'V67'
for serializable access
)
order by custnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s9')
    
    #  same as above, only use a join instead of the view partsfor
    
    stmt = """select custname
from """ + gvars.g_schema_arkcasedb + """.customer 
where custnum <>
(select custnum
from """ + gvars.g_schema_arkcasedb + """.orders,
 """ + gvars.g_schema_arkcasedb + """.odetail,
 """ + gvars.g_schema_arkcasedb + """.parts 
where ( """ + gvars.g_schema_arkcasedb + """.orders.ordernum =  """ + gvars.g_schema_arkcasedb + """.odetail.ordernum) and
( """ + gvars.g_schema_arkcasedb + """.odetail.partnum =  """ + gvars.g_schema_arkcasedb + """.parts.partnum) and
(location = 'V67')
for serializable access
)
order by custnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s10')
    
    #  get supplier names for suppliers who supply part 4102
    #  and part 5504
    
    stmt = """select suppname
from """ + gvars.g_schema_arkcasedb + """.supplier 
where suppnum in
(select suppnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where partnum = 4102
for read uncommitted access
)
and suppnum =ANY
(select suppnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where partnum = 5504
for read committed access
)
order by suppnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s11')
    
    #  get supplier names for suppliers who supply part 4102
    #  and part 5504
    
    stmt = """select suppname
from """ + gvars.g_schema_arkcasedb + """.supplier 
where suppnum in
(select suppnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where partnum = 4102
for serializable access
)
and suppnum =ANY
(select suppnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where partnum = 5504
for read committed access
)
order by suppnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s12')
    
    #  get supplier names for suppliers who supply part 4102
    #  and part 5504
    
    stmt = """select suppname
from """ + gvars.g_schema_arkcasedb + """.supplier 
where suppnum in
(select suppnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where partnum = 4102
for read uncommitted access
)
and suppnum =ANY
(select suppnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where partnum = 5504
for serializable access
)
order by suppnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s13')
    
    #  get supplier names for suppliers who supply at least
    #  one part whose inventory is negative (less than 0)
    
    stmt = """select suppname
from """ + gvars.g_schema_arkcasedb + """.supplier 
where suppnum in
(select suppnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where partnum in
(select partnum
from """ + gvars.g_schema_arkcasedb + """.parts 
where inventory < 0
for read uncommitted access
)
for serializable access
)
for read committed access
order by suppnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s14')
    
    #  get age of those employees whose salary is less than or
    #  equal to the salary of the youngest employee (use aliases)
    
    stmt = """select X.age
from """ + gvars.g_schema_arkcasedb + """.employee X
where X.salary <=
(select salary
from """ + gvars.g_schema_arkcasedb + """.employee Y
where Y.age <= ALL
(select Z.age
from """ + gvars.g_schema_arkcasedb + """.employee Z
for serializable access
)
for read committed access
)
for read uncommitted access
order by empnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s15')
    
    #  get salesman names who have orders for parts priced < 8000
    #  (eliminate duplicate salesman names,order numbers, and
    #  records where the price = 8000)
    
    stmt = """select distinct salesman
from """ + gvars.g_schema_arkcasedb + """.orders 
where ordernum in
(select distinct ordernum
from """ + gvars.g_schema_arkcasedb + """.odetail,""" + gvars.g_schema_arkcasedb + """.parts 
where  """ + gvars.g_schema_arkcasedb + """.odetail.partnum =  """ + gvars.g_schema_arkcasedb + """.parts.partnum
and price <
(select distinct price
from """ + gvars.g_schema_arkcasedb + """.parts 
where price = 8000
for read uncommitted access
)
for serializable access
)
for read committed access
order by salesman;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s16')
    
    #  get salesman names and their customer names for salesman
    #  who work in the Central region
    
    stmt = """select empname,custname
from """ + gvars.g_schema_arkcasedb + """.salecust 
where empname in
(select empname
from """ + gvars.g_schema_arkcasedb + """.emppub 
where regnum in
(select regnum
from """ + gvars.g_schema_arkcasedb + """.region 
where regname = 'CENTRAL'
for read committed access
)
for serializable access
)
for read uncommitted access
order by custname;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s17')
    
    _testmgr.testcase_end(desc)

def test006(desc="""a06"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0014 : A06
    #  Description:        This test verifies the SQL SELECT
    #                      statements with UnCorrelated SubQueries
    #                      in their WHERE clauses.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    
    #   Get employee names whose salary is greater than the average
    #   salary of all employees
    
    stmt = """select empname
from """ + gvars.g_schema_arkcasedb + """.employee 
where salary >
(select avg(salary)
from """ + gvars.g_schema_arkcasedb + """.employee 
)
order by empnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s0')
    
    #   Get part name(s) which have the highest profit margin
    
    stmt = """select distinct partname
from """ + gvars.g_schema_arkcasedb + """.parts, """ + gvars.g_schema_arkcasedb + """.fromsup 
where  """ + gvars.g_schema_arkcasedb + """.parts.partnum =  """ + gvars.g_schema_arkcasedb + """.fromsup.partnum
and (price - partcost) =
(select max(price - partcost)
from """ + gvars.g_schema_arkcasedb + """.parts, """ + gvars.g_schema_arkcasedb + """.fromsup 
where  """ + gvars.g_schema_arkcasedb + """.parts.partnum =  """ + gvars.g_schema_arkcasedb + """.fromsup.partnum
)
order by partname;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s1')
    
    #  get employee names whose salary is greater than all the
    #  branches average salary
    
    stmt = """select empname
from """ + gvars.g_schema_arkcasedb + """.employee 
where salary >ALL
(select avg(salary)
from """ + gvars.g_schema_arkcasedb + """.employee 
group by regnum, branchnum
)
order by empnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s2')
    
    #  get the average and total salary of employees whose salary
    #  is greater than all branches average salary
    
    stmt = """select avg(salary),sum(salary)
from """ + gvars.g_schema_arkcasedb + """.employee 
where salary >ALL
(select avg(salary)
from """ + gvars.g_schema_arkcasedb + """.employee 
group by regnum, branchnum
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s3')
    
    #  get the average and total salary of employees whose salary
    #  is greater than all branches average salary (use distinct
    #  salaries for the average in both the outer and subquery)
    
    stmt = """select avg(distinct salary),sum(salary)
from """ + gvars.g_schema_arkcasedb + """.employee 
where salary >ALL
(select avg(distinct salary)
from """ + gvars.g_schema_arkcasedb + """.employee 
group by regnum, branchnum
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s4')
    
    #  get employee names whose salary is greater than the average
    #  salary of branch #1 in region #1
    
    stmt = """select empname
from """ + gvars.g_schema_arkcasedb + """.employee 
where salary >
(select avg(salary)
from """ + gvars.g_schema_arkcasedb + """.employee 
where regnum = 1 and branchnum = 1
)
order by empnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s5')
    
    #  get employee names whose salary is greater than the average
    #  salary of all branches whose minimum salary is greater than
    #  20000
    
    stmt = """select empname
from """ + gvars.g_schema_arkcasedb + """.employee 
where salary >ALL
(select avg(salary)
from """ + gvars.g_schema_arkcasedb + """.employee 
group by regnum, branchnum
having min(salary) > 20000
)
order by empnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s6')
    
    #  get the partnames and their prices for the most expensive
    #  part and the least expensive part
    
    stmt = """select partname,price
from """ + gvars.g_schema_arkcasedb + """.parts 
where price =
(select max(price)
from """ + gvars.g_schema_arkcasedb + """.parts 
)
or price =
(select min(price)
from """ + gvars.g_schema_arkcasedb + """.parts 
)
order by partnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s7')
    #  get supplier names for suppliers whose total cost of all
    #  parts they supply exceeds 50000
    
    stmt = """select suppname
from """ + gvars.g_schema_arkcasedb + """.supplier 
where suppnum in
(select suppnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
group by suppnum
having sum(partcost) > 50000
)
order by suppnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s8')
    
    #  get employee names for employees who make the same salary
    #  as at least 2 other employees
    stmt = """select empname
from """ + gvars.g_schema_arkcasedb + """.employee 
where salary in
(select salary
from """ + gvars.g_schema_arkcasedb + """.employee 
group by salary
having count(*) >= 3
)
order by salary;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s9')
    
    #  get part names whose price exceeds the 'median' price
    #   min(price) + ((max(price) - min(price)) / 2)
    
    stmt = """select partname
from """ + gvars.g_schema_arkcasedb + """.parts 
where price >
(select min(price) + ((max(price) - min(price)) / 2)
from """ + gvars.g_schema_arkcasedb + """.parts 
)
order by partnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s10')
    
    _testmgr.testcase_end(desc)

def test007(desc="""a07"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0014 : A07
    #  Description:        This test verifies the SQL SELECT
    #                      statements with UnCorrelated SubQueries
    #                      in their WHERE clauses.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    
    stmt = """create table sqnotin 
(aname char(12) no default not null ) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table sqnotin2 
(aname char(12) no default not null ) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # Insert values into table SQNOTIN2
    
    stmt = """INSERT INTO sqnotin2 
VALUES
('Aase       ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('Acker      ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('Aguilera   ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('Aldrich    ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('Alvarez    ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('AndersonD  ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('Appler     ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('Aquino     ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('August     ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('Baines     ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('Bankhead   ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('Bannister  ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('Barfield   ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('Bean       ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('Belcher    ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('Benedict   ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('Berroa     ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('Birkbeck   ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('Black      ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('Blauser    ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('Blocker    ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('Boever     ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('Boone      ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('Borders    ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('Bosio      ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('Braggs     ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('Brett      ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('Brikbeck   ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('Brock      ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('Buckner    ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('Burns      ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('Cadaret    ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('Calderon   ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('Cangelosi  ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('Carreon    ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('CarterG    ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('Clancy     ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('ClarkJ     ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('Clary      ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('Clutterbuck');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('Cone       ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('Crawford   ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('Crews      ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('Crim       ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('Daniels    ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('Darling    ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('DavisJ     ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('DavisJohn  ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('DavisM     ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('DavisS     ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('De Los Sant');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('DeLeonJ    ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('Deer       ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('Dempsey    ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('Denson     ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('Devereaux  ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('Dykstra    ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('Eave       ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('Eichorn    ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('Eisenreich ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('Elster     ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('Engle      ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('EvansD     ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('Farr       ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('Felder     ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('FernandezS ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('FernandezT ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('Filer      ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('Fisk       ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('Fossas     ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('Francona   ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('Gant       ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('Gantner    ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('GibsonK    ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('Glavine    ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('GonzalezJ  ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('Gooden     ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('Gordon     ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('Greene     ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('Gregg      ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('Griffin    ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('Gruber     ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('Gubicza    ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('Guerrero   ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('Guillen    ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('GwynnC     ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('HamiltonJ  ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('HarrisL    ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('HatcherM   ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('Havens     ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('Heep       ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('Henke      ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('HernandezK ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('Hershiser  ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('Higuera    ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('Holton     ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('HowellJ    ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('Innis      ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('JacksonB   ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('JacksonD   ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('Jeffries   ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('JohnsonH   ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('JohnsonL   ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('Jones      ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('JonesB     ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('Justice    ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('Karkovice  ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('Key        ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('Knudson    ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('LaPoint    ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('LaValliere ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('Lansford   ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('LeachT     ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('Leary      ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('Leibrandt  ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('Lemke      ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('Leonard    ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('Lilliquist ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('Liriano    ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('Lombardi   ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('Luecken    ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('LyonsB     ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('LyonsS     ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('Macfarlane ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('Magadan    ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('Manrique   ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('Marshall   ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('MartinezR  ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('Mazzilli   ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('McClure    ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('McDowellJ  ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('McDowellO  ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('McDowellR  ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('McGee      ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('McReynolds ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('McWilliamsL');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('Meyer      ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('MillerK    ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('Mitchell   ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('Molitor    ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('Montgomery ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('MorganM    ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('Morrison   ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('Moseby     ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('MurphyDa   ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('Murray     ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('Musselman  ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('Myers      ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('Navarro    ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('Nieves     ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('Nunez      ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('NunezE     ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('O'Brien    ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15005')
    stmt = """INSERT INTO sqnotin2 
VALUES
('O'BrienC   ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15005')
    stmt = """INSERT INTO sqnotin2 
VALUES
('Ojeda      ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('Olwine     ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('Ontiveros  ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('Palacios   ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('Pall       ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO sqnotin2 
VALUES
('Paris      ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin2 
values
('Parker     ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin2 
values
('Pasqua     ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin2 
values
('Pecota     ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin2 
values
('PenaA      ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin2 
values
('Pendleton  ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin2 
values
('Perry      ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin2 
values
('Peterek    ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin2 
values
('Plesac     ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin2 
values
('Polidor    ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin2 
values
('Powell     ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin2 
values
('Puleo      ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin2 
values
('Quirk      ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin2 
values
('Randolph   ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin2 
values
('Reuss      ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin2 
values
('RipkenC    ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin2 
values
('Robidoux   ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin2 
values
('Romero     ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin2 
values
('Rosenberg  ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin2 
values
('RussellJ   ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin2 
values
('Saberhagen ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin2 
values
('Salas      ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin2 
values
('SalazarA   ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin2 
values
('Samuel     ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin2 
values
('Sanchez    ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin2 
values
('Sasser     ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin2 
values
('SaxS       ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin2 
values
('SchmidtD   ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin2 
values
('Sciosia    ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin2 
values
('Searage    ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin2 
values
('Seitzer    ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin2 
values
('Sheffield  ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin2 
values
('Shelby     ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin2 
values
('SimmonsT   ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin2 
values
('SmithL     ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin2 
values
('SmithP     ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin2 
values
('SmithZ     ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin2 
values
('Smoltz     ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin2 
values
('Soto       ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin2 
values
('SpiersB    ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin2 
values
('Stanton    ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin2 
values
('Stieb      ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin2 
values
('Stillwell  ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin2 
values
('Stottlemyre');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin2 
values
('Strawberry ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin2 
values
('Stubbs     ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin2 
values
('Sundberg   ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin2 
values
('Surhoff    ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin2 
values
('Tabler     ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin2 
values
('Tartabull  ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin2 
values
('Teufel     ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin2 
values
('Thigpen    ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin2 
values
('ThomasA    ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin2 
values
('Thurman    ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin2 
values
('Traber     ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin2 
values
('Treadway   ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin2 
values
('Tudor      ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin2 
values
('Valdez     ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin2 
values
('Valenzuela ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin2 
values
('VanSlyke   ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin2 
values
('Vaughn     ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin2 
values
('Viola      ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin2 
values
('Ward       ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin2 
values
('WashingtonC');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin2 
values
('Wegman     ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin2 
values
('Wellman    ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin2 
values
('Wells      ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin2 
values
('Wetherby   ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin2 
values
('Wetteland  ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin2 
values
('WhiteF     ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin2 
values
('Whited     ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin2 
values
('WilliamsE  ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin2 
values
('WilsonM    ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin2 
values
('WilsonW    ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin2 
values
('Winn       ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin2 
values
('Winters    ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin2 
values
('Worrell    ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin2 
values
('Yount      ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # Insert values into table SQNOTIN
    
    stmt = """insert into sqnotin 
values
('AndersonD  ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin 
values
('Baines     ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin 
values
('Barfield   ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin 
values
('Bean       ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin 
values
('Benedict   ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin 
values
('Berroa     ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin 
values
('Blauser    ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin 
values
('Blocker    ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin 
values
('Boone      ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin 
values
('Borders    ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin 
values
('Braggs     ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin 
values
('Brett      ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin 
values
('Brock      ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin 
values
('Buckner    ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin 
values
('Calderon   ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin 
values
('Cangelosi  ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin 
values
('Carreon    ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin 
values
('CarterG    ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin 
values
('ClarkJ     ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin 
values
('Daniels    ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin 
values
('DavisJ     ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin 
values
('DavisM     ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin 
values
('De Los Sant');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin 
values
('Deer       ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin 
values
('Dempsey    ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin 
values
('Denson     ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin 
values
('Devereaux  ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin 
values
('Dykstra    ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin 
values
('Eisenreich ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin 
values
('Elster     ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin 
values
('Engle      ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin 
values
('EvansD     ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin 
values
('Felder     ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin 
values
('FernandezT ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin 
values
('Fisk       ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin 
values
('Francona   ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin 
values
('Gant       ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin 
values
('Gantner    ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin 
values
('GibsonK    ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin 
values
('GonzalezJ  ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin 
values
('Gregg      ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin 
values
('Griffin    ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin 
values
('Gruber     ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin 
values
('Guerrero   ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin 
values
('Guillen    ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin 
values
('GwynnC     ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin 
values
('HamiltonJ  ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin 
values
('HarrisL    ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin 
values
('HatcherM   ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin 
values
('Heep       ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin 
values
('HernandezK ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin 
values
('JacksonB   ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin 
values
('Jeffries   ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin 
values
('JohnsonH   ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin 
values
('JohnsonL   ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin 
values
('Justice    ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin 
values
('Karkovice  ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin 
values
('LaValliere ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin 
values
('Lansford   ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin 
values
('Lemke      ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin 
values
('Leonard    ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin 
values
('Liriano    ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin 
values
('Lombardi   ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin 
values
('LyonsB     ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin 
values
('LyonsS     ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin 
values
('Macfarlane ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin 
values
('Magadan    ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin 
values
('Manrique   ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin 
values
('Marshall   ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin 
values
('Mazzilli   ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin 
values
('McDowellO  ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin 
values
('McGee      ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin 
values
('McReynolds ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin 
values
('Meyer      ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin 
values
('MillerK    ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin 
values
('Mitchell   ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin 
values
('Molitor    ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin 
values
('Moseby     ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin 
values
('MurphyDa   ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin 
values
('Murray     ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin 
values
('O'BrienC   ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15005')
    stmt = """insert into sqnotin 
values
('Palacios   ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin 
values
('Parker     ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin 
values
('Pasqua     ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin 
values
('Pecota     ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin 
values
('Pendleton  ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin 
values
('Perry      ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin 
values
('Polidor    ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin 
values
('Quirk      ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin 
values
('Randolph   ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin 
values
('RipkenC    ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin 
values
('Robidoux   ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin 
values
('Romero     ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin 
values
('RussellJ   ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin 
values
('Samuel     ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin 
values
('Sasser     ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin 
values
('SaxS       ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin 
values
('Sciosia    ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin 
values
('Seitzer    ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin 
values
('Sheffield  ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin 
values
('Shelby     ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin 
values
('SmithL     ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin 
values
('Smoltz     ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin 
values
('SpiersB    ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin 
values
('Stillwell  ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin 
values
('Strawberry ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin 
values
('Stubbs     ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin 
values
('Sundberg   ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin 
values
('Surhoff    ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin 
values
('Tabler     ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin 
values
('Tartabull  ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin 
values
('Teufel     ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin 
values
('ThomasA    ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin 
values
('Thurman    ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin 
values
('Traber     ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin 
values
('Treadway   ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin 
values
('VanSlyke   ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin 
values
('Vaughn     ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin 
values
('WashingtonC');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin 
values
('Wellman    ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin 
values
('Wetherby   ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin 
values
('WhiteF     ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin 
values
('Whited     ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin 
values
('WilliamsE  ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin 
values
('WilsonM    ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin 
values
('WilsonW    ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin 
values
('Winters    ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin 
values
('Xxxxxxx    ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into sqnotin 
values
('Yount      ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    #  Select ... NOT IN ... subquery
    
    stmt = """select aname from sqnotin 
where aname not in (select aname from sqnotin2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s3')
    
    stmt = """drop  table sqnotin;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop  table sqnotin2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test008(desc="""a08"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """create table a7table0 
(empnum           pic 9(04) no default not null
,regnum           pic 9(02) default null
,pic_x253         pic x(253)
,varchar_254      varchar(254)
,pic_x255         pic x(255)
) no partition;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into a7table0 values
(11,6,
null,
'rabbit rabbit rabbit rabbit rabbit '
'rabbit rabbit rabbit rabbit rabbit '
'rabbit rabbit rabbit rabbit rabbit '
'rabbit rabbit rabbit rabbit rabbit '
'rabbit rabbit rabbit rabbit rabbit '
'rabbit rabbit rabbit rabbit rabbit '
'rabbit rabbit rabbit rabbit rabbit '
'rabbit ',
'Some bunny loves you');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into a7table0 values
(12, 44,
'I shot the sheriff but I did not shoot the deputy',
'deputy dog                         '
'deputy dog                         '
'deputy dog                         '
'deputy dog                         '
'deputy dog                         '
'deputy dog                         '
'deputy dog                         '
'deputy ',
'the deputy ate rabbit stew by the fire');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into a7table0 values
(13,4,
'M-I-C-K-E-Y M-O-U-S-E',
'three blind mice, three blind mice'
'three blind mice, three blind mice'
'three blind mice, three blind mice'
'three blind mice, three blind mice'
'three blind mice, three blind mice'
'three blind mice, three blind mice'
'three blind mice, three blind mice'
'three ',
'the deputy ate rabbit stew by the fire');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into a7table0 values
(14, 52,
'Hippity-hoppity Easter''s on its way',
'deputy dog                         '
'deputy dog                         '
'deputy dog                         '
'deputy dog                         '
'deputy dog                         '
'deputy dog                         '
'deputy dog                         '
'deputy ',
'How do I love thee, let me count the ways');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into a7table0 values
(15,2,
'Donald loves Daisy',
'three blind mice, three blind mice'
'three blind mice, three blind mice'
'three blind mice, three blind mice'
'three blind mice, three blind mice'
'three blind mice, three blind mice'
'three blind mice, three blind mice'
'three blind mice, three blind mice',
'Some bunny loves you');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into a7table0 values
(66, 5,
'M-I-C-K-E-Y M-O-U-S-E',
'deputy dog                         '
'deputy dog                         '
'deputy dog                         '
'deputy dog                         '
'deputy dog                         '
'deputy dog                         '
'deputy dog                         '
'deputy',
'the deputy ate rabbit stew by the fire');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a7table0 values
(67, 1,
'How do elephants get toe jam?',
'How many elephants can you get in a VW?'
'How many elephants can you get in a VW?'
'How many elephants can you get in a VW?'
'How many elephants can you get in a VW?'
'How many elephants can you get in a VW?'
'How many elephants can you get in a VW?',
'Why did the elephant cross the street?');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select * from a7table0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s0')
    
    stmt = """select empnum,regnum,pic_x255
from a7table0 
where pic_x255
IN (select pic_x255 from a7table0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s1')
    
    stmt = """select *
from a7table0 
where varchar_254
IN (select varchar_254 from a7table0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s2')
    
    stmt = """select empnum, pic_x253
from a7table0 
where pic_x253
IN (select pic_x253 from a7table0 
where pic_x253 is null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """drop table a7table0;"""
    output = _dci.cmdexec(stmt)
    
    #              End of test case ARKT0014
    _testmgr.testcase_end(desc)

