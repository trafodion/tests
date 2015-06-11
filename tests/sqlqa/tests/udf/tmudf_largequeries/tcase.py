# @@@ START COPYRIGHT @@@
#
# (C) Copyright 2015 Hewlett-Packard Development Company, L.P.
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

# This set of tests include actual TPCH queries with embedded UDFs in the
# queries.  Each query is run twice.  The first time UDF is not involved
# and the second time UDFs are embedded in the query.  The tests ensure that
# the way the UDFs used in the query do not change the results of the query.
# The results from the two queries should be the same.
# Be aware that these are large queries.  Unless you have a system that is
# in decent size, you should not try this set of tests on a small machine.

def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci
    
    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()

def test001(desc="""rowcounts"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    stmt = """set schema """ + gvars.tpch2x_schema + """;"""
    output = _dci.cmdexec(stmt)

    # Do a quick double check on table row counts first.
    stmt = """select count(*) from CUSTOMER;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '300000')
    stmt = """select count(*) from LINEITEM;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '11997996')
    stmt = """select count(*) from NATION;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '25')
    stmt = """select count(*) from ORDERS;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '3000000')
    stmt = """select count(*) from PARTSUPP;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '1600000')
    stmt = """select count(*) from PART;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '400000')
    stmt = """select count(*) from REGION;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '5')
    stmt = """select count(*) from SUPPLIER;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '20000')
    
    _testmgr.testcase_end(desc)

def test002(desc="""Q14"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    stmt = """set schema """ + gvars.tpch2x_schema + """;"""
    output = _dci.cmdexec(stmt)

    # Query Stream 0
    # TPC TPC-H Parameter Substitution (Version 2.3.1 build 2)
    # using 638592433 as a seed to the RNG
    # ?SECTION Q14
    # TPC-H/TPC-R Promotion Effect Query (Q14)
    # Stream 0, Query 14
    # Database -- <catalog>.<schema>
   
    # determine what % of revenue in a given year & month was derived
    # from promotional parts shipped in a given month.

    # 1st query without UDF
    stmt = """prepare xx from select
cast( (100.00 * sum(case
when p_type like 'PROMO%'
then l_extendedprice * (1 - l_discount)
else 0
end) / sum(l_extendedprice * (1 - l_discount))
) as numeric(18,3)) as promo_revenue
from
lineitem,
part
where
l_partkey = p_partkey
and l_shipdate >= date '1996-01-01'
and l_shipdate < date '1996-01-01' + interval '1' month;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/A01.exp""", """f1""")

    # 2nd query with UDF. Should return the same results as the 1st query.
    stmt = """prepare xx from select
cast( (100.00 * sum(case
when p_type like 'PROMO%'
then l_extendedprice * (1 - l_discount)
else 0
end) / sum(l_extendedprice * (1 - l_discount))
) as numeric(18,3)) as promo_revenue
from
UDF(""" + defs.my_schema + """.qaTmudfGeneral(TABLE(select * from lineitem),
'TEST_RUNTIME_EMIT_X_ROWS', '1')),
UDF(""" + defs.my_schema + """.qaTmudfGeneral(TABLE(select * from part),
'TEST_RUNTIME_EMIT_X_ROWS', '1'))
where
l_partkey = p_partkey
and l_shipdate >= date '1996-01-01'
and l_shipdate < date '1996-01-01' + interval '1' month;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/A01.exp""", """f1""")
    
    _testmgr.testcase_end(desc)

def test003(desc="""Q2"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    stmt = """set schema """ + gvars.tpch2x_schema + """;"""
    output = _dci.cmdexec(stmt)

    # ?SECTION Q2
    # TPC-H/TPC-R Minimum Cost Supplier Query (Q2)
    # Stream 0, Query 2
    # Database -- <catalog>.<schema>
    
    # For a given region, find the supplier who can supply a part
    # type and size at least cost.a

    # 1st query without UDF
    stmt = """prepare xx from select
--    [first 100]
cast(s_acctbal as numeric(18,2)),
s_name,
n_name,
p_partkey,
p_mfgr,
s_address,
s_phone,
s_comment
from
part,
supplier,
partsupp,
nation,
region
where
p_partkey = ps_partkey
and s_suppkey = ps_suppkey
and p_size = 5
and p_type like '%NICKEL'
and s_nationkey = n_nationkey
and n_regionkey = r_regionkey
and r_name = 'AMERICA'
and ps_supplycost = (
select
min(ps_supplycost)
from
partsupp,
supplier,
nation,
region
where
p_partkey = ps_partkey
and s_suppkey = ps_suppkey
and s_nationkey = n_nationkey
and n_regionkey = r_regionkey
and r_name = 'AMERICA'
)
order by
s_acctbal desc,
n_name,
s_name,
p_partkey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/A02.exp""", """f1""")

    # 2nd query with UDF. Should return the same results as the 1st query.
    stmt = """prepare xx from select
