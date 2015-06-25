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
import time

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


# ===================================================
# join on 2 salted tables with same # of partitions should be
# co-partitioned (eg. no repartition/exchange on either side of join).
# ===================================================
def test_join(desc="""join co-partitioned """):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return
    defs.testid = """join co-partitioned"""

    stmt = """cqd HBASE_HASH2_PARTITIONING reset;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """cqd HBASE_RANGE_PARTITIONING reset;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    # --Q1------------------------------------------------
    stmt = ("""prepare XX from select * from """ +
            gvars.g_schema_tpch2x + """.lineitem, """ +
            gvars.g_schema_tpch2x + """.orders""" +
            """ where l_orderkey = o_orderkey and l_orderkey = 10675237""" +
            """ and l_shipdate = date'1996-06-18' and l_linenumber = 1;""")
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)

    stmt = """execute is_serial_plan;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, 'PASS')

    # --Q2------------------------------------------------
    stmt = ("""prepare XX from select * from """ +
            gvars.g_schema_tpch2x + """.lineitem, """ +
            gvars.g_schema_tpch2x + """.orders""" +
            """ where l_orderkey = o_orderkey and l_orderkey = 10675237;""")
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)

    stmt = """execute is_serial_plan;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, 'PASS')

    # --Q3------------------------------------------------
    stmt = ("""prepare XX from select * from """ +
            gvars.g_schema_tpch2x + """.lineitem, """ +
            gvars.g_schema_tpch2x + """.orders""" +
            """ where l_orderkey = o_orderkey and""" +
            """ l_shipdate = date'1996-08-01';""")
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)

    stmt = """execute is_parallel_plan;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, 'PASS')

    # --Q4------------------------------------------------
    stmt = ("""prepare XX from select * from """ +
            gvars.g_schema_tpch2x + """.lineitem, """ +
            gvars.g_schema_tpch2x + """.orders""" +
            """ where l_orderkey = o_orderkey;""")
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)

    stmt = """execute is_parallel_plan;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, 'PASS')

    _testmgr.testcase_end(desc)
