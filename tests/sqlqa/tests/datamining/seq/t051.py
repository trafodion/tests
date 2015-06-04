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
    
def test001(desc="""test051"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test051
    # Sequence function tests: test for BIT PRECISION INT
    # 3. moving functions with 3 arguments
    #
    stmt = """select a, b,
movingcount(b,5,150) as mcount_b,
movingsum(b,5,150) as msum_b
from vwseqtb49 
sequence by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test051.exp""", 's1')
    # expect movingcount to go from 1 - 5 and then all fives, dropping to
    #    fours on rows 13-17 and 66-70
    # expect movingsum at row 14 = 17653, 42 = 68313, 67 = 89053, 99 = 159492
    
    stmt = """select a, b,
movingmax(b,5,150) as mmax_b,
movingmin(b,5,150) as mmin_b
from vwseqtb49 
sequence by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test051.exp""", 's2')
    # expect movingmax at row 6 = 1526, 33 = 11795, 49 = 166565, 82 = 26239
    # expect movingmin        6 = 453,  33 = 11256, 49 = 15269,  82 = 24826
    
    stmt = """select a, b,
movingsum(b,5,150) as msum_b,
cast(movingavg(b,5,150) as dec(18,3)) as mavg_b
from vwseqtb49 
sequence by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test051.exp""", 's3')
    # expect movingsum at row 15 = 20078, 39 = 64511, 68 = 91047, 99 = 159492
    #    & movingavg at row 15 = 5019.5, 39 = 12902.2, 68 = 22761.75, 99 = 31898.4
    
    stmt = """select a, b,
cast (movingstddev(b,5,150) as dec (18,3)) as mstdev_b,
cast (movingvariance(b,5,150) as dec (18,3)) as mvar_b
from vwseqtb49 
sequence by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test051.exp""", 's4')
    # expect mstddev at row 20 = 836.132, 55 = 449.935, 90 = 423.214
    # expect mvar at row 20 = 699117.5, 55 = 202441.5, 90 = 179109.7
    
    _testmgr.testcase_end(desc)

