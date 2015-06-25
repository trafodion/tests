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


def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci

    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()

    output = _dci.cmdexec("""set schema compiler_hbasepart;""")


def qry_orders_nosaltmreg(cqd_hash2p_val='ON', cqd_rangep_val='ON',
                          stats_flag=None):

    if stats_flag == 'stats':
        tblname = 'nosaltmreg_orders_ws'
    else:
        tblname = 'nosaltmreg_orders'

    if cqd_hash2p_val == 'ON' and cqd_rangep_val == 'OFF':
        verify_stmt = 'is_hash2_part'
        verify_gbob = verify_stmt
    elif cqd_hash2p_val == 'OFF' and cqd_rangep_val == 'OFF':
        verify_stmt = 'is_serial_plan'
        verify_gbob = 'is_range_part'
    else:
        verify_stmt = 'is_range_part'
        verify_gbob = verify_stmt

    stmt = """cqd HBASE_HASH2_PARTITIONING '""" + cqd_hash2p_val + """';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """cqd HBASE_RANGE_PARTITIONING '""" + cqd_rangep_val + """';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """cqd HBASE_MIN_BYTES_PER_ESP_PARTITION '10';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """showcontrol default;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    # --Q1------------------------------------------------
    # select on EXACT KEY: serial plan
    stmt = ("""prepare XX from select * from """ + tblname +
            """ where o_orderkey = 1000000;""")
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)

    stmt = """execute is_serial_plan;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, 'PASS')

    # --Q2------------------------------------------------
    # select with IN clause: serial plan
    stmt = ("""prepare XX from select * from """ + tblname +
            """ where o_orderkey in (1000, 500000, 10000, 50000,""" +
            """ 100000, 5000, 100, 500);""")
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)

    #stmt = """explain XX;"""
    #output = _dci.cmdexec(stmt)

    stmt = """execute is_serial_plan;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, 'PASS')

    # --Q3------------------------------------------------
    # query involving range on key
    stmt = ("""prepare XX from select * from """ + tblname +
            """ where o_orderkey < 300000;""")
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)

    stmt = """execute is_serial_plan;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, 'PASS')

    # --Q4------------------------------------------------
    # query involving range on key
    stmt = ("""prepare XX from select * from """ + tblname +
            """ where o_orderkey > 905000;""")
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)

    if stats_flag == 'stats':
        _dci.unexpect_any_substr(output, 'hash2')
    else:
        stmt = """execute is_serial_plan;"""
        output = _dci.cmdexec(stmt)
        _dci.expect_any_substr(output, 'PASS')

    # debug
    #output = _dci.cmdexec("""explain XX;""")

    # --Q5------------------------------------------------
    # query involving range on key
    stmt = ("""prepare XX from select * from """ + tblname +
            """ where o_orderkey > 909000 or o_orderkey < 1500;""")
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)

    if stats_flag == 'stats':
        _dci.unexpect_any_substr(output, 'hash2')
    else:
        stmt = """execute is_serial_plan;"""
        output = _dci.cmdexec(stmt)
        _dci.expect_any_substr(output, 'PASS')

    # debug
    #output = _dci.cmdexec("""explain XX;""")

    # --Q6------------------------------------------------
    # query involving small range on keys: serial plan
    stmt = ("""prepare XX from select * from """ + tblname +
            """ where o_orderkey between 400000 and 400100;""")
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)

    stmt = """execute is_serial_plan;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, 'PASS')

    # --Q7------------------------------------------------
    # query involving small range on keys: serial plan
    stmt = ("""prepare XX from select * from """ + tblname +
            """ where o_orderkey <= 50;""")
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)

    stmt = """execute is_serial_plan;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, 'PASS')

    # --Q8------------------------------------------------
    # query involving small range on keys: serial plan
    stmt = ("""prepare XX from select * from """ + tblname +
            """ where o_orderkey >= 999985;""")
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)

    if stats_flag == 'stats':
        _dci.unexpect_any_substr(output, 'hash2')
    else:
        stmt = """execute is_serial_plan;"""
        output = _dci.cmdexec(stmt)
        _dci.expect_any_substr(output, 'PASS')

    # debug
    #output = _dci.cmdexec("""explain XX;""")

    # --Q9------------------------------------------------
    # query involving large range on keys: parallel plan
    stmt = ("""prepare XX from select * from """ + tblname +
            """ where o_orderkey between 300000 and 400000;""")
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)

    stmt = """execute is_serial_plan;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, 'PASS')

    # --Q10-----------------------------------------------
    stmt = ("""prepare XX from select * from """ + tblname +
            """ where o_orderkey > 600000 and o_orderkey < 600500;""")
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)

    stmt = """execute is_serial_plan;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, 'PASS')

    # --Q11-----------------------------------------------
    # GROUP BY over a full table: parallel plan
    stmt = ("""prepare XX from select o_custkey, sum(o_totalprice) from """ +
            tblname + """ group by o_custkey;""")
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)

    #stmt = """execute is_serial_plan;"""
    #output = _dci.cmdexec(stmt)
    #_dci.expect_any_substr(output, 'PASS')

    # debug
    #output = _dci.cmdexec("""explain XX;""")

    # --Q12-----------------------------------------------
    # ORDER BY over a full table: parallel plan
    stmt = ("""prepare XX from select * from """ + tblname +
            """ order by o_orderkey;""")
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)

    if stats_flag == 'stats':
        _dci.unexpect_any_substr(output, 'hash2')
    else:
        stmt = """execute is_serial_plan;"""
        output = _dci.cmdexec(stmt)
        _dci.expect_any_substr(output, 'PASS')

    # --Q13-----------------------------------------------
    # ORDER BY DESC
    stmt = ("""prepare XX from select * from """ + tblname +
            """ order by o_orderkey DESC;""")
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)

    stmt = """execute is_parallel_plan;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, 'PASS')

    stmt = """execute is_hash2_part;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, 'PASS')

    stmt = """cqd HBASE_HASH2_PARTITIONING reset;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """cqd HBASE_RANGE_PARTITIONING reset;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)


def qry_lineitem_nosaltmreg(cqd_hash2p_val='ON', cqd_rangep_val='ON',
                            stats_flag=None):

    if stats_flag == 'stats':
        tblname = 'nosaltmreg_lineitem_ws'
    else:
        tblname = 'nosaltmreg_lineitem'

    if cqd_hash2p_val == 'ON' and cqd_rangep_val == 'OFF':
        verify_stmt = 'is_hash2_part'
        verify_gbob = verify_stmt
    elif cqd_hash2p_val == 'OFF' and cqd_rangep_val == 'OFF':
        verify_stmt = 'is_serial_plan'
        verify_gbob = 'is_range_part'
    else:
        verify_stmt = 'is_range_part'
        verify_gbob = verify_stmt

    stmt = """cqd HBASE_HASH2_PARTITIONING '""" + cqd_hash2p_val + """';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """cqd HBASE_RANGE_PARTITIONING '""" + cqd_rangep_val + """';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """cqd HBASE_MIN_BYTES_PER_ESP_PARTITION '10';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """showcontrol query default HBASE_HASH2_PARTITIONING;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """showcontrol query default HBASE_RANGE_PARTITIONING;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """showcontrol query default HBASE_STATS_PARTITIONING;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    # --Q1------------------------------------------------
    # select on EXACT KEY: serial plan
    stmt = ("""prepare XX from select * from """ + tblname +
            """ where l_shipdate=date'1996-06-18' and""" +
            """ l_orderkey = 10675237 and l_linenumber = 1;""")
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)

    #stmt = """explain XX;"""
    #output = _dci.cmdexec(stmt)

    stmt = """execute is_serial_plan;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, 'PASS')

    # --Q2------------------------------------------------
    # select on partial key
    stmt = ("""prepare XX from select * from """ + tblname +
            """ where l_shipdate=date'1996-06-18';""")
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)

    #stmt = """explain XX;"""
    #output = _dci.cmdexec(stmt)

    stmt = """execute is_serial_plan;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, 'PASS')

    # --Q3------------------------------------------------
    # select on partial key
    stmt = ("""prepare XX from select * from """ + tblname +
            """ where l_orderkey = 10675237;""")
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)

    #stmt = """explain XX;"""
    #output = _dci.cmdexec(stmt)

    stmt = """execute is_serial_plan;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, 'PASS')

    # --Q4------------------------------------------------
    # select with IN clause: serial plan
    stmt = ("""prepare XX from select * from """ + tblname +
            """ where l_shipdate in (date'1996-06-18', date'1998-06-18',""" +
            """ date'1992-06-18', date'1995-12-31');""")
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)

    #stmt = """explain XX;"""
    #output = _dci.cmdexec(stmt)

    stmt = """execute is_serial_plan;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, 'PASS')

    # --Q5------------------------------------------------
    # select with IN clause: serial plan
    stmt = ("""prepare XX from select * from """ + tblname +
            """ where l_shipdate=date'1996-06-18' and""" +
            """ l_orderkey in (11651779,11197828,9084833,9346147,11822080);""")
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)

    #stmt = """explain XX;"""
    #output = _dci.cmdexec(stmt)

    stmt = """execute is_serial_plan;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, 'PASS')

    # --Q6------------------------------------------------
    # select with IN clause: serial plan
    stmt = ("""prepare XX from select * from """ + tblname +
            """ where l_shipdate=date'1996-06-18' and""" +
            """ l_orderkey in (11651779,11197828,9084833,9346147,11822080)""" +
            """ and l_linenumber = 4;""")
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)

    #stmt = """explain XX;"""
    #output = _dci.cmdexec(stmt)

    stmt = """execute is_serial_plan;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, 'PASS')

    # --Q7------------------------------------------------
    # query involving range on key
    stmt = ("""prepare XX from select * from """ + tblname +
            """ where l_shipdate < date'1992-03-01';""")
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)

    stmt = """execute is_serial_plan;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, 'PASS')

    # --Q8------------------------------------------------
    # query involving range on key
    stmt = ("""prepare XX from select * from """ + tblname +
            """ where l_shipdate < date'1992-03-01'""" +
            """ and l_orderkey >= 11000000;""")
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)

    stmt = """execute is_serial_plan;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, 'PASS')

    # --Q9------------------------------------------------
    # query involving range on key
    stmt = ("""prepare XX from select * from """ + tblname +
            """ where l_shipdate < date'1992-03-01' and""" +
            """ l_orderkey >= 11000000 and l_linenumber between 2 and 4;""")
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)

    stmt = """execute is_serial_plan;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, 'PASS')

    # --Q10-----------------------------------------------
    # query involving small range on keys: serial plan
    stmt = ("""prepare XX from select * from """ + tblname +
            """ where l_shipdate = date'1996-06-18' and""" +
            """ (l_orderkey between 9084833 and 9084850) and""" +
            """ (l_linenumber between 2 and 3);""")
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)

    stmt = """execute is_serial_plan;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, 'PASS')

    # --Q11-----------------------------------------------
    # query involving small range on partial key
    stmt = ("""prepare XX from select * from """ + tblname +
            """ where l_orderkey between 9084833 and 9084850;""")
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)

    stmt = """execute is_serial_plan;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, 'PASS')

    # --Q12-----------------------------------------------
    # GROUP BY over a full table
    stmt = ("""prepare XX from select l_shipdate, l_orderkey,""" +
            """ l_linenumber, avg(l_discount) from """ + tblname +
            """ group by l_shipdate, l_orderkey, l_linenumber;""")
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)

    stmt = """execute is_serial_plan;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, 'PASS')

    # --Q13-----------------------------------------------
    # ORDER BY over a full table
    stmt = ("""prepare XX from select * from """ + tblname +
            """ order by l_shipdate;""")
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)

    stmt = """execute is_serial_plan;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, 'PASS')

    # --Q14-----------------------------------------------
    stmt = ("""prepare XX from select * from """ + tblname +
            """ order by l_orderkey, l_linenumber;""")
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)

    stmt = """execute is_parallel_plan;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, 'PASS')

    stmt = """execute is_hash2_part;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, 'PASS')

    # --Q15-----------------------------------------------
    stmt = ("""prepare XX from select * from """ + tblname +
            """ order by l_shipdate, l_orderkey, l_linenumber;""")
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)

    stmt = """execute is_serial_plan;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, 'PASS')

    # --Q16-----------------------------------------------
    stmt = ("""prepare XX from select * from """ + tblname +
            """ order by l_partkey, l_commitdate;""")
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)

    stmt = """execute is_parallel_plan;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, 'PASS')

    stmt = """execute is_hash2_part;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, 'PASS')

    # --Q17-----------------------------------------------
    # ORDER BY DESC
    stmt = ("""prepare XX from select * from """ + tblname +
            """ order by l_shipdate DESC;""")
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)

    stmt = """execute is_parallel_plan;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, 'PASS')

    stmt = """execute is_hash2_part;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, 'PASS')

    # --Q18-----------------------------------------------
    stmt = ("""prepare XX from select * from """ + tblname +
            """ order by l_shipdate DESC, l_linenumber ASC,""" +
            """ l_orderkey DESC;""")
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)

    stmt = """execute is_parallel_plan;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, 'PASS')

    stmt = """execute is_hash2_part;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, 'PASS')

    stmt = """cqd HBASE_HASH2_PARTITIONING reset;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)


