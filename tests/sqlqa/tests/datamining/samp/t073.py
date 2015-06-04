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
    
def test001(desc="""test073"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test073
    # DDunn
    # 1999-01-18
    # Testing sampling on a table with an index.
    #
    stmt = """create index ixsamp066a on samptb066a (salary);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index ixsamp066b on samptb066b (datehired);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select samptb066a.empid, samptb066a.salary
from samptb066a 
where samptb066a.empid in
(select samptb066b.empid
from samptb066b 
sample first 7 rows
sort by empid)
order by empid;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test073.exp""", 's3')
    # expect 7 rows with these values
    #        123     25000.00
    #       1234     20000.00
    #       2345     36000.00
    #       3455     45000.00
    #       4567     30000.00
    #       4900     45000.00
    #       5678     50000.00
    
    stmt = """select samptb066a.empid, samptb066a.salary
from samptb066a 
where samptb066a.empid in
(select samptb066b.empid
from samptb066b)
sample first 7 rows
sort by empid
order by empid;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test073.exp""", 's4')
    # expect the same 7 rows as above
    
    stmt = """select samptb066a.empid, samptb066a.salary
from samptb066a 
where samptb066a.empid in
(select samptb066b.empid
from samptb066b 
sample periodic 2 rows every 4 rows
sort by empid)
order by empid;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test073.exp""", 's5')
    # expect 7 rows with these values
    #        123     25000.00
    #       1234     20000.00
    #       4567     30000.00
    #       4900     45000.00
    #       6789     55000.00
    #       6798     60000.00
    #       9123     20050.00
    
    stmt = """select empid, salary
from samptb066a 
sample first 3 rows sort by salary, empid
order by salary, empid;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test073.exp""", 's6')
    # expect 3 rows with these values:
    #        1234     20000.00
    #        6234     20000.00
    #        9123     20050.00
    
    stmt = """drop index ixsamp066a;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index ixsamp066b;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

