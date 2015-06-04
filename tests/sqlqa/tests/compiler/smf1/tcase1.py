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
    
    stmt = """set param ?curr_model 'T1';"""
    output = _dci.cmdexec(stmt)

def test001(desc="""PH Baseline without sort multiblock"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    stmt = """set param ?q 1;"""
    output = _dci.cmdexec(stmt)
    
    #set showshape on;
    # 2X rowcount 4
    
    # Summary pricing report for all lineitems as of a given ship date.
    # Expected to scan 95-97% of table.
    
    stmt = """prepare xx from
select
l_returnflag,
l_linestatus,
cast(sum(l_quantity)
as numeric(18,2)) as sum_qty,
cast(sum(l_extendedprice)
as numeric(18,2)) as sum_base_price,
cast(sum(l_extendedprice * (1 - l_discount))
as numeric(18,2)) as sum_disc_price,
cast(sum(l_extendedprice * (1 - l_discount)*(1+l_tax))
as numeric(18,2)) as sum_charge,
cast(avg(l_quantity)
as numeric(18,3)) as avg_qty,
cast(avg(l_extendedprice)
as numeric(18,3)) as avg_price,
cast(avg(l_discount)
as numeric(18,3)) as avg_disc,
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
    
    #set showshape off;
    
    stmt = """log """ + defs.work_dir + """/dslog clear;"""
    output = _dci.cmdexec(stmt)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    stmt = """log off;"""
    output = _dci.cmdexec(stmt)
    
    defs.et = _testmgr.shell_call("""grep "Compile Time" """ + defs.work_dir + """/dslog | awk ' { print $3 } '""").strip()
    
    stmt = """execute save_plan;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into """ + defs.my_schema + """.timetable (query,cardinal,T1_cost,T1_cmp_time)
(select ?q,cardinality,total_cost, time '""" + defs.et + """' from table(explain(NULL,'XX'))
where operator = 'ROOT');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/A100.RESULT""", 'ph1')
    
    ##expectstat $test_dir/A100.$MODEL ex1a
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """log """ + defs.work_dir + """/dslog clear;"""
    output = _dci.cmdexec(stmt)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    stmt = """log off;"""
    output = _dci.cmdexec(stmt)
    
    defs.et = _testmgr.shell_call("""grep "Elapsed Time" """ + defs.work_dir + """/dslog | awk ' { print $3 } '""").strip()
    
    stmt = """update """ + defs.my_schema + """.timetable set T1_time = time '""" + defs.et + """'
where query = ?q;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    ##endtestcase
    
    ##testcase O2 PH Query 2
    #set showshape on;
    stmt = """set param ?q 2;"""
    output = _dci.cmdexec(stmt)
    
    #set showshape on;
    # 2X rowcount = 955
    # Database -- <catalog>.<schema>
    
    # For a given region, find the supplier who can supply a part
    # type and size at least cost.
    
    stmt = """prepare xx from
select
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
    
    #set showshape off;
    
    stmt = """log """ + defs.work_dir + """/dslog clear;"""
    output = _dci.cmdexec(stmt)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    stmt = """log off;"""
    output = _dci.cmdexec(stmt)
    
    defs.et = _testmgr.shell_call("""grep "Compile Time" """ + defs.work_dir + """/dslog | awk ' { print $3 } '""").strip()
    
    stmt = """execute save_plan;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into """ + defs.my_schema + """.timetable (query,cardinal,T1_cost,T1_cmp_time)
(select ?q,cardinality,total_cost, time '""" + defs.et + """' from table(explain(NULL,'XX'))
where operator = 'ROOT');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/A100.RESULT""", 'ph2')
    
    ##expectstat $test_dir/A100.$MODEL ex2a
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """log """ + defs.work_dir + """/dslog clear;"""
    output = _dci.cmdexec(stmt)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    stmt = """log off;"""
    output = _dci.cmdexec(stmt)
    
    defs.et = _testmgr.shell_call("""grep "Elapsed Time" """ + defs.work_dir + """/dslog | awk ' { print $3 } '""").strip()
    
    stmt = """update """ + defs.my_schema + """.timetable set T1_time = time '""" + defs.et + """'
where query = ?q;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    ##endtestcase
    
    ##testcase O3 PH query 3
    stmt = """set param ?q 3;"""
    output = _dci.cmdexec(stmt)
    
    #set showshape on;
    # TPC-H/TPC-R Shipping Priority Query (Q3)
    # 2X rowcount = 22518
    # Database -- <catalog>.<schema>
    
    # retrieves the shipping priority and potential revenue of orders
    # having the largest revenue among those that had not been shipped
    # as of a given date.
    
    stmt = """prepare xx from
