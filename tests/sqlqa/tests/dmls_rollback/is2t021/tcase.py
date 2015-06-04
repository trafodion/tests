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
    # AUTOABORT syntax test with legal value
    # SET TRANSACTION ... AUTOABORT [ timeout | 0 | RESET ]
    #   timeout is integer {HOUR[S] | MINUTE[S] | SECOND[S]}
    
    stmt = """showtransaction;"""
    output = _dci.cmdexec(stmt)
    
    # t01.1: -1 seconds
    stmt = """SET TRANSACTION AUTOABORT RESET;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t01.2:
    stmt = """SHOWTRANSACTION;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _dci = _testmgr.get_dci_proc('mymxci')
    stmt = """env;"""
    output = _dci.cmdexec(stmt)
    
    # t01.4: 20 seconds
    stmt = """SET TRANSACTION AUTOABORT 000020 SECONDS;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """SHOWTRANSACTION;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t01.5: 7200 seconds
    stmt = """SET TRANSACTION AUTOABORT 00002 HOUR;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """SHOWTRANSACTION;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t01.6: 420000 seconds
    stmt = """SET TRANSACTION AUTOABORT 07000 MINUTES;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """SHOWTRANSACTION;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t01.7: minimum allowed timeout interval
    stmt = """SET TRANSACTION AUTOABORT 20 SECONDS;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """SHOWTRANSACTION;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t01.8:
    stmt = """SET TRANSACTION AUTOABORT 21 SECOND;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """SHOWTRANSACTION;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t01.9: maximum allowed timeout interval for seconds
    stmt = """SET TRANSACTION AUTOABORT 21474836 SECOND;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """SHOWTRANSACTION;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t01.10:
    stmt = """SET TRANSACTION AUTOABORT 21474835 SECONDS;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """SHOWTRANSACTION;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t01.11: 60 seconds
    stmt = """SET TRANSACTION AUTOABORT 1 minute;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """SHOWTRANSACTION;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t01.12: 21474780 seconds
    stmt = """SET TRANSACTION AUTOABORT 357913 minutes;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """SHOWTRANSACTION;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t01.13: 21474720 seconds
    stmt = """SET TRANSACTION AUTOABORT 357912 minute;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """SHOWTRANSACTION;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t01.14: 1140 seconds
    stmt = """SET TRANSACTION AUTOABORT 19 minute;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """SHOWTRANSACTION;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t01.15: 21474000 seconds
    stmt = """SET TRANSACTION AUTOABORT 5965 hours;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """SHOWTRANSACTION;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t01.16: 21470400 seconds
    stmt = """SET TRANSACTION AUTOABORT 5964 hour;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """SHOWTRANSACTION;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t01.17:
    stmt = """SET TRANSACTION AUTOABORT 0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """SHOWTRANSACTION;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t01.18:  68400 seconds
    stmt = """SET TRANSACTION AUTOABORT 19 hours;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """SHOWTRANSACTION;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t01.19: 0 seconds
    stmt = """SET TRANSACTION AUTOABORT 00000;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """SHOWTRANSACTION;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t01.20: -1 seconds
    stmt = """SET TRANSACTION AUTOABORT RESET;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """SHOWTRANSACTION;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _dci = _testmgr.get_default_dci_proc()
    
    # t01.21:
    stmt = """SHOWTRANSACTION;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

