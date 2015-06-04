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
    #ascii function
    stmt = """Select ASCII(LAST_NAME) from emp group by ASCII(LAST_NAME);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a01s1""")
    
    #char function
    stmt = """Select CHAR(ASCII(FIRST_NAME)) from emp group by CHAR(ASCII(FIRST_NAME));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a01s2""")
    
    #char_length function
    stmt = """Select CHAR_LENGTH(LAST_NAME) from emp group by  CHAR_LENGTH(LAST_NAME);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a01s3""")
    
    #code_value function
    stmt = """Select CODE_VALUE(FIRST_NAME) from emp group by  CODE_VALUE(FIRST_NAME);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a01s4""")
    
    #concat function
    stmt = """Select CONCAT(LAST_NAME, FIRST_NAME) from emp group by CONCAT(LAST_NAME, FIRST_NAME);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a01s5""")
    
    _testmgr.testcase_end(desc)

def test002(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #insert function
    stmt = """Select INSERT(LAST_NAME,2,3,'new') from emp group by INSERT(LAST_NAME,2,3,'new');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a02s1""")
    
    #lcase function
    stmt = """Select LCASE(FIRST_NAME) from emp group by  LCASE(FIRST_NAME);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a02s2""")
    
    #left function
    stmt = """Select LEFT(LAST_NAME,3) from emp group by  LEFT(LAST_NAME,3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a02s3""")
    
    #locate function
    stmt = """Select LOCATE('a',FIRST_NAME) from emp group by LOCATE('a',FIRST_NAME);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a02s4""")
    
    #lower function
    stmt = """Select LOWER(LAST_NAME) from emp group by  LOWER(LAST_NAME);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a02s5""")
    
    _testmgr.testcase_end(desc)

def test003(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #lpad function
    stmt = """Select LPAD(FIRST_NAME,3,'new') from emp group by LPAD(FIRST_NAME,3,'new');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a03s1""")
    
    #ltrim function
    stmt = """Select LTRIM(LAST_NAME) from emp group by  LTRIM(LAST_NAME);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a03s2""")
    
    #octet_length function
    stmt = """Select OCTET_LENGTH(FIRST_NAME) from emp group by OCTET_LENGTH(FIRST_NAME);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a03s3""")
    
    #position function
    stmt = """Select POSITION('a' in LAST_NAME) from emp group by POSITION('a' in LAST_NAME);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a03s4""")
    
    #repeat function
    stmt = """Select REPEAT(FIRST_NAME, 2) from emp group by REPEAT(FIRST_NAME, 2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a03s5""")
    
    #replace function
    stmt = """Select REPLACE(LAST_NAME,'a','e') from emp group by  REPLACE(LAST_NAME,'a','e');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a03s6""")
    
    _testmgr.testcase_end(desc)

def test004(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #right function
    stmt = """select RIGHT(FIRST_NAME,3) from emp group by  RIGHT(FIRST_NAME,3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a04s1""")
    
    #rpad function
    stmt = """Select RPAD(LAST_NAME,3,'aaa') from emp group by RPAD(LAST_NAME,3,'aaa');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a04s2""")
    
    #rtrim function
    stmt = """Select RTRIM(FIRST_NAME) from emp group by RTRIM(FIRST_NAME);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a04s3""")
    
    #space function
    stmt = """Select SPACE(3) from emp group by SPACE(3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a04s4""")
    
    #substring function
    stmt = """Select SUBSTRING(LAST_NAME,3,3) from emp group by  SUBSTRING(LAST_NAME,3,3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a04s5""")
    
    _testmgr.testcase_end(desc)

def test005(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    #trim function
    stmt = """Select TRIM(BOTH 'a' from LAST_NAME) from emp group by TRIM(BOTH 'a' from LAST_NAME);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a05s1""")
    
    #ucase function
    stmt = """Select UCASE(FIRST_NAME) from emp group by UCASE(FIRST_NAME);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a05s2""")
    
    #upper function
    stmt = """Select UPPER(LAST_NAME) from emp group by UPPER(LAST_NAME);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a05s3""")
    
    #upshift function
    stmt = """Select UPSHIFT(FIRST_NAME) from emp group by UPSHIFT(FIRST_NAME);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a05s4""")
    
    _testmgr.testcase_end(desc)

