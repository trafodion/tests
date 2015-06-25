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
    _dci.setup_schema(defs.my_schema)

    # cqds for bulkload
    stmt = """cqd COMP_BOOL_226 'ON';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """cqd TRAF_LOAD_PREP_TMP_LOCATION '/bulkload/';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """cqd TRAF_LOAD_TAKE_SNAPSHOT 'OFF';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    # ===================================
    # setup for tcase_salt tests
    # ===================================

    stmt = """drop table salt_orders cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table salt_lineitem cascade;"""
    output = _dci.cmdexec(stmt)

    # salt_orders: salted, no statistics
    stmt = """create table salt_orders
primary key (o_orderkey) salt using 8 partitions no load
as select * from g_tpch2x.orders;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 0)

    stmt = """load into salt_orders select * from g_tpch2x.orders;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """select count(*) from salt_orders;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '3000000')

    # salt_lineitem: salted, no statistics
    stmt = """create table salt_lineitem
primary key (l_shipdate ASC, l_orderkey ASC, l_linenumber ASC)
salt using 8 partitions no load
as select * from g_tpch2x.lineitem;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 0)

    stmt = """load into salt_lineitem select * from g_tpch2x.lineitem;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """select count(*) from salt_lineitem;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '11997996')

    # ===================================
    # setup for tcase_nosalt_mreg tests
    # ===================================
    stmt = """drop table nosaltmreg_orders cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table nosaltmreg_orders_ws cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table nosaltmreg_lineitem cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table nosaltmreg_lineitem_ws cascade;"""
    output = _dci.cmdexec(stmt)

    # nosaltmreg_orders: nonsalted, multi-region, no statistics
    stmt = """create table nosaltmreg_orders
primary key (o_orderkey) number of partitions 8 no load
as select * from g_tpch2x.orders;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 0)

    stmt = """load into nosaltmreg_orders select * from g_tpch2x.orders;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """select count(*) from nosaltmreg_orders;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '3000000')

    # nosaltmreg_orders_ws: nonsalted, multi region server, with statistics
    stmt = """create table nosaltmreg_orders_ws
primary key (o_orderkey) number of partitions 8 no load
as select * from g_tpch2x.orders;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 0)

    stmt = """load into nosaltmreg_orders_ws select * from g_tpch2x.orders;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """select count(*) from nosaltmreg_orders_ws;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '3000000')

    stmt = """update statistics for table nosaltmreg_orders_ws
on every column sample random 10 percent;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """showstats for table nosaltmreg_orders_ws on every key detail;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_any_substr(output, ("""No Histograms exist for the""" +
                                      """ requested columns or groups"""))

    # nosaltmreg_lineitem: nonsalted, multi-region, no statistics
    stmt = """create table nosaltmreg_lineitem
primary key (l_shipdate ASC, l_orderkey ASC, l_linenumber ASC)
number of partitions 8 no load
as select * from g_tpch2x.lineitem;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 0)

    stmt = """load into nosaltmreg_lineitem select * from g_tpch2x.lineitem;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """select count(*) from nosaltmreg_lineitem;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '11997996')

    # nosaltmreg_lineitem_ws: nonsalted, multi-region, with statistics
    stmt = """create table nosaltmreg_lineitem_ws
primary key (l_shipdate ASC, l_orderkey ASC, l_linenumber ASC)
number of partitions 8 no load
as select * from g_tpch2x.lineitem;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 0)

    stmt = """load into nosaltmreg_lineitem_ws
select * from g_tpch2x.lineitem;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """select count(*) from nosaltmreg_lineitem_ws;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '11997996')

    stmt = """update statistics for table nosaltmreg_lineitem_ws
on every column sample random 10 percent;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """showstats for table nosaltmreg_lineitem_ws
on every column detail;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_any_substr(output, ("""No Histograms exist for the""" +
                                      """ requested columns or groups"""))

    # ===================================
    # setup for tcase_nosalt_sreg tests
    # ===================================

    stmt = """drop table nosaltsreg_orders cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table nosaltsreg_orders_ws cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table nosaltsreg_lineitem cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table nosaltsreg_lineitem_ws cascade;"""
    output = _dci.cmdexec(stmt)

    # nosaltsreg_orders: nonsalted, single-region, no statistics
    stmt = """create table nosaltsreg_orders
