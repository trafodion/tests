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
    #numeric term
    stmt = """Select -50 from emp group by -50;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a01s1""")
    stmt = """Select 1 from emp group by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a01s2""")
    
    #numeric-expression + numeric-term
    stmt = """Select salary + 1000 from emp group by salary + 1000;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a01s3""")
    stmt = """Select salary - 1000 from emp group by salary - 1000;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a01s4""")
    
    #numeric-expression - numeric-term
    stmt = """Select salary + dept_num from emp group by salary + dept_num;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a01s5""")
    stmt = """Select salary - marital_status from emp group by salary - marital_status;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a01s6""")
    
    _testmgr.testcase_end(desc)

def test002(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #* product
    stmt = """Select salary * 1.10 from emp group by salary * 1.10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a02s1""")
    stmt = """Select salary * dept_num from emp group by salary * dept_num;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a02s2""")
    stmt = """Select salary * dept_num * marital_status from emp group by salary * dept_num * marital_status;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a02s3""")
    stmt = """Select salary ** 2 from emp group by salary ** 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a02s4""")
    
    _testmgr.testcase_end(desc)

def test003(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #a * ( b - c) expression with numeric literals
    stmt = """Select 12 * (7-4) from emp group by 12 * (7-4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a03s1""")
    stmt = """Select salary * (dept_num - marital_status) from emp group by salary * (dept_num - marital_status);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a03s2""")
    stmt = """Select salary*2 + (50-dept_num) - marital_status from emp group by salary*2 + (50-dept_num) - marital_status;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a03s3""")
    _testmgr.testcase_end(desc)

