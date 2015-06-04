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
    
def test001(desc="""test015"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test015
    # Sequence function tests: test for RUNNINGSUM(column)
    #
    stmt = """select runningsum (i1) as runningsum_i1, i1
from vwseqtb2 sequence by ts;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test015.exp""", 's1')
    # expect 20 rows with the following values in order:
    
    # RUNNINGSUM_I1         I1
    # --------------------  -----------
    #
    #                    1            1
    #                    3            2
    #                    6            3
    #                   10            4
    #                   15            5
    #                   21            6
    #                   28            7
    #                   36            8
    #                   45            9
    #                   55           10
    #                   66           11
    #                   78           12
    #                   91           13
    #                  105           14
    #                  120           15
    #                  136           16
    #                  153           17
    #                  171           18
    #                  190           19
    #                  210           20
    
    stmt = """select runningsum (i1) as runningsum_i1, i1
from vwseqtb2 sequence by ts asc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test015.exp""", 's2')
    # expect 20 rows with identical values as above
    
    # equivalent in standard SQL
    stmt = """select (select sum (i1) from vwseqtb2 x where x.i1 <= y.i1)
as runningsum_i1, i1
from vwseqtb2 y
order by ts;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test015.exp""", 's3')
    # expect 20 rows with identical values as above
    
    stmt = """select runningsum (i1) as runningsum_i1, i1
from vwseqtb2 sequence by ts desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test015.exp""", 's4')
    # expect 20 rows with the following values in order:
    
    # RUNNINGSUM_I1         I1
    # --------------------  -----------
    #
    #                   20           20
    #                   39           19
    #                   57           18
    #                   74           17
    #                   90           16
    #                  105           15
    #                  119           14
    #                  132           13
    #                  144           12
    #                  155           11
    #                  165           10
    #                  174            9
    #                  182            8
    #                  189            7
    #                  195            6
    #                  200            5
    #                  204            4
    #                  207            3
    #                  209            2
    #                  210            1
    
    stmt = """select runningsum (i2) as runningsum_i2, i2
from vwseqtb2 sequence by i2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test015.exp""", 's5')
    # expect 20 rows with the following values in order:
    
    # RUNNINGSUM_I2         I2
    # --------------------  -----------
    #
    #                   61           61
    #                 1525         1464
    #                 3510         1985
    #                 6090         2580
    #                10687         4597
    #                15505         4818
    #                21720         6215
    #                28236         6516
    #                35683         7447
    #                44918         9235
    #                56716        11798
    #                68682        11966
    #                81880        13198
    #               100938        19058
    #               121057        20119
    #               144510        23453
    #               168237        23727
    #               193235        24998
    #               221409        28174
    #               250655        29246
    
    _testmgr.testcase_end(desc)

