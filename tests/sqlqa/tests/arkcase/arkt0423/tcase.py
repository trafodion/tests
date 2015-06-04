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
    
def test001(desc="""Correlated subquery in having clause"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     A01
    #  Description:        Correlated subquery with IN clause between
    #                      outer query and subquery
    #                      Correlated subquery in having clause test
    #                      - tests the use of the IN operator connecting
    #                      the outer query with the subquery.
    #                      Vary attributes as described in testunit
    #                      comments . Test the use of NOT IN.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    #
    
    # Query 1
    # get supplier numbers for suppliers who supply part 4102
    
    stmt = """set param ?p 4102;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select suppnum
from """ + gvars.g_schema_arkcasedb + """.supplier 
group by suppnum
having ?p in
(select partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where  """ + gvars.g_schema_arkcasedb + """.supplier.suppnum = suppnum);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s0')
    
    #  Query 2
    #  same as above , add fromsup as qualifier for suppnum
    stmt = """select suppnum
from """ + gvars.g_schema_arkcasedb + """.supplier 
group by suppnum
having ?p in
(select partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where  """ + gvars.g_schema_arkcasedb + """.supplier.suppnum =  """ + gvars.g_schema_arkcasedb + """.fromsup.suppnum);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s1')
    
    #  Query 3
    #  get supplier numbers for suppliers who DON'T supply part 4102
    stmt = """select suppnum
from """ + gvars.g_schema_arkcasedb + """.supplier 
group by suppnum
having ?p   NOT in
(select partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where  """ + gvars.g_schema_arkcasedb + """.supplier.suppnum = suppnum);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s2')
    
    #  Query 4
    #  same as previous, except use alias
    stmt = """select suppnum
from """ + gvars.g_schema_arkcasedb + """.supplier X
group by suppnum
having ?p   NOT in
(select partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where X.suppnum = suppnum);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s3')
    
    #  Query 5
    #  get part numbers whose price is equal to its' cost from
    #  at least one supplier
    stmt = """select partnum
from """ + gvars.g_schema_arkcasedb + """.parts 
group by partnum, price
having price IN
(select partcost
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where  """ + gvars.g_schema_arkcasedb + """.parts.partnum =  """ + gvars.g_schema_arkcasedb + """.fromsup.partnum
group by partcost
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s4')
    
    # Query 6
    # same as above, except eliminate parts costing 20100
    stmt = """set param ?p 20100;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select partnum
from """ + gvars.g_schema_arkcasedb + """.parts 
group by partnum, price
having price IN
(select partcost
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where  """ + gvars.g_schema_arkcasedb + """.parts.partnum =  """ + gvars.g_schema_arkcasedb + """.fromsup.partnum
group by partcost
having partcost <> ?p
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s5')
    
    #  Query 7
    #  same as above, except eliminate 'group by' and use 'distinct'
    stmt = """select partnum
from """ + gvars.g_schema_arkcasedb + """.parts 
group by partnum, price
having price IN
(select distinct partcost
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where  """ + gvars.g_schema_arkcasedb + """.parts.partnum =  """ + gvars.g_schema_arkcasedb + """.fromsup.partnum
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s6')
    
    #  Query 8
    #  get part numbers for all parts supplied by more than one supplier
    stmt = """select distinct X.partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup X
group by partnum, suppnum
having X.partnum in
(select Y.partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup Y
where Y.suppnum <> X.suppnum
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s7')
    
    #  Query 9
    #  same as above, with 'distinct Y.partnum'
    stmt = """select distinct X.partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup X
group by partnum, suppnum
having X.partnum in
(select distinct Y.partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup Y
where Y.suppnum <> X.suppnum
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s8')
    
    #  Query 10
    #  same as first, with 'group by Y.partnum'
    stmt = """select distinct X.partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup X
group by partnum, suppnum
having X.partnum in
(select Y.partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup Y
where Y.suppnum <> X.suppnum
group by Y.partnum
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s9')
    
    # Query 11
    # use having clause to eliminate part # 4101 in subquery
    stmt = """set param ?p 4101;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select X.partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup X
group by partnum, suppnum
having X.partnum in
(select Y.partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup Y
where Y.suppnum <> X.suppnum
group by Y.partnum
having Y.partnum <> ?p
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s10')
    
    # Query 12
    # get salesman #'s and order #'s for salesman who have orders
    # for parts stored at location H76
    stmt = """set param ?p 'H76';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select salesman,ordernum
from """ + gvars.g_schema_arkcasedb + """.orders 
group by salesman, ordernum
having ?p in
(select """ + gvars.g_schema_arkcasedb + """.parts.location
from """ + gvars.g_schema_arkcasedb + """.odetail,""" + gvars.g_schema_arkcasedb + """.parts 
where ( """ + gvars.g_schema_arkcasedb + """.odetail.partnum =  """ + gvars.g_schema_arkcasedb + """.parts.partnum)
and ( """ + gvars.g_schema_arkcasedb + """.orders.ordernum =  """ + gvars.g_schema_arkcasedb + """.odetail.ordernum)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s11')
    
    #  Query 13
    #  same as above, use 'distinct parts.location'
    stmt = """select salesman,ordernum
from """ + gvars.g_schema_arkcasedb + """.orders 
group by salesman, ordernum
having ?p in
(select distinct  """ + gvars.g_schema_arkcasedb + """.parts.location
from """ + gvars.g_schema_arkcasedb + """.odetail,""" + gvars.g_schema_arkcasedb + """.parts 
where ( """ + gvars.g_schema_arkcasedb + """.odetail.partnum =  """ + gvars.g_schema_arkcasedb + """.parts.partnum)
and ( """ + gvars.g_schema_arkcasedb + """.orders.ordernum =  """ + gvars.g_schema_arkcasedb + """.odetail.ordernum) );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s12')
    
    #  Query 14
    #  same as first, use 'group by parts.location' to eliminate
    #  duplicates
    stmt = """select salesman,ordernum
from """ + gvars.g_schema_arkcasedb + """.orders 
group by salesman, ordernum
having ?p in
(select  """ + gvars.g_schema_arkcasedb + """.parts.location
from """ + gvars.g_schema_arkcasedb + """.odetail,""" + gvars.g_schema_arkcasedb + """.parts 
where ( """ + gvars.g_schema_arkcasedb + """.odetail.partnum =  """ + gvars.g_schema_arkcasedb + """.parts.partnum)
and ( """ + gvars.g_schema_arkcasedb + """.orders.ordernum =  """ + gvars.g_schema_arkcasedb + """.odetail.ordernum)
group by  """ + gvars.g_schema_arkcasedb + """.parts.location
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s13')
    
    #  Query 15
    #  same as first, except order by ordernum
    stmt = """select salesman,ordernum
from """ + gvars.g_schema_arkcasedb + """.orders 
group by salesman, ordernum
having ?p in
(select  """ + gvars.g_schema_arkcasedb + """.parts.location
from """ + gvars.g_schema_arkcasedb + """.odetail,""" + gvars.g_schema_arkcasedb + """.parts 
where ( """ + gvars.g_schema_arkcasedb + """.odetail.partnum =  """ + gvars.g_schema_arkcasedb + """.parts.partnum)
and ( """ + gvars.g_schema_arkcasedb + """.orders.ordernum =  """ + gvars.g_schema_arkcasedb + """.odetail.ordernum) )
order by ordernum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s14')
    
    #  Query 16
    #  get part numbers whose cost is greater than 10000 and whose
    #  price is equal to its' cost from at least one supplier
    #  NOTE: the subquery here returns 0 records sometimes.
    stmt = """select partnum
from """ + gvars.g_schema_arkcasedb + """.parts 
group by partnum, price
having price IN
(select partcost
from """ + gvars.g_schema_arkcasedb + """.expfroms 
where  """ + gvars.g_schema_arkcasedb + """.parts.partnum =  """ + gvars.g_schema_arkcasedb + """.expfroms.partnum
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s15')
    
    #  Query 17
    #  get salesman numbers for salesman who have already sold
    #  a previous order (a lower order number is a previous order)
    stmt = """select salesman
from """ + gvars.g_schema_arkcasedb + """.orders X
group by salesman, ordernum
having salesman in
(select salesman
from """ + gvars.g_schema_arkcasedb + """.orders Y
where Y.ordernum < X.ordernum
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s16')
    
    # Query 18
    # get employee names who do not work at first branches
    # (eliminate duplicates)
    stmt = """set param ?p 1;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select empname
from """ + gvars.g_schema_arkcasedb + """.employee 
group by branchnum, empname
having ?p not in
(select branchnum
from """ + gvars.g_schema_arkcasedb + """.branch 
where  """ + gvars.g_schema_arkcasedb + """.employee.branchnum =  """ + gvars.g_schema_arkcasedb + """.branch.branchnum
group by branchnum
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s17')
    
    # Query 19
    # same as above, use DISTINCT instead of GROUP BY
    stmt = """set param ?p 1;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select empname
from """ + gvars.g_schema_arkcasedb + """.employee 
group by branchnum, empname
having ?p not in
(select distinct branchnum
from """ + gvars.g_schema_arkcasedb + """.branch 
where  """ + gvars.g_schema_arkcasedb + """.employee.branchnum =  """ + gvars.g_schema_arkcasedb + """.branch.branchnum );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s18')
    
    # Query 20
    # same as query before last, but use HAVING with GROUP BY
    # instead of WHERE
    stmt = """set param ?p 1;"""
    output = _dci.cmdexec(stmt)
    stmt = """select empname
from """ + gvars.g_schema_arkcasedb + """.employee 
group by branchnum, empname
having ?p not in
(select branchnum
from """ + gvars.g_schema_arkcasedb + """.branch 
group by branchnum
having branchnum =  """ + gvars.g_schema_arkcasedb + """.employee.branchnum
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s19')
    
    # Query 21
    # get part numbers, for parts supplied by supplier 15 and
    # supplied by at least one other supplier
    stmt = """set param ?p 15;"""
    output = _dci.cmdexec(stmt)
    stmt = """select partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup X
where suppnum <> ?p
group by partnum
having ?p in
(select suppnum
from """ + gvars.g_schema_arkcasedb + """.fromsup Y
where Y.partnum = X.partnum
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s20')
    
    # Query 22
    # get customer numbers for customers who have not ordered parts
    # stored at location 'V67'
    stmt = """set param ?p 'V67';"""
    output = _dci.cmdexec(stmt)
    stmt = """select custnum
from """ + gvars.g_schema_arkcasedb + """.customer 
group by custnum
having ?p not in
(select col_2
from """ + gvars.g_schema_arkcasedb + """.partsfor 
where custnum = col_12
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s21')
    
    _testmgr.testcase_end(desc)

def test002(desc="""Correlated subquery in having clause test"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     A02
    #  Description:        Correlated subquery with simple and quantified
    #                      comparison operators between outer query and subquery
    #                      Correlated subquery in having clause test
    #                      - this tests the use of simple comparison operators
    #                      (<,<=,=,<>,>,>=) and quantified comparison operators
    #                      (=ANY,>ALL,etc.) as the relational operator
    #                      between the outer and subqueries.
    #                      Note that some of the subqueries in this testcase
    #                      return 0 records (empty sets ) sometimes.
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
    
    # Query 1
    # get employee name who is manager of region 1
    stmt = """set param ?p 0;"""
    output = _dci.cmdexec(stmt)
    stmt = """select empname
from """ + gvars.g_schema_arkcasedb + """.employee 
group by empnum, empname
having (?p + 1) =
(select regnum
from """ + gvars.g_schema_arkcasedb + """.region 
where manager = empnum);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s0')
    
    # Query 2
    # same as above, add qualifications
    stmt = """set param ?p 1;"""
    output = _dci.cmdexec(stmt)
    stmt = """select empname
from """ + gvars.g_schema_arkcasedb + """.employee 
group by empnum, empname
having ?p =
(select regnum
from """ + gvars.g_schema_arkcasedb + """.region 
where  """ + gvars.g_schema_arkcasedb + """.region.manager = """ + gvars.g_schema_arkcasedb + """.employee.empnum);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s1')
    
    # Query 3
    # get customer numbers whose salesman is not salesman #212
    stmt = """set param ?p 212;"""
    output = _dci.cmdexec(stmt)
    stmt = """select custnum
from """ + gvars.g_schema_arkcasedb + """.customer 
group by custnum
having ?p  <>
(select distinct col_11
from """ + gvars.g_schema_arkcasedb + """.partsfor 
where  """ + gvars.g_schema_arkcasedb + """.customer.custnum = """ + gvars.g_schema_arkcasedb + """.partsfor.col_12
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s2')
    
    # Query 4
    # same as above, use join instead of view partsfor
    stmt = """set param ?p 424;"""
    output = _dci.cmdexec(stmt)
    stmt = """select custnum
from """ + gvars.g_schema_arkcasedb + """.customer 
group by custnum
having (?p / 2) <>
(select distinct salesman
from """ + gvars.g_schema_arkcasedb + """.orders,""" + gvars.g_schema_arkcasedb + """.odetail,""" + gvars.g_schema_arkcasedb + """.parts 
where ( """ + gvars.g_schema_arkcasedb + """.orders.ordernum =  """ + gvars.g_schema_arkcasedb + """.odetail.ordernum)
and   ( """ + gvars.g_schema_arkcasedb + """.odetail.partnum =  """ + gvars.g_schema_arkcasedb + """.parts.partnum)
and   ( """ + gvars.g_schema_arkcasedb + """.customer.custnum = """ + gvars.g_schema_arkcasedb + """.orders.custnum)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s3')
    
    # Query 5
    # get part numbers for parts whose price is less than 2000
    # more than its' cost from all suppliers
    stmt = """set param ?p 1000;"""
    output = _dci.cmdexec(stmt)
    stmt = """select partnum
from """ + gvars.g_schema_arkcasedb + """.parts 
group by partnum, price
having (price - (?p * 2)) <all
(select partcost
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where  """ + gvars.g_schema_arkcasedb + """.parts.partnum = """ + gvars.g_schema_arkcasedb + """.fromsup.partnum
group by partcost
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s4')
    
    #  Query 6
    #  get part names for parts who have the same price as at
    #  least one other part
    stmt = """select col_1
from """ + gvars.g_schema_arkcasedb + """.partsfor X
group by col_1, col_3
having X.col_3 =SOME
(select Y.col_3
from """ + gvars.g_schema_arkcasedb + """.partsfor Y
where X.col_1 <> Y.col_1
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s5')
    
    #  Query 7
    #   get supplier numbers and part number for suppliers whose
    #   cost for that part is less than or equal to some other
    #   suppliers cost for that part
    #   note: subquery returns 0 records sometimes
    stmt = """select suppnum,partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup X
group by suppnum, partnum, partcost
having partcost <=SOME
(select partcost
from """ + gvars.g_schema_arkcasedb + """.fromsup Y
where X.suppnum <> Y.suppnum
and X.partnum = Y.partnum
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s6')
    
    #  Query 8
    #  same as above, use <=ANY instead of SOME
    stmt = """select suppnum,partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup X
group by suppnum, partnum, partcost
having partcost <=ANY
(select partcost
from """ + gvars.g_schema_arkcasedb + """.fromsup Y
where X.suppnum <> Y.suppnum
and X.partnum = Y.partnum
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s7')
    
    #  Query 9
    #  same as above, use <ALL instead
    stmt = """select suppnum,partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup X
group by suppnum, partnum, partcost
having partcost <ALL
(select partcost
from """ + gvars.g_schema_arkcasedb + """.fromsup Y
where X.suppnum <> Y.suppnum
and X.partnum = Y.partnum
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s8')
    
    # Query 10
    # get supplier numbers for suppliers who supply part 4102
    stmt = """set param ?p 4102;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select suppnum
from """ + gvars.g_schema_arkcasedb + """.supplier 
group by suppnum
having ?p =SOME
(select partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where  """ + gvars.g_schema_arkcasedb + """.supplier.suppnum = suppnum);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s9')
    
    #  Query 11
    #  same as above , add fromsup as qualifier for suppnum
    stmt = """select suppnum
from """ + gvars.g_schema_arkcasedb + """.supplier 
group by suppnum
having ?p =ANY
(select partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where  """ + gvars.g_schema_arkcasedb + """.supplier.suppnum =  """ + gvars.g_schema_arkcasedb + """.fromsup.suppnum);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s10')
    
    #  Query 12
    #  get supplier numbers for suppliers who DON'T supply part 4102
    stmt = """select suppnum
from """ + gvars.g_schema_arkcasedb + """.supplier 
group by suppnum
having ?p <> SOME
(select partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where  """ + gvars.g_schema_arkcasedb + """.supplier.suppnum = suppnum);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s11')
    
    #  Query 13
    #  same as previous, except use alias
    stmt = """select suppnum
from """ + gvars.g_schema_arkcasedb + """.supplier X
group by suppnum
having ?p <> ANY
(select partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where X.suppnum = suppnum);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s12')
    
    #  Query 14
    #  get part numbers whose price is equal to its' cost from
    #  at least one supplier
    stmt = """select partnum
from """ + gvars.g_schema_arkcasedb + """.parts 
group by partnum, price
having price =SOME
(select partcost
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where  """ + gvars.g_schema_arkcasedb + """.parts.partnum =  """ + gvars.g_schema_arkcasedb + """.fromsup.partnum
group by partcost
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s13')
    
    # Query 15
    # same as above, except eliminate parts costing 20100
    stmt = """set param ?p 20100;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select partnum
from """ + gvars.g_schema_arkcasedb + """.parts 
group by partnum, price
having price =ANY
(select partcost
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where  """ + gvars.g_schema_arkcasedb + """.parts.partnum =  """ + gvars.g_schema_arkcasedb + """.fromsup.partnum
group by partcost
having partcost <> ?p
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s14')
    
    #  Query 16
    #  same as above, except eliminate 'group by' and use 'distinct'
    stmt = """select partnum
from """ + gvars.g_schema_arkcasedb + """.parts 
group by partnum, price
having price =SOME
(select distinct partcost
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where  """ + gvars.g_schema_arkcasedb + """.parts.partnum =  """ + gvars.g_schema_arkcasedb + """.fromsup.partnum
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s15')
    
    #  Query 17
    #  get part numbers for all parts supplied by more than one supplier
    stmt = """select distinct X.partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup X
group by partnum, suppnum
having X.partnum =ANY
(select Y.partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup Y
where Y.suppnum <> X.suppnum
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s16')
    
    #  Query 18
    #  same as above, with 'distinct Y.partnum'
    stmt = """select distinct X.partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup X
group by partnum, suppnum
having X.partnum =SOME
(select distinct Y.partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup Y
where Y.suppnum <> X.suppnum
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s17')
    
    #  Query 19
    #  same as first, with 'group by Y.partnum'
    stmt = """select distinct X.partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup X
group by partnum, suppnum
having X.partnum =ANY
(select Y.partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup Y
where Y.suppnum <> X.suppnum
group by Y.partnum
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s18')
    
    #  Query 20
    #  use having clause to eliminate part # 4101 in subquery
    stmt = """select X.partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup X
group by partnum, suppnum
having X.partnum =SOME
(select Y.partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup Y
where Y.suppnum <> X.suppnum
group by Y.partnum
having Y.partnum <> 4101
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s19')
    
    # Query 21
    # get salesman #'s and order #'s for salesman who have
    # orders for parts stored at location H76
    stmt = """set param ?p 'H76';"""
    output = _dci.cmdexec(stmt)
    stmt = """select salesman,ordernum
from """ + gvars.g_schema_arkcasedb + """.orders 
group by ordernum, salesman
having ?p =ANY
(select """ + gvars.g_schema_arkcasedb + """.parts.location
from """ + gvars.g_schema_arkcasedb + """.odetail,""" + gvars.g_schema_arkcasedb + """.parts 
where ( """ + gvars.g_schema_arkcasedb + """.odetail.partnum =  """ + gvars.g_schema_arkcasedb + """.parts.partnum)
and ( """ + gvars.g_schema_arkcasedb + """.orders.ordernum =  """ + gvars.g_schema_arkcasedb + """.odetail.ordernum)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s20')
    
    #  Query 22
    #  same as above, use 'distinct parts.location'
    stmt = """select salesman,ordernum
from """ + gvars.g_schema_arkcasedb + """.orders 
group by ordernum, salesman
having ?p  =SOME
(select distinct """ + gvars.g_schema_arkcasedb + """.parts.location
from """ + gvars.g_schema_arkcasedb + """.odetail,""" + gvars.g_schema_arkcasedb + """.parts 
where ( """ + gvars.g_schema_arkcasedb + """.odetail.partnum =  """ + gvars.g_schema_arkcasedb + """.parts.partnum)
and ( """ + gvars.g_schema_arkcasedb + """.orders.ordernum =  """ + gvars.g_schema_arkcasedb + """.odetail.ordernum)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s21')
    
    #  Query 23
    #  same as first, use 'group by parts.location' to eliminate
    #  duplicates
    stmt = """select salesman,ordernum
from """ + gvars.g_schema_arkcasedb + """.orders 
group by ordernum, salesman
having ?p    =ANY
(select  """ + gvars.g_schema_arkcasedb + """.parts.location
from """ + gvars.g_schema_arkcasedb + """.odetail,""" + gvars.g_schema_arkcasedb + """.parts 
where ( """ + gvars.g_schema_arkcasedb + """.odetail.partnum =  """ + gvars.g_schema_arkcasedb + """.parts.partnum)
and ( """ + gvars.g_schema_arkcasedb + """.orders.ordernum =  """ + gvars.g_schema_arkcasedb + """.odetail.ordernum)
group by  """ + gvars.g_schema_arkcasedb + """.parts.location
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s22')
    #  Query 24
    #  same as first, except order by ordernum
    stmt = """select salesman,ordernum
from """ + gvars.g_schema_arkcasedb + """.orders 
group by ordernum, salesman
having ?p    =SOME
(select  """ + gvars.g_schema_arkcasedb + """.parts.location
from """ + gvars.g_schema_arkcasedb + """.odetail,""" + gvars.g_schema_arkcasedb + """.parts 
where ( """ + gvars.g_schema_arkcasedb + """.odetail.partnum =  """ + gvars.g_schema_arkcasedb + """.parts.partnum)
and ( """ + gvars.g_schema_arkcasedb + """.orders.ordernum =  """ + gvars.g_schema_arkcasedb + """.odetail.ordernum)
)
order by ordernum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s23')
    
    #  Query 25
    #  get part numbers whose cost is greater than 10000 and whose
    #  price is equal to its' cost from at least one supplier
    #  NOTE: the subquery here returns 0 records sometimes.
    stmt = """select partnum
from """ + gvars.g_schema_arkcasedb + """.parts 
group by partnum, price
having price =ANY
(select partcost
from """ + gvars.g_schema_arkcasedb + """.expfroms 
where  """ + gvars.g_schema_arkcasedb + """.parts.partnum =  """ + gvars.g_schema_arkcasedb + """.expfroms.partnum
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s24')
    
    #  Query 26
    #  get salesman numbers for salesman who have already sold
    #  a previous order (a lower order number is a previous
    #  order)
    stmt = """select salesman
from """ + gvars.g_schema_arkcasedb + """.orders X
group by salesman, ordernum
having salesman =SOME
(select salesman
from """ + gvars.g_schema_arkcasedb + """.orders Y
where Y.ordernum < X.ordernum
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s25')
    
    # Query 27
    # get employee names who do not work at first branches
    # (eliminate duplicates)
    stmt = """set param ?p 1;"""
    output = _dci.cmdexec(stmt)
    stmt = """select empname
from """ + gvars.g_schema_arkcasedb + """.employee 
group by branchnum, empname
having ?p <> ANY
(select branchnum
from """ + gvars.g_schema_arkcasedb + """.branch 
where  """ + gvars.g_schema_arkcasedb + """.employee.branchnum =  """ + gvars.g_schema_arkcasedb + """.branch.branchnum
group by branchnum
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s26')
    
    #  Query 28
    #  same as above, use DISTINCT instead of GROUP BY
    #  not =SOME
    stmt = """select empname
from """ + gvars.g_schema_arkcasedb + """.employee 
group by branchnum, empname
having ?p <> SOME
(select distinct branchnum
from """ + gvars.g_schema_arkcasedb + """.branch 
where  """ + gvars.g_schema_arkcasedb + """.employee.branchnum =  """ + gvars.g_schema_arkcasedb + """.branch.branchnum
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s27')
    #  Query 29
    #  same as above, use DISTINCT instead of GROUP BY
    stmt = """select empname
from """ + gvars.g_schema_arkcasedb + """.employee 
group by branchnum, empname
having  ?p  <> SOME
(select distinct branchnum
from """ + gvars.g_schema_arkcasedb + """.branch 
where  """ + gvars.g_schema_arkcasedb + """.employee.branchnum =  """ + gvars.g_schema_arkcasedb + """.branch.branchnum
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s28')
    
    # Query 30
    # same as query before last, but use HAVING with GROUP BY
    # instead of WHERE
    stmt = """set param ?p 1;"""
    output = _dci.cmdexec(stmt)
    stmt = """select empname
from """ + gvars.g_schema_arkcasedb + """.employee 
group by branchnum, empname
having ?p <> ANY
(select branchnum
from """ + gvars.g_schema_arkcasedb + """.branch 
group by branchnum
having branchnum =  """ + gvars.g_schema_arkcasedb + """.employee.branchnum
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s29')
    
    # Query 31
    # get customer numbers for customers who have not ordered parts
    # stored at location 'V67'
    stmt = """set param ?p 'V67';"""
    output = _dci.cmdexec(stmt)
    stmt = """select custnum
from """ + gvars.g_schema_arkcasedb + """.customer 
group by custnum
having ?p <> SOME
(select col_2
from """ + gvars.g_schema_arkcasedb + """.partsfor 
where custnum = col_12
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s30')
    
    _testmgr.testcase_end(desc)

def test003(desc="""correlated subquery with translated IN form of"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #  EXISTS/NOT EXISTS
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     A03
    #  Description:        Correlated subquery in having clause test
    #                      - this tests the use of a correlated subquery
    #                      with translated IN form of EXISTS/NOT EXISTS
    #                      quanitifiers.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    #  Notes:
    #  This test case incorporates features detailed in the "Title"
    #  by Ima Programmer (Version 1.1, <date>).
    #
    # =================== End Test Case Header  ===================
    
    # Query 1
    # get supplier numbers for suppliers who supply part 4102
    stmt = """set param ?p 4102;"""
    output = _dci.cmdexec(stmt)
    stmt = """select suppnum
from """ + gvars.g_schema_arkcasedb + """.supplier 
group by suppnum
having exists
(select *
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where  """ + gvars.g_schema_arkcasedb + """.supplier.suppnum = suppnum
and partnum = ?p
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s0')
    
    #  Query 2
    #  same as above, change 'select *' to 'select partnum'
    stmt = """select suppnum
from """ + gvars.g_schema_arkcasedb + """.supplier 
group by suppnum
having exists
(select partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where  """ + gvars.g_schema_arkcasedb + """.supplier.suppnum = suppnum
and partnum = ?p
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s1')
    
    #  Query 3
    #  get supplier names for suppliers who DON'T supply part 4102       y
    stmt = """select suppnum
from """ + gvars.g_schema_arkcasedb + """.supplier 
group by suppnum
having not exists
(select *
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where  """ + gvars.g_schema_arkcasedb + """.supplier.suppnum = suppnum
and partnum = ?p
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s2')
    
    #  Query 4
    #  get part numbers for all parts supplied by more than
    #  one supplier
    stmt = """select distinct X.partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup X
group by partnum, suppnum
having exists
(select Y.partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup Y
where Y.suppnum <> X.suppnum
and X.partnum = Y.partnum
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s3')
    
    # Query 5
    # get salesman #'s and order #'s for salesman who have orders
    # for parts stored at location H76
    stmt = """set param ?p 'H76';"""
    output = _dci.cmdexec(stmt)
    stmt = """select salesman,ordernum
from """ + gvars.g_schema_arkcasedb + """.orders 
group by salesman, ordernum
having exists
(select *
from """ + gvars.g_schema_arkcasedb + """.odetail,""" + gvars.g_schema_arkcasedb + """.parts 
where ( """ + gvars.g_schema_arkcasedb + """.odetail.partnum =  """ + gvars.g_schema_arkcasedb + """.parts.partnum)
and ( """ + gvars.g_schema_arkcasedb + """.orders.ordernum =  """ + gvars.g_schema_arkcasedb + """.odetail.ordernum)
and ( """ + gvars.g_schema_arkcasedb + """.parts.location = ?p)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s4')
    
    #  Query 6
    #  get part numbers whose cost is greater than 10000 and whose
    #  price is equal to its' cost from at least one supplier
    stmt = """select partnum
from """ + gvars.g_schema_arkcasedb + """.parts 
group by partnum, price
having exists
(select *
from """ + gvars.g_schema_arkcasedb + """.expfroms 
where ( """ + gvars.g_schema_arkcasedb + """.parts.partnum =  """ + gvars.g_schema_arkcasedb + """.expfroms.partnum)
and (price = partcost)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s5')
    
    #  Query 7
    #  get salesman numbers for salesman who have already sold
    #  a previous order (a lower order number is a previous order)
    stmt = """select salesman
from """ + gvars.g_schema_arkcasedb + """.orders X
group by salesman, ordernum
having exists
(select salesman
from """ + gvars.g_schema_arkcasedb + """.orders Y
where (Y.ordernum < X.ordernum)
and (X.salesman = Y.salesman)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s6')
    
    # Query 8
    # get employee names who do not work at first branches
    # (eliminate duplicates)
    stmt = """set param ?p 1;"""
    output = _dci.cmdexec(stmt)
    stmt = """select empname
from """ + gvars.g_schema_arkcasedb + """.employee 
group by branchnum, empname
having not exists
(select branchnum
from """ + gvars.g_schema_arkcasedb + """.branch 
where ( """ + gvars.g_schema_arkcasedb + """.employee.branchnum =  """ + gvars.g_schema_arkcasedb + """.branch.branchnum)
and (branchnum = ?p)
group by branchnum
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s7')
    
    #  Query 9
    #  get employee names who do not work at first branches
    #   eliminate duplicates and use having clause
    stmt = """select empname
from """ + gvars.g_schema_arkcasedb + """.employee 
group by branchnum, empname
having not exists
(select branchnum
from """ + gvars.g_schema_arkcasedb + """.branch 
where ( """ + gvars.g_schema_arkcasedb + """.employee.branchnum =  """ + gvars.g_schema_arkcasedb + """.branch.branchnum)
group by branchnum
having branchnum = ?p
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s8')
    
    # Query 10
    # get part numbers for parts supplied by supplier 15
    # and supplied by at least one other supplier
    stmt = """set param ?p 15;"""
    output = _dci.cmdexec(stmt)
    stmt = """select partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup X
where suppnum <> ?p
group by partnum
having exists
(select *
from """ + gvars.g_schema_arkcasedb + """.fromsup Y
where (Y.partnum = X.partnum)
and (suppnum = ?p)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s9')
    
    # Query 11
    # get supplier numbers for suppliers who are in the same state      e
    # as supplier 1
    stmt = """set param ?p 1;"""
    output = _dci.cmdexec(stmt)
    stmt = """select suppnum
from """ + gvars.g_schema_arkcasedb + """.supplier X
group by state, suppnum
having exists
(select suppnum
from """ + gvars.g_schema_arkcasedb + """.supplier Y
where (Y.state = X.state)
and (suppnum = ?p)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s10')
    
    # Query 12
    # get customer numbers for customers who have not ordered
    # parts stored at location V67
    stmt = """set param ?p 'V67';"""
    output = _dci.cmdexec(stmt)
    stmt = """select custnum
from """ + gvars.g_schema_arkcasedb + """.customer 
group by custnum
having not exists
(select *
from """ + gvars.g_schema_arkcasedb + """.partsfor 
where (custnum = col_12)
and (col_2 = ?p)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s11')
    
    _testmgr.testcase_end(desc)

def test004(desc="""multiply nested subqueries and multiple subqueries"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #  connected with and/or.
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     A04
    #  Description:        Multiple nesting,multiple subqueries connected
    #                      with and/or,mixed correlated/uncorrelated
    #                      nested subqueries
    #                      Correlated subquery in having clause test
    #                      - this tests multiply nested subqueries and
    #                      multiple subqueries connected with and/or.
    #                      This testcase also tests SELECT's with
    #                      subqueries in both the where clause and having
    #                      clause, both seperate and nested, correlated
    #                      and uncorrelated.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    #  Notes:
    #  This test case incorporates features detailed in the "Title"
    #  by Ima Programmer (Version 1.1, <date>).
    #
    # =================== End Test Case Header  ===================
    
    # Query 1
    # get supplier numbers for suppliers who supply
    # part 4102 and part 5504
    stmt = """set param ?p 4102;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p1 5504;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select suppnum
from """ + gvars.g_schema_arkcasedb + """.supplier 
group by suppnum
having ?p in
(select partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where  """ + gvars.g_schema_arkcasedb + """.fromsup.suppnum =  """ + gvars.g_schema_arkcasedb + """.supplier.suppnum
)
and ?p1 =ANY
(select partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where  """ + gvars.g_schema_arkcasedb + """.fromsup.suppnum =  """ + gvars.g_schema_arkcasedb + """.supplier.suppnum
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s0')
    
    #  Query 2
    #  get supplier numbers for suppliers who supply part 4102
    #  and part 5504, except use a subquery in both a where
    #  clause and having clause
    stmt = """select suppnum
from """ + gvars.g_schema_arkcasedb + """.supplier 
where ?p in
(select partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where  """ + gvars.g_schema_arkcasedb + """.fromsup.suppnum =  """ + gvars.g_schema_arkcasedb + """.supplier.suppnum
)
group by suppnum
having ?p1 =ANY
(select partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where  """ + gvars.g_schema_arkcasedb + """.fromsup.suppnum =  """ + gvars.g_schema_arkcasedb + """.supplier.suppnum
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s1')
    
    #  Query 3
    #  same as first,except one subquery correlated, other uncorrelated
    stmt = """select suppnum
from """ + gvars.g_schema_arkcasedb + """.supplier 
group by suppnum
having ?p in
(select partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where  """ + gvars.g_schema_arkcasedb + """.fromsup.suppnum =  """ + gvars.g_schema_arkcasedb + """.supplier.suppnum
)
and suppnum =ANY
(select suppnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where partnum = ?p1
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s2')
    
    #  Query 4
    #  get supplier numbers for suppliers who supply part 4102
    #  and part 5504, except use a subquery in both a where
    #  clause and having clause, and use one correlated and one
    #  uncorrelated subquery
    stmt = """select suppnum
from """ + gvars.g_schema_arkcasedb + """.supplier 
where ?p in
(select partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where  """ + gvars.g_schema_arkcasedb + """.fromsup.suppnum =  """ + gvars.g_schema_arkcasedb + """.supplier.suppnum
)
group by suppnum
having suppnum =ANY
(select suppnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where partnum = ?p1
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s3')
    
    #  Query 5
    #  get supplier numbers for suppliers who supply part 4102
    #  OR 5504
    stmt = """select suppnum
from """ + gvars.g_schema_arkcasedb + """.supplier 
group by suppnum
having ?p in
(select partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where """ + gvars.g_schema_arkcasedb + """.fromsup.suppnum = """ + gvars.g_schema_arkcasedb + """.supplier.suppnum
)
OR ?p1 =ANY
(select partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where """ + gvars.g_schema_arkcasedb + """.fromsup.suppnum = """ + gvars.g_schema_arkcasedb + """.supplier.suppnum
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s4')
    
    #  Query 6
    #  same as above, except one subquery correlated, other uncorrelated
    stmt = """select suppnum
from """ + gvars.g_schema_arkcasedb + """.supplier 
group by suppnum
having ?p in
(select partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where  """ + gvars.g_schema_arkcasedb + """.fromsup.suppnum = """ + gvars.g_schema_arkcasedb + """.supplier.suppnum
)
OR suppnum =ANY
(select suppnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where partnum = ?p1
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s5')
    
    #  Query 7
    #  get supplier numbers for suppliers who DON'T supply parts
    #  4102 or 5504
    stmt = """select suppnum
from """ + gvars.g_schema_arkcasedb + """.supplier 
group by suppnum
having NOT (?p in
(select partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where  """ + gvars.g_schema_arkcasedb + """.fromsup.suppnum =  """ + gvars.g_schema_arkcasedb + """.supplier.suppnum
)
OR suppnum =ANY
(select suppnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where partnum = ?p1
));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s6')
    
    #  Query 8
    #  get supplier numbers for suppliers who DON'T supply parts
    #  4102 or 5504, except use a subquery in both the where clause
    #  and a having clause
    stmt = """select suppnum
from """ + gvars.g_schema_arkcasedb + """.supplier 
where NOT (?p in
(select partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where  """ + gvars.g_schema_arkcasedb + """.fromsup.suppnum =  """ + gvars.g_schema_arkcasedb + """.supplier.suppnum
))
group by suppnum
having suppnum <> ANY
(select suppnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where partnum = ?p1
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s7')
    
    # Query 9
    # get supplier numbers for suppliers who supply parts 4102,
    # 5504, and 5505
    stmt = """set param ?p2 5505;"""
    output = _dci.cmdexec(stmt)
    stmt = """select suppnum
from """ + gvars.g_schema_arkcasedb + """.supplier 
group by suppnum
having ?p in
(select partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where  """ + gvars.g_schema_arkcasedb + """.fromsup.suppnum =  """ + gvars.g_schema_arkcasedb + """.supplier.suppnum
)
and ?p1 =ANY
(select partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where  """ + gvars.g_schema_arkcasedb + """.fromsup.suppnum =  """ + gvars.g_schema_arkcasedb + """.supplier.suppnum
)
and suppnum =SOME
(select suppnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where partnum = ?p2
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s8')
    
    # Query 10
    # get supplier numbers for suppliers who supply at least
    # one part whose inventory is negative (both subqueries in
    # a having clause)
    stmt = """set param ?p 1;"""
    output = _dci.cmdexec(stmt)
    stmt = """select suppnum
from """ + gvars.g_schema_arkcasedb + """.supplier 
group by suppnum
having suppnum in
(select suppnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
group by partnum, suppnum
having (0/ ?p) >
(select inventory
from """ + gvars.g_schema_arkcasedb + """.parts 
where  """ + gvars.g_schema_arkcasedb + """.parts.partnum =  """ + gvars.g_schema_arkcasedb + """.fromsup.partnum
)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s9')
    
    # Query 11
    # get supplier numbers for suppliers who supply at least
    # one part whose inventory is negative  (put outer subquery
    # in a having clause and the inner in a where clause)
    stmt = """set param ?p 1;"""
    output = _dci.cmdexec(stmt)
    stmt = """select suppnum
from """ + gvars.g_schema_arkcasedb + """.supplier 
group by suppnum
having suppnum in
(select suppnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where (?p - 1) >
(select inventory
from """ + gvars.g_schema_arkcasedb + """.parts 
where  """ + gvars.g_schema_arkcasedb + """.parts.partnum =  """ + gvars.g_schema_arkcasedb + """.fromsup.partnum
)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s10')
    
    # Query 12
    # get supplier names for suppliers who supply at least
    # one part whose inventory is negative (put outer subquery
    # in a where clause and the inner in a having clause)
    stmt = """set param ?p 0;"""
    output = _dci.cmdexec(stmt)
    stmt = """select suppname
from """ + gvars.g_schema_arkcasedb + """.supplier 
where suppnum in
(select suppnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
group by partnum, suppnum
having ?p >
(select inventory
from """ + gvars.g_schema_arkcasedb + """.parts 
where  """ + gvars.g_schema_arkcasedb + """.parts.partnum =  """ + gvars.g_schema_arkcasedb + """.fromsup.partnum
)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s11')
    
    # Query 13
    # get supplier numbers for suppliers who supply part 'LP 900 LPM'
    # (put both subqueries in having clauses)
    stmt = """set param ?p 'LP  900 LPM';"""
    output = _dci.cmdexec(stmt)
    stmt = """select suppnum
from """ + gvars.g_schema_arkcasedb + """.supplier 
group by suppnum
having suppnum IN
(select suppnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
group by suppnum, partnum
having ?p in
(select partname
from """ + gvars.g_schema_arkcasedb + """.parts 
where  """ + gvars.g_schema_arkcasedb + """.parts.partnum =  """ + gvars.g_schema_arkcasedb + """.fromsup.partnum
)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s12')
    
    #  Query 14
    #  get supplier numbers for suppliers who supply part 'LP 900 LPM'
    #  (put outer subquery in a having clause, inner in a where clause)
    stmt = """select suppnum
from """ + gvars.g_schema_arkcasedb + """.supplier 
group by suppnum
having suppnum IN
(select suppnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where ?p in
(select partname
from """ + gvars.g_schema_arkcasedb + """.parts 
where  """ + gvars.g_schema_arkcasedb + """.parts.partnum =  """ + gvars.g_schema_arkcasedb + """.fromsup.partnum
)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s13')
    
    #  Query 15
    #  get supplier names for suppliers who supply part LP 900 LPM
    #  (put inner subquery in a having clause, outer in a where clause)
    stmt = """select suppname
from """ + gvars.g_schema_arkcasedb + """.supplier 
where suppnum IN
(select suppnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
group by suppnum, partnum
having ?p in
(select partname
from """ + gvars.g_schema_arkcasedb + """.parts 
where  """ + gvars.g_schema_arkcasedb + """.parts.partnum =  """ + gvars.g_schema_arkcasedb + """.fromsup.partnum
)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s14')
    
    #  Query 16
    #  get employee names for employees who do not work at branches
    #  which are in the same city as the regional headquarters
    #  (put both subqueries in having clauses)
    stmt = """select empname
from """ + gvars.g_schema_arkcasedb + """.employee 
group by empname, branchnum, regnum
having branchnum not in
(select branchnum
from """ + gvars.g_schema_arkcasedb + """.branch 
group by  """ + gvars.g_schema_arkcasedb + """.branch.branchnum,  """ + gvars.g_schema_arkcasedb + """.branch.regnum,
 """ + gvars.g_schema_arkcasedb + """.branch.branchname
having  """ + gvars.g_schema_arkcasedb + """.branch.regnum =  """ + gvars.g_schema_arkcasedb + """.employee.regnum
and branchname =
(select location
from """ + gvars.g_schema_arkcasedb + """.region 
where  """ + gvars.g_schema_arkcasedb + """.region.regnum =  """ + gvars.g_schema_arkcasedb + """.employee.regnum
)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s15')
    
    #  Query 17
    #  get employee names for employees who do not work at branches
    #  which are in the same city as the regional headquarters
    #  (put outer subquery in a having clause, inner in where clause)
    stmt = """select empname
from """ + gvars.g_schema_arkcasedb + """.employee 
group by empname, branchnum, regnum
having branchnum not in
(select branchnum
from """ + gvars.g_schema_arkcasedb + """.branch 
where  """ + gvars.g_schema_arkcasedb + """.branch.regnum =  """ + gvars.g_schema_arkcasedb + """.employee.regnum
and branchname =
(select location
from """ + gvars.g_schema_arkcasedb + """.region 
where  """ + gvars.g_schema_arkcasedb + """.region.regnum =  """ + gvars.g_schema_arkcasedb + """.employee.regnum
)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s16')
    
    #  Query 18
    #  get employee names for employees who do not work at branches
    #  which are in the same city as the regional headquarters
    #  (put inner subquery in a having clause, outer in where clause)
    stmt = """select empname
from """ + gvars.g_schema_arkcasedb + """.employee 
where branchnum not in
(select branchnum
from """ + gvars.g_schema_arkcasedb + """.branch 
group by  """ + gvars.g_schema_arkcasedb + """.branch.branchnum,  """ + gvars.g_schema_arkcasedb + """.branch.regnum,
 """ + gvars.g_schema_arkcasedb + """.branch.branchname
having  """ + gvars.g_schema_arkcasedb + """.branch.regnum =  """ + gvars.g_schema_arkcasedb + """.employee.regnum
and branchname =
(select location
from """ + gvars.g_schema_arkcasedb + """.region 
where  """ + gvars.g_schema_arkcasedb + """.region.regnum =  """ + gvars.g_schema_arkcasedb + """.employee.regnum
)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s17')
    
    #  Query 19
    #  get part numbers for all parts supplied by more than
    #  two suppliers
    #  (put both subqueries in having clauses)
    stmt = """select distinct X.partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup X
group by partnum, suppnum
having X.partnum in
(select Y.partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup Y
group by partnum, suppnum
having Y.suppnum <> X.suppnum
and Y.partnum in
(select Z.partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup Z
where Z.suppnum <> Y.suppnum
and Z.suppnum <> X.suppnum
)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s18')
    
    #  Query 20
    #  get part numbers for all parts supplied by more than
    #  two suppliers
    #  (put outer subquery in a having clause, inner in a where clause)
    stmt = """select distinct X.partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup X
group by partnum, suppnum
having X.partnum in
(select Y.partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup Y
where Y.suppnum <> X.suppnum
and Y.partnum in
(select Z.partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup Z
where Z.suppnum <> Y.suppnum
and Z.suppnum <> X.suppnum
)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s19')
    
    #  Query 21
    #  get part numbers for all parts supplied by more than
    #  two suppliers
    #  (put both subqueries in having clauses, but also use a where
    #  clause in the inner subquery. This tests the use of the same
    #  correlation variable in both a WHERE clause and a GROUP BY
    #  clause.
    stmt = """select distinct X.partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup X
group by partnum, suppnum
having X.partnum in
(select Y.partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup Y
where Y.suppnum <> X.suppnum
group by partnum, suppnum
having Y.partnum in
(select Z.partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup Z
where Z.suppnum <> Y.suppnum
and Z.suppnum <> X.suppnum
)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s20')
    
    #  Query 22
    #  get part numbers for all parts supplied by more than
    #  two suppliers
    #  (put inner subquery in a having clause, outer in a where clause)
    stmt = """select distinct X.partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup X
where X.partnum in
(select Y.partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup Y
group by partnum, suppnum
having Y.suppnum <> X.suppnum
and Y.partnum in
(select Z.partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup Z
where Z.suppnum <> Y.suppnum
and Z.suppnum <> X.suppnum
)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s21')
    
    #  Query 23
    #  same as above, use view fsdetail instead
    stmt = """select distinct X.col_1
from """ + gvars.g_schema_arkcasedb + """.fsdetail X
group by col_1, col_2
having X.col_1 in
(select Y.col_1
from """ + gvars.g_schema_arkcasedb + """.fsdetail Y
group by col_1, col_2
having Y.col_2 <> X.col_2
and Y.col_1 in
(select Z.col_1
from """ + gvars.g_schema_arkcasedb + """.fsdetail Z
where Z.col_2 <> Y.col_2
and Z.col_2 <> X.col_2
)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s22')
    
    #  Query 24
    #  same as above, except use table fromsup instead of fsdetail
    #  for one of the fsdetail occurences
    stmt = """select distinct partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
group by partnum, suppnum
having partnum in
(select Y.col_1
from """ + gvars.g_schema_arkcasedb + """.fsdetail Y
group by col_1, col_2
having Y.col_2 <>  """ + gvars.g_schema_arkcasedb + """.fromsup.suppnum
and Y.col_1 in
(select Z.col_1
from """ + gvars.g_schema_arkcasedb + """.fsdetail Z
where Z.col_2 <> Y.col_2
and Z.col_2 <>  """ + gvars.g_schema_arkcasedb + """.fromsup.suppnum
)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s23')
    
    #  Query 25
    #  get salesman numbers and order numbers for salesman who
    #  have orders for parts stored at location H76 and which
    #  have a cost less than or equal to 2500 from all
    #  suppliers that supply that part
    
    # EL 01/08/98
    stmt = """select salesman,ordernum
from """ + gvars.g_schema_arkcasedb + """.orders 
group by ordernum, salesman
having 'H76' in
(select  """ + gvars.g_schema_arkcasedb + """.parts.location
from """ + gvars.g_schema_arkcasedb + """.odetail,""" + gvars.g_schema_arkcasedb + """.parts 
where ( """ + gvars.g_schema_arkcasedb + """.odetail.partnum =  """ + gvars.g_schema_arkcasedb + """.parts.partnum)
and ( """ + gvars.g_schema_arkcasedb + """.orders.ordernum =  """ + gvars.g_schema_arkcasedb + """.odetail.ordernum)
group by  """ + gvars.g_schema_arkcasedb + """.parts.partnum,""" + gvars.g_schema_arkcasedb + """.parts.location,
 """ + gvars.g_schema_arkcasedb + """.odetail.partnum
having 2500 >ALL
(select partcost
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where  """ + gvars.g_schema_arkcasedb + """.fromsup.partnum =  """ + gvars.g_schema_arkcasedb + """.odetail.partnum
)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s24')
    
    # Query 26
    # same as above, except use additional subquery instead of join
    stmt = """set param ?p 'H76';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p1 2000;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p2 500;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select salesman,ordernum
from """ + gvars.g_schema_arkcasedb + """.orders 
group by ordernum, salesman
having ordernum in
(select ordernum
from """ + gvars.g_schema_arkcasedb + """.odetail 
group by ordernum, partnum
having ?p in
(select location
from """ + gvars.g_schema_arkcasedb + """.parts 
group by partnum, location
having partnum =  """ + gvars.g_schema_arkcasedb + """.odetail.partnum
and (?p1 + ?p2) >ALL
(select partcost
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where  """ + gvars.g_schema_arkcasedb + """.fromsup.partnum =  """ + gvars.g_schema_arkcasedb + """.odetail.partnum
)
)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s25')
    
    _testmgr.testcase_end(desc)

def test005(desc="""The use of for read uncommitted access"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     A05
    #  Description:        Correlated subquery in having clause test
    #                      - this tests the use of for read uncommitted access,
    #                      for read uncommitted access, and for
    #                      serializable access inside of subqueries.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    #  Notes:
    #
    # =================== End Test Case Header  ===================
    #
    
    #  Query 1
    #  get part numbers for all parts supplied by more than one supplier
    stmt = """select distinct X.partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup X
group by partnum, suppnum
having X.partnum in
(select distinct Y.partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup Y
where Y.suppnum <> X.suppnum
for read uncommitted access
)
for read committed access
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s0')
    
    #  Query 2
    #  get part numbers for all parts supplied by more than one supplier
    stmt = """select distinct X.partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup X
group by partnum, suppnum
having X.partnum in
(select distinct Y.partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup Y
where Y.suppnum <> X.suppnum
for read committed access
)
for serializable access
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s1')
    
    #  Query 3
    #  get part numbers for all parts supplied by more than one supplier
    stmt = """select distinct X.partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup X
group by partnum, suppnum
having X.partnum in
(select distinct Y.partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup Y
where Y.suppnum <> X.suppnum
for serializable access
)
for serializable access
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s2')
    
    #  Query 4
    #  get part numbers whose cost is greater than 10000 and whose
    #  price is equal to its' cost from at least one supplier
    #  NOTE: the subquery here returns 0 records sometimes.
    stmt = """select partnum
from """ + gvars.g_schema_arkcasedb + """.parts 
group by partnum, price
having price IN
(select partcost
from """ + gvars.g_schema_arkcasedb + """.expfroms 
where  """ + gvars.g_schema_arkcasedb + """.parts.partnum =  """ + gvars.g_schema_arkcasedb + """.expfroms.partnum
for serializable access
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s3')
    
    # Query 5
    # get part numbers for parts whose price is less than 2000
    # more than its' cost from all suppliers
    stmt = """set param ?p 4000;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select partnum
from """ + gvars.g_schema_arkcasedb + """.parts 
group by partnum, price
having (price - ?p /2) <all
(select partcost
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where  """ + gvars.g_schema_arkcasedb + """.parts.partnum =  """ + gvars.g_schema_arkcasedb + """.fromsup.partnum
group by partcost
for read uncommitted access
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s4')
    
    #  Query 6
    #  get part names for parts who have the same price as at
    #  least one other part
    stmt = """select col_1
from """ + gvars.g_schema_arkcasedb + """.partsfor X
group by col_1, col_3
having X.col_3 =SOME
(select Y.col_3
from """ + gvars.g_schema_arkcasedb + """.partsfor Y
where X.col_1 <> Y.col_1
for read uncommitted access
)
for read uncommitted access
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s5')
    
    #  Query 7
    #  get part names for parts who have the same price as at
    #  least one other part
    stmt = """select col_1
from """ + gvars.g_schema_arkcasedb + """.partsfor X
group by col_1, col_3
having X.col_3 =SOME
(select Y.col_3
from """ + gvars.g_schema_arkcasedb + """.partsfor Y
where X.col_1 <> Y.col_1
for read committed access
)
for read committed access
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s6')
    
    #  Query 8
    #  get part names for parts who have the same price as at
    #  least one other part
    stmt = """select col_1
from """ + gvars.g_schema_arkcasedb + """.partsfor X
group by col_1, col_3
having X.col_3 =SOME
(select Y.col_3
from """ + gvars.g_schema_arkcasedb + """.partsfor Y
where X.col_1 <> Y.col_1
for serializable access
)
for read uncommitted access
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s7')
    
    #  Query 9
    #  get part numbers for all parts supplied by more than
    #  one supplier
    stmt = """select distinct X.partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup X
group by partnum, suppnum
having exists
(select Y.partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup Y
where Y.suppnum <> X.suppnum
and X.partnum = Y.partnum
for serializable access
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s8')
    
    # Query 10
    
    # get supplier numbers for suppliers who supply part 4102
    # and part 5504
    stmt = """set param ?p 4102;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p1 5504;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select suppnum
from """ + gvars.g_schema_arkcasedb + """.supplier 
group by suppnum
having ?p in
(select partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where  """ + gvars.g_schema_arkcasedb + """.fromsup.suppnum =  """ + gvars.g_schema_arkcasedb + """.supplier.suppnum
for serializable access
)
and ?p1 =ANY
(select partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where  """ + gvars.g_schema_arkcasedb + """.fromsup.suppnum =  """ + gvars.g_schema_arkcasedb + """.supplier.suppnum
for read committed access
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s9')
    
    #  Query 11
    #  get supplier numbers for suppliers who supply part 4102
    #  and part 5504, except use a subquery in both a where clause
    #  and having clause
    
    stmt = """select suppnum
from """ + gvars.g_schema_arkcasedb + """.supplier 
where ?p in
(select partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where  """ + gvars.g_schema_arkcasedb + """.fromsup.suppnum =  """ + gvars.g_schema_arkcasedb + """.supplier.suppnum
for serializable access
)
group by suppnum
having ?p1 =ANY
(select partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where  """ + gvars.g_schema_arkcasedb + """.fromsup.suppnum = """ + gvars.g_schema_arkcasedb + """.supplier.suppnum
for read uncommitted access
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s10')
    
    #  Query 12
    #  get employee names for employees who do not work at branches
    #  which are in the same city as the regional headquarters
    #  (put both subqueries in having clauses)
    stmt = """select empname
from """ + gvars.g_schema_arkcasedb + """.employee 
group by empname, branchnum, regnum
having branchnum not in
(select branchnum
from """ + gvars.g_schema_arkcasedb + """.branch 
group by  """ + gvars.g_schema_arkcasedb + """.branch.branchnum,  """ + gvars.g_schema_arkcasedb + """.branch.regnum,
 """ + gvars.g_schema_arkcasedb + """.branch.branchname
having  """ + gvars.g_schema_arkcasedb + """.branch.regnum =  """ + gvars.g_schema_arkcasedb + """.employee.regnum
and branchname =
(select location
from """ + gvars.g_schema_arkcasedb + """.region 
where  """ + gvars.g_schema_arkcasedb + """.region.regnum =  """ + gvars.g_schema_arkcasedb + """.employee.regnum
for read uncommitted access
)
for read committed access
)
for serializable access
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s11')
    
    #  Query 13
    #  get employee names for employees who do not work at branches
    #  which are in the same city as the regional headquarters
    #  (put outer subquery in where clause, inner in having clause)
    stmt = """select empname
from """ + gvars.g_schema_arkcasedb + """.employee 
where branchnum not in
(select branchnum
from """ + gvars.g_schema_arkcasedb + """.branch 
group by  """ + gvars.g_schema_arkcasedb + """.branch.branchnum,  """ + gvars.g_schema_arkcasedb + """.branch.regnum,
 """ + gvars.g_schema_arkcasedb + """.branch.branchname
having  """ + gvars.g_schema_arkcasedb + """.branch.regnum =  """ + gvars.g_schema_arkcasedb + """.employee.regnum
and branchname =
(select location
from """ + gvars.g_schema_arkcasedb + """.region 
where  """ + gvars.g_schema_arkcasedb + """.region.regnum =  """ + gvars.g_schema_arkcasedb + """.employee.regnum
for serializable access
)
for read committed access
)
for read uncommitted access
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s12')
    
    #  Query 14
    #  get part numbers for all parts supplied by more than
    #  two suppliers
    #  (put both subqueries in having clauses)
    stmt = """select distinct X.partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup X
group by partnum, suppnum
having X.partnum in
(select Y.partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup Y
group by partnum, suppnum
having Y.suppnum <> X.suppnum
and Y.partnum in
(select Z.partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup Z
where Z.suppnum <> Y.suppnum
and Z.suppnum <> X.suppnum
for read committed access
)
for read uncommitted access
)
for serializable access
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s13')
    
    #  Query 15
    #  same as above, use view fsdetail instead
    stmt = """select distinct X.col_1
from """ + gvars.g_schema_arkcasedb + """.fsdetail X
group by col_1, col_2
having X.col_1 in
(select Y.col_1
from """ + gvars.g_schema_arkcasedb + """.fsdetail Y
group by col_1, col_2
having Y.col_2 <> X.col_2
and Y.col_1 in
(select Z.col_1
from """ + gvars.g_schema_arkcasedb + """.fsdetail Z
where Z.col_2 <> Y.col_2
and Z.col_2 <> X.col_2
for read uncommitted access
)
for serializable access
)
for read committed access
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s14')
    
    #  Query 16
    #  same as above, except use table fromsup instead of fsdetail
    #  for one of the fsdetail occurences
    stmt = """select distinct partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
group by partnum, suppnum
having partnum in
(select Y.col_1
from """ + gvars.g_schema_arkcasedb + """.fsdetail Y
group by col_1, col_2
having Y.col_2 <>  """ + gvars.g_schema_arkcasedb + """.fromsup.suppnum
and Y.col_1 in
(select Z.col_1
from """ + gvars.g_schema_arkcasedb + """.fsdetail Z
where Z.col_2 <> Y.col_2
and Z.col_2 <>  """ + gvars.g_schema_arkcasedb + """.fromsup.suppnum
for serializable access
)
for serializable access
)
for serializable access
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s15')
    
    _testmgr.testcase_end(desc)

def test006(desc="""The selection of aggregate functions (COUNT, AVG, MAX, MIN, SUM)"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     A06
    #  Description:        Select correlated subquery in HAVING clause
    #                      test - this tests the selection of aggregate
    #                      functions (COUNT, AVG, MAX, MIN, SUM).
    #                      Aggregates are tested in the SELECT clause,
    #                      WHERE clause and in the havING clause.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    #  Notes:
    #
    # =================== End Test Case Header  ===================
    #
    #  Query 1
    #  get part numbers and total value per order for that part
    #  for parts whose average total value per order is greater
    #  than the cost of its inventory
    
    stmt = """select  """ + gvars.g_schema_arkcasedb + """.odetail.partnum, sum(quantity * price)
from """ + gvars.g_schema_arkcasedb + """.odetail,""" + gvars.g_schema_arkcasedb + """.parts 
where  """ + gvars.g_schema_arkcasedb + """.odetail.partnum =  """ + gvars.g_schema_arkcasedb + """.parts.partnum
group by  """ + gvars.g_schema_arkcasedb + """.odetail.partnum
having avg(quantity * price) >
(select avg(partcost * inventory)
from """ + gvars.g_schema_arkcasedb + """.fromsup,""" + gvars.g_schema_arkcasedb + """.parts 
where  """ + gvars.g_schema_arkcasedb + """.fromsup.partnum =  """ + gvars.g_schema_arkcasedb + """.parts.partnum
and  """ + gvars.g_schema_arkcasedb + """.fromsup.partnum =  """ + gvars.g_schema_arkcasedb + """.odetail.partnum
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s0')
    
    #  Query 2
    #  get region #, branch#, and the average payroll for the branch(s)
    #  with the highest average payroll (having clause eliminates
    #  average payroll for the current branch so >ALL can be used
    #  instead of >=ALL)
    stmt = """select regnum, branchnum, avg(X.salary)
from """ + gvars.g_schema_arkcasedb + """.employee X
group by regnum, branchnum
having avg(X.salary) >ALL
(select avg(Y.salary)
from """ + gvars.g_schema_arkcasedb + """.employee Y
group by regnum, branchnum
having avg(Y.salary) <> avg(X.salary)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s1')
    
    # Query 3
    # get region #, branch#, and the 'median' payroll for the branch(s)
    # with the highest median payroll (having clause eliminates
    # median payroll for the current branch so >ALL can be used
    # instead of >=ALL)
    stmt = """set param ?p 2;"""
    output = _dci.cmdexec(stmt)
    stmt = """select regnum,branchnum,min(salary) + ((max(salary) - min(salary)) / ?p)
from """ + gvars.g_schema_arkcasedb + """.employee X
group by regnum, branchnum
having min(salary) + ((max(salary) - min(salary)) / ?p) >ALL
(select min(Y.salary) + ((max(Y.salary) - min(Y.salary)) / ?p)
from """ + gvars.g_schema_arkcasedb + """.employee Y
group by regnum, branchnum
having min(Y.salary) + ((max(Y.salary) - min(Y.salary)) / ?p) <>
min(X.salary) + ((max(X.salary) - min(X.salary)) / ?p)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s2')
    
    #  Query 4
    #  get region # and branch # for branches where the average
    #  pay (not counting duplicates) is greater than the average
    #  pay with the largest and smallest salaries excluded.
    stmt = """select regnum, branchnum
from """ + gvars.g_schema_arkcasedb + """.employee X
group by regnum, branchnum
having avg(distinct salary) >
(select avg(Y.salary)
from """ + gvars.g_schema_arkcasedb + """.employee Y
where salary <> max(X.salary) and
salary <> min(X.salary) and
(Y.regnum = X.regnum) and
(Y.branchnum = X.branchnum)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s3')
    
    #  Query 5
    #  get region # and branch # for branches where the average
    #  pay is greater than the average pay with the largest
    #  and smallest salaries excluded.
    stmt = """select regnum, branchnum
from """ + gvars.g_schema_arkcasedb + """.employee X
group by regnum, branchnum
having avg(salary) >
(select avg(Y.salary)
from """ + gvars.g_schema_arkcasedb + """.employee Y
where salary <> max(X.salary) and
salary <> min(X.salary) and
(Y.regnum = X.regnum) and
(Y.branchnum = X.branchnum)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s4')
    
    # Query 6
    # get region # and branch # for branches whose average salary
    # is greater than their managers' salary - 10000
    stmt = """set param ?p 10000;"""
    output = _dci.cmdexec(stmt)
    stmt = """select regnum, branchnum
from """ + gvars.g_schema_arkcasedb + """.employee X
group by regnum, branchnum
having avg(salary) >
(select (salary - ?p)
from """ + gvars.g_schema_arkcasedb + """.employee Y , """ + gvars.g_schema_arkcasedb + """.branch 
where Y.regnum =  """ + gvars.g_schema_arkcasedb + """.branch.regnum
and Y.branchnum =  """ + gvars.g_schema_arkcasedb + """.branch.branchnum
and Y.empnum =  """ + gvars.g_schema_arkcasedb + """.branch.manager
and Y.regnum = X.regnum
and Y.branchnum = X.branchnum
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s5')
    
    #  Query 7
    #  get region # and branch # for branches A whose total payroll
    #  is greater than the total payroll of every other branch, not
    #  counting salaries less than the minimum salary of branch 'A'
    stmt = """select regnum, branchnum
from """ + gvars.g_schema_arkcasedb + """.employee X
group by regnum, branchnum
having sum(salary) >ALL
(select sum(Y.salary)
from """ + gvars.g_schema_arkcasedb + """.employee Y
where salary >= min(X.salary)
group by regnum, branchnum
having sum(Y.salary) <>  sum(X.salary)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s6')
    
    _testmgr.testcase_end(desc)

