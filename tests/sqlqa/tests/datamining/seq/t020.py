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
    # Sequence function tests: MOVINGMAX
    #
    stmt = """select i, c, movingmax (c, 1) as movmax_c
from vwseqtb4 
sequence by i;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test020.exp""", 's1')
    # expect 10 rows with the following data in order:
    #          1            2            2
    #          2            4            4
    #          3            6            6
    #          4            8            8
    #          5            ?            ?
    #          6            5            5
    #          7            7            7
    #          8            9            9
    #          9           11           11
    #         10           10           10
    
    stmt = """select i, c, movingmax (c, 666) as movmax_c
from vwseqtb4 
sequence by i;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test020.exp""", 's2')
    # expect 10 rows with the following data in order:
    #          1            2            2
    #          2            4            4
    #          3            6            6
    #          4            8            8
    #          5            ?            8
    #          6            5            8
    #          7            7            8
    #          8            9            9
    #          9           11           11
    #         10           10           11
    
    # the following expression evaluates to 4
    stmt = """select i, c, movingmax (c, 3.08000000000000000E+002 / 77) as movmax_c
from vwseqtb4 
sequence by i;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test020.exp""", 's3')
    # expect 10 rows with the following data in order:
    #          1            2            2
    #          2            4            4
    #          3            6            6
    #          4            8            8
    #          5            ?            8
    #          6            5            8
    #          7            7            8
    #          8            9            9
    #          9           11           11
    #         10           10           11
    
    stmt = """select i, c, cast (movingmax (c, 3) as char (3)) as movmax_c
from vwseqtb4 
sequence by i;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test020.exp""", 's4')
    # expect 10 rows with the following data in order:
    #          1            2  2
    #          2            4  4
    #          3            6  6
    #          4            8  8
    #          5            ?  8
    #          6            5  8
    #          7            7  7
    #          8            9  9
    #          9           11  11
    #         10           10  11
    
    stmt = """select i, c, movingmax (c, 007) as movmax_c
from vwseqtb4 
sequence by i;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test020.exp""", 's5')
    # expect 10 rows with the following data in order:
    #          1            2            2
    #          2            4            4
    #          3            6            6
    #          4            8            8
    #          5            ?            8
    #          6            5            8
    #          7            7            8
    #          8            9            9
    #          9           11           11
    #         10           10           11
    
    _testmgr.testcase_end(desc)

