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
    
def test001(desc="""test047"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test047
    # JClear
    # 1999-03-08
    # Sequence function tests: test for LARGEINT
    # 2. moving functions with 2 arguments
    #
    stmt = """select a, b,
movingcount(b,5) as mcount_b,
cast (movingsum(b,5) as dec (18,0)) as msum_b
from vwseqtb46 
sequence by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test047.exp""", 's1')
    # expect movingcount to go from 1 - 5 and then all fives
    # expect msum at row 9 =  3858525218, 37 = 5299252835, 67 = 785501240
    
    stmt = """select a, b,
movingmax(b,5) as mmax_b,
movingmin(b,5) as mmin_b
from vwseqtb46 
sequence by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test047.exp""", 's2')
    # expect mmax at row 9 = 2114926591, 37 = 2005525393, 67 = 226777108
    # expect mmin at row 9 = 41368546, 37 = 211262085, 67 = 21079259
    
    stmt = """select a, b,
cast (movingsum(b,5) as dec (18,0)) as msum_b,
cast (movingavg(b,5) as dec(18,3)) as mavg_b
from vwseqtb46 
sequence by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test047.exp""", 's3')
    # expect msum at row 9 = 3858525218, 37 = 5299252835, 67 = 785501240
    #      & mavg at row 9 =  771705043, 37 = 1059850567, 67 = 157100248
    
    stmt = """select a, b,
cast (movingstddev(b,5) as dec (18,3)) as mstdev_b,
cast (movingvariance(b,5) as largeint) as mvar_b
from vwseqtb46 
sequence by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test047.exp""", 's4')
    # expect mstddev at 13 = 882300567.277, 47 = 682539587.547, 69 = 712973843.913
    # mvar at 13 = 778454291018435... 47 = 465860288569237... 69 = 508331702105039...
    _testmgr.testcase_end(desc)

