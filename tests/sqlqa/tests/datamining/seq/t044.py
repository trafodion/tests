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
    
def test001(desc="""test044"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test044
    # JClear
    # 1999-03-03
    # Sequence function tests: test for SMALLINT
    # 2. moving functions with 2 arguments
    #
    stmt = """select a, c,
movingcount(c,5) as mcount_c,
movingsum(c,5) as msum_c
from vwseqtb43 
sequence by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test044.exp""", 's1')
    # expect movingcount to go from 1 - 5 and then all fives, dropping to
    #    fours on rows 53-56 and 85-89
    # expect movingsum at row 14 = 25210, 42 = 74677, 66 = 111587, 99 = 157408
    
    stmt = """select a, c,
movingmax(c,5) as mmax_c,
movingmin(c,5) as mmin_c
from vwseqtb43 
sequence by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test044.exp""", 's2')
    # expect movingmax at row 13 = 5573, 33 = 12483, 66 = 22634, 82 = 26517
    # expect movingmin        13 = 3740, 33 = 11402, 66 = 22196, 82 = 24553
    
    stmt = """select a, c,
movingsum(c,5) as msum_c,
cast(movingavg(c,5) as dec(18,3)) as mavg_c
from vwseqtb43 
sequence by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test044.exp""", 's3')
    # expect movingsum at row 14 = 25210, 42 = 74677, 66 = 111587, 99 = 157408
    #      & mvavg at row 14 = 5042, 39 = 13791, 66 = 22317.4, 99 = 31481.6
    
    stmt = """select a, c,
cast (movingstddev(c,5) as dec (18,3)) as mstdev_c,
cast (movingvariance(c,5) as dec (18,3)) as mvar_c
from vwseqtb43 
sequence by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test044.exp""", 's4')
    # expect mstddev at row 14 = 765.221, 55 = 8360.736, 89 = 12492.939
    # expect mvar at row 14 = 585562.5, 55 = 69901901.3, 89 = 156073514.3
    
    _testmgr.testcase_end(desc)

