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
    
def test001(desc="""test020"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test020
    # dec100.sql
    # jclear
    # 1997-04-29
    # New aggregate tests.
    # Tests aggregate function s, including Variance and StdDev,
    # on a decimal (10, 5) column containing 100 rows of with mixed
    # positive and negative values and a few nulls.
    
    stmt = """select
Count (*) as "Count",
Max (num) as "Max",
Min (num) as "Min"
from dec100;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test020exp""", 'test020a')
    # expect 1 row with the following values:
    # 	Count	100
    # 	Max	3241419930.5751
    # 	Min	-3245121455.10584
    
    stmt = """select
Avg (num) as "Avg",
Sum (num) as "Sum"
from dec100;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test020exp""", 'test020b')
    # expect 1 row with the following values:
    # 	Ave	146097189.389351
    # 	Sum	14025330181.3777
    
    stmt = """select
Variance (num) as "PVariance",
StdDev (num) as "PStdDev"
from dec100;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test020exp""", 'test020c')
    # expect 1 row with the following values:
    #
    # 	Pvar	2.66279127249995E+18
    # 	PStDev	1631806138.14875
    
    _testmgr.testcase_end(desc)

