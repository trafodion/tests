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
    
    stmt = """create schema """ + defs.my_schema + """;"""
    output = _dci.cmdexec(stmt)
    stmt = """set schema """ + defs.my_schema + """;"""
    output = _dci.cmdexec(stmt)
    stmt = """CREATE VIEW REVENUE (SUPPLIER_NO, TOTAL_REVENUE) AS
SELECT G_TPCH2X.LINEITEM.L_SUPPKEY, SUM(G_TPCH2X.LINEITEM.L_EXTENDEDPRICE *
(1 - G_TPCH2X.LINEITEM.L_DISCOUNT)) FROM G_TPCH2X.LINEITEM WHERE
G_TPCH2X.LINEITEM.L_SHIPDATE >= DATE '1993-02-01' AND
G_TPCH2X.LINEITEM.L_SHIPDATE < DATE '1993-02-01' + INTERVAL '3' MONTH
GROUP BY G_TPCH2X.LINEITEM.L_SUPPKEY ;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table  exp_tab(operator  varchar(25), detail_stat varchar(250)) no partitions;"""
    output = _dci.cmdexec(stmt)
    stmt = """set schema """ + gvars.g_schema_tpch2x + """;"""
    output = _dci.cmdexec(stmt)
    
    #cqd EXPLAIN_DISPLAY_FORMAT 'external';
    #CPU_TIME, IO_TIME, MSG_TIME, IDLE_TIME, PROBES, TOTAL_TIME
    #cqd EXPLAIN_DISPLAY_FORMAT 'external_detailed';
    #CPU_TIME, IO_TIME, MSG_TIME, IDLE_TIME, PROBES, IO_SEQ, IO_RAND, TOTAL_TIME
    #cqd EXPLAIN_DISPLAY_FORMAT 'internal';
    #TC_PROC, TC_PROD, TC_SENT, IO_SEQ, IO_RAND
    stmt = """cqd EXPLAIN_DISPLAY_FORMAT 'external';"""
    output = _dci.cmdexec(stmt)
    #cqd EXPLAIN_DISPLAY_FORMAT 'external_detailed';
    #cqd EXPLAIN_DISPLAY_FORMAT 'internal';
    stmt = """prepare explainIt from
select substring(cast(SEQ_NUM+100 as char(3)),2,2) s,
cast(LEFT_CHILD_SEQ_NUM as char(2)) lc,
cast(RIGHT_CHILD_SEQ_NUM as char(2)) rc,
substring(operator,1,16) operator,
substring
(substring(tname from (1+locate('.',tname))),
(1+locate('.',substring(tname from (1+locate('.',tname))))),
10
) tab_name,
cast(cardinality as char(11)) cardinal,
cast(operator_cost as char(11)) op_cost,
cast(total_cost as char(11)) tot_cost,
cast(detail_cost as char(256)) detail_cost  -- This is the one that shows all the individual cost components in detail.
from table (explain(NULL,'XX'))
order by 1 desc;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare explainIt2 from
select substring(operator,1,16) operator,
cast(detail_cost as char(356)) detail_cost  -- This is the one that shows all the individual cost components in detail.
from table (explain(NULL,'XX'))
order by 1 desc;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare mytab2 from insert into """ + defs.my_schema + """.exp_tab(select substring(operator,1,16) operator, cast(detail_cost as char(400)) detail_cost from table (explain(NULL,'XX'))) order by 1 desc;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare mytab3 from delete from """ + defs.my_schema + """.exp_tab;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare check2 from
select 'FAIL', operator, detail_stat
from """ + defs.my_schema + """.exp_tab
where locate('CPU_TIME', detail_stat) = 0
and
locate('IO_TIME', detail_stat) = 0
and
locate('MSG_TIME', detail_stat) = 0
and
locate('IDLE_TIME', detail_stat) = 0
and
locate('PROBES', detail_stat) = 0;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare check4 from
select 'FAIL', operator, detail_stat
from """ + defs.my_schema + """.exp_tab
where locate('TC_PROC', detail_stat) = 0
and
locate('TC_PROCD', detail_stat) = 0
and
locate('TC_SENT', detail_stat) = 0
and
locate('IO_SEQ', detail_stat) = 0
and
locate('IO_RAND', detail_stat) = 0;"""
    output = _dci.cmdexec(stmt)
    