select [first 300]
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
    
    #set showshape off;
    
    stmt = """log """ + defs.work_dir + """/dslog clear;"""
    output = _dci.cmdexec(stmt)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    stmt = """log off;"""
    output = _dci.cmdexec(stmt)
    
    defs.et = _testmgr.shell_call("""grep "Compile Time" """ + defs.work_dir + """/dslog | awk ' { print $3 } '""").strip()
    
    stmt = """execute save_plan;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into """ + defs.my_schema + """.timetable (query,cardinal,T1_cost,T1_cmp_time)
(select ?q,cardinality,total_cost, time '""" + defs.et + """' from table(explain(NULL,'XX'))
where operator = 'ROOT');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/A100.RESULT""", 'ph3')
    ##expectstat $test_dir/A100.$MODEL ex3a
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """log """ + defs.work_dir + """/dslog clear;"""
    output = _dci.cmdexec(stmt)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    stmt = """log off;"""
    output = _dci.cmdexec(stmt)
    
    defs.et = _testmgr.shell_call("""grep "Elapsed Time" """ + defs.work_dir + """/dslog | awk ' { print $3 } '""").strip()
    
    stmt = """update """ + defs.my_schema + """.timetable set T1_time = time '""" + defs.et + """'
where query = ?q;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    ##endtestcase
    
    ##testcase O4 PH Query 4
    #set showshape on;
    stmt = """set param ?q 4;"""
    output = _dci.cmdexec(stmt)
    
    #set showshape on;
    # TPC-H/TPC-R Order Priority Checking Query (Q4)
    # 2X rowcount = 5
    # Database -- <catalog>.<schema>
    
    # counts the number of orders ordered in a given quarter of a given
    # year in which at least at least one lineitem was received later
    # than its committed date. The query lists the count of such orders
    # for each order priority sorted in ascending priority order.
    
    stmt = """prepare xx from
select
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
    
    #set showshape off;
    
    stmt = """log """ + defs.work_dir + """/dslog clear;"""
    output = _dci.cmdexec(stmt)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    stmt = """log off;"""
    output = _dci.cmdexec(stmt)
    
    defs.et = _testmgr.shell_call("""grep "Compile Time" """ + defs.work_dir + """/dslog | awk ' { print $3 } '""").strip()
    
    stmt = """execute save_plan;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into """ + defs.my_schema + """.timetable (query,cardinal,T1_cost,T1_cmp_time)
(select ?q,cardinality,total_cost, time '""" + defs.et + """' from table(explain(NULL,'XX'))
where operator = 'ROOT');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/A100.RESULT""", 'ph4')
    
    ##expectstat $test_dir/A100.$MODEL ex4a
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """log """ + defs.work_dir + """/dslog clear;"""
    output = _dci.cmdexec(stmt)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    stmt = """log off;"""
    output = _dci.cmdexec(stmt)
    
    defs.et = _testmgr.shell_call("""grep "Elapsed Time" """ + defs.work_dir + """/dslog | awk ' { print $3 } '""").strip()
    
    stmt = """update """ + defs.my_schema + """.timetable set T1_time = time '""" + defs.et + """'
where query = ?q;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    ##endtestcase
    
    ##testcase O5 PH query 5
    
    stmt = """set param ?q 5;"""
    output = _dci.cmdexec(stmt)
    
    #set showshape on;
    # TPC-H/TPC-R Local Supplier Volume Query (Q5)
    # 2X rowcount = 5
    # Database -- <catalog>.<schema>
    
    # For each nation in a region, list the revenue resulting from
    # lineitem transactions in which the customer ordering parts and the
    # supplier filling them were both within that nation. Only parts
    # ordered in a given year are considered.  Ordered by revenue.
    
    stmt = """prepare xx from
