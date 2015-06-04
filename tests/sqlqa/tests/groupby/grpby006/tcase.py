# @@@ START COPYRIGHT @@@
#
# (C) Copyright 2014-2015 Hewlett-Packard Development Company, L.P.
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

#other functions
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
    #cast expression
    stmt = """select cast (current as date)-hire_date from emp
group by
cast (current as date)-hire_date;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 4)
    
    stmt = """Select
case dept_num
when 10 then 'Manager'
when 20 then 'supervisor'
when 30 then 'engineer'
else 'Programmer'
end
from emp
group by
case dept_num
when 10 then 'Manager'
when 20 then 'supervisor'
when 30 then 'engineer'
else 'Programmer'
end;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a01s2""")
    
    _testmgr.testcase_end(desc)

def test002(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    stmt = """Select
case
when dept_num=10 then salary*1.10
when dept_num=20 then salary*2.20
when dept_num=30 then salary*3.30
else
salary
end
from emp
group by
case
when dept_num=10 then salary*1.10
when dept_num=20 then salary*2.20
when dept_num=30 then salary*3.30
else
salary
end;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a02s1""")
    
    #current expression
    stmt = """Select current_user from emp
group by
current_user;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    
    _testmgr.testcase_end(desc)

def test003(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #hashpartfunc expression
    stmt = """select hashpartfunc(dept_num for 4) from emp
group by
hashpartfunc(dept_num for 4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a03s1""")
    
    #session_user expression
    stmt = """Select session_user from emp
group by
session_user;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    
    #user expression
    stmt = """Select user from emp
group by
user;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)

    _testmgr.testcase_end(desc)

