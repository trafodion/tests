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

import q05sql
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
    
def test001(desc="""q03:"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """set param ?i1 90;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare q03 from
SELECT l_returnflag,
l_linestatus,
SUM(l_quantity) as sum_qty,
CAST(SUM(l_extendedprice) AS NUMERIC(18,2)) as sum_base_price,
CAST(SUM(l_extendedprice * (1-l_discount)) AS NUMERIC(18,2))
as sum_disc_price,
CAST(SUM(l_extendedprice * (1-l_discount) * (1 + l_tax)) AS NUMERIC(18,2))
as sum_charge,
AVG(l_quantity) as avg_qty,
AVG(l_extendedprice) as avg_price,
AVG(CAST(l_discount AS NUMERIC (10,3))),
AVG(l_discount) as avg_disc,
COUNT(*) as count_order
FROM lineitem
WHERE l_shipdate <= DATE '1998-12-01' - cast(?i1 as interval day(3))
GROUP BY l_returnflag, l_linestatus
ORDER BY l_returnflag, l_linestatus
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain q03;"""
    output = _dci.cmdexec(stmt)
    
    # unexpect any ERROR[8551] Error 31
    stmt = """execute q03;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    _dci.expect_selected_msg(output, 4)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test002(desc="""q05: Q5 Local supplier volume query"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """set schema """ + gvars.g_schema_tpch2x + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """prepare q05 from
SELECT [last 1] n_name,
CAST(SUM(l_extendedprice*(1-l_discount)) AS NUMERIC(18,2)) as revenue
FROM customer, orders, lineitem, supplier, nation, region
WHERE c_custkey = o_custkey
AND o_orderkey = l_orderkey
AND l_suppkey = s_suppkey
AND c_nationkey= s_nationkey
AND s_nationkey = n_nationkey
AND n_regionkey = r_regionkey
AND r_name =  cast('ASIA' as char(25))
AND o_orderdate >=  cast('1994-01-01' as date)
AND o_orderdate <  cast('1994-01-01' as date) + interval '1' year
GROUP BY n_name
ORDER BY 2 desc
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # q05.1:
    stmt = """execute q05;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    stmt = """log """ + defs.work_dir + """/q05log cmdtext off, quiet, clear;"""
    output = _dci.cmdexec(stmt)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    stmt = """log off;"""
    output = _dci.cmdexec(stmt)
    output = _testmgr.shell_call("""cat """ + defs.work_dir + """/q05log | grep -v Time | grep -v EOC | grep -v log | grep -v '>>' | cut -c 1-43 > """ + defs.work_dir + """/q05exp""")
    
    # q05.2:
    stmt = """execute q05;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    q05sql._init(_testmgr)
    
    # q05.3:
    stmt = """execute q05;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    q05sql._init(_testmgr)
    
    # q05.4:
    stmt = """execute q05;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    q05sql._init(_testmgr)
    
    # q05.5:
    stmt = """execute q05;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    q05sql._init(_testmgr)
    
    # q05.6:
    stmt = """execute q05;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    q05sql._init(_testmgr)
    
    # q05.7:
    stmt = """execute q05;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    q05sql._init(_testmgr)
    
    _testmgr.testcase_end(desc)

