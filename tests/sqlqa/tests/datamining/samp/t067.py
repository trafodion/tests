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
    
def test001(desc="""test067"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test067
    # DDunn
    # 1999-01-18
    # Sampling test with join and insert-select
    # depends on tables samptb066a, b & c created in test066
    #
    # check the straight data first
    stmt = """select s.empid, s.salary, e.datehired
from samptb066a s, samptb066b e
where s.empid = e.empid and datehired < date '2000-01-01'
order by s.empid;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test067.exp""", 's1')
    # expect 12 rows with the following values in order of the 1st column:
    #         123     25000.00  1999-01-01
    #        1234     20000.00  1979-12-12
    #        2345     36000.00  1987-07-29
    #        3455     45000.00  1991-01-01
    #        4900     45000.00  1997-03-06
    #        5678     50000.00  1983-12-01
    #        6234     20000.00  1976-04-04
    #        6789     55000.00  1990-09-07
    #        6798     60000.00  1986-03-04
    #        8901     40000.00  1993-04-05
    #        9012     40000.00  1940-10-04
    #        9123     20050.00  1995-01-15
    
    stmt = """delete from samptb066c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 0)
    # making sure the scratch table is empty
    
    # do the insert-select
    stmt = """insert into samptb066c 
select s.empid, s.salary, e.datehired
from samptb066a s, samptb066b e
where s.empid = e.empid and datehired < date '2000-01-01'
sample first 9 rows sort by s.empid, s.salary, e.empid
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 9)
    # pass if 9 rows inserted
    
    stmt = """select id, cast (pay as dec (15,2)), hiredate
from samptb066c 
order by id;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test067.exp""", 's4')
    # expect the first 9 rows of the data above
    
    # cleanup
    stmt = """delete from samptb066c;"""
    output = _dci.cmdexec(stmt)
    # pass if 9 rows deleted
    
    _testmgr.testcase_end(desc)