--    [first 100]
cast(s_acctbal as numeric(18,2)),
s_name,
n_name,
p_partkey,
p_mfgr,
s_address,
s_phone,
s_comment
from
part,
supplier,
partsupp,
nation,
region
where
p_partkey = ps_partkey
and s_suppkey = ps_suppkey
and p_size = 5
and p_type like '%NICKEL'
and s_nationkey = n_nationkey
and n_regionkey = r_regionkey
and r_name = 'AMERICA'
and ps_supplycost = (
select
min(ps_supplycost)
from
UDF(""" + defs.my_schema + """.qaTmudfGeneral(TABLE(select * from partsupp),
'TEST_RUNTIME_EMIT_X_ROWS', '1')),
UDF(""" + defs.my_schema + """.qaTmudfGeneral(TABLE(select * from supplier),
'TEST_RUNTIME_EMIT_X_ROWS', '1')),
UDF(""" + defs.my_schema + """.qaTmudfGeneral(TABLE(select * from nation),
'TEST_RUNTIME_EMIT_X_ROWS', '1')),
UDF(""" + defs.my_schema + """.qaTmudfGeneral(TABLE(select * from region),
'TEST_RUNTIME_EMIT_X_ROWS', '1'))
where
p_partkey = ps_partkey
and s_suppkey = ps_suppkey
and s_nationkey = n_nationkey
and n_regionkey = r_regionkey
and r_name = 'AMERICA'
)
order by
s_acctbal desc,
n_name,
s_name,
p_partkey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/A02.exp""", """f1""")

    _testmgr.testcase_end(desc)

def test004(desc="""Q9"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    stmt = """set schema """ + gvars.tpch2x_schema + """;"""
    output = _dci.cmdexec(stmt)
    
    # ?SECTION Q9
    # TPC-H/TPC-R Product Type Profit Measure Query (Q9)
    # Stream 0, Query 9
    # Database -- <catalog>.<schema>
    
    # determine how much profit is made on a line of
    # parts, broken out by supplier nation and year.

    # 1st query without UDF
    stmt = """prepare xx from select
nation,
o_year,
cast(sum(amount) as numeric(18,2)) as sum_profit
from
(
select
n_name as nation,
extract(year from o_orderdate) as o_year,
l_extendedprice * (1 - l_discount) - ps_supplycost * l_quantity as amount
from
part,
supplier,
lineitem,
partsupp,
orders,
nation
where
s_suppkey = l_suppkey
and ps_suppkey = l_suppkey
and ps_partkey = l_partkey
and p_partkey = l_partkey
and o_orderkey = l_orderkey
and s_nationkey = n_nationkey
and p_name like '%maroon%'
) as profit
group by
nation,
o_year
order by
nation,
o_year desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/A03.exp""", """f1""")
   
    # 2nd query with UDF. Should return the same results as the 1st query. 
    stmt = """prepare xx from select
nation,
o_year,
cast(sum(amount) as numeric(18,2)) as sum_profit
from
(
select
n_name as nation,
extract(year from o_orderdate) as o_year,
l_extendedprice * (1 - l_discount) - ps_supplycost * l_quantity as amount
from
UDF(""" + defs.my_schema + """.qaTmudfGeneral(TABLE(select * from part),
'TEST_RUNTIME_EMIT_X_ROWS', '1')),
UDF(""" + defs.my_schema + """.qaTmudfGeneral(TABLE(select * from supplier),
'TEST_RUNTIME_EMIT_X_ROWS', '1')),
UDF(""" + defs.my_schema + """.qaTmudfGeneral(TABLE(select * from lineitem),
'TEST_RUNTIME_EMIT_X_ROWS', '1')),
UDF(""" + defs.my_schema + """.qaTmudfGeneral(TABLE(select * from partsupp),
'TEST_RUNTIME_EMIT_X_ROWS', '1')),
UDF(""" + defs.my_schema + """.qaTmudfGeneral(TABLE(select * from orders),
'TEST_RUNTIME_EMIT_X_ROWS', '1')),
UDF(""" + defs.my_schema + """.qaTmudfGeneral(TABLE(select * from nation),
'TEST_RUNTIME_EMIT_X_ROWS', '1'))
where
s_suppkey = l_suppkey
and ps_suppkey = l_suppkey
and ps_partkey = l_partkey
and p_partkey = l_partkey
and o_orderkey = l_orderkey
and s_nationkey = n_nationkey
and p_name like '%maroon%'
) as profit
group by
nation,
o_year
order by
nation,
o_year desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/A03.exp""", """f1""")
    
    _testmgr.testcase_end(desc)

def test005(desc="""Q6"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    stmt = """set schema """ + gvars.tpch2x_schema + """;"""
    output = _dci.cmdexec(stmt)
    
    # ?SECTION Q6
    # TPC-H/TPC-R Forecasting Revenue Change Query (Q6)
    # Stream 0, Query 6
    # Database -- <catalog>.<schema>
    
    # consider all lineitems shipped in a given year with discounts
    # within a specified range.  Lists the amount by which the total revenue
    # would have increased if these discounts had been eliminated.

    # 1st query without UDF
    stmt = """prepare xx from select
cast(sum(l_extendedprice*l_discount) as numeric(18,2)) as revenue
from
lineitem
where
l_shipdate >= date '1997-01-01'
and l_shipdate < date '1997-01-01' + interval '1' year
and l_discount between 0.03 - 0.01 and 0.03 + 0.01
and l_quantity < 25;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/A04.exp""", """f1""")
   
    # 2nd query with UDF. Should return the same results as the 1st query.
    stmt = """prepare xx from select
cast(sum(l_extendedprice*l_discount) as numeric(18,2)) as revenue
from
UDF(""" + defs.my_schema + """.qaTmudfGeneral(TABLE(select * from lineitem),
'TEST_RUNTIME_EMIT_X_ROWS', '1'))
where
l_shipdate >= date '1997-01-01'
and l_shipdate < date '1997-01-01' + interval '1' year
and l_discount between 0.03 - 0.01 and 0.03 + 0.01
and l_quantity < 25;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/A04.exp""", """f1""")
    
    _testmgr.testcase_end(desc)

def test006(desc="""Q8"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    stmt = """set schema """ + gvars.tpch2x_schema + """;"""
    output = _dci.cmdexec(stmt)
    
    # ?SECTION Q8
    # TPC-H/TPC-R National Market Share Query (Q8)
    # Stream 0, Query 8
    # Database -- <catalog>.<schema>
    
    # determines how the market share of a given nation in a given
    # region has changed over two years for a given part type. Market
    # share is the fraction of the revenue from products of a given type
    # that was generated by suppliers from the given nation.

    # 1st query without UDF
    stmt = """prepare xx from select
