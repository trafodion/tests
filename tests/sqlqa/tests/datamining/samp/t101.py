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
    
def test001(desc="""test101"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test101
    # JClear
    # 1998-11-02
    # Sampling tests: negative test of handling incorrect size specifications
    #
    stmt = """select * from vwsamptb1 
sample first -666 rows
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select * from vwsamptb1 
sample first 3.14159 rows
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4114')
    
    stmt = """select * from vwsamptb1 
sample first plenty rows
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select * from vwsamptb1 please
sample first 1000 rows thanks
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select * from vwsamptb1 
sample periodic 13 rows every 10 rows
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4115')
    
    # dividing by zero
    stmt = """select * from vwsamptb1 
sample first (600 + 66) * 7 / (4 * 3 - (11 + 1)) rows
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    _testmgr.testcase_end(desc)

