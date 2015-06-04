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
    
    stmt = """prepare save_plan from
insert into """ + defs.my_schema + """.plantable
select ?q,?curr_model,cast(SEQ_NUM as smallint) s,
cast(LEFT_CHILD_SEQ_NUM as smallint) lc,
cast(RIGHT_CHILD_SEQ_NUM as smallint) rc,
substring(operator,1,30) operator
from table (explain(NULL,'XX'))
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare compare_T1_and_T2 from
update """ + defs.my_schema + """.timetable set T1_vs_T2_plan =
(select case
when plan_ops.match_ops =  T1_vs_T2.match_ops then 'MATCH'
else 'DIFFER'
end
from (select count(*) match_ops
from """ + defs.my_schema + """.plantable plan_T1,
""" + defs.my_schema + """.plantable plan_T2
where  plan_T1.seq_num = plan_T2.seq_num and
plan_T1.operator = plan_T2.operator and
plan_T1.model = 'T1' and plan_T2.model = 'T2' and
plan_T1.query_no = ?q and
plan_T2.query_no = ?q) T1_vs_T2,
(select max(seq_num) match_ops from """ + defs.my_schema + """.plantable plan_T1
where plan_T1.query_no = ?q and
plan_T1.model = 'T1') plan_ops )
where query = ?q ;"""
    output = _dci.cmdexec(stmt)
    #
    #prepare comp_bp_and_T2 from
    #update $my_schema.timetable set bp_vs_T2_plan =
    #(select case
    #         when plan_ops.match_ops =  bp_vs_T2.match_ops then 'MATCH'
    #         else 'DIFFER'
    #       end
    #from (select count(*) match_ops
    #      from $my_schema.plantable plan_bp,
    #           $my_schema.plantable plan_T2
    #      where  plan_bp.seq_num = plan_T2.seq_num and
    #             plan_bp.operator = plan_T2.operator and
    #             plan_bp.model = 'ON' and plan_T2.model = 'BPNEW' and
    #             plan_bp.query_no = ?q and
    #             plan_T2.query_no = ?q) bp_vs_T2,
    #     (select max(seq_num) match_ops from $my_schema.plantable plan_bp
    #       where plan_bp.query_no = ?q and
    #             plan_bp.model = 'BP') plan_ops )
    #where query = ?q ;
    #
    #
    #
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
cast(total_cost as char(11)) tot_cost
from table (explain(NULL,'XX'))
order by 1 desc;"""
    output = _dci.cmdexec(stmt)
    #
    stmt = """prepare comp_explain from
select substring(cast(SEQ_NUM+100 as char(3)),2,2) s,
cast(LEFT_CHILD_SEQ_NUM as char(2)) lc,
cast(RIGHT_CHILD_SEQ_NUM as char(2)) rc,
substring(operator,1,30) operator
from table (explain(NULL,'XX'))
order by 1 desc;"""
    output = _dci.cmdexec(stmt)
    #
    stmt = """prepare get_low_values  from
update """ + defs.my_schema + """.timetable
set low_time =
case when (T1_time + interval '1' second)  < T2_time  then T1_time
else T2_time
end,
low_type =
case when (T1_time + interval '1' second)  < T2_time  then 'T1'
else 'T2'
end
where query = ?q;"""
    output = _dci.cmdexec(stmt)
    #
    stmt = """prepare comp_plan_and_cost from
select
low_type, T1_vs_T2_plan, low_time,
case
when T1_vs_T2_plan = 'MATCH'
then 'PASS'
else 'FAIL'
end
from """ + defs.my_schema + """.timetable
where query = ?q;"""
    output = _dci.cmdexec(stmt)
    #
    stmt = """prepare list_all_plans from
select cast(query as char(2)) q,
cast(cardinal as char(12)) cardinality,
cast(T2_cost as char(12)) T2_cost,
T2_cmp_time,
T2_time,
cast(T1_cost as char(12)) T1_cost,
T1_cmp_time,
T1_time,
low_time,
low_type,
T1_vs_T2_plan
from """ + defs.my_schema + """.timetable
order by 1,2;"""
    output = _dci.cmdexec(stmt)
    #
    #
