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
    
def test001(desc="""test053"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test053
    # JClear
    # 2002-08-12
    # Sequence function tests: test for FLOAT
    # 2. moving functions with 2 arguments
    #
    stmt = """select a, cast (b as dec (8, 3)) as col_b,
cast (movingcount (*, 5) as smallint) as mcount_star,
cast (movingsum (b, 5) as dec (12, 3)) as msum_b
from vwseqtb52 
sequence by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test053.exp""", 's1')
    # expect movingcount to go from 1 - 5 with the rest all 5
    # expect movingsum at row 21 = 33655.078, 42 = 53614.999,
    #                         74 = 111604.449, 99 = 151950.064
    
    stmt = """select a, cast (b as dec (8, 3)) as col_b,
cast (movingmax (b, 5) as dec (8, 3)) as mmax_b,
cast (movingmin (b, 5) as dec (8, 3)) as mmin_b
from vwseqtb52 
sequence by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test053.exp""", 's2')
    # expect movingmax at row 6 = 3732.614,  33 = 10821.252,
    #                        49 = 16987.203, 82 = 26378.298
    # expect movingmin        6 = 604.326,   33 = 9473.235,
    #                        49 = 15702.188, 82 = 23989.806
    
    stmt = """select a, cast (b as dec (8, 3)) as col_b,
cast ((movingsum (b, 5) / movingcount (b, 5)) as dec (8, 3)) as myavg,
cast (movingavg (b, 5) as dec (8, 3)) as mvavg_b
from vwseqtb52 
sequence by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test053.exp""", 's3')
    # the last 2 columns should contain identical values
    
    stmt = """select a, cast (b as dec (8, 3)) as col_b,
cast (movingstddev (b, 5) as dec (8, 3)) as mstdev_b,
cast (movingvariance (b, 5) as dec (12, 3)) as mvar_b
from vwseqtb52 
sequence by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test053.exp""", 's4')
    # expect mstdev at row 5 = 1556.560
    # expect mvar at row 5 = 2422878.045
    
    _testmgr.testcase_end(desc)

