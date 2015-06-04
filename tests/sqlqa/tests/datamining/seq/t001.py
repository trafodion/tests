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
    
def test001(desc="""test001"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test001
    # Sequence function tests: 1st example from the External Specs.
    #
    stmt = """SELECT RUNNINGCOUNT (*)
B,
OFFSET (B, -3) as off_b_3,
C,
OFFSET (C, 3) as off_c_3,
ROWS SINCE (C < 450) as rowssince,
ROWS SINCE INCLUSIVE (C < 450) as rowssince_inc,
dt
FROM seqtb1 
SEQUENCE BY dt
;"""
    output = _dci.cmdexec(stmt)
    # expect 33 rows in order with the following values:
    #  B     OFF_B_3      C      OFF_C_3   ROWSSINCE  ROWSSINCE_INC    DT
    #  1        ?        920          ?         1           1       1980-11-03
    #  2        ?        950          ?         2           2       1980-12-03
    #  3        ?        190          ?         3           0       1981-01-03
    #  4        ?        211        920         1           0       1981-02-03
    #  5        ?        941        950         1           1       1981-03-03
    #  6        ?        171        190         2           0       1981-04-03
    #  7        ?        102        211         1           0       1981-05-03
    #  8        ?        232        941         1           0       1981-06-03
    #  9        ?        262        171         1           0       1981-07-03
    # 10        ?        492        102         1           1       1981-08-03
    # 11        ?        423        232         2           0       1981-09-03
    # 12        ?        453        262         1           1       1981-10-03
    # 13        ?        593        492         2           2       1981-11-03
    # 14        ?        514        423         3           3       1981-12-03
    # 15        ?        644        453         4           4       1982-01-03
    # 16        ?        774        593         5           5       1982-02-03
    # 17        ?        505        514         6           6       1982-03-03
    # 18        ?        635        644         7           7       1982-04-03
    # 19        ?        665        774         8           8       1982-05-03
    # 20        ?        895        505         9           9       1982-06-03
    # 21        ?        726        635        10          10       1982-07-03
    # 22        ?        856        665        11          11       1982-08-03
    # 23        ?        996        895        12          12       1982-09-03
    # 24        ?        917        726        13          13       1982-10-03
    # 25        ?        957        856        14          14       1982-11-03
    # 26        ?        987        996        15          15       1982-12-03
    # 27        ?        118        917        16           0       1983-01-03
    # 28        ?        248        957         1           0       1983-02-03
    # 29        ?        978        987         1           1       1983-03-03
    # 30        ?        209        118         2           0       1983-04-03
    # 31        ?        239        248         1           0       1983-05-03
    # 32        ?        369        978         1           0       1983-06-03
    # 33        ?        499        209         1           1       1983-07-03
    
    _testmgr.testcase_end(desc)

