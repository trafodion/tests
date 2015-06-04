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
    
def test001(desc="""test070"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test070
    # Sequence function tests: test for NCHAR
    # 1. running functions -- count max min
    # 2. moving functions with 2 arguments
    # 3. moving functions with 3 arguments
    #
    stmt = """select count (*) from vwseqtb70;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test070.exp""", 's1')
    # expect count = 100
    
    stmt = """select a, b,
runningcount(*) as rcount_star,
runningcount(b) as rcount_b,
runningmax(b) as rmax_b,
runningmin(b) as rmin_b
from vwseqtb70 
sequence by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test070.exp""", 's2')
    # expect the count(*) to run from 1-100
    # expect the count(b) to run from 1-93, with dupes at the null rows
    # expect max at row 10 = 'Cnfwjsbmgg', 55 = 'Ndgmbrssyk', 90 = 'Wosexcnfqw'
    # expect the min at all rows = 'Aedrmcurrb'
    
    # 2. moving functions -- count max min -- 2 arguments
    stmt = """select a, b,
movingcount(b, 6) as mcount_b,
movingmax(b, 6) as mmax_b,
movingmin(b, 6) as mmin_b
from vwseqtb70 
sequence by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test070.exp""", 's3')
    # expect the count to run 1 - 6, then all 6's, except 5's at the nulls
    # expect max at row 10 = 'Cnfwjsbmgg', 55 = 'Ndgmbrssyk', 90 = 'Wosexcnfqw'
    # expect min at row 10 = 'Bcfqvgueye', 55 = 'Mtsplrcpep', 90 = 'Vxsdbrnbdr'
    
    # 3. moving functions -- count max min -- 3 arguments
    stmt = """select a, b,
movingcount(b, 6, 90) as mcount_b,
movingmax(b, 6, 90) as mmax_b,
movingmin(b, 6, 90) as mmin_b
from vwseqtb70 
sequence by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test070.exp""", 's4')
    # expect the count to run 1 - 6, then all 6's, except 5's at the nulls
    # expect max at row 10 = 'Cnfwjsbmgg', 55 = 'Ndgmbrssyk', 90 = 'Wosexcnfqw'
    # expect min at row 10 = 'Bcfqvgueye', 55 = 'Mtsplrcpep', 90 = 'Vxsdbrnbdr'
    
    _testmgr.testcase_end(desc)