o_year,
cast(sum(case
when nation = 'JORDAN' then volume
else 0
end) / sum(volume) as numeric(18,3)) as mkt_share
from
(
select
extract(year from o_orderdate) as o_year,
l_extendedprice * (1 - l_discount) as volume,
n2.n_name as nation
from
part,
supplier,
lineitem,
orders,
customer,
nation n1,
nation n2,
region
where
p_partkey = l_partkey
and s_suppkey = l_suppkey
and l_orderkey = o_orderkey
and o_custkey = c_custkey
and c_nationkey = n1.n_nationkey
and n1.n_regionkey = r_regionkey
and r_name = 'MIDDLE EAST'
and s_nationkey = n2.n_nationkey
and o_orderdate between date '1995-01-01' and date '1996-12-31'
and p_type = 'LARGE ANODIZED COPPER'
) as all_nations
group by
o_year
order by
o_year;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/A05.exp""", """f1""")
   
    # 2nd query with UDF. Should return the same results as the 1st query. 
    stmt = """prepare xx from select
o_year,
cast(sum(case
when nation = 'JORDAN' then volume
else 0
end) / sum(volume) as numeric(18,3)) as mkt_share
from
(
select
extract(year from o_orderdate) as o_year,
l_extendedprice * (1 - l_discount) as volume,
n2.n_name as nation
from
UDF(""" + defs.my_schema + """.qaTmudfGeneral(TABLE(select * from part),
'TEST_RUNTIME_EMIT_X_ROWS', '1')),
UDF(""" + defs.my_schema + """.qaTmudfGeneral(TABLE(select * from supplier),
'TEST_RUNTIME_EMIT_X_ROWS', '1')),
UDF(""" + defs.my_schema + """.qaTmudfGeneral(TABLE(select * from lineitem),
'TEST_RUNTIME_EMIT_X_ROWS', '1')),
UDF(""" + defs.my_schema + """.qaTmudfGeneral(TABLE(select * from orders),
'TEST_RUNTIME_EMIT_X_ROWS', '1')),
UDF(""" + defs.my_schema + """.qaTmudfGeneral(TABLE(select * from customer),
'TEST_RUNTIME_EMIT_X_ROWS', '1')),
UDF(""" + defs.my_schema + """.qaTmudfGeneral(TABLE(select * from nation),
'TEST_RUNTIME_EMIT_X_ROWS', '1')) n1,
UDF(""" + defs.my_schema + """.qaTmudfGeneral(TABLE(select * from nation),
'TEST_RUNTIME_EMIT_X_ROWS', '1')) n2,
UDF(""" + defs.my_schema + """.qaTmudfGeneral(TABLE(select * from region),
'TEST_RUNTIME_EMIT_X_ROWS', '1'))
where
p_partkey = l_partkey
and s_suppkey = l_suppkey
and l_orderkey = o_orderkey
and o_custkey = c_custkey
and c_nationkey = n1.n_nationkey
and n1.n_regionkey = r_regionkey
and r_name = 'MIDDLE EAST'
and s_nationkey = n2.n_nationkey
and o_orderdate between date '1995-01-01' and date '1996-12-31'
and p_type = 'LARGE ANODIZED COPPER'
) as all_nations
group by
o_year
order by
o_year;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/A05.exp""", """f1""")
    
    _testmgr.testcase_end(desc)

def test007(desc="""Q13"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    stmt = """set schema """ + gvars.tpch2x_schema + """;"""
    output = _dci.cmdexec(stmt)
    
    # ?SECTION Q13
    # TPC-H/TPC-R Customer Distribution Query (Q13)
    # Stream 0, Query 13
    # Database -- <catalog>.<schema>
    
    # determines the distribution of customers by the number of orders
    # they have made, including customers who have no record of orders,
    # past or present. Counts and reports how many customers have no
    # orders, how many have 1, 2, 3, etc. A check is made to ensure that
    # the orders counted do not fall into one of several special categories
    # of orders. Special categories are identified in the order comment
    # column by looking for a particular pattern.

    # 1st query without UDF
    stmt = """prepare xx from select
c_count,
count(*) as custdist
from
(
select
c_custkey,
count(o_orderkey)
from
customer left outer join orders on
c_custkey = o_custkey
and o_comment not like '%special%accounts%'
group by
c_custkey
) as c_orders (c_custkey, c_count)
group by
c_count
order by
custdist desc,
c_count desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/A06.exp""", """f1""")
   
    # 2nd query with UDF. Should return the same results as the 1st query. 
    stmt = """prepare xx from select
c_count,
count(*) as custdist
from
(
select
c_custkey,
count(o_orderkey)
from
UDF(""" + defs.my_schema + """.qaTmudfGeneral(TABLE(select * from customer),
'TEST_RUNTIME_EMIT_X_ROWS', '1'))
left outer join 
UDF(""" + defs.my_schema + """.qaTmudfGeneral(TABLE(select * from orders),
'TEST_RUNTIME_EMIT_X_ROWS', '1'))
on
c_custkey = o_custkey
and o_comment not like '%special%accounts%'
group by
c_custkey
) as c_orders (c_custkey, c_count)
group by
c_count
order by
custdist desc,
c_count desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/A06.exp""", """f1""")
    
    _testmgr.testcase_end(desc)

def test008(desc="""Q3"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    stmt = """set schema """ + gvars.tpch2x_schema + """;"""
    output = _dci.cmdexec(stmt)
    
    # ?SECTION Q3
    # TPC-H/TPC-R Shipping Priority Query (Q3)
    # Stream 0, Query 3
    # Database -- <catalog>.<schema>
    
    # retrieves the shipping priority and potential revenue of orders
    # having the largest revenue among those that had not been shipped
    # as of a given date.

    # 1st query without UDF
    stmt = """prepare xx from select
