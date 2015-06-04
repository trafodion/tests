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
    
    stmt = """prepare explainIt from
select substring(cast(SEQ_NUM+100 as char(3)),2,2) s,
substring(operator,1,16) operator,
cast(LEFT_CHILD_SEQ_NUM as char(2)) lc,
cast(RIGHT_CHILD_SEQ_NUM as char(2)) rc,
substring
(substring(tname from (1+locate('.',tname))),
(1+locate('.',substring(tname from (1+locate('.',tname))))),
10
) tab_name,
cast(cardinality as char(11)) cardinal
from table (explain(NULL,'XX'))
order by 1 desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##define unnest8_Q1
    stmt = """prepare xx from select A
from  T1
where b in (select T2.d
from T2
where T1.A = T2.C)
AND
T1.B >= 1 ORDER BY A;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #execute explainIt;
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/unnest8.exp""", """Q1_""" + defs.test_id + """""")
    
    ##define unnest8_Q2
    stmt = """prepare xx from select t1.a
from t1
where t1.b in (select t2.d
from t2
where t1.A = t2.c OR t2.c >= 1)ORDER BY A;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    #execute explainIt;
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/unnest8.exp""", """Q2_""" + defs.test_id + """""")
    
    ##define unnest8_Q3
    # Wrong output in Setup2/3
    stmt = """prepare xx from select t1.a
from t1
where t1.b in (select t2.d
from t2
where t1.a = t2.c)
OR
t1.b >= 1 ORDER BY A;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    #execute explainIt;
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/unnest8.exp""", """Q3_""" + defs.test_id + """""")
    
    ##define unnest8_Q4
    stmt = """prepare xx from select t1.a
from t1
where t1.b in (select t2.d
from t2)
OR
t1.b >= 1 ORDER BY A;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    #execute explainIt;
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/unnest8.exp""", """Q4_""" + defs.test_id + """""")
    
    ##define unnest8_Q5
    stmt = """prepare xx from select t1.a
from t1
where t1.b not in (select t2.d
from t2
where t1.a = t2.c) ORDER BY A;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    #execute explainIt;
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/unnest8.exp""", """Q5_""" + defs.test_id + """""")
    
    ##define unnest8_Q6
    # NOT IN with OR inside, uses anti_SemiJoin transformation
    stmt = """prepare xx from select t1.a
from t1
where t1.b not in (select t2.d
from t2
where t1.a = t2.c OR t2.c>= 1)ORDER BY A;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    #execute explainIt;
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    ##define unnest8_Q7
    # NOT IN with AND outside, uses anti_SemiJoin transformation
    stmt = """prepare xx from select t1.a
from t1
where t1.b not in (select t2.c
from t2
where t2.c = t1.a) AND t1.b >= 1 ORDER BY A;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    #execute explainIt;
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/unnest8.exp""", """Q7_""" + defs.test_id + """""")
    
    ##define unnest8_Q8
    # NOT IN with OR outside subquery, requires Join-Agg transformation
    stmt = """prepare xx from select t1.a
from t1
where t1.b not in (select t2.c
from t2
where t2.c = t1.a)
OR
t1.b >= 1 ORDER BY A;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    #execute explainIt;
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/unnest8.exp""", """Q8_""" + defs.test_id + """""")
    
    ##define unnest8_Q9
    # ANY with AND, uses SemiJoin transformation
    stmt = """prepare xx from select t1.a
from t1
where t1.b = any (select t2.c
from t2
where t1.a = t2.c)
AND
t1.b >= 1 ORDER BY A;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    #execute explainIt;
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    ##define unnest8_Q10
    # ANY with OR inside subquery, requires Semijoin transformation
    stmt = """prepare xx from select t1.a
from t1
where t1.b = any (select t2.c
from t2
where t1.a = t2.c OR t2.c >= 1)ORDER BY A;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    #execute explainIt;
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/unnest8.exp""", """Q10_""" + defs.test_id + """""")
    
    ##define unnest8_Q11
    # ANY with OR outside subquery, requires Join-Agg transformation
    stmt = """prepare xx from select t1.a
from t1
where t1.b = any (select t2.c
from t2
where t2.c = t1.a)
OR
t1.b >= 1 ORDER BY A;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    #execute explainIt;
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/unnest8.exp""", """Q11_""" + defs.test_id + """""")
    
    ##define unnest8_Q12
    # simple NOT ANY, uses anti_SemiJoin transformation
    stmt = """prepare xx from select t1.a
from t1
where t1.b <> any (select t2.c
from t2
where t2.c = t1.a) ORDER BY A;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    #execute explainIt;
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/unnest8.exp""", """Q12_""" + defs.test_id + """""")
    
    ##define unnest8_Q13
    # NOT ANY with OR inside, uses anti_SemiJoin transformation
    stmt = """prepare xx from select t1.a
