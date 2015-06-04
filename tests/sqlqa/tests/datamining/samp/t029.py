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
    
def test001(desc="""test029"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test029
    # JClear
    # 1998-12-15
    # more first 10 tests: running sequence functions
    # calculated answers are in test029.dat
    #
    stmt = """select runningsum (b) from vwsamptb1 
sample first 10 rows
sort by a
sequence by a
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test029.exp""", 's1')
    # expect 10 rows with value 250
    #        250
    #      26706
    #      40772
    #      64976
    #      96121
    #     124906
    #     148595
    #     170939
    #     188318
    #     212902
    
    stmt = """select runningmax (b) from vwsamptb1 
sample first 10 rows
sort by a
sequence by a
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test029.exp""", 's2')
    # expect 10 rows with these values in order:
    #      250
    #      26456
    #      26456
    #      26456
    #      31145
    #      31145
    #      31145
    #      31145
    #      31145
    #      31145
    
    stmt = """select runningmin (b) from vwsamptb1 
sample first 10 rows
sort by a
sequence by a
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test029.exp""", 's3')
    # expect 10 rows with value 250
    
    stmt = """select cast (runningavg (b) as dec (15,2)) from vwsamptb1 
sample first 10 rows
sort by a
sequence by a
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test029.exp""", 's4')
    # expect 10 rows with these values in order:
    #-         250.00
    #-       13353.00
    #-       13590.66
    #-       16244.00
    #-       19224.20
    #-       20817.66
    #-       20924.22
    #-       21227.85
    #-       21290.20
    #-       21367.37
    
    stmt = """select cast (runningstddev (b) as dec (15,2)) from vwsamptb1 
sample first 10 rows
sort by a
sequence by a
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test029.exp""", 's5')
    # expect 10 rows with these values in order:
    #               .00
    #           8921.605
    #           9382.835
    #           9929.473
    #          10716.583
    #          11679.077
    #          11947.081
    #          12306.808
    #          13109.465
    #          18530.440
    
    stmt = """select cast (runningvariance (b) as dec (15,2)) from vwsamptb1 
sample first 10 rows
sort by a
sequence by a
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test029.exp""", 's6')
    # expect 10 rows with these values in order:
    #               .00
    #       79595027.956
    #       88037584.444
    #       98594428.554
    #      114845157.810
    #      136400837.067
    #      142732754.667
    #      151457526.200
    #      171858065.333
    #      343377218.000
    
    _testmgr.testcase_end(desc)