--      [first 10]
l_orderkey,
cast(sum(l_extendedprice*(1-l_discount)) as numeric(18,2)) as revenue,
o_orderdate,
o_shippriority
from
customer,
orders,
lineitem
where
c_mktsegment = 'HOUSEHOLD'
and c_custkey = o_custkey
and l_orderkey = o_orderkey
and o_orderdate < date '1995-03-12'
and l_shipdate > date '1995-03-12'
group by
l_orderkey,
o_orderdate,
o_shippriority
order by
revenue desc,
o_orderdate;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/A07.exp""", """f1""")
   
    # 2nd query with UDF. Should return the same results as the 1st query. 
    stmt = """prepare xx from select
--      [first 10]
l_orderkey,
cast(sum(l_extendedprice*(1-l_discount)) as numeric(18,2)) as revenue,
o_orderdate,
o_shippriority
from
UDF(""" + defs.my_schema + """.qaTmudfGeneral(TABLE(select * from customer),
'TEST_RUNTIME_EMIT_X_ROWS', '1')),
UDF(""" + defs.my_schema + """.qaTmudfGeneral(TABLE(select * from orders),
'TEST_RUNTIME_EMIT_X_ROWS', '1')),
UDF(""" + defs.my_schema + """.qaTmudfGeneral(TABLE(select * from lineitem),
'TEST_RUNTIME_EMIT_X_ROWS', '1'))
where
c_mktsegment = 'HOUSEHOLD'
and c_custkey = o_custkey
and l_orderkey = o_orderkey
and o_orderdate < date '1995-03-12'
and l_shipdate > date '1995-03-12'
group by
l_orderkey,
o_orderdate,
o_shippriority
order by
revenue desc,
o_orderdate;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/A07.exp""", """f1""")
    
    _testmgr.testcase_end(desc)

def test009(desc="""Q16"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    stmt = """set schema """ + gvars.tpch2x_schema + """;"""
    output = _dci.cmdexec(stmt)
    
    # ?SECTION Q16
    # TPC-H/TPC-R Parts/Supplier Relationship Query (Q16)
    # Stream 0, Query 16
    # Database -- <catalog>.<schema>
    
    # count the number of suppliers who can supply parts that satisfy a
    # particular customer's requirements

    # 1st query without UDF
    stmt = """prepare xx from select
--      [last 0]
p_brand,
p_type,
p_size,
count(distinct ps_suppkey) as supplier_cnt
from
partsupp,
part
where
p_partkey = ps_partkey
and p_brand <> 'Brand#13'
and p_type not like 'SMALL PLATED%'
and p_size in (22, 14, 8, 18, 49, 1, 33, 6)
and ps_suppkey not in (
select
s_suppkey
from
supplier
where
s_comment like '%Customer%Complaints%'
)
group by
p_brand,
p_type,
p_size
order by
supplier_cnt desc,
p_brand,
p_type,
p_size;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/A08.exp""", """f1""")
   
    # 2nd query with UDF. Should return the same results as the 1st query. 
    stmt = """prepare xx from select
--      [last 0]
p_brand,
p_type,
p_size,
count(distinct ps_suppkey) as supplier_cnt
from
partsupp,
part
where
p_partkey = ps_partkey
and p_brand <> 'Brand#13'
and p_type not like 'SMALL PLATED%'
and p_size in (22, 14, 8, 18, 49, 1, 33, 6)
and ps_suppkey not in (
select
s_suppkey
from
UDF(""" + defs.my_schema + """.qaTmudfGeneral(TABLE(select * from supplier),
'TEST_RUNTIME_EMIT_X_ROWS', '1'))
where
s_comment like '%Customer%Complaints%'
)
group by
p_brand,
p_type,
p_size
order by
supplier_cnt desc,
p_brand,
p_type,
p_size;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/A08.exp""", """f1""")
    
    _testmgr.testcase_end(desc)

def test010(desc="""Q4"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    stmt = """set schema """ + gvars.tpch2x_schema + """;"""
    output = _dci.cmdexec(stmt)
    
    # ?SECTION Q4
    # TPC-H/TPC-R Order Priority Checking Query (Q4)
    # Stream 0, Query 4
    # Database -- <catalog>.<schema>
    
    # counts the number of orders ordered in a given quarter of a given
    # year in which at least at least one lineitem was received later
    # than its committed date. The query lists the count of such orders
    # for each order priority sorted in ascending priority order.

    # 1st query without UDF
    stmt = """prepare xx from select
o_orderpriority,
count(*) as order_count
from
orders
where
o_orderdate >= date '1994-10-01'
and o_orderdate < date '1994-10-01' + interval '3' month
and exists (
select
*
from
lineitem
where
l_orderkey = o_orderkey
and l_commitdate < l_receiptdate
)
group by
o_orderpriority
order by
o_orderpriority;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/A09.exp""", """f1""")
    
    # 2nd query with UDF. Should return the same results as the 1st query.
    stmt = """prepare xx from select
o_orderpriority,
count(*) as order_count
from
orders
where
o_orderdate >= date '1994-10-01'
and o_orderdate < date '1994-10-01' + interval '3' month
and exists (
select
*
from
UDF(""" + defs.my_schema + """.qaTmudfGeneral(TABLE(select * from lineitem),
'TEST_RUNTIME_EMIT_X_ROWS', '1'))
where
l_orderkey = o_orderkey
and l_commitdate < l_receiptdate
)
group by
o_orderpriority
order by
o_orderpriority;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/A09.exp""", """f1""")
    
    _testmgr.testcase_end(desc)

def test011(desc="""Q11"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    stmt = """set schema """ + gvars.tpch2x_schema + """;"""
    output = _dci.cmdexec(stmt)
    
    # ?SECTION Q11
    # TPC-H/TPC-R Important Stock Identification Query (Q11)
    # Stream 0, Query 11
    # Database -- <catalog>.<schema>
    
    # find, for suppliers in a given nation, all the parts that represent
    # a significant percentage of the total value of all available parts

    # 1st query without UDF
    stmt = """prepare xx from select
