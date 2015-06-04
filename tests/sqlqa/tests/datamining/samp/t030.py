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
    
def test001(desc="""test030"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test030
    # JClear
    # 1998-12-15
    # more first 10 tests: moving sequence functions
    # calculated values are in test029.dat
    #
    stmt = """select movingsum (b, 5) from vwsamptb1 
sample first 10 rows
sort by a
sequence by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test030.exp""", 's1')
    # expect 10 rows with these values:
    #         250
    #       26706
    #       40772
    #       64976
    #       96121
    #      124656
    #      121889
    #      130167
    #      123342
    #      116781
    
    stmt = """select movingmax (b, 5) from vwsamptb1 
sample first 10 rows
sort by a
sequence by a
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test030.exp""", 's2')
    # expect 10 rows with these values in order:
    #      250
    #    26456
    #    26456
    #    26456
    #    31145
    #    31145
    #    31145
    #    31145
    #    31145
    #    31145
    
    stmt = """select movingmin (b, 5) from vwsamptb1 
sample first 10 rows
sort by a
sequence by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test030.exp""", 's3')
    # expect 10 rows with these values:
    #      250
    #      250
    #      250
    #      250
    #      250
    #    14066
    #    14066
    #    22344
    #    17379
    #    17379
    
    stmt = """select cast (movingavg (b, 5) as dec (15,2)) from vwsamptb1 
sample first 10 rows
sort by a
sequence by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test030.exp""", 's4')
    # expect 10 rows with these values in order:
    #      250.00
    #    13353.00
    #    13590.67
    #    16244.00
    #    19224.20
    #    24931.20
    #    24377.80
    #    26033.40
    #    24668.40
    #    23356.20
    
    stmt = """select cast (movingstddev (b, 5) as dec (15,2)) from vwsamptb1 
sample first 10 rows
sort by a
sequence by a
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test030.exp""", 's5')
    # expect 10 rows with these values in order:
    #          .00
    #      3746.810
    #      4118.300
    #      5440.362
    #      6558.511
    #      6602.452
    #     11947.081
    #     12306.808
    #     13109.465
    #     18530.440
    
    stmt = """select cast (movingvariance (b, 5) as dec (15,2)) from vwsamptb1 
sample first 10 rows
sort by a
sequence by a
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test030.exp""", 's6')
    # expect 10 rows with these values in order:
    #              .00
    #      14038586.300
    #      16960396.700
    #      29597538.800
    #      43014069.700
    #      43592372.700
    #     142732754.667
    #     151457526.200
    #     171858065.333
    #     343377218.000
    
    _testmgr.testcase_end(desc)

