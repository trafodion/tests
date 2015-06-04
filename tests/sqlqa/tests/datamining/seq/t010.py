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
    
def test001(desc="""test010"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test010
    # Sequence function tests: OFFSET()
    #
    stmt = """select offset (i1, 3) as "offset (i1,3)"
from vwseqtb2 
where i2 > 60
sequence by ts;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test010.exp""", 's1')
    # expect 20 rows with these values in order:
    # "offset (i1,3)"
    # -------------
    #
    #           ?
    #           ?
    #           ?
    #           1
    #           2
    #           3
    #           4
    #           5
    #           6
    #           7
    #           8
    #           9
    #          10
    #          11
    #          12
    #          13
    #          14
    #          15
    #          16
    #          17
    
    stmt = """select offset (i2, 10) as "offset (i2,10)"
from vwseqtb2 
where i2 > 60
sequence by i2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test010.exp""", 's2')
    # expect 20 rows with these values in order:
    # "offset (i2,10)"
    # ---------------
    #
    #               ?
    #               ?
    #               ?
    #               ?
    #               ?
    #               ?
    #               ?
    #               ?
    #               ?
    #               ?
    #              61
    #            1464
    #            1985
    #            2580
    #            4597
    #            4818
    #            6215
    #            6516
    #            7447
    #            9235
    
    stmt = """select offset (ts, 19) as "offset (ts,19)"
from vwseqtb2 
where i2 > 60
sequence by ts;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test010.exp""", 's3')
    # expect 20 rows with 19 nulls and the value 1950-03-05 08:32:09.000000
    
    # out of range offset gets all nulls
    stmt = """select offset (ts, 21) as "offset (ts,21)"
from vwseqtb2 
where i2 > 60
sequence by ts;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test010.exp""", 's4')
    # expect 20 rows with all nulls
    
    _testmgr.testcase_end(desc)

