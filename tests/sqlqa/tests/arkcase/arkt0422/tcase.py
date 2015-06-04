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
    
def test001(desc="""Correlated subquery with IN clause between outer query"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #  and subquery
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     A01
    #  Description:        Correlated subquery with IN clause between
    #                      outer query and subquery
    #                      Correlated subquery in where clause test
    #                      - tests the use of the IN operator connecting
    #                      the outer query with the subquery.
    #                      Vary attributes as described in testunit comments
    #                     above. Test the use of NOT IN.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    #  Notes:
    #  This test case incorporates features detailed in the "Title"
    #  by Ima Programmer (Version 1.1, <date>).
    #
    # =================== End Test Case Header  ===================
    
    # get supplier names for suppliers who supply part 4102
    
    stmt = """set param ?p 4102;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select suppname
from """ + gvars.g_schema_arkcasedb + """.supplier 
where ?p in
(select partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where  """ + gvars.g_schema_arkcasedb + """.supplier.suppnum = suppnum);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s0')
    
    # same as above , add fromsup as qualifier for suppnum
    stmt = """set param ?p 4102;"""
    output = _dci.cmdexec(stmt)
    stmt = """select suppname
from """ + gvars.g_schema_arkcasedb + """.supplier 
where ?p in
(select partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where  """ + gvars.g_schema_arkcasedb + """.supplier.suppnum =  """ + gvars.g_schema_arkcasedb + """.fromsup.suppnum);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s1')
    
    # get supplier names for suppliers who DON'T supply part 4102
    stmt = """set param ?p 4100;"""
    output = _dci.cmdexec(stmt)
    stmt = """select suppname
from """ + gvars.g_schema_arkcasedb + """.supplier 
where (?p + 2 ) NOT in
(select partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where  """ + gvars.g_schema_arkcasedb + """.supplier.suppnum = suppnum);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s2')
    
    # same as first, except use alias
    stmt = """set param ?p 4102;"""
    output = _dci.cmdexec(stmt)
    stmt = """select suppname
from """ + gvars.g_schema_arkcasedb + """.supplier X
where ?p in
(select partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where X.suppnum = suppnum);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s3')
    
    #  get part names whose price is equal to its' cost from
    #  at least one supplier
    stmt = """select partname
from """ + gvars.g_schema_arkcasedb + """.parts 
where price IN
(select partcost
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where  """ + gvars.g_schema_arkcasedb + """.parts.partnum =  """ + gvars.g_schema_arkcasedb + """.fromsup.partnum
group by partcost
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s4')
    
    # same as above, except eliminate parts costing 20100
    stmt = """set param ?p 20100;"""
    output = _dci.cmdexec(stmt)
    stmt = """select partname
from """ + gvars.g_schema_arkcasedb + """.parts 
where price IN
(select partcost
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where  """ + gvars.g_schema_arkcasedb + """.parts.partnum =  """ + gvars.g_schema_arkcasedb + """.fromsup.partnum
group by partcost
having partcost <> ?p
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s5')
    
    #  same as above, except eliminate 'group by' and use 'distinct'
    stmt = """select partname
from """ + gvars.g_schema_arkcasedb + """.parts 
where price IN
(select distinct partcost
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where  """ + gvars.g_schema_arkcasedb + """.parts.partnum =  """ + gvars.g_schema_arkcasedb + """.fromsup.partnum
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s6')
    
    #  get region names where the manager's employee # is equal
    #  to 1.
    stmt = """select regname
from """ + gvars.g_schema_arkcasedb + """.region 
where 1 in
(select *
from """ + gvars.g_schema_arkcasedb + """.empone 
where  """ + gvars.g_schema_arkcasedb + """.empone.empnum =  """ + gvars.g_schema_arkcasedb + """.region.manager);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s7')
    
    #  same as above, without qualifiers
    stmt = """select regname
from """ + gvars.g_schema_arkcasedb + """.region 
where 1 in
(select *
from """ + gvars.g_schema_arkcasedb + """.empone 
where empnum = manager);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s8')
    
    #  get part numbers for all parts supplied by more than one supplier
    stmt = """select distinct X.partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup X
where X.partnum in
(select Y.partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup Y
where Y.suppnum <> X.suppnum
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s9')
    
    #  same as above, with 'distinct Y.partnum'
    stmt = """select distinct X.partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup X
where X.partnum in
(select distinct Y.partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup Y
where Y.suppnum <> X.suppnum
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s10')
    
    #  same as first, with 'group by Y.partnum'
    stmt = """select distinct X.partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup X
where X.partnum in
(select Y.partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup Y
where Y.suppnum <> X.suppnum
group by Y.partnum
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s11')
    
    #  same as first, with 'group by X.partnum' instead of
    #  'distinct X.partnum'
    stmt = """select X.partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup X
where X.partnum in
(select Y.partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup Y
where Y.suppnum <> X.suppnum
)
group by X.partnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s12')
    
    #  same as first, but with two group by clauses
    stmt = """select X.partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup X
where X.partnum in
(select Y.partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup Y
where Y.suppnum <> X.suppnum
group by Y.partnum
)
group by X.partnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s13')
    
    #  use having clause to eliminate part # 4101 in subquery
    stmt = """select X.partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup X
where X.partnum in
(select Y.partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup Y
where Y.suppnum <> X.suppnum
group by Y.partnum
having Y.partnum <> 4101
)
group by X.partnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s14')
    
    # use having clause to eliminate part #4101 in outer query
    stmt = """set param ?p 4098;"""
    output = _dci.cmdexec(stmt)
    stmt = """select X.partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup X
where X.partnum in
(select Y.partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup Y
where Y.suppnum <> X.suppnum
group by Y.partnum
)
group by X.partnum
having X.partnum <> (?p + 3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s15')
    
    #  use having clause in both outer and subquery
    stmt = """select X.partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup X
where X.partnum in
(select Y.partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup Y
where Y.suppnum <> X.suppnum
group by Y.partnum
having Y.partnum <> (?p + 3)
)
group by X.partnum
having X.partnum <> (?p + 3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s16')
    
    # get salesman #'s and order #'s for salesman who have orders
    # for parts stored at location H76
    stmt = """set param ?p 'H76';"""
    output = _dci.cmdexec(stmt)
    stmt = """select salesman,ordernum
from """ + gvars.g_schema_arkcasedb + """.orders 
where ?p in
(select """ + gvars.g_schema_arkcasedb + """.parts.location
from """ + gvars.g_schema_arkcasedb + """.odetail, """ + gvars.g_schema_arkcasedb + """.parts 
where ( """ + gvars.g_schema_arkcasedb + """.odetail.partnum =  """ + gvars.g_schema_arkcasedb + """.parts.partnum)
and ( """ + gvars.g_schema_arkcasedb + """.orders.ordernum =  """ + gvars.g_schema_arkcasedb + """.odetail.ordernum) );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s17')
    
    #  same as above, use 'distinct parts.location'
    stmt = """select salesman,ordernum
from """ + gvars.g_schema_arkcasedb + """.orders 
where ?p in
(select distinct  """ + gvars.g_schema_arkcasedb + """.parts.location
from """ + gvars.g_schema_arkcasedb + """.odetail, """ + gvars.g_schema_arkcasedb + """.parts 
where ( """ + gvars.g_schema_arkcasedb + """.odetail.partnum =  """ + gvars.g_schema_arkcasedb + """.parts.partnum)
and ( """ + gvars.g_schema_arkcasedb + """.orders.ordernum =  """ + gvars.g_schema_arkcasedb + """.odetail.ordernum) );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s18')
    
    #  same as first, use 'group by parts.location' to eliminate
    #  duplicates
    stmt = """select salesman,ordernum
from """ + gvars.g_schema_arkcasedb + """.orders 
where ?p in
(select  """ + gvars.g_schema_arkcasedb + """.parts.location
from """ + gvars.g_schema_arkcasedb + """.odetail, """ + gvars.g_schema_arkcasedb + """.parts 
where ( """ + gvars.g_schema_arkcasedb + """.odetail.partnum =  """ + gvars.g_schema_arkcasedb + """.parts.partnum)
and ( """ + gvars.g_schema_arkcasedb + """.orders.ordernum =  """ + gvars.g_schema_arkcasedb + """.odetail.ordernum)
group by  """ + gvars.g_schema_arkcasedb + """.parts.location );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s19')
    
    #  same as first, except order by ordernum
    stmt = """select salesman,ordernum
from """ + gvars.g_schema_arkcasedb + """.orders 
where ?p in
(select  """ + gvars.g_schema_arkcasedb + """.parts.location
from """ + gvars.g_schema_arkcasedb + """.odetail, """ + gvars.g_schema_arkcasedb + """.parts 
where ( """ + gvars.g_schema_arkcasedb + """.odetail.partnum =  """ + gvars.g_schema_arkcasedb + """.parts.partnum)
and ( """ + gvars.g_schema_arkcasedb + """.orders.ordernum =  """ + gvars.g_schema_arkcasedb + """.odetail.ordernum) )
order by ordernum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s20')
    
    #  get part names whose cost is greater than 10000 and whose
    #  price is equal to its' cost from at least one supplier
    #  NOTE: the subquery here returns 0 records sometimes.
    stmt = """select partname
from """ + gvars.g_schema_arkcasedb + """.parts 
where price IN
(select partcost
from """ + gvars.g_schema_arkcasedb + """.expfroms 
where  """ + gvars.g_schema_arkcasedb + """.parts.partnum =  """ + gvars.g_schema_arkcasedb + """.expfroms.partnum
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s21')
    
    #  get salesman numbers for salesman who have already sold
    #  a previous order (a lower order number is a previous
    #  order)
    stmt = """select salesman
from """ + gvars.g_schema_arkcasedb + """.orders X
where salesman in
(select salesman
from """ + gvars.g_schema_arkcasedb + """.orders Y
where Y.ordernum < X.ordernum
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s22')
    
    # get employee names who do not work at first branches
    # (eliminate duplicates)
    stmt = """set param ?p 1;"""
    output = _dci.cmdexec(stmt)
    stmt = """select empname
from """ + gvars.g_schema_arkcasedb + """.employee 
where ?p not in
(select branchnum
from """ + gvars.g_schema_arkcasedb + """.branch 
where  """ + gvars.g_schema_arkcasedb + """.employee.branchnum =  """ + gvars.g_schema_arkcasedb + """.branch.branchnum
group by branchnum
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s23')
    
    #  same as above, use DISTINCT instead of GROUP BY
    stmt = """select empname
from """ + gvars.g_schema_arkcasedb + """.employee 
where ?p not in
(select distinct branchnum
from """ + gvars.g_schema_arkcasedb + """.branch 
where  """ + gvars.g_schema_arkcasedb + """.employee.branchnum =  """ + gvars.g_schema_arkcasedb + """.branch.branchnum );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s24')
    
    #  same as query before last, but use HAVING with GROUP BY
    #  instead of WHERE
    stmt = """select empname
from """ + gvars.g_schema_arkcasedb + """.employee 
where ?p not in
(select branchnum
from """ + gvars.g_schema_arkcasedb + """.branch 
group by branchnum
having branchnum =  """ + gvars.g_schema_arkcasedb + """.employee.branchnum
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s25')
    
    # get supplier numbers, for suppliers who supply at least
    # one part supplied by supplier 15
    stmt = """set param ?p 3;"""
    output = _dci.cmdexec(stmt)
    stmt = """select distinct suppnum
from """ + gvars.g_schema_arkcasedb + """.fromsup X
where (?p * 5) in
(select suppnum
from """ + gvars.g_schema_arkcasedb + """.fromsup Y
where Y.partnum = X.partnum
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s26')
    
    # get supplier numbers for suppliers who are in the same
    # state as supplier 1.
    stmt = """set param ?p 2;"""
    output = _dci.cmdexec(stmt)
    stmt = """select suppnum
from """ + gvars.g_schema_arkcasedb + """.supplier X
where (?p - 1) in
(select suppnum
from """ + gvars.g_schema_arkcasedb + """.supplier Y
where Y.state = X.state
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s27')
    
    # get customer names for customers who have not ordered parts
    # stored at location 'V67'
    stmt = """set param ?p 'V67';"""
    output = _dci.cmdexec(stmt)
    stmt = """select custname
from """ + gvars.g_schema_arkcasedb + """.customer 
where ?p not in
(select col_2
from """ + gvars.g_schema_arkcasedb + """.partsfor 
where custnum = col_12
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s28')
    
    _testmgr.testcase_end(desc)

def test002(desc="""Correlated subquery with simple and quantified comparison"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #  operators between outer query and subquery.
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     A02
    #  Description:        Correlated subquery with simple and quantified
    #                      comparison operators between outer query and subquery.
    #                      Correlated subquery in where clause test
    #                      - this tests the use of simple comparison operators
    #                      (<,<=,=,<>,>,>=) and quantified comparison operators
    #                      (=ANY,>ALL,etc.) as the relational operator
    #                      between the outer and subqueries. Note that some of
    #                      the subqueries in this testcase return 0
    #                      records (empty sets ) sometimes
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    #  Notes:
    #  This test case incorporates features detailed in the "Title"
    #  by Ima Programmer (Version 1.1, <date>).
    #
    # =================== End Test Case Header  ===================
    
    # get employee name who is manager of region 1
    
    stmt = """set param ?p 1;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select empname
from """ + gvars.g_schema_arkcasedb + """.employee 
where ?p =
(select regnum
from """ + gvars.g_schema_arkcasedb + """.region 
where manager = empnum);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s0')
    
    #  same as above, add qualifications
    stmt = """select empname
from """ + gvars.g_schema_arkcasedb + """.employee 
where ?p =
(select regnum
from """ + gvars.g_schema_arkcasedb + """.region 
where  """ + gvars.g_schema_arkcasedb + """.region.manager =   """ + gvars.g_schema_arkcasedb + """.employee.empnum);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s1')
    
    # get customer names whose salesman is not salesman #212
    stmt = """set param ?p 212;"""
    output = _dci.cmdexec(stmt)
    stmt = """select custname
from """ + gvars.g_schema_arkcasedb + """.customer 
where ?p not in
(select col_11
from """ + gvars.g_schema_arkcasedb + """.partsfor 
where  """ + gvars.g_schema_arkcasedb + """.customer.custnum =  """ + gvars.g_schema_arkcasedb + """.partsfor.col_12
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s2')
    
    #  same as above, use join instead of view partsfor
    stmt = """select custname
from """ + gvars.g_schema_arkcasedb + """.customer 
where ?p not in
(select salesman
from """ + gvars.g_schema_arkcasedb + """.orders, """ + gvars.g_schema_arkcasedb + """.odetail, """ + gvars.g_schema_arkcasedb + """.parts 
where ( """ + gvars.g_schema_arkcasedb + """.orders.ordernum =  """ + gvars.g_schema_arkcasedb + """.odetail.ordernum) and
( """ + gvars.g_schema_arkcasedb + """.odetail.partnum =  """ + gvars.g_schema_arkcasedb + """.parts.partnum) and
( """ + gvars.g_schema_arkcasedb + """.customer.custnum = """ + gvars.g_schema_arkcasedb + """.orders.custnum) );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s3')
    
    # get part names for parts whose price is less than 2000
    # more than its' cost from ll suppliers
    stmt = """set param ?p 2000;"""
    output = _dci.cmdexec(stmt)
    stmt = """select partname
from """ + gvars.g_schema_arkcasedb + """.parts 
where (price - ?p) <all
(select partcost
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where  """ + gvars.g_schema_arkcasedb + """.parts.partnum =  """ + gvars.g_schema_arkcasedb + """.fromsup.partnum
group by partcost
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s4')
    
    #  get part names for parts who have the same price as at
    #  least one other part
    stmt = """select col_1
from """ + gvars.g_schema_arkcasedb + """.partsfor X
where X.col_3 = SOME
(select Y.col_3
from """ + gvars.g_schema_arkcasedb + """.partsfor Y
where X.col_1 <> Y.col_1
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s5')
    
    #   get supplier numbers and part number for suppliers whose
    #  cost for that part is less than or equal to some other
    #  suppliers cost for that part
    #   note: subquery returns 0 records sometimes
    stmt = """select suppnum,partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup X
where partcost <=SOME
(select partcost
from """ + gvars.g_schema_arkcasedb + """.fromsup Y
where X.suppnum <> Y.suppnum
and X.partnum = Y.partnum
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s6')
    
    #  same as above, use <=ANY instead of SOME
    stmt = """select suppnum,partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup X
where partcost <=ANY
(select partcost
from """ + gvars.g_schema_arkcasedb + """.fromsup Y
where X.suppnum <> Y.suppnum
and X.partnum = Y.partnum
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s7')
    
    #  same as above, use <ALL instead
    stmt = """select suppnum,partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup X
where partcost < ALL
(select partcost
from """ + gvars.g_schema_arkcasedb + """.fromsup Y
where X.suppnum <> Y.suppnum
and X.partnum = Y.partnum
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s8')
    
    # get supplier numbers for other suppliers who supply
    # at least one part supplied by supplier 15.
    # note: subquery returns 0 records (an empty set) sometimes
    stmt = """set param ?p 15;"""
    output = _dci.cmdexec(stmt)
    stmt = """select distinct suppnum
from """ + gvars.g_schema_arkcasedb + """.fromsup X
where X.partnum =SOME
(select Y.partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup Y
where (X.suppnum <> Y.suppnum)
and (Y.suppnum = ?p)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s9')
    
    # get supplier numbers who are in the same state as supplier 1
    stmt = """set param ?p 2;"""
    output = _dci.cmdexec(stmt)
    stmt = """select suppnum
from """ + gvars.g_schema_arkcasedb + """.supplier X
where (?p -1) =ANY
(select suppnum
from """ + gvars.g_schema_arkcasedb + """.supplier Y
where X.state = Y.state
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s10')
    
    # get supplier names for suppliers who supply part 4102
    stmt = """set param ?p 4102;"""
    output = _dci.cmdexec(stmt)
    stmt = """select suppname
from """ + gvars.g_schema_arkcasedb + """.supplier 
where ?p =SOME
(select partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where  """ + gvars.g_schema_arkcasedb + """.supplier.suppnum = suppnum);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s11')
    
    #  same as above , add fromsup as qualifier for suppnum
    stmt = """select suppname
from """ + gvars.g_schema_arkcasedb + """.supplier 
where ?p =ANY
(select partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where  """ + gvars.g_schema_arkcasedb + """.supplier.suppnum =  """ + gvars.g_schema_arkcasedb + """.fromsup.suppnum);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s12')
    
    #  get supplier names for suppliers who DON'T supply part 4102
    stmt = """select suppname
from """ + gvars.g_schema_arkcasedb + """.supplier 
where ?p =SOME
(select partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where  """ + gvars.g_schema_arkcasedb + """.supplier.suppnum = suppnum);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s13')
    
    #  same as first, except use alias
    stmt = """select suppname
from """ + gvars.g_schema_arkcasedb + """.supplier X
where ?p =ANY
(select partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where X.suppnum = suppnum);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s14')
    
    #  get part names whose price is equal to its' cost from
    #  at least one supplier
    stmt = """select partname
from """ + gvars.g_schema_arkcasedb + """.parts 
where price =SOME
(select partcost
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where  """ + gvars.g_schema_arkcasedb + """.parts.partnum =  """ + gvars.g_schema_arkcasedb + """.fromsup.partnum
group by partcost
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s15')
    
    # same as above, except eliminate parts costing 20100
    stmt = """set param ?p 20100;"""
    output = _dci.cmdexec(stmt)
    stmt = """select partname
from """ + gvars.g_schema_arkcasedb + """.parts 
where price =ANY
(select partcost
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where  """ + gvars.g_schema_arkcasedb + """.parts.partnum =  """ + gvars.g_schema_arkcasedb + """.fromsup.partnum
group by partcost
having partcost <> ?p
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s16')
    
    #  same as above, except eliminate 'group by' and use 'distinct'
    stmt = """select partname
from """ + gvars.g_schema_arkcasedb + """.parts 
where price =SOME
(select distinct partcost
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where  """ + gvars.g_schema_arkcasedb + """.parts.partnum =  """ + gvars.g_schema_arkcasedb + """.fromsup.partnum
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s17')
    
    # get region names where the manager's employee # is equal
    # to 1.
    stmt = """set param ?p 1;"""
    output = _dci.cmdexec(stmt)
    stmt = """select regname
from """ + gvars.g_schema_arkcasedb + """.region 
where ?p =ANY
(select *
from """ + gvars.g_schema_arkcasedb + """.empone 
where  """ + gvars.g_schema_arkcasedb + """.empone.empnum =  """ + gvars.g_schema_arkcasedb + """.region.manager);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s18')
    
    #  same as above, without qualifiers
    stmt = """select regname
from """ + gvars.g_schema_arkcasedb + """.region 
where ?p =SOME
(select *
from """ + gvars.g_schema_arkcasedb + """.empone 
where empnum = manager);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s19')
    
    #  get part numbers for all parts supplied by more than one supplier
    stmt = """select distinct X.partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup X
where X.partnum =ANY
(select Y.partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup Y
where Y.suppnum <> X.suppnum
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s20')
    
    #  same as above, with 'distinct Y.partnum'
    stmt = """select distinct X.partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup X
where X.partnum =SOME
(select distinct Y.partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup Y
where Y.suppnum <> X.suppnum
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s21')
    
    #  same as first, with 'group by Y.partnum'
    stmt = """select distinct X.partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup X
where X.partnum =ANY
(select Y.partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup Y
where Y.suppnum <> X.suppnum
group by Y.partnum
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s22')
    
    #  same as first, with 'group by X.partnum' instead of
    #  'distinct X.partnum'
    stmt = """select X.partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup X
where X.partnum =SOME
(select Y.partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup Y
where Y.suppnum <> X.suppnum
)
group by X.partnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s23')
    
    #  same as first, but with two group by clauses
    stmt = """select X.partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup X
where X.partnum =ANY
(select Y.partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup Y
where Y.suppnum <> X.suppnum
group by Y.partnum
)
group by X.partnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s24')
    
    #  use having clause to eliminate part # 4101 in subquery
    stmt = """select X.partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup X
where X.partnum =SOME
(select Y.partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup Y
where Y.suppnum <> X.suppnum
group by Y.partnum
having Y.partnum <> 4101
)
group by X.partnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s25')
    
    # use having clause to eliminate part #4101 in outer query
    stmt = """set param ?p 4101;"""
    output = _dci.cmdexec(stmt)
    stmt = """select X.partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup X
where X.partnum =ANY
(select Y.partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup Y
where Y.suppnum <> X.suppnum
group by Y.partnum
)
group by X.partnum
having X.partnum <> ?p;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s26')
    
    #  use having clause in both outer and subquery
    stmt = """select X.partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup X
where X.partnum =SOME
(select Y.partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup Y
where Y.suppnum <> X.suppnum
group by Y.partnum
having Y.partnum <> ?p
)
group by X.partnum
having X.partnum <> ?p;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s27')
    
    # get salesman #'s and order #'s for salesman who have orders
    # for parts stored at location H76
    stmt = """set param ?p 'H76';"""
    output = _dci.cmdexec(stmt)
    stmt = """select salesman,ordernum
from """ + gvars.g_schema_arkcasedb + """.orders 
where ?p =ANY
(select """ + gvars.g_schema_arkcasedb + """.parts.location
from """ + gvars.g_schema_arkcasedb + """.odetail, """ + gvars.g_schema_arkcasedb + """.parts 
where ( """ + gvars.g_schema_arkcasedb + """.odetail.partnum =  """ + gvars.g_schema_arkcasedb + """.parts.partnum)
and ( """ + gvars.g_schema_arkcasedb + """.orders.ordernum =  """ + gvars.g_schema_arkcasedb + """.odetail.ordernum) );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s28')
    
    #  same as above, use 'distinct parts.location'
    stmt = """select salesman,ordernum
from """ + gvars.g_schema_arkcasedb + """.orders 
where ?p =SOME
(select distinct  """ + gvars.g_schema_arkcasedb + """.parts.location
from """ + gvars.g_schema_arkcasedb + """.odetail, """ + gvars.g_schema_arkcasedb + """.parts 
where ( """ + gvars.g_schema_arkcasedb + """.odetail.partnum =  """ + gvars.g_schema_arkcasedb + """.parts.partnum)
and ( """ + gvars.g_schema_arkcasedb + """.orders.ordernum =  """ + gvars.g_schema_arkcasedb + """.odetail.ordernum) );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s29')
    
    #  same as first, use 'group by parts.location' to eliminate
    #  duplicates
    stmt = """select salesman,ordernum
from """ + gvars.g_schema_arkcasedb + """.orders 
where ?p =ANY
(select  """ + gvars.g_schema_arkcasedb + """.parts.location
from """ + gvars.g_schema_arkcasedb + """.odetail, """ + gvars.g_schema_arkcasedb + """.parts 
where ( """ + gvars.g_schema_arkcasedb + """.odetail.partnum =  """ + gvars.g_schema_arkcasedb + """.parts.partnum)
and ( """ + gvars.g_schema_arkcasedb + """.orders.ordernum =  """ + gvars.g_schema_arkcasedb + """.odetail.ordernum)
group by  """ + gvars.g_schema_arkcasedb + """.parts.location );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s30')
    
    #  same as first, except order by  ordernum
    stmt = """select salesman,ordernum
from """ + gvars.g_schema_arkcasedb + """.orders 
where ?p =SOME
(select """ + gvars.g_schema_arkcasedb + """.parts.location
from """ + gvars.g_schema_arkcasedb + """.odetail, """ + gvars.g_schema_arkcasedb + """.parts 
where ( """ + gvars.g_schema_arkcasedb + """.odetail.partnum =  """ + gvars.g_schema_arkcasedb + """.parts.partnum)
and ( """ + gvars.g_schema_arkcasedb + """.orders.ordernum =  """ + gvars.g_schema_arkcasedb + """.odetail.ordernum) )
order by  ordernum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s31')
    
    #  get part names whose cost is greater than 10000 and whose
    #  price is equal to its' cost from t least one supplier
    #  NOTE: the subquery here returns 0 records sometimes.
    stmt = """select partname
from """ + gvars.g_schema_arkcasedb + """.parts 
where price =ANY
(select partcost
from """ + gvars.g_schema_arkcasedb + """.expfroms 
where  """ + gvars.g_schema_arkcasedb + """.parts.partnum =  """ + gvars.g_schema_arkcasedb + """.expfroms.partnum
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s32')
    
    #  get salesman numbers for salesman who have already sold
    #  a previous order (a lower order number is a previous
    #  order)
    stmt = """select salesman
from """ + gvars.g_schema_arkcasedb + """.orders X
where salesman =SOME
(select salesman
from """ + gvars.g_schema_arkcasedb + """.orders Y
where Y.ordernum < X.ordernum
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s33')
    
    # get employee names who do not work at first branches
    # (eliminate duplicates)
    stmt = """set param ?p 1;"""
    output = _dci.cmdexec(stmt)
    stmt = """select empname
from """ + gvars.g_schema_arkcasedb + """.employee 
where ?p =ANY
(select branchnum
from """ + gvars.g_schema_arkcasedb + """.branch 
where  """ + gvars.g_schema_arkcasedb + """.employee.branchnum =  """ + gvars.g_schema_arkcasedb + """.branch.branchnum
group by branchnum
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s34')
    
    #  same as above, use DISTINCT instead of GROUP BY
    stmt = """select empname
from """ + gvars.g_schema_arkcasedb + """.employee 
where ?p =SOME
(select distinct branchnum
from """ + gvars.g_schema_arkcasedb + """.branch 
where  """ + gvars.g_schema_arkcasedb + """.employee.branchnum =  """ + gvars.g_schema_arkcasedb + """.branch.branchnum );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s35')
    
    #  same as query before last, but use HAVING with GROUP BY
    #  instead of WHERE
    stmt = """select empname
from """ + gvars.g_schema_arkcasedb + """.employee 
where ?p <> ANY
(select branchnum
from """ + gvars.g_schema_arkcasedb + """.branch 
group by branchnum
having branchnum =  """ + gvars.g_schema_arkcasedb + """.employee.branchnum
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s36')
    
    # get region names where the managers' employee number is
    # less than 100
    stmt = """set param ?p 50;"""
    output = _dci.cmdexec(stmt)
    stmt = """select regname
from """ + gvars.g_schema_arkcasedb + """.region 
where (?p * 2) >
(select empnum
from """ + gvars.g_schema_arkcasedb + """.empone 
where  """ + gvars.g_schema_arkcasedb + """.empone.empnum =  """ + gvars.g_schema_arkcasedb + """.region.manager
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s37')
    
    # get customer names for customers who have not ordered parts
    # stored at location 'V67'
    stmt = """set param ?p 'V67';"""
    output = _dci.cmdexec(stmt)
    stmt = """select custname
from """ + gvars.g_schema_arkcasedb + """.customer 
where ?p <>SOME
(select col_2
from """ + gvars.g_schema_arkcasedb + """.partsfor 
where custnum = col_12
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s38')
    
    _testmgr.testcase_end(desc)

def test003(desc="""Correlated subquery with FOR ALL/implication from of"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # form of EXISTS/NOT EXISTS
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     A03
    #  Description:        Correlated subquery with FOR ALL/implication
    #                      form of EXISTS/NOT EXISTS
    #                      Correlated subquery in where clause test
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
    #
    
    # get supplier names for suppliers who supply part 4102
    
    stmt = """set param ?p 4102;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select suppname
from """ + gvars.g_schema_arkcasedb + """.supplier 
where exists
(select *
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where  """ + gvars.g_schema_arkcasedb + """.supplier.suppnum = suppnum
and partnum = ?p
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s0')
    
    #  same as above, change 'select *' to 'select partnum'
    stmt = """select suppname
from """ + gvars.g_schema_arkcasedb + """.supplier 
where exists
(select partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where  """ + gvars.g_schema_arkcasedb + """.supplier.suppnum = suppnum
and partnum = ?p
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s1')
    
    #  get supplier names for suppliers who DON'T supply part 4102
    stmt = """select suppname
from """ + gvars.g_schema_arkcasedb + """.supplier 
where not exists
(select *
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where  """ + gvars.g_schema_arkcasedb + """.supplier.suppnum = suppnum
and partnum = ?p
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s2')
    
    # get region names where the manager's employee # is equal
    # to 1.
    stmt = """set param ?p 1;"""
    output = _dci.cmdexec(stmt)
    stmt = """select regname
from """ + gvars.g_schema_arkcasedb + """.region 
where exists
(select *
from """ + gvars.g_schema_arkcasedb + """.empone 
where  """ + gvars.g_schema_arkcasedb + """.empone.empnum =  """ + gvars.g_schema_arkcasedb + """.region.manager
and empnum = ?p
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s3')
    
    #  get part numbers for all parts supplied by more than
    #  one supplier
    stmt = """select distinct X.partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup X
where exists
(select Y.partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup Y
where Y.suppnum <> X.suppnum
and X.partnum = Y.partnum
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s4')
    
    # get salesman #'s and order #'s for salesman who have orders
    # for parts stored at location H76
    stmt = """set param ?p 'H76';"""
    output = _dci.cmdexec(stmt)
    stmt = """select salesman,ordernum
from """ + gvars.g_schema_arkcasedb + """.orders 
where exists
(select *
from """ + gvars.g_schema_arkcasedb + """.odetail, """ + gvars.g_schema_arkcasedb + """.parts 
where ( """ + gvars.g_schema_arkcasedb + """.odetail.partnum =  """ + gvars.g_schema_arkcasedb + """.parts.partnum)
and ( """ + gvars.g_schema_arkcasedb + """.orders.ordernum =  """ + gvars.g_schema_arkcasedb + """.odetail.ordernum) and
( """ + gvars.g_schema_arkcasedb + """.parts.location = ?p) );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s5')
    
    #  get part names whose cost is greater than 10000 and whose
    #  price is equal to its' cost from at least one supplier
    stmt = """select partname
from """ + gvars.g_schema_arkcasedb + """.parts 
where exists
(select *
from """ + gvars.g_schema_arkcasedb + """.expfroms 
where ( """ + gvars.g_schema_arkcasedb + """.parts.partnum =  """ + gvars.g_schema_arkcasedb + """.expfroms.partnum)
and (price = partcost)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s6')
    
    #  get salesman numbers for salesman who have already sold
    #  a previous order (a lower order number is a previous order)
    stmt = """select salesman
from """ + gvars.g_schema_arkcasedb + """.orders X
where exists
(select salesman
from """ + gvars.g_schema_arkcasedb + """.orders Y
where (Y.ordernum < X.ordernum)
and (X.salesman = Y.salesman)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s7')
    
    # get employee names who do not work at first branches
    # (eliminate duplicates)
    stmt = """set param ?p 1;"""
    output = _dci.cmdexec(stmt)
    stmt = """select empname
from """ + gvars.g_schema_arkcasedb + """.employee 
where not exists
(select branchnum
from """ + gvars.g_schema_arkcasedb + """.branch 
where ( """ + gvars.g_schema_arkcasedb + """.employee.branchnum =  """ + gvars.g_schema_arkcasedb + """.branch.branchnum)
and (branchnum = ?p)
group by branchnum
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s8')
    
    # get employee names who do not work at first branches
    # eliminate duplicates and use having clause
    stmt = """set param ?p 1;"""
    output = _dci.cmdexec(stmt)
    stmt = """select empname
from """ + gvars.g_schema_arkcasedb + """.employee 
where not exists
(select branchnum
from """ + gvars.g_schema_arkcasedb + """.branch 
where ( """ + gvars.g_schema_arkcasedb + """.employee.branchnum =  """ + gvars.g_schema_arkcasedb + """.branch.branchnum)
group by branchnum
having branchnum = ?p
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s9')
    
    # get supplier numbers for suppliers who supply at least
    # one part supplied by supplier 15
    stmt = """set param ?p 15;"""
    output = _dci.cmdexec(stmt)
    stmt = """select distinct suppnum
from """ + gvars.g_schema_arkcasedb + """.fromsup X
where exists
(select *
from """ + gvars.g_schema_arkcasedb + """.fromsup Y
where (Y.partnum = X.partnum)
and (suppnum = ?p)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s10')
    
    # get supplier numbers for suppliers who are in the same state
    # as supplier 1
    stmt = """set param ?p 1;"""
    output = _dci.cmdexec(stmt)
    stmt = """select suppnum
from """ + gvars.g_schema_arkcasedb + """.supplier X
where exists
(select suppnum
from """ + gvars.g_schema_arkcasedb + """.supplier Y
where (Y.state = X.state)
and (suppnum = ?p)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s11')
    
    # get customer names for customers who have not ordered parts
    # stored at location V67
    stmt = """set param ?p 'V67';"""
    output = _dci.cmdexec(stmt)
    stmt = """select custname
from """ + gvars.g_schema_arkcasedb + """.customer 
where not exists
(select *
from """ + gvars.g_schema_arkcasedb + """.partsfor 
where (custnum = col_12)
and (col_2 = ?p)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s12')
    
    _testmgr.testcase_end(desc)

def test004(desc="""Correlated subquery with FOR ALL/implication from of"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #  EXISTS/NOT EXISTS
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     A04
    #  Description:        Correlated subquery with FOR ALL/implication
    #                      form of EXISTS/NOT EXISTS
    #                      Correlated subquery in where clause test
    #                      - this tests the use of EXIST/NOT EXISTS
    #                      to simulate the use of FOR ALL.
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
    # get suppliers names for suppliers who supply all parts
    # with part numbers between 4000 and 5200.
    
    stmt = """set param ?p 4000;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p1 5200;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select suppname
from """ + gvars.g_schema_arkcasedb + """.supplier 
where not exists
(select *
from """ + gvars.g_schema_arkcasedb + """.parts 
where (partnum between ?p and ?p1)
and not exists
(select *
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where ( """ + gvars.g_schema_arkcasedb + """.parts.partnum =  """ + gvars.g_schema_arkcasedb + """.fromsup.partnum)
and ( """ + gvars.g_schema_arkcasedb + """.supplier.suppnum =  """ + gvars.g_schema_arkcasedb + """.fromsup.suppnum)
)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s0')
    
    #  Query 2
    #  same as above, except use 'distinct *'
    stmt = """select suppname
from """ + gvars.g_schema_arkcasedb + """.supplier 
where not exists
(select distinct *
from """ + gvars.g_schema_arkcasedb + """.parts 
where (partnum between ?p and ?p1)
and not exists
(select distinct  *
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where ( """ + gvars.g_schema_arkcasedb + """.parts.partnum =  """ + gvars.g_schema_arkcasedb + """.fromsup.partnum)
and ( """ + gvars.g_schema_arkcasedb + """.supplier.suppnum =  """ + gvars.g_schema_arkcasedb + """.fromsup.suppnum)
)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s1')
    
    #  Query 3
    #  same as above, except use 'distinct partnum'
    stmt = """select suppname
from """ + gvars.g_schema_arkcasedb + """.supplier 
where not exists
(select distinct partnum
from """ + gvars.g_schema_arkcasedb + """.parts 
where (partnum between ?p and ?p1)
and not exists
(select distinct partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where ( """ + gvars.g_schema_arkcasedb + """.parts.partnum =  """ + gvars.g_schema_arkcasedb + """.fromsup.partnum)
and ( """ + gvars.g_schema_arkcasedb + """.supplier.suppnum =  """ + gvars.g_schema_arkcasedb + """.fromsup.suppnum)
)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s2')
    
    # Query 4
    # get supplier numbers for suppliers who supply at least
    # all those parts supplied by supplier 6.
    stmt = """set param ?p 6;"""
    output = _dci.cmdexec(stmt)
    stmt = """select distinct suppnum
from """ + gvars.g_schema_arkcasedb + """.fromsup X
where not exists
(select partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup Y
where suppnum = ?p
and not exists
(select *
from """ + gvars.g_schema_arkcasedb + """.fromsup Z
where X.suppnum = Z.suppnum
and Z.partnum = Y.partnum
)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s3')
    
    #  Query 5
    #  same as above, except use 'group by suppnum' instead of
    #  select distinct suppnum to eliminate duplicates
    stmt = """select suppnum
from """ + gvars.g_schema_arkcasedb + """.fromsup X
where not exists
(select *
from """ + gvars.g_schema_arkcasedb + """.fromsup Y
where suppnum = ?p
and not exists
(select *
from """ + gvars.g_schema_arkcasedb + """.fromsup Z
where X.suppnum = Z.suppnum
and Z.partnum = Y.partnum
)
)
group by suppnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s4')
    
    # Query 6
    # get customer numbers for customers who have not
    # (ordered any parts which are in locations beginning
    #  with 'k' and are supplied by suppliers located in
    # 'California')
    stmt = """set param ?p 'k%';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p1 'California';"""
    output = _dci.cmdexec(stmt)
    stmt = """select custnum
from """ + gvars.g_schema_arkcasedb + """.orders 
where not exists
(select *
from """ + gvars.g_schema_arkcasedb + """.odetail 
where  """ + gvars.g_schema_arkcasedb + """.orders.ordernum =  """ + gvars.g_schema_arkcasedb + """.odetail.ordernum
and partnum in
(select partnum
from """ + gvars.g_schema_arkcasedb + """.parts 
where location like ?p
)
and partnum in
(select partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup, """ + gvars.g_schema_arkcasedb + """.supplier 
where  """ + gvars.g_schema_arkcasedb + """.fromsup.suppnum =  """ + gvars.g_schema_arkcasedb + """.supplier.suppnum
and  """ + gvars.g_schema_arkcasedb + """.supplier.state = ?p1
)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s5')
    
    #  Query 7
    #  same as above, translate 'IN' to 'EXISTS'
    stmt = """select custnum
from """ + gvars.g_schema_arkcasedb + """.orders 
where not exists
(select *
from """ + gvars.g_schema_arkcasedb + """.odetail 
where  """ + gvars.g_schema_arkcasedb + """.orders.ordernum =  """ + gvars.g_schema_arkcasedb + """.odetail.ordernum
and exists
(select partnum
from """ + gvars.g_schema_arkcasedb + """.parts 
where location like ?p
and  """ + gvars.g_schema_arkcasedb + """.odetail.partnum =  """ + gvars.g_schema_arkcasedb + """.parts.partnum
)
and exists
(select partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup, """ + gvars.g_schema_arkcasedb + """.supplier 
where """ + gvars.g_schema_arkcasedb + """.fromsup.suppnum =  """ + gvars.g_schema_arkcasedb + """.supplier.suppnum
and  """ + gvars.g_schema_arkcasedb + """.supplier.state = ?p1
and  """ + gvars.g_schema_arkcasedb + """.odetail.partnum =  """ + gvars.g_schema_arkcasedb + """.fromsup.partnum
)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s6')
    
    #  Query 8
    #  get part numbers for parts supplied to all customers
    #  in California
    stmt = """select distinct partnum
from """ + gvars.g_schema_arkcasedb + """.odetail X
where not exists
(select *
from """ + gvars.g_schema_arkcasedb + """.orders, """ + gvars.g_schema_arkcasedb + """.customer 
where  """ + gvars.g_schema_arkcasedb + """.orders.custnum =  """ + gvars.g_schema_arkcasedb + """.customer.custnum
and  """ + gvars.g_schema_arkcasedb + """.customer.state = ?p1
and not exists
(select *
from """ + gvars.g_schema_arkcasedb + """.odetail Y
where Y.partnum = X.partnum
and  """ + gvars.g_schema_arkcasedb + """.orders.ordernum = Y.ordernum
)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s7')
    
    #  Query 9
    #  same as above, except use nested subquery instead of join
    stmt = """select distinct partnum
from """ + gvars.g_schema_arkcasedb + """.odetail X
where not exists
(select *
from """ + gvars.g_schema_arkcasedb + """.orders 
where  """ + gvars.g_schema_arkcasedb + """.orders.custnum in
(select custnum
from """ + gvars.g_schema_arkcasedb + """.customer 
where state = ?p1
)
and not exists
(select *
from """ + gvars.g_schema_arkcasedb + """.odetail Y
where Y.partnum = X.partnum
and  """ + gvars.g_schema_arkcasedb + """.orders.ordernum = Y.ordernum
)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s8')
    
    #  Query 10
    #  get customer numbers for customers that have ordered
    #  all parts supplied by supplier 6.
    stmt = """select custnum
from """ + gvars.g_schema_arkcasedb + """.orders 
where not exists
(select partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where suppnum = 6
and not exists
(select *
from """ + gvars.g_schema_arkcasedb + """.odetail 
where """ + gvars.g_schema_arkcasedb + """.odetail.partnum = """ + gvars.g_schema_arkcasedb + """.fromsup.partnum
and  """ + gvars.g_schema_arkcasedb + """.orders.ordernum =  """ + gvars.g_schema_arkcasedb + """.odetail.ordernum )
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s9')
    
    #  Query 11
    #  same as above,only more complex
    stmt = """select custnum
from """ + gvars.g_schema_arkcasedb + """.orders 
where not exists
(select partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup X
where exists
(select *
from """ + gvars.g_schema_arkcasedb + """.fromsup Y
where Y.suppnum = 6
and Y.partnum = X.partnum
)
and not exists
(select *
from """ + gvars.g_schema_arkcasedb + """.odetail 
where  """ + gvars.g_schema_arkcasedb + """.odetail.partnum =  x.partnum
and  """ + gvars.g_schema_arkcasedb + """.orders.ordernum =  """ + gvars.g_schema_arkcasedb + """.odetail.ordernum )
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s10')
    
    #  Query 12
    #  same as above, but use EXISTS identity to move 'and' inside
    #  the preceding subquery
    stmt = """select custnum
from """ + gvars.g_schema_arkcasedb + """.orders 
where not exists
(select partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup X
where exists
(select *
from """ + gvars.g_schema_arkcasedb + """.fromsup Y
where Y.suppnum = 6
and Y.partnum = X.partnum
and not exists
(select *
from """ + gvars.g_schema_arkcasedb + """.odetail 
where  """ + gvars.g_schema_arkcasedb + """.odetail.partnum =  X.partnum
and  """ + gvars.g_schema_arkcasedb + """.orders.ordernum =  """ + gvars.g_schema_arkcasedb + """.odetail.ordernum )
)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s11')
    
    #  Query 13
    #  get customer numbers for customers such that every
    #  part they have ordered is supplied by supplier 1 or
    #  supplier 6.
    stmt = """select custnum
from """ + gvars.g_schema_arkcasedb + """.orders 
where not exists
(select *
from """ + gvars.g_schema_arkcasedb + """.odetail 
where  """ + gvars.g_schema_arkcasedb + """.orders.ordernum =  """ + gvars.g_schema_arkcasedb + """.odetail.ordernum
and not exists
(select partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where  """ + gvars.g_schema_arkcasedb + """.fromsup.partnum =  """ + gvars.g_schema_arkcasedb + """.odetail.partnum
and ((suppnum = 1) or (suppnum = 6))
)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s12')
    
    #  Query 14
    #  get customer numbers for customers who get parts
    #  from all suppliers
    stmt = """select custnum
from """ + gvars.g_schema_arkcasedb + """.orders 
where not exists
(select distinct suppnum
from """ + gvars.g_schema_arkcasedb + """.fromsup X
where not exists
(select *
from """ + gvars.g_schema_arkcasedb + """.odetail, """ + gvars.g_schema_arkcasedb + """.fromsup Y
where  """ + gvars.g_schema_arkcasedb + """.orders.ordernum =  """ + gvars.g_schema_arkcasedb + """.odetail.ordernum
and Y.partnum =  """ + gvars.g_schema_arkcasedb + """.odetail.partnum
and Y.suppnum = X.suppnum
)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s13')
    
    #  Query 15
    #  same as above, except use additional subquery instead of
    #  a join
    stmt = """select custnum
from """ + gvars.g_schema_arkcasedb + """.orders 
where not exists
(select distinct suppnum
from """ + gvars.g_schema_arkcasedb + """.fromsup X
where not exists
(select *
from """ + gvars.g_schema_arkcasedb + """.odetail 
where  """ + gvars.g_schema_arkcasedb + """.orders.ordernum =  """ + gvars.g_schema_arkcasedb + """.odetail.ordernum
and partnum in
(select partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup Y
where Y.suppnum = X.suppnum
)
)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s14')
    
    # Query 16
    # same as first, except use view FSDETAIL, which is a join of
    # odetail and fromsup through partnum, instead of using that
    # join explicitly
    stmt = """select custnum
from """ + gvars.g_schema_arkcasedb + """.orders 
where not exists
(select distinct suppnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where not exists
(select *
from """ + gvars.g_schema_arkcasedb + """.fsdetail 
where  """ + gvars.g_schema_arkcasedb + """.orders.ordernum = col_4
and  """ + gvars.g_schema_arkcasedb + """.fsdetail.col_2 =  """ + gvars.g_schema_arkcasedb + """.fromsup.suppnum
)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    #  Query 17
    #  get supplier numbers for which all customers use at
    #  least one of their parts
    stmt = """select suppnum
from """ + gvars.g_schema_arkcasedb + """.fromsup X
where not exists
(select custnum
from """ + gvars.g_schema_arkcasedb + """.orders 
where not exists
(select *
from """ + gvars.g_schema_arkcasedb + """.odetail, """ + gvars.g_schema_arkcasedb + """.fromsup Y
where  """ + gvars.g_schema_arkcasedb + """.odetail.ordernum =  """ + gvars.g_schema_arkcasedb + """.orders.ordernum
and  """ + gvars.g_schema_arkcasedb + """.odetail.partnum = Y.partnum
and Y.suppnum = X.suppnum
)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s15')
    
    _testmgr.testcase_end(desc)

def test005(desc="""Multiple nesting,multiple subqueries connected with"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # and/or,mixed correlated/uncorrelated nested subqueries
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     A05
    #  Description:        Multiple nesting,multiple subqueries connected with
    #                      and/or,mixed correlated/uncorrelated nested subqueries
    #                      Correlated subquery in where clause test
    #                      - this tests multiply nested subqueries
    #                      and multiple subqueries connected with
    #                      and/or.
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
    # get supplier names for suppliers who supply part 4102
    # and part 5504
    
    stmt = """set param ?p 5504;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p1 4102;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select suppname
from """ + gvars.g_schema_arkcasedb + """.supplier 
where ?p1 in
(select partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where """ + gvars.g_schema_arkcasedb + """.fromsup.suppnum = """ + gvars.g_schema_arkcasedb + """.supplier.suppnum
)
and ?p =ANY
(select partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where  """ + gvars.g_schema_arkcasedb + """.fromsup.suppnum =  """ + gvars.g_schema_arkcasedb + """.supplier.suppnum
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s0')
    
    # Query 2
    # same as above,except one subquery correlated, other uncorrelated
    stmt = """set param ?p 4102;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p1 5504;"""
    output = _dci.cmdexec(stmt)
    stmt = """select suppname
from """ + gvars.g_schema_arkcasedb + """.supplier 
where ?p in
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
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s1')
    
    # Query 3
    # get supplier names for suppliers who supply part 4102
    # OR 5504
    stmt = """set param ?p 4102;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p1 5504;"""
    output = _dci.cmdexec(stmt)
    stmt = """select suppname
from """ + gvars.g_schema_arkcasedb + """.supplier 
where ?p in
(select partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where  """ + gvars.g_schema_arkcasedb + """.fromsup.suppnum =  """ + gvars.g_schema_arkcasedb + """.supplier.suppnum
)
OR ?p1 =ANY
(select partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where  """ + gvars.g_schema_arkcasedb + """.fromsup.suppnum =  """ + gvars.g_schema_arkcasedb + """.supplier.suppnum
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s2')
    
    #  Query 4
    #  same as above, except one subquery correlated, other uncorrelated
    stmt = """select suppname
from """ + gvars.g_schema_arkcasedb + """.supplier 
where ?p in
(select partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where  """ + gvars.g_schema_arkcasedb + """.fromsup.suppnum =  """ + gvars.g_schema_arkcasedb + """.supplier.suppnum
)
OR suppnum =ANY
(select suppnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where partnum = ?p1
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s3')
    
    #  Query 5
    #  get supplier names for suppliers who DON'T supply parts
    #  4102 or 5504
    stmt = """select suppname
from """ + gvars.g_schema_arkcasedb + """.supplier 
where NOT (?p in
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
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s4')
    
    # Query 6
    # get supplier names for suppliers who supply parts 4102,
    # 5504, and 5505
    stmt = """set param ?p2 5505;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select suppname
from """ + gvars.g_schema_arkcasedb + """.supplier 
where ?p in
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
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s5')
    
    # Query 7
    # get supplier names for suppliers who supply at least
    # one part whose inventory is negative
    stmt = """set param ?p 0;"""
    output = _dci.cmdexec(stmt)
    stmt = """select suppname
from """ + gvars.g_schema_arkcasedb + """.supplier 
where suppnum in
(select suppnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where ?p >
(select inventory
from """ + gvars.g_schema_arkcasedb + """.parts 
where  """ + gvars.g_schema_arkcasedb + """.parts.partnum =  """ + gvars.g_schema_arkcasedb + """.fromsup.partnum
)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s6')
    
    # Query 8
    # get supplier names for suppliers who supply part 'LP 900 LPM'
    stmt = """set param ?p 'LP 900 LPM';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select suppname
from """ + gvars.g_schema_arkcasedb + """.supplier 
where suppnum IN
(select suppnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where ?p in
(select partname
from """ + gvars.g_schema_arkcasedb + """.parts 
where  """ + gvars.g_schema_arkcasedb + """.parts.partnum =  """ + gvars.g_schema_arkcasedb + """.fromsup.partnum
)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    #  Query 9
    #  get employee names and their jobs for employees who do
    #  not work at branches which are in the same city as the
    #  regional headquarters
    stmt = """select empname,job
from """ + gvars.g_schema_arkcasedb + """.employee 
where branchnum not in
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
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s7')
    
    #  Query 10
    #  get part numbers for all parts supplied by more than
    #  two suppliers
    stmt = """select distinct X.partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup X
where X.partnum in
(select Y.partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup Y
where Y.suppnum <> X.suppnum
and Y.partnum in
(select Z.partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup Z
where Z.suppnum <> Y.suppnum
and Z.suppnum <>  X.suppnum
)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s8')
    
    #  Query 11
    #  same as above, use view fsdetail instead
    stmt = """select distinct X.col_1
from """ + gvars.g_schema_arkcasedb + """.fsdetail X
where X.col_1 in
(select Y.col_1
from """ + gvars.g_schema_arkcasedb + """.fsdetail Y
where Y.col_2 <> X.col_2
and Y.col_1 in
(select Z.col_1
from """ + gvars.g_schema_arkcasedb + """.fsdetail Z
where Z.col_2 <> Y.col_2
and Z.col_2 <> X.col_2
)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s9')
    
    #  Query 12
    #  same as above, except use table fromsup instead of fsdetail
    #  for one of the fsdetail occurences
    stmt = """select distinct partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where partnum in
(select Y.col_1
from """ + gvars.g_schema_arkcasedb + """.fsdetail Y
where Y.col_2 <>  """ + gvars.g_schema_arkcasedb + """.fromsup.suppnum
and Y.col_1 in
(select Z.col_1
from """ + gvars.g_schema_arkcasedb + """.fsdetail Z
where Z.col_2 <> Y.col_2
and Z.col_2 <>  """ + gvars.g_schema_arkcasedb + """.fromsup.suppnum
)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s10')
    
    # Query 13
    # get salesman numbers and order numbers for salesman who
    # have orders for parts stored at location H76 and which
    # have a cost less than 2500 from all suppliers that supply
    # that part
    stmt = """set param ?p 'H76';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p1 2500;"""
    output = _dci.cmdexec(stmt)
    stmt = """select salesman,ordernum
from """ + gvars.g_schema_arkcasedb + """.orders 
where ?p in
(select  """ + gvars.g_schema_arkcasedb + """.parts.location
from """ + gvars.g_schema_arkcasedb + """.odetail, """ + gvars.g_schema_arkcasedb + """.parts 
where ( """ + gvars.g_schema_arkcasedb + """.odetail.partnum =  """ + gvars.g_schema_arkcasedb + """.parts.partnum)
and ( """ + gvars.g_schema_arkcasedb + """.orders.ordernum =  """ + gvars.g_schema_arkcasedb + """.odetail.ordernum)
and ?p1 >ALL
(select partcost
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where  """ + gvars.g_schema_arkcasedb + """.fromsup.partnum =  """ + gvars.g_schema_arkcasedb + """.odetail.partnum
)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s11')
    
    #  Query 14
    #  same as above, except use additional subquery instead of join
    stmt = """select salesman,ordernum
from """ + gvars.g_schema_arkcasedb + """.orders 
where ordernum in
(select ordernum
from """ + gvars.g_schema_arkcasedb + """.odetail 
where ?p in
(select location
from """ + gvars.g_schema_arkcasedb + """.parts 
where partnum =  """ + gvars.g_schema_arkcasedb + """.odetail.partnum
and ?p1 >ALL
(select partcost
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where  """ + gvars.g_schema_arkcasedb + """.fromsup.partnum =  """ + gvars.g_schema_arkcasedb + """.odetail.partnum
)
)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s12')
    
    #  Query 15
    #  same as above, except move final AND condition outside the
    #  subquery
    stmt = """select salesman,ordernum
from """ + gvars.g_schema_arkcasedb + """.orders 
where ordernum in
(select ordernum
from """ + gvars.g_schema_arkcasedb + """.odetail 
where ?p in
(select location
from """ + gvars.g_schema_arkcasedb + """.parts 
where partnum =  """ + gvars.g_schema_arkcasedb + """.odetail.partnum
)
and ?p1 >ALL
(select partcost
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where  """ + gvars.g_schema_arkcasedb + """.fromsup.partnum =  """ + gvars.g_schema_arkcasedb + """.odetail.partnum
)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s13')
    
    _testmgr.testcase_end(desc)

def test006(desc="""Correlated subquery in where clause"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     A06
    #  Description:        Correlated subquery in where clause test
    #                      - this tests the use of
    #                      for READ UNCOMMITTED access,
    #                      for READ COMMITTED access,
    #                      for SERIALIZABLE access
    #                      inside of subqueries.
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
    #  Query 1
    #  get part numbers for all parts supplied by more than one supplier
    
    stmt = """select distinct X.partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup X
where X.partnum in
(select distinct Y.partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup Y
where Y.suppnum <> X.suppnum
for read uncommitted access
)
for read committed access
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s0')
    
    #  Query 2
    #  get part numbers for all parts supplied by more than one supplier
    stmt = """select distinct X.partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup X
where X.partnum in
(select distinct Y.partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup Y
where Y.suppnum <> X.suppnum
for read committed access
)
for serializable access
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s1')
    
    #  Query 3
    #  get part numbers for all parts supplied by more than one supplier
    stmt = """select distinct X.partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup X
where X.partnum in
(select distinct Y.partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup Y
where Y.suppnum <> X.suppnum
for serializable access
)
for serializable access
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s2')
    
    #  Query 4
    #  get part names whose cost is greater than 10000 and whose
    #  price is equal to its' cost from at least one supplier
    #  NOTE: the subquery here returns 0 records sometimes.
    stmt = """select partname
from """ + gvars.g_schema_arkcasedb + """.parts 
where price IN
(select partcost
from """ + gvars.g_schema_arkcasedb + """.expfroms 
where  """ + gvars.g_schema_arkcasedb + """.parts.partnum =  """ + gvars.g_schema_arkcasedb + """.expfroms.partnum
for serializable access
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s3')
    
    # Query 5
    # get part names for parts whose price is less than 2000
    # more than its' cost from all suppliers
    stmt = """set param ?p 2000;"""
    output = _dci.cmdexec(stmt)
    stmt = """select partname
from """ + gvars.g_schema_arkcasedb + """.parts 
where (price - ?p) <all
(select partcost
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where  """ + gvars.g_schema_arkcasedb + """.parts.partnum =  """ + gvars.g_schema_arkcasedb + """.fromsup.partnum
group by partcost
for read uncommitted access
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s4')
    
    #  Query 6
    #  get part names for parts who have the same price as at
    #  least one other part
    stmt = """select col_1
from """ + gvars.g_schema_arkcasedb + """.partsfor X
where X.col_3 =SOME
(select Y.col_3
from """ + gvars.g_schema_arkcasedb + """.partsfor Y
where X.col_1 <> Y.col_1
for read uncommitted access
)
for read uncommitted access
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s5')
    
    #  Query 7
    #  get part names for parts who have the same price as at
    #  least one other part
    stmt = """select col_1
from """ + gvars.g_schema_arkcasedb + """.partsfor X
where X.col_3 =SOME
(select Y.col_3
from """ + gvars.g_schema_arkcasedb + """.partsfor Y
where X.col_1 <> Y.col_1
for read committed access
)
for read committed access
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s6')
    
    #  Query 8
    #  get part names for parts who have the same price as at
    #  least one other part
    stmt = """select col_1
from """ + gvars.g_schema_arkcasedb + """.partsfor X
where X.col_3 =SOME
(select Y.col_3
from """ + gvars.g_schema_arkcasedb + """.partsfor Y
where X.col_1 <> Y.col_1
for serializable access
)
for read uncommitted access
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s7')
    
    #  Query 9
    #  get part numbers for all parts supplied by more than
    #  one supplier
    stmt = """select distinct X.partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup X
where exists
(select Y.partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup Y
where Y.suppnum <> X.suppnum
and X.partnum = Y.partnum
for serializable access
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s8')
    
    # Query 10
    # get supplier numbers for suppliers who supply at least
    # all those parts supplied by supplier 6.
    stmt = """set param ?p  3;"""
    output = _dci.cmdexec(stmt)
    stmt = """select distinct suppnum
from """ + gvars.g_schema_arkcasedb + """.fromsup X
where not exists
(select partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup Y
where suppnum = ?p * 2
and not exists
(select *
from """ + gvars.g_schema_arkcasedb + """.fromsup Z
where X.suppnum = Z.suppnum
and Z.partnum = Y.partnum
for read uncommitted access
)
for read committed access
)
for serializable access
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s9')
    
    #  Query 11
    #  get part numbers for parts supplied to all customers
    #  in California
    stmt = """select distinct partnum
from """ + gvars.g_schema_arkcasedb + """.odetail X
where not exists
(select *
from """ + gvars.g_schema_arkcasedb + """.orders, """ + gvars.g_schema_arkcasedb + """.customer 
where  """ + gvars.g_schema_arkcasedb + """.orders.custnum =  """ + gvars.g_schema_arkcasedb + """.customer.custnum
and  """ + gvars.g_schema_arkcasedb + """.customer.state = 'California'
and not exists
(select *
from """ + gvars.g_schema_arkcasedb + """.odetail Y
where Y.partnum = X.partnum
and  """ + gvars.g_schema_arkcasedb + """.orders.ordernum = Y.ordernum
for read uncommitted access
)
for serializable access
)
for read committed access
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s10')
    
    # Query 12
    # get supplier names for suppliers who supply part 4102
    # and part 5504
    stmt = """set param ?p 4102;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p1 5504;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select suppname
from """ + gvars.g_schema_arkcasedb + """.supplier 
where ?p in
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
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s11')
    
    #  Query 13
    #  get part numbers for all parts supplied by more than
    #  two suppliers
    stmt = """select distinct X.partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup X
where X.partnum in
(select Y.partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup Y
where Y.suppnum <> X.suppnum
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
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s12')
    
    #  Query 14
    #  same as above, use view fsdetail instead
    stmt = """select distinct X.col_1
from """ + gvars.g_schema_arkcasedb + """.fsdetail X
where X.col_1 in
(select Y.col_1
from """ + gvars.g_schema_arkcasedb + """.fsdetail Y
where Y.col_2 <> X.col_2
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
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s13')
    
    _testmgr.testcase_end(desc)

def test007(desc="""SELECT aggregate functions with aggregates in subquery"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     A07
    #  Description:        SELECT aggregate functions with aggregates in
    #                      subquery
    #                      SELECT correlated subquery in WHERE clause
    #                      test - this tests the selection of aggregate
    #                      functions (COUNT, AVG, MAX, MIN, SUM).
    #                      Aggregates are tested in the SELECT clause
    #                      and in the HAVING clause.
    
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
    # get partnames whose price is less than 2000 more than it's
    # average cost from all suppliers who supply it
    
    stmt = """set param ?p 2000;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select partname
from """ + gvars.g_schema_arkcasedb + """.parts 
where price <
(select avg(partcost) + ?p
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where partnum =  """ + gvars.g_schema_arkcasedb + """.parts.partnum
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s0')
    
    # Query 2
    # get branchnames of branches whose total yearly payroll
    # exceeds 150000
    stmt = """set param ?p 150000;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select branchname
from """ + gvars.g_schema_arkcasedb + """.branch 
where exists
(select regnum
from """ + gvars.g_schema_arkcasedb + """.employee 
where  """ + gvars.g_schema_arkcasedb + """.employee.regnum =  """ + gvars.g_schema_arkcasedb + """.branch.regnum
and    """ + gvars.g_schema_arkcasedb + """.employee.branchnum =  """ + gvars.g_schema_arkcasedb + """.branch.branchnum
group by regnum, branchnum
having sum(salary) > ?p
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s1')
    
    #  Query 3
    #  get employee names whose salaries are greater than the
    #  average salary for their branch
    stmt = """select empname
from """ + gvars.g_schema_arkcasedb + """.employee X
where salary >
(select avg(salary)
from """ + gvars.g_schema_arkcasedb + """.employee Y
where Y.branchnum = X.branchnum
and Y.regnum = X.regnum
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s2')
    
    # Query 4
    # get employee names whose salaries are greater than the
    # 'median' salary for their branch
    stmt = """set param ?p 2;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select empname
from """ + gvars.g_schema_arkcasedb + """.employee X
where salary >
(select min(salary) + ((max(salary) - min(salary)) / ?p)
from """ + gvars.g_schema_arkcasedb + """.employee Y
where Y.branchnum = X.branchnum
and Y.regnum = X.regnum
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s3')
    
    #  Query 5
    #  get employee names of those employees whose age is greater
    #  than or equal to the max. age of the branch in their region
    #  with the highest average age
    stmt = """select empname
from """ + gvars.g_schema_arkcasedb + """.employee X
where age >=ALL
(select max(age)
from """ + gvars.g_schema_arkcasedb + """.employee Y
where Y.regnum = X.regnum
group by branchnum
having avg(age) >=ALL
(select avg(age)
from """ + gvars.g_schema_arkcasedb + """.employee Z
where Z.regnum = X.regnum
group by branchnum
)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s4')
    
    #  Query 6
    #  get employee names of those employees whose age is greater
    #  than or equal to the max. age of the branch in their region
    #  with the highest average age (eliminate middle WHERE clause)
    stmt = """select empname
from """ + gvars.g_schema_arkcasedb + """.employee X
where age >=ALL
(select max(age)
from """ + gvars.g_schema_arkcasedb + """.employee Y
group by regnum, branchnum
having Y.regnum = X.regnum
and avg(age) >=ALL
(select avg(age)
from """ + gvars.g_schema_arkcasedb + """.employee Z
where Z.regnum = X.regnum
group by branchnum
)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s5')
    
    #  Query 7
    #  get employee names who make more than the average salary
    #  for their branch, excluding the branchs' managers' salary
    stmt = """select empname
from """ + gvars.g_schema_arkcasedb + """.employee X
where salary >
(select avg(salary)
from """ + gvars.g_schema_arkcasedb + """.employee Y, """ + gvars.g_schema_arkcasedb + """.branch 
where Y.regnum =  """ + gvars.g_schema_arkcasedb + """.branch.regnum
and Y.branchnum =  """ + gvars.g_schema_arkcasedb + """.branch.branchnum
and Y.empnum <>  """ + gvars.g_schema_arkcasedb + """.branch.manager
and X.regnum = Y.regnum
and X.branchnum = Y.branchnum
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s6')
    
    _testmgr.testcase_end(desc)

def test008(desc="""SELECT with subquery on the left-hand of predicate."""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     A08
    #  Description:        SELECT with subquery on the left-hand of
    #			predicate.  Also the create view uses the
    #			same method.
    # =================== End Test Case Header  ===================
    
    stmt = """drop table tab1;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table tab1 (
char_1                    char(1)        DEFAULT NULL
, varchar_1                 VARCHAR(2)     DEFAULT NULL
, numeric_1                 NUMERIC(4,0)   DEFAULT NULL
, pic_comp_1                PIC S9(3)V9(5) DEFAULT NULL
, medium_1                  INT            DEFAULT NULL
, decimal_1                 DECIMAL(1,0)   DEFAULT NULL
, real_1                    real           DEFAULT NULL
, y_to_d_1                  DATE           DEFAULT NULL
, y_to_d_2                  DATE           DEFAULT NULL
, time_1                    TIME           DEFAULT NULL
, iy_to_mo                  INTERVAL YEAR(4) TO MONTH DEFAULT NULL
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into tab1 values('C','FF',3000,43.405,65,4,40.4567,DATE '1997-06-12',DATE '1997-06-13', TIME '12:40:05',INTERVAL '0-4' YEAR TO MONTH);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """create table tab2 (
char_1                    char(1)        DEFAULT NULL
, varchar_1                 VARCHAR(2)     DEFAULT NULL
, numeric_1                 NUMERIC(4,0)   DEFAULT NULL
, pic_comp_1                PIC S9(3)V9(5) DEFAULT NULL
, medium_1                  INT            DEFAULT NULL
, decimal_1                 DECIMAL(1,0)   DEFAULT NULL
, real_1                    real           DEFAULT NULL
, y_to_d_1                  DATE           DEFAULT NULL
, y_to_d_2                  DATE           DEFAULT NULL
, time_1                    TIME           DEFAULT NULL
, iy_to_mo                  INTERVAL YEAR(4) TO MONTH DEFAULT NULL
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into tab2 values('A','DD',1000,23.405,45,2,10.31,DATE '1997-06-01',DATE  '1997-06-03', TIME '13:40:05',INTERVAL '2-7' YEAR TO MONTH);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into tab2 values('B','EE',2000,33.405,55,3,20.200,DATE '1997-06-06',DATE '1997-06-03', TIME '13:00:05',INTERVAL '1-8' YEAR TO MONTH);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into tab2 values('C','FF',3000,43.405,65,4,40.4567,DATE '1997-06-12',DATE '1997-06-13', TIME '12:40:05',INTERVAL '0-4' YEAR TO MONTH);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into tab2 values('D','AD',1000,23.405,45,2,10.31,DATE '1997-06-01',DATE '1997-06-03', TIME '13:40:05',INTERVAL '2-7' YEAR TO MONTH);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into tab2 values('E','AE',2000,33.405,55,3,20.200,DATE '1997-06-06',DATE '1997-06-03', TIME '13:00:05',INTERVAL '1-8' YEAR TO MONTH);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into tab2 values('F','AF',3000,43.405,65,4,40.4567,DATE '1900-06-12',DATE '1897-06-13', TIME '02:59:59',INTERVAL '4-4' YEAR TO MONTH);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into tab2 values('G','BF',3000,43.405,65,4,40.4567,DATE '1997-06-12',DATE '1997-06-13', TIME '12:40:05',INTERVAL '0-4' YEAR TO MONTH);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into tab2 (char_1, varchar_1) values('Z','ZE');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select char_1, pic_comp_1, iy_to_mo
from tab1 
where (select varchar_1 from tab2 where varchar_1 = 'FF') = tab1.varchar_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s0')
    
    stmt = """set param ?p '12:40:05';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select char_1, cast(medium_1 as varchar(30)), cast(time_1 as varchar(12))
from tab2 
where
(select time_1
from tab1 where cast(time_1 as varchar(8)) = '12:40:05') in (?p);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s1')
    
    stmt = """set param ?m 65;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select char_1, medium_1, time_1
from tab2 
where
(select char_1
from tab1 where medium_1 in (100, 40, 37.08, 130-?m)) is not null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s2')
    
    stmt = """select char_1 || cast(medium_1 as varchar(30)) || cast(time_1 as char(12))
from tab2 
where
(select char_1
from tab1 where medium_1 not in (100, 40, 37.08, 130*?m)) is not null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s3')
    
    stmt = """select char_1, varchar_1, medium_1, time_1
from tab2 
where
(select varchar_1
from tab1 
where medium_1 not in (100, 40, 37.08, 130*?m)) = any
(select varchar_1
from tab2 
group by varchar_1
having varchar_1 is not null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s4')
    
    stmt = """insert into tab2 (char_1, varchar_1) values('Z','YE');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select distinct (char_1), pic_comp_1 + 100.00009, time_1
from tab2 
where (select cast(iy_to_mo as varchar(8)) from tab1) is not null
group by char_1, pic_comp_1, time_1
order by 1, 2 desc, 3 desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s5')
    
    stmt = """select char_1, medium_1, time_1
from tab2 
where
(select time_1
from tab1 where tab1.time_1 = tab2.time_1) in (?p);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s6')
    
    # AR 2/7/07 Added order by
    stmt = """select char_1, max(medium_1), time_1
from tab2 
group by char_1, medium_1, time_1, y_to_d_1
having
(select time_1
from tab1 where tab1.time_1 = tab2.time_1 and
 tab1.y_to_d_1 = tab2.y_to_d_1) in (?p) order by char_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s7')
    
    stmt = """select char_1, min(medium_1), time_1
from tab2 
group by char_1, medium_1, time_1
having (select min(time_1) from tab1) = tab2.time_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s8')
    
    stmt = """select char_1, avg(medium_1), time_1
from tab2 
group by char_1, medium_1, time_1, numeric_1
having (select avg(numeric_1) from tab1) = tab2.numeric_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s9')
    
    stmt = """select char_1, avg(medium_1), time_1
from tab2 
group by char_1, medium_1, time_1
having (select time_1
from tab1 
group by time_1
having time_1 is not null) = tab2.time_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s10')
    
    stmt = """select char_1, avg(medium_1), time_1
from tab2 
group by char_1, medium_1, time_1
having (select time_1
from tab1 
group by time_1
having time_1 is not null) <> tab2.time_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s11')
    
    stmt = """select time_1
from tab2 
group by time_1
having (select tab1.time_1 from tab1 
group by time_1
having time_1 in
(select time_1 from tab1 
group by time_1
having time_1 in
(cast('00:59:50' as time), cast('12:34:45' as time), tab1.time_1))) 	in (tab2.time_1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s12')
    
    stmt = """select char_1, varchar_1, iy_to_mo, y_to_d_2
from tab2 
where (select iy_to_mo from tab1) between
cast('00-01' as interval year(4) to month) and
cast('9999-11' as interval year(4) to month);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s13')
    
    stmt = """select *
from tab2 
group by char_1, varchar_1, medium_1, numeric_1, pic_comp_1, decimal_1,
real_1, time_1, y_to_d_1, y_to_d_2, iy_to_mo
having exists
(select real_1 from tab1 
where (select distinct(real_1) from tab1) <> some
(select real_1 from tab2));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s14')
    
    ##expect any *--- SQL operation complete.*
    stmt = """create view vtab12 
as select * from tab2 
where (select y_to_d_1 from tab1) = tab2.y_to_d_1;"""
    output = _dci.cmdexec(stmt)
    
    ##expectfile ${test_dir}/a08exp a08s15
    stmt = """select * from vtab12;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s from select char_1, numeric_1
from tab2 
group by char_1, numeric_1
having  (char_1, numeric_1) in
(  values ('A', 1000), ('F', 3000), (char_1, 2000));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s16')
    
    stmt = """select char_1, numeric_1
from tab2 
group by char_1, numeric_1
having (char_1, numeric_1) in
(values (char_1, 9999));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """select char_1, numeric_1
from tab2 
group by char_1, numeric_1
having numeric_1 in (values (1000));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s18')
    
    _testmgr.testcase_end(desc)

