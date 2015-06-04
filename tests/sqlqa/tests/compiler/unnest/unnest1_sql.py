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
    
    ##define unnest1_Q1
    stmt = """prepare XX from SELECT A  FROM T1
WHERE  B <= (SELECT  MAX (C) FROM T2 WHERE T2.D <> T1.A AND T2.E >= 1) Order By A;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    #execute explainIt;
    
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/unnest1.exp""", """Q1_""" + defs.test_id + """""")
    
    ##define unnest1_Q2
    stmt = """PREPARE XX FROM SELECT A FROM T1
WHERE  B <>  (SELECT  MAX (C) FROM T2 WHERE T2.D <> T1.A AND T2.E  >=1) Order By A;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    #execute explainIt;
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/unnest1.exp""", """Q2_""" + defs.test_id + """""")
    
    ##define unnest1_Q3
    stmt = """PREPARE XX FROM SELECT A FROM T1
WHERE  B >  (SELECT  MAX (C) FROM T2 WHERE T2.D <> T1.A AND T2.E  >=1) Order By A;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    #execute explainIt;
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    ##define unnest1_Q4
    stmt = """PREPARE XX FROM SELECT A FROM T1
WHERE  B = (SELECT  MIN (C) FROM T2 WHERE T2.D <> T1.A AND T2.E  >= 1) Order By A;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    #execute explainIt;
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/unnest1.exp""", """Q4_""" + defs.test_id + """""")
    
    ##define unnest1_Q5
    stmt = """PREPARE XX FROM SELECT A FROM T1
WHERE  B <>  (SELECT  MIN (C) FROM T2 WHERE T2.D <> T1.A AND T2.E  >= 1)
Order By A
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    #execute explainIt;
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/unnest1.exp""", """Q5_""" + defs.test_id + """""")
    
    ##define unnest1_Q6
    stmt = """PREPARE XX FROM SELECT A FROM T1
WHERE  B >  (SELECT  MIN (C) FROM T2 WHERE T2.D <> T1.A AND T2.E  >= 1) Order By A;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    #execute explainIt;
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/unnest1.exp""", """Q6_""" + defs.test_id + """""")
    
    ##define unnest1_Q7
    stmt = """PREPARE XX FROM SELECT A FROM T1