select
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
    
    #set showshape off;
    
    stmt = """log """ + defs.work_dir + """/dslog clear;"""
    output = _dci.cmdexec(stmt)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    stmt = """log off;"""
    output = _dci.cmdexec(stmt)
    
    defs.et = _testmgr.shell_call("""grep "Compile Time" """ + defs.work_dir + """/dslog | awk ' { print $3 } '""").strip()
    
    stmt = """execute save_plan;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into """ + defs.my_schema + """.timetable (query,cardinal,T1_cost,T1_cmp_time)
(select ?q,cardinality,total_cost, time '""" + defs.et + """' from table(explain(NULL,'XX'))
where operator = 'ROOT');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/A100.RESULT""", 'ph5')
    ##expectstat $test_dir/A100.$MODEL ex5a
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """log """ + defs.work_dir + """/dslog clear;"""
    output = _dci.cmdexec(stmt)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    stmt = """log off;"""
    output = _dci.cmdexec(stmt)
    
    defs.et = _testmgr.shell_call("""grep "Elapsed Time" """ + defs.work_dir + """/dslog | awk ' { print $3 } '""").strip()
    
    stmt = """update """ + defs.my_schema + """.timetable set T1_time = time '""" + defs.et + """'
where query = ?q;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    ##endtestcase
    ##testcase O6 PH Query 6
    #set showshape on;
    stmt = """set param ?q 6;"""
    output = _dci.cmdexec(stmt)
    
    #set showshape on;
    # TPC-H/TPC-R Forecasting Revenue Change Query (Q6)
    # 2X rowcount = 1
    # Database -- <catalog>.<schema>
    
    # consider all lineitems shipped in a given year with discounts
    # within a specified range.  Lists the amount by which the total revenue
    # would have increased if these discounts had been eliminated.
    
    stmt = """prepare xx from
select
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
    
    #set showshape off;
    
    stmt = """log """ + defs.work_dir + """/dslog clear;"""
    output = _dci.cmdexec(stmt)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    stmt = """log off;"""
    output = _dci.cmdexec(stmt)
    
    defs.et = _testmgr.shell_call("""grep "Compile Time" """ + defs.work_dir + """/dslog | awk ' { print $3 } '""").strip()
    
    stmt = """execute save_plan;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into """ + defs.my_schema + """.timetable (query,cardinal,T1_cost,T1_cmp_time)
(select ?q,cardinality,total_cost, time '""" + defs.et + """' from table(explain(NULL,'XX'))
where operator = 'ROOT');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/A100.RESULT""", 'ph6')
    
    ##expectstat $test_dir/A100.$MODEL ex6a
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """log """ + defs.work_dir + """/dslog clear;"""
    output = _dci.cmdexec(stmt)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    stmt = """log off;"""
    output = _dci.cmdexec(stmt)
    
    defs.et = _testmgr.shell_call("""grep "Elapsed Time" """ + defs.work_dir + """/dslog | awk ' { print $3 } '""").strip()
    
    stmt = """update """ + defs.my_schema + """.timetable set T1_time = time '""" + defs.et + """'
where query = ?q;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    ##endtestcase
    ##testcase O7 PH query 7
    stmt = """set param ?q 7;"""
    output = _dci.cmdexec(stmt)
    
    #set showshape on;
    # TPC-H/TPC-R Volume Shipping Query (Q7)
    # 2X rowcount = 4
    # Database -- <catalog>.<schema>
    
    # for two given nations, find the gross discounted revenues derived
    # from lineitems in which parts were shipped from a supplier in
    # either nation to a customer in the other nation during 1995 and
    # 1996.  Order by supplier nation, customer nation, and year.
    
    stmt = """prepare xx from
