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
    
def test001(desc="""test042"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test042
    # Sequence function tests: test for INT
    # 3. moving functions with 3 arguments
    #
    stmt = """select a, b,
movingcount(*,5,150) as mcount_star,
movingsum(b,5,150) as msum_b
from vwseqtb40 
sequence by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test042.exp""", 's1')
    # expect movingcount to go from 1 - 5 and then remain all fives
    # expect movingsum at row 29 = 29726, 42 = 56035, 71 = 82806, 99 = 156588
    
    stmt = """select a, b,
movingmax(b,5,150) as mmax_b,
movingmin(b,5,150) as mmin_b
from vwseqtb40 
sequence by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test042.exp""", 's2')
    # expect movingmax at row 6 = 1223, 29 = 7577, 49 = 14585, 82 = 24703
    # expect movingmin        6 = 74,   29 = 7311, 49 = 12630, 82 = 23375
    
    stmt = """select a, b,
movingcount(b,5,150) as mcount_b,
cast(movingavg(b,5,150) as dec(18,3)) as mavg_b
from vwseqtb40 
sequence by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test042.exp""", 's3')
    # expect movingcount to go from 1 - 5 and then remain all fives
    #    (except at the null rows where it should have 5 rows with 4)
    # expect mvg. avg at 29 = 7431.5, 39 = 10128.8, 71 = 20726.5, 99 = 31317.6
    
    stmt = """select a, b,
cast (movingstddev(b,5,150) as dec (18,3)) as mstdev_b,
cast (movingvariance(b,5,150) as dec (18,3)) as mvar_b
from vwseqtb40 
sequence by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test042.exp""", 's4')
    # expect mstdev at row 7 = 372.083, 34 = 643.745, 80 = 399.447
    # expect mvar at row 7 = 138445.8, 34 = 414407.0, 80 = 159558.2
    
    _testmgr.testcase_end(desc)

