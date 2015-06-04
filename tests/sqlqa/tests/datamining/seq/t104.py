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
    
def test001(desc="""test104"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test104
    # "Nested THIS function erroneously detected as inside another
    #  sequence function"
    #
    # *** ERROR[4108] Inside a ROWS SINCE, another sequence function
    # contained an invalid reference to the THIS function.
    #
    # the workaround:
    stmt = """select a, b, c,
cast (movingavg (c, 3, rows since inclusive ((a) <> OFFSET(a, 1))+1)
as dec (10,3))
from
(values
(1234,         23,      11),
(1234,         24,      17),
(2345,         23,      14),
(2345,         24,      15),
(2345,         25,      15),
(2345,         26,      11))
as T(a, b, c)
sequence by a, b
order by 1, 2, 3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test104.exp""", 's1')
    # expect 6 rows with these values in this order:
    #     1234      23      11        11.000
    #     1234      24      17        14.000
    #     2345      23      14        14.000
    #     2345      24      15        14.500
    #     2345      25      15        14.666
    #     2345      26      11        13.666
    
    stmt = """select a, b, c,
cast (movingavg (c, 3, rows since (this (a) <> a))
as dec (10,3))
from
(values
(1234,         23,      11),
(1234,         24,      17),
(2345,         23,      14),
(2345,         24,      15),
(2345,         25,      15),
(2345,         26,      11))
as T(a, b, c)
sequence by a, b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test104.exp""", 's2')
    # expect 6 rows with these values in this order:
    #     1234      23      11        11.000
    #     1234      24      17        14.000
    #     2345      23      14        14.000
    #     2345      24      15        14.500
    #     2345      25      15        14.666
    #     2345      26      11        13.666
    
    _testmgr.testcase_end(desc)