WHERE  B = (SELECT  AVG (C) FROM T2 WHERE T2.D <> T1.A AND T2.E  >= 1) Order By A;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    #execute explainIt;
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    ##define unnest1_Q8
    stmt = """PREPARE XX FROM SELECT A FROM T1
WHERE  B <>  (SELECT  AVG (C) FROM T2 WHERE T2.D <> T1.A AND T2.E  >= 1) Order By A;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    #execute explainIt;
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/unnest1.exp""", """Q8_""" + defs.test_id + """""")
    
    ##define unnest1_Q9
    stmt = """PREPARE XX FROM SELECT A FROM T1
WHERE  B <=  (SELECT  AVG (C) FROM T2 WHERE T2.D <> T1.A AND T2.E  >= 1) Order By A;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    #execute explainIt;
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/unnest1.exp""", """Q9_""" + defs.test_id + """""")
    
    ##define unnest1_Q10
    stmt = """PREPARE XX FROM SELECT A FROM T1
WHERE  B <= (SELECT  SUM (C) FROM T2 WHERE T2.D <> T1.A AND T2.E  >= 1) Order By A;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    #execute explainIt;
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/unnest1.exp""", """Q10_""" + defs.test_id + """""")
    
    ##define unnest1_Q11
    stmt = """PREPARE XX FROM SELECT A FROM T1
WHERE  B <>  (SELECT  SUM (C) FROM T2 WHERE T2.D <> T1.A AND T2.E  >= 1) Order By A;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    #execute explainIt;
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/unnest1.exp""", """Q11_""" + defs.test_id + """""")
    
    ##define unnest1_Q12
    stmt = """PREPARE XX FROM SELECT A FROM T1
WHERE  B <>  (SELECT  SUM (C) FROM T2 WHERE T2.D <> T1.A AND T2.E  >= 1) Order By A;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    #execute explainIt;
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/unnest1.exp""", """Q12_""" + defs.test_id + """""")
    
    ##define unnest1_Q13
    stmt = """PREPARE XX FROM SELECT A FROM T1
WHERE  B <= (SELECT  MAX (C) FROM T2 WHERE T2.D <> T1.A AND T2.E  >= 1  OR  T1.A <> T2.D ) Order By A;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    #execute explainIt;
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/unnest1.exp""", """Q13_""" + defs.test_id + """""")
    
    ##define unnest1_Q14
    stmt = """PREPARE XX FROM SELECT A FROM T1
WHERE  B <= (SELECT  MAX (C) FROM T2 WHERE T2.D <> T1.A OR  T2.E  >= 1  OR  T1.A <> T2.D ) Order By A;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    #execute explainIt;
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/unnest1.exp""", """Q14_""" + defs.test_id + """""")
    
    ##define unnest1_Q15
    stmt = """PREPARE XX FROM SELECT A FROM T1
WHERE  B <= (SELECT  MAX (C) FROM T2 WHERE T2.D <> T1.A AND  T2.E  >= 1  AND  T1.A > T2.D ) Order By A;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    #execute explainIt;
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/unnest1.exp""", """Q15_""" + defs.test_id + """""")
    
    ##define unnest1_Q16
    stmt = """PREPARE XX FROM SELECT A FROM T1   WHERE  B <=
(SELECT  MAX (C) FROM T2  WHERE T2.D <> T1.A OR   T2.E  >= 1    OR   T2.D  >
(SELECT AVG(T3.F) FROM  T3  WHERE  T3.G <> T1.A  AND  T3.H <= T2.E)
) Order By A;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    #execute explainIt;
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/unnest1.exp""", """Q16_""" + defs.test_id + """""")
    
    ##define unnest1_Q17
    stmt = """PREPARE XX FROM SELECT A FROM T1  WHERE  B <>
(SELECT  MAX (C) FROM T2  WHERE T2.D <> T1.A OR   T2.E  >= 1    OR   T2.D >
(SELECT AVG(T3.F) FROM T3  WHERE  T3.G <> T1.A  AND  T3.H <= T2. E)
) Order By A;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    #execute explainIt;
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/unnest1.exp""", """Q17_""" + defs.test_id + """""")
    
    ##define unnest1_Q18
    stmt = """PREPARE XX FROM SELECT A FROM T1  WHERE  B <=
(SELECT  MAX (C) FROM T2  WHERE T2.D <> T1.A OR   T2.E  >= 1  OR   T2.D >=
(SELECT AVG(T3.F) FROM T3  WHERE  T3.G = T1.A  AND  T3.H < T2. E)
) Order By A;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    #execute explainIt;
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/unnest1.exp""", """Q18_""" + defs.test_id + """""")
    
    ##define unnest1_Q19
    stmt = """PREPARE XX FROM SELECT A FROM T1  WHERE  B <=
(SELECT  MAX (C) FROM T2  WHERE T2.D <> T1.A OR   T2.E  >= 1    OR   T2.D >
(SELECT AVG(T3.F) FROM T3  WHERE  T3.G = T2.C  AND  T3.H < T2. E) ) Order By A;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    #execute explainIt;
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/unnest1.exp""", """Q19_""" + defs.test_id + """""")
    
    ##define unnest1_Q20
    stmt = """PREPARE XX FROM SELECT A FROM T1  WHERE  B <=
(SELECT  MAX (C) FROM T2  WHERE T2.D <> T1.A OR   T2.E  >= 1    OR   T2.D >
(SELECT AVG(T3.F) FROM T3  WHERE  T3.G = T2.C  AND  T3.H < T2. E) ) Order By A;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    #execute explainIt;
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/unnest1.exp""", """Q20_""" + defs.test_id + """""")
    
    ##define unnest1_Q21
    stmt = """PREPARE XX FROM SELECT A FROM T1  WHERE  B <=
(SELECT  MAX (C) FROM T2  WHERE  T2.D <> T1.A OR   T2.E  >= 1    OR   T2.D >
(SELECT AVG(T3.F) FROM T3  WHERE   T3.H < T2. E  AND  T3.H > T1.A AND T3.G   <
(SELECT  MAX(T4.L) FROM T4  WHERE  T4.J  > T3.G  AND  T3.H < T2. E  AND  T4.K > T2.C  AND  T4.K <  T1.A)
)  ) Order By A;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    #execute explainIt;
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/unnest1.exp""", """Q21_""" + defs.test_id + """""")
    
    ##define unnest1_Q22
    stmt = """PREPARE XX FROM SELECT A FROM T1  WHERE  B <=
(SELECT  MAX (C) FROM T2  WHERE  T2.D <> T1.A OR   T2.E  >= 1    OR   T2.D >
(SELECT AVG(T3.F) FROM T3  WHERE   T3.H < T2. E  AND  T3.H > T1.A AND T3.G   <
(SELECT  MAX(T4.L) FROM T4  WHERE  T4.J  > T3.G  AND  T3.H < T2.E  AND  T4.K > T2.C  AND  T4.K <  T1.A)
)  )
Order By A
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    #execute explainIt;
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/unnest1.exp""", """Q22_""" + defs.test_id + """""")
    
    ##define unnest1_Q23
    stmt = """PREPARE XX FROM SELECT A FROM T1  WHERE  B <= ALL
(SELECT  T2.C FROM T2  WHERE  T2.D <> T1.A OR   T2.E  >= 1    OR   T2.D >  ANY
(SELECT T3.F FROM T3  WHERE   T3.H < T2. E  AND  T3.H > T1.A AND T3.G   <
(SELECT  MAX(T4.L) FROM T4  WHERE  T4.J  > T3.G  AND  T3.H < T2. E  AND  T4.K > T2.C  AND  T4.K <  T1.A  OR  T4. K =
(SELECT  MIN(T5.R) FROM T5 WHERE T5.O > T4.J AND T5.P > T4.K   )
)  )) Order By A;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    #execute explainIt;
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/unnest1.exp""", """Q23_""" + defs.test_id + """""")
    
    ##define unnest1_Q24
    stmt = """PREPARE XX FROM SELECT A FROM T1  WHERE  B <= ALL
(SELECT  T2.C FROM T2  WHERE  T2.D <> T1.A OR   T2.E  >= 10    OR   T2.D >  ANY
(SELECT T3.F FROM T3  WHERE   T3.H < T2. E  AND  T3.H > T1.A AND T3.G   <  ALL
(SELECT  T4.L FROM T4  WHERE  T4.J  > T3.G  AND  T3.H < T2.E  AND  T4.K > T2.C  AND  T4.K <  T1.A  OR  T4.K = ANY
(SELECT  T5.R FROM T5 WHERE T5.O > T4.J AND T5.P > T4.K   )
)  )) Order By A;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    #execute explainIt;
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/unnest1.exp""", """Q24_""" + defs.test_id + """""")
    
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
