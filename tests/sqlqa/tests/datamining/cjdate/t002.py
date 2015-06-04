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
    
def test001(desc="""test002"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test002
    # JClear
    # 1999-06-01
    # CJDate tests (5th ed. p147): simple queries
    #--------------------------------------------
    #
    stmt = """select pnum
from spj 
order by pnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test002.exp""", 's1')
    # expect 24 rows with the following values in order
    #      p1
    #      p1
    #      p1
    #      p2
    #      p2
    #      p3
    #      p3
    #      p3
    #      p3
    #      p3
    #      p3
    #      p3
    #      p3
    #      p3
    #      p4
    #      p4
    #      p5
    #      p5
    #      p5
    #      p5
    #      p6
    #      p6
    #      p6
    #      p6
    
    #- select pnum
    #-   from vpspj
    #-     order by pnum;
    # expect the same values as above
    
    stmt = """select pnum
from hpspj 
order by pnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test002.exp""", 's2')
    # the same values as above
    
    stmt = """select distinct pnum
from spj 
order by pnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test002.exp""", 's3')
    # expect 6 rows with values P1 - P6
    
    #- select distinct pnum
    #-   from vpspj
    #-     order by pnum;
    # expect 6 rows with values P1 - P6
    
    stmt = """select distinct pnum
from hpspj 
order by pnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test002.exp""", 's4')
    # expect 6 rows with values P1 - P6
    
    _testmgr.testcase_end(desc)

