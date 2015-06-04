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
    
def test001(desc="""test062"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test062
    # JClear
    # 2002-08-16
    # Sequence function tests: test for DECIMAL
    # 2. moving functions with 2 arguments
    #
    stmt = """select a, b,
cast (movingcount (*, 5) as smallint) as mcount_star,
movingsum (b, 5) as msum_b
from vwseqtb61 
sequence by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test062.exp""", 's1')
    # expect movingcount to go from 1 - 5 with the rest all 5
    # expect movingsum at row 21 = 72276.078, 42 = 71123.008,
    #                         74 = 80186.601, 99 = 100252.897
    
    stmt = """select a, b,
movingmax (b, 5) as mmax_b,
movingmin (b, 5) as mmin_b
from vwseqtb61 
sequence by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test062.exp""", 's2')
    # expect movingmax at row 6 = 31632.134,  33 = 26301.836,
    #                        49 = 31710.172,  82 = 30669.535
    # expect movingmin        6 = 3672.279,   33 = 2353.169,
    #                        49 = 1239.321,   82 = 7991.768
    
    stmt = """select a, b,
movingsum (b, 5) / movingcount (b, 5) as myavg,
movingavg (b, 5) as mvavg_b
from vwseqtb61 
sequence by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test062.exp""", 's3')
    # the last 2 columns should contain identical values
    
    stmt = """select a, b,
cast (movingstddev (b, 5) as dec (8, 3)) as mstdev_b,
cast (movingvariance (b, 5) as dec (12, 3)) as mvar_b
from vwseqtb61 
sequence by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test062.exp""", 's4')
    # expect mstdev at row 5 = 14819.848
    # expect mvar at row 5 = 219627882.800
    
    _testmgr.testcase_end(desc)

