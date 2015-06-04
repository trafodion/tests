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

import time
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
    
def test001(desc="""Costing anomaly in fake histograms"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    stmt = """set schema """ + defs.my_schema + """;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """control query default query_cache '0';"""
    output = _dci.cmdexec(stmt)
    
    # no case attached to this, but fix is very small
    # known as R2.1 costing anomaly
    # when predicate is outside upper or lower boundaries of actual values in
    # table, then "fake" histograms are used.  There was a bug in this code causing
    # extra probes and inflated costing.  Cost for lower boundary predicate should
    # be the same as below lower boundary one.
   
    stmt = """create table lineitem like """ + gvars.g_schema_tpch2x + """.lineitem with constraints with partitions;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    stmt = gvars.inscmd + """ lineitem (select * from """ + gvars.g_schema_tpch2x + """.lineitem);"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)

    stmt = """create index lineix1 on lineitem (l_suppkey);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """update statistics for table lineitem on every key sample;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    stmt = """select count(*) from lineitem;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '11997996')
 
    # force index/table join
    stmt = """control query shape nested_join(cut,cut);"""
    output = _dci.cmdexec(stmt)
    
    #beneath lower boundary
    stmt = """prepare X1 from
select * from lineitem
where l_suppkey <= 0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select substring(cast(SEQ_NUM+100 as char(3)),2,2) s,
cast(LEFT_CHILD_SEQ_NUM as char(2)) lc,
cast(RIGHT_CHILD_SEQ_NUM as char(2)) rc,
substring(operator,1,17) operator,
substring
(substring(tname from (1+locate('.',tname))),
(1+locate('.',substring(tname from (1+locate('.',tname))))),
10
) tab_name,
cast(cardinality as char(11)) cardinal,
cast(operator_cost as char(11)) op_cost,
cast(total_cost as char(11)) tot_cost
from table (explain(NULL,'X1'))
order by 1 desc;"""
    output = _dci.cmdexec(stmt)
    
    # lower boundary
    stmt = """prepare XX from
select * from lineitem
where l_suppkey <= 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select substring(cast(SEQ_NUM+100 as char(3)),2,2) s,
cast(LEFT_CHILD_SEQ_NUM as char(2)) lc,
cast(RIGHT_CHILD_SEQ_NUM as char(2)) rc,
substring(operator,1,17) operator,
substring
(substring(tname from (1+locate('.',tname))),
(1+locate('.',substring(tname from (1+locate('.',tname))))),
10
) tab_name,
cast(cardinality as char(11)) cardinal,
cast(operator_cost as char(11)) op_cost,
cast(total_cost as char(11)) tot_cost
from table (explain(NULL,'XX'))
order by 1 desc;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select case when xx.operator_cost = x1.operator_cost
then 'PASS'
else 'FAIL'
end
from (select operator_cost from table (explain(null,'XX'))
where operator = 'FILE_SCAN_UNIQUE') xx,
(select operator_cost from table (explain(null,'X1'))
where operator = 'FILE_SCAN_UNIQUE') x1;"""
    output = _dci.cmdexec(stmt)
    # TRAF _dci.expect_str_token(output, """PASS""")
    
    # over upper boundary
    
    stmt = """prepare X1 from
select * from lineitem
where l_suppkey >=20001;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select substring(cast(SEQ_NUM+100 as char(3)),2,2) s,
cast(LEFT_CHILD_SEQ_NUM as char(2)) lc,
cast(RIGHT_CHILD_SEQ_NUM as char(2)) rc,
substring(operator,1,17) operator,
substring
(substring(tname from (1+locate('.',tname))),
(1+locate('.',substring(tname from (1+locate('.',tname))))),
10
) tab_name,
cast(cardinality as char(11)) cardinal,
cast(operator_cost as char(11)) op_cost,
cast(total_cost as char(11)) tot_cost
from table (explain(NULL,'X1'))
order by 1 desc;"""
    output = _dci.cmdexec(stmt)
    
    # at upper boundary
    stmt = """prepare XX from
select * from lineitem
where l_suppkey >= 20000;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select substring(cast(SEQ_NUM+100 as char(3)),2,2) s,
cast(LEFT_CHILD_SEQ_NUM as char(2)) lc,
cast(RIGHT_CHILD_SEQ_NUM as char(2)) rc,
substring(operator,1,17) operator,
substring
(substring(tname from (1+locate('.',tname))),
(1+locate('.',substring(tname from (1+locate('.',tname))))),
10
) tab_name,
cast(cardinality as char(11)) cardinal,
cast(operator_cost as char(11)) op_cost,
cast(total_cost as char(11)) tot_cost
from table (explain(NULL,'XX'))
order by 1 desc;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select case when xx.operator_cost = x1.operator_cost
then 'PASS'
else 'FAIL'
end
from (select operator_cost from table (explain(null,'XX'))
where operator = 'FILE_SCAN_UNIQUE') xx,
(select operator_cost from table (explain(null,'X1'))
where operator = 'FILE_SCAN_UNIQUE') x1;"""
    output = _dci.cmdexec(stmt)
    # TRAF _dci.expect_str_token(output, """PASS""")
    
    # cleanup
    stmt = """drop table lineitem;"""
    output = _dci.cmdexec(stmt)
    stmt = """control query shape cut;"""
    output = _dci.cmdexec(stmt)
    stmt = """control query shape off;"""
    output = _dci.cmdexec(stmt)
    stmt = """control query default query_cache reset;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

