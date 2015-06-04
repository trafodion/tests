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
    
def test001(desc="""test018"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test018
    # dbl100.sql
    # jclear
    # 1997-04-29
    # New aggregate tests.
    # Tests aggregate function s, including Variance and StdDev,
    # on a double precision column containing 100 rows of doubles
    # with mixed positive and negative values and a few nulls.
    
    stmt = """select
Count (*) as "Count",
Max (dbl100) as "Max",
Min (dbl100) as "Min"
from dbls100;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test018exp""", 'test018a')
    # expect 1 row with the following values:
    # 	Count	100
    # 	Max	3241419930.5751
    # 	Min	-3245121455.10584
    
    ##expectfile ${test_dir}/test018exp test018b
    stmt = """select
Avg (dbl100) as "Avg",
Sum (dbl100) as "Sum"
from dbls100;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    # expect 1 row with the following values:
    # 	Ave	146097189.389351
    # 	Sum	14025330181.3777
    
    stmt = """select
Variance (dbl100) as "Variance",
StdDev (dbl100) as "StdDev"
from dbls100;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test018exp""", 'test018c')
    # expect 1 row with the following values:
    #
    # 	Var	2.69082065431573860E+018
    # 	StDev	1.64037210849116130E+009
    
    _testmgr.testcase_end(desc)