from t1
where t1.b <> any (select t2.c
from t2
where t2.c = t1.a OR t2.c  >= 1)ORDER BY A;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    #execute explainIt;
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/unnest8.exp""", """Q13_""" + defs.test_id + """""")
    
    ##define unnest8_Q14
    # NOT ANY with AND outside, uses anti_SemiJoin transformation
    stmt = """prepare xx from select t1.a
from t1
where t1.b <> any (select t2.c
from t2
where t2.c = t1.b) AND t1.a >= 1 ORDER BY A;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    #execute explainIt;
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    ##define unnest8_Q15
    # NOT ANY with OR outside subquery, requires Join-Agg transformation
    stmt = """prepare xx from select t1.a
from t1
where t1.b <> any (select t2.c
from t2
where t2.c = t1.b)
OR
t1.b >= 1 ORDER BY A;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #execute explainIt;
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/unnest8.exp""", """Q15_""" + defs.test_id + """""")
    
    ##define unnest8_Q16
    # EXISTS with AND, uses SemiJoin transformation
    stmt = """prepare xx from select t1.a
from t1
where exists (select t2.c
from t2
where t2.c = t1.a)
AND
t1.b >= 1 ORDER BY A;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    #execute explainIt;
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/unnest8.exp""", """Q16_""" + defs.test_id + """""")
    
    ##define unnest8_Q17
    # EXISTS with OR inside subquery, requires Semijoin transformation
    stmt = """prepare xx from select t1.a
from t1
where exists (select t2.c
from t2
where t2.c = t1.a OR t2.c >= 1)ORDER BY A;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    #execute explainIt;
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/unnest8.exp""", """Q17_""" + defs.test_id + """""")
    
    ##define unnest8_Q18
    
    # EXISTS with OR outside subquery, requires Join-Agg transformation
    stmt = """prepare xx from select t1.a
from t1
where exists (select t2.c
from t2
where t2.c = t1.a)
OR
t1.b >= 1 ORDER BY A;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    #execute explainIt;
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/unnest8.exp""", """Q18_""" + defs.test_id + """""")
    
    ##define unnest8_Q19
    # EXISTS with AND outside subquery, requires Join-Agg transformation
    stmt = """prepare xx from select t1.a
from t1
where exists (select t2.c
from t2
where t2.c = t1.a)
AND
t1.b >= 1 ORDER BY A;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    #execute explainIt;
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/unnest8.exp""", """Q19_""" + defs.test_id + """""")
    
    ##define unnest8_Q20
    # simple NOT EXISTS, uses Join-Agg transformation
    stmt = """prepare xx from select t1.a
from t1
where not exists (select t2.c
from t2
where t2.c = t1.a) ORDER BY A;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #execute explainIt;
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/unnest8.exp""", """Q20_""" + defs.test_id + """""")
    ##define unnest8_Q21
    # NOT EXISTS with OR inside, uses Join-Agg transformation
    stmt = """prepare xx from select t1.a
from t1
where not exists (select t2.c
from t2
where t2.c = t1.a OR t1.b >= 1)ORDER BY A;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    #execute explainIt;
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/unnest8.exp""", """Q21_""" + defs.test_id + """""")
    ##define unnest8_Q22
    # NOT EXISTS with AND outside, uses Join_Agg transformation
    stmt = """prepare xx from select t1.a
from t1
where not exists (select t2.c
from t2
where t2.c = t1.a) AND t1.b >= 1 ORDER BY A;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    #execute explainIt;
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    ##define unnest8_Q23
    # ALL uses anti_SemiJoin transformation
    stmt = """prepare xx from select t1.a
from t1
where t1.b = all (select t2.c
from t2
where t2.c = t1.b)ORDER BY A ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #execute explainIt;
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/unnest8.exp""", """Q23_""" + defs.test_id + """""")
    ##define unnest8_Q24
    # ALL with AND, uses SemiJoin transformation
    stmt = """prepare xx from select t1.a
from t1
where t1.b = all (select t2.c
from t2
where t1.b = t2.c)
AND
t1.b >= 1 ORDER BY A;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    #execute explainIt;
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/unnest8.exp""", """Q24_""" + defs.test_id + """""")
    ##define unnest8_Q25
    # ALL with OR inside subquery, requires anti_Semijoin transformation
    stmt = """prepare xx from select t1.a
from t1
where t1.b = all (select t2.c
from t2
where t2.c = t1.b OR t1.b = 1) ORDER BY A;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    #execute explainIt;
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/unnest8.exp""", """Q25_""" + defs.test_id + """""")
    
    ##define unnest8_Q26
    # ALL with OR outside subquery, requires Join-Agg transformation
    stmt = """prepare xx from select t1.a
