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

#Case statements not tested in the previous test
def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci
    
    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()
    
def test001(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #Positive tests will be written for different kind of datatypes in case stmt.
    
    #Datatype char
    stmt = """Select case
when last_name='CLARK' then 'Programmer'
when last_name='CRINAR' then 'Analyst'
else 'Intern'
end
from emp1
group by
case
when last_name='CLARK' then 'Programmer'
when last_name='CRINAR' then 'Analyst'
else 'Intern'
end;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a01s1""")
    
    #Datatype character varying
    stmt = """Select case
when job_code='Programmer' then 'Programming'
when job_code='Analyst' then 'Analyse problems'
else 'Help Out'
end
from emp1
group by
case
when job_code='Programmer' then 'Programming'
when job_code='Analyst' then 'Analyse problems'
else 'Help Out'
end;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a01s2""")
    
    #Data type varchar
    stmt = """Select case
when responsible='Programming' then 80000
when responsible='Analyse problems' then 50000
else 35000
end
from emp1
group by
case
when responsible='Programming' then 80000
when responsible='Analyse problems' then 50000
else 35000
end;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a01s3""")
    
    #Data type numeric
    stmt = """Select case
when salary=80000 then 'CLARK'
when salary=50000 then 'CRINAR'
else 'GREEN'
end
from emp1
group by
case
when salary=80000 then 'CLARK'
when salary=50000 then 'CRINAR'
else 'GREEN'
end;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a01s4""")
    
    #Data type smallint
    stmt = """Select case
when employee_id=10 then 1
when employee_id=20 then 2
else 1
end
from emp2
group by
case
when employee_id=10 then 1
when employee_id=20 then 2
else 1
end;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a01s5""")
    
    #Data type int
    stmt = """Select case
when marital_status=1 then 1000
when marital_status=2 then 1500
else 1300
end
from emp2
group by
case
when marital_status=1 then 1000
when marital_status=2 then 1500
else 1300
end;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a01s6""")
    
    #Data type large int
    stmt = """Select case
when bonus=1000 then 10
when bonus=1500 then 15
else 12
end
from emp2
group by
case
when bonus=1000 then 10
when bonus=1500 then 15
else 12
end;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a01s7""")
    
    #Data type dec
    stmt = """Select case
when vacation=10 then 400
when vacation=20 then 300
else 200
end
from emp2
group by
case
when vacation=10 then 400
when vacation=20 then 300
else 200
end;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a01s8""")
    
    #Data type float
    stmt = """Select case
when tax=400 then 300
when tax=300 then 250
else 150
end
from emp2
group by
case
when tax=400 then 300
when tax=300 then 250
else 150
end;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a01s9""")
    
    #Data type real
    stmt = """Select case
when retire=300 then 'a'
when retire=250 then 'b'
else 'c'
end
from emp2
group by
case
when retire=300 then 'a'
when retire=250 then 'b'
else 'c'
end;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a01s10""")
    
    #Data type char
    stmt = """Select case
when code='a' then 10
when code='b' then 20
else 30
end
from emp2
group by
case
when code='a' then 10
when code='b' then 20
else 30
end;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a01s11""")
    
    #Data type double precision
    stmt = """Select case
when col1=30 then '1998-04-03'
when col1=25 then '1999-05-06'
else '2000-01-02'
end
from emp3
group by
case
when col1=30 then '1998-04-03'
when col1=25 then '1999-05-06'
else '2000-01-02'
end;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a01s12""")
    
    #Data type date
    stmt = """Select case
when hire_date= DATE '1998-04-03' then '08:30:30'
when hire_date= DATE '1999-05-06' then '08:45:00'
else '09:00:00'
end
from emp3
group by
case
when hire_date= DATE '1998-04-03' then '08:30:30'
when hire_date= DATE '1999-05-06' then '08:45:00'
else '09:00:00'
end;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a01s13""")
    
    #Data type time
    stmt = """Select case
when start_time=TIME '08:30:30' then '2007-06-01:16:30:30'
when start_time=TIME '08:45:00' then '2007-06-01:16:45:00'
else '2007-06-01:17:15:30'
end
from emp3
group by
case
when start_time=TIME '08:30:30' then '2007-06-01:16:30:30'
when start_time=TIME '08:45:00' then '2007-06-01:16:45:00'
else '2007-06-01:17:15:30'
end;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a01s14""")
    
    #Data type timestamp
    stmt = """Select case
when end_time=TIMESTAMP '2007-06-01:16:30:30' then INTERVAL '9-03'  YEAR TO MONTH
when end_time=TIMESTAMP '2007-06-01:16:45:00' then INTERVAL '8-01'  YEAR TO MONTH
else INTERVAL '7-05'  YEAR TO MONTH
end
from emp3
group by
case
when end_time=TIMESTAMP '2007-06-01:16:30:30' then INTERVAL '9-03'  YEAR TO MONTH
when end_time=TIMESTAMP '2007-06-01:16:45:00' then INTERVAL '8-01'  YEAR TO MONTH
else INTERVAL '7-05'  YEAR TO MONTH
end;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a01s15""")
    
    #Data type interval year to month
    stmt = """Select case
when experience=INTERVAL '9-03'  YEAR TO MONTH then 10
when experience=INTERVAL '8-01'  YEAR TO MONTH then 20
else 30
end
from emp3
group by
case
when experience=INTERVAL '9-03'  YEAR TO MONTH then 10
when experience=INTERVAL '8-01'  YEAR TO MONTH then 20
else 30
end;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a01s16""")
    
    _testmgr.testcase_end(desc)

