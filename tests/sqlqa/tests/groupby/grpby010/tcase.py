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
    
def test001(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    stmt = """SELECT
avg(salary)
from emp
group by
avg(salary)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4197')
    
    _testmgr.testcase_end(desc)

def test002(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    stmt = """SELECT
count(*)
from emp
group by
count(*)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4197')
    
    _testmgr.testcase_end(desc)

def test003(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    stmt = """SELECT
max(salary)
from emp
group by
max(salary)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4197')
    
    _testmgr.testcase_end(desc)

def test004(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    stmt = """SELECT
min(salary)
from emp
group by
min(salary)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4197')
    
    _testmgr.testcase_end(desc)

def test005(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    stmt = """SELECT
stddev(salary)
from emp
group by
stddev(salary)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4197')
    
    _testmgr.testcase_end(desc)

def test006(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    stmt = """SELECT
sum(salary)
from emp
group by
sum(salary)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4197')
    
    _testmgr.testcase_end(desc)

def test007(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    stmt = """SELECT
variance(salary)
from emp
group by
variance(salary)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4197')
    _testmgr.testcase_end(desc)