from t1
where t1.b = all (select t2.c
from t2
where t2.c = t1.b)
OR
t1.b >= 1 ORDER BY A;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    #execute explainIt;
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/unnest8.exp""", """Q26_""" + defs.test_id + """""")
    
    ##define unnest8_Q27
    # simple NOT ALL, uses anti_semiJoin transformation
    stmt = """prepare xx from select t1.a
from t1
where t1.b <> all (select t2.c
from t2
where t2.c <> t1.b) ORDER BY A;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    #execute explainIt;
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/unnest8.exp""", """Q27_""" + defs.test_id + """""")
    
    ##define unnest8_Q28
    # NOT ALL with OR inside, uses anti_semijoin transformation
    stmt = """prepare xx from select t1.a
from t1
where t1.b <> all (select t2.c
from t2
where t2.c = t1.b OR t2.D >= 1) ORDER BY A ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    #execute explainIt;
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/unnest8.exp""", """Q28_""" + defs.test_id + """""")
    
    ##define unnest8_Q29
    # NOT ALL with AND outside, uses anti_semijoin transformation
    stmt = """prepare xx from select t1.a
from t1
where t1.b <> all (select t2.c
from t2
where t1.b <> t2.E) AND t1.b >= 1 ORDER BY A;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    #execute explainIt;
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/unnest8.exp""", """Q29_""" + defs.test_id + """""")
    
    ##define unnest8_Q30
    # NOT ALL with OR outside subquery, requires Join-Agg transformation
    stmt = """prepare xx from select t1.a
from t1
where t1.b <> all (select t2.c
from t2
where t2.e = t1.b)
OR
t1.b >= 1 ORDER BY A;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    #execute explainIt;
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/unnest8.exp""", """Q30_""" + defs.test_id + """""")
    
    ##define unnest8_Q31
    stmt = """prepare xx from select t1.a
from t1
where t1.b <> (select max (t2.c)
from t2
where t2.d = t1.a and t2.c <= 9) ORDER BY A;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    #execute explainIt;
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/unnest8.exp""", """Q31_""" + defs.test_id + """""")
    
    ##define unnest8_Q32
    stmt = """prepare xx from select t1.a
from t1
where t1.b <= (select max (t2.d)
from t2
where t2.e = t1.b and t2.d <= 1000 ) ORDER BY A;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    #execute explainIt;
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/unnest8.exp""", """Q32_""" + defs.test_id + """""")
    
    ##define unnest8_Q33
    stmt = """prepare xx from select t1.a from t1
where t1.b <> (select max(t2.c) from
t2 where t2.c = t1.b and
t2.c = (select min(t3.g) from
t3 where t3.f <> t2.c )) ORDER BY A;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    #execute explainIt;
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    ##define unnest8_Q34
    stmt = """prepare xx from select t1.a
from t1
where t1.b = all (select t2.c
from t2
where t2.c <> t1.b)
OR
t1.b >= 1 ORDER BY A;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    #execute explainIt;
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/unnest8.exp""", """Q34_""" + defs.test_id + """""")
    
    ##define unnest8_Q35
    stmt = """prepare xx from select t1.a
from t1
where t1.b = all (select t2.c
from t2
where t1.b = t2.c)
OR
t1.b = 1 ORDER BY A;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #execute explainIt;
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/unnest8.exp""", """Q35_""" + defs.test_id + """""")
    ##define unnest8_Q36
    stmt = """prepare xx from select t1.a
from t1
where t1.b <= (select AVG(t2.c)
from t2
where t1.b = t2.e) ORDER BY A;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    #execute explainIt;
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/unnest8.exp""", """Q36_""" + defs.test_id + """""")
    ##define unnest8_Q37
    stmt = """prepare xx from select t1.a
from t1
where t1.b = (select t2.c
from t2
where t1.b = t2.c) ORDER BY A;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    #execute explainIt;
    ##expectfile ${test_dir}/unnest8.exp Q37_${test_id}
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8401')
    ##define unnest8_Q38
    stmt = """control query default comp_int_77 '33554432' ;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare xx from select t1.a
from t1
where (select t2.c
from t2
where t1.b = t2.c) is null ORDER BY A;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #execute explainIt;
    ##expectfile ${test_dir}/unnest8.exp Q38_${test_id}
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8401')
    stmt = """control query default comp_int_77 'Reset' ;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """drop table T1 cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table T2 cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table T3 cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table T4 cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table T5 cascade;"""
    output = _dci.cmdexec(stmt)
