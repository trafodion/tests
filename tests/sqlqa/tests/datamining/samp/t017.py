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
    
def test001(desc="""test017"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test017
    # JClear
    # 1998-11-12
    # Sampling tests: tests on a VP table using params
    # 3. Balance
    #
    stmt = """set param ?five 5;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?ten 10;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?fifteen 15;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?forty 40;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?fifty 50;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?sixty 60;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?seventy 70;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?ninety 90;"""
    output = _dci.cmdexec(stmt)
    #
    stmt = """select * from vwsamptb3 
sample first
balance when a < ?fifty then ?fifteen rows
when a > ?fifty then ?fifteen rows
end
sort by a;"""
    output = _dci.cmdexec(stmt)
    # expect 30 rows with a values from 1-15, 51-65
    
    stmt = """select * from vwsamptb3 
sample first
balance when a < ?forty then ?ten rows
when a >= ?sixty then ?ten rows
end
sort by a asc;"""
    output = _dci.cmdexec(stmt)
    # expect 20 rows with a values from 1-10, 60-79
    
    stmt = """select * from vwsamptb3 
sample first
balance when a <= ?ten then ?fifteen rows         -- XXXXX oversampling
when a > ?fifty then ?fifteen rows
end
sort by a desc;"""
    output = _dci.cmdexec(stmt)
    # expect 25 rows with a values from 100-86, 10-1
    
    stmt = """select * from vwsamptb3 
sample first
balance when a < ?seventy then ?five rows
when a > ?ninety then ?five rows
end
sort by a desc
order by a;"""
    output = _dci.cmdexec(stmt)
    # expect 10 rows with a values from 65-69, 96-100
    
    _testmgr.testcase_end(desc)

