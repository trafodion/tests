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

#Sequence functions

def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci
    
    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()
    
def test001(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    stmt = """select diff1(salary) from emp sequence by salary group by diff1(salary);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4109')
    stmt = """select diff2(salary) from emp sequence by salary group by diff2(salary);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4109')
    
    _testmgr.testcase_end(desc)

def test002(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    stmt = """select movingavg(salary,3) from emp sequence by salary group by  movingavg(salary,3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4109')
    stmt = """select movingcount(salary,3) from emp sequence by salary group by movingcount(salary,3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4109')
    stmt = """select movingmax(salary,3) from emp sequence by salary group by movingmax(salary,3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4109')
    stmt = """select movingmin(salary,3) from emp sequence by salary group by movingmin(salary,3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4109')
    stmt = """select movingstddev(salary,3) from emp sequence by salary group by movingstddev(salary,3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4109')
    stmt = """select movingsum(salary,3) from emp sequence by salary group by movingsum(salary,3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4109')
    stmt = """select movingvariance(salary,3) from emp sequence by salary group by movingvariance(salary,3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4109')
    
    _testmgr.testcase_end(desc)

def test003(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    stmt = """select offset(salary,3) from emp sequence by salary group by offset(salary,3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4109')
    
    _testmgr.testcase_end(desc)

def test004(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #running sequencefunctions
    stmt = """select runningavg(salary) from emp sequence by salary group by runningavg(salary);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4109')
    stmt = """select runningcount(salary) from emp sequence by salary group by runningcount(salary);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4109')
    stmt = """select runningmax(salary) from emp sequence by salary group by runningmax(salary);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4109')
    stmt = """select runningmin(salary) from emp sequence by salary group by runningmin(salary);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4109')
    stmt = """select runningstddev(salary) from emp sequence by salary group by runningstddev(salary);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4109')
    stmt = """select runningsum(salary) from emp sequence by salary group by runningsum(salary);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4109')
    stmt = """select runningvariance(salary) from emp sequence by salary group by runningvariance(salary);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4109')
    stmt = """select runningcount(salary) from emp sequence by salary group by runningcount(salary);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4109')
    stmt = """select lastnotnull(salary) from emp sequence by salary group by lastnotnull(salary);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4109')
    stmt = """select rows since (salary is null) from emp sequence by salary group by rows since (salary is null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4109')
    _testmgr.testcase_end(desc)

