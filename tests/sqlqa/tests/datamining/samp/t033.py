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
    
def test001(desc="""test033"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test033
    # JClear
    # 1999-01-14
    # Sampling tests: random sampling on an empty table
    #
    stmt = """select count (*) from vwsamptb33 
sample random 300 percent
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test033.exp""", 's1')
    # expect count = 0
    
    stmt = """select count (*) from vwsamptb33 
sample random 300 percent rows
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test033.exp""", 's2')
    # expect count = 0
    
    # expect all nulls from the following queries
    stmt = """select cast (avg (d) as dec (18,3)) as average,
cast (variance (d) as dec (18,3))as var,
cast (stddev (d) as dec (18,3)) as stnddev
from vwsamptb33 
sample random 30 percent;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test033.exp""", 's3')
    
    stmt = """select cast (avg (d) as dec (18,3)) as average,
cast (variance (d) as dec (18,3)) as var,
cast (stddev (d) as dec (18,3)) as stnddev
from vwsamptb33 
sample random 30 percent rows;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test033.exp""", 's4')
    
    stmt = """select sum (d) / 10
from vwsamptb33;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test033.exp""", 's5')
    
    stmt = """select sum (d) from vwsamptb33 
sample random 10 percent rows;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test033.exp""", 's6')
    
    _testmgr.testcase_end(desc)