primary key (o_orderkey) no partition no load
as select * from g_tpch2x.orders;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 0)

    stmt = """load into nosaltsreg_orders select * from g_tpch2x.orders;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """select count(*) from nosaltsreg_orders;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '3000000')

    # nosaltsreg_orders_ws: nonsalted, single region server, with statistics
    stmt = """create table nosaltsreg_orders_ws
primary key (o_orderkey) no partition no load
as select * from g_tpch2x.orders;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 0)

    stmt = """load into nosaltsreg_orders_ws select * from g_tpch2x.orders;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """select count(*) from nosaltsreg_orders_ws;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '3000000')

    stmt = """update statistics for table nosaltsreg_orders_ws
on every column sample random 10 percent;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """showstats for table nosaltsreg_orders_ws on every key detail;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_any_substr(output, ("""No Histograms exist for the""" +
                                      """ requested columns or groups"""))

    # nosaltsreg_lineitem: nonsalted, single-region, no statistics
    stmt = """create table nosaltsreg_lineitem
primary key (l_shipdate ASC, l_orderkey ASC, l_linenumber ASC)
no partition no load
as select * from g_tpch2x.lineitem;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 0)

    stmt = """load into nosaltsreg_lineitem select * from g_tpch2x.lineitem;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """select count(*) from nosaltsreg_lineitem;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '11997996')

    # nosaltsreg_lineitem_ws: nonsalted, single-region, with statistics
    stmt = """create table nosaltsreg_lineitem_ws
primary key (l_shipdate ASC, l_orderkey ASC, l_linenumber ASC)
no partition no load
as select * from g_tpch2x.lineitem;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 0)

    stmt = """load into nosaltsreg_lineitem_ws
select * from g_tpch2x.lineitem;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """select count(*) from nosaltsreg_lineitem_ws;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '11997996')

    stmt = """update statistics for table nosaltsreg_lineitem_ws
on every column sample random 10 percent;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """showstats for table nosaltsreg_lineitem_ws
on every column detail;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_any_substr(output, ("""No Histograms exist for the""" +
                                      """ requested columns or groups"""))

    stmt = """cqd COMP_BOOL_226 reset;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """cqd TRAF_LOAD_PREP_TMP_LOCATION reset;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """cqd TRAF_LOAD_TAKE_SNAPSHOT reset;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """cqd QUERY_CACHE '0';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    # workaround lp bug 1409937
    stmt = """cqd CACHE_HISTOGRAMS 'OFF';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """cqd CACHE_HISTOGRAMS reset;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """prepare is_parallel_plan from
select CASE operator WHEN 'ESP_EXCHANGE' then 'PASS' ELSE 'FAIL' END
from table(explain(NULL, 'XX')) where seq_num =
(select seq_num-1 from table(explain(NULL, 'XX')) where operator = 'ROOT');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    stmt = """prepare is_serial_plan from
select CASE operator WHEN 'ESP_EXCHANGE' then 'FAIL' ELSE 'PASS' END
from table(explain(NULL, 'XX')) where seq_num =
(select seq_num-1 from table(explain(NULL, 'XX')) where operator = 'ROOT');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    stmt = """prepare is_hash2_part from
select CASE WHEN offset = 0 THEN 'FAIL' ELSE 'PASS' END
from (select locate('hash2 partitioned', description) as offset, description
from table(explain(null,'XX'))
where (seq_num = (select seq_num + 1 from table(explain(null,'XX'))
where operator = 'TRAFODION_SCAN') and operator = 'ESP_EXCHANGE') OR
(seq_num = (select seq_num + 2 from table(explain(null,'XX'))
where operator = 'TRAFODION_SCAN') and operator = 'ESP_EXCHANGE')) t;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    stmt = """prepare is_range_part from
select CASE WHEN offset = 0 THEN 'FAIL' ELSE 'PASS' END
from (select locate('range partitioned', description) as offset, description
from table(explain(null,'XX'))
where (seq_num = (select seq_num + 1 from table(explain(null,'XX'))
where operator = 'TRAFODION_SCAN') and operator = 'ESP_EXCHANGE') OR
(seq_num = (select seq_num + 2 from table(explain(null,'XX'))
where operator = 'TRAFODION_SCAN') and operator = 'ESP_EXCHANGE')) t;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    # to show distribution of rows read from each ESP
    #stmt = """cqd DETAILED_STATISTICS 'ALL';"""
    #output = _dci.cmdexec(stmt)
    #_dci.expect_complete_msg(output)

    stmt = """prepare esp_row_distrib from
select frag_num, inst_num, seq_num,
cast(substring(variable_info from position('AccessedRows' in variable_info)
for position('DiskIOs' in variable_info) -
position('AccessedRows' in variable_info))
as char(40) character set iso88591) as rows_accessed
from table(statistics(null, 'XX'))
where tdb_name = 'EX_HBASE_ACCESS';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
