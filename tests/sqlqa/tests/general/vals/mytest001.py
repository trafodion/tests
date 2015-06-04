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

# test001
# JClear
# 1999-04-06
# VALUES tests
# different datatypes
#
# character
def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci
    
    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()
    
    stmt = """values ('string', 'This is a string as long as I can successfully concentrate on one line');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test001.exp""", """test001a""")
    
    # integer
    stmt = """values (-32768, -2147483648, 4294967295, -4294967295);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test001.exp""", """test001b""")
    
    # floating point
    stmt = """values (-12345.6789, 3.15294645999999990E+004,
cast (6.15559495508183610E+005 as dec (18,4)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test001.exp""", """test001c""")
    
    # time
    stmt = """values (time '12:30:15 am',
timestamp '2000-01-01 00:00:00');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test001.exp""", """test001d""")
    
    # date: international, usa, european
    stmt = """values (date '1999-12-31', date '12/31/1999', date '31.12.1999');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test001.exp""", """test001e""")
    
    # interval
    stmt = """values (interval '364:23:59:59.9999' day (3) to second (4));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test001.exp""", """test001f""")
    
