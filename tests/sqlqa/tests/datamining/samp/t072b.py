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
    
def test001(desc="""test072b"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test072b
    # jclear
    # 1999-01-19
    # messy sampling query with IN and EXISTS as create view
    
    stmt = """create view vwsamp072b as
select empid, salary
from samptb066a 
where empid in
(select empid
from samptb066b 
sample first 5 rows sort by empid)
and exists
(select empid from samptb066a where empid in
(select empid
from samptb066b 
sample first 5 rows sort by empid));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from vwsamp072b 
order by empid;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test072b.exp""", 's2')
    # expect 5 rows like this
    #       123     25000.00
    #      1234     20000.00
    #      2345     36000.00
    #      3455     45000.00
    #      4567     30000.00
    
    # cleanup
    stmt = """drop view vwsamp072b;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