select
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
and l_shipdate between
date '1995-01-01' and date '1996-12-31'
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
    
    #set showshape off;
    
    stmt = """log """ + defs.work_dir + """/dslog clear;"""
    output = _dci.cmdexec(stmt)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    stmt = """log off;"""
    output = _dci.cmdexec(stmt)
    
    defs.et = _testmgr.shell_call("""grep "Compile Time" """ + defs.work_dir + """/dslog | awk ' { print $3 } '""").strip()
    
    stmt = """execute save_plan;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into """ + defs.my_schema + """.timetable (query,cardinal,T1_cost,T1_cmp_time)
(select ?q,cardinality,total_cost, time '""" + defs.et + """' from table(explain(NULL,'XX'))
where operator = 'ROOT');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/A100.RESULT""", 'ph7')
    
    ##expectstat $test_dir/A100.$MODEL ex7a
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """log """ + defs.work_dir + """/dslog clear;"""
    output = _dci.cmdexec(stmt)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    stmt = """log off;"""
    output = _dci.cmdexec(stmt)
    
    defs.et = _testmgr.shell_call("""grep "Elapsed Time" """ + defs.work_dir + """/dslog | awk ' { print $3 } '""").strip()
    
    stmt = """update """ + defs.my_schema + """.timetable set T1_time = time '""" + defs.et + """'
where query = ?q;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    ##endtestcase
    ##testcase O8 PH Query 8
    stmt = """set param ?q 8;"""
    output = _dci.cmdexec(stmt)
    
    #set showshape on;
    # TPC-H/TPC-R National Market Share Query (Q8)
    # 2X rowcount = 2
    # Database -- <catalog>.<schema>
    
    # determines how the market share of a given nation in a given
    # region has changed over two years for a given part type. Market
    # share is the fraction of the revenue from products of a given type
    # that was generated by suppliers from the given nation.
    
    stmt = """prepare xx from
select
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
and o_orderdate between
date '1995-01-01' and date '1996-12-31'
and p_type = 'LARGE ANODIZED COPPER'
) as all_nations
group by
o_year
order by
o_year;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #set showshape off;
    
    stmt = """log """ + defs.work_dir + """/dslog clear;"""
    output = _dci.cmdexec(stmt)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    stmt = """log off;"""
    output = _dci.cmdexec(stmt)
    
    defs.et = _testmgr.shell_call("""grep "Compile Time" """ + defs.work_dir + """/dslog | awk ' { print $3 } '""").strip()
    
    stmt = """execute save_plan;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into """ + defs.my_schema + """.timetable (query,cardinal,T1_cost,T1_cmp_time)
(select ?q,cardinality,total_cost, time '""" + defs.et + """' from table(explain(NULL,'XX'))
where operator = 'ROOT');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/A100.RESULT""", 'ph8')
    
    ##expectstat $test_dir/A100.$MODEL ex8a
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """log """ + defs.work_dir + """/dslog clear;"""
    output = _dci.cmdexec(stmt)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    stmt = """log off;"""
    output = _dci.cmdexec(stmt)
    
    defs.et = _testmgr.shell_call("""grep "Elapsed Time" """ + defs.work_dir + """/dslog | awk ' { print $3 } '""").strip()
    
    stmt = """update """ + defs.my_schema + """.timetable set T1_time = time '""" + defs.et + """'
where query = ?q;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    ##endtestcase
    ##testcase O9 PH Query 9
    stmt = """set param ?q 9;"""
    output = _dci.cmdexec(stmt)
    
    #set showshape on;
    # TPC-H/TPC-R Product Type Profit Measure Query (Q9)
    # 2X rowcount = 175
    # Database -- <catalog>.<schema>
    
    # determine how much profit is made on a line of
    # parts, broken out by supplier nation and year.
    
    stmt = """prepare xx from
