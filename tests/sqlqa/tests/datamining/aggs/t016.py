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
    
def test001(desc="""test016"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test016
    # float100.sql
    # jclear
    # 1997-04-29
    # New aggregate tests.
    # Tests aggregate function s, including Variance and StdDev,
    # on a float column containing 100 rows of floats with mixed
    # positive and negative values and a few nulls.
    
    stmt = """select
Count (*) as "Count",
Max (flt100) as "Max",
Min (flt100) as "Min"
from float100;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test016exp""", 'test016a')
    # expect 1 row with the following values:
    # 	Count	100
    # 	Max	31529.4646
    # 	Min	-32235.29774
    
    ##expectfile ${test_dir}/test016exp test016b
    stmt = """select
Avg (flt100) as "Avg",
Sum (flt100) as "Sum"
from float100;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    # expect 1 row with the following values:
    # 	Ave	6345.9741842268
    # 	Sum	615559.49587
    
    ##expectfile ${test_dir}/test016exp test016c
    ##expectfile ${test_dir}/test016exp test016c
    stmt = """select
Variance (flt100) as "Variance",
StdDev (flt100) as "StdDev"
from float100;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    # expect 1 row with the following values:
    # 	Var	2.91305728456180630E+008
    # 	StDev	1.70676808165661640E+004
    #
    
    _testmgr.testcase_end(desc)

