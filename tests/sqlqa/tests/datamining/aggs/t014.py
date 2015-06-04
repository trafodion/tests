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
    
def test001(desc="""test014"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test014
    # minmax.sql
    # jclear
    # 1997-04-28
    # New aggregate tests.
    # Tests Variance and StdDev on a table containing 200 rows
    # with INT_MIN, INT_MAX, SMALLINT_MIN, & SMALLINT_MAX values.
    
    stmt = """select
Variance (minint) as "VarMinInt",
StdDev (minint) as "StDMinint"
from minmax;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test014exp""", 'test014a')
    # expect 1 row with the following values:
    # 	VarMinint		4.56044484991869500E+017
    # 	StDevMinint		6.75310658135846020E+008
    
    stmt = """select
Variance (maxint) as "VarMaxInt",
StdDev (maxint) as "StDMaxint"
from minmax;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test014exp""", 'test014b')
    # expect 1 row with the following values:
    # 	VarMaxint		4.56044484567145280E+017
    # 	StDevMaxint		6.75310657821380260E+008
    
    stmt = """select
Variance (minsmall) as "VarMinSmall",
StdDev (minsmall) as "StDMinSmall"
from minmax;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test014exp""", 'test014c')
    # expect 1 row with the following values:
    # 	VarMinsmall		1.05856865887979840E+008
    # 	StDevMinsmall		1.02886765858384260E+004
    
    stmt = """select
Variance (maxsmall) as "VarMaxSmall",
StdDev (maxsmall) as "StDMaxSmall"
from minmax;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test014exp""", 'test014d')
    # expect 1 row with the following values:
    # 	VarMaxsmall		1.05850395111515240E+008
    # 	StDevMaxsmall		1.02883621199642480E+004
    _testmgr.testcase_end(desc)