select
nation,
o_year,
cast(sum(amount) as numeric(18,2)) as sum_profit
from
(
select
n_name as nation,
extract(year from o_orderdate) as o_year,
l_extendedprice * (1 - l_discount) - ps_supplycost
* l_quantity as amount
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
    
    #set showshape off;
    
    stmt = """log """ + defs.work_dir + """/dslog clear;"""
    output = _dci.cmdexec(stmt)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    stmt = """log off;"""
    output = _dci.cmdexec(stmt)
    
    defs.et = _testmgr.shell_call("""grep "Compile Time" """ + defs.work_dir + """/dslog | awk ' { print $3 } '""").strip()
    
    stmt = """execute save_plan;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into """ + defs.my_schema + """.timetable (query,cardinal,T1_cost,T1_cmp_time)
(select ?q,cardinality,total_cost, time '""" + defs.et + """' from table(explain(NULL,'XX'))
where operator = 'ROOT');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/A100.RESULT""", 'ph9')
    
    ##expectstat $test_dir/A100.$MODEL ex9a
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """log """ + defs.work_dir + """/dslog clear;"""
    output = _dci.cmdexec(stmt)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    stmt = """log off;"""
    output = _dci.cmdexec(stmt)
    
    defs.et = _testmgr.shell_call("""grep "Elapsed Time" """ + defs.work_dir + """/dslog | awk ' { print $3 } '""").strip()
    
    stmt = """update """ + defs.my_schema + """.timetable set T1_time = time '""" + defs.et + """'
where query = ?q;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    ##endtestcase
    ##testcase PH10 Query 10
    stmt = """set param ?q 10;"""
    output = _dci.cmdexec(stmt)
    
    #set showshape on;
    # TPC-H/TPC-R Returned Item Reporting Query (Q10)
    # 2X rowcount 76335
    # Database -- <catalog>.<schema>
    
    # identifies customers who might be having problems with the parts
    # that are shipped to them (returning them)
    
    stmt = """prepare xx from
select [first 100]
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
    
    #set showshape off;
    
    stmt = """log """ + defs.work_dir + """/dslog clear;"""
    output = _dci.cmdexec(stmt)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    stmt = """log off;"""
    output = _dci.cmdexec(stmt)
    
    defs.et = _testmgr.shell_call("""grep "Compile Time" """ + defs.work_dir + """/dslog | awk ' { print $3 } '""").strip()
    
    stmt = """execute save_plan;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into """ + defs.my_schema + """.timetable (query,cardinal,T1_cost,T1_cmp_time)
(select ?q,cardinality,total_cost, time '""" + defs.et + """' from table(explain(NULL,'XX'))
where operator = 'ROOT');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/A100.RESULT""", 'ph10')
    
    ##expectstat $test_dir/A100.$MODEL ex10a
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """log """ + defs.work_dir + """/dslog clear;"""
    output = _dci.cmdexec(stmt)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    stmt = """log off;"""
    output = _dci.cmdexec(stmt)
    
    defs.et = _testmgr.shell_call("""grep "Elapsed Time" """ + defs.work_dir + """/dslog | awk ' { print $3 } '""").strip()
    
    stmt = """update """ + defs.my_schema + """.timetable set T1_time = time '""" + defs.et + """'
where query = ?q;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    ##endtestcase
    ##testcase PH11 PH Query 11
    stmt = """set param ?q 11;"""
    output = _dci.cmdexec(stmt)
    
    #set showshape on;
    # 2X rowcount 57045
    # Database -- <catalog>.<schema>
    
    # find, for suppliers in a given nation, all the parts that represent
    # a significant percentage of the total value of all available parts
    
    stmt = """prepare xx from
