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
    
def test001(desc="""t01"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # Illegal syntax for SET TRANSACTION NO ROLLBACK { ON | OFF }
    
    # t01.1:
    ##expectfile $test_dir/t01exp t01s1
    # capture initial value for NO ROLLBACK
    stmt = """log """ + defs.work_dir + """/showtrans.log clear;"""
    output = _dci.cmdexec(stmt)
    stmt = """SHOWTRANSACTION;"""
    output = _dci.cmdexec(stmt)
    stmt = """log off;"""
    output = _dci.cmdexec(stmt)
    defs.init_norollback = """`grep 'NO ROLLBACK' """ + defs.work_dir + """/showtrans.log | cut -f2 -d':'`"""
    output = _testmgr.shell_call("""rm """ + defs.work_dir + """/showtrans.log""")
    
    # t01.2:
    stmt = """SET TRANSACTION ROLLBACK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # t01.3:
    stmt = """SET TRANSACTION ROLLBACK -1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # t01.4:
    stmt = """SET TRANSACTION ROLLBACK ON;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # t01.5:
    stmt = """SET TRANSACTION ROLLBACK OFF;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """showtransaction;"""
    output = _dci.cmdexec(stmt)
    
    # t01.7:
    stmt = """SET TRANSACTION NO ROLLBACK ONF;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """showtransaction;"""
    output = _dci.cmdexec(stmt)
    
    # t01.8:
    stmt = """SET TRANSACTION NO ROLLBACKS ON;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # the value for NO ROLLBACK should not change
    stmt = """log """ + defs.work_dir + """/showtrans.log clear;"""
    output = _dci.cmdexec(stmt)
    stmt = """showtransaction;"""
    output = _dci.cmdexec(stmt)
    stmt = """log off;"""
    output = _dci.cmdexec(stmt)
    defs.curr_norollback = """`grep 'NO ROLLBACK' """ + defs.work_dir + """/showtrans.log | cut -f2 -d':'`"""
    output = _testmgr.shell_call("""rm """ + defs.work_dir + """/showtrans.log""")
   
    if defs.init_norollback == defs.curr_norollback:
        output = 'PASS'
    else:
        output = 'FAIL' 
    _dci.expect_str_token(output, """PASS""")
    
    # t01.9:
    stmt = """SET TRANSACTION NO ROLLBACK -1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # t01.10:
    stmt = """SET TRANSACTION NO ROLLBACK 0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # t01.11:
    stmt = """SET TRANSACTION NO ROLLBACK OFFFFF;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # t01.12:
    stmt = """SET TRANSACTION NO ROLL BACK ON;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # t01.13:
    stmt = """SET TRANSACTION NO ROLL BACK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # t01.14:
    stmt = """SET TRANSACTION -1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # t01.15:
    stmt = """SET TRANSACTION AUTOCOMMIT OFF, NO ROLLBACK ON;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # t01.16:
    stmt = """SET TRANSACTION AUTOCOMMIT ON, NO ROLLBACK OFF;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # t01.17:
    ##expectfile $test_dir/t01exp t01s17
    stmt = """SET TRANSACTION NO ROLLBACK ON, NO ROLLBACK OFF;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3237')
    
    # t01.18:
    stmt = """SET TRANSACTION ISOLATION LEVEL READ COMMITTED, READ WRITE, NO ROLLBACK ON;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showtransaction;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t01.19:
    stmt = """SET TRANSACTION ISOLATION LEVEL READ COMMITTED, NO ROLLBACK ON;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showtransaction;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t01.20:
    stmt = """SET TRANSACTION NO ROLLBACK ON, ISOLATION LEVEL READ COMMITTED;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showtransaction;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t01.21:
    stmt = """SET TRANSACTION NO ROLLBACK OFF, ISOLATION LEVEL READ COMMITTED, READ ONLY;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showtransaction;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t01.22:
    stmt = """SET TRANSACTION ROLLBACK OFF, ISOLATION LEVEL READ COMMITTED;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # t01.23:
    stmt = """SET TRANSACTION NO ROLLBACK OFF, DIAGNOSTICS SIZE 10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showtransaction;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t01.24:
    stmt = """set param ?p 20;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """SET TRANSACTION DIAGNOSTICS SIZE ?p, no rollback on;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showtransaction;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t01.25:
    stmt = """SET TRANSACTION READ ONLY, DIAGNOSTICS SIZE 5, no rollback on;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """SHOWTRANSACTION;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    # Reset the transaction so that the schema can be dropped.   
    stmt = """SET TRANSACTION ISOLATION LEVEL READ COMMITTED, READ WRITE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
 
    _testmgr.testcase_end(desc)

def test002(desc="""t02"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    # t02.1:
    stmt = """set transaction no rollback off;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showtransaction;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t02.2:
    stmt = """set transaction isolation level read uncommitted;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showtransaction;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """set transaction no rollback;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t02.4:
    stmt = """set transaction autocommit off;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showtransaction;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t02.5:
    stmt = """set transaction isolation level repeatable read;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showtransaction;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t02.6:
    stmt = """set transaction no rollback;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showtransaction;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t02.9:
    stmt = """set transaction isolation level serializable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showtransaction;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t02.10:
    stmt = """set transaction read write;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t02.11:
    stmt = """set transaction no rollback off;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showtransaction;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t02.12:
    stmt = """set transaction isolation level serializable, no rollback off, read write;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showtransaction;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t02.13:
    stmt = """set transaction isolation level serializable, no rollback on;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showtransaction;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t02.14:
    stmt = """set transaction isolation level serializable, read write, no rollback off;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showtransaction;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t02.16:
    stmt = """set transaction no rollback on, autoabort 20 seconds, read only;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showtransaction;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t02.17:
    stmt = """set transaction no rollback on;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showtransaction;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t02.18:
    stmt = """set transaction autoabort 20 seconds;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showtransaction;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t02.20:
    stmt = """set transaction no rollback on, autoabort 20 seconds;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showtransaction;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t02.21:
    stmt = """set transaction autocommit on;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showtransaction;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    # Reset the transaction so that the schema can be dropped.
    stmt = """SET TRANSACTION ISOLATION LEVEL READ COMMITTED, READ WRITE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
 
    _testmgr.testcase_end(desc)

def test003(desc="""t03"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """showtransaction;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t03.1:
    stmt = """set transaction no rollback off;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showtransaction;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t03.2:
    stmt = """set transaction isolation level read uncommitted;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showtransaction;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t03.4:
    stmt = """set transaction autocommit off;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showtransaction;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t03.5:
    stmt = """set transaction isolation level repeatable read;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showtransaction;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t03.6:
    stmt = """set transaction no rollback, autoabort 21 hours,
isolation level read uncommitted;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showtransaction;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t03.9:
    stmt = """set transaction isolation level serializable,
no rollback off, autoabort 1 hours, read write, DIAGNOSTICS size 10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showtransaction;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t03.10:
    stmt = """set transaction read only;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showtransaction;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t03.11:
    stmt = """set transaction no rollback off;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showtransaction;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t03.12:
    stmt = """set transaction autoabort 3 hours;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showtransaction;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t03.13:
    # #expectfile $test_dir/t03exp t03s13a
    stmt = """set transaction autoabort 3 hours, autoabort 2 minutes;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3238')
    
    stmt = """showtransaction;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t03.13: syntax error
    ##expectfile $test_dir/t03exp t03s13c
    stmt = """set transaction autoabort 3 hours,, autoabort 2 minutes,,;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # t03.14:
    stmt = """set transaction isolation level serializable,
no rollback off, autoabort 1 hours, read only, DIAGNOSTICS size 10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showtransaction;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t03.15:
    stmt = """set transaction isolation level serializable, autocommit on,
no rollback off, autoabort 1 hours, read only, DIAGNOSTICS size 10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """showtransaction;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t03.16:
    stmt = """set transaction autocommit on;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    # Reset the transaction so that the schema can be dropped.
    stmt = """SET TRANSACTION ISOLATION LEVEL READ COMMITTED, READ WRITE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

