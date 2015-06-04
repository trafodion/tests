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
    
def test001(desc="""test069"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test069
    # JClear
    # 1998-11-05
    # Sequence function tests: test for VARCHAR(10)
    # 1. running functions -- count max min
    # 2. moving functions with 2 arguments
    # 3. moving functions with 3 arguments
    #
    stmt = """select count (*) from vwseqtb69;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test069.exp""", 's1')
    # expect count = 100
    
    stmt = """select a, d,
runningcount(d) as rcount_d,
runningmax(d) as rmax_d,
runningmin(d) as rmin_d
from vwseqtb69 
sequence by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test069.exp""", 's2')
    # expect the count to run 1-94 with dupes at rows 27, 59, 60, 66, 83 & 100
    # expect max at row 6 = 'Bt', 59 = 'Pkfwl', 70 = 'Saetaemk'
    # expect the min at all rows = 'Abdnjitum'
    
    # 2. moving functions -- count max min -- 2 arguments
    stmt = """select a, d,
movingcount(d, 5) as mcount_d,
movingmax(d, 5) as mmax_d,
movingmin(d, 5) as mmin_d
from vwseqtb69 
sequence by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test069.exp""", 's3')
    # expect the count to run 1 - 5, then all 5's (-1 at each null)
    # expect max at row 6 = 'Bt',  59 = 'Pkfwl', 99 = 'Ztdscgxrtt'
    # expect min at row 6 = 'Aut', 59 = 'Olr',   99 = 'Yfjhxkb'
    
    # 3. moving functions -- count max min -- 3 arguments
    stmt = """select a, d,
movingcount(d, 5, 90) as mcount_d,
movingmax(d, 5, 90) as mmax_d,
movingmin(d, 5, 90) as mmin_d
from vwseqtb69 
sequence by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test069.exp""", 's4')
    # expect the count to run 1 - 5, then all 5's (-1 at each null)
    # expect max at row 16 = 'Fcto', 70 = 'Saetaemk', 93 = 'Ybdb'
    # expect min at row 16 = 'Dl',   70 = 'Rkqcw',    93 = 'Xfi'
    
    _testmgr.testcase_end(desc)

