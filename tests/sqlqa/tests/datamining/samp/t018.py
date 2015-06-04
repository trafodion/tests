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
    # JClear
    # 1998-11-15
    # Sampling tests: tests on a plain table using expressions
    #
    # 1. First-N
    stmt = """select * from vwsamptb3 
sample first (select cast (avg (a) / 5 as int) from vwsamptb3) rows
sort by a;"""
    output = _dci.cmdexec(stmt)
    # expression evaluates to 10
    # expect 10 rows with a values from 1-10
    
    stmt = """select * from vwsamptb3 
sample first (select cast (avg (a) / 5 as int) from vwsamptb3) rows
sort by a desc;"""
    output = _dci.cmdexec(stmt)
    # expression evaluates to 10
    # expect 10 rows with a values from 100-91
    
    stmt = """select avg (b) from vwsamptb3 
where a is not null
and a > 0
sample first (select cast (avg (a) / 5 as int) from vwsamptb3) rows;"""
    output = _dci.cmdexec(stmt)
    # expression evaluates to 10
    # expect avg of b = 21290.200
    
    # 2. Periodic
    stmt = """select * from vwsamptb3 
where a > -666
sample periodic (select cast (avg (a) / 10 as int) from vwsamptb3) rows
every (select cast (avg (a) / 5 as int) from vwsamptb3) rows
sort by a;"""
    output = _dci.cmdexec(stmt)
    # expressions evaluate to 5 & 10
    # expect 50 rows with a values from 1-5, 10-15 etc.
    
    stmt = """select * from vwsamptb3 
where a between 0 and 100
sample periodic (select cast (avg (a) / 10 as int) from vwsamptb3) rows
every (select cast (avg (a) / 5 as int) from vwsamptb3) rows
sort by a;"""
    output = _dci.cmdexec(stmt)
    # expressions evaluate to 5 & 10
    # expect 50 rows with a values from 1-5, 10-15 etc.
    
    # 3. Balance
    
    stmt = """set param ?fifty 50;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?twentyfive 25;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select * from vwsamptb2 
sample first
balance when a < ?fifty then ?twentyfive rows
when a > ?fifty then ?twentyfive rows
end
sort by a asc
order by a desc;"""
    output = _dci.cmdexec(stmt)
    # expect 50 rows with a values from 1-25, 50-75
    
    stmt = """select * from vwsamptb3 
sample first of (select cast (avg (a) * 2 as int) - 1) exact
balance when a < ?fifty then ?twentyfive
when a > ?fifty then ?twentyfive
end
sort by a;"""
    output = _dci.cmdexec(stmt)
    # expression evaluates to 100
    # expect 10 rows with a values from 1-10
    
    _testmgr.testcase_end(desc)

