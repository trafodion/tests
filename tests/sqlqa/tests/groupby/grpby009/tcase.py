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
    #abs function
    stmt = """select abs(salary+10) from emp group by abs(salary+10);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a01s1""")
    
    #acos function
    stmt = """select acos(salary/100000) from emp  where salary< 50000 group by acos(salary/100000);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a01s2""")
    
    #asin function
    stmt = """select asin(salary/1000000) from emp  where salary > 50000 group by asin(salary/1000000);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a01s3""")
    
    #atan function
    stmt = """select atan(salary) from emp  group by atan(salary);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a01s4""")
    
    _testmgr.testcase_end(desc)

def test002(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #atan2 function
    stmt = """select atan2(salary, 1000) from emp group by atan2(salary, 1000);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a02s1""")
    
    #ceiling function
    stmt = """select ceiling(salary) from emp  group by ceiling(salary);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a02s2""")
    
    #cos function
    stmt = """select cos(salary) from emp  group by cos(salary);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a02s3""")
    
    #cosh function
    stmt = """select cosh(salary/10000) from emp group by cosh(salary/10000);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a02s4""")
    
    _testmgr.testcase_end(desc)

def test003(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #degrees function
    stmt = """select degrees(salary) from emp  group by degrees(salary);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a03s1""")
    
    #exp function
    stmt = """select exp(salary/10000) from emp  group by exp(salary/10000);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a03s2""")
    
    #floor function
    stmt = """select floor(salary) from emp  group by floor(salary);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a03s3""")
    
    #log function
    stmt = """select log(salary) from emp  group by log(salary);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a03s4""")
    
    _testmgr.testcase_end(desc)

def test004(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #log10 function
    stmt = """select log10(salary) from emp  group by log10(salary);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a04s1""")
    
    #mod function
    stmt = """select mod(10,3) from emp group by mod(10,3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a04s2""")
    
    #p1 function
    stmt = """select pi() from emp  group by pi();"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a04s3""")
    
    #power function
    stmt = """select power(salary,2) from emp  group by power(salary,2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a04s4""")
    
    _testmgr.testcase_end(desc)

def test005(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #radians function
    stmt = """select radians(salary) from emp  group by radians(salary);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a05s1""")
    
    #sign function
    stmt = """select sign(salary) from emp  group by  sign(salary);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a05s2""")
    
    #sin function
    stmt = """select sin(salary) from emp  group by  sin(salary);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a05s3""")
    
    #sinh function
    stmt = """select sinh(salary/10000) from emp where salary<50000 group by  sinh(salary/10000);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a05s4""")
    
    _testmgr.testcase_end(desc)

def test006(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #sqrt function
    stmt = """select sqrt(salary) from emp  group by sqrt(salary);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a06s1""")
    
    #tan function
    stmt = """select tan(salary) from emp  group by  tan(salary);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a06s2""")
    
    #tanh function
    stmt = """select tanh(salary) from emp  group by  tanh(salary);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a06s3""")
    _testmgr.testcase_end(desc)

