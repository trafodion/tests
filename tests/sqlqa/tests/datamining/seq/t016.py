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
    # Sequence function tests: test for RUNNINGAVG(column)
    #
    stmt = """select cast (runningavg (i1) as dec (5,2))
as runningavg_i1, i1
from vwseqtb2 sequence by ts;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test016.exp""", 's1')
    # expect 20 rows with the following values in order:
    
    # RUNNINGAVG_I1  I1
    # -------------  -----------
    #
    #          1.00            1
    #          1.50            2
    #          2.00            3
    #          2.50            4
    #          3.00            5
    #          3.50            6
    #          4.00            7
    #          4.50            8
    #          5.00            9
    #          5.50           10
    #          6.00           11
    #          6.50           12
    #          7.00           13
    #          7.50           14
    #          8.00           15
    #          8.50           16
    #          9.00           17
    #          9.50           18
    #         10.00           19
    #         10.50           20
    
    stmt = """select cast (runningavg (i1) as dec (5,2))
as runningavg_i1, i1
from vwseqtb2 sequence by ts asc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test016.exp""", 's2')
    # expect 20 rows with identical values as above
    
    # semantic equivalent:
    stmt = """select cast (runningsum (i1) / runningcount (i1) as dec (5,2))
as runningavg_i1, i1
from vwseqtb2 please
sequence by ts;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test016.exp""", 's3')
    # expect 20 rows with identical values as above
    
    stmt = """select cast (runningavg (i1) as dec (5,2))
as runningavg_i1, i1
from vwseqtb2 sequence by ts desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test016.exp""", 's4')
    # expect 20 rows with the following values in order:
    
    # RUNNINGAVG_I1  I1
    # -------------  -----------
    #
    #         20.00           20
    #         19.50           19
    #         19.00           18
    #         18.50           17
    #         18.00           16
    #         17.50           15
    #         17.00           14
    #         16.50           13
    #         16.00           12
    #         15.50           11
    #         15.00           10
    #         14.50            9
    #         14.00            8
    #         13.50            7
    #         13.00            6
    #         12.50            5
    #         12.00            4
    #         11.50            3
    #         11.00            2
    #         10.50            1
    
    stmt = """select cast (runningavg (i2) as dec (10,3))
as runningavg_i2, i2
from vwseqtb2 sequence by i2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test016.exp""", 's5')
    # expect 20 rows with the following values in order:
    #       61.00           61
    #      762.50         1464
    #     1170.00         1985
    #     1522.50         2580
    #     2137.40         4597
    #     2584.17         4818
    #     3102.86         6215
    #     3529.50         6516
    #     3964.78         7447
    #     4491.80         9235
    #     5156.00        11798
    #     5723.50        11966
    #     6298.46        13198
    #     7209.86        19058
    #     8070.47        20119
    #     9031.88        23453
    #     9896.29        23727
    #    10735.28        24998
    #    11653.11        28174
    #    12532.75        29246
    
    # semantic equivalent:
    stmt = """select cast (runningsum (i2) / runningcount (i2) as dec (10,3))
as runningavg_i2, i2
from vwseqtb2 please
sequence by i2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test016.exp""", 's6')
    # expect 20 rows with identical values as above
    
    _testmgr.testcase_end(desc)