--      [last 0]
ps_partkey,
cast(sum(ps_supplycost * ps_availqty) as numeric(18,2)) as valuea
from
partsupp,
supplier,
nation
where
ps_suppkey = s_suppkey
and s_nationkey = n_nationkey
and n_name = 'ROMANIA'
group by
ps_partkey having
sum(ps_supplycost * ps_availqty) > (
select
sum(ps_supplycost * ps_availqty) * 0.0001000000
from
partsupp,
supplier,
nation
where
ps_suppkey = s_suppkey
and s_nationkey = n_nationkey
and n_name = 'ROMANIA'
)
order by
valuea desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/A10.exp""", """f1""")
   
    # 2nd query with UDF. Should return the same results as the 1st query. 
    stmt = """prepare xx from select
--      [last 0]
ps_partkey,
cast(sum(ps_supplycost * ps_availqty) as numeric(18,2)) as valuea
from
partsupp,
supplier,
nation
where
ps_suppkey = s_suppkey
and s_nationkey = n_nationkey
and n_name = 'ROMANIA'
group by
ps_partkey having
sum(ps_supplycost * ps_availqty) > (
select
sum(ps_supplycost * ps_availqty) * 0.0001000000
from
UDF(""" + defs.my_schema + """.qaTmudfGeneral(TABLE(select * from partsupp),
'TEST_RUNTIME_EMIT_X_ROWS', '1')),
UDF(""" + defs.my_schema + """.qaTmudfGeneral(TABLE(select * from supplier),
'TEST_RUNTIME_EMIT_X_ROWS', '1')),
UDF(""" + defs.my_schema + """.qaTmudfGeneral(TABLE(select * from nation),
'TEST_RUNTIME_EMIT_X_ROWS', '1'))
where
ps_suppkey = s_suppkey
and s_nationkey = n_nationkey
and n_name = 'ROMANIA'
)
order by
valuea desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/A10.exp""", """f1""")
    
    _testmgr.testcase_end(desc)

def test012(desc="""Q15"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    stmt = """set schema """ + gvars.tpch2x_schema + """;"""
    output = _dci.cmdexec(stmt)
    
    # ?SECTION Q15
    # TPC-H/TPC-R Top Supplier Query (Q15)
    # Stream 0, Query 15
    # Database -- <catalog>.<schema>
    
    # determines supplier who contributed most to the overall revenue
    # for parts shipped during a given quarter of a given year.
    # Fix -- cast predicate and subquery to ensure match
    # Fix -- replaced view with in-line SQL
   
    # 1st query without UDF 
    stmt = """prepare xx from select
s_suppkey,
s_name,
s_address,
s_phone,
cast(total_revenue as numeric(18,2))
from
supplier,
(
select
l_suppkey,
sum(l_extendedprice * (1 - l_discount))
from
lineitem
where
l_shipdate >= date '1994-02-01'
and l_shipdate < date '1994-02-01' + interval '3' month
group by
l_suppkey
) as v(supplier_no, total_revenue)
where
s_suppkey = supplier_no
and cast((total_revenue + 0.005) as numeric(18,2)) = (
select
cast((max(total_revenue) + 0.005) as numeric(18,2))
from
(
select
l_suppkey,
sum(l_extendedprice * (1 - l_discount))
from
lineitem
where
l_shipdate >= date '1994-02-01'
and l_shipdate < date '1994-02-01' + interval '3' month
group by
l_suppkey
) as v1(supplier_no, total_revenue)
)
order by
s_suppkey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/A11.exp""", """f1""")
   
    # 2nd query with UDF. Should return the same results as the 1st query. 
    stmt = """prepare xx from select
s_suppkey,
s_name,
s_address,
s_phone,
cast(total_revenue as numeric(18,2))
from
UDF(""" + defs.my_schema + """.qaTmudfGeneral(TABLE(select * from supplier),
'TEST_RUNTIME_EMIT_X_ROWS', '1')),
(
select
l_suppkey,
sum(l_extendedprice * (1 - l_discount))
from
UDF(""" + defs.my_schema + """.qaTmudfGeneral(TABLE(select * from lineitem),
'TEST_RUNTIME_EMIT_X_ROWS', '1'))
where
l_shipdate >= date '1994-02-01'
and l_shipdate < date '1994-02-01' + interval '3' month
group by
l_suppkey
) as v(supplier_no, total_revenue)
where
s_suppkey = supplier_no
and cast((total_revenue + 0.005) as numeric(18,2)) = (
select
cast((max(total_revenue) + 0.005) as numeric(18,2))
from
(
select
l_suppkey,
sum(l_extendedprice * (1 - l_discount))
from
UDF(""" + defs.my_schema + """.qaTmudfGeneral(TABLE(select * from lineitem),
'TEST_RUNTIME_EMIT_X_ROWS', '1'))
where
l_shipdate >= date '1994-02-01'
and l_shipdate < date '1994-02-01' + interval '3' month
group by
l_suppkey
) as v1(supplier_no, total_revenue)
)
order by
s_suppkey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/A11.exp""", """f1""")
    
    _testmgr.testcase_end(desc)

def test013(desc="""Q1"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    stmt = """set schema """ + gvars.tpch2x_schema + """;"""
    output = _dci.cmdexec(stmt)
    
    # ?SECTION Q1
    # TPC-H/TPC-R Pricing Summary Report Query (Q1)
    # Stream 0, Query 1
    # Database -- <catalog>.<schema>
    
    # Summary pricing report for all lineitems as of a given ship date.
    # Expected to scan 95-97% of table.

    # 1st query without UDF
    stmt = """prepare xx from select