select [first 100]
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
sum(ps_supplycost * ps_availqty) * 0.0000002500
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
    
    #set showshape off;
    
    stmt = """log """ + defs.work_dir + """/dslog clear;"""
    output = _dci.cmdexec(stmt)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    stmt = """log off;"""
    output = _dci.cmdexec(stmt)
    
    defs.et = _testmgr.shell_call("""grep "Compile Time" """ + defs.work_dir + """/dslog | awk ' { print $3 } '""").strip()
    
    stmt = """execute save_plan;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into """ + defs.my_schema + """.timetable (query,cardinal,T1_cost,T1_cmp_time)
(select ?q,cardinality,total_cost, time '""" + defs.et + """' from table(explain(NULL,'XX'))
where operator = 'ROOT');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/A100.RESULT""", 'ph11')
    
    ##expectstat $test_dir/A100.$MODEL ex11a
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """log """ + defs.work_dir + """/dslog clear;"""
    output = _dci.cmdexec(stmt)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    stmt = """log off;"""
    output = _dci.cmdexec(stmt)
    
    defs.et = _testmgr.shell_call("""grep "Elapsed Time" """ + defs.work_dir + """/dslog | awk ' { print $3 } '""").strip()
    
    stmt = """update """ + defs.my_schema + """.timetable set T1_time = time '""" + defs.et + """'
where query = ?q;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    ##endtestcase
    ##testcase PH12 PH Query 12
    stmt = """set param ?q 12;"""
    output = _dci.cmdexec(stmt)
    
    #set showshape on;
    # TPC-H/TPC-R Shipping Modes and Order Priority Query (Q12)
    # 2X rowcount 2
    # Database -- <catalog>.<schema>
    
    # determines whether less expensive shipping modes are negatively
    # affecting critical priority orders
    
    stmt = """prepare xx from
select
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
    
    #set showshape off;
    
    stmt = """log """ + defs.work_dir + """/dslog clear;"""
    output = _dci.cmdexec(stmt)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    stmt = """log off;"""
    output = _dci.cmdexec(stmt)
    
    defs.et = _testmgr.shell_call("""grep "Compile Time" """ + defs.work_dir + """/dslog | awk ' { print $3 } '""").strip()
    
    stmt = """execute save_plan;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into """ + defs.my_schema + """.timetable (query,cardinal,T1_cost,T1_cmp_time)
(select ?q,cardinality,total_cost, time '""" + defs.et + """' from table(explain(NULL,'XX'))
where operator = 'ROOT');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/A100.RESULT""", 'ph12')
    
    ##expectstat $test_dir/A100.$MODEL ex12a
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """log """ + defs.work_dir + """/dslog clear;"""
    output = _dci.cmdexec(stmt)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    stmt = """log off;"""
    output = _dci.cmdexec(stmt)
    
    defs.et = _testmgr.shell_call("""grep "Elapsed Time" """ + defs.work_dir + """/dslog | awk ' { print $3 } '""").strip()
    
    stmt = """update """ + defs.my_schema + """.timetable set T1_time = time '""" + defs.et + """'
where query = ?q;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    ##endtestcase
    ##testcase PH13 PH Query 13
    stmt = """set param ?q 13;"""
    output = _dci.cmdexec(stmt)
    
    #set showshape on;
    # TPC-H/TPC-R Customer Distribution Query (Q13)
    # 2X rowcount = 2
    # Database -- <catalog>.<schema>
    
    # determines the distribution of customers by the number of orders
    # they have made, including customers who have no record of orders,
    # past or present. Counts and reports how many customers have no
    # orders, how many have 1, 2, 3, etc. A check is made to ensure that
    # the orders counted do not fall into one of several special categories
    # of orders. Special categories are identified in the order comment
    # column by looking for a particular pattern.
    
    stmt = """prepare xx from
