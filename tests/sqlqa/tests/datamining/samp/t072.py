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
    
def test001(desc="""test072"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test072
    # DDunn
    # 1999-01-18
    # Testing sampling within a view.
    # Creating the same type of view twice with the random verb.
    # The views should theoretically consist of different rows.
    #
    
    stmt = """update statistics for table samptb066a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test072.exp""", 's1')
    stmt = """update statistics for table samptb066b;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create view vwsamp072a (id, pay) as
select empid, salary
from samptb066a 
where empid in
(select empid
from samptb066b 
sample random 50 percent);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test072.exp""", 's2')
    
    stmt = """select * from vwsamp072a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test072.exp""", 's3')
    
    stmt = """create view vwsamp072b as
select empid, salary
from samptb066a 
where empid in
(select empid
from samptb066b 
sample random 50 percent);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test072.exp""", 's4')
    
    stmt = """select * from vwsamp072b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test072.exp""", 's5')
    
    # cleanup
    stmt = """drop view vwsamp072a;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop view vwsamp072b;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