l_returnflag,
l_linestatus,
cast(sum(l_quantity)                                   as numeric(18,2)) as sum_qty,
cast(sum(l_extendedprice)                              as numeric(18,2)) as sum_base_price,
cast(sum(l_extendedprice * (1 - l_discount))           as numeric(18,2)) as sum_disc_price,
cast(sum(l_extendedprice * (1 - l_discount)*(1+l_tax)) as numeric(18,2)) as sum_charge,
cast(avg(l_quantity)                                   as numeric(18,3)) as avg_qty,
cast(avg(l_extendedprice)                              as numeric(18,3)) as avg_price,
cast(avg(l_discount)                                   as numeric(18,3)) as avg_disc,
count(*) as count_order
from
lineitem
where
l_shipdate <= date '1998-12-01' - interval '69' day (3)
group by
l_returnflag,
l_linestatus
order by
l_returnflag,
l_linestatus;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/A12.exp""", """f1""")

    # 2nd query with UDF. Should return the same results as the 1st query.    
    stmt = """prepare xx from select
l_returnflag,
l_linestatus,
cast(sum(l_quantity)                                   as numeric(18,2)) as sum_qty,
cast(sum(l_extendedprice)                              as numeric(18,2)) as sum_base_price,
cast(sum(l_extendedprice * (1 - l_discount))           as numeric(18,2)) as sum_disc_price,
cast(sum(l_extendedprice * (1 - l_discount)*(1+l_tax)) as numeric(18,2)) as sum_charge,
cast(avg(l_quantity)                                   as numeric(18,3)) as avg_qty,
cast(avg(l_extendedprice)                              as numeric(18,3)) as avg_price,
cast(avg(l_discount)                                   as numeric(18,3)) as avg_disc,
count(*) as count_order
from
UDF(""" + defs.my_schema + """.qaTmudfGeneral(TABLE(select * from lineitem),
'TEST_RUNTIME_EMIT_X_ROWS', '1'))
where
l_shipdate <= date '1998-12-01' - interval '69' day (3)
group by
l_returnflag,
l_linestatus
order by
l_returnflag,
l_linestatus;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/A12.exp""", """f1""")
    
    _testmgr.testcase_end(desc)

def test014(desc="""Q10"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    stmt = """set schema """ + gvars.tpch2x_schema + """;"""
    output = _dci.cmdexec(stmt)
    
    # ?SECTION Q10
    # TPC-H/TPC-R Returned Item Reporting Query (Q10)
    # Stream 0, Query 10
    # Database -- <catalog>.<schema>
    
    # identifies customers who might be having problems with the parts
    # that are shipped to them (returning them)

    # 1st query without UDF
    stmt = """prepare xx from select
--     [first 20]
c_custkey,
c_name,
cast(sum(l_extendedprice * (1 - l_discount)) as numeric(18,2)) as revenue,
cast(c_acctbal as numeric(18,2)),
n_name,
c_address,
c_phone,
c_comment
from
customer,
orders,
lineitem,
nation
where
c_custkey = o_custkey
and l_orderkey = o_orderkey
and o_orderdate >= date '1994-07-01'
and o_orderdate < date '1994-07-01' + interval '3' month
and l_returnflag = 'R'
and c_nationkey = n_nationkey
group by
c_custkey,
c_name,
c_acctbal,
c_phone,
n_name,
c_address,
c_comment
order by
revenue desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/A13.exp""", """f1""")
   
    # 2nd query with UDF. Should return the same results as the 1st query. 
    stmt = """prepare xx from select
--     [first 20]
c_custkey,
c_name,
cast(sum(l_extendedprice * (1 - l_discount)) as numeric(18,2)) as revenue,
cast(c_acctbal as numeric(18,2)),
n_name,
c_address,
c_phone,
c_comment
from
UDF(""" + defs.my_schema + """.qaTmudfGeneral(TABLE(select * from customer),
'TEST_RUNTIME_EMIT_X_ROWS', '1')),
UDF(""" + defs.my_schema + """.qaTmudfGeneral(TABLE(select * from orders),
'TEST_RUNTIME_EMIT_X_ROWS', '1')),
UDF(""" + defs.my_schema + """.qaTmudfGeneral(TABLE(select * from lineitem),
'TEST_RUNTIME_EMIT_X_ROWS', '1')),
UDF(""" + defs.my_schema + """.qaTmudfGeneral(TABLE(select * from nation),
'TEST_RUNTIME_EMIT_X_ROWS', '1'))
where
c_custkey = o_custkey
and l_orderkey = o_orderkey
and o_orderdate >= date '1994-07-01'
and o_orderdate < date '1994-07-01' + interval '3' month
and l_returnflag = 'R'
and c_nationkey = n_nationkey
group by
c_custkey,
c_name,
c_acctbal,
c_phone,
n_name,
c_address,
c_comment
order by
revenue desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/A13.exp""", """f1""")
    
    _testmgr.testcase_end(desc)

def test015(desc="""Q19"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    stmt = """set schema """ + gvars.tpch2x_schema + """;"""
    output = _dci.cmdexec(stmt)
    
    # ?SECTION Q19
    # TPC-H/TPC-R Discounted Revenue Query (Q19)
    # Stream 0, Query 19
    # Database -- <catalog>.<schema>
    
    # find gross discounted revenue for all orders for three different
    # types of parts that were shipped by air or delivered in person

    # 1st query without UDF
    stmt = """prepare xx from select
