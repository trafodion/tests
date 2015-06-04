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

# test002
# JClear
# 1999-04-06
# VALUES tests with string functions
#
def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci
    
    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()
    
    stmt = """values (ascii ('Z'));		-- expect 90"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test002.exp""", """test002a""")
    
    stmt = """values (char (65+25));		-- expect Z"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test002.exp""", """test002b""")
    
    stmt = """values (char_length ('how long is this string going to be?') / 4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test002.exp""", """test002c""")
    # should be 9
    
    stmt = """values (octet_length ('how long is this string going to be?') / 1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test002.exp""", """test002d""")
    # should be 36
    
    stmt = """values (concat ('This string ', 'and this one'),
'Or this one' || ' and this.');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test002.exp""", """test002e""")
    
    stmt = """values ((select 'W' || 'ho ' || upper (lower (upshift
(substring (substring (substring (substring
(its from 2 for 10) from 3 for 8) from 2 for 5) from 3 for 2))))
|| '?' as anything
from anywhere thanks
where its not like 'nothing else'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test002.exp""", """test002f""")
    
    stmt = """values ((SELECT OK.OK from OK OK
WHERE OK.OK >= OK.OK
AND OK.OK <= OK.OK
AND OK.OK BETWEEN
OK.OK AND OK.OK));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test002.exp""", """test002g""")
    
