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
    
def test001(desc="""test071"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test071
    # Sequence function tests: test for VARNCHAR
    # tests ascending and descending sequence
    # 1. running functions -- count max min
    # 2. moving functions with 2 arguments
    # 3. moving functions with 3 arguments
    #
    stmt = """select count (*) from vwseqtb71;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test071.exp""", 's1')
    # expect count = 100
    
    # sequence ascending
    stmt = """select a, d,
runningcount(d) as rcount_d,
runningmax(d) as rmax_d,
runningmin(d) as rmin_d
from vwseqtb71 
sequence by a asc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test071.exp""", 's2')
    # expect the count to run 1-100
    # expect max at row 6 = 'Bt', 58 = 'Pkfwl', 70 = 'Saetaemk'
    # expect the min at all rows = 'Abdnjitum'
    
    # sequence descending
    stmt = """select a, d,
runningcount(d) as rcount_d,
runningmax(d) as rmax_d,
runningmin(d) as rmin_d
from vwseqtb71 
sequence by a desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test071.exp""", 's3')
    # expect the count to run 1-96 with dupes at 20, 21, 73 & 80
    # expect max at all rows = 'Zyr'
    # expect the min at row 95 = 'Yfjhxkb', 41 = 'Liuihaaq', 4 = 'Bjlbg'
    
    # 2. moving functions -- count max min -- 2 arguments
    # sequence ascending
    stmt = """select a, d,
movingcount(d, 7) as mcount_d,
movingmax(d, 7) as mmax_d,
movingmin(d, 7) as mmin_d
from vwseqtb71 
sequence by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test071.exp""", 's4')
    # expect the count to run 1 - 7, then all 7's
    # expect max at row 6 = 'Bt',  58 = 'Pkfwl', 99 = 'Ztdscgxrtt'
    # expect min at row 6 = 'Abdnjitum', 58 = 'Nvax',   99 = 'Ybdb'
    
    # sequence descending
    stmt = """select a, d,
movingcount(d, 7) as mcount_d,
movingmax(d, 7) as mmax_d,
movingmin(d, 7) as mmin_d
from vwseqtb71 
sequence by a desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test071.exp""", 's5')
    # expect the count to run 1 - 7, then all 7's
    # expect max at row 99 = 'Zyr',  52 = 'Pkfwl', 6 = 'Dl'
    # expect min at row 99 = 'Ztdscgxrtt', 52 = 'Nvax',   6 = 'Bt'
    
    # 3. moving functions -- count max min -- 3 arguments
    # sequence ascending
    stmt = """select a, d,
movingcount(d, 7, 90) as mcount_d,
movingmax(d, 7, 90) as mmax_d,
movingmin(d, 7, 90) as mmin_d
from vwseqtb71 
sequence by a asc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test071.exp""", 's6')
    # expect the count to run 1 - 7, then all 7's (6's at the null points)
    # expect max at row 16 = 'Fcto', 70 = 'Saetaemk', 93 = 'Ybdb'
    # expect min at row 16 = 'Cst',   70 = 'Qfwaalacb',    93 = 'Wp'
    
    # sequence descending
    stmt = """select a, d,
movingcount(d, 7, 90) as mcount_d,
movingmax(d, 7, 90) as mmax_d,
movingmin(d, 7, 90) as mmin_d
from vwseqtb71 
sequence by a desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test071.exp""", 's7')
    # expect the count to run 1 - 7, then all 7's (except at the nulls)
    # expect max at row 93 = 'Ztdscgxrtt', 70 = 'Tkvtkyip', 16 = 'Gm'
    # expect min at row 93 = 'Ybdb',   70 = 'Saetaemk',    16 = 'Fcto'
    
    _testmgr.testcase_end(desc)

