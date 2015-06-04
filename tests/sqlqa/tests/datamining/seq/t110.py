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
    
def test001(desc="""test110"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test110
    # jc
    # 2002-08-09
    # Test for the fix to the Average functions:
    # Treat NULL not as a 0 but as a NULL and don't count the row as a row.
    #    create table seqtb107 (a int, b int);
    #
    stmt = """BEGIN WORK;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into seqtb107 values
(1, 2), (2, 3), (3, 4), (4, 5), (5, 6),
(6, 7), (7, 8), (8, 9), (9, 10), (10, 11);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 10)
    
    stmt = """select a, b,
cast (RUNNINGSUM (b) as smallint) as rsum,
cast (RUNNINGCOUNT (b) as smallint) as rcnt,
cast (RUNNINGSUM (b) / RUNNINGCOUNT (b) as dec (8,3)) as cavg,
cast (RUNNINGAVG (b) as dec (8,3)) as ravg
from seqtb107 sequence by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test110.exp""", 's2')
    
    # the last 2 columns should contain identical values
    
    stmt = """select a, b,
cast (MOVINGSUM (b, 3) as smallint) as mvsum,
cast (MOVINGCOUNT (b, 3) as smallint) as mvcnt,
cast ((MOVINGSUM (b, 3) / MOVINGCOUNT (b, 3)) as dec (8,3)) as cavg,
cast (MOVINGAVG (b, 3) as dec (8,3)) as mvavg
from seqtb107 sequence by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test110.exp""", 's3')
    
    # the last 2 columns should contain identical values
    
    stmt = """delete from seqtb107;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into seqtb107 values               -- all zeroes
(1, 0), (2, 0), (3, 0), (4, 0), (5, 0),
(6, 0), (7, 0), (8, 0), (9, 0), (10, 0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 10)
    
    stmt = """select a, b,
cast (RUNNINGSUM (b) as smallint) as rsum,
cast (RUNNINGCOUNT (b) as smallint) as rcnt,
cast (RUNNINGSUM (b) / RUNNINGCOUNT (b) as dec (8,3)) as cavg,
cast (RUNNINGAVG (b) as dec (8,3)) as ravg
from seqtb107 sequence by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test110.exp""", 's5')
    
    # expect all zeroes except the count which runs from 1 - 10
    
    stmt = """select a, b,
cast (MOVINGSUM (b, 3) as smallint) as mvsum,
cast (MOVINGCOUNT (b, 3) as smallint) as mvcnt,
cast ((MOVINGSUM (b, 3) / MOVINGCOUNT (b, 3)) as dec (8,3)) as cavg,
cast (MOVINGAVG (b, 3) as dec (8,3)) as mvavg
from seqtb107 sequence by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test110.exp""", 's6')
    
    # expect all zeroes except the count which runs from 1 - 3, then all threes
    
    stmt = """ROLLBACK WORK;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

