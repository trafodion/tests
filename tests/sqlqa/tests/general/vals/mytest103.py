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
    
    stmt = """values (cast(interval '1234567890' minute(10)
as interval second(6,6)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8411')
    # expect error 8411
    
    stmt = """values (cast(interval '834' year(3) as interval month(3)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8411')
    # expect error 8411
    
    stmt = """values (cast(interval '417' day(3) as interval hour(3)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8411')
    # expect error 8411
    
    stmt = """values (cast(interval '167' hour (3) as interval minute(3)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8411')
    # expect error 8411
    
    stmt = """values (cast(interval '16667' minute(10) as interval second(6,4)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8411')
    # expect error 8411
    
    stmt = """values (cast(interval '1234' minute(10) as interval second(5,4)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test103.exp""", """test103f""")
    # should get 74040.0000
    
    stmt = """values (cast(interval '1234' minute(10) as interval second(5,5)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test103.exp""", """test103g""")
    # should get 74040.00000
    
    stmt = """values (cast(interval '1234' minute(5) as interval second(5,4)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test103.exp""", """test103h""")
    # should get 74040.0000
    
    stmt = """values (cast (interval '833' year(3)
as interval month (4)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test103.exp""", """test103i""")
    # expect 9996
    
    stmt = """values (cast (interval '834' year(3)
as interval month (4)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8411')
    # expect error 8411
    
    stmt = """values (cast (interval '416' day(3)
as interval hour (4)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test103.exp""", """test103k""")
    # expect 9984
    
    stmt = """values (cast (interval '417' day(3)
as interval hour (4)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8411')
    # expect error 8411
    
    stmt = """values (cast (interval '166' hour (3)
as interval minute (4)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test103.exp""", """test103m""")
    # expect 9960
    
    stmt = """values (cast (interval '167' hour (3)
as interval minute (4)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8411')
    # expect error 8411
    
    stmt = """values (cast (interval '1234567890' minute(10)
as interval second (6,6)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8411')
    # expect error 8411
    
    stmt = """values (cast (interval '1234567.123456' second(8,6)
as interval second(6,6)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8411')
    # expect error 8411
    
    stmt = """values (cast (interval '1234567.123456' second(8,6)
as interval second(7,6)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test103.exp""", """test103q""")
    # expect 1234567.123456
    
    stmt = """values (cast (interval '16666' minute(10)
as interval second (6,6)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test103.exp""", """test103s""")
    # expect 999960.000000
    
    stmt = """values (cast (interval '16667' minute(10) as interval second (6,6)) );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8411')
    # expect error 8411
    
    stmt = """values (cast (interval '400' hour(4) as interval minute(4))  );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8411')
    # expect error 8411
    
    stmt = """values (cast (interval '600' hour(4) as interval minute(4))  );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8411')
    # expect error 8411
    
    stmt = """values (cast (interval '166:59' hour(3) to minute
as interval minute(4) to second) );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8411')
    # expect error 8411
    
    stmt = """values (cast (interval '165:59' hour(3) to minute
as interval minute(4) to second) );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test103.exp""", """test103x""")
    # expect 9959:00.000000
    