# ===================================================
# TESTCASE for NON-SALTED, MULTI-REGION table WITH STATS
# hash2 part = ON, range part = ON: parallel with RANGE partitioning
# hash2 part = OFF, range part = ON: parallel with RANGE partitioning
# hash2 part = ON, range part = OFF: parallel with HASH2 partitioning
# hash2 part = OFF, range part = OFF: serial plan
# exceptions:
#    single record SELECT with keys specified: always serial plan
#    queries involving small ranges on keys (no more than 10-50 rows
#        in result set): serial plan
#    groupby over a full table: parallel plan
#    orderby over a full table: parallel plan
# join on 2 salted tables with same # of partitions should be
# co-partitioned (eg. no repartition/exchange on either side of join).
# ===================================================
def test_hpON_rpON_nosaltmreg(desc="""hpON,rpON,stats,nosalt,multi-region"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return
    defs.testid = """test_hpON_rpON_nosaltmreg"""

    # hash2 partitioning = ON, range partitioning = ON
    # nonsalt multi-region table with statistics
    # expect: range partitioning
    qry_orders_nosaltmreg('ON', 'ON', 'stats')
    qry_lineitem_nosaltmreg('ON', 'ON', 'stats')
    _testmgr.testcase_end(desc)


def test_hpOFF_rpON_nosaltmreg(desc="""hpOFF,rpON,stats,nosalt,
multi-region"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return
    defs.testid = """test_hpOFF_rpON_nosaltmreg"""

    # hash2 partitioning = OFF, range partitioning = ON
    # nonsalt multi-region table with statistics
    # expect: range partitioning
    qry_orders_nosaltmreg('OFF', 'ON', 'stats')
    qry_lineitem_nosaltmreg('OFF', 'ON', 'stats')
    _testmgr.testcase_end(desc)


def test_hpON_rpOFF_nosaltmreg(desc="""hpON,rpOFF,stats,nosalt,
multi-region"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return
    defs.testid = """test_hpON_rpOFF_nosaltmreg"""

    # hash2 partitioning = ON, range partitioning = OFF
    # nonsalt multi-region table with statistics
    # expect: hash2 partitioning
    qry_orders_nosaltmreg('ON', 'OFF', 'stats')
    qry_lineitem_nosaltmreg('ON', 'OFF', 'stats')
    _testmgr.testcase_end(desc)


def test_hpOFF_rpOFF_nosaltmreg(desc="""hpOFF,rpOFF,stats,nosalt,
multi-region"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return
    defs.testid = """test_hpOFF_rpOFF_nosaltmreg"""

    # hash2 partitioning = OFF, range partitioning = OFF
    qry_orders_nosaltmreg('OFF', 'OFF', 'stats')
    qry_lineitem_nosaltmreg('OFF', 'OFF', 'stats')
    _testmgr.testcase_end(desc)


# ===================================================
# TESTCASE for NON-SALTED, MULTI-REGION table with NO STATS
# hash2 part = ON, range part = ON: parallel with RANGE partitioning
# hash2 part = OFF, range part = ON: parallel with RANGE partitioning
# hash2 part = ON, range part = OFF: parallel with HASH2 partitioning
# hash2 part = OFF, range part = OFF: serial plan
# exceptions:
#    single record SELECT with keys specified: always serial plan
#    queries involving small ranges on keys (no more than 10-50 rows
#        in result set): serial plan
#    groupby over a full table: parallel plan
#    orderby over a full table: parallel plan
# join on 2 salted tables with same # of partitions should be
# co-partitioned (eg. no repartition/exchange on either side of join).
# ===================================================
def test_hpON_rpON_nostat_nosaltmreg(desc="""hpON,rpON,nostats,nosalt,
multi-region"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return
    defs.testid = """test_hpON_rpON_nostat_nosaltmreg"""

    # hash2 partitioning = ON, range partitioning = ON
    # nonsalt multi-region table, NO statistics
    # expect: range partitioning
    qry_orders_nosaltmreg('ON', 'ON')
    qry_lineitem_nosaltmreg('ON', 'ON')
    _testmgr.testcase_end(desc)


def test_hpOFF_rpON_nostat_nosaltmreg(desc="""hpOFF,rpON,nostats,nosalt,
multi-region"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return
    defs.testid = """test_hpOFF_rpON_nostat_nosaltmreg"""

    # hash2 partitioning = OFF, range partitioning = ON
    # nonsalt multi-region table, NO statistics
    # expect: range partitioning
    qry_orders_nosaltmreg('OFF', 'ON')
    qry_lineitem_nosaltmreg('OFF', 'ON')
    _testmgr.testcase_end(desc)


def test_hpON_rpOFF_nostat_nosaltmreg(desc="""hpON,rpOFF,nostats,nosalt,
multi-region"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return
    defs.testid = """test_hpON_rpOFF_nostat_nosaltmreg"""

    # hash2 partitioning = ON, range partitioning = OFF
    # nonsalt multi-region table, NO statistics
    # expect: hash2 partitioning
    qry_orders_nosaltmreg('ON', 'OFF')
    qry_lineitem_nosaltmreg('ON', 'OFF')
    _testmgr.testcase_end(desc)


def test_hpOFF_rpOFF_nostat_nosaltmreg(desc="""hpOFF,rpOFF,nostats,nosalt,
multi-region"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return
    defs.testid = """test_hpOFF_rpOFF_nostat_nosaltmreg"""

    # hash2 partitioning = OFF, range partitioning = OFF
    # nonsalt multi-region table, NO statistics
    qry_orders_nosaltmreg('OFF', 'OFF')
    qry_lineitem_nosaltmreg('OFF', 'OFF')
    _testmgr.testcase_end(desc)
