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
    
def test001(desc="""test064"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test064
    # DDunn
    # 1999-01-18
    # Testing sampling with params.
    # params are currently not supported
    #
    stmt = """set param ?psize 10;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?nblocks 4;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?somany 20;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?pperiodic 5;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select empid, salary
from samptb051 
sample first 10 rows
sort by empid;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test064.exp""", 's1')
    # expect 10 rows with the following values in this order
    #       40000.00
    #       45000.00
    #       55000.00
    #       25000.00
    #       30000.00
    #       40000.00
    #       36000.00
    #       60000.00
    #       20050.00
    #       20000.00
    
    # params are not supported thus
    # the queries would result in syntax errors
    stmt = """select empid, salary
from samptb051 
sample first ?psize rows
sort by empid;"""
    output = _dci.cmdexec(stmt)
    # expect the same 10 rows as above
    
    stmt = """select empid, salary
from samptb051 
sample random ?psize percent;"""
    output = _dci.cmdexec(stmt)
    # expect random 10 rows
    
    stmt = """select empid, salary
from samptb051 
sample random ?psize percent clusters of ?nblocks blocks;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select empid, salary
from samptb051 
sample periodic ?pperiodic rows every 20 rows sort by empid;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select empid, salary
from samptb051 
sample periodic ?pperiodic rows every ?somany rows sort by empid;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

