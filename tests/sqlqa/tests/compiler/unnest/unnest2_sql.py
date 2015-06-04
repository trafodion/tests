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
    
    ##define unnest2_Q1
    stmt = """PREPARE XX FROM SELECT A  FROM T1
WHERE  B  IN   (SELECT  MAX (C)  FROM T2 )Order By A;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    #execute explainIt;
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    ##define unnest2_Q2
    stmt = """PREPARE XX FROM SELECT A FROM T1
WHERE  B  IN   (SELECT  C  FROM T2  )Order By A;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    #execute explainIt;
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/unnest2.exp""", """Q2_""" + defs.test_id + """""")
    
    ##define unnest2_Q3
    stmt = """PREPARE XX FROM SELECT A FROM T1
WHERE  B  IN   (SELECT  MIN (C)  FROM T2  )Order By A;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    #execute explainIt;
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/unnest2.exp""", """Q3_""" + defs.test_id + """""")
    
    ##define unnest2_Q4
    stmt = """PREPARE XX FROM SELECT A FROM T1
WHERE  B  NOT IN   (SELECT  SUM (C)  FROM T2 )Order By A;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    #execute explainIt;
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/unnest2.exp""", """Q4_""" + defs.test_id + """""")
    
    ##define unnest2_Q5
    stmt = """PREPARE XX FROM SELECT A FROM T1
WHERE  B  NOT  IN   (SELECT  C   FROM T2  )Order By A;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    #execute explainIt;
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/unnest2.exp""", """Q5_""" + defs.test_id + """""")
    
    ##define unnest2_Q6
    stmt = """PREPARE XX FROM SELECT A FROM T1
WHERE  B NOT  IN   (SELECT  MAX (C) FROM T2  )Order By A;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    #execute explainIt;
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/unnest2.exp""", """Q6_""" + defs.test_id + """""")
    
    ##define unnest2_Q7
    stmt = """PREPARE XX FROM SELECT A FROM T1
WHERE   EXISTS   (SELECT  MAX (C)  FROM T2  )Order By A;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    #execute explainIt;
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/unnest2.exp""", """Q7_""" + defs.test_id + """""")
    
    ##define unnest2_Q8
    stmt = """PREPARE XX FROM SELECT A FROM T1
WHERE   EXISTS  (SELECT   AVG(E)  FROM T2  WHERE  T1.B <> T2.D  )Order By A;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    #execute explainIt;
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/unnest2.exp""", """Q8_""" + defs.test_id + """""")
    
    ##define unnest2_Q9
    stmt = """PREPARE XX FROM SELECT A FROM T1
WHERE   EXISTS   (SELECT  E  FROM T2  WHERE T1.B <> T2.D )Order By A;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    #execute explainIt;
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/unnest2.exp""", """Q9_""" + defs.test_id + """""")
    
    ##define unnest2_Q10
    stmt = """PREPARE XX FROM SELECT A FROM T1
WHERE  NOT  EXISTS   (SELECT  C, D  FROM T2 )Order By A;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    #execute explainIt;
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    ##define unnest2_Q11
    stmt = """PREPARE XX FROM SELECT A FROM T1
WHERE  NOT  EXISTS   (SELECT  MAX (C) , MIN (D), AVG(E)  FROM T2  )Order By A;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    #execute explainIt;
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    ##define unnest2_Q12
    stmt = """PREPARE XX FROM SELECT A FROM T1
WHERE  NOT  EXISTS   (SELECT  SUM(E) FROM T2  )Order By A;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    #execute explainIt;
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
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