select
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
and o_orderdate between
date '1995-01-01' and date '1996-12-31'
and p_type = 'LARGE ANODIZED COPPER'
) as all_nations
group by
o_year
order by
o_year;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #set showshape off;
    
    stmt = """log """ + defs.work_dir + """/dslog clear;"""
    output = _dci.cmdexec(stmt)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    stmt = """log off;"""
    output = _dci.cmdexec(stmt)
    
    defs.et = _testmgr.shell_call("""grep "Compile Time" """ + defs.work_dir + """/dslog | awk ' { print $3 } '""").strip()
    
    stmt = """execute save_plan;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into """ + defs.my_schema + """.timetable (query,cardinal,T1_cost,T1_cmp_time)
(select ?q,cardinality,total_cost, time '""" + defs.et + """' from table(explain(NULL,'XX'))
where operator = 'ROOT');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/A100.RESULT""", 'ph13')
    
    ##expectstat $test_dir/A100.$MODEL ex13a
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """log """ + defs.work_dir + """/dslog clear;"""
    output = _dci.cmdexec(stmt)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    stmt = """log off;"""
    output = _dci.cmdexec(stmt)
    
    defs.et = _testmgr.shell_call("""grep "Elapsed Time" """ + defs.work_dir + """/dslog | awk ' { print $3 } '""").strip()
    
    stmt = """update """ + defs.my_schema + """.timetable set T1_time = time '""" + defs.et + """'
where query = ?q;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    ##endtestcase
    ##testcase PH14 PH Query 14
    stmt = """set param ?q 14;"""
    output = _dci.cmdexec(stmt)
    
    #set showshape on;
    # TPC TPC-H Parameter Substitution (Version 2.3.1 build 2)
    # TPC-H/TPC-R Promotion Effect Query (Q14)
    # 2X rowcount = 1
    # Database -- <catalog>.<schema>
    
    # determine what % of revenue in a given year & month was derived
    # from promotional parts shipped in a given month.
    
    stmt = """prepare xx from
select
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
    
    #set showshape off;
    
    stmt = """log """ + defs.work_dir + """/dslog clear;"""
    output = _dci.cmdexec(stmt)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    stmt = """log off;"""
    output = _dci.cmdexec(stmt)
    
    defs.et = _testmgr.shell_call("""grep "Compile Time" """ + defs.work_dir + """/dslog | awk ' { print $3 } '""").strip()
    
    stmt = """execute save_plan;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into """ + defs.my_schema + """.timetable (query,cardinal,T1_cost,T1_cmp_time)
(select ?q,cardinality,total_cost, time '""" + defs.et + """' from table(explain(NULL,'XX'))
where operator = 'ROOT');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/A100.RESULT""", 'ph14')
    
    ##expectstat $test_dir/A100.$MODEL ex14a
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """log """ + defs.work_dir + """/dslog clear;"""
    output = _dci.cmdexec(stmt)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    stmt = """log off;"""
    output = _dci.cmdexec(stmt)
    
    defs.et = _testmgr.shell_call("""grep "Elapsed Time" """ + defs.work_dir + """/dslog | awk ' { print $3 } '""").strip()
    
    stmt = """update """ + defs.my_schema + """.timetable set T1_time = time '""" + defs.et + """'
where query = ?q;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    ##endtestcase
    ##testcase PH15 PH Query 15
    stmt = """set param ?q 15;"""
    output = _dci.cmdexec(stmt)
    
    #set showshape on;
    # TPC-H/TPC-R Top Supplier Query (Q15)
    # 2X rowcount = 1
    # Database -- <catalog>.<schema>
    
    # determines supplier who contributed most to the overall revenue
    # for parts shipped during a given quarter of a given year.
    
    stmt = """prepare xx from
