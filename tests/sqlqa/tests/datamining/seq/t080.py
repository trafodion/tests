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
    
def test001(desc="""test080"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test080
    # JClear
    # 1998-11-18
    # Sequence functions: running function tests for IN, NOT IN
    #
    # IN
    stmt = """select a, b,
runningcount(*) as rcount_star,
runningcount(b) as rcount_b,
runningsum(b) as rsum_b
from vwseqtb40 
where a IN (
select a
from vwseqtb40 
where a is not null and a <= 50)
sequence by a asc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test080.exp""", 's1')
    # expect the count(*) to run from 1-50
    # expect the count(b) to run from 1-49 with a dupe at row 29
    # expect the sum at row 16 = 40737, 32 = 14667, 49 = 343651
    
    stmt = """select a, b,
runningcount(*) as rcount_star,
runningcount(b) as rcount_b,
runningsum(b) as rsum_b
from vwseqtb40 
where a NOT IN (
select a
from vwseqtb40 
where a is not null and a >= 50)
sequence by a asc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test080.exp""", 's2')
    # expect the count(*) to run from 1-49
    # expect the count(b) to run from 1-48 with a dupe at row 29
    # expect the sum at row 16 = 40737, 32 = 14667, 49 = 343651
    
    stmt = """select a, b,
runningcount(*) as rcount_star,
runningcount(b) as rcount_b,
runningsum(b) as rsum_b
from vwseqtb40 
where NOT (a IN (
select a
from vwseqtb40 
where a is not null and a >= 50))
sequence by a asc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test080.exp""", 's3')
    # expect the count(*) to run from 1-49
    # expect the count(b) to run from 1-48 with a dupe at row 29
    # expect the sum at row 16 = 40737, 32 = 14667, 49 = 343651
    
    _testmgr.testcase_end(desc)