def test002(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #Negative tests having different set in case & group by
    stmt = """Select case
when last_name='CLARK' then 'Programmer'
when last_name='CRINAR' then 'Analyst'
else 'Intern'
end
from emp1
group by
case
when last_name='CLARK' then 'Programmer'
else 'Intern'
end;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4197')
    
    #Negative test containing subquery in groupby
    stmt = """Select case
when job_code=(select job_code from emp1 where last_name='CLARK') then 'Programming'
end
from emp1
where last_name in ( Select last_name from emp1)
group by
case
when job_code=(select job_code from emp1 where last_name='CLARK') then 'Programming'
end;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4197')
    
    #Try case stmt without else
    stmt = """Select case
when responsible='Programming' then 80000
when responsible='Analyse problems' then 50000
end
from emp1
group by
case
when responsible='Programming' then 80000
when responsible='Analyse problems' then 50000
end;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a02s3""")
    
    #Try with only one case
    stmt = """Select case
when employee_id=10 then 1
end
from emp2
group by
case
when employee_id=10 then 1
end;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a02s4""")
    
    #Use of Case (with  values) with other string functions.
    stmt = """Select case
when ASCII(code)<99 then 1000
when ASCII(code)=99 then 1500
else ASCII(code)
end
from emp2
group by
case
when ASCII(code)<99 then 1000
when ASCII(code)=99 then 1500
else ASCII(code)
end;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a02s5""")
    
    _testmgr.testcase_end(desc)

def test003(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #Use of Case (with search conditions)
    stmt = """Select case
when vacation=10 then 400
when vacation=20 then 300
else 200
end
from emp2 where vacation>5
group by
case
when vacation=10 then 400
when vacation=20 then 300
else 200
end;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a03s1""")
    
    #Use of Case (with  values) with aggregates.
    stmt = """Select case
when tax=400 then min(retire)
when tax=300 then max(retire)
else retire
end
from emp2
group by
case
when tax=400 then min(retire)
when tax=300 then max(retire)
else retire
end;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4197')
    
    #Use of Case with   IN clause.
    stmt = """Select case
when col1=30 then '1998-04-03'
when col1=25 then '1999-05-06'
else '2000-01-02'
end
from emp3
where col1 in (30, 25,65)
group by
case
when col1=30 then '1998-04-03'
when col1=25 then '1999-05-06'
else '2000-01-02'
end;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a03s3""")
    
    #Use of Case (search  condition) in Use with nulls.
    stmt = """Select case
when end_time=TIMESTAMP '2007-06-01:16:30:30' then INTERVAL '9-03'  YEAR TO MONTH
when end_time=TIMESTAMP '2007-06-01:16:45:00' then INTERVAL '8-01'  YEAR TO MONTH
else NULL
end
from emp3
group by
case
when end_time=TIMESTAMP '2007-06-01:16:30:30' then INTERVAL '9-03'  YEAR TO MONTH
when end_time=TIMESTAMP '2007-06-01:16:45:00' then INTERVAL '8-01'  YEAR TO MONTH
else NULL
end;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a03s4""")
    
    #Use tests for combination   of different data types in CASE.
    stmt = """Select case
when experience=INTERVAL '9-03'  YEAR TO MONTH AND col1=30 then 10
when experience=INTERVAL '8-01'  YEAR TO MONTH AND col1=25 then 20
else 30
end
from emp3
group by
case
when experience=INTERVAL '9-03'  YEAR TO MONTH AND col1=30 then 10
when experience=INTERVAL '8-01'  YEAR TO MONTH AND col1=25 then 20
else 30
end;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a03s5""")
    _testmgr.testcase_end(desc)

