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
    
def test001(desc="""test102"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test102
    # JClear
    # 1998-11-18
    # Sampling tests: unsupported features
    #
    # relative in FIRST-N
    stmt = """select * from vwsamptb1 
sample first 10 percent rows
sort by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4113')
    
    # params are not supported in sample tests
    stmt = """set param ?ten 10;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select * from vwsamptb1 
sample first ?ten rows
sort by a;"""
    output = _dci.cmdexec(stmt)
    
    # expressions
    stmt = """select * from vwsamptb1 
sample first (2+3)*2 rows
sort by a;"""
    output = _dci.cmdexec(stmt)
    
    # absolute in RANDOM
    stmt = """select count (*) from vwsamptb1 
sample random 10 rows;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4113')
    
    _testmgr.testcase_end(desc)

