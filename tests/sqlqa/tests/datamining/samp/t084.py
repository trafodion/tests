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
    
def test001(desc="""test084"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test084
    # JClear
    # 1999-02-02
    # Sampling with group by ... having
    #
    stmt = """select avg(a) from samptb1 
sample random 100 percent rows
group by b
having avg (a) = 20;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test084.exp""", 's1')
    
    stmt = """select avg(a) from samptb1 
sample random 100 percent rows
group by b
having avg (a) = 20.0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test084.exp""", 's2')
    
    # there is non-deterministic from following query, it depends on which 50 rows
    # used for sample
    ##expectfile ${test_dir}/test084.exp s3
    stmt = """select avg(a) from samptb1 
sample first 50 rows
group by b
having avg (a) = 20;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    ##expectfile ${test_dir}/test084.exp s4
    stmt = """select avg(a) from samptb1 
sample first 50 rows
group by b
having avg (a) = 20.0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    _testmgr.testcase_end(desc)

