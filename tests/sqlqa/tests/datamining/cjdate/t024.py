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
    
def test001(desc="""test024"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test024
    # JClear
    # 1999-06-02
    # CJDate tests (5th ed. p173): Simple query with between. Exercise 6.4
    # "Get all shipments where the quantity is in the range 300 to 750 inclusive
    #
    stmt = """select snum, pnum, jnum, qty
from spj 
where qty >= 300
and qty <= 750
order by snum, pnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test024.exp""", 's1')
    # expect 11 ordered rows with the following values:
    #      s1     p1      j4            700
    #      s2     p3      j1            400
    #      s2     p3      j4            500
    #      s2     p3      j5            600
    #      s2     p3      j6            400
    #      s3     p4      j2            500
    #      s4     p6      j3            300
    #      s4     p6      j7            300
    #      s5     p5      j4            400
    #      s5     p5      j5            500
    #      s5     p6      j4            500
    
    stmt = """select snum, pnum, jnum, qty
from spj 
where qty between 300 and 750
order by snum, pnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test024.exp""", 's2')
    # expect the same as above
    
    #- select snum, pnum, jnum, qty
    #-   from vpspj
    #-     where qty >= 300
    #-       and qty <= 750
    #-         order by snum, pnum;
    # expect the same as above
    
    #- select snum, pnum, jnum, qty
    #-   from vpspj
    #-     where qty between 300 and 750
    #-       order by snum, pnum;
    # expect the same as above
    
    stmt = """select snum, pnum, jnum, qty
from hpspj 
where qty >= 300
and qty <= 750
order by snum, pnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test024.exp""", 's3')
    # expect the same as above
    
    stmt = """select snum, pnum, jnum, qty
from hpspj 
where qty between 300 and 750
order by snum, pnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test024.exp""", 's4')
    # expect the same as above
    
    _testmgr.testcase_end(desc)

