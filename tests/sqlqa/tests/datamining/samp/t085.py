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
    
def test001(desc="""test085"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test085
    # JClear
    # 1999-02-01
    # Sampling: FIRST-N with UNION
    #
    stmt = """select * from vwsamptb085a 
sample first 10 rows
sort by a
union
select x, y, z from vwsamptb085b 
order by a, b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test085.exp""", 's1')
    # expect 35 rows with a values 1-10 & 100-124
    
    stmt = """select a * 10, b, c from vwsamptb085a 
sample first 10 rows
sort by a
union
select x, y, z from vwsamptb085b 
order by 1, 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test085.exp""", 's2')
    # expect 35 rows with a values 10-100 & 100-124
    
    stmt = """select * from vwsamptb085a 
sample first 10 rows
sort by a
union
select x, y, z from vwsamptb085b 
sample first 10 rows
sort by x
order by a, b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test085.exp""", 's3')
    # expect 20 rows with a values 1-10 & 100-109
    
    stmt = """select * from vwsamptb085a 
sample first 10 rows
sort by a
union all
select x, y, z from vwsamptb085b 
order by a, b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test085.exp""", 's4')
    # expect 35 rows with a values 1-10 & 100-124
    
    stmt = """select a * 10, b, c from vwsamptb085a 
sample first 10 rows
sort by a
union all
select x, y, z from vwsamptb085b 
order by 1, 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test085.exp""", 's5')
    # expect 35 rows with a values 10-100 & 100-124
    
    stmt = """select * from vwsamptb085a 
sample first 10 rows
sort by a
union all
select x, y, z from vwsamptb085b 
sample first 10 rows
sort by x
order by a, b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test085.exp""", 's6')
    # expect 20 rows with a values 1-10 & 100-109
    
    _testmgr.testcase_end(desc)