cast (sum(l_extendedprice* (1 - l_discount)) as numeric(18,4)) as revenue
from
lineitem,
part
where
(
p_partkey = l_partkey
and p_brand = 'Brand#11'
and p_container in ('SM CASE', 'SM BOX', 'SM PACK', 'SM PKG')
and l_quantity >= 1 and l_quantity <= 1 + 10
and p_size between 1 and 5
and l_shipmode in ('AIR', 'AIR REG')
and l_shipinstruct = 'DELIVER IN PERSON'
)
or
(
p_partkey = l_partkey
and p_brand = 'Brand#22'
and p_container in ('MED BAG', 'MED BOX', 'MED PKG', 'MED PACK')
and l_quantity >= 13 and l_quantity <= 13 + 10
and p_size between 1 and 10
and l_shipmode in ('AIR', 'AIR REG')
and l_shipinstruct = 'DELIVER IN PERSON'
)
or
(
p_partkey = l_partkey
and p_brand = 'Brand#52'
and p_container in ('LG CASE', 'LG BOX', 'LG PACK', 'LG PKG')
and l_quantity >= 21 and l_quantity <= 21 + 10
and p_size between 1 and 15
and l_shipmode in ('AIR', 'AIR REG')
and l_shipinstruct = 'DELIVER IN PERSON'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/A14.exp""", """f1""")
   
    # 2nd query with UDF. Should return the same results as the 1st query. 

    stmt = """prepare xx from select
cast (sum(l_extendedprice* (1 - l_discount)) as numeric(18,4)) as revenue
from
UDF(""" + defs.my_schema + """.qaTmudfGeneral(TABLE(select * from lineitem),
'TEST_RUNTIME_EMIT_X_ROWS', '1')),
UDF(""" + defs.my_schema + """.qaTmudfGeneral(TABLE(select * from part),
'TEST_RUNTIME_EMIT_X_ROWS', '1'))
where
(
p_partkey = l_partkey
and p_brand = 'Brand#11'
and p_container in ('SM CASE', 'SM BOX', 'SM PACK', 'SM PKG')
and l_quantity >= 1 and l_quantity <= 1 + 10
and p_size between 1 and 5
and l_shipmode in ('AIR', 'AIR REG')
and l_shipinstruct = 'DELIVER IN PERSON'
)
or
(
p_partkey = l_partkey
and p_brand = 'Brand#22'
and p_container in ('MED BAG', 'MED BOX', 'MED PKG', 'MED PACK')
and l_quantity >= 13 and l_quantity <= 13 + 10
and p_size between 1 and 10
and l_shipmode in ('AIR', 'AIR REG')
and l_shipinstruct = 'DELIVER IN PERSON'
)
or
(
p_partkey = l_partkey
and p_brand = 'Brand#52'
and p_container in ('LG CASE', 'LG BOX', 'LG PACK', 'LG PKG')
and l_quantity >= 21 and l_quantity <= 21 + 10
and p_size between 1 and 15
and l_shipmode in ('AIR', 'AIR REG')
and l_shipinstruct = 'DELIVER IN PERSON'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/A14.exp""", """f1""")
    
    _testmgr.testcase_end(desc)

def test016(desc="""Q5"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    stmt = """set schema """ + gvars.tpch2x_schema + """;"""
    output = _dci.cmdexec(stmt)
    
    # ?SECTION Q5
    # TPC-H/TPC-R Local Supplier Volume Query (Q5)
    # Stream 0, Query 5
    # Database -- <catalog>.<schema>
    
    # For each nation in a region, list the revenue resulting from
    # lineitem transactions in which the customer ordering parts and the
    # supplier filling them were both within that nation. Only parts
    # ordered in a given year are considered.  Ordered by revenue.

    # 1st query without UDF
    stmt = """prepare xx from select
n_name,
cast(sum(l_extendedprice * (1 - l_discount)) as numeric(18,2)) as revenue
from
customer,
orders,
lineitem,
supplier,
nation,
region
where
c_custkey = o_custkey
and l_orderkey = o_orderkey
and l_suppkey = s_suppkey
and c_nationkey = s_nationkey
and s_nationkey = n_nationkey
and n_regionkey = r_regionkey
and r_name = 'ASIA'
and o_orderdate >= date '1997-01-01'
and o_orderdate < date '1997-01-01' + interval '1' year
group by
n_name
order by
revenue desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/A15.exp""", """f1""")
   
    # 2nd query with UDF. Should return the same results as the 1st query. 
    stmt = """prepare xx from select
n_name,
cast(sum(l_extendedprice * (1 - l_discount)) as numeric(18,2)) as revenue
from
UDF(""" + defs.my_schema + """.qaTmudfGeneral(TABLE(select * from customer),
'TEST_RUNTIME_EMIT_X_ROWS', '1')),
UDF(""" + defs.my_schema + """.qaTmudfGeneral(TABLE(select * from orders),
'TEST_RUNTIME_EMIT_X_ROWS', '1')),
UDF(""" + defs.my_schema + """.qaTmudfGeneral(TABLE(select * from lineitem),
'TEST_RUNTIME_EMIT_X_ROWS', '1')),
UDF(""" + defs.my_schema + """.qaTmudfGeneral(TABLE(select * from supplier),
'TEST_RUNTIME_EMIT_X_ROWS', '1')),
UDF(""" + defs.my_schema + """.qaTmudfGeneral(TABLE(select * from nation),
'TEST_RUNTIME_EMIT_X_ROWS', '1')),
UDF(""" + defs.my_schema + """.qaTmudfGeneral(TABLE(select * from region),
'TEST_RUNTIME_EMIT_X_ROWS', '1'))
where
c_custkey = o_custkey
and l_orderkey = o_orderkey
and l_suppkey = s_suppkey
and c_nationkey = s_nationkey
and s_nationkey = n_nationkey
and n_regionkey = r_regionkey
and r_name = 'ASIA'
and o_orderdate >= date '1997-01-01'
and o_orderdate < date '1997-01-01' + interval '1' year
group by
n_name
order by
revenue desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/A15.exp""", """f1""")
    
    _testmgr.testcase_end(desc)

def test017(desc="""Q7"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    stmt = """set schema """ + gvars.tpch2x_schema + """;"""
    output = _dci.cmdexec(stmt)
    
    # ?SECTION Q7
    # TPC-H/TPC-R Volume Shipping Query (Q7)
    # Stream 0, Query 7
    # Database -- <catalog>.<schema>
    
    # for two given nations, find the gross discounted revenues derived
    # from lineitems in which parts were shipped from a supplier in
    # either nation to a customer in the other nation during 1995 and
    # 1996.  Order by supplier nation, customer nation, and year.

    # 1st query without UDF
    stmt = """prepare xx from select
supp_nation,
cust_nation,
l_year,
cast(sum(volume) as numeric(18,2)) as revenue
from
(
select
n1.n_name as supp_nation,
n2.n_name as cust_nation,
extract(year from l_shipdate) as l_year,
l_extendedprice * (1 - l_discount) as volume
from
supplier,
lineitem,
orders,
customer,
nation n1,
nation n2
where
s_suppkey = l_suppkey
and o_orderkey = l_orderkey
and c_custkey = o_custkey
and s_nationkey = n1.n_nationkey
and c_nationkey = n2.n_nationkey
and (
(n1.n_name = 'ETHIOPIA' and n2.n_name = 'JORDAN')
or (n1.n_name = 'JORDAN' and n2.n_name = 'ETHIOPIA')
)
and l_shipdate between date '1995-01-01' and date '1996-12-31'
) as shipping
group by
supp_nation,
cust_nation,
l_year
order by
supp_nation,
cust_nation,
l_year;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/A16.exp""", """f1""")
   
    # 2nd query with UDF. Should return the same results as the 1st query. 
    stmt = """prepare xx from select
supp_nation,
cust_nation,
l_year,
cast(sum(volume) as numeric(18,2)) as revenue
from
(
select
n1.n_name as supp_nation,
n2.n_name as cust_nation,
extract(year from l_shipdate) as l_year,
l_extendedprice * (1 - l_discount) as volume
from
UDF(""" + defs.my_schema + """.qaTmudfGeneral(TABLE(select * from supplier),
'TEST_RUNTIME_EMIT_X_ROWS', '1')),
UDF(""" + defs.my_schema + """.qaTmudfGeneral(TABLE(select * from lineitem),
'TEST_RUNTIME_EMIT_X_ROWS', '1')),
UDF(""" + defs.my_schema + """.qaTmudfGeneral(TABLE(select * from orders),
'TEST_RUNTIME_EMIT_X_ROWS', '1')),
UDF(""" + defs.my_schema + """.qaTmudfGeneral(TABLE(select * from customer),
'TEST_RUNTIME_EMIT_X_ROWS', '1')),
UDF(""" + defs.my_schema + """.qaTmudfGeneral(TABLE(select * from nation),
'TEST_RUNTIME_EMIT_X_ROWS', '1')) n1,
UDF(""" + defs.my_schema + """.qaTmudfGeneral(TABLE(select * from nation),
'TEST_RUNTIME_EMIT_X_ROWS', '1')) n2
where
s_suppkey = l_suppkey
and o_orderkey = l_orderkey
and c_custkey = o_custkey
and s_nationkey = n1.n_nationkey
and c_nationkey = n2.n_nationkey
and (
(n1.n_name = 'ETHIOPIA' and n2.n_name = 'JORDAN')
or (n1.n_name = 'JORDAN' and n2.n_name = 'ETHIOPIA')
)
and l_shipdate between date '1995-01-01' and date '1996-12-31'
) as shipping
group by
supp_nation,
cust_nation,
l_year
order by
supp_nation,
cust_nation,
l_year;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/A16.exp""", """f1""")
    
    _testmgr.testcase_end(desc)

def test018(desc="""Q12"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    stmt = """set schema """ + gvars.tpch2x_schema + """;"""
    output = _dci.cmdexec(stmt)
    
    # ?SECTION Q12
    # TPC-H/TPC-R Shipping Modes and Order Priority Query (Q12)
    # Stream 0, Query 12
    # Database -- <catalog>.<schema>
    
    # determines whether less expensive shipping modes are negatively
    # affecting critical priority orders

    # 1st query without UDF
    stmt = """prepare xx from select
l_shipmode,
sum(case
when o_orderpriority = '1-URGENT'
or o_orderpriority = '2-HIGH'
then 1
else 0
end) as high_line_count,
sum(case
when o_orderpriority <> '1-URGENT'
and o_orderpriority <> '2-HIGH'
then 1
else 0
end) as low_line_count
from
orders,
lineitem
where
o_orderkey = l_orderkey
and l_shipmode in ('REG AIR', 'AIR')
and l_commitdate < l_receiptdate
and l_shipdate < l_commitdate
and l_receiptdate >= date '1995-01-01'
and l_receiptdate < date '1995-01-01' + interval '1' year
group by
l_shipmode
order by
l_shipmode;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/A17.exp""", """f1""")
   
    # 2nd query with UDF. Should return the same results as the 1st query. 
    stmt = """prepare xx from select
l_shipmode,
sum(case
when o_orderpriority = '1-URGENT'
or o_orderpriority = '2-HIGH'
then 1
else 0
end) as high_line_count,
sum(case
when o_orderpriority <> '1-URGENT'
and o_orderpriority <> '2-HIGH'
then 1
else 0
end) as low_line_count
from
UDF(""" + defs.my_schema + """.qaTmudfGeneral(TABLE(select * from orders),
'TEST_RUNTIME_EMIT_X_ROWS', '1')),
UDF(""" + defs.my_schema + """.qaTmudfGeneral(TABLE(select * from lineitem),
'TEST_RUNTIME_EMIT_X_ROWS', '1'))
where
o_orderkey = l_orderkey
and l_shipmode in ('REG AIR', 'AIR')
and l_commitdate < l_receiptdate
and l_shipdate < l_commitdate
and l_receiptdate >= date '1995-01-01'
and l_receiptdate < date '1995-01-01' + interval '1' year
group by
l_shipmode
order by
l_shipmode;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/A17.exp""", """f1""")
    
    _testmgr.testcase_end(desc)

