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
    
def test001(desc="""test013"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test013
    # maxmin.sql
    # jclear
    # 1997-04-28
    # new aggregate tests
    # tests AVG, COUNT, & SUM on a table containing 100 rows.
    # with INT_MIN, INT_MAX, SMALLINT_MIN, & SMALLINT_MAX values.
    
    stmt = """select
avg (minint),
sum (minint)
from minmax;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test013exp""", 'test013a')
    # expect 1 row with the following values:
    # 	-1911260452.2300000000000000000  -191126045223
    
    stmt = """select
count (minint),
sum (minint) / count (minint)
from minmax;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test013exp""", 'test013b')
    # expect 1 row with the following values:
    # 	100  -1911260452.2300000000000000000
    
    stmt = """select
avg (maxint),
sum (maxint)
from minmax;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test013exp""", 'test013c')
    # expect 1 row with the following values:
    # 	1911260451.3400000000000000000  191126045134
    
    stmt = """select
count (maxint),
sum (maxint) / count (maxint)
from minmax;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test013exp""", 'test013d')
    # expect 1 row with the following values:
    # 	100   1911260451.3400000000000000000
    
    stmt = """select
avg (minsmall),
sum (minsmall)
from minmax;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test013exp""", 'test013e')
    # expect 1 row with the following values:
    # 	-29169.0300000000000000000   -2916903
    
    stmt = """select
count (minsmall),
sum (minsmall) / count (minsmall)
from minmax;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test013exp""", 'test013f')
    # expect 1 row with the following values:
    # 	100  -29169.0300000000000000000
    
    stmt = """select
avg (maxsmall),
sum (maxsmall)
from minmax;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test013exp""", 'test013g')
    # expect 1 row with the following values:
    # 	29168.1400000000000000000   2916814
    
    stmt = """select
count (maxsmall),
sum (maxsmall) / count (maxsmall)
from minmax;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test013exp""", 'test013h')
    # expect 1 row with the following values:
    # 	100   29168.1400000000000000000
    #------ eof --------
    
    _testmgr.testcase_end(desc)