select
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
    
    #set showshape off;
    
    stmt = """log """ + defs.work_dir + """/dslog clear;"""
    output = _dci.cmdexec(stmt)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    stmt = """log off;"""
    output = _dci.cmdexec(stmt)
    
    defs.et = _testmgr.shell_call("""grep "Compile Time" """ + defs.work_dir + """/dslog | awk ' { print $3 } '""").strip()
    
    stmt = """execute save_plan;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into """ + defs.my_schema + """.timetable (query,cardinal,T1_cost,T1_cmp_time)
(select ?q,cardinality,total_cost, time '""" + defs.et + """' from table(explain(NULL,'XX'))
where operator = 'ROOT');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/A100.RESULT""", 'ph15')
    
    ##expectstat $test_dir/A100.$MODEL ex15a
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """log """ + defs.work_dir + """/dslog clear;"""
    output = _dci.cmdexec(stmt)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    stmt = """log off;"""
    output = _dci.cmdexec(stmt)
    
    defs.et = _testmgr.shell_call("""grep "Elapsed Time" """ + defs.work_dir + """/dslog | awk ' { print $3 } '""").strip()
    
    stmt = """update """ + defs.my_schema + """.timetable set T1_time = time '""" + defs.et + """'
where query = ?q;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    ##endtestcase
    ##testcase PH16 PH Query 16
    stmt = """set param ?q 16;"""
    output = _dci.cmdexec(stmt)
    
    #set showshape on;
    # TPC-H/TPC-R Parts/Supplier Relationship Query (Q16)
    # 2X rowcount = 24521
    # Database -- <catalog>.<schema>
    
    # count the number of suppliers who can supply parts that satisfy a
    # particular customer's requirements
    
    stmt = """prepare xx from
select [first 200]
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
    
    #set showshape off;
    
    stmt = """log """ + defs.work_dir + """/dslog clear;"""
    output = _dci.cmdexec(stmt)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    stmt = """log off;"""
    output = _dci.cmdexec(stmt)
    
    defs.et = _testmgr.shell_call("""grep "Compile Time" """ + defs.work_dir + """/dslog | awk ' { print $3 } '""").strip()
    
    stmt = """execute save_plan;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into """ + defs.my_schema + """.timetable (query,cardinal,T1_cost,T1_cmp_time)
(select ?q,cardinality,total_cost, time '""" + defs.et + """' from table(explain(NULL,'XX'))
where operator = 'ROOT');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/A100.RESULT""", 'ph16')
    
    ##expectstat $test_dir/A100.$MODEL ex16a
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """log """ + defs.work_dir + """/dslog clear;"""
    output = _dci.cmdexec(stmt)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    stmt = """log off;"""
    output = _dci.cmdexec(stmt)
    
    defs.et = _testmgr.shell_call("""grep "Elapsed Time" """ + defs.work_dir + """/dslog | awk ' { print $3 } '""").strip()
    
    stmt = """update """ + defs.my_schema + """.timetable set T1_time = time '""" + defs.et + """'
where query = ?q;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    ##endtestcase
    ##testcase PH19 PH Query 19
    stmt = """set param ?q 19;"""
    output = _dci.cmdexec(stmt)
    
    #set showshape on;
    # TPC-H/TPC-R Discounted Revenue Query (Q19)
    # 2X rowcoun = 1
    # Database -- <catalog>.<schema>
    
    # find gross discounted revenue for all orders for three different
    # types of parts that were shipped by air or delivered in person
    
    stmt = """prepare xx from
select
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
    
    #set showshape off;
    
    stmt = """log """ + defs.work_dir + """/dslog clear;"""
    output = _dci.cmdexec(stmt)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    stmt = """log off;"""
    output = _dci.cmdexec(stmt)
    
    defs.et = _testmgr.shell_call("""grep "Compile Time" """ + defs.work_dir + """/dslog | awk ' { print $3 } '""").strip()
    
    stmt = """execute save_plan;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into """ + defs.my_schema + """.timetable (query,cardinal,T1_cost,T1_cmp_time)
(select ?q,cardinality,total_cost, time '""" + defs.et + """' from table(explain(NULL,'XX'))
where operator = 'ROOT');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/A100.RESULT""", 'ph19')
    
    ##expectstat $test_dir/A100.$MODEL ex19a
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """log """ + defs.work_dir + """/dslog clear;"""
    output = _dci.cmdexec(stmt)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    stmt = """log off;"""
    output = _dci.cmdexec(stmt)
    
    defs.et = _testmgr.shell_call("""grep "Elapsed Time" """ + defs.work_dir + """/dslog | awk ' { print $3 } '""").strip()
    
    stmt = """update """ + defs.my_schema + """.timetable set T1_time = time '""" + defs.et + """'
where query = ?q;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    _testmgr.testcase_end(desc)

